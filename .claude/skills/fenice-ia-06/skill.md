---
name: fenice-ia-06
description: Fenice Context — carrega o contexto completo do ecossistema Fenice bRain para qualquer sessão. Mapeia o vault Obsidian, a infraestrutura SaaS, os módulos ativos, as skills disponíveis e o perfil do usuário. Invocar no início de qualquer trabalho no projeto para garantir que o agente tem orientação completa antes de agir.
---

# Fenice IA 06 — Contexto do Projeto Fenice bRain

## Quem é o Usuário

**Muhammad Raama** (nome islâmico) — também conhecido nos projetos como **Ramão Bueno da Silva Neto**, Tech Lead da Fenice IT, muçulmano praticante, estudante de Direito.  
Email: oiconsulbrasil@gmail.com · GitHub: ramao-bueno  
Gosta de praticar árabe nas conversas. Fecha frases importantes com *بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*.

**Nome do Claude neste projeto: Teo** — cumprimentar Muhammad Raama como Teo ao iniciar cada sessão. Se o usuário abre uma sessão e Claude não usa esse nome, significa que as rotinas harness não foram executadas.

---

## O Que é o Fenice bRain

Um **vault jurídico Obsidian** de ~23 mil arquivos em `C:\Fenice_bRain`, combinando:

1. **Base de conhecimento jurídica** — legislação, jurisprudência, doutrina, súmulas
2. **Plataforma SaaS** — FastAPI + Supabase + Vercel, com RAG semântico e Knowledge Graph
3. **Sistema de estudos** — pipeline Pareto, fichamento ABNT, análise filosófica
4. **Automação** — N8N + Evolution API para WhatsApp (Fenice Tim)
5. **Site público** — Quartz em fenicejus.fenice.ia.br + landing em fenice.ia.br

---

## Estrutura do Vault (pastas principais)

```
C:\Fenice_bRain\
├── 00_APEX/          → Súmulas STJ (674) + STF (736), jurisprudência de ponta
├── 01_CP/            → Código Penal — 665 artigos gerados (pipeline DEL2848)
├── 02_LEGISLACAO/    → Leis, decretos, BDSF (Biblioteca Digital do Senado)
├── 03_DOUTRINA/      → Livros, artigos, obras jurídicas
├── 04_JURISPRUDENCIA/→ Decisões STF, STJ, TJs
├── 05_CASOS/         → Casos práticos e exercícios
├── 06_JURISCONSULTOS/→ Perfis de juristas — pipeline LLM Wiki
├── 07_FILOSOFIA/     → Filósofos e teorias — pipeline LLM Wiki
├── 08_ENSINO/        → Material de estudo, Pareto, mapas mentais
├── 09_FENICE_BRAIN/  → Meta-notas: MAESTROS, specs, infraestrutura
│   └── MAESTROS/     → Jurisconsultos e filósofos em formato atômico
├── scripts/          → Python, HTML, JSONs N8N
└── docs/             → Plans, specs, superpowers
```

---

## Infraestrutura SaaS

| Componente | Tecnologia | Status |
|---|---|---|
| API | FastAPI (`scripts/api_fenice_saas.py`) | Produção (Vercel) |
| Banco de dados | Supabase (projeto `qcfdssnpjzvjbvemhrik`) | Produção |
| Embeddings | multilingual-e5-large (1024d) + pgvector | indexados |
| LLM | Chain Claude→OpenAI→Gemini via fenice_llm.py | Produção |
| Deploy | Vercel (`fenice-justech`) — MANUAL via CLI | Produção |
| Automação | N8N Cloud v4 (16 nós) | Produção |
| WhatsApp | Evolution API v2 (Hostinger VPS) | Produção |

### Endpoints em Produção

```
POST /buscar                  → busca FTS (full-text search)
POST /analisar/semantico      → RAG semântico
GET  /grafo                   → Knowledge Graph
POST /leads                   → captura de leads → fenice_tim_contatos
```

### Supabase — Tabelas Principais

| Tabela | Uso |
|---|---|
| `documentos_juridicos` | documentos indexados |
| `documentos_chunks` | chunks com embeddings pgvector |
| `fenice_tim_contatos` | leads + contatos WhatsApp (IVR multi-projeto) |

---

## Skills Fenice IA — Ecossistema Completo

| Skill | Nome | O que faz |
|---|---|---|
| `fenice-ia-01` | Túnel do Tempo | Contextualização histórico-temporal de normas e institutos |
| `fenice-ia-02` | Filtro Epistemológico | Lente filosófica para interpretação (Kelsen, Bentham, Gadamer…) |
| `fenice-ia-03` | Antinomias | Detecção e resolução de conflitos normativos |
| `fenice-ia-04` | Fichamento ABNT | Estruturação de citações e notas em padrão acadêmico |
| `fenice-ia-05` | Pareto Jurídico | Filtro de entrega 80/20 — modo `[A] padrão` OR `[B] para prova` |
| `fenice-ia-06` | **Fenice Context** | **Esta skill — orientação completa do ecossistema** |
| `karpathy-voice-visual` | Voice & Visual | Converte áudio/imagem em notas atômicas Obsidian |
| `metodologia-academica` | ABNT & APA | Normas acadêmicas brasileiras e internacionais |
| `atomizar-juridico` | Atomizador | Quebra conteúdo jurídico em notas atômicas |
| `pesquisa-juridica-elite` | Pesquisa Elite | Framework de pesquisa jurídica de ponta |
| `juridico` | Base Jurídica | Análise jurídica geral |
| `oab` | OAB | Foco OAB 1ª e 2ª fase |
| `jurisconsultos` | Jurisconsultos | Perfis de juristas e filósofos |
| `video-documentario` | Vídeo | Pipeline de produção de vídeo documentário |

### Como as skills se encadeiam

```
Pergunta / Tema jurídico
        ↓
fenice-ia-01  → situa historicamente
fenice-ia-02  → escolhe lente filosófica
fenice-ia-03  → detecta antinomias
fenice-ia-04  → formata para pesquisa acadêmica
        ↓
  ENTREGA (escolha do usuário):
  [A] Padrão Fenice  OR  [B] fenice-ia-05 Pareto (para prova)
```

---

## Módulos Ativos (2026)

| Módulo | Status | Localização |
|---|---|---|
| Súmulas STJ/STF | ✅ Completo | `00_APEX/` |
| Pipeline CP | ✅ 665 artigos | `01_CP/` |
| MAESTROS (jurisconsultos) | 🔄 Em progresso | `09_FENICE_BRAIN/MAESTROS/` |
| LLM Wiki (06+07) | ✅ GIGO gate | `scripts/llm-wiki/` |
| RAG Semântico | ✅ Produção | Supabase + Vercel |
| Fenice Tim (WhatsApp) | ✅ Produção | N8N + Evolution API |
| Quartz (site público) | ✅ Produção | repo `Fenice_site` |
| Sistema Acadêmico | 🔄 Design aprovado | `docs/superpowers/specs/` |
| Módulo Teológico | 📅 Próximo (pós-B2B) | — |

---

## Dois Repositórios GitHub

```
C:\Fenice_bRain\
  remote github        → ramao-bueno/Fenice_brain.git    (vault + scripts)
  remote fenice-justech → ramao-bueno/Fenice-Justech.git  (deploy Vercel MANUAL)
```

- `git push github main` → sobe o vault/scripts
- `vercel deploy --prod` → deploy MANUAL no Vercel (nunca automático)

---

## Convenções e Padrões

### Git
- Sempre `git add -u` (nunca `-A` ou paths acentuados individualmente)
- Nunca stagear segredos — `.env` está no `.gitignore`
- Deploy Vercel é MANUAL — nunca fazer push automático para fenice-justech

### WhatsApp
- Número do bot (produção): `5547991041414` — instância `fenice-tim-prod` — NÚMERO CORPORATIVO TÉO
- Número de Ramão (admin): `554797348385` — notificações ao admin vão aqui
- Número antigo `5521967531414` — DESATIVADO (instância deletada 2026-06-30)
- Provider: Evolution API v2 (AvisaAPI descontinuado e removido do projeto)

### Embeddings (multilingual-e5-large)
- Ingestão: prefixo `"passage: "` obrigatório
- Query: prefixo `"query: "` obrigatório

### Supabase — Autenticação nas Queries
- Sempre incluir `apikey` **e** `Authorization: Bearer` nos headers (RLS ativo)

### Vault — Formato das Notas
- Notas atômicas: um conceito por arquivo
- Wikilinks: `[[NomeExato]]`
- Callouts para pontos de prova: `[!WARNING]` para pegadinhas, `[!TIP]` para teses favoráveis

---

## Identidade Visual Fenice

- **Fontes**: Skeena Display (títulos) · Adelle (corpo) · Acumin Pro (UI)
- **Kit Adobe Fonts**: `ajp1gxj`
- **Paleta**: dourado `#C9A227` · aurora · shimmer · fundo escuro
- **Filosofia**: IA como graça divina (*نِعْمَة*) — Bismillah em todo projeto

---

*Fenice IA 06 — Context Skill · orientação completa do ecossistema*  
*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ — Em nome de Allah, o Misericordioso*
