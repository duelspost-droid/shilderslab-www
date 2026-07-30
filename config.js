/* ──────────────────────────────────────────────────────────────
   쉴더스랩 — 백엔드 연결 설정
   anon(publishable) 키는 공개되어도 되는 값이다. 실제 보호는 RLS + SECURITY DEFINER RPC.
   service_role 키는 절대 이 파일(또는 프런트 어디에도) 두지 않는다.
   ────────────────────────────────────────────────────────────── */
window.SL_CONFIG = {
  SUPABASE_URL: "https://nrdapzgtibbusvoaceuh.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_DckNy92c8WFGYWNPRsEjag_q-JQs9km",

  // 회사 정보 — 값이 빈 문자열이면 화면에 렌더하지 않는다(임시 문구 노출 방지).
  COMPANY: {
    nameKo: "쉴더스랩",
    nameEn: "SHILDERS LAB",
    legalKo: "",          // 예: "주식회사 쉴더스랩"  ← 등기 상호 확정 후 입력
    ceo: "",              // 대표자명
    bizNo: "",            // 사업자등록번호
    addr: "",             // 주소
    tel: "",              // 대표번호
    fax: "",
    email: "contact@shilderslab.com",
    privacyOfficer: "",   // 개인정보 보호책임자
    founded: "2026",
  },
};
