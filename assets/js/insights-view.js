/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_dynamic.py 의 VIEW_JS 상수. */
(function () {
  var titleEl = document.getElementById("p-title");
  var headEl = document.getElementById("post-head");
  var bodyEl = document.getElementById("p-body");

  /* 이스케이프 후 최소 마크다운만 변환 — 원문 HTML은 절대 삽입하지 않는다. */
  function renderBody(src) {
    var safe = SL.esc(src || "");
    var lines = safe.split(/\r?\n/), out = [], list = null;
    function closeList() {
      if (list) { out.push("<" + list.t + ">" + list.items.join("") + "</" + list.t + ">"); list = null; }
    }
    lines.forEach(function (raw) {
      var line = raw.trim();
      if (!line) { closeList(); return; }
      var h = /^(#{2,3})\s+(.*)$/.exec(line);
      if (h) { closeList(); out.push("<h" + h[1].length + ">" + h[2] + "</h" + h[1].length + ">"); return; }
      var ul = /^[-*]\s+(.*)$/.exec(line);
      if (ul) {
        if (!list || list.t !== "ul") { closeList(); list = { t: "ul", items: [] }; }
        list.items.push("<li>" + ul[1] + "</li>"); return;
      }
      var ol = /^\d+\.\s+(.*)$/.exec(line);
      if (ol) {
        if (!list || list.t !== "ol") { closeList(); list = { t: "ol", items: [] }; }
        list.items.push("<li>" + ol[1] + "</li>"); return;
      }
      if (/^&gt;\s?/.test(line)) {
        closeList(); out.push("<blockquote>" + line.replace(/^&gt;\s?/, "") + "</blockquote>"); return;
      }
      closeList(); out.push("<p>" + line + "</p>");
    });
    closeList();
    var html = out.join("\n")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
    html = html.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, txt, url) {
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
    /* canonical 은 이 동적 뷰(?slug=)가 아니라 **정적 정본 경로**를 가리킨다.
       빌드가 /insights/<slug>/ 를 정적 생성하므로, 쿼리스트링판은 그쪽으로 흡수돼
       중복 콘텐츠로 색인되지 않는다. */
    var canon = "https://shilderslab.com/insights/" + encodeURIComponent(slug) + "/";
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
      '<div class="lbl ko" style="margin-bottom:18px">' + SL.esc(p.category || "인사이트") +
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
