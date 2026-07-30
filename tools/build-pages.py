#!/usr/bin/env python3
"""
쉴더스랩 정적 페이지 빌더
  · 공용 셸(head/nav/footer)을 한 곳에서 관리하고, 페이지별 body만 정의해 정적 HTML을 생성한다.
  · 출력은 100% 정적 HTML(런타임 조립 없음) → SEO·GitHub Pages 그대로 호환.
  · sync_shell(): 손으로 쓴 페이지(index.html, services/index.html)의 <header>/<footer> 블록도
    이 템플릿 기준으로 덮어써 드리프트를 방지한다.
사용: python3 tools/build-pages.py            # 전체 생성 + 셸 동기화
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA_HOST = "https://nrdapzgtibbusvoaceuh.supabase.co"
SUPA_WS = "wss://nrdapzgtibbusvoaceuh.supabase.co"

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; "
       f"connect-src 'self' {SUPA_HOST} {SUPA_WS}; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none'")

NAV = """<header class="nav" id="nav">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="쉴더스랩 홈">
      <img class="mark" src="/assets/ci/symbol.svg" alt="" width="38" height="38">
      <span class="txt"><b>쉴더스랩</b><span>SHILDERS LAB</span></span>
    </a>
    <nav class="menu" id="menu" aria-label="주요 메뉴">
      <a href="/services/">서비스</a>
      <a href="/about/">회사소개</a>
      <a href="/insights/">인사이트</a>
      <a href="/careers/">채용</a>
      <a class="nav-cta" href="/contact/">상담 · 견적 요청</a>
    </nav>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>"""

FOOTER = """<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/ci/lockup-horizontal-dark.svg" alt="쉴더스랩 SHILDERS LAB" height="42" style="height:42px;width:auto">
        <p>정보보호 컨설팅 전문기업. 규제 대응과 공격자 관점의 기술 진단을 한 팀에서 수행합니다.</p>
      </div>
      <div class="foot-col">
        <h5>Services</h5>
        <a href="/services/#isms">ISMS-P 인증 컨설팅</a>
        <a href="/services/#pentest">모의해킹 · 침투테스트</a>
        <a href="/services/#vuln">취약점 진단</a>
        <a href="/services/#privacy">개인정보 컴플라이언스</a>
        <a href="/services/#cloud">클라우드 보안</a>
      </div>
      <div class="foot-col">
        <h5>Company</h5>
        <a href="/about/">회사소개</a>
        <a href="/insights/">인사이트</a>
        <a href="/careers/">채용</a>
        <a href="/brand/">브랜드 · CI</a>
        <a href="/contact/">문의</a>
      </div>
      <div class="foot-col">
        <h5>Contact</h5>
        <a href="mailto:contact@shilderslab.com">contact@shilderslab.com</a>
        <span>평일 09:00 – 18:00</span>
        <a href="/contact/">상담 · 견적 요청 →</a>
      </div>
    </div>
    <div class="legal">
      <div>
        <div class="biz" id="bizline"></div>
        <div class="copy">© <span data-year>2026</span> SHILDERS LAB. All rights reserved.</div>
      </div>
      <div class="legal-links">
        <a href="/legal/privacy.html">개인정보처리방침</a>
        <a href="/legal/terms.html">이용약관</a>
        <a href="/admin/">관리자</a>
      </div>
    </div>
  </div>
</footer>"""

SCRIPTS = """<script src="/config.js"></script>
<script src="/assets/vendor/supabase.min.js"></script>
<script src="/assets/js/supa.js"></script>
<script src="/assets/js/site.js"></script>"""


def page(path, title, desc, body, canonical, extra_css="", extra_js="", ld=""):
    head_extra = f"\n<style>\n{extra_css}\n</style>" if extra_css else ""
    ld_block = f'\n<script type="application/ld+json">\n{ld}\n</script>' if ld else ""
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://shilderslab.com{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="쉴더스랩">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://shilderslab.com{canonical}">
<meta property="og:image" content="https://shilderslab.com/assets/ci/og-cover.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/ci/favicon.svg" type="image/svg+xml">
<link rel="mask-icon" href="/assets/ci/mask-icon.svg" color="#12B5CE">
<link rel="apple-touch-icon" href="/assets/ci/apple-touch-icon.png">
<meta name="theme-color" content="#050B16">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">{head_extra}{ld_block}
</head>
<body>
<div class="progress" id="progress"></div>

{NAV}

{body}

{FOOTER}

{SCRIPTS}
{extra_js}
</body>
</html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path}  ({len(html):,}B)")


def build_all():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import content_static as S, content_legal as L, content_dynamic as D

    page("about/index.html",
         "회사소개 | 쉴더스랩 — 정보보호 컨설팅",
         "쉴더스랩(SHILDERS LAB)은 2026년 설립된 정보보호 컨설팅 기업입니다. 관리체계 인증 컨설팅과 실제 공격 관점의 기술 진단을 한 팀에서 수행합니다.",
         S.ABOUT_BODY, "/about/", extra_css=S.ABOUT_CSS,
         ld='{"@context":"https://schema.org","@type":"AboutPage","name":"회사소개 | 쉴더스랩",'
            '"url":"https://shilderslab.com/about/"}')

    page("brand/index.html",
         "브랜드 · CI | 쉴더스랩",
         "쉴더스랩 CI 벡터 원본(SVG) 다운로드와 사용 규칙. 워드마크까지 아웃라인 패스로 변환되어 폰트 설치 없이 동일하게 렌더됩니다.",
         S.BRAND_BODY, "/brand/", extra_css=S.BRAND_CSS)

    page("legal/privacy.html",
         "개인정보처리방침 | 쉴더스랩",
         "쉴더스랩 웹사이트의 개인정보 수집 항목, 처리 목적, 보유 기간, 위탁·국외이전, 정보주체의 권리 안내.",
         L.PRIVACY_BODY, "/legal/privacy.html", extra_css=L.LEGAL_CSS)

    page("legal/terms.html",
         "이용약관 | 쉴더스랩",
         "쉴더스랩 웹사이트 이용약관 — 서비스 내용, 이용자의 의무, 지식재산권, 면책 및 관할.",
         L.TERMS_BODY, "/legal/terms.html", extra_css=L.LEGAL_CSS)

    page("insights/index.html",
         "인사이트 | 쉴더스랩 — 보안 규제와 진단 현장 이야기",
         "규제 변화와 진단 현장에서 반복적으로 발견되는 문제, 실제로 통했던 조치 방법을 정리한 쉴더스랩의 보안 인사이트.",
         D.INSIGHTS_BODY, "/insights/", extra_css=D.INSIGHTS_CSS, extra_js=D.INSIGHTS_JS,
         ld='{"@context":"https://schema.org","@type":"Blog","name":"쉴더스랩 인사이트",'
            '"url":"https://shilderslab.com/insights/"}')

    page("insights/view.html",
         "인사이트 | 쉴더스랩",
         "쉴더스랩 보안 인사이트 상세.",
         D.VIEW_BODY, "/insights/", extra_js=D.VIEW_JS)

    page("careers/index.html",
         "채용 | 쉴더스랩 — 정보보호 컨설턴트 채용",
         "쉴더스랩 채용 공고와 지원 접수. 근거로 검증하는 정보보호 컨설턴트·모의해킹·클라우드 보안 인재를 찾습니다.",
         D.CAREERS_BODY, "/careers/", extra_css=D.CAREERS_CSS, extra_js=D.CAREERS_JS)

    page("contact/index.html",
         "상담 · 견적 요청 | 쉴더스랩",
         "정보보호 컨설팅 상담·견적 요청. 범위 검토와 견적 산정까지는 비용이 발생하지 않으며, 영업일 기준 24시간 내 초기 회신합니다.",
         D.CONTACT_BODY, "/contact/", extra_css=D.CONTACT_CSS, extra_js=D.CONTACT_JS,
         ld='{"@context":"https://schema.org","@type":"ContactPage","name":"상담 · 견적 요청 | 쉴더스랩",'
            '"url":"https://shilderslab.com/contact/"}')


def sync_shell(paths):
    """손으로 작성한 페이지의 nav/footer 블록을 템플릿과 동기화."""
    for p in paths:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            continue
        src = open(full, encoding="utf-8").read()
        new = re.sub(r'<header class="nav" id="nav">.*?</header>', lambda m: NAV, src, flags=re.S)
        new = re.sub(r'<footer class="site">.*?</footer>', lambda m: FOOTER, new, flags=re.S)
        if new != src:
            open(full, "w", encoding="utf-8").write(new)
            print(f"  ↻ {p} 셸 동기화")
        else:
            print(f"  = {p} 변경 없음")


if __name__ == "__main__":
    print("페이지 생성:")
    build_all()
    print("공용 셸 동기화:")
    sync_shell(["index.html", "services/index.html"])
    print("완료.")
