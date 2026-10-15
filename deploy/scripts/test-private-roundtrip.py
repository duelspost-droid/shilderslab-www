#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""비공개 데이터 이관 경로를 가짜 데이터로 끝까지 돌려 본다 — Docker·실데이터 없이.

    python3 deploy/scripts/test-private-roundtrip.py

  원본 DB(가짜 개인정보·까다로운 문자열) ─ export-private.sql ─▶ 대시보드 CSV 모양
    ─ convert-dashboard-dump.py ─▶ export/ 3개 ─ import-to-server.sh ─▶ 새 DB
  그리고 8개 테이블·로그인 계정·신원이 원본과 같은지, 비밀번호·시퀀스가 의도대로인지 본다.
필요한 것: pgserver (test-db.py 와 같다)
"""
import importlib.util, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEPLOY = os.path.dirname(HERE)
ROOT = os.path.dirname(DEPLOY)
spec = importlib.util.spec_from_file_location("testdb", os.path.join(HERE, "test-db.py"))
T = importlib.util.module_from_spec(spec); sys.argv = sys.argv[:1]; spec.loader.exec_module(T)

U1, U2, U3 = ("11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222",
              "33333333-3333-4333-8333-333333333333")
U9 = "99999999-9999-4999-8999-999999999999"          # 새 서버에서 GoTrue 로 먼저 만든 부트스트랩 계정(U1 과 같은 이메일, 다른 id)
NIL = "00000000-0000-0000-0000-000000000000"
HASH1, HASH2, HASH3 = "$2a$10$fakehashONE.................................", "$2a$10$fakehashTWO...", "$2a$10$other"
BOOT = "$2a$10$bootstrapKEEP"                       # 새 서버에 미리 있던 같은 id 계정의 비밀번호 — 해시 없는 덤프가 지우면 안 된다
TRICKY = "O'Reilly \"따옴표\" back\\slash\nSET search_path = evil;\n$sl_dump$ 🛡️ 한글·IP"
SETLINES = "안녕하세요.\nSETUP 비용이 궁금합니다.\nSELECT pg_catalog.set_config(x)\n감사합니다."   # 경로 A 줄 필터 함정

# GoTrue v2.158.1 의 auth.users 모양(관련 열): instance_id·토큰 4열은 NULL 허용·기본값 없음,
# 나머지 토큰류는 기본값 ''. GoTrue 는 instance_id = NIL 로 계정을 찾고 토큰 열을 문자열로 읽는다.
AUTH_DDL = """set role supabase_auth_admin;
create table if not exists auth.users (instance_id uuid null, id uuid primary key, aud varchar(255), role varchar(255),
  email varchar(255), encrypted_password varchar(255), email_confirmed_at timestamptz, invited_at timestamptz,
  confirmation_token varchar(255), confirmation_sent_at timestamptz, recovery_token varchar(255), recovery_sent_at timestamptz,
  email_change_token_new varchar(255), email_change varchar(255), email_change_sent_at timestamptz,
  last_sign_in_at timestamptz, raw_app_meta_data jsonb, raw_user_meta_data jsonb, is_super_admin boolean,
  created_at timestamptz, updated_at timestamptz, phone text default null, phone_change text default '',
  phone_change_token varchar(255) default '', email_change_token_current varchar(255) default '',
  reauthentication_token varchar(255) default '', is_sso_user boolean not null default false);
create unique index if not exists users_email_partial_key on auth.users (email) where (is_sso_user = false);
create table if not exists auth.identities (id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  identity_data jsonb not null, provider text not null, provider_id text not null,
  last_sign_in_at timestamptz, created_at timestamptz default now(), updated_at timestamptz default now(),
  email text generated always as (lower(identity_data->>'email')) stored, unique (provider_id, provider));
reset role;"""

def schema(pg):
    pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
    pg.psql(AUTH_DDL)
    pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
    for f in sorted(os.listdir(os.path.join(ROOT, "supabase/migrations"))):
        if f.endswith(".sql"): pg.psql(file=os.path.join(ROOT, "supabase/migrations", f))

def q(pg, sql):
    return pg.psql(sql).stdout.strip()

def main():
    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        print(f"  {'✓' if cond else '✗'} {name}" + (f" — {detail}" if detail and not cond else ""))
        ok = ok and bool(cond)

    src, dst = T.PG(), T.PG()
    work = tempfile.mkdtemp(prefix="sl-roundtrip-")
    try:
        schema(src); schema(dst)
        # ── 원본: 가짜 계정 3개(2개는 이 사이트 관리자, 1개는 공유 프로젝트의 다른 서비스 사용자)
        lit = lambda s: "'" + s.replace("'", "''") + "'"
        src.psql(f"""set session_replication_role = replica;
insert into auth.users (instance_id,id,aud,role,email,encrypted_password,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at,
                        confirmation_token,recovery_token,email_change_token_new,email_change) values
 ('{NIL}','{U1}','authenticated','authenticated','owner@example.test',{lit(HASH1)},now(),now(),'{{"provider":"email","providers":["email"]}}',{lit(json.dumps({"name": TRICKY}, ensure_ascii=False))}, now()-interval '30 days', now(),'','','',''),
 ('{NIL}','{U2}','authenticated','authenticated','editor@example.test',{lit(HASH2)},now(),null,'{{}}','{{}}', now()-interval '3 days', now(),'','','',''),
 ('{NIL}','{U3}','authenticated','authenticated','other-service@example.test',{lit(HASH3)},now(),null,'{{}}','{{}}', now(), now(),'','','','');
insert into auth.identities (user_id,identity_data,provider,provider_id) values
 ('{U1}','{{"sub":"{U1}","email":"owner@example.test"}}','email','{U1}'),
 ('{U2}','{{"sub":"{U2}","email":"editor@example.test"}}','email','{U2}'),
 ('{U3}','{{"sub":"{U3}","email":"other-service@example.test"}}','email','{U3}');
insert into public.sl_admins (email, role, user_id, pw_managed, note) values
 ('owner@example.test','admin','{U1}',false,{lit(TRICKY)}),
 ('editor@example.test','editor','{U2}',true,null),
 ('pending@example.test','editor',null,false,'미결속');
insert into public.sl_inquiries (company,name,email,phone,service,message,consent_at,ip,user_agent) values
 ({lit(TRICKY)},'홍길동','a@example.test','010-0000-0000','pentest',{lit(TRICKY)},now(),'203.0.113.7','UA "x"'),
 ('','김빈칸','b@example.test','','',{lit(SETLINES)},now(),null,null);
insert into public.sl_applications (name,email,phone,position,summary,link,consent_at) values
 ('지원자','c@example.test','','보안 컨설턴트',{lit(TRICKY)},'https://example.test/cv',now());
insert into public.sl_audit (kind,action,detail,ip,user_agent) values
 ('visit','visit','{{"path":"/","nested":{{"a":[1,2,{{"b":null}}]}}}}','198.51.100.1','UA'),
 ('submit','inquiry',{lit(json.dumps({"t": TRICKY}, ensure_ascii=False))},null,null);
update public.sl_content set value = {lit(TRICKY)} where key = (select min(key) from public.sl_content);""")
        n_audit = int(q(src, "select count(*) from public.sl_audit"))

        # ── 대시보드에서 Run → Download CSV 한 것과 같은 파일
        dump = q(src, open(os.path.join(HERE, "export-private.sql"), encoding="utf-8").read())
        csv_path = os.path.join(work, "Supabase Snippet Untitled query.csv")
        open(csv_path, "w", encoding="utf-8").write('dump\n"' + dump.replace('"', '""') + '"\n')
        d = json.loads(dump)
        check("덤프에 비밀번호 해시가 없다", "fakehash" not in dump and "bootstrap" not in dump)
        check("다른 서비스 사용자는 덤프에 없다", "other-service@example.test" not in dump)

        out = os.path.join(work, "export")
        r = subprocess.run([sys.executable, os.path.join(HERE, "convert-dashboard-dump.py"), csv_path, out],
                           capture_output=True, text=True)
        check("변환기 실행", r.returncode == 0, (r.stderr or r.stdout)[-400:])
        check("변환기 출력에 개인정보가 찍히지 않는다", "홍길동" not in r.stdout and "@example.test" not in r.stdout)
        check("출력 파일 권한 600", all(oct(os.stat(os.path.join(out, f)).st_mode)[-3:] == "600"
                                     for f in ("public-data.sql", "auth-users.csv", "auth-identities.csv")))

        # ── 새 서버: init-db 처럼 공개 시드를 넣고, GoTrue 로 먼저 만든 계정 둘을 둔다
        #    U2 = 같은 id(비밀번호 있음 → 해시 없는 덤프가 지우면 안 됨) · U9 = U1 과 같은 이메일·다른 id(덤프가 이겨야 함)
        dst.psql(file=os.path.join(DEPLOY, "db/03-seed-public.sql"))
        dst.psql(f"""insert into auth.users (instance_id,id,aud,role,email,encrypted_password,created_at,updated_at,confirmation_token,recovery_token,email_change_token_new,email_change) values
                    ('{NIL}','{U2}','authenticated','authenticated','editor@example.test',{lit(BOOT)},now(),now(),'','','',''),
                    ('{NIL}','{U9}','authenticated','authenticated','OWNER@example.test','$2a$10$boot9',now(),now(),'','','','');
                    insert into auth.identities (user_id,identity_data,provider,provider_id)
                    values ('{U9}','{{"sub":"{U9}","email":"owner@example.test"}}','email','{U9}');""")
        psql_cmd = f"{T.BIN}/psql -h {dst.dir} -p {dst.port} -U postgres -d postgres -v ON_ERROR_STOP=1 -q -X"
        r = subprocess.run(["bash", os.path.join(HERE, "import-to-server.sh"), out],
                           env={**os.environ, "SL_PSQL": psql_cmd, "SL_ASSUME_YES": "1"}, capture_output=True, text=True)
        check("import-to-server.sh 실행", r.returncode == 0, (r.stderr or r.stdout)[-600:])
        check("적재 보고: GoTrue 가 못 찾는 관리자 계정 0", "GoTrue 가 못 찾는 관리자 계정 0" in r.stdout, r.stdout[-400:])
        check("적재 보고: 비밀번호 미설정 관리자 1명(owner)", "비밀번호 미설정 관리자 1" in r.stdout, r.stdout[-400:])

        # ── 비교
        order = {"sl_admins": "email", "sl_inquiries": "id", "sl_applications": "id", "sl_audit": "id",
                 "sl_content": "key", "sl_insights": "id", "sl_jobs": "id", "sl_settings": "key"}
        for t, k in order.items():
            sq = f"select coalesce(json_agg(r order by r.{k}), '[]')::text from public.{t} r"
            a, b = q(src, sq), q(dst, sq)
            check(f"{t} 원본과 같음 ({len(json.loads(a))}행)", a == b, "다름")
        cols = "id,aud,role,email,email_confirmed_at,last_sign_in_at,raw_app_meta_data,raw_user_meta_data,created_at,updated_at"
        uq = f"select coalesce(json_agg(json_build_array({cols}) order by id), '[]')::text from auth.users where id in ('{U1}','{U2}')"
        check("로그인 계정(해시 외 열) 원본과 같음", q(src, uq) == q(dst, uq))
        iq = f"select coalesce(json_agg(json_build_array(id,user_id,identity_data,provider,provider_id) order by user_id), '[]')::text from auth.identities where user_id in ('{U1}','{U2}')"
        check("로그인 신원 원본과 같음", q(src, iq) == q(dst, iq))
        check("다른 서비스 사용자는 옮겨지지 않음", q(dst, f"select count(*) from auth.users where id='{U3}'") == "0")
        check("같은 id 로 있던 계정의 비밀번호는 유지(해시 없는 덤프가 지우지 않음)", q(dst, f"select encrypted_password from auth.users where id='{U2}'") == BOOT)
        check("덤프로 새로 생긴 계정은 비밀번호 없음(set-admin-password.sh 대상)",
              q(dst, f"select encrypted_password is null from auth.users where id='{U1}'") == "t")
        check("같은 이메일·다른 id 부트스트랩 계정은 지워지고 신원도 함께 지워짐",
              q(dst, f"select (select count(*) from auth.users where id='{U9}') + (select count(*) from auth.identities where user_id='{U9}')") == "0")
        # GoTrue 가 실제로 쓰는 조회 조건 — FindUserByID / FindUserByEmailAndAudience
        check("GoTrue 조회 조건으로 관리자 2명 모두 찾힘(instance_id·토큰 열)",
              q(dst, f"""select count(*) from auth.users where instance_id='{NIL}' and id in ('{U1}','{U2}')
                         and confirmation_token is not null and recovery_token is not null
                         and email_change_token_new is not null and email_change is not null""") == "2")
        check("이메일 로그인 조회 조건으로도 찾힘",
              q(dst, f"select count(*) from auth.users where instance_id='{NIL}' and lower(email)='owner@example.test' and aud='authenticated'") == "1")
        nxt = int(q(dst, "select nextval(pg_get_serial_sequence('public.sl_audit','id'))"))
        mx = int(q(src, "select max(id) from public.sl_audit"))
        check(f"감사 로그 번호가 이어진다(다음 {nxt} > 최대 {mx})", nxt == mx + 1)
        check(f"감사 로그 {n_audit}행 — 적재 중 트리거로 늘지 않음", q(dst, "select count(*) from public.sl_audit") == str(n_audit))
        # ── 경로 A(pg_dump) — 머리말 필터가 여러 줄 값 속 "SET…" 줄을 지우지 않는지
        dst2 = T.PG()
        try:
            schema(dst2); dst2.psql(file=os.path.join(DEPLOY, "db/03-seed-public.sql"))
            outa = os.path.join(work, "export-a"); os.makedirs(outa)
            tabs = []
            for t in order: tabs += ["-t", f"public.{t}"]
            dumpa = subprocess.run([f"{T.BIN}/pg_dump", "-h", src.dir, "-p", str(src.port), "-U", "postgres", "-d", "postgres",
                                    "--data-only", "--column-inserts", "--no-owner", "--no-privileges"] + tabs,
                                   capture_output=True, text=True, check=True).stdout
            open(os.path.join(outa, "public-data.sql"), "w", encoding="utf-8").write(dumpa)
            for f in ("auth-users.csv", "auth-identities.csv"):
                subprocess.run(["cp", os.path.join(out, f), outa], check=True)
            psql2 = f"{T.BIN}/psql -h {dst2.dir} -p {dst2.port} -U postgres -d postgres -v ON_ERROR_STOP=1 -q -X"
            r = subprocess.run(["bash", os.path.join(HERE, "import-to-server.sh"), outa],
                               env={**os.environ, "SL_PSQL": psql2, "SL_ASSUME_YES": "1"}, capture_output=True, text=True)
            check("경로 A(pg_dump) 적재 실행", r.returncode == 0, (r.stderr or r.stdout)[-600:])
            sq = "select coalesce(json_agg(r order by r.id), '[]')::text from public.sl_inquiries r"
            check("경로 A: 'SET…' 으로 시작하는 줄이 든 문의 본문이 그대로", q(src, sq) == q(dst2, sq), "다름")
        finally:
            dst2.stop()
    finally:
        src.stop(); dst.stop()
        subprocess.run(["rm", "-rf", work])
    print("통과" if ok else "실패")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
