#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`supabase/migrations/0005_shilderslab_content.sql` 을 생성한다.

시드 값을 손으로 SQL 에 옮겨 적지 않는다 — `content_blocks.py` 의 default 와 갈라지는 순간
관리자 화면에 뜨는 문구와 실제 페이지 문구가 달라지기 때문이다. 이 스크립트가 유일한 경로다.

사용: python3 tools/gen-content-seed.py
"""
import os, sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
from content_blocks import BLOCKS  # noqa: E402

OUT = os.path.join(ROOT, "supabase", "migrations", "0005_shilderslab_content.sql")


def q(s):
    """SQL 문자열 리터럴. 작은따옴표만 이스케이프하면 된다(달러 인용은 쓰지 않는다)."""
    return "'" + str(s).replace("'", "''") + "'"


SCHEMA = """-- ══════════════════════════════════════════════════════════════════════
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
"""

TAIL = """on conflict (key) do update set
  kind       = excluded.kind,
  section    = excluded.section,
  label      = excluded.label,
  hint       = excluded.hint,
  sort_order = excluded.sort_order;
-- ↑ value 는 의도적으로 제외했다. 마이그레이션을 다시 돌려도 오너가 고친 문구가 살아남는다.

-- 확인: 블록 수가 아래와 같아야 한다.
-- select count(*) from public.sl_content;   -- => {n}
"""


def main():
    rows = []
    for i, b in enumerate(BLOCKS):
        rows.append("  (" + ", ".join([
            q(b["key"]), q(b["default"]), q(b["kind"]),
            q(b["section"]), q(b["label"]), q(b["hint"]), str((i + 1) * 10),
        ]) + ")")
    sql = SCHEMA + ",\n".join(rows) + "\n" + TAIL.replace("{n}", str(len(BLOCKS)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(sql)
    print(f"  ✓ {os.path.relpath(OUT, ROOT)}  블록 {len(BLOCKS)}개 · {len(sql):,}B")
    secs = []
    for b in BLOCKS:
        if b["section"] not in secs:
            secs.append(b["section"])
    for s in secs:
        n = sum(1 for b in BLOCKS if b["section"] == s)
        print(f"      {s} {n}개")


if __name__ == "__main__":
    main()
