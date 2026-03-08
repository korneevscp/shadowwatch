# ╔══════════════════════════════════════════╗
# ║     ShadowWatch — monitor.py             ║
# ║     Surveillance données personnelles    ║
# ╚══════════════════════════════════════════╝

import smtplib, ssl, requests, time, json, os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googlesearch import search
from bs4 import BeautifulSoup

# ══ MODIFIE CES LIGNES ══════════════════════
SMTP_HOST  = "smtp.gmail.com"
SMTP_PORT  = 587
SMTP_USER  = "ton_email@gmail.com"          # ← Ton adresse Gmail (expéditeur)
SMTP_PASS  = "xxxx xxxx xxxx xxxx"          # ← App Password Google (16 caractères)
ALERT_TO   = "destination@email.fr"         # ← Email qui reçoit les alertes

KEYWORDS = [
    "Prénom Nom",                            # ← Ton nom complet
    "ton@email.fr",                          # ← Ton adresse email
    "+33612345678",                          # ← Ton numéro de téléphone
    "ton_pseudo",                            # ← Pseudos, ancienne adresse, etc.
]
# ════════════════════════════════════════════

HEADERS      = {"User-Agent": "Mozilla/5.0"}
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_history.json")

# ══ HISTORIQUE ═══════════════════════════════
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# ══ EMAIL ════════════════════════════════════
def send_email(findings):
    date = datetime.now().strftime("%d/%m/%Y a %H:%M")
    if findings:
        subject = f"[ALERTE] ShadowWatch — {len(findings)} exposition(s) detectee(s)"
        color   = "#ff3b5c"
        icon    = "ALERTE"
        summary = f"{len(findings)} exposition(s) de vos donnees ont ete trouvees sur le web."
        rows = "".join(
            f"<tr>"
            f"<td style='padding:10px 12px;color:#ff3b5c;font-family:monospace;border-bottom:1px solid #1a2332;white-space:nowrap'>{s}</td>"
            f"<td style='padding:10px 12px;color:#c8d8e8;font-family:monospace;border-bottom:1px solid #1a2332;word-break:break-all'>{d}</td>"
            f"</tr>"
            for s, d in findings
        )
        body = f"""<table style="width:100%;border-collapse:collapse;background:#0d1218;margin-top:16px;border-radius:6px;overflow:hidden">
          <tr>
            <th style="padding:10px 12px;color:#00ff88;text-align:left;border-bottom:1px solid #1a2332;font-family:monospace">Source</th>
            <th style="padding:10px 12px;color:#00ff88;text-align:left;border-bottom:1px solid #1a2332;font-family:monospace">Detail</th>
          </tr>
          {rows}
        </table>"""
    else:
        subject = "[OK] ShadowWatch — Scan propre, aucune exposition"
        color   = "#00ff88"
        icon    = "OK"
        summary = "Aucune exposition de vos donnees detectee. Tout est clean."
        body    = """<div style="background:#0d1218;border:1px solid #1a2332;border-radius:6px;
                     padding:28px;text-align:center;margin-top:16px;color:#00ff88;
                     font-family:monospace;font-size:1.1rem">
                     Aucune donnee exposee detectee
                     </div>"""

    html = f"""
    <div style="background:#080c10;padding:32px;font-family:monospace;max-width:700px;margin:0 auto">
      <div style="border-bottom:2px solid {color};padding-bottom:16px;margin-bottom:20px">
        <h2 style="color:{color};margin:0;font-size:1.2rem;letter-spacing:1px">[{icon}] ShadowWatch</h2>
        <p style="color:#4a6070;margin:6px 0 0;font-size:0.78rem">Rapport automatique du {date}</p>
      </div>
      <p style="color:#c8d8e8;margin-bottom:8px;font-size:0.88rem">{summary}</p>
      {body}
      <p style="color:#4a6070;margin-top:24px;font-size:0.7rem;border-top:1px solid #1a2332;padding-top:12px">
        ShadowWatch — surveillance automatique | Sources: Google, Pastebin, BreachDirectory, Ahmia (Tor)
      </p>
    </div>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SMTP_USER
    msg["To"]      = ALERT_TO
    msg.attach(MIMEText(html, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(SMTP_USER, ALERT_TO, msg.as_string())
    print(f"[EMAIL] Envoye : {subject}")

# ══ SOURCES ══════════════════════════════════
def scan_google(keyword):
    found = []
    try:
        for url in search(f'"{keyword}"', num_results=5, sleep_interval=10):
            found.append(("Google", url))
    except Exception as e:
        print(f"Google: {e}")
    return found

def scan_pastebin(keyword):
    found = []
    try:
        for url in search(f'site:pastebin.com "{keyword}"', num_results=3, sleep_interval=10):
            found.append(("Pastebin", url))
    except Exception as e:
        print(f"Pastebin: {e}")
    return found

def scan_breachdirectory(email):
    found = []
    try:
        url = f"https://breachdirectory.org/api?func=auto&term={email}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("success") and data.get("result"):
                for item in data["result"][:5]:
                    src = item.get("sources", ["?"])[0]
                    found.append(("BreachDirectory", f"Fuite: {src}"))
    except Exception as e:
        print(f"BreachDirectory: {e}")
    return found

def scan_ahmia(keyword):
    found = []
    try:
        url = f"https://ahmia.fi/search/?q={requests.utils.quote(keyword)}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for res in soup.select("li.result h4")[:3]:
            found.append(("Ahmia (Tor)", res.text.strip()))
    except Exception as e:
        print(f"Ahmia: {e}")
    return found

# ══ SCAN PRINCIPAL ════════════════════════════
def run_scan():
    print("\n=== ShadowWatch — Demarrage du scan ===\n")
    all_findings = []
    for kw in KEYWORDS:
        print(f"-> Scan: {kw}")
        all_findings += scan_google(kw)
        all_findings += scan_pastebin(kw)
        all_findings += scan_ahmia(kw)
        if "@" in kw:
            all_findings += scan_breachdirectory(kw)
        time.sleep(15)

    history = load_history()
    history.insert(0, {
        "date":      datetime.now().strftime("%d/%m/%Y %H:%M"),
        "timestamp": time.time(),
        "total":     len(all_findings),
        "findings":  [{"source": s, "detail": d} for s, d in all_findings]
    })
    save_history(history[:50])

    send_email(all_findings)

    if all_findings:
        print(f"[ALERTE] {len(all_findings)} exposition(s) detectee(s)")
    else:
        print("[OK] Aucune exposition detectee")
    print("=== Scan termine ===\n")

if __name__ == "__main__":
    run_scan()
