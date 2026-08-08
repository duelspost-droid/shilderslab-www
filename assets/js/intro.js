/* ══════════════════════════════════════════════════════════════════════
   assets/js/intro.js — 홈 인트로 v3 "도장된 방패(Painted Shield)"  5초.

   ▣ 무엇이 바뀌었나 — 가장 중요한 것부터
   1) **v2 가 밋밋했던 이유는 렌더 버그가 아니라 "재질이 없어서"다.** (실측으로 확인)
      크롬 1280×820 에서 v2 를 그대로 띄워 뒤 층과 앞 층의 화면 좌표를 쟀다 —
      정지 자세에서 4.51px, 진입 중(t=600, opacity .988)에도 3.25px 어긋나 있다.
      **v2 의 압출은 살아 있었다.** 다만 22겹이 전부 단색 #0F3227 한 톤이라
      옆면이 "어두운 슬래브 한 덩어리"로 읽혔을 뿐이다. 그래서 이 파일이 고치는 것은
      기하가 아니라 **빛**이다(아래 조명 모델).
      ⚠ 다만 v2 의 **구조는 엔진 의존적으로 위험했다.** opacity 가 preserve-3d 인
      `.mark` 위에서 움직였는데, CSS Transforms L2 의 grouping 규칙상
      opacity(<1)·filter·mask·clip-path·mix-blend-mode·will-change:opacity 가 걸린
      원소는 used transform-style 이 flat 으로 강제된다. 크롬에서는 안쪽 `.breathe`
      의 preserve-3d 가 방패막이가 되어 살아남았지만 그건 스펙이 보장하는 동작이
      아니다. **실측: `.breathe` 에 opacity(또는 filter)를 걸면 층간 변위가
      5.02px → -0.67px 로 즉시 붕괴한다.** 즉 층의 직속 부모에 한 번만 붙으면 끝난다.
      → 이 파일은 불투명도를 3D **바깥** 래퍼(.markBox)로 완전히 빼냈다. 3D 서브트리
      (.mark/.breathe) 안에는 grouping 속성이 하나도 없다. 어떤 엔진에서도 재발 불가.
      ⚠ 아래 [3D 금지 목록] 주석과 하단 회귀 가드를 반드시 읽을 것.
   2) **레이아웃을 애니메이션하지 않는다.** v2 는 네 군데를 위반했다 —
      .vrule{height}, .hrule{width}, .bar{width, 5000ms 내내}, .edge{left}.
      전부 scaleY/scaleX/translateX 로 바꿨다. 이제 키프레임에 레이아웃 속성 0개.
   3) **판면(measure)이 하나다.** --m 하나가 워드마크·규칙선·캡션 표의 좌우 끝을
      지배하고 세로 리듬은 6px 배수(36/18/30/18)다. v2 는 워드마크 clamp(206,31vw,330)
      과 규칙선 min(56vw,410px)이 서로 다른 폭이라 정렬이 어긋나 있었다.
   4) **마지막 800ms 는 완전히 정지한다(HOLD).** 호흡은 무한 루프가 아니라 1회다.
      한 번도 멎지 않는 화면은 타이틀이 아니라 로딩 스피너로 읽힌다.

   ▣ 화려함을 어디까지 풀었나 — 새 색은 0개다
   · --accent-2 / --accent / --accent-3 을 OKLCh 로 찍으면
     L .2878/.3740/.4804, C .0454/.0607/.0741, h 169.3/167.1/166.0 —
     브랜드가 이미 **명암 램프**를 정의해 두었다. 22층의 색은 전부 그 꺾은선 위의
     점이고, 노출을 역산해 **앞면 중앙이 정확히 #1A4B3A** 가 되게 고정했다.
     스포이트로 찍으면 브랜드색이 나온다. CI 는 1비트도 안 움직였다.
   · **빛나는 것은 없고, 빛을 받는 것만 있다.** 광원은 물체 밖에 있고 표면은 반사만
     한다. 노린 재질은 금속·유리가 아니라 무광 도장(반광 락커) — 스페큘러 로브를
     일부러 넓고 약하게(지수 5·10, 최대 22%) 잡았다. 좁고 센 하이라이트는 크롬 도금이다.
   · filter / blur / box-shadow / mix-blend-mode **0개.** 접지 그림자는 blur 가 아니라
     radial-gradient 두 장이고 물체의 초록을 머금는다(반사광).

   ▣ CSP: 외부 리소스 0. 종이결은 data-URI 타일(img-src 'self' data: 로 허용).
     광택은 **SVG 내부 clipPath** 로만 클립한다 — HTML 원소에 mask:url() 을 걸면
     사파리의 3D 컨텍스트에서 깨진 이력이 있다. 그 위험을 아예 만들지 않았다.

   ▣ 언제 뜨지 않는가(전부 의도된 것)
     한 세션 1회 · prefers-reduced-motion · ?nointro · 백그라운드 탭이면 대기
     클릭 · Esc · 아무 키 · [건너뛰기] 로 즉시 닫힘 · ?intro 로 강제 재생(점검용)
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var KEY = "sl-intro-seen";
  var TOTAL = 5000;

  /* ── 타임라인(ms). 여기만 만지면 전부 따라 움직인다 ────────────────── */
  var T = {
    VR:      20,    // 세로 헤어라인이 자란다
    MARK:    180,   // 심볼 등장(회전 진입 + 접지 그림자)
    SHEEN:   900,   // 광택 띠 — 밝은 중심이 ≈1360ms 에 앞면 중앙을,
                    //           ≈1560ms 에 앞면 오른쪽 끝을 지난다(실측)
    WIPE:    1620,  // 워드마크 — 띠가 앞면을 빠져나가고(1560) 심볼이 자세를 잡는(1680)
                    //           그 박자. 시간표가 아니라 결과다.
    REST:    1680,  // 심볼 정지 자세 도달
    BREATHE: 1850,  // 호흡 **1회**(무한 아님) → 3550ms 에 완전히 멎는다
    KO:      2500,
    HR:      2820,
    CAPS:    3020,
    HOLD:    3580,  // ← 여기부터 4380 까지 800ms, 화면이 완전히 정지한다
    OUT:     4380
  };
  var D = { IN: 1500, FADE: 500, SHEEN: 1250, WIPE: 880, BREATHE: 1700, OUT: 620 };

  var FORCE = location.search.indexOf("intro") >= 0 &&
              location.search.indexOf("nointro") < 0;

  function skipReason() {
    if (FORCE) return null;                    // 점검용 강제 재생(오너 미리보기 경로)
    try {
      if (location.search.indexOf("nointro") >= 0) return "쿼리";
      if (sessionStorage.getItem(KEY)) return "이번 세션에 이미 봄";
    } catch (e) { /* 스토리지 차단 — 그냥 재생한다 */ }
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return "동작 최소화 설정";
    }
    return null;
  }

  if (skipReason()) return;

  if (!FORCE && document.hidden) {             // 보이지도 않은 채 "봤음"으로 기록되면 안 된다
    document.addEventListener("visibilitychange", function once() {
      if (document.hidden) return;
      document.removeEventListener("visibilitychange", once);
      if (!skipReason()) start();
    });
    return;
  }

  start();

  /* ══════════════════════════════════════════════════════════════════
     조명 모델 — 부팅 시 1회 계산 → 정적 fill → 래스터 1회 → 프레임당 페인트 0
     ══════════════════════════════════════════════════════════════════ */
  function toS(c) { return c <= 0.0031308 ? c * 12.92 : 1.055 * Math.pow(c, 1 / 2.4) - 0.055; }
  function byte(c) { return Math.max(0, Math.min(255, Math.round(toS(c) * 255))); }
  function okRGB(L, a, b) {
    var l = Math.pow(L + 0.3963377774 * a + 0.2158037573 * b, 3),
        m = Math.pow(L - 0.1055613458 * a - 0.0638541728 * b, 3),
        s = Math.pow(L - 0.0894841775 * a - 1.2914855480 * b, 3);
    return [ 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  }
  /* 색역 밖이면 **명도는 지키고 채도만** 이분 탐색으로 줄인다(색이 탁해지지 않는다) */
  function hexOf(L, C, h) {
    var t = h * Math.PI / 180, a = C * Math.cos(t), b = C * Math.sin(t), lo = 0, hi = 1, r;
    for (var k = 0; k < 14; k++) {
      var q = (lo + hi) / 2; r = okRGB(L, a * q, b * q);
      if (r[0] >= -6e-4 && r[0] <= 1.0006 && r[1] >= -6e-4 && r[1] <= 1.0006 &&
          r[2] >= -6e-4 && r[2] <= 1.0006) lo = q; else hi = q;
    }
    r = okRGB(L, a * lo, b * lo);
    return "#" + ((1 << 24) + (byte(r[0]) << 16) + (byte(r[1]) << 8) + byte(r[2])).toString(16).slice(1);
  }
  /* 브랜드 램프 — accent-2 / accent / accent-3 의 OKLCh 좌표를 그대로 통과하는 꺾은선.
     밝기만 정하면 채도·색상이 브랜드가 정한 대로 따라온다. 새 색은 없다. */
  var A2 = [0.2878, 0.0454, 169.3], A1 = [0.3740, 0.0607, 167.1], A3 = [0.4804, 0.0741, 166.0];
  function ramp(L) {
    var p = L < A1[0] ? A2 : A1, q = L < A1[0] ? A1 : A3, u = (L - p[0]) / (q[0] - p[0]);
    return { C: Math.max(0.004, p[1] + (q[1] - p[1]) * u), h: p[2] + (q[2] - p[2]) * u };
  }
  var L_ACC = A1[0], LIGHT_L = 0.9673, LIGHT_H = 88.6;   // 광원색 = 종이색 #F6F4EF

  /* 3점 리그. x→오른쪽, y→위, z→보는 사람.
     key  좌상 전방 넓은 소프트박스 — 앞면 밝기를 정한다
     kick 우상 그레이징 — 드러난 옆면 띠만 훑어 모서리를 세운다
     bnc  아래 전방 — 종이에서 올라오는 따뜻한 반사광 */
  function nz(v) { var m = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]); return [v[0] / m, v[1] / m, v[2] / m]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  var KEY_D = nz([-0.44, 0.52, 0.73]), KICK_D = nz([0.50, 0.78, 0.20]), BNC_D = nz([0.26, -0.80, 0.54]);
  var hKey = nz([KEY_D[0], KEY_D[1], KEY_D[2] + 1]), hKick = nz([KICK_D[0], KICK_D[1], KICK_D[2] + 1]);
  var I_KEY = 0.66, I_KICK = 0.09, I_BNC = 0.13, I_AMB = 0.10;
  var S_KEY = 0.05, S_KICK = 0.34, E_KEY = 5, E_KICK = 10, S_FRESNEL = 0.05, S_MAX = 0.22;

  function wrap(d, w) { return Math.max(0, (d + w) / (1 + w)); }   // 넓은 광원은 형태를 감싼다
  function diffuse(n) {
    return I_KEY * wrap(dot(n, KEY_D), 0.35) + I_KICK * wrap(dot(n, KICK_D), 0.25)
         + I_BNC * wrap(dot(n, BNC_D), 0.55) + I_AMB;
  }
  function specular(n, k) {                                        // 무광 도장 = 넓고 약한 로브
    var s = S_KEY * Math.pow(Math.max(0, dot(n, hKey)), E_KEY)
          + S_KICK * Math.pow(Math.max(0, dot(n, hKick)), E_KICK);
    s += S_FRESNEL * Math.pow(1 - Math.abs(n[2]), 5);              // 시선에 수직인 면의 그레이징
    return s * k;
  }
  var D_FACE = diffuse([0, 0, 1]);
  var S_FACE = specular([0, 0, 1], 1) * (1.15 + 0.60) / 2;
  /* 노출 역산 — 앞면 중앙의 **최종** 색이 정확히 #1A4B3A 가 되게 확산광을 맞춘다.
     "브랜드색"은 곧 이 조명 아래 앞면의 겉보기색이다(실제 도장 샘플과 같은 정의). */
  var EXPOSURE = Math.pow(((L_ACC - S_FACE * LIGHT_L) / (1 - S_FACE)) / L_ACC, 3);

  function paint(d, s, k) {
    var Ld = L_ACC * Math.pow(Math.max(0.02, d / D_FACE * k * EXPOSURE), 1 / 3);   // L ∝ Y^(1/3)
    var t = Math.min(S_MAX, Math.max(0, s));
    var rel = Math.max(0, (t - S_FACE) / (S_MAX - S_FACE));   // 앞면보다 더 반짝이는 몫만 탈색
    var L = Ld + t * (LIGHT_L - Ld);                          // 유전체 정반사는 광원색이다
    var r = ramp(L), C = r.C * (1 - 0.18 * rel), h = r.h + (LIGHT_H - r.h) * 0.10 * rel;
    if (Ld < A2[0]) {                                         // 어두운 쪽은 종이 바운스가 지배
      var w = Math.min(1, (A2[0] - Ld) / 0.09) * 0.35;
      C *= (1 - 0.22 * w); h -= (r.h - 102) * w;
    }
    return hexOf(L, C, h);
  }
  function nrm(m, phi) {
    var c = Math.cos(phi), s = Math.sin(phi), L = Math.sqrt(m[0] * m[0] + m[1] * m[1]);
    return [m[0] / L * c, m[1] / L * c, s];
  }
  var RAD = Math.PI / 180;
  var SIDE_LIT = [0.622, 0.783], SIDE_DRK = [-0.622, -0.783];     // 옆면 축 ↗밝음 → ↙어두움
  function occlusion(t) { return 0.42 + 0.58 * Math.pow(t, 1.35); }
  function contact(i) { return 1 - 0.14 * Math.exp(-Math.pow(i / 2.4, 2)); }

  function shadeLayer(i, N, cham) {
    var t = i / (N - 1);
    var kind = i === N - 1 ? "face" : (i >= N - 4 ? "chamfer" : "wall");
    var phi = kind === "face" ? 90 * RAD : (kind === "chamfer" ? 45 * RAD : 0);
    var k = contact(i) * (kind === "face" ? 1 : occlusion(t));
    var nl, nd;
    if (kind === "face") { nl = nd = [0, 0, 1]; }
    else { nl = nrm(SIDE_LIT, phi); nd = nrm(SIDE_DRK, phi); }
    var dl = diffuse(nl), dd = diffuse(nd), sl = specular(nl, k), sd = specular(nd, k);
    if (kind === "face") { dl *= 1.050; dd *= 0.950; sl *= 1.15; sd *= 0.60; }
    return {
      kind: kind,
      lit: paint(dl, sl, k), mid: paint((dl + dd) / 2, (sl + sd) / 2, k), drk: paint(dd, sd, k),
      /* 앞 4층은 진짜 45° 모따기 — **앞면이 가장 작고** 뒤로 갈수록 넓어진다.
         작은 뷰포트에서 안티에일리어싱에 먹히지 않게 인셋을 키운다(cham). */
      scale: i > N - 5 ? 1 - cham * (i - (N - 5)) : (i < 3 ? 1 - 0.0030 * (3 - i) : 1)
    };
  }

  /* ══════════════════════════════════════════════════════════════════ */
  function start() {
    var SMALL = innerWidth < 620;
    var LOW = SMALL || (navigator.hardwareConcurrency || 8) <= 4 ||
              (window.devicePixelRatio || 1) > 2.4;
    /* 두께(THICK)는 고정이고 STEP 만 늘어난다 → 그림은 같고 칠할 면만 36% 준다.
       레이어 메모리는 DPR 2 기준으로 잡는다: 352²×4B×22 ≈ 11MB(14층이면 7MB). */
    var LAYERS = LOW ? 14 : 22, THICK = 19, STEP = THICK / (LAYERS - 1);
    var CHAM = SMALL ? 0.0062 : 0.0042;

    /* 종이결 — feTurbulence 를 data-URI 타일 1장으로 굽고 background-size 로 반복한다.
       딱 한 번 래스터되고 그 뒤엔 정적 비트맵이다(움직이지 않는다). */
    var GRAIN = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.5'/%3E%3C/svg%3E\")";

    var css = [
      /* ── 판면 ──────────────────────────────────────────────────────
         --m 하나가 워드마크·규칙선·캡션 표의 **같은 좌우 끝**을 만든다.
         규칙선만 넓히는 순간 아마추어가 된다. 세로는 6px 배수(36/18/30/18). */
      '#sl-intro{--m:clamp(212px,32vw,344px);--mk:clamp(124px,15.5vw,176px);',
      '  position:fixed;inset:0;z-index:9999;overflow:hidden;',
      '  color:var(--ink,#15181B);',
      /* 배경은 처음부터 끝까지 한 번도 움직이지 않는다 — 페인트 1회 */
      '  background:radial-gradient(124% 92% at 50% 38%,var(--white,#FFFDFA) 0%,',
      '    var(--paper,#F6F4EF) 44%,var(--paper-2,#EFECE4) 78%,var(--paper-3,#E8E4DA) 100%);',
      '  animation:sl-out ' + D.OUT + 'ms cubic-bezier(.4,0,.24,1) ' + T.OUT + 'ms forwards}',
      /* 퇴장은 커튼이 아니라 **디졸브**다 — 뒤의 본문(같은 종이색)이 비쳐 나오며
         인트로가 "끝나는" 게 아니라 사이트가 "도착"하는 것으로 읽힌다 */
      '@keyframes sl-out{to{opacity:0;visibility:hidden}}',
      '#sl-intro .grain{position:absolute;inset:0;pointer-events:none;opacity:.34;',
      '  background-image:' + GRAIN + ';background-size:140px 140px}',

      '#sl-intro .stage{position:absolute;inset:0;display:grid;place-items:center;',
      '  align-content:center}',

      /* ── 세로 헤어라인 — height 애니메이션 금지, scaleY 로 자란다.
            심볼의 S 카운터(구멍)를 관통해 보이는 것은 **의도한 것이다.**
            22겹 전부에 같은 구멍이 뚫려 있다는 증거이고, 그게 이 물건이
            "색칠한 종이"가 아니라 진짜 뚫린 판이라는 가장 싼 증명이다. */
      '#sl-intro .vrule{position:absolute;top:50%;left:50%;width:1px;height:min(74vh,600px);',
      '  background:var(--rule,#DDD8CE);transform:translate(-50%,-50%) scaleY(0);',
      '  animation:sl-v .5s cubic-bezier(.2,.7,.2,1) ' + T.VR + 'ms forwards}',
      '@keyframes sl-v{to{transform:translate(-50%,-50%) scaleY(1)}}',

      /* ══ 심볼 ══════════════════════════════════════════════════════
         [3D 금지 목록] .markBox 안쪽(.mark / .breathe)에는 **절대로**
         opacity(<1) · filter · mask · clip-path · mix-blend-mode ·
         will-change:opacity 를 붙이지 마라. 하나만 붙어도 grouping 속성이 되어
         used transform-style 이 flat 으로 강제되고 22겹이 다시 한 장으로 눌린다.
         실측(Chrome): .breathe 에 opacity:.5 또는 filter 를 걸면 층간 변위가
         5.02px → -0.67px 로 즉시 붕괴한다. .mark 쪽은 크롬에선 .breathe 의
         preserve-3d 가 막아 주지만 **스펙이 보장하는 동작이 아니다** — 둘 다 금지.
         불투명도가 필요하면 → .markBox(3D 바깥, perspective 를 가진 래퍼)에 건다.
         leaf(.lay, .sheen)는 3D 자식이 없으므로 opacity/clip 을 걸어도 무해하다. */
      '#sl-intro .markCell{position:relative;display:grid;place-items:center;',
      '  width:var(--mk);height:var(--mk)}',
      '#sl-intro .markBox{position:absolute;inset:0;display:grid;place-items:center;',
      '  perspective:1250px;perspective-origin:50% 42%;',
      '  animation:sl-fade ' + D.FADE + 'ms linear ' + T.MARK + 'ms both}',
      '@keyframes sl-fade{0%{opacity:0}100%{opacity:1}}',
      '#sl-intro .mark{position:relative;width:100%;height:100%;',
      '  transform-style:preserve-3d;will-change:transform;',
      '  animation:sl-in ' + D.IN + 'ms ' + T.MARK + 'ms both}',
      /* 키프레임마다 개별 animation-timing-function — 하나의 애니메이션 안에서
         가속 → 오버슛 → 급정지를 만든다. JS 0줄, rAF 0회. */
      '@keyframes sl-in{',
      '  0%{transform:rotateY(-64deg) rotateX(-10deg) scale(.92);',
      '     animation-timing-function:cubic-bezier(.17,.86,.26,1)}',
      '  72%{transform:rotateY(4deg) rotateX(-2.5deg) scale(1.02);',
      '     animation-timing-function:cubic-bezier(.32,.9,.3,1)}',
      /* rotateX 는 **음수**여야 한다. 그래야 드러나는 옆면이 우상이 되어 키커와 맞는다.
         양수면 옆면이 우하로 내려가 조명과 어긋나고 형태가 안 선다.
         -96deg 로 시작하면 90도를 지나며 층계단이 빗살로 드러난다 → -64deg. */
      '  100%{transform:rotateY(-14deg) rotateX(-6deg) scale(1)}}',
      /* 호흡 — **무한이 아니라 1회.** 3550ms 에 정확히 0deg 로 돌아와 멎는다. */
      '#sl-intro .breathe{position:absolute;inset:0;transform-style:preserve-3d;',
      '  will-change:transform;',
      '  animation:sl-breathe ' + D.BREATHE + 'ms cubic-bezier(.4,0,.2,1) ' + T.BREATHE + 'ms both}',
      '@keyframes sl-breathe{0%,100%{transform:rotateY(0deg)}50%{transform:rotateY(3.2deg)}}',
      '#sl-intro .lay{position:absolute;inset:0}',
      '#sl-intro .lay svg,#sl-intro .sheen svg{width:100%;height:100%;display:block}',

      /* 접지 그림자 — blur 금지(22겹 × blur 는 즉사다). radial-gradient 두 장이면
         되고 합성 단계 텍스처 샘플링 2회라 사실상 공짜다. 컨택트는 물체의 초록을
         머금는다(반사광) — 중성 회색이면 오려 붙인 티가 난다.
         ⚠ perspective 래퍼 **바깥**에 둔다. 안에 두면 z=0 의 앞면과 z-파이팅한다. */
      '#sl-intro .plinth{position:absolute;left:50%;top:50%;width:100%;height:100%;',
      '  transform:translate(-50%,-50%);pointer-events:none;',
      '  animation:sl-plinth ' + D.IN + 'ms cubic-bezier(.17,.86,.26,1) ' + T.MARK + 'ms both}',
      '#sl-intro .shA{position:absolute;left:50%;top:56%;width:214%;height:66%;',
      '  transform:translate(-50%,0);background:radial-gradient(50% 50% at 50% 50%,',
      '  rgba(21,38,31,.097),rgba(21,38,31,.052) 44%,rgba(21,38,31,0) 74%)}',
      '#sl-intro .shB{position:absolute;left:53%;top:63%;width:96%;height:22%;',
      '  transform:translate(-50%,0);background:radial-gradient(50% 50% at 50% 50%,',
      '  rgba(21,38,31,.288),rgba(21,38,31,.14) 46%,rgba(21,38,31,0) 78%)}',
      '@keyframes sl-plinth{0%{opacity:0;transform:translate(-50%,-50%) scale(1.5,.5)}',
      '  55%{opacity:.55}100%{opacity:1;transform:translate(-50%,-50%) scale(1)}}',

      /* ── 광택 — **SVG 내부 clipPath** 로만 클립한다.
            HTML 원소에 mask:url() 을 걸면 사파리의 preserve-3d 안에서 깨진 이력이 있다.
            여기서는 SVG 안에서 끝나므로 그 위험이 아예 없다.
            .sheen 은 leaf 다(3D 자식 없음) → 여기 opacity 를 걸어도 3D 가 안 죽는다.
            .band/.drift 는 SVG <g> 이고 **translate 만** 쓴다(사파리에서 transform-origin
            해석이 갈리는 건 회전·스케일이지 이동이 아니다). 단위는 뷰박스 유저 유닛. */
      '#sl-intro .sheen{position:absolute;inset:0;transform:translateZ(.6px);',
      '  pointer-events:none}',
      '#sl-intro .band{animation:sl-band ' + D.SHEEN + 'ms cubic-bezier(.42,0,.34,1) ' + T.SHEEN + 'ms both}',
      '@keyframes sl-band{0%{transform:translateX(-32px)}100%{transform:translateX(74px)}}',
      /* 층 색은 정적이라 회전만으로는 하이라이트가 안 움직인다. 상주 반사광(.wash)을
         호흡과 **같은 지연·같은 주기**로 흔들어야 "물체가 돌면 빛이 흐른다"가 성립한다. */
      '#sl-intro .drift{animation:sl-drift ' + D.BREATHE + 'ms cubic-bezier(.4,0,.2,1) ' + T.BREATHE + 'ms both}',
      '@keyframes sl-drift{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}',
      '#sl-intro .wash{opacity:0;animation:sl-wash .6s ease-out ' + (T.SHEEN + 250) + 'ms forwards}',
      '@keyframes sl-wash{to{opacity:1}}',

      /* ── 워드마크 ────────────────────────────────────────────────
         aspect-ratio 로 **자리를 미리 잡는다.** fetch 로 늦게 도착하는 SVG 가
         레이아웃을 밀면 무대가 통째로 흔들린다. (주입 후 실제 viewBox 로 갱신한다 —
         CI 자산의 viewBox 가 나중에 교정돼도 이 파일은 안 고쳐도 된다.) */
      '#sl-intro .nameRow{position:relative;margin-top:36px;width:var(--m)}',
      '#sl-intro .name{color:var(--ink,#15181B);aspect-ratio:1010.7/100;',
      '  clip-path:inset(0 100% 0 0);',
      '  animation:sl-wipe ' + D.WIPE + 'ms cubic-bezier(.22,.72,.2,1) ' + T.WIPE + 'ms forwards}',
      '#sl-intro .name svg{width:100%;height:auto;display:block}',
      '@keyframes sl-wipe{to{clip-path:inset(0 0 0 0)}}',
      /* ⚠ v2 는 left 를 애니메이션했다(매 프레임 레이아웃). translateX 로 교체.
         이동량을 판면 --m 에서 직접 계산하므로 값이 정적이고 컴포지터가 가져간다.
         상하 페이드 그라디언트라 상자가 아니라 "지나가는 모서리"로 읽힌다. */
      '#sl-intro .edge{position:absolute;top:-12%;bottom:-12%;left:0;width:1px;opacity:0;',
      '  background:linear-gradient(to bottom,rgba(26,75,58,0),var(--accent,#1A4B3A) 18%,',
      '    var(--accent,#1A4B3A) 82%,rgba(26,75,58,0));',
      '  animation:sl-edge ' + D.WIPE + 'ms cubic-bezier(.22,.72,.2,1) ' + T.WIPE + 'ms forwards}',
      '@keyframes sl-edge{0%{opacity:.9;transform:translateX(0)}88%{opacity:.9}',
      '  100%{opacity:0;transform:translateX(var(--m))}}',

      '#sl-intro .ko{margin-top:18px;color:var(--ink-2,#4A5157);opacity:0;font-weight:500;',
      '  font-size:clamp(.8rem,1.35vw,.94rem);letter-spacing:.34em;text-indent:.34em;',
      '  animation:sl-rise .44s cubic-bezier(.2,.7,.2,1) ' + T.KO + 'ms forwards}',
      '@keyframes sl-rise{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}',

      /* ⚠ width 애니메이션 금지 → scaleX. 중앙에서 양쪽으로 자란다. 폭은 --m 이다. */
      '#sl-intro .hrule{margin-top:30px;height:1px;width:var(--m);',
      '  background:var(--rule-2,#C6C0B3);transform:scaleX(0);',
      '  animation:sl-h .64s cubic-bezier(.2,.7,.2,1) ' + T.HR + 'ms forwards}',
      '@keyframes sl-h{to{transform:scaleX(1)}}',

      /* 태그라인을 문장이 아니라 **표**로 짠다. 밀도는 여기서 생긴다.
         1fr auto 1fr auto 1fr — 구분선이 판면의 정확히 1/3·2/3 에 서고 양 끝 활자가
         규칙선 끝에 딱 맞는다. space-between 은 칸 너비가 달라 구분선이 삐뚤어 보인다.
         height 를 못 박아 웹폰트 swap 이 들어와도 무대 높이가 안 흔들린다.
         ⚠ IBM Plex **Mono 는 400·500 만** 로드된다(600 은 Sans KR 에만 있다).
            모노로 600 을 쓰면 합성 볼드로 뭉갠다 → 여기 활자는 전부 400. */
      '#sl-intro .caps{margin-top:18px;display:grid;align-items:center;height:14px;',
      '  grid-template-columns:1fr auto 1fr auto 1fr;width:var(--m);',
      '  font-family:var(--font-mono,monospace);font-weight:400;line-height:14px;',
      '  font-size:clamp(9.5px,1.05vw,11px);letter-spacing:.14em;color:var(--ink-3,#7C838A)}',
      '#sl-intro .caps span{opacity:0;white-space:nowrap;',
      '  animation:sl-rise .38s cubic-bezier(.2,.7,.2,1) both}',
      '#sl-intro .caps span:nth-of-type(1){text-align:left}',
      '#sl-intro .caps span:nth-of-type(2){text-align:center}',
      /* 자간은 마지막 글자 **뒤에도** 붙는다 — 오른끝 정렬을 되돌려 준다 */
      '#sl-intro .caps span:nth-of-type(3){text-align:right;margin-right:-.14em}',
      '#sl-intro .caps i{width:1px;height:11px;background:var(--rule-2,#C6C0B3);',
      '  transform:scaleY(0);animation:sl-div .3s cubic-bezier(.2,.7,.2,1) both}',
      '@keyframes sl-div{to{transform:scaleY(1)}}',

      '#sl-intro .skip{position:fixed;right:22px;bottom:22px;background:none;border:0;',
      '  font-family:var(--font-mono,monospace);font-size:.68rem;letter-spacing:.12em;',
      '  color:var(--ink-3,#7C838A);cursor:pointer;padding:10px 4px;text-transform:uppercase}',
      '#sl-intro .skip:hover,#sl-intro .skip:focus-visible{color:var(--accent,#1A4B3A)}',
      /* ⚠ v2 는 width 를 5000ms 내내 애니메이션했다 — 매 프레임 레이아웃이다.
         scaleX 로 바꾸면 같은 그림에 레이아웃 0회. 가장 큰 단일 성능 개선이다. */
      '#sl-intro .bar{position:fixed;left:0;bottom:0;height:2px;width:100%;',
      '  background:var(--accent,#1A4B3A);opacity:.4;transform:scaleX(0);transform-origin:0 50%;',
      '  animation:sl-bar ' + TOTAL + 'ms linear forwards}',
      '@keyframes sl-bar{to{transform:scaleX(1)}}',

      'html.sl-intro-on,html.sl-intro-on body{overflow:hidden}',
      '@media (prefers-reduced-motion:reduce){#sl-intro{display:none}}',
      '@media (max-width:620px){',
      '  #sl-intro{--m:min(calc(100vw - 40px),300px);--mk:min(40vw,152px)}',
      '  #sl-intro .markBox{perspective:900px}',
      '  #sl-intro .caps{font-size:9px;letter-spacing:.06em}',
      '  #sl-intro .caps span:nth-of-type(3){margin-right:-.06em}}',
      '@media (max-width:360px){#sl-intro .caps{font-size:8.5px;letter-spacing:.03em}}'
    ].join("\n");

    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var el = document.createElement("div");
    el.id = "sl-intro";
    el.setAttribute("role", "presentation");   // 장식이다. 본문은 뒤에 이미 있다.
    el.setAttribute("aria-hidden", "true");
    el.innerHTML =
      (LOW ? "" : '<div class="grain"></div>') +
      '<div class="stage">' +
        '<span class="vrule"></span>' +
        '<div class="markCell">' +
          '<div class="plinth"><i class="shA"></i><i class="shB"></i></div>' +
          '<div class="markBox"><div class="mark">' +
            '<div class="breathe" id="sl-mark"></div>' +
          '</div></div>' +
        '</div>' +
        '<div class="nameRow"><div class="name" id="sl-name"></div><span class="edge"></span></div>' +
        '<div class="ko">쉴더스랩</div>' +
        '<span class="hrule"></span>' +
        '<div class="caps">' +
          '<span style="animation-delay:' + T.CAPS + 'ms">ISMS-P 인증</span>' +
          '<i style="animation-delay:' + (T.CAPS + 70) + 'ms"></i>' +
          '<span style="animation-delay:' + (T.CAPS + 90) + 'ms">모의해킹</span>' +
          '<i style="animation-delay:' + (T.CAPS + 160) + 'ms"></i>' +
          '<span style="animation-delay:' + (T.CAPS + 180) + 'ms">취약점 진단</span>' +
        '</div>' +
      '</div>' +
      /* aria-hidden 컨테이너 안의 포커스 가능 요소는 접근성 위반이다.
         아무 키·클릭·5초로도 닫히므로 탭 순서에서 뺀다. */
      '<button class="skip" type="button" tabindex="-1">건너뛰기 ESC</button>' +
      '<span class="bar"></span>';

    document.documentElement.classList.add("sl-intro-on");
    document.body.appendChild(el);
    try { sessionStorage.setItem(KEY, "1"); } catch (e) { /* noop */ }

    /* ── 압출 심볼 만들기 ────────────────────────────────────────────
       symbol.svg 는 fill-rule=evenodd 짜리 **단일 컴파운드 패스**다(방패 + S 카운터).
       우리는 그 패스를 쪼개지 않는다 — 22겹 전부에 같은 구멍이 뚫리므로 S 는 끝까지
       진짜 관통 구멍이고, 회전하면 안쪽 벽이 드러난다. 문자열 파싱 가정이 0개라
       CI 를 재출력해도 조용히 깨질 곳이 없다(쪼개야 할 일이 생기면
       ci-meta.json 의 "shield" 필드를 써라 — 문자열 split 에 기대지 마라). */
    fetch("/assets/ci/symbol.svg")
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (txt) {
        var box = document.getElementById("sl-mark");
        if (!box) return;
        var d = "";
        if (txt) {
          var p = new DOMParser().parseFromString(txt, "image/svg+xml").querySelector("path");
          if (p) d = (p.getAttribute("d") || "").trim();
        }
        if (!d) {                              // 폴백 — 평면 한 장(인트로가 통째로 사라지진 않게)
          box.innerHTML = '<img src="/assets/ci/symbol.svg" alt="" ' +
                          'style="width:100%;height:100%;display:block">';
          return;
        }
        box.innerHTML = buildMark(d, LAYERS, STEP, CHAM);
      })
      .catch(function () { /* 폴백조차 실패해도 나머지 인트로는 진행된다 */ });

    /* 워드마크는 fill=currentColor 라 <img> 로는 색이 죽는다. 같은 출처라 그대로 끼운다. */
    fetch("/assets/ci/wordmark-en.svg")
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (txt) {
        var box = document.getElementById("sl-name");
        if (!box || !txt) return;
        box.innerHTML = txt;
        var svg = box.querySelector("svg");
        if (!svg) return;
        svg.removeAttribute("width"); svg.removeAttribute("height");
        /* 예약해 둔 비율을 실제 viewBox 로 갱신한다 — tools/build-ci.py 에서
           워드마크 viewBox 가 교정되면(현재 잉크가 잘려 있다) 자동으로 따라온다. */
        var vb = (svg.getAttribute("viewBox") || "").split(/[\s,]+/).map(Number);
        if (vb.length === 4 && vb[2] > 0 && vb[3] > 0) {
          box.style.aspectRatio = vb[2] + " / " + vb[3];
        }
      })
      .catch(function () { /* 워드마크만 빠진다 */ });

    /* 다 움직인 뒤 승격을 푼다 — 3580ms 이후는 완전 정지(HOLD)라 붙들고 있을 이유가 없다 */
    var relT = setTimeout(function () {
      var a = el.querySelector(".mark"), b = el.querySelector(".breathe");
      if (a) a.style.willChange = "auto";
      if (b) b.style.willChange = "auto";
    }, T.HOLD);

    /* ── 회귀 가드 (?intro 미리보기에서만 돈다) ────────────────────────
       3D 가 다시 평탄화되면 뒤 층과 앞 층이 화면에서 **완전히 겹친다.**
       정지 자세 rotateY(-14deg) 에서 두께 19px 은 가로 변위 ≈19×sin14° 를 만든다 —
       실측 데스크톱 5.02px / 모바일(perspective 900) 4.72px. 평탄화되면 0 이 된다.
       ⚠ 폭(width)으로 재면 안 된다. 모따기 때문에 앞면이 뒤층보다 오히려 작아서
          폭 차이는 0.4px 밖에 안 난다(실측). **좌표 변위**가 유일하게 신뢰할 신호다.
       이 파일을 나중에 손대는 사람이 "페이드 하나 추가"하다 v2 버그를 재발시킨다. */
    if (FORCE) setTimeout(function () {
      var l = el.querySelectorAll(".mark .lay");
      if (l.length < 3) return;
      var dx = l[0].getBoundingClientRect().left - l[l.length - 1].getBoundingClientRect().left;
      if (Math.abs(dx) < 2) {
        console.warn("[sl-intro] 3D 평탄화 감지(층간 변위 " + dx.toFixed(2) + "px) — " +
          ".mark/.breathe 계열에 opacity·filter·mask·clip-path·mix-blend-mode·" +
          "will-change:opacity 가 붙었는지 확인하라. 불투명도는 .markBox 가 진다.");
      }
    }, 2600);

    /* ── 종료 ── */
    var done = false;
    function close() {
      if (done) return;
      done = true;
      clearTimeout(relT);
      document.documentElement.classList.remove("sl-intro-on");
      el.style.transition = "opacity .32s ease";
      el.style.opacity = "0";
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 350);
      document.removeEventListener("keydown", onKey, true);
    }
    function onKey(e) {
      if (e.key === "Tab") return;   // 접근성 — 탭 이동까지 가로채지 않는다
      close();
    }
    el.addEventListener("click", close);
    document.addEventListener("keydown", onKey, true);
    setTimeout(close, TOTAL);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) close();  // 멈춘 애니메이션이 남아 있지 않게
    });
  }

  /* ══════════════════════════════════════════════════════════════════
     층 쌓기 — 그라디언트 defs 는 문서에 한 벌만 두고 각 층이 url(#id) 로 참조한다.
     그라디언트 fill 은 Skia 셰이더라 flat fill 과 래스터 비용이 사실상 같다.
     ══════════════════════════════════════════════════════════════════ */
  function buildMark(d, N, STEP, CHAM) {
    var defs = "", lays = "", i;
    for (i = 0; i < N; i++) {
      var L = shadeLayer(i, N, CHAM);
      /* 압출 층 하나는 단색밖에 못 칠하므로 등고선을 따라 도는 법선 변화를 표현할 수
         없다. 그런데 정지 자세가 rotateY(-14deg) rotateX(-6deg) 이면 뒤 층은 화면에서
         오른쪽·위로 밀리므로 **실제로 드러나는 옆면 띠는 우상 테두리 하나뿐**이다.
         즉 그 띠 방향의 선형 그라디언트 하나면 물리적으로 충분하다.
         덤으로 S 카운터의 벽은 정확히 반대쪽인 좌하로 드러나므로 같은 축에서 자동으로
         어두운 끝을 받는다 — 축 하나로 바깥과 안쪽이 동시에 맞는다.
         앞면은 키가 만드는 완만한 낙차 ↖→↘, 옆면·모따기는 키커가 훑는 ↗→↙. */
      var ax = L.kind === "face" ? [0.16, 0.02, 0.84, 0.98] : [0.88, 0.06, 0.12, 0.94];
      defs += '<linearGradient id="slG' + i + '" x1="' + ax[0] + '" y1="' + ax[1] +
              '" x2="' + ax[2] + '" y2="' + ax[3] + '">' +
              '<stop offset="0" stop-color="' + L.lit + '"/>' +
              '<stop offset=".5" stop-color="' + L.mid + '"/>' +
              '<stop offset="1" stop-color="' + L.drk + '"/></linearGradient>';
      var z = -(N - 1 - i) * STEP;             // i = N-1 이 앞면(z=0)
      lays += '<i class="lay" style="transform:translateZ(' + z.toFixed(2) + 'px)' +
              (L.scale !== 1 ? ' scale(' + L.scale.toFixed(4) + ')' : '') + '">' +
              svgTag('<path d="' + d + '" fill="url(#slG' + i + ')" fill-rule="evenodd"/>') +
              '</i>';
    }
    /* 광택 — SVG 안에서 끝난다(HTML mask 없음 = 사파리 위험 없음).
       .wash 는 상주 반사광(호흡과 같은 주기로 흐른다), .band 는 1회 통과하는 띠.
       최대 19% 흰색 — 앞면 위에서 R 26→45. 그 이상은 광택 도장이 되고 싸구려가 된다. */
    var sheen =
      '<i class="sheen">' + svgTag(
        '<defs>' +
          '<linearGradient id="slBand" x1="0" y1="0" x2="1" y2="0">' +
            '<stop offset="0" stop-color="#FFFDFA" stop-opacity="0"/>' +
            '<stop offset=".40" stop-color="#FFFDFA" stop-opacity=".11"/>' +
            '<stop offset=".52" stop-color="#FFFDFA" stop-opacity=".19"/>' +
            '<stop offset=".64" stop-color="#FFFDFA" stop-opacity=".09"/>' +
            '<stop offset="1" stop-color="#FFFDFA" stop-opacity="0"/></linearGradient>' +
          '<linearGradient id="slWash" x1=".08" y1="0" x2=".92" y2="1">' +
            '<stop offset="0" stop-color="#FFFDFA" stop-opacity=".075"/>' +
            '<stop offset=".42" stop-color="#FFFDFA" stop-opacity=".035"/>' +
            '<stop offset=".78" stop-color="#FFFDFA" stop-opacity="0"/></linearGradient>' +
          '<clipPath id="slClip"><path d="' + d + '" clip-rule="evenodd"/></clipPath>' +
        '</defs>' +
        '<g clip-path="url(#slClip)"><g class="drift">' +
          '<rect class="wash" x="-8" y="-8" width="80" height="80" fill="url(#slWash)"/>' +
          '<g class="band"><rect x="0" y="-26" width="26" height="116" ' +
            'fill="url(#slBand)" transform="rotate(15 13 32)"/></g>' +
        '</g></g>') + '</i>';

    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' +
           '<defs>' + defs + '</defs></svg>' + lays + sheen;
  }

  function svgTag(inner) {
    return '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
           inner + '</svg>';
  }
})();
