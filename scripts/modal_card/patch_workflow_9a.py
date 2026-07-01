import json, sys
from pathlib import Path

WF = Path(r"C:\Fenice_bRain\scripts\n8n_fenice_tim_v4.json")
CARD_URL = "https://qcfdssnpjzvjbvemhrik.supabase.co/storage/v1/object/public/modal/modal_teo.jpg"

CAPTION = (
    "*Teo — Intelligence Concierge*\n"
    "Escolha um serviço e responda com o número (0 a 6).\n"
    "*7* ou *sair* para encerrar.\n"
    "🌐 https://www.fenice.ia.br"
)

MENU = "9a. Enviar Menu Principal"
LOGO = "9-logo. Enviar Logo Fenice"


def _num_expr(node):
    for p in node["parameters"].get("bodyParameters", {}).get("parameters", []):
        if p["name"] == "number":
            return p["value"]
    return "={{ $('7. Decidir Próxima Ação').item.json.numero }}"


def patch():
    wf = json.loads(WF.read_text(encoding="utf-8"))
    nodes, conns = wf["nodes"], wf["connections"]

    img_names = [n["name"] for n in nodes if n["name"].startswith("9a-img")]

    # 1) nó 9a -> sendMedia (cartão) + legenda-menu
    for n in nodes:
        if n["name"] == MENU:
            num = _num_expr(n)
            n["parameters"]["url"] = n["parameters"]["url"].replace("/message/sendText/", "/message/sendMedia/")
            n["parameters"]["bodyParameters"] = {"parameters": [
                {"name": "number", "value": num},
                {"name": "mediatype", "value": "image"},
                {"name": "media", "value": CARD_URL},
                {"name": "caption", "value": CAPTION},
            ]}

    # 2) remover nós órfãos 9a-img* e o 9-logo redundante
    nodes[:] = [n for n in nodes if n["name"] not in img_names and n["name"] != LOGO]

    # 3) religar: qualquer aresta que apontava para 9-logo agora aponta para 9a
    for src, spec in conns.items():
        for grp in spec.get("main", []):
            for c in grp:
                if c.get("node") == LOGO:
                    c["node"] = MENU
    conns.pop(LOGO, None)
    for name in img_names:
        conns.pop(name, None)

    # 4) 7 = sair -> adiciona "7" ao RESET_WORDS em todos os nós que o definem
    n_reset = 0
    for n in nodes:
        params = n.get("parameters", {})
        code = params.get("jsCode")
        if isinstance(code, str) and 'RESET_WORDS' in code and '"reiniciar","sair"]' in code:
            params["jsCode"] = code.replace('"reiniciar","sair"]', '"reiniciar","sair","7"]')
            n_reset += 1

    WF.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"patch OK | removidos img={len(img_names)} + 9-logo | RESET_WORDS+7 em {n_reset} nó(s) | nós={len(nodes)}")


if __name__ == "__main__":
    patch()
