/* ══════════════════════════════════════════════════════════════════════
   홈 인트로 — 약 8초. CI 심볼을 3D 로 세워 보여 준 뒤 로크업으로 정착시킨다.

   왜 이렇게 만들었는가
   · **외부 라이브러리를 쓰지 않는다.** CSP 가 script-src 'self' 이고, 이 저장소는
     CDN 의존을 없애 온 이력이 있다(supabase-js 도 자체 호스팅). three.js 같은 것을 끌어오면
     그 결정을 되돌리게 된다. 그래서 CSS 3D(perspective + translateZ 적층)로만 만든다.
   · **브랜드 규칙을 지킨다.** 그라데이션·블롭·글로우 금지, 로고 변형 금지(v2 규칙).
     입체감은 같은 색 판을 z 축으로 겹쳐 만든다. 새 색을 만들지 않는다.
   · **본문을 가리지 않는다.** 오버레이는 JS 가 나중에 끼워 넣는다. 정적 HTML 에는 없으므로
     크롤러와 JS 미실행 환경은 처음부터 본문을 본다.

   언제 뜨지 않는가 (전부 의도된 것이다)
   · 한 세션에 한 번만 — 매번 8초를 강제하면 재방문자에게는 방해다.
   · prefers-reduced-motion 이 켜져 있으면 아예 뜨지 않는다.
   · 주소에 ?nointro 가 있으면 건너뛴다(공유·점검용).
   · 클릭 · Esc · 아무 키 · [건너뛰기] 로 즉시 닫힌다.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var KEY = "sl-intro-seen";
  var TOTAL = 8000;          // 전체 길이(ms). 타임라인 CSS 와 함께 움직인다.

  /* ?intro — 세션 기록과 탭 상태를 무시하고 강제로 재생한다.
     오너가 다시 보고 싶을 때, 그리고 점검할 때 쓴다. */
  var FORCE = location.search.indexOf("intro") >= 0 &&
              location.search.indexOf("nointro") < 0;

  function skipReason() {
    if (FORCE) return null;
    try {
      if (location.search.indexOf("nointro") >= 0) return "쿼리";
      if (sessionStorage.getItem(KEY)) return "이번 세션에 이미 봄";
    } catch (e) { /* 스토리지 차단 환경 — 그냥 재생한다 */ }
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return "동작 최소화 설정";
    }
    return null;
  }

  if (skipReason()) return;

  /* 백그라운드 탭에서 열렸다면 **시작하지 않고 기다린다.**
     그냥 재생하면 화면에 보이지도 않은 채 타이머가 흐르고, "이번 세션에 봤다"고
     기록돼 정작 탭을 열었을 때는 영영 안 나온다. 보일 때 시작한다. */
  if (!FORCE && document.hidden) {
    document.addEventListener("visibilitychange", function once() {
      if (document.hidden) return;
      document.removeEventListener("visibilitychange", once);
      if (!skipReason()) start();
    });
    return;
  }

  start();

  function start() {
  /* ─────────── 스타일 (이 페이지에서만 쓰므로 여기서 주입한다) ─────────── */
  var css = [
    '#sl-intro{position:fixed;inset:0;z-index:9999;background:var(--paper,#F6F4EF);',
    '  display:grid;place-items:center;overflow:hidden;',
    '  animation:sl-out .7s cubic-bezier(.4,0,.2,1) ' + (TOTAL - 700) + 'ms forwards}',
    '#sl-intro .stage{position:relative;display:grid;place-items:center;gap:0;',
    '  perspective:1100px;perspective-origin:50% 45%}',

    /* 세로 헤어라인 — 중앙에서 위아래로 그어진다 */
    '#sl-intro .vrule{position:absolute;top:50%;left:50%;width:1px;height:0;',
    '  background:var(--rule,#DDD8CE);transform:translate(-50%,-50%);',
    '  animation:sl-vrule 1s cubic-bezier(.2,.7,.2,1) .05s forwards}',
    '@keyframes sl-vrule{to{height:min(72vh,560px)}}',

    /* 실드 — 같은 판을 z 로 겹쳐 두께를 만든다 */
    '#sl-intro .mark{position:relative;transform-style:preserve-3d;',
    '  width:clamp(104px,15vw,168px);height:clamp(104px,15vw,168px);',
    '  animation:sl-mark 2.4s cubic-bezier(.16,.84,.24,1) .35s both}',
    '#sl-intro .mark img{position:absolute;inset:0;width:100%;height:100%;display:block}',
    '#sl-intro .mark .depth{opacity:.09}',
    '@keyframes sl-mark{',
    '  0%{transform:rotateY(-78deg) translateZ(-40px) scale(.86);opacity:0}',
    '  55%{opacity:1}',
    '  78%{transform:rotateY(7deg) translateZ(0) scale(1.015)}',
    '  100%{transform:rotateY(0deg) translateZ(0) scale(1);opacity:1}}',

    /* 워드마크 — 좌→우 와이프 */
    '#sl-intro .name{margin-top:34px;color:var(--ink,#15181B);',
    '  width:clamp(210px,32vw,340px);',
    '  clip-path:inset(0 100% 0 0);opacity:0;',
    '  animation:sl-wipe 1.1s cubic-bezier(.2,.7,.2,1) 2.5s forwards}',
    '#sl-intro .name svg{width:100%;height:auto;display:block}',
    '@keyframes sl-wipe{0%{opacity:1;clip-path:inset(0 100% 0 0)}',
    '  100%{opacity:1;clip-path:inset(0 0 0 0)}}',

    '#sl-intro .ko{margin-top:14px;color:var(--ink-2,#4A5157);opacity:0;',
    '  font-size:clamp(.86rem,1.5vw,1rem);letter-spacing:.02em;',
    '  animation:sl-rise .8s cubic-bezier(.2,.7,.2,1) 3.5s forwards}',
    '#sl-intro .tag{margin-top:26px;color:var(--ink-3,#7C838A);opacity:0;',
    '  font-size:clamp(.72rem,1.2vw,.82rem);letter-spacing:.02em;text-align:center;',
    '  animation:sl-rise .8s cubic-bezier(.2,.7,.2,1) 4.5s forwards}',
    '@keyframes sl-rise{0%{opacity:0;transform:translateY(9px)}100%{opacity:1;transform:none}}',

    /* 가로 헤어라인 — 중앙에서 좌우로 */
    '#sl-intro .hrule{margin-top:30px;height:1px;width:0;background:var(--rule-2,#C9C3B6);',
    '  animation:sl-hrule 1.2s cubic-bezier(.2,.7,.2,1) 5.1s forwards}',
    '@keyframes sl-hrule{to{width:min(58vw,420px)}}',

    '#sl-intro .skip{position:fixed;right:22px;bottom:22px;background:none;border:0;',
    '  font-family:var(--font-mono,monospace);font-size:.68rem;letter-spacing:.12em;',
    '  color:var(--ink-3,#7C838A);cursor:pointer;padding:10px 4px;text-transform:uppercase}',
    '#sl-intro .skip:hover,#sl-intro .skip:focus-visible{color:var(--accent,#1A4B3A)}',
    '#sl-intro .bar{position:fixed;left:0;bottom:0;height:2px;width:0;',
    '  background:var(--accent,#1A4B3A);opacity:.5;',
    '  animation:sl-bar ' + TOTAL + 'ms linear forwards}',
    '@keyframes sl-bar{to{width:100%}}',
    '@keyframes sl-out{to{opacity:0;visibility:hidden}}',
    'html.sl-intro-on,html.sl-intro-on body{overflow:hidden}',
    /* 안전장치 — 동작 최소화 환경에서 혹시 열렸다면 즉시 지운다 */
    '@media (prefers-reduced-motion: reduce){#sl-intro{display:none}}',
  ].join("\n");

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  /* ─────────── 마크업 ─────────── */
  var el = document.createElement("div");
  el.id = "sl-intro";
  /* 스크린리더에는 장식이다. 본문은 뒤에 이미 있다. */
  el.setAttribute("role", "presentation");
  el.setAttribute("aria-hidden", "true");
  el.innerHTML =
    '<div class="stage">' +
      '<span class="vrule"></span>' +
      '<div class="mark">' +
        /* 두께 판. z 로만 밀면 정면에서 겹쳐 보이지 않으니 대각선으로도 조금 민다.
           그래야 회전이 끝난 뒤에도 입체가 남는다. 색은 팔레트 밖으로 나가지 않게
           단색 판을 낮은 불투명도로 겹치기만 한다(그라데이션·글로우 금지). */
        '<img class="depth" src="/assets/ci/symbol-mono-black.svg" alt="" style="transform:translate3d(7px,7px,-11px)">' +
        '<img class="depth" src="/assets/ci/symbol-mono-black.svg" alt="" style="transform:translate3d(5px,5px,-8px)">' +
        '<img class="depth" src="/assets/ci/symbol-mono-black.svg" alt="" style="transform:translate3d(3px,3px,-5px)">' +
        '<img class="depth" src="/assets/ci/symbol-mono-black.svg" alt="" style="transform:translate3d(1.5px,1.5px,-2px)">' +
        '<img src="/assets/ci/symbol.svg" alt="">' +
      "</div>" +
      '<div class="name" id="sl-intro-name"></div>' +
      '<div class="ko">쉴더스랩</div>' +
      '<span class="hrule"></span>' +
      '<div class="tag">정보보호 컨설팅 — ISMS-P 인증 · 모의해킹 · 취약점 진단</div>' +
    "</div>" +
    '<button class="skip" type="button">건너뛰기 ESC</button>' +
    '<span class="bar"></span>';

  /* 워드마크는 fill="currentColor" 라 <img> 로는 색이 죽는다.
     같은 출처 파일이라 그대로 끼워 넣고 색을 물려준다. */
  fetch("/assets/ci/wordmark-en.svg")
    .then(function (r) { return r.ok ? r.text() : ""; })
    .then(function (svg) {
      var box = document.getElementById("sl-intro-name");
      if (box && svg) box.innerHTML = svg;
    })
    .catch(function () { /* 없으면 워드마크만 빠진다 — 인트로는 계속된다 */ });

  document.documentElement.classList.add("sl-intro-on");
  document.body.appendChild(el);
  try { sessionStorage.setItem(KEY, "1"); } catch (e) { /* noop */ }

  /* ─────────── 종료 ─────────── */
  var done = false;
  function close() {
    if (done) return;
    done = true;
    document.documentElement.classList.remove("sl-intro-on");
    el.style.transition = "opacity .35s ease";
    el.style.opacity = "0";
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 380);
    document.removeEventListener("keydown", onKey, true);
  }
  function onKey(e) {
    if (e.key === "Tab") return;      // 접근성 — 탭 이동까지 가로채지 않는다
    close();
  }

  el.addEventListener("click", close);
  document.addEventListener("keydown", onKey, true);
  setTimeout(close, TOTAL);
  /* 재생 중에 탭을 벗어나면 닫는다 — 애니메이션이 멈춘 채 남아 있지 않게. */
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) close();
  });
  }
})();
