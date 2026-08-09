# -*- coding: utf-8 -*-
"""신뢰 센터 · 규제 가이드
   리서치 결과 반영:
     · 보안 컨설팅사에 대한 실제 의심은 "우리 데이터가 어떻게 되나"이다. 여기에 직접 답한다.
     · 자사 사이트를 자기 체크리스트로 점검하고 **잔여위험까지 공개**한다(첫 고객은 자기 자신).
     · 규제 정보는 기준일과 출처를 함께 밝힌다. 정확도 자체가 상품이다.
"""

# ══════════════════════════════════════════════════════════════════════
# 신뢰 센터
# ══════════════════════════════════════════════════════════════════════
TRUST_TITLE = "신뢰 센터 | 쉴더스랩 — 데이터 취급 · 계약 조건 · 자사 보안"
TRUST_DESC = ("맡기신 진단 데이터의 보관 위치와 파기 시점, 계약 단계에서 담당자가 확인하실 조건을 정리했습니다. "
              "자사 웹사이트에 적용한 조치와 남은 위험, 취약점 제보 창구도 함께 싣습니다.")

TRUST_CSS = """
  .trust-kv{border-top:1px solid var(--ink)}
  .trust-kv .row{display:grid;grid-template-columns:200px 1fr;gap:24px;padding:17px 0;
    border-bottom:1px solid var(--rule)}
  .trust-kv .k{font-family:var(--font-mono);font-size:.66rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--ink-3);padding-top:4px}
  .trust-kv .v{font-size:.94rem;color:var(--ink-2);line-height:1.72}
  .trust-kv .v b{color:var(--ink)}
  .state{display:inline-block;font-family:var(--font-mono);font-size:.62rem;letter-spacing:.1em;
    text-transform:uppercase;padding:2px 8px;border:1px solid;margin-right:8px;vertical-align:1px}
  .state.yes{border-color:var(--accent);color:var(--accent)}
  .state.no{border-color:var(--rule-2);color:var(--ink-3)}
  .state.plan{border-color:var(--ochre);color:var(--ochre)}
  @media (max-width:720px){.trust-kv .row{grid-template-columns:1fr;gap:6px}}
"""

TRUST_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 신뢰 센터</div>
    <h1 class="d1" data-content="trust.hero_title">우리에게 맡긴 것이<br>어떻게 다뤄지는지</h1>
    <p class="lead" data-content="trust.hero_lead">진단이 끝나도 구성도와 계정 체계, 취약점 목록은 저희 쪽에 남기 때문에
       그 자료를 어디에 두는지, 얼마나 갖고 있다가 어떻게 없애는지를 아래에 적었습니다.
       계약 전에 미리 보셔도 됩니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Data handling</span></div>
      <div class="body">
        <h2 class="d2">진단 데이터 취급</h2>
        <p class="lead">과업이 진행되면 구성 정보와 로그, 발견 사항과 화면 캡처가 저희 손에 들어옵니다.
           그 자료를 어떻게 다루는지 아래에 적었고, 여기 적힌 문장은 계약서에도 같은 내용으로 들어갑니다.</p>
      </div>
    </div>
    <div class="trust-kv">
      <div class="row"><div class="k">수집 범위</div>
        <div class="v">과업에 필요한 만큼만 봅니다. <b>고객사의 실제 개인정보는 원칙적으로 열람 대상에서
          제외합니다.</b> 확인이 꼭 필요하면 먼저 합의한 뒤 최소 건수만 화면으로 살피고, 내려받거나 복제하는 일 없이 그 자리에서 끝냅니다.</div></div>
      <div class="row"><div class="k">보관</div>
        <div class="v">과업마다 저장소를 나누고, 그 과업에 투입된 인력에게만 접근 권한을 줍니다.
          사본은 지정한 저장소 안에서만 오갑니다.</div></div>
      <div class="row"><div class="k">전달</div>
        <div class="v">산출물은 착수할 때 정한 경로로만 오갑니다. 고객사에서 쓰시던 전달 체계가 있으면 그 체계를 우선 따르고,
          메일에 붙이기 곤란한 자료는 착수 회의에서 별도 경로를 정해 둡니다.</div></div>
      <div class="row"><div class="k">보존 기간</div>
        <div class="v">기본값은 <b>과업 종료 후 3개월</b>. 재점검이나 뒤늦게 오는 질의에 답하려면 그만큼은 필요합니다.
          계약으로 더 짧게 잡아도 되고, 종료 즉시 파기를 요청하셔도 됩니다.</div></div>
      <div class="row"><div class="k">파기</div>
        <div class="v">기간이 끝나면 복구할 수 없는 방식으로 지운 뒤 <b>파기 확인서</b>를 드리며,
          종이로 뽑은 것이 있었다면 파쇄한 사실까지 확인서에 적습니다.</div></div>
      <div class="row"><div class="k">인력 통제</div>
        <div class="v">과업에 들어가는 사람은 착수 전에 각자 비밀유지 서약서에 서명합니다.
          누가 어떤 자산에 접근했는지는 기록으로 남습니다. 사람이 바뀌면 바뀌기 전에 알려드립니다.
          요청하시면 <b>참여자 명단과 역할</b>을 계약 단계에서 서면으로 드립니다.</div></div>
      <div class="row"><div class="k">2차 이용</div>
        <div class="v">고객사 자료는 저희 홍보에 쓰지 않습니다. 세미나 발표도, 제안서 사례도 마찬가지입니다.
          익명 처리를 거쳤더라도 <b>인용은 서면 동의를 받은 뒤에만 합니다.</b></div></div>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Contract</span></div>
      <div class="body">
        <h2 class="d2">계약 조건 · 보유 지위</h2>
        <p class="lead">계약 검토 단계에서 담당자가 결국 확인하게 되는 항목만 모아 미리 표로 만들었습니다.
           보유 지위는 있는 그대로 적습니다.</p>
      </div>
    </div>
    <div class="trust-kv">
      <div class="row"><div class="k">비밀유지계약</div>
        <div class="v"><span class="state yes">제공</span>착수 전에 맺습니다. 고객사 양식이 있으면 그쪽을 먼저 검토합니다.
          쓰시던 양식이 없으면 저희 표준 양식을 미리 보내드립니다.</div></div>
      <div class="row"><div class="k">재하도급</div>
        <div class="v"><span class="state no">없음</span>받은 과업을 제3자에게 넘기지 않습니다.
          외부 전문가를 불러야 할 일이 생기면 먼저 알리고 동의를 받은 뒤에 착수합니다.</div></div>
      <div class="row"><div class="k">정보보호 전문서비스기업 지정</div>
        <div class="v"><span class="state plan">미보유</span>「정보보호산업의 진흥에 관한 법률」에 따른 지정 사업자가 아닙니다.
          주요정보통신기반시설 취약점 분석·평가처럼 이 지정을 요구하는 과업은 지정 사업자의 몫입니다.
          지정 여부가 바뀌면 이 표부터 고칩니다.</div></div>
      <div class="row"><div class="k">개인정보 영향평가 기관</div>
        <div class="v"><span class="state no">미해당</span>지정 평가기관이 아닙니다. 평가를 받는 쪽에서 <b>대응 준비</b>를 돕는 일까지가 저희가 맡는 범위입니다.</div></div>
      <div class="row"><div class="k">배상책임보험</div>
        <div class="v"><span class="state plan">확인 필요</span>가입 여부와 한도는 계약 단계에서 서면으로 확인해 드립니다.
          확정되면 한도 금액까지 이 표에 옮겨 적습니다.</div></div>
      <div class="row"><div class="k">법인 신원</div>
        <div class="v">상호와 대표자, 사업자등록번호와 주소, 개인정보 보호책임자를 전 페이지 하단
          사업자 정보란에 싣습니다. 서면이 필요하시면 계약 단계에서 따로 드립니다.</div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Our own site</span></div>
      <div class="body">
        <h2 class="d2">첫 고객은<br>우리 자신입니다</h2>
        <p class="lead">이 사이트를 저희 체크리스트로 점검하고, 적용한 조치와 <b>아직 남아 있는 위험</b>을 한자리에 적었습니다.
           고객사에 드리는 보고서와 형식이 같으니 계약 전에 저희 보고서가 어떻게 생겼는지 미리 보시는 셈입니다.</p>
      </div>
    </div>
    <div class="g12">
      <div class="c6">
        <h3 class="d3" style="font-size:1rem;margin-bottom:16px">적용한 조치</h3>
        <ul class="ticks">
          <li><span><b>전 구간 HTTPS</b> — 인증서를 걸고, HTTP로 들어온 요청은 전부 되돌립니다.</span></li>
          <li><span><b>외부 스크립트 0개</b> — 백엔드 클라이언트까지 직접 호스팅해서, 콘텐츠 보안 정책(CSP)이
            허용하는 스크립트 출처를 자기 도메인 하나로 묶었습니다.</span></li>
          <li><span><b>개인정보 테이블은 열려 있지 않습니다</b> — 문의·지원 데이터에는 공개 조회 정책을 아예
            만들지 않았습니다. 적재는 서버측 검증 함수로만 이뤄집니다. 익명 키로는 한 줄도 읽히지 않습니다.</span></li>
          <li><span><b>제출 남용 방어</b> — 서버에서 입력을 검증하고, 요청 빈도를 두 겹으로 제한하고,
            폼에는 허니팟을 심었습니다.</span></li>
          <li><span><b>보관 기간 자동 삭제</b> — 방문 로그와 문의·지원 데이터에는 보존 기간이 걸려 있고,
            기간이 지난 행부터 스케줄러가 지웁니다.</span></li>
          <li><span><b>관리자 접근 통제</b> — 미리 등록한 계정만 들어옵니다. 관리자가 무엇을 했는지는
            전부 감사 로그에 남습니다.</span></li>
        </ul>
      </div>
      <div class="c5 start8">
        <h3 class="d3" style="font-size:1rem;margin-bottom:16px">남아 있는 위험</h3>
        <ul class="ticks">
          <li><span><b>인라인 스크립트 허용</b> — 정적 사이트 구조 때문에 CSP에서 인라인 스크립트를 아직
            허용합니다. 출력값은 전부 이스케이프하고 CMS 본문은 평문으로만 출력합니다.
            그래도 이 항목은 완화가 아니라 <b>수용</b>으로 분류합니다.</span></li>
          <li><span><b>외부 웹폰트</b> — 서체를 밖에서 불러오는 탓에 방문자 IP가 해당 사업자에게 넘어갑니다.
            처리방침 위탁 항목에 이 사실을 밝혔고, 자체 호스팅으로 옮기는 방안을 검토하고 있습니다.</span></li>
          <li><span><b>법인 정보 미게시</b> — 하단 사업자 정보란이 비어 있습니다. 확정되는 대로 채웁니다.</span></li>
        </ul>
        <p class="tiny" style="margin-top:20px">
          2026년 7월 점검 기준. 항목이 해소되면 해소일을 붙여 이력에 남깁니다. 분기마다 다시 점검하고 이 날짜를 갱신합니다.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="sec band-3">
  <div class="shell g12">
    <div class="c5 col-head">
      <span class="lbl">04 / Vulnerability disclosure</span>
      <h2 class="d2">취약점을<br>발견하셨다면</h2>
      <p class="lead">이 사이트나 저희가 운영하는 자산에서 이상한 점을 발견하셨습니까?
         알려주시면 확인하겠습니다. 선의로 제보해 주신 분께는 법적 책임을 묻지 않습니다.</p>
    </div>
    <div class="c6 start7">
      <div class="trust-kv">
        <div class="row"><div class="k">접수</div>
          <div class="v"><a href="mailto:contact@shilderslab.com" style="border-bottom:1px solid var(--rule-2)">contact@shilderslab.com</a>
            — 제목 앞에 <b>[제보]</b>를 붙여 주시면 우선 확인합니다.</div></div>
        <div class="row"><div class="k">회신</div>
          <div class="v">영업일 기준 <b>3일 안에</b> 접수를 알려드립니다. 검토 결과는 <b>14일 안에</b> 회신하는 것을 목표로 합니다.</div></div>
        <div class="row"><div class="k">범위</div>
          <div class="v">shilderslab.com과 그 하위 경로입니다. 서비스 거부(DoS)와 물리적 침입, 사회공학은
            제외합니다. 제3자 서비스를 건드리는 시험도 마찬가지입니다.</div></div>
        <div class="row"><div class="k">원칙</div>
          <div class="v">확인에 필요한 범위에서만 시험해 주시고, 다른 사람의 데이터를 열어 보거나 서비스를
            멈추게 하는 시도는 피해 주시기 바랍니다. 공개는 조치가 끝난 뒤로 미뤄 주시면 좋겠습니다.</div></div>
        <div class="row"><div class="k">사례</div>
          <div class="v">금전 포상 제도는 운영하지 않습니다. 원하시면 조치를 마친 뒤 공개 감사 표기를 남겨 드립니다.</div></div>
        <div class="row"><div class="k">기계 판독</div>
          <div class="v"><a href="/.well-known/security.txt" style="border-bottom:1px solid var(--rule-2)">/.well-known/security.txt</a></div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7 col-head">
      <span class="lbl">Contact</span>
      <h2 class="d2">더 확인하고 싶은<br>조건이 있으면 말씀해 주세요</h2>
      <p class="lead">계약 조건이든 데이터 취급이든, 이 표에 없는 항목이 필요하시면 문의로 남겨 주시면 됩니다.
         투입 인력 구성까지 계약 전에 서면으로 답변드립니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <a class="btn" href="/contact/">문의하기</a>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════════
# 규제 가이드
# ══════════════════════════════════════════════════════════════════════
REG_TITLE = "규제 가이드 | 쉴더스랩 — ISMS-P · 개인정보 · CSAP 한눈에"
REG_DESC = ("ISMS/ISMS-P와 개인정보보호법 안전성 확보조치, CSAP와 ISO 27001을 근거 법령·대상·주기로 "
            "비교했습니다. 법령이 수행 주체를 정해 둔 업무가 무엇인지도 함께 구분했습니다.")

REG_CSS = """
  .reg-note{background:var(--paper-2);border-left:2px solid var(--ochre);padding:16px 20px;
    font-size:.88rem;color:var(--ink-2);line-height:1.75;margin:0 0 34px}
  .split3{display:grid;grid-template-columns:repeat(3,1fr);gap:0 var(--gut)}
  .split3 .b{border-top:1px solid var(--ink);padding:18px 0 28px}
  .split3 .b .k{font-family:var(--font-mono);font-size:.64rem;letter-spacing:.12em;
    text-transform:uppercase;display:block;margin-bottom:12px}
  .split3 .b.a .k{color:var(--accent)}
  .split3 .b.n .k{color:var(--bad)}
  .split3 .b.m .k{color:var(--ochre)}
  .split3 .b p{font-size:.9rem;color:var(--ink-2);line-height:1.72;margin-bottom:12px}
  .split3 .b ul{list-style:none;display:grid;gap:8px}
  .split3 .b li{font-size:.88rem;color:var(--ink-2);padding-left:14px;position:relative;line-height:1.6}
  .split3 .b li::before{content:"·";position:absolute;left:0;color:var(--ink-3)}
  @media (max-width:900px){.split3{grid-template-columns:1fr}}
"""

REG_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 규제 가이드</div>
    <h1 class="d1" data-content="regulations.hero_title">무엇이 우리에게<br>해당되는가</h1>
    <p class="lead" data-content="regulations.hero_lead">제도 이름은 익숙한데 우리 회사가 어디에 걸리는지는 애매하실 겁니다.
       그래서 국내 정보보호 제도를 근거 법령과 대상, 주기로 나란히 놓고 정리했습니다.
       다만 수치와 해석은 원문으로 최종 확인하시는 편이 안전합니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="reg-note">
      <b>기준일 안내</b> — 2026년 7월에 정리한 내용입니다. 고시와 시행령은 언제든 개정되므로
      실제 대응에 들어가실 때는 소관 기관의 최신 원문을 확인하셔야 합니다.
      어느 조문인지 확인이 필요하시면 <a href="/contact/" style="border-bottom:1px solid var(--rule-2)">문의</a>주세요.
      근거 조문을 붙여 회신드립니다.
    </div>

    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Overview</span></div>
      <div class="body"><h2 class="d2">제도 비교</h2></div>
    </div>
    <table class="spec">
      <thead><tr><th>제도</th><th>성격</th><th>주요 대상</th><th>주기</th><th>심사 주체</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="제도">ISMS</td>
          <td data-l="성격">법정 인증<br>(요건 충족 시 의무)</td>
          <td data-l="대상">정보통신서비스 제공자 등 법령이 정한 기준 충족 사업자</td>
          <td data-l="주기">최초 인증 후 <b>연 1회 사후심사</b>, 3년마다 갱신심사</td>
          <td data-l="주체">인증기관 · 심사기관</td>
        </tr>
        <tr>
          <td data-l="제도">ISMS-P</td>
          <td data-l="성격">법정 인증<br>(개인정보 영역 포함)</td>
          <td data-l="대상">ISMS 대상 중 개인정보 처리 영역까지 인증받으려는 조직</td>
          <td data-l="주기">ISMS와 동일</td>
          <td data-l="주체">인증기관 · 심사기관</td>
        </tr>
        <tr>
          <td data-l="제도">개인정보 안전성 확보조치</td>
          <td data-l="성격">법령상 <b>상시 의무</b><br>(인증 아님)</td>
          <td data-l="대상">개인정보처리자 전반</td>
          <td data-l="주기">상시 이행 · 정기 점검 권고</td>
          <td data-l="주체">자체 이행 (감독기관 조사 대상)</td>
        </tr>
        <tr>
          <td data-l="제도">개인정보 영향평가(PIA)</td>
          <td data-l="성격">법정 평가</td>
          <td data-l="대상">일정 규모 이상의 개인정보파일을 구축·운용하는 공공기관 등</td>
          <td data-l="주기">구축·변경 시</td>
          <td data-l="주체"><b>지정 평가기관</b></td>
        </tr>
        <tr>
          <td data-l="제도">주요정보통신기반시설<br>취약점 분석·평가</td>
          <td data-l="성격">법정 점검</td>
          <td data-l="대상">기반시설로 지정된 시설의 관리기관</td>
          <td data-l="주기">정기(연 단위)</td>
          <td data-l="주체"><b>정보보호 전문서비스기업</b> 등 법령이 정한 주체</td>
        </tr>
        <tr>
          <td data-l="제도">CSAP<br>(클라우드 보안인증)</td>
          <td data-l="성격">공공 조달 전제 인증</td>
          <td data-l="대상">공공기관에 클라우드 서비스를 제공하려는 사업자</td>
          <td data-l="주기">최초 인증 후 사후관리</td>
          <td data-l="주체">인증기관</td>
        </tr>
        <tr>
          <td data-l="제도">ISO/IEC 27001</td>
          <td data-l="성격">국제 표준 인증<br>(자율)</td>
          <td data-l="대상">해외 고객·파트너 요구가 있는 조직</td>
          <td data-l="주기">연 1회 사후심사, 3년 갱신</td>
          <td data-l="주체">인증기관(민간)</td>
        </tr>
      </tbody>
    </table>
    <p class="tiny" style="margin-top:16px">
      의무 대상인지 아닌지는 매출액과 이용자 수, 업종과 기관 유형을 따져 봐야 갈립니다.
      위 표는 제도의 성격을 나란히 놓고 보기 위한 것입니다. 우리 회사에 실제로 걸리는지는 원문으로 확인하셔야 합니다.
    </p>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / ISMS-P structure</span></div>
      <div class="body">
        <h2 class="d2">ISMS-P 인증기준의 구조</h2>
        <p class="lead">인증기준은 세 영역으로 나뉘고, 어느 인증을 받느냐에 따라 적용 범위가 갈립니다.
           ISMS는 앞의 두 영역까지, ISMS-P는 세 영역 전부가 대상입니다.</p>
      </div>
    </div>
    <table class="spec">
      <thead><tr><th>영역</th><th>다루는 것</th><th>ISMS</th><th>ISMS-P</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="영역">1. 관리체계 수립 및 운영</td>
          <td data-l="내용">경영진이 참여하고 조직과 자원을 붙인 뒤, 위험관리와 운영·점검·개선이 한 바퀴 도는 구조</td>
          <td data-l="ISMS">적용</td><td data-l="ISMS-P">적용</td>
        </tr>
        <tr>
          <td data-l="영역">2. 보호대책 요구사항</td>
          <td data-l="내용">정책과 인적·자산 관리부터 접근통제와 암호화, 물리·운영 보안, 사고대응과 재해복구까지 묶은 통제 항목</td>
          <td data-l="ISMS">적용</td><td data-l="ISMS-P">적용</td>
        </tr>
        <tr>
          <td data-l="영역">3. 개인정보 처리단계별 요구사항</td>
          <td data-l="내용">수집·보유에서 이용·제공을 거쳐 파기까지, 단계마다 지켜야 할 요건과 정보주체 권리보장</td>
          <td data-l="ISMS">—</td><td data-l="ISMS-P">적용</td>
        </tr>
      </tbody>
    </table>
    <div class="reg-note" style="margin-top:26px;border-left-color:var(--accent);background:var(--wash)">
      <b>준비 순서에 대한 실무 조언</b> — 세 영역 중 <b>1. 관리체계</b>가 제일 늦게 끝납니다.
      정책 문서를 쓰는 일이 아니라 <b>운영 기록이 쌓이기를 기다리는 일</b>이기 때문입니다.
      착수하자마자 문서 작업에 매달리기보다, 접근권한 검토와 변경 관리, 로그 점검을 먼저 돌려 두시길 권합니다.
      그래야 심사 시점에 내놓을 기록이 두꺼워집니다. 확인 목록은
      <a href="/resources/isms-p-readiness/" style="border-bottom:1px solid var(--rule-2)">ISMS-P 착수 전 자가점검</a>에
      따로 정리했습니다.
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Who can do what</span></div>
      <div class="body">
        <h2 class="d2">수행 자격이<br>제한된 업무</h2>
        <p class="lead">발주하려는 업무가 어떤 유형이냐에 따라 맡길 수 있는 업체가 달라집니다.
           법령이 수행 주체를 직접 정해 둔 업무가 따로 있기 때문입니다.
           발주 전에 이 구분만 확인해 두셔도 업체 선정이 한결 수월해집니다.</p>
      </div>
    </div>
    <div class="split3">
      <div class="b n">
        <span class="k">지정·인가 기관만</span>
        <p>법령이 수행 주체를 이름으로 못 박은 업무여서, 일반 컨설팅사가 수주하는 것 자체가 문제가 됩니다.</p>
        <ul>
          <li>주요정보통신기반시설 취약점 분석·평가</li>
          <li>개인정보 영향평가(PIA) 수행</li>
          <li>ISMS-P 인증 심사</li>
          <li>CSAP 인증 심사</li>
        </ul>
      </div>
      <div class="b m">
        <span class="k">발주기관 편에서 지원</span>
        <p>심사와 평가 자체는 지정 기관이 수행합니다. 컨설팅사가 맡는 부분은 그 심사를 받는 쪽의 준비입니다.
          자료를 정비하고 미비점을 미리 찾아내는 일이 여기 들어갑니다.</p>
        <ul>
          <li>인증 취득 준비 · 심사 대응</li>
          <li>영향평가 대응 자료 정비</li>
          <li>CSAP 요건 정리 · 사전 점검</li>
          <li>기반시설 점검 항목을 참고한 자체 진단</li>
        </ul>
      </div>
      <div class="b a">
        <span class="k">자격 제한 없음</span>
        <p>여기서는 자격 요건보다 수행 역량이 결과를 좌우합니다. 업체를 고르실 때는 방법론과 산출물 견본을 나란히 놓고 비교해 보시길 권합니다.</p>
        <ul>
          <li>모의해킹 · 침투테스트</li>
          <li>자체 취약점 진단</li>
          <li>클라우드 구성 진단</li>
          <li>개인정보 컴플라이언스 점검</li>
          <li>보안 정책 수립 · 교육</li>
        </ul>
      </div>
    </div>
    <p class="tiny" style="margin-top:26px">
      저희가 맡지 않는 과업은 <a href="/services/" style="border-bottom:1px solid var(--rule-2)">서비스 페이지</a>와
      <a href="/trust/" style="border-bottom:1px solid var(--rule-2)">신뢰 센터</a>에 적어 두었습니다.
    </p>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7 col-head">
      <span class="lbl">Contact</span>
      <h2 class="d2">우리가 대상인지부터<br>확인해 드립니다</h2>
      <p class="lead">매출 규모와 이용자 수, 업종, 처리하시는 개인정보 종류만 알려 주시면 됩니다.
         어떤 제도가 걸리는지 근거 조문을 붙여 답을 드립니다. 이 확인에는 비용을 청구하지 않습니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <a class="btn" href="/contact/">대상 여부 문의</a>
    </div>
  </div>
</section>"""
