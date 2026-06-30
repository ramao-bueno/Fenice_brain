# Fenice Tim — WOW Experience Design Spec

**Data:** 2026-06-29  
**Status:** Aprovado  
**Autor:** Ramão Bueno + Claude Sonnet 4.6

---

## Visão Geral

Transformar o atendimento da Fenice IT em uma experiência de classe mundial,
combinando os princípios do **Nubank** (WOW moment, empatia, resolução em 1 toque)
e **Zappos** (autonomia, "nunca dizer não", conexão emocional) aplicados ao
contexto jurídico-tecnológico brasileiro via WhatsApp + N8N + Evolution API.

**Goal:** Quando um prospect preenche o formulário de contato em fenice.ia.br,
ele recebe uma experiência que o transforma em promotor da marca antes mesmo
de contratar qualquer serviço.

---

## Princípios WOW (Nubank + Zappos)

| Princípio | Origem | Implementação no Fenice Tim |
|---|---|---|
| WOW moment | Nubank | Dica jurídica/filosófica gratuita no 1º contato via Groq |
| Empatia real | Nubank | Bot usa nome próprio, tom caloroso, sem corpo-speak |
| Resolução em 1 toque | Nubank | Bot tenta resolver antes de perguntar |
| Nunca "não sei" | Zappos | Prompt Groq reformulado — sempre oferece próximo passo |
| Conexão emocional | Zappos | Resposta personalizada ao assunto específico do lead |
| Contexto no escalonamento | Zappos | Opção 0 envia histórico completo ao admin |
| Proatividade | Amazon | Bot aborda lead imediatamente após cadastro |

---

## Arquitetura

```
[fenice.ia.br — formulário]
        │ POST /leads (nome, telefone, email, empresa, interesse)
        ▼
[FastAPI — api_fenice_saas.py]
        │ 1. Valida campos
        │ 2. Salva fenice_tim_contatos (numero=telefone, area=interesse, estagio=lead_site)
        │ 3. POST → N8N_WEBHOOK_LEADS
        │ 4. Retorna 200 imediatamente
        ▼
[N8N — workflow fenice-leads (NOVO)]
        ├── Nó A: Groq gera WOW insight (dica sobre o assunto do lead)
        ├── Nó B: WhatsApp admin (5547991041414) via Evolution API
        ├── Nó C: E-mail confirmação ao prospect (Microsoft 365 SMTP)
        └── Nó D: WhatsApp proativo ao lead com WOW insight (Evolution API)
                        │ (quando lead responde)
                        ▼
                [N8N — fenice-tim existente]
                        └── área já salva → roteia sem mostrar menu
```

---

## 1. Frontend — Formulário (landing.html)

### Campos

| Campo | Tipo | Obrigatório | Validação |
|---|---|---|---|
| Nome completo | text | Sim | mín. 3 chars |
| Telefone WhatsApp | tel | Sim | formato `(XX) XXXXX-XXXX` → envia como `55XXXXXXXXXXX` |
| E-mail profissional | email | Sim | regex padrão |
| Escritório/empresa | text | Não | — |
| Assunto | modal selector | Sim | 1 opção obrigatória |
| Descrição (se Outros) | text | Condicional | máx. 80 chars |

### Modal de Assunto — 7 opções

```
1. 🏢  B2B Corporativo
2. ⚖️  Consultoria Jurídica
3. 🎓  Ensino Acadêmico
4. 👁️  Observatório da Mulher
5. ⚡  API & Desenvolvedores
6. 🧠  Filosofia & Teologia
7. 💬  Outros → campo: "Descreva em palavras-chave" (máx. 80 chars)
```

### Mapeamento assunto → área IVR

| Modal | area no Supabase |
|---|---|
| B2B Corporativo | `b2b` |
| Consultoria Jurídica | `juridico` |
| Ensino Acadêmico | `academico` |
| Observatório da Mulher | `observatorio` |
| API & Desenvolvedores | `api` |
| Filosofia & Teologia | `filosofia` |
| Outros | `outros` + texto em `dados.descricao` |

### UX

- Botão "Enviar mensagem" fica desabilitado até todos os campos obrigatórios preenchidos
- Após envio com sucesso: exibe mensagem "Recebemos seu contato! Em instantes você receberá uma mensagem no WhatsApp." + confete/animação
- Máscara automática no campo telefone

---

## 2. FastAPI — `/leads` (api_fenice_saas.py)

### Modelo de entrada (LeadRequest)

```python
class LeadRequest(BaseModel):
    nome:      str          # obrigatório
    telefone:  str          # obrigatório — formato 55XXXXXXXXXXX
    email:     str          # obrigatório
    empresa:   str | None = None
    interesse: str          # obrigatório — área IVR ou "outros:texto"
```

### Fluxo

1. Valida email (regex) e telefone (11-13 dígitos, começa com 55)
2. Normaliza telefone: remove não-dígitos, adiciona `55` se necessário
3. Salva em `fenice_tim_contatos`:
   - `numero = telefone`
   - `nome = nome`
   - `area = interesse` (área IVR)
   - `estagio = "lead_site"`
   - `dados = { email, empresa, descricao_outros }`
   - `on_conflict = numero` (merge-duplicates)
4. POST para `N8N_WEBHOOK_LEADS` com payload completo (não-bloqueante, background task)
5. Retorna `{ ok: true, mensagem: "..." }` imediatamente

### Remoções

- Remover toda lógica SMTP do `_notificar_lead` — e-mail passa a ser responsabilidade do N8N
- Remover referências a AvisaAPI
- Manter apenas: salvar Supabase + POST N8N

### Payload enviado ao N8N

```json
{
  "evento": "novo_lead",
  "nome": "João Silva",
  "telefone": "5547991041414",
  "email": "joao@silva.com",
  "empresa": "Silva Advogados",
  "interesse": "juridico",
  "interesse_label": "Consultoria Jurídica",
  "descricao_outros": null,
  "origem": "fenice.ia.br/contato",
  "timestamp": "2026-06-29T14:30:00Z"
}
```

---

## 3. N8N — Workflow `fenice-leads` (NOVO)

### Nós

**Nó 1 — Webhook trigger**
- Path: `fenice-leads`
- URL produção: `https://feniceit.app.n8n.cloud/webhook/fenice-leads`
- Método: POST

**Nó 2 — Groq: gerar WOW insight**
- Chama Groq `llama-3.3-70b` com prompt:
```
Você é o Téo, assistente jurídico-filosófico da Fenice IT.
Um prospect se interessou por: {interesse_label}.
Gere 1 insight jurídico/filosófico surpreendente e relevante sobre este tema.
Máximo 2 linhas. Tom: inteligente, caloroso, sem juridiquês.
Formato: apenas o insight, sem introdução.
```
- Output: `wow_insight` (string)

**Nó 3 — WhatsApp admin (notificação)**
- Para: `5547991041414` via Evolution API
- Mensagem:
```
🏛️ *Novo Lead — Fenice IT*

👤 *Nome:* {nome}
📱 *WhatsApp:* +{telefone}
📧 *E-mail:* {email}
🏢 *Empresa:* {empresa || "—"}
💼 *Assunto:* {interesse_label}
{se outros: "📝 Detalhe: {descricao_outros}"}

_Lead salvo no Supabase · área: {interesse}_
© 2026 Fenice IT · Justech.IA
```

**Nó 4 — E-mail ao prospect (Microsoft 365)**
- SMTP: `smtp.office365.com:587` (STARTTLS)
- De: `fenice_tech@fenice.ia.br`
- Para: `{email}`
- Assunto: `Fenice IA recebeu seu contato, {primeiro_nome}!`
- Corpo:
```
Olá, {primeiro_nome}!

Ficamos muito felizes com seu interesse em {interesse_label}.

Nossa equipe já foi notificada e em instantes o Téo, nosso assistente 
inteligente, vai entrar em contato pelo seu WhatsApp para uma conversa 
inicial sobre como podemos ajudar.

Enquanto isso, saiba que a Fenice IT combina inteligência artificial, 
filosofia e direito para entregar soluções que nenhuma LegalTech 
brasileira oferece.

Até já!
Equipe Fenice IT · Justech.IA
https://fenice.ia.br
```

**Nó 5 — WhatsApp proativo ao lead (WOW moment)**
- Para: `{telefone}` via Evolution API
- Mensagem:
```
Olá, {primeiro_nome}! 🏛️

Sou o *Téo*, assistente inteligente da *Fenice IT · Justech.IA*.

Vi que você tem interesse em *{interesse_label}* — ótima escolha!

💡 *Você sabia?*
{wow_insight}

Posso te contar mais sobre como a Fenice IT pode ajudar com {interesse_label}?
É só responder aqui. 😊

© 2026 Fenice IT · Justech.IA
```
_(contém `🏛️` e `© 2026` → BOT_SIGS detecta eco, sem loop)_

### Ordem de execução

Nó 1 → Nó 2 (Groq) → Nós 3+4 em paralelo → Nó 5 (WhatsApp lead)

Nó 5 depois de 3+4 garante que admin já foi notificado antes do lead receber o WhatsApp.

---

## 4. Prompt Groq reformulado (fenice-tim existente)

Adicionar ao system prompt do bot nas respostas da área:

```
REGRAS DE ATENDIMENTO FENICE TIM:
1. Sempre endereçar pelo primeiro nome do cliente
2. Nunca usar "não sei" ou "não posso" — sempre oferecer próximo passo
3. Se não tiver a informação, dizer: "Deixa eu verificar isso para você — um momento!"
4. Manter tom: inteligente, caloroso, sem juridiquês
5. Sempre encerrar com uma pergunta ou próximo passo concreto
6. Escalonamento humano (opção 0): enviar resumo completo da conversa ao admin
```

---

## 5. Variáveis de Ambiente

### Vercel (api_fenice_saas.py)

| Variável | Valor |
|---|---|
| `N8N_WEBHOOK_LEADS` | `https://feniceit.app.n8n.cloud/webhook/fenice-leads` |

### N8N (workflow fenice-leads)

| Variável | Valor |
|---|---|
| SMTP User | `fenice_tech@fenice.ia.br` |
| SMTP Pass | `170962Ra@` |
| SMTP Host | `smtp.office365.com` |
| SMTP Port | `587` |
| Evolution URL | `https://evolution-api-9fbw.srv1784289.hstgr.cloud` |
| Evolution ApiKey | `XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7` |
| Evolution Instance | `fenice-tim` |
| Groq ApiKey | (já configurado no N8N) |

---

## 6. Testes de Aceitação

1. **Lead submete formulário** → recebe WhatsApp do bot em < 30s com WOW insight
2. **Admin recebe notificação** no WhatsApp corporativo em < 15s
3. **Lead recebe e-mail** de confirmação em < 60s
4. **Lead responde "oi"** para o bot após cadastro → bot continua na área, sem mostrar menu
5. **Lead digita "menu"** → bot mostra menu (reset explícito funciona)
6. **Lead escolhe opção "0"** → admin recebe histórico completo
7. **Campo "Outros"** → WOW insight gerado com base nas palavras-chave informadas

---

## Arquivos Modificados

| Arquivo | Tipo | Mudança |
|---|---|---|
| `scripts/landing.html` | Modificar | Campo telefone + modal assunto + máscara |
| `scripts/api_fenice_saas.py` | Modificar | Novo modelo LeadRequest + limpar SMTP/AvisaAPI |
| `scripts/n8n_fenice_leads.json` | Criar | Workflow novo com 5 nós |
| `scripts/n8n_fenice_tim_v4.json` | Modificar | Prompt Groq reformulado (Zappos rules) |
| `.env` | Modificar | `N8N_WEBHOOK_LEADS=...` |

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ — Em nome de Allah, o Misericordioso*  
*Fenice IT · Justech.IA — Filosofia e Direito, Sabedoria e Justiça*
