-- ════════════════════════════════════════════════════════════════════════════
-- 0003_shilderslab_hardening.sql — 라이브 감사(2026-07-30) 후속 보강
--   대상 프로젝트: nrdapzgtibbusvoaceuh
--
--   1) 공개 RPC 서버측 검증 보강 — 이메일·연락처 길이(프런트 maxlength 는 우회 가능)
--   2) 남용 방어 2차 계층 — IP 기준 레이트리밋은 X-Forwarded-For 위조로 무력화될 수 있으므로
--      IP 와 무관한 전역 시간당 상한을 추가한다(대량 자동 제출 차단).
--   3) 개인정보 자동 파기 — 처리방침에 고지한 보유기간(문의 1년 / 지원 6개월)을 실제로 이행하는 함수.
--      기존 sl_audit_purge(로그)와 함께 sl_purge_all() 로 묶는다.
--   4) 보유기간 자동 실행 스케줄(pg_cron) — 확장을 쓸 수 없는 환경이면 조용히 건너뛰고 안내만 남긴다.
--   5) sl_set_updated_at() search_path 고정(다른 함수와 일관성).
--
--   재실행 안전(idempotent). 0001 적용 이후에 실행할 것.
-- ════════════════════════════════════════════════════════════════════════════

-- ─────────────── 5) 트리거 함수 search_path 고정 ───────────────
create or replace function public.sl_set_updated_at()
returns trigger language plpgsql set search_path = public as $$
begin
  new.updated_at := now();
  return new;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 1)+2) 문의 제출 RPC 재정의 — 길이 검증 + 전역 상한
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_submit_inquiry(
  p_company text, p_name text, p_email text, p_phone text,
  p_service text, p_message text, p_consent boolean
) returns uuid
language plpgsql security definer set search_path = public as $$
declare v_ip text; v_id uuid; v_recent int; v_global int;
begin
  if p_consent is not true then
    raise exception '개인정보 수집·이용 동의가 필요합니다.' using errcode = '22023';
  end if;
  if coalesce(trim(p_company),'') = '' or coalesce(trim(p_name),'') = ''
     or coalesce(trim(p_message),'') = '' then
    raise exception '필수 항목이 비어 있습니다.' using errcode = '22023';
  end if;
  if coalesce(trim(p_email),'') !~ '^[^@[:space:]]+@[^@[:space:].]+\.[^@[:space:]]+$' then
    raise exception '이메일 형식이 올바르지 않습니다.' using errcode = '22023';
  end if;
  if char_length(p_message) > 4000 or char_length(p_company) > 80
     or char_length(p_name) > 40 or char_length(coalesce(p_phone,'')) > 30
     or char_length(coalesce(p_service,'')) > 80
     or char_length(coalesce(p_email,'')) > 120 then
    raise exception '입력 길이가 허용 범위를 초과했습니다.' using errcode = '22023';
  end if;

  v_ip := public._sl_client_ip();

  -- (a) IP 기준: 시간당 5건
  select count(*) into v_recent
    from public.sl_inquiries
   where ip is not distinct from v_ip
     and created_at > now() - interval '1 hour';
  if v_recent >= 5 then
    raise exception 'too many requests — 잠시 후 다시 시도해 주세요.' using errcode = '54000';
  end if;

  -- (b) 전역 기준: IP 위조로 (a)를 우회하는 대량 제출 차단. 정상 트래픽에는 도달하지 않는 값.
  select count(*) into v_global
    from public.sl_inquiries
   where created_at > now() - interval '1 hour';
  if v_global >= 60 then
    raise exception 'too many requests — 접수량이 일시적으로 많습니다. 잠시 후 다시 시도해 주세요.'
      using errcode = '54000';
  end if;

  insert into public.sl_inquiries(company, name, email, phone, service, message, ip, user_agent)
  values (trim(p_company), trim(p_name), lower(trim(p_email)), coalesce(trim(p_phone),''),
          coalesce(trim(p_service),''), trim(p_message), v_ip, public._sl_user_agent())
  returning id into v_id;

  insert into public.sl_audit(kind, action, entity, entity_id, ip, user_agent, detail)
  values ('submit', 'inquiry_created', 'sl_inquiries', v_id::text, v_ip, public._sl_user_agent(),
          jsonb_build_object('service', coalesce(trim(p_service),'')));
  return v_id;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 1)+2) 채용 지원 RPC 재정의 — 길이 검증 + 전역 상한
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_apply(
  p_name text, p_email text, p_phone text, p_position text,
  p_summary text, p_link text, p_consent boolean
) returns uuid
language plpgsql security definer set search_path = public as $$
declare v_ip text; v_id uuid; v_recent int; v_global int; v_link text;
begin
  if p_consent is not true then
    raise exception '개인정보 수집·이용 동의가 필요합니다.' using errcode = '22023';
  end if;
  if coalesce(trim(p_name),'') = '' or coalesce(trim(p_summary),'') = '' then
    raise exception '필수 항목이 비어 있습니다.' using errcode = '22023';
  end if;
  if coalesce(trim(p_email),'') !~ '^[^@[:space:]]+@[^@[:space:].]+\.[^@[:space:]]+$' then
    raise exception '이메일 형식이 올바르지 않습니다.' using errcode = '22023';
  end if;
  if char_length(p_summary) > 3000 or char_length(p_name) > 40
     or char_length(coalesce(p_position,'')) > 80 or char_length(coalesce(p_link,'')) > 300
     or char_length(coalesce(p_email,'')) > 120 or char_length(coalesce(p_phone,'')) > 30 then
    raise exception '입력 길이가 허용 범위를 초과했습니다.' using errcode = '22023';
  end if;

  v_link := coalesce(trim(p_link), '');
  if v_link <> '' and v_link !~* '^https?://' then
    raise exception '링크는 http(s) 주소만 입력할 수 있습니다.' using errcode = '22023';
  end if;

  v_ip := public._sl_client_ip();

  select count(*) into v_recent
    from public.sl_applications
   where ip is not distinct from v_ip
     and created_at > now() - interval '1 hour';
  if v_recent >= 3 then
    raise exception 'too many requests — 잠시 후 다시 시도해 주세요.' using errcode = '54000';
  end if;

  select count(*) into v_global
    from public.sl_applications
   where created_at > now() - interval '1 hour';
  if v_global >= 40 then
    raise exception 'too many requests — 접수량이 일시적으로 많습니다. 잠시 후 다시 시도해 주세요.'
      using errcode = '54000';
  end if;

  insert into public.sl_applications(name, email, phone, position, summary, link, ip, user_agent)
  values (trim(p_name), lower(trim(p_email)), coalesce(trim(p_phone),''),
          coalesce(trim(p_position),''), trim(p_summary), v_link, v_ip, public._sl_user_agent())
  returning id into v_id;

  insert into public.sl_audit(kind, action, entity, entity_id, ip, user_agent, detail)
  values ('submit', 'application_created', 'sl_applications', v_id::text, v_ip, public._sl_user_agent(),
          jsonb_build_object('position', coalesce(trim(p_position),'')));
  return v_id;
end $$;

-- 권한 재부여(create or replace 는 기존 권한을 유지하지만 명시적으로 고정)
revoke all on function public.sl_submit_inquiry(text,text,text,text,text,text,boolean) from public;
grant  execute on function public.sl_submit_inquiry(text,text,text,text,text,text,boolean) to anon, authenticated;
revoke all on function public.sl_apply(text,text,text,text,text,text,boolean) from public;
grant  execute on function public.sl_apply(text,text,text,text,text,text,boolean) to anon, authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 3) 개인정보 보유기간 이행 — 처리방침 고지값과 동일하게 파기
--    · 문의  : 접수 후 1년   (방침: 문의 처리 완료 후 1년)
--    · 지원서: 접수 후 6개월 (방침: 전형 종료 후 6개월 / 상시 지원은 접수일 기준 6개월)
--    보존이 필요한 건은 관리자가 상태를 done 으로 두고 별도 보관하는 것이 아니라,
--    기간이 지나면 예외 없이 파기한다(최소보관 원칙).
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_pii_purge() returns void
language sql security definer set search_path = public as $$
  with a as (
    delete from public.sl_inquiries
     where created_at < now() - interval '1 year' returning 1
  ), b as (
    delete from public.sl_applications
     where created_at < now() - interval '6 months' returning 1
  )
  select null::void;
$$;

-- 로그 + PII 를 한 번에 정리하는 진입점
create or replace function public.sl_purge_all() returns void
language sql security definer set search_path = public as $$
  select public.sl_audit_purge();
  select public.sl_pii_purge();
$$;

revoke all on function public.sl_pii_purge() from public, anon, authenticated;
revoke all on function public.sl_purge_all() from public, anon, authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 4) 자동 실행 스케줄 — pg_cron 사용 가능하면 등록, 아니면 건너뛴다.
--    (처리방침의 "자동 삭제" 고지를 실제로 이행하기 위한 단계)
-- ════════════════════════════════════════════════════════════════════════════
do $$
begin
  begin
    create extension if not exists pg_cron;
  exception when others then
    raise notice 'pg_cron 확장을 활성화할 수 없습니다(%): 대시보드 Database → Extensions 에서 활성화 후 이 파일을 재실행하세요.', sqlerrm;
    return;
  end;

  begin
    perform cron.unschedule('sl_purge_daily');
  exception when others then
    null;  -- 기존 잡이 없으면 무시
  end;

  perform cron.schedule('sl_purge_daily', '20 3 * * *', 'select public.sl_purge_all();');
  raise notice 'sl_purge_daily 등록 완료 (매일 03:20 UTC)';
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 검증용 조회 (실행 후 확인)
--   select jobname, schedule, active from cron.job where jobname = 'sl_purge_daily';
--   select proname from pg_proc where proname in ('sl_pii_purge','sl_purge_all');
-- ════════════════════════════════════════════════════════════════════════════
