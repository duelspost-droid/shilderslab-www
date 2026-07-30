-- ════════════════════════════════════════════════════════════════════════════
-- 0001_shilderslab_core.sql — 쉴더스랩(shilderslab.com) 백엔드 코어
--   ⚠ 공유 프로젝트 전제 조건
--     이 Supabase 프로젝트는 다른 서비스와 공유한다. 즉 로그인 사용자가 곧 이 사이트의 관리자는 아니다.
--     따라서 "authenticated = 관리자" 가정을 쓰지 않고, 전 테이블을
--     sl_admins 화이트리스트(is_sl_admin())로 게이트한다.
--
--   설계 원칙
--     1) 공개 읽기는 published 행만. 미게시·PII 테이블은 anon 정책 자체를 만들지 않는다.
--     2 )문의·지원 등 사용자 입력은 INSERT 정책 없이 SECURITY DEFINER RPC로만 적재
--        (검증 + IP 기준 레이트리밋을 서버측에서 강제).
--     3) 감사 로그는 RPC로만 적재 → 클라이언트가 임의 로그를 심을 수 없다.
--     4) 재실행 안전(idempotent): if not exists / drop policy if exists / create or replace.
--
--   적용: Supabase 대시보드 SQL Editor에 붙여넣고 1회 실행.
-- ════════════════════════════════════════════════════════════════════════════

-- ─────────────────────────── 공통 트리거 함수 ───────────────────────────
create or replace function public.sl_set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;

-- ═══════════════════ 1) 관리자 화이트리스트 ═══════════════════
create table if not exists public.sl_admins (
  email       text primary key,
  role        text not null default 'admin' check (role in ('admin','editor')),
  note        text,
  created_at  timestamptz not null default now()
);
alter table public.sl_admins enable row level security;

-- SECURITY DEFINER → sl_admins RLS를 우회해 조회(정책 자기참조 재귀 방지)
create or replace function public.is_sl_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.sl_admins a
     where lower(a.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

drop policy if exists sl_admins_read on public.sl_admins;
create policy sl_admins_read on public.sl_admins for select to authenticated
  using (public.is_sl_admin());
-- 쓰기 정책 없음 → 관리자 추가/삭제는 SQL(또는 service_role)로만.

-- 최초 관리자 등록 — 공개 저장소이므로 실제 주소를 파일에 남기지 않는다.
-- 아래 한 줄의 <관리자 이메일> 을 바꿔 SQL Editor 에서 직접 실행할 것.
-- 해당 주소는 Authentication → Users 에 로그인 계정으로도 존재해야 권한이 붙는다.
--   insert into public.sl_admins(email, role, note)
--   values ('<관리자 이메일>', 'admin', '쉴더스랩 관리자') on conflict (email) do nothing;

-- ═══════════════════ 2) 사이트 설정 (kv) ═══════════════════
create table if not exists public.sl_settings (
  key         text primary key,
  value       jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);
alter table public.sl_settings enable row level security;

drop policy if exists sl_settings_read  on public.sl_settings;
drop policy if exists sl_settings_write on public.sl_settings;
create policy sl_settings_read  on public.sl_settings for select using (true);
create policy sl_settings_write on public.sl_settings for all to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());

-- ═══════════════════ 3) 인사이트 (CMS) ═══════════════════
create table if not exists public.sl_insights (
  id            uuid primary key default gen_random_uuid(),
  slug          text not null unique,
  category      text not null default '인사이트',
  title         text not null,
  summary       text not null default '',
  body          text not null default '',
  author        text not null default '',
  published     boolean not null default false,
  published_at  date not null default current_date,
  sort_order    int not null default 0,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  constraint sl_insights_slug_fmt check (slug ~ '^[a-z0-9]([a-z0-9-]{0,78}[a-z0-9])?$'),
  constraint sl_insights_title_len check (char_length(title) between 1 and 200)
);
create index if not exists sl_insights_pub_idx on public.sl_insights(published, published_at desc);
alter table public.sl_insights enable row level security;

drop policy if exists sl_insights_read_pub on public.sl_insights;
drop policy if exists sl_insights_read_all on public.sl_insights;
drop policy if exists sl_insights_write    on public.sl_insights;
create policy sl_insights_read_pub on public.sl_insights for select using (published = true);
create policy sl_insights_read_all on public.sl_insights for select to authenticated
  using (public.is_sl_admin());
create policy sl_insights_write    on public.sl_insights for all to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());

-- ═══════════════════ 4) 채용 공고 ═══════════════════
create table if not exists public.sl_jobs (
  id               uuid primary key default gen_random_uuid(),
  title            text not null,
  team             text not null default '',
  employment_type  text not null default '정규직',
  location         text not null default '',
  summary          text not null default '',
  body             text not null default '',
  closes_at        date,
  published        boolean not null default false,
  sort_order       int not null default 0,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  constraint sl_jobs_title_len check (char_length(title) between 1 and 160)
);
create index if not exists sl_jobs_pub_idx on public.sl_jobs(published, sort_order);
alter table public.sl_jobs enable row level security;

drop policy if exists sl_jobs_read_pub on public.sl_jobs;
drop policy if exists sl_jobs_read_all on public.sl_jobs;
drop policy if exists sl_jobs_write    on public.sl_jobs;
create policy sl_jobs_read_pub on public.sl_jobs for select using (published = true);
create policy sl_jobs_read_all on public.sl_jobs for select to authenticated
  using (public.is_sl_admin());
create policy sl_jobs_write    on public.sl_jobs for all to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());

-- ═══════════════════ 5) 문의 · 견적 (PII) ═══════════════════
create table if not exists public.sl_inquiries (
  id          uuid primary key default gen_random_uuid(),
  company     text not null,
  name        text not null,
  email       text not null,
  phone       text not null default '',
  service     text not null default '',
  message     text not null,
  status      text not null default 'new' check (status in ('new','doing','done','drop')),
  admin_note  text not null default '',
  ip          text,
  user_agent  text,
  consent_at  timestamptz not null default now(),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists sl_inq_created_idx on public.sl_inquiries(created_at desc);
create index if not exists sl_inq_status_idx  on public.sl_inquiries(status, created_at desc);
create index if not exists sl_inq_ip_idx      on public.sl_inquiries(ip, created_at desc);
alter table public.sl_inquiries enable row level security;

-- 익명 정책 없음(조회·삽입 모두 차단). 관리자만 열람/상태 변경, 삽입은 RPC 전용.
drop policy if exists sl_inq_admin_read   on public.sl_inquiries;
drop policy if exists sl_inq_admin_update on public.sl_inquiries;
drop policy if exists sl_inq_admin_delete on public.sl_inquiries;
create policy sl_inq_admin_read   on public.sl_inquiries for select to authenticated
  using (public.is_sl_admin());
create policy sl_inq_admin_update on public.sl_inquiries for update to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());
create policy sl_inq_admin_delete on public.sl_inquiries for delete to authenticated
  using (public.is_sl_admin());

-- ═══════════════════ 6) 채용 지원 (PII) ═══════════════════
create table if not exists public.sl_applications (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  email       text not null,
  phone       text not null default '',
  position    text not null default '',
  summary     text not null default '',
  link        text not null default '',
  status      text not null default 'new' check (status in ('new','doing','done','drop')),
  admin_note  text not null default '',
  ip          text,
  user_agent  text,
  consent_at  timestamptz not null default now(),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists sl_app_created_idx on public.sl_applications(created_at desc);
create index if not exists sl_app_status_idx  on public.sl_applications(status, created_at desc);
create index if not exists sl_app_ip_idx      on public.sl_applications(ip, created_at desc);
alter table public.sl_applications enable row level security;

drop policy if exists sl_app_admin_read   on public.sl_applications;
drop policy if exists sl_app_admin_update on public.sl_applications;
drop policy if exists sl_app_admin_delete on public.sl_applications;
create policy sl_app_admin_read   on public.sl_applications for select to authenticated
  using (public.is_sl_admin());
create policy sl_app_admin_update on public.sl_applications for update to authenticated
  using (public.is_sl_admin()) with check (public.is_sl_admin());
create policy sl_app_admin_delete on public.sl_applications for delete to authenticated
  using (public.is_sl_admin());

-- ═══════════════════ 7) 감사 · 방문 로그 ═══════════════════
create table if not exists public.sl_audit (
  id          bigint generated always as identity primary key,
  kind        text not null default 'admin',   -- admin | visit | submit
  actor       uuid,
  actor_email text,
  action      text not null,
  entity      text,
  entity_id   text,
  detail      jsonb not null default '{}'::jsonb,
  ip          text,
  user_agent  text,
  created_at  timestamptz not null default now()
);
create index if not exists sl_audit_created_idx on public.sl_audit(created_at desc);
create index if not exists sl_audit_kind_idx    on public.sl_audit(kind, created_at desc);
create index if not exists sl_audit_entity_idx  on public.sl_audit(entity, created_at desc);
alter table public.sl_audit enable row level security;

drop policy if exists sl_audit_admin_read on public.sl_audit;
create policy sl_audit_admin_read on public.sl_audit for select to authenticated
  using (public.is_sl_admin());
-- INSERT/UPDATE/DELETE 정책 없음 → 아래 RPC로만 적재.

-- ─────────────────────────── updated_at 트리거 ───────────────────────────
do $$
declare t text;
begin
  foreach t in array array['sl_settings','sl_insights','sl_jobs','sl_inquiries','sl_applications']
  loop
    execute format('drop trigger if exists trg_%1$s_updated on public.%1$s', t);
    execute format('create trigger trg_%1$s_updated before update on public.%1$s
                    for each row execute function public.sl_set_updated_at()', t);
  end loop;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 요청 컨텍스트 추출 (내부 전용)
--   ⚠ x-forwarded-for 최좌측 값은 신뢰 프록시가 재작성하지 않으면 위조 가능하다.
--     레이트리밋·통계 보조용으로만 쓰고, 보안 판단의 단독 근거로 삼지 않는다.
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public._sl_client_ip() returns text
language sql stable set search_path = public as $$
  select nullif(trim(split_part(
    coalesce(current_setting('request.headers', true), '{}')::json ->> 'x-forwarded-for', ',', 1)), '');
$$;

create or replace function public._sl_user_agent() returns text
language sql stable set search_path = public as $$
  select left(coalesce(current_setting('request.headers', true), '{}')::json ->> 'user-agent', 400);
$$;

-- ════════════════════════════════════════════════════════════════════════════
-- 공개 제출 RPC — 문의 · 견적
--   검증: 동의 필수 / 이메일 형식 / 길이 상한 / IP 기준 시간당 5건
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_submit_inquiry(
  p_company text, p_name text, p_email text, p_phone text,
  p_service text, p_message text, p_consent boolean
) returns uuid
language plpgsql security definer set search_path = public as $$
declare v_ip text; v_id uuid; v_recent int;
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
     or char_length(coalesce(p_service,'')) > 80 then
    raise exception '입력 길이가 허용 범위를 초과했습니다.' using errcode = '22023';
  end if;

  v_ip := public._sl_client_ip();
  select count(*) into v_recent
    from public.sl_inquiries
   where ip is not distinct from v_ip
     and created_at > now() - interval '1 hour';
  if v_recent >= 5 then
    raise exception 'too many requests — 잠시 후 다시 시도해 주세요.' using errcode = '54000';
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
-- 공개 제출 RPC — 채용 지원
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_apply(
  p_name text, p_email text, p_phone text, p_position text,
  p_summary text, p_link text, p_consent boolean
) returns uuid
language plpgsql security definer set search_path = public as $$
declare v_ip text; v_id uuid; v_recent int; v_link text;
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
     or char_length(coalesce(p_position,'')) > 80 or char_length(coalesce(p_link,'')) > 300 then
    raise exception '입력 길이가 허용 범위를 초과했습니다.' using errcode = '22023';
  end if;

  -- 링크는 http/https 만 저장(javascript: 등 차단)
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

  insert into public.sl_applications(name, email, phone, position, summary, link, ip, user_agent)
  values (trim(p_name), lower(trim(p_email)), coalesce(trim(p_phone),''),
          coalesce(trim(p_position),''), trim(p_summary), v_link, v_ip, public._sl_user_agent())
  returning id into v_id;

  insert into public.sl_audit(kind, action, entity, entity_id, ip, user_agent, detail)
  values ('submit', 'application_created', 'sl_applications', v_id::text, v_ip, public._sl_user_agent(),
          jsonb_build_object('position', coalesce(trim(p_position),'')));
  return v_id;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 방문 로깅 (익명 허용) — 경로 형식 검증 + 동일 IP·경로 10분 중복 억제
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_log_visit(p_page text default null) returns void
language plpgsql security definer set search_path = public as $$
declare v_page text; v_ip text; v_ref text;
begin
  v_page := left(coalesce(p_page, '/'), 300);
  if v_page !~ '^/[A-Za-z0-9/_.\-]*$' then v_page := '/'; end if;
  v_ip := public._sl_client_ip();
  if exists (
    select 1 from public.sl_audit
     where kind = 'visit' and entity = v_page
       and ip is not distinct from v_ip
       and created_at > now() - interval '10 minutes'
  ) then return; end if;
  v_ref := coalesce(current_setting('request.headers', true), '{}')::json ->> 'referer';
  insert into public.sl_audit(kind, action, entity, ip, user_agent, detail)
  values ('visit', 'visit', v_page, v_ip, public._sl_user_agent(),
          case when v_ref is null then '{}'::jsonb
               else jsonb_build_object('ref', left(v_ref, 300)) end);
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 관리자 행위 로깅 — 화이트리스트 계정만
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_log(
  p_action text, p_entity text default null, p_entity_id text default null,
  p_detail jsonb default '{}'::jsonb
) returns void
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'auth required'; end if;
  if not public.is_sl_admin() then raise exception 'not an authorized admin'; end if;
  if coalesce(p_action,'') = '' then raise exception 'action required'; end if;
  insert into public.sl_audit(kind, actor, actor_email, action, entity, entity_id, detail, ip, user_agent)
  values ('admin', auth.uid(), auth.jwt() ->> 'email', left(p_action, 60),
          left(p_entity, 80), left(p_entity_id, 80), coalesce(p_detail, '{}'::jsonb),
          public._sl_client_ip(), public._sl_user_agent());
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 관리자 대시보드 통계 (관리자 전용)
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_stats() returns jsonb
language plpgsql security definer set search_path = public as $$
declare v jsonb;
begin
  if not public.is_sl_admin() then raise exception 'not an authorized admin'; end if;
  select jsonb_build_object(
    'inq_new',      (select count(*) from public.sl_inquiries where status = 'new'),
    'inq_total',    (select count(*) from public.sl_inquiries),
    'inq_7d',       (select count(*) from public.sl_inquiries where created_at > now() - interval '7 days'),
    'app_new',      (select count(*) from public.sl_applications where status = 'new'),
    'app_total',    (select count(*) from public.sl_applications),
    'insight_pub',  (select count(*) from public.sl_insights where published),
    'insight_total',(select count(*) from public.sl_insights),
    'job_pub',      (select count(*) from public.sl_jobs where published),
    'visit_today',  (select count(*) from public.sl_audit
                      where kind = 'visit' and created_at > date_trunc('day', now())),
    'visit_7d',     (select count(*) from public.sl_audit
                      where kind = 'visit' and created_at > now() - interval '7 days'),
    'visit_30d',    (select count(*) from public.sl_audit
                      where kind = 'visit' and created_at > now() - interval '30 days'),
    'top_pages',    (select coalesce(jsonb_agg(t), '[]'::jsonb) from (
                      select entity as page, count(*) as n from public.sl_audit
                       where kind = 'visit' and created_at > now() - interval '30 days'
                       group by entity order by count(*) desc limit 8) t),
    'daily',        (select coalesce(jsonb_agg(d order by d->>'day'), '[]'::jsonb) from (
                      select jsonb_build_object('day', to_char(date_trunc('day', created_at), 'MM-DD'),
                                                'n', count(*)) as d
                        from public.sl_audit
                       where kind = 'visit' and created_at > now() - interval '14 days'
                       group by date_trunc('day', created_at)) s)
  ) into v;
  return v;
end $$;

-- ════════════════════════════════════════════════════════════════════════════
-- 보존 정책: 방문 90일 / 관리·제출 로그 365일 경과분 삭제
--   (pg_cron 사용 시:  select cron.schedule('sl_audit_purge_daily','20 3 * * *',
--                        $$ select public.sl_audit_purge(); $$);)
-- ════════════════════════════════════════════════════════════════════════════
create or replace function public.sl_audit_purge() returns void
language sql security definer set search_path = public as $$
  delete from public.sl_audit
   where (kind = 'visit' and created_at < now() - interval '90 days')
      or (kind in ('admin','submit') and created_at < now() - interval '365 days');
$$;

-- ─────────────────────────── 실행 권한 ───────────────────────────
revoke all on function public._sl_client_ip()  from public, anon, authenticated;
revoke all on function public._sl_user_agent() from public, anon, authenticated;
revoke all on function public.sl_audit_purge() from public, anon, authenticated;

revoke all on function public.sl_submit_inquiry(text,text,text,text,text,text,boolean) from public;
grant  execute on function public.sl_submit_inquiry(text,text,text,text,text,text,boolean) to anon, authenticated;

revoke all on function public.sl_apply(text,text,text,text,text,text,boolean) from public;
grant  execute on function public.sl_apply(text,text,text,text,text,text,boolean) to anon, authenticated;

revoke all on function public.sl_log_visit(text) from public;
grant  execute on function public.sl_log_visit(text) to anon, authenticated;

revoke all on function public.sl_log(text,text,text,jsonb) from public, anon;
grant  execute on function public.sl_log(text,text,text,jsonb) to authenticated;

revoke all on function public.sl_stats() from public, anon;
grant  execute on function public.sl_stats() to authenticated;

revoke all on function public.is_sl_admin() from public, anon;
grant  execute on function public.is_sl_admin() to authenticated;

-- ════════════════════════════════════════════════════════════════════════════
-- 완료. 시드 데이터는 0002_shilderslab_seed.sql 로 분리.
-- ════════════════════════════════════════════════════════════════════════════
