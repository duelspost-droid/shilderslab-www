# -*- coding: utf-8 -*-
"""공용 셸 v2 — head / masthead / footer.
   페이지는 전부 이 셸을 통해 생성한다(홈·서비스 포함). 내비 변경은 NAV 한 곳만 고친다.
"""

SUPA_HOST = "https://nrdapzgtibbusvoaceuh.supabase.co"
SUPA_WS = "wss://nrdapzgtibbusvoaceuh.supabase.co"

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; "
       f"connect-src 'self' {SUPA_HOST} {SUPA_WS}; "
       "base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none'")

# 실제로 쓰는 것만 요청한다. 이 URL 이 렌더 차단 스타일시트라, 안 쓰는 페이스를
# 얹어두면 첫 화면이 그만큼 늦게 뜨고 그 사이 시스템 폰트로 그려졌다 바뀐다.
#   · Sans KR 300  — CSS 선언 0건이라 제거
#   · Serif        — 인용문(.pull)이 전부 한글인데 IBM Plex Serif 에는 한글 글리프가 없다.
#                    실측 결과 한 글자도 렌더되지 않고 Sans KR 로 떨어졌다(폭 349.83 vs
#                    Serif 단독 340.11). 내려받기만 하고 쓰이지 않아 제거했다.
#                    라틴 인용문이 필요해지면 --font-serif 의 Georgia 가 받는다.
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=IBM+Plex+Mono:wght@400;500&"
         "family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap")

# (라벨, 경로) — 순서가 곧 내비 순서
NAV = [
    ("서비스", "/services/"),
    ("진단 방법론", "/method/"),
    ("자료실", "/resources/"),
    ("인사이트", "/insights/"),
    ("회사소개", "/about/"),
]

CTA = ("상담 요청", "/contact/")


def masthead():
    links = "\n".join(
        f'      <a href="{href}">{label}</a>' for label, href in NAV)
    return f"""<header class="masthead" id="masthead">
  <div class="shell bar">
    <a class="brand" href="/" aria-label="쉴더스랩 홈">
      <img src="/assets/ci/lockup-horizontal-light.svg" alt="쉴더스랩 SHIELDUS LAB" height="36">
    </a>
    <nav class="nav" id="nav" aria-label="주요 메뉴">
{links}
      <a class="cta" href="{CTA[1]}">{CTA[0]}</a>
    </nav>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false"><i></i><i></i></button>
  </div>
</header>"""


FOOTER = """<footer class="site">
  <div class="shell">
    <div class="top">
      <div class="fbrand">
        <img src="/assets/ci/lockup-horizontal-dark.svg" alt="쉴더스랩 SHIELDUS LAB">
        <p data-content="footer.blurb">규제 대응과 공격자 관점의 기술 진단을 한 팀에서 수행하는 정보보호 컨설팅 조직입니다.
           발견에는 재현 절차를, 종료에는 재점검을 붙입니다.</p>
      </div>
      <div class="fcol">
        <h5>Services</h5>
        <a href="/services/isms-p/">ISMS-P 인증 컨설팅</a>
        <a href="/services/pentest/">모의해킹 · 침투테스트</a>
        <a href="/services/assessment/">취약점 진단</a>
        <a href="/services/privacy/">개인정보 컴플라이언스</a>
        <a href="/services/cloud/">클라우드 보안</a>
        <a href="/services/governance/">거버넌스 · 교육</a>
      </div>
      <div class="fcol">
        <h5>Company</h5>
        <a href="/about/">회사소개</a>
        <a href="/method/">진단 방법론</a>
        <a href="/regulations/">규제 가이드</a>
        <a href="/resources/">자료실</a>
        <a href="/careers/">채용</a>
        <a href="/brand/">브랜드 · CI</a>
      </div>
      <div class="fcol">
        <h5>Contact</h5>
        <a href="mailto:contact@shilderslab.com">contact@shilderslab.com</a>
        <span data-setting="business_hours">평일 09:00 – 18:00</span>
        <a href="/contact/">상담 · 견적 요청 →</a>
      </div>
    </div>
    <div class="legal">
      <div>
        <div class="biz" id="bizline"></div>
        <div class="copy">© <span data-year>2026</span> SHIELDUS LAB. All rights reserved.</div>
      </div>
      <div class="flinks">
        <a href="/legal/privacy.html">개인정보처리방침</a>
        <a href="/legal/terms.html">이용약관</a>
      </div>
    </div>
  </div>
</footer>"""

SCRIPTS = """<script src="/config.js"></script>
<script src="/assets/vendor/supabase.min.js"></script>
<script src="/assets/js/supa.js"></script>
<script src="/assets/js/site.js"></script>"""


def head(title, desc, canonical, extra_css="", ld=""):
    css = f"\n<style>\n{extra_css}\n</style>" if extra_css else ""
    ldb = f'\n<script type="application/ld+json">\n{ld}\n</script>' if ld else ""
    return f"""<meta charset="UTF-8">
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
<link rel="mask-icon" href="/assets/ci/mask-icon.svg" color="#1A4B3A">
<link rel="apple-touch-icon" href="/assets/ci/apple-touch-icon.png">
<meta name="theme-color" content="#F6F4EF">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">{css}{ldb}"""
