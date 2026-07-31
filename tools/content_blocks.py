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
    # ─────────────────────────── 회사소개 ───────────────────────────
    dict(
        key="about.hero_title", kind="text", section="회사소개", label="상단 큰 제목",
        hint="줄바꿈한 자리에서 실제로 줄이 바뀝니다. 3줄을 넘기지 않는 편이 좋습니다.",
        default="확인한 것만\n보고서에 씁니다",
    ),
    dict(
        key="about.hero_lead", kind="text", section="회사소개", label="상단 소개 문단",
        hint="제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.",
        default="쉴더스랩(SHIELDUS LAB)은 정보보호 컨설팅 회사입니다. "
                "ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하고, "
                "조치를 확인하는 재점검까지를 과업 범위로 봅니다.",
    ),
    dict(
        key="about.view_title", kind="text", section="회사소개", label="01 관점 — 제목",
        hint="줄바꿈이 그대로 반영됩니다.",
        default="발견마다 담당자와\n순서를 붙입니다",
    ),
    dict(
        key="about.view_body", kind="rich", section="회사소개", label="01 관점 — 본문",
        hint="빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.",
        default=(
            "진단을 받은 다음 해에 같은 항목이 다시 지적되는 일이 있습니다. "
            "발견 사항이 담당 조직의 작업 단위로 옮겨지지 않고, 조치 결과를 확인하는 절차가 "
            "**계약 범위에 없을 때** 그렇습니다.\n\n"
            "쉴더스랩은 발견을 규제 항목과 시스템 담당자의 작업 단위에 함께 연결합니다. "
            "조치가 적용됐는지 재점검으로 확인한 뒤 과업을 닫습니다. "
            "“무엇이 취약한가”에서 멈추지 않습니다. “지금은 안전한가”에 답하고 끝냅니다."
        ),
    ),
    # ─────────────────────────── 대표이사 인사말 ───────────────────────────
    dict(
        key="about.message_title", kind="text", section="대표이사 인사말", label="제목",
        hint="", default="대표이사 인사말",
    ),
    dict(
        key="about.message_body", kind="rich", section="대표이사 인사말", label="본문",
        hint="빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.",
        default=(
            "두꺼운 보고서를 받고도 다음 주 월요일에 무엇부터 손댈지 정하지 못하는 상황이 있습니다. "
            "저는 그 상태를 **컨설팅의 실패**로 봅니다.\n\n"
            "쉴더스랩은 그 지점에서 시작했습니다. 취약점을 찾아내는 일만으로는 변별력이 되기 어렵습니다. "
            "발견을 규제 조항과 담당자의 작업 단위로 옮기고, 우선순위에 근거를 붙이고, "
            "조치를 다시 확인한 뒤 과업을 닫습니다. 여기까지를 계약 범위에 넣습니다.\n\n"
            "저희가 스스로에게 두는 규칙은 두 가지입니다. 첫째, **할 수 없는 일을 할 수 있다고 말하지 않습니다.** "
            "법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위가 있습니다. "
            "그 경계는 홈페이지에 그대로 적어 두었습니다. 둘째, **확인하지 않은 것을 확인했다고 쓰지 않습니다.** "
            "재현되지 않은 취약점은 보고서에 올리지 않습니다.\n\n"
            "그래서 방법론과 산출물 규격을 계약 전에 공개합니다. "
            "저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 한다고 보기 때문입니다. "
            "함께 볼 범위부터 편하게 말씀해 주시면, 거기서부터 시작하겠습니다."
        ),
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
        hint="줄바꿈이 그대로 반영됩니다.", default="여섯 개 영역을\n같은 위험도 표로 봅니다",
    ),
    dict(
        key="services.hero_lead", kind="text", section="서비스", label="상단 소개 문단",
        hint="서비스 목록 위에 놓이는 한 문단입니다.",
        default="관리체계와 기술진단을 다른 업체가 맡으면 보고서 두 개의 위험도 기준이 서로 다릅니다. "
                "쉴더스랩은 여섯 영역의 발견을 같은 등급 정의로 판정하고, 하나의 우선순위 목록으로 묶습니다.",
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
