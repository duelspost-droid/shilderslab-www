# 쉴더스랩 웹사이트 — 일반 서버 이관 명세서

| 항목 | 내용 |
|---|---|
| 문서 버전 | 1.0 |
| 작성일 | 2026-10-02 |
| 대상 독자 | 서버를 구축·운영할 엔지니어, 호스팅·SI 업체 |
| 관련 파일 | `deploy/` 디렉터리 전체 (부록 B) |
| 정본 저장소 | `github.com/duelspost-droid/shilderslab-www` (main) |

> 이 문서만 보고 서버를 새로 세울 수 있도록 썼다.
> ⚠ 저장소가 public 이라 **레이트리밋 임계값 같은 수치는 본문에 적지 않고** 설정 파일을 가리킨다(HANDOFF 규칙). 모든 수치는 현재 운영 중인 설정과
> 마이그레이션 파일에서 **실측해 옮긴 값**이다. 추정한 값은 그렇다고 표시했다.

## 0. 구성 선택지 — 먼저 결정할 것

선택할 수 있는 것은 **두 가지 축**이고, 서로 독립이다. 나머지는 고정이다.

| 축 | 선택지 | 권장 |
|---|---|---|
| **① 설치 방식** | **A. Docker Compose** — 구성요소 5개를 컨테이너로 한 번에 올린다 | ✅ |
| | **B. 직접 설치** — 각 구성요소를 OS 에 설치하고 systemd 로 띄운다(부록 C) | 컨테이너 금지 환경일 때 |
| **② 웹 서버** | **nginx** | ✅ |
| | **Apache httpd 2.4** (부록 C.3, `deploy/apache/site.conf`) | 사내 표준이 Apache 일 때 |

조합별 준비 상태

| 조합 | 제공 파일 | 비고 |
|---|---|---|
| **A + nginx** | `docker-compose.yml` + `nginx/site.conf` | **가장 빠르다.** 파일 그대로 `up` 하면 된다 |
| B + nginx | `nginx/site.conf` (upstream 주소만 `127.0.0.1` 로) | 부록 C.1~C.2 |
| B + Apache | `apache/site.conf` | 부록 C.3. **레이트리밋 모듈 별도 필요** |
| A + Apache | 미제공 | 가능은 하다(compose 의 `web` 을 `httpd` 이미지로 교체). 굳이 그럴 이유가 없어 만들지 않았다 |

**고정 — 선택 불가**

| 구성요소 | 이유 |
|---|---|
| PostgreSQL 16 | 스키마가 PostgreSQL 전용 기능(RLS·SECURITY DEFINER·jsonb)에 묶여 있다. MySQL·Oracle 불가(2.2항) |
| PostgREST · GoTrue · Deno 함수 | 지금 쓰는 것과 같은 제품이라 프런트를 고치지 않아도 된다(2.3~2.5항) |
| WAS(Tomcat 등) | **필요 없다.** Java 애플리케이션이 없다(2.1항, 부록 C.4) |

---

## 1. 개요

### 1.1 목적과 범위
현재 사이트는 **GitHub Pages(정적 호스팅) + Supabase(관리형 백엔드)** 두 곳에 나뉘어 있다.
이를 **단일 일반 서버(VPS·IDC·사내 서버)** 로 옮긴다.

이관 대상
- 정적 웹사이트 28개 페이지와 자산(약 2.4MB)
- 데이터베이스 — 테이블 8 · 함수 27 · RLS 정책 18 (모두 최종 상태, 13항 실측)
- 로그인(관리자 인증)
- 서버 함수 1종(관리자 계정 생성·삭제·비밀번호 재설정)

### 1.2 현재 구성 (As-Is)

```
 방문자 브라우저
   │
   ├─ HTML/CSS/JS ─────────▶ GitHub Pages  (shilderslab.com, Let's Encrypt)
   │
   └─ API (supabase-js) ───▶ Supabase 관리형 (us-east-1 추정, 12항 참조)
                               ├ PostgREST   /rest/v1      테이블 조회·RPC
                               ├ GoTrue      /auth/v1      관리자 로그인
                               ├ Edge Fn     /functions/v1 관리자 계정 관리
                               └ PostgreSQL               데이터 저장
```

### 1.3 목표 구성 (To-Be)

```
 방문자 브라우저
   │  HTTPS 443
   ▼
 ┌─────────────────────── 일반 서버 1대 ───────────────────────┐
 │                                                             │
 │  nginx (웹 서버 · 리버스 프록시 · TLS 종단)                  │
 │   ├ /            → 정적 파일 (/var/www/site)                 │
 │   ├ /rest/v1/    → PostgREST   :3000                         │
 │   ├ /auth/v1/    → GoTrue      :9999                         │
 │   └ /functions/v1/sl-admin-user → Deno 서비스 :8080          │
 │                                                             │
 │  PostgreSQL 16  :5432  (외부 비공개)                          │
 └─────────────────────────────────────────────────────────────┘
```

**프런트엔드 코드는 거의 바꾸지 않는다.** 브라우저의 supabase-js 는 `{URL}/rest/v1`·`/auth/v1`·
`/functions/v1` 경로로 호출하는데, nginx 가 같은 경로를 받아 내부 서비스로 넘기기 때문이다.
바꾸는 것은 `config.js` 의 API 주소·공개 키, 그리고 페이지 CSP 의 `connect-src` 두 가지뿐이다.

### 1.4 이관하지 않는 것
| 대상 | 사유 |
|---|---|
| Supabase Realtime | 사이트에서 쓰지 않는다(코드 실측: `channel()`·`realtime` 0건) |
| Supabase Storage | 쓰지 않는다(`.storage` 0건). 이미지·PDF 는 전부 정적 파일 |
| `notify-inquiry` Edge 함수 | 지금도 **미배포**다. 필요해지면 adminfn 과 같은 방식으로 추가한다 |
| Supabase 대시보드 | 운영 도구일 뿐 서비스 구성요소가 아니다. 대체는 10항(운영) |

---

## 2. 기술 스택 결정과 근거

### 2.1 웹 서버 — **nginx** (권장)

이 사이트에는 **Java·JSP·Servlet 코드가 한 줄도 없다.** 페이지는 빌드 시점에 Python 이
만들어 둔 순수 HTML 이고, 동적 처리는 전부 PostgreSQL 함수와 두 개의 독립 서비스(Go·Haskell
바이너리)가 맡는다. 따라서 **WAS(Tomcat·JEUS·WebLogic)는 필요 없다.**

| 후보 | 판정 | 이유 |
|---|---|---|
| **nginx 1.27** | ✅ **권장** | 정적 파일 서빙과 리버스 프록시가 본업. 설정 한 파일(`nginx/site.conf`)로 TLS·보안 헤더·레이트리밋·API 라우팅을 모두 처리한다 |
| Apache httpd 2.4 | ⭕ 가능 | 같은 일을 `mod_proxy`·`mod_ssl`·`mod_headers` 로 할 수 있다. 사내 표준이 Apache 라면 써도 된다 — **부록 C** 에 대응 설정을 실었다. 단 레이트리밋은 `mod_evasive` 등 별도 모듈이 필요하다 |
| Caddy 2 | ⭕ 가능 | 인증서 자동 발급·갱신이 내장돼 운영이 가장 간단하다. 다만 국내 운영 인력에게 익숙하지 않을 수 있다 |
| Tomcat 등 WAS | ❌ 부적합 | 서빙할 Java 애플리케이션이 없다. JVM 을 상주시키는 비용(메모리 512MB~)만 생기고 얻는 것이 없다. 정적 파일 서빙 성능도 nginx 보다 떨어진다 |

### 2.2 데이터베이스 — **PostgreSQL 16** (필수, 대체 불가)

**MySQL·MariaDB·Oracle·MSSQL 로는 옮길 수 없다.** 스키마가 PostgreSQL 전용 기능에
깊게 의존하기 때문이다(마이그레이션 파일 실측).

| PostgreSQL 전용 기능 | 사용 횟수 | 다른 DB 로 옮기면 |
|---|---|---|
| Row Level Security (행 단위 보안 정책) | 테이블 8개 전부 · 정책 18개 | MySQL·MariaDB 에는 RLS 가 없다. **보안 모델 전체를 애플리케이션 코드로 다시 짜야 한다** |
| `SECURITY DEFINER` 함수 | 29회 | 개인정보 테이블은 이 함수로만 쓰기가 허용된다. 동등 기능 없음 |
| `jsonb` | 40회 | 감사 로그·설정값. MySQL `JSON` 과 연산자가 다르다 |
| `gen_random_uuid()` | 4회 | 기본키 생성 |
| PostgREST | 전 API | **PostgreSQL 전용 제품**이다. DB 를 바꾸면 API 계층 전체를 새로 써야 한다 |

버전 하한은 **PostgreSQL 13** 이다(`gen_random_uuid` 내장). 운영 지원 기간을 고려해 **16** 을 쓴다.
관리형 DB(AWS RDS·Azure·NCP Cloud DB for PostgreSQL)도 가능하나, **13항의 롤 생성 권한**이 필요하다.

### 2.3 API 계층 — **PostgREST 12.2**
PostgreSQL 스키마를 그대로 REST API 로 노출하는 단일 바이너리(Haskell). 현재 Supabase 가
내부적으로 쓰는 것과 **같은 제품**이라 동작이 바뀌지 않는다. 직접 코딩한 API 가 없으므로
이것을 대체하려면 테이블 6개 조회와 RPC 17개를 백엔드 코드로 새로 구현해야 한다.

### 2.4 인증 — **GoTrue 2.158** (Supabase Auth)
현재 쓰는 인증 서버와 **같은 제품**이다. 관리자 계정·비밀번호 해시(bcrypt)를 그대로 옮길 수 있어
**관리자가 비밀번호를 다시 정할 필요가 없다.** 스키마가 `auth.users` 를 직접 조인하므로
(8회) 다른 인증 방식으로 바꾸려면 0004·0006 마이그레이션을 다시 써야 한다.

### 2.5 서버 함수 — **Deno 2.1**
`supabase/functions/sl-admin-user/index.ts`(268줄)를 **코드 수정 없이** 그대로 실행한다.
이 코드는 모의해킹 확증 수정(0007)을 거쳤다. 다른 언어로 옮겨 쓰면 fail-closed·롤백·
"삭제 대상은 DB 가 판정" 같은 보안 성질을 놓칠 위험이 커서 이식하지 않는다.
(이관을 위해 바꾼 것은 CORS 출처를 환경변수로 받게 한 1곳뿐이다.)

### 2.6 배포 방식 — **Docker Compose** (권장) / 직접 설치(가능)
위 다섯 구성요소의 **버전을 고정**하고 한 번에 올리기 위해 Docker Compose 를 쓴다.
사내 정책상 컨테이너를 쓸 수 없다면 **부록 C** 의 직접 설치 절차를 따른다.

| 구성요소 | 이미지(고정 버전) | 실재 확인 |
|---|---|---|
| DB | `postgres:16` | ✅ Docker Hub |
| 인증 | `supabase/gotrue:v2.158.1` | ✅ |
| API | `postgrest/postgrest:v12.2.3` | ✅ |
| 웹 | `nginx:1.27-alpine` | ✅ |
| 함수 | `denoland/deno:alpine-2.1.4` | ✅ |

---

## 3. 서버 사양

### 3.1 하드웨어
트래픽은 회사 소개 사이트 수준(일 수백~수천 PV)을 전제로 한다. 아래 메모리 수치는
각 구성요소의 통상 상주량을 합산한 **추정치**이며, 구축 후 `docker stats` 로 실측해 조정한다.

| 구분 | 최소 | 권장 | 비고 |
|---|---|---|---|
| vCPU | 1 | **2** | 1코어도 동작하나 백업·인증서 갱신이 겹치면 지연된다 |
| 메모리 | 2 GB | **4 GB** | PostgreSQL 200~500MB · GoTrue/PostgREST 각 ~30MB · Deno ~50MB · nginx ~10MB (추정) |
| 디스크 | 20 GB SSD | **40 GB SSD** | OS·이미지 ~8GB, DB 는 현재 1MB 미만. 백업 보관분을 감안 |
| 네트워크 | 공인 IPv4 1개 | 공인 IPv4 + IPv6 | |

### 3.2 운영체제
| 권장 | 대안 |
|---|---|
| **Ubuntu Server 24.04 LTS** (지원 2029-04) | Rocky Linux 9 / RHEL 9 (부록 C 의 패키지 명령이 다르다) |

필수 패키지: Docker Engine 27+ · Docker Compose v2 · certbot · git · python3(빌드용)

### 3.3 네트워크·방화벽

| 방향 | 포트 | 용도 | 허용 대상 |
|---|---|---|---|
| 인바운드 | 80/tcp | HTTP → HTTPS 리다이렉트, 인증서 발급 검증 | 전체 |
| 인바운드 | 443/tcp | HTTPS 서비스 | 전체 |
| 인바운드 | 22/tcp | SSH 관리 | **관리자 IP 만** |
| 아웃바운드 | 443/tcp | Let's Encrypt · Docker 이미지 · Google Fonts | 전체 |
| 아웃바운드 | 587/tcp | 비밀번호 재설정 메일(SMTP) | 메일 서버 |

> 🚨 **5432(PostgreSQL)·3000·9999·8080·8081 은 절대 외부에 열지 않는다.**
> compose 는 이 포트들을 `expose`(내부망)로만 열고 `ports`(외부 공개)로 열지 않도록 짜여 있다.
> 클라우드 보안그룹·ufw 에서도 80·443·22 외에는 막는다.

### 3.4 도메인·DNS·TLS

| 항목 | 값 |
|---|---|
| 서비스 도메인 | `shielduslab.com` (전환 예정, **현재 미확보**) / `shilderslab.com` (현행) |
| DNS 레코드 | `A @ → 서버 공인 IP` · `A www → 서버 공인 IP` (또는 CNAME www → @) |
| 🚨 MX 레코드 | **기존 Google Workspace MX 를 지우지 말 것.** A 레코드를 *추가*하는 것이지 전체 교체가 아니다 |
| TLS 인증서 | Let's Encrypt (certbot, 90일 자동 갱신) |
| TLS 버전 | TLS 1.2 · 1.3 만 허용 |
| 옛 도메인 | `shilderslab.com` 은 보유하며 **301 영구 리다이렉트** (검색 순위 승계) |

---

## 4. 데이터베이스 상세 명세

### 4.1 인스턴스 설정
| 항목 | 값 | 근거 |
|---|---|---|
| 제품·버전 | PostgreSQL 16 | 2.2항 |
| 문자셋 | UTF8 | 한글 데이터 |
| 타임존 | `Asia/Seoul` | 접수 시각·보존기간 계산 기준 |
| 접속 | 컨테이너 내부망 전용 | 외부 비공개 |
| 확장 | **없음(필수 아님)** · `pg_cron` 선택(4.7항) | `gen_random_uuid()` 는 PG13+ 코어 내장. pgcrypto 전용 함수 사용 0회(실측) — contrib 없는 최소 설치에서도 동작 |

### 4.2 롤(사용자) 명세
관리형 Supabase 가 미리 만들어 두던 롤이다. **맨 PostgreSQL 에는 없으므로**
`deploy/db/01-roles-auth.sql` 이 만든다. 이 파일 없이 마이그레이션을 적용하면 0001 에서 즉시 실패한다.

| 롤 | 로그인 | 역할 | RLS |
|---|---|---|---|
| `authenticator` | ✅ | PostgREST 가 접속하는 계정. JWT 의 `role` 을 보고 아래 셋 중 하나로 전환한다 | 적용 |
| `anon` | ❌ | 비로그인 방문자 | 적용 |
| `authenticated` | ❌ | 로그인한 관리자 | 적용 |
| `service_role` | ❌ | 서버 함수 전용. **RLS 를 우회**한다 | **우회** |
| `supabase_auth_admin` | ✅ | GoTrue 전용. `auth` 스키마 소유자 | — |
| `postgres` | ✅ | 슈퍼유저. 마이그레이션·백업·보존기간 파기에만 쓴다 | 우회 |

### 4.3 스키마
| 스키마 | 소유 | 내용 |
|---|---|---|
| `public` | postgres | 사이트 테이블 8개 · 함수 27개 |
| `auth` | supabase_auth_admin | 로그인 계정(`auth.users`) — **GoTrue 가 첫 기동 시 직접 만든다** · 헬퍼 함수 `auth.uid()`·`auth.jwt()`·`auth.role()`·`auth.email()` |

`auth.uid()`·`auth.jwt()` 는 **RLS 정책 전체가 기대는 함수**다(각 16회·9회 사용).
PostgREST 가 요청마다 넣어 주는 `request.jwt.claims` 설정값에서 JWT 페이로드를 읽는다.

### 4.4 테이블 명세

| 테이블 | 컬럼 | 용도 | 개인정보 | 쓰기 경로 | 보존기간 |
|---|---|---|---|---|---|
| `sl_inquiries` | 14 | 상담·견적 문의 | 🔴 **이름·이메일·전화** | RPC `sl_submit_inquiry` 만 | **1년** 후 자동 파기 |
| `sl_applications` | 14 | 채용 지원 | 🔴 **이름·이메일·전화** | RPC `sl_apply` 만 | **6개월** 후 자동 파기 |
| `sl_audit` | 11 | 방문·관리자 행위·제출 이벤트 로그 | 🟡 IP·User-Agent | RPC `sl_log`·`sl_log_visit` | 방문 **90일** · 관리/제출 **365일** |
| `sl_admins` | 4+ | 관리자 화이트리스트(역할 admin/editor) | 🟡 이메일 | RPC `sl_admin_*` 만 | 수동 |
| `sl_content` | 9 | 페이지 문구 CMS (현재 51블록) | — | 관리자 콘솔 | — |
| `sl_insights` | 12 | 인사이트 글 (현재 3건) | — | 관리자 콘솔 | — |
| `sl_jobs` | 12 | 채용 공고 (현재 2건) | — | 관리자 콘솔 | — |
| `sl_settings` | 3 | 사이트 설정 key-value (현재 4건) | — | 관리자 콘솔 | — |

> 🔴 **개인정보 테이블(`sl_inquiries`·`sl_applications`)에는 INSERT 정책이 아예 없다.**
> 방문자는 `SECURITY DEFINER` RPC 로만 쓸 수 있고, 그 안에서 동의 여부·이메일 형식·길이 상한·
> IP 기준 레이트리밋을 검사한다.
> 테이블 INSERT **권한**은 기본 권한으로 열려 있지만 **INSERT 정책이 없어서 RLS 가 막는다**
> (13항 실측: 공개 키로 직접 INSERT → 거부). 이관 후에도 **이 두 테이블에 INSERT 정책을 만들지 말 것.**

### 4.5 함수(RPC) 명세 — 최종 상태 27개

| 분류 | 개수 | 함수 | 호출 가능 |
|---|---|---|---|
| 공개 쓰기 | 3 | `sl_submit_inquiry` · `sl_apply` · `sl_log_visit` | 비로그인(anon) |
| 관리자 | 14 | `is_sl_admin` · `is_sl_owner` · `sl_my_role` · `sl_my_email` · `sl_stats` · `sl_log` · `sl_admin_list` · `sl_admin_add` · `sl_admin_link` · `sl_admin_set_role` · `sl_admin_remove` · `sl_admin_login_uid` · `sl_admin_pw_uid` · `sl_admin_pw_logged` | 로그인(authenticated) — 함수 내부에서 다시 권한 판정 |
| 보존기간 파기 | 3 | `sl_pii_purge` · `sl_audit_purge` · `sl_purge_all` | **postgres 만** (모든 롤에서 회수) |
| 내부 보조 | 3 | `_sl_client_ip` · `_sl_user_agent` · `_sl_active_owners` | 내부 호출 전용 |
| 트리거 | 4 | `sl_set_updated_at` · `sl_content_touch` · `sl_content_audit` · `_sl_guard_pw_managed` | 트리거 전용 |

> `_sl_client_ip()` 는 **`X-Forwarded-For` 헤더**로 방문자 IP 를 읽는다(레이트리밋 근거).
> 🚨 nginx 가 이 헤더를 넘기지 않으면 **모든 요청이 같은 IP 로 보여 레이트리밋이 무력화**된다.
> `nginx/site.conf` 의 `/rest/v1/` 블록이 이를 설정한다 — 지우지 말 것.

### 4.6 RLS(행 단위 보안) 요약
- 8개 테이블 **전부** RLS 활성, 정책 **18개**(최종 상태 실측).
  마이그레이션에는 `create policy` 문장이 21개 있지만 0004 가 일부를 지우고 다시 만들어 최종은 18개다.
- 🚨 **보안을 맡는 것은 GRANT 가 아니라 RLS 다.** 관리형 Supabase 처럼 public 의 모든 테이블에
  anon·authenticated 권한을 기본으로 주고(`01-roles-auth.sql`), 차단은 RLS 정책이 한다.
  마이그레이션에는 테이블 GRANT 가 **한 줄도 없다**(실측 0건) — 이 기본 권한을 전제로 짜여 있다.
  기본 권한을 빼면 사이트가 빈 화면이 되고(13항 결함 ①), RLS 를 끄면 개인정보가 노출된다.
- 권한은 이메일 문자열이 아니라 **`auth.users.id`(불변 식별자)에 결속**한다(0004).
  화이트리스트에 이메일만 있고 로그인 계정이 연결되지 않은 행은 **권한이 0** 이다.
- 앱 안에서 스스로 관리자가 되는 경로는 의도적으로 없다. **첫 관리자는 SQL 로만** 세운다(7항 4단계).

### 4.7 보존기간 자동 파기
개인정보처리방침에 고지된 보존기간을 지키는 장치다. **법적 의무이므로 반드시 동작시킨다.**

| 방법 | 설정 |
|---|---|
| A. 서버 cron (권장 — 추가 설치 없음) | `/etc/cron.d/shieldus-purge` : `20 3 * * * root docker compose -f /srv/shieldus/deploy/docker-compose.yml exec -T db psql -U postgres -c "select public.sl_purge_all();"` |
| B. pg_cron 확장 | `postgres:16` 이미지에는 없다. pg_cron 이 포함된 이미지로 바꾸고 `shared_preload_libraries='pg_cron'` 설정 후 0003 을 재적용하면 스스로 등록된다 |

현재 관리형 환경에서는 pg_cron 잡 `sl_purge_daily`(매일 03:20 UTC)가 돌고 있다.
**이관 직후 A 를 설정하지 않으면 파기가 멈춘다** — 9항 검증 체크리스트에 포함했다.

---

## 5. 애플리케이션 구성요소 명세

| 서비스 | 이미지 | 내부 포트 | 외부 공개 | 역할 |
|---|---|---|---|---|
| `db` | postgres:16 | 5432 | ❌ | 데이터 저장. 볼륨 `db-data` |
| `auth` | supabase/gotrue:v2.158.1 | 9999 | ❌ (nginx 경유) | 관리자 로그인·JWT 발급·비밀번호 변경 |
| `rest` | postgrest/postgrest:v12.2.3 | 3000 | ❌ (nginx 경유) | 테이블 조회·RPC 를 REST 로 노출 |
| `adminfn` | deno 2.1 (레포 원본 그대로) | 8080 | ❌ (nginx 경유) | 관리자 계정 생성·삭제·비밀번호 재설정 |
| `web` | nginx:1.27-alpine | 80 · 443 · 8081 | ✅ 80·443 만 | 정적 사이트 · TLS · 보안 헤더 · 레이트리밋 · 라우팅 |

### 5.1 서비스 간 의존·기동 순서
```
db (healthy) ─┬─▶ auth ─┐
              └─▶ rest ─┼─▶ adminfn ─▶ web
```
`db` 의 `pg_isready` 헬스체크가 통과해야 나머지가 뜬다.

### 5.2 핵심 설정값 (상세는 부록 A)
| 설정 | 값 | 주의 |
|---|---|---|
| `JWT_SECRET` | 48자 무작위 | **GoTrue 와 PostgREST 가 같은 값**이어야 한다. 다르면 로그인 직후 모든 요청이 401 |
| `ANON_KEY` | JWT(role=anon) | 브라우저 `config.js` 에 들어간다. 공개돼도 RLS 가 막는다 |
| `SERVICE_ROLE_KEY` | JWT(role=service_role) | **RLS 우회 키. 서버 `.env` 에만.** 저장소·브라우저에 두지 않는다 |
| `GOTRUE_DISABLE_SIGNUP` | `true` | 🚨 셀프 가입 차단. 열면 0004 의 권한 설계가 무의미해진다 |
| `PGRST_OPENAPI_MODE` | `disabled` | API 구조(테이블·함수 목록)를 외부에 공개하지 않는다 |

### 5.3 라우팅 (nginx)
| 경로 | 대상 | 레이트리밋 |
|---|---|---|
| `/` | 정적 파일 | — |
| `/assets/` | 정적 파일 (30일 캐시) | — |
| `/admin/` | 정적 파일 (`no-store`) | — |
| `/rest/v1/` | rest:3000 (접두 제거) | IP 기준 — 값은 `nginx/site.conf` |
| `/auth/v1/` | auth:9999 (접두 제거) | IP 기준, REST 보다 엄격 — 무차별 대입 방어 |
| `/functions/v1/sl-admin-user` | adminfn:8080 | — (함수 내부에서 owner 판정) |
| `/functions/*` 그 외 | 404 | — |
| `/tools/` `/supabase/` `/deploy/` `/.git/` | 404 | 저장소 내부 파일 노출 차단 |

---

## 6. 보안 설계

### 6.1 이관으로 **좋아지는** 것
GitHub Pages 의 한계로 지금까지 못 하던 것을 서버에서 직접 설정한다.

| 항목 | 현재(Pages) | 이관 후 |
|---|---|---|
| HSTS | ❌ 설정 불가 | ✅ `max-age=31536000; includeSubDomains` |
| X-Content-Type-Options | ❌ | ✅ `nosniff` |
| X-Frame-Options | ❌ (CSP `frame-ancestors` 로만) | ✅ `DENY` |
| Permissions-Policy | ❌ | ✅ 위치·마이크·카메라 차단 |
| 로그인 레이트리밋 | 관리형 기본값 | ✅ 앞단(nginx)에서 IP 기준 제한 추가 |
| 데이터 위치 | 미국(us-east-1 추정) | ✅ **서버 소재지** — 국내 서버면 국외이전 고지 해소(12항) |

### 6.2 이관으로 **새로 생기는** 책임
관리형 서비스가 대신 하던 일을 이제 직접 해야 한다.

| 책임 | 관리형에서는 | 이관 후 담당 |
|---|---|---|
| OS·패키지 보안 패치 | 해당 없음 | 운영자 — `unattended-upgrades` 권장 |
| DB 백업 | Supabase 일일 백업 | 운영자 — 10.1항 |
| 이미지 버전 갱신 | Supabase | 운영자 — 분기 1회 점검 |
| TLS 인증서 갱신 | GitHub | certbot 자동(점검만) |
| 장애 감시 | Supabase 상태 페이지 | 운영자 — 10.3항 |

### 6.3 반드시 지킬 것
1. **`.env` 와 `SERVICE_ROLE_KEY` 는 저장소에 커밋하지 않는다.** 이 저장소는 public 이다.
2. 5432·3000·9999·8080·8081 을 외부에 열지 않는다(3.3항).
3. `GOTRUE_DISABLE_SIGNUP=true` 를 유지한다.
4. nginx 의 `X-Forwarded-For` 전달을 지우지 않는다(4.5항).
5. 개인정보 테이블에 INSERT 정책을 만들지 않고, RLS 를 끄지 않는다(4.4·4.6항).
6. HSTS `preload` 는 HTTPS 가 안정적으로 도는 것을 **최소 2주 확인한 뒤** 붙인다(되돌리기 어렵다).

---

## 7. 이관 절차

담당: **[오너]** 계정·비밀번호·키가 필요한 일 / **[엔지니어]** 그 외.
예상 소요: 서버 준비 완료 기준 **반나절** (DNS 전파 대기 제외).

### 0단계 — 사전 준비 [오너]
- [ ] 서버 확보(3항 사양) · SSH 접속 확인
- [ ] 도메인 확보 및 DNS 관리 권한 (`shielduslab.com`)
- [ ] Supabase **service_role 키** 또는 DB 접속 문자열 확보 — 개인정보 테이블과 로그인 계정은 이것 없이 내보낼 수 없다(8항)

### 1단계 — 서버 기본 구성 [엔지니어]
```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install ca-certificates curl git python3 certbot ufw
curl -fsSL https://get.docker.com | sudo sh
sudo ufw allow 22/tcp && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp && sudo ufw --force enable
sudo git clone https://github.com/duelspost-droid/shilderslab-www.git /srv/shieldus
```

### 2단계 — 키 생성과 환경 설정 [엔지니어]
```bash
cd /srv/shieldus/deploy
cp .env.example .env
bash scripts/gen-keys.sh >> .env          # JWT_SECRET · ANON_KEY · SERVICE_ROLE_KEY
vi .env                                    # POSTGRES_PASSWORD · PUBLIC_URL · SERVER_NAME · SMTP 채우기
chmod 600 .env
```

### 3단계 — DB·서비스 기동과 스키마 적용 [엔지니어]
```bash
python3 scripts/test-db.py         # (권장) DB 계층 사전 검증 — 13항. 실패하면 진행하지 않는다
python3 scripts/export-public.py   # 🚨 이관 당일 공개 데이터 시드를 다시 뜬다(스냅숏이 낡았을 수 있다)
bash scripts/init-db.sh            # 01 롤 → GoTrue 기동(auth.users 생성 대기) → 0001~0007 → 공개 시드
```
순서가 중요하다. `init-db.sh` 가 **GoTrue 가 `auth.users` 를 만든 것을 확인한 뒤** 0001~0007 을 넣는다.
0004 가 `auth.users` 를 조인하므로 순서가 바뀌면 함수 생성에서 실패한다.

### 4단계 — 데이터 이관 [오너 + 엔지니어]
```bash
# [오너] 관리형 Supabase 에서 전체 덤프 (8항)
SUPABASE_DB_URL='postgresql://postgres:<비밀번호>@db.<ref>.supabase.co:5432/postgres' \
  bash scripts/export-from-supabase.sh
# [엔지니어] 새 서버에 적재
bash scripts/import-to-server.sh export/
```
덤프를 못 받는 경우(최초 구축 등)에는 **첫 관리자를 SQL 로 세운다**(HANDOFF 3항 ② 절차와 동일).

### 5단계 — TLS 인증서 [엔지니어]
```bash
# 최초 발급은 standalone — 이 시점엔 web 이 아직 안 떠 있어 80 포트가 비어 있다(init-db.sh 가 web 을 띄우지 않는다)
sudo certbot certonly --standalone -d shielduslab.com -d www.shielduslab.com
mkdir -p certs certbot-www
sudo cp /etc/letsencrypt/live/shielduslab.com/{fullchain,privkey}.pem certs/
docker compose up -d web
```
⚠ **갱신은 webroot 로 해야 한다.** standalone 으로 발급한 인증서는 갱신도 standalone 으로 시도하는데,
그때는 nginx 가 80 을 잡고 있어 **60일 뒤 조용히 실패**한다. 10.4항의 갱신 명령이 `--webroot` 로 덮어쓴다.

### 6단계 — 프런트엔드 연결 [엔지니어]
```bash
python3 tools/set-domain.py --to shielduslab.com --apply   # 사이트 도메인 일괄 교체
# config.js : SUPABASE_URL → https://shielduslab.com , 공개 키 → 새 ANON_KEY
# tools/shell.py CSP : connect-src 의 *.supabase.co → 'self'
python3 tools/build-pages.py
docker compose restart web
```

> ⚠ `set-domain.py` 는 **코드만** 바꾼다. **DB 에 저장된 값**은 그대로다 —
> 현재 `sl_settings.contact_email` 1건이 구 도메인 주소를 담고 있다(2026-10-02 실측).
> 관리자 콘솔 [설정]에서 새 주소로 고친다. 메일함이 새 도메인에 준비된 뒤에 바꿔야 문의 회신이 끊기지 않는다.

### 7단계 — 검증 [엔지니어] → 9항 체크리스트 전부 통과

### 8단계 — 전환 [오너]
- [ ] DNS A 레코드를 새 서버로 (🚨 **MX 유지**)
- [ ] `shilderslab.com` → `https://shielduslab.com` 301 (가비아 URL 포워딩)
- [ ] 보존기간 파기 cron 등록(4.7항) — **잊으면 법적 보존기간을 넘긴다**
- [ ] 관리형 Supabase 는 **최소 30일 병행 보관 후** 해지(11항 롤백 대비)

---

## 8. 데이터 이관 상세

### 8.1 무엇을 누가 내보내는가

| 데이터 | 건수(2026-10-02 실측) | 내보내기 | 담당 |
|---|---|---|---|
| `sl_content` 페이지 문구 | 51 | ✅ **완료** — `db/03-seed-public.sql` 에 포함 | 이미 됨 |
| `sl_insights` 인사이트 | 3 | ✅ **완료** | 이미 됨 |
| `sl_jobs` 채용 공고 | 2 | ✅ **완료** | 이미 됨 |
| `sl_settings` 설정 | 4 | ✅ **완료** | 이미 됨 |
| `sl_inquiries` 문의 🔴 | 비공개 | ❌ 공개 키로는 0행(RLS) | **오너** |
| `sl_applications` 지원 🔴 | 비공개 | ❌ 0행(RLS) | **오너** |
| `sl_admins` 관리자 목록 | 비공개 | ❌ 0행(RLS) | **오너** |
| `sl_audit` 감사 로그 | 비공개 | ❌ 0행(RLS) | **오너** |
| `auth.users` 로그인 계정 | 비공개 | ❌ auth 스키마 | **오너** |

공개 키(anon)로 내보낼 수 있는 것은 이미 다 내보냈다. 나머지 다섯은 **RLS 가 정상 동작해서**
공개 키로 0행이 나온다 — 이것이 보안 설계가 맞게 돌고 있다는 증거이기도 하다.

### 8.2 오너가 하는 전체 덤프
`scripts/export-from-supabase.sh` 가 `pg_dump` 로 다섯 대상을 뜬다.
Supabase 대시보드 → Project Settings → Database → **Connection string(Direct)** 이 필요하다.

- 🔴 **개인정보가 들어 있다.** 덤프 파일은 암호화된 경로로만 옮기고, 이관 후 즉시 삭제한다.
- 로그인 계정은 **비밀번호 해시(bcrypt)째 옮긴다** — 관리자가 비밀번호를 다시 정할 필요가 없다.
- `auth.users` 의 `id` 를 바꾸지 않는다. `sl_admins.user_id` 가 이 값을 참조한다(4.6항).

### 8.3 덤프를 못 받는 경우
최초 구축이거나 관리형 접속이 안 될 때는 **빈 상태에서 시작**한다.
1. GoTrue 관리 API 로 관리자 계정 1개 생성(비밀번호는 오너가 직접 입력)
2. HANDOFF 3항 ② 의 부트스트랩 SQL 로 그 계정을 `admin` 으로 결속
3. 문의·지원·감사 로그는 **이전되지 않는다** — 오너가 수용 여부를 결정한다

---

## 9. 검증 체크리스트

`scripts/verify.sh https://<도메인>` 이 아래 중 자동화 가능한 항목을 돌린다.

### 9.1 기능
- [ ] 홈·회사소개·서비스·방법론 등 주요 경로 200
- [ ] 없는 경로 → 404 페이지
- [ ] 문의 제출 → 관리자 콘솔 [문의] 탭에 표시
- [ ] 관리자 로그인 · 문구 저장 1회 · 계정 목록 열기 1회
- [ ] 비밀번호 변경(adminfn 경유) 1회

### 9.2 보안 경계 — **하나라도 실패하면 개통하지 않는다**
- [ ] 공개 키로 `sl_inquiries` · `sl_applications` · `sl_admins` · `sl_audit` 조회 → **0행**
- [ ] 공개 키로 `sl_stats` · `sl_log` RPC → **거부**
- [ ] 공개 키로 셀프 가입 `POST /auth/v1/signup` → **거부**
- [ ] 동의 없이 `sl_submit_inquiry` → 거부
- [ ] 외부에서 5432·3000·9999·8080·8081 접속 → **불가**
- [ ] `/tools/` · `/supabase/` · `/deploy/` · `/.git/` → 404
- [ ] 응답 헤더에 HSTS · nosniff · X-Frame-Options 존재

### 9.3 운영
- [ ] 보존기간 파기 cron 등록 확인 (`select public.sl_purge_all();` 수동 1회 성공)
- [ ] 백업 1회 생성 + **복원 시험 1회**
- [ ] 인증서 만료일 확인 · `certbot renew --dry-run --webroot -w /srv/shieldus/deploy/certbot-www` 성공 **(nginx 가 떠 있는 상태로)**

---

## 10. 운영

### 10.1 백업
| 항목 | 설정 |
|---|---|
| 방식 | `pg_dump -Fc` (압축 커스텀 포맷) |
| 주기 | 매일 04:00 |
| 보관 | 7일 일별 + 4주 주별 |
| 위치 | 서버 밖(오브젝트 스토리지 등). **같은 디스크에만 두면 백업이 아니다** |
| 🔴 주의 | 개인정보 포함 → 암호화 보관. 보관 기간이 보존기간(4.4항)보다 길면 파기 의무와 충돌한다 |
| 복원 시험 | 분기 1회 |

### 10.2 로그
| 대상 | 위치 |
|---|---|
| 웹 접근·오류 | `docker compose logs web` |
| 인증 | `docker compose logs auth` |
| API | `docker compose logs rest` |
| 사이트 감사 로그 | DB `sl_audit` (관리자 콘솔 [로그·감사] 탭) |

Docker 로그 순환을 켠다: `/etc/docker/daemon.json` 에 `"log-opts": {"max-size":"20m","max-file":"5"}`

### 10.3 감시
최소한 외부 업타임 감시 1개(UptimeRobot 등)로 `https://<도메인>/` 와
`https://<도메인>/rest/v1/sl_content?select=key&limit=1`(공개 키 헤더 포함)을 5분 간격 확인.

### 10.4 인증서 자동 갱신
```cron
0 4 * * 1  root certbot renew --quiet --webroot -w /srv/shieldus/deploy/certbot-www --deploy-hook "cp /etc/letsencrypt/live/shielduslab.com/*.pem /srv/shieldus/deploy/certs/ && docker compose -f /srv/shieldus/deploy/docker-compose.yml exec web nginx -s reload"
```

### 10.5 콘텐츠 배포
지금과 같다 — 레포에서 `python3 tools/build-pages.py` 후, 서버에서 `git pull` 만 하면 nginx 가
새 파일을 바로 서빙한다(재시작 불필요). 관리자 콘솔의 문구 수정은 DB 에 저장되므로 배포가 필요 없다.

---

## 11. 롤백 계획
관리형 Supabase 와 GitHub Pages 를 **최소 30일 해지하지 않고 둔다.**

| 시점 | 롤백 방법 | 소요 |
|---|---|---|
| DNS 전환 전 | 새 서버만 내리면 된다. 영향 없음 | 즉시 |
| DNS 전환 후 | DNS A 레코드를 GitHub Pages IP 4개로 되돌린다 · `config.js` 를 이전 값으로 | DNS TTL(600초) |
| 전환 후 데이터 발생 | 그 사이 새 서버에 들어온 문의는 **관리형으로 역이관**해야 한다 → 전환 직후 며칠은 문의를 매일 확인 | 수동 |

---

## 12. 위험과 대응

| 위험 | 영향 | 대응 |
|---|---|---|
| 🔴 **개인정보처리방침 국외이전 고지가 틀어진다** | 법적 고지 오류 | 현재 고지는 *"Supabase, Inc. — 미국"* 이다(리전 us-east-1 을 2026-08-09 지연 측정으로 확인). **국내 서버로 옮기면 이 행은 사실이 아니게 된다.** 이관과 **같은 날** `tools/content_legal.py` 3항을 고친다 — Supabase 행 삭제, 호스팅 업체가 수탁자가 되면 그 행 추가. Google Fonts(미국) 행은 유지 |
| `JWT_SECRET` 불일치 | 로그인 후 전부 401 | `.env` 한 값을 두 서비스가 읽게 compose 가 짜여 있다. 손으로 바꾸지 말 것 |
| `X-Forwarded-For` 누락 | 레이트리밋 무력화 | 9.2항 검증에 포함 |
| 보존기간 cron 누락 | 개인정보 과보관 (법적) | 7단계 8번·9.3항에 이중으로 넣었다 |
| 단일 서버 장애 | 사이트 중단 | 백업·복원 시험(10.1). 가용성 요구가 높아지면 DB 를 관리형으로 분리 |
| 이미지 버전 노후 | 보안 취약점 | 분기 1회 버전 점검 |
| `.env` 유출 | service_role 로 전체 데이터 접근 | `chmod 600`, 저장소 커밋 금지, 유출 시 `gen-keys.sh` 로 재발급 후 재기동 |

---

## 13. 사전 검증 결과 — DB 계층 (2026-10-02)

`deploy/scripts/test-db.py` 로 **실제 PostgreSQL 16.2** 에서 이 패키지를 끝까지 돌렸다.
Docker 없이 돌아가므로 **배포 전에 누구나 다시 돌릴 수 있다**(`pip install pgserver` 후 실행).

### 13.1 결과 — **통과 36 · 실패 0**

| 영역 | 확인한 것 |
|---|---|
| 부트스트랩 | 롤 5개 생성 · auth 헬퍼 4개 |
| GoTrue 함정 | GoTrue 가 `auth.uid()` 를 옛 방식으로 덮어쓰면 **실제로 NULL** 이 됨을 재현 → 재적용으로 복구됨을 확인 · 신·구 클레임 모두 동작 |
| 마이그레이션 | 0001~0007 전부 적용 성공 |
| 시드 | 공개 데이터 60행 적재 · 트리거가 꺼진 채 들어가 감사 로그 무증가 · **두 번 적용해도 행 수 불변**(재실행 안전) |
| 최종 구조 | RLS 활성 테이블 8 · 정책 18 · 함수 27 |
| 비로그인(anon) | 공개 문구 51행 읽힘 · 개인정보·관리자·감사 4개 테이블 **0행** · 개인정보 테이블 **직접 INSERT 거부(RLS)** · 관리 함수 3종 거부 · 동의 없는 문의 거부 · 정상 문의는 RPC 로 접수 · `X-Forwarded-For` IP 가 감사 로그에 기록 |
| 관리자 로그인 | `is_sl_admin()=true` · 문의 열람 · 계정 목록 |
| 비관리자 로그인 | `is_sl_admin()=false` · 문의 0행 |
| 탈취 시나리오(0004) | **이메일만 같고 계정 ID 가 다른 사용자 → 관리자 아님** |
| 운영 | 보존기간 파기 `sl_purge_all()` 실행 |

### 13.2 검증이 잡아낸 결함 4건 — 전부 수정함

이 검증을 돌리기 전 패키지에는 아래 결함이 있었다. **그대로 배포했다면 ①은 사이트를 빈 화면으로 만들었다.**

| # | 결함 | 증상 | 수정 |
|---|---|---|---|
| ① | 🔴 **Supabase 기본 권한 누락** | 비로그인 방문자가 공개 문구조차 못 읽음(`permission denied for table sl_content`), 관리자도 문의를 못 봄 | 관리형과 같은 기본 권한을 `01-roles-auth.sql` 에서 재현. 마이그레이션의 테이블 GRANT 가 0건이라 이 전제가 필수였다 |
| ② | 시드의 jsonb 값 미인용 | `sl_settings.value` 적재 실패(`invalid input syntax for type json`) | 마이그레이션에서 컬럼 타입을 읽는 `export-public.py` 로 교체 |
| ③ | 시드와 초기값의 slug 충돌 | `sl_insights` 적재 실패(`duplicate key … slug_key`) — 0002 초기값과 라이브가 slug 는 같고 id 가 다름 | 공개 테이블은 비우고 라이브 상태로 채우도록 변경(라이브가 정본) |
| ④ | 불필요한 `pgcrypto` 의존 | contrib 패키지 없는 최소 설치 PostgreSQL 에서 첫 파일부터 실패 | 제거. `gen_random_uuid()` 는 PG13+ 코어 내장, pgcrypto 전용 함수 사용 0회 |

명세서 숫자 1건도 바로잡았다 — RLS 정책 수를 `create policy` 문장 수(21)로 적었는데 최종 상태는 **18** 이다.

### 13.3 검증하지 **못한** 것

| 대상 | 이유 | 대신 |
|---|---|---|
| GoTrue · PostgREST · nginx 실기동 | 검증 환경에 Docker 가 없었다 | 구성은 공식 문서 기준. **서버에서 `verify.sh` 로 확인** — 보안 경계 항목 실패 시 종료코드 1 |
| `export-from-supabase.sh` | 관리형 DB 접속 문자열이 없었다 | 오너 첫 실행 시 확인. `import-to-server.sh` 가 끝에 결속 끊긴 관리자 수를 출력한다 |
| 실제 GoTrue 의 `auth.users` | 대역(마이그레이션이 쓰는 5개 컬럼)으로 시험했다 | 실제 GoTrue 가 만드는 테이블은 컬럼이 더 많다 — 상위 호환이므로 영향 없음 |
| Apache 설정 | httpd 바이너리가 없었다 | `apachectl configtest` 로 서버에서 확인 |

---

## 부록 A. 환경변수 전체 목록 (`deploy/.env`)

| 변수 | 필수 | 예 | 설명 |
|---|---|---|---|
| `POSTGRES_PASSWORD` | ✅ | (32자 무작위) | DB 슈퍼유저 · authenticator · supabase_auth_admin 공통 |
| `JWT_SECRET` | ✅ | `gen-keys.sh` 산출 | GoTrue·PostgREST 공통 서명 키 |
| `ANON_KEY` | ✅ | `gen-keys.sh` 산출 | 공개 키 — `config.js` 에도 넣는다 |
| `SERVICE_ROLE_KEY` | ✅ | `gen-keys.sh` 산출 | 🔴 비밀. adminfn 만 쓴다 |
| `PUBLIC_URL` | ✅ | `https://shielduslab.com` | 사이트 주소 · CORS 허용 출처 |
| `SERVER_NAME` | ✅ | `shielduslab.com www.shielduslab.com` | nginx server_name |
| `SITE_ROOT` | | `../` | 정적 파일 루트(기본: 레포 루트) |
| `MAILER_AUTOCONFIRM` | | `false` | 관리자 계정은 오너가 만들므로 false 유지 |
| `SMTP_HOST` 등 5종 | 비밀번호 재설정 메일을 쓸 때 | | |

## 부록 B. 파일 목록 (`deploy/`)

| 파일 | 역할 |
|---|---|
| `SPEC.md` | 이 문서 |
| `README.md` | 빠른 시작(명령만) |
| `.env.example` | 환경변수 견본 |
| `docker-compose.yml` | 서비스 5종 정의 |
| `db/01-roles-auth.sql` | 롤·auth 헬퍼 (관리형이 하던 부트스트랩) |
| `db/03-seed-public.sql` | 공개 데이터 60행 (실데이터) |
| `nginx/site.conf` | 웹 서버·게이트웨이·보안 헤더 |
| `services/admin-user/Dockerfile` | Edge 함수 원본을 그대로 실행 |
| `scripts/gen-keys.sh` | JWT 시크릿·키 생성 |
| `scripts/init-db.sh` | 스키마를 순서대로 적용 |
| `scripts/export-from-supabase.sh` | 관리형 전체 덤프(오너) |
| `scripts/import-to-server.sh` | 덤프 적재 |
| `scripts/verify.sh` | 9항 자동 검증 (서버에서) |
| `scripts/test-db.py` | **13항 — Docker 없이 DB 계층 사전 검증** |
| `scripts/export-public.py` | 공개 데이터 시드 재생성(**이관 당일 다시 돌린다**) |
| `db/01b-role-passwords.sh` | initdb 단계에서 롤 비밀번호를 `.env` 값으로 맞춤 |
| `apache/site.conf` | 부록 C — Apache 를 쓸 경우 |
| (명세서 부록 D) | 테이블 정의서 — 실제 카탈로그 추출 |

스키마의 정본은 여전히 `supabase/migrations/0001~0007` 이다. `deploy/` 는 그것을 **복사하지 않고**
순서대로 적용만 한다 — 사본을 두면 원본과 갈라진다.

## 부록 C. Docker 없이 직접 설치하는 경우

사내 정책상 컨테이너를 쓸 수 없을 때의 대응 절차다. **구성요소와 버전은 2.6항과 같다.**
각 서비스를 systemd 로 띄우고, 포트는 전부 `127.0.0.1` 에만 묶는다.

### C.1 PostgreSQL 16
```bash
sudo apt -y install postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
sudo apt -y install postgresql-16
# listen_addresses = 'localhost' 확인 (/etc/postgresql/16/main/postgresql.conf)
sudo -u postgres psql -f /srv/shieldus/deploy/db/01-roles-auth.sql
sudo -u postgres psql -c "alter role authenticator password '<POSTGRES_PASSWORD>';"
sudo -u postgres psql -c "alter role supabase_auth_admin password '<POSTGRES_PASSWORD>';"
```

### C.2 GoTrue · PostgREST · Deno (단일 바이너리)
| 구성요소 | 받는 곳 | 실행 |
|---|---|---|
| GoTrue v2.158.1 | github.com/supabase/auth/releases | `auth serve` (환경변수는 compose 의 `auth.environment` 와 동일, `GOTRUE_DB_DATABASE_URL` 의 호스트만 `localhost`) |
| PostgREST v12.2.3 | github.com/PostgREST/postgrest/releases | `postgrest /etc/postgrest.conf` |
| Deno 2.1.4 | `curl -fsSL https://deno.land/install.sh \| sh` | `deno run --allow-net --allow-env supabase/functions/sl-admin-user/index.ts` |

`/etc/postgrest.conf`
```ini
db-uri       = "postgres://authenticator:<POSTGRES_PASSWORD>@127.0.0.1:5432/postgres"
db-schemas   = "public"
db-anon-role = "anon"
jwt-secret   = "<JWT_SECRET>"
openapi-mode = "disabled"
server-host  = "127.0.0.1"
server-port  = 3000
```

systemd 단위 예 — `/etc/systemd/system/shieldus-rest.service`
```ini
[Unit]
Description=Shieldus PostgREST
After=postgresql.service
Requires=postgresql.service

[Service]
ExecStart=/usr/local/bin/postgrest /etc/postgrest.conf
Restart=always
User=shieldus
NoNewPrivileges=true
ProtectSystem=strict

[Install]
WantedBy=multi-user.target
```
GoTrue(`shieldus-auth`)·Deno(`shieldus-adminfn`)도 같은 형식으로 만든다.
**adminfn 의 `SUPABASE_URL` 은 `http://127.0.0.1:8081`** (웹 서버의 내부 전용 포트)로 둔다.

### C.3 웹 서버를 Apache httpd 로 쓰는 경우
`deploy/apache/site.conf` 에 nginx 설정과 동등한 구성을 실었다. 필요한 모듈:
```bash
sudo a2enmod ssl proxy proxy_http headers rewrite expires
```
nginx 와 다른 점:
- **레이트리밋이 기본 모듈에 없다.** `mod_evasive` 또는 `mod_security` 를 추가하거나,
  레이트리밋을 앞단(CDN·방화벽)에 맡긴다. 이 경우 9.2항 검증 전에 대안이 동작하는지 확인한다.
- `ProxyPass` 의 끝 슬래시 규칙이 nginx 와 같다 — `/rest/v1/ → http://127.0.0.1:3000/` 처럼
  **양쪽 모두 슬래시로 끝나야** 접두가 떨어진다.

### C.4 WAS(Tomcat 등)를 반드시 써야 하는 환경이라면
서빙할 Java 애플리케이션이 없으므로 Tomcat 은 **정적 파일 서버 역할만** 하게 된다.
가능은 하지만 권하지 않는다. 그래도 써야 한다면:
- 정적 사이트를 `webapps/ROOT/` 에 두고,
- `/rest/v1`·`/auth/v1`·`/functions/v1` 프록시는 **앞단에 Apache 또는 nginx 를 반드시 둔다**
  (Tomcat 단독으로는 리버스 프록시·보안 헤더·레이트리밋을 깔끔하게 처리하기 어렵다).
결국 Apache/nginx 가 필요하므로 Tomcat 을 빼는 편이 구성이 단순하다.

## 부록 D. 테이블 정의서 (실측)

마이그레이션 0001~0007 을 **실제 PostgreSQL 16.2 에 적용한 결과의 시스템 카탈로그**에서 뽑았다(손으로 쓰지 않음).
생성 절차는 13항과 같다. 표의 `NN` 은 NOT NULL, `PK` 는 기본키. 🔴 개인정보 · 🟡 준개인정보.

### D.1 `sl_inquiries` — 상담·견적 문의

| 항목 | 내용 |
|---|---|
| 개인정보 | 🔴 이름·이메일·전화 |
| 보존기간 | 접수 1년 후 자동 파기 |
| 쓰기 경로 | RPC `sl_submit_inquiry` 만 (INSERT 정책 없음) |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `id` | uuid | ✓ | `gen_random_uuid()` | ✓ | 문의 ID |
| 2 | `company` | text | ✓ |  |  | 회사명 |
| 3 | `name` | text | ✓ |  |  | 🔴 담당자 이름 |
| 4 | `email` | text | ✓ |  |  | 🔴 담당자 이메일 |
| 5 | `phone` | text | ✓ | `''` |  | 🔴 담당자 전화 |
| 6 | `service` | text | ✓ | `''` |  | 문의 유형 |
| 7 | `message` | text | ✓ |  |  | 문의 내용 |
| 8 | `status` | text | ✓ | `'new'` |  | 처리 상태 new/doing/done/drop |
| 9 | `admin_note` | text | ✓ | `''` |  | 관리자 메모 |
| 10 | `ip` | text |  |  |  | 제출 IP(레이트리밋·감사) |
| 11 | `user_agent` | text |  |  |  | 제출 브라우저 |
| 12 | `consent_at` | timestamptz | ✓ | `now()` |  | 개인정보 수집·이용 동의 시각 |
| 13 | `created_at` | timestamptz | ✓ | `now()` |  | 접수 시각 — 보존기간 기준 |
| 14 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |

**제약**

- `sl_inquiries_status_check` — `CHECK ((status = ANY (ARRAY['new'::text, 'doing'::text, 'done'::text, 'drop'::text])))`

**인덱스**

- `sl_inq_created_idx`
- `sl_inq_ip_idx`
- `sl_inq_status_idx`

**RLS 정책** (3개)

- `sl_inq_admin_delete` — DELETE · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_inq_admin_read` — SELECT · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_inq_admin_update` — UPDATE · 대상 `authenticated` · 조건 `is_sl_admin()`

**트리거**

- `trg_sl_inquiries_updated` — BEFORE UPDATE

### D.2 `sl_applications` — 채용 지원

| 항목 | 내용 |
|---|---|
| 개인정보 | 🔴 이름·이메일·전화 |
| 보존기간 | 접수 6개월 후 자동 파기 |
| 쓰기 경로 | RPC `sl_apply` 만 (INSERT 정책 없음) |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `id` | uuid | ✓ | `gen_random_uuid()` | ✓ | 지원 ID |
| 2 | `name` | text | ✓ |  |  | 🔴 지원자 이름 |
| 3 | `email` | text | ✓ |  |  | 🔴 지원자 이메일 |
| 4 | `phone` | text | ✓ | `''` |  | 🔴 지원자 전화 |
| 5 | `position` | text | ✓ | `''` |  | 지원 포지션 |
| 6 | `summary` | text | ✓ | `''` |  | 자기소개 요약 |
| 7 | `link` | text | ✓ | `''` |  | 이력서·포트폴리오 링크 |
| 8 | `status` | text | ✓ | `'new'` |  | 처리 상태 new/doing/done/drop |
| 9 | `admin_note` | text | ✓ | `''` |  | 관리자 메모 |
| 10 | `ip` | text |  |  |  | 제출 IP(레이트리밋·감사) |
| 11 | `user_agent` | text |  |  |  | 제출 브라우저 |
| 12 | `consent_at` | timestamptz | ✓ | `now()` |  | 개인정보 수집·이용 동의 시각 |
| 13 | `created_at` | timestamptz | ✓ | `now()` |  | 접수 시각 — 보존기간 기준 |
| 14 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |

**제약**

- `sl_applications_status_check` — `CHECK ((status = ANY (ARRAY['new'::text, 'doing'::text, 'done'::text, 'drop'::text])))`

**인덱스**

- `sl_app_created_idx`
- `sl_app_ip_idx`
- `sl_app_status_idx`

**RLS 정책** (3개)

- `sl_app_admin_delete` — DELETE · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_app_admin_read` — SELECT · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_app_admin_update` — UPDATE · 대상 `authenticated` · 조건 `is_sl_admin()`

**트리거**

- `trg_sl_applications_updated` — BEFORE UPDATE

### D.3 `sl_audit` — 방문·관리자 행위·제출 이벤트 로그

| 항목 | 내용 |
|---|---|
| 개인정보 | 🟡 IP·User-Agent |
| 보존기간 | 방문 90일 · 관리/제출 365일 후 자동 파기 |
| 쓰기 경로 | RPC `sl_log`·`sl_log_visit`, 트리거 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `id` | bigint | ✓ | `IDENTITY` | ✓ | 일련번호(IDENTITY) |
| 2 | `kind` | text | ✓ | `'admin'` |  | 구분 visit / admin / submit |
| 3 | `actor` | uuid |  |  |  | 행위자 계정 ID |
| 4 | `actor_email` | text |  |  |  | 행위자 이메일 |
| 5 | `action` | text | ✓ |  |  | 행위 |
| 6 | `entity` | text |  |  |  | 대상 객체 |
| 7 | `entity_id` | text |  |  |  | 대상 ID |
| 8 | `detail` | jsonb | ✓ | `'{}'` |  | 상세(JSON) |
| 9 | `ip` | text |  |  |  | 요청 IP |
| 10 | `user_agent` | text |  |  |  | 요청 브라우저 |
| 11 | `created_at` | timestamptz | ✓ | `now()` |  | 기록 시각 — 보존기간 기준 |

**인덱스**

- `sl_audit_created_idx`
- `sl_audit_entity_idx`
- `sl_audit_kind_idx`

**RLS 정책** (1개)

- `sl_audit_admin_read` — SELECT · 대상 `authenticated` · 조건 `is_sl_owner()`

### D.4 `sl_admins` — 관리자 화이트리스트(역할 admin/editor)

| 항목 | 내용 |
|---|---|
| 개인정보 | 🟡 이메일 |
| 보존기간 | 수동 |
| 쓰기 경로 | RPC `sl_admin_*` 만 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `email` | text | ✓ |  | ✓ | 관리자 이메일(소문자). 화이트리스트 키 |
| 2 | `role` | text | ✓ | `'editor'` |  | 역할 — admin(계정·설정·로그 포함 전체) / editor(콘텐츠·문의) |
| 3 | `note` | text |  |  |  | 메모 |
| 4 | `created_at` | timestamptz | ✓ | `now()` |  | 등록 시각 |
| 5 | `user_id` | uuid |  |  |  | 결속된 로그인 계정 ID(auth.users.id). **NULL 이면 권한 없음** |
| 6 | `pw_managed` | boolean | ✓ | `false` |  | 콘솔이 비밀번호를 만든 계정 여부. service_role 만 변경 가능(트리거) |

**제약**

- `sl_admins_role_check` — `CHECK ((role = ANY (ARRAY['admin'::text, 'editor'::text])))`

**인덱스**

- `sl_admins_email_lower_key`
- `sl_admins_user_id_key`

**RLS 정책** (1개)

- `sl_admins_read` — SELECT · 대상 `authenticated` · 조건 `is_sl_owner()`

**트리거**

- `sl_admins_guard_pw_managed` — BEFORE UPDATE

### D.5 `sl_content` — 페이지 문구 CMS

| 항목 | 내용 |
|---|---|
| 개인정보 | 없음 |
| 보존기간 | — |
| 쓰기 경로 | 관리자 콘솔 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `key` | text | ✓ |  | ✓ | 블록 키(예: home.hero_title). 페이지의 data-content 앵커와 일치 |
| 2 | `value` | text | ✓ | `''` |  | 문구(평문·최소 마크다운. HTML 저장 안 함) |
| 3 | `kind` | text | ✓ | `'text'` |  | text / rich |
| 4 | `section` | text | ✓ | `'기타'` |  | 콘솔 분류 |
| 5 | `label` | text | ✓ | `''` |  | 콘솔 표시 이름 |
| 6 | `hint` | text | ✓ | `''` |  | 콘솔 도움말 |
| 7 | `sort_order` | integer | ✓ | `0` |  | 콘솔 정렬 순서 |
| 8 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |
| 9 | `updated_by` | uuid |  |  |  | 수정한 관리자 계정 ID |

**제약**

- `sl_content_kind_chk` — `CHECK ((kind = ANY (ARRAY['text'::text, 'rich'::text])))`
- `sl_content_len_chk` — `CHECK ((length(value) <= 20000))`

**RLS 정책** (2개)

- `sl_content_read` — SELECT · 대상 `public` · 조건 `true`
- `sl_content_write` — ALL · 대상 `authenticated` · 조건 `is_sl_admin()`

**트리거**

- `sl_content_audit_trg` — AFTER UPDATE/INSERT
- `sl_content_touch_trg` — BEFORE UPDATE/INSERT

### D.6 `sl_insights` — 인사이트 글

| 항목 | 내용 |
|---|---|
| 개인정보 | 없음 |
| 보존기간 | — |
| 쓰기 경로 | 관리자 콘솔 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `id` | uuid | ✓ | `gen_random_uuid()` | ✓ | 글 ID |
| 2 | `slug` | text | ✓ |  |  | URL 경로(유일) — /insights/<slug>/ |
| 3 | `category` | text | ✓ | `'인사이트'` |  | 분류 |
| 4 | `title` | text | ✓ |  |  | 제목 |
| 5 | `summary` | text | ✓ | `''` |  | 요약 |
| 6 | `body` | text | ✓ | `''` |  | 본문(최소 마크다운) |
| 7 | `author` | text | ✓ | `''` |  | 작성자 |
| 8 | `published` | boolean | ✓ | `false` |  | 공개 여부 |
| 9 | `published_at` | date | ✓ | `CURRENT_DATE` |  | 게시일 |
| 10 | `sort_order` | integer | ✓ | `0` |  | 정렬 순서 |
| 11 | `created_at` | timestamptz | ✓ | `now()` |  | 생성 시각 |
| 12 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |

**제약**

- `sl_insights_slug_fmt` — `CHECK ((slug ~ '^[a-z0-9]([a-z0-9-]{0,78}[a-z0-9])?$'::text))`
- `sl_insights_slug_key` — `UNIQUE (slug)`
- `sl_insights_title_len` — `CHECK (((char_length(title) >= 1) AND (char_length(title) <= 200)))`

**인덱스**

- `sl_insights_pub_idx`
- `sl_insights_slug_key`

**RLS 정책** (3개)

- `sl_insights_read_all` — SELECT · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_insights_read_pub` — SELECT · 대상 `public` · 조건 `(published = true)`
- `sl_insights_write` — ALL · 대상 `authenticated` · 조건 `is_sl_admin()`

**트리거**

- `trg_sl_insights_updated` — BEFORE UPDATE

### D.7 `sl_jobs` — 채용 공고

| 항목 | 내용 |
|---|---|
| 개인정보 | 없음 |
| 보존기간 | — |
| 쓰기 경로 | 관리자 콘솔 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `id` | uuid | ✓ | `gen_random_uuid()` | ✓ | 공고 ID |
| 2 | `title` | text | ✓ |  |  | 포지션명 |
| 3 | `team` | text | ✓ | `''` |  | 소속 팀 |
| 4 | `employment_type` | text | ✓ | `'정규직'` |  | 고용 형태 |
| 5 | `location` | text | ✓ | `''` |  | 근무지 |
| 6 | `summary` | text | ✓ | `''` |  | 요약 |
| 7 | `body` | text | ✓ | `''` |  | 상세(최소 마크다운) |
| 8 | `closes_at` | date |  |  |  | 마감일(NULL = 상시) |
| 9 | `published` | boolean | ✓ | `false` |  | 공개 여부 |
| 10 | `sort_order` | integer | ✓ | `0` |  | 정렬 순서 |
| 11 | `created_at` | timestamptz | ✓ | `now()` |  | 생성 시각 |
| 12 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |

**제약**

- `sl_jobs_title_len` — `CHECK (((char_length(title) >= 1) AND (char_length(title) <= 160)))`

**인덱스**

- `sl_jobs_pub_idx`

**RLS 정책** (3개)

- `sl_jobs_read_all` — SELECT · 대상 `authenticated` · 조건 `is_sl_admin()`
- `sl_jobs_read_pub` — SELECT · 대상 `public` · 조건 `(published = true)`
- `sl_jobs_write` — ALL · 대상 `authenticated` · 조건 `is_sl_admin()`

**트리거**

- `trg_sl_jobs_updated` — BEFORE UPDATE

### D.8 `sl_settings` — 사이트 설정(key-value)

| 항목 | 내용 |
|---|---|
| 개인정보 | 없음 |
| 보존기간 | — |
| 쓰기 경로 | 관리자 콘솔 |

| # | 컬럼 | 타입 | NN | 기본값 | PK | 설명 |
|---|---|---|---|---|---|---|
| 1 | `key` | text | ✓ |  | ✓ | 설정 키(대표 이메일·운영 시간·회신 안내·공지 배너 등) |
| 2 | `value` | jsonb | ✓ | `'{}'` |  | 값(JSON) |
| 3 | `updated_at` | timestamptz | ✓ | `now()` |  | 수정 시각 |

**RLS 정책** (2개)

- `sl_settings_read` — SELECT · 대상 `public` · 조건 `true`
- `sl_settings_write` — ALL · 대상 `authenticated` · 조건 `is_sl_owner()`

**트리거**

- `trg_sl_settings_updated` — BEFORE UPDATE

