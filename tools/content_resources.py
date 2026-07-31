# -*- coding: utf-8 -*-
"""자료실 v2 — 실제로 쓸 수 있는 문서를 공개한다.
   신생 조직이 실적 없이 신뢰를 만드는 장치: 회사 소개가 아니라 담당자가 당장 쓸 목록을 준다.
   문서는 어느 업체와 일하든 사용할 수 있도록 중립적으로 쓴다(자사 홍보 문구를 섞지 않는다).
"""

RES_TITLE = "자료실 | 쉴더스랩 — 담당자가 바로 쓰는 점검 목록"
RES_DESC = ("모의해킹 제안서 비교 체크리스트, ISMS-P 착수 전 자가점검, 진단 보고서 구성 샘플. "
            "계약 없이 바로 쓰실 수 있도록 공개합니다.")

RES_CSS = """
  .res-list{border-top:1px solid var(--ink)}
  .res-row{display:grid;grid-template-columns:56px 1.1fr 1.4fr auto;gap:var(--gut);padding:30px 0;
    border-bottom:1px solid var(--rule);align-items:start;transition:background .18s}
  .res-row:hover{background:rgba(26,75,58,.035)}
  .res-row .n{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.1em;
    color:var(--ink-3);padding-top:6px}
  .res-row h3{font-size:1.16rem;letter-spacing:-.022em;margin-bottom:8px}
  .res-row .kind{font-family:var(--font-mono);font-size:.64rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--accent)}
  .res-row p{font-size:.93rem;color:var(--ink-2);line-height:1.72}
  .res-row .go{font-family:var(--font-mono);font-size:.7rem;color:var(--ink-3);
    white-space:nowrap;padding-top:6px}
  .res-row:hover .go{color:var(--accent)}
  @media (max-width:900px){.res-row{grid-template-columns:1fr;gap:10px}
    .res-row .n{padding-top:0}.res-row .go{display:none}}
"""

RES_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 자료실</div>
    <h1 class="d1">계약 없이도<br>바로 쓰실 수 있게</h1>
    <p class="lead">실제 과업에서 쓰는 자료를 그대로 올려 두었습니다.
       로그인도, 이메일 입력도 필요 없습니다.
       <b>다른 업체와 일하실 때 쓰셔도 됩니다.</b> 그러라고 만든 문서입니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="res-list">
      <a class="res-row" href="/resources/pentest-rfp/">
        <span class="n">01</span>
        <div><span class="kind">Checklist</span><h3>모의해킹 제안서 비교 체크리스트</h3></div>
        <p>같은 “웹 모의해킹”인데 견적이 몇 배씩 차이 나는 이유를 항목으로 정리했습니다.
           업체에 그대로 물어보실 수 있도록 질문 형태로 썼습니다.</p>
        <span class="go">열기 →</span>
      </a>
      <a class="res-row" href="/resources/isms-p-readiness/">
        <span class="n">02</span>
        <div><span class="kind">Self-check</span><h3>ISMS-P 착수 전 자가점검</h3></div>
        <p>컨설팅을 부르기 전에 스스로 확인할 수 있는 항목입니다.
           여기서 “아니오”가 많을수록 준비 기간이 길어집니다.</p>
        <span class="go">열기 →</span>
      </a>
      <a class="res-row" href="/resources/report-anatomy/">
        <span class="n">03</span>
        <div><span class="kind">Sample</span><h3>진단 보고서 구성 샘플</h3></div>
        <p>보고서가 어떻게 생겼는지 목차와 각 장의 작성 기준, 발견 사항 1건의 서술 예시를 공개합니다.</p>
        <span class="go">열기 →</span>
      </a>
    </div>
    <p class="tiny" style="margin-top:30px">
      필요한 자료가 없다면 <a href="/contact/" style="border-bottom:1px solid var(--rule-2)">알려주세요</a>.
      반복해서 요청받는 주제부터 문서로 만듭니다.
    </p>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">체크리스트를 채우다<br>막히면 물어보세요</h2>
      <p class="lead">항목 해석이나 우리 환경에 맞는 판단이 필요하시면 회신드립니다. 상담 자체에는 비용이 없습니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <a class="btn" href="/contact/">상담 요청</a>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 문서 공통
# ══════════════════════════════════════════════════════════════════════
DOC_CSS = """
  .doc-wrap{display:grid;grid-template-columns:220px 1fr;gap:56px;align-items:start}
  .toc{position:sticky;top:96px;border-top:1px solid var(--ink);padding-top:16px}
  .toc .k{font-family:var(--font-mono);font-size:.62rem;letter-spacing:.14em;
    text-transform:uppercase;color:var(--ink-3);display:block;margin-bottom:14px}
  .toc a{display:block;font-size:.86rem;color:var(--ink-2);padding:7px 0;line-height:1.5}
  .toc a:hover{color:var(--accent)}
  .doc-body{max-width:74ch}
  .doc-body h2{font-size:1.24rem;margin:52px 0 16px;padding-top:22px;border-top:1px solid var(--ink);
    letter-spacing:-.02em;scroll-margin-top:96px}
  .doc-body h2:first-child{margin-top:0}
  .doc-body h3{font-size:1rem;margin:30px 0 10px}
  .doc-body p{font-size:.98rem;color:var(--ink-2);line-height:1.82;margin-bottom:16px}
  .doc-body b{color:var(--ink);font-weight:600}
  .doc-body .q{border-left:2px solid var(--accent);padding:4px 0 4px 20px;margin:18px 0 20px}
  .doc-body .q .ask{font-size:.98rem;color:var(--ink);font-weight:500;margin-bottom:8px;line-height:1.7}
  .doc-body .q .good{font-size:.9rem;color:var(--ink-2);line-height:1.75}
  .doc-body .q .good em{font-style:normal;font-family:var(--font-mono);font-size:.62rem;
    letter-spacing:.12em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:5px}
  .chk{border-top:1px solid var(--rule);margin:20px 0}
  .chk li{list-style:none;display:grid;grid-template-columns:26px 1fr;gap:12px;padding:14px 0;
    border-bottom:1px solid var(--rule);font-size:.94rem;color:var(--ink-2);line-height:1.72}
  .chk li::before{content:"□";color:var(--ink-3);font-size:1rem;line-height:1.5}
  .chk li b{color:var(--ink);font-weight:600}
  .chk li .why{display:block;font-size:.85rem;color:var(--ink-3);margin-top:5px;line-height:1.6}
  .doc-note{background:var(--wash);border-left:2px solid var(--accent);padding:18px 22px;
    font-size:.92rem;color:var(--ink-2);line-height:1.78;margin:26px 0}
  .toc-mobile{display:none}
  @media (max-width:980px){
    .doc-wrap{grid-template-columns:1fr;gap:0}
    .toc{display:none}
  }
"""


def _doc(kicker, h1, lead, toc, body):
    toc_html = "\n".join(f'      <a href="#{i}">{t}</a>' for i, t in toc)
    return f"""<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · <a href="/resources/">자료실</a> · {kicker}</div>
    <h1 class="d2">{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>

<section class="sec">
  <div class="shell doc-wrap">
    <nav class="toc">
      <span class="k">목차</span>
{toc_html}
    </nav>
    <div class="doc-body">
{body}
      <div style="margin-top:60px;padding-top:24px;border-top:1px solid var(--ink);display:flex;
                  gap:16px;flex-wrap:wrap;justify-content:space-between;align-items:center">
        <a class="alink" href="/resources/">자료실 목록</a>
        <a class="btn btn-sm" href="/contact/">해석이 필요하면 물어보기</a>
      </div>
    </div>
  </div>
</section>"""


# ══════════════════════════════════════════════════════════════════════
# 01. 모의해킹 제안서 비교 체크리스트
# ══════════════════════════════════════════════════════════════════════
_RFP_BODY = """      <p>모의해킹 견적은 같은 대상, 같은 이름의 과업인데도 업체마다 몇 배씩 차이가 납니다.
         대부분은 업체의 욕심이 아니라 <b>범위와 방식이 다르기 때문</b>입니다.
         아래 항목을 그대로 물어보시면 어느 제안이 무엇을 포함하고 있는지 드러납니다.</p>

      <div class="doc-note">
        이 문서는 특정 업체를 위해 쓰지 않았습니다. 받으신 제안서 전부에 같은 질문을 던지시면 됩니다.
      </div>

      <h2 id="s1">1. 진단 방식 — 도구인가 사람인가</h2>
      <p>가장 큰 비용 차이가 여기서 납니다. 스캐너 결과를 정리한 보고서와, 각 항목을 사람이 재현해
         오탐을 걸러낸 보고서는 작업량이 다릅니다.</p>
      <div class="q">
        <div class="ask">“자동 스캔과 수동 검증의 비중은 어느 정도입니까?”</div>
        <div class="good"><em>좋은 답변</em>수동 검증 항목을 구체적으로 말하고, 스캐너는 후보 탐색에만 쓴다고 답하는 경우.
          “도구 3종을 사용합니다”처럼 도구 이름만 나열하면 실제 검증 범위를 다시 물어보세요.</div>
      </div>
      <div class="q">
        <div class="ask">“오탐은 어떻게 처리합니까? 보고서에 오탐이 남을 수 있습니까?”</div>
        <div class="good"><em>좋은 답변</em>재현되지 않은 항목은 싣지 않거나 “확인 필요”로 분리한다고 답하는 경우.
          오탐 처리 기준이 없으면 조치 단계에서 담당자 시간이 그만큼 사라집니다.</div>
      </div>

      <h2 id="s2">2. 인증 이후 영역을 보는가</h2>
      <p>로그인 전 화면만 점검하는 진단은 실제 위험의 일부만 봅니다.
         권한별 계정을 발급해 <b>인가 우회, 수평·수직 권한 상승, 업무 논리 결함</b>을 확인하는지가 핵심입니다.</p>
      <div class="q">
        <div class="ask">“테스트 계정은 몇 종류나 필요합니까? 권한별로 다 보십니까?”</div>
        <div class="good"><em>좋은 답변</em>일반/관리자/타 조직 등 권한 조합을 요구하는 경우.
          계정을 요구하지 않는다면 인증 이후 영역을 보지 않겠다는 뜻일 수 있습니다.</div>
      </div>

      <h2 id="s3">3. API와 모바일이 범위에 있는가</h2>
      <p>화면만 점검하고 API를 제외하면, 가장 흔한 대량 정보 노출 경로가 빠집니다.
         모바일 앱이 있다면 <b>앱 자체 점검</b>과 <b>앱이 호출하는 API 점검</b>은 별개 작업입니다.</p>
      <div class="q">
        <div class="ask">“API 엔드포인트는 몇 개까지 포함됩니까? 산정 기준은 무엇입니까?”</div>
        <div class="good"><em>좋은 답변</em>엔드포인트 수 또는 기능 단위로 산정 기준을 제시하는 경우.
          “웹에 포함”이라고만 답하면 실제 점검 여부를 문서로 확인하세요.</div>
      </div>

      <h2 id="s4">4. 재점검이 포함되어 있는가</h2>
      <p>조치 후 재점검이 없으면 “고쳤다고 생각한 상태”로 끝납니다.
         포함 여부와 <b>범위</b>(전체 재수행 / 조치 항목 한정)를 함께 확인하세요.</p>
      <div class="q">
        <div class="ask">“재점검은 몇 회 포함이고, 범위는 어디까지입니까? 추가 비용이 발생하는 조건은?”</div>
        <div class="good"><em>좋은 답변</em>포함 횟수와 범위, 유효 기간(예: 종료 후 N개월 내)을 숫자로 답하는 경우.</div>
      </div>

      <h2 id="s5">5. 산출물이 정의되어 있는가</h2>
      <p>“보고서 1식”은 정의가 아닙니다. 어떤 문서를 몇 종 받는지, 각 문서에 무엇이 들어가는지를
         계약서에 적을 수 있어야 합니다.</p>
      <ul class="chk">
        <li><span><b>발견 사항별 재현 절차</b>가 포함되는가
          <span class="why">요청·응답 등 근거 없이 “취약함”만 적힌 보고서는 조치에 쓸 수 없습니다.</span></span></li>
        <li><span><b>위험도 산정 기준</b>이 보고서에 명시되는가
          <span class="why">등급 정의가 없으면 “High가 왜 High인가”로 회의가 한 번 더 생깁니다.</span></span></li>
        <li><span><b>경영진 요약</b>과 <b>실무 조치 가이드</b>가 분리되는가</span></li>
        <li><span><b>조치 우선순위</b>가 제시되는가 (위험도만이 아니라 조치 난이도까지)</span></li>
        <li><span>보고 <b>회의</b>가 포함되는가, 몇 회인가</span></li>
      </ul>

      <h2 id="s6">6. 수행 규칙이 문서로 있는가</h2>
      <p>진단은 사고와 종이 한 장 차이입니다. 아래가 서면으로 정해지지 않으면 나중에 책임 문제가 생깁니다.</p>
      <ul class="chk">
        <li><span><b>대상 범위</b>가 IP·도메인·계정 단위로 특정되는가</span></li>
        <li><span><b>수행 시간대</b>와 가용성 영향 가능성에 대한 합의가 있는가</span></li>
        <li><span><b>비상 정지 조건</b>과 연락 체계가 정해져 있는가</span></li>
        <li><span><b>실데이터 취급 원칙</b>(열람 범위, 추출 금지)이 명시되는가</span></li>
        <li><span><b>Critical 발견 시 즉시 통보</b> 조항이 있는가</span></li>
      </ul>

      <h2 id="s7">7. 데이터 파기와 비밀유지</h2>
      <ul class="chk">
        <li><span><b>NDA</b>를 착수 전에 체결하는가</span></li>
        <li><span>진단 데이터의 <b>보관 기간</b>과 <b>파기 시점</b>이 정해져 있는가</span></li>
        <li><span><b>파기 확인서</b>를 제공하는가</span></li>
        <li><span>산출물 전달 <b>경로</b>가 안전하게 합의되어 있는가</span></li>
      </ul>

      <h2 id="s8">8. 누가 수행하는가</h2>
      <p>제안서에 적힌 회사와 실제 수행 인력이 다른 경우가 있습니다.
         국내 조달에서 구매자가 실제로 평가하는 항목이기도 합니다.</p>
      <ul class="chk">
        <li><span><b>참여 인력의 이력</b>(경력 연차, 수행 분야)이 제시되는가</span></li>
        <li><span>재하도급 여부와 범위가 명시되는가</span></li>
        <li><span>과업 중 <b>인력 교체</b> 시 통보·승인 절차가 있는가</span></li>
      </ul>

      <h2 id="s9">비교표로 쓰기</h2>
      <p>제안서가 여러 건이면 아래 형태로 옮겨 놓고 비교하시면 차이가 한눈에 보입니다.</p>
      <table class="spec">
        <thead><tr><th>항목</th><th>업체 A</th><th>업체 B</th><th>업체 C</th></tr></thead>
        <tbody>
          <tr><td data-l="항목">수동 검증 비중</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">인증 이후 영역</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">API 포함 / 산정 기준</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">재점검 횟수 · 범위</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">산출물 종수</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">수행 규칙 문서</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">파기 확인서</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">참여 인력 이력</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
          <tr><td data-l="항목">금액</td><td data-l="업체 A"></td><td data-l="업체 B"></td><td data-l="업체 C"></td></tr>
        </tbody>
      </table>
      <div class="doc-note">
        쉴더스랩의 답은 <a href="/services/pentest/">모의해킹 서비스 페이지</a>와
        <a href="/method/">진단 방법론</a>에 미리 적어 두었습니다. 같은 기준으로 비교해 보세요.
      </div>"""

# ══════════════════════════════════════════════════════════════════════
# 02. ISMS-P 착수 전 자가점검
# ══════════════════════════════════════════════════════════════════════
_ISMS_BODY = """      <p>같은 규모의 조직인데 어떤 곳은 준비에 6개월, 어떤 곳은 1년 반이 걸립니다.
         차이를 만드는 것은 문서량보다 <b>지금 남아 있는 운영 기록</b>과 <b>범위 확정 여부</b>입니다.
         컨설팅을 부르기 전에 아래를 먼저 확인해 보세요.</p>

      <div class="doc-note">
        “아니오”가 많다고 문제가 아닙니다. 준비 기간을 현실적으로 잡는 데 필요한 정보일 뿐입니다.
        오히려 이 목록을 채워서 오시면 첫 미팅에서 바로 일정 산정이 가능합니다.
      </div>

      <h2 id="a">A. 범위</h2>
      <ul class="chk">
        <li><span>인증을 받을 <b>서비스와 조직의 경계</b>가 문장으로 적혀 있다.
          <span class="why">“회사 전체”는 범위가 아닙니다. 어떤 서비스, 어떤 조직, 어떤 시스템인지가 필요합니다.</span></span></li>
        <li><span>범위 안 <b>자산 목록</b>(서버·네트워크·애플리케이션·개인정보 처리 시스템)이 최신이다.</span></li>
        <li><span>범위 <b>밖</b> 시스템과의 <b>연계 지점</b>이 파악되어 있다.
          <span class="why">심사에서 자주 질문받는 지점입니다. 연계 구간의 통제가 없으면 범위 설정이 무의미해집니다.</span></span></li>
        <li><span>클라우드·SaaS 사용 현황이 목록화되어 있다.</span></li>
      </ul>

      <h2 id="b">B. 문서</h2>
      <ul class="chk">
        <li><span>정보보호 <b>정책·지침</b>이 존재한다.</span></li>
        <li><span>그 문서의 내용이 <b>실제 업무 절차와 일치</b>한다.
          <span class="why">여기서 “아니오”면 문서를 새로 만드는 것보다 현실에 맞게 걷어내는 작업이 먼저입니다.</span></span></li>
        <li><span>문서에 <b>제정·개정 이력</b>과 승인 흔적이 남아 있다.</span></li>
        <li><span>담당자가 바뀌어도 찾을 수 있는 위치에 보관되어 있다.</span></li>
      </ul>

      <h2 id="c">C. 운영 기록 — 기간이 가장 크게 갈리는 항목</h2>
      <p>정책은 하루면 만들 수 있지만, 운영 기록은 <b>시간이 지나야 생깁니다</b>.
         아래 항목이 비어 있으면 그만큼의 시간이 준비 기간에 그대로 더해집니다.</p>
      <ul class="chk">
        <li><span>최근 <b>접근권한 검토</b>를 수행하고 기록을 남긴 적이 있다.</span></li>
        <li><span><b>변경 관리</b>(시스템 변경 요청·승인·적용) 기록이 남아 있다.</span></li>
        <li><span><b>접속기록</b>을 보관하고, 주기적으로 점검한 흔적이 있다.</span></li>
        <li><span><b>백업 복구 시험</b>을 수행하고 결과를 기록한 적이 있다.</span></li>
        <li><span><b>보안 교육</b>을 실시하고 참석 기록이 있다.</span></li>
        <li><span><b>취약점 점검</b>을 수행하고 조치 결과를 기록한 적이 있다.</span></li>
      </ul>

      <h2 id="d">D. 위험평가</h2>
      <ul class="chk">
        <li><span>위험평가를 수행한 적이 있고, <b>산정 기준</b>이 문서로 있다.</span></li>
        <li><span>수용 가능한 위험 수준(DoA)을 <b>누가 결정했는지</b> 설명할 수 있다.</span></li>
        <li><span>위험평가 결과가 <b>조치 계획</b>으로 이어졌고 이행 상태를 추적하고 있다.</span></li>
        <li><span>기술 취약점 진단 결과가 위험평가에 <b>반영</b>되어 있다.
          <span class="why">진단과 관리체계를 다른 업체가 맡으면 이 연결이 자주 끊깁니다.</span></span></li>
      </ul>

      <h2 id="e">E. 개인정보 (ISMS-P를 받는 경우)</h2>
      <ul class="chk">
        <li><span>개인정보 <b>처리 흐름</b>(수집→저장→이용→제공/위탁→파기)이 그려져 있다.</span></li>
        <li><span>수집 항목별 <b>법적 근거</b>를 설명할 수 있다.</span></li>
        <li><span><b>위탁·재위탁</b> 현황이 목록화되어 있고 계약서에 필수 조항이 있다.</span></li>
        <li><span><b>국외이전</b>(해외 클라우드·SaaS 포함) 현황이 파악되어 있다.</span></li>
        <li><span>처리방침이 <b>현재 실제 처리와 일치</b>한다.</span></li>
      </ul>

      <h2 id="f">F. 조직과 일정</h2>
      <ul class="chk">
        <li><span>보안 <b>담당자</b>가 지정되어 있고, 업무 시간이 확보되어 있다.
          <span class="why">겸직이어도 괜찮지만 “아무도 없음”이면 컨설팅 효과가 크게 떨어집니다.</span></span></li>
        <li><span>경영진이 <b>의사결정</b>에 참여할 수 있다(위험 수용 결정 등).</span></li>
        <li><span>시스템 담당 조직이 <b>인터뷰와 조치</b>에 협조 가능하다.</span></li>
        <li><span>목표 심사 시점이 정해져 있다면, 그 날짜가 <b>고정</b>인지 조정 가능한지 안다.</span></li>
      </ul>

      <h2 id="g">결과를 어떻게 읽을까</h2>
      <p><b>C(운영 기록)에서 “아니오”가 3개 이상</b>이면, 문서 작업보다 기록을 남기는 활동을 먼저 시작하는 편이
         전체 일정을 줄입니다. <b>A(범위)에서 “아니오”가 있으면</b> 다른 작업을 시작하기 전에 범위부터 확정해야
         산출물을 두 번 만들지 않습니다.</p>
      <p>이 목록을 채운 상태로 상담을 요청하시면, 첫 회신에서 준비 기간과 우선순위를 훨씬 구체적으로 드릴 수 있습니다.</p>
      <div class="doc-note">
        의무 대상 여부 판단이 필요하시면 사업 현황(매출 규모, 이용자 수, 업종)을 함께 알려주세요.
        근거 조문과 함께 검토 의견을 정리해 회신드립니다.
      </div>"""

# ══════════════════════════════════════════════════════════════════════
# 03. 진단 보고서 구성 샘플
# ══════════════════════════════════════════════════════════════════════
_REPORT_BODY = """      <p>보고서를 받아 보기 전에는 그 보고서가 쓸 만한지 알기 어렵습니다.
         그래서 저희 보고서의 <b>목차와 각 장의 작성 기준</b>, 그리고 발견 사항 한 건이 실제로 어떻게 기술되는지를
         공개합니다.</p>

      <h2 id="toc">1. 목차</h2>
      <table class="spec">
        <thead><tr><th>장</th><th>내용</th><th>읽는 사람</th></tr></thead>
        <tbody>
          <tr><td data-l="장">0. 요약</td><td data-l="내용">과업 개요, 총평, 등급별 발견 건수, 즉시 조치 필요 항목</td>
            <td data-l="독자">경영진</td></tr>
          <tr><td data-l="장">1. 과업 개요</td><td data-l="내용">범위(포함·제외), 수행 기간, 수행 방식, 제약 조건</td>
            <td data-l="독자">공통</td></tr>
          <tr><td data-l="장">2. 판정 기준</td><td data-l="내용">위험도 등급 정의, 산정 방식, “확인 필요” 처리 원칙</td>
            <td data-l="독자">공통</td></tr>
          <tr><td data-l="장">3. 발견 사항</td><td data-l="내용">항목별 상세 — 아래 3장 형식 참조</td>
            <td data-l="독자">실무</td></tr>
          <tr><td data-l="장">4. 조치 우선순위</td><td data-l="내용">위험도 × 조치 난이도 매트릭스, 권장 순서</td>
            <td data-l="독자">실무 · 관리자</td></tr>
          <tr><td data-l="장">5. 잔여위험</td><td data-l="내용">이번 과업에서 닫지 못한 항목과 사유</td>
            <td data-l="독자">경영진 · 감사</td></tr>
          <tr><td data-l="장">부록 A</td><td data-l="내용">점검 항목 전체 목록과 판정 결과(양호 포함)</td>
            <td data-l="독자">감사 · 심사 대응</td></tr>
          <tr><td data-l="장">부록 B</td><td data-l="내용">수행 이력 · 사용 도구 · 데이터 파기 확인</td>
            <td data-l="독자">감사</td></tr>
        </tbody>
      </table>
      <p><b>부록 A를 넣는 이유</b>: 취약 항목만 담긴 보고서는 인증 심사나 내부 감사에서
         “점검은 했는데 무엇을 점검했는지”를 증명하지 못합니다. 양호 판정 항목도 근거와 함께 남깁니다.</p>

      <h2 id="finding">2. 발견 사항 1건의 서술 형식</h2>
      <p>발견 사항은 아래 8개 항목을 고정 순서로 씁니다. 항목이 비면 그 이유를 적습니다.</p>
      <ul class="chk">
        <li><span><b>식별번호 · 제목</b> — 조치 티켓에 그대로 옮길 수 있는 한 줄</span></li>
        <li><span><b>위험도 · 산정 근거</b> — 등급과 함께 왜 그 등급인지</span></li>
        <li><span><b>대상</b> — URL·호스트·파일 경로 등 특정 가능한 위치</span></li>
        <li><span><b>현상</b> — 확인된 사실만. 추정은 별도 표기</span></li>
        <li><span><b>재현 절차</b> — 같은 결과를 얻기 위한 최소 단계와 근거(요청/응답, 설정값, 명령)</span></li>
        <li><span><b>영향</b> — 이 항목이 악용되면 무엇이 가능한가</span></li>
        <li><span><b>조치 방향</b> — 무엇을 어떻게. 설정 예시나 코드 수준 권고 포함</span></li>
        <li><span><b>조치 확인 방법</b> — 담당자가 스스로 닫혔는지 확인하는 방법</span></li>
      </ul>

      <h3>예시 (익명화 · 형식 설명용)</h3>
      <div class="doc-note" style="background:var(--paper-2);border-left-color:var(--rule-2)">
        <p style="margin:0 0 10px"><b>WEB-014 · 타 사용자 주문 정보 조회 가능 (인가 우회)</b></p>
        <p style="margin:0 0 10px"><b>위험도</b> High — 인증된 일반 사용자 권한으로 타인의 개인정보에 접근 가능하며,
          재현이 안정적임. 대량 조회 가능 여부는 아래 “영향” 참조.</p>
        <p style="margin:0 0 10px"><b>대상</b> GET /api/v2/orders/{orderId} — 운영 도메인</p>
        <p style="margin:0 0 10px"><b>현상</b> 주문 식별자를 다른 값으로 변경해 요청하면 소유자 검증 없이 응답함.
          응답 본문에 수령인 성명·연락처·주소가 포함됨.</p>
        <p style="margin:0 0 10px"><b>재현 절차</b> ① 계정 A로 로그인해 주문 상세 조회 → ② 요청의 orderId를
          계정 B의 주문 식별자로 변경 → ③ 200 응답과 함께 계정 B의 정보가 반환됨. (요청·응답 원문 첨부)</p>
        <p style="margin:0 0 10px"><b>영향</b> 식별자가 순차 증가 형식이어서 반복 요청으로 다수 주문 정보 수집이 가능함.
          개인정보 유출로 직결됨.</p>
        <p style="margin:0 0 10px"><b>조치 방향</b> 서버 측에서 요청 주체와 리소스 소유자의 일치를 검증.
          식별자를 추측 불가능한 값으로 변경하는 것은 보완책이며 단독 조치로는 불충분함.</p>
        <p style="margin:0"><b>조치 확인 방법</b> 동일 절차로 타 계정 식별자 요청 시 403 응답 확인.
          접근 실패 로그가 남는지 함께 확인.</p>
      </div>

      <h2 id="what">3. 이 형식이 만드는 차이</h2>
      <p><b>조치 확인 방법</b>이 있으면 담당자가 재점검을 기다리지 않고 스스로 검증할 수 있습니다.
         <b>산정 근거</b>가 있으면 등급을 두고 회의가 한 번 줄어듭니다.
         <b>추정과 사실의 분리</b>가 있으면 오탐으로 인한 불필요한 작업이 사라집니다.</p>
      <p>보고서 형식은 취향의 문제처럼 보이지만, 실제로는 조치가 끝까지 가느냐를 결정합니다.</p>

      <h2 id="ask">4. 요청하실 수 있는 것</h2>
      <ul class="chk">
        <li><span>사내 티켓 시스템에 맞춘 <b>발견 사항 CSV/JSON</b> 형식</span></li>
        <li><span>인증 심사 대응용 <b>항목 매핑표</b>(발견 사항 ↔ 인증기준 항목)</span></li>
        <li><span>경영진 보고용 <b>요약 슬라이드</b></span></li>
        <li><span>영문 보고서(해외 본사·감사 대응용)</span></li>
      </ul>
      <p>착수 전에 말씀해 주시면 산출물 목록에 포함해 계약서에 명시합니다.</p>"""


RES_DOCS = [
    {
        "slug": "pentest-rfp",
        "title": "모의해킹 제안서 비교 체크리스트 | 쉴더스랩 자료실",
        "desc": "모의해킹 견적이 몇 배씩 차이 나는 이유를 항목으로 정리한 체크리스트. "
                "업체에 그대로 물어볼 수 있는 질문 형태로 정리했습니다.",
        "body": _doc(
            "제안서 비교 체크리스트",
            "모의해킹 제안서<br>비교 체크리스트",
            "같은 “웹 모의해킹”인데 견적이 몇 배씩 차이 나는 이유는 대개 범위와 방식이 다르기 때문입니다. "
            "아래 질문을 모든 제안서에 똑같이 던져 보세요.",
            [("s1", "1. 진단 방식"), ("s2", "2. 인증 이후 영역"), ("s3", "3. API · 모바일"),
             ("s4", "4. 재점검"), ("s5", "5. 산출물"), ("s6", "6. 수행 규칙"),
             ("s7", "7. 파기 · 비밀유지"), ("s8", "8. 수행 인력"), ("s9", "비교표로 쓰기")],
            _RFP_BODY),
    },
    {
        "slug": "isms-p-readiness",
        "title": "ISMS-P 착수 전 자가점검 | 쉴더스랩 자료실",
        "desc": "컨설팅을 부르기 전에 스스로 확인하는 ISMS-P 준비 상태 자가점검 목록. "
                "범위·문서·운영 기록·위험평가·개인정보·조직 6개 영역.",
        "body": _doc(
            "ISMS-P 자가점검",
            "ISMS-P 착수 전<br>자가점검",
            "준비 기간을 좌우하는 것은 문서량보다 지금 남아 있는 운영 기록입니다. "
            "컨설팅을 부르기 전에 아래를 먼저 확인해 보세요.",
            [("a", "A. 범위"), ("b", "B. 문서"), ("c", "C. 운영 기록"), ("d", "D. 위험평가"),
             ("e", "E. 개인정보"), ("f", "F. 조직과 일정"), ("g", "결과 읽는 법")],
            _ISMS_BODY),
    },
    {
        "slug": "report-anatomy",
        "title": "진단 보고서 구성 샘플 | 쉴더스랩 자료실",
        "desc": "진단 보고서의 목차와 각 장의 작성 기준, 발견 사항 한 건이 실제로 어떻게 기술되는지 공개합니다.",
        "body": _doc(
            "보고서 구성 샘플",
            "진단 보고서<br>구성 샘플",
            "보고서를 받기 전에는 그것이 쓸 만한지 알기 어렵습니다. 목차와 각 장의 작성 기준, "
            "발견 사항 한 건의 서술 형식을 그대로 공개합니다.",
            [("toc", "1. 목차"), ("finding", "2. 발견 사항 형식"), ("what", "3. 형식이 만드는 차이"),
             ("ask", "4. 요청 가능 항목")],
            _REPORT_BODY),
    },
]
