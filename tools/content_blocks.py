# -*- coding: utf-8 -*-
"""관리자 콘솔에서 편집하는 콘텐츠 블록의 **정본 정의**.

이 표 하나가 세 곳을 먹인다 — 정의가 갈라지지 않게 하기 위함이다.
  · 빌드    `build-pages.py` : DB 값이 있으면 그 값을, 비어 있으면 여기 default 를 구워 넣는다
  · 시드    `gen-content-seed.py` : 이 표에서 `0005_shilderslab_content.sql` 을 생성한다
  · 관리자  `admin/` : section·label·hint 로 편집 화면을 그린다(값은 DB 에서 읽는다)

kind
  text : 평문. 이스케이프한 뒤 줄바꿈을 <br> 로 바꾼다. `<h1>` `<p>` `<span>` 안에 쓴다.
  rich : 최소 마크다운(**굵게**, - 목록, 1. 목록, > 인용, [링크](/경로), `코드`).
         `<p>` 를 만들어 내므로 **`<div>` 안에만** 쓴다. `<p data-content>` 에 rich 를 쓰면
         `<p>` 안에 `<p>` 가 생겨 마크업이 깨진다.

HTML 쪽 규칙 — `data-content="키"` 를 단 요소의 **안쪽 전체**가 교체 대상이다.
같은 태그를 안에 중첩하면 치환이 잘린다(예: `<div data-content>` 안의 `<div>`). 넣지 말 것.
"""

BLOCKS = [
    # ─────────────────────────── 홈 ───────────────────────────
    # 기본값은 tools/align-blocks.py 가 페이지 HTML 리터럴에서 채운다. 손으로 적지 않는다.
    dict(key="home.hero_title", kind="text", section="홈", label="상단 큰 제목",
         hint="사이트에서 가장 먼저 읽히는 문장입니다. 줄바꿈이 그대로 반영됩니다.", default="조치가 끝났는지\n다시 확인하고 닫습니다"),
    dict(key="home.hero_lead", kind="text", section="홈", label="상단 소개 문단",
         hint="제목 아래 한 문단. 검색 결과 미리보기에도 영향을 줍니다.", default="ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 맡습니다. 취약하다고 적은 항목에는 어떻게 재현했는지를 덧붙이고, 조치가 끝나면 한 번 더 들어가 닫혔는지 확인합니다."),
    dict(key="home.services_title", kind="text", section="홈", label="01 서비스 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="규제와 공격,\n양쪽에서 봅니다"),
    dict(key="home.services_lead", kind="text", section="홈", label="01 서비스 — 소개 문단",
         hint="", default="인증 심사 대응과 기술 진단을 서로 다른 업체에 나눠 맡기면 어떻게 될까요? 같은 자산을 두 번 조사하고도, 심사에서 지적된 결함과 실제 침해 경로는 끝내 어긋난 채 남습니다. 그 둘을 맞춰 보는 일이 결국 담당자 몫이 되기 때문에, 저희는 두 영역을 하나의 범위 정의서 안에서 설계합니다."),
    dict(key="home.method_title", kind="text", section="홈", label="02 방법론 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="모든 과업은\n같은 다섯 단계를 거칩니다"),
    dict(key="home.method_lead", kind="text", section="홈", label="02 방법론 — 소개 문단",
         hint="‘다섯 단계’ 라는 서술은 /method/ 의 실제 단계 수와 맞아야 합니다.", default="단계마다 나가는 산출물은 계약서에 문서명 단위로 적힙니다. 마지막 재점검이 끝나기 전에는 종료로 처리하지 않습니다."),
    dict(key="home.why_title", kind="text", section="홈", label="03 판단 기준 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="판단 기준을\n먼저 공개합니다"),
    dict(key="home.why_lead", kind="text", section="홈", label="03 판단 기준 — 소개 문단",
         hint="", default="제안서를 나란히 놓고 보면 문장은 다들 비슷한데, 정작 누가 무엇을 어떻게 하겠다는 것인지는 잘 드러나지 않습니다. 그래서 위험도 산정 기준과 산출물 목록, 맡지 않는 과업까지 계약 전에 공개합니다. 저희 제안서에만 쓰시라고 올린 자료는 아닙니다."),
    dict(key="home.resources_title", kind="text", section="홈", label="04 자료실 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="로그인 없이\n바로 쓰실 수 있습니다"),
    dict(key="home.resources_lead", kind="text", section="홈", label="04 자료실 — 소개 문단",
         hint="", default="진단 현장에 실제로 들고 나가는 체크리스트입니다. 이메일을 남기실 필요는 없습니다. 다른 업체와 진행 중이셔도 활용하시는 데 문제없습니다."),
    dict(key="home.insights_title", kind="text", section="홈", label="05 인사이트 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="현장에서 반복되는 것들"),
    dict(key="home.insights_lead", kind="text", section="홈", label="05 인사이트 — 소개 문단",
         hint="", default="같은 질문을 여러 번 받으면 글로 정리합니다. 규제 해석이 엇갈리는 대목, 조치가 번번이 멈추는 지점을 다룹니다."),
    dict(key="home.cta_title", kind="text", section="홈", label="맨 아래 상담 유도 — 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="지금 상태를\n확인하는 것부터"),
    dict(key="home.cta_lead", kind="text", section="홈", label="맨 아래 상담 유도 — 문단",
         hint="비용 청구 여부 같은 약속이 들어 있습니다. 실제 운영과 맞는지 확인하고 고치세요.",
         default="어디부터 봐야 할지 모르시겠다면 진단 대상과 목표 일정, 이 두 가지만 알려 주시면 필요한 점검 항목과 예상 기간을 정리해 보내 드립니다. 범위 검토와 견적 산정에는 비용이 붙지 않습니다."),
    # ─────────────────────────── 진단 방법론 ───────────────────────────
    dict(key="method.hero_title", kind="text", section="진단 방법론", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="계약 전에\n먼저 공개합니다"),
    dict(key="method.hero_lead", kind="text", section="진단 방법론", label="상단 소개 문단",
         hint="", default="제안서를 여러 곳에서 받아 놓고도 무엇을 기준으로 비교해야 할지 막막할 때가 있습니다. 쉴더스랩은 그래서 실제로 쓰는 5단계 절차와 위험도 산정 기준, 산출물 규격을 계약 전에 공개합니다. 감추면 비교가 안 되니까요."),
    # ─────────────────────────── 자료실 ───────────────────────────
    dict(key="resources.hero_title", kind="text", section="자료실", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="계약 없이도\n바로 쓰실 수 있게"),
    dict(key="resources.hero_lead", kind="text", section="자료실", label="상단 소개 문단",
         hint="", default="저희가 과업에서 쓰는 문서를 손질 없이 그대로 올렸으니, 로그인이나 이메일 주소를 남기실 필요 없이 바로 여시면 됩니다. **다른 업체와 일하실 때 쓰셔도 됩니다.** 애초에 그러라고 공개한 문서입니다."),
    # ─────────────────────────── 신뢰 센터 ───────────────────────────
    dict(key="trust.hero_title", kind="text", section="신뢰 센터", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="우리에게 맡긴 것이\n어떻게 다뤄지는지"),
    dict(key="trust.hero_lead", kind="text", section="신뢰 센터", label="상단 소개 문단",
         hint="", default="진단이 끝나도 구성도와 계정 체계, 취약점 목록은 저희 쪽에 남기 때문에 그 자료를 어디에 두는지, 얼마나 갖고 있다가 어떻게 없애는지를 아래에 적었습니다. 계약 전에 미리 보셔도 됩니다."),
    # ─────────────────────────── 규제 가이드 ───────────────────────────
    dict(key="regulations.hero_title", kind="text", section="규제 가이드", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="무엇이 우리에게\n해당되는가"),
    dict(key="regulations.hero_lead", kind="text", section="규제 가이드", label="상단 소개 문단",
         hint="법령·제도 서술이 섞여 있습니다. 사실관계는 원문으로 확인하고 고치세요.", default="제도 이름은 익숙한데 우리 회사가 어디에 걸리는지는 애매하실 겁니다. 그래서 국내 정보보호 제도를 근거 법령과 대상, 주기로 나란히 놓고 정리했습니다. 다만 수치와 해석은 원문으로 최종 확인하시는 편이 안전합니다."),
    # ─────────────────────────── 인사이트 ───────────────────────────
    dict(key="insights.hero_title", kind="text", section="인사이트", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다. 글 목록은 [인사이트] 탭에서 관리합니다.", default="현장에서\n반복되는 것들"),
    dict(key="insights.hero_lead", kind="text", section="인사이트", label="상단 소개 문단",
         hint="", default="진단을 나가면 조직은 달라도 같은 문제가 반복됩니다. 규제 해석이 갈리는 지점, 조치가 자주 미끄러지는 지점, 그리고 실제로 통했던 방법을 기록합니다."),
    # ─────────────────────────── 채용 ───────────────────────────
    dict(key="careers.hero_title", kind="text", section="채용", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다. 공고는 [채용 공고] 탭에서 관리합니다.", default="근거로 말하는\n사람을 찾습니다"),
    dict(key="careers.hero_lead", kind="text", section="채용", label="상단 소개 문단",
         hint="", default="“아마 취약할 것 같다”가 아니라 “이렇게 재현된다”로 말하는 사람과 일합니다. 경력의 길이보다 검증하는 습관을 봅니다."),
    # ─────────────────────────── 문의 ───────────────────────────
    dict(key="contact.hero_title", kind="text", section="문의", label="상단 큰 제목",
         hint="줄바꿈이 그대로 반영됩니다.", default="범위부터\n같이 정리합니다"),
    dict(key="contact.hero_lead", kind="text", section="문의", label="상단 소개 문단",
         hint="비용 청구 여부 같은 약속이 들어 있습니다. 실제 운영과 맞는지 확인하고 고치세요.",
         default="무엇이 필요한지 확정되지 않아도 괜찮습니다. 현재 상황만 알려주시면 필요한 진단과 우선순위, 예상 일정을 정리해 회신드립니다. **범위 검토와 견적 산정에는 비용이 발생하지 않습니다.**"),
    # ─────────────────────────── 회사소개 ───────────────────────────
    dict(
        key="about.hero_title", kind="text", section="회사소개", label="상단 큰 제목",
        hint="줄바꿈한 자리에서 실제로 줄이 바뀝니다. 3줄을 넘기지 않는 편이 좋습니다.",
        default="확인한 것만\n보고서에 씁니다",
    ),
    dict(
        key="about.hero_lead", kind="text", section="회사소개", label="상단 소개 문단",
        hint="제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.",
        default="쉴더스랩(SHIELDUS LAB)은 ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사이며, 진단으로 찾아낸 항목이 실제 조치로 이어지는 데까지를 과업 범위로 봅니다. 그래서 보고서 제출은 중간 지점입니다.",
    ),
    dict(
        key="about.view_title", kind="text", section="회사소개", label="01 관점 — 제목",
        hint="줄바꿈이 그대로 반영됩니다.",
        default="발견마다 담당자와\n순서를 붙입니다",
    ),
    dict(
        key="about.view_body", kind="rich", section="회사소개", label="01 관점 — 본문",
        hint="빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.",
        default="작년 보고서에 있던 항목이 올해 또 올라오는 이유는 무엇일까요. 담당자가 손을 놓아서인 경우는 드뭅니다. 발견 사항이 어느 조직의 어떤 작업으로 넘어가는지 적혀 있지 않고, 고쳤는지 되짚는 절차가 **계약 범위에 없을 때** 같은 목록이 해마다 되돌아옵니다.\n\n그래서 저희는 발견마다 걸리는 규제 조항과 그 항목을 받아 갈 담당 조직을 함께 붙이고, 조치가 적용됐는지는 재점검에서 직접 열어 확인합니다. “지금은 안전한가”라는 질문까지 답한 뒤에 과업을 닫습니다.",
    ),
    dict(
        key="about.name_title", kind="text", section="회사소개", label="02 사명 — 제목",
        hint="줄바꿈이 그대로 반영됩니다.",
        default="이름이 곧\n하는 일입니다",
    ),
    dict(
        key="about.name_body", kind="rich", section="회사소개", label="02 사명 — 본문",
        hint="사명의 뜻(SHIELD·US·LAB)을 설명하는 문단입니다. 빈 줄로 문단을 나누고 **굵게** 를 씁니다.",
        default="**shield us**, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 **LAB**이 붙어 사명이 됐습니다. 국문 **쉴더스랩**과 영문 표기는 같은 말을 두 번 적은 것입니다.\n\n여기서 **us**는 고객사만 가리키는 말이 아닙니다. 저희도 그 안에 들어갑니다. 지켜 주는 쪽과 지킴받는 쪽을 갈라 놓으면 보고서를 건네는 순간 일이 끝나 버리고, 그래서 조치가 닫히기 전까지는 저희 과업도 열려 있습니다.\n\n**LAB**은 방법을 열어 둔다는 뜻으로 씁니다. 진단 순서와 위험도 등급 기준을 계약 전에 공개하고, 발견 하나하나에 재현 절차를 적습니다. 다시 해 봐도 같은 결과가 나오지 않는 항목은 연구 결과라고 부를 수 없습니다.",
    ),
    # ─────────────────────────── 대표이사 인사말 ───────────────────────────
    dict(
        key="about.message_title", kind="text", section="대표이사 인사말", label="제목",
        hint="", default="대표이사 인사말",
    ),
    dict(
        key="about.message_body", kind="rich", section="대표이사 인사말", label="본문",
        hint="빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.",
        default="두꺼운 보고서를 다 읽고도 다음 주 월요일 아침에 무엇부터 손대야 할지 모르겠다면, 저는 그것을 **컨설팅의 실패**라고 봅니다.\n\n쉴더스랩은 그 지점에서 출발했습니다. 취약점 목록을 넘기는 데서 멈추면 담당자의 다음 주는 어제와 똑같기 때문입니다. 저희는 발견을 규제 조항과 담당 조직의 작업 단위로 옮기고, 왜 그 순서여야 하는지를 옆에 적습니다. 조치를 다시 확인하는 데까지가 계약 범위입니다.\n\n**할 수 없는 일을 할 수 있다고 말씀드리지 않습니다.** 법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위도 있습니다. 그 경계는 이 홈페이지에 숨김 없이 적어 두었습니다. **확인하지 않은 것을 확인했다고 쓰는 일도 없습니다.** 재현되지 않은 취약점은 보고서에 올라가지 않습니다.\n\n방법론과 산출물 규격을 계약 전에 공개하는 것도 같은 이유에서입니다. 저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 하니까요. 어디부터 봐야 할지 모르시겠다면 그 이야기부터 꺼내 주셔도 됩니다. 범위를 정하는 일에서부터 시작하겠습니다.",
    ),
    dict(
        key="about.message_role", kind="text", section="대표이사 인사말", label="서명 — 직함",
        hint="", default="쉴더스랩 대표이사",
    ),
    dict(
        key="about.message_name", kind="text", section="대표이사 인사말", label="서명 — 성명",
        hint="푸터의 ‘대표자’ 표기와는 별개입니다. 그쪽은 [법인 정보]의 대표자명을 씁니다.",
        default="이성훈",
    ),
    # ─────────────────────────── 서비스 ───────────────────────────
    dict(
        key="services.hero_title", kind="text", section="서비스", label="상단 큰 제목",
        hint="줄바꿈이 그대로 반영됩니다.", default="보고서가 두 개면\n우선순위도 두 개입니다",
    ),
    dict(
        key="services.hero_lead", kind="text", section="서비스", label="상단 소개 문단",
        hint="서비스 목록 위에 놓이는 한 문단입니다.",
        default="관리체계는 A업체, 기술진단은 B업체. 이렇게 갈라 맡기면 담당자 책상 위에 위험도 기준이 서로 다른 보고서 두 권이 놓입니다. 어느 쪽 “높음”을 먼저 잡아야 하는지는 어느 쪽에도 적혀 있지 않습니다. 여섯 영역의 발견을 같은 등급 정의로 판정해 우선순위 목록 하나로 묶는 이유입니다.",
    ),
    # ─────────────────────────── 브랜드 ───────────────────────────
    dict(
        key="brand.name_summary", kind="text", section="브랜드 · CI", label="사명의 뜻 (요약)",
        hint="/brand/ 맨 위에 놓이는 요약입니다. 자세한 설명은 [회사소개]의 ‘02 사명’ 블록에 있습니다.",
        default="shield us, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 LAB이 붙었습니다. 로고의 실드와 그 안의 각인도 같은 뜻에서 나왔습니다.",
    ),
    # ─────────────────────────── 푸터 ───────────────────────────
    dict(
        key="footer.blurb", kind="text", section="푸터", label="푸터 소개 문단",
        hint="모든 페이지 하단에 공통으로 나옵니다.",
        default="ISMS-P 인증 대응과 기술 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사입니다. "
                "발견에는 재현 절차를, 종료에는 재점검을 붙입니다.",
    ),
    # ─────────────────────────── 법인 정보 ───────────────────────────
    # 값이 비면 화면에 렌더하지 않는다(임시 문구 노출 방지). config.js 의 COMPANY 를 덮어쓴다.
    dict(key="company.legal_name", kind="text", section="법인 정보", label="등기 상호",
         hint="예: 주식회사 쉴더스랩. 비워두면 ‘쉴더스랩’으로 표시됩니다.", default=""),
    dict(key="company.ceo", kind="text", section="법인 정보", label="대표자명",
         hint="푸터 사업자 정보에 표시됩니다.", default="이성훈"),
    dict(key="company.biz_no", kind="text", section="법인 정보", label="사업자등록번호",
         hint="예: 000-00-00000", default=""),
    dict(key="company.addr", kind="text", section="법인 정보", label="사업장 주소", hint="", default=""),
    dict(key="company.tel", kind="text", section="법인 정보", label="대표번호", hint="", default=""),
    dict(key="company.fax", kind="text", section="법인 정보", label="팩스", hint="", default=""),
    dict(key="company.privacy_officer", kind="text", section="법인 정보", label="개인정보 보호책임자",
         hint="개인정보처리방침이 이 값을 참조합니다. 대외 홍보 전에 채워야 고지 요건이 완성됩니다.",
         default=""),
]

BY_KEY = {b["key"]: b for b in BLOCKS}


def default_of(key):
    b = BY_KEY.get(key)
    return b["default"] if b else ""


def kind_of(key):
    b = BY_KEY.get(key)
    return b["kind"] if b else "text"
