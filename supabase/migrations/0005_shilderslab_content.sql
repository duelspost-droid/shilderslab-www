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
  ('about.hero_lead', '쉴더스랩(SHIELDUS LAB)은 정보보호 컨설팅 회사입니다. ISMS-P 인증 대응과 모의해킹·취약점 진단을 한 계약 안에서 수행하고, 조치를 확인하는 재점검까지를 과업 범위로 봅니다.', 'text', '회사소개', '상단 소개 문단', '제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.', 20),
  ('about.view_title', '발견마다 담당자와
순서를 붙입니다', 'text', '회사소개', '01 관점 — 제목', '줄바꿈이 그대로 반영됩니다.', 30),
  ('about.view_body', '진단을 받은 다음 해에 같은 항목이 다시 지적되는 일이 있습니다. 발견 사항이 담당 조직의 작업 단위로 옮겨지지 않고, 조치 결과를 확인하는 절차가 **계약 범위에 없을 때** 그렇습니다.

쉴더스랩은 발견을 규제 항목과 시스템 담당자의 작업 단위에 함께 연결합니다. 조치가 적용됐는지 재점검으로 확인한 뒤 과업을 닫습니다. “무엇이 취약한가”에서 멈추지 않습니다. “지금은 안전한가”에 답하고 끝냅니다.', 'rich', '회사소개', '01 관점 — 본문', '빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.', 40),
  ('about.name_title', '이름이 곧
하는 일입니다', 'text', '회사소개', '02 사명 — 제목', '줄바꿈이 그대로 반영됩니다.', 50),
  ('about.name_body', '**SHIELD** 지킨다 · **US** 우리를 · **LAB** 연구한다. 사명은 이 세 낱말을 그대로 이어 붙인 것입니다. 국문 **쉴더스랩**은 ‘shield us’를 이어 읽은 음차이므로, 영문과 국문은 다른 이름이 아니라 같은 말입니다.

**US** 는 고객사를 가리키는 말이면서 저희를 포함하는 말입니다. 보안은 지켜 주는 쪽과 지킴받는 쪽으로 나뉘지 않습니다. 같은 위협 아래 있는 사람들이 같은 편에서 막는 일입니다. 그래서 저희는 진단을 넘겨주고 끝내지 않고, 조치가 닫힐 때까지 함께 봅니다.

**LAB** 은 연구를 뜻합니다. 저희에게 연구는 방법을 공개하는 일입니다. 진단 절차와 위험도 등급 정의, 보고서 구성을 계약 전에 공개하고, 발견마다 재현 절차를 붙입니다. 다시 확인할 수 없는 주장은 연구가 아니라고 봅니다.', 'rich', '회사소개', '02 사명 — 본문', '사명의 뜻(SHIELD·US·LAB)을 설명하는 문단입니다. 빈 줄로 문단을 나누고 **굵게** 를 씁니다.', 60),
  ('about.message_title', '대표이사 인사말', 'text', '대표이사 인사말', '제목', '', 70),
  ('about.message_body', '두꺼운 보고서를 받고도 다음 주 월요일에 무엇부터 손댈지 정하지 못하는 상황이 있습니다. 저는 그 상태를 **컨설팅의 실패**로 봅니다.

쉴더스랩은 그 지점에서 시작했습니다. 취약점을 찾아내는 일만으로는 변별력이 되기 어렵습니다. 발견을 규제 조항과 담당자의 작업 단위로 옮기고, 우선순위에 근거를 붙이고, 조치를 다시 확인한 뒤 과업을 닫습니다. 여기까지를 계약 범위에 넣습니다.

저희가 스스로에게 두는 규칙은 두 가지입니다. 첫째, **할 수 없는 일을 할 수 있다고 말하지 않습니다.** 법령상 수행 자격이 제한된 과업이 있고, 저희가 보유하지 않은 지위가 있습니다. 그 경계는 홈페이지에 그대로 적어 두었습니다. 둘째, **확인하지 않은 것을 확인했다고 쓰지 않습니다.** 재현되지 않은 취약점은 보고서에 올리지 않습니다.

그래서 방법론과 산출물 규격을 계약 전에 공개합니다. 저희 판정이 맞는지 고객사가 직접 되짚어 볼 수 있어야 한다고 보기 때문입니다. 함께 볼 범위부터 편하게 말씀해 주시면, 거기서부터 시작하겠습니다.', 'rich', '대표이사 인사말', '본문', '빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.', 80),
  ('about.message_role', '쉴더스랩 대표이사', 'text', '대표이사 인사말', '서명 — 직함', '', 90),
  ('about.message_name', '이성훈', 'text', '대표이사 인사말', '서명 — 성명', '푸터의 ‘대표자’ 표기와는 별개입니다. 그쪽은 [법인 정보]의 대표자명을 씁니다.', 100),
  ('services.hero_title', '여섯 개 영역을
같은 위험도 표로 봅니다', 'text', '서비스', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 110),
  ('services.hero_lead', '관리체계와 기술진단을 다른 업체가 맡으면 보고서 두 개의 위험도 기준이 서로 다릅니다. 쉴더스랩은 여섯 영역의 발견을 같은 등급 정의로 판정하고, 하나의 우선순위 목록으로 묶습니다.', 'text', '서비스', '상단 소개 문단', '서비스 목록 위에 놓이는 한 문단입니다.', 120),
  ('brand.name_summary', 'SHIELD 지킨다 · US 우리를 · LAB 연구한다 — 우리를 지키는 방법을 연구한다는 뜻입니다. 국문 쉴더스랩은 ‘shield us’를 이어 읽은 음차로, 영문과 국문은 같은 말입니다. 로고의 실드와 그 안의 각인도 이 뜻에서 나왔습니다.', 'text', '브랜드 · CI', '사명의 뜻 (요약)', '/brand/ 맨 위에 놓이는 요약입니다. 자세한 설명은 [회사소개]의 ‘02 사명’ 블록에 있습니다.', 130),
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
