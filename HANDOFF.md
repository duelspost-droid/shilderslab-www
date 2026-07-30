# HANDOFF — 쉴더스랩 웹사이트

> 이 문서가 **정본**이다. 세션이 바뀌거나 다른 PC에서 이어받을 때 이 파일을 먼저 읽는다.
> 상태·결정·남은 작업을 여기서만 관리한다.

최초 작성: 2026-07-30

---

## 1. 현재 상태

| 항목 | 상태 |
|---|---|
| 프런트 (11개 페이지) | ✅ 작성 완료 · 로컬 검증 통과(전 경로 200, 콘솔 오류 0) |
| CI 벡터 원본 | ✅ 심볼·가로/세로 락업·모노·워드마크·파비콘·OG (아웃라인 패스) |
| DB 스키마·RLS·RPC (`0001`) | ⏳ **라이브 미적용** — SQL Editor에서 1회 실행 필요 |
| 초기 콘텐츠 시드 (`0002`) | ⏳ 라이브 미적용 (0001 이후 실행) |
| 관리자 콘솔 | ✅ 작성 완료 (로그인·문의·지원·CMS·로그·설정) — DB 적용 후 동작 |
| GitHub 저장소 · Pages | ⏳ 생성·푸시 대기 |
| 도메인 (가비아 DNS) | ⏳ 레코드 등록 대기 (아래 4항) |
| 접수 알림 메일 (선택) | ⏳ `notify-inquiry` 미배포 |

로컬 경로: `/Users/hk/shilderslab-www`

---

## 2. 아키텍처 결정 (요약)

- **정적 프런트 + Supabase**: jbax-www(`/ax/`)와 동일한 방식. 빌드 도구·서버 런타임 없음 → GitHub Pages로 즉시 배포.
- **Supabase 프로젝트 공유** (`nrdapzgtibbusvoaceuh`, secuday/VulnScan/jbax-www와 동일):
  → 이 프로젝트에는 **다른 서비스의 로그인 사용자가 존재**한다. 따라서 기존 `ax_*` 테이블이 쓰던
  `for all to authenticated using (true)` 패턴은 여기서 **권한 결함**이므로 사용하지 않았고,
  전 테이블 쓰기를 `sl_admins` 화이트리스트(`is_sl_admin()`)로 게이트했다.
- **PII 테이블은 공개 정책 자체를 만들지 않음**: `sl_inquiries` / `sl_applications` 는 INSERT 정책이 없고
  `SECURITY DEFINER` RPC(`sl_submit_inquiry`, `sl_apply`)로만 적재된다. 동의 필수·이메일 형식·길이 상한·
  **IP 기준 레이트리밋**(문의 5건/시간, 지원 3건/시간)을 서버측에서 강제한다.
- **CDN 의존 제거**: supabase-js를 `assets/vendor/` 에 자체 호스팅 → CSP를 `script-src 'self'` 로 좁혔다.
- **워드마크 아웃라인**: 로고에 `<text>` 를 쓰지 않고 글리프를 패스로 변환해 임베드. 폰트 없는 환경·인쇄·커팅에서 동일 렌더.

---

## 3. 오너 조치 필요 (순서대로)

### ① DB 마이그레이션 적용 — 가장 먼저
Supabase 대시보드 → 프로젝트 `nrdapzgtibbusvoaceuh` → SQL Editor 에서 순서대로 1회 실행:

1. `supabase/migrations/0001_shilderslab_core.sql`
2. `supabase/migrations/0002_shilderslab_seed.sql`

두 파일 모두 **재실행 안전**(idempotent)하다. 적용 전에는 문의 폼이 "지금은 접수를 처리할 수 없습니다"로
안전하게 실패하고, 인사이트 영역은 "준비 중" 문구가 나온다(사이트 자체는 정상).

검증 쿼리:
```sql
select count(*) from sl_insights where published;      -- 3
select public.is_sl_admin();                            -- 관리자 계정 로그인 시 true
```

### ② 관리자 계정
`0001` 시드가 `duels@jbfg.com` 을 관리자로 등록한다. 이 계정은 **해당 Supabase 프로젝트의 `auth.users`에
이미 존재해야** 로그인이 된다(없으면 대시보드 Authentication → Users 에서 생성).
쉴더스랩 전용 주소를 쓰려면:
```sql
insert into public.sl_admins(email, role, note)
values ('본인@shilderslab.com', 'admin', '쉴더스랩 관리자') on conflict do nothing;
```
계정 자체는 Supabase Authentication → Users → Add user 로 생성한다. (비밀번호 입력은 오너가 직접)

### ③ 가비아 DNS — shilderslab.com → GitHub Pages
가비아 My가비아 → DNS 관리 → shilderslab.com → 레코드 수정에서:

| 타입 | 호스트 | 값 | TTL |
|---|---|---|---|
| A | @ | 185.199.108.153 | 3600 |
| A | @ | 185.199.109.153 | 3600 |
| A | @ | 185.199.110.153 | 3600 |
| A | @ | 185.199.111.153 | 3600 |
| CNAME | www | duelspost-droid.github.io. | 3600 |

등록 후 GitHub 저장소 → Settings → Pages → Custom domain 에 `shilderslab.com` 입력,
DNS 검증 통과 후 **Enforce HTTPS** 체크(인증서 발급까지 수십 분 소요될 수 있음).
※ 가비아 로그인은 CAPTCHA로 자동화가 불가능하므로 오너가 직접 진행해야 한다.

### ④ 법인 정보 입력 (`config.js`)
`config.js` 의 `COMPANY` 에서 빈 문자열인 항목을 채운다. **빈 값은 화면에 렌더되지 않으므로**
지금 상태로 배포해도 어색한 자리표시자가 노출되지는 않는다. 채우면 전 페이지 푸터에 자동 표시된다.

```js
legalKo: "",          // 등기 상호 (예: 주식회사 쉴더스랩)
ceo: "",              // 대표자명
bizNo: "",            // 사업자등록번호
addr: "",             // 사업장 주소
tel: "",              // 대표번호
privacyOfficer: "",   // 개인정보 보호책임자
```

> ⚠️ 개인정보처리방침(`/legal/privacy.html`)은 상호·대표자·주소·보호책임자를 **푸터 사업자 정보로 참조**하도록
> 작성되어 있다. 대외 홍보 전에 위 값을 채워야 고지 요건이 완성된다.

### ⑤ (선택) 접수 알림 메일
`supabase/functions/notify-inquiry/index.ts` 상단 주석의 3단계(함수 배포 → 시크릿 등록 → DB 웹훅 연결).
배포하지 않아도 사이트·관리자 콘솔은 정상 동작한다(관리자 대시보드에 새 문의 배지 표시).

---

## 4. 남은 개선 과제 (P1~P3)

- **P1** 실적 지표 갱신: 홈 `#why` 의 지표는 현재 **정책 기준**(24h 회신·5단계·4영역·재점검 1회)이다.
  프로젝트 이력이 쌓이면 실제 수행 건수로 교체. 없는 실적을 숫자로 만들지 않는다.
- **P1** 사업자 정보 입력(위 ④) 후 개인정보처리방침 재확인.
- **P2** 인사이트 상세 페이지의 SEO: 현재 CMS 렌더(클라이언트)라 크롤러가 본문을 늦게 본다.
  검색 유입이 중요해지면 발행 시 정적 HTML을 생성하는 방식(빌더 확장)으로 전환.
- **P2** Supabase 리전 확인 후 개인정보처리방침 국외이전 항목에 정확한 국가·리전 명시
  (현재 "미국(Supabase, Inc.)" 으로 기재).
- **P3** 팀·자격 보유 현황 섹션(회사소개)에 실제 인력·자격 정보 추가.
- **P3** `sl_audit_purge()` 자동 실행: pg_cron 설치 시 일 1회 스케줄 등록
  (`select cron.schedule('sl_audit_purge_daily','20 3 * * *', $$ select public.sl_audit_purge(); $$);`).

---

## 5. 작업 규칙

- **비밀번호·API 키·토큰 입력은 오너가 직접** 한다. Claude는 폼의 이름 필드까지만 채운다.
- `config.js` 에는 anon(publishable) 키만 둔다. `service_role` 키는 프런트에 절대 두지 않는다.
- 문의·지원 데이터는 실제 개인정보다. 스크린샷·로그·커밋에 내용을 남기지 않는다.
- 리브랜딩 금지: 딥 잉크 네이비(`#050B16`) + 사이버 시안(`#12B5CE`). 로고 변형 금지(`/brand/` 규칙 참조).
- 세션 종료 시 이 문서를 갱신하고 커밋한다.

---

## 6. 검증 기록

- 2026-07-30 · 로컬(`python3 -m http.server 8188`) 전 경로 200 확인(11페이지 + 정적 자원 11개).
- 2026-07-30 · `/contact/` 런타임 검증: supabase-js 로드·클라이언트 생성·폼 필드 7개·nav active·푸터 사업자 렌더·콘솔 오류 0.
- 2026-07-30 · `/insights/` DB 미적용 상태에서 폴백 문구 정상 표시(그레이스풀 디그레이드 확인).
- 2026-07-30 · 전 JS 파일 및 인라인 스크립트 5개 `node --check` 통과.
