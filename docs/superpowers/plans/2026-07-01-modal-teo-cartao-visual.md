# Modal Téo — Cartão Visual Único · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir o menu de emojis do Téo por um cartão visual único (imagem composta) e corrigir os dois bugs que impediam as imagens de funcionar em produção (`sendImage`→`sendMedia`, hospedagem 404).

**Architecture:** Um template HTML autocontido é renderizado para PNG (Playwright headless). O PNG é testado por base64 no WhatsApp corporativo, depois hospedado no Supabase Storage (bucket público). O nó `9a` do workflow N8N passa a enviar essa imagem via `sendMedia`, e os 4 nós `9a-img*` são removidos. Re-push via API N8N.

**Tech Stack:** Python 3.14 (stdlib `urllib`, `base64`, `pathlib`, `json`), Playwright (headless Chromium), Pillow (validação de imagem), Evolution API v2, Supabase Storage REST, N8N Public API v1.

## Global Constraints

- Numeração do menu **inalterada**: `1–6` + `0`. Rotas `MENU_OPCOES` **não mudam**.
- Item 1 label = **`TIM br`** (era "B2B Corporativo").
- Rodapé — assinatura padrão EXATA (3 linhas):
  `👤 Teo — Intelligence Concierge` / `© 2026 Fenice IT Justech.IA` / `by Tech Lead Ramão Bueno`
- Persona: **Téo** (nunca "assistente"/"bot"/"IA"). Copy externa: se citar IA, usar "com o auxílio das maiores plataformas de IA — CLAUDE & Open IA".
- Endpoint de mídia: **`/message/sendMedia/`** (NUNCA `/message/sendImage/`).
- Canvas do cartão: retrato **1080×1440**.
- Estilo: fundo preto brilhante + dourado/laranja (identidade Fenice).
- Paths de arquivo/pasta **ASCII-safe** (fluxo git do projeto).
- N8N PUT: body só `{name,nodes,connections,settings}`; `settings` mínimo `{"executionOrder":"v1","saveManualExecutions":true}`; **sempre GET→backup antes do PUT**.
- Segredos vêm de `C:\Fenice_bRain\.env` (gitignored) — nunca hardcodar no repo.
- Assets fonte: `C:\Fenice_site\TIM\*.jpeg` (nomes com acento/espaço — abrir via `pathlib.Path`).

---

## File Structure

- `scripts/modal_card/card_template.html` — template do cartão (CSS + placeholders `{{IMG_*}}`, `{{...}}`).
- `scripts/modal_card/build_card.py` — injeta os 10 logos (base64) no template → `card_built.html`.
- `scripts/modal_card/render_card.py` — Playwright: `card_built.html` → `card.png` (1080×1440).
- `scripts/modal_card/send_card_test.py` — envia `card.png` (base64) via `sendMedia` ao corporativo.
- `scripts/modal_card/upload_card_supabase.py` — sobe `card.png` ao bucket público `modal`, valida URL.
- `scripts/modal_card/patch_workflow_9a.py` — edita `n8n_fenice_tim_v4.json` (9a→sendMedia, remove `9a-img*`).
- `scripts/modal_card/push_workflow.py` — backup live + PUT + activate + verify (reutiliza receita conhecida).
- Modify: `scripts/n8n_fenice_tim_v4.json` — nó `9a` + remoção dos `9a-img*`.

Assets → label (exatos):
`emoji tim.jpeg`→1 TIM br · `Acadêmico Ciências Jurídicas.jpeg`→2 · `mulheres.jpeg`→3 · `api e desenvolvedores.jpeg`→4 · `consultoria jurídica.jpeg`→5 · `filosofia.jpeg`→6 · `especialista.jpeg`→0 · `téo.jpeg`→avatar · `logo fenice emoji.jpeg`→topo-dir · `saida.jpeg`→ícone sair.

---

### Task 1: Template HTML + build com assets embutidos

**Files:**
- Create: `scripts/modal_card/card_template.html`
- Create: `scripts/modal_card/build_card.py`
- Create: `scripts/modal_card/test_build.py`

**Interfaces:**
- Produces: `card_built.html` (arquivo), e função `build(template_path, assets_dir, out_path) -> Path`.

- [ ] **Step 1: Criar o template HTML** — `scripts/modal_card/card_template.html`

```html
<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',Arial,sans-serif; }
  #card { width:1080px; height:1440px; background:radial-gradient(120% 80% at 50% 0%, #1a1205 0%, #0a0a0a 55%, #000 100%);
          color:#f5e9c8; padding:64px 56px; display:flex; flex-direction:column; }
  .top { display:flex; align-items:center; gap:28px; border-bottom:2px solid #c8a13a55; padding-bottom:32px; }
  .top .teo { width:132px; height:132px; border-radius:24px; object-fit:cover; box-shadow:0 0 32px #c8a13a55; }
  .top .title { flex:1; }
  .top .title h1 { font-size:52px; color:#f2c85a; letter-spacing:.5px; }
  .top .title p { font-size:30px; color:#cdbf9a; }
  .top .fenice { width:104px; height:104px; border-radius:50%; object-fit:cover; box-shadow:0 0 24px #c8a13a66; }
  .items { flex:1; display:flex; flex-direction:column; justify-content:center; gap:22px; }
  .row { display:flex; align-items:center; gap:28px; background:#ffffff08; border:1px solid #c8a13a33;
         border-radius:22px; padding:18px 26px; }
  .row img { width:88px; height:88px; border-radius:16px; object-fit:cover; background:#fff; }
  .row .num { font-size:44px; font-weight:700; color:#f2c85a; width:54px; text-align:center; }
  .row .lbl { font-size:38px; color:#f5e9c8; }
  .foot { border-top:2px solid #c8a13a55; padding-top:28px; text-align:center; }
  .foot .cta { font-size:32px; color:#f2c85a; margin-bottom:18px; }
  .foot .sig { font-size:26px; color:#cdbf9a; line-height:1.5; }
</style></head><body>
<div id="card">
  <div class="top">
    <img class="teo" src="{{IMG_TEO}}" alt="Téo">
    <div class="title"><h1>Téo</h1><p>Intelligence Concierge</p></div>
    <img class="fenice" src="{{IMG_FENICE}}" alt="Fenice">
  </div>
  <div class="items">
    <div class="row"><img src="{{IMG_TIM}}"><span class="num">1</span><span class="lbl">TIM br</span></div>
    <div class="row"><img src="{{IMG_ACAD}}"><span class="num">2</span><span class="lbl">Acadêmico &amp; Pesquisa</span></div>
    <div class="row"><img src="{{IMG_OBS}}"><span class="num">3</span><span class="lbl">Observatório da Mulher SFS</span></div>
    <div class="row"><img src="{{IMG_API}}"><span class="num">4</span><span class="lbl">API &amp; Desenvolvedores</span></div>
    <div class="row"><img src="{{IMG_JUR}}"><span class="num">5</span><span class="lbl">Consultoria Jurídica</span></div>
    <div class="row"><img src="{{IMG_FILO}}"><span class="num">6</span><span class="lbl">Filosofia &amp; Teologia</span></div>
    <div class="row"><img src="{{IMG_ESP}}"><span class="num">0</span><span class="lbl">Falar com Especialista</span></div>
  </div>
  <div class="foot">
    <div class="cta">Digite o número · ou <b>sair</b></div>
    <div class="sig">👤 Teo — Intelligence Concierge<br>© 2026 Fenice IT Justech.IA<br>by Tech Lead Ramão Bueno</div>
  </div>
</div></body></html>
```

- [ ] **Step 2: Escrever o teste falhando** — `scripts/modal_card/test_build.py`

```python
from pathlib import Path
import subprocess, sys

BASE = Path(__file__).parent

def test_build_produces_html_without_placeholders():
    out = BASE / "card_built.html"
    if out.exists(): out.unlink()
    r = subprocess.run([sys.executable, str(BASE / "build_card.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists(), "card_built.html não foi criado"
    html = out.read_text(encoding="utf-8")
    assert "{{" not in html, "restaram placeholders não substituídos"
    assert html.count("data:image/") >= 10, "esperados >=10 assets embutidos em base64"
    assert "by Tech Lead Ramão Bueno" in html
```

- [ ] **Step 3: Rodar o teste e ver falhar**

Run: `python -m pytest scripts/modal_card/test_build.py -v`
Expected: FAIL (build_card.py ainda não existe → returncode != 0)

- [ ] **Step 4: Implementar** — `scripts/modal_card/build_card.py`

```python
import base64, sys
from pathlib import Path

BASE = Path(__file__).parent
ASSETS = Path(r"C:\Fenice_site\TIM")
MAP = {
    "IMG_TEO":    "téo.jpeg",
    "IMG_FENICE": "logo fenice emoji.jpeg",
    "IMG_TIM":    "emoji tim.jpeg",
    "IMG_ACAD":   "Acadêmico Ciências Jurídicas.jpeg",
    "IMG_OBS":    "mulheres.jpeg",
    "IMG_API":    "api e desenvolvedores.jpeg",
    "IMG_JUR":    "consultoria jurídica.jpeg",
    "IMG_FILO":   "filosofia.jpeg",
    "IMG_ESP":    "especialista.jpeg",
}

def _data_uri(p: Path) -> str:
    b = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b}"

def build(template=BASE/"card_template.html", assets=ASSETS, out=BASE/"card_built.html") -> Path:
    html = Path(template).read_text(encoding="utf-8")
    for key, fname in MAP.items():
        src = Path(assets) / fname
        if not src.exists():
            raise FileNotFoundError(f"asset ausente: {src}")
        html = html.replace("{{"+key+"}}", _data_uri(src))
    Path(out).write_text(html, encoding="utf-8")
    return Path(out)

if __name__ == "__main__":
    p = build()
    print("card_built.html gerado:", p)
```

- [ ] **Step 5: Rodar o teste e ver passar**

Run: `python -m pytest scripts/modal_card/test_build.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/modal_card/card_template.html scripts/modal_card/build_card.py scripts/modal_card/test_build.py
git commit -m "feat(modal): template HTML do cartão Téo + build com assets base64"
```

---

### Task 2: Renderizar HTML → PNG 1080×1440 (Playwright)

**Files:**
- Create: `scripts/modal_card/render_card.py`
- Create: `scripts/modal_card/test_render.py`

**Interfaces:**
- Consumes: `card_built.html` (de Task 1).
- Produces: `card.png` (1080×1440) e função `render(html_path, out_png) -> Path`.

- [ ] **Step 1: Escrever o teste falhando** — `scripts/modal_card/test_render.py`

```python
from pathlib import Path
import subprocess, sys
from PIL import Image

BASE = Path(__file__).parent

def test_render_produces_1080x1440_png():
    png = BASE / "card.png"
    if png.exists(): png.unlink()
    subprocess.run([sys.executable, str(BASE/"build_card.py")], check=True)
    r = subprocess.run([sys.executable, str(BASE/"render_card.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert png.exists(), "card.png não foi criado"
    w, h = Image.open(png).size
    assert (w, h) == (1080, 1440), f"dimensões erradas: {w}x{h}"
    assert png.stat().st_size > 20000, "PNG suspeito de estar vazio"
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `python -m pytest scripts/modal_card/test_render.py -v`
Expected: FAIL (render_card.py não existe)

- [ ] **Step 3: Implementar** — `scripts/modal_card/render_card.py`

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent

def render(html=BASE/"card_built.html", out=BASE/"card.png") -> Path:
    url = Path(html).resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width":1080, "height":1440})
        page.goto(url)
        page.locator("#card").screenshot(path=str(out))
        browser.close()
    return Path(out)

if __name__ == "__main__":
    print("card.png gerado:", render())
```

- [ ] **Step 4: Garantir dependências (uma vez)**

Run: `python -m pip install playwright pillow && python -m playwright install chromium`
Expected: instalação concluída sem erro

- [ ] **Step 5: Rodar e ver passar**

Run: `python -m pytest scripts/modal_card/test_render.py -v`
Expected: PASS

- [ ] **Step 6: Preview manual** — abrir `scripts/modal_card/card.png` e conferir visual (logos, cores, rodapé). Ajustar CSS no template se necessário e re-rodar Task 1+2.

- [ ] **Step 7: Commit**

```bash
git add scripts/modal_card/render_card.py scripts/modal_card/test_render.py
git commit -m "feat(modal): render Playwright do cartão para PNG 1080x1440"
```

---

### Task 3: Envio de teste (base64) ao corporativo — checkpoint humano

**Files:**
- Create: `scripts/modal_card/send_card_test.py`

**Interfaces:**
- Consumes: `card.png` (Task 2); `.env` (EVOLUTION_*).
- Produces: efeito colateral (mensagem no WhatsApp); imprime HTTP status.

- [ ] **Step 1: Implementar** — `scripts/modal_card/send_card_test.py`

```python
import os, sys, json, base64, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent  # C:\Fenice_bRain

def _env():
    e = {}
    for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); e[k.strip()] = v.strip()
    return e

CAPTION = ("👤 *Teo — Intelligence Concierge*\n\n"
           "Escolha uma opção — digite o número (0–6). Para sair, digite *sair*.\n\n"
           "© 2026 Fenice IT Justech.IA\nby Tech Lead Ramão Bueno")

def main(numero="5547991041414"):
    e = _env()
    url = e["EVOLUTION_API_URL"].rstrip("/"); apikey = e["EVOLUTION_API_KEY"]; inst = e["EVOLUTION_INSTANCE"]
    b64 = base64.b64encode((BASE/"card.png").read_bytes()).decode()
    payload = {"number": numero, "mediatype": "image", "media": b64, "fileName": "modal_teo.png", "caption": CAPTION}
    req = urllib.request.Request(f"{url}/message/sendMedia/{inst}",
        data=json.dumps(payload).encode(), headers={"apikey": apikey, "Content-Type": "application/json"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=45); res = json.load(r)
        print("[ENVIO] HTTP", r.status, "| id=", (res.get("key") or {}).get("id"), "| status=", res.get("status"))
    except urllib.error.HTTPError as ex:
        print("[ENVIO] ERRO", ex.code, ex.read().decode()[:400]); sys.exit(1)

if __name__ == "__main__":
    main(*sys.argv[1:])
```

- [ ] **Step 2: Rodar o envio de teste**

Run: `python scripts/modal_card/send_card_test.py`
Expected: `[ENVIO] HTTP 201` com messageId

- [ ] **Step 3: Checkpoint humano** — Ramão confere no WhatsApp `47 99104-1414` se o cartão chegou como **imagem** e ficou bonito. **NÃO prosseguir sem o "OK".** Se pedir ajustes visuais, voltar à Task 1/2.

- [ ] **Step 4: Commit**

```bash
git add scripts/modal_card/send_card_test.py
git commit -m "feat(modal): script de envio de teste do cartão via sendMedia base64"
```

---

### Task 4: Hospedar no Supabase Storage (bucket público) + validar URL

**Files:**
- Create: `scripts/modal_card/upload_card_supabase.py`

**Interfaces:**
- Consumes: `card.png`; `.env` (SUPABASE_URL, SUPABASE_SERVICE_KEY).
- Produces: URL pública estável; imprime a URL (usada na Task 5).

- [ ] **Step 1: Implementar** — `scripts/modal_card/upload_card_supabase.py`

```python
import os, sys, json, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent

def _env():
    e = {}
    for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); e[k.strip()] = v.strip()
    return e

BUCKET = "modal"; OBJECT = "modal_teo.png"

def _req(url, method, key, data=None, ctype="application/json"):
    h = {"Authorization": f"Bearer {key}", "apikey": key, "Content-Type": ctype}
    return urllib.request.Request(url, data=data, headers=h, method=method)

def main():
    e = _env(); base = e["SUPABASE_URL"].rstrip("/"); key = e["SUPABASE_SERVICE_KEY"]
    # 1) garantir bucket público (ignora erro se já existe)
    try:
        urllib.request.urlopen(_req(f"{base}/storage/v1/bucket", "POST", key,
            json.dumps({"id": BUCKET, "name": BUCKET, "public": True}).encode()), timeout=20)
        print("[bucket] criado")
    except urllib.error.HTTPError as ex:
        print("[bucket] já existe/《", ex.code, "》")
    # 2) upload (upsert)
    img = (BASE/"card.png").read_bytes()
    up = _req(f"{base}/storage/v1/object/{BUCKET}/{OBJECT}", "POST", key, img, "image/png")
    up.add_header("x-upsert", "true")
    try:
        urllib.request.urlopen(up, timeout=45); print("[upload] ok")
    except urllib.error.HTTPError as ex:
        print("[upload] ERRO", ex.code, ex.read().decode()[:300]); sys.exit(1)
    # 3) URL pública + validação
    public = f"{base}/storage/v1/object/public/{BUCKET}/{OBJECT}"
    r = urllib.request.urlopen(public, timeout=20)
    assert r.status == 200 and r.headers.get("Content-Type","").startswith("image"), "URL pública inválida"
    print("PUBLIC_URL:", public)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o upload**

Run: `python scripts/modal_card/upload_card_supabase.py`
Expected: última linha `PUBLIC_URL: https://qcfdssnpjzvjbvemhrik.supabase.co/storage/v1/object/public/modal/modal_teo.png` (HTTP 200 na validação)

- [ ] **Step 3: Anotar a PUBLIC_URL** para a Task 5.

- [ ] **Step 4: Commit**

```bash
git add scripts/modal_card/upload_card_supabase.py
git commit -m "feat(modal): upload do cartão ao Supabase Storage (bucket público) + validação de URL"
```

---

### Task 5: Patch do nó 9a (sendMedia + remoção dos 9a-img*) e re-push

**Files:**
- Create: `scripts/modal_card/patch_workflow_9a.py`
- Create: `scripts/modal_card/push_workflow.py`
- Modify: `scripts/n8n_fenice_tim_v4.json`

**Interfaces:**
- Consumes: PUBLIC_URL (Task 4); `.env` (N8N_*).
- Produces: `n8n_fenice_tim_v4.json` atualizado; workflow em produção atualizado.

- [ ] **Step 1: Implementar o patch do JSON** — `scripts/modal_card/patch_workflow_9a.py`

```python
import json, sys
from pathlib import Path

WF = Path(r"C:\Fenice_bRain\scripts\n8n_fenice_tim_v4.json")
CAPTION = ("👤 *Teo — Intelligence Concierge*\n\n"
           "Escolha uma opção — digite o número (0–6). Para sair, digite *sair*.\n\n"
           "© 2026 Fenice IT Justech.IA\nby Tech Lead Ramão Bueno")

def patch(public_url: str):
    wf = json.loads(WF.read_text(encoding="utf-8"))
    img_names = [n["name"] for n in wf["nodes"] if n.get("name","").startswith("9a-img")]
    menu_name = next(n["name"] for n in wf["nodes"] if n.get("name","").startswith("9a. Enviar Menu"))

    # 1) descobrir para onde o último 9a-img aponta (para religar 9a diretamente)
    conns = wf["connections"]
    # cadeia começa em menu_name -> img1 -> ... -> imgN -> destino_final
    def next_of(name):
        c = conns.get(name, {}).get("main", [[]])
        return c[0][0]["node"] if c and c[0] else None
    # segue a cadeia a partir do menu até sair dos nós 9a-img
    cur = next_of(menu_name); destino_final = None
    while cur:
        if cur.startswith("9a-img"):
            destino_final = next_of(cur); cur = destino_final
        else:
            destino_final = cur; break

    # 2) converter o nó de menu para sendMedia (imagem hospedada)
    for n in wf["nodes"]:
        if n["name"] == menu_name:
            body = {"parameters":[
                {"name":"number","value":n_number(n)},
                {"name":"mediatype","value":"image"},
                {"name":"media","value":public_url},
                {"name":"fileName","value":"modal_teo.png"},
                {"name":"caption","value":CAPTION},
            ]}
            # troca URL do endpoint sendText->sendMedia e o body
            _set_url_sendmedia(n); n["parameters"]["bodyParameters"] = body

    # 3) remover os nós 9a-img* e suas conexões
    wf["nodes"] = [n for n in wf["nodes"] if not n["name"].startswith("9a-img")]
    for name in img_names:
        conns.pop(name, None)
    # 4) religar menu -> destino_final
    if destino_final:
        conns[menu_name] = {"main": [[{"node": destino_final, "type": "main", "index": 0}]]}
    else:
        conns.pop(menu_name, None)

    WF.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"patch ok: removidos {len(img_names)} nós img; menu->{destino_final}")

def n_number(node):
    for p in node["parameters"].get("bodyParameters",{}).get("parameters",[]):
        if p["name"] == "number": return p["value"]
    return "={{ $('7. Decidir Próxima Ação').item.json.numero }}"

def _set_url_sendmedia(node):
    node["parameters"]["url"] = node["parameters"]["url"].replace("/message/sendText/", "/message/sendMedia/")

if __name__ == "__main__":
    patch(sys.argv[1])
```

- [ ] **Step 2: Rodar o patch com a PUBLIC_URL**

Run: `python scripts/modal_card/patch_workflow_9a.py "https://qcfdssnpjzvjbvemhrik.supabase.co/storage/v1/object/public/modal/modal_teo.png"`
Expected: `patch ok: removidos 4 nós img; menu->...`

- [ ] **Step 3: Validar o JSON localmente**

Run: `python -c "import json; d=json.load(open(r'scripts/n8n_fenice_tim_v4.json',encoding='utf-8')); assert not [n for n in d['nodes'] if n['name'].startswith('9a-img')]; assert any('sendMedia' in json.dumps(n) for n in d['nodes'] if n['name'].startswith('9a. Enviar Menu')); print('JSON OK', len(d['nodes']),'nós')"`
Expected: `JSON OK 35 nós` (39 − 4 imgs)

- [ ] **Step 4: Implementar o push** — `scripts/modal_card/push_workflow.py`

```python
import os, sys, json, glob, datetime, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r"C:\Fenice_bRain")
def _env():
    e={};
    for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); e[k.strip()]=v.strip()
    return e

def call(url, key, method="GET", payload=None):
    H={"X-N8N-API-KEY":key,"Accept":"application/json","Content-Type":"application/json"}
    data=json.dumps(payload,ensure_ascii=False).encode() if payload is not None else None
    r=urllib.request.urlopen(urllib.request.Request(url,data=data,headers=H,method=method),timeout=60)
    return r.status, json.load(r)

def main():
    e=_env(); wid=e["N8N_WORKFLOW_ID"]; key=e["N8N_API_KEY"]
    base=f"https://feniceit.app.n8n.cloud/api/v1/workflows/{wid}"
    st, live = call(base, key)
    ts=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bkp=ROOT/f"scripts/_backup_n8n_v4_LIVE_{ts}.json"
    bkp.write_text(json.dumps(live,ensure_ascii=False,indent=2),encoding="utf-8")
    print("[backup]", bkp.name, len(live.get("nodes",[])), "nós")
    g=json.loads((ROOT/"scripts/n8n_fenice_tim_v4.json").read_text(encoding="utf-8"))
    payload={"name":g["name"],"nodes":g["nodes"],"connections":g["connections"],
             "settings":{"executionOrder":"v1","saveManualExecutions":True}}
    st,res=call(base,key,"PUT",payload); print("[PUT]",st,len(res.get("nodes",[])),"nós, active=",res.get("active"))
    if not res.get("active"): call(base+"/activate",key,"POST",{}); print("[activate] ok")
    st,chk=call(base,key)
    imgs=[n["name"] for n in chk["nodes"] if n["name"].startswith("9a-img")]
    media=any("sendMedia" in json.dumps(n) for n in chk["nodes"] if n["name"].startswith("9a. Enviar Menu"))
    print(f"[verify] {len(chk['nodes'])} nós | 9a-img restantes={imgs} | 9a usa sendMedia={media}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Rodar o push**

Run: `python scripts/modal_card/push_workflow.py`
Expected: `[verify] 35 nós | 9a-img restantes=[] | 9a usa sendMedia=True` e `active=True`

- [ ] **Step 6: Teste E2E real** — Ramão manda "oi" de outro número ao `47 99104-1414`. Esperado: Téo responde com o **cartão único** (imagem) + legenda; digitar `1` roteia para TIM/b2b.

- [ ] **Step 7: Commit**

```bash
git add scripts/modal_card/patch_workflow_9a.py scripts/modal_card/push_workflow.py scripts/n8n_fenice_tim_v4.json
git commit -m "feat(modal): 9a via sendMedia (cartão único) + remove nós 9a-img; re-push N8N"
```

---

## Self-Review

**1. Spec coverage:**
- §1 bugs (sendImage→sendMedia, hospedagem) → Tasks 4 e 5 ✅
- §2 restrição plataforma (cartão único) → Tasks 1–2 ✅
- §3 layout/estilo/mapeamento/rodapé → Task 1 (template) ✅
- §3 rename item 1 "TIM br" → Task 1 template ✅; numeração 1–6+0 → template + patch preserva rotas ✅
- §4 pipeline (HTML→Playwright→base64 teste→Supabase→9a→push) → Tasks 1,2,3,4,5 ✅
- §5 tratamento de erros → build FileNotFound (T1), render assert (T2), send HTTPError exit (T3), URL 200 assert (T4), backup antes de PUT (T5) ✅
- §6 aceite → checkpoints humanos T3 e T5-step6 ✅

**2. Placeholder scan:** sem TBD/TODO; todo passo tem código ou comando real. ✅

**3. Type consistency:** `CAPTION` idêntica em T3 e T5; `build()/render()/patch()/main()` com assinaturas consistentes; nomes de nós (`9a. Enviar Menu`, `9a-img*`) batem com o que foi observado no JSON real. ✅

*© 2026 Fenice IT Justech.IA — by Tech Lead Ramão Bueno*
