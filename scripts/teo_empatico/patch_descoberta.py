"""Task 4 — Téo Empático no IVR live.

Espelha a lógica (inferirArea/isSaudacao/descoberta) no workflow n8n_fenice_tim_v4.json
e liga o ramo `descoberta` reusando o pipeline do `responder` (nó 10 → Gemini → envia → log).

5 mudanças, 0 nós novos:
  1. Nó 7  — ramo empático (inferirArea -> set_area | saudação -> menu | incerto -> descoberta)
  2. Nó 8  — regra Switch `descoberta` (clona a regra `responder`)
  3. Conn  — saída descoberta -> nó 10
  4. Nó 10 — DISCOVERY_PROMPT quando _acao == descoberta
  5. Nó 14 — preserva estagio "descoberta" (grude entre mensagens)

Uso:
  python patch_descoberta.py --dry-run   # aplica em memória, mostra diff, NÃO grava/publica
  python patch_descoberta.py             # grava local + backup live + PUT + activate + verify
"""
import copy, json, sys, datetime, urllib.request
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")
WF = ROOT / "scripts" / "n8n_fenice_tim_v4.json"
WID = "UKfz7lxQTQcnbOMV"
BASE = f"https://feniceit.app.n8n.cloud/api/v1/workflows/{WID}"

# ── injeção de lógica no nó 7 (sem backslash exceto \s em regex literal → raw string) ──
INJECT_HELPERS = r"""
const AREA_KEYWORDS={b2b:["tim","corporativo","operadora","b2b","plano da empresa","plano corporativo"],academico:["faculdade","estudar","estudo","prova","concurso","oab","aula","matéria","materia","univille"],observatorio:["monitorar","monitoramento","observatório","observatorio","acompanhar processo"],api:["api","integração","integracao","webhook","integrar sistema","desenvolvedor"],juridico:["advogado","processo judicial","penal","civil","constitucional","tributário","tributario","trabalhista","dúvida jurídica","duvida juridica","petição","peticao"],filosofia:["filosofia","filosófico","filosofico","ética","etica","pensador","existência","existencia"]};
const _casa=(t,m)=>{if(t.length<=3&&!t.includes(" ")){const i=m.indexOf(t);if(i<0)return false;const a=m[i-1]||"",b=m[i+t.length]||"";return !/[a-z0-9]/.test(a)&&!/[a-z0-9]/.test(b);}return m.includes(t);};
const inferirArea=(msg)=>{const m=(msg||"").toLowerCase();if(!m)return null;for(const[ar,ts]of Object.entries(AREA_KEYWORDS)){if(ts.some(t=>_casa(t,m)))return ar;}return null;};
const SAUDACOES=["oi","ola","olá","opa","oie","e ai","eai","hey","hi","bom dia","boa tarde","boa noite","salam","salaam","as salamu alaikum","saudações","saudacoes"];
const isSaudacao=(msg)=>{const m=(msg||"").toLowerCase().replace(/[!.?,]+$/g,"").trim();if(!m)return false;if(SAUDACOES.includes(m))return true;const ini=SAUDACOES.some(s=>m.startsWith(s));return ini&&m.split(/\s+/).length<=3;};
"""

N7_ANCHOR = "const detectarIntencao = (m) => { const s=(m||'').toLowerCase(); return SINAIS.some(x=>s.includes(x)); };"
N7_OLD = 'if (!areaAtual) return [{ json: { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 } }];'
N7_NEW = (
    'if (!areaAtual) {\n'
    '  const areaInferida = inferirArea(mensagem);\n'
    '  if (areaInferida) return [{ json: { ...base, _acao: "set_area", areaAtual: areaInferida, msgCount: 0 } }];\n'
    '  if (isSaudacao(mensagem)) return [{ json: { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 } }];\n'
    '  return [{ json: { ...base, _acao: "descoberta", estagio: "descoberta", areaAtual: null } }];\n'
    '}'
)

DISCOVERY_PROMPT_JS = (
    "const _acao = dados._acao;\n"
    "const DISCOVERY_PROMPT = `Você é o *Teo*, Intelligence Concierge da Fenice IT, no WhatsApp. "
    "O usuário ainda não disse claramente o que precisa. ACOLHA com calor e descubra JUNTO com ele o que procura — "
    "nunca pressione, nunca liste opções secas, nunca peça para \"digitar um número\". Trate como Dr./Dra. "
    "Valide o que ele disse, faça 1 pergunta gentil, e deixe claro que pode se expressar do jeito que quiser. "
    "Máximo 3 linhas. Não use a palavra \"IA\" sozinha. Cliente: ${nome}.`;\n"
)
N10_DEST_OLD = "const { numero, nome, mensagem, areaAtual } = dados;"
N10_DEST_NEW = "const { numero, nome, mensagem, areaAtual } = dados;\n" + DISCOVERY_PROMPT_JS
N10_SP_OLD = "const sistemaPrompt = SYSTEM_PROMPTS[areaAtual] || SYSTEM_PROMPTS.juridico;"
N10_SP_NEW = "const sistemaPrompt = _acao === 'descoberta' ? DISCOVERY_PROMPT : (SYSTEM_PROMPTS[areaAtual] || SYSTEM_PROMPTS.juridico);"

N14_OLD = "const estagioLog = TERMINAIS.includes(dadosAcao.estagio) ? dadosAcao.estagio : 'atendimento';"
N14_NEW = "const estagioLog = (TERMINAIS.includes(dadosAcao.estagio) || dadosAcao.estagio === 'descoberta') ? dadosAcao.estagio : 'atendimento';"

SWITCH = "8. Switch por Ação"
N10 = "10. Montar Prompt por Área"


def _sub(code, old, new, label):
    assert old in code, f"[{label}] âncora NÃO encontrada — arquivo divergiu:\n  {old[:80]}"
    assert code.count(old) == 1, f"[{label}] âncora ambígua ({code.count(old)}x)"
    return code.replace(old, new)


def mutate(wf):
    N = {n["name"]: n for n in wf["nodes"]}
    log = []

    # 1) Nó 7
    c7 = N["7. Decidir Próxima Ação"]["parameters"]["jsCode"]
    c7 = _sub(c7, N7_ANCHOR, N7_ANCHOR + INJECT_HELPERS.rstrip("\n"), "n7-helpers")
    c7 = _sub(c7, N7_OLD, N7_NEW, "n7-branch")
    N["7. Decidir Próxima Ação"]["parameters"]["jsCode"] = c7
    log.append("① nó 7: helpers + ramo empático")

    # 2) Nó 8 — clona a regra 'responder' e vira 'descoberta'
    rules = N[SWITCH]["parameters"]["rules"]["values"]
    if not any(r.get("outputKey") == "descoberta" for r in rules):
        base_rule = next(r for r in rules if r.get("outputKey") == "responder")
        nova = copy.deepcopy(base_rule)
        nova["conditions"]["conditions"][0]["rightValue"] = "descoberta"
        nova["outputKey"] = "descoberta"
        rules.append(nova)
        log.append("② nó 8: regra Switch 'descoberta'")
    else:
        log.append("② nó 8: regra 'descoberta' já existe")

    # 3) Conexão saída descoberta -> nó 10
    mainconns = wf["connections"][SWITCH]["main"]
    idx = next(i for i, r in enumerate(rules) if r.get("outputKey") == "descoberta")
    while len(mainconns) <= idx:
        mainconns.append([])
    if not any(c["node"] == N10 for c in mainconns[idx]):
        mainconns[idx] = [{"node": N10, "type": "main", "index": 0}]
        log.append(f"③ conexão: Switch out{idx} (descoberta) -> {N10}")
    else:
        log.append("③ conexão descoberta já existe")

    # 4) Nó 10
    c10 = N[N10]["parameters"]["jsCode"]
    c10 = _sub(c10, N10_DEST_OLD, N10_DEST_NEW, "n10-dest")
    c10 = _sub(c10, N10_SP_OLD, N10_SP_NEW, "n10-prompt")
    N[N10]["parameters"]["jsCode"] = c10
    log.append("④ nó 10: DISCOVERY_PROMPT condicional")

    # 5) Nó 14
    c14 = N["14. Montar Logs"]["parameters"]["jsCode"]
    c14 = _sub(c14, N14_OLD, N14_NEW, "n14-estagio")
    N["14. Montar Logs"]["parameters"]["jsCode"] = c14
    log.append("⑤ nó 14: preserva estagio 'descoberta'")

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
        print("\n[dry-run] nada gravado nem publicado. Nós:", len(wf["nodes"]),
              "| saídas Switch:", len(wf["connections"][SWITCH]["main"]))
        return

    WF.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n[local] arquivo gravado")

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
    C = {n["name"]: n for n in chk["nodes"]}
    ok7 = "descoberta" in C["7. Decidir Próxima Ação"]["parameters"]["jsCode"]
    okrule = any(r.get("outputKey") == "descoberta" for r in C[SWITCH]["parameters"]["rules"]["values"])
    ok10 = "DISCOVERY_PROMPT" in C[N10]["parameters"]["jsCode"]
    ok14 = "estagio === 'descoberta'" in C["14. Montar Logs"]["parameters"]["jsCode"]
    print(f"[verify] n7={ok7} | switch_rule={okrule} | n10={ok10} | n14={ok14} | active={chk.get('active')}")


if __name__ == "__main__":
    main()
