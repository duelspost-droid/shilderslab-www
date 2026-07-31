#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사이트 도메인 일괄 교체.

왜 상수가 아니라 스크립트인가
  콘텐츠 파일(`content_*.py`)에는 **CSS 중괄호가 섞인 긴 문자열**이 들어 있다.
  f-string 으로 바꾸면 `{` 를 전부 이스케이프해야 하고, 한 군데만 놓쳐도 빌드가 깨진다.
  도메인 교체는 자주 있는 일이 아니므로, 리터럴을 그대로 두고 이 스크립트로 한 번에 바꾼다.

무엇을 바꾸는가
  코드·정적 파일·생성물의 도메인 문자열 전부. **CNAME 은 건드리지 않는다** —
  그건 GitHub Pages 호스팅 바인딩이라 DNS 전환과 함께 움직여야 한다(3항 참조).

사용법
  python3 tools/set-domain.py --to shielduslab.com          # 미리보기(변경 안 함)
  python3 tools/set-domain.py --to shielduslab.com --apply  # 실제 교체
  python3 tools/build-pages.py                              # 반드시 재빌드
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 교체 대상. CNAME 은 의도적으로 제외한다(호스팅 바인딩 — DNS 전환 시 함께 바꾼다).
TARGETS = [
    "tools/shell.py", "tools/build-pages.py", "tools/build-card.py",
    "tools/content_home.py", "tools/content_pages.py", "tools/content_services.py",
    "tools/content_resources.py", "tools/content_trust.py", "tools/content_dynamic.py",
    "tools/content_legal.py", "tools/content_blocks.py",
    "config.js", "admin/admin.js", "robots.txt", ".well-known/security.txt",
    "supabase/functions/notify-inquiry/index.ts",
    "supabase/functions/sl-admin-user/index.ts",
]
# 생성물도 함께(재빌드로 덮이지만, 빌드 전 상태가 어긋나 보이지 않게)
GENERATED_GLOB = (".html", ".xml")

KNOWN = ["shilderslab.com", "shielduslab.com", "shilduslab.com"]


def files():
    out = [os.path.join(ROOT, t) for t in TARGETS]
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in
                   (".git", "node_modules", "assets", "supabase", "tools", ".venv")]
        for n in names:
            if n.endswith(GENERATED_GLOB):
                out.append(os.path.join(base, n))
    return [p for p in out if os.path.exists(p)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="새 도메인 (예: shielduslab.com)")
    ap.add_argument("--apply", action="store_true", help="실제로 파일을 고친다")
    a = ap.parse_args()
    new = a.to.strip().lower()
    if not re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", new):
        raise SystemExit(f"도메인 형식이 아닙니다: {new}")
    olds = [d for d in KNOWN if d != new]

    total, touched = 0, []
    for path in files():
        try:
            s = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        n = sum(s.count(o) for o in olds)
        if not n:
            continue
        total += n
        touched.append((os.path.relpath(path, ROOT), n))
        if a.apply:
            for o in olds:
                s = s.replace(o, new)
            open(path, "w", encoding="utf-8").write(s)

    for rel, n in sorted(touched, key=lambda r: -r[1]):
        print(f"  {n:4d}  {rel}")
    print(f"\n  총 {total}건 / {len(touched)}개 파일 → {new}")
    if not a.apply:
        print("  (미리보기입니다. 실제 교체는 --apply)")
    else:
        print("  ⚠ CNAME 은 바꾸지 않았습니다 — DNS 전환 시 함께 처리하십시오.")
        print("  다음: python3 tools/build-pages.py")


if __name__ == "__main__":
    main()
