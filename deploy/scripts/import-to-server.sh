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
# · 덤프는 둘 중 하나: export-from-supabase.sh(비밀번호 해시 포함) 또는
#   대시보드 export-private.sql + convert-dashboard-dump.py(해시 없음 → 적재 뒤 set-admin-password.sh).
#   해시가 비어 있으면 이미 있는 계정의 비밀번호는 지우지 않는다(coalesce).
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
SRC="${1:?덤프 디렉터리를 지정하세요 (예: export/)}"
cd "$(dirname "$0")/.."
for f in public-data.sql auth-users.csv auth-identities.csv; do
  [ -f "$SRC/$f" ] || { echo "✗ $SRC/$f 가 없습니다"; exit 1; }
done
# SL_PSQL 은 검증용(로컬 PostgreSQL 로 왕복 시험할 때)만 쓴다. 서버에서는 지정하지 않는다.
PSQL="${SL_PSQL:-docker compose exec -T db psql -v ON_ERROR_STOP=1 -U postgres -d postgres -q}"

echo "⚠ public 테이블 8개를 비우고 덤프로 다시 채웁니다. 계속하려면 yes:"
if [ "${SL_ASSUME_YES:-}" = "1" ]; then ans=yes; else read -r ans; fi
[ "$ans" = "yes" ] || { echo "중단"; exit 1; }

{
  echo "begin;"
  # 실패한 문장이 DB 로그에 통째로 남지 않게(그 문장에 개인정보 표 전체가 들어 있다)
  echo "set log_min_error_statement = panic;"
  # 로그인 계정 — 임시 테이블을 거쳐 upsert (이미 만든 부트스트랩 계정과 충돌해도 덤프가 이긴다)
  echo "create temp table _u (like auth.users including defaults) on commit drop;"
  echo "\\copy _u (id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at) from stdin with csv header"
  cat "$SRC/auth-users.csv"
  echo "\\."
  # 같은 이메일인데 id 가 다른 계정(새 서버에서 GoTrue 로 먼저 만든 부트스트랩 계정 등)은 지운다 — 덤프의 id 가
  # sl_admins.user_id 와 맞물려 있으므로 덤프가 이긴다. 신원·세션은 FK cascade 로 함께 지워지는데,
  # cascade 도 트리거라 replica 모드에선 돌지 않는다 → 반드시 replica 로 바꾸기 **전에** 지운다.
  echo "delete from auth.users u using _u where lower(u.email) = lower(_u.email) and u.id <> _u.id;"
  echo "set session_replication_role = replica;"
  echo "truncate public.sl_admins, public.sl_inquiries, public.sl_applications, public.sl_audit,"
  echo "         public.sl_content, public.sl_insights, public.sl_jobs, public.sl_settings;"
  # GoTrue(v2.158) 는 instance_id = 00000000-… 로 계정을 찾고, 토큰 열을 Go 문자열로 읽는다(NULL 이면 500).
  # 덤프에는 이 열들이 없으므로 GoTrue 가 직접 만든 계정과 같은 값으로 채운다 — 안 채우면 로그인·비밀번호 설정이 404.
  echo "insert into auth.users (instance_id,id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at,
                                confirmation_token,recovery_token,email_change_token_new,email_change)
        select '00000000-0000-0000-0000-000000000000',id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at,
               '','','','' from _u
        on conflict (id) do update set encrypted_password=coalesce(excluded.encrypted_password, auth.users.encrypted_password),
          instance_id=excluded.instance_id,
          aud=excluded.aud, role=excluded.role, email=excluded.email, email_confirmed_at=excluded.email_confirmed_at,
          last_sign_in_at=excluded.last_sign_in_at, raw_app_meta_data=excluded.raw_app_meta_data,
          raw_user_meta_data=excluded.raw_user_meta_data, created_at=excluded.created_at, updated_at=excluded.updated_at,
          confirmation_token=coalesce(auth.users.confirmation_token,''), recovery_token=coalesce(auth.users.recovery_token,''),
          email_change_token_new=coalesce(auth.users.email_change_token_new,''), email_change=coalesce(auth.users.email_change,'');"
  echo "create temp table _i (like auth.identities including defaults) on commit drop;"
  echo "\\copy _i (id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at) from stdin with csv header"
  cat "$SRC/auth-identities.csv"
  echo "\\."
  echo "insert into auth.identities (id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at)
        select id,user_id,identity_data,provider,provider_id,last_sign_in_at,created_at,updated_at from _i
        on conflict do nothing;"
  # pg_dump 머리말(SET … · set_config)만 걸러 낸다 — 첫 INSERT 이후는 건드리지 않는다.
  # (파일 전체에 걸면 여러 줄 문의 본문 속 "SET…" 으로 시작하는 줄까지 조용히 지워진다 — 경로 A)
  awk 'BEGIN{h=1} /^INSERT /{h=0} !(h && /^(SET |SELECT pg_catalog\.set_config)/)' "$SRC/public-data.sql"
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
            where a.user_id is not null and not exists (select 1 from auth.users u where u.id=a.user_id)
union all select '  ⚠ GoTrue 가 못 찾는 관리자 계정 ' || count(*) from public.sl_admins a
            join auth.users u on u.id = a.user_id
           where u.instance_id is distinct from '00000000-0000-0000-0000-000000000000'
              or u.confirmation_token is null or u.recovery_token is null
              or u.email_change_token_new is null or u.email_change is null
union all select '  🔑 비밀번호 미설정 관리자 ' || count(*) from public.sl_admins a
            join auth.users u on u.id = a.user_id where u.encrypted_password is null or u.encrypted_password = '';
EOSQL
echo "  (⚠ 두 줄이 0 이 아니면 그 관리자는 로그인할 수 없다)"
echo "  (비밀번호 미설정이 0 이 아니면 지금 바로 관리자마다:  bash scripts/set-admin-password.sh <이메일>)"
