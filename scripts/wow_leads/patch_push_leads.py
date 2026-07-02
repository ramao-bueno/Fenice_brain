"""Finaliza o WOW: preenche o client_secret real no nó de token Azure e
ajusta o sender do e-mail Graph para o endereço validado (202).

- Lê segredos do .env (NUNCA imprime o secret).
- Faz backup do workflow live antes do PUT.
- Idempotente: seguro re-executar.
"""
import json, datetime, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")
WID = "wNBR7zxLTmg7gzaq"
BASE = f"https://feniceit.app.n8n.cloud/api/v1/workflows/{WID}"

TOKEN_NODE = "5b-token. Obter Token Azure"
MAIL_NODE = "5b. E-mail Prospect (Graph API)"
ADMIN_NODE = "5a. WhatsApp Admin"
LEAD_NODE = "5c. WhatsApp Proativo Lead (WOW)"
SENDER = "fenice_tech@fenice.ia.br"
PLACEHOLDER = "AZURE_CLIENT_SECRET_CONFIGURED_IN_N8N"
BAD_INSTANCE = "/fenice-tim"
GOOD_INSTANCE = "/fenice-tim-prod"
ADMIN_OLD = "5521967531414"
ADMIN_NEW = "5547991041414"  # mesmo número que o IVR usa p/ notificar Ramão


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


def _bp(node, name):
    for p in node["parameters"].get("bodyParameters", {}).get("parameters", []):
        if p["name"] == name:
            return p
    return None


def main():
    e = _env()
    key = e["N8N_API_KEY"]
    secret = e["AZURE_CLIENT_SECRET"]

    st, live = call(BASE, key)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bkp = ROOT / f"scripts/_backup_leads_LIVE_{ts}.json"
    bkp.write_text(json.dumps(live, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[backup]", bkp.name, len(live.get("nodes", [])), "nós")

    N = {n["name"]: n for n in live["nodes"]}

    # 1) client_secret real no nó de token
    cs = _bp(N[TOKEN_NODE], "client_secret")
    before = "placeholder" if cs["value"] == PLACEHOLDER else "já configurado"
    cs["value"] = secret
    print(f"[token] client_secret: {before} -> real ({len(secret)} chars)")

    # 2) sender validado no nó de e-mail
    murl = N[MAIL_NODE]["parameters"]
    old = murl["url"]
    murl["url"] = f"https://graph.microsoft.com/v1.0/users/{SENDER}/sendMail"
    print(f"[mail] sender: {old.split('/users/')[-1].split('/sendMail')[0]} -> {SENDER}")

    # 3) instância Evolution correta em 5a e 5c
    for nm in (ADMIN_NODE, LEAD_NODE):
        u = N[nm]["parameters"]["url"]
        if u.endswith(BAD_INSTANCE):
            N[nm]["parameters"]["url"] = u[: -len(BAD_INSTANCE)] + GOOD_INSTANCE
            print(f"[{nm[:3]}] instância: fenice-tim -> fenice-tim-prod")
        else:
            print(f"[{nm[:3]}] instância já ok ({u.rsplit('/',1)[-1]})")

    # 3b) 5a: número admin alinhado ao corporativo (mesmo do IVR)
    num = _bp(N[ADMIN_NODE], "number")
    if num["value"] == ADMIN_OLD:
        num["value"] = ADMIN_NEW
        print(f"[5a] número admin: {ADMIN_OLD} -> {ADMIN_NEW}")
    else:
        print(f"[5a] número admin já ok ({num['value']})")

    # 4) 5c: quebras de linha reais dentro da string JS -> escape \n (senão 'invalid syntax')
    tp = _bp(N[LEAD_NODE], "text")
    if "\n" in tp["value"]:
        n_nl = tp["value"].count("\n")
        tp["value"] = tp["value"].replace("\n", "\\n")
        print(f"[5c] texto: {n_nl} newline(s) cru(s) -> escapado(s) \\n")
    else:
        print("[5c] texto já sem newline cru")

    payload = {"name": live["name"], "nodes": live["nodes"], "connections": live["connections"],
               "settings": {"executionOrder": "v1", "saveManualExecutions": True}}
    st, res = call(BASE, key, "PUT", payload)
    print("[PUT]", st, len(res.get("nodes", [])), "nós, active=", res.get("active"))
    if not res.get("active"):
        call(BASE + "/activate", key, "POST", {})
        print("[activate] ok")

    # verify
    st, chk = call(BASE, key)
    C = {n["name"]: n for n in chk["nodes"]}
    csv = _bp(C[TOKEN_NODE], "client_secret")["value"]
    ok_secret = csv != PLACEHOLDER and len(csv) > 10
    ok_sender = SENDER in C[MAIL_NODE]["parameters"]["url"]
    ok_inst = all(C[nm]["parameters"]["url"].endswith(GOOD_INSTANCE) for nm in (ADMIN_NODE, LEAD_NODE))
    ok_5c = "\n" not in _bp(C[LEAD_NODE], "text")["value"]
    ok_admin = _bp(C[ADMIN_NODE], "number")["value"] == ADMIN_NEW
    print(f"[verify] secret_ok={ok_secret} | sender_ok={ok_sender} | instancia_ok={ok_inst} | 5c_ok={ok_5c} | admin_ok={ok_admin} | active={chk.get('active')}")


if __name__ == "__main__":
    main()
