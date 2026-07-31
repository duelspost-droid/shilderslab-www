# -*- coding: utf-8 -*-
"""신뢰 센터 · 규제 가이드
   리서치 결과 반영:
     · 신생 보안 컨설팅사에 대한 실제 의심은 "우리 데이터가 어떻게 되나"이다. 여기에 직접 답한다.
     · 자사 사이트를 자기 체크리스트로 점검하고 **잔여위험까지 공개**한다(첫 고객은 자기 자신).
     · 규제 정보는 기준일과 출처를 함께 밝힌다. 정확도 자체가 상품이다.
"""

# ══════════════════════════════════════════════════════════════════════
# 신뢰 센터
# ══════════════════════════════════════════════════════════════════════
TRUST_TITLE = "신뢰 센터 | 쉴더스랩 — 데이터 취급 · 계약 조건 · 자사 보안"
TRUST_DESC = ("진단 데이터를 어떻게 취급하는지, 계약 조건은 무엇인지, 자사 웹사이트의 보안 조치와 "
              "남은 위험은 무엇인지 공개합니다. 취약점 제보 창구도 여기에 있습니다.")

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
    <h1 class="d1">우리에게 맡긴 것이<br>어떻게 다뤄지는지</h1>
    <p class="lead">진단을 맡기시면 구성도와 계정 체계, 취약점 목록이 쉴더스랩 쪽에 남습니다.
       그 자료를 어디에 얼마나 두고 어떻게 없애는지 이 페이지에 적어 두었습니다.
       계약 전에 확인하셔도 됩니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Data handling</span></div>
      <div class="body">
        <h2 class="d2">진단 데이터 취급</h2>
        <p class="lead">과업 중 확보되는 자료(구성 정보, 로그, 발견 사항, 화면 캡처)는 아래 원칙으로 취급합니다.
           계약서에 동일한 내용을 넣습니다.</p>
      </div>
    </div>
    <div class="trust-kv">
      <div class="row"><div class="k">수집 범위</div>
        <div class="v">과업 수행에 필요한 최소 범위로 제한합니다. <b>실데이터(고객사의 실제 개인정보)는
          원칙적으로 열람하지 않으며</b>, 확인이 불가피한 경우 사전 합의 후 최소 건수만 확인하고 추출·복제하지 않습니다.</div></div>
      <div class="row"><div class="k">보관</div>
        <div class="v">과업별로 분리된 저장소에 보관하며, 해당 과업 수행 인력만 접근합니다.
          개인 단말의 임의 위치에 사본을 두지 않습니다.</div></div>
      <div class="row"><div class="k">전달</div>
        <div class="v">산출물은 착수 시 합의한 경로로만 전달합니다. 이메일 첨부가 부적절한 자료는
          별도 경로를 사용하며, 고객사 지정 경로가 있으면 그쪽을 따릅니다.</div></div>
      <div class="row"><div class="k">보존 기간</div>
        <div class="v">기본값은 <b>과업 종료 후 3개월</b>입니다(재점검·질의 대응 목적).
          계약으로 더 짧게 정할 수 있으며, 종료 즉시 파기를 요청하실 수도 있습니다.</div></div>
      <div class="row"><div class="k">파기</div>
        <div class="v">보존 기간 종료 시 복구 불가능한 방법으로 삭제하고 <b>파기 확인서</b>를 제공합니다.
          출력물이 있었다면 파쇄 사실을 함께 기재합니다.</div></div>
      <div class="row"><div class="k">인력 통제</div>
        <div class="v">과업에 참여하는 사람은 착수 전에 개별 비밀유지 서약서에 서명합니다.
          누가 어떤 자산에 접근했는지 기록을 남기고, 참여자가 바뀌면 사전에 알립니다.
          요청하시면 <b>참여자 명단과 역할</b>을 계약 단계에서 서면으로 드립니다.</div></div>
      <div class="row"><div class="k">2차 이용</div>
        <div class="v">고객사 자료를 마케팅·홍보·사례 발표에 사용하지 않습니다.
          익명화하더라도 <b>사전 서면 동의 없이는 인용하지 않습니다.</b></div></div>
    </div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / Contract</span></div>
      <div class="body">
        <h2 class="d2">계약 조건 · 보유 지위</h2>
        <p class="lead">가지고 있는 것과 없는 것을 같은 표에 적습니다. 없는 것은 없다고 씁니다.</p>
      </div>
    </div>
    <div class="trust-kv">
      <div class="row"><div class="k">비밀유지계약</div>
        <div class="v"><span class="state yes">제공</span>착수 전 체결합니다. 고객사 양식이 있으면 그것을 우선 검토합니다.
          표준 양식이 필요하시면 요청 시 사전 제공합니다.</div></div>
      <div class="row"><div class="k">재하도급</div>
        <div class="v"><span class="state no">없음</span>과업을 제3자에게 재하도급하지 않습니다.
          외부 전문가 참여가 필요한 경우 사전에 알리고 동의를 받습니다.</div></div>
      <div class="row"><div class="k">정보보호 전문서비스기업 지정</div>
        <div class="v"><span class="state plan">미보유</span>「정보보호산업의 진흥에 관한 법률」에 따른 지정 사업자가 아닙니다.
          해당 지정이 요구되는 과업(주요정보통신기반시설 취약점 분석·평가 등)은 수주하지 않습니다.
          지정 요건(기술인력·자본·설비·심사)을 충족하는 시점에 이 항목을 갱신합니다.</div></div>
      <div class="row"><div class="k">개인정보 영향평가 기관</div>
        <div class="v"><span class="state no">미해당</span>지정 평가기관이 아닙니다. 영향평가 <b>대응 준비</b>만 지원합니다.</div></div>
      <div class="row"><div class="k">배상책임보험</div>
        <div class="v"><span class="state plan">확인 필요</span>가입 여부와 한도는 계약 단계에서 서면으로 확인해 드립니다.
          이 항목은 확정되는 대로 이 페이지에 수치와 함께 게시합니다.</div></div>
      <div class="row"><div class="k">법인 신원</div>
        <div class="v">상호 · 대표자 · 사업자등록번호 · 주소 · 개인정보 보호책임자는
          사업자 등록 정보 확정 후 이 페이지와 전 페이지 하단에 게시합니다.
          그때까지는 계약 단계에서 서면으로 제공합니다.</div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Our own site</span></div>
      <div class="body">
        <h2 class="d2">첫 고객은<br>우리 자신입니다</h2>
        <p class="lead">이 사이트에 무엇을 적용했고 무엇이 <b>남아 있는지</b> 항목으로 적습니다.
           고객사 보고서에 쓰는 것과 같은 형식이라, 저희 보고서가 어떻게 생겼는지 미리 보실 수 있습니다.</p>
      </div>
    </div>
    <div class="g12">
      <div class="c6">
        <h3 class="d3" style="font-size:1rem;margin-bottom:16px">적용한 조치</h3>
        <ul class="ticks">
          <li><span><b>전 구간 HTTPS</b> — 인증서 적용 및 HTTP 접속 강제 리다이렉트.</span></li>
          <li><span><b>콘텐츠 보안 정책(CSP)</b> — 외부 스크립트 0개. 백엔드 클라이언트를 자체 호스팅해
            스크립트 출처를 자기 도메인으로 제한.</span></li>
          <li><span><b>개인정보 테이블 직접 접근 차단</b> — 문의·지원 데이터는 공개 조회 정책 자체를 만들지 않고,
            서버측 검증 함수로만 적재합니다. 익명 키로는 읽을 수 없습니다.</span></li>
          <li><span><b>제출 남용 방어</b> — 서버측 입력 검증, 요청 빈도 제한(2계층), 폼 허니팟.</span></li>
          <li><span><b>보관 기간 자동 삭제</b> — 방문 로그·문의·지원 데이터에 보존 기간을 걸고
            스케줄러가 자동 파기합니다.</span></li>
          <li><span><b>관리자 접근 통제</b> — 사전 등록된 계정만 허용(화이트리스트), 모든 관리자 행위를 감사 로그로 기록.</span></li>
        </ul>
      </div>
      <div class="c5 start8">
        <h3 class="d3" style="font-size:1rem;margin-bottom:16px">남아 있는 위험</h3>
        <ul class="ticks">
          <li><span><b>인라인 스크립트 허용</b> — 정적 사이트 구조상 CSP에서 인라인 스크립트를 허용하고 있습니다.
            출력값은 전부 이스케이프하고 CMS 본문은 HTML을 렌더하지 않지만, 이 항목은 완화가 아니라
            <b>수용</b>으로 분류합니다.</span></li>
          <li><span><b>외부 웹폰트</b> — 서체를 외부에서 불러오므로 방문자 IP가 해당 사업자에 전달됩니다.
            처리방침 위탁 항목에 기재했으며, 자체 호스팅으로 전환을 검토 중입니다.</span></li>
          <li><span><b>법인 정보 미게시</b> — 사업자 등록 정보 확정 전이라 하단 사업자 정보가 비어 있습니다.</span></li>
        </ul>
        <p class="tiny" style="margin-top:20px">
          2026년 7월 점검 기준입니다. 항목이 해소되면 해소일과 함께 이력에 남기고, 분기마다 다시 점검해 이 날짜를 갱신합니다.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="sec band-3">
  <div class="shell g12">
    <div class="c5">
      <span class="lbl">04 / Vulnerability disclosure</span>
      <h2 class="d2" style="margin:20px 0 22px">취약점을<br>발견하셨다면</h2>
      <p class="lead">이 사이트나 저희가 운영하는 자산에서 문제를 찾으셨다면 알려주세요.
         선의의 제보자에게 법적 조치를 취하지 않습니다.</p>
    </div>
    <div class="c6 start7">
      <div class="trust-kv">
        <div class="row"><div class="k">접수</div>
          <div class="v"><a href="mailto:contact@shilderslab.com" style="border-bottom:1px solid var(--rule-2)">contact@shilderslab.com</a>
            — 제목에 <b>[제보]</b>를 붙여 주시면 우선 확인합니다.</div></div>
        <div class="row"><div class="k">회신</div>
          <div class="v">영업일 기준 <b>3일 내</b> 접수 확인, <b>14일 내</b> 검토 결과 회신을 목표로 합니다.</div></div>
        <div class="row"><div class="k">범위</div>
          <div class="v">shilderslab.com 및 하위 경로. 서비스 거부(DoS), 물리적 침입, 사회공학,
            제3자 서비스에 대한 시험은 제외합니다.</div></div>
        <div class="row"><div class="k">원칙</div>
          <div class="v">확인에 필요한 최소 범위에서만 검증해 주시고, 타인의 데이터에 접근하거나
            서비스를 훼손하지 말아 주세요. 조치 완료 전 공개는 자제해 주시면 감사하겠습니다.</div></div>
        <div class="row"><div class="k">사례</div>
          <div class="v">현재 금전적 포상 제도는 운영하지 않습니다. 원하시면 조치 후 공개 감사 표기를 드립니다.</div></div>
        <div class="row"><div class="k">기계 판독</div>
          <div class="v"><a href="/.well-known/security.txt" style="border-bottom:1px solid var(--rule-2)">/.well-known/security.txt</a></div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">더 확인하고 싶은<br>조건이 있으면 말씀해 주세요</h2>
      <p class="lead">계약 조건, 데이터 취급, 인력 구성 중 확인이 필요한 항목이 있으면 계약 전에 서면으로 답변드립니다.</p>
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
REG_DESC = ("ISMS/ISMS-P, 개인정보보호법 안전성 확보조치, CSAP, ISO 27001 등 국내 정보보호 제도를 "
            "근거 법령·대상·주기 기준으로 비교하고, 수행 자격이 제한된 업무를 구분해 정리했습니다.")

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
    <h1 class="d1">무엇이 우리에게<br>해당되는가</h1>
    <p class="lead">제도가 많다 보니 “우리가 뭘 해야 하는지”부터 막힙니다.
       국내 정보보호 제도를 근거 법령·대상·주기 기준으로 정리했습니다.
       수치와 해석은 반드시 원문으로 최종 확인하시고, 판단이 어려우면 문의해 주세요.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="reg-note">
      <b>기준일 안내</b> — 이 페이지는 2026년 7월 기준으로 정리했습니다.
      고시·시행령은 개정될 수 있으므로 실제 대응 시에는 소관 기관의 최신 원문을 확인하셔야 합니다.
      확인이 필요한 항목은 <a href="/contact/" style="border-bottom:1px solid var(--rule-2)">문의</a>주시면
      근거 조문과 함께 회신드립니다.
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
      의무 대상 여부는 매출액·이용자 수·업종·기관 유형 등 세부 기준으로 판단합니다.
      위 표는 제도의 성격을 비교하기 위한 것이며, 개별 적용 여부는 원문 확인이 필요합니다.
    </p>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / ISMS-P structure</span></div>
      <div class="body">
        <h2 class="d2">ISMS-P 인증기준의 구조</h2>
        <p class="lead">세 영역으로 나뉘며, 인증 유형에 따라 적용 범위가 달라집니다.
           ISMS는 앞의 두 영역, ISMS-P는 세 영역 전부가 대상입니다.</p>
      </div>
    </div>
    <table class="spec">
      <thead><tr><th>영역</th><th>다루는 것</th><th>ISMS</th><th>ISMS-P</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="영역">1. 관리체계 수립 및 운영</td>
          <td data-l="내용">경영진 참여, 조직·자원, 위험관리, 운영·점검·개선의 순환 구조</td>
          <td data-l="ISMS">적용</td><td data-l="ISMS-P">적용</td>
        </tr>
        <tr>
          <td data-l="영역">2. 보호대책 요구사항</td>
          <td data-l="내용">정책·인적·자산·접근통제·암호화·물리·운영·사고대응·재해복구 등 통제 항목</td>
          <td data-l="ISMS">적용</td><td data-l="ISMS-P">적용</td>
        </tr>
        <tr>
          <td data-l="영역">3. 개인정보 처리단계별 요구사항</td>
          <td data-l="내용">수집·보유, 이용·제공, 파기, 정보주체 권리보장까지 처리 단계별 요건</td>
          <td data-l="ISMS">—</td><td data-l="ISMS-P">적용</td>
        </tr>
      </tbody>
    </table>
    <div class="reg-note" style="margin-top:26px;border-left-color:var(--accent);background:var(--wash)">
      <b>준비 순서에 대한 실무 조언</b> — 세 영역 중 <b>1. 관리체계</b>가 가장 늦게 완성됩니다.
      정책을 쓰는 일이 아니라 <b>운영 기록이 쌓이는 일</b>이기 때문입니다.
      그래서 준비를 시작할 때 문서 작업보다 접근권한 검토·변경 관리·로그 점검 같은 활동을 먼저 돌리는 편이
      전체 일정을 줄입니다. 자세한 확인 목록은
      <a href="/resources/isms-p-readiness/" style="border-bottom:1px solid var(--rule-2)">ISMS-P 착수 전 자가점검</a>에
      정리해 두었습니다.
    </div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">03 / Who can do what</span></div>
      <div class="body">
        <h2 class="d2">수행 자격이<br>제한된 업무</h2>
        <p class="lead">모든 보안 업무를 아무 업체나 할 수 있는 것은 아닙니다.
           발주 전에 이 구분을 알고 계시면 잘못된 업체 선정을 피할 수 있습니다.</p>
      </div>
    </div>
    <div class="split3">
      <div class="b n">
        <span class="k">지정·인가 기관만</span>
        <p>법령이 수행 주체를 특정한 업무입니다. 일반 컨설팅사가 수주하면 그 자체가 문제가 됩니다.</p>
        <ul>
          <li>주요정보통신기반시설 취약점 분석·평가</li>
          <li>개인정보 영향평가(PIA) 수행</li>
          <li>ISMS-P 인증 심사</li>
          <li>CSAP 인증 심사</li>
        </ul>
      </div>
      <div class="b m">
        <span class="k">발주기관 편에서 지원</span>
        <p>심사·평가 자체는 못 하지만, 받는 쪽을 준비시키는 일은 컨설팅사가 합니다.</p>
        <ul>
          <li>인증 취득 준비 · 심사 대응</li>
          <li>영향평가 대응 자료 정비</li>
          <li>CSAP 요건 정리 · 사전 점검</li>
          <li>기반시설 점검 항목을 참고한 자체 진단</li>
        </ul>
      </div>
      <div class="b a">
        <span class="k">자격 제한 없음</span>
        <p>역량으로 경쟁하는 영역입니다. 업체 선정 시 방법론과 산출물을 비교하세요.</p>
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
      쉴더스랩이 수행하지 않는 과업은 <a href="/services/" style="border-bottom:1px solid var(--rule-2)">서비스 페이지</a>와
      <a href="/trust/" style="border-bottom:1px solid var(--rule-2)">신뢰 센터</a>에 명시했습니다.
    </p>
  </div>
</section>

<section class="sec band-dark cta">
  <div class="shell g12">
    <div class="c7">
      <span class="lbl">Contact</span>
      <h2 class="d2" style="margin:18px 0 18px">우리가 대상인지부터<br>확인해 드립니다</h2>
      <p class="lead">사업 현황(매출 규모, 이용자 수, 업종, 처리하는 개인정보)을 알려주시면
         해당 제도와 근거 조문을 정리해 회신드립니다. 이 확인에는 비용이 발생하지 않습니다.</p>
    </div>
    <div class="c4 start9" style="display:flex;align-items:flex-end">
      <a class="btn" href="/contact/">대상 여부 문의</a>
    </div>
  </div>
</section>"""
