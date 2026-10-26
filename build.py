#!/usr/bin/env python3
"""Generate worker.js: a binding-free Cloudflare Worker serving index.html."""
import json, pathlib
here = pathlib.Path(__file__).parent
html = (here / "index.html").read_text(encoding="utf-8")
worker = (
    "export default {\n"
    "  async fetch(request) {\n"
    "    const url = new URL(request.url);\n"
    "    if (url.pathname !== '/' && url.pathname !== '/index.html') {\n"
    "      return new Response('Not found', { status: 404 });\n"
    "    }\n"
    f"    return new Response({json.dumps(html)}, {{\n"
    "      headers: { 'content-type': 'text/html;charset=utf-8', 'cache-control': 'no-cache' },\n"
    "    });\n"
    "  },\n"
    "};\n"
)
(here / "worker.js").write_text(worker, encoding="utf-8")
print(f"worker.js written ({len(worker)} bytes) from index.html ({len(html)} bytes)")
