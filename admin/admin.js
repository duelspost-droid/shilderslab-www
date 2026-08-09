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
  var state = { email: "", role: "", cache: {} };

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

  /* 모달 세대 번호. #modal-body 는 모든 모달이 **공유하는 하나의 엘리먼트**라,
     느린 조회가 끝나고 돌아왔을 때 그 사이 열린 다른 모달의 내용을 덮어쓸 수 있다.
     (실제 사고 경로: [오늘 방문]을 열어 두고 닫은 뒤 [비밀번호 재설정]을 열면,
      뒤늦게 도착한 방문 목록이 임시 비밀번호가 적힌 화면을 지워 버린다.)
     "모달이 열려 있는가" 로는 못 막는다 — 다른 모달도 열려 있는 상태이기 때문이다.
     요청 시점의 번호를 들고 있다가 돌아와서 같은지 확인한다. */
  var modalSeq = 0;

  function openModal(title, bodyHtml, actions) {
    modalSeq++;
    document.getElementById("modal-title").textContent = title;
    document.getElementById("modal-body").innerHTML = bodyHtml;
    var wrap = document.getElementById("modal-actions");
    wrap.innerHTML = "";
    (actions || []).forEach(function (a) {
      var b = document.createElement("button");
      /* ⚠ `a.cls || "btn-line"` 이면 **cls:"" 로 넘긴 확인 버튼**(저장·삭제·재설정)이
         취소와 똑같은 외곽선 버튼이 된다 — 실제로 전부 구분이 안 되고 있었다.
         cls 를 아예 안 준 경우만 btn-line(보조), "" 는 기본 .btn(강조)로 둔다. */
      b.className = "btn " + (a.cls == null ? "btn-line" : a.cls) + " btn-sm";
      b.textContent = a.label;
      b.addEventListener("click", a.on);
      wrap.appendChild(b);
    });
    modal.classList.add("on");
  }
  /** 모달의 확인(마지막) 버튼을 저장 중에 잠근다 — 연타로 같은 글이 두 번 등록되던 문제.
      복구용 함수를 돌려주므로 실패 시 되돌리면 된다. */
  function lockModalAction(labelWhileBusy) {
    var wrap = document.getElementById("modal-actions");
    var btns = wrap ? wrap.querySelectorAll("button") : [];
    if (!btns.length) return function () {};
    var b = btns[btns.length - 1];
    var prev = b.textContent, prevDisabled = b.disabled;
    b.disabled = true;
    b.textContent = labelWhileBusy || "저장 중…";
    return function () { b.disabled = prevDisabled; b.textContent = prev; };
  }

  function closeModal() {
    modalSeq++;
    modal.classList.remove("on");
    /* 임시 비밀번호 등 민감값이 DOM 에 남지 않게 비운다 */
    document.getElementById("modal-body").innerHTML = "";
    document.getElementById("modal-actions").innerHTML = "";
  }
  modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });

  /** 관리자 행위 로깅 — 실패해도 화면 흐름을 막지 않는다.
      ⚠ db.rpc() 가 돌려주는 PostgrestBuilder 는 **Promise 가 아니라 thenable** 이다.
      then() 만 있고 catch() 는 없다(assets/vendor/supabase.min.js 실측:
      typeof builder.catch === "undefined", builder instanceof Promise === false).
      그래서 `db.rpc(...).catch(...)` 는 호출 즉시 TypeError 를 **동기적으로** 던졌고,
      감사 실패를 흡수하려던 장치가 오히려 호출자 흐름을 끊고 있었다.

      실제 피해(2026-08-08 적대적 검증에서 발견, 라이브에 나가 있던 코드):
        · 로그인 직후 audit("login") 이 던져 loadDash()/loadInq()/loadApp() 이 실행되지 않음
          → 콘솔이 빈 화면. 게다가 그 거부는 이미 숨겨진 로그인 화면의 알림칸으로 흘러가 무증상
        · 로그아웃 버튼이 signOut() 에 도달하지 못함 → 세션이 localStorage 에 그대로 남음
        · 비밀번호 변경은 서버에서 성공했는데 화면에는 실패로 표시(모달도 닫히지 않아 입력값 잔존)

      Promise.resolve() 로 감싸면 thenable 이 진짜 Promise 가 되어 catch 가 붙는다.
      혹시 모를 동기 예외까지 try 로 막아 이 함수는 **절대 던지지 않는다**. */
  function audit(action, entity, id, detail) {
    try {
      return Promise.resolve(db.rpc("sl_log", {
        p_action: action, p_entity: entity || null,
        p_entity_id: id ? String(id) : null, p_detail: detail || {},
      })).catch(function () { /* noop */ });
    } catch (e) {
      return Promise.resolve();
    }
  }

  function val(id) { var e = document.getElementById(id); return e ? e.value : ""; }
  function checked(id) { var e = document.getElementById(id); return !!(e && e.checked); }

  /* ═══════════════ 경로 → 페이지 이름 ═══════════════
     방문 로그에는 `/services/cloud/` 같은 경로만 남는다. 목록에서 경로만 보면
     어느 화면인지 매번 머릿속으로 옮겨야 해서, 사람이 읽는 이름을 함께 보여준다.

     이름표(admin/page-titles.js)는 **빌드 생성물**이다 — 페이지를 추가하면 저절로 따라온다.
     다만 빌드 이후 콘솔에서 발행한 인사이트는 아직 그 안에 없다. 그런 경로만
     withPageTitles() 가 DB 제목으로 메운다(못 메워도 경로로는 보인다). */
  var PAGE_TITLES = window.SL_PAGE_TITLES || {};

  function normPath(p) {
    var s = String(p || "/").split("#")[0].split("?")[0];
    if (!s) return "/";
    if (s.charAt(0) !== "/") s = "/" + s;
    /* `/about` 과 `/about/` 이 따로 집계되지 않게 맞춘다. 파일 경로(.html)는 그대로 둔다. */
    if (s.length > 1 && s.slice(-1) !== "/" && s.indexOf(".") === -1) s += "/";
    return s;
  }

  function pageName(p) { return PAGE_TITLES[normPath(p)] || ""; }

  /** 상위 묶음 이름. `/services/cloud/` → "서비스" (한 칸 위 경로의 이름)
      최상위 페이지의 부모는 "/"(홈)인데, 그걸 묶음으로 붙이면 `홈 › 회사소개` 처럼
      모든 줄에 "홈" 이 달려 오히려 읽기 나빠진다. 그래서 "/" 는 묶음으로 치지 않는다. */
  function pageGroup(p) {
    var s = normPath(p), up = s.replace(/[^/]+\/$/, "");
    if (!up || up === s || up === "/") return "";
    return PAGE_TITLES[up] || "";
  }

  /** 목록 한 칸 — 이름을 위에, 경로를 아래에. 이름을 모르면 경로만 크게 보인다.

      경로는 **로그에 남은 원본 그대로** 보여 준다. 집계(sl_stats)는 원본 문자열로 묶는데
      화면에만 정규화한 값을 쓰면, `/about` 과 `/about/` 이 서로 다른 두 줄로 집계돼 놓고
      화면에는 똑같은 `/about/` 이 두 번 뜬다 — 무엇이 실제로 요청된 경로인지 알 수 없게 된다.
      정규화는 **이름을 찾을 때만** 쓴다. */
  function pageCell(p) {
    var raw = String(p == null || p === "" ? "/" : p);
    var sp = normPath(raw), nm = pageName(sp), gp = pageGroup(sp);
    if (!nm) return '<span class="pg"><b class="pg-name">' + esc(raw) + "</b></span>";
    return '<span class="pg"><b class="pg-name">' +
      (gp ? '<span class="pg-group">' + esc(gp) + " › </span>" : "") + esc(nm) +
      "</b><code>" + esc(raw) + "</code></span>";
  }

  /** 이름을 모르는 인사이트 경로만 DB 에서 제목을 채운 뒤 cb 를 부른다. */
  function withPageTitles(paths, cb) {
    var want = [];
    (paths || []).forEach(function (p) {
      var s = normPath(p), m = /^\/insights\/([^/]+)\/$/.exec(s);
      if (m && !PAGE_TITLES[s] && want.indexOf(m[1]) === -1) want.push(m[1]);
    });
    if (!want.length) { cb(); return; }
    /* ⚠ .in() 이 돌려주는 것도 PostgrestBuilder(지연 thenable)다 — Promise 로 감싼다. */
    Promise.resolve(db.from("sl_insights").select("slug,title").in("slug", want))
      .then(function (r) {
        ((r && r.data) || []).forEach(function (x) {
          if (x && x.slug) PAGE_TITLES["/insights/" + x.slug + "/"] = x.title || "";
        });
      })
      .catch(function () { /* 이름을 못 채워도 경로로는 보인다 */ })
      .then(cb, cb);
  }

  /* ═══════════════ 인증 ═══════════════
     Supabase 인증에는 사용자명 provider 가 없다 — 식별자는 반드시 이메일 형식이어야 한다.
     그래서 화면에서만 아이디를 받고, 여기서 고정 도메인을 붙여 이메일로 바꾼다.
     `shieldusadmin` → `shieldusadmin@<LOGIN_DOMAIN>`

     조회 테이블을 두지 않고 **접미사 규칙**으로 푸는 이유:
     아이디→이메일 매핑을 공개 경로에 두면 아이디를 아는 사람이 연결된 주소를 알아낼 수 있다.
     계정 주소를 회사 도메인으로 고정하면 알아내도 잃을 것이 없다.
     개인 주소(예: 개인 메일)를 계정 이메일로 쓰면 그 주소가 로그인 화면에서 드러난다 —
     그 조합은 피한다.

     ⚠ LOGIN_DOMAIN 은 **실제 계정 이메일의 도메인과 같아야** 아이디 로그인이 동작한다.
     계정 주소를 바꾸면 여기도 함께 바꾼다. @ 를 포함해 입력하면 규칙을 건너뛰므로,
     도메인이 어긋나 있어도 이메일 전체를 넣어 로그인할 수 있다(잠김 방지). */
  var LOGIN_DOMAIN = "shielduslab.com";

  function toLoginEmail(input) {
    var s = (input || "").trim();
    if (!s) return "";
    return s.indexOf("@") >= 0 ? s : s.toLowerCase() + "@" + LOGIN_DOMAIN;
  }

  var loginForm = document.getElementById("login-form");
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = document.getElementById("lg-submit");
    var email = toLoginEmail(val("lg-email")), pw = val("lg-pw");
    if (!email || !pw) { show("login-alert", "bad", "아이디와 비밀번호를 입력해 주세요."); return; }
    btn.disabled = true; btn.textContent = "확인 중…";
    db.auth.signInWithPassword({ email: email, password: pw }).then(function (r) {
      if (r.error) throw r.error;
      return gate();
    }).catch(function (err) {
      var m = (err && err.message) || "";
      /* 아이디가 존재하는지 여부는 알려주지 않는다 — 열거를 막기 위해 문구를 하나로 둔다. */
      show("login-alert", "bad", /Invalid login/i.test(m)
        ? "아이디 또는 비밀번호가 올바르지 않습니다."
        : "로그인에 실패했습니다: " + m);
      btn.disabled = false; btn.textContent = "로그인";
    });
  });

  /* ═══════════════ 비밀번호 변경 (본인) ═══════════════
     임시 비밀번호로 처음 들어온 관리자가 콘솔 안에서 바로 바꿀 수 있게 한다.
     이 화면이 없으면 Supabase 대시보드에 들어가야 하고, 대시보드 접근 권한이 없는
     editor 는 비밀번호를 스스로 바꿀 방법이 아예 없다.

     · 입력값은 모달 안에만 두고 닫을 때 DOM 에서 지운다(closeModal 이 비운다).
     · 감사 로그에는 **행위만** 남긴다. 비밀번호도, 길이도 남기지 않는다.
     · 프로젝트에 'Secure password change' 가 켜져 있으면 서버가 재인증(nonce)을 요구한다.
       그 경우는 사용자에게 재로그인을 안내한다 — 콘솔에서 처리하지 않는다. */
  var PW_MIN = 10;

  function openSelfPasswordModal() {
    openModal("비밀번호 변경",
      '<div class="form">' +
      '<div class="field"><label for="pw-new">새 비밀번호</label>' +
      '<input id="pw-new" type="password" autocomplete="new-password" maxlength="72">' +
      '<div class="hint">' + PW_MIN + '자 이상. 다른 서비스에서 쓰지 않는 것으로 정하세요.</div></div>' +
      '<div class="field"><label for="pw-new2">새 비밀번호 확인</label>' +
      '<input id="pw-new2" type="password" autocomplete="new-password" maxlength="72"></div>' +
      '<div class="alert" id="pw-alert" role="status"></div>' +
      '</div>',
      [{ label: "취소", on: closeModal },
       { label: "변경", cls: "primary", on: doChangePassword }]);
    var f = document.getElementById("pw-new");
    if (f) f.focus();
  }

  /* 헤더에서도, [계정 관리] 내 계정 행에서도 같은 모달을 연다. */
  document.getElementById("pw-change").addEventListener("click", openSelfPasswordModal);

  function doChangePassword() {
    var a = val("pw-new"), b = val("pw-new2");
    if (a.length < PW_MIN) {
      show("pw-alert", "bad", "비밀번호는 " + PW_MIN + "자 이상이어야 합니다."); return;
    }
    if (a !== b) { show("pw-alert", "bad", "두 입력이 서로 다릅니다."); return; }

    show("pw-alert", "ok", "변경하는 중…");
    db.auth.updateUser({ password: a }).then(function (r) {
      if (r.error) {
        var m = String(r.error.message || "");
        if (/reauthenticat/i.test(m)) {
          show("pw-alert", "bad",
               "보안 설정 때문에 재인증이 필요합니다. 로그아웃 후 다시 로그인한 뒤 시도해 주세요.");
        } else if (/same as the old|should be different/i.test(m)) {
          show("pw-alert", "bad", "지금 쓰고 있는 비밀번호와 같습니다. 다른 값으로 정해 주세요.");
        } else if (/weak|pwned|password/i.test(m)) {
          show("pw-alert", "bad", "이 비밀번호는 사용할 수 없습니다: " + m);
        } else {
          show("pw-alert", "bad", "변경하지 못했습니다: " + m);
        }
        return;
      }
      /* 비밀번호·길이 등 값은 로그에 남기지 않는다. */
      audit("change_password", "auth.users", null, {});
      show("pw-alert", "ok", "변경되었습니다. 다음 로그인부터 새 비밀번호를 쓰세요.");
      setTimeout(closeModal, 1600);
    }).catch(function (e) {
      /* 네트워크 단절 등 — 여기서 잡지 않으면 "변경하는 중…" 에서 멈춘 것처럼 보인다. */
      show("pw-alert", "bad", "요청이 실패했습니다. 연결을 확인하고 다시 시도해 주세요."
           + (e && e.message ? " (" + e.message + ")" : ""));
    });
  }

  document.getElementById("logout").addEventListener("click", function () {
    /* 감사 로깅이나 signOut 이 실패해도 **반드시** 화면을 초기화한다.
       로그아웃이 조용히 무동작으로 끝나면 세션이 localStorage 에 남아,
       공용 PC 에서 다음 사람이 그대로 콘솔에 들어간다. */
    audit("logout")
      .then(function () { return db.auth.signOut(); })
      .catch(function () { /* 세션 정리는 아래 reload 로라도 끊는다 */ })
      .then(function () { location.reload(); });
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
        return db.rpc("sl_my_role").then(function (rr) {
          if (rr && rr.error) {
            /* 0004 미적용이거나 일시 장애 — 권한 없음으로 단정하지 않는다.
               탭은 그대로 두고 경고만 띄운다(실제 차단은 서버측 RPC/정책이 한다). */
            state.role = "unknown";
          } else {
            state.role = (rr && rr.data) || "editor";
          }
          loginView.style.display = "none";
          appView.style.display = "";
          document.getElementById("who").innerHTML =
            "<b>" + esc(state.email) + "</b> · " +
            '<span class="badge ' + (state.role === "admin" ? "on" : "off") + '">' +
            esc(state.role) + "</span>";
          /* editor 는 계정 관리·설정·로그 탭을 볼 수 없다(서버측에서도 차단된다) */
          if (state.role === "unknown") {
            var warn = document.createElement("div");
            warn.className = "alert on info";
            warn.style.margin = "18px 0 0";
            warn.textContent =
              "역할 정보를 확인할 수 없습니다. 마이그레이션(0004)이 적용되지 않았거나 일시 장애일 수 있습니다. " +
              "계정 관리·설정 기능은 서버에서 거부될 수 있습니다.";
            var host = document.querySelector("#app-view .shell");
            if (host) host.insertBefore(warn, host.firstChild);
          } else if (state.role !== "admin") {
            Array.prototype.forEach.call(document.querySelectorAll("[data-owner]"), function (el) {
              el.style.display = "none";
            });
          }
          audit("login");
          loadDash(); loadInq(); loadApp();
        });
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
    var loaders = { dash: loadDash, inq: loadInq, app: loadApp, ins: loadIns, job: loadJob,
                    cnt: loadCnt, card: loadCard, log: loadLog, acct: loadAcct, set: loadSet };
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

  /* ═══════════════ 방문 상세 ═══════════════
     대시보드의 [오늘 방문] 카드를 누르면 열린다.
     원본은 sl_audit 의 kind='visit' 행이다(sl_log_visit 가 적재, 동일 IP·경로 10분 중복 제외).
     개인 식별을 늘리지 않기 위해 **개별 IP 는 보여주지 않고** 고유 IP 개수만 센다. */
  function openVisitDetail() {
    openModal("오늘 방문 상세", '<div class="empty">불러오는 중…</div>',
              [{ label: "닫기", on: closeModal }]);
    var seq = modalSeq;   /* 돌아왔을 때 아직 '이' 모달인지 확인하는 표 */
    var since = new Date(); since.setHours(0, 0, 0, 0);

    db.from("sl_audit").select("entity,ip,detail,created_at")
      .eq("kind", "visit").gte("created_at", since.toISOString())
      .order("created_at", { ascending: false }).limit(1000)
      .then(function (r) {
        if (modalSeq !== seq) return;   /* 그 사이 다른 모달이 열렸다 — 남의 화면을 건드리지 않는다 */
        var box = document.getElementById("modal-body");
        if (!box) return;
        if (r.error) {
          box.innerHTML = emptyBox("방문 기록을 불러오지 못했습니다: " + r.error.message +
            " (감사 로그 열람은 admin 역할만 가능합니다)");
          return;
        }
        var rows = r.data || [];
        if (!rows.length) {
          box.innerHTML = emptyBox(
            "오늘 기록된 방문이 없습니다. 관리자 화면은 집계에서 빠지므로(data-no-log) " +
            "공개 페이지를 열어야 쌓입니다.");
          return;
        }
        var byPage = {}, byHour = new Array(24).fill(0), byRef = {}, ips = {};
        rows.forEach(function (v) {
          var pg = v.entity || "/";
          byPage[pg] = (byPage[pg] || 0) + 1;
          byHour[new Date(v.created_at).getHours()]++;
          if (v.ip) ips[v.ip] = 1;
          var ref = (v.detail && v.detail.ref) || "";
          var host = "직접 방문 · 북마크";
          if (ref) { try { host = new URL(ref).hostname; } catch (e) { host = ref.slice(0, 40); } }
          byRef[host] = (byRef[host] || 0) + 1;
        });
        var sort = function (o) {
          return Object.keys(o).map(function (k) { return [k, o[k]]; })
                       .sort(function (a, b) { return b[1] - a[1]; });
        };
        var maxH = Math.max.apply(null, byHour) || 1;

        withPageTitles(Object.keys(byPage), function () {
        /* 제목 조회 중에 다른 모달이 열렸을 수 있다. 세대가 다르면 손대지 않는다. */
        if (modalSeq !== seq) return;
        box = document.getElementById("modal-body");
        if (!box) return;
        var html =
          '<div class="mini-stats" style="margin-bottom:20px">' +
            '<div class="mini-stat"><b>' + rows.length + "</b><span>오늘 방문</span></div>" +
            '<div class="mini-stat"><b>' + Object.keys(ips).length + "</b><span>고유 방문자</span></div>" +
            '<div class="mini-stat"><b>' + Object.keys(byPage).length + "</b><span>열린 페이지</span></div>" +
          "</div>" +
          '<h3 style="font-size:.92rem;margin:0 0 10px">시간대별</h3>' +
          '<div class="bars" style="height:110px;margin-bottom:22px">' +
            byHour.map(function (n, h) {
              return '<div class="b" style="height:' + Math.max(3, Math.round((n / maxH) * 100)) +
                '%" title="' + escA(h + "시 · " + n + "건") + '"><span>' +
                (h % 3 === 0 ? h : "") + "</span></div>";
            }).join("") +
          "</div>" +
          '<h3 style="font-size:.92rem;margin:0 0 10px">페이지별</h3>' +
          '<ul class="toppages" style="margin-bottom:22px">' +
            sort(byPage).slice(0, 15).map(function (p) {
              return "<li>" + pageCell(p[0]) + "<b>" + p[1] + "</b></li>";
            }).join("") +
          "</ul>" +
          '<h3 style="font-size:.92rem;margin:0 0 10px">유입 경로</h3>' +
          '<ul class="toppages" style="margin-bottom:22px">' +
            sort(byRef).slice(0, 10).map(function (p) {
              return "<li><code>" + esc(p[0]) + "</code><b>" + p[1] + "</b></li>";
            }).join("") +
          "</ul>" +
          '<h3 style="font-size:.92rem;margin:0 0 10px">최근 방문</h3>' +
          '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>시각</th><th>페이지</th><th>유입</th></tr></thead><tbody>' +
            rows.slice(0, 30).map(function (v) {
              var ref = (v.detail && v.detail.ref) || "";
              var host = "직접";
              if (ref) { try { host = new URL(ref).hostname; } catch (e) { host = ref.slice(0, 30); } }
              return "<tr><td>" + esc(SL.fmtDateTime(v.created_at)) + "</td><td>" +
                pageCell(v.entity) + "</td><td>" + esc(host) + "</td></tr>";
            }).join("") +
          "</tbody></table></div>" +
          '<p class="tiny" style="margin-top:14px">동일 IP·경로는 10분 안에 중복으로 세지 않습니다. ' +
          "관리자 화면은 집계에서 제외됩니다.</p>";
        box.innerHTML = html;
        });
      });
  }

  document.addEventListener("click", function (e) {
    var s = e.target.closest("[data-stat]");
    if (s && s.getAttribute("data-stat") === "visit") openVisitDetail();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var s = e.target.closest && e.target.closest("[data-stat]");
    if (s && s.getAttribute("data-stat") === "visit") { e.preventDefault(); openVisitDetail(); }
  });

  /* ═══════════════ 대시보드 ═══════════════ */
  function loadDash() {
    /* 목록 탭들은 "불러오는 중…"을 보여 주는데 대시보드만 빈 화면이었다 —
       느린 회선에서 로그인 직후 아무것도 없는 화면이 잠깐 뜬다. 자리표시를 먼저 채운다. */
    var statsBox = document.getElementById("stats");
    if (statsBox && !statsBox.children.length) {
      statsBox.innerHTML = '<div class="empty" style="grid-column:1/-1">불러오는 중…</div>';
    }
    var recentBox = document.getElementById("recent-inq");
    if (recentBox && !recentBox.children.length) recentBox.innerHTML = emptyBox("불러오는 중…");

    db.rpc("sl_stats").then(function (r) {
      if (r.error) throw r.error;
      var s = r.data || {};
      /* 4번째 항목은 클릭 동작: 탭 이동(data-goto) 또는 상세 모달(data-stat) */
      var cards = [
        ["새 문의", s.inq_new, "미확인 상태", { goto: "inq" }],
        ["문의 (7일)", s.inq_7d, "총 " + (s.inq_total || 0) + "건", { goto: "inq" }],
        ["새 지원서", s.app_new, "총 " + (s.app_total || 0) + "건", { goto: "app" }],
        ["오늘 방문", s.visit_today, "7일 " + (s.visit_7d || 0) + " · 30일 " + (s.visit_30d || 0),
         { stat: "visit" }],
        ["인사이트", s.insight_pub, "전체 " + (s.insight_total || 0) + "건 중 공개", { goto: "ins" }],
        ["공개 공고", s.job_pub, "채용 페이지 노출", { goto: "job" }],
      ];
      document.getElementById("stats").innerHTML = cards.map(function (c) {
        var act = c[3] || {};
        var attr = act.goto ? ' data-goto="' + act.goto + '"'
                 : act.stat ? ' data-stat="' + act.stat + '"' : "";
        var cls = "mini-stat" + (attr ? " clickable" : "");
        var a11y = attr ? ' role="button" tabindex="0"' : "";
        return '<div class="' + cls + '"' + attr + a11y + "><b>" + esc(c[1] == null ? 0 : c[1]) +
          "</b><span>" + esc(c[0]) + '</span><span style="color:var(--muted);opacity:.75">' +
          esc(c[2]) + "</span></div>";
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
      withPageTitles(tp.map(function (p) { return p.page; }), function () {
        document.getElementById("toppages").innerHTML = tp.length
          ? tp.map(function (p) {
              return "<li>" + pageCell(p.page) + "<b>" + esc(p.n) + "</b></li>";
            }).join("")
          : '<li style="color:var(--muted)">데이터 없음</li>';
      });
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
    var unlock = lockModalAction();   /* 연타로 같은 글이 두 번 등록되지 않게 */
    var p = id ? db.from("sl_insights").update(payload).eq("id", id)
               : db.from("sl_insights").insert(payload);
    Promise.resolve(p).then(function (r) {
      if (r && r.error) {
        unlock();
        show("md-alert", "bad", /duplicate|unique/i.test(r.error.message)
          ? "이미 사용 중인 slug 입니다." : r.error.message);
        return;
      }
      audit(id ? "update" : "create", "sl_insights", id || payload.slug, { title: payload.title });
      closeModal(); loadIns(); loadDash();
    }).catch(function (e) {
      unlock();
      show("md-alert", "bad", "저장하지 못했습니다: " + ((e && e.message) || "연결을 확인해 주세요."));
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
    var unlock = lockModalAction();   /* 연타로 같은 공고가 두 번 등록되지 않게 */
    var p = id ? db.from("sl_jobs").update(payload).eq("id", id) : db.from("sl_jobs").insert(payload);
    Promise.resolve(p).then(function (r) {
      if (r && r.error) { unlock(); show("md-alert", "bad", r.error.message); return; }
      audit(id ? "update" : "create", "sl_jobs", id || payload.title, { title: payload.title });
      closeModal(); loadJob(); loadDash();
    }).catch(function (e) {
      unlock();
      show("md-alert", "bad", "저장하지 못했습니다: " + ((e && e.message) || "연결을 확인해 주세요."));
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


  /* ═══════════════ 명함 ═══════════════
     공개 페이지(/brand/)에 있던 것을 여기로 옮겼다. 대외 공개할 자료가 아니라 내부 자료다.
     파일 이름이 규칙적이라(card-{A|B|C}[-ko]-{front|back}.{svg,pdf,png,jpg})
     목록을 손으로 적지 않고 조합으로 만든다 — 시안이 늘어도 여기만 고치면 된다. */
  var CARD_SETS = [
    { key: "A", name: "에디토리얼", desc: "상단 액센트 바 + 좌측 정렬. 정보 위계가 가장 분명하다. 기본 권장안." },
    { key: "B", name: "여백형", desc: "심볼과 이름만 남긴 구성. 직함이 길거나 연락처가 적을 때 잘 맞는다." },
    { key: "C", name: "역상", desc: "딥 파인 바탕에 페이퍼 글자. 대외 행사용으로 눈에 띈다." },
  ];
  var CARD_VARIANTS = [
    { suffix: "", label: "영문형", note: "SHIELDUS LAB 우선" },
    { suffix: "-ko", label: "한글형", note: "쉴더스랩 우선 · 영문 병기" },
  ];
  var CARD_SIDES = [{ k: "front", ko: "앞면" }, { k: "back", ko: "뒷면" }];

  function loadCard() {
    var box = document.getElementById("card-grid");
    if (!box) return;
    var html = "";
    CARD_VARIANTS.forEach(function (v) {
      html += '<h3 class="cnt-sec">' + esc(v.label) +
              ' <span class="kind-tag">' + esc(v.note) + "</span></h3>";
      CARD_SETS.forEach(function (s) {
        var base = "/assets/ci/card/card-" + s.key + v.suffix;
        html += '<div class="card-set">' +
          '<div class="card-set-head"><b>시안 ' + s.key + " · " + esc(s.name) + "</b>" +
          '<span class="hint" style="margin:0">' + esc(s.desc) + "</span></div>" +
          '<div class="card-sides">' +
          CARD_SIDES.map(function (sd) {
            var f = base + "-" + sd.k;
            return '<div class="card-one">' +
              '<a href="' + f + '@300.jpg" target="_blank" rel="noopener" class="card-shot">' +
                '<img src="' + f + '@300.jpg" alt="" loading="lazy"></a>' +
              '<div class="card-cap">' + sd.ko + "</div>" +
              '<div class="card-dl">' +
                '<a href="' + f + '.pdf" download><b>PDF</b></a>' +
                '<a href="' + f + '.svg" download>SVG</a>' +
                '<a href="' + f + '@300.png" download>PNG</a>' +
                '<a href="' + f + '@300.jpg" download>JPG</a>' +
                '<a href="' + f + '-guide.svg" download title="재단선·안전여백 표시">가이드</a>' +
              "</div></div>";
          }).join("") +
          "</div></div>";
      });
    });
    box.innerHTML = html;
  }

  /* ═══════════════ 페이지 문구 (sl_content) ═══════════════
     값은 평문/최소 마크다운으로만 저장한다. HTML 을 저장하지 않는 것이 이 화면의 계약이고,
     그래서 공개 페이지에서 이스케이프 후 렌더해도 안전하다. */
  var cntRows = [];

  /** 입력한 그대로가 화면에서 어떻게 보이는지 아래에 그려 준다.
      공개 페이지와 **같은 렌더러**(SL.md / 이스케이프 후 줄바꿈→<br>)를 쓴다.
      여기서 다르게 그리면 미리보기가 거짓말이 된다. */
  function renderPreview(el, kind, i) {
    var box = document.getElementById("cnt-f-" + i + "-prev");
    if (!box) return;
    var v = (el.value || "").trim();
    if (!v) {
      box.innerHTML = '<span style="color:var(--muted)">비워 두면 사이트 기본 문구가 그대로 나옵니다.</span>';
      return;
    }
    if (kind === "rich" && window.SL && SL.md) {
      /* 문단 끝 표시(¶)는 CSS 의 .prev-rich>p::after 가 붙인다 — HTML 을 건드리지 않는다. */
      box.innerHTML = SL.md(v);
    } else {
      /* 줄바꿈 자리에 ↵ 를 눈에 보이게 찍는다. 실제 출력은 <br> 하나뿐이다. */
      box.innerHTML = esc(v).replace(/\n/g, '<span class="brk">↵</span><br>');
    }
  }

  /** 대분류 이름 → 카드 인덱스. 렌더 순서(sort_order)가 곧 카드 순서다. */
  function secIdxOf(section) {
    var seen = [], idx = -1;
    for (var i = 0; i < cntRows.length; i++) {
      var s = cntRows[i].section;
      if (seen.indexOf(s) < 0) { seen.push(s); }
      if (s === section) { idx = seen.indexOf(s); break; }
    }
    return idx;
  }

  /** 그 대분류에 저장 안 된 변경이 있는지 계산해 카드에 표식을 켠다. */
  function markSectionDirty(section) {
    var idx = secIdxOf(section);
    var card = document.getElementById("cnt-card-" + idx);
    if (!card) return;
    var dirty = false;
    cntRows.forEach(function (row, i) {
      if (row.section !== section || dirty) return;
      var el = document.getElementById("cnt-f-" + i);
      if (el && el.value !== (row.value || "")) dirty = true;
    });
    card.classList.toggle("dirty", dirty);
  }

  function refreshAllDirty() {
    var seen = [];
    cntRows.forEach(function (r) {
      if (seen.indexOf(r.section) < 0) { seen.push(r.section); markSectionDirty(r.section); }
    });
  }

  /** 바뀐 항목만 저장한다. rows 를 좁히면 그 대분류만 저장된다. */
  function saveCnt(rowsFilter, alertId, doneMsgEl) {
    var changed = [];
    cntRows.forEach(function (row, i) {
      if (rowsFilter && !rowsFilter(row)) return;
      var el = document.getElementById("cnt-f-" + i);
      if (!el) return;
      if (el.value === (row.value || "")) return;
      changed.push({ key: row.key, value: el.value });
    });
    if (!changed.length) {
      if (doneMsgEl) { doneMsgEl.textContent = "바뀐 내용이 없습니다."; setTimeout(function () { doneMsgEl.textContent = ""; }, 2500); }
      else show(alertId, "ok", "바뀐 내용이 없습니다.");
      return;
    }
    if (doneMsgEl) doneMsgEl.textContent = "저장하는 중…";
    var done = 0, failed = null;
    changed.forEach(function (c) {
      /* key 만 보내면 나머지 컬럼이 기본값으로 덮인다 — value 만 갱신한다. */
      Promise.resolve(db.from("sl_content").update({ value: c.value }).eq("key", c.key))
        .then(function (r) {
          done++;
          if (r && r.error && !failed) failed = r.error.message;
          if (done !== changed.length) return;
          if (failed) {
            if (doneMsgEl) doneMsgEl.textContent = "";
            show(alertId, "bad", "저장 실패: " + failed);
            return;
          }
          changed.forEach(function (c2) {
            for (var i = 0; i < cntRows.length; i++) {
              if (cntRows[i].key === c2.key) { cntRows[i].value = c2.value; break; }
            }
          });
          audit("update_content", "sl_content", changed.map(function (c2) { return c2.key; }).join(","),
                { count: changed.length });
          refreshAllDirty();
          if (doneMsgEl) {
            doneMsgEl.textContent = changed.length + "개 저장됨";
            setTimeout(function () { doneMsgEl.textContent = ""; }, 3000);
          }
          show(alertId, "ok",
               changed.length + "개 항목을 저장했습니다. 공개 페이지는 새로고침하면 바로 반영됩니다.");
        }).catch(function (e) {
          done++;
          if (!failed) failed = (e && e.message) || "알 수 없는 오류";
          if (done === changed.length) {
            if (doneMsgEl) doneMsgEl.textContent = "";
            show(alertId, "bad", "저장 실패: " + failed);
          }
        });
    });
  }

  function loadCnt() {
    db.from("sl_content").select("key,value,kind,section,label,hint,sort_order")
      .order("sort_order", { ascending: true })
      .then(function (r) {
        var box = document.getElementById("cnt-body");
        if (r.error) {
          cntRows = [];
          box.innerHTML = emptyBox(
            "문구 목록을 불러오지 못했습니다. 0005 마이그레이션이 아직 적용되지 않았을 수 있습니다. (" +
            r.error.message + ")");
          return;
        }
        cntRows = r.data || [];
        if (!cntRows.length) {
          box.innerHTML = emptyBox("편집할 문구 블록이 없습니다. 0005 마이그레이션을 적용해 주세요.");
          return;
        }
        /* 대분류(section)마다 접이식 카드 하나. 49블록을 한 화면에 펼치면 못 쓴다.
           카드 안에 그 묶음만 저장하는 버튼을 따로 둔다(전체 저장도 헤더에 남긴다). */
        var html = "", sec = null, secIdx = -1, secCount = 0;
        function closeSection() {
          if (sec === null) return "";
          return '<div class="sec-save">' +
                   '<span class="tiny" id="cnt-sec-msg-' + secIdx + '"></span>' +
                   '<button class="btn btn-line btn-sm" data-cnt-save-sec="' + secIdx + '">' +
                     esc(sec) + " 저장</button>" +
                 "</div></div></div></details>";
        }
        cntRows.forEach(function (row, i) {
          if (row.section !== sec) {
            html += closeSection();
            sec = row.section; secIdx++;
            secCount = 0;
            cntRows.forEach(function (r2) { if (r2.section === sec) secCount++; });
            html += '<details class="cnt-card" id="cnt-card-' + secIdx + '" data-sec-idx="' + secIdx + '">' +
              '<summary><span class="sec-name">' + esc(sec) + "</span>" +
              '<span class="sec-count">' + secCount + "</span>" +
              '<span class="sec-dirty">● 저장 안 된 변경</span></summary>' +
              '<div class="sec-body"><div class="form" style="max-width:820px">';
          }
          var id = "cnt-f-" + i;
          var rich = row.kind === "rich";
          /* 줄바꿈을 쓰려면 한 줄짜리 입력칸이면 안 된다.
             예전에는 값이 90자 미만이면 <input> 을 줘서 Enter 를 아예 칠 수 없었다. */
          html += '<div class="field">' +
            '<label for="' + id + '">' + esc(row.label || row.key) +
              ' <span class="kind-tag">' + (rich ? "여러 문단" : "한 문단") + "</span></label>" +
            '<textarea id="' + id + '" rows="' + (rich ? 10 : 3) + '" maxlength="20000"></textarea>' +
            '<div class="fmt">' + (rich
              ? "<b>Enter 를 치면 문단이 나뉩니다.</b> 한 번이든 두 번이든 결과는 같습니다" +
                "(읽기 편하게 빈 줄을 넣으셔도 됩니다). 한 문단 안에서 줄만 바꾸는 방법은 없습니다.<br>" +
                "<code>**굵게**</code> · <code>- 목록</code> · <code>1. 번호</code> · " +
                "<code>&gt; 인용</code> · <code>[링크](/services/)</code>"
              : "<b>Enter</b> 를 치면 그 자리에서 화면의 줄이 바뀝니다. 제목은 보통 2줄까지가 보기 좋습니다.<br>" +
                "<code>**굵게**</code> 같은 표기는 여기서 쓰지 않습니다. 글자만 넣어 주세요.") +
            "</div>" +
            (row.hint ? '<div class="hint">' + esc(row.hint) + "</div>" : "") +
            '<div class="prev-wrap"><div class="prev-head">화면에 나오는 모습' +
              '<span class="brk-legend">' + (rich ? "¶ 문단 끝" : "↵ 줄바꿈") + "</span></div>" +
              '<div class="prev' + (rich ? " prev-rich" : "") + '" id="' + id + '-prev"></div></div>' +
            '<div class="hint mono" style="opacity:.7">' + esc(row.key) + "</div>" +
            "</div>";
        });
        html += closeSection();
        box.innerHTML = html;
        cntRows.forEach(function (row, i) {
          var el = document.getElementById("cnt-f-" + i);
          if (!el) return;
          el.value = row.value || "";
          el.setAttribute("data-sec-idx", String(secIdxOf(row.section)));
          var draw = function () {
            renderPreview(el, row.kind, i);
            markSectionDirty(row.section);   /* 어느 묶음에 미저장 변경이 있는지 표식 */
          };
          el.addEventListener("input", draw);
          renderPreview(el, row.kind, i);
        });
      });
  }

  /* 전체 저장 — 모든 대분류에서 바뀐 것만 */
  document.getElementById("cnt-save").addEventListener("click", function () {
    if (!cntRows.length) { show("cnt-alert", "bad", "불러온 문구가 없어 저장할 수 없습니다."); return; }
    saveCnt(null, "cnt-alert", null);
  });

  /* 대분류별 저장 — 카드 안 버튼(위임). 그 묶음만 저장한다. */
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-cnt-save-sec]");
    if (!b) return;
    var idx = Number(b.getAttribute("data-cnt-save-sec"));
    var seen = [], section = null;
    cntRows.forEach(function (r) {
      if (seen.indexOf(r.section) < 0) seen.push(r.section);
    });
    section = seen[idx];
    if (section == null) return;
    saveCnt(function (row) { return row.section === section; }, "cnt-alert",
            document.getElementById("cnt-sec-msg-" + idx));
  });

  /* 모두 펼치기 / 접기 — 49블록을 훑을 때 편하도록 */
  document.getElementById("cnt-expand").addEventListener("click", function () {
    var cards = document.querySelectorAll("#cnt-body .cnt-card");
    if (!cards.length) return;
    var anyClosed = Array.prototype.some.call(cards, function (c) { return !c.open; });
    Array.prototype.forEach.call(cards, function (c) { c.open = anyClosed; });
    this.textContent = anyClosed ? "모두 접기" : "모두 펼치기";
  });


  /* ═══════════════ 계정 관리 (admin 역할 전용) ═══════════════ */
  function tempPassword(len) {
    /* 혼동하기 쉬운 문자(0/O, 1/l/I)를 뺀 문자군들. */
    len = len || 20;
    var UP = "ABCDEFGHJKLMNPQRSTUVWXYZ";
    var LO = "abcdefghijkmnopqrstuvwxyz";
    var NU = "23456789";
    var SY = "!@#$%^&*-_";
    var ALL = UP + LO + NU + SY;
    var crypto = window.crypto || window.msCrypto;
    var buf = new Uint32Array(len);
    crypto.getRandomValues(buf);
    /* 각 문자군을 **최소 한 개씩** 넣는다 — Supabase 에 "대/소/숫자/기호 필수" 정책이
       켜져 있어도 통과하도록. (예전엔 순수 무작위라 이따금 한 군이 빠져 거부됐다.) */
    var out = [UP[buf[0] % UP.length], LO[buf[1] % LO.length],
               NU[buf[2] % NU.length], SY[buf[3] % SY.length]];
    for (var i = 4; i < len; i++) out.push(ALL[buf[i] % ALL.length]);
    /* Fisher–Yates 셔플 — 앞 네 자리가 늘 대·소·숫·기호로 고정되지 않게. */
    var sh = new Uint32Array(len);
    crypto.getRandomValues(sh);
    for (var j = len - 1; j > 0; j--) {
      var k = sh[j] % (j + 1), t = out[j]; out[j] = out[k]; out[k] = t;
    }
    return out.join("");
  }

  var PW_TEMP_MIN = 12;   // Edge(service_role)가 요구하는 최소 길이와 같아야 한다.

  /** 편집 가능한 비밀번호 칸 + [다시 생성] 버튼.
      계정 생성·비밀번호 재설정 모달이 **같은 UI** 를 쓰도록 공용화했다.
      자동값을 그대로 써도 되고, 지우고 직접 정해도 된다. */
  function pwFieldHtml(id, pw, labelText, hintText) {
    return '<div class="field">' +
      '<label for="' + id + '">' + esc(labelText) + "</label>" +
      '<div class="pw-row">' +
        '<input id="' + id + '" type="text" maxlength="72" value="' + escA(pw) + '" ' +
        'autocomplete="off" spellcheck="false" ' +
        "style=\"font-family:'IBM Plex Mono',monospace\">" +
        '<button type="button" class="btn btn-line btn-sm" data-pw-regen="' + id +
        '">다시 생성</button>' +
      "</div>" +
      '<div class="hint">' + esc(hintText) + "</div></div>";
  }

  /** Edge 함수 실패에서 **서버가 보낸 한국어 사유**를 꺼내 cb(메시지, 상태코드) 로 넘긴다.

      supabase-js 는 비-2xx 응답을 FunctionsHttpError 로 감싸는데, 그 message 는
      "Edge Function returned a non-2xx status code" 라는 **영문 고정 문자열**이다.
      그걸 그대로 보여주면 관리자는 무엇이 잘못됐는지 알 수 없다 —
      "관리자 목록에 없는 계정입니다" 같은 진짜 사유는 err.context(Response) 본문에 들어 있다. */
  function fnFail(err, cb) {
    var ctx = err && err.context;
    var status = (ctx && ctx.status) || 0;
    var generic = (err && err.message) || "알 수 없는 오류";
    if (!ctx || typeof ctx.json !== "function") { cb(generic, status); return; }
    Promise.resolve(ctx.json()).then(function (b) {
      cb((b && (b.message || b.error)) || generic, status);
    }).catch(function () { cb(generic, status); });
  }

  /** 함수가 아직 배포되지 않은 상태인지.

      두 갈래를 모두 인정해야 한다(실측):
       ① 미배포 프로젝트의 게이트웨이는 `404 {"code":"NOT_FOUND"}` 를 준다.
       ② 그런데 그 404 는 **CORS preflight 에서** 먼저 터진다. 비-2xx 인 데다
          preflight 응답의 allow-headers 에 content-type 이 없어 브라우저가 요청을 막는다.
          그러면 supabase-js 는 FunctionsFetchError 를 던지고 context 는 Response 가 아니라
          TypeError 라 status 가 0 이다. ①만 보면 이 흔한 경우를 놓쳐서
          "재설정 실패: Failed to send a request to the Edge Function" 라는
          영문만 뜬다 — 오너는 무엇을 해야 하는지 알 수 없다. */
  function notDeployed(msg, status) {
    var m = String(msg);
    if (status === 404 && /function not found|not found/i.test(m)) return true;
    return status === 0 && /failed to send a request|failed to fetch|networkerror/i.test(m);
  }

  function loadAcct() {
    var box = document.getElementById("acct-table");
    box.innerHTML = emptyBox("불러오는 중…");
    db.rpc("sl_admin_list").then(function (r) {
      if (r.error) { box.innerHTML = emptyBox("불러오지 못했습니다: " + r.error.message); return; }
      var rows = r.data || [];
      state.cache.acct = {};
      rows.forEach(function (x) { state.cache.acct[x.email] = x; });
      if (!rows.length) { box.innerHTML = emptyBox("등록된 관리자가 없습니다."); return; }
      /* 락아웃 판정은 '로그인 연결된 admin' 수로 한다(서버와 같은 기준) */
      var owners = rows.filter(function (x) { return x.role === "admin" && x.linked; }).length;
      box.innerHTML = '<table class="tbl"><thead><tr><th>이메일</th><th>역할</th><th>권한 결속</th>' +
        "<th>최근 로그인</th><th>등록일</th><th>메모</th><th></th></tr></thead><tbody>" +
        rows.map(function (x) {
          var lastAdmin = x.role === "admin" && x.linked && owners <= 1;
          var acts = [];
          if (!x.linked) {
            acts.push('<button class="lnk" data-acct-link="' + escA(x.email) + '">연결</button>');
          }
          if (!x.is_self && !lastAdmin) {
            acts.push('<button class="lnk" data-acct-role="' + escA(x.email) + '">' +
              (x.role === "admin" ? "editor 로 변경" : "admin 으로 변경") + "</button>");
          }
          /* 비밀번호 재설정은 **마지막 admin 이어도 막지 않는다** — 계정을 없애는 게 아니라서
             락아웃을 만들지 않고, 관리자가 한 명뿐일 때야말로 가장 필요하다.
             다만 **이 사이트가 만든 계정(pw_managed)** 에만 붙인다. 공유 Supabase 프로젝트라
             [연결]로 끌어온 남의 계정까지 바꿀 수 있으면 그건 탈취다(0006 참조).
             서버도 같은 기준으로 거부하므로 버튼이 없는 것은 화면 편의일 뿐 방어선이 아니다. */
          if (x.linked && !x.is_self && x.pw_managed) {
            acts.push('<button class="lnk" data-acct-pw="' + escA(x.email) + '">비밀번호 재설정</button>');
          }
          if (!x.is_self && !lastAdmin) {
            acts.push('<button class="lnk danger" data-acct-del="' + escA(x.email) + '">삭제</button>');
          }
          if (x.is_self) acts.push('<button class="lnk" data-acct-self-pw="1">내 비밀번호 변경</button>');
          else if (lastAdmin) acts.push('<span class="tiny">마지막 admin</span>');
          return '<tr><td class="t-title">' + esc(x.email) + "</td>" +
            '<td><span class="badge ' + (x.role === "admin" ? "on" : "off") + '">' + esc(x.role) + "</span></td>" +
            "<td>" + (x.linked
              ? '<span class="badge done">연결됨</span>'
              : '<span class="badge doing">미연결 · 권한 없음</span>') + "</td>" +
            "<td>" + esc(x.last_sign_in_at ? SL.fmtDateTime(x.last_sign_in_at) : "-") + "</td>" +
            "<td>" + esc(SL.fmtDate(x.created_at)) + "</td>" +
            "<td>" + esc(x.note || "-") + "</td>" +
            '<td><div class="row-actions">' + acts.join("") + "</div></td></tr>";
        }).join("") + "</tbody></table>";
    });
  }

  document.getElementById("acct-reload").addEventListener("click", loadAcct);

  document.getElementById("acct-new").addEventListener("click", function () {
    var pw = tempPassword();
    openModal("관리자 추가",
      '<div class="field"><label for="ac-email">이메일 *</label>' +
      '<input id="ac-email" type="email" maxlength="160" placeholder="name@shilderslab.com"></div>' +
      '<div class="field"><label for="ac-role">역할</label><select id="ac-role">' +
      '<option value="editor">editor — 콘텐츠 · 문의 처리</option>' +
      '<option value="admin">admin — 계정 · 설정까지 전체</option></select></div>' +
      '<div class="field"><label for="ac-note">메모</label>' +
      '<input id="ac-note" type="text" maxlength="200" placeholder="담당 · 소속 등"></div>' +
      '<label class="consent"><input type="checkbox" id="ac-login" checked>' +
      "<span><b>로그인 계정을 함께 생성</b>합니다(권장). 체크를 해제하면 <b>이미 존재하는 확인된 계정</b>에만 " +
      "권한을 붙입니다 — 계정이 없으면 등록이 거부됩니다.</span></label>" +
      '<div id="ac-pw-wrap" style="display:none">' +
      pwFieldHtml("ac-pw", pw, "초기 비밀번호 (직접 정해도 됩니다)",
        PW_TEMP_MIN + "자 이상. 자동값을 그대로 써도 되고 원하는 값으로 바꿔도 됩니다. " +
        "안전한 경로로 전달하고 첫 로그인 후 변경하도록 안내하세요. 창을 닫으면 다시 볼 수 없습니다.") +
      "</div>" +
      '<div class="alert" id="md-alert"></div>',
      [
        { label: "취소", on: closeModal },
        { label: "추가", cls: "", on: function () {
            var email = val("ac-email").trim().toLowerCase();
            var role = val("ac-role");
            var note = val("ac-note").trim();
            var withLogin = checked("ac-login");
            if (!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email)) {
              show("md-alert", "bad", "이메일 형식을 확인해 주세요."); return;
            }
            if (withLogin && val("ac-pw").length < PW_TEMP_MIN) {
              show("md-alert", "bad", "초기 비밀번호는 " + PW_TEMP_MIN + "자 이상이어야 합니다."); return;
            }
            if (!withLogin) {
              db.rpc("sl_admin_add", { p_email: email, p_role: role, p_note: note })
                .then(function (r) {
                  if (r.error) {
                    show("md-alert", "bad", r.error.message +
                      " (계정이 없다면 체크를 켜서 함께 생성하거나, Supabase 대시보드에서 먼저 계정을 만드세요.)");
                    return;
                  }
                  closeModal(); loadAcct();
                });
              return;
            }
            /* 로그인 계정까지 생성 — Edge 함수 필요 */
            show("md-alert", "info", "계정을 생성하는 중…");
            db.functions.invoke("sl-admin-user", {
              body: { action: "create", email: email, password: val("ac-pw"), role: role, note: note },
            }).then(function (r) {
              if (r.error) throw r.error;
              /* ⚠ 여기서 closeModal() 을 부르면 임시 비밀번호가 화면에서 사라진다
                 (closeModal 이 모달 본문을 비운다). 한 번만 보여 주는 값이라 그러면
                 담당자에게 전달할 방법이 없어진다 — 재설정 흐름과 같이 열어 둔다. */
              show("md-alert", "ok",
                   "계정을 만들었습니다. 위 임시 비밀번호를 지금 복사해 전달하세요 — " +
                   "창을 닫으면 다시 볼 수 없습니다.");
              loadAcct();   /* 목록은 뒤에서 갱신 */
              /* 같은 계정을 두 번 만들지 않게 [추가] 는 치우고 [닫기] 만 남긴다. */
              var wrap = document.getElementById("modal-actions");
              if (wrap) {
                wrap.innerHTML = "";
                var okBtn = document.createElement("button");
                okBtn.className = "btn btn-sm";
                okBtn.textContent = "복사했습니다 · 닫기";
                okBtn.addEventListener("click", closeModal);
                wrap.appendChild(okBtn);
              }
            }).catch(function (err) {
              fnFail(err, function (m, st) {
                show("md-alert", "bad", notDeployed(m, st)
                  ? "로그인 계정 생성 함수(sl-admin-user)가 배포되지 않았습니다. " +
                    "Supabase 대시보드에서 계정을 먼저 만든 뒤, 체크를 해제해 등록하세요."
                  : "계정 생성 실패: " + m);
              });
            });
          } },
      ]);
    var chk = document.getElementById("ac-login");
    chk.addEventListener("change", function () {
      document.getElementById("ac-pw-wrap").style.display = chk.checked ? "" : "none";
    });
  });

  document.addEventListener("click", function (e) {
    /* [다시 생성] — 어느 모달이든 pwFieldHtml 로 만든 칸이면 이 버튼이 값을 새로 채운다. */
    var rg = e.target.closest("[data-pw-regen]");
    if (rg) {
      var f = document.getElementById(rg.getAttribute("data-pw-regen"));
      if (f) { f.value = tempPassword(); f.focus(); f.select(); }
      return;
    }

    var lk = e.target.closest("[data-acct-link]");
    if (lk) {
      var lem = lk.getAttribute("data-acct-link");
      db.rpc("sl_admin_link", { p_email: lem }).then(function (r) {
        if (r.error) {
          show("acct-alert", "bad", lem + " 연결 실패: " + r.error.message);
          return;
        }
        show("acct-alert", "ok", lem + " 의 로그인 계정을 연결했습니다. 이제 권한이 적용됩니다.");
        loadAcct();
      });
      return;
    }
    var rl = e.target.closest("[data-acct-role]");
    if (rl) {
      var email = rl.getAttribute("data-acct-role");
      var cur = state.cache.acct[email];
      var next = cur.role === "admin" ? "editor" : "admin";
      openModal("역할 변경",
        "<p style='color:var(--ink-2);line-height:1.7'><b>" + esc(email) + "</b> 의 역할을 " +
        "<b>" + esc(cur.role) + "</b> → <b>" + esc(next) + "</b> 로 변경합니다." +
        (next === "admin"
          ? " admin 은 계정 관리와 사이트 설정까지 모두 접근할 수 있습니다."
          : " editor 는 계정 관리·설정에 접근할 수 없습니다.") + "</p>" +
        '<div class="alert" id="md-alert"></div>',
        [{ label: "취소", on: closeModal },
         { label: "변경", cls: "", on: function () {
             db.rpc("sl_admin_set_role", { p_email: email, p_role: next }).then(function (r) {
               if (r.error) { show("md-alert", "bad", r.error.message); return; }
               closeModal(); loadAcct();
             });
           } }]);
      return;
    }
    if (e.target.closest("[data-acct-self-pw]")) { openSelfPasswordModal(); return; }

    var pw = e.target.closest("[data-acct-pw]");
    if (pw) {
      var pem = pw.getAttribute("data-acct-pw");
      var tmp = tempPassword();
      openModal("비밀번호 재설정",
        "<p style='color:var(--ink-2);line-height:1.7'><b>" + esc(pem) + "</b> 의 비밀번호를 " +
        "아래 값으로 바꿉니다. 본인이 쓰던 비밀번호는 즉시 무효가 됩니다.</p>" +
        '<div style="margin-top:14px">' +
        pwFieldHtml("pr-pw", tmp, "새 비밀번호 (직접 정해도 됩니다)",
          PW_TEMP_MIN + "자 이상. 자동값을 그대로 써도 되고 원하는 값으로 바꿔도 됩니다. " +
          "안전한 경로로 전달하고 첫 로그인 후 바꾸도록 안내하세요.") +
        "</div>" +
        '<div class="alert" id="md-alert"></div>',
        [{ label: "취소", on: closeModal },
         { label: "재설정", cls: "", on: function () {
             var np = val("pr-pw");
             if (np.length < PW_TEMP_MIN) {
               show("md-alert", "bad", "새 비밀번호는 " + PW_TEMP_MIN + "자 이상이어야 합니다."); return;
             }
             show("md-alert", "info", "재설정하는 중…");
             /* 값을 화면 밖으로 내보내기 전에 복사해 둘 기회를 준다 — 성공해도 모달은 바로 닫지 않는다. */
             db.functions.invoke("sl-admin-user", {
               body: { action: "set_password", email: pem, password: np },
             }).then(function (r) {
               if (r.error) throw r.error;
               var d = r.data || {};
               if (d.error) throw new Error(d.message || d.error);
               show("md-alert", "ok",
                 "재설정했습니다. 위 값을 지금 복사해 전달하세요 — 창을 닫으면 다시 볼 수 없습니다." +
                 (d.logged === false ? " (감사 로그 기록에는 실패했습니다.)" : ""));
               loadAcct();
             }).catch(function (err) {
               fnFail(err, function (m, st) {
                 show("md-alert", "bad", notDeployed(m, st)
                   ? "비밀번호 재설정 함수(sl-admin-user)가 배포되지 않았습니다. " +
                     "Supabase 대시보드 → Edge Functions 에서 배포한 뒤 다시 시도하세요."
                   : "재설정 실패: " + m);
               });
             });
           } }]);
      return;
    }

    var dl = e.target.closest("[data-acct-del]");
    if (dl) {
      var em = dl.getAttribute("data-acct-del");
      var it = state.cache.acct[em];
      openModal("관리자 삭제",
        "<p style='color:var(--ink-2);line-height:1.7'><b>" + esc(em) + "</b> 를 관리자 목록에서 제거합니다. " +
        "즉시 콘솔 접근이 차단됩니다.</p>" +
        "<p class='tiny' style='margin-top:12px'>" +
        /* sl_admin_list 가 주는 필드는 has_login 이 아니라 linked 다.
           예전 코드가 없는 필드를 봐서 **로그인 계정이 있어도 항상 "없습니다"** 라고 안내했다. */
        (it && it.linked
          ? "Supabase 로그인 계정은 그대로 남습니다. 계정까지 삭제하려면 Supabase 대시보드에서 처리하세요."
          : "이 이메일에는 로그인 계정이 없습니다.") + "</p>" +
        '<div class="alert" id="md-alert"></div>',
        [{ label: "취소", on: closeModal },
         { label: "삭제 확인", cls: "", on: function () {
             db.rpc("sl_admin_remove", { p_email: em }).then(function (r) {
               if (r.error) { show("md-alert", "bad", r.error.message); return; }
               closeModal(); loadAcct();
             });
           } }]);
    }
  });

  /* ═══════════════ 시작 ═══════════════ */
  loginView.style.display = "";
  gate();
})();
