"""Guardrail anti-"não existe" no nó 10 (Montar Prompt).

Regra já decidida: na ausência de dados, o Téo NUNCA nega existência nem inventa —
responde "não encontrei na base, vou pesquisar". 3 trechos endurecidos.

Uso: python patch_prompt_guardrail.py [--dry-run]
"""
import json, sys, datetime, urllib.request
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")
WF = ROOT / "scripts" / "n8n_fenice_tim_v4.json"
WID = "UKfz7lxQTQcnbOMV"
BASE = f"https://feniceit.app.n8n.cloud/api/v1/workflows/{WID}"
NODE10 = "10. Montar Prompt por Área"

FRASE = ('"Não encontrei este ponto na minha base agora, Dr(a). — '
         'vou pesquisar e retorno com a fundamentação."')

A1_OLD = "• Nunca invente leis, artigos ou jurisprudência. Se não souber → diga que pesquisa."
A1_NEW = ('• PROIBIDO afirmar que uma lei, artigo ou instituto "não existe" ou "não há". '
          "Você NÃO tem a base completa. Nunca invente e NUNCA negue existência. "
          "Na dúvida ou ausência de dados responda EXATAMENTE: " + FRASE)

A2_OLD = "Se não cobrir, use seu conhecimento mas seja honesto."
A2_NEW = "Se não cobrir, NÃO afirme que algo não existe: diga que vai pesquisar e retornar. Nunca invente."

A3_OLD = "Responda com base no seu conhecimento jurídico. Seja preciso e cite a base legal quando possível."
A3_NEW = ("ATENÇÃO: a base Fenice NÃO retornou dispositivo para esta consulta. JAMAIS afirme que algo "
          "não existe nem invente. Responda: " + FRASE)


def _sub(code, old, new, label):
    assert old in code, f"[{label}] âncora NÃO encontrada"
    assert code.count(old) == 1, f"[{label}] âncora ambígua ({code.count(old)}x)"
    return code.replace(old, new)


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
    N = {n["name"]: n for n in wf["nodes"]}
    c = N[NODE10]["parameters"]["jsCode"]
    c = _sub(c, A1_OLD, A1_NEW, "regra")
    c = _sub(c, A2_OLD, A2_NEW, "ramo-com-rag")
    c = _sub(c, A3_OLD, A3_NEW, "ramo-sem-rag")
    N[NODE10]["parameters"]["jsCode"] = c
    print("=== 3 trechos endurecidos (regra + ramo com RAG + ramo sem RAG) ===")
    if dry:
        print("[dry-run] nada gravado")
        return
    WF.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[local] gravado")
    e = _env(); key = e["N8N_API_KEY"]
    st, live = call(BASE, key)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"scripts/_backup_n8n_v4_LIVE_{ts}.json").write_text(
        json.dumps(live, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[backup] gravado")
    payload = {"name": wf["name"], "nodes": wf["nodes"], "connections": wf["connections"],
               "settings": {"executionOrder": "v1", "saveManualExecutions": True}}
    st, res = call(BASE, key, "PUT", payload)
    print("[PUT]", st, "active=", res.get("active"))
    if not res.get("active"):
        call(BASE + "/activate", key, "POST", {})
    st, chk = call(BASE, key)
    ok = "NUNCA negue existência" in {n["name"]: n for n in chk["nodes"]}[NODE10]["parameters"]["jsCode"]
    print(f"[verify] guardrail_live={ok} | active={chk.get('active')}")


if __name__ == "__main__":
    main()
