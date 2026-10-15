#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대시보드에서 받은 비공개 데이터 덤프 → import-to-server.sh 가 읽는 파일 3개.   (HANDOFF 13항 ②)

    python3 deploy/scripts/convert-dashboard-dump.py <받은파일.csv|.json>  [출력폴더=deploy/export]

받은 파일 = Supabase SQL 편집기에서 deploy/scripts/export-private.sql 을 실행하고
            결과(dump 한 칸)를 [Export → Download CSV] 또는 [Copy as JSON] 으로 저장한 것.
나오는 것 = public-data.sql · auth-users.csv · auth-identities.csv  (import-to-server.sh 의 입력 그대로)

export-from-supabase.sh(Docker·DB 비밀번호 필요)와 같은 결과를 내되 한 가지가 다르다:
  🔑 **비밀번호 해시가 없다.** 대시보드 쿼리는 해시를 꺼내지 않는다. 그래서 auth-users.csv 의
     encrypted_password 칸이 비어 있고, 적재 뒤 관리자마다 scripts/set-admin-password.sh 로 비밀번호를 새로 정한다.

🔴 입력·출력 모두 개인정보다. 레포 밖(또는 gitignore 된 deploy/export/)에만 두고, 이관이 끝나면 지운다.
   이 스크립트는 내용을 화면에 찍지 않는다 — 건수만 보여 준다.
"""
import csv, io, json, os, secrets, stat, sys

TABLES = ["sl_admins", "sl_inquiries", "sl_applications", "sl_audit",
          "sl_content", "sl_insights", "sl_jobs", "sl_settings"]          # 8개 — import 가 비우는 목록과 같다
USER_COLS = ["id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "last_sign_in_at",
             "raw_app_meta_data", "raw_user_meta_data", "created_at", "updated_at"]
IDENT_COLS = ["id", "user_id", "identity_data", "provider", "provider_id", "last_sign_in_at", "created_at", "updated_at"]


def load(path):
    """Download CSV · Copy as JSON · 셀 값만 복사한 원문 — 셋 다 받는다."""
    raw = open(path, encoding="utf-8-sig").read().strip()
    if raw.startswith("{"):
        return json.loads(raw)
    if raw.startswith("["):                                   # Copy as JSON → [{"dump": "..."}]
        rows = json.loads(raw)
        return json.loads(rows[0]["dump"])
    csv.field_size_limit(1 << 30)                             # dump 한 칸이 수백 KB 다
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows or "dump" not in rows[0]:
        sys.exit("✗ 'dump' 열이 없다 — export-private.sql 의 결과를 저장한 파일인지 확인")
    return json.loads(rows[0]["dump"])


def csv_field(v):
    """psql \\copy … csv 와 같은 규칙: NULL = 빈 칸(따옴표 없음), 값은 따옴표로 감싼다(빈 문자열 "" 과 NULL 을 구분)."""
    return "" if v is None else '"' + str(v).replace('"', '""') + '"'


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)               # 600


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = load(sys.argv[1])
    if d.get("format") != "sl-private-dump/1":
        sys.exit(f"✗ 형식이 다르다: {d.get('format')!r} (sl-private-dump/1 이어야 한다)")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "export")
    os.makedirs(out, exist_ok=True); os.chmod(out, stat.S_IRWXU)  # 700

    tables = d["tables"]
    missing = [t for t in TABLES if t not in tables]
    if missing:
        sys.exit(f"✗ 덤프에 테이블이 없다: {missing}")

    # ── public-data.sql: 테이블마다 JSON 배열 하나 → json_populate_recordset 으로 넣는다.
    #    열을 이름으로 맞추므로 열 순서·타입(uuid·timestamptz·jsonb·date)을 따로 다룰 필요가 없다.
    #    JSON 은 한 줄로 쓴다 — import 스크립트가 'SET…' 으로 시작하는 줄을 걸러 내기 때문(줄바꿈은 \\n 으로 이스케이프된다).
    blob = json.dumps(tables, ensure_ascii=False)
    tag = "$sl_dump$"
    while tag in blob:
        tag = f"$sl_dump_{secrets.token_hex(4)}$"
    lines = [f"-- 비공개 데이터 덤프 → convert-dashboard-dump.py",
             f"--   원본 생성 {d.get('generated_at')} · 원본 PostgreSQL {d.get('server_version')}",
             f"--   🔴 개인정보 포함 — 커밋 금지 · 이관 후 삭제"]
    for t in TABLES:
        js = json.dumps(tables[t], ensure_ascii=False, separators=(",", ":"))
        over = " OVERRIDING SYSTEM VALUE" if t == "sl_audit" else ""      # id 가 IDENTITY — 원래 번호를 보존한다
        lines.append(f"INSERT INTO public.{t}{over} SELECT * FROM json_populate_recordset(NULL::public.{t}, {tag}{js}{tag});")
    # IDENTITY 시퀀스를 원래 최댓값 다음으로 — 안 하면 다음 감사 로그가 1번과 충돌한다
    lines.append("SELECT pg_catalog.setval(pg_get_serial_sequence('public.sl_audit', 'id'), "
                 "(SELECT coalesce(max(id), 1) FROM public.sl_audit), (SELECT count(*) > 0 FROM public.sl_audit));")
    write(os.path.join(out, "public-data.sql"), "\n".join(lines) + "\n")

    # ── auth-users.csv: 대시보드 쿼리는 비밀번호 해시를 꺼내지 않는다 → encrypted_password 는 NULL
    users = d.get("auth_users") or []
    rows = [",".join(USER_COLS)]
    for u in users:
        if len(u) != 10:
            sys.exit(f"✗ auth_users 행의 칸 수가 10 이 아니다({len(u)}) — export-private.sql 이 바뀌었는지 확인")
        rec = dict(zip([c for c in USER_COLS if c != "encrypted_password"], u))
        rec["encrypted_password"] = None
        rows.append(",".join(csv_field(rec[c]) for c in USER_COLS))
    write(os.path.join(out, "auth-users.csv"), "\n".join(rows) + "\n")

    idents = d.get("auth_identities") or []
    rows = [",".join(IDENT_COLS)]
    for i in idents:
        if len(i) != len(IDENT_COLS):
            sys.exit(f"✗ auth_identities 행의 칸 수가 {len(IDENT_COLS)} 이 아니다({len(i)})")
        rows.append(",".join(csv_field(v) for v in i))
    write(os.path.join(out, "auth-identities.csv"), "\n".join(rows) + "\n")

    linked = {a.get("user_id") for a in tables["sl_admins"] if a.get("user_id")}
    have = {u[0] for u in users}
    print(f"✓ {out}/  (권한 600)")
    print("  " + " · ".join(f"{t.replace('sl_', '')} {len(tables[t])}" for t in TABLES))
    print(f"  로그인 계정 {len(users)} · 신원 {len(idents)} · 원본 PostgreSQL {d.get('server_version')}")
    if linked - have:
        print(f"  ⚠ 관리자에 결속됐는데 계정이 덤프에 없는 user_id {len(linked - have)}개 — 적재 뒤 그 관리자는 권한이 없다")
    print("  🔑 비밀번호 해시 없음 → 적재 뒤 관리자마다:  bash scripts/set-admin-password.sh <이메일>")
    print("  다음: 새 서버 deploy/ 에서  bash scripts/import-to-server.sh export/")


if __name__ == "__main__":
    main()
