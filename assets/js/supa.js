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
    if (/^\//.test(s) && !/^\/\//.test(s)) return s; // 사이트 내부 절대경로
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
    var allowed = { sl_insights: 1, sl_jobs: 1, sl_settings: 1 };
    if (!allowed[table]) return Promise.resolve({ data: [], error: new Error("not allowed") });
    var q = c.from(table).select(opts.columns || "*");
    if (table !== "sl_settings") q = q.eq("published", true);
    if (opts.order) q = q.order(opts.order.col, { ascending: !!opts.order.asc, nullsFirst: false });
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

  window.SL = {
    cfg: CFG, db: db, esc: esc, escA: escA, safeUrl: safeUrl,
    fmtDate: fmtDate, fmtDateTime: fmtDateTime,
    logVisit: logVisit, listPublished: listPublished, loadSettings: loadSettings,
  };
})();
