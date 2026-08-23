/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_dynamic.py 의 CON_JS 상수. */
(function () {
  var form = document.getElementById("inq-form");
  var alertEl = document.getElementById("inq-alert");
  var btn = document.getElementById("inq-submit");

  /* 알림은 폼 맨 위에 있고 제출 버튼은 맨 아래다 — 스크롤해 주지 않으면 성공/실패 메시지를
     사용자가 보지 못한 채 "아무 일도 안 일어났다"고 느낀다(채용 폼과 같은 동작으로 통일). */
  function show(kind, msg) {
    alertEl.className = "alert on " + kind; alertEl.textContent = msg;
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
    return [[g("inq-company"), !g("inq-company").value.trim()],
            [g("inq-name"), !g("inq-name").value.trim()],
            [g("inq-email"), !/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(g("inq-email").value.trim())],
            [g("inq-service"), !g("inq-service").value],
            [g("inq-message"), g("inq-message").value.trim().length < 5]];
  }
  /* 오류를 고치면 그 자리에서 빨간 표시가 사라진다. 재제출해야만 풀리면
     "고쳤는데도 계속 틀렸다고 한다"고 읽힌다. */
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
    var hp = document.getElementById("inq-website");
    if (hp && hp.value) {
      form.reset();
      show("ok", "문의가 접수되었습니다. 영업일 기준 24시간 내에 담당자가 회신드립니다.");
      return;
    }
    var company = document.getElementById("inq-company");
    var name = document.getElementById("inq-name");
    var email = document.getElementById("inq-email");
    var phone = document.getElementById("inq-phone");
    var service = document.getElementById("inq-service");
    var message = document.getElementById("inq-message");
    var consent = document.getElementById("inq-consent");

    var bad = false, firstBad = null;
    checks().forEach(function (p) {
      markErr(p[0], p[1]); if (p[1]) { bad = true; if (!firstBad) firstBad = p[0]; }
    });
    if (bad) { show("bad", "입력값을 확인해 주세요."); if (firstBad) firstBad.focus(); return; }
    if (!consent.checked) { show("bad", "개인정보 수집·이용 동의가 필요합니다."); return; }

    var c = SL.db();
    if (!c) { show("bad", "지금은 접수를 처리할 수 없습니다. contact@shilderslab.com 으로 보내주세요."); return; }

    btn.disabled = true; btn.textContent = "전송 중…";
    c.rpc("sl_submit_inquiry", {
      p_company: company.value.trim(), p_name: name.value.trim(), p_email: email.value.trim(),
      p_phone: phone.value.trim(), p_service: service.value, p_message: message.value.trim(), p_consent: true
    }).then(function (r) {
      if (r.error) throw r.error;
      form.reset();
      show("ok", "문의가 접수되었습니다. 영업일 기준 24시간 내에 담당자가 회신드립니다.");
      btn.textContent = "접수 완료";
      /* 영구 비활성으로 두면 추가 문의를 못 한다. 잠깐 완료를 보여 준 뒤 되살린다. */
      setTimeout(function () { btn.disabled = false; btn.textContent = "문의 보내기"; }, 4000);
    }).catch(function (err) {
      var m = (err && err.message) || "";
      show("bad", /too many|rate/i.test(m)
        ? "짧은 시간에 여러 번 접수되었습니다. 잠시 후 다시 시도해 주세요."
        : "전송에 실패했습니다. contact@shilderslab.com 으로 보내주시면 확인하겠습니다.");
      btn.disabled = false; btn.textContent = "문의 보내기";
    });
  });
})();
