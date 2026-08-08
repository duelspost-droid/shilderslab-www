/* ══════════════════════════════════════════════════════════════════════
   홈 인트로 — 5초. CI 심볼을 **실제로 압출한 입체**로 세워 보여 준다.

   무엇이 3D 인가
   · 심볼(symbol.svg)은 fill-rule=evenodd 짜리 **단일 컴파운드 패스**다.
     그 패스를 22장 복제해 z 축으로 0.85px 씩 밀어 쌓으면 두께가 생긴다.
     회전하면 옆면이 실제로 드러난다 — 그림자를 흉내 낸 것이 아니라 형태가 있는 것이다.
   · 정지 자세를 정면(0도)이 아니라 rotateY(-11deg) rotateX(4.5deg) 로 둔다.
     정면으로 세우면 옆면이 사라져 다시 납작해 보이기 때문이다.
   · 앞면은 딥 파인(--accent), 옆면 층은 한 단 어두운 --accent-2 다.
     새 색을 만들지 않았고 그라데이션·글로우도 쓰지 않았다(v2 브랜드 규칙).

   왜 라이브러리를 안 쓰는가
   · CSP 가 script-src 'self' 이고, 이 저장소는 CDN 의존을 없애 온 이력이 있다
     (supabase-js 도 자체 호스팅). three.js 를 끌어오면 그 결정을 되돌린다.

   언제 뜨지 않는가 (전부 의도된 것이다)
   · 한 세션에 한 번만 · prefers-reduced-motion 이면 재생하지 않음
   · ?nointro 로 끄고 ?intro 로 다시 본다(미리보기·점검용)
   · 클릭 · Esc · 아무 키 · [건너뛰기] 로 즉시 닫힘
   · **백그라운드 탭에서 열렸다면 시작하지 않고 기다린다** — 보이지도 않은 채
     "봤음"으로 기록되면 정작 탭을 열었을 때 영영 안 나온다.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var KEY = "sl-intro-seen";
  var TOTAL = 5000;      // 전체 길이(ms). 아래 타임라인 상수와 함께 움직인다.
  var LAYERS = 22;       // 압출 층수. 많을수록 옆면이 매끈하다.
  var STEP = 0.85;       // 층 간격(px). LAYERS × STEP ≒ 19px 두께.

  var FORCE = location.search.indexOf("intro") >= 0 &&
              location.search.indexOf("nointro") < 0;

  function skipReason() {
    if (FORCE) return null;
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
    var REST = "rotateY(-11deg) rotateX(4.5deg)";

    var css = [
      '#sl-intro{position:fixed;inset:0;z-index:9999;background:var(--paper,#F6F4EF);',
      '  display:grid;place-items:center;overflow:hidden;',
      '  animation:sl-out .62s cubic-bezier(.4,0,.2,1) ' + (TOTAL - 620) + 'ms forwards}',
      '#sl-intro .stage{position:relative;display:grid;place-items:center;',
      '  perspective:1250px;perspective-origin:50% 44%}',

      /* 세로 헤어라인 — 중앙에서 위아래로 */
      '#sl-intro .vrule{position:absolute;top:50%;left:50%;width:1px;height:0;',
      '  background:var(--rule,#DDD8CE);transform:translate(-50%,-50%);',
      '  animation:sl-v .5s cubic-bezier(.2,.7,.2,1) .02s forwards}',
      '@keyframes sl-v{to{height:min(74vh,600px)}}',

      /* 압출 심볼 */
      '#sl-intro .mark{position:relative;transform-style:preserve-3d;',
      '  width:clamp(112px,15.5vw,176px);height:clamp(112px,15.5vw,176px);',
      '  animation:sl-in 1.5s cubic-bezier(.17,.86,.26,1) .18s both}',
      '#sl-intro .mark .lay{position:absolute;inset:0;width:100%;height:100%;',
      '  transform-style:preserve-3d}',
      '#sl-intro .mark svg{width:100%;height:100%;display:block}',
      '@keyframes sl-in{',
      '  0%{transform:rotateY(-96deg) rotateX(10deg) scale(.9);opacity:0}',
      '  40%{opacity:1}',
      '  72%{transform:rotateY(3deg) rotateX(2deg) scale(1.02)}',
      '  100%{transform:' + REST + ' scale(1);opacity:1}}',
      /* 정착 후 아주 미세한 호흡 — 정지 화면처럼 굳지 않게 */
      /* ⚠ 크기를 반드시 준다. 안 주면 이 래퍼가 0×0 이 되고,
         inset:0 인 층들이 전부 접혀 심볼이 사라진다(실제로 그랬다). */
      '#sl-intro .breathe{position:absolute;inset:0;',
      '  animation:sl-breathe 5.4s ease-in-out 1.75s infinite;',
      '  transform-style:preserve-3d}',
      '@keyframes sl-breathe{0%,100%{transform:rotateY(0deg)}50%{transform:rotateY(4.5deg)}}',

      /* 워드마크 — 진행하는 헤어라인이 지나가며 드러난다 */
      '#sl-intro .nameRow{position:relative;margin-top:32px;',
      '  width:clamp(206px,31vw,330px)}',
      '#sl-intro .name{color:var(--ink,#15181B);clip-path:inset(0 100% 0 0);',
      '  animation:sl-wipe .92s cubic-bezier(.22,.72,.2,1) 1.5s forwards}',
      '#sl-intro .name svg{width:100%;height:auto;display:block}',
      '@keyframes sl-wipe{to{clip-path:inset(0 0 0 0)}}',
      '#sl-intro .edge{position:absolute;top:-6%;bottom:-6%;left:0;width:1px;',
      '  background:var(--accent,#1A4B3A);opacity:0;',
      '  animation:sl-edge .92s cubic-bezier(.22,.72,.2,1) 1.5s forwards}',
      '@keyframes sl-edge{0%{opacity:.9;left:0}92%{opacity:.9}100%{opacity:0;left:100%}}',

      '#sl-intro .ko{margin-top:13px;color:var(--ink-2,#4A5157);opacity:0;',
      '  font-size:clamp(.84rem,1.45vw,.98rem);letter-spacing:.03em;',
      '  animation:sl-rise .5s cubic-bezier(.2,.7,.2,1) 2.35s forwards}',
      '#sl-intro .hrule{margin-top:26px;height:1px;width:0;background:var(--rule-2,#C6C0B3);',
      '  animation:sl-h .7s cubic-bezier(.2,.7,.2,1) 2.75s forwards}',
      '@keyframes sl-h{to{width:min(56vw,410px)}}',
      '#sl-intro .tag{margin-top:22px;color:var(--ink-3,#7C838A);opacity:0;text-align:center;',
      '  font-size:clamp(.71rem,1.15vw,.81rem);letter-spacing:.02em;',
      '  animation:sl-rise .55s cubic-bezier(.2,.7,.2,1) 3.1s forwards}',
      '@keyframes sl-rise{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}',

      '#sl-intro .skip{position:fixed;right:22px;bottom:22px;background:none;border:0;',
      '  font-family:var(--font-mono,monospace);font-size:.68rem;letter-spacing:.12em;',
      '  color:var(--ink-3,#7C838A);cursor:pointer;padding:10px 4px;text-transform:uppercase}',
      '#sl-intro .skip:hover,#sl-intro .skip:focus-visible{color:var(--accent,#1A4B3A)}',
      '#sl-intro .bar{position:fixed;left:0;bottom:0;height:2px;width:0;',
      '  background:var(--accent,#1A4B3A);opacity:.45;',
      '  animation:sl-bar ' + TOTAL + 'ms linear forwards}',
      '@keyframes sl-bar{to{width:100%}}',
      '@keyframes sl-out{to{opacity:0;visibility:hidden}}',
      'html.sl-intro-on,html.sl-intro-on body{overflow:hidden}',
      '@media (prefers-reduced-motion: reduce){#sl-intro{display:none}}',
      '@media (max-width:620px){#sl-intro .stage{perspective:900px}}',
    ].join("\n");

    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var el = document.createElement("div");
    el.id = "sl-intro";
    el.setAttribute("role", "presentation");   // 장식이다. 본문은 뒤에 이미 있다.
    el.setAttribute("aria-hidden", "true");
    el.innerHTML =
      '<div class="stage">' +
        '<span class="vrule"></span>' +
        '<div class="mark"><div class="breathe" id="sl-mark"></div></div>' +
        '<div class="nameRow"><div class="name" id="sl-name"></div><span class="edge"></span></div>' +
        '<div class="ko">쉴더스랩</div>' +
        '<span class="hrule"></span>' +
        '<div class="tag">정보보호 컨설팅 — ISMS-P 인증 · 모의해킹 · 취약점 진단</div>' +
      "</div>" +
      '<button class="skip" type="button">건너뛰기 ESC</button>' +
      '<span class="bar"></span>';

    document.documentElement.classList.add("sl-intro-on");
    document.body.appendChild(el);
    try { sessionStorage.setItem(KEY, "1"); } catch (e) { /* noop */ }

    /* ── 압출 심볼 만들기 ────────────────────────────────────────────
       symbol.svg 의 패스를 가져와 층층이 쌓는다. 실패하면 원본 이미지 한 장으로 떨어진다
       (인트로가 통째로 사라지지는 않게). */
    var FACE = "#1A4B3A", BODY = "#0F3227";
    fetch("/assets/ci/symbol.svg")
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (txt) {
        var box = document.getElementById("sl-mark");
        if (!box) return;
        var d = "";
        if (txt) {
          var doc = new DOMParser().parseFromString(txt, "image/svg+xml");
          var p = doc.querySelector("path");
          if (p) d = p.getAttribute("d") || "";
        }
        if (!d) {                              // 폴백 — 평면 한 장
          box.innerHTML = '<img src="/assets/ci/symbol.svg" alt="" ' +
                          'style="width:100%;height:100%;display:block">';
          return;
        }
        var html = "";
        for (var i = 0; i < LAYERS; i++) {
          var z = -(LAYERS - 1 - i) * STEP;    // i = LAYERS-1 이 앞면(z=0)
          var fill = i === LAYERS - 1 ? FACE : BODY;
          html += '<div class="lay" style="transform:translateZ(' + z.toFixed(2) + 'px)">' +
                  '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
                  '<path d="' + d + '" fill="' + fill + '" fill-rule="evenodd"/></svg></div>';
        }
        box.innerHTML = html;
      })
      .catch(function () { /* 폴백조차 실패해도 나머지 인트로는 진행된다 */ });

    /* 워드마크는 fill=currentColor 라 <img> 로는 색이 죽는다. 같은 출처라 그대로 끼워 넣는다. */
    fetch("/assets/ci/wordmark-en.svg")
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (svg) {
        var box = document.getElementById("sl-name");
        if (box && svg) box.innerHTML = svg;
      })
      .catch(function () { /* 워드마크만 빠진다 */ });

    /* ── 종료 ── */
    var done = false;
    function close() {
      if (done) return;
      done = true;
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
      if (document.hidden) close();   // 멈춘 애니메이션이 남아 있지 않게
    });
  }
})();
