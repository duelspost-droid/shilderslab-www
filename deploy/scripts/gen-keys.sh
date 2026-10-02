#!/usr/bin/env bash
# JWT 시크릿과 anon / service_role 키를 만든다.
#
# 관리형 Supabase 가 주던 키는 **그 프로젝트 전용**이라 자체 호스팅에서는 쓸 수 없다.
# 여기서 새로 만든 뒤 .env 와 config.js 에 넣는다.
#   · JWT_SECRET      : GoTrue 와 PostgREST 가 **같은 값**을 써야 한다. 다르면 로그인 토큰이 거부된다.
#   · ANON_KEY        : 브라우저에 공개되는 키. 공개돼도 RLS 가 막는다.
#   · SERVICE_ROLE_KEY: RLS 를 우회한다. **절대 브라우저·공개 저장소에 두지 않는다.**
set -euo pipefail

SECRET="${1:-$(head -c 48 /dev/urandom | base64 | tr -d '=+/' | cut -c1-48)}"
EXP_YEARS="${EXP_YEARS:-10}"

mint() {  # $1=role
  python3 - "$SECRET" "$1" "$EXP_YEARS" <<'PY'
import base64, hashlib, hmac, json, sys, time
secret, role, years = sys.argv[1], sys.argv[2], int(sys.argv[3])
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b'=').decode()
now = int(time.time())
head = b64(json.dumps({"alg":"HS256","typ":"JWT"},separators=(',',':')).encode())
body = b64(json.dumps({"role":role,"iss":"supabase","iat":now,
                       "exp":now+years*31536000},separators=(',',':')).encode())
msg  = f"{head}.{body}".encode()
sig  = b64(hmac.new(secret.encode(), msg, hashlib.sha256).digest())
print(f"{head}.{body}.{sig}")
PY
}

echo "# ── gen-keys.sh 산출물 — .env 에 그대로 붙여 넣으세요 ─────────────"
echo "JWT_SECRET=$SECRET"
echo "ANON_KEY=$(mint anon)"
echo "SERVICE_ROLE_KEY=$(mint service_role)"
echo
echo "# ANON_KEY 는 config.js 에도 넣습니다(브라우저에 공개되는 값이라 괜찮습니다)."
echo "# SERVICE_ROLE_KEY 는 .env 에만 둡니다. 저장소에 커밋하지 마세요."
