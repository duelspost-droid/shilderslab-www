/* ──────────────────────────────────────────────────────────────
   쉴더스랩 — 공용 사이트 스크립트 (내비·리빌·카운터·푸터·방문로깅)
   ────────────────────────────────────────────────────────────── */
(function () {
  "use strict";
  var doc = document, C = (window.SL_CONFIG || {}).COMPANY || {};

  /* ─────────── 내비게이션 ─────────── */
  var nav = doc.getElementById("nav");
  var bar = doc.getElementById("progress");
  var burger = doc.getElementById("burger");
  var menu = doc.getElementById("menu");

  function onScroll() {
    var y = window.scrollY || doc.documentElement.scrollTop;
    if (nav) nav.classList.toggle("scrolled", y > 24);
    if (bar) {
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      burger.classList.toggle("on", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        menu.classList.remove("open");
        burger.classList.remove("on");
      }
    });
  }

  /* 현재 경로에 맞는 메뉴 활성화 */
  (function activeLink() {
    if (!menu) return;
    var path = location.pathname.replace(/index\.html$/, "").replace(/\/+$/, "") || "/";
    Array.prototype.forEach.call(menu.querySelectorAll("a[href]"), function (a) {
      var href = a.getAttribute("href") || "";
      if (href.charAt(0) === "#" || /^https?:/i.test(href)) return;
      var norm = href.replace(/index\.html$/, "").replace(/\/+$/, "") || "/";
      if (norm !== "/" && path.indexOf(norm) === 0) a.classList.add("active");
      else if (norm === "/" && path === "/") a.classList.add("active");
    });
  })();

  /* ─────────── 스크롤 리빌 ─────────── */
  var revealEls = doc.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    Array.prototype.forEach.call(revealEls, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(revealEls, function (el) { el.classList.add("in"); });
  }

  /* ─────────── 숫자 카운트업 ─────────── */
  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count") || "0");
    var suffix = el.getAttribute("data-suffix") || "";
    var prefix = el.getAttribute("data-prefix") || "";
    var group = el.getAttribute("data-group") !== "false";
    var dur = 1500, t0 = null;
    function fmt(n) {
      var v = target % 1 === 0 ? Math.round(n) : Math.round(n * 10) / 10;
      return prefix + (group ? v.toLocaleString("ko-KR") : String(v)) + suffix;
    }
    function frame(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      el.textContent = fmt(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  var counters = doc.querySelectorAll("[data-count]");
  if (counters.length) {
    var reduce = false;
    try { reduce = matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
    if ("IntersectionObserver" in window && !reduce) {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { countUp(en.target); io2.unobserve(en.target); }
        });
      }, { threshold: 0.4 });
      Array.prototype.forEach.call(counters, function (el) { io2.observe(el); });
    } else {
      Array.prototype.forEach.call(counters, function (el) {
        var t = parseFloat(el.getAttribute("data-count") || "0");
        el.textContent = (el.getAttribute("data-prefix") || "") +
          t.toLocaleString("ko-KR") + (el.getAttribute("data-suffix") || "");
      });
    }
  }

  /* ─────────── 카드 포인터 글로우 ─────────── */
  Array.prototype.forEach.call(doc.querySelectorAll(".card"), function (card) {
    card.addEventListener("pointermove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
      card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
    });
  });

  /* ─────────── 히어로 실드 궤도 점 ─────────── */
  (function orbit() {
    var stage = doc.querySelector(".shield-stage");
    if (!stage) return;
    var dots = stage.querySelectorAll(".orbit-dot");
    if (!dots.length) return;
    var reduce = false;
    try { reduce = matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
    var t = 0;
    function tick() {
      t += 0.0042;
      Array.prototype.forEach.call(dots, function (d, i) {
        var rad = (stage.clientWidth / 2) * (i === 0 ? 0.89 : 0.67);
        var a = t * (i === 0 ? 1 : -1.35) + i * 2.1;
        d.style.transform = "translate(" + Math.cos(a) * rad + "px," + Math.sin(a) * rad + "px)";
      });
      requestAnimationFrame(tick);
    }
    if (!reduce) requestAnimationFrame(tick);
  })();

  /* ─────────── 푸터: 연도·사업자 정보(빈 값은 렌더 생략) ─────────── */
  Array.prototype.forEach.call(doc.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  var bizEl = doc.getElementById("bizline");
  if (bizEl) {
    var esc = (window.SL && window.SL.esc) || function (s) { return String(s == null ? "" : s); };
    var rows = [
      ["상호", C.legalKo || C.nameKo], ["대표자", C.ceo], ["사업자등록번호", C.bizNo],
      ["주소", C.addr], ["대표번호", C.tel], ["팩스", C.fax],
      ["이메일", C.email], ["개인정보 보호책임자", C.privacyOfficer],
    ].filter(function (r) { return r[1]; });
    bizEl.innerHTML = rows.map(function (r) {
      return "<b>" + esc(r[0]) + "</b> " + esc(r[1]);
    }).join(" &nbsp;·&nbsp; ");
  }

  /* ─────────── 공지 배너 (sl_settings.notice, 관리자 화면에서 관리) ─────────── */
  if (window.SL && SL.db && SL.db() && !doc.body.hasAttribute("data-no-log")) {
    SL.loadSettings().then(function (s) {
      var n = s && s.notice;
      if (!n || !n.on || !n.text) return;
      var esc = SL.esc, href = SL.safeUrl(n.href);
      var bar = doc.createElement("div");
      bar.className = "notice-bar";
      bar.innerHTML = href
        ? '<a href="' + SL.escA(href) + '">' + esc(n.text) + " <b>→</b></a>"
        : "<span>" + esc(n.text) + "</span>";
      doc.body.insertBefore(bar, doc.body.firstChild);
      doc.documentElement.classList.add("has-notice");
    });
  }

  /* ─────────── 방문 로깅 (백엔드 설정 시) ─────────── */
  if (window.SL && window.SL.logVisit && !doc.body.hasAttribute("data-no-log")) {
    if ("requestIdleCallback" in window) requestIdleCallback(function () { window.SL.logVisit(); });
    else setTimeout(function () { window.SL.logVisit(); }, 1200);
  }
})();
