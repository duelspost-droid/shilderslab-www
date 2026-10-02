#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""일반 서버 이관 패키지(납품용 파일 묶음)를 만든다 — 어느 PC 에서든 같은 결과.

    python3 deploy/scripts/build-package.py            # dist/쉴더스랩_서버이관_패키지_<날짜>/
    python3 deploy/scripts/build-package.py --zip      # + zip · SHA256SUMS

왜 스크립트인가
  dist/ 는 소스 사본과 (나중에) 개인정보 덤프가 들어가므로 gitignore 다. 그래서 **다른 PC 로
  따라가지 않는다.** 대신 이 스크립트를 커밋해 두고 어디서든 다시 만든다.

필요한 것
  · git · python3
  · ~/.venvs/sl (또는 현재 파이썬) 에 pgserver — 최종스키마·테이블정의서를 실제 PG16 에서 뽑는다
      python3 -m venv ~/.venvs/sl && ~/.venvs/sl/bin/pip install pgserver
    없으면 그 두 산출물만 건너뛰고 나머지는 만든다.

구성
  00_먼저읽기.txt
  01_명세서/      SPEC.md 사본 (+ docx·pdf — 생성기 미구현, HANDOFF 13항)
  02_소스코드/    git archive HEAD — 커밋된 것만이라 .env 같은 비밀이 섞일 수 없다
  03_DB/1_스키마/ 적용 순서 번호를 붙인 사본 + 적용순서.txt
  03_DB/2_데이터/ 공개데이터.sql(실행 시점 라이브 스냅숏) · 비공개데이터/(오너 덤프 자리)
  03_DB/          최종스키마_참조용.sql · 테이블정의서.md/.csv (실 PG 카탈로그 추출)
"""
import argparse, csv, datetime, glob, hashlib, importlib.util, json, os, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEPLOY = os.path.dirname(HERE)
ROOT = os.path.dirname(DEPLOY)

# ── 테이블 정의서용 설명 (카탈로그에는 없는 사람용 설명) ──────────────────────
META = {
 "sl_inquiries":   ("상담·견적 문의", "🔴 이름·이메일·전화", "접수 1년 후 자동 파기", "RPC `sl_submit_inquiry` 만 (INSERT 정책 없음)"),
 "sl_applications":("채용 지원", "🔴 이름·이메일·전화", "접수 6개월 후 자동 파기", "RPC `sl_apply` 만 (INSERT 정책 없음)"),
 "sl_audit":       ("방문·관리자 행위·제출 이벤트 로그", "🟡 IP·User-Agent", "방문 90일 · 관리/제출 365일 후 자동 파기", "RPC `sl_log`·`sl_log_visit`, 트리거"),
 "sl_admins":      ("관리자 화이트리스트(역할 admin/editor)", "🟡 이메일", "수동", "RPC `sl_admin_*` 만"),
 "sl_content":     ("페이지 문구 CMS", "없음", "—", "관리자 콘솔"),
 "sl_insights":    ("인사이트 글", "없음", "—", "관리자 콘솔"),
 "sl_jobs":        ("채용 공고", "없음", "—", "관리자 콘솔"),
 "sl_settings":    ("사이트 설정(key-value)", "없음", "—", "관리자 콘솔"),
}
DESC = {
"sl_admins":{"email":"관리자 이메일(소문자). 화이트리스트 키","role":"역할 — admin(계정·설정·로그 포함 전체) / editor(콘텐츠·문의)","note":"메모","created_at":"등록 시각","user_id":"결속된 로그인 계정 ID(auth.users.id). **NULL 이면 권한 없음**","pw_managed":"콘솔이 비밀번호를 만든 계정 여부. service_role 만 변경 가능(트리거)"},
"sl_applications":{"id":"지원 ID","name":"🔴 지원자 이름","email":"🔴 지원자 이메일","phone":"🔴 지원자 전화","position":"지원 포지션","summary":"자기소개 요약","link":"이력서·포트폴리오 링크","status":"처리 상태 new/doing/done/drop","admin_note":"관리자 메모","ip":"제출 IP(레이트리밋·감사)","user_agent":"제출 브라우저","consent_at":"개인정보 수집·이용 동의 시각","created_at":"접수 시각 — 보존기간 기준","updated_at":"수정 시각"},
"sl_audit":{"id":"일련번호(IDENTITY)","kind":"구분 visit / admin / submit","actor":"행위자 계정 ID","actor_email":"행위자 이메일","action":"행위","entity":"대상 객체","entity_id":"대상 ID","detail":"상세(JSON)","ip":"요청 IP","user_agent":"요청 브라우저","created_at":"기록 시각 — 보존기간 기준"},
"sl_content":{"key":"블록 키(예: home.hero_title). 페이지의 data-content 앵커와 일치","value":"문구(평문·최소 마크다운. HTML 저장 안 함)","kind":"text / rich","section":"콘솔 분류","label":"콘솔 표시 이름","hint":"콘솔 도움말","sort_order":"콘솔 정렬 순서","updated_at":"수정 시각","updated_by":"수정한 관리자 계정 ID"},
"sl_inquiries":{"id":"문의 ID","company":"회사명","name":"🔴 담당자 이름","email":"🔴 담당자 이메일","phone":"🔴 담당자 전화","service":"문의 유형","message":"문의 내용","status":"처리 상태 new/doing/done/drop","admin_note":"관리자 메모","ip":"제출 IP(레이트리밋·감사)","user_agent":"제출 브라우저","consent_at":"개인정보 수집·이용 동의 시각","created_at":"접수 시각 — 보존기간 기준","updated_at":"수정 시각"},
"sl_insights":{"id":"글 ID","slug":"URL 경로(유일) — /insights/<slug>/","category":"분류","title":"제목","summary":"요약","body":"본문(최소 마크다운)","author":"작성자","published":"공개 여부","published_at":"게시일","sort_order":"정렬 순서","created_at":"생성 시각","updated_at":"수정 시각"},
"sl_jobs":{"id":"공고 ID","title":"포지션명","team":"소속 팀","employment_type":"고용 형태","location":"근무지","summary":"요약","body":"상세(최소 마크다운)","closes_at":"마감일(NULL = 상시)","published":"공개 여부","sort_order":"정렬 순서","created_at":"생성 시각","updated_at":"수정 시각"},
"sl_settings":{"key":"설정 키(대표 이메일·운영 시간·회신 안내·공지 배너 등)","value":"값(JSON)","updated_at":"수정 시각"},
}
ORDER = ["sl_inquiries","sl_applications","sl_audit","sl_admins","sl_content","sl_insights","sl_jobs","sl_settings"]

APPLY_ORDER_TXT = """스키마 적용 순서 — 반드시 이 순서대로 (자동화: 02_소스코드/shilderslab-www/deploy/scripts/init-db.sh)

  1_롤_인증부트스트랩.sql        롤 5개 · auth 헬퍼 · Supabase 기본 권한 재현
  1b_롤_비밀번호설정.sh          롤 비밀번호를 .env 값으로 (Docker 는 자동 실행)
  2 ※ 인증 서버(GoTrue)를 한 번 기동해 auth.users 테이블이 생기게 한다
  1_롤_인증부트스트랩.sql        ← 한 번 더. GoTrue 가 auth.uid() 를 옛 방식으로 덮어썼을 수 있다
  3_0001 ~ 9_0007                마이그레이션 7개 (파일명 숫자 순)
  다음 → 2_데이터/공개데이터.sql (트리거를 끈 세션에서: set session_replication_role = replica;)

⚠ 순서를 어기면
  · 1 없이 0001 → 즉시 실패 (anon 등 롤이 없다)
  · GoTrue 이전에 0004 → 실패 (auth.users 를 조인한다)
  · 1 재적용 생략 → 에러 없이 관리자가 아무것도 못 보는 상태가 될 수 있다 (명세서 13항)

이 파일들은 02_소스코드/shilderslab-www/ 의 deploy/db · supabase/migrations 와 같은 내용이다.
실행 스크립트는 02_소스코드 쪽에서 돌린다(상대 경로를 쓴다).
"""
PRIVATE_TXT = """비공개 데이터 — 이 폴더는 비어 있는 것이 정상이다

들어갈 것: 문의 · 채용 지원 · 관리자 목록 · 감사 로그 · 로그인 계정(비밀번호 해시 포함)
공개 키로는 0행이라(RLS 정상 동작) 패키지 빌드가 뽑을 수 없다. 오너가 직접 뜬다.

  cd 02_소스코드/shilderslab-www/deploy
  SUPABASE_DB_URL='postgresql://postgres:<비밀번호>@db.<ref>.supabase.co:5432/postgres' \\
    bash scripts/export-from-supabase.sh
  → deploy/export/ 에 public-data.sql · auth-users.csv · auth-identities.csv 가 생긴다

🔴 개인정보와 비밀번호 해시가 들어 있다. 암호화된 경로로만 옮기고, 이관 후 양쪽 모두 지운다.
   (shred -u export/*)  패키지를 업체에 넘길 때 이 폴더를 채운 채로 보내지 말 것 — 덤프는 별도 경로로.
"""

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def step_source(pkg):
    dst = os.path.join(pkg, "02_소스코드"); os.makedirs(dst, exist_ok=True)
    tar = subprocess.run(["git", "-C", ROOT, "archive", "--format=tar", "--prefix=shilderslab-www/", "HEAD"],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", dst], input=tar, check=True)
    head = run(["git", "-C", ROOT, "log", "--oneline", "-1"]).stdout.strip()
    n = sum(len(f) for _, _, f in os.walk(dst))
    leaks = [os.path.join(r, f) for r, _, fs in os.walk(dst) for f in fs if f == ".env"]
    if leaks: sys.exit(f"✗ 소스 사본에 .env 가 있다: {leaks}")
    print(f"  ✓ 02_소스코드 — {n}파일 · 커밋 {head}")
    return head

def step_db_files(pkg):
    s = os.path.join(pkg, "03_DB", "1_스키마"); os.makedirs(s, exist_ok=True)
    os.makedirs(os.path.join(pkg, "03_DB", "2_데이터", "비공개데이터"), exist_ok=True)
    shutil.copy(os.path.join(DEPLOY, "db/01-roles-auth.sql"), os.path.join(s, "1_롤_인증부트스트랩.sql"))
    shutil.copy(os.path.join(DEPLOY, "db/01b-role-passwords.sh"), os.path.join(s, "1b_롤_비밀번호설정.sh"))
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "supabase/migrations/0*.sql"))), 3):
        shutil.copy(f, os.path.join(s, f"{i}_{os.path.basename(f)}"))
    open(os.path.join(s, "적용순서.txt"), "w", encoding="utf-8").write(APPLY_ORDER_TXT)
    open(os.path.join(pkg, "03_DB", "2_데이터", "비공개데이터", "안내.txt"), "w", encoding="utf-8").write(PRIVATE_TXT)
    # 공개 데이터는 실행 시점 라이브에서 다시 뜬다(스냅숏)
    r = subprocess.run([sys.executable, os.path.join(HERE, "export-public.py")], capture_output=True, text=True)
    if r.returncode == 0:
        shutil.copy(os.path.join(DEPLOY, "db/03-seed-public.sql"), os.path.join(pkg, "03_DB/2_데이터/공개데이터.sql"))
        print("  ✓ 03_DB 스키마 9 · 공개데이터 — " + r.stdout.strip().splitlines()[-1].strip())
    else:
        shutil.copy(os.path.join(DEPLOY, "db/03-seed-public.sql"), os.path.join(pkg, "03_DB/2_데이터/공개데이터.sql"))
        print("  ⚠ 라이브 재추출 실패 — 커밋된 시드를 대신 넣었다(날짜 확인): " + (r.stderr or r.stdout).strip()[:120])

def step_catalog(pkg):
    """실제 PG16 에 적용한 뒤 최종 스키마 DDL 과 테이블 정의서를 뽑는다."""
    spec = importlib.util.spec_from_file_location("testdb", os.path.join(HERE, "test-db.py"))
    t = importlib.util.module_from_spec(spec)
    argv = sys.argv; sys.argv = [argv[0]]
    try:
        spec.loader.exec_module(t)
    except SystemExit as e:
        sys.argv = argv
        print(f"  ⚠ 최종스키마·테이블정의서 건너뜀 — {e} (pip install pgserver)"); return
    sys.argv = argv
    pg = t.PG()
    try:
        pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
        pg.psql("""set role supabase_auth_admin;
          create table if not exists auth.users (id uuid primary key, aud text, role text, email text unique,
            encrypted_password text, email_confirmed_at timestamptz, last_sign_in_at timestamptz,
            raw_app_meta_data jsonb, raw_user_meta_data jsonb,
            created_at timestamptz default now(), updated_at timestamptz default now());""")
        pg.psql(file=os.path.join(DEPLOY, "db/01-roles-auth.sql"))
        for f in sorted(glob.glob(os.path.join(ROOT, "supabase/migrations/0*.sql"))): pg.psql(file=f)
        ddl = run([f"{t.BIN}/pg_dump", "-h", pg.dir, "-p", str(pg.port), "-U", "postgres", "-d", "postgres",
                   "--schema-only", "--no-owner", "-n", "public"]).stdout
        open(os.path.join(pkg, "03_DB/최종스키마_참조용.sql"), "w", encoding="utf-8").write(
            "-- 최종 스키마 (참조용) — 마이그레이션 0001~0007 을 실제 PostgreSQL 16 에 적용한 결과\n"
            "--   ⚠ 이 파일로 DB 를 만들지 말 것. 적용은 1_스키마/ 를 순서대로(init-db.sh).\n"
            "--   생성: deploy/scripts/build-package.py → pg_dump --schema-only -n public\n\n" + ddl)
        q = lambda s: [l.split("|") for l in pg.psql(s).stdout.strip().splitlines() if l]
        cols = q(r"""select c.relname, a.attnum, a.attname, format_type(a.atttypid,a.atttypmod), a.attnotnull,
               coalesce(pg_get_expr(d.adbin,d.adrelid),''), a.attidentity,
               exists(select 1 from pg_index i where i.indrelid=c.oid and i.indisprimary and a.attnum=any(i.indkey))
          from pg_class c join pg_namespace n on n.oid=c.relnamespace
          join pg_attribute a on a.attrelid=c.oid and a.attnum>0 and not a.attisdropped
          left join pg_attrdef d on d.adrelid=c.oid and d.adnum=a.attnum
         where n.nspname='public' and c.relkind='r' order by c.relname,a.attnum""")
        cons = [l.split("|", 2) for l in pg.psql(r"""select conrelid::regclass::text, conname, pg_get_constraintdef(oid)
          from pg_constraint where connamespace='public'::regnamespace and contype in ('u','c') order by 1,2""").stdout.strip().splitlines()]
        pols = [l.split("|", 5) for l in pg.psql(r"""select tablename, policyname, cmd, array_to_string(roles,','),
          coalesce(qual,''), coalesce(with_check,'') from pg_policies where schemaname='public' order by 1,2""").stdout.strip().splitlines()]
        idx = [l.split("|", 2) for l in pg.psql(r"""select tablename, indexname, indexdef from pg_indexes
          where schemaname='public' order by 1,2""").stdout.strip().splitlines()]
        trg = [l.split("|", 2) for l in pg.psql(r"""select event_object_table, trigger_name,
          action_timing||' '||string_agg(event_manipulation,'/') from information_schema.triggers
          where trigger_schema='public' group by 1,2,action_timing order by 1,2""").stdout.strip().splitlines()]
    finally:
        pg.stop()
    write_definition(pkg, cols, cons, pols, idx, trg)

def write_definition(pkg, cols, cons, pols, idx, trg):
    TYPE = {"timestamp with time zone": "timestamptz"}
    by = {}
    for t, n, c, ty, nn, df, ident, pk in cols:
        by.setdefault(t, []).append((int(n), c, TYPE.get(ty, ty), nn == "t", df, ident, pk == "t"))
    short = lambda x: (lambda y: y if len(y) <= 22 else y[:21] + "…")(x.replace("::text", "").replace("::jsonb", ""))
    md = ["# 쉴더스랩 DB 테이블 정의서", "",
          "마이그레이션 0001~0007 을 **실제 PostgreSQL 16 에 적용한 결과의 시스템 카탈로그**에서 뽑았다.",
          "`NN` = NOT NULL · `PK` = 기본키 · 🔴 개인정보 · 🟡 준개인정보", ""]
    rows = [["테이블", "순번", "컬럼", "타입", "NOT NULL", "기본값", "PK", "설명"]]
    for i, t in enumerate(ORDER, 1):
        pur, pii, ret, wr = META[t]
        md += [f"## {i}. `{t}` — {pur}", "", "| 항목 | 내용 |", "|---|---|",
               f"| 개인정보 | {pii} |", f"| 보존기간 | {ret} |", f"| 쓰기 경로 | {wr} |", "",
               "| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |", "|---|---|---|---|---|---|---|"]
        for n, c, ty, nn, df, ident, pk in sorted(by.get(t, [])):
            dfv = "IDENTITY" if ident in ("a", "d") else short(df)
            d = DESC.get(t, {}).get(c, "")
            md.append(f"| {n} | `{c}` | {ty} | {'✓' if nn else ''} | {('`' + dfv + '`') if dfv else ''} | {'✓' if pk else ''} | {d} |")
            rows.append([t, n, c, ty, "Y" if nn else "", dfv, "Y" if pk else "", d.replace("**", "")])
        cs = [x for x in cons if x[0] == t]
        ix = [x for x in idx if x[0] == t and not x[1].endswith("_pkey")]
        po = [x for x in pols if x[0] == t]
        tr = [x for x in trg if x[0] == t]
        if cs: md += ["", "**제약**", ""] + [f"- `{x[1]}` — `{x[2][:90]}`" for x in cs]
        if ix: md += ["", "**인덱스**", ""] + [f"- `{x[1]}`" for x in ix]
        md += ["", "**RLS 정책** " + ("(없음 — RLS 활성이므로 **모든 직접 접근 거부**)" if not po else f"({len(po)}개)"), ""]
        for x in po:
            cond = (x[4] or x[5]).replace("\n", " ")
            md.append(f"- `{x[1]}` — {x[2]} · 대상 `{x[3]}` · 조건 `{cond[:70]}{'…' if len(cond) > 70 else ''}`")
        if tr: md += ["", "**트리거**", ""] + [f"- `{x[1]}` — {x[2]}" for x in tr]
        md.append("")
    open(os.path.join(pkg, "03_DB/테이블정의서.md"), "w", encoding="utf-8").write("\n".join(md))
    with open(os.path.join(pkg, "03_DB/테이블정의서.csv"), "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"  ✓ 최종스키마_참조용.sql · 테이블정의서.md/.csv — 테이블 {len(by)} · 컬럼 {len(rows)-1} · "
          f"정책 {len(pols)} · 인덱스 {len(idx)} · 트리거 {len(trg)}")

def step_docs(pkg):
    d = os.path.join(pkg, "01_명세서"); os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(DEPLOY, "SPEC.md"), os.path.join(d, "쉴더스랩_일반서버_이관명세서.md"))
    # docx · pdf 생성기는 아직 없다 — HANDOFF 13항. 만들어지면 여기서 부른다.
    for gen, ext in (("render-spec-docx.js", "docx"), ("render-spec-pdf.py", "pdf")):
        if os.path.exists(os.path.join(HERE, gen)):
            print(f"  · {gen} 실행 — (구현 시 연결)")
    print("  ✓ 01_명세서 — SPEC.md 사본 (docx·pdf 미생성: HANDOFF 13항)")

def step_readme(pkg, head, stamp):
    txt = f"""쉴더스랩 웹사이트 — 일반 서버 이관 패키지
생성 {stamp} · 소스 커밋 {head}

먼저 읽을 것
  01_명세서/쉴더스랩_일반서버_이관명세서   — 0장(선택지) → 7장(절차) 순서로
    · 설치 방식: Docker Compose(권장) 또는 직접 설치
    · 웹 서버  : nginx(권장) 또는 Apache httpd
    · DB       : PostgreSQL (선택 불가 — 명세서 2.2)
    · WAS(Tomcat 등): 필요 없음 (명세서 2.1)

구성
  01_명세서/  설계·선택지·절차·검증·운영·롤백·테이블 정의서(부록 D)
  02_소스코드/shilderslab-www/
              웹사이트 전체 소스(커밋된 파일만 — 비밀 없음)
              deploy/  ← 서버 구성(docker-compose · nginx · apache · 스크립트)
  03_DB/      1_스키마(적용 순서 번호) · 2_데이터 · 최종스키마_참조용 · 테이블정의서(md·csv)

비공개 데이터(문의·지원·관리자·로그인 계정)는 이 패키지에 없다 — 03_DB/2_데이터/비공개데이터/안내.txt
배포 전 DB 사전 검증: 02_소스코드/shilderslab-www 에서  python3 deploy/scripts/test-db.py
"""
    open(os.path.join(pkg, "00_먼저읽기.txt"), "w", encoding="utf-8").write(txt)

def step_zip(pkg):
    sums = []
    for r, _, fs in os.walk(pkg):
        for f in sorted(fs):
            p = os.path.join(r, f)
            sums.append(f"{hashlib.sha256(open(p,'rb').read()).hexdigest()}  {os.path.relpath(p, pkg)}")
    open(os.path.join(pkg, "SHA256SUMS.txt"), "w", encoding="utf-8").write("\n".join(sorted(sums, key=lambda x: x[66:])) + "\n")
    z = pkg + ".zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for r, _, fs in os.walk(pkg):
            for f in fs:
                p = os.path.join(r, f); zf.write(p, os.path.relpath(p, os.path.dirname(pkg)))
    print(f"  ✓ {os.path.relpath(z, ROOT)} ({os.path.getsize(z)/1e6:.1f}MB) · SHA256SUMS {len(sums)}개")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--zip", action="store_true")
    ap.add_argument("--stamp", default=datetime.date.today().strftime("%Y%m%d"))
    a = ap.parse_args()
    pkg = os.path.join(ROOT, "dist", f"쉴더스랩_서버이관_패키지_{a.stamp}")
    private = os.path.join(pkg, "03_DB/2_데이터/비공개데이터")
    if os.path.isdir(private) and any(f != "안내.txt" for f in os.listdir(private)):
        sys.exit("✗ 비공개데이터 폴더에 덤프가 있다 — 지우고 다시 만들면 사라진다. 먼저 옮겨 두라.")
    shutil.rmtree(pkg, ignore_errors=True); os.makedirs(pkg)
    print(f"▶ {os.path.relpath(pkg, ROOT)}")
    head = step_source(pkg); step_db_files(pkg); step_catalog(pkg); step_docs(pkg)
    step_readme(pkg, head, a.stamp)
    if a.zip: step_zip(pkg)
    print("완료")

if __name__ == "__main__":
    main()
