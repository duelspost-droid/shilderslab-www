#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# 스키마를 **정해진 순서대로** 적용하고 서비스를 띄운다.  (SPEC 7항 3단계)
#
#   1) db 기동 — 01-roles-auth.sql · 01b-role-passwords.sh 자동 실행(빈 볼륨일 때)
#   2) 롤 비밀번호를 .env 값으로 재확인(볼륨이 이미 있던 경우 대비)
#   3) GoTrue 기동 → auth.users 가 생길 때까지 대기
#   4) 01-roles-auth.sql 재적용 — GoTrue 가 auth.uid() 를 옛 방식으로 덮어썼을 수 있다
#   5) supabase/migrations/0001~0007 순서대로
#   6) 공개 시드(03) — 트리거를 끈 세션에서(원래 수정 시각 보존)
#   7) 나머지 서비스 기동 · PostgREST 스키마 캐시 갱신
#
# 재실행 안전: 모든 단계가 멱등이다.
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")/.."                      # deploy/
[ -f .env ] || { echo "✗ deploy/.env 가 없습니다. .env.example 을 복사해 채우세요."; exit 1; }
set -a; . ./.env; set +a

DC="docker compose"
PSQL="$DC exec -T db psql -v ON_ERROR_STOP=1 -U postgres -d postgres -q"
step(){ printf "\n▶ %s\n" "$*"; }

step "1/7 DB 기동"
$DC up -d db
for i in $(seq 1 60); do
  $DC exec -T db pg_isready -U postgres >/dev/null 2>&1 && break
  sleep 2; [ "$i" = 60 ] && { echo "✗ DB 가 2분 안에 뜨지 않았습니다"; exit 1; }
done
echo "  ✓ DB 준비"

step "2/7 롤 비밀번호 확인"
$PSQL <<EOSQL
alter role authenticator       password '${POSTGRES_PASSWORD}';
alter role supabase_auth_admin password '${POSTGRES_PASSWORD}';
EOSQL
echo "  ✓ authenticator · supabase_auth_admin"

step "3/7 GoTrue 기동 → auth.users 생성 대기"
$DC up -d auth
for i in $(seq 1 60); do
  n=$($PSQL -tAc "select count(*) from information_schema.tables where table_schema='auth' and table_name='users'" 2>/dev/null || echo 0)
  [ "$n" = "1" ] && break
  sleep 2; [ "$i" = 60 ] && { echo "✗ GoTrue 가 auth.users 를 만들지 못했습니다:"; $DC logs --tail 30 auth; exit 1; }
done
echo "  ✓ auth.users 존재"

step "4/7 auth 헬퍼 재적용 (GoTrue 덮어쓰기 대비)"
$PSQL < db/01-roles-auth.sql
echo "  ✓ auth.uid() · auth.jwt() — 신·구 설정값 모두 읽는 버전으로 고정"

step "5/7 마이그레이션 0001~0007"
for f in ../supabase/migrations/0*.sql; do
  $PSQL < "$f" && echo "  ✓ $(basename "$f")"
done

step "6/7 공개 데이터 시드 (트리거 끔 — 원래 수정 시각 보존)"
{ echo "set session_replication_role = replica;"; cat db/03-seed-public.sql; } | $PSQL
echo "  ✓ sl_content · sl_insights · sl_jobs · sl_settings"

step "7/7 API 서비스 기동 (web 은 인증서 발급 뒤에 — SPEC 7항 5단계)"
# ⚠ 여기서 web 까지 띄우면 인증서가 없어 nginx 가 재시작을 반복하고,
#   그 사이 80 포트가 오락가락해 certbot --standalone 발급도 실패한다.
$DC up -d rest adminfn
$PSQL -c "notify pgrst, 'reload schema';"

echo
echo "── 적재 결과 ──"
$PSQL -tA <<'EOSQL'
select '  sl_content   ' || count(*) from public.sl_content
union all select '  sl_insights  ' || count(*) from public.sl_insights
union all select '  sl_jobs      ' || count(*) from public.sl_jobs
union all select '  sl_settings  ' || count(*) from public.sl_settings
union all select '  관리자(연결) ' || count(*) from public.sl_admins where user_id is not null
union all select '  RLS 정책     ' || count(*) from pg_policies where schemaname='public';
EOSQL
cat <<'MSG'

다음 단계
  · 관리형에서 덤프가 있으면  : bash scripts/import-to-server.sh export/
  · 없으면 첫 관리자를 SQL 로  : HANDOFF.md 3항 ② (관리자 0명이면 콘솔에 아무도 못 들어간다)
  · 인증서 발급 후 web 기동     : SPEC 7항 5단계
  · 검증                       : bash scripts/verify.sh https://<도메인>
MSG
