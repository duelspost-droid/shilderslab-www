-- ════════════════════════════════════════════════════════════════════════════
-- 0007_shilderslab_pw_managed_boundary.sql — 계정 탈취 잔여 경로 차단
--
--   ── 왜 (모의해킹 확증, high) ─────────────────────────────────────────
--   0006 은 "이 사이트가 만든 계정(pw_managed=true)만" 비밀번호 재설정 대상으로 삼아,
--   공유 Supabase 프로젝트(타 서비스 다수)의 남 계정을 admin 이 [연결]로 끌어와
--   탈취하는 것을 막으려 했다. 그런데 그 경계를 세우는 pw_managed 를 **오너가 임의로
--   켤 수 있었다.** sl_admin_mark_pw_managed(text) 가 authenticated 에 grant 돼 있고
--   게이트가 is_sl_owner() 뿐이라, 장악되거나 악의적인 오너 1명이 3단계로 남의 계정을 탈취한다:
--     ① sl_admin_add(victim@타서비스)  — 확인된 기존 auth 계정의 user_id 가 그대로 결속됨
--     ② sl_admin_mark_pw_managed(victim) — 그 행의 pw_managed 를 true 로 뒤집음
--     ③ Edge set_password           — sl_admin_pw_uid 가 (linked·pw_managed·not-self) 통과 → 교체
--   0006 이 정확히 막으려던 크로스테넌트 격리가 그 지점에서 뚫린다.
--
--   ── 고침 ─────────────────────────────────────────────────────────────
--   pw_managed 는 **이 사이트가 auth 계정을 방금 생성한 경우에만** 켜져야 한다.
--   그 유일한 주체는 Edge 함수(sl-admin-user)의 create 경로다. 그래서:
--     · 독립 호출 가능한 sl_admin_mark_pw_managed(text) 를 **제거**한다.
--       (authenticated 오너가 PostgREST 로 직접 부를 수 있던 벡터를 없앤다.)
--     · pw_managed 설정은 Edge 가 **service_role 로, 방금 만든 uid 에 한해** 직접 한다
--       (index.ts create 경로의 PATCH sl_admins?user_id=eq.<newId>).
--       authenticated 는 sl_admins 쓰기 정책상 is_sl_owner 여도 pw_managed 를 바꿀 수 있으나,
--       아래 트리거가 그 값 변경을 service_role 이외에는 거부한다(이중 방어).
--
--   재실행 안전(idempotent). 0006 적용 이후에 실행할 것.
-- ════════════════════════════════════════════════════════════════════════════

-- ① 위험한 RPC 제거 — 오너가 임의 계정의 pw_managed 를 켜던 경로.
drop function if exists public.sl_admin_mark_pw_managed(text);

-- ② 핵심 방어: pw_managed 는 service_role 만 바꿀 수 있다.
--   RPC 를 지워도 오너는 sl_admins 쓰기 RLS 정책(to authenticated using is_sl_owner())으로
--   테이블을 **직접 PATCH** 할 수 있다 — pw_managed=true 로도. 그래서 트리거가 실질 방어다.
--   Edge 는 service_role 로 PATCH 하므로 통과하고, authenticated(오너) 의 pw_managed 변경은 거부한다.
--   ⚠ SECURITY INVOKER(기본) 여야 한다. DEFINER 면 current_user 가 정의자(postgres)로 바뀌어
--     호출자 역할을 못 본다. INVOKER 면 PostgREST 가 SET ROLE 한 실제 역할(service_role/authenticated)이 보인다.
create or replace function public._sl_guard_pw_managed()
returns trigger language plpgsql set search_path = public, pg_temp as $$
begin
  if new.pw_managed is distinct from old.pw_managed
     and current_user <> 'service_role' then
    raise exception 'pw_managed 는 계정 생성 경로(service_role)에서만 설정할 수 있습니다.'
      using errcode = '42501';
  end if;
  return new;
end $$;

drop trigger if exists sl_admins_guard_pw_managed on public.sl_admins;
create trigger sl_admins_guard_pw_managed
  before update on public.sl_admins
  for each row execute function public._sl_guard_pw_managed();

-- ════════════════════════════════════════════════════════════════════════════
-- 적용 후 확인
--   -- ① RPC 가 사라졌는지 (0행)
--   select proname from pg_proc where proname = 'sl_admin_mark_pw_managed';
--   -- ② 트리거가 붙었는지 (1행)
--   select tgname from pg_trigger where tgname = 'sl_admins_guard_pw_managed';
--   -- ③ (오너 세션) pw_managed 를 authenticated 로 켜려 하면 42501 이어야 한다:
--   --    update public.sl_admins set pw_managed=true where email='...';  → 예외
-- ════════════════════════════════════════════════════════════════════════════
