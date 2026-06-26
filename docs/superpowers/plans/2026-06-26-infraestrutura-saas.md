# Infraestrutura SaaS — Plano de Implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: Use `superpowers:executing-plans` para executar tarefa a tarefa.

**Goal:** Validar e colocar em produção o RAG semântico jurídico + corrigir 3 gaps de frontend (login, D3 graph, formulário de leads).

**Architecture:** FastAPI (Vercel) → pgvector (Supabase) via `fenice_rag_semantic.py`; frontend SPA em `landing.html` servido como rota GET `/` da API.

**Tech Stack:** Python 3.11, FastAPI, sentence-transformers (local), Groq llama-3.3-70b, Supabase pgvector, D3.js v7, Vercel serverless

## Estado Atual (2026-06-26)

| Componente | Status |
|---|---|
| `fenice_rag_semantic.py` | ✅ implementado |
| `fenice_ingestor.py` | ✅ implementado |
| `api_fenice_saas.py` endpoint `/analisar/semantico` | ✅ implementado |
| Supabase `documentos_juridicos` | ✅ 4.269 rows |
| Supabase `documentos_chunks` (embeddings 1024d) | ✅ 4.269 rows |
| Supabase RPC `match_chunks` | ✅ funcional |
| `requirements-local.txt` com sentence-transformers | ✅ |
| Login modal no frontend | ✅ código presente |
| D3 graph no frontend | ✅ código presente |
| Formulário de leads | ❌ ausente |
| Deploy Vercel validado | ⏳ pendente |

## Global Constraints

- Python ≥ 3.11; FastAPI ≥ 0.111; supabase-py ≥ 2.4
- `torch` e `sentence-transformers` **nunca vão para o Vercel** (serverless)
- O Vercel serve o endpoint `/analisar/semantico` como `503` quando sem torch — comportamento esperado e documentado
- `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` devem estar no painel Vercel
- Formulário de leads salva em `fenice_tim_contatos` (tabela existente no Supabase)
- Não alterar nenhum endpoint existente — apenas adicionar

---

### Task 1: Testar pipeline RAG localmente

**Files:**
- Modify: `requirements-local.txt` (só verificação, não deve precisar alterar)
- Test: rodar `scripts/fenice_rag_semantic.py` diretamente

**Interfaces:**
- Produz: confirmação de que `RAGEngine.query()` retorna `{"resposta": "...", "fontes": [...], "confianca": "alta"|"média"}`

- [ ] **Step 1: Instalar dependências locais**

```bash
cd C:\Fenice_bRain
pip install -r requirements-local.txt
```

Esperado: pacotes instalados sem erro (sentence-transformers baixa o modelo na primeira execução, ~2.6GB).

- [ ] **Step 2: Rodar o motor semântico diretamente**

```bash
cd C:\Fenice_bRain
python scripts/fenice_rag_semantic.py "Quais as penas para homicídio doloso no Código Penal?"
```

Esperado:
```
[RAGEngine] Carregando intfloat/multilingual-e5-large na CPU...
[RAGEngine] Motor semântico pronto.

PERGUNTA: Quais as penas para homicídio doloso...
CONFIANÇA: alta
RESPOSTA: De acordo com o Art. 121 do CP...
FONTES (3):
  CP Art. 121 — similarity: 0.91 — vigente: True
```

Se `CONFIANÇA: insuficiente` — a tabela tem dados mas nenhum chunk se encaixa. Verificar:

```bash
# Confirmar que chunks têm embeddings não-nulos
curl -s "https://qcfdssnpjzvjbvemhrik.supabase.co/rest/v1/documentos_chunks?select=id,embedding&limit=1&not.embedding=is.null" \
  -H "apikey: $(grep SUPABASE_SERVICE_KEY C:\Fenice_bRain\.env | cut -d= -f2)" | head -c 200
```

- [ ] **Step 3: Testar via API local**

```bash
# Terminal 1 — iniciar API local
cd C:\Fenice_bRain
uvicorn scripts.api_fenice_saas:app --reload --port 8001
```

```bash
# Terminal 2 — chamar endpoint semântico
curl -s -X POST http://localhost:8001/analisar/semantico \
  -H "Content-Type: application/json" \
  -H "X-Fenice-Key: fenice_premium_internal_2026" \
  -d '{"pergunta": "contrato verbal tem validade?"}' | python -m json.tool
```

Esperado: JSON com `resposta`, `fontes` (≥ 1), `confianca: "alta"` ou `"média"`.

- [ ] **Step 4: Commit**

```bash
git add requirements-local.txt  # se precisou alterar
git commit -m "test: validação local do RAG semântico"
```

---

### Task 2: Verificar e corrigir login no site de produção

**Files:**
- Verify: `scripts/landing.html` (linhas 1920–1996)
- Verify: `scripts/api_fenice_saas.py` endpoint `/auth` (linha 263)
- Possibly modify: `scripts/landing.html` se houver bug

**Interfaces:**
- Consome: endpoint `POST /auth` com `{usuario, senha}`, retorna `{ok: true, token: "fenice_<ts>_<sig>"}`
- Produz: modal fecha ao fazer login com `admin` / `fenice@2025`

- [ ] **Step 1: Verificar variáveis de ambiente no Vercel**

Acesse: https://vercel.com/ramao-bueno/fenice-justech/settings/environment-variables

Confirme que as seguintes vars existem em **Production**:
- `SITE_USER` = `admin`
- `SITE_PASS` = `fenice@2025`
- `SITE_SECRET` = `fenice_secret_local`
- `SUPABASE_URL` = `https://qcfdssnpjzvjbvemhrik.supabase.co`
- `SUPABASE_SERVICE_KEY` = (o JWT longo)
- `GROQ_API_KEY` = (o gsk_...)

Se alguma estiver faltando, adicionar pelo painel ou via CLI:

```bash
# Instalar CLI Vercel se não estiver
npm i -g vercel

# Adicionar var de ambiente
vercel env add SITE_PASS production
# digitar: fenice@2025
```

- [ ] **Step 2: Testar /auth diretamente em produção**

```bash
curl -s -X POST https://fenice.ia.br/auth \
  -H "Content-Type: application/json" \
  -d '{"usuario": "admin", "senha": "fenice@2025"}' | python -m json.tool
```

Esperado: `{"ok": true, "token": "fenice_<timestamp>_<sig>"}`

Se retornar `503 SITE_PASS não configurado` → adicionar env var no Vercel e fazer re-deploy.

Se retornar `404` → o deploy do Vercel não incluiu o arquivo `api/index.py` correto.

- [ ] **Step 3: Testar login no browser**

Abrir https://fenice.ia.br — modal de login deve aparecer.  
Inserir `admin` / `fenice@2025` → modal deve fechar.

Se o modal aparecer mas o login não funcionar: abrir Console do browser (F12) e verificar a resposta da request para `/auth`.

- [ ] **Step 4: Se o modal não aparecer** 

Verificar no browser console se há erro de script. O overlay `#fenice-overlay` tem `display: flex` por padrão — se não aparecer, pode ser CSS sobreposto.

Adicionar temporariamente ao `landing.html` para debug:
```javascript
// No console do browser:
document.getElementById('fenice-overlay').style.display = 'flex';
```

- [ ] **Step 5: Commit se houver correção no landing.html**

```bash
git add scripts/landing.html
git commit -m "fix: login modal — corrige abertura/autenticação"
```

---

### Task 3: Verificar e corrigir D3 graph

**Files:**
- Verify: `scripts/landing.html` (seção D3, ~linha 2230)
- Verify: `scripts/api_fenice_saas.py` endpoint GET `/grafo`

**Interfaces:**
- Consome: `GET /grafo` → `{nos: [...], arestas: [...], amostra_legislacao: [...]}`
- Produz: grafo D3 visível na seção "Mapa de Conhecimento"

- [ ] **Step 1: Testar endpoint /grafo**

```bash
curl -s https://fenice.ia.br/grafo | python -m json.tool | head -50
```

Esperado: JSON com `nos` e `arestas` (arrays com ao menos alguns itens).

Se retornar `[]` ou arrays vazios → as tabelas `grafo_nos` e `grafo_arestas` no Supabase estão vazias.  
Verificar:

```bash
curl -s "https://qcfdssnpjzvjbvemhrik.supabase.co/rest/v1/grafo_nos?select=count" \
  -H "apikey: $(grep SUPABASE_SERVICE_KEY C:\Fenice_bRain\.env | cut -d= -f2)" \
  -H "Prefer: count=exact"
```

- [ ] **Step 2: Verificar renderização no browser**

Abrir https://fenice.ia.br, fazer login, e navegar até a seção do grafo.  
Console F12 → verificar se há erros relacionados ao D3.

Se `D3 is not defined` → o CDN do D3 está bloqueado. Verificar a linha:

```html
<!-- scripts/landing.html ~linha 2230 -->
s.src = 'https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js';
```

Alternativa se o CDN falhar — substituir por:
```html
s.src = 'https://unpkg.com/d3@7/dist/d3.min.js';
```

- [ ] **Step 3: Se grafo_nos estiver vazio**

O grafo precisa ser populado. Verificar se há script de população:

```bash
ls C:\Fenice_bRain\scripts\ | grep -i grafo
```

Se existir `gerar_grafo.py` ou similar, rodar. Se não existir, o grafo estará vazio até que um pipeline de população seja criado — deixar como item futuro.

- [ ] **Step 4: Commit se houver correção**

```bash
git add scripts/landing.html
git commit -m "fix: D3 graph — corrige carregamento e renderização"
```

---

### Task 4: Adicionar formulário de leads ao landing.html

**Files:**
- Modify: `scripts/landing.html` — adicionar seção de leads antes do footer
- Modify: `scripts/api_fenice_saas.py` — adicionar endpoint `POST /leads`

**Interfaces:**
- Produz: `POST /leads` aceita `{nome, email, empresa?, interesse}` e salva em `fenice_tim_contatos`
- Produz: formulário HTML visível na landing, com validação e feedback visual

- [ ] **Step 1: Adicionar endpoint POST /leads na API**

Em `scripts/api_fenice_saas.py`, após o endpoint `/tcc` (por volta da linha 770), adicionar:

```python
class LeadRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    empresa: Optional[str] = Field(None, max_length=120)
    interesse: str = Field(..., min_length=3, max_length=200)

@app.post("/leads", tags=["Free"], summary="Captura de leads (contato comercial)")
async def capturar_lead(body: LeadRequest) -> dict:
    try:
        _sb().table("fenice_tim_contatos").insert({
            "nome": body.nome,
            "telefone": body.email,   # campo reutilizado para email
            "area":     body.interesse,
            "status":   "lead_site",
        }).execute()
        return {"ok": True, "mensagem": "Recebemos seu contato! Retornaremos em breve."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
```

*Nota: `fenice_tim_contatos` usa `telefone` como campo livre — reutilizamos para email de lead.*

- [ ] **Step 2: Escrever o teste do endpoint**

```bash
curl -s -X POST http://localhost:8001/leads \
  -H "Content-Type: application/json" \
  -d '{"nome":"Dr. Teste Silva","email":"teste@escritorio.adv.br","empresa":"Escritório Silva","interesse":"Busca semântica de jurisprudência"}' | python -m json.tool
```

Esperado: `{"ok": true, "mensagem": "Recebemos seu contato!..."}`

- [ ] **Step 3: Adicionar seção de leads no landing.html**

Localizar a tag `<!-- FOOTER -->` ou `<footer>` no `landing.html` e inserir antes dela:

```html
<!-- ── LEADS FORM ── -->
<section id="contato" class="section reveal" style="max-width:540px;margin:0 auto 5rem;text-align:center;">
  <p class="section-tag">Contato</p>
  <h2 class="section-title">Quer usar a Fenice IA no seu escritório?</h2>
  <p class="section-sub" style="margin-bottom:2rem;">Preencha o formulário e nossa equipe entra em contato em até 24h.</p>
  <form id="leads-form" style="display:flex;flex-direction:column;gap:1rem;">
    <input id="lead-nome"      type="text"  placeholder="Seu nome completo"          required maxlength="120"
           style="padding:0.8rem 1rem;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);font-family:inherit;font-size:0.95rem;">
    <input id="lead-email"     type="email" placeholder="E-mail profissional"        required
           style="padding:0.8rem 1rem;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);font-family:inherit;font-size:0.95rem;">
    <input id="lead-empresa"   type="text"  placeholder="Escritório / empresa (opcional)" maxlength="120"
           style="padding:0.8rem 1rem;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);font-family:inherit;font-size:0.95rem;">
    <input id="lead-interesse" type="text"  placeholder="O que você quer resolver?"  required maxlength="200"
           style="padding:0.8rem 1rem;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);font-family:inherit;font-size:0.95rem;">
    <button type="submit" class="btn-primary" id="lead-btn" style="margin-top:0.5rem;">
      Enviar mensagem
    </button>
    <p id="lead-msg" style="font-size:0.9rem;min-height:1.4rem;"></p>
  </form>
</section>
```

E o script correspondente (antes de `</body>`):

```html
<script>
(function () {
  const form   = document.getElementById('leads-form');
  const msgEl  = document.getElementById('lead-msg');
  const btn    = document.getElementById('lead-btn');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.textContent = 'Enviando…';
    msgEl.style.color = '';
    msgEl.textContent = '';

    const body = {
      nome:      document.getElementById('lead-nome').value.trim(),
      email:     document.getElementById('lead-email').value.trim(),
      empresa:   document.getElementById('lead-empresa').value.trim() || undefined,
      interesse: document.getElementById('lead-interesse').value.trim(),
    };

    try {
      const res  = await fetch('/leads', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) });
      const data = await res.json();
      if (res.ok) {
        msgEl.style.color = 'var(--free)';
        msgEl.textContent = data.mensagem;
        form.reset();
      } else {
        msgEl.style.color = '#f87171';
        msgEl.textContent = data.detail || 'Erro ao enviar. Tente novamente.';
      }
    } catch {
      msgEl.style.color = '#f87171';
      msgEl.textContent = 'Erro de conexão.';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Enviar mensagem';
    }
  });
})();
</script>
```

- [ ] **Step 4: Adicionar link "Contato" na nav**

Em `scripts/landing.html`, na `<ul class="nav-links">` (~linha 1340), adicionar:

```html
<li><a href="#contato">Contato</a></li>
```

- [ ] **Step 5: Testar formulário no browser local**

```bash
# Terminal 1
uvicorn scripts.api_fenice_saas:app --reload --port 8001

# Browser: abrir http://localhost:8001
# Preencher o formulário de contato e verificar:
# 1. Mensagem de sucesso aparece em verde
# 2. No Supabase: SELECT * FROM fenice_tim_contatos ORDER BY id DESC LIMIT 3;
```

- [ ] **Step 6: Commit**

```bash
git add scripts/landing.html scripts/api_fenice_saas.py
git commit -m "feat: adiciona formulário de leads e endpoint POST /leads"
```

---

### Task 5: Deploy para Vercel e validação em produção

**Files:**
- Verify: `api/index.py` (entry point Vercel)
- Verify: `vercel.json` (configuração de rotas)

**Interfaces:**
- Produz: todos os endpoints funcionando em `https://fenice.ia.br`
- Produz: `/analisar/semantico` retornando 503 esperado (sem torch) com mensagem clara

- [ ] **Step 1: Verificar api/index.py**

```bash
cat C:\Fenice_bRain\api\index.py
```

Deve conter `from scripts.api_fenice_saas import app` (ou equivalente).  
Se não existir:

```python
# api/index.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.api_fenice_saas import app
```

- [ ] **Step 2: Verificar vercel.json**

```bash
cat C:\Fenice_bRain\vercel.json
```

Deve ter rota catch-all para a API:

```json
{
  "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
}
```

- [ ] **Step 3: Commitar e fazer push**

```bash
git add -u
git push origin main
```

O Vercel auto-deploya (webhook configurado) ou acionar manualmente:

```bash
vercel --prod
```

- [ ] **Step 4: Verificar health em produção**

```bash
curl -s https://fenice.ia.br/health | python -m json.tool
```

Esperado:
```json
{
  "status": "ok",
  "db": "ok",
  "rag": "indisponível (sem torch)",
  "timestamp": "..."
}
```

- [ ] **Step 5: Testar todos os endpoints críticos em produção**

```bash
# Login
curl -s -X POST https://fenice.ia.br/auth \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin","senha":"fenice@2025"}'

# Busca keyword
curl -s -X POST https://fenice.ia.br/buscar \
  -H "Content-Type: application/json" \
  -d '{"query":"homicídio doloso","limite":3}' | python -m json.tool

# Leads
curl -s -X POST https://fenice.ia.br/leads \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste Prod","email":"prod@test.com","interesse":"validação"}' | python -m json.tool

# RAG (esperado 503 no Vercel)
curl -s -X POST https://fenice.ia.br/analisar/semantico \
  -H "Content-Type: application/json" \
  -H "X-Fenice-Key: fenice_premium_internal_2026" \
  -d '{"pergunta":"teste"}' | python -m json.tool
```

- [ ] **Step 6: Commit final**

```bash
git add .
git commit -m "deploy: infraestrutura SaaS v1 em produção — RAG local + leads form"
```

---

## Pós-Plano — Fase 2 (Mês 2)

Após validação local do RAG:

1. **Together.ai**: substituir `sentence-transformers` local por chamada HTTP `https://api.together.xyz/inference` com modelo `intfloat/multilingual-e5-large-instruct` — `pip install` remove `torch` do deploy.
2. **RAG no Vercel**: com Together.ai, o `/analisar/semantico` passa a funcionar em produção (sem torch).
3. **Planos pagos**: integrar Stripe para chaves premium por assinatura.

---

*Plano criado em 2026-06-26 — Ramão Bueno + Claude Sonnet 4.6*
