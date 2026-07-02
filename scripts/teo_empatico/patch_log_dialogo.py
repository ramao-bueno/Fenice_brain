"""Task 6 — captura de diálogos no IVR.

Adiciona 2 nós de log (clonados do 15a, que já traz url-base + service key):
  - "Log Diálogo (in)"  — ramo paralelo do nó 7 (toda mensagem do usuário)
  - "Log Diálogo (out)" — ramo paralelo do nó 13 (resposta do Téo via Gemini)

Ambos continueOnFail (logar NUNCA quebra/atrasa o atendimento) e são dead-ends
(não alimentam nada downstream → não interferem no fluxo).

Uso:
  python patch_log_dialogo.py --dry-run
  python patch_log_dialogo.py
"""
import copy, json, sys, uuid, datetime, urllib.request
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")
WF = ROOT / "scripts" / "n8n_fenice_tim_v4.json"
WID = "UKfz7lxQTQcnbOMV"
BASE = f"https://feniceit.app.n8n.cloud/api/v1/workflows/{WID}"

CLONE_FROM = "15a. Log Supabase (interacoes)"
NODE7 = "7. Decidir Próxima Ação"
NODE13 = "13. Enviar Resposta (Evolution API)"
LOG_IN = "Log Diálogo (in)"
LOG_OUT = "Log Diálogo (out)"

BODY_IN = ('={{ JSON.stringify({ numero: $json.numero, direcao: "in", '
           'mensagem: $json.mensagem, area: $json.areaAtual, estagio: $json.estagio, '
           'acao: $json._acao, canal: "whatsapp" }) }}')
BODY_OUT = ("={{ JSON.stringify({ numero: $('7. Decidir Próxima Ação').item.json.numero, "
            'direcao: "out", mensagem: $(\'12. Extrair Resposta Gemini\').item.json.respostaAi, '
            "area: $('7. Decidir Próxima Ação').item.json.areaAtual, "
            "estagio: $('7. Decidir Próxima Ação').item.json.estagio, canal: \"whatsapp\" }) }}")


def _set_header(node, name, value):
    for p in node["parameters"]["headerParameters"]["parameters"]:
        if p["name"] == name:
            p["value"] = value
            return


def _make_log_node(base, name, body, pos):
    n = copy.deepcopy(base)
    n["name"] = name
    n["id"] = str(uuid.uuid4())
    n["position"] = pos
    n["continueOnFail"] = True
    url_base = n["parameters"]["url"].rsplit("/", 1)[0]  # .../rest/v1
    n["parameters"]["url"] = url_base + "/fenice_tim_dialogos"
    n["parameters"]["body"] = body
    _set_header(n, "Prefer", "return=minimal")
    return n


def mutate(wf):
    N = {n["name"]: n for n in wf["nodes"]}
    existing = {n["name"] for n in wf["nodes"]}
    log = []
    base = N[CLONE_FROM]

    if LOG_IN not in existing:
        wf["nodes"].append(_make_log_node(base, LOG_IN, BODY_IN, [1040, 780]))
        log.append(f"① nó '{LOG_IN}' criado (clonado de {CLONE_FROM})")
    else:
        log.append(f"① '{LOG_IN}' já existe")
    if LOG_OUT not in existing:
        wf["nodes"].append(_make_log_node(base, LOG_OUT, BODY_OUT, [2360, 880]))
        log.append(f"② nó '{LOG_OUT}' criado")
    else:
        log.append(f"② '{LOG_OUT}' já existe")

    # fan-out: nó 7 -> logIN (paralelo ao Switch); nó 13 -> logOUT (paralelo ao 14)
    c7 = wf["connections"][NODE7]["main"][0]
    if not any(c["node"] == LOG_IN for c in c7):
        c7.append({"node": LOG_IN, "type": "main", "index": 0})
        log.append(f"③ conexão: {NODE7} -> {LOG_IN} (dead-end)")
    c13 = wf["connections"][NODE13]["main"][0]
    if not any(c["node"] == LOG_OUT for c in c13):
        c13.append({"node": LOG_OUT, "type": "main", "index": 0})
        log.append(f"④ conexão: {NODE13} -> {LOG_OUT} (dead-end)")
    return log


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
    dry = "--dry-run" in sys.argv
    wf = json.loads(WF.read_text(encoding="utf-8"))
    log = mutate(wf)
    print("=== mutações ===")
    for l in log:
        print("  ", l)
    if dry:
        print("\n[dry-run] nada gravado. Nós:", len(wf["nodes"]))
        return

    WF.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n[local] gravado")
    e = _env(); key = e["N8N_API_KEY"]
    st, live = call(BASE, key)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bkp = ROOT / f"scripts/_backup_n8n_v4_LIVE_{ts}.json"
    bkp.write_text(json.dumps(live, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[backup]", bkp.name, len(live.get("nodes", [])), "nós")
    payload = {"name": wf["name"], "nodes": wf["nodes"], "connections": wf["connections"],
               "settings": {"executionOrder": "v1", "saveManualExecutions": True}}
    st, res = call(BASE, key, "PUT", payload)
    print("[PUT]", st, len(res.get("nodes", [])), "nós, active=", res.get("active"))
    if not res.get("active"):
        call(BASE + "/activate", key, "POST", {}); print("[activate] ok")
    st, chk = call(BASE, key)
    names = {n["name"] for n in chk["nodes"]}
    print(f"[verify] logIN={LOG_IN in names} | logOUT={LOG_OUT in names} | nós={len(chk['nodes'])} | active={chk.get('active')}")


if __name__ == "__main__":
    main()
