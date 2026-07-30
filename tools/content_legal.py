# -*- coding: utf-8 -*-
"""법적 고지 페이지 — 개인정보처리방침 · 이용약관
   ※ 실제 수집 항목(문의 폼·채용 지원·방문 로그)과 처리 위탁(GitHub Pages / Supabase)에 맞춰 작성.
      회사 법인 정보(상호·대표자·주소·보호책임자)는 config.js COMPANY 값이 채워지면 푸터에 함께 노출된다.
"""

LEGAL_CSS = """
  .doc{max-width:860px;margin:0 auto}
  .doc h2{font-size:1.22rem;margin:38px 0 14px;color:#fff;padding-top:14px;border-top:1px solid var(--line)}
  .doc h2:first-of-type{border-top:0;padding-top:0;margin-top:0}
  .doc h3{font-size:1rem;margin:22px 0 10px;color:var(--cy-200)}
  .doc p{color:var(--fg-dim);font-size:.95rem;margin-bottom:14px}
  .doc ul,.doc ol{color:var(--fg-dim);font-size:.95rem;margin:0 0 16px 22px}
  .doc li{margin-bottom:8px}
  .doc .note{border:1px solid var(--line);border-radius:var(--r-md);padding:16px 18px;
    background:rgba(56,216,239,.05);font-size:.9rem;color:var(--fg-dim);margin-bottom:20px}
  .doc table{width:100%;border-collapse:collapse;font-size:.88rem;margin-bottom:18px;
    border:1px solid var(--line);border-radius:var(--r-md);overflow:hidden}
  .doc th{background:rgba(3,7,14,.5);color:var(--cy-300);text-align:left;padding:11px 14px;
    font-size:.78rem;letter-spacing:.6px;border-bottom:1px solid var(--line)}
  .doc td{padding:11px 14px;border-bottom:1px solid rgba(255,255,255,.05);color:var(--fg-dim);vertical-align:top}
  .doc tr:last-child td{border-bottom:0}
  .doc .rev{font-size:.82rem;color:var(--muted);margin-top:36px;padding-top:18px;border-top:1px solid var(--line)}
  @media (max-width:640px){.doc table,.doc thead,.doc tbody,.doc th,.doc td,.doc tr{display:block}
    .doc th{display:none}.doc td{border-bottom:0;padding:4px 14px}
    .doc tr{border-bottom:1px solid var(--line);padding:10px 0}
    .doc td::before{content:attr(data-l) " · ";color:var(--cy-400);font-weight:700}}
"""

PRIVACY_BODY = """<section class="page-head">
  <div class="wrap">
    <div class="crumb"><a href="/">홈</a> / 개인정보처리방침</div>
    <h1 class="display">개인정보처리방침</h1>
    <p>쉴더스랩은 「개인정보 보호법」에 따라 정보주체의 개인정보를 보호하고
       이와 관련한 고충을 신속히 처리하기 위하여 다음과 같이 개인정보처리방침을 수립·공개합니다.</p>
  </div>
</section>

<section class="sec tight">
  <div class="wrap doc">
    <div class="note">
      이 웹사이트는 <b>상담·견적 문의</b>, <b>채용 지원</b>, <b>웹사이트 운영 로그</b> 목적으로만 개인정보를 처리합니다.
      마케팅·광고 목적의 활용, 제3자 판매, 자동화된 프로파일링은 수행하지 않습니다.
    </div>

    <h2>1. 처리하는 개인정보 항목 및 목적</h2>
    <table>
      <thead><tr><th>구분</th><th>수집 항목</th><th>처리 목적</th><th>보유·이용 기간</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="구분">상담 · 견적 문의</td>
          <td data-l="항목">회사명, 담당자 성명, 이메일, (선택) 연락처, 문의 유형, 문의 내용<br>
              <span style="color:var(--muted)">(자동 수집) 접속 IP 주소, 브라우저 정보(User-Agent)</span></td>
          <td data-l="목적">문의 접수·확인, 상담 및 견적 회신, 과업 범위 협의<br>
              <span style="color:var(--muted)">자동 수집 항목은 중복·스팸 접수 방지 목적으로만 이용</span></td>
          <td data-l="기간">문의 처리 완료 후 1년 (이후 지체 없이 파기)</td>
        </tr>
        <tr>
          <td data-l="구분">채용 지원</td>
          <td data-l="항목">성명, 이메일, (선택) 연락처, 지원 직무, 경력 요약, (선택) 포트폴리오·이력서 링크<br>
              <span style="color:var(--muted)">(자동 수집) 접속 IP 주소, 브라우저 정보(User-Agent)</span></td>
          <td data-l="목적">채용 전형 진행, 전형 결과 안내<br>
              <span style="color:var(--muted)">자동 수집 항목은 중복·스팸 접수 방지 목적으로만 이용</span></td>
          <td data-l="기간">해당 채용 전형 종료 후 6개월<br>(진행 중인 전형이 없는 상시 지원은 접수일로부터 6개월)<br>동의 철회 시 즉시 파기</td>
        </tr>
        <tr>
          <td data-l="구분">웹사이트 운영 로그</td>
          <td data-l="항목">접속 IP 주소, 접속 일시, 요청 경로, 브라우저 정보(User-Agent), 연결 경로(Referer)</td>
          <td data-l="목적">서비스 운영 통계, 오류·비정상 접근 확인 등 보안 관리</td>
          <td data-l="기간">90일 (자동 삭제)</td>
        </tr>
        <tr>
          <td data-l="구분">문의·지원 접수 기록<br>(감사 로그)</td>
          <td data-l="항목">접속 IP 주소, 브라우저 정보(User-Agent), 접수 시각, 접수 구분(문의 유형·지원 직무)</td>
          <td data-l="목적">중복·부정 접수 확인 및 침해사고 대응</td>
          <td data-l="기간">1년 (자동 삭제)</td>
        </tr>
        <tr>
          <td data-l="구분">관리자 접속 기록</td>
          <td data-l="항목">관리자 계정 이메일, 접속 일시, IP 주소, 수행 작업 내역</td>
          <td data-l="목적">관리자 행위에 대한 감사 및 사고 대응</td>
          <td data-l="기간">1년 (자동 삭제)</td>
        </tr>
      </tbody>
    </table>
    <p>문의·지원 과정에서 개인정보를 수집할 때에는 수집 항목, 목적, 보유 기간을 안내하고
       정보주체의 <b>동의를 받은 후</b>에 처리합니다. 필수 항목 외 선택 항목은 기재하지 않아도 서비스 이용에 제한이 없습니다.</p>
    <p>서비스 수행(컨설팅 과업) 과정에서 고객사로부터 제공받는 자료의 처리는 개별 계약과
       비밀유지계약(NDA)에 따르며, 이 방침은 본 웹사이트를 통한 처리에 적용됩니다.</p>

    <h2>2. 개인정보의 제3자 제공</h2>
    <p>쉴더스랩은 정보주체의 개인정보를 제3자에게 제공하지 않습니다.
       다만 법령에 특별한 규정이 있거나 수사기관이 법령에 정해진 절차와 방법에 따라 요구하는 경우에는 예외로 합니다.</p>

    <h2>3. 개인정보 처리업무의 위탁 및 국외 이전</h2>
    <p>서비스 운영을 위해 아래와 같이 처리업무를 위탁하고 있으며, 해당 업무 수행을 위해 개인정보가 국외로 이전됩니다.</p>
    <table>
      <thead><tr><th>수탁자 · 연락처</th><th>위탁 업무</th><th>이전 항목</th><th>이전 국가</th><th>이전 시기 · 방법</th><th>보유기간</th></tr></thead>
      <tbody>
        <tr>
          <td data-l="수탁자">GitHub, Inc.<br><span style="color:var(--muted)">support.github.com/contact/privacy</span></td>
          <td data-l="업무">웹사이트 호스팅(GitHub Pages) 및 전송 구간 운영</td>
          <td data-l="항목">접속 IP, 접속 일시, 요청 정보</td>
          <td data-l="국가">미국</td>
          <td data-l="시기·방법">이용자의 사이트 접속 시점에 정보통신망을 통해 수시 이전(HTTPS 전송)</td>
          <td data-l="기간">위탁 계약 종료 시까지</td>
        </tr>
        <tr>
          <td data-l="수탁자">Supabase, Inc.<br><span style="color:var(--muted)">privacy@supabase.io</span></td>
          <td data-l="업무">데이터베이스·인증 서비스 호스팅(문의·지원·로그 저장)</td>
          <td data-l="항목">위 1항의 수집 항목</td>
          <td data-l="국가">미국</td>
          <td data-l="시기·방법">문의·지원 접수 및 방문 로깅 시점에 정보통신망을 통해 수시 이전(HTTPS 전송)</td>
          <td data-l="기간">위탁 계약 종료 시까지</td>
        </tr>
        <tr>
          <td data-l="수탁자">Google LLC<br><span style="color:var(--muted)">policies.google.com/privacy</span></td>
          <td data-l="업무">웹폰트(Google Fonts) 제공</td>
          <td data-l="항목">접속 IP, 브라우저 정보(User-Agent)</td>
          <td data-l="국가">미국</td>
          <td data-l="시기·방법">페이지 로딩 시 브라우저가 폰트를 내려받는 시점에 이전(HTTPS 전송)</td>
          <td data-l="기간">Google 정책에 따름</td>
        </tr>
      </tbody>
    </table>
    <p>정보주체는 국외 이전을 거부할 수 있습니다. 다만 이 경우 웹사이트를 통한 문의·지원 접수가 제한되며,
       이메일(contact@shilderslab.com)로 문의하실 수 있습니다.</p>

    <h2>4. 개인정보의 파기 절차 및 방법</h2>
    <ul>
      <li>보유 기간이 경과하거나 처리 목적이 달성된 개인정보는 지체 없이 파기합니다.</li>
      <li>전자적 파일 형태의 정보는 복구·재생이 불가능한 방법으로 영구 삭제하며, 출력물은 파쇄 또는 소각합니다.</li>
      <li>웹사이트 운영 로그 및 관리자 접속 기록은 보유 기간이 지난 시점에 자동 삭제 절차로 파기됩니다.</li>
    </ul>

    <h2>5. 정보주체의 권리와 행사 방법</h2>
    <p>정보주체는 언제든지 다음 권리를 행사할 수 있습니다.</p>
    <ol>
      <li>개인정보 열람 요구</li>
      <li>오류 등이 있을 경우 정정 요구</li>
      <li>삭제 요구</li>
      <li>처리 정지 요구</li>
      <li>동의 철회</li>
    </ol>
    <p>권리 행사는 <a href="mailto:contact@shilderslab.com" style="color:var(--cy-300)">contact@shilderslab.com</a>
       으로 서면·전자우편 등을 통해 요청하실 수 있으며, 쉴더스랩은 지체 없이 조치합니다.
       정보주체의 열람·정정·삭제 요구는 법령에서 정한 사유가 없는 한 제한하지 않습니다.</p>

    <h2>6. 개인정보의 안전성 확보 조치</h2>
    <ul>
      <li><b>접근 권한 관리</b> — 관리자 화면은 사전 등록된 계정만 접근할 수 있도록 화이트리스트로 통제하며,
          권한 없는 계정의 조회·수정을 데이터베이스 수준(행 단위 보안 정책)에서 차단합니다.</li>
      <li><b>전송 구간 암호화</b> — 웹사이트 전 구간에 HTTPS(TLS)를 적용합니다.</li>
      <li><b>접속 기록 보관·점검</b> — 관리자 행위 기록을 별도 저장하고, 임의 수정·삭제가 불가능한 경로로만 적재합니다.</li>
      <li><b>최소 수집</b> — 목적 달성에 필요한 최소한의 항목만 수집하며, 주민등록번호 등 고유식별정보와
          민감정보는 수집하지 않습니다.</li>
      <li><b>보관 기간 자동 관리</b> — 로그성 정보는 보유 기간 경과 시 자동 삭제됩니다.</li>
    </ul>

    <h2>7. 쿠키 등 자동 수집 장치의 운영</h2>
    <p>본 웹사이트는 광고·행태정보 수집 목적의 쿠키나 제3자 추적 스크립트를 사용하지 않습니다.
       관리자 로그인 상태 유지를 위해 브라우저의 로컬 저장소(localStorage)에 인증 토큰을 저장하며,
       이는 로그아웃 시 삭제됩니다.</p>

    <h2>8. 개인정보 보호책임자 및 문의처</h2>
    <p>개인정보 처리에 관한 문의, 불만처리, 피해구제 등에 관한 사항은 아래로 연락해 주시기 바랍니다.</p>
    <ul>
      <li>이메일: <a href="mailto:contact@shilderslab.com" style="color:var(--cy-300)">contact@shilderslab.com</a></li>
      <li>개인정보 보호책임자: 문의·열람 청구는 위 이메일로 접수하며, 접수 즉시 담당자가 처리합니다.
          (보호책임자 성명·직책은 조직 확정 후 본 항목에 게시합니다.)</li>
      <li>상호 및 대표자, 사업장 주소는 사업자 등록 정보 확정 후 본 페이지 하단(사업자 정보)에 게시합니다.</li>
    </ul>
    <p>개인정보 침해에 대한 신고·상담이 필요한 경우 아래 기관에 문의할 수 있습니다.</p>
    <ul>
      <li>개인정보침해 신고센터 (한국인터넷진흥원) — 국번 없이 118</li>
      <li>개인정보 분쟁조정위원회 — 1833-6972</li>
      <li>대검찰청 사이버수사과 — 1301 / 경찰청 사이버범죄 신고시스템 — 182</li>
    </ul>

    <h2>9. 방침의 변경</h2>
    <p>이 개인정보처리방침의 내용 추가·삭제 및 수정이 있을 경우 시행 7일 전부터 웹사이트를 통해 공지합니다.
       다만 정보주체 권리의 중요한 변경이 있을 경우에는 최소 30일 전에 공지합니다.</p>

    <div class="rev">
      시행일: 2026년 7월 30일 (최초 제정)<br>
      본 방침은 쉴더스랩 웹사이트(shilderslab.com)를 통한 개인정보 처리에 적용됩니다.
    </div>
  </div>
</section>"""

TERMS_BODY = """<section class="page-head">
  <div class="wrap">
    <div class="crumb"><a href="/">홈</a> / 이용약관</div>
    <h1 class="display">이용약관</h1>
    <p>본 약관은 쉴더스랩이 운영하는 웹사이트(shilderslab.com, 이하 “본 사이트”)의 이용 조건과 절차에 관한 사항을 정합니다.</p>
  </div>
</section>

<section class="sec tight">
  <div class="wrap doc">
    <h2>제1조 (목적 및 적용)</h2>
    <p>본 약관은 본 사이트가 제공하는 정보 및 문의·지원 접수 기능(이하 “서비스”)의 이용에 관하여
       쉴더스랩(이하 “회사”)과 이용자 간의 권리·의무 및 책임 사항을 규정함을 목적으로 합니다.
       컨설팅 용역의 수행 조건은 별도의 개별 계약에 따르며, 본 약관과 개별 계약이 상충하는 경우 개별 계약이 우선합니다.</p>

    <h2>제2조 (서비스의 내용)</h2>
    <ul>
      <li>회사 및 서비스 소개 정보의 제공</li>
      <li>보안 인사이트·공지 등 콘텐츠의 제공</li>
      <li>상담·견적 문의 및 채용 지원의 온라인 접수</li>
    </ul>

    <h2>제3조 (이용자의 의무)</h2>
    <p>이용자는 다음 행위를 하여서는 안 됩니다.</p>
    <ol>
      <li>타인의 정보를 도용하거나 허위 정보를 입력하는 행위</li>
      <li>본 사이트 또는 연결된 시스템에 대한 <b>사전 서면 승인 없는 취약점 점검, 침투 시도, 자동화된 대량 요청</b>,
          그 밖에 정상적인 운영을 방해하는 행위</li>
      <li>본 사이트의 콘텐츠를 무단으로 복제·배포·전송하거나 상업적으로 이용하는 행위</li>
      <li>악성코드 유포, 접근 권한 우회, 관리자 기능에 대한 무단 접근 시도</li>
      <li>법령 또는 공서양속에 위반되는 행위</li>
    </ol>
    <div class="note">
      보안 취약점을 발견하신 경우 악용하지 마시고
      <a href="mailto:contact@shilderslab.com" style="color:var(--cy-300)">contact@shilderslab.com</a>
      으로 알려주시기 바랍니다. 신고 내용은 비공개로 검토하며, 선의의 신고자에게 법적 조치를 취하지 않습니다.
    </div>

    <h2>제4조 (지식재산권)</h2>
    <p>본 사이트에 게시된 텍스트·이미지·문서 양식·로고 등 콘텐츠에 대한 지식재산권은 쉴더스랩에 귀속됩니다.
       이용자는 쉴더스랩의 사전 승인 없이 이를 복제·수정·배포·전송하거나 제3자에게 이용하게 할 수 없습니다.</p>
    <p>단, 브랜드 리소스 페이지에서 제공하는 로고 파일은 쉴더스랩을 <b>정확하게 지칭·표기하는 목적</b>에 한하여
       원형 그대로 사용할 수 있으며, 변형 및 후원·제휴 관계를 오인시킬 수 있는 사용은 금지됩니다.</p>

    <h2>제5조 (문의 및 지원 접수의 처리)</h2>
    <ul>
      <li>문의 접수는 계약의 청약이나 승낙을 구성하지 않으며, 용역의 성립은 별도 계약 체결로만 이루어집니다.</li>
      <li>제출된 문의·지원 정보는 개인정보처리방침에 정한 목적과 기간 내에서만 처리됩니다.</li>
      <li>회사는 스팸·자동화된 반복 제출로 판단되는 접수를 처리하지 않거나 차단할 수 있습니다.</li>
    </ul>

    <h2>제6조 (콘텐츠의 성격 및 면책)</h2>
    <p>본 사이트의 보안 인사이트 등 콘텐츠는 일반적인 정보 제공을 목적으로 하며,
       특정 조직의 상황에 대한 법률 자문이나 개별 보안 조치의 보증으로 해석될 수 없습니다.
       회사는 콘텐츠의 정확성을 위해 노력하지만, 이용자가 콘텐츠에 근거해 취한 조치의 결과에 대해서는 책임을 지지 않습니다.
       다만 회사의 고의 또는 중대한 과실이 있는 경우에는 그러하지 아니합니다.</p>
    <p>회사는 천재지변, 정전, 호스팅·통신 사업자의 장애 등 통제 불가능한 사유로 인한 서비스 중단에 대하여
       책임을 지지 않습니다. 다만 회사의 고의 또는 중대한 과실이 있는 경우에는 그러하지 아니합니다.</p>

    <h2>제7조 (서비스의 변경 및 중단)</h2>
    <p>회사는 운영상·기술상 필요에 따라 서비스의 내용을 변경하거나 중단할 수 있으며,
       중요한 변경 사항은 본 사이트를 통해 공지합니다.</p>

    <h2>제8조 (약관의 변경)</h2>
    <p>회사는 필요한 경우 본 약관을 변경할 수 있으며, 변경된 약관은 시행 7일 전(이용자에게 불리한 변경은 30일 전)부터
       본 사이트에 공지한 후 효력이 발생합니다.
       이용자가 변경된 약관에 동의하지 않는 경우 서비스 이용을 중단할 수 있습니다.</p>

    <h2>제9조 (준거법 및 관할)</h2>
    <p>본 약관은 대한민국 법령에 따라 해석됩니다. 서비스 이용과 관련하여 회사와 이용자 간에 분쟁이 발생한 경우,
       소는 민사소송법이 정한 관할 법원에 제기합니다.</p>

    <div class="rev">시행일: 2026년 7월 30일 (최초 제정)</div>
  </div>
</section>"""
