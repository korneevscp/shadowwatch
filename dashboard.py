# ╔══════════════════════════════════════════╗
# ║     ShadowWatch — dashboard.py           ║
# ║     Interface web locale                 ║
# ╚══════════════════════════════════════════╝

import json, os, subprocess, sys, threading, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_history.json")
PORT = 8080

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def run_scan_async():
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor.py")
    subprocess.Popen([sys.executable, script],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)

def build_html():
    history = load_history()
    total_scans  = len(history)
    total_found  = sum(s["total"] for s in history)
    last_scan    = history[0]["date"] if history else "Jamais"
    danger_scans = sum(1 for s in history if s["total"] > 0)

    rows = ""
    for scan in history:
        cls   = "danger" if scan["total"] > 0 else "ok"
        label = f"{scan['total']} alerte(s)" if scan["total"] > 0 else "Clean"
        details = ""
        if scan["findings"]:
            details = "<div class='findings'>" + "".join(
                f"<div class='finding'><span class='src'>{f['source']}</span>"
                f"<span class='det'>{f['detail']}</span></div>"
                for f in scan["findings"]
            ) + "</div>"
        rows += f"""
        <div class="entry {cls}">
          <div class="entry-header" onclick="toggle(this)">
            <span class="entry-date">{scan['date']}</span>
            <span class="badge {cls}">{label}</span>
            <span class="arrow">▼</span>
          </div>
          {details}
        </div>"""

    if not rows:
        rows = "<div class='empty'>Aucun scan effectue. Clique sur LANCER UN SCAN pour commencer.</div>"

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="30">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ShadowWatch</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:#080c10; --panel:#0d1218; --border:#1a2332;
  --green:#00ff88; --blue:#00cfff; --red:#ff3b5c;
  --text:#c8d8e8; --muted:#4a6070;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Space Mono',monospace;min-height:100vh;padding:32px 20px}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(0,255,136,.025) 1px,transparent 1px),
  linear-gradient(90deg,rgba(0,255,136,.025) 1px,transparent 1px);
  background-size:40px 40px}}
.wrap{{max-width:860px;margin:0 auto;position:relative;z-index:1}}

header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:32px;flex-wrap:wrap;gap:12px}}
.logo h1{{font-family:'Syne',sans-serif;font-size:1.7rem;color:#fff}}
.logo p{{font-size:.62rem;color:var(--green);letter-spacing:3px;margin-top:3px}}
.live{{display:flex;align-items:center;gap:8px;font-size:.65rem;color:var(--green);
  border:1px solid var(--green);padding:6px 14px;border-radius:20px}}
.dot{{width:7px;height:7px;border-radius:50%;background:var(--green);animation:blink 1.5s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}

.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px}}
.stat{{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:18px;text-align:center}}
.stat-val{{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:var(--green)}}
.stat-val.red{{color:var(--red)}}
.stat-val.sm{{font-size:.9rem;margin-top:6px}}
.stat-label{{font-size:.58rem;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-top:5px}}

.toolbar{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}}
.section-title{{font-size:.78rem;color:var(--green);letter-spacing:2px;text-transform:uppercase}}
.btn{{background:var(--green);color:#000;font-family:'Space Mono',monospace;font-size:.72rem;
  font-weight:700;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;
  letter-spacing:1px;text-decoration:none;transition:all .2s;display:inline-block}}
.btn:hover{{background:#00cc6e;box-shadow:0 0 20px rgba(0,255,136,.3)}}

.entry{{background:var(--panel);border:1px solid var(--border);border-radius:8px;margin-bottom:8px;overflow:hidden}}
.entry.danger{{border-color:rgba(255,59,92,.35)}}
.entry.ok{{border-color:rgba(0,255,136,.15)}}
.entry-header{{display:flex;align-items:center;gap:14px;padding:14px 18px;cursor:pointer}}
.entry-header:hover{{background:rgba(255,255,255,.02)}}
.entry-date{{flex:1;font-size:.8rem}}
.badge{{font-size:.62rem;letter-spacing:1px;padding:3px 10px;border-radius:12px}}
.badge.danger{{background:rgba(255,59,92,.1);color:var(--red);border:1px solid rgba(255,59,92,.3)}}
.badge.ok{{background:rgba(0,255,136,.08);color:var(--green);border:1px solid rgba(0,255,136,.2)}}
.arrow{{color:var(--muted);font-size:.65rem;transition:transform .2s}}
.entry.open .arrow{{transform:rotate(180deg)}}

.findings{{display:none;border-top:1px solid var(--border);padding:10px 18px}}
.entry.open .findings{{display:block}}
.finding{{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid var(--border);font-size:.73rem}}
.finding:last-child{{border-bottom:none}}
.src{{color:var(--red);min-width:130px;flex-shrink:0}}
.det{{color:var(--muted);word-break:break-all}}

.empty{{color:var(--muted);text-align:center;padding:40px;font-size:.82rem}}
.note{{font-size:.62rem;color:var(--muted);text-align:center;margin-top:20px}}
@media(max-width:600px){{.stats{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">
      <h1>👁 ShadowWatch</h1>
      <p>DASHBOARD — localhost:{PORT}</p>
    </div>
    <div class="live"><div class="dot"></div>EN LIGNE</div>
  </header>

  <div class="stats">
    <div class="stat">
      <div class="stat-val {'red' if total_found > 0 else ''}">{total_found}</div>
      <div class="stat-label">Expositions totales</div>
    </div>
    <div class="stat">
      <div class="stat-val">{total_scans}</div>
      <div class="stat-label">Scans effectues</div>
    </div>
    <div class="stat">
      <div class="stat-val {'red' if danger_scans > 0 else ''}">{danger_scans}</div>
      <div class="stat-label">Scans avec alertes</div>
    </div>
    <div class="stat">
      <div class="stat-val sm">{last_scan}</div>
      <div class="stat-label">Dernier scan</div>
    </div>
  </div>

  <div class="toolbar">
    <div class="section-title">Historique des scans</div>
    <a href="/scan" class="btn">▶ LANCER UN SCAN</a>
  </div>

  {rows}

  <div class="note">Page actualisee automatiquement toutes les 30 secondes</div>
</div>
<script>
function toggle(el) {{
  el.parentElement.classList.toggle('open');
}}
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/scan":
            run_scan_async()
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            html = build_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(html))
            self.end_headers()
            self.wfile.write(html)


if __name__ == "__main__":
    print("\n=== ShadowWatch Dashboard ===")
    print(f"Ouvre : http://localhost:{PORT}")
    print("Ctrl+C pour arreter\n")
    threading.Timer(1.2, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    server = HTTPServer(("localhost", PORT), Handler)
    server.serve_forever()
