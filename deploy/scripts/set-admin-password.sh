#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# 관리자 로그인 비밀번호를 정한다 — 새 서버에서.   (SPEC 7항 4단계 · 8.2 B)
#   bash scripts/set-admin-password.sh <관리자 이메일>
#
# 언제: 대시보드 덤프(export-private.sql → convert-dashboard-dump.py)로 옮기면 비밀번호 해시가 없어
#       관리자가 로그인할 수 없다. import-to-server.sh **직후 바로** 관리자마다 한 번 돌린다. 분실 시에도 쓴다.
# 어떻게: GoTrue 관리 API(PUT /admin/users/<id>)를 service_role 키로 부른다 — 해시는 GoTrue 가 만든다.
#       요청은 auth 컨테이너의 네트워크 안에서 보낸다(curl 이미지) → TLS·DNS·웹 서버가 아직 없어도 된다.
# 전제: deploy/.env 가 채워져 있고 db·auth 가 떠 있다(init-db.sh 이후). 인터넷(curl 이미지 내려받기).
# 비밀번호·키는 화면·명령줄 인자·로그에 남기지 않는다(표준입력으로만 넘긴다).
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail
EMAIL="${1:?관리자 이메일을 지정하세요}"
cd "$(dirname "$0")/.."
[ -f .env ] || { echo "✗ deploy/.env 가 없습니다"; exit 1; }
# .env 를 bash 로 실행하지 않고 필요한 키만 읽는다(따옴표 유무와 무관하게)
KEY="$(grep -E '^SERVICE_ROLE_KEY=' .env | tail -1 | cut -d= -f2- | sed -E 's/^["'\'']//; s/["'\'']$//')"
[ -n "$KEY" ] || { echo "✗ .env 에 SERVICE_ROLE_KEY 가 없습니다"; exit 1; }
AUTH_CID="$(docker compose ps -q auth)"
[ -n "$AUTH_CID" ] || { echo "✗ auth 컨테이너가 떠 있지 않습니다(docker compose up -d auth)"; exit 1; }

# 이메일은 psql 변수로 넘긴다(문자열 이어 붙이기 금지 — 따옴표가 든 입력이 SQL 이 되지 않게)
UID_="$(docker compose exec -T db psql -U postgres -d postgres -tA -v email="$EMAIL" <<'EOSQL'
select u.id from auth.users u join public.sl_admins a on a.user_id = u.id
 where lower(u.email) = lower(:'email');
EOSQL
)"
[ -n "$UID_" ] || { echo "✗ $EMAIL — 관리자로 결속된 로그인 계정이 없습니다(import 결과의 '연결 끊긴 관리자' 확인)"; exit 1; }

IFS= read -rsp "새 비밀번호: " PW; echo
IFS= read -rsp "한 번 더: " PW2; echo
[ "$PW" = "$PW2" ] || { echo "✗ 두 번 입력한 값이 다릅니다"; exit 1; }
[ "${#PW}" -ge 10 ] || { echo "✗ 10자 이상으로 정하세요"; exit 1; }

# curl 설정 파일(-K -)을 표준입력으로 만든다 — 키·비밀번호가 인자에 나타나지 않는다
CFG='
import json, os, sys
q = lambda s: "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\""
print("url = " + q("http://localhost:9999/admin/users/" + os.environ["SL_UID"]))
print("request = \"PUT\"")
print("header = " + q("Authorization: Bearer " + os.environ["SL_KEY"]))
print("header = \"Content-Type: application/json\"")
print("data-binary = " + q(json.dumps({"password": sys.stdin.read()})))
'
code="$(printf '%s' "$PW" | SL_KEY="$KEY" SL_UID="$UID_" python3 -c "$CFG" \
  | docker run --rm -i --network "container:${AUTH_CID}" curlimages/curl:8.10.1 \
      -sS -o /dev/null -w '%{http_code}' -K -)" || code="${code:-000}"
unset PW PW2 KEY
[ "$code" = "200" ] || { echo "✗ GoTrue 응답 $code — docker compose logs auth 로 원인 확인"; exit 1; }
echo "✓ $EMAIL 비밀번호를 정했습니다. 웹 서버가 뜬 뒤 /admin/ 에서 로그인해 확인하세요."
