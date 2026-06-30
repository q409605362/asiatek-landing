export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type, Authorization" }});
    }
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === "/" || path === "/health") {
      return new Response(JSON.stringify({ service: "Asiatek AI API Gateway", status: "running", version: "2.0-cloudflare", endpoints: ["/qwen/v1/chat/completions", "/deepseek/v1/chat/completions"] }), { headers: { "Content-Type": "application/json" }});
    }
    const routes = {
      "/qwen/v1/chat/completions": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
      "/deepseek/v1/chat/completions": "https://api.deepseek.com/v1/chat/completions"
    };
    const upstream = routes[path];
    if (!upstream) {
      return new Response(JSON.stringify({ error: "Not Found", path }), { status: 404 });
    }
    const auth = request.headers.get("Authorization");
    if (!auth) {
      return new Response(JSON.stringify({ error: "Missing Authorization header" }), { status: 401 });
    }
    let key = path.startsWith("/qwen") ? env.DASHSCOPE_API_KEY : env.DEEPSEEK_API_KEY;
    if (!key) {
      return new Response(JSON.stringify({ error: "API Key not configured" }), { status: 500 });
    }
    const headers = new Headers(request.headers);
    headers.set("Authorization", "Bearer " + key);
    headers.set("Host", new URL(upstream).hostname);
    try {
      const res = await fetch(upstream, { method: request.method, headers, body: request.method !== "GET" ? request.body : undefined });
      const resHeaders = new Headers(res.headers);
      resHeaders.set("Access-Control-Allow-Origin", "*");
      return new Response(res.body, { status: res.status, headers: resHeaders });
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { status: 502 });
    }
  }
};
