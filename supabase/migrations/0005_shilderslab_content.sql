-- ══════════════════════════════════════════════════════════════════════
-- 0005 — 페이지 문구 CMS (sl_content)
--
-- 목적: 자주 바뀌는 문구(회사소개·대표이사 인사말·서비스 인트로·푸터·법인 정보)를
--       코드 수정 없이 관리자 콘솔에서 고칠 수 있게 한다.
--
-- 설계 메모
--  · 값은 **평문/최소 마크다운**으로 저장한다. HTML 을 그대로 저장하지 않는다 —
--    관리자 계정이 탈취돼도 저장된 문자열이 스크립트로 실행되지 않게 하기 위함이다.
--    렌더는 빌드(build-pages.py) 와 클라이언트(site.js) 양쪽에서 이스케이프 후 수행한다.
--  · 값이 비어 있으면 코드에 박힌 기본 문구가 그대로 나온다(빈 화면이 되지 않는다).
--  · SEO: 빌드 시점에 정적 HTML 로 구워 넣고, 저장 직후에는 클라이언트가 덮어쓴다.
--    → 크롤러는 정적 본문을 보고, 관리자는 재빌드를 기다리지 않는다.
--  · 쓰기 권한은 is_sl_admin() — admin·editor 모두 문구를 고칠 수 있다.
--    (계정·설정과 달리 문구 수정은 되돌리기 쉬운 작업이다)
--
-- 재실행 안전(idempotent). **재실행해도 value 는 덮어쓰지 않는다** — 아래 시드의
-- on conflict 절이 메타데이터(kind/section/label/hint/sort_order)만 갱신한다.
-- ══════════════════════════════════════════════════════════════════════

create table if not exists public.sl_content (
  key         text primary key,
  value       text        not null default '',
  kind        text        not null default 'text',
  section     text        not null default '기타',
  label       text        not null default '',
  hint        text        not null default '',
  sort_order  int         not null default 0,
  updated_at  timestamptz not null default now(),
  updated_by  uuid
);

-- 방어적 상한 — 관리자 실수나 계정 탈취로 거대한 문자열이 들어가는 것을 막는다.
alter table public.sl_content drop constraint if exists sl_content_kind_chk;
alter table public.sl_content add  constraint sl_content_kind_chk check (kind in ('text','rich'));
alter table public.sl_content drop constraint if exists sl_content_len_chk;
alter table public.sl_content add  constraint sl_content_len_chk  check (length(value) <= 20000);

alter table public.sl_content enable row level security;

-- 읽기는 공개다. 어차피 공개 페이지에 나가는 문구이고, 클라이언트가 직접 읽어 덮어쓴다.
drop policy if exists sl_content_read on public.sl_content;
create policy sl_content_read on public.sl_content for select using (true);

-- 쓰기는 관리자(admin·editor)만.
drop policy if exists sl_content_write on public.sl_content;
create policy sl_content_write on public.sl_content for all to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());

-- ─────────── 갱신 흔적 ───────────
create or replace function public.sl_content_touch()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $fn$
begin
  new.updated_at := now();
  new.updated_by := auth.uid();
  return new;
end $fn$;

drop trigger if exists sl_content_touch_trg on public.sl_content;
create trigger sl_content_touch_trg before insert or update on public.sl_content
  for each row execute function public.sl_content_touch();

-- ─────────── 감사 로그 ───────────
-- 누가 어떤 블록을 언제 고쳤는지 남긴다. 본문 전체는 남기지 않는다(로그가 비대해지고,
-- 감사 로그 열람 권한이 곧 문구 이력 열람 권한이 되는 것도 바람직하지 않다).
create or replace function public.sl_content_audit()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $fn$
begin
  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail)
  values ('admin', auth.uid(), public.sl_my_email(), 'update_content', 'sl_content', new.key,
          jsonb_build_object('bytes', length(new.value)));
  return null;
end $fn$;

drop trigger if exists sl_content_audit_trg on public.sl_content;
create trigger sl_content_audit_trg after insert or update on public.sl_content
  for each row execute function public.sl_content_audit();

-- ══════════════════════════════════════════════════════════════════════
-- 시드 — tools/content_blocks.py 에서 생성됨. 손으로 고치지 말 것.
--   고칠 일이 생기면 content_blocks.py 를 고치고 tools/gen-content-seed.py 를 다시 돌린다.
-- ══════════════════════════════════════════════════════════════════════

insert into public.sl_content (key, value, kind, section, label, hint, sort_order) values
  ('about.hero_title', '확인한 것만
보고서에 씁니다', 'text', '회사소개', '상단 큰 제목', '줄바꿈한 자리에서 실제로 줄이 바뀝니다. 3줄을 넘기지 않는 편이 좋습니다.', 10),
  ('about.hero_lead', '쉴더스랩(SHIELDUS LAB)은 ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사이며, 진단으로 찾아낸 항목이 실제 조치로 이어지는 데까지를 과업 범위로 봅니다. 그래서 보고서 제출은 중간 지점입니다.', 'text', '회사소개', '상단 소개 문단', '제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.', 20),
  ('about.view_title', '발견마다 담당자와
순서를 붙입니다', 'text', '회사소개', '01 관점 — 제목', '줄바꿈이 그대로 반영됩니다.', 30),
  ('about.view_body', '작년 보고서에 있던 항목이 올해 또 올라오는 이유는 무엇일까요. 담당자가 손을 놓아서인 경우는 드뭅니다. 발견 사항이 어느 조직의 어떤 작업으로 넘어가는지 적혀 있지 않고, 고쳤는지 되짚는 절차가 **계약 범위에 없을 때** 같은 목록이 해마다 되돌아옵니다.

그래서 저희는 발견마다 걸리는 규제 조항과 그 항목을 받아 갈 담당 조직을 함께 붙이고, 조치가 적용됐는지는 재점검에서 직접 열어 확인합니다. “지금은 안전한가”라는 질문까지 답한 뒤에 과업을 닫습니다.', 'rich', '회사소개', '01 관점 — 본문', '빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.', 40),
  ('about.name_title', '이름이 곧
하는 일입니다', 'text', '회사소개', '02 사명 — 제목', '줄바꿈이 그대로 반영됩니다.', 50),
  ('about.name_body', '**shield us**, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 **LAB**이 붙어 사명이 됐습니다. 국문 **쉴더스랩**과 영문 표기는 같은 말을 두 번 적은 것입니다.

여기서 **us**는 고객사만 가리키는 말이 아닙니다. 저희도 그 안에 들어갑니다. 지켜 주는 쪽과 지킴받는 쪽을 갈라 놓으면 보고서를 건네는 순간 일이 끝나 버리고, 그래서 조치가 닫히기 전까지는 저희 과업도 열려 있습니다.

**LAB**은 방법을 열어 둔다는 뜻으로 씁니다. 진단 순서와 위험도 등급 기준을 계약 전에 공개하고, 발견 하나하나에 재현 절차를 적습니다. 다시 해 봐도 같은 결과가 나오지 않는 항목은 연구 결과라고 부를 수 없습니다.', 'rich', '회사소개', '02 사명 — 본문', '사명의 뜻(SHIELD·US·LAB)을 설명하는 문단입니다. 빈 줄로 문단을 나누고 **굵게** 를 씁니다.', 60),
  ('about.message_title', '대표이사 인사말', 'text', '대표이사 인사말', '제목', '', 70),
  ('about.message_body', '두꺼운 보고서를 다 읽고도 다음 주 월요일 아침에 무엇부터 손대야 할지 모르겠다면, 저는 그것을 **컨설팅의 실패**라고 봅니다.

쉴더스랩은 그 지점에서 출발했습니다. 취약점 목록을 넘기는 데서 멈추면 담당자의 다음 주는 어제와 똑같기 때문입니다. 저희는 발견을 규제 조항과 담당 조직의 작업 단위로 옮기고, 왜 그 순서여야 하는지를 옆에 적습니다. 조치를 다시 확인하는 데까지가 계약 범위입니다.

**할 수 없는 일을 할 수 있다고 말씀드리지 않습니다.** 법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위도 있습니다. 그 경계는 이 홈페이지에 숨김 없이 적어 두었습니다. **확인하지 않은 것을 확인했다고 쓰는 일도 없습니다.** 재현되지 않은 취약점은 보고서에 올라가지 않습니다.

방법론과 산출물 규격을 계약 전에 공개하는 것도 같은 이유에서입니다. 저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 하니까요. 어디부터 봐야 할지 모르시겠다면 그 이야기부터 꺼내 주셔도 됩니다. 범위를 정하는 일에서부터 시작하겠습니다.', 'rich', '대표이사 인사말', '본문', '빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.', 80),
  ('about.message_role', '쉴더스랩 대표이사', 'text', '대표이사 인사말', '서명 — 직함', '', 90),
  ('about.message_name', '이성훈', 'text', '대표이사 인사말', '서명 — 성명', '푸터의 ‘대표자’ 표기와는 별개입니다. 그쪽은 [법인 정보]의 대표자명을 씁니다.', 100),
  ('services.hero_title', '보고서가 두 개면
우선순위도 두 개입니다', 'text', '서비스', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 110),
  ('services.hero_lead', '관리체계는 A업체, 기술진단은 B업체. 이렇게 갈라 맡기면 담당자 책상 위에 위험도 기준이 서로 다른 보고서 두 권이 놓입니다. 어느 쪽 “높음”을 먼저 잡아야 하는지는 어느 쪽에도 적혀 있지 않습니다. 여섯 영역의 발견을 같은 등급 정의로 판정해 우선순위 목록 하나로 묶는 이유입니다.', 'text', '서비스', '상단 소개 문단', '서비스 목록 위에 놓이는 한 문단입니다.', 120),
  ('brand.name_summary', 'shield us, 우리를 지킨다. 이어 읽으면 쉴더스가 되고, 여기에 연구를 뜻하는 LAB이 붙었습니다. 로고의 실드와 그 안의 각인도 같은 뜻에서 나왔습니다.', 'text', '브랜드 · CI', '사명의 뜻 (요약)', '/brand/ 맨 위에 놓이는 요약입니다. 자세한 설명은 [회사소개]의 ‘02 사명’ 블록에 있습니다.', 130),
  ('footer.blurb', 'ISMS-P 인증 대응과 기술 진단을 한 계약 안에서 수행하는 정보보호 컨설팅 회사입니다. 발견에는 재현 절차를, 종료에는 재점검을 붙입니다.', 'text', '푸터', '푸터 소개 문단', '모든 페이지 하단에 공통으로 나옵니다.', 140),
  ('company.legal_name', '', 'text', '법인 정보', '등기 상호', '예: 주식회사 쉴더스랩. 비워두면 ‘쉴더스랩’으로 표시됩니다.', 150),
  ('company.ceo', '이성훈', 'text', '법인 정보', '대표자명', '푸터 사업자 정보에 표시됩니다.', 160),
  ('company.biz_no', '', 'text', '법인 정보', '사업자등록번호', '예: 000-00-00000', 170),
  ('company.addr', '', 'text', '법인 정보', '사업장 주소', '', 180),
  ('company.tel', '', 'text', '법인 정보', '대표번호', '', 190),
  ('company.fax', '', 'text', '법인 정보', '팩스', '', 200),
  ('company.privacy_officer', '', 'text', '법인 정보', '개인정보 보호책임자', '개인정보처리방침이 이 값을 참조합니다. 대외 홍보 전에 채워야 고지 요건이 완성됩니다.', 210)
on conflict (key) do update set
  kind       = excluded.kind,
  section    = excluded.section,
  label      = excluded.label,
  hint       = excluded.hint,
  sort_order = excluded.sort_order;
-- ↑ value 는 의도적으로 제외했다. 마이그레이션을 다시 돌려도 오너가 고친 문구가 살아남는다.

-- 확인: 블록 수가 아래와 같아야 한다.
-- select count(*) from public.sl_content;   -- => 21
