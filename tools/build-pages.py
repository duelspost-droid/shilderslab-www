#!/usr/bin/env python3
"""
쉴더스랩 정적 사이트 빌더 v2
  · 모든 페이지를 이 빌더로 생성한다(홈·서비스 포함) — 손으로 쓴 예외 페이지 없음.
  · 셸(head/masthead/footer)은 tools/shell.py 한 곳에서 관리한다.
  · sitemap.xml 은 정적 페이지 + CMS 공개 인사이트로 빌드 시 생성한다.
사용: python3 tools/build-pages.py
"""
import os, sys, json, re, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell  # noqa: E402


import content_blocks  # noqa: E402

# 빌드 시작 시 한 번 채운다(fetch_content). key -> {"value":…, "kind":…}
CONTENT = {}

# data-content 를 단 요소의 안쪽 전체를 교체한다.
#   여는 태그를 잡고, 같은 태그명으로 닫힐 때까지를 비탐욕으로 문다.
#   → data-content 요소 안에 같은 태그를 중첩하면 안 된다(content_blocks.py 주석 참조).
_CONTENT_RE = re.compile(r'(<(\w+)\b[^>]*\bdata-content="([^"]+)"[^>]*>)(.*?)(</\2>)', re.S)


def render_block(key, value):
    """저장된 평문/마크다운 → HTML. 이스케이프가 먼저이므로 원문 HTML은 출력되지 않는다."""
    if content_blocks.kind_of(key) == "rich":
        return md(value)
    return esc(value).replace("\n", "<br>")


def apply_content(html):
    """DB 값이 있는 블록만 갈아끼운다. 비어 있으면 코드에 박힌 기본 문구를 그대로 둔다
       — 관리자가 실수로 비워도 페이지가 빈칸이 되지 않게."""
    if not CONTENT:
        return html

    def rep(m):
        key = m.group(3)
        row = CONTENT.get(key)
        if not row:
            return m.group(0)
        v = (row.get("value") or "").strip()
        if not v:
            return m.group(0)
        return m.group(1) + render_block(key, v) + m.group(5)

    return _CONTENT_RE.sub(rep, html)


def page(path, title, desc, body, canonical, extra_css="", extra_js="", ld="", body_attr=""):
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
{shell.head(title, desc, canonical, extra_css, ld)}
</head>
<body{(' ' + body_attr) if body_attr else ''}>

{shell.masthead()}

<main>
{body}
</main>

{shell.FOOTER}

{shell.SCRIPTS}
{extra_js}
</body>
</html>
"""
    html = apply_content(html)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path:<36} {len(html):>7,}B")
    return path


def _rest(path):
    """anon 키로 REST 조회. 공개 읽기 권한이 있는 테이블만 대상으로 한다."""
    cfg = open(os.path.join(ROOT, "config.js"), encoding="utf-8").read()
    url = re.search(r'SUPABASE_URL:\s*"([^"]+)"', cfg).group(1)
    key = re.search(r'SUPABASE_ANON_KEY:\s*"([^"]+)"', cfg).group(1)
    req = urllib.request.Request(
        f"{url}/rest/v1/{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def fetch_insights():
    """공개 인사이트 전문(빌드 시점) — 정적 페이지 생성용. 실패해도 빌드는 계속한다."""
    try:
        return _rest("sl_insights?select=slug,category,title,summary,body,author,published_at"
                     "&published=eq.true&order=sort_order.desc,published_at.desc&limit=500")
    except Exception as e:
        print(f"  ! 인사이트 조회 실패({e.__class__.__name__}) — 정적 글 페이지 생략")
        return []


def fetch_content():
    """관리자가 고친 문구를 빌드 시점에 구워 넣기 위해 읽는다.
       0005 미적용이거나 네트워크가 없으면 조용히 비운다 — 그 경우 코드 기본 문구로 빌드된다."""
    try:
        rows = _rest("sl_content?select=key,value,kind&limit=500")
    except Exception as e:
        print(f"  ! 콘텐츠 조회 실패({e.__class__.__name__}) — 코드 기본 문구로 빌드합니다"
              f" (0005 마이그레이션 미적용이면 정상)")
        return {}
    out = {r["key"]: r for r in rows if r.get("key")}
    filled = sum(1 for r in out.values() if (r.get("value") or "").strip())
    unknown = [k for k in out if k not in content_blocks.BY_KEY]
    if unknown:
        print(f"  ! DB 에만 있는 블록 {len(unknown)}개 — 페이지에 자리가 없어 무시합니다: {', '.join(unknown[:5])}")
    missing = [b["key"] for b in content_blocks.BLOCKS if b["key"] not in out]
    if missing:
        print(f"  ! DB 에 없는 블록 {len(missing)}개 — 코드 기본값 사용(0005 재적용 필요): {', '.join(missing[:5])}")
    print(f"  · 콘텐츠 블록 {len(out)}개 조회 · 값이 채워진 것 {filled}개")
    return out


def esc(v):
    return (str(v if v is not None else "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def md(src):
    """assets/js/supa.js 의 클라이언트 렌더러와 동일한 최소 마크다운 → HTML.
       이스케이프를 먼저 하므로 원문 HTML은 절대 출력되지 않는다."""
    import re as _re
    safe = esc(src)
    out, lst = [], None

    def close():
        nonlocal lst
        if lst:
            out.append(f"<{lst[0]}>" + "".join(lst[1]) + f"</{lst[0]}>")
            lst = None

    for raw in safe.split("\n"):
        line = raw.strip()
        if not line:
            close(); continue
        m = _re.match(r"^(#{2,3})\s+(.*)$", line)
        if m:
            close(); n = len(m.group(1)); out.append(f"<h{n}>{m.group(2)}</h{n}>"); continue
        m = _re.match(r"^[-*]\s+(.*)$", line)
        if m:
            if not lst or lst[0] != "ul":
                close(); lst = ("ul", [])
            lst[1].append(f"<li>{m.group(1)}</li>"); continue
        m = _re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            if not lst or lst[0] != "ol":
                close(); lst = ("ol", [])
            lst[1].append(f"<li>{m.group(1)}</li>"); continue
        if line.startswith("&gt;"):
            close(); out.append("<blockquote>" + _re.sub(r"^&gt;\s?", "", line) + "</blockquote>"); continue
        close(); out.append(f"<p>{line}</p>")
    close()
    html = "\n".join(out)
    html = _re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", html)
    html = _re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    def link(m2):
        txt, url = m2.group(1), m2.group(2).replace("&amp;", "&")
        if url.startswith("http://") or url.startswith("https://"):
            return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{txt}</a>'
        if url.startswith("/") and not url.startswith("//"):
            return f'<a href="{esc(url)}">{txt}</a>'
        return txt

    return _re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, html)


def fmt_date(v):
    s2 = str(v or "")[:10]
    return s2.replace("-", ".") if len(s2) == 10 else s2


def build_insight_pages(posts):
    """공개 글마다 정적 페이지를 만든다 — 크롤러·SNS가 본문과 메타를 바로 읽을 수 있게."""
    made = []
    for p in posts:
        slug = p.get("slug") or ""
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
            continue
        title = p.get("title") or slug
        summary = (p.get("summary") or "").strip()
        cat = p.get("category") or "인사이트"
        author = p.get("author") or "쉴더스랩"
        date = p.get("published_at") or ""
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "Article",
            "headline": title, "description": summary[:160],
            "datePublished": str(date)[:10],
            "author": {"@type": "Organization", "name": author},
            "publisher": {"@type": "Organization", "name": "쉴더스랩",
                          "logo": {"@type": "ImageObject",
                                   "url": "https://shilderslab.com/assets/ci/symbol.svg"}},
            "mainEntityOfPage": f"https://shilderslab.com/insights/{slug}/",
        }, ensure_ascii=False)
        body = f"""<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · <a href="/insights/">인사이트</a></div>
    <div class="lbl" style="margin-bottom:18px">{esc(cat)} &nbsp;·&nbsp; {esc(fmt_date(date))} &nbsp;·&nbsp; {esc(author)}</div>
    <h1 class="d2">{esc(title)}</h1>
    {f'<p class="lead" style="margin-top:20px;max-width:58ch">{esc(summary)}</p>' if summary else ""}
  </div>
</section>

<section class="sec">
  <div class="shell">
    <article class="article">
      <div class="body">
{md(p.get("body") or "")}
      </div>
      <div style="margin-top:56px;padding-top:24px;border-top:1px solid var(--ink);display:flex;
                  gap:16px;flex-wrap:wrap;justify-content:space-between;align-items:center">
        <a class="alink" href="/insights/">인사이트 목록</a>
        <a class="btn btn-sm" href="/contact/">이 주제로 상담 요청</a>
      </div>
    </article>
  </div>
</section>"""
        page(f"insights/{slug}/index.html", f"{title} | 쉴더스랩 인사이트",
             (summary or title)[:150], body, f"/insights/{slug}/", ld=ld)
        made.append((f"/insights/{slug}/", str(date)[:10] or None))
    return made


def build_sitemap(rows_static, rows_posts):
    today = datetime.date.today().isoformat()
    rows = [(p, today, pr) for p, pr in rows_static]
    rows += [(u, d or today, "0.7") for u, d in rows_posts]

    def x(v):
        return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    body = "\n".join(
        f"  <url><loc>https://shilderslab.com{x(loc)}</loc>"
        f"<lastmod>{lm}</lastmod><priority>{pr}</priority></url>" for loc, lm, pr in rows)
    out = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ sitemap.xml                        {len(rows)} URL")


def url_of(path):
    u = "/" + path
    return u[:-len("index.html")] if u.endswith("/index.html") else u


def main():
    import content_home as H
    import content_services as S
    import content_pages as P
    import content_resources as R
    import content_trust as T
    import content_legal as L
    import content_dynamic as D

    global CONTENT
    print("콘텐츠(CMS):")
    CONTENT = fetch_content()

    print("페이지 생성:")
    static = []

    def add(path, prio, *a, **kw):
        static.append((url_of(page(path, *a, **kw)), prio))

    add("index.html", "1.0", H.TITLE, H.DESC, H.BODY, "/", H.CSS, H.JS, H.LD)

    add("services/index.html", "0.9", S.TITLE, S.DESC, S.BODY, "/services/", S.CSS)
    for svc in S.DETAILS:
        add(f"services/{svc['slug']}/index.html", "0.8", svc["title"], svc["desc"], svc["body"],
            f"/services/{svc['slug']}/", S.DETAIL_CSS)

    add("method/index.html", "0.8", P.METHOD_TITLE, P.METHOD_DESC, P.METHOD_BODY, "/method/", P.METHOD_CSS)

    add("resources/index.html", "0.8", R.RES_TITLE, R.RES_DESC, R.RES_BODY, "/resources/", R.RES_CSS)
    for doc in R.RES_DOCS:
        add(f"resources/{doc['slug']}/index.html", "0.7", doc["title"], doc["desc"], doc["body"],
            f"/resources/{doc['slug']}/", R.DOC_CSS)

    add("regulations/index.html", "0.8", T.REG_TITLE, T.REG_DESC, T.REG_BODY, "/regulations/", T.REG_CSS)
    add("trust/index.html", "0.7", T.TRUST_TITLE, T.TRUST_DESC, T.TRUST_BODY, "/trust/", T.TRUST_CSS)

    add("about/index.html", "0.7", P.ABOUT_TITLE, P.ABOUT_DESC, P.ABOUT_BODY, "/about/", P.ABOUT_CSS,
        ld=P.ABOUT_LD)
    add("brand/index.html", "0.4", P.BRAND_TITLE, P.BRAND_DESC, P.BRAND_BODY, "/brand/", P.BRAND_CSS)

    add("insights/index.html", "0.8", D.INS_TITLE, D.INS_DESC, D.INS_BODY, "/insights/",
        D.INS_CSS, D.INS_JS, D.INS_LD)
    add("careers/index.html", "0.6", D.CAR_TITLE, D.CAR_DESC, D.CAR_BODY, "/careers/", D.CAR_CSS, D.CAR_JS)
    add("contact/index.html", "0.9", D.CON_TITLE, D.CON_DESC, D.CON_BODY, "/contact/",
        D.CON_CSS, D.CON_JS, D.CON_LD)

    add("legal/privacy.html", "0.3", L.PRIVACY_TITLE, L.PRIVACY_DESC, L.PRIVACY_BODY,
        "/legal/privacy.html", L.CSS)
    add("legal/terms.html", "0.3", L.TERMS_TITLE, L.TERMS_DESC, L.TERMS_BODY,
        "/legal/terms.html", L.CSS)

    # 인사이트: CMS 공개분을 정적 페이지로 생성(크롤러·SNS 대응) + 동적 폴백 유지
    print("인사이트 정적 생성:")
    posts = fetch_insights()
    made = build_insight_pages(posts)
    if not made:
        print("  · 생성된 글 없음")
    page("insights/view.html", D.VIEW_TITLE, D.VIEW_DESC, D.VIEW_BODY, "/insights/view.html",
         extra_js=D.VIEW_JS)

    page("404.html", P.NF_TITLE, P.NF_DESC, P.NF_BODY, "/404.html", extra_js=P.NF_JS)

    print("사이트맵:")
    build_sitemap(static, made)
    print("완료.")


if __name__ == "__main__":
    main()
