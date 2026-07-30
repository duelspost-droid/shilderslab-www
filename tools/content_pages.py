# -*- coding: utf-8 -*-
"""정적 콘텐츠 페이지 v2 — 회사소개 · 진단 방법론 · 자료실 · 브랜드 · 404"""

from content_resources import RES_TITLE, RES_DESC, RES_CSS, RES_BODY  # noqa: F401

# ══════════════════════════════════════════════════════════════════════
# 회사소개
# ══════════════════════════════════════════════════════════════════════
ABOUT_TITLE = "회사소개 | 쉴더스랩 — 정보보호 컨설팅"
ABOUT_DESC = ("쉴더스랩은 2026년 설립된 정보보호 컨설팅 조직입니다. 관리체계 인증과 공격자 관점의 "
              "기술 진단을 한 팀에서 수행하고, 조치 확인까지를 과업 범위로 봅니다.")
ABOUT_LD = ('{"@context":"https://schema.org","@type":"AboutPage","name":"회사소개 | 쉴더스랩",'
            '"url":"https://shilderslab.com/about/"}')

ABOUT_CSS = """
  .tl{border-top:1px solid var(--ink)}
  .tl .item{display:grid;grid-template-columns:120px 1fr;gap:var(--gut);padding:22px 0;
    border-bottom:1px solid var(--rule)}
  .tl time{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.1em;color:var(--accent);
    padding-top:4px}
  .tl h4{font-size:1rem;margin-bottom:6px}
  .tl p{font-size:.92rem;color:var(--ink-2);line-height:1.72;max-width:62ch}
  @media (max-width:720px){.tl .item{grid-template-columns:1fr;gap:6px}}
"""

ABOUT_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 회사소개</div>
    <h1 class="d1">보안을<br>검증의 문제로<br>다룹니다</h1>
    <p class="lead">쉴더스랩(SHILDERS LAB)은 2026년에 설립된 정보보호 컨설팅 조직입니다.
       인증 기준을 충족시키는 관리체계 컨설팅과, 실제 공격 관점의 기술 진단을 한 팀에서 수행합니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">01 / Our view</span>
      <h2 class="d2" style="margin:20px 0 26px">보고서는 결과가 아니라<br>작업 지시서입니다</h2>
      <p class="lead" style="margin-bottom:18px">
        많은 조직이 진단을 받고도 이듬해 같은 취약점을 다시 발견합니다. 원인은 대개 진단 역량이 아니라
        <b>조치까지 이어지지 않는 구조</b>입니다. 발견 사항이 담당자의 언어로 번역되지 않고, 우선순위가 없고,
        조치 결과를 확인하는 절차가 없기 때문입니다.
      </p>
      <p class="lead">
        그래서 저희는 발견을 규제 항목과 시스템 담당자의 작업 단위에 함께 연결합니다.
        그리고 조치가 실제로 적용되었는지 재점검으로 확인한 뒤 과업을 종료합니다.
        “무엇이 취약한가”에서 멈추지 않고 “지금은 안전한가”에 답하는 것이 기준입니다.
      </p>
      <div class="pull" style="margin-top:44px">
        <p>취약점을 찾는 일은 절반입니다. 나머지 절반은 그것이 닫혔다는 걸 증명하는 일입니다.</p>
        <cite>쉴더스랩 과업 원칙</cite>
      </div>
    </div>
    <div class="c4 start9">
      <div class="kv">
        <div class="row"><div class="k">기업명</div><div class="v">쉴더스랩 (SHILDERS LAB)</div></div>
        <div class="row"><div class="k">설립</div><div class="v">2026년</div></div>
        <div class="row"><div class="k">사업 분야</div><div class="v">정보보호 컨설팅 — 관리체계 인증, 모의해킹,
          취약점 진단, 개인정보 컴플라이언스, 클라우드 보안</div></div>
        <div class="row"><div class="k">문의</div>
          <div class="v"><a href="mailto:contact@shilderslab.com" style="border-bottom:1px solid var(--rule-2)">contact@shilderslab.com</a></div></div>
        <div class="row"><div class="k">웹사이트</div><div class="v">shilderslab.com</div></div>
      </div>
      <p class="tiny" style="margin-top:18px">
        사업자 등록 정보(상호·대표자·주소)는 확정 후 페이지 하단에 게시합니다.
      </p>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Principles</span></div>
      <div class="body">
        <h2 class="d2">일하는 방식 세 가지</h2>
        <p class="lead">신생 조직이 신뢰를 얻는 방법은 실적을 주장하는 것이 아니라
           판단 근거를 공개하는 것이라고 봅니다.</p>
      </div>
    </div>
    <div class="cols cols-3 divided">
      <div class="col-item rv">
        <span class="n">01</span>
        <h3>근거 없는 지적은 하지 않습니다</h3>
        <p>모든 발견 사항에 재현 절차와 확인 근거를 붙입니다. 판단이 어려운 항목은 추정으로 적지 않고
           “확인 필요”로 분리해 표기합니다. 오탐을 남기면 담당자의 시간이 사라집니다.</p>
      </div>
      <div class="col-item rv d1">
        <span class="n">02</span>
        <h3>조치 가능한 형태로 전달합니다</h3>
        <p>위험도와 조치 난이도를 함께 산정해 우선순위를 제시합니다. 경영진 보고용 요약과 실무 조치
           가이드를 분리해 각자 필요한 것만 보게 합니다.</p>
      </div>
      <div class="col-item rv d2">
        <span class="n">03</span>
        <h3>알게 된 것은 밖으로 나가지 않습니다</h3>
        <p>착수 전 NDA를 체결하고, 진단 데이터는 합의된 경로로만 취급합니다. 보관 기간이 끝나면 파기하고
           파기 확인서를 제공합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">03 / Capability</span>
      <h2 class="d2" style="margin:20px 0 24px">규제와 공격,<br>두 언어를 함께</h2>
      <p class="lead">관리체계 컨설팅과 기술 진단을 서로 다른 회사가 맡으면, 심사는 통과하지만
         침해 경로는 그대로 남는 상태가 만들어집니다. 저희는 두 관점을 같은 프로젝트 안에서 다룹니다.</p>
      <div style="margin-top:32px"><a class="alink" href="/method/">진단 방법론 전체 보기</a></div>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>관리체계</b> — ISMS-P 인증기준, 개인정보보호법상 안전성 확보조치, 내부 정책 체계</span></li>
        <li><span><b>기술 진단</b> — 웹·API·모바일·내부망 모의해킹, 인프라·소스코드 취약점 진단</span></li>
        <li><span><b>클라우드</b> — AWS·Azure·GCP 구성 진단, IAM 권한과 로깅 체계 검토</span></li>
        <li><span><b>운영 정착</b> — 침해사고 대응 절차, 모의훈련, 담당자·임직원 교육</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-3">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">04 / History</span></div>
      <div class="body"><h2 class="d2">연혁</h2></div>
    </div>
    <div class="tl">
      <div class="item">
        <time>2026</time>
        <div>
          <h4>쉴더스랩 설립</h4>
          <p>정보보호 컨설팅 전문 조직으로 출발. 관리체계 인증과 기술 진단을 함께 수행하는 서비스 체계를 정립했습니다.</p>
        </div>
      </div>
      <div class="item">
        <time>2026</time>
        <div>
          <h4>표준 방법론 · 산출물 규격 확립</h4>
          <p>5단계 컨설팅 프로세스(범위 정의 → 진단 → 분석·보고 → 이행 지원 → 재점검)와
             위험도 산정 기준, 보고서 구성을 문서화해 공개했습니다.</p>
        </div>
      </div>
      <div class="item">
        <time>진행 중</time>
        <div>
          <h4>공개 자료 축적</h4>
          <p>담당자가 계약 없이도 바로 쓸 수 있는 점검 체크리스트와 진단 항목표를 자료실에 공개하고 있습니다.
             이력과 사례는 수행이 쌓이는 대로 이 페이지에 갱신합니다.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">함께 볼 범위부터 이야기해 주세요</h2>
      <p class="lead">현재 규제 요건과 시스템 구성을 알려주시면, 필요한 진단과 우선순위를 정리해 회신드립니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn" href="/contact/">상담 요청</a>
        <a class="btn btn-line" href="/services/">서비스 보기</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 진단 방법론
# ══════════════════════════════════════════════════════════════════════
METHOD_TITLE = "진단 방법론 | 쉴더스랩 — 절차 · 위험도 산정 · 산출물 규격"
METHOD_DESC = ("쉴더스랩이 실제로 쓰는 진단 방법론을 공개합니다. 5단계 절차, 위험도 산정 기준, "
               "보고서 구성, 수행 규칙(Rules of Engagement), 하지 않는 일까지 계약 전에 확인하세요.")

METHOD_CSS = """
  .phase{border-top:1px solid var(--ink);padding:26px 0 34px;display:grid;
    grid-template-columns:56px 1fr 1fr;gap:var(--gut)}
  .phase .n{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.1em;color:var(--accent);
    padding-top:5px}
  .phase h3{font-size:1.18rem;margin-bottom:10px;letter-spacing:-.022em}
  .phase .what{font-size:.94rem;color:var(--ink-2);line-height:1.78;max-width:46ch}
  .phase .out .k{font-family:'IBM Plex Mono',monospace;font-size:.64rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--ink-3);margin-bottom:10px;display:block}
  .phase .out ul{list-style:none;display:grid;gap:7px}
  .phase .out li{font-size:.88rem;color:var(--ink-2);padding-left:14px;position:relative;line-height:1.6}
  .phase .out li::before{content:"·";position:absolute;left:0;color:var(--ink-3)}
  .sev td:first-child{white-space:nowrap}
  .sev .dot{display:inline-block;width:8px;height:8px;margin-right:9px;vertical-align:middle}
  .no-list li b{color:var(--ink)}
  @media (max-width:900px){.phase{grid-template-columns:1fr;gap:14px}
    .phase .n{padding-top:0}}
"""

METHOD_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 진단 방법론</div>
    <h1 class="d1">계약 전에<br>먼저 공개합니다</h1>
    <p class="lead">진단은 결과보다 절차가 신뢰를 만듭니다. 저희가 실제로 쓰는 단계, 위험도 산정 기준,
       산출물 구성, 수행 규칙을 그대로 공개합니다. 제안서를 비교하실 때 기준으로 쓰셔도 됩니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Process</span></div>
      <div class="body">
        <h2 class="d2">5단계 표준 절차</h2>
        <p class="lead">모든 과업은 같은 단계를 거칩니다. 마지막 재점검이 끝나야 종료로 봅니다.
           단계별 산출물은 계약서에 그대로 명시됩니다.</p>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">01</div>
      <div>
        <h3>범위 정의</h3>
        <p class="what">대상 자산과 시스템, 적용 규제, 제약 조건(운영시간·부하 허용 범위·접근 경로)을 확정합니다.
           범위가 흔들리면 이후 산출물이 전부 다시 만들어지므로, 이 단계에서 경계와 제외 대상을 문서로 못 박습니다.</p>
      </div>
      <div class="out">
        <span class="k">산출물</span>
        <ul>
          <li>과업 범위 정의서(대상·제외·전제조건)</li>
          <li>수행 규칙 합의서(Rules of Engagement)</li>
          <li>일정표 · 담당자 연락 체계</li>
        </ul>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">02</div>
      <div>
        <h3>진단 수행</h3>
        <p class="what">관리·기술·개인정보 영역을 병행 진단합니다. 자동 스캔 결과는 그대로 보고하지 않고,
           사람이 재현해 오탐을 제거한 항목만 남깁니다. 진행 중 중대한 발견이 나오면 보고서를 기다리지 않고 즉시 통보합니다.</p>
      </div>
      <div class="out">
        <span class="k">산출물</span>
        <ul>
          <li>중간 공유(주 1회 또는 마일스톤 기준)</li>
          <li>긴급 발견 즉시 통보 (Critical 한정)</li>
          <li>진단 로그 · 수행 이력</li>
        </ul>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">03</div>
      <div>
        <h3>분석 · 보고</h3>
        <p class="what">발견 사항마다 재현 절차, 영향 범위, 위험도, 조치 방향을 붙입니다.
           위험도는 아래 기준표로 산정하고 산정 근거를 함께 적습니다. 경영진 요약과 실무 조치 가이드는 분리합니다.</p>
      </div>
      <div class="out">
        <span class="k">산출물</span>
        <ul>
          <li>진단 결과 보고서(요약본 · 상세본)</li>
          <li>발견 사항별 재현 절차와 근거</li>
          <li>조치 우선순위표(위험도 × 조치 난이도)</li>
        </ul>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">04</div>
      <div>
        <h3>이행 지원</h3>
        <p class="what">조치 자체는 시스템 담당 조직이 수행합니다. 저희는 조치 방향 협의, 설정 예시 제공,
           적용안 검토를 맡습니다. 조직 사정상 지금 못 고치는 항목은 억지로 닫지 않고 잔여위험으로 남깁니다.</p>
      </div>
      <div class="out">
        <span class="k">산출물</span>
        <ul>
          <li>조치 가이드(설정 예시 · 코드 수준 권고)</li>
          <li>담당자 질의 대응</li>
          <li>잔여위험 수용 문서 초안</li>
        </ul>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">05</div>
      <div>
        <h3>재점검</h3>
        <p class="what">조치했다고 보고된 항목을 다시 확인합니다. 재점검 1회는 기본 범위에 포함됩니다.
           확인되지 않은 항목은 “조치 완료”로 적지 않습니다.</p>
      </div>
      <div class="out">
        <span class="k">산출물</span>
        <ul>
          <li>재점검 결과서(항목별 조치 확인/미확인)</li>
          <li>최종 잔여위험 목록</li>
          <li>진단 데이터 파기 확인서</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Severity</span></div>
      <div class="body">
        <h2 class="d2">위험도 산정 기준</h2>
        <p class="lead">등급은 느낌이 아니라 기준으로 정합니다. 아래 정의를 보고서 첫 장에 함께 싣기 때문에,
           담당자가 등급의 의미를 두고 협의할 필요가 없습니다.</p>
      </div>
    </div>
    <table class="spec sev">
      <thead><tr><th>등급</th><th>정의</th><th>대응 기준</th></tr></thead>
      <tbody>
        <tr>
          <td><span class="dot" style="background:#8C3A2E"></span>Critical</td>
          <td>인증 없이 또는 일반 사용자 권한으로 시스템 장악·대량 개인정보 접근이 가능한 상태.
              공격 난이도가 낮고 재현이 안정적임.</td>
          <td>발견 즉시 통보. 보고서 제출 전 협의 시작.</td>
        </tr>
        <tr>
          <td><span class="dot" style="background:#B4551F"></span>High</td>
          <td>특정 조건에서 권한 상승·인가 우회·중요 정보 노출이 가능. 실제 침해로 이어질 경로가 확인됨.</td>
          <td>보고 후 우선 조치 대상. 재점검 필수.</td>
        </tr>
        <tr>
          <td><span class="dot" style="background:#8A6224"></span>Medium</td>
          <td>단독으로는 영향이 제한적이나 다른 취약점과 결합 시 위험이 커지는 항목,
              또는 규제 기준 미충족 사항.</td>
          <td>조치 계획에 포함. 일정 협의.</td>
        </tr>
        <tr>
          <td><span class="dot" style="background:#5B6B62"></span>Low</td>
          <td>정보 노출 수준이 낮거나 악용 조건이 비현실적인 항목. 보안 강화 권고.</td>
          <td>여건에 따라 조치 또는 수용.</td>
        </tr>
        <tr>
          <td><span class="dot" style="background:#9AA29B"></span>확인 필요</td>
          <td>제한된 접근 권한이나 환경 차이로 재현을 확정하지 못한 항목.
              <b>취약으로 단정하지 않습니다.</b></td>
          <td>추가 정보 제공 시 재확인.</td>
        </tr>
      </tbody>
    </table>
    <p class="tiny" style="margin-top:18px">
      CVSS 점수를 함께 요구하시면 산정치를 병기합니다. 다만 최종 우선순위는 CVSS가 아니라
      고객사 환경에서의 실제 영향과 조치 난이도로 정합니다.
    </p>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">03 / Rules of engagement</span>
      <h2 class="d2" style="margin:20px 0 24px">수행 규칙</h2>
      <p class="lead">진단은 합의된 범위 안에서만 수행합니다. 아래 항목은 착수 전 서면으로 확정합니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>사전 서면 승인</b> — 대상 IP·도메인·계정 범위를 명시한 승인 없이는 어떤 시험도 하지 않습니다.</span></li>
        <li><span><b>가용성 영향</b> — 부하를 유발할 수 있는 시험은 별도 합의 후, 합의된 시간대에만 수행합니다.</span></li>
        <li><span><b>데이터 취급</b> — 실데이터 열람은 필요한 최소 범위로 제한하고, 추출·복제하지 않습니다.</span></li>
        <li><span><b>제3자 자산</b> — 고객사 소유가 아닌 자산(외부 SaaS·공용 인프라)은 범위에서 제외합니다.</span></li>
        <li><span><b>비상 정지</b> — 이상 징후가 확인되면 즉시 중단하고 담당자에게 통보합니다.</span></li>
        <li><span><b>기록 보존</b> — 수행 이력을 남겨 사후에 “누가 무엇을 했는지” 재구성할 수 있게 합니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-3">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">04 / What we don't do</span>
      <h2 class="d2" style="margin:20px 0 24px">하지 않는 일</h2>
      <p class="lead">할 수 있는 것만큼 하지 않는 것도 미리 밝히는 편이 서로에게 낫습니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks no-list">
        <li><span><b>스캐너 결과 납품</b> — 도구 출력물을 그대로 옮겨 담은 보고서는 만들지 않습니다.
          오탐 제거와 재현이 끝난 항목만 싣습니다.</span></li>
        <li><span><b>확인 없는 “조치 완료”</b> — 재점검으로 확인되지 않은 항목은 완료로 기재하지 않습니다.</span></li>
        <li><span><b>인증 통과 보장</b> — 심사 결과를 보장한다는 약속은 하지 않습니다.
          결함 발생 가능 지점을 사전에 드러내는 것이 저희 역할입니다.</span></li>
        <li><span><b>보안 솔루션 판매</b> — 제품을 팔지 않습니다. 도입이 필요하면 요건만 정의하고
          선정은 고객사가 합니다.</span></li>
        <li><span><b>범위 밖 진단</b> — 승인되지 않은 자산은 “해보니 되더라”라도 손대지 않습니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Next</span>
      <h2 class="d2" style="margin:18px 0 18px">이 기준으로<br>우리 환경을 보면 어떻게 될까요</h2>
      <p class="lead">현재 시스템 구성만 알려주시면 어떤 단계에 무엇이 필요한지 정리해 회신드립니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn" href="/contact/">상담 요청</a>
        <a class="btn btn-line" href="/resources/">자료실 보기</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 브랜드
# ══════════════════════════════════════════════════════════════════════
BRAND_TITLE = "브랜드 · CI | 쉴더스랩"
BRAND_DESC = ("쉴더스랩 CI 벡터 원본(SVG) 다운로드와 사용 규칙. 워드마크까지 아웃라인 패스로 변환되어 "
              "폰트 설치 없이 동일하게 렌더됩니다.")

BRAND_CSS = """
  .assets{display:grid;grid-template-columns:repeat(3,1fr);gap:0 var(--gut)}
  .asset{border-top:1px solid var(--ink);padding-top:0}
  .asset .stage{display:flex;align-items:center;justify-content:center;padding:38px 24px;min-height:150px;
    border-bottom:1px solid var(--rule)}
  .asset .stage.light{background:var(--white)}
  .asset .stage.dark{background:var(--dark)}
  .asset .stage img{max-height:52px;width:auto}
  .asset .meta{padding:16px 0 30px}
  .asset .meta b{display:block;font-size:.94rem;font-weight:600;margin-bottom:5px}
  .asset .meta span{display:block;font-size:.8rem;color:var(--ink-3);margin-bottom:14px}
  .sw{display:grid;grid-template-columns:repeat(4,1fr);gap:0 var(--gut)}
  .sw .s{border-top:1px solid var(--ink)}
  .sw .chip{height:88px}
  .sw .i{padding:12px 0 22px}
  .sw .i b{display:block;font-size:.86rem;font-weight:500}
  .sw .i code{font-family:'IBM Plex Mono',monospace;font-size:.74rem;color:var(--ink-3)}
  .rules{display:grid;grid-template-columns:1fr 1fr;gap:var(--gut)}
  .rules h4{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.12em;
    text-transform:uppercase;margin-bottom:16px;padding-top:18px;border-top:1px solid var(--ink)}
  .rules .yes h4{color:var(--accent)}
  .rules .no h4{color:var(--bad)}
  @media (max-width:900px){.assets{grid-template-columns:repeat(2,1fr)}.sw{grid-template-columns:repeat(2,1fr)}}
  @media (max-width:640px){.assets{grid-template-columns:1fr}.rules{grid-template-columns:1fr}}
"""

BRAND_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 브랜드 · CI</div>
    <h1 class="d2">쉴더스랩 CI</h1>
    <p class="lead">모든 로고 파일은 <b>벡터(SVG) 원본</b>이며, 워드마크까지 실제 아웃라인 패스로 변환되어 있습니다.
       폰트가 설치되지 않은 환경에서도 동일하게 렌더되고, 인쇄·간판·커팅 등 로우데이터가 필요한 작업에
       그대로 사용할 수 있습니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Logo</span></div>
      <div class="body"><h2 class="d3">로고 원본</h2>
        <p class="lead">용도에 맞는 파일을 사용하세요.</p></div>
    </div>
    <div class="assets">
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-horizontal-light.svg" alt="가로형 로고(밝은 배경용)"></div>
        <div class="meta"><b>가로형 · 밝은 배경</b><span>기본 로고. 웹·문서 표준</span>
          <a class="alink" href="/assets/ci/lockup-horizontal-light.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-horizontal-dark.svg" alt="가로형 로고(어두운 배경용)"></div>
        <div class="meta"><b>가로형 · 어두운 배경</b><span>다크 배경·영상</span>
          <a class="alink" href="/assets/ci/lockup-horizontal-dark.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-stacked-light.svg" alt="세로형 로고" style="max-height:96px"></div>
        <div class="meta"><b>세로형</b><span>정방형 공간·배너·굿즈</span>
          <a class="alink" href="/assets/ci/lockup-stacked-light.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/symbol.svg" alt="심볼" style="max-height:64px"></div>
        <div class="meta"><b>심볼</b><span>앱 아이콘·프로필·워터마크</span>
          <a class="alink" href="/assets/ci/symbol.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-mono-black.svg" alt="단색 로고(검정)"></div>
        <div class="meta"><b>단색 · 검정</b><span>흑백 인쇄·팩스·각인</span>
          <a class="alink" href="/assets/ci/lockup-mono-black.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-mono-white.svg" alt="단색 로고(흰색)"></div>
        <div class="meta"><b>단색 · 흰색</b><span>사진 위·단색 배경</span>
          <a class="alink" href="/assets/ci/lockup-mono-white.svg" download>SVG</a></div>
      </div>
    </div>
    <p class="tiny" style="margin-top:26px">
      그 외: <a href="/assets/ci/wordmark-en.svg" download>영문 워드마크</a> ·
      <a href="/assets/ci/wordmark-ko.svg" download>국문 워드마크</a> ·
      <a href="/assets/ci/symbol-mono.svg" download>심볼 단색(currentColor)</a> ·
      <a href="/assets/ci/favicon.svg" download>파비콘</a> ·
      <a href="/assets/ci/og-cover.svg" download>OG 커버</a>
      &nbsp;— 워드마크는 Manrope / Noto Sans KR(SIL Open Font License 1.1) 글리프를 아웃라인 변환해 제작했습니다.
    </p>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Color</span></div>
      <div class="body"><h2 class="d3">브랜드 컬러</h2>
        <p class="lead">딥 파인 그린 하나를 액센트로 씁니다. 배경은 웜 오프화이트, 텍스트는 잉크입니다.</p></div>
    </div>
    <div class="sw">
      <div class="s"><div class="chip" style="background:#1A4B3A"></div><div class="i"><b>Accent · 딥 파인</b><code>#1A4B3A</code></div></div>
      <div class="s"><div class="chip" style="background:#0F3227"></div><div class="i"><b>Accent Deep</b><code>#0F3227</code></div></div>
      <div class="s"><div class="chip" style="background:#2E6B54"></div><div class="i"><b>Accent Light</b><code>#2E6B54</code></div></div>
      <div class="s"><div class="chip" style="background:#15181B"></div><div class="i"><b>Ink</b><code>#15181B</code></div></div>
      <div class="s"><div class="chip" style="background:#F6F4EF;border:1px solid var(--rule)"></div><div class="i"><b>Paper</b><code>#F6F4EF</code></div></div>
      <div class="s"><div class="chip" style="background:#EFECE4"></div><div class="i"><b>Paper 2</b><code>#EFECE4</code></div></div>
      <div class="s"><div class="chip" style="background:#4A5157"></div><div class="i"><b>Ink 2</b><code>#4A5157</code></div></div>
      <div class="s"><div class="chip" style="background:#8A6224"></div><div class="i"><b>Ochre · 강조</b><code>#8A6224</code></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Usage</span></div>
      <div class="body"><h2 class="d3">사용 규칙</h2>
        <p class="lead">최소 여백은 심볼 높이의 0.4배, 최소 크기는 심볼 20px / 가로형 락업 높이 24px 이상을 권장합니다.</p></div>
    </div>
    <div class="rules">
      <div class="yes">
        <h4>권장</h4>
        <ul class="bullets">
          <li>배경 밝기에 맞는 파일(밝은/어두운/단색) 사용</li>
          <li>가로·세로 비율 유지하며 크기만 조정</li>
          <li>단색 사용이 필요하면 mono 파일 사용</li>
          <li>다른 요소와 겹치지 않도록 여백 확보</li>
        </ul>
      </div>
      <div class="no">
        <h4>금지</h4>
        <ul class="bullets">
          <li>임의 색상 변경, 그라데이션 적용</li>
          <li>비율 왜곡, 회전, 기울임, 그림자·외곽선 추가</li>
          <li>심볼 일부만 잘라내 별도 도형처럼 사용</li>
          <li>복잡한 사진 위에 저대비로 배치</li>
          <li>다른 로고와 결합해 새로운 마크 생성</li>
        </ul>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 404
# ══════════════════════════════════════════════════════════════════════
NF_TITLE = "페이지를 찾을 수 없습니다 | 쉴더스랩"
NF_DESC = "요청하신 페이지를 찾을 수 없습니다."

NF_JS = """<script>
/* /insights/<slug>/ 로 들어왔는데 아직 정적 페이지가 없는 글이면(최근 발행분)
   동적 렌더러로 넘겨 준다. 그 외에는 일반 404 화면을 그대로 보여준다. */
(function () {
  var m = /^\/insights\/([a-z0-9][a-z0-9-]*)\/?$/.exec(location.pathname);
  if (m) {
    location.replace("/insights/view.html?slug=" + encodeURIComponent(m[1]));
  }
})();
</script>"""

NF_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 404</div>
    <h1 class="d1">요청하신 페이지가<br>없습니다</h1>
    <p class="lead">주소가 변경되었거나 삭제된 페이지입니다. 아래에서 필요한 곳으로 이동해 주세요.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="cols cols-3 divided">
      <a class="col-item" href="/services/"><span class="n">01</span><h3>서비스</h3>
        <p>ISMS-P 인증, 모의해킹, 취약점 진단 등 여섯 개 영역</p><span class="go alink">이동</span></a>
      <a class="col-item" href="/method/"><span class="n">02</span><h3>진단 방법론</h3>
        <p>절차·위험도 기준·산출물 규격을 계약 전에 공개합니다</p><span class="go alink">이동</span></a>
      <a class="col-item" href="/contact/"><span class="n">03</span><h3>상담 요청</h3>
        <p>범위 검토와 견적 산정에는 비용이 발생하지 않습니다</p><span class="go alink">이동</span></a>
    </div>
  </div>
</section>"""
