# -*- coding: utf-8 -*-
"""정적 콘텐츠 페이지 v2 — 회사소개 · 진단 방법론 · 자료실 · 브랜드 · 404"""

from content_resources import RES_TITLE, RES_DESC, RES_CSS, RES_BODY  # noqa: F401

# ══════════════════════════════════════════════════════════════════════
# 회사소개
# ══════════════════════════════════════════════════════════════════════
ABOUT_TITLE = "회사소개 | 쉴더스랩 — 정보보호 컨설팅"
ABOUT_DESC = ("쉴더스랩은 ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 "
              "회사입니다. 발견마다 규제 조항과 담당 조직을 붙이고, 재점검으로 조치를 확인한 뒤 과업을 마칩니다.")
ABOUT_LD = ('{"@context":"https://schema.org","@type":"AboutPage","name":"회사소개 | 쉴더스랩",'
            '"url":"https://shilderslab.com/about/"}')

ABOUT_CSS = """
  .tl{border-top:1px solid var(--ink)}
  .tl .item{display:grid;grid-template-columns:120px 1fr;gap:var(--gut);padding:22px 0;
    border-bottom:1px solid var(--rule)}
  .tl time{font-family:var(--font-mono);font-size:.7rem;letter-spacing:.1em;color:var(--accent);
    padding-top:4px}
  .tl h4{font-size:1rem;margin-bottom:6px}
  .tl p{font-size:.92rem;color:var(--ink-2);line-height:1.72;max-width:62ch}
  @media (max-width:720px){.tl .item{grid-template-columns:1fr;gap:6px}}
"""

ABOUT_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 회사소개</div>
    <h1 class="d1" data-content="about.hero_title">확인한 것만<br>보고서에 씁니다</h1>
    <p class="lead" data-content="about.hero_lead">쉴더스랩(SHIELDUS LAB)은 ISMS-P 인증 대응과 모의해킹·취약점 진단을
       한 계약 안에서 수행하는 정보보호 컨설팅 회사이며, 진단으로 찾아낸 항목이 실제 조치로 이어지는 데까지를
       과업 범위로 봅니다. 그래서 보고서 제출은 중간 지점입니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">01 / Our view</span>
      <h2 class="d2" style="margin:20px 0 26px" data-content="about.view_title">발견마다 담당자와<br>순서를 붙입니다</h2>
      <div class="lead cms-rich" data-content="about.view_body">
        <p>
          작년 보고서에 있던 항목이 올해 또 올라오는 이유는 무엇일까요.
          담당자가 손을 놓아서인 경우는 드뭅니다. 발견 사항이 어느 조직의 어떤 작업으로 넘어가는지 적혀 있지 않고,
          고쳤는지 되짚는 절차가 <b>계약 범위에 없을 때</b> 같은 목록이 해마다 되돌아옵니다.
        </p>
        <p>
          그래서 저희는 발견마다 걸리는 규제 조항과 그 항목을 받아 갈 담당 조직을 함께 붙이고,
          조치가 적용됐는지는 재점검에서 직접 열어 확인합니다.
          “지금은 안전한가”라는 질문까지 답한 뒤에 과업을 닫습니다.
        </p>
      </div>
      <div class="pull" style="margin-top:44px">
        <p>확인한 범위와 확인하지 못한 범위를 보고서 안에서 구분해 표시합니다.
           그래야 다음 사람이 어디서부터 이어받을지 알 수 있습니다.</p>
        <cite>보고서 작성 규칙</cite>
      </div>
    </div>
    <div class="c4 start9">
      <div class="kv">
        <div class="row"><div class="k">기업명</div><div class="v">쉴더스랩 (SHIELDUS LAB)</div></div>
        <div class="row"><div class="k">설립</div><div class="v">2026년</div></div>
        <div class="row"><div class="k">사업 분야</div><div class="v">정보보호 컨설팅 — 관리체계 인증, 모의해킹,
          취약점 진단, 개인정보 컴플라이언스, 클라우드 보안</div></div>
        <div class="row"><div class="k">문의</div>
          <div class="v"><a href="mailto:contact@shilderslab.com" style="border-bottom:1px solid var(--rule-2)">contact@shilderslab.com</a></div></div>
        <div class="row"><div class="k">웹사이트</div><div class="v">shilderslab.com</div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell g12">
    <div class="c3">
      <span class="lbl">02 / Name</span>
    </div>
    <div class="c8 start4">
      <h2 class="d2" style="margin:0 0 30px" data-content="about.name_title">이름이 곧<br>하는 일입니다</h2>
      <div class="lead cms-rich" data-content="about.name_body">
        <p>
          <b>shield us</b>, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 <b>LAB</b>이 붙어 사명이 됐습니다.
          국문 <b>쉴더스랩</b>과 영문 표기는 같은 말을 두 번 적은 것입니다.
        </p>
        <p>
          여기서 <b>us</b>는 고객사만 가리키는 말이 아닙니다. 저희도 그 안에 들어갑니다.
          지켜 주는 쪽과 지킴받는 쪽을 갈라 놓으면 보고서를 건네는 순간 일이 끝나 버리고,
          그래서 조치가 닫히기 전까지는 저희 과업도 열려 있습니다.
        </p>
        <p>
          <b>LAB</b>은 방법을 열어 둔다는 뜻으로 씁니다.
          진단 순서와 위험도 등급 기준을 계약 전에 공개하고, 발견 하나하나에 재현 절차를 적습니다.
          다시 해 봐도 같은 결과가 나오지 않는 항목은 연구 결과라고 부를 수 없습니다.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c3">
      <span class="lbl">03 / Message</span>
    </div>
    <div class="c8 start4">
      <h2 class="d2" style="margin:0 0 30px" data-content="about.message_title">대표이사 인사말</h2>
      <div class="lead cms-rich" data-content="about.message_body">
        <p>
          두꺼운 보고서를 다 읽고도 다음 주 월요일 아침에 무엇부터 손대야 할지 모르겠다면,
          저는 그것을 <b>컨설팅의 실패</b>라고 봅니다.
        </p>
        <p>
          쉴더스랩은 그 지점에서 출발했습니다. 취약점 목록을 넘기는 데서 멈추면 담당자의 다음 주는 어제와 똑같기 때문입니다.
          저희는 발견을 규제 조항과 담당 조직의 작업 단위로 옮기고, 왜 그 순서여야 하는지를 옆에 적습니다.
          조치를 다시 확인하는 데까지가 계약 범위입니다.
        </p>
        <p>
          <b>할 수 없는 일을 할 수 있다고 말씀드리지 않습니다.</b>
          법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위도 있습니다.
          그 경계는 이 홈페이지에 숨김 없이 적어 두었습니다.
          <b>확인하지 않은 것을 확인했다고 쓰는 일도 없습니다.</b> 재현되지 않은 취약점은 보고서에 올라가지 않습니다.
        </p>
        <p>
          방법론과 산출물 규격을 계약 전에 공개하는 것도 같은 이유에서입니다.
          저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 하니까요.
          어디부터 봐야 할지 모르시겠다면 그 이야기부터 꺼내 주셔도 됩니다. 범위를 정하는 일에서부터 시작하겠습니다.
        </p>
      </div>
      <div class="sign" style="margin-top:40px">
        <p class="tiny" style="margin-bottom:6px" data-content="about.message_role">쉴더스랩 대표이사</p>
        <p class="d3" style="font-size:1.24rem" data-content="about.message_name">이성훈</p>
      </div>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">04 / Principles</span></div>
      <div class="body">
        <h2 class="d2">일하는 방식</h2>
        <p class="lead">근거를 공개하지 않으면 고객사는 저희 결론이 맞는지 확인할 길이 없습니다.
           아래 항목은 요청하시면 계약서 조항으로 넣습니다.</p>
      </div>
    </div>
    <div class="cols cols-3 divided">
      <div class="col-item rv">
        <span class="n">01</span>
        <h3>근거부터</h3>
        <p>발견마다 재현 절차와 확인 근거가 붙습니다. 판단이 서지 않는 항목은 추정으로 적지 않고
           “확인 필요”로 분리합니다. 무엇을 더 받으면 확정되는지도 그 자리에 밝혀 드립니다.</p>
      </div>
      <div class="col-item rv rv-d1">
        <span class="n">02</span>
        <h3>월요일에 바로 손댈 수 있게</h3>
        <p>위험도 하나로 순서가 정해지지는 않습니다. 고치는 데 걸리는 시간을 나란히 놓고 봐야
           다음 주에 실제로 착수할 항목이 추려집니다.</p>
      </div>
      <div class="col-item rv rv-d2">
        <span class="n">03</span>
        <h3>알게 된 것은 밖으로 나가지 않습니다</h3>
        <p>착수 전 NDA를 먼저 쓰고, 진단 데이터는 합의된 경로로만 주고받으며, 보관 기간이 끝나면
           파기한 뒤 확인서를 드립니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">05 / Capability</span>
      <h2 class="d2" style="margin:20px 0 24px">규제와 공격,<br>두 언어를 함께</h2>
      <p class="lead">심사원 앞에서 쓰는 말과, 공격자가 지나갈 길을 찾을 때 쓰는 말은 다릅니다.
         이 둘을 다른 회사에 나눠 맡기면 담당자 책상 위에 목록이 두 개 남습니다.
         저희는 한 프로젝트 안에서 보고, 우선순위 목록 하나로 합쳐 드립니다.</p>
      <div style="margin-top:32px"><a class="alink" href="/method/">진단 방법론 전체 보기</a></div>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>관리체계</b> — ISMS-P 인증기준과 개인정보보호법상 안전성 확보조치를 놓고, 내부 정책이 실제 운영과 맞물려 있는지 봅니다.</span></li>
        <li><span><b>기술 진단</b> — 웹·API·모바일·내부망 모의해킹. 인프라와 소스코드 취약점 진단도 여기 들어갑니다.</span></li>
        <li><span><b>클라우드</b> — AWS·Azure·GCP 구성을 진단하면서 IAM 권한 범위와 로그 적재 상태를 확인합니다.</span></li>
        <li><span><b>운영 정착</b> — 사고가 나면 누가 먼저 전화를 받는지부터 정합니다. 모의훈련과 담당자 교육도 함께 합니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">함께 볼 범위부터 이야기해 주세요</h2>
      <p class="lead">지금 걸려 있는 규제 요건과 시스템 구성만 알려 주시면,
         어떤 진단이 왜 필요한지 적어 보내 드립니다.</p>
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
METHOD_DESC = ("쉴더스랩이 실제로 쓰는 진단 방법론을 계약 전에 공개합니다. 5단계 절차와 위험도 산정 "
               "기준, 산출물 규격, 수행 규칙(Rules of Engagement), 그리고 하지 않는 일까지.")

METHOD_CSS = """
  .phase{border-top:1px solid var(--ink);padding:26px 0 34px;display:grid;
    grid-template-columns:56px 1fr 1fr;gap:var(--gut)}
  .phase .n{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.1em;color:var(--accent);
    padding-top:5px}
  .phase h3{font-size:1.18rem;margin-bottom:10px;letter-spacing:-.022em}
  .phase .what{font-size:.94rem;color:var(--ink-2);line-height:1.78;max-width:46ch}
  .phase .out .k{font-family:var(--font-mono);font-size:.64rem;letter-spacing:.12em;
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
    <h1 class="d1" data-content="method.hero_title">계약 전에<br>먼저 공개합니다</h1>
    <p class="lead" data-content="method.hero_lead">제안서를 여러 곳에서 받아 놓고도 무엇을 기준으로 비교해야 할지 막막할 때가 있습니다.
       쉴더스랩은 그래서 실제로 쓰는 5단계 절차와 위험도 산정 기준, 산출물 규격을 계약 전에 공개합니다.
       감추면 비교가 안 되니까요.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Process</span></div>
      <div class="body">
        <h2 class="d2">5단계 표준 절차</h2>
        <p class="lead">과업 종류가 달라도 단계는 같고, 05 재점검이 끝나야 종료입니다.
           각 단계에서 무엇이 나오는지는 계약서에 명시합니다.</p>
      </div>
    </div>

    <div class="phase rv">
      <div class="n">01</div>
      <div>
        <h3>범위 정의</h3>
        <p class="what">어디까지 볼지부터 정합니다. 대상 자산과 적용 규제는 물론이고, 언제 시험해도 되는지,
           부하는 어디까지 허용되는지, 어느 경로로 들어가야 하는지까지 여기서 확정합니다.
           이 단계가 흔들리면 뒤따르는 산출물을 전부 다시 만들게 되므로, 범위 밖으로 빼는 대상까지 문서에 남깁니다.</p>
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
        <p class="what">관리·기술·개인정보를 나눠 맡아 동시에 진행합니다. 자동 스캔 결과는 옮겨 담지 않고,
           사람이 한 번 재현해 본 항목만 남깁니다. Critical이 나오면 보고서를 기다리지 않고 바로 연락드립니다.</p>
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
        <p class="what">발견마다 재현 절차와 조치 방향을 달고, 영향 범위와 등급 판정 근거도 같은 항목 안에 적습니다.
           경영진이 읽을 요약과 실무자가 들고 다닐 가이드는 따로 만듭니다.</p>
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
        <p class="what">실제로 고치는 손은 시스템 담당 조직입니다. 저희는 방향을 잡아 드리고, 설정 예시를 제공하고,
           적용안이 맞는지 검토합니다. 조직 사정상 당장 고치기 어려운 항목은 억지로 닫지 않고 잔여위험으로 남깁니다.</p>
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
        <p class="what">조치했다고 올라온 항목을 저희가 다시 열어 봅니다. 재점검 1회는 기본 범위이며,
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
        <p class="lead">“이건 왜 High입니까?” 보고 자리에서 가장 자주 나오는 질문입니다.
           그래서 항목마다 아래 표의 어느 줄에 걸려 그 등급이 됐는지 밝히고, 같은 표를 보고서 첫 장에도 싣습니다.</p>
      </div>
    </div>
    <table class="spec sev">
      <thead><tr><th>등급</th><th>정의</th><th>대응 기준</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="등급"><span class="dot" style="background:#8C3A2E"></span>Critical</td>
          <td data-l="정의">인증 없이 또는 일반 사용자 권한으로 시스템 장악·대량 개인정보 접근이 가능한 상태.
              공격 난이도가 낮고 재현이 안정적임.</td>
          <td data-l="대응 기준">발견 즉시 통보. 보고서 제출 전 협의 시작.</td>
        </tr>
        <tr>
          <td data-l="등급"><span class="dot" style="background:#B4551F"></span>High</td>
          <td data-l="정의">특정 조건에서 권한 상승·인가 우회·중요 정보 노출이 가능. 실제 침해로 이어질 경로가 확인됨.</td>
          <td data-l="대응 기준">보고 후 우선 조치 대상. 재점검 필수.</td>
        </tr>
        <tr>
          <td data-l="등급"><span class="dot" style="background:#8A6224"></span>Medium</td>
          <td data-l="정의">단독으로는 영향이 제한적이나 다른 취약점과 결합 시 위험이 커지는 항목,
              또는 규제 기준 미충족 사항.</td>
          <td data-l="대응 기준">조치 계획에 포함. 일정 협의.</td>
        </tr>
        <tr>
          <td data-l="등급"><span class="dot" style="background:#5B6B62"></span>Low</td>
          <td data-l="정의">정보 노출 수준이 낮거나 악용 조건이 비현실적인 항목. 보안 강화 권고.</td>
          <td data-l="대응 기준">여건에 따라 조치 또는 수용.</td>
        </tr>
        <tr>
          <td data-l="등급"><span class="dot" style="background:#9AA29B"></span>확인 필요</td>
          <td data-l="정의">제한된 접근 권한이나 환경 차이로 재현을 확정하지 못한 항목.
              <b>취약으로 단정하지 않습니다.</b></td>
          <td data-l="대응 기준">추가 정보 제공 시 재확인.</td>
        </tr>
      </tbody>
    </table>
    <p class="tiny" style="margin-top:18px">
      CVSS 점수가 필요하시면 옆에 나란히 적어 드립니다. 다만 조치 순서는 그 환경에서 실제로
      어떤 피해가 생기는지, 고치는 데 얼마나 걸리는지를 보고 정합니다.
    </p>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">03 / Rules of engagement</span>
      <h2 class="d2" style="margin:20px 0 24px">수행 규칙</h2>
      <p class="lead">합의된 범위 밖은 건드리지 않습니다. 아래 항목은 착수 전에 서면으로 확정합니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>사전 서면 승인</b> — 대상 IP·도메인·계정 범위를 적은 승인서가 없으면 시험을 시작하지 않습니다.</span></li>
        <li><span><b>가용성</b> — 부하가 걸릴 수 있는 시험은 따로 합의하고, 합의한 시간대에만 돌립니다.</span></li>
        <li><span><b>실데이터를 다루는 방식</b> — 열람은 필요한 최소 범위까지입니다. 밖으로 내보내거나 사본을 남기지 않습니다.</span></li>
        <li><span><b>제3자 자산</b> — 고객사 소유가 아닌 외부 SaaS나 공용 인프라는 범위에서 뺍니다.</span></li>
        <li><span><b>이상 징후가 보이면 멈춥니다</b> — 서비스에 영향이 갈 조짐이 확인되면 그 자리에서 중단하고 담당자에게 알립니다. 재개할지는 담당자가 정합니다.</span></li>
        <li><span><b>기록 보존</b> — 누가 언제 무엇을 했는지 나중에 되짚을 수 있도록 수행 이력을 남깁니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-3">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">04 / What we don't do</span>
      <h2 class="d2" style="margin:20px 0 24px">하지 않는 일</h2>
      <p class="lead">계약서에 도장을 찍은 뒤에 알게 되면 서로 곤란합니다. 그래서 미리 밝혀 드립니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks no-list">
        <li><span><b>스캐너 결과 납품</b> — 도구 출력물을 그대로 옮겨 담은 보고서는 만들지 않습니다.
          오탐을 걷어 내고 사람이 재현한 항목만 싣습니다.</span></li>
        <li><span><b>확인 없는 “조치 완료”</b> — 재점검에서 저희가 직접 확인한 항목만 완료로 기록합니다.</span></li>
        <li><span><b>인증 통과 보장</b> — 심사 결과를 보장하겠다는 약속은 드리지 않습니다.
          결함이 날 만한 지점을 심사 전에 드러내는 것이 저희 몫입니다.</span></li>
        <li><span><b>보안 솔루션 판매</b> — 제품을 팔지 않는 대신, 도입이 필요하면 요건만 정리해 드리고
          어느 제품을 살지는 고객사가 정합니다.</span></li>
        <li><span><b>범위 밖 진단</b> — 승인되지 않은 자산은 “해 보니 되던데요”라도 손대지 않습니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Next</span>
      <h2 class="d2" style="margin:18px 0 18px">이 기준으로<br>우리 환경을 보면 어떻게 될까요</h2>
      <p class="lead">이 페이지를 그대로 들고 다른 회사 제안서와 비교해 보셔도 됩니다.
         저희 쪽 이야기가 필요해지면, 그때 시스템 구성만 알려 주세요.</p>
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
BRAND_DESC = ("쉴더스랩 CI 벡터 원본(SVG)을 내려받으실 수 있습니다. 워드마크의 글자까지 아웃라인 패스로 "
              "변환해 두어, 폰트가 설치되지 않은 컴퓨터에서 열어도 모양이 흐트러지지 않습니다.")

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
  .sw .i code{font-family:var(--font-mono);font-size:.74rem;color:var(--ink-3)}
  .rules{display:grid;grid-template-columns:1fr 1fr;gap:var(--gut)}
  /* 내용이 한글("권장"/"금지")이라 모노를 쓰면 폴백된다. 산세리프로 되돌리고
     두께도 500 으로 명시한다 — h4 는 전역 규칙에서 600 을 받는데 모노는 600 을 안 싣는다. */
  .rules h4{font-family:var(--font-sans);font-size:.72rem;letter-spacing:.02em;font-weight:500;
    margin-bottom:16px;padding-top:18px;border-top:1px solid var(--ink)}
  .rules .yes h4{color:var(--accent)}
  .rules .no h4{color:var(--bad)}
  @media (max-width:900px){.assets{grid-template-columns:repeat(2,1fr)}.sw{grid-template-columns:repeat(2,1fr)}}
  @media (max-width:640px){.assets{grid-template-columns:1fr}.rules{grid-template-columns:1fr}}

"""

BRAND_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 브랜드 · CI</div>
    <h1 class="d2">쉴더스랩 CI</h1>
    <p class="lead">인쇄소나 간판 업체가 원본 데이터를 달라고 하면 어떤 파일을 보내야 할까요.
       여기 있는 로고는 전부 <b>벡터(SVG) 원본</b>이라, 이 페이지에서 내려받은 파일을 그대로 넘기시면 됩니다.
       워드마크의 글자까지 아웃라인 패스로 바꿔 두었기 때문에 폰트가 설치되지 않은 컴퓨터에서 열어도 모양이 흐트러지지 않습니다.</p>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Name</span></div>
      <div class="body">
        <h2 class="d3">사명의 뜻</h2>
        <p class="lead" data-content="brand.name_summary">shield us, 우리를 지킨다.
           이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 LAB이 붙었습니다.
           로고의 실드와 그 안의 각인도 같은 뜻에서 나왔습니다.</p>
        <p class="tiny" style="margin-top:14px">
          자세한 설명은 <a href="/about/" style="border-bottom:1px solid var(--rule-2)">회사소개</a>에 있습니다.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Logo</span></div>
      <div class="body"><h2 class="d3">로고 원본</h2>
        <p class="lead">쓰실 자리에 맞는 파일을 내려받으시면 됩니다.</p></div>
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
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Korean lockup</span></div>
      <div class="body"><h2 class="d3">한글형 <span class="ko">(국문 우선 · 영문 병기)</span></h2>
        <p class="lead">국문 계약서나 국내 인쇄물처럼 한글이 주인공인 자리에 씁니다.
           구조는 기본형과 같고 위계만 뒤집혀, <b>쉴더스랩</b>이 크고 SHIELDUS LAB 이 아래에 작게 붙습니다.
           한 지면에 기본형과 한글형을 섞어 쓰는 것만 피해 주세요.</p></div>
    </div>
    <div class="assets">
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-ko-horizontal-light.svg" alt="한글형 가로 로고(밝은 배경용)"></div>
        <div class="meta"><b>한글형 가로 · 밝은 배경</b><span>국문 문서 표준</span>
          <a class="alink" href="/assets/ci/lockup-ko-horizontal-light.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-ko-horizontal-dark.svg" alt="한글형 가로 로고(어두운 배경용)"></div>
        <div class="meta"><b>한글형 가로 · 어두운 배경</b><span>다크 배경·영상</span>
          <a class="alink" href="/assets/ci/lockup-ko-horizontal-dark.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-ko-stacked-light.svg" alt="한글형 세로 로고" style="max-height:96px"></div>
        <div class="meta"><b>한글형 세로</b><span>정방형 공간·배너·굿즈</span>
          <a class="alink" href="/assets/ci/lockup-ko-stacked-light.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-ko-stacked-dark.svg" alt="한글형 세로 로고(어두운 배경용)" style="max-height:96px"></div>
        <div class="meta"><b>한글형 세로 · 어두운 배경</b><span>다크 배경</span>
          <a class="alink" href="/assets/ci/lockup-ko-stacked-dark.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage light"><img src="/assets/ci/lockup-ko-mono-black.svg" alt="한글형 단색 로고(검정)"></div>
        <div class="meta"><b>한글형 단색 · 검정</b><span>흑백 인쇄·각인</span>
          <a class="alink" href="/assets/ci/lockup-ko-mono-black.svg" download>SVG</a></div>
      </div>
      <div class="asset">
        <div class="stage dark"><img src="/assets/ci/lockup-ko-mono-white.svg" alt="한글형 단색 로고(흰색)"></div>
        <div class="meta"><b>한글형 단색 · 흰색</b><span>사진 위·단색 배경</span>
          <a class="alink" href="/assets/ci/lockup-ko-mono-white.svg" download>SVG</a></div>
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
      <div class="idx"><span class="lbl">04 / Color</span></div>
      <div class="body"><h2 class="d3">브랜드 컬러</h2>
        <p class="lead">액센트는 딥 파인 그린 하나입니다. 배경에는 웜 오프화이트, 글자에는 잉크를 씁니다.
           나머지는 이 셋을 받쳐 주는 색입니다.</p></div>
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
      <div class="idx"><span class="lbl">05 / Usage</span></div>
      <div class="body"><h2 class="d3">사용 규칙</h2>
        <p class="lead">여백은 심볼 높이의 0.4배 이상. 크기는 심볼 20px, 가로형 락업 높이 24px 아래로는 내리지 마세요.</p></div>
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
/* /insights/<slug>/ 로 들어왔는데 정적 페이지가 생성되지 않은 글이면(최근 발행분)
   동적 렌더러로 넘겨 준다. 그 외에는 일반 404 화면을 보여준다. */
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
    <p class="lead">주소가 바뀌었거나 지워진 페이지입니다. 찾으시던 것이 아래 셋 중 하나일 수 있습니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="cols cols-3 divided">
      <a class="col-item" href="/services/"><span class="n">01</span><h3>서비스</h3>
        <p>ISMS-P 인증부터 모의해킹까지, 여섯 개 영역</p><span class="go alink">이동</span></a>
      <a class="col-item" href="/method/"><span class="n">02</span><h3>진단 방법론</h3>
        <p>어떤 순서로 진단하는지 계약 전에 다 적어 뒀습니다</p><span class="go alink">이동</span></a>
      <a class="col-item" href="/contact/"><span class="n">03</span><h3>상담 요청</h3>
        <p>범위 검토와 견적 산정에는 비용이 붙지 않습니다</p><span class="go alink">이동</span></a>
    </div>
  </div>
</section>"""
