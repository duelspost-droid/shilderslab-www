-- ═══════════════════════════════════════════════════════════════════════════
-- 01 · 롤 · auth 스키마 부트스트랩  (관리형 Supabase 가 대신 해 주던 일)
--
-- 왜 이 파일이 먼저인가
--   `supabase/migrations/*.sql` 은 `auth.uid()` 16회 · `auth.jwt()` 9회 ·
--   `auth.users` 8회를 쓰고, 정책을 `anon`/`authenticated` 롤에 건다.
--   관리형 Supabase 에는 이것들이 이미 있지만 **맨 Postgres 에는 없다.**
--   이 파일이 그 공백을 메운다. 없으면 0001 적용이 즉시 실패한다.
--
-- 적용 순서
--   01-roles-auth.sql  →  (GoTrue 가 auth.users 를 만든다)  →  02-schema.sql  →  03-seed
--   ⚠ GoTrue 를 먼저 한 번 띄워 auth.users 가 생긴 뒤에 02 를 적용한다.
--     0004 가 auth.users 를 조인하므로 테이블이 없으면 함수 생성에서 막힌다.
--
-- 멱등: 전부 재실행 안전.
-- ═══════════════════════════════════════════════════════════════════════════

-- 확장 불필요: gen_random_uuid() 는 PostgreSQL 13+ 코어 내장이고, 마이그레이션은 pgcrypto 전용
-- 함수(crypt·digest 등)를 쓰지 않는다(실측 0회). contrib 패키지가 없는 최소 설치에서도 동작해야 하므로
-- 여기서 확장을 만들지 않는다. (test-db.py 가 pgcrypto 없는 PostgreSQL 에서 이 결함을 잡았다.)

-- ─────────────────────────────────────────────────────────────────────────
-- 1) 롤
--    PostgREST 는 `authenticator` 로 접속해, JWT 의 role 클레임을 보고
--    anon / authenticated / service_role 로 SET ROLE 한다.
--    그래서 authenticator 만 LOGIN 이고 나머지는 NOLOGIN 이다.
-- ─────────────────────────────────────────────────────────────────────────
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'anon') then
    create role anon nologin noinherit;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticated') then
    create role authenticated nologin noinherit;
  end if;
  -- service_role 은 RLS 를 우회한다. Edge/서버 전용이며 브라우저에 절대 두지 않는다.
  if not exists (select 1 from pg_roles where rolname = 'service_role') then
    create role service_role nologin noinherit bypassrls;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticator') then
    -- 비밀번호는 아래 ALTER 에서 .env 값으로 바꾼다(여기서는 만들기만).
    create role authenticator login noinherit password 'postgres';
  end if;
  -- GoTrue 전용 롤. auth 스키마의 소유자가 된다.
  if not exists (select 1 from pg_roles where rolname = 'supabase_auth_admin') then
    create role supabase_auth_admin login noinherit createrole password 'postgres';
  end if;
end$$;

grant anon, authenticated, service_role to authenticator;

-- ─────────────────────────────────────────────────────────────────────────
-- 2) auth 스키마 — GoTrue 가 여기에 users 테이블을 만든다
-- ─────────────────────────────────────────────────────────────────────────
create schema if not exists auth authorization supabase_auth_admin;
grant usage on schema auth to anon, authenticated, service_role;

-- ─────────────────────────────────────────────────────────────────────────
-- 3) auth.uid() / auth.jwt() / auth.role() / auth.email()
--    PostgREST 가 요청마다 `request.jwt.claims` 에 JWT 페이로드를 넣어 준다.
--    이 헬퍼들이 그 값을 읽는다. **RLS 정책 전체가 이 두 함수에 걸려 있다.**
--    ⚠ current_setting 의 두 번째 인자 true = 설정이 없으면 NULL(에러 아님).
--      이게 빠지면 비로그인 요청에서 함수가 터져 anon 경로가 전부 500 이 된다.
-- ─────────────────────────────────────────────────────────────────────────
-- 🚨 두 가지 설정값을 모두 읽는다.
--   PostgREST 12(PGRST_DB_USE_LEGACY_GUCS=false)는 `request.jwt.claims`(JSON 한 덩어리)만 넣는다.
--   반면 GoTrue 는 첫 기동 때 자기 마이그레이션으로 이 함수들을 **옛 방식**
--   (`request.jwt.claim.sub` 처럼 클레임마다 따로)으로 덮어쓸 수 있다.
--   그 상태가 되면 auth.uid() 가 항상 NULL → RLS 21개가 관리자를 못 알아본다(에러 없이 조용히).
--   그래서 둘 다 읽게 짜고, scripts/init-db.sh 가 GoTrue 기동 **후에** 이 파일을 다시 적용한다.
create or replace function auth.jwt() returns jsonb
language sql stable
as $$
  select coalesce(
    nullif(current_setting('request.jwt.claims', true), '')::jsonb,
    '{}'::jsonb
  );
$$;

create or replace function auth.uid() returns uuid
language sql stable
as $$
  select nullif(coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    auth.jwt() ->> 'sub'
  ), '')::uuid;
$$;

create or replace function auth.role() returns text
language sql stable
as $$
  select nullif(coalesce(
    nullif(current_setting('request.jwt.claim.role', true), ''),
    auth.jwt() ->> 'role'
  ), '');
$$;

create or replace function auth.email() returns text
language sql stable
as $$
  select nullif(coalesce(
    nullif(current_setting('request.jwt.claim.email', true), ''),
    auth.jwt() ->> 'email'
  ), '');
$$;

-- GoTrue(supabase_auth_admin)가 같은 이름을 다시 만들 때 소유권 충돌로 막히지 않게 넘겨 둔다.
alter function auth.jwt()   owner to supabase_auth_admin;
alter function auth.uid()   owner to supabase_auth_admin;
alter function auth.role()  owner to supabase_auth_admin;
alter function auth.email() owner to supabase_auth_admin;

grant execute on function auth.jwt(), auth.uid(), auth.role(), auth.email()
  to anon, authenticated, service_role;

-- ─────────────────────────────────────────────────────────────────────────
-- 4) public 스키마 기본 권한
--    0001~0007 이 테이블마다 명시적으로 grant 하지만, 스키마 usage 는 여기서 준다.
-- ─────────────────────────────────────────────────────────────────────────
grant usage on schema public to anon, authenticated, service_role;

-- 🚨 관리형 Supabase 의 **기본 권한을 그대로 재현한다.** (이것이 빠지면 사이트가 빈 화면이 된다)
--   Supabase 는 public 스키마의 모든 테이블·함수에 anon·authenticated·service_role 권한을
--   기본으로 주고, **실제 차단은 RLS 가 한다.** 마이그레이션 0001~0007 은 테이블 grant 를
--   한 줄도 하지 않고 이 기본 권한 위에서 RLS 정책만 건다(실측: 테이블 grant 문 0건).
--   맨 PostgreSQL 에는 이 기본값이 없어서, 빠뜨리면 anon 이 공개 문구조차 못 읽고
--   관리자도 문의를 못 본다 — test-db.py 가 `permission denied for table sl_content` 로 잡았다.
--
--   ⚠ 예전 이 자리의 주석은 "기본 권한을 열지 않는다, 마이그레이션이 테이블마다 명시 grant 한다" 였다.
--     **사실이 아니었다.** 보안은 grant 가 아니라 RLS(8개 테이블 전부 활성)와 민감 함수의
--     명시 revoke(0003·0004)가 맡는다. 개인정보 테이블은 INSERT 정책이 없어 RLS 가 직접 쓰기를 막는다.
grant all on all tables    in schema public to anon, authenticated, service_role;
grant all on all functions in schema public to anon, authenticated, service_role;
grant all on all sequences in schema public to anon, authenticated, service_role;
-- 이후 마이그레이션이 만드는 객체에도 같은 기본값이 붙게 한다(0001~0007 은 postgres 로 실행된다).
alter default privileges for role postgres in schema public
  grant all on tables    to anon, authenticated, service_role;
alter default privileges for role postgres in schema public
  grant all on functions to anon, authenticated, service_role;
alter default privileges for role postgres in schema public
  grant all on sequences to anon, authenticated, service_role;
-- 민감 함수(보존기간 파기·IP 조회 등)는 마이그레이션이 생성 직후 명시적으로 revoke 한다.
-- 순서가 '기본 grant → 생성 → revoke' 라서 그 revoke 가 마지막에 이긴다(관리형과 같은 결과).
