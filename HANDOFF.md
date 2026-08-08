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
| 페이지 문구 CMS (`0005`) | ✅ **라이브 적용 완료** — **블록 49개**(2026-08-08 홈 본문 12블록 추가, 실측 확인) · 하이드레이션 E2E 검증 통과(6항) |
| 관리자 콘솔 | ✅ 계정 관리 · 페이지 문구 · **비밀번호 변경** · **아이디 로그인** · 로그인 이후 흐름을 끊던 `audit()` 결함 수정(6항) — **오너 로그인 실검증은 아직**(비밀번호는 오너만) |
| 영문 사명 표기 | ✅ `SHIELDUS LAB` — 페이지·CI·명함 전부 반영 |
| 브랜드 자산 | ✅ CI 기본형 + **한글형(국문 우선·영문 병기) 6종** · 명함 **60개**(영문형 30 + 한글형 30) |
| 명함 발주 | ⛔ **보류** — 명함에 전환 예정 도메인이 새겨져 있고 아직 확보 전(`/brand/` 경고 게재) |
| 타이포그래피 | ✅ 합성 볼드 제거 · 폰트 스택 토큰화 · 한글 라벨 보정 특정도 수정 · 미사용 페이스 제거 |
| 카피 톤 | ✅ 기계적 문형 정비 + **신생 프레임 제거**(설립 시기·실적 유무를 앞세우지 않음) |
| 모바일 | ✅ 390px 검증 — 가로 스크롤 없음, 표 카드형 접힘, 드로어 정상 |
| GitHub 저장소 · Pages | ✅ [duelspost-droid/shilderslab-www](https://github.com/duelspost-droid/shilderslab-www) · Pages 빌드 성공 |
| 서비스 도메인 | ✅ `shilderslab.com` (가비아) — 등록·전파·HTTPS 완료 |
| 전환 예정 도메인 | ⏳ `shielduslab.com` **미확보**(확보는 확정) → 확보 후 11항 절차 실행. **명함 도메인은 사이트와 별개 변수**이므로 `set-domain.py` 대상에서 제외돼 있다 |
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

- `0005_shilderslab_content.sql` — ✅ **적용 완료 (2026-07-30, 2026-08-01, 2026-08-08 재적용)**. 페이지 문구 CMS(`sl_content`), 블록 **49개**.
  블록을 추가하면 재적용해야 DB 에 들어간다. 재적용해도 기존 값은 보존된다(실측 확인).
  ```sql
  select count(*) from public.sl_content;              -- 49
  select key, length(value) from public.sl_content order by sort_order;
  ```
  ⚠ **재실행해도 오너가 고친 문구는 덮어쓰지 않는다** — 시드의 `on conflict` 가 메타데이터만 갱신한다.
  2026-08-08 재적용 직후 실측으로 확인했다: 오너가 콘솔에서 고쳐 둔 `home.hero_title`
  (“정보보호 전문가가  제대로 처리합니다”)이 그대로 살아 있었다.

### ⑦ 페이지 문구 CMS 사용법 (0005 적용 후)
관리자 콘솔 → **[페이지 문구]** 탭. 편집 가능한 **49개** 블록:
홈 14 · 방법론 2 · 자료실 2 · 신뢰센터 2 · 규제 2 · 인사이트 2 · 채용 2 · 문의 2 ·
회사소개 6 · 대표이사 인사말 4 · 서비스 2 · 브랜드·CI 1 · 푸터 1 · 법인 정보 7.

홈은 히어로만 올라가 있어서 정작 본문(“규제와 공격, 양쪽에서 봅니다” 등 01 Services~Contact
6개 섹션의 제목·리드)이 콘솔에 없었다. 2026-08-08 에 12블록을 추가해 메웠다.

- **비워두면 코드 기본 문구가 그대로 나온다.** 실수로 지워도 빈 화면이 되지 않는다.
- 저장하면 **방문자에게는 즉시** 반영된다(클라이언트가 다시 그림).
  **정적 HTML 에는 다음 배포 때** 구워진다 — 검색엔진·SNS 크롤러는 정적 본문을 읽으므로
  중요한 문구를 바꿨다면 `python3 tools/build-pages.py` 후 푸시해 두는 편이 좋다.
- 값은 **평문/최소 마크다운**으로만 저장된다(HTML 저장 안 함). 빌드·클라이언트 양쪽이 이스케이프 후 렌더한다.
- 블록을 **추가·삭제**하려면 `tools/content_blocks.py` 를 고치고 `python3 tools/gen-content-seed.py` 로
  0005 를 재생성한 뒤 다시 적용한다. 페이지 HTML 쪽에는 `data-content="키"` 앵커를 달아야 한다.
  같은 태그를 앵커 안에 중첩하면 치환이 잘린다(주석 참조).
- `company.*` 는 `config.js` 의 `COMPANY` 를 덮어쓴다. 즉 **법인 정보는 이제 콘솔에서 입력하면 된다**(④ 대체).

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

**로그인 방법** (2026-08-01 실측 확인)
`/admin/` → **이메일 + 비밀번호**(`signInWithPassword`). 매직링크·소셜 로그인은 쓰지 않는다.
계정은 **공유 Supabase 프로젝트에 이미 있던 오너 계정**이므로 **기존 비밀번호를 그대로** 쓴다.
이 저장소는 public 이라 주소는 여기 적지 않는다 — 아래 SQL 로 확인한다.
```sql
select a.email, a.role, (a.user_id is not null) as bound,
       u.email_confirmed_at is not null as confirmed, u.last_sign_in_at
  from public.sl_admins a left join auth.users u on u.id = a.user_id;
```
실측: 1행 · role `admin` · bound ✅ · confirmed ✅ · 마지막 로그인 2026-07-30 03:02 UTC
(= 그 비밀번호로 로그인된 이력이 있다).

**비밀번호를 모를 때** — Supabase 대시보드 → Authentication → Users → 해당 계정 → `⋯`
→ *Send password recovery* 또는 *Reset password*. **비밀번호 입력·설정은 오너가 직접 한다.**

**비밀번호 변경** — 콘솔 헤더 **[비밀번호 변경]**(2026-08-08 추가). 로그인한 본인 계정을 바꾼다.
이 화면이 생기기 전에는 Supabase 대시보드까지 가야 했고, 대시보드 권한이 없는 `editor` 는
스스로 바꿀 방법이 아예 없었다. 임시 비밀번호로 처음 들어와 바로 교체하는 흐름을 여기서 끝낸다.

### ⑧ 관리자 주소 교체 절차 (예: `shieldusadmin@…` 으로 바꿀 때)

> **전제 — 새 주소는 메일을 받을 수 있어야 한다.** 확인 메일·비밀번호 재설정 링크가 그리로 간다.
> 실측(2026-08-08): `shilderslab.com` 은 **MX 레코드가 없어 메일을 받지 못한다.**
> 이 도메인으로 관리자 주소를 만들면 비밀번호를 잊는 순간 복구 경로가 사라진다. 쓰지 말 것.
> `shielduslab.com` 은 Google Workspace(`smtp.google.com`) 가 걸려 있고, `jbfg.com` 도 정상이다.

**순서를 지킨다. 뒤집으면 잠긴다.**

1. **(오너) 계정 생성** — Supabase 대시보드 → Authentication → Users → **Add user**
   → 새 이메일 + 임시 비밀번호 + **Auto Confirm User 켜기**.
   *(콘솔 [계정 관리] 탭의 '새 관리자' 로도 만들 수 있다 — Edge 함수 `sl-admin-user` 배포가 전제다. 12항 참조.)*
2. **(오너/Claude) 화이트리스트 결속** — 콘솔 [계정 관리] → 추가 후 **연결**, 또는 SQL 1문장:
   ```sql
   insert into public.sl_admins (email, role, note, user_id)
   select lower(u.email), 'admin', '관리자 교체', u.id
     from auth.users u
    where lower(u.email) = lower('새_관리자_이메일')
      and u.email_confirmed_at is not null
   on conflict (lower(email))
   do update set user_id = excluded.user_id, role = 'admin';
   ```
   화이트리스트에 **이메일만 있고 `user_id` 가 없으면 권한이 전혀 없다**(0004 설계).
3. **(오너) 새 계정으로 `/admin/` 로그인** → 헤더 **[비밀번호 변경]** 으로 임시 비밀번호를 교체한다.
4. **(오너) 새 계정으로 로그인한 상태에서** [계정 관리] → 기존 계정 삭제.

`0004` 에 잠김 방지 장치가 있어 순서를 어기면 **막힌다**(설계된 동작이다):
- `자신을 삭제할 수 없습니다` — 로그인한 본인 계정은 못 지운다 → 3번을 먼저 해야 한다
- `로그인 가능한 admin 이 한 명뿐입니다` — 마지막 admin 은 못 지운다 → 2번이 끝나야 한다

⚠ 이 Supabase 프로젝트는 **다른 서비스와 공유**한다. Authentication → Users 목록에는 이 사이트와
무관한 계정도 있다. 지울 때 대상을 반드시 확인한다.

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
- **폰트 규칙(2026-07-31 정비)**
  · 폰트 스택을 직접 적지 않는다. `var(--font-sans|--font-mono|--font-serif)` 만 쓴다.
    모노·세리프 스택 2순위에 한글 폰트가 들어 있어, 라벨에 한글이 섞여도 서체가 튀지 않는다.
  · 굵기는 **600 이 볼드 끝**이다. 700 페이스는 로드하지 않으므로 700 을 쓰면 합성 볼드가 된다.
  · 한글 라벨은 모노+넓은 자간을 쓰지 않는다. 보정 목록(site.css "한글 라벨 보정")에 넣거나,
    한글·라틴이 섞이는 자리라면 마크업에 `.ko` 를 붙인다.
  · 보정 목록의 `html ` 접두를 지우지 말 것 — site.css 가 페이지 <style> 보다 먼저 로드돼
    특정도가 같으면 지기 때문이다.
  · 폰트 요청(`tools/shell.py` FONTS)은 **실제 쓰는 페이스만** 담는다. 렌더 차단 스타일시트다.
- **카피 규칙(2026-07-31 정비)** — 조사 근거는 커밋 메시지 참조
  · 히어로는 짧게. 주어를 회사명으로 두지 않는다(대기업 비전문 문법이라 신생사가 쓰면 허세로 읽힌다).
  · 서비스 설명의 주어는 **쉴더스랩**(3인칭). **“저희”는 인사말·CTA·고지에만** 쓴다.
  · “A가 아니라 B” 대구는 페이지당 1회 이하. 같은 리듬이 반복되면 사람이 쓴 글로 안 읽힌다.
  · **대개·대부분·많은 조직 금지.** 실적이 없으므로 통계형 주장을 할 자격이 없다. 조건문으로 쓴다.
  · 문단 마지막을 잠언으로 닫지 않는다. 행동·수치·문서 이름으로 착지한다.
  · 지어내면 안 되는 것 = 수행 건수·고객사·경력·자격. 써도 되는 것 = **정책 수치**
    (재점검 1회, 회신 24시간, 보존 기간, 산출물 수).
  · **인원 규모를 전제하는 표현 금지**(“한 팀에서”, “수행 인력 배정”). 1인이어도 참인 문장으로 쓴다.
- **카피에서 설립 시기·실적 유무를 앞세우지 않는다(2026-07-31 오너 방침).**
  인력이 경험자이므로 "신생이라 실적이 없다 → 대신 공개한다"는 방어적 프레임을 쓰지 않는다.
  공개하는 내용(방법론·산출물·못 하는 일·자격 미보유 사실)은 **그대로 유지**한다 — 지위를 정확히
  밝히는 것이 신뢰의 근거다. 다만 없는 경력·자격·인원을 채워 넣는 것은 여전히 금지.
  설립 연도는 기업정보 표와 JSON-LD 에 사실로 남긴다(숨기는 것이 아니라 앞세우지 않는 것).
- **CMS 문구를 고쳤으면 `python3 tools/sync-content.py --sql` 로 DB 도 함께 갱신한다.**
  코드만 고치면 빌드가 DB 값으로 덮어써서 **수정이 조용히 사라진다**(실제로 겪음).
  🚨 **단, 오너가 콘솔을 쓰기 시작한 뒤로는 무턱대고 돌리면 안 된다.** 이 도구는 코드→DB 한 방향이라
  오너가 고쳐 둔 문구를 되돌려 버린다(`where value =` 조건은 *SQL 생성 이후*의 변경만 막는다).
  2026-08-08 기준 코드와 다른 14블록(각 페이지 `*.hero_title`/`hero_lead` 계열)은 **전부 오너 편집분**이다.
  내가 코드 문구를 실제로 고친 게 아니라면 리포트의 “차이”는 정상이다 — 그대로 두라.
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

**페이지 문구 CMS — 0005 적용 후 실측 (2026-07-30)**

| 검증 | 결과 |
|---|---|
| SQL 에디터 실행(postgres · Primary Database) | ✅ "Success. No rows returned" |
| anon 조회 | ✅ 18행 — 회사소개 4 · 인사말 4 · 서비스 2 · 푸터 1 · 법인 정보 7 |
| anon `PATCH` | ✅ 200 이지만 **0행 반환 · 값 불변**(RLS 차단) |
| anon `POST` | ✅ 401 |
| anon `DELETE` | ✅ 204 이지만 **0행 · 대상 행 그대로**. PostgREST 는 0행 삭제도 204 를 준다 — **상태코드만 보고 성공으로 오판하지 말 것** |
| anon `sl_audit` 조회 | ✅ 0행 |
| 빌드가 DB 값을 구워 넣는가 | ✅ "콘텐츠 블록 18개 조회 · 값이 채워진 것 12개" |
| 왕복 무손실 | ✅ 태그 제거·공백 정규화 후 `/about/` 텍스트가 적용 전과 **완전 동일**(3,370자) |
| **클라이언트 하이드레이션 E2E** | ✅ `about.message_role` 을 DB 에서만 바꾸자 **정적 HTML 은 옛 문구, 브라우저는 새 문구** 렌더 → 즉시 반영 경로 실증. 확인 후 원래 값으로 되돌렸고 라이브 재확인함 |

**관리자 콘솔 적대적 검증 (2026-08-08 · 4관점 37 에이전트, 반증 통과분만 채택)**

확정된 high 2건은 **같은 뿌리**였다 — `db.rpc()` 가 돌려주는 PostgrestBuilder 는
Promise 가 아니라 **thenable** 이다. `then()` 만 있고 `catch()` 가 없다(실측:
`typeof builder.catch === "undefined"`, `builder instanceof Promise === false`).
그래서 `audit()` 의 `db.rpc(...).catch(...)` 가 호출 즉시 TypeError 를 **동기적으로** 던졌다.

| 끊긴 곳 | 증상 |
|---|---|
| 로그인 | `audit("login")` 이 `loadDash()/loadInq()/loadApp()` **직전**에서 던져 콘솔이 빈 화면. 거부가 이미 숨겨진 로그인 알림칸으로 흘러가 **무증상** |
| 로그아웃 | `signOut()` 에 도달 못 함 → 세션이 `localStorage` 에 남고 자동 갱신됨. 공용 PC 위험 |
| 비밀번호 변경 | 서버는 성공인데 화면은 실패로 표시 · 모달이 안 닫혀 평문 비밀번호가 DOM 에 잔존 |

`audit()` 를 `Promise.resolve()` 로 감싸고 `try` 로 막아 **절대 던지지 않게** 고쳤다.
호출부 13곳이 전부 fire-and-forget 이라 한 곳 수정으로 전 경로가 해소된다.
로그아웃 체인에는 `.catch` 를 넣어 `signOut` 실패에도 `reload()` 까지 가게 했다.

> **교훈** — 이 결함이 오래 남은 이유는 '로그인 이후 흐름' 이 한 번도 실행되지 않았기 때문이다.
> 코드 리뷰나 문법 검사로는 잡히지 않는다(문법은 정상이다). 실제로 눌러 봐야 드러난다.
> 앞으로 콘솔을 고치면 **로그인 → 각 탭 → 저장 → 로그아웃** 을 한 번은 돌려 볼 것.

**미검증 (오너 비밀번호 필요)**
- `/admin/` **로그인 이후 흐름 전체** — 대시보드 통계 · 문의 처리 · [페이지 문구] 저장 · 감사 로그 열람.
  계정·권한 결속은 확인됐고(3항 ②) 남은 것은 비밀번호를 넣고 실제로 돌려 보는 일뿐이다.
  비밀번호는 오너만 다루므로 **오너가 한 번 로그인해 확인해야 한다.**
  가장 확인 가치가 높은 경로: **[페이지 문구]에서 한 블록을 고쳐 저장 → 공개 페이지 새로고침**
  (저장 경로 + 하이드레이션 + 감사 로그가 한 번에 검증된다).

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
| 2026-07-30 | 푸터 메뉴에서 **신뢰 센터 링크 제거**(오너 지시). 페이지 `/trust/` 는 **유지** — `.well-known/security.txt` 의 `Policy:` 가 이 URL을 가리켜 삭제하면 취약점 제보 정책이 404가 된다 | — |
| 2026-07-30 | 대표이사 **이성훈** 확정 → `config.js` 반영 + `/about/` 인사말 섹션 신설 · CI 심볼 A/B/C 비교 시트 제시 | **인사말 문안 오너 승인 후 배포**(미배포 로컬 커밋) · 심볼 확정 |
| 2026-07-30 | **페이지 문구 CMS 구축**(`0005` + 빌드 치환 + 클라이언트 하이드레이션 + 관리자 [페이지 문구] 탭, 블록 18개) | **오너가 `0005` 적용해야 동작**(3항 ①⑦) · CI 심볼 여전히 미확정 |
| 2026-07-30 | **`0005` 라이브 적용**(Supabase 대시보드) · DB 값으로 전 페이지 재빌드 · 권한 경계·왕복 무손실·하이드레이션 E2E 검증(6항) | 관리자 콘솔 로그인 후 저장 경로만 미검증(비밀번호는 오너) · CI 심볼 |
| 2026-07-30 | **CI 심볼 확정 — 현행 'S' 유지**(오너 판단). 자산 무변경 | 법인 정보 입력(콘솔) · 도메인 판단 |
| 2026-07-31 | **타이포그래피 전면 정비** — 합성 볼드 제거(b,strong→600) · 폰트 스택 토큰화(57곳) · 한글 라벨 보정이 페이지 CSS 에 밀려 무시되던 문제 수정(html 접두) · `.ko` 유틸리티 도입 · 미사용 페이스 제거(Sans KR 300, Serif) | — |
| 2026-07-31 | **카피 톤 정비** — 국내 보안·전문서비스 사이트 조사(인용 49건) 후 기계적 문형 제거(“A가 아니라 B” 31→13 · 근거 없는 일반화 14→4 · 자기 인용·잠언 제거) · `tools/sync-content.py` 신설 | **CMS 8블록 DB 반영 대기** — `supabase/oneoff/2026-07-31_copy-tone-sync.sql` |
| 2026-07-31 | **신생 프레임 제거**(오너 방침: 경험 많은 인력이므로 새로움을 앞세우지 않음) — 홈 03 섹션·히어로 지표·회사소개 첫 문장 재작성 · **연혁 섹션 삭제** · 신뢰센터 성장 서사 제거 | CMS 8블록 DB 반영 대기(동일 SQL) |
| 2026-07-31 | **명함 비율 재조정** — 심볼 6.2→9.87mm · 워드마크 cap 3.1→4.2 · 국문 사명 병기 · 시안 B 앞면에 회사명 신설 · 도메인 `shilduslab.com` 반영(DOMAIN 상수) | **shilduslab.com 미등록** — 등록·메일 확인 전 인쇄 금지(/brand/ 경고 게재) |
| 2026-07-31 | **한글형(국문 우선·영문 병기) 추가** — CI 락업 6종 · 명함 `--ko` 30종(총 60개) · /brand/ 에 02 Korean lockup 섹션 신설 | — |
| 2026-07-31 | 명함 도메인 **shielduslab.com** 으로 확정·60개 재생성(앞 커밋의 shilduslab 은 오기) | **사이트 도메인 전환** — CNAME·인증서·canonical·CSP·security.txt·JSON-LD |
| 2026-07-31 | **도메인 정본 shielduslab.com 확정** — 코드·콘텐츠 244건 교체(`tools/set-domain.py` 신설) | **DNS 전환 대기**(11항 절차서) · 도메인 확보 후 실행 |
| 2026-08-01 | **도메인 코드 원복(253건)** — `shielduslab.com` 이 제3자(Squarespace) 운영 중임을 실측하고, canonical·og·sitemap 이 남의 도메인을 정본으로 지목하던 상태를 해소 · `/brand/` 인쇄 보류 경고가 `set-domain.py` 에 뒤집힌 것 수정(도메인 리터럴 제거) | **도메인 확보 후 재전환**(11항) |
| 2026-08-01 | **CMS 8블록 DB 반영 완료**(카피 톤 정비 + 신생 프레임 제거가 이제 라이브에 보인다) · 적용 전 `services.hero_lead` 문구 정본 드리프트 1건 발견·해소 | — |
| 2026-08-01 | **사명의 뜻 섹션 신설** — `/about/` 02 Name(SHIELD·US·LAB 3문단) · `/brand/` 01 Name(요약) · CMS 블록 3개 추가(18→21), `0005` 재적용 | — |
| 2026-08-01 | 관리자 로그인 절차 확인·문서화(3항 ②) — 계정 결속·이메일 확인·마지막 로그인 이력 실측 | **오너가 한 번 로그인해 저장 경로 확인**(6항 미검증) |
| 2026-08-01 | 세션 상태 동기화 · **명함 도메인 불일치 복구**(원복이 `build-card.py` 까지 쓸어갔으나 산출물은 미재생성 → 코드를 파일에 맞춤) · `set-domain.py` 교체 대상에서 명함 빌더 분리 | 도메인 확보 → 11항 · 법인 정보 입력 · /team/ |
| 2026-08-08 | 콘솔에 **비밀번호 변경** 추가(헤더 → 모달 → `auth.updateUser`) · 헤더 모바일 정비 · **관리자 주소 교체 절차** 정리(3항 ⑧) · `shilderslab.com` **MX 없음** 실측 | **새 관리자 주소 확정 필요**(메일 수신 가능한 도메인) · 도메인 소유 확인 |
| 2026-08-08 | **아이디 로그인**(`shieldusadmin` → 접미사 규칙으로 이메일 변환) · 적대적 검증에서 **`audit()` 가 콘솔 전체를 끊고 있던 high 결함 발견·수정**(6항) | 계정 주소 확정(도메인 소유 확인) · 오너 로그인 실검증 |
| 2026-08-08 | **타이포 정비**(`.d1` 클래스 충돌·모노에 한글·합성 볼드 — 실측 0건까지) · **관리자 [페이지 문구] 커버리지 21→37블록**(홈 등 8페이지 앵커 추가) · **방문 로그가 한 건도 안 쌓이던 문제 수정**(PostgrestBuilder 지연 실행) · [오늘 방문] 상세 · 문구 입력 가이드/미리보기 · **홈 인트로(8초)** | 인트로 길이는 `intro.js` 의 TOTAL 한 줄로 조절 |
| 2026-08-08 | 인트로 5초·입체 강화(22레이어 압출) · **명함 전부를 콘솔 [명함] 탭 하나로 통합**(60링크) · `/brand/` 를 인쇄 사양 대신 **CI 규정 8절**로 재구성 | — |
| 2026-08-08 | **[인기 페이지]에 페이지 이름 병기**(경로 위에 이름, 상위 묶음까지 — 이름표는 빌드 생성물) · **콘솔에서 비밀번호 재설정**(0006 + Edge `set_password`) · Edge 가 자동 주입 service_role 로 폴백해 **Secret 입력이 없어짐** | 🔒 **0006 적용 + `sl-admin-user` 배포**를 해야 동작(12항) |
| 2026-08-08 | **홈 본문이 콘솔에 없던 문제 해결** — “규제와 공격, 양쪽에서 봅니다” 등 홈 6개 섹션 제목·리드 12블록 추가(**37→49**), `0005` 재적용·재빌드 | 🚨 이후 **`sync-content.py` 를 무턱대고 돌리지 말 것** — 코드와 다른 14블록은 오너 편집분(10항) |

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

**2) ~~대표이사 인사말~~ — ✅ 작성 완료 (2026-07-30) · 오너 문안 확인 대기**
대표이사 **이성훈**. `config.js` COMPANY.ceo 입력 → 전 페이지 푸터 사업자정보에 "대표자 이성훈" 자동 렌더.
`/about/` 에 `02 / Message` 섹션 신설(이하 라벨 03~05 로 밀림). 서명은 "쉴더스랩 대표이사 / 이성훈".
문안은 사이트 기존 논조를 따랐고 **실적·경력·자격을 일절 지어내지 않았다** — 회사의 태도(할 수 없는 일은
말하지 않는다 / 확인하지 않은 것은 쓰지 않는다)만 서술했다.
> 본인 명의로 나가는 글이므로 **오너가 문안을 읽고 승인한 뒤 배포**한다. 수정은 `content_pages.py` 의
> `02 / Message` 섹션에서 하고 재빌드한다.

**3) ~~CI 심볼 재검토~~ — ✅ 종결: 현행 'S' 유지 (2026-07-30 오너 확정)**
16/32/64px + 역상 + 브라우저 탭 시뮬레이션 비교 시트를 만들어 A(S 현행) · B(U) · C(US) 세 안을 제시했고,
**오너가 A(현행 S 유지)를 선택**했다. 자산은 하나도 바뀌지 않았다.

실측 기록(64 그리드, 각인 잉크 폭/높이): S 22.6/28.6 · U 22.4/28.1 · US 29.2/17.2.
US 는 cap 을 16.5 로 줄여야 들어가고 그 결과 실드 안에서 시각적으로 약간 위로 뜬다.

> 다시 논의가 열릴 경우를 위해: 각인 글자는 **`build-ci.py` 와 `build-card.py` 두 곳에 각각 하드코딩**되어 있다
> (`build-ci.py` 91~97·197~199 / `build-card.py` 115·127). 한쪽만 고치면 **명함 30종만 옛 각인으로 남는다** —
> 사명 표기 변경 때 실제로 겪은 사고와 같은 구조다. 바꾸게 되면 두 파일을 함께 고치고 두 빌더를 모두 돌린 뒤,
> `assets/ci/` 와 `assets/ci/card/` 를 **둘 다** 눈으로 확인할 것.

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

---

## 11. 도메인 전환 — shilderslab.com → shielduslab.com

**최종 정본은 `shielduslab.com`** (2026-07-31 오너 확정). 옛 도메인은 **보유하면서 301 리다이렉트**.
**단, 도메인 확보 전까지 코드는 `shilderslab.com` 을 유지한다**(아래 현재 상태 참조).

### 현재 상태 (2026-08-01 갱신)
| 항목 | 상태 |
|---|---|
| 코드·콘텐츠 | ↩️ **`shilderslab.com` 으로 되돌림** (253건). 도메인 확보 전까지는 라이브 도메인을 정본으로 둔다 |
| `CNAME` · Pages 바인딩 | `shilderslab.com` (인증서 approved · https 강제) — 그대로 |
| 도메인 확보 | ⏳ **미확보.** `shielduslab.com` 은 **제3자(Squarespace)가 "곧 출시 예정" 페이지를 서비스 중**이다(2026-08-01 실측: 200, `Server: Squarespace`, 우리 자산 경로는 401) |
| 명함 | 새 도메인(`shielduslab.com`)으로 제작 완료 — 60개. `/brand/` 에 **발주 보류 경고** 게재 중 |

> 🚨 **되돌린 이유.** 코드 전환이 도메인 확보보다 먼저 나가 있었다. 그 상태에서는 라이브 사이트의
> `canonical`·`og:url`·`sitemap`·JSON-LD 가 **남이 운영 중인 도메인을 정본으로 지목**한다.
> 아무 데도 가리키지 않는 것보다 나쁘다 — 크롤러가 canonical 을 따르면 색인이 그쪽으로 넘어간다.
> **도메인이 손에 들어온 뒤에 다시 전환한다:**
> ```bash
> python3 tools/set-domain.py --to shielduslab.com --apply && python3 tools/build-pages.py
> ```
>
> ⚠ `set-domain.py` 는 **본문 산문의 도메인까지** 바꾼다. `/brand/` 인쇄 보류 경고가 실제로
> 거꾸로 뒤집혀("명함에는 shilderslab.com 이 새겨져 있으나…") 한 번 사고가 났다.
> 지금은 주소를 적지 않고 "전환 예정 도메인"으로 쓴다. 설명문에 도메인 리터럴을 넣지 말 것.

### 실행 순서 — 이 순서를 지킨다

**① DNS 먼저** (새 도메인 관리 콘솔)
```
A     @     185.199.108.153
A     @     185.199.109.153
A     @     185.199.110.153
A     @     185.199.111.153
CNAME www   duelspost-droid.github.io.
```
> 🚨 **MX 레코드를 지우지 말 것.** 새 도메인에는 Google Workspace 메일(`smtp.google.com`)이
> 이미 걸려 있다. A 레코드는 **추가**하는 것이지 전체 교체가 아니다. 지우면 메일이 끊긴다.

전파 확인(권위 NS 와 공용 리졸버 양쪽):
```bash
dig +short shielduslab.com A
dig +short @8.8.8.8 shielduslab.com A
dig +short shielduslab.com MX     # 비어 있으면 안 된다
```

**② DNS 가 응답한 뒤에 Pages 커스텀 도메인 교체**
```bash
gh api -X PUT repos/duelspost-droid/shilderslab-www/pages -f cname=shielduslab.com
gh api repos/duelspost-droid/shilderslab-www/pages --jq '.https_certificate.state'
gh api -X PUT repos/duelspost-droid/shilderslab-www/pages -F https_enforced=true   # approved 후
```
> 🚨 **DNS 보다 먼저 커스텀 도메인을 설정하면 `https_certificate.state` 가 `null` 로 굳어
> 영영 발급되지 않는다.** 그 상태가 되면 `-f cname=""` 로 비웠다가 다시 설정해 재트리거한다.
> 이 PUT 은 레포 main 에 CNAME 커밋을 자동 생성하므로 다음 push 전에 `git rebase origin/main`.

**③ 옛 도메인 301** — 가비아 DNS 관리에서 `shilderslab.com` URL 포워딩 → `https://shielduslab.com`
(301 영구이동). 포워딩 설정 전까지 옛 주소는 404 가 된다 — ②와 붙여서 처리한다.

**④ 마무리**
- Supabase Edge `sl-admin-user` 를 배포한다면 **전환 후에** 한다(CORS 가 새 도메인 고정).
- Google Search Console 에 새 속성 등록 + 사이트맵 제출.
- `/brand/` 명함 섹션의 발주 보류 경고 제거.

### 되돌리기
```bash
python3 tools/set-domain.py --to shilderslab.com --apply && python3 tools/build-pages.py
gh api -X PUT repos/duelspost-droid/shilderslab-www/pages -f cname=shilderslab.com
```

---

## 12. 콘솔에서 계정 만들기 · 비밀번호 재설정 (2026-08-08)

### 무엇이 되는가
[계정 관리] 탭에서 admin 역할이 다음을 한다.
- **계정 생성** — 이메일·역할·메모 + 임시 비밀번호 자동 생성(기존 기능)
- **비밀번호 재설정** — 담당자가 잊었을 때 임시 비밀번호를 새로 발급(신규)
- **내 비밀번호 변경** — 헤더와 내 계정 행 양쪽에서 같은 모달

왜 필요했나: 재설정 메일 경로가 이 프로젝트에서는 사실상 막혀 있다.
커스텀 SMTP 가 꺼져 있어 **시간당 2통**이고, `shilderslab.com` 에는 **MX 가 없어** 회사 주소로는
아예 받지 못한다(6항 실측). 대시보드는 오너만 들어간다.

### 전제 두 가지 — 둘 다 해야 동작한다

**① 마이그레이션 `0006_shilderslab_admin_password.sql` 적용**
```sql
select proname from pg_proc where proname in ('sl_admin_pw_uid','sl_admin_pw_logged');  -- 2행
```

**② Edge 함수 `sl-admin-user` 배포** — 대시보드 → Edge Functions → Deploy →
이름 `sl-admin-user` → `supabase/functions/sl-admin-user/index.ts` 내용 붙여넣기 →
**Verify JWT 토글 OFF**(브라우저 CORS preflight 에는 JWT 가 없어 401 이 된다. 대신 함수가
호출자 토큰으로 `is_sl_owner()` 를 확인한다).

> 🔑 **Secret 을 넣을 필요가 없다.** `SUPABASE_SERVICE_ROLE_KEY` 는 Supabase 가 Edge 런타임에
> 자동 주입한다. 예전 주석은 `SL_SERVICE_ROLE_KEY` 를 손으로 넣으라고 했으나, 그러면 오너가
> service_role 키를 직접 복사해 옮겨야 했다. 이제 자동 주입값으로 폴백한다
> (굳이 다른 키를 쓰고 싶을 때만 `SL_SERVICE_ROLE_KEY` 를 넣으면 그쪽이 우선한다).

배포 전에는 버튼을 눌러도 "함수가 배포되지 않았습니다" 안내가 뜬다 — 조용히 실패하지 않는다.
(미배포 프로젝트는 CORS preflight 단계에서 막혀 상태코드가 0 으로 오므로, 404 만 보면 이 안내를
놓친다. `notDeployed()` 가 두 갈래를 모두 인정한다 — 실측으로 확인한 동작이다.)

### 안전 장치 (공유 프로젝트라 중요하다)
비밀번호를 **누구에게** 바꿔도 되는지는 Edge 가 아니라 **DB 가 판정한다**(`sl_admin_pw_uid`).
- 우리 화이트리스트(`sl_admins`) 밖 계정 → `null` → Edge 가 404 로 멈춘다.
- **`pw_managed` 가 아닌 계정 → 거부.** ← 적대적 검토가 잡아낸 진짜 구멍
- 로그인 계정이 없는 빈 슬롯 → 거부
- 자기 자신 → 거부(자기 비밀번호는 재인증 정책을 그대로 거치는 [비밀번호 변경] 으로)

> 🚨 **화이트리스트만으로는 경계가 되지 않는다.** `sl_admins` 는 admin 이 임의 이메일로
> 채울 수 있는 목록이다. 그래서 admin 이 ① 공유 프로젝트에 있는 **남의 서비스 사용자 이메일**을
> [관리자 추가](로그인 생성 체크 해제)로 넣고 ② 그 사람의 기존 계정이 결속되면
> ③ 비밀번호를 바꿔 **계정을 탈취**할 수 있었다. 재설정 기능이 없던 때는 ①②가
> "우리 콘솔 접근 허용" 에 그쳤는데, 재설정이 생기면서 같은 동작의 의미가 달라진 것이다.
> → `sl_admins.pw_managed` 를 두어 **이 사이트가 직접 만든 계정만** 재설정 대상으로 좁혔다.
> 콘솔에서 새로 만들면 켜지고, [연결]로 기존 계정을 갖다 붙이면 켜지지 않는다.
> 0006 은 적용 시점의 기존 목록만 1회 백필한다(그 목록은 오너가 직접 관리해 온 우리 계정들이다).
- **마지막 admin 은 막지 않는다.** 삭제와 달리 재설정은 계정을 없애지 않아 락아웃을 만들지 않고,
  관리자가 한 명뿐일 때야말로 가장 필요하다. 그래서 삭제용 `sl_admin_login_uid` 를 재사용하지 않고
  함수를 따로 뒀다.

감사 로그는 **실제로 바뀐 뒤에만** `admin_password_reset` 으로 남는다(`sl_admin_pw_logged`).
비밀번호 값도 길이도 남기지 않는다.

### 인기 페이지 이름 병기
`admin/page-titles.js` 는 **빌드 생성물**이다(`tools/build-pages.py`). 손으로 고치지 마라 —
페이지를 추가하면 저절로 따라온다. 빌드 이후 콘솔에서 발행한 인사이트만 콘솔이 DB 에서 제목을 보충한다.
표에 없는 경로(봇이 긁는 `/wp-admin/` 같은 404 흡수 경로)는 경로만 보인다 — 정상이다.
