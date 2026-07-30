# 쉴더스랩 (SHIELDUS LAB) — shilderslab.com

정보보호 컨설팅 기업 쉴더스랩의 공식 웹사이트. **정적 프런트(GitHub Pages) + Supabase 백엔드** 구성.

- 라이브: https://shilderslab.com
- 관리자 콘솔: https://shilderslab.com/admin/ (등록된 관리자 계정만)

## 구성

```
/                       홈 (히어로·서비스·프로세스·인사이트 프리뷰)
/services/              서비스 6개 영역 상세 + FAQ
/about/                 회사소개·원칙·연혁
/insights/              인사이트 목록 (CMS)
/insights/view.html     인사이트 상세 (?slug=…)
/careers/               채용 공고(CMS) + 지원 접수
/contact/               상담·견적 요청 폼
/brand/                 CI 벡터 원본 다운로드 + 사용 규칙
/legal/privacy.html     개인정보처리방침
/legal/terms.html       이용약관
/admin/                 관리자 콘솔 (대시보드·문의·지원·CMS·로그·설정)

assets/css/site.css     전 페이지 공용 디자인 시스템
assets/js/site.js       내비·리빌·카운터·공지배너·방문로깅 + 페이지 문구(CMS) 반영
assets/js/supa.js       Supabase 클라이언트 + esc/safeUrl/md 등 공용 유틸
assets/vendor/           supabase-js UMD (자체 호스팅 — CDN 의존 없음)
assets/ci/              CI 벡터 원본(SVG) + OG/파비콘 래스터
config.js               Supabase URL/anon 키 + 회사 정보(COMPANY, sl_content 가 덮어씀)
supabase/migrations/    DB 스키마·RLS·RPC (0001) · 시드 (0002) · 하드닝 (0003)
                        · 관리자 역할 (0004) · 페이지 문구 CMS (0005)
supabase/functions/     notify-inquiry (선택: 접수 알림 메일)
tools/                  페이지 빌더 · CI 생성기 · 명함 생성기
tools/content_blocks.py 관리자가 편집하는 문구 블록의 정본 정의(빌드·시드·관리자 UI 공용)
tools/gen-content-seed.py  content_blocks.py → 0005 SQL 생성기
```

## 페이지 문구를 고치는 두 가지 경로

| 대상 | 방법 |
|---|---|
| 회사소개·대표이사 인사말·서비스 인트로·푸터·법인 정보 | 관리자 콘솔 → **[페이지 문구]** 탭 (재빌드 없이 즉시 반영) |
| 그 밖의 모든 페이지 | `tools/content_*.py` 수정 → `python3 tools/build-pages.py` → 푸시 |

CMS 블록은 HTML 에 `data-content="키"` 앵커로 표시돼 있다. 빌드가 DB 값을 정적 HTML 에 구워 넣고
(검색엔진 대응), 클라이언트가 같은 값으로 다시 그린다(저장 직후 반영). 값이 비면 코드 기본 문구가 남는다.

## 로컬 개발

정적 파일이므로 빌드 도구 없이 확인 가능하다.

```bash
python3 -m http.server 8188 --directory /Users/hk/shilderslab-www
```

`http://localhost:8188` 접속. (Claude Preview MCP 사용 시 `~/.claude/launch.json` 의 `shilderslab` 설정)

### 페이지 수정 방법

- **홈 · 서비스**: `index.html`, `services/index.html` 직접 편집
- **그 외 페이지**: `tools/content_*.py` 의 본문을 고치고 아래 실행 (헤더/푸터는 `tools/build-pages.py` 한 곳에서 관리)

```bash
python3 tools/build-pages.py
```

이 명령은 페이지를 재생성하고, 직접 편집한 두 페이지의 `<header>`/`<footer>` 블록도 템플릿과 동기화한다.

### CI 재생성

`tools/build-ci.py` 는 Manrope / Noto Sans KR(SIL OFL) 글리프를 **아웃라인 패스로 변환**해 로고 SVG를 생성한다.
폰트 파일과 `fonttools` 가 필요하며, 생성 결과(SVG)는 저장소에 커밋되어 있으므로 평소에는 실행할 필요가 없다.

## 배포

`main` 브랜치에 push하면 GitHub Pages가 자동 배포한다. `CNAME`(shilderslab.com)과 `.nojekyll` 포함.

## 백엔드

Supabase 프로젝트 `nrdapzgtibbusvoaceuh` 를 다른 서비스와 **공유**한다. 따라서 `authenticated`는 관리자를 의미하지 않으며,
모든 쓰기·조회 권한은 `sl_admins` 화이트리스트(`is_sl_admin()`)로 게이트한다.

| 테이블 | 용도 | 공개 접근 |
|---|---|---|
| `sl_admins` | 관리자 화이트리스트 | 없음 (SQL로만 등록) |
| `sl_settings` | 공지 배너 등 사이트 설정 | 읽기만 |
| `sl_insights` | 인사이트 CMS | `published=true` 읽기만 |
| `sl_jobs` | 채용 공고 CMS | `published=true` 읽기만 |
| `sl_inquiries` | 문의·견적 (PII) | **없음** — RPC로만 적재 |
| `sl_applications` | 채용 지원 (PII) | **없음** — RPC로만 적재 |
| `sl_audit` | 관리자·제출·방문 로그 | 없음 — RPC로만 적재 |

공개 RPC: `sl_submit_inquiry` · `sl_apply` · `sl_log_visit` (모두 SECURITY DEFINER + 서버측 검증 + IP 레이트리밋)

자세한 운영 상태와 남은 작업은 [HANDOFF.md](HANDOFF.md) 참조.
