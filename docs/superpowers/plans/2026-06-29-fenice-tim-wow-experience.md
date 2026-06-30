# Fenice Tim WOW Experience — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Quando um prospect preenche o formulário fenice.ia.br, recebe WhatsApp proativo com insight jurídico gratuito (WOW moment), e-mail de confirmação Microsoft 365, e entra automaticamente no bot Fenice Tim.

**Architecture:** FastAPI `/leads` salva no Supabase e dispara webhook N8N `fenice-leads`. O workflow N8N executa 4 ações em paralelo: notificação WhatsApp ao admin, e-mail ao prospect via Office365, insight WOW gerado pelo Groq, e WhatsApp proativo ao lead. O bot fenice-tim recebe o lead com área pré-salva — sem mostrar menu.

**Tech Stack:** FastAPI (Pydantic v2), N8N Cloud, Evolution API v2, Groq llama-3.3-70b, Office365 SMTP, Supabase REST, Vercel

## Global Constraints

- WhatsApp: sempre via Evolution API `https://evolution-api-9fbw.srv1784289.hstgr.cloud` — NUNCA via AvisaAPI
- Instância Evolution: `fenice-tim` | ApiKey: `XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7`
- Bot admin WhatsApp: `5547991041414` (recebe notificação) | Admin pessoal: `554797348385`
- SMTP: `smtp.office365.com:587` | User: `fenice_tech@fenice.ia.br` | Pass: `170962Ra@`
- Supabase URL: `https://qcfdssnpjzvjbvemhrik.supabase.co`
- N8N Cloud: `feniceit.app.n8n.cloud`
- BOT_SIGS obrigatório em toda msg do bot: `["🏛️", "© 2026", "👤 *Atendimento", "Atendimento encerrado"]`
- Deploy site: MANUAL via `vercel deploy --prod` — nunca auto-deploy
- Commit: sempre `git add -u` (nunca `-A` ou paths acentuados individualmente)
- Arquivo fonte N8N: `scripts/n8n_fenice_leads.json` (criar) e `scripts/n8n_fenice_tim_v4.json` (já existente)

---

## Task 1: FastAPI /leads — modelo + limpeza + webhook N8N

**Files:**
- Modify: `scripts/api_fenice_saas.py:138-142` (LeadRequest)
- Modify: `scripts/api_fenice_saas.py:934-1009` (_notificar_lead)
- Modify: `scripts/api_fenice_saas.py:1012-1063` (capturar_lead)

**Interfaces:**
- Produces: endpoint `POST /leads` que aceita `{ nome, telefone, email, empresa?, interesse, interesse_label, descricao_outros? }` e retorna `{ ok: true, mensagem: str }`
- Produces: POST para `N8N_WEBHOOK_LEADS` com payload completo

- [ ] **Step 1: Localizar e ler o modelo atual**

Abrir `scripts/api_fenice_saas.py` linha 138. Confirmar que `LeadRequest` tem apenas: `nome`, `email`, `empresa`, `interesse`.

- [ ] **Step 2: Atualizar LeadRequest (linhas 138-142)**

Substituir o bloco `class LeadRequest`:

```python
class LeadRequest(BaseModel):
    nome:             str           = Field(..., min_length=2, max_length=120)
    telefone:         str           = Field(..., description="Formato: 55XXXXXXXXXXX")
    email:            str           = Field(..., description="E-mail profissional")
    empresa:          Optional[str] = Field(None, max_length=120)
    interesse:        str           = Field(..., min_length=2, max_length=50,
                                           description="Área IVR: b2b|juridico|academico|observatorio|api|filosofia|outros")
    interesse_label:  str           = Field(..., min_length=2, max_length=100,
                                           description="Rótulo legível: 'B2B Corporativo', etc.")
    descricao_outros: Optional[str] = Field(None, max_length=80,
                                           description="Palavras-chave se interesse=outros")
```

- [ ] **Step 3: Substituir _notificar_lead — remover SMTP e AvisaAPI, manter só N8N**

Localizar a função `_notificar_lead` (linha ~934). Substituir **toda a função** por:

```python
async def _notificar_lead(lead: LeadRequest) -> None:
    """Dispara N8N fenice-leads webhook em background. Falha silenciosa."""
    n8n_url = os.environ.get("N8N_WEBHOOK_LEADS", "")
    if not n8n_url:
        print("[leads] N8N_WEBHOOK_LEADS não configurado — pulando notificação")
        return
    payload = {
        "evento":            "novo_lead",
        "nome":              lead.nome,
        "telefone":          lead.telefone,
        "email":             lead.email,
        "empresa":           lead.empresa or "",
        "interesse":         lead.interesse,
        "interesse_label":   lead.interesse_label,
        "descricao_outros":  lead.descricao_outros or "",
        "origem":            "fenice.ia.br/contato",
        "timestamp":         datetime.utcnow().isoformat() + "Z",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(n8n_url, json=payload)
    except Exception as exc:
        print(f"[leads] N8N webhook falhou: {exc}")
```

- [ ] **Step 4: Atualizar capturar_lead — validar telefone + salvar com numero=telefone**

Localizar `@app.post("/leads"` (linha ~1012). Substituir o corpo da função:

```python
@app.post("/leads", tags=["Free"], summary="Captura de leads (contato comercial)")
async def capturar_lead(body: LeadRequest) -> dict:
    import re as _re_lead
    # validar email
    if not _re_lead.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", body.email):
        raise HTTPException(status_code=422, detail="E-mail inválido.")
    # validar e normalizar telefone: aceita 10-15 dígitos, adiciona 55 se necessário
    tel = _re_lead.sub(r"[^0-9]", "", body.telefone)
    if len(tel) == 11:
        tel = "55" + tel
    if not _re_lead.match(r"^55\d{10,11}$", tel):
        raise HTTPException(status_code=422, detail="Telefone inválido. Use formato (XX) XXXXX-XXXX.")
    body = body.model_copy(update={"telefone": tel})

    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Banco de dados não configurado.")

    hdrs = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }
    payload = {
        "numero":  tel,
        "nome":    body.nome,
        "area":    body.interesse,
        "estagio": "lead_site",
        "dados":   {
            "email":            body.email,
            "empresa":          body.empresa,
            "interesse_label":  body.interesse_label,
            "descricao_outros": body.descricao_outros,
        },
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            f"{sb_url}/rest/v1/fenice_tim_contatos",
            headers=hdrs,
            params={"on_conflict": "numero"},
            json=payload,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"Erro ao salvar lead: {r.text[:200]}")

    import asyncio
    asyncio.create_task(_notificar_lead(body))
    return {"ok": True, "mensagem": "Recebemos seu contato! Em instantes você receberá uma mensagem no WhatsApp."}
```

- [ ] **Step 5: Verificar que não há mais referências a AvisaAPI ou smtp no bloco /leads**

```powershell
Select-String -Path "scripts\api_fenice_saas.py" -Pattern "avisa|smtp|SMTP_PASS|SMTP_USER" | Where-Object { $_.LineNumber -gt 900 -and $_.LineNumber -lt 1100 }
```

Resultado esperado: nenhuma linha com essas referências no bloco de leads.

- [ ] **Step 6: Commit**

```bash
git add -u
git commit -m "feat(leads): telefone obrigatório + modelo atualizado + N8N webhook (remove SMTP/AvisaAPI)"
```

---

## Task 2: Frontend — campo telefone + modal de assunto

**Files:**
- Modify: `scripts/landing.html:1873-1889` (HTML do formulário)
- Modify: `scripts/landing.html:3004-3054` (JS do formulário)

**Interfaces:**
- Consumes: endpoint `POST /leads` da Task 1 com campos `{ nome, telefone, email, empresa?, interesse, interesse_label, descricao_outros? }`
- Produces: formulário com 5 campos + modal de assunto com 7 opções

- [ ] **Step 1: Substituir o HTML do formulário (linhas 1873-1889)**

Localizar o bloco `<form id="leads-form"` e substituir por:

```html
<form id="leads-form" novalidate>
  <div style="display:flex;flex-direction:column;gap:0.85rem;">
    <input id="lead-nome" type="text" placeholder="Seu nome completo *" required maxlength="120"
           class="lead-input">
    <input id="lead-telefone" type="tel" placeholder="WhatsApp: (XX) XXXXX-XXXX *" required
           class="lead-input" maxlength="16" autocomplete="tel">
    <input id="lead-email" type="email" placeholder="E-mail profissional *" required
           class="lead-input">
    <input id="lead-empresa" type="text" placeholder="Escritório ou empresa (opcional)" maxlength="120"
           class="lead-input">
    <!-- Seletor de assunto via modal -->
    <button type="button" id="lead-assunto-btn" class="lead-input" aria-haspopup="dialog"
            style="text-align:left;cursor:pointer;color:rgba(255,255,255,0.45);background:transparent;">
      Assunto *
    </button>
    <input type="hidden" id="lead-interesse" required>
    <input type="hidden" id="lead-interesse-label">
    <!-- Campo Outros (aparece só quando selecionado) -->
    <div id="lead-outros-wrap" style="display:none;">
      <input id="lead-outros" type="text" maxlength="80"
             placeholder="Descreva em palavras-chave (ex: startup, projeto social) *"
             class="lead-input">
    </div>
    <button type="submit" class="btn-primary" id="lead-btn"
            style="margin-top:0.4rem;width:100%;justify-content:center;cursor:pointer;border:none;">
      Enviar mensagem
    </button>
  </div>
  <p id="lead-msg" style="margin-top:0.9rem;font-size:0.9rem;min-height:1.4rem;text-align:center;"></p>
</form>

<!-- Modal de assunto -->
<div id="assunto-modal" role="dialog" aria-modal="true" aria-label="Selecione o assunto"
     style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9000;
            align-items:center;justify-content:center;">
  <div style="background:#1a1a2e;border:1px solid rgba(201,162,39,0.3);border-radius:1rem;
              padding:2rem;max-width:400px;width:90%;max-height:90vh;overflow-y:auto;">
    <h3 style="color:#C9A227;margin:0 0 1.2rem;font-size:1.1rem;">Qual é o seu interesse?</h3>
    <div style="display:flex;flex-direction:column;gap:0.6rem;" id="assunto-opcoes">
      <button class="assunto-opt" data-value="b2b"          data-label="B2B Corporativo">🏢  B2B Corporativo</button>
      <button class="assunto-opt" data-value="juridico"     data-label="Consultoria Jurídica">⚖️  Consultoria Jurídica</button>
      <button class="assunto-opt" data-value="academico"    data-label="Ensino Acadêmico">🎓  Ensino Acadêmico</button>
      <button class="assunto-opt" data-value="observatorio" data-label="Observatório da Mulher">👁️  Observatório da Mulher</button>
      <button class="assunto-opt" data-value="api"          data-label="API &amp; Desenvolvedores">⚡  API &amp; Desenvolvedores</button>
      <button class="assunto-opt" data-value="filosofia"    data-label="Filosofia &amp; Teologia">🧠  Filosofia &amp; Teologia</button>
      <button class="assunto-opt" data-value="outros"       data-label="Outros">💬  Outros</button>
    </div>
    <button id="assunto-fechar" style="margin-top:1rem;background:none;border:none;color:rgba(255,255,255,0.4);
            cursor:pointer;font-size:0.85rem;">✕ Fechar</button>
  </div>
</div>
```

Adicionar ao `<style>` existente:

```css
.assunto-opt {
  background: rgba(201,162,39,0.08);
  border: 1px solid rgba(201,162,39,0.2);
  border-radius: 0.5rem;
  color: rgba(255,255,255,0.85);
  padding: 0.75rem 1rem;
  text-align: left;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.assunto-opt:hover { background: rgba(201,162,39,0.18); }
.assunto-opt.selected { background: rgba(201,162,39,0.25); border-color: #C9A227; color: #C9A227; }
```

- [ ] **Step 2: Substituir o JS do formulário (bloco `/* ── LEADS FORM ── */`)**

Substituir o bloco inteiro `(function () { ... })();` do leads form:

```javascript
/* ── LEADS FORM ── */
(function () {
  const form    = document.getElementById('leads-form');
  const msgEl   = document.getElementById('lead-msg');
  const btn     = document.getElementById('lead-btn');
  const modal   = document.getElementById('assunto-modal');
  const assBtn  = document.getElementById('lead-assunto-btn');
  const outWrap = document.getElementById('lead-outros-wrap');
  if (!form) return;

  // Máscara telefone: (XX) XXXXX-XXXX
  document.getElementById('lead-telefone').addEventListener('input', function () {
    let v = this.value.replace(/\D/g, '').substring(0, 11);
    if (v.length > 6) v = '(' + v.substring(0,2) + ') ' + v.substring(2,7) + '-' + v.substring(7);
    else if (v.length > 2) v = '(' + v.substring(0,2) + ') ' + v.substring(2);
    else if (v.length > 0) v = '(' + v;
    this.value = v;
  });

  // Abrir modal de assunto
  assBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    modal.focus();
  });

  // Fechar modal
  document.getElementById('assunto-fechar').addEventListener('click', () => {
    modal.style.display = 'none';
  });
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
  });

  // Selecionar opção
  document.querySelectorAll('.assunto-opt').forEach(opt => {
    opt.addEventListener('click', () => {
      document.querySelectorAll('.assunto-opt').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      const value = opt.dataset.value;
      const label = opt.dataset.label;
      document.getElementById('lead-interesse').value = value;
      document.getElementById('lead-interesse-label').value = label;
      assBtn.textContent = label;
      assBtn.style.color = '#C9A227';
      outWrap.style.display = value === 'outros' ? 'block' : 'none';
      if (value !== 'outros') document.getElementById('lead-outros').value = '';
      modal.style.display = 'none';
    });
  });

  // Submit
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome     = document.getElementById('lead-nome').value.trim();
    const telRaw   = document.getElementById('lead-telefone').value.trim();
    const email    = document.getElementById('lead-email').value.trim();
    const empresa  = document.getElementById('lead-empresa').value.trim();
    const interesse       = document.getElementById('lead-interesse').value;
    const interesseLabel  = document.getElementById('lead-interesse-label').value;
    const outros   = document.getElementById('lead-outros').value.trim();

    if (!nome || !telRaw || !email || !interesse) {
      msgEl.style.color = '#f87171';
      msgEl.textContent = 'Preencha todos os campos obrigatórios (*).';
      return;
    }
    if (interesse === 'outros' && !outros) {
      msgEl.style.color = '#f87171';
      msgEl.textContent = 'Descreva o assunto em palavras-chave.';
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Enviando…';
    msgEl.style.color = '';
    msgEl.textContent = '';

    try {
      const body = { nome, telefone: telRaw, email, interesse, interesse_label: interesseLabel };
      if (empresa) body.empresa = empresa;
      if (outros)  body.descricao_outros = outros;

      const res  = await fetch('/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        msgEl.style.color = '#34d399';
        msgEl.textContent = '✅ ' + data.mensagem;
        form.reset();
        assBtn.textContent = 'Assunto *';
        assBtn.style.color = 'rgba(255,255,255,0.45)';
        outWrap.style.display = 'none';
        document.querySelectorAll('.assunto-opt').forEach(o => o.classList.remove('selected'));
      } else {
        msgEl.style.color = '#f87171';
        msgEl.textContent = data.detail || 'Erro ao enviar. Tente novamente.';
      }
    } catch {
      msgEl.style.color = '#f87171';
      msgEl.textContent = 'Erro de conexão. Tente novamente.';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Enviar mensagem';
    }
  });
})();
```

- [ ] **Step 3: Testar no browser localmente**

```powershell
Start-Process "C:\Fenice_bRain\scripts\landing.html"
```

Verificar:
- Campo telefone aplica máscara `(XX) XXXXX-XXXX`
- Botão "Assunto *" abre modal com 7 opções
- Seleção "Outros" exibe campo de palavras-chave
- Botão "Enviar mensagem" fica ativo após preencher todos os campos

- [ ] **Step 4: Commit**

```bash
git add -u
git commit -m "feat(frontend): campo telefone + modal assunto 7 opções + WOW UX"
```

---

## Task 3: N8N workflow fenice-leads (novo JSON)

**Files:**
- Create: `scripts/n8n_fenice_leads.json`
- Modify: `scripts/n8n_fenice_tim_v4.json` (prompt Groq — adicionar Zappos rules)

**Interfaces:**
- Consumes: webhook POST de `N8N_WEBHOOK_LEADS` com campos da Task 1
- Produces: workflow importável no N8N Cloud com 5 nós

- [ ] **Step 1: Criar scripts/n8n_fenice_leads.json**

Criar o arquivo com o seguinte conteúdo:

```json
{
  "name": "Fenice Tim — fenice-leads (WOW Experience)",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "fenice-leads",
        "responseMode": "onReceived",
        "options": {}
      },
      "name": "1. Receber Lead do Site",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [160, 400]
    },
    {
      "parameters": {
        "jsCode": "const d = $input.first().json?.body || $input.first().json;\nconst nome = d.nome || 'Cliente';\nconst primeiroNome = nome.split(' ')[0];\nconst telefone = d.telefone || '';\nconst email = d.email || '';\nconst empresa = d.empresa || '';\nconst interesse = d.interesse || 'juridico';\nconst interesseLabel = d.interesse_label || interesse;\nconst descricaoOutros = d.descricao_outros || '';\nconst temaParaGroq = interesse === 'outros' ? (descricaoOutros || 'direito e tecnologia') : interesseLabel;\n\nconst groqBody = JSON.stringify({\n  model: 'llama-3.3-70b-versatile',\n  messages: [\n    {\n      role: 'system',\n      content: 'Você é o Téo, assistente jurídico-filosófico da Fenice IT. Responda APENAS com o insight, sem introdução, sem aspas, sem formatação markdown. Máximo 2 linhas curtas.'\n    },\n    {\n      role: 'user',\n      content: `Um prospect se interessou por: ${temaParaGroq}. Gere 1 insight jurídico ou filosófico surpreendente e relevante sobre este tema. Tom: inteligente, caloroso, acessível.`\n    }\n  ],\n  max_tokens: 120,\n  temperature: 0.8\n});\n\nreturn [{ json: { nome, primeiroNome, telefone, email, empresa, interesse, interesseLabel, descricaoOutros, temaParaGroq, groqBody } }];"
      },
      "name": "2. Preparar Dados + Prompt Groq",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [380, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "Authorization", "value": "Bearer {{GROQ_API_KEY_N8N}}" },
            { "name": "Content-Type",  "value": "application/json" }
          ]
        },
        "sendBody": true,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": "={{ $json.groqBody }}",
        "options": { "timeout": 15000 }
      },
      "name": "3. Groq — WOW Insight",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [600, 400],
      "continueOnFail": true
    },
    {
      "parameters": {
        "jsCode": "const dados = $('2. Preparar Dados + Prompt Groq').first().json;\nconst groqResp = $input.first().json;\nlet wowInsight = 'A Fenice IT combina inteligência artificial, filosofia e direito para entregar o que nenhuma LegalTech brasileira oferece.';\ntry {\n  const msg = groqResp?.choices?.[0]?.message?.content;\n  if (msg && msg.length > 10) wowInsight = msg.trim();\n} catch(e) {}\nreturn [{ json: { ...dados, wowInsight } }];"
      },
      "name": "4. Extrair WOW Insight",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [820, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://evolution-api-9fbw.srv1784289.hstgr.cloud/message/sendText/fenice-tim",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "apikey",        "value": "XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7" },
            { "name": "Content-Type",  "value": "application/json" }
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            { "name": "number", "value": "5547991041414" },
            { "name": "text",   "value": "={{ '🏛️ *Novo Lead — Fenice IT*\\n\\n👤 *Nome:* ' + $json.nome + '\\n📱 *WhatsApp:* +' + $json.telefone + '\\n📧 *E-mail:* ' + $json.email + '\\n🏢 *Empresa:* ' + ($json.empresa || '—') + '\\n💼 *Assunto:* ' + $json.interesseLabel + ($json.descricaoOutros ? '\\n📝 *Detalhe:* ' + $json.descricaoOutros : '') + '\\n\\n_Lead salvo no Supabase · área: ' + $json.interesse + '_\\n© 2026 Fenice IT · Justech.IA' }}"
          ]
        },
        "options": { "timeout": 15000 }
      },
      "name": "5a. WhatsApp Admin",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [1040, 200],
      "continueOnFail": true
    },
    {
      "parameters": {
        "fromEmail": "fenice_tech@fenice.ia.br",
        "toEmail": "={{ $('4. Extrair WOW Insight').item.json.email }}",
        "subject": "={{ 'Fenice IA recebeu seu contato, ' + $('4. Extrair WOW Insight').item.json.primeiroNome + '!' }}",
        "emailType": "text",
        "message": "={{ 'Olá, ' + $('4. Extrair WOW Insight').item.json.primeiroNome + '!\\n\\nFicamos muito felizes com seu interesse em ' + $('4. Extrair WOW Insight').item.json.interesseLabel + '.\\n\\nNossa equipe já foi notificada e em instantes o Téo, nosso assistente inteligente, vai entrar em contato pelo seu WhatsApp para uma conversa inicial sobre como podemos ajudar.\\n\\nEnquanto isso, saiba que a Fenice IT combina inteligência artificial, filosofia e direito para entregar soluções que nenhuma LegalTech brasileira oferece.\\n\\nAté já!\\nEquipe Fenice IT · Justech.IA\\nhttps://fenice.ia.br' }}",
        "options": {}
      },
      "name": "5b. E-mail Prospect (Office365)",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2.1,
      "position": [1040, 400],
      "continueOnFail": true,
      "credentials": {
        "smtp": {
          "id": "{{SMTP_CREDENTIAL_ID}}",
          "name": "Fenice Office365"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://evolution-api-9fbw.srv1784289.hstgr.cloud/message/sendText/fenice-tim",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "apikey",       "value": "XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7" },
            { "name": "Content-Type", "value": "application/json" }
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            { "name": "number", "value": "={{ $('4. Extrair WOW Insight').item.json.telefone }}" },
            { "name": "text",   "value": "={{ 'Olá, ' + $('4. Extrair WOW Insight').item.json.primeiroNome + '! 🏛️\\n\\nSou o *Téo*, assistente inteligente da *Fenice IT · Justech.IA*.\\n\\nVi que você tem interesse em *' + $('4. Extrair WOW Insight').item.json.interesseLabel + '* — ótima escolha!\\n\\n💡 *Você sabia?*\\n' + $('4. Extrair WOW Insight').item.json.wowInsight + '\\n\\nPosso te contar mais sobre como a Fenice IT pode ajudar com ' + $('4. Extrair WOW Insight').item.json.interesseLabel + '? É só responder aqui. 😊\\n\\n© 2026 Fenice IT · Justech.IA' }}"
          ]
        },
        "options": { "timeout": 15000 }
      },
      "name": "5c. WhatsApp Proativo Lead (WOW)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [1040, 600],
      "continueOnFail": true
    }
  ],
  "connections": {
    "1. Receber Lead do Site": {
      "main": [[{ "node": "2. Preparar Dados + Prompt Groq", "type": "main", "index": 0 }]]
    },
    "2. Preparar Dados + Prompt Groq": {
      "main": [[{ "node": "3. Groq — WOW Insight", "type": "main", "index": 0 }]]
    },
    "3. Groq — WOW Insight": {
      "main": [[{ "node": "4. Extrair WOW Insight", "type": "main", "index": 0 }]]
    },
    "4. Extrair WOW Insight": {
      "main": [
        [
          { "node": "5a. WhatsApp Admin",             "type": "main", "index": 0 },
          { "node": "5b. E-mail Prospect (Office365)", "type": "main", "index": 0 },
          { "node": "5c. WhatsApp Proativo Lead (WOW)","type": "main", "index": 0 }
        ]
      ]
    }
  },
  "settings": { "executionOrder": "v1" }
}
```

- [ ] **Step 2: Atualizar prompt Groq no fenice-tim (Zappos rules)**

Localizar nó "10. Montar Prompt por Área" em `scripts/n8n_fenice_tim_v4.json` (linha ~454). Encontrar onde o `system` prompt é montado e adicionar as regras Zappos ao final do system message:

Dentro do código JS do nó 10, localizar a linha que define `systemMsg` e adicionar ao final:

```javascript
systemMsg += '\n\nREGRAS DE ATENDIMENTO FENICE TIM:\n1. Sempre endereçar pelo primeiro nome\n2. Nunca usar "não sei" ou "não posso" — sempre próximo passo\n3. Se não tiver a informação: "Deixa eu verificar — um momento!"\n4. Tom: inteligente, caloroso, sem juridiquês\n5. Sempre encerrar com pergunta ou próximo passo concreto';
```

- [ ] **Step 3: Validar JSON fenice-leads**

```bash
python -c "import json; json.load(open('scripts/n8n_fenice_leads.json', encoding='utf-8')); print('JSON OK')"
```

Resultado esperado: `JSON OK`

- [ ] **Step 4: Commit**

```bash
git add -u
git commit -m "feat(n8n): workflow fenice-leads WOW Experience + Zappos rules no Téo"
```

---

## Task 4: Deploy + Configuração + Teste

**Files:**
- Config: Vercel env vars (via CLI)
- Config: N8N Cloud (import via UI)
- Config: N8N SMTP credential (via UI)

**Interfaces:**
- Consumes: todos os arquivos commitados nas Tasks 1-3
- Produces: sistema em produção testado contra critérios de aceitação

- [ ] **Step 1: Adicionar N8N_WEBHOOK_LEADS no Vercel**

```powershell
cd C:\Fenice_bRain
vercel env add N8N_WEBHOOK_LEADS production
```

Quando perguntado o valor, digitar:
```
https://feniceit.app.n8n.cloud/webhook/fenice-leads
```

- [ ] **Step 2: Deploy Vercel**

```powershell
vercel deploy --prod
```

Aguardar `Production: https://fenice.ia.br` na saída.

- [ ] **Step 3: Importar fenice-leads no N8N Cloud**

1. Acessar `https://feniceit.app.n8n.cloud`
2. Menu lateral → **Workflows** → **Import from file**
3. Selecionar `C:\Fenice_bRain\scripts\n8n_fenice_leads.json`
4. Após importar, **ativar** o workflow (toggle no canto superior direito)

- [ ] **Step 4: Configurar credencial SMTP Office365 no N8N**

1. No N8N, ir em **Credentials** → **New** → buscar **SMTP**
2. Preencher:
   - Host: `smtp.office365.com`
   - Port: `587`
   - SSL: `STARTTLS`
   - User: `fenice_tech@fenice.ia.br`
   - Password: `170962Ra@`
   - Nome da credencial: `Fenice Office365`
3. Salvar e testar conexão
4. Abrir o workflow `fenice-leads`, editar o nó `5b. E-mail Prospect (Office365)`, selecionar a credencial `Fenice Office365`

- [ ] **Step 5: Importar fenice-tim v4 atualizado no N8N Cloud**

1. No N8N, abrir o workflow `Fenice_Tim — WhatsApp IVR v4`
2. Menu → **Import from file**
3. Selecionar `C:\Fenice_bRain\scripts\n8n_fenice_tim_v4.json`
4. Confirmar a substituição e **reativar** o workflow

- [ ] **Step 6: Teste de aceitação — Lead completo**

Abrir `https://fenice.ia.br` e preencher o formulário com dados reais:
- Nome: `Teste WOW`
- Telefone: `(47) 99104-1414` (número pessoal de Ramão)
- E-mail: `oiconsulbrasil@gmail.com`
- Assunto: `Consultoria Jurídica`

Verificar em < 60 segundos:
- [ ] Admin recebe WhatsApp em `5547991041414` com os dados do lead
- [ ] Lead recebe WhatsApp proativo em `5547991041414` com WOW insight do Groq
- [ ] Lead recebe e-mail de confirmação em `oiconsulbrasil@gmail.com`
- [ ] Lead salvo no Supabase: `fenice_tim_contatos` com `area=juridico, estagio=lead_site`

- [ ] **Step 7: Teste de continuidade — "oi" após cadastro**

No WhatsApp `5547991041414`, responder "oi" para o bot.

Resultado esperado: bot responde na área `juridico` sem mostrar o menu principal.

- [ ] **Step 8: Commit final**

```bash
git add -u
git commit -m "chore(deploy): WOW Experience em produção — fenice-leads + formulário + Téo Zappos"
```

---

## Self-Review

**Spec coverage checklist:**
- ✅ Campo telefone no formulário (Task 2)
- ✅ Modal de assunto com 7 opções incluindo Outros (Task 2)
- ✅ FastAPI valida e normaliza telefone (Task 1)
- ✅ Lead salvo com `numero=telefone, area=interesse` (Task 1)
- ✅ WhatsApp admin notificado (Task 3 — nó 5a)
- ✅ E-mail prospect via Office365 (Task 3 — nó 5b)
- ✅ WOW insight via Groq (Task 3 — nós 3+4)
- ✅ WhatsApp proativo ao lead com WOW (Task 3 — nó 5c)
- ✅ BOT_SIGS em toda msg do bot (nó 5c contém `🏛️` e `© 2026`)
- ✅ Zappos rules no prompt do Téo (Task 3 — step 2)
- ✅ AvisaAPI removida do FastAPI (Task 1)
- ✅ Testes de aceitação (Task 4)

**Tipo de execução recomendado:** Inline (Tasks são sequenciais — cada uma depende da anterior para teste completo)

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*  
*Fenice IT · WOW Experience — Nubank + Zappos · 2026-06-29*
