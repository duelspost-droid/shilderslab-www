#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""공개 데이터 시드 내보내기 — db/03-seed-public.sql 을 다시 만든다.

언제 쓰나
  **이관 당일에 다시 돌린다.** 시드는 실행 시점 스냅숏이라, 그 뒤 오너가 콘솔에서 문구를
  고쳤다면 낡은 값이 새 서버에 들어간다. (공개 키로 읽으므로 비밀 없이 누구나 돌릴 수 있다.)

타입을 안다
  컬럼 타입을 마이그레이션 파일에서 읽어, jsonb 컬럼은 **스칼라 문자열까지 JSON 으로 감싼다.**
  예전 버전은 sl_settings.value 를 'contact@…' 처럼 그냥 써서, 새 서버 적재 때
  `invalid input syntax for type json` 으로 실패했다(test-db.py 가 잡음).

  python3 deploy/scripts/export-public.py
"""
import datetime, glob, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(os.path.dirname(HERE), "db", "03-seed-public.sql")
TABLES = [("sl_settings", "key"), ("sl_content", "key"), ("sl_insights", "id"), ("sl_jobs", "id")]

def col_types():
    """마이그레이션에서 테이블별 컬럼 타입을 읽는다(create table + 이후 alter add)."""
    sql = "\n".join(open(f, encoding="utf-8").read()
                    for f in sorted(glob.glob(os.path.join(ROOT, "supabase/migrations/*.sql"))))
    types = {}
    for m in re.finditer(r'create table if not exists public\.(\w+)\s*\((.*?)\n\);', sql, re.S):
        t = types.setdefault(m.group(1), {})
        for line in m.group(2).split("\n"):
            p = line.strip().split()
            if len(p) >= 2 and not p[0].startswith("--") and p[0] not in (
                    "constraint", "primary", "unique", "check", "foreign"):
                t[p[0]] = p[1].rstrip(",").lower()
    for tb, c, ty in re.findall(r'alter table public\.(\w+) add column if not exists (\w+) (\w+)', sql):
        types.setdefault(tb, {})[c] = ty.lower()
    return types

def lit(v, ty):
    if v is None:
        return "null"
    if ty in ("jsonb", "json"):
        # 스칼라든 객체든 **항상** JSON 텍스트로 만든 뒤 캐스팅한다.
        return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::" + ty
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (dict, list)):
        return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"

def main():
    cfg = open(os.path.join(ROOT, "config.js"), encoding="utf-8").read()
    url = os.environ.get("SRC_URL") or re.search(r'https://[a-z0-9]+\.supabase\.co', cfg).group(0)
    key = os.environ.get("SRC_ANON_KEY") or re.search(
        r'(?:ANON_KEY|anonKey|publishable\w*)\s*[:=]\s*["\']([^"\']+)', cfg).group(1)
    types = col_types()

    out = [f"""-- ═══════════════════════════════════════════════════════════════════
-- 공개 데이터 시드 — 라이브에서 공개 키(anon)로 내보낸 실데이터
--   생성: {datetime.datetime.now().isoformat(timespec='seconds')}  ·  원본: {url}
--   생성기: deploy/scripts/export-public.py  ← 이관 당일 다시 돌릴 것(스냅숏이다)
--   포함: sl_settings · sl_content · sl_insights · sl_jobs
--   ⚠ 미포함: sl_admins · sl_inquiries · sl_applications · sl_audit · auth.users
--             RLS 로 공개 키에 0행 → 오너가 scripts/export-from-supabase.sh 로 뜬다.
--   적재: init-db.sh 가 session_replication_role=replica(트리거 끔)로 넣는다.
-- 재실행 안전: 테이블마다 비우고 라이브 상태로 다시 채운다(라이브가 정본).
-- ═══════════════════════════════════════════════════════════════════
begin;"""]
    total = 0
    for t, pk in TABLES:
        req = urllib.request.Request(f"{url}/rest/v1/{t}?select=*&order={pk}",
                                     headers={"apikey": key, "Authorization": f"Bearer {key}"})
        rows = json.load(urllib.request.urlopen(req, timeout=30))
        if not rows:
            out.append(f"\n-- ── {t}: 0행 ──"); continue
        cols = list(rows[0].keys())
        unknown = [c for c in cols if c not in types.get(t, {})]
        if unknown:
            sys.exit(f"✗ {t} 의 컬럼 {unknown} 타입을 마이그레이션에서 찾지 못했습니다 — 스키마 불일치")
        upd = ", ".join(f"{c} = excluded.{c}" for c in cols if c != pk)
        out.append(f"\n-- ── {t} ({len(rows)}행) ──")
        # 🚨 비우고 채운다. 0002·0005 마이그레이션의 초기값과 라이브 값이 **slug 는 같고 id 가 다르다.**
        #    id 로만 upsert 하면 slug 유일 제약에 걸려 실패한다(test-db.py 가 잡음).
        #    이 네 테이블은 라이브가 정본이므로 통째로 라이브 상태로 맞춘다.
        out.append(f"delete from public.{t};")
        for r in rows:
            vals = ", ".join(lit(r[c], types[t][c]) for c in cols)
            out.append(f"insert into public.{t} ({', '.join(cols)}) values ({vals})\n"
                       f"  on conflict ({pk}) do update set {upd};")
        total += len(rows)
        print(f"  ✓ {t:12s} {len(rows):3d}행")
    out.append("\ncommit;\n")
    open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print(f"  → {os.path.relpath(OUT, ROOT)}  ({total}행, {os.path.getsize(OUT):,}B)")

if __name__ == "__main__":
    main()
