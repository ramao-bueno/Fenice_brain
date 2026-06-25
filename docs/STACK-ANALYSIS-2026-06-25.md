# Fenice IT — Análise de Stack (2026-06-25)
**© 2026 Fenice IT Justech.ia · Todos os direitos reservados**
**Tech Lead: Ramão Bueno da Silva Neto**

---

## FERRAMENTAS PAGAS — Custos Ativos

| Ferramenta | Uso | Custo estimado/mês | Risco |
|---|---|---|---|
| **Vercel Pro** (fenice-tech) | Deploy `fenice.ia.br` + `observatorio-da-mulher-sfs.com.br` | ~$20 | Corrigido: Ignored Build Step ativo |
| **Claude Code** (Anthropic) | Tech Lead IA — desenvolvimento diário | $20–$100 | Baixo |
| **AvisaAPI** | WhatsApp inbound/outbound no `fenice.ia.br` | variável (BR) | 🔴 Alta: serviço pequeno, sem SLA público |
| **Adobe Fonts** (kits `ajp1gxj` + `cmr1ivs`) | Tipografia `fenice.ia.br` (skeena-display, adelle, acumin-pro, sloop-script-one, caprizant) | incluso no Adobe CC | ⚠️ Se a subscription cair, site perde tipografia |

**Estimativa mínima mensal: ~$60/mês** (sem contar AvisaAPI e Adobe CC)

---

## FERRAMENTAS GRATUITAS — Com Limites

| Ferramenta | Uso | Tier | Limite crítico |
|---|---|---|---|
| **GitHub** | Repos `Fenice_brain`, `Fenice_site` | Free | Ilimitado (repos públicos) |
| **Supabase** (`qcfdssnpjzvjbvemhrik`) | DB + Auth + Storage + WhatsApp logs | Free | 500 MB DB · 50k rows · 2 projetos |
| **Neon** (PostgreSQL serverless) | Cadastro apoiadores observatório | Free | 0.5 GB · **190h compute/mês** ← crítico |
| **Groq API** | LLM `llama-3.3-70b-versatile` — chatbot WhatsApp | Free | **6k tokens/min · 30 req/min** ← crítico |
| **N8N** | Workflow WhatsApp → Groq → AvisaAPI | Self-hosted/free | Depende da instalação |
| **Obsidian** | Vault jurídico 23k+ notas | Free (desktop) | Sem limite local |
| **Quartz v4** | `fenicejus.fenice.ia.br` | Open source | Build lento: 23k arquivos |
| **Next.js 16** | Observatório | Open source | — |
| **FastAPI** (Python) | API SaaS jurídico | Open source | — |
| **Google Fonts** | Playfair Display + Inter (observatório) | Gratuito | — |
| **Sentence Transformers** | RAG semântico local | Open source | Não roda no Vercel (sem GPU) |

---

## RISCOS MAPEADOS

### 🔴 Crítico — AvisaAPI
- Canal principal do chatbot WhatsApp
- Serviço brasileiro pequeno, sem documentação de SLA
- **Ação:** Documentar plano/credenciais + definir alternativa (Twilio ou Meta Cloud API)

### 🟠 Alto — Groq rate limit
- `llama-3.3-70b-versatile` tem limite de 6k tokens/min no free tier
- Sem retry implementado: qualquer 429 = silêncio no atendimento
- **Ação:** Retry com exponential backoff + mensagem de fallback ✅ (implementado 2026-06-25)

### 🟠 Alto — Neon free tier
- 190h de compute/mês esgotam com tráfego médio
- **Ação:** Migrar para Supabase (já no stack) ✅ (implementado 2026-06-25)

### 🟡 Médio — Adobe Fonts
- Kits `ajp1gxj` e `cmr1ivs` via `use.typekit.net`
- Se a conta Adobe CC expirar, site perde toda tipografia
- **Ação:** Fallbacks CSS implementados ✅ (implementado 2026-06-25)

### 🟡 Médio — Sentence Transformers / RAG semântico
- Requer `torch` (GPU) — não funciona no Vercel
- Em produção: busca cai para FTS keyword only
- **Ação futura:** Migrar embeddings para Supabase pgvector

---

## RECOMENDAÇÕES IMPLEMENTADAS (2026-06-25)

| # | Ação | Status |
|---|---|---|
| 1 | Migrar banco observatório: Neon → Supabase | ✅ |
| 2 | Fallbacks CSS para fontes Adobe no fenice.ia.br | ✅ |
| 3 | Retry + tratamento de 429 no Groq | ✅ |
| 4 | Documentação AvisaAPI (`docs/AVISAAPI.md`) | ✅ |

---

## PRÓXIMO INVESTIMENTO — B2B

Infraestrutura atual suporta B2B sem custo adicional de infra. Itens novos necessários:

| Ferramenta | Uso | Custo |
|---|---|---|
| **Stripe** | Pagamentos | 2.9% + $0.30/transação |
| **Resend** | E-mail transacional | Gratuito até 3k/mês; $20/mês depois |
| **Supabase Auth** | Autenticação | Já no stack (gratuito) |

---

## ALTERNATIVAS AVALIADAS

| Atual | Alternativa | Quando migrar |
|---|---|---|
| AvisaAPI | Twilio WhatsApp Business ($0.005/msg) | Se AvisaAPI ficar instável |
| Groq Free | Groq Pay-as-you-go ou Claude Haiku 4.5 | Se rate limits forem atingidos em produção |
| Neon | Supabase PostgreSQL | ✅ Migrado |
| Adobe Fonts | Self-hosted via Vercel | Se Adobe CC cancelar |
| RAG local (torch) | Supabase pgvector | Próxima sprint de IA |
