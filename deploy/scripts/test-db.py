#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DB 계층 사전 검증 — **Docker 없이** 실제 PostgreSQL 16 에서 이관 SQL 패키지를 끝까지 돌린다.

왜 필요한가
  이관에서 가장 조용히 깨지는 곳이 DB 계층이다 — 롤·auth 헬퍼·적용 순서·RLS.
  틀려도 에러가 아니라 "관리자가 아무것도 못 보는" 상태로 나타난다.
  배포 전에 이 스크립트로 확인한다.

무엇을 하는가
  임시 클러스터를 만들어 SPEC 7항 3단계(init-db.sh)와 같은 순서로 적용한 뒤,
  PostgREST 가 넣어 주는 요청 문맥(request.jwt.claims · request.headers)을 흉내 내
  anon / 관리자 / 비관리자 로그인 각각의 권한을 실제로 시험한다.

GoTrue 는 대역을 쓴다
  auth.users · auth.identities 를 마이그레이션이 쓰는 컬럼으로 직접 만든다.
  그리고 **GoTrue 가 auth.uid() 를 옛 방식으로 덮어쓰는 상황을 일부러 재현**해,
  init-db.sh 의 재적용이 그것을 바로잡는지 확인한다.

실행
  pip install pgserver        # PostgreSQL 16 바이너리 동봉 (또는 PG_BIN=/usr/lib/postgresql/16/bin)
  python3 deploy/scripts/test-db.py
"""
import json, os, shutil, socket, subprocess, sys, tempfile, time, uuid, glob

HERE = os.path.dirname(os.path.abspath(__file__))
DEPLOY = os.path.dirname(HERE)
ROOT = os.path.dirname(DEPLOY)

def find_bin():
    if os.environ.get("PG_BIN"):
        return os.environ["PG_BIN"]
    try:
        import pgserver
        return os.path.join(os.path.dirname(pgserver.__file__), "pginstall", "bin")
    except ImportError:
        sys.exit("PostgreSQL 바이너리가 없습니다. pip install pgserver 또는 PG_BIN 지정")

BIN = find_bin()
PASS, FAIL = [], []

def ok(m):  PASS.append(m); print(f"  ✅ {m}")
def ng(m, why): FAIL.append(m); print(f"  ❌ {m} — {why}")

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

class PG:
    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="shieldus-pgtest-")
        self.data = os.path.join(self.dir, "data")
        self.port = free_port()
        subprocess.run([f"{BIN}/initdb", "-D", self.data, "-U", "postgres", "-A", "trust",
                        "-E", "UTF8", "--no-locale"], check=True, capture_output=True)
        subprocess.run([f"{BIN}/pg_ctl", "-D", self.data, "-o",
                        f"-p {self.port} -k {self.dir} -c listen_addresses=''",
                        "-l", os.path.join(self.dir, "log"), "-w", "start"],
                       check=True, capture_output=True)

    def psql(self, sql=None, file=None, user="postgres", check=True, tuples=True):
        cmd = [f"{BIN}/psql", "-h", self.dir, "-p", str(self.port), "-U", user, "-d", "postgres",
               "-v", "ON_ERROR_STOP=1", "-q", "-X"]
        if tuples: cmd += ["-tA"]
        if file: cmd += ["-f", file]
        r = subprocess.run(cmd, input=sql, capture_output=True, text=True)
        if check and r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip()[:600])
        return r

    def stop(self):
        subprocess.run([f"{BIN}/pg_ctl", "-D", self.data, "-m", "immediate", "stop"],
                       capture_output=True)
        shutil.rmtree(self.dir, ignore_errors=True)

def as_role(pg, role, claims, headers=None, sql=""):
    """PostgREST 요청 하나를 흉내 낸다 — 롤 전환 + JWT 클레임 + 요청 헤더."""
    # set_config 의 반환값이 출력에 섞이면 마지막 줄 판정이 틀어진다(NULL 이 빈 줄로 나오는데
    # 그걸 건너뛰고 앞 줄의 '{}' 를 집었다). 준비 문장은 출력을 버린다.
    pre = ("\\o /dev/null\n"
           f"set role {role};\n"
           f"select set_config('request.jwt.claims', '{json.dumps(claims)}', false);\n"
           f"select set_config('request.headers', '{json.dumps(headers or {})}', false);\n"
           "\\o\n")
    return pg.psql(pre + sql, check=False)

def last(r):
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    return lines[-1] if lines else ""

def main():
    print(f"PostgreSQL: {subprocess.run([f'{BIN}/postgres','--version'],capture_output=True,text=True).stdout.strip()}")
    pg = PG()
    try:
        # ─── 1) 롤·auth 부트스트랩 ───
        print("\n▶ 1. 01-roles-auth.sql")
        pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
        roles = pg.psql("select string_agg(rolname, ',' order by rolname) from pg_roles "
                        "where rolname in ('anon','authenticated','service_role','authenticator','supabase_auth_admin')").stdout.strip()
        ok(f"롤 5개 생성 ({roles})") if roles.count(",") == 4 else ng("롤 생성", roles)

        # ─── 2) GoTrue 대역 + '옛 방식 덮어쓰기' 재현 ───
        print("\n▶ 2. GoTrue 대역 — auth.users 생성 + auth.uid() 를 옛 방식으로 덮어쓰기")
        pg.psql("""
          set role supabase_auth_admin;
          create table if not exists auth.users (
            id uuid primary key, aud text, role text, email text unique,
            encrypted_password text, email_confirmed_at timestamptz, last_sign_in_at timestamptz,
            raw_app_meta_data jsonb, raw_user_meta_data jsonb,
            created_at timestamptz default now(), updated_at timestamptz default now());
          create table if not exists auth.identities (
            id text, user_id uuid, identity_data jsonb, provider text, provider_id text,
            last_sign_in_at timestamptz, created_at timestamptz, updated_at timestamptz,
            primary key (provider, provider_id));
          -- GoTrue 의 옛 마이그레이션이 하던 정의(클레임별 GUC 만 읽는다)
          create or replace function auth.uid() returns uuid language sql stable as $$
            select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
        """)
        test_uid = str(uuid.uuid4())
        r = as_role(pg, "authenticated", {"sub": test_uid, "role": "authenticated"}, sql="select auth.uid();")
        if last(r) == "":
            ok("함정 재현 — 옛 방식 auth.uid() 는 PostgREST 12 클레임에서 NULL")
        else:
            ng("함정 재현", f"NULL 이 아님({last(r)}) — 재현 실패")

        # ─── 3) 재적용으로 복구 (init-db.sh 4단계) ───
        print("\n▶ 3. 01-roles-auth.sql 재적용 (init-db.sh 4단계)")
        pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
        r = as_role(pg, "authenticated", {"sub": test_uid, "role": "authenticated"}, sql="select auth.uid();")
        ok("새 방식 클레임 → auth.uid() 복구") if last(r) == test_uid else ng("새 방식 auth.uid()", last(r) or r.stderr[:120])
        r = pg.psql(f"set role authenticated; select set_config('request.jwt.claim.sub','{test_uid}',false); select auth.uid();", check=False)
        ok("옛 방식 클레임 → auth.uid() 도 동작") if last(r) == test_uid else ng("옛 방식 auth.uid()", last(r))

        # ─── 4) 마이그레이션 0001~0007 ───
        print("\n▶ 4. 마이그레이션 0001~0007")
        for f in sorted(glob.glob(os.path.join(ROOT, "supabase/migrations/0*.sql"))):
            try:
                pg.psql(file=f); ok(os.path.basename(f))
            except RuntimeError as e:
                ng(os.path.basename(f), str(e)[:200]); raise

        # ─── 5) 공개 시드 (트리거 끔) ───
        print("\n▶ 5. 공개 시드 03-seed-public.sql")
        seed = open(os.path.join(DEPLOY, "db/03-seed-public.sql"), encoding="utf-8").read()
        audit_before = pg.psql("select count(*) from sl_audit").stdout.strip()   # 0005 가 남긴 행은 제외
        pg.psql("set session_replication_role = replica;\n" + seed)
        cnt = pg.psql("select (select count(*) from sl_content)||'/'||(select count(*) from sl_insights)||'/'||"
                      "(select count(*) from sl_jobs)||'/'||(select count(*) from sl_settings)").stdout.strip()
        ok(f"content/insights/jobs/settings = {cnt}")
        audit = pg.psql("select count(*) from sl_audit").stdout.strip()
        ok(f"시드 적재가 감사 로그를 만들지 않음(트리거 꺼짐 · {audit_before}→{audit})") if audit == audit_before \
            else ng("시드 감사 로그", f"{audit_before}→{audit}행 — 트리거가 켜진 채 적재됨")

        # ─── 5-b) 재실행 안전 — init-db.sh 를 한 번 더 돌린 것과 같은 순서 ───
        print("\n▶ 5-b. 재실행 안전 (01 → 0001~0007 → 03 두 번째)")
        try:
            pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
            for f in sorted(glob.glob(os.path.join(ROOT, "supabase/migrations/0*.sql"))):
                pg.psql(file=f)
            pg.psql("set session_replication_role = replica;\n" + seed)
            cnt2 = pg.psql("select (select count(*) from sl_content)||'/'||(select count(*) from sl_insights)||'/'||"
                           "(select count(*) from sl_jobs)||'/'||(select count(*) from sl_settings)").stdout.strip()
            ok(f"두 번째 적용 무사 · 행 수 불변({cnt2})") if cnt2 == cnt else ng("재실행 행 수", f"{cnt} → {cnt2}")
        except RuntimeError as e:
            ng("재실행 안전", str(e)[:200])

        # ─── 6) 구조 ───
        print("\n▶ 6. 최종 구조")
        pol = pg.psql("select count(*) from pg_policies where schemaname='public'").stdout.strip()
        ok(f"RLS 정책 {pol}개") if pol == "18" else ng("RLS 정책 수", f"{pol} (명세 18)")
        rls = pg.psql("select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace "
                      "where n.nspname='public' and c.relkind='r' and c.relrowsecurity").stdout.strip()
        ok(f"RLS 활성 테이블 {rls}개") if rls == "8" else ng("RLS 활성 테이블", rls)
        fns = pg.psql("select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public'").stdout.strip()
        ok(f"public 함수 {fns}개") if fns == "27" else ng("함수 수", f"{fns} (명세 27)")

        # ─── 7) anon — 비로그인 방문자 ───
        print("\n▶ 7. anon (비로그인) 권한")
        anon = {"role": "anon"}
        hdr = {"x-forwarded-for": "203.0.113.7"}
        for t in ("sl_inquiries", "sl_applications", "sl_admins", "sl_audit"):
            r = as_role(pg, "anon", anon, hdr, f"select count(*) from public.{t};")
            v = last(r)
            if r.returncode != 0 or v == "0":
                ok(f"anon → {t} 읽기 0행/거부")
            else:
                ng(f"anon → {t}", f"{v}행 노출")
        r = as_role(pg, "anon", anon, hdr, "select count(*) from public.sl_content;")
        ok(f"anon → sl_content 읽기 {last(r)}행") if last(r) not in ("", "0") else ng("anon 공개 문구", r.stderr[:120])
        r = as_role(pg, "anon", anon, hdr, "insert into public.sl_inquiries(company,name,email,message) values('x','x','x@x.x','x');")
        ok("anon → 개인정보 테이블 직접 INSERT 거부") if r.returncode != 0 else ng("anon 직접 INSERT", "허용됨")
        for fn in ("sl_stats", "sl_admin_list", "sl_purge_all"):
            r = as_role(pg, "anon", anon, hdr, f"select public.{fn}();")
            ok(f"anon → {fn}() 거부") if r.returncode != 0 else ng(f"anon → {fn}()", "실행됨")
        r = as_role(pg, "anon", anon, hdr,
                    "select public.sl_submit_inquiry('검증','검증','v@example.invalid','','기타','동의 없음',false);")
        ok("동의 없는 문의 거부") if r.returncode != 0 else ng("동의 없는 문의", "접수됨")
        r = as_role(pg, "anon", anon, hdr,
                    "select public.sl_submit_inquiry('주식회사 검증','홍길동','v@example.invalid','010-0000-0000','ISMS-P','이관 검증용 문의입니다',true);")
        ok("동의한 문의 접수 성공(RPC 경로)") if r.returncode == 0 else ng("정상 문의 접수", r.stderr.strip()[:160])
        ip = pg.psql("select ip from public.sl_audit where kind='submit' order by created_at desc limit 1").stdout.strip()
        ok(f"X-Forwarded-For → 감사 로그 IP 기록 ({ip})") if ip.startswith("203.0.113.7") else ng("IP 기록", f"'{ip}' — 레이트리밋 근거 없음")

        # ─── 8) 관리자 / 비관리자 로그인 ───
        print("\n▶ 8. 로그인 사용자 권한")
        admin_id, other_id = str(uuid.uuid4()), str(uuid.uuid4())
        pg.psql(f"""
          insert into auth.users(id,aud,role,email,email_confirmed_at)
            values ('{admin_id}','authenticated','authenticated','admin@test.local',now()),
                   ('{other_id}','authenticated','authenticated','other@test.local',now());
          insert into public.sl_admins(email,role,note,user_id)
            values ('admin@test.local','admin','테스트',(select id from auth.users where email='admin@test.local'))
            on conflict (lower(email)) do update set user_id=excluded.user_id, role='admin';
        """)
        adm = {"sub": admin_id, "role": "authenticated", "email": "admin@test.local"}
        oth = {"sub": other_id, "role": "authenticated", "email": "other@test.local"}
        r = as_role(pg, "authenticated", adm, sql="select public.is_sl_admin();")
        ok("관리자 → is_sl_admin() = true") if last(r) == "t" else ng("관리자 판정", last(r) or r.stderr[:160])
        r = as_role(pg, "authenticated", adm, sql="select count(*) from public.sl_inquiries;")
        ok(f"관리자 → 문의 열람 {last(r)}건") if last(r) not in ("", "0") else ng("관리자 문의 열람", last(r) or r.stderr[:160])
        r = as_role(pg, "authenticated", adm, sql="select count(*) from public.sl_admin_list();")
        ok(f"관리자 → 계정 목록 {last(r)}행") if r.returncode == 0 else ng("관리자 계정 목록", r.stderr[:160])
        r = as_role(pg, "authenticated", oth, sql="select public.is_sl_admin();")
        ok("비관리자 로그인 → is_sl_admin() = false") if last(r) == "f" else ng("비관리자 판정", last(r))
        r = as_role(pg, "authenticated", oth, sql="select count(*) from public.sl_inquiries;")
        ok("비관리자 로그인 → 문의 0행") if last(r) == "0" or r.returncode != 0 else ng("비관리자 문의", f"{last(r)}행 노출")
        # 이메일만 같고 user_id 가 다른 계정 — '빈 관리자 슬롯' 탈취 시나리오(0004)
        spoof = {"sub": str(uuid.uuid4()), "role": "authenticated", "email": "admin@test.local"}
        r = as_role(pg, "authenticated", spoof, sql="select public.is_sl_admin();")
        ok("이메일만 같은 다른 계정 → 관리자 아님(user_id 결속)") if last(r) == "f" else ng("이메일 위조", "관리자로 인정됨")

        # ─── 9) 운영 ───
        print("\n▶ 9. 운영 함수")
        r = pg.psql("select public.sl_purge_all();", check=False)
        ok("보존기간 파기 sl_purge_all() 실행") if r.returncode == 0 else ng("파기 함수", r.stderr[:160])
    except Exception as e:
        ng("실행 중단", str(e)[:300])
    finally:
        pg.stop()

    print(f"\n결과: 통과 {len(PASS)} · 실패 {len(FAIL)}")
    sys.exit(1 if FAIL else 0)

if __name__ == "__main__":
    main()
