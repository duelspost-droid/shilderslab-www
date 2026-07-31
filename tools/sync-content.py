#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""페이지 문구 CMS 동기화 — 코드 기본값을 DB(sl_content)에 반영하는 SQL 생성

왜 필요한가
  0005 이후 18개 블록은 **DB 값이 코드 기본값을 이긴다.** build-pages.py 가 빌드 시점에
  DB 값을 읽어 data-content 요소 안쪽을 통째로 교체하기 때문이다.
  따라서 `tools/content_*.py` 의 문구만 고치면 빌드하는 순간 DB 값으로 되돌아가고,
  **수정이 조용히 사라진다.** 이 스크립트는 그 간극을 메운다.

무엇을 보장하는가
  생성되는 UPDATE 는 `where value = <이전 값>` 조건을 단다.
  즉 **오너가 콘솔에서 고친 문구는 절대 덮어쓰지 않는다.**
  값이 이미 바뀌어 있으면 그 행은 0 rows updated 로 조용히 건너뛴다(그리고 아래 리포트에 표시된다).

사용법
  python3 tools/sync-content.py            # 차이만 보여준다(읽기 전용)
  python3 tools/sync-content.py --sql      # 적용할 SQL 을 출력한다
  → 출력된 SQL 을 Supabase SQL Editor 에서 실행한 뒤 `python3 tools/build-pages.py` 로 재빌드.

주의
  data-content 요소 **안쪽 HTML 을 그대로** 넣지 않는다. DB 에는 평문/최소 마크다운만 저장한다
  (0005 규약 — 빌드·클라이언트 양쪽이 이스케이프 후 렌더한다). 여기서도 태그를 벗겨서 비교·생성한다.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FILES = ["content_pages.py", "content_home.py", "content_services.py",
             "content_trust.py", "content_dynamic.py", "shell.py"]

# data-content 요소의 여는 태그 / 키 / 안쪽 / 닫는 태그
ANCHOR = re.compile(r'<(\w+)\b[^>]*\bdata-content="([^"]+)"[^>]*>(.*?)</\1>', re.S)


def cfg():
    """config.js 에서 URL 과 anon 키를 읽는다(레포에 있는 공개 키)."""
    s = open(os.path.join(ROOT, "config.js"), encoding="utf-8").read()
    url = re.search(r'https://[a-z0-9]+\.supabase\.co', s)
    key = re.search(r'(?:ANON_KEY|anonKey|publishable\w*)\s*[:=]\s*["\']([^"\']+)', s)
    if not (url and key):
        raise SystemExit("config.js 에서 Supabase URL/anon 키를 찾지 못했습니다.")
    return url.group(0), key.group(1)


def plain(html):
    """앵커 안쪽 HTML → DB 저장 규약(평문 + 최소 마크다운).

    순서가 중요하다. 소스의 줄바꿈은 **코드 가독성을 위한 줄맞춤**일 뿐이라 공백으로 접어야 하고,
    의미가 있는 줄바꿈(<br>)과 문단 경계(</p><p>)는 그 뒤에 넣어야 한다.
    반대로 하면 줄맞춤까지 줄바꿈으로 굳어 DB 값과 영원히 어긋난다.
      1) 강조 <b>/<strong> → ** (DB 는 마크다운으로 저장한다)
      2) 모든 공백·줄바꿈을 공백 하나로 접는다
      3) <br> → 줄바꿈, </p><p> → 빈 줄
      4) 남은 태그 제거 · 엔티티 복원
    """
    t = re.sub(r'</?(?:b|strong)>', '**', html)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s*</p>\s*<p[^>]*>\s*', '\n\n', t)
    t = re.sub(r'\s*<br\s*/?>\s*', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = (t.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
          .replace('&amp;', '&').replace('&middot;', '·'))
    t = re.sub(r'[ \t]+', ' ', t)
    return "\n".join(line.strip() for line in t.split("\n")).strip()


def code_defaults():
    out = {}
    for f in SRC_FILES:
        p = os.path.join(ROOT, "tools", f)
        if not os.path.exists(p):
            continue
        for m in ANCHOR.finditer(open(p, encoding="utf-8").read()):
            out[m.group(2)] = plain(m.group(3))
    return out


def db_values(url, key):
    req = urllib.request.Request(
        f"{url}/rest/v1/sl_content?select=key,value&limit=500",
        headers={"apikey": key, "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        rows = json.load(r)
    return {r["key"]: (r.get("value") or "") for r in rows}


def q(s):
    return "'" + s.replace("'", "''") + "'"


def main():
    want_sql = "--sql" in sys.argv
    url, key = cfg()
    code, db = code_defaults(), db_values(url, key)

    changed, missing, absent = [], [], []
    for k, new in sorted(code.items()):
        if k not in db:
            absent.append(k)
            continue
        old = (db[k] or "").strip()
        if old == new.strip():
            continue
        changed.append((k, old, new.strip()))
    for k in sorted(db):
        if k not in code and (db[k] or "").strip():
            missing.append(k)

    if not want_sql:
        print(f"코드 앵커 {len(code)}개 · DB 행 {len(db)}개")
        print(f"차이 {len(changed)}개\n")
        for k, old, new in changed:
            print(f"── {k}")
            print(f"   DB  : {old[:88]}")
            print(f"   코드: {new[:88]}")
        if absent:
            print(f"\n! DB 에 없는 키 {len(absent)}개(0005 재적용 필요): {', '.join(absent)}")
        if missing:
            print(f"! 코드에 앵커가 없는 DB 키 {len(missing)}개: {', '.join(missing)}")
        if changed:
            print("\n적용할 SQL 을 보려면: python3 tools/sync-content.py --sql")
        return

    if not changed:
        print("-- 차이 없음. 실행할 것이 없습니다.")
        return

    print("-- 페이지 문구 동기화 (tools/sync-content.py 생성)")
    print("-- 각 UPDATE 는 '값이 아직 이전 상태일 때만' 적용된다 →")
    print("-- 오너가 콘솔에서 이미 고친 문구는 건드리지 않는다(0 rows 로 지나감).")
    print("begin;")
    for k, old, new in changed:
        print(f"\nupdate public.sl_content set value = {q(new)}\n"
              f" where key = {q(k)} and value = {q(old)};")
    print("\n-- 확인: 위 UPDATE 가 전부 반영됐는지")
    print("select key, length(value) as len from public.sl_content")
    print(f" where key in ({', '.join(q(k) for k, _, _ in changed)}) order by key;")
    print("commit;")


if __name__ == "__main__":
    main()
