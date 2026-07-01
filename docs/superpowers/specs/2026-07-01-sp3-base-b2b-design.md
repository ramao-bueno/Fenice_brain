# SP-3 · Base de Conhecimento B2B — Design Spec

**Data:** 2026-07-01
**Status:** Aprovado (aguardando revisão final do spec)
**Autor:** Ramão Bueno + Claude
**Roadmap:** ver [2026-06-30-fenice-roadmap-macro.md](2026-06-30-fenice-roadmap-macro.md)

---

## Visão Geral

Base de dados B2B que recebe as exportações de empresas das parceiras (a TIM é a
primeira), normaliza num registro canônico por CNPJ, habilita a prospecção ativa
"cachorro perdigueiro" (Hunter) e desemboca no atendimento WOW (SP-1).

O formato da planilha TIM é apenas **uma amostra** — a base é agnóstica ao
formato: múltiplos formatos, múltiplas parceiras, enriquecível por outros players
(alinhado à Missão/Visão: estar sempre à frente do cliente).

---

## Fronteira do Subprojeto

- **SP-3 entrega (MVP):** Camadas 1-2 (RAW/staging + canônico) + mapeador `TIM_v1`
  + importador Python + a definição da ponte para as Camadas 3 e 4.
- **Preparado, não construído agora:** Camada 3 (enriquecimento externo automático)
  e a automação da Camada 4 (disparo WOW automático).
- **Fora do SP-3:** cobrança/BKO (TIM); CRM visual + Power BI (SP-3 fase futura);
  o motor de atendimento em si (SP-1, já construído).

---

## Arquitetura — 4 Camadas

```
CAMADA 1 · RAW / STAGING
  fenice_b2b_importacoes   1 linha por arquivo (parceira, formato, data, contagem)
  fenice_b2b_staging       1 linha bruta (dados_raw jsonb — original fiel), cnpj
  → reprocessável; guarda o original quando o formato mudar
                │  mapeador por formato ("TIM_v1" → canônico)
                ▼
CAMADA 2 · CANÔNICO
  fenice_b2b_empresas      1 registro por CNPJ (normalizado + scores + fontes)
  fenice_b2b_socios        ponte PF↔PJ (sócio ↔ contato B2C)
                │
                ▼
CAMADA 3 · ENRIQUECIMENTO (preparada)
  outros players alimentam o MESMO registro canônico; cada dado rastreia a fonte
                │
                ▼
CAMADA 4 · WOW ATENDIMENTO (ponte definida, automação futura)
  do dado B2B → ação de relacionamento WOW (reusa SP-1: Evolution + N8N + Téo)
  empresa/sócio abordado → cria/atualiza contato → dispara padrão WOW → handoff Ramão
```

---

## Modelo de Dados

### `fenice_b2b_importacoes` (Camada 1 — lote)
| Campo | Tipo | Nota |
|---|---|---|
| `id` | uuid PK | |
| `parceira` | text | ex: "TIM" |
| `formato` | text | ex: "TIM_v1" |
| `arquivo_nome` | text | nome do arquivo importado |
| `importado_em` | timestamptz | default now() |
| `linhas_total` | int | linhas do arquivo |
| `linhas_ok` | int | linhas processadas ao canônico |

### `fenice_b2b_staging` (Camada 1 — linha bruta)
| Campo | Tipo | Nota |
|---|---|---|
| `id` | uuid PK | |
| `importacao_id` | uuid FK → importacoes | |
| `linha_num` | int | posição no arquivo |
| `dados_raw` | jsonb | a linha EXATA como veio (fiel) |
| `cnpj` | text | extraído para vínculo |
| `processado` | bool | default false |
| `erro` | text | null se ok |

### `fenice_b2b_empresas` (Camada 2 — canônico, PK = cnpj)
Identificação: `cnpj` (PK), `razao_social`, `nome_fantasia`
Localização: `uf`, `municipio`, `bairro`, `logradouro`, `cep`, `numero`
Qualificação: `data_abertura` (date), `porte_receita`, `porte_estimado`, `faturamento_estimado`, `funcionarios_estimado`, `opcao_mei` (bool), `opcao_simples` (bool), `matriz_filial`
Atividade: `cnae_fiscal`, `descricao_cnae`
Contato (jsonb): `emails` (array de string), `telefones` (array `[{numero, qualidade}]`), `links` (array de string)
Inteligência: `operadora_atual` (text, technographic), `score_fit` (int null), `score_intent` (int null)
Funil/gestão: `status` (text — os 7 da TIM), `observacao`, `estagio_fenice` (text null — mapeamento opcional)
Rastreio: `fontes` (jsonb — quais importações/parceiras alimentaram), `criado_em`, `atualizado_em`

### `fenice_b2b_socios` (Camada 2 — ponte PF↔PJ)
| Campo | Tipo | Nota |
|---|---|---|
| `id` | uuid PK | |
| `cnpj` | text FK → empresas | |
| `nome_socio` | text | |
| `qualificacao` | text | ex: "Sócio-Administrador" |
| `cpf` | text null | chave da ponte quando disponível |
| `contato_b2c_id` | FK → fenice_tim_contatos, null | **a ponte** — preenchido quando casa com um contato B2C |

---

## Mapeador `TIM_v1`

Converte as 25 colunas da planilha TIM → canônico. Parsing dos campos compostos:
- **Telefones:** `"(47)992082320 (alta), (47)21112000 (media)"` → `[{"numero":"5547992082320","qualidade":"alta"}, ...]` (normaliza para 55+DDD+número)
- **Emails:** split por vírgula, trim, lowercase → array; descarta vazios
- **Socios:** `"Elias Martins (Socio-Administrador),Enm Ltda. (Socio)"` → 1 linha em `fenice_b2b_socios` por sócio (nome + qualificação entre parênteses)
- **Links:** split por vírgula, trim → array
- **opcao_mei / opcao_simples:** `"NAO"`/`"SIM"` → bool
- **data_abertura:** `"23/06/2006"` → date (dd/mm/aaaa)
- **status:** mantém o valor da TIM (7 status); default "Não abordado" se vazio

Os 7 status TIM (mantidos fiéis): `Não abordado`, `Não consegui contato`, `Sem perfil`, `Sem interesse`, `Já é da TIM`, `Contrato com concorrência`, `Reunião marcada`.

---

## Importador Python

`scripts/importar_b2b.py` — funções puras testáveis + I/O:
- `parse_telefones(bruto) → list[dict]`
- `parse_emails(bruto) → list[str]`
- `parse_socios(bruto) → list[dict]`
- `parse_links(bruto) → list[str]`
- `mapear_tim_v1(linha_raw: dict) → (empresa: dict, socios: list[dict])`
- `carregar_xlsx(caminho, aba) → list[dict]` (linhas brutas via openpyxl)
- `importar(caminho, sb_url, sb_key) → dict` (grava importacao + staging + upsert empresas/socios)

Upsert por CNPJ (`on_conflict=cnpj`, merge). Re-importar atualiza sem duplicar;
`fontes` acumula a procedência. Sócios: dedup por (cnpj, nome_socio).

---

## Camada 4 · Ponte WOW (definida agora, automação futura)

Quando o Hunter decide abordar uma empresa (ou o `status` avança para
"Reunião marcada"), o dado B2B vira ação de relacionamento WOW reusando o SP-1:
1. Cria/atualiza um contato em `fenice_tim_contatos` (área `b2b`), vinculando ao CNPJ.
2. Se o telefone abordado é de um sócio, preenche `contato_b2c_id` no `fenice_b2b_socios` (fecha a ponte PF↔PJ).
3. Dispara o padrão WOW (Téo, insight, handoff ao Ramão) via a infra do SP-1.

No MVP, a Camada 4 entrega a **definição do vínculo** (empresa↔contato) e a função
que cria o contato B2B a partir de uma empresa; a automação de disparo em massa
(campanhas PAP) é fase futura.

---

## Boas Práticas Mundiais Incorporadas

| Prática | Fonte | Aplicação |
|---|---|---|
| 4 tipos de dado (contact/firmographic/technographic/intent) | Apollo/ZoomInfo/Clearbit | `operadora_atual` = technographic; scores = intent/fit |
| Separar FIT de INTENT em 2 números | Salespanel | `score_fit` e `score_intent` distintos |
| ICP como filtro sobre firmographics | Digital Applied | consulta SQL sobre porte/cnae/uf/faturamento (sem tabela extra) |
| Waterfall enrichment (várias fontes, 1 registro) | Amplemarket | `fontes` jsonb no registro canônico |
| Negative signals no funil | Bombora | os status "Sem perfil"/"Já é da TIM"/"Concorrência" |

Scoring automático e enriquecimento externo: **fase futura** (campos já preparados).

---

## Tratamento de Erros

| Falha | Comportamento |
|---|---|
| Linha sem CNPJ | grava em staging com `erro`, `processado=false`; não vai ao canônico |
| Telefone/email malformado | campo parcial (o que der para extrair); não aborta a linha |
| CNPJ duplicado no arquivo | upsert merge (última linha vence; `fontes` acumula) |
| Supabase indisponível | aborta com mensagem clara; staging não é gravado pela metade |
| Coluna ausente no formato | mapeador usa default; registra no `erro` da staging |

---

## Testes de Aceitação

1. `parse_telefones("(47)992082320 (alta), (47)21112000 (media)")` → 2 itens com qualidade e número normalizado 55...
2. `parse_emails("a@x.com,B@Y.com")` → `["a@x.com","b@y.com"]`
3. `parse_socios("Elias Martins (Socio-Administrador),Enm Ltda. (Socio)")` → 2 sócios com nome+qualificação
4. `mapear_tim_v1(linha)` → empresa canônica com `status="Não abordado"` default e sócios extraídos
5. Importar a planilha real (`docs/Prospects Ramão.xlsx`, 60 empresas) → 60 registros em `fenice_b2b_empresas`, staging preenchido, `fontes` com "TIM"
6. Re-importar o mesmo arquivo → sem duplicatas (upsert por CNPJ)
7. Consulta ICP: `descricao_cnae ILIKE '%transporte%' AND uf='SC'` retorna o subconjunto correto
8. Criar contato B2B a partir de uma empresa → linha em `fenice_tim_contatos` (área b2b) vinculada ao CNPJ

---

## Fora de Escopo (explícito)

- Cobrança / BKO / CPF → TIM.
- CRM visual (telas) + Power BI → SP-3 fase futura.
- Enriquecimento externo automático (Camada 3) + campanhas PAP em massa (Camada 4) → futuro.
- Scoring automático (fit/intent calculados) → futuro; campos preparados.
- Motor de atendimento (SP-1) → já construído.

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ — Das cinzas, ressurgimos.*
*Fenice IT · Justech.IA*
