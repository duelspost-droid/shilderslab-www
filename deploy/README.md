# 일반 서버 이관 — 빠른 시작

**설계·근거·선택지는 [SPEC.md](SPEC.md)** 에 있다. 여기는 명령만 모았다.

| 먼저 정할 것 | 권장 |
|---|---|
| 설치 방식 | Docker Compose (컨테이너 금지면 SPEC 부록 C) |
| 웹 서버 | nginx (사내 표준이 Apache 면 `apache/site.conf`) |
| DB | PostgreSQL 16 — **선택 불가**(SPEC 2.2) |
| WAS(Tomcat 등) | **필요 없음**(SPEC 2.1) |

```bash
# 0) 서버: Ubuntu 24.04 · 2vCPU · 4GB · 40GB SSD · 80/443/22 만 개방
git clone https://github.com/duelspost-droid/shilderslab-www.git /srv/shieldus
cd /srv/shieldus/deploy

# 1) 키·환경
cp .env.example .env && bash scripts/gen-keys.sh >> .env && vi .env && chmod 600 .env

# 2) DB·서비스 (순서가 중요 — 스크립트가 지킨다)
python3 scripts/test-db.py           # Docker 없이 DB 계층 사전 검증(pip install pgserver) — 36항목
python3 scripts/export-public.py     # 이관 당일 공개 데이터 시드 다시 뜨기
bash scripts/init-db.sh

# 3) 데이터 (오너가 관리형에서 뜬 덤프가 있을 때)
bash scripts/import-to-server.sh export/

# 4) TLS
sudo certbot certonly --standalone -d shielduslab.com -d www.shielduslab.com
mkdir -p certs certbot-www && sudo cp /etc/letsencrypt/live/shielduslab.com/{fullchain,privkey}.pem certs/
#   갱신 cron 은 반드시 --webroot (SPEC 10.4) — standalone 이면 60일 뒤 갱신 실패
docker compose up -d web

# 5) 프런트 연결 (레포 루트에서)
cd .. && python3 tools/set-domain.py --to shielduslab.com --apply
#   config.js 의 SUPABASE_URL·공개 키, tools/shell.py CSP connect-src 수정 → SPEC 7항 6단계
python3 tools/build-pages.py

# 6) 검증 — 보안 경계 실패 시 개통 금지
bash deploy/scripts/verify.sh https://shielduslab.com

# 7) 보존기간 파기 cron (🔴 법적 의무 — 잊지 말 것)
echo '20 3 * * * root docker compose -f /srv/shieldus/deploy/docker-compose.yml exec -T db psql -U postgres -c "select public.sl_purge_all();"' \
  | sudo tee /etc/cron.d/shieldus-purge
```
