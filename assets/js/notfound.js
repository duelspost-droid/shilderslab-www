/* 생성 근거: CSP 에서 script-src 'unsafe-inline' 제거를 위해 인라인 <script> 를 외부로 뺐다.
   원본은 tools/content_pages.py 의 NF_JS 상수. */
/* /insights/<slug>/ 로 들어왔는데 정적 페이지가 생성되지 않은 글이면(최근 발행분)
   동적 렌더러로 넘겨 준다. 그 외에는 일반 404 화면을 보여준다. */
(function () {
  var m = /^\/insights\/([a-z0-9][a-z0-9-]*)\/?$/.exec(location.pathname);
  if (m) {
    location.replace("/insights/view.html?slug=" + encodeURIComponent(m[1]));
  }
})();
