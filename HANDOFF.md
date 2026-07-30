# HANDOFF — 쉴더스랩 웹사이트

> 이 문서가 **정본**이다. 세션이 바뀌거나 다른 PC에서 이어받을 때 이 파일을 먼저 읽는다.
> 상태·결정·남은 작업을 여기서만 관리한다.
>
> ⚠️ **이 저장소는 public 이다.** 계정 주소·미적용 보안조치·정확한 임계값 등 공격에 도움이 되는 정보는
> 여기 적지 않는다. 그런 항목은 로컬 메모나 비공개 채널로 관리한다.

최초 작성: 2026-07-30

---

## 1. 현재 상태

| 항목 | 상태 |
|---|---|
| 프런트 (12개 페이지) | ✅ 완료 · 로컬/라이브 검증 통과(전 경로 200, 콘솔 오류 0) |
| CI 벡터 원본 | ✅ 심볼·가로/세로 락업·모노·워드마크·파비콘·OG (아웃라인 패스) |
| DB 스키마·RLS·RPC (`0001`) | ✅ **라이브 적용 완료** (2026-07-30) |
| 초기 콘텐츠 시드 (`0002`) | ✅ 라이브 적용 완료 — 인사이트 3건 공개, 채용 2건 초안 |
| 백엔드 보안 경계 | ✅ anon 경로 E2E 검증 통과 (아래 6항) |
| 관리자 콘솔 | ⚠️ 구현 완료 · **로그인 미검증** — 관리자 Auth 계정 생성 필요(아래 ②) |
| GitHub 저장소 · Pages | ✅ [duelspost-droid/shilderslab-www](https://github.com/duelspost-droid/shilderslab-www) · Pages 빌드 성공 |
| 도메인 (가비아 DNS) | ✅ **등록 완료·전파 확인** (2026-07-30) |
| HTTPS | ✅ **인증서 발급·강제 완료** — apex/www 모두 Let's Encrypt 유효, http→https 301 |
| 라이브 감사 (5관점 병렬 + 적대적 검증) | ✅ 실시 — 확정 29건 중 high 2건 해소, 다수 반영(아래 7항) |
| 접수 알림 메일 (선택) | ⏳ `notify-inquiry` 미배포 |

로컬 경로: `/Users/hk/shilderslab-www` · 원격: `github.com/duelspost-droid/shilderslab-www` (public, main)

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

전부 재실행 안전(idempotent)이다.

### ② 관리자 Auth 계정 생성 — **아직 로그인 가능한 계정 없음**
`0001` 시드가 화이트리스트(`sl_admins`)에 오너 주소 1건을 넣어두었으나, 확인 결과 이 Supabase 프로젝트의
`auth.users` 에 대응하는 로그인 계정이 없다. 아래 확인 쿼리가 0행이면 로그인 계정을 먼저 만들어야 한다.

```sql
select count(*) from auth.users u
 where lower(u.email) in (select lower(email) from public.sl_admins);
```

**계정 생성** — Supabase 대시보드 → Authentication → Users → **Add user**
→ 이메일 입력, 비밀번호 지정, *Auto Confirm User* 켜기. (비밀번호 입력은 오너가 직접)

**다른 주소를 쓰려면** 계정 생성 후 화이트리스트에 추가:
```sql
insert into public.sl_admins(email, role, note)
values ('<사용할 주소>', 'admin', '쉴더스랩 관리자') on conflict (email) do nothing;
```

로그인 후 `/admin/` 대시보드에 통계가 보이면 정상이다. 화이트리스트에 없는 계정으로 로그인하면
콘솔이 자동 로그아웃시키고 "관리자로 등록되어 있지 않습니다" 를 표시한다.

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
- 리브랜딩 금지: 딥 잉크 네이비(`#050B16`) + 사이버 시안(`#12B5CE`). 로고 변형 금지(`/brand/` 규칙 참조).
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
