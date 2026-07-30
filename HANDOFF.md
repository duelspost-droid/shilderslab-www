# HANDOFF — 쉴더스랩 웹사이트

> 이 문서가 **정본**이다. 세션이 바뀌거나 다른 PC에서 이어받을 때 이 파일을 먼저 읽는다.
> 상태·결정·남은 작업을 여기서만 관리한다.
>
> ⚠️ **이 저장소는 public 이다.** 계정 주소·미적용 보안조치·정확한 임계값 등 공격에 도움이 되는 정보는
> 여기 적지 않는다. 그런 항목은 로컬 메모나 비공개 채널로 관리한다.

## 0. 다른 PC에서 이어받기

```bash
# 1) 클론
git clone git@github.com:duelspost-droid/shilderslab-www.git
cd shilderslab-www

# 2) 로컬 미리보기 (빌드 도구 없음 — 정적 사이트)
python3 -m http.server 8188 --directory .
#   → http://localhost:8188

# 3) 페이지 수정 후 반드시 재생성 (sitemap·인사이트 정적 페이지 포함)
python3 tools/build-pages.py

# 4) 배포 = main 푸시 (GitHub Pages 자동 빌드)
git push origin main
```

**필요한 것**: `python3` 만 있으면 페이지 빌드·미리보기가 된다.
CI 재생성(`tools/build-ci.py`)만 `fonttools` + 폰트 파일이 추가로 필요하고, 결과 SVG는 커밋되어 있으므로 평소에는 실행하지 않는다.

**어디를 먼저 보는가**
| 목적 | 파일 |
|---|---|
| 지금 상태·남은 작업 | 이 문서 1·3·8·9항 |
| 페이지 내용 수정 | `tools/content_*.py` → 빌드 |
| 내비·푸터·head | `tools/shell.py` |
| 디자인 토큰·반응형 | `assets/css/site.css` |
| 백엔드 스키마 | `supabase/migrations/` (적용 상태는 3항) |
| 관리자 콘솔 | `admin/index.html` · `admin/admin.js` |

**작업 종료 시 항상 할 것** (다음 세션·다른 PC를 위한 최소 규칙)
1. `python3 tools/build-pages.py` 실행 → 생성물까지 커밋
2. 이 문서의 **1항 상태표**와 **9항 작업 로그**를 갱신
3. 라이브에 반영해야 하는 SQL·Edge 함수가 있으면 3항에 적용 여부를 명시
4. `git push origin main`

---

## 1. 현재 상태

| 항목 | 상태 |
|---|---|
| 프런트 (25개 페이지) | ✅ v2 재설계 + CI 로고 적용 + 그리드/모바일 정비 완료 |
| CI 벡터 원본 | ✅ v2 딥 파인 단색 마크로 재생성(그라데이션 제거) |
| DB 스키마·RLS·RPC (`0001`) | ✅ **라이브 적용 완료** (2026-07-30) |
| 초기 콘텐츠 시드 (`0002`) | ✅ 라이브 적용 완료 — 인사이트 3건 공개, 채용 2건 초안 |
| 백엔드 보안 경계 | ✅ anon 경로 E2E 검증 통과 (아래 6항) |
| 관리자 콘솔 | ✅ 구현 완료(계정 관리 탭 포함) · 오너 계정 `admin` 결속 완료 — **로그인 동작 자체는 아직 미검증**(비밀번호 입력은 오너만) |
| 영문 사명 표기 | ✅ `SHIELDUS LAB` **반영 완료** (2026-07-30) — 페이지·CI·명함 30종 전부. 발주 보류 해제 |
| 모바일 | ✅ 390px 검증 — 가로 스크롤 없음, 표 카드형 접힘, 드로어 정상 |
| GitHub 저장소 · Pages | ✅ [duelspost-droid/shilderslab-www](https://github.com/duelspost-droid/shilderslab-www) · Pages 빌드 성공 |
| 도메인 (가비아 DNS) | ✅ **등록 완료·전파 확인** (2026-07-30) |
| HTTPS | ✅ **인증서 발급·강제 완료** — apex/www 모두 Let's Encrypt 유효, http→https 301 |
| 라이브 감사 (5관점 병렬 + 적대적 검증) | ✅ 실시 — 확정 29건 중 high 2건 해소, 다수 반영(아래 7항) |
| 접수 알림 메일 (선택) | ⏳ `notify-inquiry` 미배포 |

로컬 경로: macOS `/Users/hk/shilderslab-www` · Windows `C:\Users\duels\Projects\shilderslab-www`
원격: `github.com/duelspost-droid/shilderslab-www` (public, main)

---

## 2. 아키텍처 결정 (요약)

- **정적 프런트 + Supabase**: jbax-www(`/ax/`)와 동일한 방식. 빌드 도구·서버 런타임 없음 → GitHub Pages로 즉시 배포.
- **Supabase 프로젝트를 다른 서비스와 공유**한다. 따라서 이 사이트에서는 `authenticated` 를 관리자와 동일시하지 않는다.
  전 테이블의 읽기·쓰기 권한을 `sl_admins` 화이트리스트(`is_sl_admin()`)로 게이트했다.
- **PII 테이블은 공개 정책 자체를 만들지 않음**: `sl_inquiries` / `sl_applications` 는 INSERT 정책이 없고
  `SECURITY DEFINER` RPC(`sl_submit_inquiry`, `sl_apply`)로만 적재된다. 동의 필수·이메일 형식·길이 상한과
  서버측 레이트리밋(IP 기준 + 전역 상한 2계층), 폼 허니팟을 적용했다. 구체적 임계값은 마이그레이션 파일 참조.
- **CDN 의존 제거**: supabase-js를 `assets/vendor/` 에 자체 호스팅 → CSP를 `script-src 'self'` 로 좁혔다.
- **워드마크 아웃라인**: 로고에 `<text>` 를 쓰지 않고 글리프를 패스로 변환해 임베드. 폰트 없는 환경·인쇄·커팅에서 동일 렌더.

---

## 3. 오너 조치 필요 (순서대로)

### ① DB 마이그레이션
- `0001_shilderslab_core.sql` · `0002_shilderslab_seed.sql` — ✅ 적용 완료 (2026-07-30)
- `0003_shilderslab_hardening.sql` — ✅ 적용 완료 (2026-07-30). 서버측 길이 검증, 전역 남용 상한,
  개인정보 보유기간 자동 파기(`sl_pii_purge`), `pg_cron` 일일 스케줄 `sl_purge_daily`(03:20 UTC) 등록 확인.
- `0004_shilderslab_admin_roles.sql` — ✅ 적용 완료 (2026-07-30). 역할(admin/editor) 분리 + 관리자 계정 관리 RPC
  + **권한을 이메일 문자열이 아니라 로그인 계정(user_id)에 결속**.
  적대적 검토에서 나온 critical(계정 없는 화이트리스트 행을 제3자가 선점 → 관리자 탈취) 을 막기 위한 변경이다.
  적용 후 anon 경로 검증: 신규 권한 함수 7개 전부 `permission denied`.

전부 재실행 안전(idempotent)이다.

### ② 최초 관리자 부트스트랩 — ✅ 완료 (2026-07-30)
0004 부터 권한은 이메일 문자열이 아니라 **로그인 계정(auth.users.id)** 에 결속된다.
화이트리스트에 이메일만 있고 계정이 연결되지 않은 행은 **권한이 전혀 없다**.
공유 프로젝트에서 누군가 그 주소로 가입해 관리자가 되는 경로를 막기 위한 설계다.

**현재 상태(실측): `sl_admins` 1행 = 오너 계정 · role `admin` · user_id 연결됨.**
공유 프로젝트에 이미 있던 확인(confirmed) 상태의 오너 계정을 그대로 결속했으므로
계정을 새로 만들거나 비밀번호를 다룬 적이 없다. 오너는 **기존 비밀번호로 `/admin/` 로그인**한다.

아래는 관리자를 추가로 세워야 할 때(계정 분실·신규 PC 등)를 위한 절차다.

**① 계정 생성** — Supabase 대시보드 → Authentication → Users → **Add user**
→ 이메일 입력, 비밀번호 지정, **Auto Confirm User 켜기**. (비밀번호 입력은 오너가 직접)

**② 부트스트랩 SQL 1회 실행** — SQL Editor 에서 이메일만 바꿔 실행. 재실행 안전.
```sql
insert into public.sl_admins (email, role, note, user_id)
select lower(u.email), 'admin', '최초 관리자', u.id
  from auth.users u
 where lower(u.email) = lower('여기에_관리자_이메일')
   and u.email_confirmed_at is not null
on conflict (lower(email))
do update set user_id = excluded.user_id, role = 'admin';

-- 확인: 1 이상이어야 콘솔 접속 가능
select count(*) from public.sl_admins where role='admin' and user_id is not null;
```

이후 관리자 추가·연결·역할변경·삭제는 콘솔 **[계정 관리]** 탭에서 처리한다.
앱 안에서 스스로 관리자가 되는 경로는 의도적으로 없다 — 첫 관리자만 이 SQL 경로가 필요하다.

### ③ ~~가비아 DNS~~ ✅ 완료 (2026-07-30)
가비아 DNS 관리에 아래 5개 레코드 등록 완료(TTL 600). 권위 네임서버(ns.gabia.co.kr)와 공용 리졸버(8.8.8.8) 양쪽에서 응답 확인.

| 타입 | 호스트 | 값 |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | duelspost-droid.github.io. |

실측: `http://shilderslab.com/` 200 · `http://www.shilderslab.com/` → apex 301.

**남은 것 = HTTPS 인증서**: GitHub이 DNS 확인 후 Let's Encrypt 인증서를 자동 발급한다(보통 수십 분, 최대 24시간).
발급 전에는 `https://` 접속 시 `*.github.io` 인증서가 응답해 브라우저 경고가 뜬다.
발급 완료 확인:
```bash
gh api repos/duelspost-droid/shilderslab-www/pages --jq '.https_certificate.state'   # approved 면 완료
```
`approved` 가 되면 강제 HTTPS를 켠다:
```bash
gh api -X PUT repos/duelspost-droid/shilderslab-www/pages -F https_enforced=true
```
(GitHub 웹 UI 대신 위 API 로 처리했다. UI 사용이 막히는 경우 API 경로가 정본이다.)

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
- 리브랜딩 금지: v2 에디토리얼 팔레트 — 페이퍼 `#F6F4EF` · 잉크 `#15181B` · 딥 파인 `#1A4B3A`.
  그라데이션·블롭·마퀴 금지. 로고 변형 금지(`/brand/` 규칙 참조).
  단, **국문 사명 `쉴더스랩` 은 유지**한다 — shield us 의 연음 음차가 곧 "쉴더스"다(10항).
- 세션 종료 시 이 문서를 갱신하고 커밋한다.

---

## 6. 검증 기록

**프런트 (2026-07-30)**
- 로컬(`python3 -m http.server 8188`) 전 경로 200 — 12페이지 + 정적 자원 11개.
- 라이브 GitHub Pages 서빙 확인: DNS 연결 전이라 `curl --resolve shilderslab.com:80:185.199.108.153` 로
  직접 확인 — `/`, `/services/`, `/contact/`, CI 자산, `robots.txt` 모두 200, 홈 `<title>` 일치.
- `/contact/` 런타임: supabase-js 로드·클라이언트 생성·폼 필드 7개·nav active·푸터 사업자 렌더·콘솔 오류 0.
- 전 JS 파일 + 인라인 스크립트 5개 `node --check` 통과.

**백엔드 보안 경계 — anon 키 실경로 E2E (2026-07-30)**

| 검증 항목 | 결과 |
|---|---|
| 공개 인사이트 조회 | ✅ 3건 (시드) |
| 미게시 채용공고 | ✅ anon 에게 0건 노출 (published 게이트 동작) |
| `sl_stats()` anon 호출 | ✅ `permission denied for function sl_stats` |
| `sl_log()` anon 호출 (로그 위조 시도) | ✅ `permission denied for function sl_log` |
| 동의 없이 문의 제출 | ✅ 거부 — "개인정보 수집·이용 동의가 필요합니다" |
| 잘못된 이메일 형식 | ✅ 거부 — "이메일 형식이 올바르지 않습니다" |
| 정상 문의 제출 | ✅ 적재 성공(uuid 반환) |
| **적재 직후 anon 재조회** | ✅ **0행 — RLS 차단 실증** (행은 존재하나 조회 불가) |
| 방문 로깅 RPC | ✅ 성공, `sl_audit` 는 anon 조회 0행 |

※ 위 테스트로 생성된 문의 1건과 감사 로그는 SQL Editor에서 삭제 완료(`sl_inquiries` 0행 확인).

**감사 후속 실측 (2026-07-30)**

| 검증 | 결과 |
|---|---|
| HTTPS 인증서 | `state=approved`, 도메인 `shilderslab.com` · `www.shilderslab.com` |
| http → https | apex·www 모두 **301** → `https://shilderslab.com/` |
| 허니팟 | 숨김 필드가 채워진 제출은 **RPC 호출 0회**로 종료(정상 성공 메시지 노출) |
| RPC 길이 검증 | 120자 초과 이메일 · 30자 초과 연락처 모두 서버에서 거부 |
| 정상 제출(0003 이후) | 성공(uuid 반환) — RPC 재정의로 인한 회귀 없음 |
| 적재 후 anon 재조회 | 0행 — RLS 차단 유지 |
| pg_cron | `sl_purge_daily` 잡 등록 확인(매일 03:20 UTC, `sl_audit_purge` + `sl_pii_purge`) |

※ 위 테스트 데이터는 모두 삭제 완료(`sl_inquiries` 0행 확인).

**미검증 (오너 계정 필요)**
- `/admin/` 로그인 이후 흐름 전체(대시보드 통계·문의 처리·CMS 저장·감사 로그 열람).
  관리자 Auth 계정이 없어 진행 불가 — 위 ②항 완료 후 확인 필요.

---

## 7. 라이브 감사 반영 (2026-07-30)

도메인 공개 직후 5개 관점(SEO · 링크/자산 · 보안 · 콘텐츠/법적 · 프런트↔DB 계약)을 병렬 점검하고,
각 지적을 별도 에이전트가 **반증 시도**한 뒤 살아남은 것만 반영했다. 확정 29건 / 반증·기각 19건.

### 반영 완료

| 구분 | 내용 |
|---|---|
| high | HTTPS 미제공 — 인증서 발급이 **큐에 오르지도 않은 상태**(`https_certificate.state = null`)였음. 커스텀 도메인 재설정으로 재트리거 → apex·www 발급, 강제 HTTPS 적용 |
| high | 처리방침의 "전 구간 HTTPS 적용" 단언이 사실과 불일치 → HTTPS 실제 적용으로 해소 |
| 보안 | 문의·지원 폼 허니팟(봇 제출은 RPC 호출 없이 종료) · 전역 시간당 상한(IP 위조 우회 방어) · RPC 길이 검증 보강 |
| 보안 | 관리자 콘솔 프레임 버스터(meta CSP는 `frame-ancestors` 미적용) |
| 보안 | 공개 저장소에서 운영 세부정보 제거(관리자 주소·계정 보안조치 상태·정확한 임계값·공유 프로젝트 서술) |
| 법적 | 자동 수집 항목(IP·User-Agent)을 처리방침 표와 폼 동의 문구에 명시 |
| 법적 | 제출 감사 로그 항목 신설, 국외이전 표에 수탁자 연락처·이전 시기·방법 추가, Google Fonts 수탁자 등재 |
| 법적 | 고지한 "자동 삭제"를 실제로 이행 — `sl_pii_purge`(문의 1년 / 지원 6개월) + pg_cron 일일 실행 |
| 법적 | 약관: 고의·중과실 단서, 변경 공지 기준(7일/30일) 통일, 회사 정의, 문장 정리 |
| SEO | 인사이트 상세가 목록으로 canonical 되던 문제 수정(자기참조 + og 갱신) |
| SEO | `sitemap.xml` 을 빌드 시 CMS에서 생성(공개 인사이트 URL 포함), `/services/` og 보완 |
| SEO | `robots.txt` 의 `/admin/` Disallow 제거(noindex 가 읽히도록) + 공개 푸터의 관리자 링크 제거 |
| 정합성 | 관리자 '사이트 설정'이 실제로 공개 페이지에 반영되도록 소비 코드 구현 + 저장 안내 문구 정정 |
| 정합성 | 인사이트 정렬 `sort_order` 우선 통일, 발행일 미입력 시 한글 검증(원시 Postgres 에러 방지) |
| 품질 | '영업일 기준' 표현 통일, 한국어 표기 교정 |

### 남긴 것 (판단 근거 포함)

- **Google Fonts 외부 로드** — 지금은 처리방침 위탁표에 고지하는 것으로 처리했다.
  근본 해결은 woff2 self-host(한글 서브셋)이며, CSP에서 외부 도메인을 지우고 국외이전 항목도 하나 줄어든다. → P2
- **인사이트 상세의 정적 생성** — 현재 CMS 렌더(클라이언트)라 소셜 크롤러가 og 를 읽지 못한다.
  발행 시 정적 페이지를 만들려면 관리자 발행이 곧 재빌드로 이어져야 하므로 구조 변경이 필요하다. → P2
- **CSP `script-src 'unsafe-inline'`** — 정적 사이트라 인라인 스크립트에 의존한다. 출력은 전부 `SL.esc` 로
  이스케이프하고 CMS 본문은 HTML을 렌더하지 않으므로 현재 위험은 낮다고 판단. 외부 스크립트는 0개. → 수용
- **공유 Supabase 프로젝트의 이메일 셀프 가입** — 이 사이트는 가입을 쓰지 않지만, 같은 프로젝트를 쓰는
  다른 서비스가 있어 임의로 끄면 그쪽이 깨진다. **오너 판단 필요**(아래 ⑥).

### ⑥ (오너 확인) 공유 Supabase 프로젝트의 셀프 가입 설정
Authentication → Providers → Email → *Allow new users to sign up*.
이 프로젝트를 쓰는 다른 서비스가 공개 가입을 쓰지 않는다면 꺼두는 편이 안전하다.
쉴더스랩 관리자 권한은 가입과 무관하게 `sl_admins` 화이트리스트로만 부여되므로, 꺼도 이 사이트에는 영향이 없다.

---

## 8. v2 전면 재설계 (2026-07-30)

사용자 지시: “디자인을 싹 바꿔봐. 다른 정보보호컨설팅 업체 홈페이지 참고해서 내용 강화하고.
디자인이 좀더 AI로 만든것이 아닌것처럼 세련되야되.”

### 근거
국내 컨설팅사 · 글로벌 부티크 · 디자인 언어 · 규제 사실관계 · 자체 진단 **5갈래 병렬 리서치** 후 종합.
방향은 사용자가 선택: **에디토리얼 라이트** + **침착한 액센트로 교체**.

리서치에서 확인한 핵심 사실:
- 국내 컨설팅사는 절차(프로세스) 블록은 다 갖고 있지만 **산출물 목록을 공개하는 곳은 거의 없다** → 변별점
- **정보보호 전문서비스기업 지정** 없이는 주요정보통신기반시설 취약점 분석·평가를 수주할 수 없다
  → “할 수 있다”고 쓰면 안 되는 과업이 있다. 사이트에 명시함
- 구매자는 ①기업 현황 ②재무 ③수행 실적 ④참여 인력 ⑤비용으로 채점한다.
  신생사는 ③이 비므로 ④(사람)와 “공개”로 메워야 한다

### 디자인 (AI 티를 만드는 요소를 전부 제거)
| 버린 것 | 대체 |
|---|---|
| 다크 네이비 + 네온 시안 그라데이션 | 웜 오프화이트 지면(#F6F4EF) + 잉크(#15181B) + 딥 파인(#1A4B3A) |
| blob 블러 · 스캔라인 · 글로우 · 마퀴 | 헤어라인 규칙선, 여백, 정지된 배경 |
| 라운드 카드 3열 그리드 | 상단 규칙선 + 번호로 구분하는 ‘단(column)’ |
| 중앙정렬 히어로 | 좌측 본문 / 우측 스펙 메타 열 비대칭 |
| Manrope + Noto Sans KR | IBM Plex Sans KR · Mono · Serif 한 계열 |
| 그라데이션 텍스트 | 단색. 강조는 크기와 여백으로 |

**한글 조판 주의** — 모노스페이스 + 대문자 + 넓은 자간은 라틴 전용이다. 한글 라벨에 쓰면 어색해진다.
`site.css` 맨 아래 “한글 라벨 보정” 블록에서 한글이 들어가는 라벨을 산세리프로 되돌린다. 새 컴포넌트를 만들 때도 이 규칙을 지킬 것.

### 정보구조 (11 → 25 페이지)
- **서비스 상세 6종 신설** — `/services/{isms-p,pentest,assessment,privacy,cloud,governance}/`
  각 페이지: 이런 경우 필요 → 수행 범위 → 대상·전제 → **산출물** → 유의사항 → FAQ
- **`/method/`** 진단 방법론 — 5단계 절차(단계별 산출물), 위험도 등급 정의표, 수행 규칙, 하지 않는 일
- **`/resources/`** 자료실 + 실제 문서 3종
  (모의해킹 제안서 비교 체크리스트 · ISMS-P 착수 전 자가점검 · 진단 보고서 구성 샘플)
- **`/regulations/`** 규제 가이드 — 제도 비교표, ISMS-P 3영역 구조, **수행 자격이 제한된 업무** 3분할
- **`/trust/`** 신뢰 센터 — 데이터 취급, 계약 조건·보유 지위(미보유는 미보유로), **자사 사이트의 남은 위험 공개**,
  취약점 제보 정책 + `/.well-known/security.txt`
- 인사이트: 빌드 시 CMS에서 읽어 `/insights/<slug>/` **정적 페이지 생성**(SEO 근본 해결).
  최근 발행분은 404 폴백 스크립트가 동적 렌더러로 넘긴다

### 빌드 구조 변경
모든 페이지를 `tools/build-pages.py`가 생성한다(홈·서비스 포함). 손으로 쓴 예외 페이지 없음 → 셸 드리프트 불가.
```
tools/shell.py            head · masthead · footer (내비 변경은 NAV 한 곳)
tools/content_home.py     홈
tools/content_services.py 서비스 허브 + 상세 6종(_detail 함수로 동일 골격)
tools/content_pages.py    회사소개 · 방법론 · 브랜드 · 404
tools/content_resources.py 자료실 + 문서 3종
tools/content_trust.py    신뢰 센터 · 규제 가이드
tools/content_legal.py    처리방침 · 약관
tools/content_dynamic.py  인사이트 · 채용 · 문의(백엔드 연동)
```
페이지 수정 후 반드시 `python3 tools/build-pages.py` 실행. sitemap도 이때 자동 생성된다.

### 남은 것 (v2 기준 우선순위)
1. **`/team/` 사람 페이지** — 리서치가 지목한 최대 공백. 현재 사이트에 사람 이름이 0건이다.
   실적이 없을수록 “누가 하는가”가 유일한 대체 증거다. **실명·경력·보유 자격은 지어낼 수 없으므로 오너가 제공해야 한다.**
2. **샘플 진단 보고서 PDF** — 자체 데모 앱이나 의도적 취약 오픈소스를 실제로 진단해 전문 공개.
   자료실의 “보고서 구성 샘플”을 실물 PDF로 승격하는 작업.
3. 웹폰트 self-host — 외부 폰트 제거 시 CSP가 좁아지고 국외이전 항목이 하나 줄어든다.
4. 실적·사례가 쌓이면 `/about/` 연혁과 홈 지표를 실제 수치로 교체.

---

## 9. 작업 로그

세션이 끝날 때마다 한 줄씩 append 한다. 다른 PC에서 "어디까지 했나"를 이 표로만 판단할 수 있어야 한다.

| 날짜 | 한 일 | 남긴 것 |
|---|---|---|
| 2026-07-30 | 사이트 최초 구축(11페이지) · CI 벡터 원본 · DB 스키마 0001/0002 적용 · GitHub Pages 배포 | 관리자 계정·법인정보 대기 |
| 2026-07-30 | 가비아 DNS 등록 · HTTPS 인증서 발급·강제 적용 | — |
| 2026-07-30 | 라이브 감사(5관점 병렬+적대검증) 반영 · 0003 적용(레이트리밋·PII 자동파기·pg_cron) | 팀 페이지·샘플 보고서 |
| 2026-07-30 | v2 전면 재설계(에디토리얼) · 25페이지 · 방법론/자료실/규제/신뢰센터 신설 · 인사이트 정적화 | 팀 페이지(오너 자료 필요) |
| 2026-07-30 | 관리자 계정 관리(0004 + Edge + UI) · CI 로고 적용 · 그리드 버그 수정 · 모바일 정비 | — |
| 2026-07-30 | 명함 시안 3종(인쇄 납품 규격 SVG/PDF/PNG/JPG) · 권한 결속 강화(적대적 검토 critical 반영) · 0004 라이브 적용 | **최초 관리자 부트스트랩(3항 ②)**, Edge 배포(선택) |
| 2026-07-30 | 최초 관리자 부트스트랩 완료(오너 기존 계정 결속) · **사명 표기 변경 착수**(SHILDERS LAB → SHIELDUS LAB) · CI 재생성 · 빌드 폰트 레포 포함 | **§10 진행 중 작업** — 명함 30종 재생성 · 대표이사 인사말 · CI 심볼 재검토 · 도메인 판단 |
| 2026-07-30 | **명함 30종 재생성 완료**(사명 표기 변경 마무리) · `/brand/` 발주 보류 경고 제거 · Windows PC 빌드 환경 구축(§10) | 오너 판단 3건 — 대표이사 성명 · CI 심볼(A/B/C) · 도메인 |

---

## 10. 진행 중 — 사명 표기 변경 (2026-07-30 세션 중단, 여기서 이어서)

### 배경
오너 확인: 사명은 **shield + us + lab** 이다. 기존 영문 표기 `SHILDERS LAB` 은 오기였다.

**국문 `쉴더스랩` 은 바꾸지 않는다.** shield us → "쉴드어스" 의 연음 표기가 곧 "쉴더스" 이므로
국문 사명은 이미 정확하다. 따라서 이번 변경은 **영문 표기와 의미 서술에 한정**된다.

영문 표기는 `SHIELDUS LAB`(2단어)을 채택했다. 근거: 국문 `쉴더스랩`(쉴더스 + 랩)과 1:1 대응하고,
`SHIELD US` 가 눈에 그대로 읽힌다. 3단어 `SHIELD US LAB` 은 문장처럼 읽혀 사명으로서의 단위감이 약하다.
바꾸려면 `tools/build-ci.py` 의 `NAME_EN` 한 곳만 고치면 된다(환경변수 `SL_NAME_EN` 로도 override 가능).

### 이번 세션에 완료한 것
- `NAME_EN` / `DOMAIN` 상수 분리 — **사명과 도메인은 다른 값이다**(도메인은 여전히 `shilderslab.com`)
- CI 전체 재생성: 워드마크·가로/세로 락업·OG 커버·ci-meta (심볼·파비콘은 바이트 동일 = 무변경)
- 전 페이지 소스 및 재빌드 완료, 구 표기 문자열 잔존 0건
- 빌드 폰트를 레포에 포함(`tools/Manrope.ttf`, `tools/NotoSansKR.ttf`, 둘 다 SIL OFL 1.1)
  → 어느 PC에서도 네트워크 없이 CI 재생성이 재현된다. 실제로 이전 빌드와 심볼 패스가 바이트 동일함을 확인했다.

### 이어서 할 일 (우선순위 순)

**1) ~~명함 30종 재생성~~ — ✅ 완료 (2026-07-30)**
`tools/build-card.py` 를 전 포맷 한 번에 실행해 재생성했고, `/brand/` 의 발주 보류 경고(`.note-warn`)도 제거했다.
**이제 인쇄 발주가 가능하다.**
```bash
# 필요 패키지: fonttools svglib reportlab pypdf  (+ 래스터용 node/sharp)
SL_SHARP_DIR=<sharp 설치 디렉터리> python3 tools/build-card.py   # 3 시안 × 앞뒤 × SVG/PDF/PNG/JPG
```
⚠ SVG/PDF 만 갱신하고 PNG/JPG 를 남겨두면 **같은 시안의 포맷별 사명이 달라진다**. 반드시 한 번에 전부 재생성한다.
⚠ `SL_SHARP_DIR` 를 지정하지 않으면 래스터(PNG/JPG)가 **조용히 건너뛰어진다**. 위 경고가 그대로 현실이 되므로 반드시 지정한다.

실측 메모 — 재생성 후 30개 중 **22개만 변경**되는 것이 정상이다.
`card-B-front` · `card-C-back` 은 영문 워드마크가 없는 면(심볼 + 도메인 `shilderslab.com` 뿐)이라
SVG·PNG·JPG 가 바이트 동일하다. PDF 는 생성 타임스탬프 때문에 항상 변경된다.
검증은 grep 이 아니라 **`@300.jpg` 를 눈으로 확인**해야 한다(아웃라인 패스라 문자열 검색이 통하지 않는다).

**2) 대표이사 인사말** — `/about/` 에 섹션 추가. 서명에 쓸 **대표이사 성명이 없다**(`config.js` COMPANY.ceo 비어 있음).
오너가 성명을 주면 넣는다. 이름을 임의로 만들지 않는다.

**3) CI 심볼 재검토 (오너 판단 대기)** — 현재 심볼은 실드 + **'S' 각인**이다.
사명의 핵심이 "우리(us)를 지킨다"로 바뀌었으므로 'S'(Shield 의 머리글자)는 의미를 덜 담는다. 후보:
- **A. 현행 유지(S)** — 자산 보존, 변경 비용 0. 의미 반영은 문구로만.
- **B. 'U' 각인 (권장)** — U = us. 게다가 U 자체가 사발 모양이라 **실드 안의 작은 실드**로 형태가 운을 맞춘다.
  한 글자 각인이라 16px 파비콘에서도 또렷하고 각인·커팅에도 쓸 수 있다. `build-ci.py` 3줄 수정.
- **C. 'US' 두 글자** — 가장 직설적이나 16px 에서 뭉치고, 영문권에서 **US = 미국**으로 읽힐 위험이 있다. 비권장.
후보를 16/32/64px 로 렌더한 비교 시트를 만들어 오너에게 제시한 뒤 확정한다. 확정 전에는 심볼을 바꾸지 않았다.

**4) 도메인 판단 (오너)** — 사명이 `shielduslab` 인데 서비스 도메인은 `shilderslab.com` 이다.
실측 결과 **`shielduslab.com` 은 이미 타인이 선점**(Squarespace, 운영 중)해 취득할 수 없다.
`shielduslab.co.kr` · `shielduslab.kr` · `shieldus-lab.com` 은 NS 없음 = 취득 가능해 보인다.
- 유지하는 경우: 도메인은 국문 사명 `쉴더스랩` 의 음차 표기라는 설명이 성립한다. 추가 비용 0.
- 교체하는 경우: CNAME·인증서 재발급·canonical/OG/sitemap·`security.txt`·Edge CORS·메일 주소를
  모두 바꿔야 한다. **`DOMAIN` 상수와 `.com` 문자열 19개 파일**이 대상이다.
현재 코드는 **유지**를 전제로 되어 있다.

### 빌드 환경 (PC별)

**macOS** — 시스템 `python3` 에 `fontTools` 가 없어 CI 빌드가 실패한다. venv 를 만들어 썼다.
```bash
/usr/bin/python3 -m venv ~/.venvs/sl && ~/.venvs/sl/bin/pip install fonttools svglib reportlab pypdf
~/.venvs/sl/bin/python tools/build-ci.py
python3 tools/build-pages.py      # 페이지 빌더는 표준 라이브러리만 쓴다 — 시스템 python3 로 충분
```

**Windows (`C:\Users\duels\Projects\shilderslab-www`)** — 구축 완료(2026-07-30).
`python`/`python3` 는 MS Store 스텁이라 실행하면 exit 9009 로 죽는다. Python 3.12 를 따로 깔았다.
```powershell
winget install --id Python.Python.3.12 -e --scope user
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install fonttools svglib reportlab pypdf
.\.venv\Scripts\python.exe tools\build-pages.py
```
래스터용 `sharp` 는 레포 밖 별도 디렉터리에 설치하고 `SL_SHARP_DIR` 로 넘긴다(레포에 `node_modules` 를 만들지 않기 위함).
```powershell
npm install --prefix <sharp 디렉터리> sharp
$env:SL_SHARP_DIR = "<sharp 디렉터리>"
.\.venv\Scripts\python.exe tools\build-card.py
```
`.venv/` · `node_modules/` 는 `.gitignore` 에 넣어 두었다.

⚠ **PDF 손상 함정 (Windows 에서 발견, `.gitattributes` 로 봉인함)**
Windows git 기본값 `core.autocrlf=true` 인데, PDF 는 앞부분에 NUL 바이트가 없어 git 이 **텍스트로 오판**한다.
그대로 두면 체크아웃마다 LF→CRLF 치환이 일어나 **인쇄 납품용 벡터 PDF 6개가 소리 없이 깨진다**.
`.gitattributes` 에 `*.pdf binary` 를 포함해 전 플랫폼에서 바이트를 보존하도록 했다(PNG/JPG/TTF 도 함께).
텍스트는 `eol=lf` 로 못박아 macOS↔Windows 간 전체 파일 재작성 diff 가 생기지 않게 했다.
