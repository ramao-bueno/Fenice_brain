import os, sys, json, datetime, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")


def _env():
    e = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip()
    return e


def call(url, key, method="GET", payload=None):
    H = {"X-N8N-API-KEY": key, "Accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(payload, ensure_ascii=False).encode() if payload is not None else None
    r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=H, method=method), timeout=60)
    return r.status, json.load(r)


def main():
    e = _env(); wid = e["N8N_WORKFLOW_ID"]; key = e["N8N_API_KEY"]
    base = f"https://feniceit.app.n8n.cloud/api/v1/workflows/{wid}"
    st, live = call(base, key)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bkp = ROOT / f"scripts/_backup_n8n_v4_LIVE_{ts}.json"
    bkp.write_text(json.dumps(live, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[backup]", bkp.name, len(live.get("nodes", [])), "nós")
    g = json.loads((ROOT / "scripts/n8n_fenice_tim_v4.json").read_text(encoding="utf-8"))
    payload = {"name": g["name"], "nodes": g["nodes"], "connections": g["connections"],
               "settings": {"executionOrder": "v1", "saveManualExecutions": True}}
    st, res = call(base, key, "PUT", payload)
    print("[PUT]", st, len(res.get("nodes", [])), "nós, active=", res.get("active"))
    if not res.get("active"):
        call(base + "/activate", key, "POST", {}); print("[activate] ok")
    st, chk = call(base, key)
    imgs = [n["name"] for n in chk["nodes"] if n["name"].startswith("9a-img")]
    logo = any(n["name"] == "9-logo. Enviar Logo Fenice" for n in chk["nodes"])
    media = any("sendMedia" in json.dumps(n) for n in chk["nodes"] if n["name"].startswith("9a. Enviar Menu"))
    print(f"[verify] {len(chk['nodes'])} nós | 9a-img={imgs} | 9-logo={logo} | 9a=sendMedia:{media} | active={chk.get('active')}")


if __name__ == "__main__":
    main()
