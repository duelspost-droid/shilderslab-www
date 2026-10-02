#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# 덤프를 새 서버에 적재한다.  (SPEC 7항 4단계)
#   bash scripts/import-to-server.sh export/
#
# · public 8개 테이블은 **덤프가 정본**이다 — 비우고 덤프로 채운다(init 시드는 덮인다).
# · 트리거를 끈 세션(session_replication_role=replica)에서 넣는다.
#   켜 둔 채 넣으면 sl_content 의 수정 시각이 지금으로 덮이고 감사 로그에 가짜 행이 쌓인다.
# · 로그인 계정은 id 를 보존한다 — sl_admins.user_id 가 이 값을 가리킨다.
# · 전체를 한 트랜잭션으로 넣는다. 중간에 실패하면 아무것도 바뀌지 않는다.
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
SRC="${1:?덤프 디렉터리를 지정하세요 (예: export/)}"
cd "$(dirname "$0")/.."
for f in public-data.sql auth-users.csv auth-identities.csv; do
  [ -f "$SRC/$f" ] || { echo "✗ $SRC/$f 가 없습니다"; exit 1; }
done
PSQL="docker compose exec -T db psql -v ON_ERROR_STOP=1 -U postgres -d postgres -q"

echo "⚠ public 테이블 8개를 비우고 덤프로 다시 채웁니다. 계속하려면 yes:"
read -r ans; [ "$ans" = "yes" ] || { echo "중단"; exit 1; }

{
  echo "begin;"
  echo "set session_replication_role = replica;"
  echo "truncate public.sl_admins, public.sl_inquiries, public.sl_applications, public.sl_audit,"
  echo "         public.sl_content, public.sl_insights, public.sl_jobs, public.sl_settings;"
  # 로그인 계정 — 임시 테이블을 거쳐 upsert (이미 만든 부트스트랩 계정과 충돌해도 덤프가 이긴다)
  echo "create temp table _u (like auth.users including defaults) on commit drop;"
  echo "\\copy _u (id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at) from stdin with csv header"
  cat "$SRC/auth-users.csv"
  echo "\\."
  echo "insert into auth.users (id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at)
        select id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at from _u
        on conflict (id) do update set encrypted_password=excluded.encrypted_password,
          email=excluded.email, email_confirmed_at=excluded.email_confirmed_at, updated_at=excluded.updated_at;"
  echo "create temp table _i (like auth.identities including defaults) on commit drop;"
  echo "\\copy _i (id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at) from stdin with csv header"
  cat "$SRC/auth-identities.csv"
  echo "\\."
  echo "insert into auth.identities (id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at)
        select id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at from _i
        on conflict do nothing;"
  cat "$SRC/public-data.sql" | grep -vE '^(SET|SELECT pg_catalog\.set_config)'
  echo "commit;"
} | $PSQL

$PSQL -c "notify pgrst, 'reload schema';"
echo
echo "── 적재 결과 ──"
$PSQL -tA <<'EOSQL'
select '  문의          ' || count(*) from public.sl_inquiries
union all select '  지원          ' || count(*) from public.sl_applications
union all select '  관리자(연결)  ' || count(*) from public.sl_admins where user_id is not null
union all select '  로그인 계정   ' || count(*) from auth.users
union all select '  ⚠ 연결 끊긴 관리자 ' || count(*) from public.sl_admins a
            where a.user_id is not null and not exists (select 1 from auth.users u where u.id=a.user_id);
EOSQL
echo "  (마지막 줄이 0 이 아니면 관리자 결속이 깨진 것이다 — 그 관리자는 로그인해도 권한이 없다)"
