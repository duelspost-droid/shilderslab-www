/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_dynamic.py 의 INS_JS 상수. */
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
