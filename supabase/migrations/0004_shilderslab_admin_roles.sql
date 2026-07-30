-- ════════════════════════════════════════════════════════════════════════════
-- 0004_shilderslab_admin_roles.sql — 관리자 계정 관리 + 역할 분리
--
--   목적
--     · 관리자 콘솔에서 관리자 목록을 보고 추가·역할변경·삭제할 수 있게 한다.
--     · 역할을 admin / editor 로 분리한다.
--         admin  : 콘텐츠 + 계정 관리 + 설정 + 로그 열람
--         editor : 콘텐츠(인사이트·채용) + 문의·지원 처리. 계정 관리·설정은 불가.
--     · sl_admins 는 여전히 쓰기 정책이 없다. 모든 변경은 아래 SECURITY DEFINER RPC로만 일어나고
--       전부 감사 로그에 남는다.
--
--   락아웃 방지 가드 (중요)
--     · 자기 자신을 삭제할 수 없다.
--     · 자기 자신을 editor 로 강등할 수 없다(다른 admin 이 하도록).
--     · 마지막 남은 admin 은 삭제·강등할 수 없다.
--
--   ⚠ 공유 프로젝트 주의
--     이 프로젝트에는 다른 서비스의 로그인 사용자가 있다. 화이트리스트에 이메일을 추가하는 행위는
--     "그 사람이 이 사이트의 관리자가 된다"는 뜻이므로 admin 역할만 수행할 수 있게 제한한다.
--
--   재실행 안전(idempotent). 0001 적용 이후에 실행할 것.
-- ════════════════════════════════════════════════════════════════════════════

-- ─────────────── 역할 조회 ───────────────
-- 현재 요청자의 역할('admin' | 'editor' | null). RLS 우회를 위해 definer.
create or replace function public.sl_my_role()
returns text language sql stable security definer set search_path = public as $$
  select a.role from public.sl_admins a
   where lower(a.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
   limit 1;
$$;

-- 현재 요청자의 이메일(Edge 함수가 "자기 계정 삭제 금지"를 판단할 때 사용)
create or replace function public.sl_my_email()
returns text language sql stable as $$
  select lower(coalesce(auth.jwt() ->> 'email', ''));
$$;

-- admin 역할 여부(계정 관리·설정 게이트)
create or replace function public.is_sl_owner()
returns boolean language sql stable security definer set search_path = public as $$
  select coalesce(public.sl_my_role() = 'admin', false);
$$;

revoke all on function public.sl_my_role()  from public, anon;
grant  execute on function public.sl_my_role()  to authenticated;
revoke all on function public.sl_my_email()     from public, anon;
grant  execute on function public.sl_my_email() to authenticated;
revoke all on function public.is_sl_owner()     from public, anon;
grant  execute on function public.is_sl_owner() to authenticated;

-- ─────────────── 설정 쓰기는 admin 만 ───────────────
-- (0001 에서는 is_sl_admin 이었다. editor 가 사이트 설정을 바꾸지 못하게 좁힌다.)
drop policy if exists sl_settings_write on public.sl_settings;
create policy sl_settings_write on public.sl_settings for all to authenticated
  using (public.is_sl_owner()) with check (public.is_sl_owner());

-- ════════════════════════════════════════════════════════════════════════════
-- 관리자 목록 조회 — 로그인 계정 존재 여부까지 함께 준다.
--   "화이트리스트에는 있는데 로그인 계정이 없어서 못 들어오는" 상태를 콘솔에서 바로 보이게 한다.
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_admin_list()
returns jsonb language plpgsql security definer set search_path = public as $$
declare v jsonb;
begin
  if not public.is_sl_admin() then
    raise exception '관리자만 조회할 수 있습니다.' using errcode = '42501';
  end if;
  select coalesce(jsonb_agg(t order by t->>'created_at'), '[]'::jsonb) into v
  from (
    select jsonb_build_object(
      'email', a.email,
      'role', a.role,
      'note', coalesce(a.note, ''),
      'created_at', a.created_at,
      'has_login', (u.id is not null),
      'last_sign_in_at', u.last_sign_in_at,
      'is_self', lower(a.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
    ) as t
    from public.sl_admins a
    left join auth.users u on lower(u.email) = lower(a.email)
  ) s;
  return v;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 관리자 추가 — 화이트리스트에만 등록한다(로그인 계정 생성은 별도).
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_admin_add(
  p_email text, p_role text default 'editor', p_note text default ''
) returns jsonb
language plpgsql security definer set search_path = public as $$
declare v_email text; v_has_login boolean;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  v_email := lower(trim(coalesce(p_email, '')));
  if v_email !~ '^[^@[:space:]]+@[^@[:space:].]+\.[^@[:space:]]+$' then
    raise exception '이메일 형식이 올바르지 않습니다.' using errcode = '22023';
  end if;
  if char_length(v_email) > 160 or char_length(coalesce(p_note, '')) > 200 then
    raise exception '입력 길이가 허용 범위를 초과했습니다.' using errcode = '22023';
  end if;
  if coalesce(p_role, '') not in ('admin', 'editor') then
    raise exception '역할은 admin 또는 editor 만 가능합니다.' using errcode = '22023';
  end if;
  if exists (select 1 from public.sl_admins where lower(email) = v_email) then
    raise exception '이미 등록된 관리자입니다.' using errcode = '23505';
  end if;

  insert into public.sl_admins(email, role, note) values (v_email, p_role, nullif(trim(p_note), ''));

  select (u.id is not null) into v_has_login from auth.users u where lower(u.email) = v_email;
  v_has_login := coalesce(v_has_login, false);

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_add', 'sl_admins', v_email,
          jsonb_build_object('role', p_role, 'has_login', v_has_login),
          public._sl_client_ip(), public._sl_user_agent());

  return jsonb_build_object('email', v_email, 'role', p_role, 'has_login', v_has_login);
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 역할 변경 — 마지막 admin 강등 금지, 자기 강등 금지
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_admin_set_role(p_email text, p_role text)
returns void language plpgsql security definer set search_path = public as $$
declare v_email text; v_me text; v_cur text; v_admins int;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  v_email := lower(trim(coalesce(p_email, '')));
  v_me := lower(coalesce(auth.jwt() ->> 'email', ''));
  if coalesce(p_role, '') not in ('admin', 'editor') then
    raise exception '역할은 admin 또는 editor 만 가능합니다.' using errcode = '22023';
  end if;

  select role into v_cur from public.sl_admins where lower(email) = v_email;
  if v_cur is null then
    raise exception '등록되지 않은 관리자입니다.' using errcode = '02000';
  end if;
  if v_cur = p_role then return; end if;

  if v_email = v_me and p_role = 'editor' then
    raise exception '자신의 역할을 강등할 수 없습니다. 다른 admin 에게 요청하세요.' using errcode = '42501';
  end if;

  if v_cur = 'admin' and p_role = 'editor' then
    select count(*) into v_admins from public.sl_admins where role = 'admin';
    if v_admins <= 1 then
      raise exception '마지막 admin 은 강등할 수 없습니다.' using errcode = '42501';
    end if;
  end if;

  update public.sl_admins set role = p_role where lower(email) = v_email;

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_set_role', 'sl_admins', v_email,
          jsonb_build_object('from', v_cur, 'to', p_role),
          public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 관리자 삭제 — 자기 삭제 금지, 마지막 admin 삭제 금지
--   ※ 화이트리스트에서만 제거한다. Auth 로그인 계정은 그대로 남으므로,
--     계정까지 지우려면 아래 Edge 함수(sl-admin-user)를 쓰거나 대시보드에서 지운다.
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_admin_remove(p_email text)
returns void language plpgsql security definer set search_path = public as $$
declare v_email text; v_me text; v_cur text; v_admins int;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  v_email := lower(trim(coalesce(p_email, '')));
  v_me := lower(coalesce(auth.jwt() ->> 'email', ''));

  if v_email = v_me then
    raise exception '자신을 삭제할 수 없습니다.' using errcode = '42501';
  end if;

  select role into v_cur from public.sl_admins where lower(email) = v_email;
  if v_cur is null then
    raise exception '등록되지 않은 관리자입니다.' using errcode = '02000';
  end if;

  if v_cur = 'admin' then
    select count(*) into v_admins from public.sl_admins where role = 'admin';
    if v_admins <= 1 then
      raise exception '마지막 admin 은 삭제할 수 없습니다.' using errcode = '42501';
    end if;
  end if;

  delete from public.sl_admins where lower(email) = v_email;

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_remove', 'sl_admins', v_email,
          jsonb_build_object('role', v_cur), public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ─────────────── 실행 권한 ───────────────
revoke all on function public.sl_admin_list()                      from public, anon;
grant  execute on function public.sl_admin_list()                  to authenticated;
revoke all on function public.sl_admin_add(text,text,text)         from public, anon;
grant  execute on function public.sl_admin_add(text,text,text)     to authenticated;
revoke all on function public.sl_admin_set_role(text,text)         from public, anon;
grant  execute on function public.sl_admin_set_role(text,text)     to authenticated;
revoke all on function public.sl_admin_remove(text)                from public, anon;
grant  execute on function public.sl_admin_remove(text)            to authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 검증
--   select public.sl_my_role();            -- 로그인 계정의 역할
--   select public.is_sl_owner();            -- admin 이면 true
--   select public.sl_admin_list();          -- 목록(로그인 계정 존재 여부 포함)
--   -- anon 으로는 전부 permission denied 여야 한다.
-- ════════════════════════════════════════════════════════════════════════════
