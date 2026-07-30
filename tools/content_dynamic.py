# -*- coding: utf-8 -*-
"""백엔드 연동 페이지 v2 — 인사이트 목록/상세 · 채용 · 문의
   사용자 입력은 SECURITY DEFINER RPC로만 적재하고, 출력은 SL.esc() 로 이스케이프한다.
"""

# ══════════════════════════════════════════════════════════════════════
# 인사이트 목록
# ══════════════════════════════════════════════════════════════════════
INS_TITLE = "인사이트 | 쉴더스랩 — 규제 변화와 진단 현장 기록"
INS_DESC = ("규제 변화와 진단 현장에서 반복적으로 확인되는 문제, 그리고 실제로 효과가 있었던 조치를 "
            "정리한 쉴더스랩의 보안 인사이트.")
INS_LD = ('{"@context":"https://schema.org","@type":"Blog","name":"쉴더스랩 인사이트",'
          '"url":"https://shilderslab.com/insights/"}')

INS_CSS = """
  .filters{display:flex;gap:0;flex-wrap:wrap;border-top:1px solid var(--rule);margin-bottom:0}
  .filters button{background:none;border:0;cursor:pointer;padding:14px 20px 14px 0;margin-right:20px;
    font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;
    color:var(--ink-3);border-bottom:1px solid transparent;position:relative;top:1px}
  .filters button:hover{color:var(--ink)}
  .filters button.active{color:var(--accent);border-bottom-color:var(--accent)}
"""

INS_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 인사이트</div>
    <h1 class="d1">현장에서<br>반복되는 것들</h1>
    <p class="lead">진단을 나가면 조직은 달라도 같은 문제가 반복됩니다.
       규제 해석이 갈리는 지점, 조치가 자주 미끄러지는 지점, 그리고 실제로 통했던 방법을 기록합니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="filters" id="filters"></div>
    <div class="posts" id="post-list">
      <div class="empty">인사이트를 불러오는 중…</div>
    </div>
  </div>
</section>"""

INS_JS = """<script>
(function () {
  var listEl = document.getElementById("post-list");
  var filterEl = document.getElementById("filters");
  var all = [], cur = "전체";

  function render() {
    var rows = cur === "전체" ? all : all.filter(function (p) { return (p.category || "") === cur; });
    if (!rows.length) {
      listEl.innerHTML = '<div class="empty">해당 분류의 글이 아직 없습니다.</div>';
      return;
    }
    listEl.innerHTML = rows.map(function (p) {
      return '<a class="post" href="/insights/' + encodeURIComponent(p.slug) + '/">' +
        '<div class="meta">' + SL.esc(SL.fmtDate(p.published_at)) + '<br>' +
        SL.esc(p.category || "인사이트") + '</div>' +
        '<div><h3>' + SL.esc(p.title) + '</h3><p>' + SL.esc(p.summary || "") + '</p></div>' +
        '<div class="go">읽기 →</div></a>';
    }).join("");
  }

  function renderFilters() {
    var cats = ["전체"];
    all.forEach(function (p) {
      var c = p.category || "인사이트";
      if (cats.indexOf(c) < 0) cats.push(c);
    });
    if (cats.length <= 2) { filterEl.style.display = "none"; return; }
    filterEl.innerHTML = cats.map(function (c) {
      return '<button type="button" data-cat="' + SL.escA(c) + '"' +
        (c === cur ? ' class="active"' : "") + ">" + SL.esc(c) + "</button>";
    }).join("");
    Array.prototype.forEach.call(filterEl.querySelectorAll("button"), function (b) {
      b.addEventListener("click", function () {
        cur = b.getAttribute("data-cat");
        Array.prototype.forEach.call(filterEl.querySelectorAll("button"), function (x) {
          x.classList.toggle("active", x === b);
        });
        render();
      });
    });
  }

  if (!window.SL || !SL.db()) {
    listEl.innerHTML = '<div class="empty">인사이트를 준비하고 있습니다.</div>';
    return;
  }
  SL.listPublished("sl_insights", {
    columns: "slug,category,title,summary,published_at",
    order: [{ col: "sort_order", asc: false }, { col: "published_at", asc: false }], limit: 60
  }).then(function (r) {
    all = (r && r.data) || [];
    if (!all.length) {
      listEl.innerHTML = '<div class="empty">첫 글을 준비하고 있습니다. 곧 공개됩니다.</div>';
      return;
    }
    renderFilters(); render();
  }).catch(function () {
    listEl.innerHTML = '<div class="empty">목록을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.</div>';
  });
})();
</script>"""

# ══════════════════════════════════════════════════════════════════════
# 인사이트 상세
# ══════════════════════════════════════════════════════════════════════
VIEW_TITLE = "인사이트 | 쉴더스랩"
VIEW_DESC = ("규제 변화와 진단 현장에서 반복되는 문제, 실제로 통했던 조치 방법을 정리한 "
             "쉴더스랩의 보안 인사이트.")

VIEW_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · <a href="/insights/">인사이트</a></div>
    <div id="post-head"><h1 class="d2" id="p-title">불러오는 중…</h1></div>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <article class="article">
      <div class="body" id="p-body"></div>
      <div style="margin-top:56px;padding-top:24px;border-top:1px solid var(--ink);display:flex;
                  gap:16px;flex-wrap:wrap;justify-content:space-between;align-items:center">
        <a class="alink" href="/insights/">인사이트 목록</a>
        <a class="btn btn-sm" href="/contact/">이 주제로 상담 요청</a>
      </div>
    </article>
  </div>
</section>"""

VIEW_JS = """<script>
(function () {
  var titleEl = document.getElementById("p-title");
  var headEl = document.getElementById("post-head");
  var bodyEl = document.getElementById("p-body");

  /* 이스케이프 후 최소 마크다운만 변환 — 원문 HTML은 절대 삽입하지 않는다. */
  function renderBody(src) {
    var safe = SL.esc(src || "");
    var lines = safe.split(/\\r?\\n/), out = [], list = null;
    function closeList() {
      if (list) { out.push("<" + list.t + ">" + list.items.join("") + "</" + list.t + ">"); list = null; }
    }
    lines.forEach(function (raw) {
      var line = raw.trim();
      if (!line) { closeList(); return; }
      var h = /^(#{2,3})\\s+(.*)$/.exec(line);
      if (h) { closeList(); out.push("<h" + h[1].length + ">" + h[2] + "</h" + h[1].length + ">"); return; }
      var ul = /^[-*]\\s+(.*)$/.exec(line);
      if (ul) {
        if (!list || list.t !== "ul") { closeList(); list = { t: "ul", items: [] }; }
        list.items.push("<li>" + ul[1] + "</li>"); return;
      }
      var ol = /^\\d+\\.\\s+(.*)$/.exec(line);
      if (ol) {
        if (!list || list.t !== "ol") { closeList(); list = { t: "ol", items: [] }; }
        list.items.push("<li>" + ol[1] + "</li>"); return;
      }
      if (/^&gt;\\s?/.test(line)) {
        closeList(); out.push("<blockquote>" + line.replace(/^&gt;\\s?/, "") + "</blockquote>"); return;
      }
      closeList(); out.push("<p>" + line + "</p>");
    });
    closeList();
    var html = out.join("\\n")
      .replace(/\\*\\*([^*]+)\\*\\*/g, "<b>$1</b>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
    html = html.replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)\\)/g, function (m, txt, url) {
      var safeU = SL.safeUrl(url.replace(/&amp;/g, "&"));
      if (!safeU) return txt;
      var ext = /^https?:/i.test(safeU);
      return '<a href="' + SL.escA(safeU) + '"' +
        (ext ? ' target="_blank" rel="noopener noreferrer"' : "") + ">" + txt + "</a>";
    });
    return html;
  }

  var slug = new URLSearchParams(location.search).get("slug") || "";
  if (!slug || !window.SL || !SL.db()) {
    titleEl.textContent = "글을 찾을 수 없습니다";
    bodyEl.innerHTML = '<p>주소가 올바르지 않거나 삭제된 글입니다. <a href="/insights/">인사이트 목록</a>으로 이동해 주세요.</p>';
    return;
  }
  SL.listPublished("sl_insights", {
    columns: "slug,category,title,summary,body,published_at,author",
    eq: { slug: slug }, limit: 1
  }).then(function (r) {
    var p = (r && r.data && r.data[0]) || null;
    if (!p) {
      titleEl.textContent = "글을 찾을 수 없습니다";
      bodyEl.innerHTML = '<p>삭제되었거나 아직 공개되지 않은 글입니다. <a href="/insights/">인사이트 목록</a>으로 이동해 주세요.</p>';
      return;
    }
    document.title = p.title + " | 쉴더스랩 인사이트";
    var desc = String(p.summary || "").slice(0, 150);
    var canon = "https://shilderslab.com/insights/view.html?slug=" + encodeURIComponent(slug);
    function setAttr(sel, attr, val) {
      var el = document.querySelector(sel);
      if (el && val) el.setAttribute(attr, val);
    }
    setAttr('meta[name="description"]', "content", desc);
    setAttr('link[rel="canonical"]', "href", canon);
    setAttr('meta[property="og:url"]', "content", canon);
    setAttr('meta[property="og:title"]', "content", p.title + " | 쉴더스랩 인사이트");
    setAttr('meta[property="og:description"]', "content", desc);

    headEl.innerHTML =
      '<div class="lbl" style="margin-bottom:18px">' + SL.esc(p.category || "인사이트") +
      ' &nbsp;·&nbsp; ' + SL.esc(SL.fmtDate(p.published_at)) +
      (p.author ? ' &nbsp;·&nbsp; ' + SL.esc(p.author) : "") + "</div>" +
      '<h1 class="d2">' + SL.esc(p.title) + "</h1>" +
      (p.summary ? '<p class="lead" style="margin-top:20px;max-width:58ch">' + SL.esc(p.summary) + "</p>" : "");
    bodyEl.innerHTML = renderBody(p.body);
  }).catch(function () {
    titleEl.textContent = "불러오지 못했습니다";
    bodyEl.innerHTML = "<p>잠시 후 다시 시도해 주세요.</p>";
  });
})();
</script>"""

# ══════════════════════════════════════════════════════════════════════
# 채용
# ══════════════════════════════════════════════════════════════════════
CAR_TITLE = "채용 | 쉴더스랩 — 정보보호 컨설턴트 채용"
CAR_DESC = ("쉴더스랩 채용 공고와 지원 접수. 근거로 검증하는 정보보호 컨설턴트, 모의해킹, "
            "클라우드 보안 인재를 찾습니다.")

CAR_CSS = """
  .jobs{border-top:1px solid var(--ink)}
  .jobs details{border-bottom:1px solid var(--rule)}
  .jobs summary{padding:24px 0;cursor:pointer;list-style:none;display:grid;
    grid-template-columns:1fr auto;gap:20px;align-items:baseline}
  .jobs summary::-webkit-details-marker{display:none}
  .jobs .jt b{display:block;font-size:1.1rem;font-weight:600;letter-spacing:-.02em;margin-bottom:7px}
  .jobs .jt span{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.1em;
    color:var(--ink-3);text-transform:uppercase}
  .jobs .open{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.12em;
    color:var(--ink-3);text-transform:uppercase;white-space:nowrap}
  .jobs details[open] .open{color:var(--accent)}
  .jobs .jbody{padding:0 0 28px;white-space:pre-wrap;font-size:.94rem;color:var(--ink-2);
    line-height:1.82;max-width:72ch}
"""

CAR_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 채용</div>
    <h1 class="d1">근거로 말하는<br>사람을 찾습니다</h1>
    <p class="lead">“아마 취약할 것 같다”가 아니라 “이렇게 재현된다”로 말하는 사람과 일합니다.
       경력의 길이보다 검증하는 습관을 봅니다.</p>
  </div>
</section>

<section class="sec">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">01 / Open positions</span></div>
      <div class="body"><h2 class="d3">채용 중인 포지션</h2></div>
    </div>
    <div class="jobs" id="job-list"><div class="empty">공고를 불러오는 중…</div></div>
  </div>
</section>

<section class="sec band">
  <div class="shell">
    <div class="sec-head">
      <div class="idx"><span class="lbl">02 / How we work</span></div>
      <div class="body"><h2 class="d3">이렇게 일합니다</h2></div>
    </div>
    <div class="cols cols-3 divided">
      <div class="col-item rv">
        <span class="n">01</span>
        <h3>결과보다 근거</h3>
        <p>발견을 주장하려면 재현이 필요합니다. 내부 리뷰에서도 “왜 그렇게 판단했는가”를 먼저 확인합니다.</p>
      </div>
      <div class="col-item rv d1">
        <span class="n">02</span>
        <h3>혼자 결론내지 않음</h3>
        <p>위험도 산정과 보고서 논조는 교차 검토를 거칩니다. 신입도 시니어 판단에 이견을 낼 수 있어야 합니다.</p>
      </div>
      <div class="col-item rv d2">
        <span class="n">03</span>
        <h3>배운 것은 문서로</h3>
        <p>프로젝트에서 얻은 패턴은 체크리스트와 인사이트로 남깁니다. 같은 실수를 조직이 반복하지 않게 합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="apply">
  <div class="shell g12">
    <div class="c4">
      <span class="lbl">03 / Apply</span>
      <h2 class="d3" style="margin:18px 0 16px">지원하기</h2>
      <p class="small">이력서·포트폴리오는 공개 링크로 남겨 주세요. 파일 첨부는 받지 않습니다.
         상시 지원도 환영합니다.</p>
    </div>
    <div class="c7 start6">
      <form class="form" id="apply-form" novalidate>
        <div class="alert" id="ap-alert" role="status"></div>
        <div aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden">
          <label for="ap-website">웹사이트</label>
          <input id="ap-website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div class="row2">
          <div class="field">
            <label for="ap-name">성명 <span class="req">*</span></label>
            <input id="ap-name" type="text" maxlength="40" autocomplete="name" required placeholder="홍길동">
            <div class="msg">성명을 입력해 주세요.</div>
          </div>
          <div class="field">
            <label for="ap-email">이메일 <span class="req">*</span></label>
            <input id="ap-email" type="email" maxlength="120" autocomplete="email" required placeholder="name@example.com">
            <div class="msg">올바른 이메일을 입력해 주세요.</div>
          </div>
        </div>
        <div class="row2">
          <div class="field">
            <label for="ap-phone">연락처 (선택)</label>
            <input id="ap-phone" type="tel" maxlength="30" autocomplete="tel" placeholder="010-0000-0000">
          </div>
          <div class="field">
            <label for="ap-position">지원 포지션 <span class="req">*</span></label>
            <select id="ap-position" required>
              <option value="">선택해 주세요</option>
              <option>정보보호 컨설턴트 (관리체계 · ISMS-P)</option>
              <option>모의해킹 · 취약점 진단</option>
              <option>클라우드 보안</option>
              <option>개인정보 컴플라이언스</option>
              <option>상시 지원 (포지션 무관)</option>
            </select>
            <div class="msg">포지션을 선택해 주세요.</div>
          </div>
        </div>
        <div class="field">
          <label for="ap-link">이력서 · 포트폴리오 링크 (선택)</label>
          <input id="ap-link" type="url" maxlength="300" placeholder="https://">
          <div class="hint">개인 블로그, GitHub, 공개 문서 링크 등 접근 가능한 주소를 남겨 주세요.</div>
        </div>
        <div class="field">
          <label for="ap-summary">경력 · 강점 요약 <span class="req">*</span></label>
          <textarea id="ap-summary" maxlength="3000" required
            placeholder="수행한 진단·컨설팅 경험, 사용 도구, 특히 자신 있는 영역을 적어주세요."></textarea>
          <div class="msg">간단하게라도 경력 요약을 입력해 주세요.</div>
        </div>
        <label class="consent">
          <input type="checkbox" id="ap-consent" required>
          <span>채용 전형 진행을 위한 개인정보 수집·이용에 동의합니다. 수집 항목(성명·이메일·연락처·지원 내용,
            그리고 스팸·중복 접수 방지를 위해 자동 수집되는 접속 IP·브라우저 정보)은
            전형 종료 후 6개월(상시 지원은 접수일로부터 6개월)간 보관 후 파기되며, 동의 철회 시 즉시 파기됩니다.
            자세한 내용은 <a href="/legal/privacy.html" target="_blank" rel="noopener">개인정보처리방침</a>을 확인해 주세요.</span>
        </label>
        <div style="margin-top:26px;display:flex;gap:18px;align-items:center;flex-wrap:wrap">
          <button class="btn" type="submit" id="ap-submit">지원서 제출</button>
          <span class="tiny">확인까지 수일이 소요될 수 있습니다.</span>
        </div>
      </form>
    </div>
  </div>
</section>"""

CAR_JS = """<script>
(function () {
  var listEl = document.getElementById("job-list");
  if (!window.SL || !SL.db()) {
    listEl.innerHTML = '<div class="empty">현재 공개된 공고가 없습니다. 상시 지원은 아래 양식을 이용해 주세요.</div>';
  } else {
    SL.listPublished("sl_jobs", {
      columns: "title,team,employment_type,location,summary,body,closes_at",
      order: { col: "sort_order", asc: true }, limit: 30
    }).then(function (r) {
      var rows = (r && r.data) || [];
      if (!rows.length) {
        listEl.innerHTML = '<div class="empty">현재 공개된 공고가 없습니다. 상시 지원은 아래 양식을 이용해 주세요.</div>';
        return;
      }
      listEl.innerHTML = rows.map(function (j) {
        var metas = [j.team, j.employment_type, j.location].filter(Boolean).map(SL.esc).join(" · ");
        return '<details><summary><span class="jt"><b>' + SL.esc(j.title) + "</b><span>" + metas +
          (j.closes_at ? " · 마감 " + SL.esc(SL.fmtDate(j.closes_at)) : " · 채용 시 마감") +
          '</span></span><span class="open">상세 +</span></summary>' +
          '<div class="jbody">' + SL.esc(j.body || j.summary || "") +
          '<div style="margin-top:22px"><a class="btn btn-sm" href="#apply">이 포지션 지원하기</a></div></div></details>';
      }).join("");
    }).catch(function () {
      listEl.innerHTML = '<div class="empty">공고를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.</div>';
    });
  }

  var form = document.getElementById("apply-form");
  var alertEl = document.getElementById("ap-alert");
  var btn = document.getElementById("ap-submit");

  function show(kind, msg) {
    alertEl.className = "alert on " + kind;
    alertEl.textContent = msg;
    alertEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  function markErr(el, bad) { var f = el.closest(".field"); if (f) f.classList.toggle("err", !!bad); }

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

    var bad = false;
    [[name, !name.value.trim()],
     [email, !/^[^@\\s]+@[^@\\s.]+\\.[^@\\s]+$/.test(email.value.trim())],
     [pos, !pos.value],
     [summary, summary.value.trim().length < 10]].forEach(function (p) {
      markErr(p[0], p[1]); if (p[1]) bad = true;
    });
    if (bad) { show("bad", "입력값을 확인해 주세요."); return; }
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
    }).catch(function (err) {
      var m = (err && err.message) || "";
      show("bad", /too many|rate/i.test(m)
        ? "잠시 후 다시 시도해 주세요. (짧은 시간에 여러 번 제출됨)"
        : "접수에 실패했습니다. contact@shilderslab.com 으로 보내주시면 확인하겠습니다.");
      btn.disabled = false; btn.textContent = "지원서 제출";
    });
  });
})();
</script>"""

# ══════════════════════════════════════════════════════════════════════
# 문의
# ══════════════════════════════════════════════════════════════════════
CON_TITLE = "상담 · 견적 요청 | 쉴더스랩"
CON_DESC = ("정보보호 컨설팅 상담·견적 요청. 범위 검토와 견적 산정까지는 비용이 발생하지 않으며, "
            "영업일 기준 24시간 내 초기 회신합니다.")
CON_LD = ('{"@context":"https://schema.org","@type":"ContactPage","name":"상담 · 견적 요청 | 쉴더스랩",'
          '"url":"https://shilderslab.com/contact/"}')

CON_CSS = """
  .steps{list-style:none;counter-reset:s;border-top:1px solid var(--rule)}
  .steps li{counter-increment:s;display:grid;grid-template-columns:34px 1fr;gap:14px;padding:15px 0;
    border-bottom:1px solid var(--rule);font-size:.92rem;color:var(--ink-2);line-height:1.7}
  .steps li::before{content:"0" counter(s);font-family:'IBM Plex Mono',monospace;font-size:.68rem;
    letter-spacing:.1em;color:var(--accent);padding-top:5px}
  .steps li b{display:block;color:var(--ink);font-weight:600;margin-bottom:2px}
"""

CON_BODY = """<section class="phead">
  <div class="shell">
    <div class="crumb"><a href="/">홈</a> · 상담 요청</div>
    <h1 class="d1">범위부터<br>같이 정리합니다</h1>
    <p class="lead">무엇이 필요한지 확정되지 않아도 괜찮습니다. 현재 상황만 알려주시면 필요한 진단과
       우선순위, 예상 일정을 정리해 회신드립니다. <b>범위 검토와 견적 산정에는 비용이 발생하지 않습니다.</b></p>
  </div>
</section>

<section class="sec">
  <div class="shell g12">
    <div class="c7">
      <form class="form" id="inq-form" novalidate>
        <div class="alert" id="inq-alert" role="status"></div>
        <div aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden">
          <label for="inq-website">웹사이트</label>
          <input id="inq-website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <div class="row2">
          <div class="field">
            <label for="inq-company">회사명 <span class="req">*</span></label>
            <input id="inq-company" type="text" maxlength="80" autocomplete="organization" required placeholder="(주)예시">
            <div class="msg">회사명을 입력해 주세요.</div>
          </div>
          <div class="field">
            <label for="inq-name">담당자명 <span class="req">*</span></label>
            <input id="inq-name" type="text" maxlength="40" autocomplete="name" required placeholder="홍길동">
            <div class="msg">담당자명을 입력해 주세요.</div>
          </div>
        </div>
        <div class="row2">
          <div class="field">
            <label for="inq-email">이메일 <span class="req">*</span></label>
            <input id="inq-email" type="email" maxlength="120" autocomplete="email" required placeholder="name@company.com">
            <div class="msg">올바른 이메일을 입력해 주세요.</div>
          </div>
          <div class="field">
            <label for="inq-phone">연락처 (선택)</label>
            <input id="inq-phone" type="tel" maxlength="30" autocomplete="tel" placeholder="02-0000-0000">
          </div>
        </div>
        <div class="field">
          <label for="inq-service">문의 유형 <span class="req">*</span></label>
          <select id="inq-service" required>
            <option value="">선택해 주세요</option>
            <option>ISMS-P 인증 컨설팅</option>
            <option>모의해킹 · 침투테스트</option>
            <option>취약점 진단</option>
            <option>개인정보 컴플라이언스</option>
            <option>클라우드 보안</option>
            <option>보안 거버넌스 · 교육</option>
            <option>기타 · 어떤 진단이 필요한지 모르겠음</option>
          </select>
          <div class="msg">문의 유형을 선택해 주세요.</div>
        </div>
        <div class="field">
          <label for="inq-message">문의 내용 <span class="req">*</span></label>
          <textarea id="inq-message" maxlength="4000" required
            placeholder="예) 회원 30만 규모 웹서비스입니다. 내년 상반기 ISMS-P 최초 인증을 목표로 검토 중이고, 정책 문서는 아직 없습니다. 서버는 AWS 20대 규모입니다."></textarea>
          <div class="hint">시스템 규모, 목표 일정, 규제 요건을 함께 적어주시면 회신이 정확해집니다.
            <b>계정 정보·접속 경로 등 민감한 정보는 이 양식에 입력하지 마세요.</b></div>
          <div class="msg">문의 내용을 입력해 주세요.</div>
        </div>
        <label class="consent">
          <input type="checkbox" id="inq-consent" required>
          <span>상담 회신을 위한 개인정보 수집·이용에 동의합니다. 수집 항목(회사명·담당자명·이메일·연락처·문의 유형·문의 내용,
            그리고 스팸·중복 접수 방지를 위해 자동 수집되는 접속 IP·브라우저 정보)은
            문의 처리 완료 후 1년간 보관 후 파기됩니다.
            자세한 내용은 <a href="/legal/privacy.html" target="_blank" rel="noopener">개인정보처리방침</a>을 확인해 주세요.</span>
        </label>
        <div style="margin-top:26px;display:flex;gap:18px;align-items:center;flex-wrap:wrap">
          <button class="btn" type="submit" id="inq-submit">문의 보내기</button>
          <span class="tiny" data-setting="sla_note">영업일 기준 24시간 내 초기 회신</span>
        </div>
      </form>
    </div>

    <aside class="c4 start9">
      <div class="kv">
        <div class="row"><div class="k">이메일</div>
          <div class="v"><a href="mailto:contact@shilderslab.com" style="border-bottom:1px solid var(--rule-2)">contact@shilderslab.com</a></div></div>
        <div class="row"><div class="k">운영시간</div>
          <div class="v"><span data-setting="business_hours">평일 09:00 – 18:00</span><br>
            <span class="tiny">주말·공휴일 휴무</span></div></div>
        <div class="row"><div class="k">보안 신고</div>
          <div class="v">본 사이트의 취약점을 발견하셨다면 이메일로 알려주세요. 비공개로 검토하며,
            선의의 신고자에게 법적 조치를 취하지 않습니다.</div></div>
      </div>

      <h3 class="d3" style="font-size:1.02rem;margin:44px 0 16px">진행 절차</h3>
      <ol class="steps">
        <li><b>문의 접수</b>영업일 기준 24시간 내 초기 회신</li>
        <li><b>사전 미팅</b>범위·목표 일정·제약 사항 확인 (온라인 가능)</li>
        <li><b>제안 · 견적</b>진단 항목, 일정, 산출물, 비용을 문서로 제시</li>
        <li><b>계약 · NDA</b>체결 후 착수</li>
      </ol>

      <h3 class="d3" style="font-size:1.02rem;margin:44px 0 16px">미리 알려주시면 좋은 것</h3>
      <ul class="bullets">
        <li>대상 시스템 수와 형태(웹·앱·내부망·클라우드)</li>
        <li>인증 심사일이나 감사 일정 등 고정된 날짜</li>
        <li>내부 담당 조직과 의사결정 경로</li>
      </ul>
      <p class="tiny" style="margin-top:18px">계정·키·상세 구성도는 계약 및 NDA 체결 후 안전한 경로로 전달받습니다.</p>
    </aside>
  </div>
</section>"""

CON_JS = """<script>
(function () {
  var form = document.getElementById("inq-form");
  var alertEl = document.getElementById("inq-alert");
  var btn = document.getElementById("inq-submit");

  function show(kind, msg) { alertEl.className = "alert on " + kind; alertEl.textContent = msg; }
  function markErr(el, bad) { var f = el.closest(".field"); if (f) f.classList.toggle("err", !!bad); }

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

    var bad = false;
    [[company, !company.value.trim()], [name, !name.value.trim()],
     [email, !/^[^@\\s]+@[^@\\s.]+\\.[^@\\s]+$/.test(email.value.trim())],
     [service, !service.value],
     [message, message.value.trim().length < 5]].forEach(function (p) {
      markErr(p[0], p[1]); if (p[1]) bad = true;
    });
    if (bad) { show("bad", "입력값을 확인해 주세요."); return; }
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
    }).catch(function (err) {
      var m = (err && err.message) || "";
      show("bad", /too many|rate/i.test(m)
        ? "짧은 시간에 여러 번 접수되었습니다. 잠시 후 다시 시도해 주세요."
        : "전송에 실패했습니다. contact@shilderslab.com 으로 보내주시면 확인하겠습니다.");
      btn.disabled = false; btn.textContent = "문의 보내기";
    });
  });
})();
</script>"""
