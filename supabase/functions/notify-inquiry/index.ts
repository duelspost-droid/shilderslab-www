/**
 * notify-inquiry — 새 문의 · 지원서 접수 시 담당자에게 이메일 알림 (선택 기능)
 *
 * 이 함수는 사이트 동작에 필수가 아니다. 배포하지 않아도 문의 접수·관리자 콘솔은 정상 동작하며,
 * 배포하면 접수 즉시 알림을 받아 24시간 회신 약속을 지키기 쉬워진다.
 *
 * 연결 방법 (오너 작업 — 크리덴셜이 필요하므로)
 *   1) Supabase 대시보드 → Edge Functions → Deploy new function → 이름 `notify-inquiry`
 *      → 이 파일 내용을 붙여넣고 Deploy.  (Verify JWT: OFF — DB 웹훅은 JWT를 보내지 않는다.
 *        대신 아래 WEBHOOK_SECRET 로 호출자를 검증한다.)
 *   2) Edge Functions → Secrets 에 등록
 *        RESEND_API_KEY   : https://resend.com 에서 발급 (무료 티어로 충분)
 *        NOTIFY_TO        : 알림 받을 주소 (예: contact@shielduslab.com)
 *        NOTIFY_FROM      : Resend 에서 인증한 발신 도메인 주소 (예: no-reply@shielduslab.com)
 *        WEBHOOK_SECRET   : 임의의 긴 랜덤 문자열
 *   3) Database → Webhooks → Create a new hook
 *        table: sl_inquiries (INSERT)  ·  type: Supabase Edge Functions  ·  function: notify-inquiry
 *        HTTP Headers 에  x-webhook-secret: <위에서 정한 WEBHOOK_SECRET>  추가
 *        (sl_applications 용으로 동일하게 하나 더 만들면 지원서 알림도 받는다)
 *
 * 보안 메모
 *   · 본문에는 담당자 이름·회사·문의 유형만 담고, 문의 내용 전문은 넣지 않는다(메일 계정 유출 시 피해 축소).
 *     상세 내용은 관리자 콘솔에서 확인한다.
 *   · 시크릿이 설정되지 않았거나 헤더가 틀리면 202로 조용히 무시한다(정보 노출 방지).
 */

const TABLE_LABEL: Record<string, string> = {
  sl_inquiries: "문의 · 견적 요청",
  sl_applications: "채용 지원",
};

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });

  const secret = Deno.env.get("WEBHOOK_SECRET") ?? "";
  const got = req.headers.get("x-webhook-secret") ?? "";
  if (!secret || got !== secret) {
    // 호출자를 검증할 수 없으면 아무 것도 하지 않는다(200 대신 202로 응답만).
    return new Response("ignored", { status: 202 });
  }

  const apiKey = Deno.env.get("RESEND_API_KEY");
  const to = Deno.env.get("NOTIFY_TO");
  const from = Deno.env.get("NOTIFY_FROM");
  if (!apiKey || !to || !from) {
    return new Response(JSON.stringify({ ok: false, reason: "secrets not configured" }), {
      status: 200, headers: { "content-type": "application/json" },
    });
  }

  let payload: { table?: string; type?: string; record?: Record<string, unknown> };
  try {
    payload = await req.json();
  } catch {
    return new Response("bad request", { status: 400 });
  }

  const table = String(payload.table ?? "");
  const rec = payload.record ?? {};
  const label = TABLE_LABEL[table];
  if (!label || payload.type !== "INSERT") {
    return new Response("ignored", { status: 202 });
  }

  const who = String(rec.name ?? "-");
  const org = String(rec.company ?? rec.position ?? "-");
  const kind = String(rec.service ?? rec.position ?? "-");
  const at = String(rec.created_at ?? new Date().toISOString());

  const subject = `[쉴더스랩] 새 ${label} 접수 — ${org}`;
  const text = [
    `새 ${label}가 접수되었습니다.`,
    "",
    `· 이름 : ${who}`,
    `· 소속/포지션 : ${org}`,
    `· 구분 : ${kind}`,
    `· 접수 시각 : ${at}`,
    "",
    "상세 내용과 처리 상태 변경은 관리자 콘솔에서 확인하세요:",
    "https://shielduslab.com/admin/",
  ].join("\n");

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}` },
    body: JSON.stringify({ from, to: [to], subject, text }),
  });

  if (!res.ok) {
    console.error("resend failed", res.status, await res.text());
    return new Response(JSON.stringify({ ok: false, status: res.status }), {
      status: 200, headers: { "content-type": "application/json" },
    });
  }
  return new Response(JSON.stringify({ ok: true }), {
    status: 200, headers: { "content-type": "application/json" },
  });
});
