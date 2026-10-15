#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# 관리자 로그인 비밀번호를 정한다 — 새 서버에서.   (HANDOFF 13항 ②)
#   bash scripts/set-admin-password.sh <관리자 이메일>
#
# 언제: 대시보드 덤프(export-private.sql → convert-dashboard-dump.py)로 옮기면 비밀번호 해시가 없어
#       관리자가 로그인할 수 없다. 적재(import-to-server.sh) 뒤 관리자마다 한 번 돌린다. 분실 시에도 쓴다.
# 어떻게: GoTrue 관리 API(PUT /auth/v1/admin/users/<id>)를 service_role 키로 부른다 — 해시는 GoTrue 가 만든다.
# 전제: .env 가 채워져 있고 web·auth·db 가 떠 있으며 인증서가 설치돼 있다(7항 5단계 이후).
#       DNS 전환 전이어도 된다 — 요청을 이 서버(127.0.0.1)로 직접 보낸다.
# 비밀번호는 화면에 표시하지 않고, 명령줄 인자·로그에도 남기지 않는다.
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
EMAIL="${1:?관리자 이메일을 지정하세요}"
cd "$(dirname "$0")/.."
[ -f .env ] || { echo "✗ deploy/.env 가 없습니다"; exit 1; }
set -a; . ./.env; set +a
: "${SERVICE_ROLE_KEY:?.env 에 SERVICE_ROLE_KEY 가 없습니다}" "${SERVER_NAME:?.env 에 SERVER_NAME 이 없습니다}"

# 이메일은 psql 변수로 넘긴다(문자열 이어 붙이기 금지 — 따옴표가 든 입력이 SQL 이 되지 않게)
UID_="$(docker compose exec -T db psql -U postgres -d postgres -tA -v email="$EMAIL" <<'EOSQL'
select u.id from auth.users u join public.sl_admins a on a.user_id = u.id
 where lower(u.email) = lower(:'email');
EOSQL
)"
[ -n "$UID_" ] || { echo "✗ $EMAIL — 관리자로 결속된 로그인 계정이 없습니다(import 결과의 '연결 끊긴 관리자' 확인)"; exit 1; }

read -rsp "새 비밀번호: " PW; echo
read -rsp "한 번 더: " PW2; echo
[ "$PW" = "$PW2" ] || { echo "✗ 두 번 입력한 값이 다릅니다"; exit 1; }
[ "${#PW}" -ge 10 ] || { echo "✗ 10자 이상으로 정하세요"; exit 1; }

# 요청 본문·헤더를 표준입력/프로세스 치환으로 넘겨 ps 에 비밀번호·키가 보이지 않게 한다
code="$(printf '%s' "$PW" | python3 -c 'import json,sys; print(json.dumps({"password": sys.stdin.read()}))' \
  | curl -sS -o /dev/null -w '%{http_code}' -X PUT \
      --resolve "${SERVER_NAME}:443:127.0.0.1" \
      -H @<(printf 'Authorization: Bearer %s\napikey: %s\nContent-Type: application/json\n' "$SERVICE_ROLE_KEY" "$SERVICE_ROLE_KEY") \
      --data-binary @- "https://${SERVER_NAME}/auth/v1/admin/users/${UID_}")"
unset PW PW2
[ "$code" = "200" ] || { echo "✗ GoTrue 응답 $code — docker compose logs auth 로 원인 확인"; exit 1; }
echo "✓ $EMAIL 비밀번호를 정했습니다. https://${SERVER_NAME}/admin/ 에서 로그인해 확인하세요."
