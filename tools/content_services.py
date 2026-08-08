# -*- coding: utf-8 -*-
"""서비스 v2 — 개요 + 6개 상세 페이지
   국내 컨설팅사 조사 결과 반영:
     · 상세 페이지 표준 블록(정의 → 대상/의무 여부 → 절차 → 기대효과)을 따르되,
       경쟁사가 거의 공개하지 않는 **산출물**과 **하지 않는 일**을 명시해 변별력을 만든다.
     · 정보보호 전문서비스기업 지정이 필요한 과업(주요정보통신기반시설 분석·평가)은
       수행 가능하다고 쓰지 않는다. 사실대로 밝힌다.
"""
import json

TITLE = "서비스 | 쉴더스랩 — ISMS-P · 모의해킹 · 취약점 진단 · 클라우드 보안"
DESC = ("ISMS-P 인증 컨설팅, 모의해킹·침투테스트, 취약점 진단, 개인정보 컴플라이언스, 클라우드 보안, "
        "보안 거버넌스·교육. 각 서비스의 대상·수행 범위·산출물을 계약 전에 공개합니다.")

CSS = """
  .svc-list{border-top:1px solid var(--ink)}
  .svc-row{display:grid;grid-template-columns:56px 1fr 1.15fr auto;gap:var(--gut);padding:28px 0;
    border-bottom:1px solid var(--rule);align-items:start;transition:background .18s}
  .svc-row:hover{background:rgba(26,75,58,.035)}
  .svc-row .n{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.1em;
    color:var(--ink-3);padding-top:6px}
  .svc-row h3{font-size:1.22rem;letter-spacing:-.024em;margin-bottom:9px}
  .svc-row .for{font-family:var(--font-mono);font-size:.66rem;letter-spacing:.1em;
    text-transform:uppercase;color:var(--accent)}
  .svc-row p{font-size:.93rem;color:var(--ink-2);line-height:1.72}
  .svc-row .go{font-family:var(--font-mono);font-size:.7rem;color:var(--ink-3);
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
    <h1 class="d1" data-content="services.hero_title">보고서가 두 개면<br>우선순위도 두 개입니다</h1>
    <p class="lead" data-content="services.hero_lead">관리체계는 A업체, 기술진단은 B업체. 이렇게 갈라 맡기면 담당자 책상 위에 위험도 기준이 서로 다른 보고서 두 권이 놓입니다.
       어느 쪽 “높음”을 먼저 잡아야 하는지는 어느 쪽에도 적혀 있지 않습니다. 여섯 영역의 발견을 같은 등급 정의로 판정해
       우선순위 목록 하나로 묶는 이유입니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="svc-list">
      <a class="svc-row" href="/services/isms-p/">
        <span class="n">01</span>
        <div><span class="for">Certification</span><h3>ISMS-P 인증 컨설팅</h3></div>
        <p>범위를 긋는 일에서 결함을 닫는 일까지 인증 한 바퀴를 동행하되,
           심사가 끝난 다음 날에도 같은 방식으로 돌아가는 체계를 남기는 데 목표를 둡니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/pentest/">
        <span class="n">02</span>
        <div><span class="for">Offensive</span><h3>모의해킹 · 침투테스트</h3></div>
        <p>계정 하나를 손에 넣은 뒤 어디까지 들어갔는지, 그 경로를 재현해 보여 드립니다.
           스캐너 출력물을 옮겨 적는 작업과는 성격이 다릅니다.
           웹과 API가 기본이고 모바일과 내부망은 범위 협의에서 정합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/assessment/">
        <span class="n">03</span>
        <div><span class="for">Assessment</span><h3>취약점 진단</h3></div>
        <p>“양호 / 취약” 두 글자만 찍힌 표로는 담당자가 손을 댈 수 없습니다.
           무엇을 어떻게 확인했고 어디를 바꾸면 닫히는지를 항목마다 적어 드립니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/privacy/">
        <span class="n">04</span>
        <div><span class="for">Privacy</span><h3>개인정보 컴플라이언스</h3></div>
        <p>사고는 대개 처리방침 문장이 아니라 데이터가 실제로 오가는 구간에서 납니다.
           수집부터 파기까지 구간을 나눠 따라가며 각 구간의 법적 근거와 조치 상태를 확인합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/cloud/">
        <span class="n">05</span>
        <div><span class="for">Cloud</span><h3>클라우드 보안</h3></div>
        <p>처음 만들 때 켠 설정이 손대지 않은 채 남아 있는지 계정 단위로 확인해
           권한 범위와 로깅 상태를 확인합니다.</p>
        <span class="go">자세히 →</span>
      </a>
      <a class="svc-row" href="/services/governance/">
        <span class="n">06</span>
        <div><span class="for">Governance</span><h3>보안 거버넌스 · 교육</h3></div>
        <p>정책과 절차를 만든 뒤 훈련으로 한 번 돌려 봅니다.
           사고 당일에 실제로 펼쳐지는 문서인지는 그때 드러납니다.
           어긋난 부분을 고친 개정본까지 넘겨 드립니다.</p>
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
        <p class="lead">먼저 봐야 할 것은 상황마다 다르니, 아래 여섯 줄 가운데 지금과 가장 가까운 것을 골라 주세요.
           다만 의무 대상 여부는 매출과 이용자 수, 업종을 겹쳐 봐야 갈리는 문제라 자료를 놓고 검토해 드립니다.</p>
      </div>
    </div>
    <table class="spec">
      <thead><tr><th>지금 상황</th><th>관련 기준</th><th>먼저 볼 것</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="상황">인증 취득을 요구받았다<br>(고객사 · 투자사 · 규제)</td>
          <td data-l="기준">ISMS / ISMS-P 인증기준</td>
          <td data-l="시작"><a href="/services/isms-p/">ISMS-P 인증 컨설팅</a> — 범위를 긋는 일부터</td>
        </tr>
        <tr>
          <td data-l="상황">오픈 날짜가 이미 잡혔다</td>
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
          <td data-l="시작">침해 경로부터 봐야 합니다. <a href="/contact/">먼저 연락 주세요</a></td>
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
      <p class="lead">국내 정보보호 시장에는 법으로 자격이 정해진 과업이 있고, 지정을 받은 사업자만 그 일을 맡을 수 있습니다.
         그 선 밖에 있는 항목이라면 “가능하다”고 적지 않고 아래에 그대로 밝혀 둡니다.</p>
    </div>
    <div class="c6 start7">
      <ul class="ticks">
        <li><span><b>주요정보통신기반시설 취약점 분석·평가</b> — 이 과업은 「정보보호산업의 진흥에 관한 법률」에 따라
          <b>정보보호 전문서비스기업 지정</b>을 받은 사업자가 맡습니다. 쉴더스랩은 지정 사업자가 아니어서
          이 과업은 수주하지 않습니다. 다만 그 기준의 점검 항목을 참고한 자체 취약점 진단은 수행합니다.</span></li>
        <li><span><b>개인정보 영향평가(PIA) 수행</b> — 평가 자체는 지정된 평가기관의 몫입니다. 저희 자리는 그 앞쪽입니다.
          요구 자료를 정비하고 흐름도를 그려 사전 점검까지 마쳐 두는 <b>대응 준비</b>를 맡습니다.</span></li>
        <li><span><b>인증 심사</b> — 컨설팅을 한 곳이 심사까지 맡을 수는 없습니다. 심사는 인증기관과 심사기관이 합니다.
          저희는 심사 대응 준비까지 갑니다.</span></li>
        <li><span><b>보안 솔루션 판매</b> — 제품은 팔지 않습니다. 도입이 필요하면 요건까지만 써 드리고,
          어느 제품을 고를지는 담당자께서 정하시면 됩니다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">어떤 진단이 필요한지부터<br>정리해 드립니다</h2>
      <p class="lead">지금 인증 심사를 준비 중이신가요, 아니면 오픈 일정이 먼저 잡혀 있나요?
         규제 요건과 시스템 구성, 목표 시점을 적어 보내주시면 어떤 진단을 어떤 순서로 붙여야 하는지 답장에 적어 드립니다.
         범위를 잡고 견적을 내는 데까지는 비용이 붙지 않습니다.</p>
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
  .when li span.n{font-family:var(--font-mono);font-size:.68rem;letter-spacing:.1em;
    color:var(--accent);padding-top:5px}
  .out-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 var(--gut)}
  .out-grid .o{border-top:1px solid var(--ink);padding:18px 0 26px}
  .out-grid .o .k{font-family:var(--font-mono);font-size:.64rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--ink-3);display:block;margin-bottom:14px}
  .out-grid .o ul{list-style:none;display:grid;gap:9px}
  .out-grid .o li{font-size:.92rem;color:var(--ink-2);line-height:1.68;padding-left:15px;position:relative}
  .out-grid .o li::before{content:"·";position:absolute;left:0;color:var(--ink-3)}
  .nav-svc{display:flex;gap:0;flex-wrap:wrap;border-top:1px solid var(--rule);padding-top:20px;margin-top:34px}
  .nav-svc a{font-family:var(--font-mono);font-size:.68rem;letter-spacing:.1em;
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
        <p class="lead">아래 목록은 계약서에 명시되는 항목과 같습니다. 여기 없는 문서가 필요하시면 착수 전에 말씀해 주세요.
           중간에 끼워 넣으면 일정이 밀립니다.</p>
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
      모두 공개해 두었습니다. 받아 보신 다른 제안서와 나란히 놓고 비교하셔도 됩니다.
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
      <p class="lead">무엇을 언제까지 해야 하는지만 적어 보내주세요. 필요한 항목과 예상 기간을 문서로 만들어 회신해 드리며,
         이 단계까지는 비용이 붙지 않습니다.</p>
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
            "인증서 다음에<br>남는 것은 운영입니다",
            "인증서 한 장을 받는 것으로 끝나는 프로젝트를 보신 적이 있을 겁니다. 심사가 끝나면 정책 문서는 캐비닛으로 "
            "들어가고, 이듬해 사후심사를 앞두고 다시 꺼내집니다. 그사이 운영 기록이 없으니 또 급하게 채워 넣어야 합니다. "
            "저희는 이 반복을 끊는 데 목표를 둡니다. 평소 운영만 해도 증적이 남는 구조를 짜고, 그 상태에서 심사를 받습니다.",
            when=[
                "고객사와 투자사가 나란히 인증서를 요구하고 있다.",
                "의무 대상인지부터 판단이 서지 않는다.",
                "정책 문서는 있지만 실제 운영과 달라 손을 못 대고 있다.",
                "지난 심사에서 받은 결함을 올해 또 받을 것 같다.",
                "담당자가 나 혼자다.",
            ],
            scope=[
                "<b>인증 범위 설정</b> — 서비스와 조직, 자산의 경계를 먼저 확정합니다. 경계 밖에 있으면서 안쪽과 "
                "연결된 시스템도 목록에 올립니다. 여기가 흔들리면 뒤에 만든 산출물을 전부 다시 씁니다.",
                "<b>GAP 분석</b> — 인증기준 대비 지금 어디까지 와 있는지를 항목 단위로 매깁니다. 기준은 관리체계 "
                "수립·운영, 보호대책 요구사항, 개인정보 처리단계별 요구사항입니다. 이 결과가 곧 이행 로드맵의 초안이 됩니다.",
                "<b>정책·지침 현실화</b> — 문서를 늘리는 작업이 아니라, 지킬 수 없는 조항을 덜어내는 데 절반쯤이 들어갑니다.",
                "<b>위험평가</b> — 자산을 세고 위협과 취약점을 뽑아 위험도를 매깁니다. 수용 가능한 위험 수준(DoA)을 "
                "어디에 그었는지, 왜 거기인지까지 설명 가능한 형태로 남깁니다.",
                "<b>증적 체계 설계</b> — 심사 직전에 몰아서 만드는 문서 대신, 하던 일이 저절로 기록으로 남는 구조를 짭니다.",
                "<b>심사 대응</b> — 모의심사를 한 번 돌리고 인터뷰에서 무엇을 묻는지 미리 맞춰 봅니다. "
                "심사원 질의 대응부터 결함 조치와 조치 확인까지 갑니다.",
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
                "심사는 인증기관과 심사기관이 합니다. 컨설팅사가 대신 받아 줄 수 있는 일이 아닙니다.",
                "통과를 장담하지 않습니다. 결함이 나올 만한 곳을 미리 들춰내는 데까지가 저희 몫입니다.",
                "운영 기록은 시간이 지나야 생깁니다. 준비 기간이 빠듯하면 지금 확보되는 증적부터 순서를 잡습니다.",
                "의무 대상인지 아닌지는 결국 법령 해석입니다. 단정하기보다 근거 조문을 붙여 의견을 드립니다.",
            ],
            faqs=[
                ("준비 기간은 얼마나 걸리나요?",
                 "조직 규모보다 <b>지금 남아 있는 운영 기록의 양</b>이 기간을 좌우합니다. "
                 "정책만 있고 기록이 없다면 기록이 쌓일 시간 자체가 필요하고요. "
                 "남은 기간을 근거 있게 계산하려면 GAP 분석을 먼저 돌리는 편이 빠릅니다."),
                ("우리가 꼭 받아야 하는 건지 모르겠습니다.",
                 "매출액과 이용자 수, 업종처럼 법령이 정한 기준으로 갈립니다. 지금 사업 현황을 알려주시면 "
                 "근거 조문을 붙여 검토 의견을 정리해 드립니다. 의무 대상이 아니라면 인증 취득 대신 "
                 "필요한 통제만 골라 적용하는 선택지도 놓고 보겠습니다."),
                ("기술 진단은 따로 받아야 하나요?",
                 "위험평가에는 기술 취약점 진단 결과가 들어가야 합니다. 진단만 다른 곳에서 받으면 그 결과가 "
                 "위험평가와 조치계획으로 이어지지 않고 따로 놉니다. 저희는 한 프로젝트 안에서 두 축을 이어 붙입니다."),
            ]),
    },
    {
        "slug": "pentest",
        "title": "모의해킹 · 침투테스트 | 쉴더스랩",
        "desc": "웹·API·모바일·내부망 대상 모의해킹. 스캐너 결과가 아니라 재현 가능한 침해 경로와 "
                "영향 범위를 보고합니다. 수행 규칙과 산출물을 계약 전에 공개합니다.",
        "body": _detail(
            "pentest", "모의해킹",
            "어디까지 들어갈 수 있었는가",
            "스캐너가 뽑아 준 목록으로 실제 어디까지 들어갈 수 있습니까? 모의해킹이 답해야 하는 질문은 이쪽이고, "
            "저희는 그 경로를 처음부터 끝까지 재현해 보고합니다. "
            "모든 시험은 사전 서면 승인 범위 안에서만 진행하며, 가용성을 건드릴 수 있는 항목은 따로 합의한 뒤에 손댑니다.",
            when=[
                "오픈 날짜는 이미 잡혔고 마지막 확인만 남았다.",
                "고객사나 파트너가 점검 결과서를 요구한다.",
                "권한 구조가 복잡해진 뒤로 인가 로직에 자신이 없어졌고, 어디부터 봐야 할지도 모르겠다.",
                "스캐너를 돌리긴 했는데 그 결과를 어디까지 믿어야 할지 모르겠다.",
                "인증 심사에서 기술 진단 근거를 요구받았다.",
            ],
            scope=[
                "<b>웹 애플리케이션</b> — 인증과 인가를 우회할 수 있는지, 남의 권한으로 올라설 수 있는지를 봅니다. "
                "권한별 계정을 받아 <b>로그인 이후 영역</b>을 중심으로 파고듭니다. 주입과 세션 처리, 업무 논리 결함도 여기서 나옵니다.",
                "<b>API</b> — 객체 수준 권한(BOLA)과 토큰 처리, 대량 조회, 과다 노출을 확인합니다. "
                "프런트 화면만 보고 끝내면 가장 흔한 정보 노출 경로가 통째로 빠집니다.",
                "<b>모바일 앱</b> — 단말에 남는 데이터와 통신 보호를 보고, 위·변조와 루팅 우회를 시험합니다. "
                "앱이 호출하는 API는 별개 항목으로 산정합니다.",
                "<b>내부망</b> — 계정 하나가 이미 탈취됐다고 치고 시작합니다. 거기서 어디까지 번지는지, "
                "권한을 어디까지 올릴 수 있는지, 중요 자산에 닿는지를 따라갑니다.",
                "<b>시나리오 기반</b> — “고객 DB에 도달할 수 있는가” 같은 목표를 하나 정해 두고 최단 경로를 찾습니다.",
                "<b>오탐 제거</b> — 도구 출력물을 옮겨 적지 않습니다. 사람이 재현한 항목만 보고서에 올라갑니다.",
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
                "부하를 거는 시험, 그러니까 서비스 거부 성격의 항목은 기본 범위에서 뺍니다. 필요하면 따로 합의합니다.",
                "고객사 소유가 아닌 자산은 손대지 않습니다. 외부 SaaS와 공용 인프라가 여기 해당합니다.",
                "실데이터는 최소 범위만 열람하고, 추출하거나 복제하지 않습니다.",
                "Critical 등급은 보고서를 기다리지 않습니다. 발견 즉시 담당자에게 알립니다.",
            ],
            faqs=[
                ("견적 차이가 왜 이렇게 큰가요?",
                 "같은 “웹 모의해킹”이라는 이름을 달고도 안에 든 것이 다르기 때문입니다. 자동 스캔 결과를 정리해 주는 일인지, "
                 "<b>사람이 하나씩 재현하는 일</b>인지. 로그인 이후 영역을 보는지, API가 범위에 들어 있는지, 재점검이 붙어 있는지. "
                 "이 차이로 작업량이 몇 배까지 벌어집니다. 받으신 제안서를 보내주시면 어느 쪽인지 항목별로 짚어 드립니다."),
                ("운영 중인 서비스에 영향이 가지 않을까요?",
                 "운영 영향이 없는 방식과 시간대를 먼저 고릅니다. 스테이징이 있으면 그쪽을 씁니다. "
                 "운영 환경은 거기서만 확인되는 항목에 한해 제한적으로 들어갑니다. "
                 "이상 징후가 보이면 그 자리에서 멈추고 담당자에게 알립니다."),
                ("발견된 내용이 외부로 나가지 않나요?",
                 "착수 전에 NDA를 씁니다. 진단 데이터와 산출물은 합의한 경로로만 오가고, "
                 "보관 기간이 끝나면 파기한 뒤 파기 확인서를 드립니다."),
            ]),
    },
    {
        "slug": "assessment",
        "title": "취약점 진단 | 쉴더스랩",
        "desc": "서버·네트워크·DB·보안장비 설정 진단과 소스코드 시큐어코딩 진단. "
                "항목별 판정 근거와 조치 예시를 남기고, 조치 후 재점검까지 포함합니다.",
        "body": _detail(
            "assessment", "취약점 진단",
            "판정 근거를 항목마다 남깁니다",
            "“양호”와 “취약”, 두 글자만 찍힌 표를 받아 보신 적이 있을 겁니다. 그 표로는 무엇부터 손대야 할지 알 수 "
            "없기 때문에, 저희는 어떤 설정을 어디서 어떻게 확인해 그렇게 판정했는지와 무엇을 바꾸면 닫히는지를 "
            "항목마다 적어 둡니다. 담당자가 보고서를 들고 바로 작업에 들어갈 수 있어야 진단입니다.",
            when=[
                "인증 심사나 내부 감사에서 기술 진단 결과를 요구받았다.",
                "서버가 늘면서 설정이 제각각이 되었다.",
                "이전 진단 보고서를 받아 뒀지만 무엇부터 손대야 할지가 보이지 않는다.",
                "개발 조직에 건네줄 시큐어코딩 기준이 없다.",
                "조치를 마쳤다는 회신은 받았는데 정말 닫혔는지 확인할 방법이 없다.",
            ],
            scope=[
                "<b>OS · DBMS</b> — 계정과 권한부터 봅니다. 패치 수준과 로그 설정, 켜 둘 이유가 없는 서비스, "
                "손대지 않은 기본 계정이 뒤따릅니다.",
                "<b>네트워크 · 보안 장비</b> — 접근 통제 정책이 의도대로 걸려 있는지 확인합니다. "
                "관리 인터페이스가 밖에서 보이는지, 로그를 남기고는 있는지도 함께 봅니다.",
                "<b>웹서버 · WAS</b> — 디렉터리가 열려 있지는 않은지, 오류 페이지가 내부 정보를 뱉지는 않는지 봅니다. "
                "보안 헤더 설정과 업로드 처리도 점검 대상입니다.",
                "<b>소스코드</b> — 입력 검증과 인증·인가, 암호화 적용, 오류 처리를 봅니다. "
                "소스에 그대로 박혀 있는 비밀정보는 특히 눈여겨봅니다.",
                "<b>판정 근거 기록</b> — 항목마다 어떤 명령으로 어디를 봤는지와 그 결과를 남깁니다. "
                "다음 진단 때 같은 기준으로 비교하기 위해서입니다.",
                "<b>조치 우선순위</b> — 위험도만 보지 않고 조치 난이도를 같이 매깁니다. "
                "“이번 분기에 무엇부터”가 표에서 바로 읽히도록 정리합니다.",
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
                "「주요정보통신기반시설 취약점 분석·평가」는 정보보호 전문서비스기업 지정 사업자가 맡는 과업입니다. "
                "쉴더스랩은 지정 사업자가 아니고, 이 과업은 수주하지 않습니다. "
                "다만 그 기준의 점검 항목을 참고한 자체 진단은 합니다.",
                "에이전트를 깔아야 하는 자동화 도구는 기본적으로 쓰지 않습니다. 꼭 필요하면 먼저 협의합니다.",
                "소스코드 진단은 저장소 접근이나 사본이 필요합니다. 과업이 끝나면 파기합니다.",
            ],
            faqs=[
                ("점검 항목을 미리 볼 수 있나요?",
                 "네. 범위 협의 단계에서 적용할 항목표를 먼저 드립니다. "
                 "환경에 맞지 않는 항목은 빼고 필요한 항목은 넣어서 확정한 다음에 착수합니다."),
                ("자동화 도구만 돌리는 것과 진짜 다른가요?",
                 "도구는 후보를 찾는 데까지만 씁니다. 그 후보를 사람이 하나씩 확인해 오탐을 걷어내고, "
                 "이 환경에서 실제로 문제가 되는 항목만 보고서에 남깁니다. "
                 "오탐이 섞인 목록은 담당자의 시간을 가장 많이 잡아먹습니다."),
                ("재점검은 어디까지 해주나요?",
                 "조치했다고 알려주신 항목을 다시 확인하는 데까지가 기본 범위이고, 1회가 포함되어 있습니다. "
                 "전체를 다시 도는 것은 따로 산정합니다."),
            ]),
    },
    {
        "slug": "privacy",
        "title": "개인정보 컴플라이언스 | 쉴더스랩",
        "desc": "개인정보 처리 흐름 진단, 안전성 확보조치 이행 점검, 수탁사·국외이전 관리, "
                "영향평가 대응 준비를 지원합니다.",
        "body": _detail(
            "privacy", "개인정보",
            "데이터가 지나가는 길을<br>따라갑니다",
            "수집 화면에는 동의 항목이 정확히 적혀 있는데, 정작 그 데이터가 어느 테이블에 쌓여 누구에게 열려 있는지는 "
            "아무도 답하지 못하는 경우가 있습니다. 저희는 수집에서 파기까지 구간을 나눠 실제 동선을 따라가고, "
            "구간마다 법적 근거와 안전성 확보조치 이행 상태를 확인합니다.",
            when=[
                "개인정보를 대량으로 다루는데 점검을 받아본 적이 없다.",
                "처리방침을 만들어 두긴 했으나 실제 운영과 같은지는 자신이 없다.",
                "위탁과 재위탁 업체가 늘었는데 관리 절차가 없다.",
                "해외 SaaS를 쓰는데 국외이전 고지를 어떻게 해야 할지 모르겠다.",
                "영향평가 대상이 되었거나, 곧 될 것 같다.",
            ],
            scope=[
                "<b>처리 흐름도 작성</b> — 수집 경로에서 파기까지 실제 동선을 그립니다. 어디에 저장되고 누가 열어 보며 "
                "어디로 제공·위탁되는지가 한 장에 들어옵니다. 시스템 구성도와 맞대 보면 빠져 있던 경로가 드러납니다.",
                "<b>적법성 검토</b> — 항목마다 무슨 근거로 받았는지, 동의는 어떤 방식이었는지, "
                "목적을 넘어 쓰고 있지는 않은지 확인합니다.",
                "<b>안전성 확보조치 이행 점검</b> — 접근권한이 정리돼 있는지, 접속기록을 남기고 실제로 들여다보는지, "
                "암호화는 걸려 있는지, 보관과 파기가 절차대로 도는지를 봅니다.",
                "<b>수탁사 관리</b> — 지금 어디에 무엇을 맡기고 있는지부터 셉니다. "
                "계약서 필수 조항을 검토하고 정기 점검 절차를 설계합니다.",
                "<b>국외이전 점검</b> — 클라우드와 SaaS를 쓰면서 어떤 항목이 국경을 넘고 있는지 확인하고 고지 요건을 정비합니다.",
                "<b>영향평가 대응 준비</b> — 요구 자료를 정비하고 사전 점검을 돌려 평가기관 대응까지 준비해 둡니다.",
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
                "쉴더스랩은 평가기관이 아니며, 대응 준비를 지원합니다.",
                "법령 해석이 갈리는 사안에서는 단정을 피합니다. 근거와 선택지를 정리해 드리고 판단은 담당자께 맡깁니다.",
                "점검하다 실제 개인정보를 열람해야 하는 경우가 생기면, 최소 범위로 제한하고 그때마다 따로 합의합니다.",
            ],
            faqs=[
                ("ISMS-P를 하면 개인정보는 자동으로 되는 것 아닌가요?",
                 "겹치는 부분이 있지만 보는 각도가 다릅니다. ISMS-P의 개인정보 영역은 인증기준 충족 여부를 확인하고, "
                 "컴플라이언스 점검은 실제 처리 흐름이 적법한지와 조치가 이행되고 있는지를 확인합니다. "
                 "둘을 나란히 준비하시는 경우에는 중복되는 작업을 빼고 산정합니다."),
                ("영향평가 대상인지 어떻게 아나요?",
                 "처리하는 개인정보의 규모와 성격, 기관 유형에 따라 갈립니다. "
                 "현재 처리 현황을 알려주시면 근거를 붙여 판단 의견을 드립니다."),
                ("해외 SaaS를 많이 쓰는데 다 정리해야 하나요?",
                 "한꺼번에 정리하기 전에 목록부터 만드는 편이 빠릅니다. 어떤 서비스로 어떤 항목이 흘러가는지가 보이면, "
                 "고지나 동의가 필요한 것과 그렇지 않은 것이 갈립니다. 정리는 그다음입니다."),
            ]),
    },
    {
        "slug": "cloud",
        "title": "클라우드 보안 진단 | 쉴더스랩",
        "desc": "AWS·Azure·GCP 계정과 리소스 구성 진단. IAM 과다 권한, 공개 스토리지, 로깅 미비 등 "
                "구성에서 비롯되는 위험을 계정 단위로 확인합니다.",
        "body": _detail(
            "cloud", "클라우드",
            "처음 켠 설정이<br>그 자리에 남아 있습니다",
            "만들 때 열어 둔 공개 설정, 발급하고 잊은 액세스 키. 클라우드 사고는 대개 이런 데서 시작됩니다. "
            "권한이 어디까지 열려 있는지, 무엇이 밖으로 공개돼 있는지, 로그는 남고 있는지를 계정 단위로 확인합니다.",
            when=[
                "클라우드로 옮긴 뒤 보안 점검을 한 번도 해본 적이 없다.",
                "계정과 권한이 불어나 지금은 누가 무엇을 할 수 있는지 아무도 모른다.",
                "공공기관 대상 서비스를 준비하며 CSAP 요건을 확인해야 한다.",
                "IaC로 자원을 계속 늘리는데 기준선이 없다.",
                "사고가 났을 때 로그로 원인을 되짚을 수 있을지 확신이 없다.",
            ],
            scope=[
                "<b>IAM 권한</b> — 과다 권한과 와일드카드 정책, 오래 쓰지 않은 자격증명, 루트·관리자 사용 이력을 봅니다. "
                "<b>CI/CD 파이프라인 권한</b>은 사람 계정보다 센 경우가 많은데도 검토에서 자주 빠집니다.",
                "<b>네트워크 구성</b> — 보안그룹이 의도대로 좁혀져 있는지, 공개 엔드포인트와 관리 포트가 열려 있는지 확인합니다.",
                "<b>데이터 보호</b> — 스토리지 공개 설정과 스냅샷·이미지 공유 범위를 봅니다. "
                "저장·전송 구간 암호화와 키 관리 주체도 확인 대상입니다.",
                "<b>로깅 · 모니터링</b> — 감사 로그가 켜져 있는지, 얼마나 보관되는지. "
                "그리고 그 로그를 지울 수 있는 권한이 누구에게 있는지까지 확인합니다.",
                "<b>컨테이너 · 쿠버네티스</b> — 이미지를 믿을 수 있는지, 권한 상승이 가능한 설정이 남아 있는지, "
                "시크릿은 어떻게 다루는지 봅니다.",
                "<b>기준선 정의</b> — 점검으로 끝내지 않습니다. 앞으로 만들 자원에 자동으로 걸릴 기준선을 문서와 코드로 남깁니다.",
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
                "진단은 읽기 전용 권한으로 합니다. 자원을 바꾸지 않습니다.",
                "CSAP 인증 심사는 인증기관이 수행합니다. 저희는 요건 정리와 사전 점검까지 맡습니다.",
                "비용 최적화는 범위 밖입니다. 보안 관점에서만 봅니다.",
            ],
            faqs=[
                ("읽기 권한만으로 충분한가요?",
                 "구성 진단은 읽기 전용 감사 권한이면 대부분 됩니다. "
                 "권한 상승을 실제로 실증하는 것처럼 변경이 필요한 시험은 따로 합의한 뒤 격리된 환경에서 진행합니다."),
                ("CSPM 도구를 이미 쓰고 있습니다.",
                 "도구가 쌓아 놓은 알림 목록과, 그 조직에서 진짜 위험한 항목은 다릅니다. "
                 "도구 결과는 출발점으로 쓰고, 권한 구조와 데이터 흐름을 겹쳐 본 뒤에 우선순위를 다시 매깁니다."),
                ("멀티 계정 환경도 되나요?",
                 "됩니다. 계정 수와 리전 수가 산정 기준이니 범위 협의 때 알려주세요."),
            ]),
    },
    {
        "slug": "governance",
        "title": "보안 거버넌스 · 교육 | 쉴더스랩",
        "desc": "정보보호 정책·지침 체계 수립, 침해사고 대응 절차와 모의훈련, "
                "임직원 인식 교육과 개발자 시큐어코딩 교육.",
        "body": _detail(
            "governance", "거버넌스 · 교육",
            "한 번 돌려본 절차만<br>절차로 봅니다",
            "대응이 늦는 이유는 문서가 없어서가 아닙니다. 문서와 현장이 어긋나 있기 때문입니다. "
            "그래서 정책을 만든 뒤 훈련으로 한 번 돌려 봅니다. "
            "거기서 드러난 차이를 반영한 개정본까지가 저희가 넘겨 드리는 결과물입니다.",
            when=[
                "보안 담당 조직을 새로 만들었다.",
                "정책 문서는 있지만 아무도 펼쳐 보지 않는다.",
                "사고가 났을 때 누가 먼저 무엇을 하는지 정해진 것이 없다.",
                "임직원 교육이 해마다 형식으로 흘러간다.",
                "개발 조직에 보안 기준을 어떤 형태로 전달해야 할지 모르겠다.",
            ],
            scope=[
                "<b>정책 체계 설계</b> — 정책과 지침, 절차의 위계를 정리합니다. 지킬 수 있는 수준으로 낮추는 작업이 같이 들어갑니다.",
                "<b>조직 · 역할 정의</b> — 보안 의사결정을 누가 내리는지와 R&amp;R을 정합니다. "
                "겸직으로 운영되는 조직이라면 그 전제 위에서 운영 방안을 짭니다.",
                "<b>침해사고 대응 절차</b> — 사고가 나면 누가 먼저 전화를 받는지부터 정합니다. "
                "탐지에서 사후분석까지 단계를 잇고 대외 신고 기준을 붙입니다.",
                "<b>모의훈련</b> — 시나리오를 만들고 실제로 돌린 뒤, 거기서 나온 문제를 개선 과제로 넘깁니다.",
                "<b>임직원 인식 교육</b> — 그 회사 업무에서 실제로 벌어지는 사례로 진행합니다. "
                "어디서 본 듯한 일반론 슬라이드는 쓰지 않습니다.",
                "<b>개발자 시큐어코딩 교육</b> — 해당 조직의 코드에서 뽑은 패턴을 놓고 이야기합니다.",
                "<b>점검 체계</b> — 정기 점검 체크리스트와 지표를 만들어 둡니다. 담당자가 바뀌어도 운영이 남게 하려는 것입니다.",
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
                "이수증이 필요한 법정 교육은 별도 요건이 있습니다. 착수 전에 확인합니다.",
                "모의훈련은 운영 영향이 없는 범위에서 설계합니다. 실제 시스템을 멈추지 않습니다.",
                "정책 문서를 납품하는 데서 끝내지 않습니다. 운영 사이클이 최소 한 바퀴 도는 데까지 동행합니다.",
            ],
            faqs=[
                ("문서만 만들어 주는 곳과 무엇이 다른가요?",
                 "만든 정책을 최소 한 번은 실제로 돌려 봅니다. 훈련이든 점검이든 한 바퀴를 돌려야 "
                 "문서와 현장의 차이가 눈에 보입니다. 그 차이를 반영한 개정본까지가 산출물입니다."),
                ("우리 조직은 보안 전담자가 한 명뿐입니다.",
                 "그 규모에서 지킬 수 없는 절차를 만들면 문서만 남습니다. "
                 "한 명이 실제로 돌릴 수 있는 최소 체계를 먼저 세우고, 인원이 늘면 그때 확장하는 방식으로 설계합니다."),
                ("교육 자료는 재사용할 수 있나요?",
                 "네. 제작한 자료의 사용권은 고객사에 있으니 이후 내부 반복 교육에 그대로 쓰시면 됩니다."),
            ]),
    },
]


# ── 서비스 상세 구조화 데이터(schema.org Service) ──────────────────────────
# 각 상세 페이지에 Service 를 실어 검색결과가 "무슨 서비스인지" 를 구조로 읽게 한다.
# name/serviceType 는 title 에서 사명 접미사( | 쉴더스랩 …)를 뗀 짧은 이름.
# provider·url 의 도메인 리터럴은 set-domain.py 가 함께 치환한다(이 파일은 TARGETS 에 있음).
# `<` 는 < 로 — JSON-LD 가 <script> 안에 들어가므로 조기 종료를 원천 차단한다.
def _service_ld(d):
    name = d["title"].split("|")[0].strip()
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": d["desc"],
        "provider": {"@type": "Organization", "name": "쉴더스랩",
                     "url": "https://shilderslab.com"},
        "areaServed": {"@type": "Country", "name": "대한민국"},
        "url": "https://shilderslab.com/services/" + d["slug"] + "/",
    }, ensure_ascii=False).replace("<", "\\u003c")


for _d in DETAILS:
    _d["ld"] = _service_ld(_d)
