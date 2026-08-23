/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_home.py 의 JS 상수. */
(function () {
  var box = document.getElementById("home-insights");
  if (!box || !window.SL) return;
  function fallback() {
    box.innerHTML = '<div class="empty">첫 글을 준비하고 있습니다. 곧 공개됩니다.</div>';
  }
  SL.listPublished("sl_insights", {
    columns: "slug,category,title,summary,published_at",
    order: [{ col: "sort_order", asc: false }, { col: "published_at", asc: false }], limit: 3
  }).then(function (r) {
    var rows = (r && r.data) || [];
    if (!rows.length) return fallback();
    box.innerHTML = rows.map(function (p) {
      return '<a class="post" href="/insights/' + encodeURIComponent(p.slug) + '/">' +
        '<div class="meta">' + SL.esc(SL.fmtDate(p.published_at)) + '<br>' +
        SL.esc(p.category || "인사이트") + '</div>' +
        '<div><h3>' + SL.esc(p.title) + '</h3><p>' + SL.esc(p.summary || "") + '</p></div>' +
        '<div class="go">읽기 →</div></a>';
    }).join("");
  }).catch(fallback);
})();

/* 홈 06 채용 — 콘솔에서 공고를 바꾸면 재빌드를 기다리지 않고 바로 반영한다.
   빌드가 구운 정적 목록이 이미 있으므로(크롤러용) 조회 실패 시에는 **건드리지 않는다**.
   ⚠ 행 구조는 build-pages.py 의 render_home_careers() 와 같아야 한다 — 다르면 화면이 튄다. */
(function () {
  var sec = document.getElementById("home-careers");
  var box = document.getElementById("home-jobs");
  if (!sec || !box || !window.SL || !SL.db()) return;

  SL.listPublished("sl_jobs", {
    columns: "title,team,employment_type,location,closes_at",
    order: { col: "sort_order", asc: true }, limit: 4
  }).then(function (r) {
    if (r && r.error) return;                 /* 네트워크 문제일 수 있다 — 구운 목록을 남긴다 */
    var rows = (r && r.data) || [];
    if (!rows.length) { sec.hidden = true; box.innerHTML = ""; return; }
    box.innerHTML = rows.map(function (j) {
      var metas = [j.team, j.employment_type, j.location].filter(Boolean).map(SL.esc).join(" · ");
      var closes = j.closes_at ? SL.esc(SL.fmtDate(j.closes_at)) + " 마감" : "채용 시 마감";
      return '<a href="/careers/"><div><h3>' + SL.esc(j.title) + "</h3>" +
        '<div class="m">' + metas + (metas ? " · " : "") + closes + "</div></div>" +
        '<div class="go">자세히 →</div></a>';
    }).join("");
    sec.hidden = false;
  }).catch(function () { /* 구운 목록을 그대로 둔다 */ });
})();
