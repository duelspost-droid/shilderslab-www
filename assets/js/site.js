/* ──────────────────────────────────────────────────────────────
   쉴더스랩 — 공용 스크립트 v2
   내비 · 스크롤 진입 · 푸터 · 사이트 설정 반영 · 방문 로깅
   (배경 애니메이션·카운터·글로우는 v2에서 제거했다)
   ────────────────────────────────────────────────────────────── */
(function () {
  "use strict";
  var doc = document, C = (window.SL_CONFIG || {}).COMPANY || {};

  /* ─────────── 마스트헤드 ─────────── */
  var mast = doc.getElementById("masthead");
  if (mast) {
    var onScroll = function () {
      mast.classList.toggle("stuck", (window.scrollY || doc.documentElement.scrollTop) > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  var burger = doc.getElementById("burger");
  var nav = doc.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.classList.toggle("on", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      doc.documentElement.style.overflow = open ? "hidden" : "";
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        burger.classList.remove("on");
        doc.documentElement.style.overflow = "";
      }
    });
  }

  /* 현재 경로에 맞는 메뉴 표시 */
  if (nav) {
    var path = location.pathname.replace(/index\.html$/, "").replace(/\/+$/, "") || "/";
    Array.prototype.forEach.call(nav.querySelectorAll("a[href]"), function (a) {
      var href = a.getAttribute("href") || "";
      if (href.charAt(0) === "#" || /^https?:/i.test(href) || a.classList.contains("cta")) return;
      var norm = href.replace(/index\.html$/, "").replace(/\/+$/, "") || "/";
      if (norm !== "/" && path.indexOf(norm) === 0) a.classList.add("on");
      else if (norm === "/" && path === "/") a.classList.add("on");
    });
  }

  /* ─────────── 스크롤 진입 ─────────── */
  var rv = doc.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && rv.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -6% 0px" });
    Array.prototype.forEach.call(rv, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(rv, function (el) { el.classList.add("in"); });
  }

  /* ─────────── 푸터: 연도 · 사업자 정보(빈 값은 렌더 생략) ─────────── */
  Array.prototype.forEach.call(doc.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  var bizEl = doc.getElementById("bizline");
  var esc = (window.SL && window.SL.esc) || function (s) { return String(s == null ? "" : s); };

  /* 관리자 콘솔(sl_content 의 company.*)이 config.js 의 COMPANY 를 덮어쓴다.
     값이 비면 config.js 값을, 그것도 비면 아예 렌더하지 않는다(임시 문구 노출 방지). */
  function renderBizline(cnt) {
    if (!bizEl) return;
    function pick(key, fallback) {
      var row = cnt && cnt["company." + key];
      var v = row && typeof row.value === "string" ? row.value.trim() : "";
      return v || fallback || "";
    }
    var rows = [
      ["상호", pick("legal_name", C.legalKo) || C.nameKo],
      ["대표자", pick("ceo", C.ceo)],
      ["사업자등록번호", pick("biz_no", C.bizNo)],
      ["주소", pick("addr", C.addr)],
      ["대표번호", pick("tel", C.tel)],
      ["팩스", pick("fax", C.fax)],
      ["이메일", C.email],
      ["개인정보 보호책임자", pick("privacy_officer", C.privacyOfficer)],
    ].filter(function (r) { return r[1]; });
    bizEl.innerHTML = rows.map(function (r) {
      return "<b>" + esc(r[0]) + "</b> " + esc(r[1]);
    }).join("&nbsp; · &nbsp;");
  }
  renderBizline(null);   /* 백엔드 응답 전에도 config.js 기준으로 먼저 보여 준다 */

  /* ─────────── 페이지 문구(CMS) 반영 ───────────
     빌드가 이미 정적 HTML 로 구워 넣었다. 여기서 다시 그리는 이유는 관리자가 저장한 직후
     재빌드를 기다리지 않고 반영되게 하기 위함이다. 값이 비면 구워진 문구를 그대로 둔다. */
  function hydrateContent(cnt) {
    if (!cnt) return;
    Array.prototype.forEach.call(doc.querySelectorAll("[data-content]"), function (el) {
      var row = cnt[el.getAttribute("data-content")];
      if (!row) return;
      var v = typeof row.value === "string" ? row.value.trim() : "";
      if (!v) return;
      if (row.kind === "rich" && window.SL && SL.md) {
        el.innerHTML = SL.md(v);
      } else {
        el.innerHTML = esc(v).replace(/\n/g, "<br>");
      }
    });
  }

  /* ─────────── 사이트 설정 반영 + 공지 배너 ─────────── */
  if (window.SL && SL.db && SL.db() && !doc.body.hasAttribute("data-no-log")) {
    if (SL.loadContent) {
      SL.loadContent().then(function (cnt) {
        hydrateContent(cnt);
        renderBizline(cnt);
      }).catch(function () { /* 0005 미적용 등 — 구워진 문구를 그대로 둔다 */ });
    }
    SL.loadSettings().then(function (s) {
      if (s && typeof s.contact_email === "string" && s.contact_email) {
        Array.prototype.forEach.call(doc.querySelectorAll('a[href^="mailto:"]'), function (a) {
          var txt = (a.textContent || "").trim();
          a.setAttribute("href", "mailto:" + s.contact_email);
          if (/^[^@\s]+@[^@\s]+$/.test(txt)) a.textContent = s.contact_email;
        });
      }
      ["business_hours", "sla_note"].forEach(function (k) {
        if (!s || typeof s[k] !== "string" || !s[k]) return;
        Array.prototype.forEach.call(doc.querySelectorAll('[data-setting="' + k + '"]'), function (el) {
          el.textContent = s[k];
        });
      });

      var n = s && s.notice;
      if (!n || !n.on || !n.text) return;
      var e2 = SL.esc, href = SL.safeUrl(n.href);
      var bar = doc.createElement("div");
      bar.className = "notice-bar";
      bar.innerHTML = href
        ? '<a href="' + SL.escA(href) + '">' + e2(n.text) + " →</a>"
        : "<span>" + e2(n.text) + "</span>";
      doc.body.insertBefore(bar, doc.body.firstChild);
    });
  }

  /* ─────────── 방문 로깅 ─────────── */
  if (window.SL && SL.logVisit && !doc.body.hasAttribute("data-no-log")) {
    if ("requestIdleCallback" in window) requestIdleCallback(function () { SL.logVisit(); });
    else setTimeout(function () { SL.logVisit(); }, 1200);
  }
})();
