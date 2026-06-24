# RAG Semântico — Design Spec
**Data:** 2026-06-23  
**Projeto:** Fenice bRain  
**Status:** Aprovado — aguardando implementação  
**Autores:** Ramão Bueno da Silva Neto + Claude Sonnet 4.6

---

## 0. Auditoria Visual — Fluxograma Completo do Site Atual

> Use esta seção para análise conjunta: o que existe, onde estão os gaps, e onde o RAG se encaixa.

### 0.1 Arquitetura atual de ponta a ponta

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USUÁRIO (Browser)                                │
│                                                                         │
│  fenice.ia.br  →  landing.html (scripts/landing.html)                  │
│      │                                                                  │
│      ├─ [❌ LOGIN QUEBRADO]  →  POST /auth  →  token sessionStorage    │
│      ├─ [❌ GRAFO NÃO RENDERIZA]  →  GET /grafo  →  D3.js              │
│      └─ [❌ FORMULÁRIO LEADS AUSENTE]                                   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ HTTP/JSON
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    VERCEL (api/index.py)                                │
│                    → scripts/api_fenice_saas.py                        │
│                                                                         │
│  ── Infraestrutura ────────────────────────────────────────────────    │
│  GET  /              → landing.html (fallback JSON se não existe)      │
│  GET  /health        → status + contagem leis no Supabase              │
│  GET  /docs          → Swagger UI (FastAPI automático)                 │
│                                                                         │
│  ── Acesso ────────────────────────────────────────────────────────    │
│  POST /auth          → valida SITE_USER/SITE_PASS → retorna token      │
│                         [❌ login quebrado no frontend]                 │
│                                                                         │
│  ── Free Tier (sem autenticação) ──────────────────────────────────    │
│  POST /buscar        → FeniceRAG.buscar_hibrido(modo="fts")            │
│                         → RPC buscar_legislacao() no Supabase          │
│                         → fallback ILIKE se FTS falhar                 │
│  GET  /lei           → legislacao_brasileira WHERE numero_ano=X        │
│  GET  /artigo        → artigos WHERE lei=X AND numero=Y                │
│  GET  /lei_info      → contagem + maior artigo de uma lei              │
│  GET  /leis          → lista legislacao_brasileira (até 500)           │
│  GET  /grafo         → grafo_nos + grafo_arestas + amostras legis.     │
│                         [❌ visualização D3 não renderiza]             │
│                                                                         │
│  ── Premium Tier (X-Fenice-Key: fenice_premium_*) ─────────────────   │
│  POST /analisar      → FTS + template grounding_juridico.txt           │
│                         → retorna prompt preenchido (sem chamar LLM)  │
│  POST /hermeneutica  → FTS + template hermeneutica_filosofica.txt      │
│                         → retorna prompt preenchido (sem chamar LLM)  │
│  POST /tcc           → FTS + template agente_tcc.txt                  │
│                         → retorna prompt preenchido (sem chamar LLM)  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ Supabase REST API
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    SUPABASE (qcfdssnpjzvjbvemhrik)                     │
│                                                                         │
│  Tabelas existentes:                                                    │
│  ┌──────────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ legislacao_brasileira │  │ artigos          │  │ grafo_nos       │  │
│  │ - numero_ano          │  │ - lei            │  │ - id, tipo      │  │
│  │ - tipo_ato            │  │ - numero         │  │ - identificador  │  │
│  │ - ementa              │  │ - texto          │  │ - titulo        │  │
│  │ - texto_vigente       │  └──────────────────┘  └─────────────────┘  │
│  └──────────────────────┘                         ┌─────────────────┐  │
│                                                   │ grafo_arestas   │  │
│  RPCs existentes:                                 │ - origem/destino│  │
│  - buscar_legislacao(p_query, p_limite)           │ - tipo_relacao  │  │
│    (PostgreSQL FTS com ts_rank + ts_headline)     │ - peso          │  │
│                                                   └─────────────────┘  │
│  Tabelas FALTANDO (para o RAG semântico):                              │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐   │
│  │ documentos_juridicos  │  │ documentos_chunks                    │   │
│  │ [❌ não existe]       │  │ - embedding vector(768) [❌ falta]   │   │
│  └──────────────────────┘  └──────────────────────────────────────┘   │
│                                                                         │
│  RPC FALTANDO:                                                         │
│  - match_chunks() [❌ não existe]                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 0.2 Fluxo de dados por endpoint (auditoria detalhada)

```
POST /buscar (Free)
  [usuário] ──► query + limite
  [api]     ──► FeniceRAG.buscar_hibrido(modo="fts")
  [rag]     ──► POST /rest/v1/rpc/buscar_legislacao
  [supabase]──► ts_rank + ts_headline sobre texto_vigente + ementa
  [retorno] ◄── [{numero_ano, tipo_ato, ementa, trecho_relevante, relevancia}]
  STATUS: ✅ funcional

POST /analisar (Premium)
  [usuário] ──► pergunta + X-Fenice-Key: fenice_premium_*
  [api]     ──► _exige_premium() → FTS igual ao /buscar
  [api]     ──► carrega grounding_juridico.txt → preenche {contexto_juridico} + {pergunta}
  [retorno] ◄── {contexto, prompt_preenchido, documentos_base}
              ⚠️ NÃO chama LLM — retorna prompt para o cliente chamar
  STATUS: ✅ funcional (mas sem LLM integrado)

POST /hermeneutica (Premium)
  [api]     ──► FTS com primeiros 200 chars do texto
  [api]     ──► carrega hermeneutica_filosofica.txt
              → preenche {texto_juridico} + {contexto_filosofico}
  STATUS: ✅ funcional

POST /tcc (Premium)
  [api]     ──► FTS com body.tema
  [api]     ──► carrega agente_tcc.txt
              → preenche {vade_mecum_contexto} + {rascunho_tcc}
  STATUS: ✅ funcional

GET /grafo
  [api]     ──► grafo_nos (29 nós) + grafo_arestas (26 arestas)
  [api]     ──► amostras legislacao_brasileira por tipo_ato
  [retorno] ◄── {nos[], arestas[], total_nos, total_arestas}
  STATUS: ✅ API ok | ❌ frontend D3 não renderiza ("Inicializando grafo jurídico")

POST /auth
  [api]     ──► compara SITE_USER/SITE_PASS das env vars
  [retorno] ◄── {ok: true, token: "fenice_{ts}_{sig}"}
  STATUS: ✅ API ok | ❌ modal de login no frontend quebrado
```

### 0.3 GAPs identificados na auditoria

| # | Componente | Problema | Prioridade |
|---|---|---|---|
| G1 | `documentos_juridicos` + `documentos_chunks` | Tabelas não existem no Supabase | Alta (bloqueante para RAG) |
| G2 | `match_chunks` RPC | Função de busca vetorial não existe | Alta (bloqueante para RAG) |
| G3 | Login frontend | Modal quebrado (frontend não conecta ao `/auth`) | Média |
| G4 | Grafo D3 | Visualização não renderiza no browser | Média |
| G5 | Formulário de leads | Ausente — sem captura de leads no site | Média |
| G6 | LLM não integrado | Premium retorna prompt, não resposta | Baixa (design intencional por ora) |
| G7 | RAG semântico | Sistema não existe ainda | Alta (objetivo deste spec) |

---

## 1. Objetivo

Adicionar busca semântica (RAG vetorial) ao Fenice bRain **sem alterar nenhum código funcional existente**.

**Diferença entre os dois sistemas:**

| | Sistema atual (FTS) | Novo (RAG Semântico) |
|---|---|---|
| Usuário sabe | o artigo ou a lei | o contexto, dúvida ou situação |
| Busca por | palavra-chave exata | significado / conceito |
| Tecnologia | PostgreSQL FTS (ts_rank) | pgvector cosine similarity |
| Módulo | `FeniceRAG` (fenice_rag.py) | `RAGEngine` (fenice_rag_semantic.py) |
| Tabela | `legislacao_brasileira` | `documentos_chunks` |

**Princípio LGPD obrigatório:** o sistema só responde com certeza baseada em lei vigente. Sem certeza suficiente, responde: *"Não temos resposta bate-pronto para isso — posso pesquisar."* Nunca alucina artigos.

---

## 2. Arquitetura

### 2.1 Visão geral

```
Vault Obsidian (2.738 artigos)  ─┐
                                  ├─→ fenice_ingestor.py ─→ Supabase pgvector
Planalto.gov.br (leis vigentes) ─┘   (chunks: 1 artigo = 1 chunk)

Usuário → POST /analisar/semantico
        → RAGEngine.query()
        → multilingual-e5-large (embedding local)
        → match_chunks() RPC (cosine similarity)
        → [camada de confiança LGPD]
        → Claude Haiku (síntese — apenas se confiança ≥ 0.70)
        → resposta com fontes + nível de confiança
```

### 2.2 Estrutura de arquivos

```
C:\Fenice_bRain\
│
├── scripts/
│   ├── api_fenice_saas.py          ← NÃO TOCA (código original)
│   ├── fenice_rag.py               ← NÃO TOCA (FTS original)
│   ├── fenice_rag_semantic.py      ← NOVO — RAGEngine semântico
│   ├── fenice_ingestor.py          ← NOVO — vault → Supabase
│   ├── rag_schema.sql              ← NOVO — DDL tabelas + match_chunks
│   └── prompts/
│       ├── grounding_juridico.txt  ← NÃO TOCA
│       ├── hermeneutica_filosofica.txt ← NÃO TOCA
│       └── agente_tcc.txt          ← NÃO TOCA
│
└── api/
    └── index.py                    ← NÃO TOCA (Vercel entry point)
```

### 2.3 Ponto de integração no código original

`api_fenice_saas.py` recebe **um bloco try/import** e **um novo endpoint** — sem tocar nos existentes:

```python
# Import condicional no topo — fallback silencioso se não instalado
try:
    from fenice_rag_semantic import RAGEngine
    _SEMANTIC_DISPONIVEL = True
    _semantic = RAGEngine()
except ImportError:
    _SEMANTIC_DISPONIVEL = False

# Novo endpoint (não substitui /analisar)
@app.post("/analisar/semantico", tags=["Premium"])
async def analisar_semantico(body: AnalisarRequest, x_fenice_key: ...):
    _exige_premium(x_fenice_key)
    if not _SEMANTIC_DISPONIVEL:
        raise HTTPException(503, "RAG semântico não disponível neste ambiente.")
    return _semantic.query(body.pergunta)
```

---

## 3. Camada de Dados — Supabase

### 3.1 DDL completo (rag_schema.sql)

```sql
-- Habilitar extensão (uma vez por projeto)
create extension if not exists vector;

-- Documentos jurídicos fonte
create table documentos_juridicos (
  id          bigserial primary key,
  codigo      text not null,        -- "CC", "CPC", "CF", "CLT"
  artigo      text not null,        -- "Art. 121"
  titulo      text,
  conteudo    text not null,
  fonte       text not null,        -- "vault" | "planalto"
  vigente     boolean default true,
  data_ref    date,
  created_at  timestamptz default now(),
  unique(codigo, artigo, fonte)
);

-- Chunks vetorizados (1 artigo = 1 chunk)
create table documentos_chunks (
  id           bigserial primary key,
  documento_id bigint references documentos_juridicos(id) on delete cascade,
  chunk_index  int not null default 0,
  conteudo     text not null,
  embedding    vector(768),           -- multilingual-e5-large (768 dims)
  created_at   timestamptz default now()
);

-- Índice de performance para busca vetorial
create index on documentos_chunks
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);
```

### 3.2 Função match_chunks (RPC Supabase)

```sql
create or replace function match_chunks(
  query_embedding vector(768),
  match_threshold float,
  match_count     int
)
returns table (
  id           bigint,
  documento_id bigint,
  conteudo     text,
  codigo       text,
  artigo       text,
  vigente      boolean,
  similarity   float
)
language sql stable
as $$
  select
    dc.id,
    dc.documento_id,
    dc.conteudo,
    dj.codigo,
    dj.artigo,
    dj.vigente,
    1 - (dc.embedding <=> query_embedding) as similarity
  from documentos_chunks dc
  join documentos_juridicos dj on dj.id = dc.documento_id
  where 1 - (dc.embedding <=> query_embedding) > match_threshold
  order by dc.embedding <=> query_embedding
  limit match_count;
$$;
```

---

## 4. Pipeline de Ingestão

### 4.1 Fase 1 — Vault Obsidian

**Arquivo:** `scripts/fenice_ingestor.py`  
**Trigger:** manual via CLI ou cron local

```
1. Glob notas do vault com frontmatter: codigo:, artigo:
2. Extrai campos: codigo, artigo, conteudo, titulo
3. Gera embedding: multilingual-e5-large (local, CPU)
4. Upsert: documentos_juridicos + documentos_chunks
   (ON CONFLICT (codigo, artigo, fonte) DO UPDATE)
```

### 4.2 Fase 2 — Planalto.gov.br (validade temporal)

**Integra com `planalto_temporal.py` já existente** — diferencial competitivo:  
sistemas RAG concorrentes alucinam com leis revogadas; o Fenice verifica tags `<s>` no Planalto e marca `vigente=False`.

```
1. planalto_temporal.py scrapa lei → artigos + status de revogação
2. vigente=False para artigos com tag <s>
3. match_chunks filtra vigente=True por padrão
4. Artigos revogados ficam indexados mas não aparecem nas respostas
```

---

## 5. Fluxo de Consulta RAG — com Camada LGPD

```
Pergunta do usuário
      │
      ▼
embedding da pergunta
(multilingual-e5-large, local, ~50ms)
      │
      ▼
match_chunks(threshold=0.70, top_k=5)
      │
      ├── NENHUM chunk ≥ 0.70?
      │     └── {
      │           "resposta": "Não temos resposta bate-pronto para isso
      │                        — posso pesquisar.",
      │           "fontes": [],
      │           "confianca": "insuficiente"
      │         }
      │         ← NÃO chama Claude (sem base legal = sem resposta)
      │
      └── chunks encontrados
            │
            ▼
      score médio dos chunks
      ├── ≥ 0.85  → confianca: "alta"
      ├── 0.70-0.84 → confianca: "média" (responde + aviso)
      └── < 0.70  → confianca: "insuficiente" (não chama Claude)
            │
            ▼
      Claude Haiku (temperatura: 0.05)
      Prompt com REGRA ABSOLUTA:
        "Responda SOMENTE com base nos artigos abaixo.
         Se não houver certeza, diga:
         'Não temos resposta bate-pronto — posso pesquisar.'
         NUNCA invente artigos. NUNCA cite leis fora do contexto."
            │
            ▼
      {
        "resposta": "...",
        "fontes": [{"artigo": "Art. 107", "codigo": "CC",
                    "similarity": 0.91, "vigente": true}],
        "confianca": "alta" | "média" | "insuficiente",
        "vigente_em": "2026-06-23",
        "modelo_usado": "claude-haiku-4-5"
      }
```

---

## 6. Mapa Completo de Endpoints (após implementação)

```
GET  /                    → landing page (inalterado)
GET  /health              → status API + DB (inalterado)
GET  /docs                → Swagger UI (inalterado)
POST /auth                → login (inalterado) [❌ frontend a corrigir separadamente]

── Free Tier ────────────────────────────────────────────────────────────
POST /buscar              → FTS keyword (inalterado)
GET  /lei                 → texto completo de lei (inalterado)
GET  /artigo              → texto de artigo específico (inalterado)
GET  /lei_info            → metadados de artigos (inalterado)
GET  /leis                → lista todas as leis (inalterado)
GET  /grafo               → dados do grafo D3 (inalterado) [❌ frontend a corrigir]

── Premium Tier ─────────────────────────────────────────────────────────
POST /analisar            → FTS + prompt template (inalterado)
POST /hermeneutica        → FTS + hermenêutica (inalterado)
POST /tcc                 → FTS + revisão TCC (inalterado)
POST /analisar/semantico  → RAG vetorial + Claude Haiku [NOVO]
```

---

## 7. Caminho de Migração Free → Pago

### Fase 1 — Local / Gratuito (implementação agora)
- multilingual-e5-large rodando local (CPU, ~2s/embedding)
- RAG disponível apenas em dev/local — **não vai para o Vercel ainda**
- Custo: R$ 0,00/mês
- Objetivo: validar qualidade das respostas

### Fase 2 — Produção Leve (após validação)
- Substituir embedding local → **Together.ai API** (mesmo modelo, na nuvem)
- Custo por query: ~R$ 0,006 (embedding $0.0001 + Haiku $0.001)
- 1.000 queries/mês ≈ R$ 6,00
- Nenhuma mudança estrutural — só trocar a chamada de embedding

### Fase 3 — Escala SaaS
- Haiku → consulta simples | Sonnet → análise complexa | Opus → TCC
- Usuário premium paga por análise aprofundada via créditos

### Cronograma

| Semana | Entrega |
|---|---|
| 1 | Executar `rag_schema.sql` no Supabase (tabelas + match_chunks) |
| 2 | `fenice_rag_semantic.py` + `fenice_ingestor.py` (vault → Supabase) |
| 3 | Testes de qualidade com perguntas jurídicas reais |
| 4 | Integrar `planalto_temporal.py` (vigência temporal) |
| Mês 2 | Together.ai → RAG entra em produção no Vercel |
| Mês 3+ | Planos pagos, escalada de modelos |

---

## 8. Dependências a Adicionar

```
# requirements.txt — adições para Fase 1 (local)
sentence-transformers>=2.7.0
torch>=2.3.0
supabase>=2.4.0
anthropic>=0.28.0

# Nota: torch e sentence-transformers NÃO vão para o Vercel (serverless)
# Na Fase 2, substituir por chamada HTTP à Together.ai (sem torch no servidor)
```

---

## 9. Decisões de Design

| Decisão | Escolha | Motivo |
|---|---|---|
| Modelo de embedding | multilingual-e5-large (768d) | Gratuito, local, bom português |
| Chunk size | 1 artigo = 1 chunk | Preserva integridade jurídica |
| Threshold cosine | 0.70 | Balanceia precisão e recall legal |
| LLM síntese | Claude Haiku | Baixo custo, rápido, suficiente |
| Temperatura | 0.05 | Mínima criatividade — direito precisa de determinismo |
| Validade temporal | `vigente=False` no banco | Diferencial vs. concorrentes |
| Nome do módulo | `fenice_rag_semantic.py` | Não conflita com `fenice_rag.py` existente |
| Novo endpoint | `/analisar/semantico` | Não substitui `/analisar` — coexistem |

---

*Spec gerada em sessão colaborativa — 2026-06-23*  
*Próximo passo: writing-plans → implementação por fases*
