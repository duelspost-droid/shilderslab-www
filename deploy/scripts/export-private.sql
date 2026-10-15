-- ═══════════════════════════════════════════════════════════════════════════
-- [오너 실행] 비공개 데이터 내보내기 — Supabase 대시보드 SQL 편집기용.   (HANDOFF 13항 ②)
--
-- Docker·DB 비밀번호 없이 쓸 수 있는 export-from-supabase.sh 의 대안이다.
--   1) 대시보드 → SQL Editor 에 이 파일 전체를 붙여 넣고 Run
--   2) 결과(dump 한 칸) → Export → Download CSV
--   3) python3 deploy/scripts/convert-dashboard-dump.py <받은 CSV>   → deploy/export/ 에 파일 3개
--   4) 새 서버: bash scripts/import-to-server.sh export/  → bash scripts/set-admin-password.sh <이메일>
--
-- 🔑 비밀번호 해시는 꺼내지 않는다 — 관리자는 새 서버에서 비밀번호를 새로 정한다(4번).
-- 🔴 결과에 개인정보(문의·지원자 이름·이메일·전화, 접속 IP)가 들어 있다. 레포 밖에 두고 이관 후 지운다.
-- 공유 프로젝트이므로 로그인 계정은 이 사이트 관리자로 결속된 계정만 꺼낸다(다른 서비스 사용자 제외).
-- 읽기만 한다(select 하나).
-- ═══════════════════════════════════════════════════════════════════════════
select json_build_object(
  'format', 'sl-private-dump/1',
  'generated_at', now(),
  'server_version', current_setting('server_version'),
  'tables', json_build_object(
    'sl_admins',       (select coalesce(json_agg(r order by r.created_at), '[]'::json) from public.sl_admins r),
    'sl_inquiries',    (select coalesce(json_agg(r order by r.created_at), '[]'::json) from public.sl_inquiries r),
    'sl_applications', (select coalesce(json_agg(r order by r.created_at), '[]'::json) from public.sl_applications r),
    'sl_audit',        (select coalesce(json_agg(r order by r.id), '[]'::json) from public.sl_audit r),
    'sl_content',      (select coalesce(json_agg(r order by r.key), '[]'::json) from public.sl_content r),
    'sl_insights',     (select coalesce(json_agg(r order by r.created_at), '[]'::json) from public.sl_insights r),
    'sl_jobs',         (select coalesce(json_agg(r order by r.created_at), '[]'::json) from public.sl_jobs r),
    'sl_settings',     (select coalesce(json_agg(r order by r.key), '[]'::json) from public.sl_settings r)
  ),
  'auth_users', (select coalesce(json_agg(json_build_array(u.id::text, u.aud, u.role, u.email,
       u.email_confirmed_at::text, u.last_sign_in_at::text, u.raw_app_meta_data::text, u.raw_user_meta_data::text,
       u.created_at::text, u.updated_at::text) order by u.created_at), '[]'::json)
     from auth.users u where u.id in (select user_id from public.sl_admins where user_id is not null)),
  'auth_identities', (select coalesce(json_agg(json_build_array(i.id::text, i.user_id::text, i.identity_data::text,
       i.provider, i.provider_id, i.last_sign_in_at::text, i.created_at::text, i.updated_at::text) order by i.created_at), '[]'::json)
     from auth.identities i where i.user_id in (select user_id from public.sl_admins where user_id is not null))
)::text as dump;
