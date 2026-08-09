/**
 * sl-admin-user — 관리자 로그인 계정 생성 · 삭제 (선택 기능)
 *
 * 왜 Edge 함수인가
 *   Auth 계정 생성·삭제는 service_role 키가 필요하다. 그 키는 프런트에 둘 수 없으므로
 *   서버에서만 다루고, **권한 판정과 대상 검증은 전부 DB(RPC)에 맡긴다.**
 *   이 함수는 스스로 판단하지 않는다 — DB 가 허용한 것만 실행한다.
 *
 * 배포하지 않아도 관리자 콘솔의 계정 관리(등록·연결·역할변경·삭제)는 동작한다.
 * 배포하면 콘솔에서 **로그인 계정 생성/삭제까지** 처리할 수 있다.
 *
 * 배포 (오너 작업 — 크리덴셜 필요)
 *   1) 대시보드 → Edge Functions → Deploy new function → 이름 `sl-admin-user`
 *      → 이 파일 내용을 붙여넣고 Deploy.
 *      ⚠ **Verify JWT 토글 OFF** — 브라우저 CORS preflight(OPTIONS)에는 JWT 가 없어 401 이 된다.
 *        대신 이 코드가 호출자 토큰으로 `is_sl_owner()` 를 확인한다.
 *   2) Secret 입력은 **필요 없다.** SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY
 *      셋 다 런타임이 자동 주입한다. (다른 키를 쓰고 싶을 때만 SL_SERVICE_ROLE_KEY 를 넣으면 우선한다.)
 *   3) 검증: 무인증 POST → 401 · OPTIONS → 200 · 비-admin 토큰 → 403
 *
 * 계약
 *   POST { action: "create", email, password, role?, note? }
 *        → Auth 계정 생성(email_confirm) → sl_admin_add 로 화이트리스트 등록
 *          화이트리스트 등록이 실패하면 **생성한 계정을 되돌린다**(고아 계정 방지)
 *   POST { action: "set_password", email, password }
 *        → sl_admin_pw_uid(email) 로 DB 가 대상 uid 를 판정한 경우에만 비밀번호 교체
 *          (목록 밖 계정 · 로그인 없는 슬롯 · 자기 계정은 DB 가 거부)
 *          교체 성공 후 sl_admin_pw_logged 로 감사 로그를 남긴다
 *   POST { action: "delete_login", email }
 *        → sl_admin_login_uid(email) 로 DB 가 대상 uid 를 판정한 경우에만 삭제
 *          (우리 화이트리스트에 없는 계정, 자기 계정, 마지막 admin 은 DB 가 거부)
 *
 * 로그 정책: 응답 본문을 로그에 남기지 않는다(공유 프로젝트의 Edge 로그 열람 범위 때문).
 *           상태 코드와 짧은 코드만 남긴다.
 */

// ⚠ 이 값은 **관리자 콘솔이 실제로 서비스되는 출처**와 같아야 한다.
//   도메인 전환 전에 배포하면 안 된다 — 지금 사이트는 shilderslab.com 에서 돌고 있어
//   여기(shilderslab.com)와 어긋나면 브라우저가 응답을 차단한다.
//   `tools/set-domain.py` 가 이 문자열도 함께 갱신하므로, 전환 후 배포하면 맞아떨어진다.
const CORS = {
  "Access-Control-Allow-Origin": "https://shilderslab.com",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Vary": "Origin",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS, "content-type": "application/json" },
  });
}

type RpcResult =
  | { ok: true; value: unknown }
  | { ok: false; status: number; message?: string };

/** 호출자 토큰으로 RPC 호출. 실패와 false 를 구분한다(fail-closed 를 위해 필수).
 *
 *  실패하면 PostgREST 가 준 **한국어 사유**(RPC 의 raise exception 메시지)를 함께 돌려준다.
 *  이걸 버리면 "이 사이트가 만든 계정이 아닙니다" 같은 판정 사유가 화면에 닿지 못하고
 *  관리자는 영문 상태코드만 보게 된다 — 왜 막혔는지 알 수 없다. */
async function rpc(
  url: string, anon: string, token: string, fn: string, args: unknown = {},
): Promise<RpcResult> {
  const r = await fetch(`${url}/rest/v1/rpc/${fn}`, {
    method: "POST",
    headers: { apikey: anon, authorization: `Bearer ${token}`, "content-type": "application/json" },
    body: JSON.stringify(args),
  });
  if (!r.ok) {
    let message: string | undefined;
    try {
      const e = JSON.parse(await r.text());
      message = typeof e?.message === "string" ? e.message : undefined;
    } catch { /* 본문이 없거나 JSON 이 아니면 상태코드만 쓴다 */ }
    return { ok: false, status: r.status, message };
  }
  const text = await r.text();
  try {
    return { ok: true, value: text === "" ? null : JSON.parse(text) };
  } catch {
    return { ok: true, value: text };
  }
}

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "method not allowed" }, 405);

  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const anon = Deno.env.get("SUPABASE_ANON_KEY") ?? "";
  // SUPABASE_SERVICE_ROLE_KEY 는 Supabase 가 Edge 런타임에 자동 주입한다.
  // 즉 **오너가 키를 복사해 넣지 않아도 배포만 하면 동작한다** — 크리덴셜을 손으로 옮길 일이 없다.
  // SL_SERVICE_ROLE_KEY 는 굳이 다른 키를 쓰고 싶을 때만 넣는 선택지로 남긴다(있으면 우선).
  const service = Deno.env.get("SL_SERVICE_ROLE_KEY") ||
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  if (!url || !anon || !service) {
    console.error("config missing", { url: !!url, anon: !!anon, service: !!service });
    return json({ error: "server_not_configured" }, 500);
  }

  const token = (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "authorization_required" }, 401);

  // ── 권한: DB 가 판정한다. 조회 실패는 실패로 처리(fail-closed).
  const owner = await rpc(url, anon, token, "is_sl_owner");
  if (!owner.ok) {
    console.error("is_sl_owner failed", owner.status);
    return json({ error: "auth_check_failed", status: owner.status }, 503);
  }
  if (owner.value !== true) return json({ error: "admin_role_required" }, 403);

  let body: { action?: string; email?: string; password?: string; role?: string; note?: string };
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  const action = String(body.action ?? "");
  const email = String(body.email ?? "").trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email)) return json({ error: "invalid_email" }, 400);

  const svc = {
    apikey: service,
    authorization: `Bearer ${service}`,
    "content-type": "application/json",
  };

  // ══════════════ 계정 생성 ══════════════
  if (action === "create") {
    const password = String(body.password ?? "");
    if (password.length < 12) return json({ error: "weak_password" }, 400);
    const role = body.role === "admin" ? "admin" : "editor";

    const cr = await fetch(`${url}/auth/v1/admin/users`, {
      method: "POST",
      headers: svc,
      body: JSON.stringify({ email, password, email_confirm: true }),
    });
    if (!cr.ok) {
      const t = await cr.text();
      const exists = /already|exists|registered|duplicate/i.test(t);
      console.error("createUser failed", cr.status, exists ? "already_exists" : "other");
      return json(
        exists
          ? { error: "already_exists", message: "이미 로그인 계정이 존재합니다. 목록에서 ‘연결’을 사용하세요." }
          : { error: "create_failed", status: cr.status },
        exists ? 409 : 400,
      );
    }
    const created = await cr.json().catch(() => ({} as { id?: string }));
    const newId = created?.id as string | undefined;

    // 화이트리스트 등록은 **호출자 토큰**으로. sl_admin_add 는 is_sl_owner 게이트가 걸려 있어
    // service_role 로는 통과하지 못하고(email 클레임 없음), 감사 로그에도 실제 관리자가 남아야 한다.
    const add = await rpc(url, anon, token, "sl_admin_add", {
      p_email: email, p_role: role, p_note: String(body.note ?? ""),
    });

    if (!add.ok) {
      // 되돌린다 — 확인된 고아 계정을 공유 프로젝트에 남기지 않는다.
      let rolledBack = false;
      if (newId) {
        const del = await fetch(`${url}/auth/v1/admin/users/${newId}`, { method: "DELETE", headers: svc });
        rolledBack = del.ok;
      }
      console.error("allowlist add failed", add.status, "rolledBack:", rolledBack);
      return json({
        error: "allowlist_failed",
        status: add.status,
        rolled_back: rolledBack,
        message: rolledBack
          ? "화이트리스트 등록에 실패해 생성한 계정을 되돌렸습니다. 다시 시도해 주세요."
          : "화이트리스트 등록에 실패했고 계정 정리도 실패했습니다. Supabase 대시보드에서 확인이 필요합니다.",
      }, 500);
    }

    // 이 계정은 **우리가 방금 만들었다** — 나중에 콘솔에서 비밀번호를 재설정할 수 있는 유일한 조건이다.
    // ⚠ 이 표시(pw_managed)는 **service_role 로만, 방금 생성한 uid(newId)에 한해** 켠다.
    //   예전엔 sl_admin_mark_pw_managed 를 호출자(오너) 토큰으로 켰는데, 그 RPC 가
    //   authenticated 에 열려 있어 오너가 **남의 기존 계정을 sl_admin_add 로 끌어온 뒤** 켤 수 있었다
    //   → 공유 프로젝트의 타 서비스 계정 탈취 경로(모의해킹 확증, 0007 에서 그 RPC 제거).
    //   여기서는 user_id=newId 로 매칭하므로, 방금 만든 계정 외에는 절대 켤 수 없다.
    let pwManaged = false;
    if (newId) {
      const mk = await fetch(
        `${url}/rest/v1/sl_admins?user_id=eq.${newId}`,
        { method: "PATCH", headers: { ...svc, Prefer: "return=minimal" },
          body: JSON.stringify({ pw_managed: true }) });
      pwManaged = mk.ok;
      if (!mk.ok) console.error("pw_managed set failed", mk.status);
    }

    return json({ ok: true, email, role, pw_managed: pwManaged });
  }

  // ══════════════ 비밀번호 재설정 ══════════════
  // 담당자가 비밀번호를 잊었을 때 admin 이 임시 비밀번호를 발급한다.
  // 대상 판정은 DB(sl_admin_pw_uid)가 한다 — 화이트리스트 밖 계정, 로그인 없는 슬롯,
  // 자기 계정은 거기서 걸러진다. 여기서는 DB 가 uid 를 돌려준 경우에만 움직인다.
  if (action === "set_password") {
    const password = String(body.password ?? "");
    if (password.length < 12) return json({ error: "weak_password" }, 400);

    const target = await rpc(url, anon, token, "sl_admin_pw_uid", { p_email: email });
    if (!target.ok) {
      console.error("pw_uid check failed", target.status);
      // DB 가 한국어로 사유를 말해 준다(자기 계정 · 로그인 없음 · 우리가 만든 계정 아님).
      return json({
        error: "target_check_failed",
        status: target.status,
        message: target.message ?? "대상 계정을 확인하지 못했습니다.",
      }, 400);
    }
    const uid = target.value;
    if (!uid || typeof uid !== "string") {
      return json({
        error: "not_resettable",
        message: "이 사이트의 관리자 목록에 있는 계정이 아닙니다. 다른 계정의 비밀번호는 바꾸지 않습니다.",
      }, 404);
    }

    const pr = await fetch(`${url}/auth/v1/admin/users/${uid}`, {
      method: "PUT",
      headers: svc,
      body: JSON.stringify({ password }),
    });
    if (!pr.ok) {
      // 본문에 비밀번호가 섞일 수 있으므로 로그에는 상태 코드만 남긴다.
      console.error("setPassword failed", pr.status);
      return json({ error: "set_password_failed", status: pr.status }, 400);
    }

    // 실제로 바뀐 뒤에만 기록한다. 실패해도 재설정 자체는 이미 끝났으므로 성공으로 응답한다.
    const lg = await rpc(url, anon, token, "sl_admin_pw_logged", { p_email: email });
    if (!lg.ok) console.error("pw audit log failed", lg.status);

    return json({ ok: true, email, logged: lg.ok });
  }

  // ══════════════ 로그인 계정 삭제 ══════════════
  if (action === "delete_login") {
    // 대상 판정은 DB 가 한다: 화이트리스트 소속 · 자기 계정 아님 · 마지막 admin 아님
    const target = await rpc(url, anon, token, "sl_admin_login_uid", { p_email: email });
    if (!target.ok) {
      console.error("login_uid check failed", target.status);
      return json({ error: "target_check_failed", status: target.status }, 400);
    }
    const uid = target.value;
    if (!uid || typeof uid !== "string") {
      return json({
        error: "not_deletable",
        message: "이 사이트의 관리자 목록에 연결된 로그인 계정이 아닙니다. 공유 프로젝트의 다른 계정은 삭제하지 않습니다.",
      }, 404);
    }

    const dr = await fetch(`${url}/auth/v1/admin/users/${uid}`, { method: "DELETE", headers: svc });
    if (!dr.ok) {
      console.error("deleteUser failed", dr.status);
      return json({ error: "delete_failed", status: dr.status }, 400);
    }
    return json({ ok: true, email, deleted: true });
  }

  return json({ error: "unknown_action" }, 400);
});
