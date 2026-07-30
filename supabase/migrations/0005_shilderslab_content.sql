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
  ('about.hero_title', '보안을
검증의 문제로
다룹니다', 'text', '회사소개', '상단 큰 제목', '줄바꿈한 자리에서 실제로 줄이 바뀝니다. 3줄을 넘기지 않는 편이 좋습니다.', 10),
  ('about.hero_lead', '쉴더스랩(SHIELDUS LAB)은 2026년에 설립된 정보보호 컨설팅 조직입니다. 인증 기준을 충족시키는 관리체계 컨설팅과, 실제 공격 관점의 기술 진단을 한 팀에서 수행합니다.', 'text', '회사소개', '상단 소개 문단', '제목 아래 한 문단. 검색 결과에도 영향을 주는 문장입니다.', 20),
  ('about.view_title', '보고서는 결과가 아니라
작업 지시서입니다', 'text', '회사소개', '01 관점 — 제목', '줄바꿈이 그대로 반영됩니다.', 30),
  ('about.view_body', '많은 조직이 진단을 받고도 이듬해 같은 취약점을 다시 발견합니다. 원인은 대개 진단 역량이 아니라 **조치까지 이어지지 않는 구조**입니다. 발견 사항이 담당자의 언어로 번역되지 않고, 우선순위가 없고, 조치 결과를 확인하는 절차가 없기 때문입니다.

그래서 저희는 발견을 규제 항목과 시스템 담당자의 작업 단위에 함께 연결합니다. 그리고 조치가 실제로 적용되었는지 재점검으로 확인한 뒤 과업을 종료합니다. “무엇이 취약한가”에서 멈추지 않고 “지금은 안전한가”에 답하는 것이 기준입니다.', 'rich', '회사소개', '01 관점 — 본문', '빈 줄로 문단을 나눕니다. **굵게** 로 강조합니다.', 40),
  ('about.message_title', '대표이사 인사말', 'text', '대표이사 인사말', '제목', '', 50),
  ('about.message_body', '정보보호 컨설팅을 받아 본 담당자에게 무엇이 가장 아쉬웠는지 물으면, 대체로 같은 대답이 돌아옵니다. 보고서는 두꺼웠지만 **무엇부터 해야 할지는 알 수 없었다**는 것입니다.

쉴더스랩은 그 지점에서 시작했습니다. 취약점을 찾아내는 일은 이제 그 자체로 변별력이 되기 어렵습니다. 발견을 규제 조항과 시스템 담당자의 작업 단위로 옮겨 놓는 일, 우선순위를 근거와 함께 제시하는 일, 그리고 조치가 실제로 적용되었는지 다시 확인하고 과업을 닫는 일 — 저희는 여기까지를 컨설팅의 범위로 봅니다.

저희가 스스로에게 두는 규칙은 두 가지입니다. 첫째, **할 수 없는 일을 할 수 있다고 말하지 않습니다.** 법령상 수행 자격이 제한된 과업이 있고, 저희가 아직 보유하지 못한 지위가 있습니다. 그 경계는 홈페이지에 그대로 적어 두었습니다. 둘째, **확인하지 않은 것을 확인했다고 쓰지 않습니다.** 재현되지 않은 취약점은 보고서에 올리지 않고, 근거는 재현 절차와 함께 제시합니다.

보안은 결국 신뢰의 문제이고, 신뢰는 검증할 수 있을 때만 성립합니다. 고객사가 저희의 결론을 다시 확인할 수 있도록 방법론과 산출물 규격을 공개하는 이유입니다. 함께 볼 범위부터 편하게 말씀해 주시면, 거기서부터 시작하겠습니다.', 'rich', '대표이사 인사말', '본문', '빈 줄로 문단을 나눕니다. **굵게** 사용 가능. 경력·자격을 넣으실 때는 사실만 적어 주세요.', 60),
  ('about.message_role', '쉴더스랩 대표이사', 'text', '대표이사 인사말', '서명 — 직함', '', 70),
  ('about.message_name', '이성훈', 'text', '대표이사 인사말', '서명 — 성명', '푸터의 ‘대표자’ 표기와는 별개입니다. 그쪽은 [법인 정보]의 대표자명을 씁니다.', 80),
  ('services.hero_title', '여섯 개 영역,
하나의 기준', 'text', '서비스', '상단 큰 제목', '줄바꿈이 그대로 반영됩니다.', 90),
  ('services.hero_lead', '관리체계·기술진단·개인정보·클라우드를 서로 다른 언어로 다루면 조치가 흩어집니다. 모든 발견 사항을 같은 위험도 기준과 우선순위로 정리해 전달합니다.', 'text', '서비스', '상단 소개 문단', '서비스 목록 위에 놓이는 한 문단입니다.', 100),
  ('footer.blurb', '규제 대응과 공격자 관점의 기술 진단을 한 팀에서 수행하는 정보보호 컨설팅 조직입니다. 발견에는 재현 절차를, 종료에는 재점검을 붙입니다.', 'text', '푸터', '푸터 소개 문단', '모든 페이지 하단에 공통으로 나옵니다.', 110),
  ('company.legal_name', '', 'text', '법인 정보', '등기 상호', '예: 주식회사 쉴더스랩. 비워두면 ‘쉴더스랩’으로 표시됩니다.', 120),
  ('company.ceo', '이성훈', 'text', '법인 정보', '대표자명', '푸터 사업자 정보에 표시됩니다.', 130),
  ('company.biz_no', '', 'text', '법인 정보', '사업자등록번호', '예: 000-00-00000', 140),
  ('company.addr', '', 'text', '법인 정보', '사업장 주소', '', 150),
  ('company.tel', '', 'text', '법인 정보', '대표번호', '', 160),
  ('company.fax', '', 'text', '법인 정보', '팩스', '', 170),
  ('company.privacy_officer', '', 'text', '법인 정보', '개인정보 보호책임자', '개인정보처리방침이 이 값을 참조합니다. 대외 홍보 전에 채워야 고지 요건이 완성됩니다.', 180)
on conflict (key) do update set
  kind       = excluded.kind,
  section    = excluded.section,
  label      = excluded.label,
  hint       = excluded.hint,
  sort_order = excluded.sort_order;
-- ↑ value 는 의도적으로 제외했다. 마이그레이션을 다시 돌려도 오너가 고친 문구가 살아남는다.

-- 확인: 블록 수가 아래와 같아야 한다.
-- select count(*) from public.sl_content;   -- => 18
