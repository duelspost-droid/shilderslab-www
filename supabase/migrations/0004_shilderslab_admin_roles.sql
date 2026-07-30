-- ════════════════════════════════════════════════════════════════════════════
-- 0004_shilderslab_admin_roles.sql — 관리자 계정 관리 + 역할 분리 + 권한 결속 강화
--
--   ⚠ 이 파일은 0001 의 권한 판정 방식을 **교체**한다. 반드시 전문을 실행할 것.
--
--   ── 왜 교체하는가 (적대적 검토 결과) ─────────────────────────────────
--   0001 의 is_sl_admin() 은 `auth.jwt() ->> 'email'` 문자열이 sl_admins.email 과
--   같은지만 봤다. 이 프로젝트는 다른 서비스와 공유되고 셀프 가입이 열려 있을 수 있으므로,
--   **로그인 계정이 아직 없는 화이트리스트 행("빈 관리자 슬롯")이 있으면
--   제3자가 그 주소로 가입해 관리자가 될 수 있다.**
--   → 권한 판정을 이메일 문자열이 아니라 불변 식별자 auth.users.id 에 결속한다.
--     user_id 가 연결되지 않은 행은 어떤 권한도 갖지 못한다(빈 슬롯이 무해해진다).
--
--   ── 이 파일이 하는 일 ────────────────────────────────────────────────
--   1) sl_admins.user_id 추가 + 기존 행 백필 + 유일성 제약(대소문자 무관 이메일, user_id)
--   2) is_sl_admin() / sl_my_role() 을 user_id 기준으로 교체
--   3) 역할 분리: admin(계정·설정·로그) / editor(콘텐츠·문의 처리)
--   4) 계정 관리 RPC — 추가·연결·역할변경·삭제. 전건 감사 로그.
--   5) 락아웃 방지: 자기 삭제/강등 금지, **로그인 가능한 마지막 admin** 삭제·강등 금지,
--      동시 실행 경합 방지(advisory lock)
--   6) 관리자 명단·감사 로그 열람을 admin(owner) 으로 좁힘
--
--   재실행 안전(idempotent). 0001 적용 이후에 실행할 것.
-- ════════════════════════════════════════════════════════════════════════════

-- ═══════════════ 1) 스키마 — 불변 식별자 결속 ═══════════════
alter table public.sl_admins add column if not exists user_id uuid;

-- 기존 행 백필: 확인된(email_confirmed_at) 계정만 연결한다.
update public.sl_admins a
   set user_id = u.id
  from auth.users u
 where lower(u.email) = lower(a.email)
   and u.email_confirmed_at is not null
   and a.user_id is null;

create unique index if not exists sl_admins_user_id_key
  on public.sl_admins(user_id) where user_id is not null;
create unique index if not exists sl_admins_email_lower_key
  on public.sl_admins(lower(email));

-- 수동 INSERT 가 실수로 최고 권한을 만들지 않게 기본값을 editor 로 낮춘다.
alter table public.sl_admins alter column role set default 'editor';

-- ═══════════════ 2) 권한 판정 — user_id 기준 ═══════════════
create or replace function public.sl_my_role()
returns text language sql stable security definer set search_path = public, pg_temp as $$
  select a.role from public.sl_admins a
   where a.user_id is not null and a.user_id = auth.uid()
   order by a.created_at
   limit 1;
$$;

-- 0001 의 이메일 기반 판정을 대체한다(이 교체가 이 마이그레이션의 핵심).
create or replace function public.is_sl_admin()
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select public.sl_my_role() is not null;
$$;

create or replace function public.is_sl_owner()
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select coalesce(public.sl_my_role() = 'admin', false);
$$;

create or replace function public.sl_my_email()
returns text language sql stable set search_path = public, pg_temp as $$
  select lower(coalesce(auth.jwt() ->> 'email', ''));
$$;

revoke all on function public.sl_my_role()      from public, anon;
grant  execute on function public.sl_my_role()  to authenticated;
revoke all on function public.is_sl_admin()     from public, anon;
grant  execute on function public.is_sl_admin() to authenticated;
revoke all on function public.is_sl_owner()     from public, anon;
grant  execute on function public.is_sl_owner() to authenticated;
revoke all on function public.sl_my_email()     from public, anon;
grant  execute on function public.sl_my_email() to authenticated;

-- ═══════════════ 3) 열람·쓰기 게이트 조정 ═══════════════
-- 관리자 명단은 admin 만 본다(editor 는 동료의 이메일·최근 로그인 시각을 볼 이유가 없다).
drop policy if exists sl_admins_read on public.sl_admins;
create policy sl_admins_read on public.sl_admins for select to authenticated
  using (public.is_sl_owner());

-- 사이트 설정 쓰기는 admin 만.
drop policy if exists sl_settings_write on public.sl_settings;
create policy sl_settings_write on public.sl_settings for all to authenticated
  using (public.is_sl_owner()) with check (public.is_sl_owner());

-- 감사·방문 로그는 admin 만(방문자 IP·관리자 행위 이력이 들어 있다).
drop policy if exists sl_audit_admin_read on public.sl_audit;
create policy sl_audit_admin_read on public.sl_audit for select to authenticated
  using (public.is_sl_owner());

-- ═══════════════ 4) 내부 헬퍼 ═══════════════
-- 로그인 가능한(=user_id 연결된) admin 수. 락아웃 판정의 유일한 기준.
create or replace function public._sl_active_owners()
returns int language sql stable security definer set search_path = public, pg_temp as $$
  select count(*)::int from public.sl_admins
   where role = 'admin' and user_id is not null;
$$;
revoke all on function public._sl_active_owners() from public, anon, authenticated;

-- ═══════════════ 5) 관리자 목록 ═══════════════
create or replace function public.sl_admin_list()
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare v jsonb;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  select coalesce(jsonb_agg(t order by t->>'created_at'), '[]'::jsonb) into v
  from (
    select jsonb_build_object(
      'email', a.email,
      'role', a.role,
      'note', coalesce(a.note, ''),
      'created_at', a.created_at,
      'linked', (a.user_id is not null),          -- 권한이 실제로 붙어 있는가
      'last_sign_in_at', u.last_sign_in_at,
      'is_self', (a.user_id is not null and a.user_id = auth.uid())
    ) as t
    from public.sl_admins a
    left join auth.users u on u.id = a.user_id
  ) s;
  return v;
end $$;

-- ═══════════════ 6) 관리자 추가 ═══════════════
--   확인된 로그인 계정이 있어야 등록된다. "빈 슬롯"을 만들 수 없다.
create or replace function public.sl_admin_add(
  p_email text, p_role text default 'editor', p_note text default ''
) returns jsonb
language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_uid uuid;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  perform pg_advisory_xact_lock(hashtext('sl_admins'));

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

  select u.id into v_uid from auth.users u
   where lower(u.email) = v_email and u.email_confirmed_at is not null
   order by u.created_at limit 1;
  if v_uid is null then
    raise exception '확인된 로그인 계정이 없습니다. 계정을 먼저 생성한 뒤 관리자로 추가하세요.'
      using errcode = '02000';
  end if;

  insert into public.sl_admins(email, role, note, user_id)
  values (v_email, p_role, nullif(trim(p_note), ''), v_uid);

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_add', 'sl_admins', v_email,
          jsonb_build_object('role', p_role), public._sl_client_ip(), public._sl_user_agent());

  return jsonb_build_object('email', v_email, 'role', p_role, 'linked', true);
end $$;

-- ═══════════════ 7) 계정 연결 (백필 복구용) ═══════════════
--   0004 적용 전에 만들어진 "계정 없는 행"이나, 계정을 나중에 만든 경우를 연결한다.
create or replace function public.sl_admin_link(p_email text)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_uid uuid;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  perform pg_advisory_xact_lock(hashtext('sl_admins'));
  v_email := lower(trim(coalesce(p_email, '')));

  if not exists (select 1 from public.sl_admins where lower(email) = v_email) then
    raise exception '등록되지 않은 관리자입니다.' using errcode = '02000';
  end if;
  select u.id into v_uid from auth.users u
   where lower(u.email) = v_email and u.email_confirmed_at is not null
   order by u.created_at limit 1;
  if v_uid is null then
    raise exception '확인된 로그인 계정이 없습니다.' using errcode = '02000';
  end if;

  update public.sl_admins set user_id = v_uid where lower(email) = v_email;

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_link', 'sl_admins', v_email,
          jsonb_build_object('user_id', v_uid), public._sl_client_ip(), public._sl_user_agent());
  return jsonb_build_object('email', v_email, 'linked', true);
end $$;

-- ═══════════════ 8) 역할 변경 ═══════════════
create or replace function public.sl_admin_set_role(p_email text, p_role text)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_cur text; v_uid uuid;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  perform pg_advisory_xact_lock(hashtext('sl_admins'));   -- 동시 강등으로 admin 0명 방지

  v_email := lower(trim(coalesce(p_email, '')));
  if coalesce(p_role, '') not in ('admin', 'editor') then
    raise exception '역할은 admin 또는 editor 만 가능합니다.' using errcode = '22023';
  end if;

  select role, user_id into v_cur, v_uid from public.sl_admins where lower(email) = v_email;
  if v_cur is null then
    raise exception '등록되지 않은 관리자입니다.' using errcode = '02000';
  end if;
  if v_cur = p_role then return; end if;

  if v_uid is not null and v_uid = auth.uid() and p_role = 'editor' then
    raise exception '자신의 역할을 강등할 수 없습니다. 다른 admin 에게 요청하세요.' using errcode = '42501';
  end if;

  if v_cur = 'admin' and p_role = 'editor' and public._sl_active_owners() <= 1 then
    raise exception '로그인 가능한 admin 이 한 명뿐입니다. 강등할 수 없습니다.' using errcode = '42501';
  end if;

  update public.sl_admins set role = p_role where lower(email) = v_email;

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_set_role', 'sl_admins', v_email,
          jsonb_build_object('from', v_cur, 'to', p_role),
          public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ═══════════════ 9) 관리자 삭제 ═══════════════
--   화이트리스트에서만 제거한다. Auth 로그인 계정은 남으므로 오프보딩 시 별도 삭제가 필요하다.
create or replace function public.sl_admin_remove(p_email text)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_cur text; v_uid uuid;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  perform pg_advisory_xact_lock(hashtext('sl_admins'));

  v_email := lower(trim(coalesce(p_email, '')));
  select role, user_id into v_cur, v_uid from public.sl_admins where lower(email) = v_email;
  if v_cur is null then
    raise exception '등록되지 않은 관리자입니다.' using errcode = '02000';
  end if;
  if v_uid is not null and v_uid = auth.uid() then
    raise exception '자신을 삭제할 수 없습니다.' using errcode = '42501';
  end if;
  if v_cur = 'admin' and v_uid is not null and public._sl_active_owners() <= 1 then
    raise exception '로그인 가능한 admin 이 한 명뿐입니다. 삭제할 수 없습니다.' using errcode = '42501';
  end if;

  delete from public.sl_admins where lower(email) = v_email;

  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_remove', 'sl_admins', v_email,
          jsonb_build_object('role', v_cur, 'was_linked', (v_uid is not null)),
          public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ═══════════════ 10) Edge 함수 지원 — 삭제 대상 검증 ═══════════════
--   Edge 의 delete_login 이 공유 프로젝트의 임의 계정을 지우지 못하게, 대상 uid 를 DB 가 판정한다.
--   반환값이 null 이면 Edge 는 삭제를 거부해야 한다.
create or replace function public.sl_admin_login_uid(p_email text)
returns uuid language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_uid uuid;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  v_email := lower(trim(coalesce(p_email, '')));
  -- 반드시 우리 화이트리스트에 등록된 이메일이어야 한다.
  select a.user_id into v_uid from public.sl_admins a where lower(a.email) = v_email;
  if v_uid is null then
    return null;
  end if;
  if v_uid = auth.uid() then
    raise exception '자신의 로그인 계정은 삭제할 수 없습니다.' using errcode = '42501';
  end if;
  if exists (select 1 from public.sl_admins
              where user_id = v_uid and role = 'admin')
     and public._sl_active_owners() <= 1 then
    raise exception '로그인 가능한 admin 이 한 명뿐입니다.' using errcode = '42501';
  end if;
  return v_uid;
end $$;

-- ─────────────── 실행 권한 ───────────────
revoke all on function public.sl_admin_list()                      from public, anon;
grant  execute on function public.sl_admin_list()                  to authenticated;
revoke all on function public.sl_admin_add(text,text,text)         from public, anon;
grant  execute on function public.sl_admin_add(text,text,text)     to authenticated;
revoke all on function public.sl_admin_link(text)                  from public, anon;
grant  execute on function public.sl_admin_link(text)              to authenticated;
revoke all on function public.sl_admin_set_role(text,text)         from public, anon;
grant  execute on function public.sl_admin_set_role(text,text)     to authenticated;
revoke all on function public.sl_admin_remove(text)                from public, anon;
grant  execute on function public.sl_admin_remove(text)            to authenticated;
revoke all on function public.sl_admin_login_uid(text)             from public, anon;
grant  execute on function public.sl_admin_login_uid(text)         to authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 적용 후 확인
--
--   -- ① 백필 결과: linked=false 인 행은 권한이 없다(=빈 슬롯이 무해해진 상태)
--   select email, role, (user_id is not null) as linked from public.sl_admins order by created_at;
--
--   -- ② 로그인 가능한 admin 수. 0 이면 아래 복구 절차가 필요하다.
--   select count(*) from public.sl_admins where role='admin' and user_id is not null;
--
-- ⚠ 최초 관리자 부트스트랩 / admin 0명 복구
--    권한이 이메일이 아니라 계정(user_id)에 결속되므로, 첫 관리자는 반드시 이 경로로 세운다.
--    (앱 안에서 스스로 관리자가 되는 경로는 의도적으로 없다 — 그게 이 마이그레이션의 목적이다.)
--
--    ① Authentication → Users → Add user 로 계정을 만든다. **Auto Confirm User 를 켠다.**
--       (비밀번호 입력은 오너가 직접)
--    ② 아래 한 문장을 SQL Editor 에서 실행한다. 이메일만 바꾸면 된다. 재실행 안전.
--
--       insert into public.sl_admins (email, role, note, user_id)
--       select lower(u.email), 'admin', '최초 관리자', u.id
--         from auth.users u
--        where lower(u.email) = lower('여기에_관리자_이메일')
--          and u.email_confirmed_at is not null
--       on conflict (lower(email))
--       do update set user_id = excluded.user_id, role = 'admin';
--
--    ③ 확인: 아래가 1 이상이어야 콘솔에 들어갈 수 있다.
--       select count(*) from public.sl_admins where role='admin' and user_id is not null;
--
--    이후 관리자 추가·연결·삭제는 콘솔의 [계정 관리] 탭에서 하면 된다.
--
-- ⚠ 오너 확인 사항: Authentication → Providers → Email 의 'Confirm email' 을 켜 둘 것.
--    이 마이그레이션으로 이메일 선점 경로는 막혔지만, 확인 메일 절차는 유지하는 편이 안전하다.
-- ════════════════════════════════════════════════════════════════════════════
