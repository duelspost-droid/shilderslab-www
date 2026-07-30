/**
 * sl-admin-user — 관리자 로그인 계정 생성 · 삭제 (선택 기능)
 *
 * 왜 Edge 함수인가
 *   Auth 계정 생성·삭제는 service_role 키가 필요하다. 그 키는 프런트에 둘 수 없으므로
 *   서버(Edge)에서만 다루고, 호출자가 이 사이트의 admin 인지 DB에 물어서 확인한다.
 *
 * 배포하지 않아도 관리자 콘솔의 계정 관리(화이트리스트 추가·역할변경·삭제)는 동작한다.
 * 이 함수를 배포하면 콘솔에서 **로그인 계정 생성/삭제까지** 한 번에 처리할 수 있다.
 *
 * 배포 (오너 작업 — 크리덴셜이 필요하다)
 *   1) 대시보드 → Edge Functions → Deploy new function → 이름 `sl-admin-user`
 *      → 이 파일 내용을 붙여넣고 Deploy.
 *      ⚠ **Verify JWT 토글은 OFF** — 브라우저 CORS preflight(OPTIONS)에는 JWT가 없어 401이 된다.
 *        대신 이 코드가 호출자 토큰으로 `is_sl_owner()` 를 직접 확인한다.
 *   2) Edge Functions → Secrets 에 등록 (값 입력은 오너가 직접)
 *        SL_SERVICE_ROLE_KEY : Project Settings → API Keys → service_role
 *        (SUPABASE_URL 은 런타임이 자동 주입한다)
 *   3) 검증: 무인증 호출 → 401 / OPTIONS → 200
 *
 * 계약
 *   POST { action: "create", email, password, role?, note? }
 *        → Auth 계정 생성(email_confirm) + sl_admins 화이트리스트 등록
 *   POST { action: "delete_login", email }
 *        → Auth 계정만 삭제(화이트리스트는 콘솔에서 별도 삭제)
 *
 * 안전장치
 *   · 호출자가 admin 역할이 아니면 403.
 *   · 자기 자신의 로그인 계정은 삭제할 수 없다.
 *   · 비밀번호는 로그에 남기지 않는다.
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS, "content-type": "application/json" },
  });
}

async function rpc(url: string, key: string, token: string, fn: string) {
  const r = await fetch(`${url}/rest/v1/rpc/${fn}`, {
    method: "POST",
    headers: {
      apikey: key,
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: "{}",
  });
  if (!r.ok) return null;
  return await r.json();
}

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "method not allowed" }, 405);

  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const anon = Deno.env.get("SUPABASE_ANON_KEY") ?? "";
  const service = Deno.env.get("SL_SERVICE_ROLE_KEY") ?? "";
  if (!url || !service) return json({ error: "server not configured" }, 500);

  // ── 1) 호출자 확인: 토큰으로 is_sl_owner() 를 물어본다(DB가 판정한다)
  const auth = req.headers.get("authorization") ?? "";
  const token = auth.replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "authorization required" }, 401);

  const isOwner = await rpc(url, anon, token, "is_sl_owner");
  if (isOwner !== true) return json({ error: "admin 역할만 사용할 수 있습니다." }, 403);

  const me = await rpc(url, anon, token, "sl_my_email").catch(() => null);

  // ── 2) 입력
  let body: { action?: string; email?: string; password?: string; role?: string; note?: string };
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid json" }, 400);
  }
  const action = String(body.action ?? "");
  const email = String(body.email ?? "").trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email)) return json({ error: "이메일 형식 오류" }, 400);

  const svc = {
    apikey: service,
    authorization: `Bearer ${service}`,
    "content-type": "application/json",
  };

  // ── 3) 계정 생성
  if (action === "create") {
    const password = String(body.password ?? "");
    if (password.length < 12) return json({ error: "임시 비밀번호는 12자 이상이어야 합니다." }, 400);
    const role = body.role === "admin" ? "admin" : "editor";

    const cr = await fetch(`${url}/auth/v1/admin/users`, {
      method: "POST",
      headers: svc,
      body: JSON.stringify({ email, password, email_confirm: true }),
    });
    const created = await cr.json().catch(() => ({}));
    if (!cr.ok) {
      const msg = String(created?.msg ?? created?.error_description ?? created?.message ?? "");
      if (/already|exists|registered/i.test(msg)) {
        // 계정은 이미 있음 → 화이트리스트만 등록하도록 안내
        return json({ ok: false, code: "already_exists", message: "이미 로그인 계정이 존재합니다." }, 409);
      }
      console.error("createUser failed", cr.status, msg);
      return json({ error: "계정 생성 실패", status: cr.status, message: msg }, 400);
    }

    // 화이트리스트 등록 — **호출자 토큰**으로 호출한다.
    // sl_admin_add 는 is_sl_owner() 게이트가 걸려 있어 service_role 로는 통과하지 못한다
    // (service_role JWT 에는 email 클레임이 없다). 감사 로그에도 실제 관리자가 남아야 한다.
    const wl = await fetch(`${url}/rest/v1/rpc/sl_admin_add`, {
      method: "POST",
      headers: { apikey: anon, authorization: `Bearer ${token}`, "content-type": "application/json" },
      body: JSON.stringify({ p_email: email, p_role: role, p_note: String(body.note ?? "") }),
    });
    const wlOk = wl.ok;
    if (!wlOk) console.error("allowlist add failed", wl.status, await wl.text());

    return json({ ok: true, email, role, allowlisted: wlOk, user_id: created?.id ?? null });
  }

  // ── 4) 로그인 계정 삭제
  if (action === "delete_login") {
    if (me && String(me).toLowerCase() === email) {
      return json({ error: "자신의 로그인 계정은 삭제할 수 없습니다." }, 400);
    }
    const lr = await fetch(
      `${url}/auth/v1/admin/users?page=1&per_page=200`,
      { headers: svc },
    );
    const list = await lr.json().catch(() => ({}));
    const found = (list?.users ?? []).find(
      (u: { email?: string }) => (u.email ?? "").toLowerCase() === email,
    );
    if (!found) return json({ ok: false, code: "not_found", message: "로그인 계정이 없습니다." }, 404);

    const dr = await fetch(`${url}/auth/v1/admin/users/${found.id}`, {
      method: "DELETE",
      headers: svc,
    });
    if (!dr.ok) {
      console.error("deleteUser failed", dr.status, await dr.text());
      return json({ error: "계정 삭제 실패" }, 400);
    }
    return json({ ok: true, email, deleted: true });
  }

  return json({ error: "unknown action" }, 400);
});
