-- ═══════════════════════════════════════════════════════════════════
-- 공개 데이터 시드 — 라이브에서 공개 키(anon)로 내보낸 실데이터
--   생성: 2026-10-02T22:34:48  ·  원본: https://nrdapzgtibbusvoaceuh.supabase.co
--   생성기: deploy/scripts/export-public.py  ← 이관 당일 다시 돌릴 것(스냅숏이다)
--   포함: sl_settings · sl_content · sl_insights · sl_jobs
--   ⚠ 미포함: sl_admins · sl_inquiries · sl_applications · sl_audit · auth.users
--             RLS 로 공개 키에 0행 → 오너가 scripts/export-from-supabase.sh 로 뜬다.
--   적재: init-db.sh 가 session_replication_role=replica(트리거 끔)로 넣는다.
-- 재실행 안전: 테이블마다 비우고 라이브 상태로 다시 채운다(라이브가 정본).
-- ═══════════════════════════════════════════════════════════════════
begin;

-- ── sl_settings (4행) ──
delete from public.sl_settings;
insert into public.sl_settings (key, value, updated_at) values ('business_hours', '"평일 09:00 – 18:00"'::jsonb, '2026-08-09T05:33:05.684735+00:00')
  on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;
insert into public.sl_settings (key, value, updated_at) values ('contact_email', '"contact@shilderslab.com"'::jsonb, '2026-08-09T05:33:05.684735+00:00')
  on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;
insert into public.sl_settings (key, value, updated_at) values ('notice', '{"on": true, "href": "", "text": "8월 9일 우리들의 긴 여정이 시작됩니다. Keep Challenge, Win Together"}'::jsonb, '2026-08-09T05:33:05.684735+00:00')
  on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;
insert into public.sl_settings (key, value, updated_at) values ('sla_note', '"영업일 기준 24시간 내 초기 회신"'::jsonb, '2026-08-09T05:33:05.684735+00:00')
  on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;

-- ── sl_content (51행) ──
delete from public.sl_content;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.hero_lead', '쉴더스랩(SHIELDUS LAB)은 ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사이며, 진단으로 찾아낸 항목이 실제 조치로 이어지는 데까지를 과업 범위로 봅니다. 그래서 보고서 제출은 중간 지점입니다.', 'text', '회사소개', '상단 소개 문단', '제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.', 320, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.hero_title', '확인한 것만 보고서에 씁니다', 'text', '회사소개', '상단 큰 제목', '줄바꿈한 자리에서 실제로 줄이 바뀝니다. 3줄을 넘기지 않는 편이 좋습니다.', 310, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.message_body', '두꺼운 보고서를 다 읽고도 다음 주 월요일 아침에 무엇부터 손대야 할지 모르겠다면, 저는 그것을 **컨설팅의 실패**라고 봅니다.

쉴더스랩은 그 지점에서 출발했습니다. 취약점 목록을 넘기는 데서 멈추면 담당자의 다음 주는 어제와 똑같기 때문입니다. 저희는 발견을 규제 조항과 담당 조직의 작업 단위로 옮기고, 왜 그 순서여야 하는지를 옆에 적습니다. 조치를 다시 확인하는 데까지가 계약 범위입니다.

**할 수 없는 일을 할 수 있다고 말씀드리지 않습니다.** 법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위도 있습니다. 그 경계는 이 홈페이지에 숨김 없이 적어 두었습니다. **확인하지 않은 것을 확인했다고 쓰는 일도 없습니다.** 재현되지 않은 취약점은 보고서에 올라가지 않습니다.

방법론과 산출물 규격을 계약 전에 공개하는 것도 같은 이유에서입니다. 저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 하니까요. 어디부터 봐야 할지 모르시겠다면 그 이야기부터 꺼내 주셔도 됩니다. 범위를 정하는 일에서부터 시작하겠습니다.', 'rich', '대표이사 인사말', '본문', '빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.', 380, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.message_name', '이성훈', 'text', '대표이사 인사말', '서명 — 성명', '푸터의 ‘대표자’ 표기와는 별개입니다. 그쪽은 [법인 정보]의 대표자명을 씁니다.', 400, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.message_role', '쉴더스랩 대표이사', 'text', '대표이사 인사말', '서명 — 직함', '', 390, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.message_title', '대표이사 인사말', 'text', '대표이사 인사말', '제목', '', 370, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.name_body', '**shield us**, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 **LAB**이 붙어 사명이 됐습니다. 국문 **쉴더스랩**과 영문 표기는 같은 말을 두 번 적은 것입니다.

여기서 **us**는 고객사만 가리키는 말이 아닙니다. 저희도 그 안에 들어갑니다. 지켜 주는 쪽과 지킴받는 쪽을 갈라 놓으면 보고서를 건네는 순간 일이 끝나 버리고, 그래서 조치가 닫히기 전까지는 저희 과업도 열려 있습니다.

**LAB**은 방법을 열어 둔다는 뜻으로 씁니다. 진단 순서와 위험도 등급 기준을 계약 전에 공개하고, 발견 하나하나에 재현 절차를 적습니다. 다시 해 봐도 같은 결과가 나오지 않는 항목은 연구 결과라고 부를 수 없습니다.', 'rich', '회사소개', '02 사명 — 본문', '사명의 뜻(SHIELD·US·LAB)을 설명하는 문단입니다. 빈 줄로 문단을 나누고 **굵게** 를 씁니다.', 360, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.name_title', '이름이 곧. 하는 일입니다', 'text', '회사소개', '02 사명 — 제목', '줄바꿈이 그대로 반영됩니다.', 350, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.view_body', '작년 보고서에 있던 항목이 올해 또 올라오는 이유는 무엇일까요. 담당자가 손을 놓아서인 경우는 드뭅니다. 발견 사항이 어느 조직의 어떤 작업으로 넘어가는지 적혀 있지 않고, 고쳤는지 되짚는 절차가 **계약 범위에 없을 때** 같은 목록이 해마다 되돌아옵니다.

그래서 저희는 발견마다 걸리는 규제 조항과 그 항목을 받아 갈 담당 조직을 함께 붙이고, 조치가 적용됐는지는 재점검에서 직접 열어 확인합니다. “지금은 안전한가”라는 질문까지 답한 뒤에 과업을 닫습니다.', 'rich', '회사소개', '01 관점 — 본문', '빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.', 340, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('about.view_title', '발견마다 담당자와 순서를 붙입니다', 'text', '회사소개', '01 관점 — 제목', '줄바꿈이 그대로 반영됩니다.', 330, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('brand.name_summary', 'shield us, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 LAB이 붙었습니다. 로고의 실드와 그 안의 각인도 같은 뜻에서 나왔습니다.', 'text', '브랜드 · CI', '사명의 뜻 (요약)', '/brand/ 맨 위에 놓이는 요약입니다. 자세한 설명은 [회사소개]의 ‘02 사명’ 블록에 있습니다.', 430, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('careers.hero_lead', '“아마 취약할 것 같다”가 아니라 “이렇게 보여 집니다”로 말하는 사람과 일합니다. 경력의 길이보다 검증하는 습관을 봅니다.', 'text', '채용', '상단 소개 문단', '', 280, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('careers.hero_title', '자신감 있는 사람을 찾습니다', 'text', '채용', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다. 공고는 [채용 공고] 탭에서 관리합니다.', 270, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.addr', '', 'text', '법인 정보', '사업장 주소', '', 480, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.biz_no', '', 'text', '법인 정보', '사업자등록번호', '예: 000-00-00000', 470, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.ceo', '이성훈', 'text', '법인 정보', '대표자명', '푸터 사업자 정보에 표시됩니다.', 460, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.fax', '', 'text', '법인 정보', '팩스', '', 500, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.legal_name', '', 'text', '법인 정보', '등기 상호', '예: 주식회사 쉴더스랩. 비워두면 ‘쉴더스랩’으로 표시됩니다.', 450, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.privacy_officer', '', 'text', '법인 정보', '개인정보 보호책임자', '개인정보처리방침이 이 값을 참조합니다. 대외 홍보 전에 채워야 고지 요건이 완성됩니다.', 510, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('company.tel', '', 'text', '법인 정보', '대표번호', '', 490, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('contact.hero_lead', '무엇이 필요한지 확정되지 않아도 괜찮습니다. 현재 상황만 알려주시면 필요한 진단과 우선순위, 예상 일정을 정리해 회신드립니다. **범위 검토와 견적 산정에는 비용이 발생하지 않습니다.**', 'text', '문의', '상단 소개 문단', '비용 청구 여부 같은 약속이 들어 있습니다. 실제 운영과 맞는지 확인하고 고치세요.', 300, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('contact.hero_title', '범위부터 같이 정리합니다', 'text', '문의', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 290, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('footer.blurb', 'ISMS-P 인증 대응과 기술 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사입니다. 발견에는 재현 절차를, 종료에는 재점검을 붙입니다.', 'text', '푸터', '푸터 소개 문단', '모든 페이지 하단에 공통으로 나옵니다.', 440, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.careers_lead', '컨설팅은 결국 사람이 하는 일이라, 채용은 서비스 품질과 같은 문제로 봅니다. 지금 열려 있는 자리입니다.', 'text', '홈', '06 채용 — 소개 문단', '공고 목록 자체는 [채용] 탭에서 관리합니다. 여기는 그 위에 붙는 소개 문구입니다.', 140, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.careers_title', '함께 할 사람을 찾습니다', 'text', '홈', '06 채용 — 제목', '공개 채용 공고가 있을 때만 이 섹션이 홈에 나옵니다. 줄바꿈이 그대로 반영됩니다.', 130, '2026-08-09T05:35:27.396276+00:00', 'cba0d84c-e117-425f-a6ed-5dc579e7c177')
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.cta_lead', '어디부터 봐야 할지 모르시겠다면 진단 대상과 목표 일정, 이 두 가지만 알려 주시면 필요한 점검 항목과 예상 기간을 정리해 보내 드립니다. 범위 검토와 견적 산정에는 비용이 붙지 않습니다.', 'text', '홈', '맨 아래 상담 유도 — 문단', '비용 청구 여부 같은 약속이 들어 있습니다. 실제 운영과 맞는지 확인하고 고치세요.', 160, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.cta_title', '지금 상태를
확인하는 것부터', 'text', '홈', '맨 아래 상담 유도 — 제목', '줄바꿈이 그대로 반영됩니다.', 150, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.hero_lead', 'ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 맡습니다. 취약하다고 적은 항목에는 어떻게 재현했는지를 덧붙이고, 조치가 끝나면 한 번 더 들어가 조치 되었는지 확인합니다.', 'text', '홈', '상단 소개 문단', '제목 아래 한 문단. 검색 결과 미리보기에도 영향을 줍니다.', 20, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.hero_title', '정보보호 전문가가  
제대로 처리합니다', 'text', '홈', '상단 큰 제목', '사이트에서 가장 먼저 읽히는 문장입니다. 줄바꿈이 그대로 반영됩니다.', 10, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.insights_lead', '같은 질문을 여러 번 받으면 글로 정리합니다. 규제 해석이 엇갈리는 대목, 조치가 번번이 멈추는 지점을 다룹니다.', 'text', '홈', '05 인사이트 — 소개 문단', '', 120, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.insights_title', '현장에서 반복되는 것들', 'text', '홈', '05 인사이트 — 제목', '줄바꿈이 그대로 반영됩니다.', 110, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.method_lead', '단계마다 나가는 산출물은 계약서에 문서명 단위로 적힙니다. 마지막 재점검이 끝나기 전에는 종료로 처리하지 않습니다.', 'text', '홈', '02 방법론 — 소개 문단', '‘다섯 단계’ 라는 서술은 /method/ 의 실제 단계 수와 맞아야 합니다.', 60, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.method_title', '모든 과업은
같은 다섯 단계를 거칩니다', 'text', '홈', '02 방법론 — 제목', '줄바꿈이 그대로 반영됩니다.', 50, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.resources_lead', '진단 현장에 실제로 들고 나가는 체크리스트입니다. 이메일을 남기실 필요는 없습니다. 다른 업체와 진행 중이셔도 활용하시는 데 문제없습니다.', 'text', '홈', '04 자료실 — 소개 문단', '', 100, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.resources_title', '체크리스트를 기반으로
언제든지 문의하세요', 'text', '홈', '04 자료실 — 제목', '줄바꿈이 그대로 반영됩니다.', 90, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.services_lead', '인증 심사 대응과 기술 진단을 서로 다른 업체에 나눠 맡기면 어떻게 될까요? 같은 자산을 두 번 조사하고도, 심사에서 지적된 결함과 실제 침해 경로는 끝내 어긋난 채 남습니다. 그 둘을 맞춰 보는 일이 결국 담당자 몫이 되기 때문에, 저희는 두 영역을 하나의 범위 정의서 안에서 설계합니다.', 'text', '홈', '01 서비스 — 소개 문단', '', 40, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.services_title', '규제 그리고 공격과 방어,
양쪽에서 봅니다', 'text', '홈', '01 서비스 — 제목', '줄바꿈이 그대로 반영됩니다.', 30, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.why_lead', '제안서를 나란히 놓고 보면 문장은 다들 비슷한데, 정작 누가 무엇을 어떻게 하겠다는 것인지는 잘 드러나지 않습니다. 그래서 위험도 산정 기준과 산출물 목록, 맡지 않는 과업까지 계약 전에 공개합니다. 저희 제안서에만 쓰시라고 올린 자료는 아닙니다.', 'text', '홈', '03 판단 기준 — 소개 문단', '', 80, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('home.why_title', '판단 기준을
먼저 공개합니다', 'text', '홈', '03 판단 기준 — 제목', '줄바꿈이 그대로 반영됩니다.', 70, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('insights.hero_lead', '진단을 나가면 조직은 달라도 같은 문제가 반복됩니다. 규제 해석이 갈리는 지점, 조치가 자주 미끄러지는 지점, 그리고 실제로 통했던 방법을 기록합니다.', 'text', '인사이트', '상단 소개 문단', '', 260, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('insights.hero_title', '현장에서 반복되는 것들', 'text', '인사이트', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다. 글 목록은 [인사이트] 탭에서 관리합니다.', 250, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('method.hero_lead', '제안서를 여러 곳에서 받아 놓고도 무엇을 기준으로 비교해야 할지 막막할 때가 있습니다. 쉴더스랩은 그래서 실제로 쓰는 5단계 절차와 위험도 산정 기준, 산출물 규격을 계약 전에 공개합니다. 감추면 비교가 안 되니까요.', 'text', '진단 방법론', '상단 소개 문단', '', 180, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('method.hero_title', 'AI, 클라우드 등의 
환경 부터  살펴봅니다.', 'text', '진단 방법론', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 170, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('regulations.hero_lead', '제도 이름은 익숙한데 우리 회사가 어디에 걸리는지는 애매하실 겁니다. 그래서 국내 정보보호 제도를 근거 법령과 대상, 주기로 나란히 놓고 정리했습니다. 다만 수치와 해석은 원문으로 최종 확인하시는 편이 안전합니다.', 'text', '규제 가이드', '상단 소개 문단', '법령·제도 서술이 섞여 있습니다. 사실관계는 원문으로 확인하고 고치세요.', 240, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('regulations.hero_title', '무엇이 우리에게 해당되는가', 'text', '규제 가이드', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 230, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('resources.hero_lead', '저희가 과업에서 쓰는 문서를 손질 없이 그대로 올렸으니, 로그인이나 이메일 주소를 남기실 필요 없이 바로 여시면 됩니다. **다른 업체와 일하실 때 쓰셔도 됩니다.** 애초에 그러라고 공개한 문서입니다.', 'text', '자료실', '상단 소개 문단', '', 200, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('resources.hero_title', '계약 전에 활용 하실 수 있게', 'text', '자료실', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 190, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('services.hero_lead', '관리체계는 A업체, 기술진단은 B업체. 이렇게 갈라 맡기면 담당자 책상 위에 위험도 기준이 서로 다른 보고서 두 권이 놓입니다. 어느 쪽 “높음”을 먼저 잡아야 하는지는 어느 쪽에도 적혀 있지 않습니다. 여섯 영역의 발견을 같은 등급 정의로 판정해 우선순위 목록 하나로 묶는 이유입니다.', 'text', '서비스', '상단 소개 문단', '서비스 목록 위에 놓이는 한 문단입니다.', 420, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('services.hero_title', '보고서가 두 개면 우선순위도 두 개입니다', 'text', '서비스', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 410, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('trust.hero_lead', '진단이 끝나도 구성도와 계정 체계, 취약점 목록은 저희 쪽에 남기 때문에 그 자료를 어디에 두는지, 얼마나 갖고 있다가 폐기하는지를 아래에 적었습니다. 계약 전에 미리 보셔도 됩니다.', 'text', '신뢰 센터', '상단 소개 문단', '', 220, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;
insert into public.sl_content (key, value, kind, section, label, hint, sort_order, updated_at, updated_by) values ('trust.hero_title', '우리에게 맡긴 것이 어떻게 다뤄지는지', 'text', '신뢰 센터', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 210, '2026-08-09T05:25:58.015107+00:00', null)
  on conflict (key) do update set value = excluded.value, kind = excluded.kind, section = excluded.section, label = excluded.label, hint = excluded.hint, sort_order = excluded.sort_order, updated_at = excluded.updated_at, updated_by = excluded.updated_by;

-- ── sl_insights (3행) ──
delete from public.sl_insights;
insert into public.sl_insights (id, slug, category, title, summary, body, author, published, published_at, sort_order, created_at, updated_at) values ('15765016-cf0a-402e-a9c7-0895d2bb8e9a', 'cloud-misconfigurations-we-find-most', '클라우드', '클라우드 계정에서 가장 자주 발견되는 구성 다섯 가지', '클라우드 사고의 상당수는 소프트웨어 취약점이 아니라 구성에서 시작됩니다. 진단에서 반복적으로 확인되는 항목을 정리했습니다.', '클라우드 환경 진단에서 반복해서 나오는 구성 문제는 대체로 새로운 기술의 문제가 아니라, 초기 설정이 그대로 남아 있는 문제입니다.

## 1. 과도한 IAM 권한

개발 편의를 위해 부여한 광범위 권한이 운영 단계까지 남는 경우가 가장 많습니다. 관리자 권한을 가진 사용자·역할의 수, 와일드카드 권한, 오래 사용되지 않은 액세스 키를 주기적으로 점검해야 합니다. 특히 **CI/CD 파이프라인에 부여된 권한**은 사람보다 강한 권한을 갖고 있으면서 검토 대상에서 빠지곤 합니다.

## 2. 공개된 스토리지와 스냅샷

버킷 자체를 공개하지 않았더라도, 사전 서명 URL의 만료 기간이 과도하거나 스냅샷·이미지의 공유 설정이 열려 있으면 같은 결과가 됩니다. 데이터 자산 목록과 공개 여부를 함께 관리해야 합니다.

## 3. 꺼져 있거나 짧게 보관되는 감사 로그

사고 이후 원인을 확인하려면 로그가 남아 있어야 합니다. 감사 로그 활성화 여부, 보존 기간, 로그 저장 위치에 대한 접근 통제(로그를 지울 수 있는 권한이 누구에게 있는지)까지 확인이 필요합니다.

## 4. 불필요하게 열린 인바운드

`0.0.0.0/0` 으로 열린 관리 포트(SSH·RDP·DB)는 여전히 흔하게 발견됩니다. 임시로 열었다가 닫지 않은 규칙이 대부분이므로, 보안그룹 변경에 대한 승인·검토 절차가 있는지가 근본 대책입니다.

## 5. 관리 콘솔 계정의 MFA 미적용

루트·관리자 계정에 다중 인증이 적용되지 않은 상태는 단일 자격증명 유출로 전체 환경이 넘어가는 구조를 의미합니다. 계정 생성 시점의 기준선(baseline)에 포함시켜야 합니다.

## 진단 후 실제로 효과가 있었던 접근

- 기준선(baseline)을 문서가 아니라 **IaC 코드로** 관리해 신규 자원에 자동 적용
- 변경 승인 절차에 보안 검토 지점을 한 곳만 추가(전체 프로세스를 바꾸지 않음)
- 분기별 권한 검토를 담당자 개인 작업이 아니라 티켓으로 남기기

구성 진단은 범위가 넓지만 계정 단위로 빠르게 확인할 수 있는 항목이 많습니다. 현재 환경(제공자·계정 수·주요 서비스)만 알려주시면 필요한 점검 범위를 정리해 드립니다.', '쉴더스랩', true, '2026-07-16', 10, '2026-07-30T02:18:52.682805+00:00', '2026-07-30T02:18:52.682805+00:00')
  on conflict (id) do update set slug = excluded.slug, category = excluded.category, title = excluded.title, summary = excluded.summary, body = excluded.body, author = excluded.author, published = excluded.published, published_at = excluded.published_at, sort_order = excluded.sort_order, created_at = excluded.created_at, updated_at = excluded.updated_at;
insert into public.sl_insights (id, slug, category, title, summary, body, author, published, published_at, sort_order, created_at, updated_at) values ('abfa91fb-72e5-4f97-b348-ee0dedd507de', 'reading-a-penetration-test-proposal', '모의해킹', '모의해킹 견적서를 받았다면 확인해야 할 다섯 가지', '같은 "웹 모의해킹"이라는 이름으로 견적 차이가 몇 배까지 벌어집니다. 가격이 아니라 범위와 방식이 다르기 때문입니다.', '모의해킹 견적을 비교할 때 금액만 보면 실제로 무엇을 받는지 알 수 없습니다. 다음 다섯 가지를 확인하면 견적서의 성격이 드러납니다.

## 1. 자동 스캔인가, 수동 검증인가

취약점 스캐너 결과를 정리한 보고서와, 발견 항목을 사람이 직접 재현·검증한 보고서는 비용도 결과물도 다릅니다. 견적서에 **수동 점검 항목**과 **재현 절차 제공 여부**가 명시되어 있는지 확인하세요. 오탐(false positive)을 걸러내는 작업이 포함되지 않으면 조치 단계에서 시간이 더 듭니다.

## 2. 인증 이후 영역을 보는가

로그인 전 화면만 점검하는 진단은 실제 위험의 일부만 봅니다. 권한별 계정을 발급받아 **인가 우회, 수평·수직 권한 상승, 업무 논리 결함**을 확인하는지가 중요합니다. 계정 발급 협조가 필요한 항목이므로 견적 단계에서 협의되어야 합니다.

## 3. API와 모바일이 범위에 있는가

프런트엔드 화면만 점검하고 API를 제외하면, 가장 흔한 대량 정보 노출 경로가 빠집니다. 모바일 앱이 있다면 앱 자체 점검(로컬 저장 데이터·통신 보호)과 앱이 호출하는 API 점검은 별개 작업입니다.

## 4. 재점검이 포함되어 있는가

조치 후 재점검이 없으면 "고쳤다고 생각한 상태"로 끝납니다. 재점검 1회 포함 여부와, 재점검 범위(전체 재수행 / 조치 항목 한정)를 확인하세요.

## 5. 산출물과 보고 대상이 정의되어 있는가

경영진 보고용 요약과 실무 조치 가이드는 다른 문서입니다. 위험도 산정 기준(CVSS 등), 조치 우선순위 제시 방식, 보고 회의 포함 여부까지 견적서에 적혀 있으면 이후 분쟁이 줄어듭니다.

## 함께 확인하면 좋은 것

- 진단 수행 시간대와 서비스 영향 가능성에 대한 사전 합의
- 진단 데이터의 보관 기간과 파기 절차
- 발견 사항의 비밀유지 범위(NDA)

견적서 자체를 검토해 드리는 것도 가능합니다. 판단이 필요한 항목만 정리해서 회신드립니다.', '쉴더스랩', true, '2026-07-23', 20, '2026-07-30T02:18:52.682805+00:00', '2026-07-30T02:18:52.682805+00:00')
  on conflict (id) do update set slug = excluded.slug, category = excluded.category, title = excluded.title, summary = excluded.summary, body = excluded.body, author = excluded.author, published = excluded.published, published_at = excluded.published_at, sort_order = excluded.sort_order, created_at = excluded.created_at, updated_at = excluded.updated_at;
insert into public.sl_insights (id, slug, category, title, summary, body, author, published, published_at, sort_order, created_at, updated_at) values ('ce36042c-00e9-4495-bd2f-b7def93951ef', 'isms-p-first-certification-preparation', '인증 · 규제', 'ISMS-P 최초 인증, 준비 기간을 좌우하는 네 가지', '같은 규모의 조직인데 어떤 곳은 6개월, 어떤 곳은 1년 반이 걸립니다. 차이는 대부분 문서량이 아니라 준비 순서에서 생깁니다.', '최초 인증을 준비하는 조직에서 일정이 늘어지는 이유는 비슷합니다. 문서를 먼저 만들고 운영을 나중에 맞추려 하기 때문입니다.

## 1. 인증 범위를 먼저 확정한다

범위가 흔들리면 이후 모든 산출물이 다시 만들어집니다. 서비스 단위, 조직 단위, 자산(서버·네트워크·개인정보 처리 시스템) 단위로 경계를 그리고, 경계 밖 시스템과의 연계 지점을 목록화하는 것이 첫 작업입니다. 범위를 넓게 잡으면 심사 부담이 커지고, 너무 좁게 잡으면 실제 위험이 빠진 인증이 됩니다.

## 2. 문서보다 운영 기록이 먼저다

심사에서 확인하는 것은 "정책이 있는가"가 아니라 "정책대로 운영된 기록이 있는가"입니다. 접근권한 검토 이력, 변경 승인 기록, 백업 복구 시험 결과처럼 **시간이 쌓여야 생기는 증적**은 나중에 만들 수 없습니다. 준비 초기에 이런 활동을 먼저 시작해야 일정이 줄어듭니다.

## 3. 위험평가는 형식이 아니라 판단이다

자산 목록에 숫자만 채운 위험평가는 심사에서 반드시 질문을 받습니다. 위협·취약점 식별의 근거, 위험도 산정 기준, 수용 가능한 위험 수준(DoA)의 결정 주체가 설명 가능해야 합니다. 기술 취약점 진단 결과가 위험평가에 반영되어 있는지도 자주 확인되는 지점입니다.

## 4. 기술 진단과 관리체계를 분리하지 않는다

관리체계 컨설팅과 취약점 진단을 별도로 진행하면, 진단에서 나온 취약점이 위험평가와 조치 계획에 반영되지 않는 경우가 많습니다. 심사에서는 통과하더라도, 실제 침해 경로는 그대로 남습니다.

## 준비 체크리스트

- 인증 범위와 경계 연계 지점 목록이 문서로 존재한다
- 정책·지침이 실제 업무 절차와 일치한다(현실과 다른 조항이 없다)
- 최근 6개월 이상의 운영 기록(권한 검토·변경 관리·로그 점검)이 남아 있다
- 기술 취약점 진단 결과가 위험평가와 조치 계획에 연결되어 있다
- 개인정보 처리 흐름도가 최신 시스템 구성과 일치한다

인증 의무 대상 여부와 준비 기간은 조직 상황에 따라 다릅니다. 현재 상태를 기준으로 필요한 작업만 정리해 보고 싶다면 상담을 요청해 주세요.', '쉴더스랩', true, '2026-07-30', 30, '2026-07-30T02:18:52.682805+00:00', '2026-07-30T02:18:52.682805+00:00')
  on conflict (id) do update set slug = excluded.slug, category = excluded.category, title = excluded.title, summary = excluded.summary, body = excluded.body, author = excluded.author, published = excluded.published, published_at = excluded.published_at, sort_order = excluded.sort_order, created_at = excluded.created_at, updated_at = excluded.updated_at;

-- ── sl_jobs (2행) ──
delete from public.sl_jobs;
insert into public.sl_jobs (id, title, team, employment_type, location, summary, body, closes_at, published, sort_order, created_at, updated_at) values ('038147ab-495a-47ac-8a14-4792560fb493', '정보보호 컨설턴트 (관리체계 · ISMS-P)', '컨설팅팀', '정규직', '서울 (프로젝트에 따라 고객사 상주)', 'ISMS-P 인증 컨설팅과 개인정보 컴플라이언스 과업을 수행합니다.', '[담당 업무]
- ISMS-P 인증 취득·사후심사 컨설팅 (GAP 분석, 정책·지침 정비, 위험평가, 심사 대응)
- 개인정보 처리 흐름 진단 및 안전성 확보조치 이행 점검
- 진단 결과 보고서 작성 및 고객사 조치 이행 지원

[자격 요건]
- 정보보호 컨설팅 또는 기업 보안 담당 경험
- ISMS-P 인증기준에 대한 이해
- 문서로 근거를 남기는 습관

[우대 사항]
- ISMS-P 인증심사원, CISSP, CISA, CPPG 등 관련 자격
- 개인정보 영향평가(PIA) 수행 경험
- 금융·의료 등 규제 산업 프로젝트 경험

[전형 절차]
서류 검토 → 실무 인터뷰 → 최종 인터뷰 → 처우 협의

※ 상세 처우와 근무 조건은 인터뷰 단계에서 안내합니다.', null, true, 10, '2026-07-30T02:18:52.682805+00:00', '2026-08-08T08:12:32.739043+00:00')
  on conflict (id) do update set title = excluded.title, team = excluded.team, employment_type = excluded.employment_type, location = excluded.location, summary = excluded.summary, body = excluded.body, closes_at = excluded.closes_at, published = excluded.published, sort_order = excluded.sort_order, created_at = excluded.created_at, updated_at = excluded.updated_at;
insert into public.sl_jobs (id, title, team, employment_type, location, summary, body, closes_at, published, sort_order, created_at, updated_at) values ('7ae2ee44-18d3-44ea-80e7-fec2f856297d', '모의해킹 · 취약점 진단 엔지니어', '기술진단팀', '정규직', '서울', '웹·API·모바일·인프라 대상 모의해킹과 취약점 진단을 수행합니다.', '[담당 업무]
- 웹·API·모바일 애플리케이션 모의해킹 및 시나리오 기반 침투테스트
- 서버·네트워크·DB 등 인프라 취약점 진단
- 발견 사항의 재현 절차 작성, 위험도 산정, 조치 가이드 제공
- 조치 후 재점검 수행

[자격 요건]
- 모의해킹 또는 취약점 진단 수행 경험
- 웹 취약점(인증·인가·주입·업무논리)에 대한 실무 이해
- 발견 사항을 재현 가능한 형태로 문서화할 수 있는 역량

[우대 사항]
- CVE 등록, 버그바운티, CTF 입상 이력
- 클라우드 환경(AWS·Azure·GCP) 진단 경험
- 소스코드 진단 및 시큐어코딩 컨설팅 경험

[전형 절차]
서류 검토 → 기술 인터뷰(실기 포함 가능) → 최종 인터뷰 → 처우 협의

※ 진단 업무는 사전 서면 승인 범위 안에서만 수행합니다.', null, true, 20, '2026-07-30T02:18:52.682805+00:00', '2026-08-08T08:12:34.5704+00:00')
  on conflict (id) do update set title = excluded.title, team = excluded.team, employment_type = excluded.employment_type, location = excluded.location, summary = excluded.summary, body = excluded.body, closes_at = excluded.closes_at, published = excluded.published, sort_order = excluded.sort_order, created_at = excluded.created_at, updated_at = excluded.updated_at;

commit;
