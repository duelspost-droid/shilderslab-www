#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`content_blocks.py` 의 default 를 **페이지 HTML 리터럴에 맞춰 자동 정렬**한다.

왜 필요한가
  같은 '코드 기본값' 이 두 곳에 있다 — `content_blocks.py` 의 default(시드·관리자 화면)와
  `content_*.py` 의 `data-content` 안쪽(빌드 폴백). 카피를 고치면 후자만 바뀌어 둘이 갈라진다.
  실제로 갈라진 적이 있다(2026-08-01 services.hero_lead).
  손으로 옮겨 적지 말고 이 스크립트로 맞춘다.

사용
  python3 tools/align-blocks.py          # 차이만 보여준다
  python3 tools/align-blocks.py --apply  # content_blocks.py 를 실제로 고친다
  → 이어서 python3 tools/gen-content-seed.py 로 0005 를 재생성한다.
"""
import argparse
import io
import os
import re
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)

spec_path = os.path.join(SRC, "sync-content.py")


def load_sync():
    import importlib.util
    spec = importlib.util.spec_from_file_location("sync_content", spec_path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def q(s):
    """파이썬 소스에 넣을 문자열 리터럴. 줄바꿈은 \\n 으로, 따옴표는 이스케이프."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    sc = load_sync()
    code = sc.code_defaults()          # key -> 평문/마크다운 (HTML 리터럴에서 추출)
    import content_blocks

    path = os.path.join(SRC, "content_blocks.py")
    src = io.open(path, encoding="utf-8").read()

    changed, skipped = [], []
    for b in content_blocks.BLOCKS:
        k = b["key"]
        if k not in code:
            continue
        want = code[k]
        if " ".join(str(b["default"]).split()) == " ".join(want.split()):
            continue
        # default=... 를 키가 속한 dict 블록 안에서만 교체한다.
        #   기존 값은 한 줄 문자열일 수도, 여러 줄 괄호 묶음(default=( "..." "..." ))일 수도 있다.
        #   **괄호까지 통째로** 먹어야 한다. 안 그러면 잉여 ')' 가 남아 파일이 깨진다(실제로 겪음).
        m = re.search(r'(key="' + re.escape(k) + r'"\b.*?\bdefault=)(\(.*?\)|"(?:[^"\\]|\\.)*")',
                      src, re.S)
        if not m:
            skipped.append(k)
            continue
        src = src[:m.start(2)] + q(want) + src[m.end(2):]
        changed.append(k)

    print(f"정렬 대상 {len(changed)}개" + (f" · 패턴 불일치로 건너뜀 {len(skipped)}개" if skipped else ""))
    for k in changed:
        print("  -", k)
    for k in skipped:
        print("  ! 수동 확인 필요:", k)

    if a.apply and changed:
        io.open(path, "w", encoding="utf-8", newline="\n").write(src)
        import ast
        ast.parse(io.open(path, encoding="utf-8").read())
        print("\n  ✓ content_blocks.py 갱신 · 파싱 OK")
        print("  다음: python3 tools/gen-content-seed.py")
    elif not a.apply:
        print("\n  (미리보기입니다. 실제 반영은 --apply)")


if __name__ == "__main__":
    main()
