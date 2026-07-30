/* ──────────────────────────────────────────────────────────────
   쉴더스랩 — Supabase 클라이언트 + 공용 유틸 (전 페이지 공용)
   window.SL 네임스페이스로 노출. supabase.min.js(벤더)와 config.js 뒤에 로드.
   ────────────────────────────────────────────────────────────── */
(function () {
  "use strict";
  var CFG = window.SL_CONFIG || {};
  var _client = null;

  /** 지연 생성 싱글턴 클라이언트. 설정이 없으면 null. */
  function db() {
    if (_client) return _client;
    if (!window.supabase || !CFG.SUPABASE_URL || !CFG.SUPABASE_ANON_KEY) return null;
    _client = window.supabase.createClient(CFG.SUPABASE_URL, CFG.SUPABASE_ANON_KEY, {
      auth: { persistSession: true, autoRefreshToken: true, storageKey: "sl-auth" },
    });
    return _client;
  }

  /** HTML 이스케이프 — CMS/사용자 입력을 innerHTML에 넣기 전 반드시 통과시킨다. */
  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  /** 속성값용 이스케이프(따옴표 포함). */
  function escA(v) { return esc(v).replace(/`/g, "&#96;"); }

  /** 외부 링크 안전 검사 — http/https 만 통과, 그 외는 빈 문자열. */
  function safeUrl(u) {
    var s = String(u || "").trim();
    if (!s) return "";
    if (/^https?:\/\//i.test(s)) return s;
    // 사이트 내부 절대경로만 허용 — //host, /\host 같은 프로토콜 상대경로는 차단
    if (/^\//.test(s) && !/^\/[\/\\]/.test(s)) return s;
    return "";
  }

  function fmtDate(v) {
    if (!v) return "";
    var d = new Date(v);
    if (isNaN(d.getTime())) return String(v).slice(0, 10);
    return d.getFullYear() + "." + String(d.getMonth() + 1).padStart(2, "0") + "." +
           String(d.getDate()).padStart(2, "0");
  }

  function fmtDateTime(v) {
    if (!v) return "";
    var d = new Date(v);
    if (isNaN(d.getTime())) return String(v);
    return fmtDate(v) + " " + String(d.getHours()).padStart(2, "0") + ":" +
           String(d.getMinutes()).padStart(2, "0");
  }

  /** 공개 방문 로깅(실패는 무시 — 사이트 동작에 영향 없어야 한다). */
  function logVisit() {
    var c = db();
    if (!c) return;
    var p = location.pathname || "/";
    try { c.rpc("sl_log_visit", { p_page: p }); } catch (e) { /* noop */ }
  }

  /** 게시된 목록 조회. table=화이트리스트만 허용. */
  function listPublished(table, opts) {
    var c = db();
    if (!c) return Promise.resolve({ data: [], error: new Error("backend 미설정") });
    opts = opts || {};
    var allowed = { sl_insights: 1, sl_jobs: 1, sl_settings: 1, sl_content: 1 };
    if (!allowed[table]) return Promise.resolve({ data: [], error: new Error("not allowed") });
    var q = c.from(table).select(opts.columns || "*");
    /* published 컬럼이 있는 테이블만 게시 필터를 건다. kv 성격의 테이블은 전량 조회한다. */
    if (table !== "sl_settings" && table !== "sl_content") q = q.eq("published", true);
    if (opts.order) {
      var orders = Array.isArray(opts.order) ? opts.order : [opts.order];
      orders.forEach(function (o) {
        q = q.order(o.col, { ascending: !!o.asc, nullsFirst: false });
      });
    }
    if (opts.limit) q = q.limit(opts.limit);
    if (opts.eq) Object.keys(opts.eq).forEach(function (k) { q = q.eq(k, opts.eq[k]); });
    return q;
  }

  /** 설정(kv) 일괄 로드 → {key: value} */
  function loadSettings() {
    return listPublished("sl_settings", { columns: "key,value" }).then(function (r) {
      var out = {};
      (r.data || []).forEach(function (row) { out[row.key] = row.value; });
      return out;
    }).catch(function () { return {}; });
  }

  /** 페이지 문구 블록 일괄 로드 → {key: {value, kind}}
      0005 미적용이면 조용히 빈 객체를 준다 — 그 경우 빌드가 구워 넣은 문구가 그대로 남는다. */
  function loadContent() {
    return listPublished("sl_content", { columns: "key,value,kind", limit: 500 }).then(function (r) {
      var out = {};
      (r.data || []).forEach(function (row) { out[row.key] = row; });
      return out;
    }).catch(function () { return {}; });
  }

  /** 최소 마크다운 → HTML.
      tools/build-pages.py 의 md() 와 **같은 결과**를 내야 한다. 한쪽만 고치지 말 것.
      이스케이프를 먼저 하므로 저장된 원문의 HTML 은 절대 실행되지 않는다. */
  function md(src) {
    var safe = esc(src == null ? "" : src);
    var out = [], list = null;
    function close() {
      if (list) { out.push("<" + list.t + ">" + list.items.join("") + "</" + list.t + ">"); list = null; }
    }
    safe.split(/\r?\n/).forEach(function (raw) {
      var line = raw.trim();
      if (!line) { close(); return; }
      var h = /^(#{2,3})\s+(.*)$/.exec(line);
      if (h) { close(); out.push("<h" + h[1].length + ">" + h[2] + "</h" + h[1].length + ">"); return; }
      var ul = /^[-*]\s+(.*)$/.exec(line);
      if (ul) {
        if (!list || list.t !== "ul") { close(); list = { t: "ul", items: [] }; }
        list.items.push("<li>" + ul[1] + "</li>"); return;
      }
      var ol = /^\d+\.\s+(.*)$/.exec(line);
      if (ol) {
        if (!list || list.t !== "ol") { close(); list = { t: "ol", items: [] }; }
        list.items.push("<li>" + ol[1] + "</li>"); return;
      }
      if (/^&gt;\s?/.test(line)) {
        close(); out.push("<blockquote>" + line.replace(/^&gt;\s?/, "") + "</blockquote>"); return;
      }
      close(); out.push("<p>" + line + "</p>");
    });
    close();
    var html = out.join("\n")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
    return html.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, txt, url) {
      var u = url.replace(/&amp;/g, "&");
      if (/^https?:\/\//i.test(u)) {
        return '<a href="' + escA(u) + '" target="_blank" rel="noopener noreferrer">' + txt + "</a>";
      }
      if (u.charAt(0) === "/" && u.charAt(1) !== "/") return '<a href="' + escA(u) + '">' + txt + "</a>";
      return txt;
    });
  }

  window.SL = {
    cfg: CFG, db: db, esc: esc, escA: escA, safeUrl: safeUrl,
    fmtDate: fmtDate, fmtDateTime: fmtDateTime, md: md,
    logVisit: logVisit, listPublished: listPublished,
    loadSettings: loadSettings, loadContent: loadContent,
  };
})();
