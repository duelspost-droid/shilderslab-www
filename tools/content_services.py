# -*- coding: utf-8 -*-
"""서비스 v2 — 개요 + 6개 상세 페이지
   국내 컨설팅사 조사 결과 반영:
     · 상세 페이지 표준 블록(정의 → 대상/의무 여부 → 절차 → 기대효과)을 따르되,
       경쟁사가 거의 공개하지 않는 **산출물**과 **하지 않는 일**을 명시해 변별력을 만든다.
     · 정보보호 전문서비스기업 지정이 필요한 과업(주요정보통신기반시설 분석·평가)은
       수행 가능하다고 쓰지 않는다. 사실대로 밝힌다.
"""

TITLE = "서비스 | 쉴더스랩 — ISMS-P · 모의해킹 · 취약점 진단 · 클라우드 보안"
DESC = ("ISMS-P 인증 컨설팅, 모의해킹·침투테스트, 취약점 진단, 개인정보 컴플라이언스, 클라우드 보안, "
        "보안 거버넌스·교육. 각 서비스의 대상·수행 범위·산출물을 계약 전에 공개합니다.")

CSS = """
  .svc-list{border-top:1px solid var(--ink)}
  .svc-row{display:grid;grid-template-columns:56px 1fr 1.15fr auto;gap:var(--gut);padding:28px 0;
    border-bottom:1px solid var(--rule);align-items:start;transition:background .18s}
  .svc-row:hover{background:rgba(26,75,58,.035)}
  .svc-row .n{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.1em;
    color:var(--ink-3);padding-top:6px}
  .svc-row h3{font-size:1.22rem;letter-spacing:-.024em;margin-bottom:9px}
  .svc-row .for{font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.1em;
    text-transform:uppercase;color:var(--accent)}
  .svc-row p{font-size:.93rem;color:var(--ink-2);line-height:1.72}
  .svc-row .go{font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:var(--ink-3);
    white-space:nowrap;padding-top:6px}
  .svc-row:hover .go{color:var(--accent)}
  @media (max-width:900px){
    .svc-row{grid-template-columns:1fr;gap:10px}
    .svc-row .n{padding-top:0}
    .svc-row .go{display:none}
  }
"""

BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 서비스</div>
    <h1 class="d1" data-content="services.hero_title">여섯 개 영역,<br>하나의 기준</h1>
    <p class="lead" data-content="services.hero_lead">관리체계·기술진단·개인정보·클라우드를 서로 다른 언어로 다루면 조치가 흩어집니다.
       모든 발견 사항을 같은 위험도 기준과 우선순위로 정리해 전달합니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="svc-list">
      <a class="svc-row" href="/services/isms-p/">
        <span class="n">01</span>
        <div><span class="for">Certification</span><h3>ISMS-P 인증 컨설팅</h3></div>
        <p>인증 범위 설정부터 GAP 분석, 정책·지침 정비, 위험평가, 심사 대응, 결함 조치까지
           인증 전 주기를 지원합니다. 심사 이후에도 운영되는 체계를 목표로 합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/pentest/">
        <span class="n">02</span>
        <div><span class="for">Offensive</span><h3>모의해킹 · 침투테스트</h3></div>
        <p>스캐너 결과 목록이 아니라 “어디까지 들어갈 수 있었는지”를 보고합니다.
           웹·API·모바일·내부망을 대상으로 재현 가능한 침해 경로를 제시합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/assessment/">
        <span class="n">03</span>
        <div><span class="for">Assessment</span><h3>취약점 진단</h3></div>
        <p>서버·네트워크·DB·보안장비 설정과 소스코드를 항목 단위로 점검합니다.
           판정 근거와 조치 예시를 항목마다 남깁니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/privacy/">
        <span class="n">04</span>
        <div><span class="for">Privacy</span><h3>개인정보 컴플라이언스</h3></div>
        <p>문서가 아니라 실제 처리 흐름을 따라갑니다. 수집부터 파기까지 법적 근거와
           안전성 확보조치 이행 상태를 확인합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/cloud/">
        <span class="n">05</span>
        <div><span class="for">Cloud</span><h3>클라우드 보안</h3></div>
        <p>클라우드 사고 대부분은 취약점이 아니라 구성입니다. 과도한 권한, 공개된 스토리지,
           꺼져 있는 로그를 계정 단위로 확인합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/governance/">
        <span class="n">06</span>
        <div><span class="for">Governance</span><h3>보안 거버넌스 · 교육</h3></div>
        <p>사고는 절차가 없어서가 아니라 절차가 현장과 달라서 커집니다.
           운영 가능한 정책과, 실제로 돌려본 대응 절차를 만듭니다.</p>
        <span class="go">자세히 →</span>
      </a>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Where to start</span></div>
      <div class="body">
        <h2 class="d2">어디서부터 봐야 할지<br>모르겠다면</h2>
        <p class="lead">상황에 따라 먼저 봐야 할 것이 다릅니다. 아래는 자주 있는 경우입니다.
           의무 대상 여부는 매출·이용자 수·업종에 따라 달라지므로 최종 판단은 함께 확인합니다.</p>
      </div>
    </div>
    <table class="spec">
      <thead><tr><th>지금 상황</th><th>관련 기준</th><th>먼저 볼 것</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="상황">인증 취득을 요구받았다<br>(고객사 · 투자사 · 규제)</td>
          <td data-l="기준">ISMS / ISMS-P 인증기준</td>
          <td data-l="시작"><a href="/services/isms-p/">ISMS-P 인증 컨설팅</a> — 범위와 GAP부터 확인</td>
        </tr>
        <tr>
          <td data-l="상황">서비스를 곧 오픈한다</td>
          <td data-l="기준">계약상 보안 요구사항 · 자체 기준</td>
          <td data-l="시작"><a href="/services/pentest/">모의해킹</a> + <a href="/services/assessment/">취약점 진단</a></td>
        </tr>
        <tr>
          <td data-l="상황">개인정보를 대량으로 처리한다</td>
          <td data-l="기준">개인정보보호법 · 안전성 확보조치 기준</td>
          <td data-l="시작"><a href="/services/privacy/">개인정보 컴플라이언스</a></td>
        </tr>
        <tr>
          <td data-l="상황">공공기관 대상 클라우드 서비스를 제공한다</td>
          <td data-l="기준">클라우드 보안인증(CSAP)</td>
          <td data-l="시작"><a href="/services/cloud/">클라우드 보안</a> — 요건 정리와 사전 진단</td>
        </tr>
        <tr>
          <td data-l="상황">보안 담당 조직을 새로 만든다</td>
          <td data-l="기준">내부 정책 · 침해사고 대응 체계</td>
          <td data-l="시작"><a href="/services/governance/">거버넌스 · 교육</a></td>
        </tr>
        <tr>
          <td data-l="상황">사고가 났거나, 날 뻔했다</td>
          <td data-l="기준">—</td>
          <td data-l="시작">침해 경로 확인이 우선입니다. <a href="/contact/">먼저 연락 주세요</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">03 / Scope honesty</span>
      <h2 class="d2" style="margin:20px 0 24px">할 수 없는 것도<br>먼저 밝힙니다</h2>
      <p class="lead">국내 정보보호 시장에는 특정 자격을 갖춘 사업자만 수행할 수 있는 과업이 있습니다.
         해당 과업은 “가능하다”고 쓰지 않습니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>주요정보통신기반시설 취약점 분석·평가</b> — 「정보보호산업의 진흥에 관한 법률」에 따른
          <b>정보보호 전문서비스기업 지정</b>을 받은 사업자가 수행하는 과업입니다.
          쉴더스랩은 현재 지정 사업자가 아니므로 이 과업을 수주하지 않습니다.
          해당 기준의 점검 항목을 참고한 자체 취약점 진단은 수행합니다.</span></li>
        <li><span><b>개인정보 영향평가(PIA) 수행</b> — 영향평가는 지정된 평가기관이 수행합니다.
          저희는 평가기관이 아니며, <b>영향평가 대응 준비</b>(자료 정비, 흐름도 작성, 사전 점검)를 지원합니다.</span></li>
        <li><span><b>인증 심사</b> — 심사는 인증기관·심사기관의 몫입니다. 컨설팅과 심사를 같은 곳이 맡을 수 없으므로,
          저희 역할은 심사 대응 준비까지입니다.</span></li>
        <li><span><b>보안 솔루션 판매</b> — 제품을 팔지 않습니다. 도입이 필요하면 요건만 정의하고 선정은 고객사가 합니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">어떤 진단이 필요한지부터<br>같이 정리합니다</h2>
      <p class="lead">규제 요건, 시스템 구성, 목표 일정만 알려주시면 적합한 조합과 예상 일정을 정리해 회신드립니다.
         범위 검토 단계에서는 비용이 발생하지 않습니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn" href="/contact/">상담 요청</a>
        <a class="btn btn-line" href="/method/">방법론 보기</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 상세 페이지
# ══════════════════════════════════════════════════════════════════════
DETAIL_CSS = """
  .when{border-top:1px solid var(--ink)}
  .when li{display:grid;grid-template-columns:56px 1fr;gap:var(--gut);padding:18px 0;
    border-bottom:1px solid var(--rule);font-size:.96rem;color:var(--ink-2);line-height:1.72;
    list-style:none}
  .when li span.n{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;
    color:var(--accent);padding-top:5px}
  .out-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 var(--gut)}
  .out-grid .o{border-top:1px solid var(--ink);padding:18px 0 26px}
  .out-grid .o .k{font-family:'IBM Plex Mono',monospace;font-size:.64rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--ink-3);display:block;margin-bottom:14px}
  .out-grid .o ul{list-style:none;display:grid;gap:9px}
  .out-grid .o li{font-size:.92rem;color:var(--ink-2);line-height:1.68;padding-left:15px;position:relative}
  .out-grid .o li::before{content:"·";position:absolute;left:0;color:var(--ink-3)}
  .nav-svc{display:flex;gap:0;flex-wrap:wrap;border-top:1px solid var(--rule);padding-top:20px;margin-top:34px}
  .nav-svc a{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;
    text-transform:uppercase;color:var(--ink-3);padding-right:20px;margin-right:20px;
    border-right:1px solid var(--rule);margin-bottom:8px}
  .nav-svc a:last-child{border-right:0;margin-right:0;padding-right:0}
  .nav-svc a:hover,.nav-svc a.on{color:var(--accent)}
  @media (max-width:820px){.out-grid{grid-template-columns:1fr}}
"""

_ITEMS = [("isms-p", "ISMS-P"), ("pentest", "모의해킹"), ("assessment", "취약점 진단"),
          ("privacy", "개인정보"), ("cloud", "클라우드"), ("governance", "거버넌스")]


def _nav(cur):
    out = []
    for s, n in _ITEMS:
        cls = ' class="on"' if s == cur else ""
        out.append(f'<a href="/services/{s}/"{cls}>{n}</a>')
    return '<div class="nav-svc">' + "".join(out) + "</div>"


def _detail(slug, kicker, h1, lead, when, scope, outputs, targets, notes, faqs):
    when_html = "\n".join(
        f'      <li><span class="n">{i + 1:02d}</span><span>{w}</span></li>'
        for i, w in enumerate(when))
    scope_html = "\n".join(f"          <li><span>{s}</span></li>" for s in scope)
    out_html = "\n".join(f"          <li>{o}</li>" for o in outputs)
    tgt_html = "\n".join(
        f'            <tr><td data-l="구분">{k}</td><td data-l="내용">{v}</td></tr>' for k, v in targets)
    notes_html = "\n".join(f"          <li>{n}</li>" for n in notes)
    faq_html = "\n".join(
        f'      <details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in faqs)

    return f"""<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · <a href="/services/">서비스</a> · {kicker}</div>
    <h1 class="d1">{h1}</h1>
    <p class="lead">{lead}</p>
    {_nav(slug)}
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c4">
      <span class="lbl">01 / When you need it</span>
      <h2 class="d3" style="margin:18px 0 14px">이런 경우에<br>필요합니다</h2>
    </div>
    <div class="c7 start6">
      <ul class="when">
{when_html}
      </ul>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Scope</span></div>
      <div class="body"><h2 class="d2">수행 범위</h2></div>
    </div>
    <div class="g12">
      <div class="c7">
        <ul class="ticks">
{scope_html}
        </ul>
      </div>
      <div class="c4 start9">
        <table class="spec">
          <caption>대상 · 전제</caption>
          <tbody>
{tgt_html}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Deliverables</span></div>
      <div class="body">
        <h2 class="d2">산출물</h2>
        <p class="lead">계약서에 그대로 명시되는 목록입니다. 여기 없는 문서가 필요하시면 착수 전에 말씀해 주세요.</p>
      </div>
    </div>
    <div class="out-grid">
      <div class="o">
        <span class="k">기본 제공</span>
        <ul>
{out_html}
        </ul>
      </div>
      <div class="o">
        <span class="k">유의사항</span>
        <ul>
{notes_html}
        </ul>
      </div>
    </div>
    <p class="tiny" style="margin-top:26px">
      단계별 절차와 위험도 산정 기준은 <a href="/method/" style="border-bottom:1px solid var(--rule-2)">진단 방법론</a>에
      전부 공개되어 있습니다.
    </p>
  </div>
</section>

<section class="sec band-3">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">04 / FAQ</span></div>
      <div class="body"><h2 class="d2">자주 묻는 질문</h2></div>
    </div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">범위와 일정을<br>먼저 정리해 드립니다</h2>
      <p class="lead">현재 상황만 알려주시면 필요한 항목과 예상 기간을 문서로 회신드립니다.
         범위 검토와 견적 산정에는 비용이 발생하지 않습니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn" href="/contact/">상담 요청</a>
        <a class="btn btn-line" href="/services/">다른 서비스</a>
      </div>
    </div>
  </div>
</section>"""


DETAILS = [
    {
        "slug": "isms-p",
        "title": "ISMS-P 인증 컨설팅 | 쉴더스랩",
        "desc": "인증 범위 설정, GAP 분석, 정책·지침 정비, 위험평가, 심사 대응과 결함 조치까지 "
                "ISMS-P 인증 전 주기를 지원합니다. 수행 범위와 산출물을 계약 전에 공개합니다.",
        "body": _detail(
            "isms-p", "ISMS-P 인증",
            "심사를 통과하고<br>이후에도 굴러가는 체계",
            "인증 취득이 목표라도, 심사가 끝난 다음 날부터 운영되지 않는 체계는 의미가 없습니다. "
            "현황 진단부터 정책 정비, 증적이 자연히 쌓이는 구조 설계, 심사 대응, 결함 조치까지 함께 진행합니다.",
            when=[
                "고객사·투자사·규제기관으로부터 인증 취득을 요구받았다.",
                "의무 대상인지 아닌지부터 판단이 서지 않는다.",
                "정책 문서는 있는데 실제 운영과 달라서 손을 못 대고 있다.",
                "지난 심사에서 결함을 받았고 올해는 반복하고 싶지 않다.",
                "담당자가 혼자라 어디서부터 손대야 할지 모르겠다.",
            ],
            scope=[
                "<b>인증 범위 설정</b> — 서비스·조직·자산 경계를 확정하고 경계 밖 시스템과의 연계 지점을 목록화합니다. "
                "범위가 흔들리면 이후 산출물이 전부 다시 만들어집니다.",
                "<b>GAP 분석</b> — 인증기준(관리체계 수립·운영 / 보호대책 요구사항 / 개인정보 처리단계별 요구사항) "
                "대비 현재 상태를 항목 단위로 진단하고 이행 로드맵을 만듭니다.",
                "<b>정책·지침 현실화</b> — 지키지 못할 조항을 걷어내는 것도 작업입니다. "
                "문서와 실제 업무 절차를 일치시킵니다.",
                "<b>위험평가</b> — 자산 식별, 위협·취약점 도출, 위험도 산정, 수용 가능한 위험 수준(DoA) 결정까지 "
                "판단 근거가 설명 가능한 형태로 남깁니다.",
                "<b>증적 체계 설계</b> — 심사 직전에 만들어내는 문서가 아니라, 운영하면 자연히 남는 기록 구조를 만듭니다.",
                "<b>심사 대응</b> — 모의심사, 인터뷰 준비, 심사원 질의 대응, 결함 조치와 조치 확인까지 지원합니다.",
            ],
            outputs=[
                "GAP 분석 보고서 · 이행 계획서",
                "정책 / 지침 / 절차 문서 세트",
                "위험평가 결과서 · 잔여위험 수용 문서",
                "증적 관리 대장 양식",
                "모의심사 결과 및 예상 결함 목록",
                "결함 조치 확인서",
            ],
            targets=[
                ("인증 유형", "ISMS · ISMS-P"),
                ("과업 구분", "최초 인증 · 갱신 · 사후심사"),
                ("전제", "인증 범위 내 시스템 담당자 인터뷰 가능"),
                ("협조", "정책 문서 · 자산 목록 · 운영 기록 열람"),
            ],
            notes=[
                "심사는 인증기관·심사기관이 수행합니다. 컨설팅사가 심사를 대행할 수 없습니다.",
                "인증 통과를 보장하지 않습니다. 결함 발생 가능 지점을 사전에 드러내는 것이 역할입니다.",
                "운영 기록은 시간이 쌓여야 생깁니다. 준비 기간이 짧으면 확보 가능한 증적부터 우선순위를 잡습니다.",
                "의무 대상 여부는 최종적으로 법령 해석의 영역입니다. 근거 조문과 함께 검토 의견을 드립니다.",
            ],
            faqs=[
                ("준비 기간은 얼마나 걸리나요?",
                 "조직 규모보다 <b>현재 운영 기록이 얼마나 남아 있는지</b>가 기간을 좌우합니다. "
                 "정책만 있고 기록이 없는 상태라면 기록이 쌓이는 시간 자체가 필요합니다. "
                 "GAP 분석을 먼저 수행하면 남은 기간을 근거 있게 산정할 수 있습니다."),
                ("우리가 의무 대상인지 모르겠습니다.",
                 "매출액·이용자 수·업종 등 법령이 정한 기준으로 판단합니다. 현재 사업 현황을 알려주시면 "
                 "근거 조문과 함께 검토 의견을 정리해 드립니다. 의무 대상이 아니라면 인증 취득 대신 "
                 "필요한 통제만 선별해 적용하는 방향도 함께 검토합니다."),
                ("기술 진단은 따로 받아야 하나요?",
                 "위험평가에는 기술 취약점 진단 결과가 반영되어야 합니다. 별도 업체에서 진단만 받으면 "
                 "그 결과가 위험평가·조치계획으로 연결되지 않는 경우가 많습니다. "
                 "저희는 같은 프로젝트 안에서 두 축을 연결합니다."),
            ]),
    },
    {
        "slug": "pentest",
        "title": "모의해킹 · 침투테스트 | 쉴더스랩",
        "desc": "웹·API·모바일·내부망 대상 모의해킹. 스캐너 결과가 아니라 재현 가능한 침해 경로와 "
                "영향 범위를 보고합니다. 수행 규칙과 산출물을 계약 전에 공개합니다.",
        "body": _detail(
            "pentest", "모의해킹",
            "어디까지<br>들어갈 수 있었는가",
            "취약점 목록이 아니라 침해 경로를 보고합니다. 모든 시험은 사전 서면 승인 범위 안에서만 수행하고, "
            "가용성에 영향을 줄 수 있는 항목은 별도 합의 후 진행합니다.",
            when=[
                "서비스 오픈 전 마지막 확인이 필요하다.",
                "고객사·파트너가 보안 점검 결과를 요구한다.",
                "권한 구조가 복잡해져서 인가 로직에 자신이 없다.",
                "스캐너는 돌려봤는데 결과를 어디까지 믿어야 할지 모르겠다.",
                "인증 심사에서 기술 진단 근거를 요구받았다.",
            ],
            scope=[
                "<b>웹 애플리케이션</b> — 인증·인가 우회, 권한 상승, 주입, 세션 처리, 업무 논리 결함. "
                "권한별 계정을 받아 <b>로그인 이후 영역</b>을 중심으로 봅니다.",
                "<b>API</b> — 객체 수준 권한(BOLA), 토큰 처리, 대량 조회, 과다 노출. "
                "프런트 화면만 점검하면 가장 흔한 정보 노출 경로가 빠집니다.",
                "<b>모바일 앱</b> — 로컬 저장 데이터, 통신 보호, 위·변조 및 루팅 우회 검증. "
                "앱이 호출하는 API 점검은 별개 항목으로 산정합니다.",
                "<b>내부망</b> — 계정 하나가 탈취됐다고 가정하고 확산 경로, 권한 상승, 중요 자산 접근 가능성을 확인합니다.",
                "<b>시나리오 기반</b> — “고객 DB에 도달할 수 있는가” 같은 목표를 정하고 최단 경로를 검증합니다.",
                "<b>오탐 제거</b> — 도구 출력물을 그대로 싣지 않습니다. 사람이 재현한 항목만 보고서에 올라갑니다.",
            ],
            outputs=[
                "발견 사항별 재현 절차 (요청·응답 근거 포함)",
                "침해 경로 다이어그램 · 영향 범위 분석",
                "위험도 산정 결과와 산정 근거",
                "개발·운영 담당자용 조치 가이드",
                "경영진 보고용 요약본",
                "조치 후 재점검 결과서 (1회 포함)",
            ],
            targets=[
                ("대상", "웹 · API · 모바일 · 내부망 · 무선"),
                ("기법", "OWASP Top 10 / ASVS 기반 + 시나리오"),
                ("전제", "대상 범위 서면 승인, 테스트 계정 발급"),
                ("환경", "스테이징 우선, 운영은 제한적 수행"),
            ],
            notes=[
                "부하를 유발하는 시험(서비스 거부 성격)은 기본 범위에서 제외합니다. 필요 시 별도 합의합니다.",
                "고객사 소유가 아닌 자산(외부 SaaS·공용 인프라)은 범위에서 제외합니다.",
                "실데이터 열람은 최소 범위로 제한하며 추출·복제하지 않습니다.",
                "Critical 등급은 보고서를 기다리지 않고 발견 즉시 통보합니다.",
            ],
            faqs=[
                ("견적 차이가 왜 이렇게 큰가요?",
                 "같은 “웹 모의해킹”이라도 <b>자동 스캔 정리</b>인지 <b>수동 재현 검증</b>인지, "
                 "<b>로그인 이후 영역</b>을 보는지, <b>API가 범위에 있는지</b>, <b>재점검이 포함되는지</b>에 따라 "
                 "작업량이 몇 배까지 차이 납니다. 받으신 제안서를 보내주시면 어떤 범위인지 항목별로 짚어 드립니다."),
                ("운영 중인 서비스에 영향이 가지 않을까요?",
                 "기본적으로 운영 영향이 없는 방식과 시간대를 선택합니다. 스테이징을 우선 사용하고, "
                 "운영 환경은 확인이 필요한 항목에 한해 제한적으로 진행합니다. "
                 "이상 징후가 보이면 즉시 중단하고 담당자에게 알립니다."),
                ("발견된 내용이 외부로 나가지 않나요?",
                 "착수 전 NDA를 체결합니다. 진단 데이터와 산출물은 합의된 경로로만 전달하고, "
                 "보관 기간이 끝나면 파기 후 파기 확인서를 제공합니다."),
            ]),
    },
    {
        "slug": "assessment",
        "title": "취약점 진단 | 쉴더스랩",
        "desc": "서버·네트워크·DB·보안장비 설정 진단과 소스코드 시큐어코딩 진단. "
                "항목별 판정 근거와 조치 예시를 남기고, 조치 후 재점검까지 포함합니다.",
        "body": _detail(
            "assessment", "취약점 진단",
            "항목마다<br>판정 근거를 남깁니다",
            "“양호 / 취약”만 적힌 표는 조치에 쓸 수 없습니다. 어떤 설정을 어떻게 확인해서 그렇게 판정했는지, "
            "무엇을 어떻게 바꾸면 되는지를 항목마다 함께 적습니다.",
            when=[
                "인증 심사나 내부 감사에서 기술 진단 결과를 요구받았다.",
                "서버가 늘어나면서 설정이 제각각이 되었다.",
                "이전 진단 보고서를 받았는데 무엇부터 해야 할지 모르겠다.",
                "개발 조직에 시큐어코딩 기준을 주고 싶다.",
                "조치했다고 하는데 정말 닫혔는지 확인이 안 된다.",
            ],
            scope=[
                "<b>OS · DBMS</b> — 계정·권한, 패치 수준, 로그 설정, 불필요 서비스, 기본 계정.",
                "<b>네트워크 · 보안 장비</b> — 접근 통제 정책, 관리 인터페이스 노출, 로깅 설정.",
                "<b>웹서버 · WAS</b> — 디렉터리 노출, 오류 페이지, 보안 헤더, 업로드 처리.",
                "<b>소스코드</b> — 입력 검증, 인증·인가, 암호화 적용, 오류 처리, 하드코딩된 비밀정보.",
                "<b>판정 근거 기록</b> — 항목마다 확인 방법(명령·설정 위치)과 결과를 남겨 "
                "다음 진단 때 같은 기준으로 비교할 수 있게 합니다.",
                "<b>조치 우선순위</b> — 위험도와 조치 난이도를 함께 산정해 “이번 분기에 무엇부터”가 나오게 합니다.",
            ],
            outputs=[
                "항목별 진단 결과서 (양호 / 취약 / 해당없음 + 판정 근거)",
                "취약 항목 조치 가이드 및 설정 예시",
                "조치 우선순위표",
                "경영진 요약 리포트",
                "재점검 결과서 (1회 포함)",
            ],
            targets=[
                ("시스템", "Linux · Windows · DBMS · 네트워크/보안 장비"),
                ("코드", "주요 언어 · 프레임워크 시큐어코딩 진단"),
                ("항목", "공개된 기술적 점검 기준을 환경에 맞게 조정"),
                ("전제", "점검 계정 발급 또는 담당자 동석"),
            ],
            notes=[
                "「주요정보통신기반시설 취약점 분석·평가」는 정보보호 전문서비스기업 지정 사업자가 수행하는 과업입니다. "
                "쉴더스랩은 지정 사업자가 아니며 이 과업을 수주하지 않습니다. "
                "해당 기준의 점검 항목을 참고한 자체 진단은 수행합니다.",
                "에이전트 설치가 필요한 자동화 도구는 기본적으로 사용하지 않습니다. 필요 시 사전 협의합니다.",
                "소스코드 진단은 저장소 접근 또는 사본 전달이 필요하며, 과업 종료 후 파기합니다.",
            ],
            faqs=[
                ("점검 항목을 미리 볼 수 있나요?",
                 "네. 범위 협의 단계에서 적용할 항목표를 먼저 드립니다. "
                 "환경에 맞지 않는 항목은 빼고 필요한 항목은 추가해 확정한 뒤 착수합니다."),
                ("자동화 도구만 돌리는 것과 무엇이 다른가요?",
                 "도구는 후보를 찾는 데 씁니다. 각 후보를 사람이 확인해 오탐을 제거하고, "
                 "그 환경에서 실제로 문제가 되는지 판단한 항목만 보고서에 남깁니다. "
                 "오탐이 섞인 목록은 담당자의 시간을 가장 크게 낭비시킵니다."),
                ("재점검은 어디까지 해주나요?",
                 "조치했다고 통보된 항목을 다시 확인하는 것이 기본 범위(1회)입니다. "
                 "전체 재수행이 필요하면 별도로 산정합니다."),
            ]),
    },
    {
        "slug": "privacy",
        "title": "개인정보 컴플라이언스 | 쉴더스랩",
        "desc": "개인정보 처리 흐름 진단, 안전성 확보조치 이행 점검, 수탁사·국외이전 관리, "
                "영향평가 대응 준비를 지원합니다.",
        "body": _detail(
            "privacy", "개인정보",
            "문서가 아니라<br>흐름을 따라갑니다",
            "개인정보 문제는 대개 방침이 아니라 실제 처리 과정에서 생깁니다. "
            "수집부터 파기까지 데이터가 실제로 어떻게 흐르는지 따라가며 법적 근거와 조치 이행 상태를 확인합니다.",
            when=[
                "개인정보를 대량으로 처리하는데 점검을 받아본 적이 없다.",
                "처리방침을 만들어 뒀지만 실제와 같은지 확신이 없다.",
                "위탁·재위탁 업체가 늘었는데 관리 절차가 없다.",
                "해외 SaaS를 쓰는데 국외이전 고지를 어떻게 해야 할지 모르겠다.",
                "영향평가 대상이 되었거나, 될 것 같다.",
            ],
            scope=[
                "<b>처리 흐름도 작성</b> — 수집 경로, 저장 위치, 접근 주체, 제공·위탁, 파기까지 실제 흐름을 그립니다. "
                "시스템 구성도와 대조해 누락된 경로를 찾습니다.",
                "<b>적법성 검토</b> — 항목별 수집 근거, 동의 방식, 목적 범위 초과 여부를 확인합니다.",
                "<b>안전성 확보조치 이행 점검</b> — 접근권한 관리, 접속기록 보관·점검, 암호화 적용, "
                "보관·파기 절차가 실제로 돌아가는지 확인합니다.",
                "<b>수탁사 관리</b> — 위탁 현황 파악, 계약서 필수 조항 검토, 정기 점검 절차 설계.",
                "<b>국외이전 점검</b> — 클라우드·SaaS 사용에 따른 이전 현황 확인과 고지 요건 정비.",
                "<b>영향평가 대응 준비</b> — 요구 자료 정비, 사전 점검, 평가기관 대응 준비.",
            ],
            outputs=[
                "개인정보 처리 흐름도",
                "항목별 적법성 검토 결과",
                "안전성 확보조치 이행 점검 결과서",
                "개선 과제 목록 (담당 · 기한 포함)",
                "처리방침 · 동의서 개선안",
                "수탁사 점검 체크리스트",
            ],
            targets=[
                ("근거", "개인정보보호법 및 시행령, 안전성 확보조치 기준"),
                ("범위", "온라인 · 오프라인 수집 경로 모두"),
                ("전제", "처리 시스템 담당자 인터뷰, 화면·설정 확인"),
                ("연계", "ISMS-P 개인정보 영역과 함께 수행 가능"),
            ],
            notes=[
                "개인정보 영향평가(PIA)는 지정된 평가기관이 수행합니다. "
                "쉴더스랩은 평가기관이 아니며 대응 준비를 지원합니다.",
                "법령 해석이 갈리는 사안은 단정하지 않고 근거와 함께 선택지를 제시합니다.",
                "점검 과정에서 실제 개인정보 열람이 필요한 경우 최소 범위로 제한하고 별도 합의합니다.",
            ],
            faqs=[
                ("ISMS-P를 하면 개인정보는 자동으로 되는 것 아닌가요?",
                 "ISMS-P의 개인정보 영역은 인증기준 충족 여부를 봅니다. "
                 "개인정보 컴플라이언스 점검은 실제 처리 흐름의 적법성과 조치 이행을 봅니다. "
                 "겹치는 부분이 있지만 같지 않습니다. 함께 준비하는 경우 중복 작업은 제거하고 산정합니다."),
                ("영향평가 대상인지 어떻게 아나요?",
                 "처리하는 개인정보의 규모와 성격, 기관 유형에 따라 정해집니다. "
                 "현재 처리 현황을 알려주시면 근거와 함께 판단 의견을 드립니다."),
                ("해외 SaaS를 많이 쓰는데 다 정리해야 하나요?",
                 "먼저 어떤 서비스에 어떤 항목이 흘러가는지 목록화하는 것이 시작입니다. "
                 "목록이 나오면 고지·동의가 필요한 것과 그렇지 않은 것을 구분할 수 있습니다."),
            ]),
    },
    {
        "slug": "cloud",
        "title": "클라우드 보안 진단 | 쉴더스랩",
        "desc": "AWS·Azure·GCP 계정과 리소스 구성 진단. IAM 과다 권한, 공개 스토리지, 로깅 미비 등 "
                "구성에서 비롯되는 위험을 계정 단위로 확인합니다.",
        "body": _detail(
            "cloud", "클라우드",
            "사고는 취약점이 아니라<br>구성에서 시작됩니다",
            "클라우드에서 문제가 되는 것은 대개 새로운 기술이 아니라 초기 설정 그대로 남아 있는 구성입니다. "
            "권한, 공개 범위, 로깅을 계정 단위로 확인합니다.",
            when=[
                "클라우드로 옮긴 뒤 보안 점검을 한 번도 하지 않았다.",
                "계정과 권한이 늘어나 누가 무엇을 할 수 있는지 모르겠다.",
                "공공기관 대상 서비스를 준비하며 CSAP 요건을 확인해야 한다.",
                "IaC로 자원을 찍어내는데 기준선이 없다.",
                "사고가 나면 로그로 원인을 추적할 수 있는지 자신이 없다.",
            ],
            scope=[
                "<b>IAM 권한</b> — 과다 권한, 와일드카드 정책, 미사용 자격증명, 루트·관리자 사용 이력. "
                "특히 <b>CI/CD 파이프라인 권한</b>은 사람보다 강한데 검토에서 빠지는 경우가 많습니다.",
                "<b>네트워크 구성</b> — 보안그룹, 공개 엔드포인트, 관리 포트 개방 여부.",
                "<b>데이터 보호</b> — 스토리지 공개 설정, 스냅샷·이미지 공유, 저장·전송 암호화, 키 관리.",
                "<b>로깅 · 모니터링</b> — 감사 로그 활성화, 보존 기간, 그리고 로그를 지울 수 있는 권한이 누구에게 있는지.",
                "<b>컨테이너 · 쿠버네티스</b> — 이미지 신뢰성, 권한 상승 가능 설정, 시크릿 관리.",
                "<b>기준선 정의</b> — 점검으로 끝내지 않고 신규 자원에 자동 적용할 기준선을 문서와 코드로 남깁니다.",
            ],
            outputs=[
                "계정·리소스별 위험 구성 목록과 확인 근거",
                "IAM 권한 분석 결과 (과다 권한 주체 목록)",
                "기준선(baseline) 정의서",
                "IaC 반영 가이드",
                "조치 우선순위표 · 재점검 결과서",
            ],
            targets=[
                ("제공자", "AWS · Azure · GCP"),
                ("추가", "쿠버네티스 · 컨테이너 레지스트리"),
                ("전제", "읽기 전용 감사 권한 발급"),
                ("연계", "CSAP 요건 정리 · 이전 시 보안 요건 정의"),
            ],
            notes=[
                "진단은 읽기 전용 권한으로 수행합니다. 자원을 변경하지 않습니다.",
                "CSAP 인증 심사는 인증기관이 수행합니다. 저희는 요건 정리와 사전 점검을 지원합니다.",
                "비용 최적화는 범위에 포함되지 않습니다. 보안 관점에서만 봅니다.",
            ],
            faqs=[
                ("읽기 권한만으로 충분한가요?",
                 "구성 진단은 읽기 전용 감사 권한으로 대부분 가능합니다. "
                 "변경이 필요한 시험(예: 권한 상승 실증)은 별도 합의 후 격리된 환경에서 진행합니다."),
                ("CSPM 도구를 이미 쓰고 있습니다.",
                 "도구가 만든 알림 목록과, 그 조직에서 실제로 위험한 항목은 다릅니다. "
                 "도구 결과를 출발점으로 삼되 권한 구조와 데이터 흐름을 함께 보고 우선순위를 다시 정합니다."),
                ("멀티 계정 환경도 되나요?",
                 "가능합니다. 계정 수와 리전 수가 산정 기준이 되므로 범위 협의 때 알려주세요."),
            ]),
    },
    {
        "slug": "governance",
        "title": "보안 거버넌스 · 교육 | 쉴더스랩",
        "desc": "정보보호 정책·지침 체계 수립, 침해사고 대응 절차와 모의훈련, "
                "임직원 인식 교육과 개발자 시큐어코딩 교육.",
        "body": _detail(
            "governance", "거버넌스 · 교육",
            "절차가 없어서가 아니라<br>현장과 달라서 커집니다",
            "사고 대응이 늦어지는 조직은 대개 문서가 없는 게 아니라 문서와 현장이 다릅니다. "
            "실제로 한 번 돌려본 절차만 절차로 봅니다.",
            when=[
                "보안 담당 조직을 새로 만들었다.",
                "정책 문서는 있는데 아무도 보지 않는다.",
                "사고가 나면 누가 무엇을 하는지 정해져 있지 않다.",
                "임직원 교육을 형식적으로만 하고 있다.",
                "개발 조직에 보안 기준을 어떻게 전달할지 모르겠다.",
            ],
            scope=[
                "<b>정책 체계 설계</b> — 정책·지침·절차의 위계를 정리하고 지킬 수 있는 수준으로 현실화합니다.",
                "<b>조직 · 역할 정의</b> — 보안 의사결정 구조와 R&amp;R, 겸직 조직에서의 실질적 운영 방안.",
                "<b>침해사고 대응 절차</b> — 탐지·보고·격리·복구·사후분석 단계와 연락 체계, 대외 신고 기준.",
                "<b>모의훈련</b> — 시나리오 개발, 진행, 결과 기반 개선 과제 도출. 문서만 만들고 끝내지 않습니다.",
                "<b>임직원 인식 교육</b> — 업무 맥락에 맞춘 사례 중심 교육. 일반론 슬라이드는 쓰지 않습니다.",
                "<b>개발자 시큐어코딩 교육</b> — 해당 조직의 실제 코드에서 나온 패턴으로 진행합니다.",
                "<b>점검 체계</b> — 정기 점검 체크리스트와 지표를 만들어 운영이 남게 합니다.",
            ],
            outputs=[
                "정책 · 지침 문서 체계와 개정 이력 관리 방안",
                "침해사고 대응 매뉴얼 · 연락 체계도",
                "모의훈련 시나리오 및 결과 보고서",
                "교육 자료 (조직 맞춤 사례 포함)",
                "정기 점검 체크리스트 · 보안 지표 정의서",
            ],
            targets=[
                ("대상", "보안 조직 신설·재정비, 침해사고 대응 체계"),
                ("교육", "임직원 인식 · 개발자 시큐어코딩 · 담당자 실무"),
                ("형태", "온라인 · 집합 교육 모두 가능"),
                ("전제", "현행 문서와 조직도 열람"),
            ],
            notes=[
                "교육 이수증 발급이 필요한 법정 교육은 별도 요건이 있으므로 착수 전 확인합니다.",
                "모의훈련은 운영 영향이 없는 범위에서 설계하며 실제 시스템을 중단시키지 않습니다.",
                "정책 문서를 납품하는 것으로 끝내지 않습니다. 최소 1회 운영 사이클을 함께 돌립니다.",
            ],
            faqs=[
                ("문서만 만들어 주는 곳과 무엇이 다른가요?",
                 "정책을 만든 뒤 최소 한 번은 실제로 돌려봅니다. 훈련이든 점검이든 운영 사이클을 한 바퀴 돌려야 "
                 "문서와 현장의 차이가 드러납니다. 그 차이를 반영한 개정본까지가 산출물입니다."),
                ("우리 조직은 보안 전담자가 한 명뿐입니다.",
                 "겸직·1인 조직에서 지킬 수 없는 절차를 만들면 문서만 남습니다. "
                 "그 규모에서 실제로 운영 가능한 최소 체계를 먼저 세우고, 인원이 늘면 확장하는 방식으로 설계합니다."),
                ("교육 자료는 재사용할 수 있나요?",
                 "네. 제작한 교육 자료의 사용권은 고객사에 있습니다. 이후 내부 반복 교육에 활용하실 수 있습니다."),
            ]),
    },
]
