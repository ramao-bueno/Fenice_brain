import os, sys, json, base64, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent  # C:\Fenice_bRain


def _env():
    e = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip()
    return e


CAPTION = ("👤 *Teo — Intelligence Concierge*\n\n"
           "Escolha uma opção — digite o número (0–6). Para sair, digite *sair*.\n\n"
           "© 2026 Fenice IT Justech.IA\nby Tech Lead Ramão Bueno")


def main(numero="5547991041414"):
    e = _env()
    url = e["EVOLUTION_API_URL"].rstrip("/")
    apikey = e["EVOLUTION_API_KEY"]
    inst = e["EVOLUTION_INSTANCE"]
    b64 = base64.b64encode((BASE / "card.png").read_bytes()).decode()
    payload = {"number": numero, "mediatype": "image", "media": b64,
               "fileName": "modal_teo.png", "caption": CAPTION}
    req = urllib.request.Request(
        f"{url}/message/sendMedia/{inst}",
        data=json.dumps(payload).encode(),
        headers={"apikey": apikey, "Content-Type": "application/json"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=45)
        res = json.load(r)
        print("[ENVIO] HTTP", r.status, "| id=", (res.get("key") or {}).get("id"), "| status=", res.get("status"))
    except urllib.error.HTTPError as ex:
        print("[ENVIO] ERRO", ex.code, ex.read().decode()[:400])
        sys.exit(1)


if __name__ == "__main__":
    main(*sys.argv[1:])
