-- ════════════════════════════════════════════════════════════════════════════
-- 0006_shilderslab_admin_password.sql — 관리자가 다른 관리자의 비밀번호를 재설정
--
--   ── 왜 필요한가 ──────────────────────────────────────────────────────
--   담당자가 비밀번호를 잊으면 지금은 길이 두 개뿐이다.
--     ① 재설정 메일 — 이 프로젝트는 커스텀 SMTP 가 꺼져 있어 시간당 2통이고,
--        shilderslab.com 에는 MX 가 없어 회사 주소로는 아예 받지 못한다.
--     ② Supabase 대시보드 — 오너만 들어간다.
--   그래서 콘솔에서 admin 이 임시 비밀번호를 발급할 수 있게 한다.
--
--   ── 설계 원칙 (0004 를 그대로 따른다) ────────────────────────────────
--   실제 비밀번호 변경에는 service_role 키가 필요하고, 그 키는 Edge Function 에만 있다.
--   그러나 **누구의 비밀번호를 바꿔도 되는지는 DB 가 판정한다.** Edge 는 스스로 판단하지 않는다.
--   이 Supabase 프로젝트는 다른 서비스와 공유되므로, 우리 화이트리스트(sl_admins) 밖의
--   계정이 이 경로로 건드려지는 일은 **절대** 없어야 한다.
--
--   ── 삭제용 sl_admin_login_uid 를 재사용하지 않는 이유 ─────────────────
--   그 함수는 "마지막 admin" 을 거부한다. 삭제에서는 락아웃을 막는 옳은 가드지만,
--   비밀번호 재설정에는 틀렸다 — 재설정은 계정을 없애지 않으므로 락아웃을 만들지 않고,
--   오히려 **관리자가 한 명뿐인 상황이야말로 재설정이 가장 필요한 때**다.
--   그 가드를 물려받으면 정확히 필요한 순간에 막힌다. 그래서 함수를 따로 둔다.
--
--   ── 🚨 화이트리스트만으로는 경계가 되지 않는다 (적대적 검토에서 발견) ──
--   sl_admins 는 **admin 이 임의의 이메일로 채울 수 있는 목록**이다. 그래서
--     ① admin 이 공유 프로젝트에 있는 남의 서비스 사용자 이메일을 sl_admin_add 로 넣고
--     ② sl_admin_link 로 그 사람의 기존 auth 계정을 결속한 뒤
--     ③ 비밀번호를 재설정한다
--   이 3단계로 **남의 계정을 탈취**할 수 있다. 화이트리스트 소속만 확인하면 이 경로가 열린다.
--   (재설정 기능이 없던 때는 ①②가 "우리 콘솔 접근 허용" 에 그쳤다. 재설정이 생기면서
--    같은 동작의 의미가 완전히 달라졌다.)
--
--   → 그래서 경계를 하나 더 둔다: **이 사이트가 만든 로그인 계정만** 재설정 대상이다.
--     sl_admins.pw_managed 가 true 인 행만 허용한다. 이 값은
--       · 콘솔에서 계정을 새로 만들 때(sl_admin_mark_pw_managed) 켜지고
--       · sl_admin_link 로 **기존 계정을 갖다 붙일 때는 켜지지 않는다**
--     즉 남의 계정을 끌어와도 재설정 대상이 되지 않는다.
--
--   재실행 안전(idempotent). 0004 적용 이후에 실행할 것.
-- ════════════════════════════════════════════════════════════════════════════

-- ═══════════════ 0) 경계 컬럼 — 우리가 만든 계정인가 ═══════════════
alter table public.sl_admins add column if not exists pw_managed boolean not null default false;

comment on column public.sl_admins.pw_managed is
  '이 사이트가 로그인 계정을 직접 만들었는가. true 인 행만 콘솔에서 비밀번호를 재설정할 수 있다. '
  '기존 계정을 sl_admin_link 로 갖다 붙인 경우는 false 로 남아야 한다(남의 계정 탈취 방지).';

-- 백필: 지금 목록에 있는 계정은 전부 우리가 세운 관리자다(오너가 직접 관리해 온 목록).
-- ⚠ 이 백필은 **최초 1회만** 의미가 있다. 이후 추가되는 행은 위 규칙을 따른다.
--   재실행해도 이미 false 로 되돌린 행을 다시 켜지 않도록 조건을 건다.
do $$
begin
  if not exists (select 1 from public.sl_admins where pw_managed) then
    update public.sl_admins set pw_managed = true where user_id is not null;
  end if;
end $$;

-- 콘솔이 로그인 계정을 **새로 만들었을 때만** 호출한다(Edge 의 create 경로).
create or replace function public.sl_admin_mark_pw_managed(p_email text)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  update public.sl_admins set pw_managed = true
   where lower(email) = lower(trim(coalesce(p_email, '')));
end $$;

-- 콘솔이 [비밀번호 재설정] 버튼을 어디에 붙일지 알아야 하므로 목록에 pw_managed 를 얹는다.
-- (0004 의 sl_admin_list 를 그대로 두고 필드만 하나 늘린 판이다. 나머지는 동일.)
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
      'pw_managed', coalesce(a.pw_managed, false),-- 이 사이트가 만든 계정인가
      'last_sign_in_at', u.last_sign_in_at,
      'is_self', (a.user_id is not null and a.user_id = auth.uid())
    ) as t
    from public.sl_admins a
    left join auth.users u on u.id = a.user_id
  ) s;
  return v;
end $$;

-- ═══════════════ 1) 대상 판정 — 이 uid 의 비밀번호만 바꿔도 된다 ═══════════════
--
-- 반환 규칙
--   uuid      → 이 계정에 한해 재설정을 허용한다
--   null      → 우리 관리자 목록에 없는 이메일이다(공유 프로젝트의 남의 계정 포함).
--               Edge 는 여기서 반드시 멈춘다.
--   exception → 목록에는 있으나 재설정할 수 없는 상태다(사유를 한국어로 알린다)
create or replace function public.sl_admin_pw_uid(p_email text)
returns uuid language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text; v_found boolean; v_uid uuid; v_managed boolean;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;

  v_email := lower(trim(coalesce(p_email, '')));

  -- 반드시 우리 화이트리스트에 등록된 이메일이어야 한다.
  select true, a.user_id, a.pw_managed into v_found, v_uid, v_managed
    from public.sl_admins a where lower(a.email) = v_email;
  if v_found is null then
    return null;
  end if;

  if v_uid is null then
    raise exception '이 이메일에는 로그인 계정이 없습니다. 먼저 계정을 만들거나 연결하세요.'
      using errcode = '02000';
  end if;

  -- 🚨 핵심 경계. 화이트리스트 소속만으로는 부족하다(헤더 설명 참조).
  --   기존에 있던 계정을 [연결]로 갖다 붙인 행은 여기서 막힌다 —
  --   그 계정은 우리 것이 아니고, 비밀번호를 바꾸는 것은 탈취다.
  if not coalesce(v_managed, false) then
    raise exception
      '이 사이트가 만든 계정이 아닙니다. 기존 계정을 연결한 경우에는 비밀번호를 바꿀 수 없습니다 — 계정 소유자가 직접 재설정해야 합니다.'
      using errcode = '42501';
  end if;

  -- 자기 비밀번호는 이 경로로 바꾸지 않는다. 콘솔 우측 상단 [비밀번호 변경] 이
  -- Supabase 의 재인증 정책을 그대로 거치는 정식 경로다.
  if v_uid = auth.uid() then
    raise exception '자신의 비밀번호는 우측 상단 [비밀번호 변경] 에서 바꾸세요.'
      using errcode = '42501';
  end if;

  -- ⚠ 여기서 감사 로그를 남기지 않는다. 이 시점엔 아직 아무것도 바뀌지 않았다.
  --   실제로 바뀐 뒤 Edge 가 sl_admin_pw_logged() 를 호출한다.
  return v_uid;
end $$;

-- ═══════════════ 2) 사후 기록 — 실제로 바뀐 뒤에만 남는다 ═══════════════
create or replace function public.sl_admin_pw_logged(p_email text)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
declare v_email text;
begin
  if not public.is_sl_owner() then
    raise exception '계정 관리는 admin 역할만 가능합니다.' using errcode = '42501';
  end if;
  v_email := lower(trim(coalesce(p_email, '')));

  -- 비밀번호 값은 어떤 형태로도 남기지 않는다(길이·해시 포함).
  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id,
                              detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', 'admin_password_reset',
          'auth.users', v_email, jsonb_build_object('via', 'console'),
          public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ─────────────── 실행 권한 ───────────────
revoke all on function public.sl_admin_pw_uid(text)     from public, anon;
grant  execute on function public.sl_admin_pw_uid(text) to authenticated;
revoke all on function public.sl_admin_pw_logged(text)     from public, anon;
grant  execute on function public.sl_admin_pw_logged(text) to authenticated;
revoke all on function public.sl_admin_mark_pw_managed(text)     from public, anon;
grant  execute on function public.sl_admin_mark_pw_managed(text) to authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 적용 후 확인
--
--   -- ① 함수가 생겼는지
--   select proname from pg_proc
--    where proname in ('sl_admin_pw_uid','sl_admin_pw_logged','sl_admin_mark_pw_managed');  -- 3행
--
--   -- ② anon 은 실행할 수 없어야 한다 (false 두 개)
--   select has_function_privilege('anon', 'public.sl_admin_pw_uid(text)', 'execute'),
--          has_function_privilege('anon', 'public.sl_admin_pw_logged(text)', 'execute');
--
--   -- ③ 화이트리스트 밖 이메일은 null 이어야 한다(관리자로 로그인한 세션에서)
--   select public.sl_admin_pw_uid('someone-else@example.com');    -- null
--
--   -- ④ 경계 컬럼이 붙었는지. 지금 목록은 전부 true 여야 하고,
--   --    앞으로 [연결]로 붙인 행은 false 로 남아야 한다.
--   select email, (user_id is not null) as linked, pw_managed from public.sl_admins order by created_at;
-- ════════════════════════════════════════════════════════════════════════════
