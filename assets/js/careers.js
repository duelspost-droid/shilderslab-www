/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_dynamic.py 의 CAR_JS 상수. */
(function () {
  var listEl = document.getElementById("job-list");
  /* 빌드가 이미 공고를 정적으로 구워 뒀는지 — <details> 가 있으면 그렇다.
     그러면 백엔드 미설정·조회 실패 시에도 그 목록을 지우지 않는다(크롤러가 본 것과 같은 화면). */
  var hasStatic = !!listEl.querySelector("details");
  var EMPTY = '<div class="empty">현재 공개된 공고가 없습니다. 상시 지원은 아래 양식을 이용해 주세요.</div>';

  function card(j) {
    var metas = [j.team, j.employment_type, j.location].filter(Boolean).map(SL.esc).join(" · ");
    return '<details><summary><span class="jt"><b>' + SL.esc(j.title) + "</b><span>" + metas +
      (j.closes_at ? " · 마감 " + SL.esc(SL.fmtDate(j.closes_at)) : " · 채용 시 마감") +
      '</span></span><span class="open">상세 +</span></summary>' +
      '<div class="jbody">' + SL.esc(j.body || j.summary || "") +
      '<div style="margin-top:22px"><a class="btn btn-sm" href="#apply">이 포지션 지원하기</a></div></div></details>';
  }

  if (!window.SL || !SL.db()) {
    /* 백엔드 미설정 — 빌드가 구운 정적 목록을 그대로 둔다. 정적도 없으면(빌드 전) 안내. */
    if (!hasStatic) listEl.innerHTML = EMPTY;
    return;
  }
  SL.listPublished("sl_jobs", {
    columns: "title,team,employment_type,location,summary,body,closes_at",
    order: { col: "sort_order", asc: true }, limit: 30
  }).then(function (r) {
    /* 조회 실패면 정적 목록을 남긴다(DB 가 아니라 네트워크 문제일 수 있다). */
    if (r && r.error) { if (!hasStatic) listEl.innerHTML = EMPTY; return; }
    var rows = (r && r.data) || [];
    /* DB 가 정본이다 — 성공 응답이면 0개라도 정적 목록을 최신 상태로 맞춘다. */
    listEl.innerHTML = rows.length ? rows.map(card).join("") : EMPTY;
  }).catch(function () {
    if (!hasStatic) listEl.innerHTML = '<div class="empty">공고를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.</div>';
  });

  var form = document.getElementById("apply-form");
  var alertEl = document.getElementById("ap-alert");
  var btn = document.getElementById("ap-submit");

  function show(kind, msg) {
    alertEl.className = "alert on " + kind;
    alertEl.textContent = msg;
    alertEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  function markErr(el, bad) {
    var f = el.closest(".field"); if (f) f.classList.toggle("err", !!bad);
    /* 시각(빨간 밑줄)만이 아니라 프로그램적으로도 오류를 알린다(WCAG 3.3.1·4.1.2).
       오류 문구 .msg 를 aria-describedby 로 연결해 스크린리더가 필드에서 사유를 읽게 한다. */
    el.setAttribute("aria-invalid", bad ? "true" : "false");
    var msg = f && f.querySelector(".msg");
    if (msg) {
      if (!msg.id) msg.id = el.id + "-msg";
      var d = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean);
      var i = d.indexOf(msg.id);
      if (bad && i < 0) d.push(msg.id);
      if (!bad && i >= 0) d.splice(i, 1);
      if (d.length) el.setAttribute("aria-describedby", d.join(" "));
      else el.removeAttribute("aria-describedby");
    }
  }

  /* 검증 규칙을 한 곳에 둔다 — 제출할 때와 '고치는 즉시 풀어 줄 때' 같은 기준을 써야 한다. */
  function checks() {
    var g = function (id) { return document.getElementById(id); };
    return [[g("ap-name"), !g("ap-name").value.trim()],
            [g("ap-email"), !/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(g("ap-email").value.trim())],
            [g("ap-position"), !g("ap-position").value],
            [g("ap-summary"), g("ap-summary").value.trim().length < 10]];
  }
  /* 오류를 고치면 그 자리에서 빨간 표시가 사라진다(재제출 전까지 남아 있지 않게). */
  checks().forEach(function (p) {
    var el = p[0];
    if (!el) return;
    var ev = el.tagName === "SELECT" ? "change" : "input";
    el.addEventListener(ev, function () {
      if (!el.closest(".field") || !el.closest(".field").classList.contains("err")) return;
      var still = false;
      checks().forEach(function (q) { if (q[0] === el) still = q[1]; });
      if (!still) markErr(el, false);
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var hp = document.getElementById("ap-website");
    if (hp && hp.value) {
      form.reset();
      show("ok", "지원서가 접수되었습니다. 확인 후 이메일로 연락드립니다.");
      return;
    }
    var name = document.getElementById("ap-name");
    var email = document.getElementById("ap-email");
    var pos = document.getElementById("ap-position");
    var summary = document.getElementById("ap-summary");
    var consent = document.getElementById("ap-consent");
    var link = document.getElementById("ap-link");
    var phone = document.getElementById("ap-phone");

    var bad = false, firstBad = null;
    checks().forEach(function (p) {
      markErr(p[0], p[1]); if (p[1]) { bad = true; if (!firstBad) firstBad = p[0]; }
    });
    if (bad) { show("bad", "입력값을 확인해 주세요."); if (firstBad) firstBad.focus(); return; }
    if (!consent.checked) { show("bad", "개인정보 수집·이용 동의가 필요합니다."); return; }

    var c = SL.db();
    if (!c) { show("bad", "지금은 접수를 처리할 수 없습니다. contact@shilderslab.com 으로 보내주세요."); return; }

    btn.disabled = true; btn.textContent = "제출 중…";
    c.rpc("sl_apply", {
      p_name: name.value.trim(), p_email: email.value.trim(), p_phone: phone.value.trim(),
      p_position: pos.value, p_summary: summary.value.trim(), p_link: link.value.trim(), p_consent: true
    }).then(function (r) {
      if (r.error) throw r.error;
      form.reset();
      show("ok", "지원서가 접수되었습니다. 확인 후 이메일로 연락드립니다.");
      btn.textContent = "접수 완료";
      /* 영구 비활성으로 두면 다른 포지션에 다시 지원할 수 없다. 잠깐 뒤 되살린다. */
      setTimeout(function () { btn.disabled = false; btn.textContent = "지원서 제출"; }, 4000);
    }).catch(function (err) {
      var m = (err && err.message) || "";
      show("bad", /too many|rate/i.test(m)
        ? "잠시 후 다시 시도해 주세요. (짧은 시간에 여러 번 제출됨)"
        : "접수에 실패했습니다. contact@shilderslab.com 으로 보내주시면 확인하겠습니다.");
      btn.disabled = false; btn.textContent = "지원서 제출";
    });
  });
})();
