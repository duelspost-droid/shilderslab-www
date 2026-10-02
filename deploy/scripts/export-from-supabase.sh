#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# [오너 실행] 관리형 Supabase 에서 전체 데이터를 뜬다.  (SPEC 8.2항)
#
# 필요한 것 : Supabase → Project Settings → Database → Connection string (Direct)
#   SUPABASE_DB_URL='postgresql://postgres:<비밀번호>@db.<ref>.supabase.co:5432/postgres' \
#     bash scripts/export-from-supabase.sh
#
# 🔴 결과물에 **개인정보**(문의·지원자 이름·이메일·전화)와 **비밀번호 해시**가 들어 있다.
#    암호화된 경로로만 옮기고, 이관이 끝나면 즉시 지운다. 저장소에 절대 커밋하지 않는다.
#
# ⚠ 이 스크립트는 관리형 DB 접속 권한 없이 작성됐다 — 실제 실행 검증은 오너 첫 실행 때 이뤄진다.
#   auth.users 는 버전마다 컬럼이 달라 **필요한 컬럼만 골라** CSV 로 뜬다(전체 덤프는 이식 시 깨진다).
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
: "${SUPABASE_DB_URL:?SUPABASE_DB_URL 을 지정하세요(위 주석 참조)}"
cd "$(dirname "$0")/.."
OUT="export"; mkdir -p "$OUT"; chmod 700 "$OUT"

# 관리형이 PG17 일 수 있다. pg_dump 는 서버보다 같거나 높아야 하므로 17 클라이언트를 쓴다.
PGCLI="docker run --rm -i -e PGCONNECT_TIMEOUT=15 postgres:17"

echo "▶ 원본 DB 버전"
$PGCLI psql "$SUPABASE_DB_URL" -tAc "select version();" | sed 's/^/  /'

echo "▶ public 테이블 8개 (데이터만, 컬럼명 포함 INSERT)"
$PGCLI pg_dump "$SUPABASE_DB_URL" --data-only --column-inserts --no-owner --no-privileges \
  -t public.sl_admins -t public.sl_inquiries -t public.sl_applications -t public.sl_audit \
  -t public.sl_content -t public.sl_insights -t public.sl_jobs -t public.sl_settings \
  > "$OUT/public-data.sql"
echo "  ✓ $OUT/public-data.sql ($(grep -c '^INSERT' "$OUT/public-data.sql")행)"

echo "▶ 로그인 계정 (auth.users — 필요한 컬럼만)"
$PGCLI psql "$SUPABASE_DB_URL" -c "\copy (
  select id, aud, role, email, encrypted_password, email_confirmed_at,
         last_sign_in_at, raw_app_meta_data, raw_user_meta_data,
         created_at, updated_at
    from auth.users
   where id in (select user_id from public.sl_admins where user_id is not null)
) to stdout with csv header" > "$OUT/auth-users.csv"
echo "  ✓ $OUT/auth-users.csv ($(($(wc -l < "$OUT/auth-users.csv")-1))명)"
# ↑ 🚨 이 프로젝트는 다른 서비스와 **공유**되므로(secuday·VulnScan 등) auth.users 에 남의 사용자가 있다.
#    **이 사이트 관리자로 결속된 계정만** 옮긴다. 전체를 옮기면 무관한 개인정보를 반출하게 된다.

echo "▶ 로그인 신원 (auth.identities — 이메일 로그인에 필요)"
$PGCLI psql "$SUPABASE_DB_URL" -c "\copy (
  select id, user_id, identity_data, provider, provider_id,
         last_sign_in_at, created_at, updated_at
    from auth.identities
   where user_id in (select user_id from public.sl_admins where user_id is not null)
) to stdout with csv header" > "$OUT/auth-identities.csv"
echo "  ✓ $OUT/auth-identities.csv ($(($(wc -l < "$OUT/auth-identities.csv")-1))행)"

chmod 600 "$OUT"/*
cat <<'MSG'

완료. 다음:
  1) export/ 를 새 서버의 deploy/export/ 로 **암호화된 경로(scp 등)** 로 옮긴다
  2) 새 서버에서  bash scripts/import-to-server.sh export/
  3) 이관 확인 후  shred -u export/*  로 양쪽 모두 지운다
MSG
