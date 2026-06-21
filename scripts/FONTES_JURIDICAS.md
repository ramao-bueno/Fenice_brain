# Fontes Jurídicas — Fenice bRain

Catálogo de fontes primárias e secundárias integradas ao pipeline de dados jurídicos.

---

## Legislação Federal

### Planalto (Portal da Legislação)
- **URL base:** https://www.planalto.gov.br/ccivil_03/
- **Scripts:** `scripts/planalto_pipeline.py`, `scripts/atualizar_legislacao.py`
- **Docker:** `scripts/brazil-law-pipeline/`
- **Status:** Operacional — parser semântico com remoção de `<s>` (texto revogado)
- **Formato URL:** `/ccivil_03/_ato{FAIXA}/{ANO}/lei/l{NUMERO}.htm`
- **Atualização:** semanal via `python scripts/atualizar_legislacao.py`

### LexML
- **URL:** https://www.lexml.gov.br/
- **Tipo:** Repositório XML de legislação multi-esfera
- **Integração:** Futura — via API REST LexML (estruturada, ideal para OAI-PMH)
- **Vantagem:** Metadados ricos, identificadores persistentes (URN LexML)

---

## Jurisprudência

### STJ — Superior Tribunal de Justiça
- **Súmulas:** 674 notas geradas em `00_APEX/SUMULAS STJ/Sumulas/`
- **Fonte PDF:** `00_APEX/SUMULAS STJ/VerbetesSTJ.pdf`
- **Scripts:** `scripts/pipeline_sumulas_stj_pdf.py`, `scripts/extrator_pdf_sumulas_stj.py`
- **BDJUR:** https://bdjur.stj.jus.br/ — acesso bloqueado por Cloudflare (scraping manual)
- **SCON:** https://scon.stj.jus.br/ — para jurisprudência recente

### STF — Supremo Tribunal Federal
- **Súmulas:** 736 notas geradas em `00_APEX/SUMULAS STF/Sumulas/`
- **Fonte PDF:** `scripts/súmulas STF/Enunciados_Sumulas_STF_1_a_736_Completo.pdf`
- **Scripts:** `scripts/pipeline_sumulas_stf_pdf.py`, `scripts/extrator_pdf_sumulas_stf.py`
- **Status:** 726 vigentes, 10 superadas/canceladas

### jurismcp (MCP Jurídico)
- **Repo:** https://github.com/ivancaron/jurismcp
- **Tribunais:** STJ, STF, TST, TJES
- **Tecnologia:** Selenium + Patchright (Chrome headless)
- **Instalação:** Ver `scripts/INSTALAR_MCP_JURIDICO.md`
- **Config:** `.mcp.json` na raiz do vault

---

## Doutrina e Biblioteca Digital

### BDSF — Biblioteca Digital do Senado Federal
- **URL:** https://www2.senado.leg.br/bdsf/
- **Tipo:** DSpace — repositório de doutrina, estudos e legislação
- **Monitor:** `scripts/monitor_bdsf.py`
- **Atualização:** `python scripts/monitor_bdsf.py --dias 7 --salvar`
- **Notas:** `02_LEGISLACAO/BDSF/`

### LicitAI / PNCP
- **URL:** https://pncp.gov.br/
- **Projeto:** Separado (C:/LicitAI) — licitações e contratos públicos

---

## Banco de Dados

### PostgreSQL / Supabase
- **Schema:** `scripts/planalto_schema.sql`
- **Upsert:** `scripts/planalto_db.py` → classe `PlanaltoDB`
- **Config:** `.env` (DB_HOST, DB_NAME, DB_USER, DB_PASS)
- **Supabase:** Usar `DB_HOST=db.xxxx.supabase.co` + service_role_key
- **FTS:** `tsvector` em português + índice GIN
- **Grafo:** `scripts/fenice_graph_schema.sql` (grafo_nos + grafo_arestas)
- **Temporal:** `scripts/fenice_temporal_schema.sql` (histórico de revogações)

---

## API

### Fenice SaaS API (FastAPI)
- **Script:** `scripts/api_fenice_saas.py`
- **Endpoints:**
  - `GET /health`
  - `POST /buscar` — Free tier
  - `POST /analisar` — Premium (X-Fenice-Key: fenice_premium_*)
  - `POST /hermeneutica` — Premium
  - `POST /tcc` — Premium
- **Iniciar:** `uvicorn scripts.api_fenice_saas:app --reload`
- **RAG:** `scripts/fenice_rag.py`
- **Prompts:** `scripts/prompts/` (grounding, hermeneutica, tcc)

---

## SuperPowers Skills

| Skill | Função | Arquivo |
|---|---|---|
| `fenice-ia-01` | Túnel do Tempo Jurídico | `.claude/skills/fenice-ia-01/skill.md` |
| `fenice-ia-02` | Filtro Epistemológico (lentes filosóficas) | `.claude/skills/fenice-ia-02/skill.md` |
| `fenice-ia-03` | Detector de Antinomias | `.claude/skills/fenice-ia-03/skill.md` |
| `fenice-ia-04` | Exportador de Fichamento ABNT/APA | `.claude/skills/fenice-ia-04/skill.md` |
| `atomizar-juridico` | Motor de notas atômicas | `.claude/skills/atomizar-juridico/` |

---

_Última atualização: 2026-06-21_
