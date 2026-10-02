#!/bin/bash
# 01-roles-auth.sql 다음에 자동 실행된다(initdb.d 는 파일명 순).
# SQL 파일은 환경변수를 못 읽어서 롤을 임시 비밀번호로 만든다. 여기서 .env 값으로 바꾼다.
# ⚠ 이걸 안 하면 GoTrue·PostgREST 가 첫 기동부터 인증 실패로 재시작을 반복한다.
set -euo pipefail
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<EOSQL
alter role authenticator       password '${POSTGRES_PASSWORD}';
alter role supabase_auth_admin password '${POSTGRES_PASSWORD}';
EOSQL
