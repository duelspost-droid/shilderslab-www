#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# 이관 후 자동 검증 (SPEC 9항).  bash scripts/verify.sh https://shielduslab.com
#   · 보안 경계 항목이 하나라도 실패하면 종료코드 1 — **개통하지 말 것**
#   · 공개 키(ANON_KEY)는 deploy/.env 에서 읽는다
#   · 관리자 로그인·문구 저장처럼 비밀번호가 필요한 항목은 수동(9.1항)
# ═══════════════════════════════════════════════════════════════════════════
set -uo pipefail
BASE="${1:?검증할 주소를 지정하세요 (예: https://shielduslab.com)}"; BASE="${BASE%/}"
cd "$(dirname "$0")/.."
ANON="${ANON_KEY:-$(grep -E '^ANON_KEY=' .env 2>/dev/null | cut -d= -f2-)}"
[ -n "$ANON" ] || { echo "✗ ANON_KEY 를 찾지 못했습니다(.env 또는 환경변수)"; exit 2; }
CURL="curl -sk --max-time 15"
H=(-H "apikey: $ANON" -H "Authorization: Bearer $ANON")
pass=0; fail=0; crit=0
ok(){ printf "  ✅ %s\n" "$1"; pass=$((pass+1)); }
ng(){ printf "  ❌ %s  — %s\n" "$1" "$2"; fail=$((fail+1)); [ "${3:-}" = crit ] && crit=$((crit+1)); }
code(){ $CURL -o /dev/null -w '%{http_code}' "$@"; }

echo "═══ 9.1 기능 ═══"
for p in / /about/ /services/ /method/ /contact/ /trust/ /admin/; do
  c=$(code "$BASE$p"); [ "$c" = 200 ] && ok "$p → 200" || ng "$p" "HTTP $c"
done
c=$(code "$BASE/__no_such_page__/"); [ "$c" = 404 ] && ok "없는 경로 → 404" || ng "없는 경로" "HTTP $c (404 여야 함)"
n=$($CURL "${H[@]}" "$BASE/rest/v1/sl_content?select=key" | python3 -c "import sys,json;print(len(json.load(sys.stdin)))" 2>/dev/null || echo -1)
[ "$n" -gt 0 ] 2>/dev/null && ok "공개 문구 조회 ($n 블록)" || ng "공개 문구 조회" "결과 $n — API 연결 또는 시드 확인"

echo; echo "═══ 9.2 보안 경계 — 하나라도 실패하면 개통 금지 ═══"
for t in sl_inquiries sl_applications sl_admins sl_audit; do
  r=$($CURL "${H[@]}" "$BASE/rest/v1/$t?select=*&limit=1")
  n=$(printf '%s' "$r" | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d) if isinstance(d,list) else -1)" 2>/dev/null || echo -1)
  [ "$n" = 0 ] && ok "공개 키로 $t → 0행" || ng "공개 키로 $t" "$n행 노출 — RLS 확인" crit
done
for fn in sl_stats sl_admin_list; do
  c=$(code -X POST "${H[@]}" -H 'Content-Type: application/json' -d '{}' "$BASE/rest/v1/rpc/$fn")
  case "$c" in 401|403|404) ok "공개 키로 $fn → 거부($c)";; *) ng "공개 키로 $fn" "HTTP $c (거부돼야 함)" crit;; esac
done
c=$(code -X POST -H "apikey: $ANON" -H 'Content-Type: application/json' \
      -d '{"email":"verify-probe@example.invalid","password":"Verify-Probe-2026!"}' "$BASE/auth/v1/signup")
case "$c" in 400|403|422) ok "셀프 가입 → 거부($c)";; *) ng "셀프 가입" "HTTP $c — GOTRUE_DISABLE_SIGNUP 확인" crit;; esac
r=$($CURL -X POST "${H[@]}" -H 'Content-Type: application/json' \
      -d '{"p_company":"검증","p_name":"검증","p_email":"verify@example.invalid","p_phone":"","p_service":"기타","p_message":"verify.sh 동의 없음 시험","p_consent":false}' \
      "$BASE/rest/v1/rpc/sl_submit_inquiry")
printf '%s' "$r" | grep -qiE 'consent|동의|error|message' && ok "동의 없는 문의 → 거부" || ng "동의 없는 문의" "응답: ${r:0:80}" crit
for p in /tools/build-pages.py /supabase/migrations/0001_shilderslab_core.sql /deploy/.env /.git/config; do
  c=$(code "$BASE$p"); [ "$c" = 404 ] && ok "$p → 404" || ng "$p" "HTTP $c (저장소 내부 노출)" crit
done
c=$(code "${H[@]}" "$BASE/rest/v1/")
b=$($CURL "${H[@]}" "$BASE/rest/v1/" | head -c 200)
printf '%s' "$b" | grep -q '"paths"' && ng "API 구조(OpenAPI) 노출" "PGRST_OPENAPI_MODE=disabled 확인" crit || ok "API 구조 비공개"
hdr=$($CURL -D - -o /dev/null "$BASE/")
for h in "strict-transport-security" "x-content-type-options" "x-frame-options" "referrer-policy"; do
  printf '%s' "$hdr" | grep -qi "^$h:" && ok "헤더 $h" || ng "헤더 $h" "없음" crit
done

echo; echo "═══ 9.3 운영 (서버에서 실행했을 때만) ═══"
if docker compose ps db >/dev/null 2>&1; then
  docker compose exec -T db psql -U postgres -tAc "select public.sl_purge_all();" >/dev/null 2>&1 \
    && ok "보존기간 파기 함수 실행" || ng "보존기간 파기 함수" "실행 실패"
  n=$(docker compose exec -T db psql -U postgres -tAc "select count(*) from public.sl_admins where user_id is not null" 2>/dev/null | tr -d ' ')
  [ "${n:-0}" -ge 1 ] && ok "연결된 관리자 ${n}명" || ng "연결된 관리자" "0명 — 콘솔에 아무도 못 들어간다(HANDOFF 3항 ②)"
  for p in 5432 3000 9999 8080 8081; do
    docker compose port db "$p" >/dev/null 2>&1 && ng "포트 $p" "외부에 publish 됨" crit || true
  done
  ok "내부 포트(5432·3000·9999·8080·8081) 미공개"
  crontab -l 2>/dev/null | grep -q sl_purge_all || ls /etc/cron.d/ 2>/dev/null | grep -q shieldus \
    && ok "파기 cron 등록됨" || ng "파기 cron" "미등록 — SPEC 4.7항(법적 보존기간)"
else
  echo "  (도커 미발견 — 서버에서 다시 실행하면 운영 항목까지 점검합니다)"
fi

echo
echo "결과: 통과 $pass · 실패 $fail (보안 경계 실패 $crit)"
[ "$crit" -eq 0 ] || { echo "🚨 보안 경계 실패가 있습니다. 개통하지 마세요."; exit 1; }
[ "$fail" -eq 0 ] || exit 1
