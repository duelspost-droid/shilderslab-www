/* ──────────────────────────────────────────────────────────────────────────
   쉴더스랩 관리자 콘솔
     · 로그인 → sl_admins 화이트리스트 검증(is_sl_admin RPC) → 콘솔 진입
     · 모든 쓰기 작업은 sl_log RPC로 감사 로그에 남긴다
     · 출력은 전부 SL.esc / SL.escA 로 이스케이프 (CMS·사용자 입력 XSS 차단)
   ────────────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";
  /* 프레임 버스터 — meta CSP 로는 frame-ancestors 가 적용되지 않으므로 클릭재킹을 JS로 차단한다. */
  if (self !== top) {
    document.documentElement.style.display = "none";
    try { top.location = self.location; } catch (e) { location.replace("/"); }
    return;
  }
  var esc = SL.esc, escA = SL.escA, db = SL.db();
  var loginView = document.getElementById("login-view");
  var appView = document.getElementById("app-view");
  var modal = document.getElementById("modal");
  var state = { email: "", cache: {} };

  if (!db) {
    document.body.innerHTML =
      '<div class="login-box"><div class="alert on bad">백엔드 설정(config.js)이 없어 관리자 콘솔을 사용할 수 없습니다.</div></div>';
    return;
  }

  /* ═══════════════ 공통 UI 헬퍼 ═══════════════ */
  function show(id, kind, msg) {
    var el = document.getElementById(id);
    if (!el) return;
    el.className = "alert on " + kind;
    el.textContent = msg;
    if (kind === "ok") setTimeout(function () { el.className = "alert"; }, 4000);
  }
  function statusBadge(s) {
    var map = { new: ["new", "접수"], doing: ["doing", "진행"], done: ["done", "완료"], drop: ["drop", "보류"] };
    var m = map[s] || ["drop", s || "-"];
    return '<span class="badge ' + m[0] + '">' + esc(m[1]) + "</span>";
  }
  function pubBadge(p) {
    return p ? '<span class="badge on">공개</span>' : '<span class="badge off">비공개</span>';
  }
  function emptyBox(msg) { return '<div class="empty">' + esc(msg) + "</div>"; }

  function openModal(title, bodyHtml, actions) {
    document.getElementById("modal-title").textContent = title;
    document.getElementById("modal-body").innerHTML = bodyHtml;
    var wrap = document.getElementById("modal-actions");
    wrap.innerHTML = "";
    (actions || []).forEach(function (a) {
      var b = document.createElement("button");
      b.className = "btn " + (a.cls || "btn-line") + " btn-sm";
      b.textContent = a.label;
      b.addEventListener("click", a.on);
      wrap.appendChild(b);
    });
    modal.classList.add("on");
  }
  function closeModal() { modal.classList.remove("on"); }
  modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });

  /** 관리자 행위 로깅 — 실패해도 화면 흐름을 막지 않는다. */
  function audit(action, entity, id, detail) {
    return db.rpc("sl_log", {
      p_action: action, p_entity: entity || null,
      p_entity_id: id ? String(id) : null, p_detail: detail || {},
    }).catch(function () { /* noop */ });
  }

  function val(id) { var e = document.getElementById(id); return e ? e.value : ""; }
  function checked(id) { var e = document.getElementById(id); return !!(e && e.checked); }

  /* ═══════════════ 인증 ═══════════════ */
  var loginForm = document.getElementById("login-form");
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = document.getElementById("lg-submit");
    var email = val("lg-email").trim(), pw = val("lg-pw");
    if (!email || !pw) { show("login-alert", "bad", "이메일과 비밀번호를 입력해 주세요."); return; }
    btn.disabled = true; btn.textContent = "확인 중…";
    db.auth.signInWithPassword({ email: email, password: pw }).then(function (r) {
      if (r.error) throw r.error;
      return gate();
    }).catch(function (err) {
      var m = (err && err.message) || "";
      show("login-alert", "bad", /Invalid login/i.test(m)
        ? "이메일 또는 비밀번호가 올바르지 않습니다."
        : "로그인에 실패했습니다: " + m);
      btn.disabled = false; btn.textContent = "로그인";
    });
  });

  document.getElementById("logout").addEventListener("click", function () {
    audit("logout").then(function () {
      return db.auth.signOut();
    }).then(function () { location.reload(); });
  });

  /** 세션이 관리자 화이트리스트에 있는지 확인 후 콘솔 진입 */
  function gate() {
    return db.auth.getSession().then(function (r) {
      var s = r.data && r.data.session;
      if (!s) { loginView.style.display = ""; appView.style.display = "none"; return; }
      state.email = (s.user && s.user.email) || "";
      return db.rpc("is_sl_admin").then(function (res) {
        if (res.error || res.data !== true) {
          return db.auth.signOut().then(function () {
            loginView.style.display = "";
            appView.style.display = "none";
            show("login-alert", "bad", "이 계정은 관리자로 등록되어 있지 않습니다. 관리자에게 등록을 요청하세요.");
            var btn = document.getElementById("lg-submit");
            btn.disabled = false; btn.textContent = "로그인";
          });
        }
        loginView.style.display = "none";
        appView.style.display = "";
        document.getElementById("who").innerHTML = "<b>" + esc(state.email) + "</b> 로 로그인";
        audit("login");
        loadDash(); loadInq(); loadApp();
      });
    });
  }

  /* ═══════════════ 탭 ═══════════════ */
  var loaded = {};
  function goTab(name) {
    Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
      b.classList.toggle("active", b.getAttribute("data-tab") === name);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".panel"), function (p) {
      p.classList.toggle("show", p.id === "panel-" + name);
    });
    var loaders = { dash: loadDash, inq: loadInq, app: loadApp, ins: loadIns, job: loadJob, log: loadLog, set: loadSet };
    if (!loaded[name] && loaders[name]) { loaded[name] = true; loaders[name](); }
  }
  document.getElementById("tabs").addEventListener("click", function (e) {
    var b = e.target.closest("button[data-tab]");
    if (b) goTab(b.getAttribute("data-tab"));
  });
  document.addEventListener("click", function (e) {
    var g = e.target.closest("[data-goto]");
    if (g) goTab(g.getAttribute("data-goto"));
  });

  /* ═══════════════ 대시보드 ═══════════════ */
  function loadDash() {
    db.rpc("sl_stats").then(function (r) {
      if (r.error) throw r.error;
      var s = r.data || {};
      var cards = [
        ["새 문의", s.inq_new, "미확인 상태"],
        ["문의 (7일)", s.inq_7d, "총 " + (s.inq_total || 0) + "건"],
        ["새 지원서", s.app_new, "총 " + (s.app_total || 0) + "건"],
        ["오늘 방문", s.visit_today, "7일 " + (s.visit_7d || 0) + " · 30일 " + (s.visit_30d || 0)],
        ["인사이트", s.insight_pub, "전체 " + (s.insight_total || 0) + "건 중 공개"],
        ["공개 공고", s.job_pub, "채용 페이지 노출"],
      ];
      document.getElementById("stats").innerHTML = cards.map(function (c) {
        return '<div class="mini-stat"><b>' + esc(c[1] == null ? 0 : c[1]) + "</b><span>" +
          esc(c[0]) + '</span><span style="color:var(--muted);opacity:.75">' + esc(c[2]) + "</span></div>";
      }).join("");

      var badgeInq = document.getElementById("badge-inq");
      var badgeApp = document.getElementById("badge-app");
      badgeInq.innerHTML = s.inq_new ? '<span class="badge new">' + esc(s.inq_new) + "</span>" : "";
      badgeApp.innerHTML = s.app_new ? '<span class="badge new">' + esc(s.app_new) + "</span>" : "";

      var daily = s.daily || [];
      var max = daily.reduce(function (m, d) { return Math.max(m, d.n || 0); }, 1);
      document.getElementById("bars").innerHTML = daily.length
        ? daily.map(function (d) {
            return '<div class="b" style="height:' + Math.max(3, Math.round((d.n / max) * 100)) +
              '%" title="' + escA(d.day + ": " + d.n) + '"><span>' + esc(d.day) + "</span></div>";
          }).join("")
        : '<div style="color:var(--muted);font-size:.85rem">방문 기록이 아직 없습니다.</div>';

      var tp = s.top_pages || [];
      document.getElementById("toppages").innerHTML = tp.length
        ? tp.map(function (p) {
            return "<li><code>" + esc(p.page || "/") + "</code><b>" + esc(p.n) + "</b></li>";
          }).join("")
        : '<li style="color:var(--muted)">데이터 없음</li>';
    }).catch(function (err) {
      document.getElementById("stats").innerHTML =
        '<div class="alert on bad" style="grid-column:1/-1">통계를 불러오지 못했습니다. ' +
        esc((err && err.message) || "") + " — 마이그레이션(0001)이 적용되었는지 확인하세요.</div>";
    });

    db.from("sl_inquiries").select("id,created_at,company,name,service,status")
      .order("created_at", { ascending: false }).limit(5).then(function (r) {
        var box = document.getElementById("recent-inq");
        if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
        var rows = r.data || [];
        if (!rows.length) { box.innerHTML = emptyBox("접수된 문의가 없습니다."); return; }
        box.innerHTML = '<table class="tbl"><thead><tr><th>접수일</th><th>회사</th><th>담당자</th>' +
          "<th>유형</th><th>상태</th></tr></thead><tbody>" +
          rows.map(function (x) {
            return "<tr><td>" + esc(SL.fmtDateTime(x.created_at)) + '</td><td class="t-title">' +
              esc(x.company) + "</td><td>" + esc(x.name) + "</td><td>" + esc(x.service) +
              "</td><td>" + statusBadge(x.status) + "</td></tr>";
          }).join("") + "</tbody></table>";
      });
  }

  /* ═══════════════ 제출물(문의 · 지원) 공통 ═══════════════ */
  var SUBMIT_DEFS = {
    inq: {
      table: "sl_inquiries", label: "문의",
      cols: "id,created_at,company,name,email,phone,service,message,status,admin_note,ip,user_agent",
      head: ["접수일", "회사", "담당자", "유형", "상태", ""],
      row: function (x) {
        return [SL.fmtDateTime(x.created_at), x.company, x.name + " · " + x.email, x.service];
      },
      detail: function (x) {
        return [["접수일시", SL.fmtDateTime(x.created_at)], ["회사명", x.company], ["담당자", x.name],
                ["이메일", x.email], ["연락처", x.phone || "-"], ["문의 유형", x.service || "-"],
                ["문의 내용", x.message], ["접속 IP", x.ip || "-"], ["User-Agent", x.user_agent || "-"]];
      },
    },
    app: {
      table: "sl_applications", label: "지원서",
      cols: "id,created_at,name,email,phone,position,summary,link,status,admin_note,ip,user_agent",
      head: ["접수일", "성명", "연락", "포지션", "상태", ""],
      row: function (x) {
        return [SL.fmtDateTime(x.created_at), x.name, x.email + (x.phone ? " · " + x.phone : ""), x.position];
      },
      detail: function (x) {
        return [["접수일시", SL.fmtDateTime(x.created_at)], ["성명", x.name], ["이메일", x.email],
                ["연락처", x.phone || "-"], ["지원 포지션", x.position || "-"],
                ["링크", x.link || "-"], ["경력 요약", x.summary], ["접속 IP", x.ip || "-"]];
      },
    },
  };

  function loadSubmits(key) {
    var d = SUBMIT_DEFS[key];
    var box = document.getElementById(key + "-table");
    var filter = val(key + "-filter");
    box.innerHTML = emptyBox("불러오는 중…");
    var q = db.from(d.table).select(d.cols).order("created_at", { ascending: false }).limit(300);
    if (filter) q = q.eq("status", filter);
    q.then(function (r) {
      if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
      var rows = r.data || [];
      state.cache[key] = {};
      rows.forEach(function (x) { state.cache[key][x.id] = x; });
      if (!rows.length) { box.innerHTML = emptyBox("표시할 " + d.label + "가 없습니다."); return; }
      box.innerHTML = '<table class="tbl"><thead><tr>' +
        d.head.map(function (h) { return "<th>" + esc(h) + "</th>"; }).join("") +
        "</tr></thead><tbody>" + rows.map(function (x) {
          var cells = d.row(x).map(function (c, i) {
            return "<td" + (i === 1 ? ' class="t-title"' : "") + ">" + esc(c || "-") + "</td>";
          }).join("");
          return "<tr>" + cells + "<td>" + statusBadge(x.status) + "</td>" +
            '<td><div class="row-actions"><button class="lnk" data-view="' + escA(key) +
            '" data-id="' + escA(x.id) + '">상세</button></div></td></tr>';
        }).join("") + "</tbody></table>";
    });
  }

  function openSubmit(key, id) {
    var d = SUBMIT_DEFS[key];
    var x = state.cache[key] && state.cache[key][id];
    if (!x) return;
    var dl = d.detail(x).map(function (p) {
      return "<dt>" + esc(p[0]) + "</dt><dd>" + esc(p[1]) + "</dd>";
    }).join("");
    var html =
      '<dl class="detail-dl">' + dl + "</dl>" +
      '<div class="field" style="margin-top:22px"><label for="md-status">처리 상태</label>' +
      '<select id="md-status">' +
      ["new:접수", "doing:진행", "done:완료", "drop:보류 · 종료"].map(function (o) {
        var p = o.split(":");
        return '<option value="' + p[0] + '"' + (x.status === p[0] ? " selected" : "") + ">" + esc(p[1]) + "</option>";
      }).join("") + "</select></div>" +
      '<div class="field"><label for="md-note">관리자 메모</label>' +
      '<textarea id="md-note" maxlength="2000" style="min-height:100px">' + esc(x.admin_note || "") + "</textarea></div>" +
      '<div class="alert" id="md-alert"></div>';

    openModal(d.label + " 상세", html, [
      { label: "닫기", on: closeModal },
      { label: "삭제", cls: "btn-line", on: function () {
          openModal(d.label + " 삭제", "<p style='color:var(--fg-dim)'>이 " + esc(d.label) +
            "를 완전히 삭제합니다. 복구할 수 없습니다.</p><p style='color:var(--fg-dim);margin-top:10px'><b>" +
            esc((x.company || x.name) + " · " + SL.fmtDateTime(x.created_at)) + "</b></p>", [
            { label: "취소", on: function () { openSubmit(key, id); } },
            { label: "삭제 확인", cls: "", on: function () {
                db.from(d.table).delete().eq("id", id).then(function (r) {
                  if (r.error) { show("md-alert", "bad", r.error.message); return; }
                  audit("delete", d.table, id, { label: d.label });
                  closeModal(); loadSubmits(key); loadDash();
                });
              } },
          ]);
        } },
      { label: "저장", cls: "", on: function () {
          var st = val("md-status"), note = val("md-note");
          db.from(d.table).update({ status: st, admin_note: note }).eq("id", id).then(function (r) {
            if (r.error) { show("md-alert", "bad", r.error.message); return; }
            audit("update", d.table, id, { status: st });
            closeModal(); loadSubmits(key); loadDash();
          });
        } },
    ]);
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-view]");
    if (b) openSubmit(b.getAttribute("data-view"), b.getAttribute("data-id"));
  });

  function loadInq() { loadSubmits("inq"); }
  function loadApp() { loadSubmits("app"); }
  document.getElementById("inq-reload").addEventListener("click", loadInq);
  document.getElementById("app-reload").addEventListener("click", loadApp);
  document.getElementById("inq-filter").addEventListener("change", loadInq);
  document.getElementById("app-filter").addEventListener("change", loadApp);

  /* ═══════════════ 인사이트 CMS ═══════════════ */
  function loadIns() {
    var box = document.getElementById("ins-table");
    box.innerHTML = emptyBox("불러오는 중…");
    db.from("sl_insights").select("id,slug,category,title,summary,body,author,published,published_at,sort_order")
      .order("sort_order", { ascending: false })
      .order("published_at", { ascending: false }).limit(200).then(function (r) {
        if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
        var rows = r.data || [];
        state.cache.ins = {};
        rows.forEach(function (x) { state.cache.ins[x.id] = x; });
        if (!rows.length) { box.innerHTML = emptyBox("등록된 글이 없습니다. ‘새 글 작성’으로 시작하세요."); return; }
        box.innerHTML = '<table class="tbl"><thead><tr><th>발행일</th><th>제목</th><th>분류</th>' +
          "<th>상태</th><th>순서</th><th></th></tr></thead><tbody>" +
          rows.map(function (x) {
            return "<tr><td>" + esc(SL.fmtDate(x.published_at)) + '</td><td class="t-title">' + esc(x.title) +
              '<div style="color:var(--muted);font-size:.76rem;font-family:ui-monospace">/' + esc(x.slug) + "</div></td>" +
              "<td>" + esc(x.category) + "</td><td>" + pubBadge(x.published) + "</td><td>" + esc(x.sort_order) + "</td>" +
              '<td><div class="row-actions">' +
              '<button class="lnk" data-ins-edit="' + escA(x.id) + '">수정</button>' +
              '<button class="lnk" data-ins-toggle="' + escA(x.id) + '">' + (x.published ? "비공개" : "공개") + "</button>" +
              '<button class="lnk danger" data-ins-del="' + escA(x.id) + '">삭제</button>' +
              "</div></td></tr>";
          }).join("") + "</tbody></table>";
      });
  }

  function insForm(x) {
    x = x || {};
    return '<div class="row2"><div class="field"><label for="f-title">제목 *</label>' +
      '<input id="f-title" maxlength="200" value="' + escA(x.title || "") + '"></div>' +
      '<div class="field"><label for="f-slug">주소(slug) *</label>' +
      '<input id="f-slug" maxlength="80" value="' + escA(x.slug || "") + '" placeholder="isms-p-checklist">' +
      '<div class="hint">영문 소문자·숫자·하이픈만. 공개 후 변경하면 기존 링크가 깨집니다.</div></div></div>' +
      '<div class="row2"><div class="field"><label for="f-cat">분류</label>' +
      '<input id="f-cat" maxlength="40" value="' + escA(x.category || "인사이트") + '"></div>' +
      '<div class="field"><label for="f-author">작성자</label>' +
      '<input id="f-author" maxlength="40" value="' + escA(x.author || "쉴더스랩") + '"></div></div>' +
      '<div class="row2"><div class="field"><label for="f-date">발행일</label>' +
      '<input id="f-date" type="date" value="' + escA((x.published_at || new Date().toISOString().slice(0, 10))) + '"></div>' +
      '<div class="field"><label for="f-order">정렬 순서(클수록 위)</label>' +
      '<input id="f-order" type="number" value="' + escA(x.sort_order == null ? 0 : x.sort_order) + '"></div></div>' +
      '<div class="field"><label for="f-summary">요약</label>' +
      '<textarea id="f-summary" maxlength="400" style="min-height:70px">' + esc(x.summary || "") + "</textarea></div>" +
      '<div class="field"><label for="f-body">본문</label>' +
      '<textarea id="f-body" style="min-height:260px">' + esc(x.body || "") + "</textarea>" +
      '<div class="hint">## 소제목 · - 목록 · **강조** · [링크](https://…) 형식을 지원합니다. HTML은 그대로 출력되지 않습니다(안전).</div></div>' +
      '<label class="consent"><input type="checkbox" id="f-pub"' + (x.published ? " checked" : "") +
      "><span>지금 공개합니다.</span></label>" +
      '<div class="alert" id="md-alert"></div>';
  }

  function saveIns(id) {
    var payload = {
      title: val("f-title").trim(), slug: val("f-slug").trim().toLowerCase(),
      category: val("f-cat").trim() || "인사이트", author: val("f-author").trim(),
      published_at: val("f-date") || new Date().toISOString().slice(0, 10),
      sort_order: parseInt(val("f-order"), 10) || 0,
      summary: val("f-summary").trim(), body: val("f-body"), published: checked("f-pub"),
    };
    if (!payload.title) { show("md-alert", "bad", "제목을 입력해 주세요."); return; }
    if (!/^[a-z0-9]([a-z0-9-]{0,78}[a-z0-9])?$/.test(payload.slug)) {
      show("md-alert", "bad", "slug 는 영문 소문자·숫자·하이픈만 사용할 수 있습니다."); return;
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(payload.published_at)) {
      show("md-alert", "bad", "발행일을 선택해 주세요."); return;
    }
    var p = id ? db.from("sl_insights").update(payload).eq("id", id)
               : db.from("sl_insights").insert(payload);
    p.then(function (r) {
      if (r.error) {
        show("md-alert", "bad", /duplicate|unique/i.test(r.error.message)
          ? "이미 사용 중인 slug 입니다." : r.error.message);
        return;
      }
      audit(id ? "update" : "create", "sl_insights", id || payload.slug, { title: payload.title });
      closeModal(); loadIns(); loadDash();
    });
  }

  document.getElementById("ins-new").addEventListener("click", function () {
    openModal("새 인사이트", insForm(null), [
      { label: "취소", on: closeModal },
      { label: "저장", cls: "", on: function () { saveIns(null); } },
    ]);
  });

  document.addEventListener("click", function (e) {
    var ed = e.target.closest("[data-ins-edit]");
    if (ed) {
      var x = state.cache.ins[ed.getAttribute("data-ins-edit")];
      openModal("인사이트 수정", insForm(x), [
        { label: "취소", on: closeModal },
        { label: "저장", cls: "", on: function () { saveIns(x.id); } },
      ]);
      return;
    }
    var tg = e.target.closest("[data-ins-toggle]");
    if (tg) {
      var id = tg.getAttribute("data-ins-toggle"), cur = state.cache.ins[id];
      db.from("sl_insights").update({ published: !cur.published }).eq("id", id).then(function (r) {
        if (!r.error) { audit("publish_toggle", "sl_insights", id, { to: !cur.published }); loadIns(); loadDash(); }
      });
      return;
    }
    var dl = e.target.closest("[data-ins-del]");
    if (dl) {
      var did = dl.getAttribute("data-ins-del"), item = state.cache.ins[did];
      openModal("인사이트 삭제", "<p style='color:var(--fg-dim)'>‘" + esc(item.title) +
        "’ 글을 삭제합니다. 복구할 수 없습니다.</p>", [
        { label: "취소", on: closeModal },
        { label: "삭제 확인", cls: "", on: function () {
            db.from("sl_insights").delete().eq("id", did).then(function (r) {
              if (!r.error) { audit("delete", "sl_insights", did, { title: item.title }); closeModal(); loadIns(); loadDash(); }
            });
          } },
      ]);
    }
  });

  /* ═══════════════ 채용 공고 CMS ═══════════════ */
  function loadJob() {
    var box = document.getElementById("job-table");
    box.innerHTML = emptyBox("불러오는 중…");
    db.from("sl_jobs").select("*").order("sort_order", { ascending: true }).limit(100).then(function (r) {
      if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
      var rows = r.data || [];
      state.cache.job = {};
      rows.forEach(function (x) { state.cache.job[x.id] = x; });
      if (!rows.length) { box.innerHTML = emptyBox("등록된 공고가 없습니다."); return; }
      box.innerHTML = '<table class="tbl"><thead><tr><th>포지션</th><th>팀</th><th>형태</th>' +
        "<th>마감</th><th>상태</th><th></th></tr></thead><tbody>" +
        rows.map(function (x) {
          return '<tr><td class="t-title">' + esc(x.title) + "</td><td>" + esc(x.team || "-") +
            "</td><td>" + esc(x.employment_type || "-") + "</td><td>" +
            esc(x.closes_at ? SL.fmtDate(x.closes_at) : "채용 시 마감") + "</td><td>" + pubBadge(x.published) + "</td>" +
            '<td><div class="row-actions">' +
            '<button class="lnk" data-job-edit="' + escA(x.id) + '">수정</button>' +
            '<button class="lnk" data-job-toggle="' + escA(x.id) + '">' + (x.published ? "비공개" : "공개") + "</button>" +
            '<button class="lnk danger" data-job-del="' + escA(x.id) + '">삭제</button>' +
            "</div></td></tr>";
        }).join("") + "</tbody></table>";
    });
  }

  function jobForm(x) {
    x = x || {};
    return '<div class="field"><label for="j-title">포지션명 *</label>' +
      '<input id="j-title" maxlength="160" value="' + escA(x.title || "") + '"></div>' +
      '<div class="row2"><div class="field"><label for="j-team">팀</label>' +
      '<input id="j-team" maxlength="60" value="' + escA(x.team || "") + '"></div>' +
      '<div class="field"><label for="j-type">고용 형태</label>' +
      '<input id="j-type" maxlength="40" value="' + escA(x.employment_type || "정규직") + '"></div></div>' +
      '<div class="row2"><div class="field"><label for="j-loc">근무지</label>' +
      '<input id="j-loc" maxlength="80" value="' + escA(x.location || "") + '"></div>' +
      '<div class="field"><label for="j-close">마감일 <span class="hint" style="display:inline;margin:0">(비우면 상시)</span></label>' +
      '<input id="j-close" type="date" value="' + escA(x.closes_at || "") + '"></div></div>' +
      '<div class="field"><label for="j-summary">한 줄 요약</label>' +
      '<input id="j-summary" maxlength="200" value="' + escA(x.summary || "") + '"></div>' +
      '<div class="field"><label for="j-body">상세 내용</label>' +
      '<textarea id="j-body" style="min-height:240px" placeholder="[담당 업무]\n- …\n\n[자격 요건]\n- …">' +
      esc(x.body || "") + "</textarea>" +
      '<div class="hint">줄바꿈이 그대로 표시됩니다.</div></div>' +
      '<div class="field"><label for="j-order">정렬 순서(작을수록 위)</label>' +
      '<input id="j-order" type="number" value="' + escA(x.sort_order == null ? 0 : x.sort_order) + '"></div>' +
      '<label class="consent"><input type="checkbox" id="j-pub"' + (x.published ? " checked" : "") +
      "><span>채용 페이지에 공개합니다.</span></label>" +
      '<div class="alert" id="md-alert"></div>';
  }

  function saveJob(id) {
    var payload = {
      title: val("j-title").trim(), team: val("j-team").trim(),
      employment_type: val("j-type").trim(), location: val("j-loc").trim(),
      closes_at: val("j-close") || null, summary: val("j-summary").trim(),
      body: val("j-body"), sort_order: parseInt(val("j-order"), 10) || 0,
      published: checked("j-pub"),
    };
    if (!payload.title) { show("md-alert", "bad", "포지션명을 입력해 주세요."); return; }
    var p = id ? db.from("sl_jobs").update(payload).eq("id", id) : db.from("sl_jobs").insert(payload);
    p.then(function (r) {
      if (r.error) { show("md-alert", "bad", r.error.message); return; }
      audit(id ? "update" : "create", "sl_jobs", id || payload.title, { title: payload.title });
      closeModal(); loadJob(); loadDash();
    });
  }

  document.getElementById("job-new").addEventListener("click", function () {
    openModal("새 채용 공고", jobForm(null), [
      { label: "취소", on: closeModal },
      { label: "저장", cls: "", on: function () { saveJob(null); } },
    ]);
  });

  document.addEventListener("click", function (e) {
    var ed = e.target.closest("[data-job-edit]");
    if (ed) {
      var x = state.cache.job[ed.getAttribute("data-job-edit")];
      openModal("채용 공고 수정", jobForm(x), [
        { label: "취소", on: closeModal },
        { label: "저장", cls: "", on: function () { saveJob(x.id); } },
      ]);
      return;
    }
    var tg = e.target.closest("[data-job-toggle]");
    if (tg) {
      var id = tg.getAttribute("data-job-toggle"), cur = state.cache.job[id];
      db.from("sl_jobs").update({ published: !cur.published }).eq("id", id).then(function (r) {
        if (!r.error) { audit("publish_toggle", "sl_jobs", id, { to: !cur.published }); loadJob(); loadDash(); }
      });
      return;
    }
    var dl = e.target.closest("[data-job-del]");
    if (dl) {
      var did = dl.getAttribute("data-job-del"), item = state.cache.job[did];
      openModal("공고 삭제", "<p style='color:var(--fg-dim)'>‘" + esc(item.title) + "’ 공고를 삭제합니다.</p>", [
        { label: "취소", on: closeModal },
        { label: "삭제 확인", cls: "", on: function () {
            db.from("sl_jobs").delete().eq("id", did).then(function (r) {
              if (!r.error) { audit("delete", "sl_jobs", did, { title: item.title }); closeModal(); loadJob(); loadDash(); }
            });
          } },
      ]);
    }
  });

  /* ═══════════════ 로그 · 감사 ═══════════════ */
  function loadLog() {
    var box = document.getElementById("log-table");
    box.innerHTML = emptyBox("불러오는 중…");
    var kind = val("log-filter");
    var q = db.from("sl_audit").select("id,kind,actor_email,action,entity,entity_id,detail,ip,created_at")
      .order("created_at", { ascending: false }).limit(250);
    if (kind) q = q.eq("kind", kind);
    q.then(function (r) {
      if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
      var rows = r.data || [];
      if (!rows.length) { box.innerHTML = emptyBox("기록이 없습니다."); return; }
      box.innerHTML = '<table class="tbl"><thead><tr><th>시각</th><th>구분</th><th>행위자</th>' +
        "<th>동작</th><th>대상</th><th>IP</th><th>상세</th></tr></thead><tbody>" +
        rows.map(function (x) {
          var kindLabel = { admin: "관리자", visit: "방문", submit: "제출" }[x.kind] || x.kind;
          var det = "";
          try { det = x.detail && Object.keys(x.detail).length ? JSON.stringify(x.detail) : ""; } catch (e) {}
          return "<tr><td>" + esc(SL.fmtDateTime(x.created_at)) + "</td><td>" + esc(kindLabel) + "</td>" +
            "<td>" + esc(x.actor_email || "-") + '</td><td class="t-title">' + esc(x.action) + "</td>" +
            "<td>" + esc(x.entity || "-") + "</td><td>" + esc(x.ip || "-") + "</td>" +
            '<td style="max-width:260px;word-break:break-all;font-size:.78rem">' + esc(det) + "</td></tr>";
        }).join("") + "</tbody></table>";
    });
  }
  document.getElementById("log-reload").addEventListener("click", loadLog);
  document.getElementById("log-filter").addEventListener("change", loadLog);

  /* ═══════════════ 설정 ═══════════════ */
  function loadSet() {
    db.from("sl_settings").select("key,value").then(function (r) {
      if (r.error) { show("set-alert", "bad", "설정을 불러오지 못했습니다: " + r.error.message); return; }
      var m = {};
      (r.data || []).forEach(function (row) { m[row.key] = row.value; });
      var n = m.notice || {};
      document.getElementById("set-notice-on").checked = !!n.on;
      document.getElementById("set-notice-text").value = n.text || "";
      document.getElementById("set-notice-href").value = n.href || "";
      document.getElementById("set-email").value = typeof m.contact_email === "string" ? m.contact_email : "";
      document.getElementById("set-hours").value = typeof m.business_hours === "string" ? m.business_hours : "";
      document.getElementById("set-sla").value = typeof m.sla_note === "string" ? m.sla_note : "";
    });
  }

  document.getElementById("set-save").addEventListener("click", function () {
    var href = val("set-notice-href").trim();
    if (href && !/^https?:\/\//i.test(href) && href.charAt(0) !== "/") {
      show("set-alert", "bad", "공지 링크는 / 로 시작하는 내부 경로 또는 http(s) 주소만 사용할 수 있습니다.");
      return;
    }
    var rows = [
      { key: "notice", value: { on: checked("set-notice-on"), text: val("set-notice-text").trim(), href: href } },
      { key: "contact_email", value: val("set-email").trim() },
      { key: "business_hours", value: val("set-hours").trim() },
      { key: "sla_note", value: val("set-sla").trim() },
    ];
    db.from("sl_settings").upsert(rows, { onConflict: "key" }).then(function (r) {
      if (r.error) { show("set-alert", "bad", r.error.message); return; }
      audit("update_setting", "sl_settings", "notice", { on: checked("set-notice-on") });
      show("set-alert", "ok", "저장되었습니다. 공개 페이지에는 새로고침 시 반영됩니다.");
    });
  });

  /* ═══════════════ 시작 ═══════════════ */
  loginView.style.display = "";
  gate();
})();
