# -*- coding: utf-8 -*-
"""정적 콘텐츠 페이지 정의 — 회사소개 · 브랜드(CI) · 개인정보처리방침 · 이용약관"""

ABOUT_CSS = """
  .principle{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
  .pr{border:1px solid var(--line);border-radius:var(--r-lg);padding:26px;
    background:linear-gradient(168deg,rgba(255,255,255,.042),rgba(255,255,255,.012))}
  .pr b{display:block;font-family:'Manrope';font-size:2rem;color:rgba(56,216,239,.28);line-height:1;margin-bottom:14px}
  .pr h3{font-size:1.06rem;margin-bottom:9px;color:#fff}
  .pr p{font-size:.92rem;color:var(--fg-dim)}
  .overview{border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
  .overview dl{display:grid;grid-template-columns:180px 1fr;margin:0}
  .overview dt{padding:15px 20px;font-size:.84rem;font-weight:700;color:var(--cy-300);
    background:rgba(3,7,14,.4);border-bottom:1px solid var(--line)}
  .overview dd{padding:15px 20px;font-size:.9rem;color:var(--fg-dim);border-bottom:1px solid var(--line);margin:0}
  .overview dl > :nth-last-child(1), .overview dl > :nth-last-child(2){border-bottom:0}
  .tl{position:relative;padding-left:30px}
  .tl::before{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:1px;
    background:linear-gradient(180deg,var(--cy-500),rgba(139,147,248,.4),transparent)}
  .tl-item{position:relative;padding-bottom:26px}
  .tl-item::before{content:"";position:absolute;left:-27px;top:6px;width:9px;height:9px;border-radius:50%;
    background:var(--cy-400);box-shadow:0 0 0 4px rgba(5,11,22,.9),0 0 12px rgba(56,216,239,.6)}
  .tl-item time{font-family:'Manrope';font-size:.8rem;font-weight:800;color:var(--cy-300);letter-spacing:.6px}
  .tl-item h4{font-size:1rem;margin:5px 0 5px;color:#fff}
  .tl-item p{font-size:.88rem;color:var(--muted)}
  @media (max-width:900px){.principle{grid-template-columns:1fr}.overview dl{grid-template-columns:1fr}
    .overview dt{border-bottom:0;padding-bottom:0;background:none}
    .overview dd{padding-top:6px}}
"""

ABOUT_BODY = """<section class="page-head">
  <div class="wrap">
    <div class="crumb"><a href="/">홈</a> / 회사소개</div>
    <span class="eyebrow"><span class="dot"></span>ABOUT US</span>
    <h1 class="display">정보보호를 <span class="grad">검증</span>의 문제로 다룹니다</h1>
    <p>쉴더스랩(SHILDERS LAB)은 2026년에 설립된 정보보호 컨설팅 기업입니다.
       인증 기준을 충족시키는 관리체계 컨설팅과, 실제 공격 관점의 기술 진단을 한 팀에서 수행합니다.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">OUR VIEW</span>
      <h2 style="font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:18px">보고서는 결과가 아니라 시작입니다</h2>
      <p style="color:var(--fg-dim);margin-bottom:16px">
        많은 조직이 진단을 받고도 같은 취약점을 다음 해에 다시 발견합니다.
        원인은 대체로 진단 능력이 아니라 <b style="color:#fff">조치까지 이어지지 않는 구조</b>에 있습니다.
        발견 사항이 담당자의 언어로 번역되지 않고, 우선순위가 없고, 조치 결과를 확인하는 절차가 없기 때문입니다.
      </p>
      <p style="color:var(--fg-dim)">
        쉴더스랩은 진단 결과를 규제 항목과 시스템 담당자의 작업 단위에 함께 연결합니다.
        그리고 조치가 실제로 적용되었는지 재점검으로 확인한 뒤 과업을 종료합니다.
        “무엇이 취약한가”에서 멈추지 않고 “지금 안전한가”에 답하는 것이 저희 기준입니다.
      </p>
    </div>
    <div class="reveal d2">
      <div class="overview">
        <dl>
          <dt>기업명</dt><dd>쉴더스랩 (SHILDERS LAB)</dd>
          <dt>설립</dt><dd>2026년</dd>
          <dt>사업 분야</dt><dd>정보보호 컨설팅 — 관리체계 인증, 모의해킹, 취약점 진단, 개인정보 컴플라이언스, 클라우드 보안</dd>
          <dt>주요 서비스</dt><dd>ISMS-P 인증 컨설팅 · 모의해킹 · 취약점 진단 · 개인정보 영향평가 대응 · 클라우드 보안 진단 · 보안 교육</dd>
          <dt>문의</dt><dd><a href="mailto:contact@shilderslab.com" style="color:var(--cy-300)">contact@shilderslab.com</a></dd>
          <dt>웹사이트</dt><dd>shilderslab.com</dd>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="sec tight" style="background:linear-gradient(180deg,transparent,rgba(56,216,239,.03),transparent)">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="kicker">PRINCIPLES</span>
      <h2>일하는 방식 세 가지</h2>
    </div>
    <div class="principle reveal d1">
      <div class="pr">
        <b class="display">01</b>
        <h3>근거 없는 지적은 하지 않습니다</h3>
        <p>모든 발견 사항에는 재현 절차와 확인 근거를 첨부합니다. 판단이 어려운 항목은 추정이 아니라
           확인 필요 항목으로 분리해 표기합니다.</p>
      </div>
      <div class="pr">
        <b class="display">02</b>
        <h3>조치 가능한 형태로 전달합니다</h3>
        <p>위험도와 조치 난이도를 함께 산정해 우선순위를 제시합니다. 경영진 보고용 요약과
           실무 조치 가이드를 분리해 각자 필요한 정보만 보게 합니다.</p>
      </div>
      <div class="pr">
        <b class="display">03</b>
        <h3>알게 된 것은 밖으로 나가지 않습니다</h3>
        <p>착수 전 NDA를 체결하고, 진단 데이터는 합의된 경로로만 취급합니다.
           보관 기간 종료 후 파기하고 파기 확인서를 제공합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">CAPABILITY</span>
      <h2 style="font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:18px">규제와 공격, 두 언어를 함께</h2>
      <p style="color:var(--fg-dim);margin-bottom:24px">
        관리체계 컨설팅과 기술 진단이 서로 다른 회사에서 진행되면, 심사는 통과하지만
        정작 침해 경로는 남아 있는 상태가 만들어집니다. 쉴더스랩은 두 관점을 같은 프로젝트 안에서 다룹니다.
      </p>
      <ul class="checklist">
        <li><span class="tick">✓</span><span><b>관리체계</b> — ISMS-P 인증기준, 개인정보보호법상 안전성 확보조치, 내부 정책 체계</span></li>
        <li><span class="tick">✓</span><span><b>기술 진단</b> — 웹·API·모바일·내부망 모의해킹, 인프라·소스코드 취약점 진단</span></li>
        <li><span class="tick">✓</span><span><b>클라우드</b> — AWS·Azure·GCP 구성 진단, IAM 권한 및 로깅 체계 검토</span></li>
        <li><span class="tick">✓</span><span><b>운영 정착</b> — 침해사고 대응 절차, 모의훈련, 담당자·임직원 교육</span></li>
      </ul>
    </div>
    <div class="reveal d2">
      <span class="kicker">HISTORY</span>
      <h2 style="font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:24px">연혁</h2>
      <div class="tl">
        <div class="tl-item">
          <time>2026</time>
          <h4>쉴더스랩 설립</h4>
          <p>정보보호 컨설팅 전문 조직으로 출발. 관리체계 인증과 기술 진단을 함께 수행하는 서비스 체계를 정립했습니다.</p>
        </div>
        <div class="tl-item">
          <time>2026</time>
          <h4>서비스 체계 확립</h4>
          <p>5단계 표준 컨설팅 프로세스(범위 정의 → 진단 → 분석·보고 → 이행 지원 → 재점검)와 산출물 표준을 마련했습니다.</p>
        </div>
        <div class="tl-item">
          <time>진행 중</time>
          <h4>전문 영역 확장</h4>
          <p>클라우드 보안 진단과 침해사고 대응 체계 구축 역량을 강화하고 있습니다. 주요 이력은 이 페이지와 인사이트를 통해 갱신됩니다.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec tight">
  <div class="wrap">
    <div class="cta-band reveal">
      <h2 class="display">함께 볼 수 있는 범위부터 이야기해 주세요</h2>
      <p>현재 규제 요건과 시스템 구성을 알려주시면, 필요한 진단과 우선순위를 정리해 회신드립니다.</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a class="btn btn-primary" href="/contact/">상담 · 견적 요청</a>
        <a class="btn btn-ghost" href="/services/">서비스 보기</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════
BRAND_CSS = """
  .swatches{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px}
  .sw{border:1px solid var(--line);border-radius:var(--r-md);overflow:hidden}
  .sw .chipc{height:82px}
  .sw .info{padding:12px 14px;background:rgba(255,255,255,.02)}
  .sw b{display:block;font-size:.84rem;color:#fff}
  .sw code{font-size:.74rem;color:var(--muted);font-family:ui-monospace,Menlo,monospace}
  .assets{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
  .asset{border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;
    background:linear-gradient(168deg,rgba(255,255,255,.04),rgba(255,255,255,.012))}
  .asset .stage{display:flex;align-items:center;justify-content:center;padding:30px 22px;min-height:130px}
  .asset .stage.light{background:#F4F7FB}
  .asset .stage.dark{background:var(--ink-950)}
  .asset .stage img{max-height:56px;width:auto}
  .asset .meta{padding:16px 18px;border-top:1px solid var(--line)}
  .asset .meta b{display:block;font-size:.9rem;color:#fff;margin-bottom:4px}
  .asset .meta span{font-size:.76rem;color:var(--muted);display:block;margin-bottom:10px}
  .rules{display:grid;grid-template-columns:1fr 1fr;gap:22px}
  .rule{border:1px solid var(--line);border-radius:var(--r-lg);padding:24px}
  .rule.ok{border-color:rgba(52,211,153,.28);background:rgba(52,211,153,.05)}
  .rule.no{border-color:rgba(248,113,113,.26);background:rgba(248,113,113,.05)}
  .rule h4{font-size:.94rem;margin-bottom:14px;display:flex;align-items:center;gap:8px}
  .rule.ok h4{color:#8ff0c8}.rule.no h4{color:#ffb4b4}
  .rule ul{list-style:none;display:grid;gap:9px}
  .rule li{font-size:.88rem;color:var(--fg-dim);display:flex;gap:9px}
  .rule li::before{content:"·";color:var(--muted)}
  @media (max-width:820px){.rules{grid-template-columns:1fr}}
"""

BRAND_BODY = """<section class="page-head">
  <div class="wrap">
    <div class="crumb"><a href="/">홈</a> / 브랜드 · CI</div>
    <span class="eyebrow"><span class="dot"></span>BRAND IDENTITY</span>
    <h1 class="display">쉴더스랩 CI</h1>
    <p>모든 로고 파일은 <b>벡터(SVG) 원본</b>이며, 워드마크까지 실제 아웃라인 패스로 변환되어 있습니다.
       폰트가 설치되지 않은 환경에서도 동일하게 렌더되고, 인쇄·간판·커팅 등 로우데이터가 필요한 작업에 그대로 사용할 수 있습니다.</p>
  </div>
</section>

<section class="sec tight">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">LOGO ASSETS</span>
      <h2>로고 원본 (SVG)</h2>
      <p>용도에 맞는 파일을 사용하세요. 각 파일은 우클릭 저장 또는 아래 링크로 내려받을 수 있습니다.</p>
    </div>
    <div class="assets reveal d1">
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-horizontal-dark.svg" alt="가로형 로고(어두운 배경용)"></div>
        <div class="meta"><b>가로형 · 어두운 배경</b><span>기본 로고. 웹·프레젠테이션 표준</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/lockup-horizontal-dark.svg" download>SVG 다운로드</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-horizontal-light.svg" alt="가로형 로고(밝은 배경용)"></div>
        <div class="meta"><b>가로형 · 밝은 배경</b><span>흰 배경 문서·인쇄물</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/lockup-horizontal-light.svg" download>SVG 다운로드</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-stacked-dark.svg" alt="세로형 로고" style="max-height:96px"></div>
        <div class="meta"><b>세로형</b><span>정방형 공간·배너·굿즈</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/lockup-stacked-dark.svg" download>SVG 다운로드</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/symbol.svg" alt="심볼" style="max-height:74px"></div>
        <div class="meta"><b>심볼</b><span>앱 아이콘·프로필·워터마크</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/symbol.svg" download>SVG 다운로드</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-mono-black.svg" alt="단색 로고(검정)"></div>
        <div class="meta"><b>단색 · 검정</b><span>흑백 인쇄·팩스·각인</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/lockup-mono-black.svg" download>SVG 다운로드</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-mono-white.svg" alt="단색 로고(흰색)"></div>
        <div class="meta"><b>단색 · 흰색</b><span>사진 위·단색 배경</span>
          <a class="btn btn-ghost btn-sm" href="/assets/ci/lockup-mono-white.svg" download>SVG 다운로드</a></div>
      </div>
    </div>
    <p class="form-note reveal" style="margin-top:18px">
      그 외 파일: <a href="/assets/ci/wordmark-en.svg" download style="color:var(--cy-300)">영문 워드마크</a> ·
      <a href="/assets/ci/wordmark-ko.svg" download style="color:var(--cy-300)">국문 워드마크</a> ·
      <a href="/assets/ci/symbol-mono.svg" download style="color:var(--cy-300)">심볼 단색(currentColor)</a> ·
      <a href="/assets/ci/favicon.svg" download style="color:var(--cy-300)">파비콘</a> ·
      <a href="/assets/ci/og-cover.svg" download style="color:var(--cy-300)">OG 커버</a>
      &nbsp;— 워드마크는 Manrope / Noto Sans KR(SIL Open Font License 1.1) 글리프를 아웃라인 변환해 제작했습니다.
    </p>
  </div>
</section>

<section class="sec tight">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">COLOR</span>
      <h2>브랜드 컬러</h2>
      <p>프라이머리는 사이버 시안 계열입니다. 배경은 딥 잉크 네이비를 기본으로 사용합니다.</p>
    </div>
    <div class="swatches reveal d1">
      <div class="sw"><div class="chipc" style="background:#7CEBFB"></div><div class="info"><b>Cyan 300</b><code>#7CEBFB</code></div></div>
      <div class="sw"><div class="chipc" style="background:#38D8EF"></div><div class="info"><b>Cyan 400</b><code>#38D8EF</code></div></div>
      <div class="sw"><div class="chipc" style="background:#12B5CE"></div><div class="info"><b>Cyan 500 · 주색</b><code>#12B5CE</code></div></div>
      <div class="sw"><div class="chipc" style="background:#0A8CA3"></div><div class="info"><b>Cyan 600</b><code>#0A8CA3</code></div></div>
      <div class="sw"><div class="chipc" style="background:#8B93F8"></div><div class="info"><b>Indigo 400 · 보조</b><code>#8B93F8</code></div></div>
      <div class="sw"><div class="chipc" style="background:#050B16"></div><div class="info"><b>Ink 900 · 배경</b><code>#050B16</code></div></div>
      <div class="sw"><div class="chipc" style="background:#03070E"></div><div class="info"><b>Ink 950</b><code>#03070E</code></div></div>
      <div class="sw"><div class="chipc" style="background:#E9F1FB"></div><div class="info"><b>Text</b><code>#E9F1FB</code></div></div>
    </div>
  </div>
</section>

<section class="sec tight">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">USAGE</span>
      <h2>사용 규칙</h2>
      <p>최소 여백은 심볼 높이의 0.4배, 최소 크기는 심볼 20px / 가로형 락업 높이 24px 이상을 권장합니다.</p>
    </div>
    <div class="rules reveal d1">
      <div class="rule ok">
        <h4>권장</h4>
        <ul>
          <li>배경 밝기에 맞는 파일(어두운/밝은/단색) 사용</li>
          <li>가로·세로 비율 유지하며 크기만 조정</li>
          <li>단색 사용이 필요한 경우 mono 파일 사용</li>
          <li>충분한 여백 확보 — 다른 요소와 겹치지 않게</li>
        </ul>
      </div>
      <div class="rule no">
        <h4>금지</h4>
        <ul>
          <li>임의 색상 변경, 그라데이션 교체</li>
          <li>비율 왜곡, 회전, 기울임, 그림자·외곽선 추가</li>
          <li>심볼 일부만 잘라내 별도 도형처럼 사용</li>
          <li>복잡한 사진 위에 저대비로 배치</li>
          <li>다른 로고와 결합해 새로운 마크 생성</li>
        </ul>
      </div>
    </div>
  </div>
</section>"""
