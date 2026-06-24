---
name: juridico
description: Use when the user asks any question about Brazilian law, analyzes legal texts, needs vault navigation for legal content, works on OAB exam prep, requests legal document drafting, or any juridical task in the Fenice bRain context.
---

# Jurídico — Hub Orquestrador do Fenice bRain

## Visão Geral

Ponto de entrada unificado para toda tarefa jurídica no Fenice bRain. Identifica o tipo de trabalho e roteia para a sub-skill correta — ou executa diretamente quando não há sub-skill específica.

---

## Roteador de Sub-Skills

| Tipo de tarefa | Sub-skill a invocar |
|---|---|
| Processar texto jurídico bruto → notas atômicas Obsidian | `atomizar-juridico` |
| Avaliar qualidade de fontes / grounding de prompt | `pesquisa-juridica-elite` |
| Reconstruir lei em data passada (direito intertemporal) | `fenice-ia-01` |
| Análise com lente filosófica (Kelsen, Foucault, Gadamer…) | `fenice-ia-02` |
| Detectar antinomias / conflitos normativos | `fenice-ia-03` |
| Gerar citação ABNT/APA + fichamento com insight | `fenice-ia-04` |
| Q&A geral de direito, OAB, redação de peça processual | **executar direto** (ver seções abaixo) |

---

## Mapa do Vault — Onde Encontrar o Quê

```
Fenice_bRain/
├─ 00_APEX/
│  ├─ SUMULAS STF/Sumulas/      ← 736 súmulas STF atomizadas
│  └─ SUMULAS STJ/Sumulas/      ← 674 súmulas STJ atomizadas
├─ 01_PRIVADO/
│  └─ Codigos/CC/               ← Código Civil — notas por artigo
├─ 02_LEGISLACAO/               ← Legislação federal indexada
├─ 02_PENAL/Codigos/            ← Código Penal + jurisprudência
├─ 03_PROCESSO_CIVIL/           ← CPC + jurisprudência + fichamentos
├─ 03_PUBLICO/                  ← Direito Constitucional e Administrativo
├─ 04_TRABALHO/                 ← CLT e direito do trabalho
├─ 05_ESPECIAL/                 ← CDC, ECA, legislação especial
├─ 06_JURISCONSULTOS/           ← Doutrina — notas por jurista
├─ 07_FILOSOFIA/MAESTROS/       ← Doutrina filosófico-jurídica
├─ 08_ENSINO/                   ← Material didático
└─ _sistema/OAB/                ← Estatuto da OAB (Lei 8.906) atomizado
```

---

## Protocolo para Q&A Jurídico Direto

Ao responder perguntas de direito sem sub-skill específica:

1. **Buscar no vault primeiro** — usar `mcp__mcpvault__search_notes` com o tema antes de usar conhecimento geral
2. **Prioridade de fontes** (do mais para o menos confiável):
   - Texto legal oficial (Planalto / vault)
   - Súmulas STF/STJ do vault
   - Doutrina Tier A ingerida (`06_JURISCONSULTOS/`, `07_FILOSOFIA/`)
   - Conhecimento do modelo (declarar explicitamente quando usado)
3. **Sempre citar** — artigo, súmula ou autor; nunca afirmar tese sem âncora
4. **Sinalizar divergência** — quando houver posição majoritária vs. minoritária, indicar explicitamente

---

## OAB — Protocolo de Estudo

Para questões de OAB e estudo do Estatuto da OAB:

- **Fonte primária:** `_sistema/OAB/` — artigos da Lei 8.906 atomizados
- **Formato de resposta de questão:**
  ```markdown
  **Gabarito:** [letra]
  **Fundamento:** [artigo X, §Y da Lei 8.906 ou CED]
  > [!WARNING] Pegadinha
  > [ponto de atenção que gera erro frequente]
  ```
- **Temas recorrentes em prova:** imunidades do advogado (art. 7º), impedimentos e incompatibilidades (arts. 27–28), honorários (arts. 22–24), Tribunal de Ética (arts. 49–50), prescrição disciplinar (art. 43)
- Sempre verificar se a questão pede o **Estatuto** (Lei 8.906) ou o **CED** (Código de Ética e Disciplina)

---

## Redação de Peças Processuais

Para redigir petições, contratos ou documentos jurídicos:

1. **Identificar o rito:** qual o procedimento aplicável (CPC, CLT, Juizados, etc.)
2. **Estrutura mínima de petição inicial:**
   - Endereçamento → Qualificação das partes → Dos Fatos → Do Direito → Do Pedido → Valor da causa
3. **Invocar `fenice-ia-04`** ao final para gerar referências ABNT dos dispositivos citados
4. **Linguagem:** formal, precisa, sem jargões desnecessários — clareza favorece o julgador

---

## Callouts Obsidian — Padrão do Vault

Ao gerar notas ou análises para salvar no vault, usar:

| Tipo | Uso |
|---|---|
| `> [!NOTE]` | Observação geral / conceito |
| `> [!TIP]` | Tese favorável / dica prática |
| `> [!WARNING]` | Pegadinha / ponto de atenção em prova |
| `> [!DANGER]` | Erro fatal / posição sumulada contrária |
| `> [!QUOTE]` | Citação de doutrina ou jurisprudência |
| `> [!EXAMPLE]` | Caso concreto / exemplo prático |

---

## API Fenice (quando disponível)

| Endpoint | Uso |
|---|---|
| `POST /buscar` | Pesquisa FTS na legislação indexada (free) |
| `POST /analisar` | Análise jurídica com grounding RAG (premium) |
| `POST /hermeneutica` | Interpretação com lente filosófica (premium) |

Iniciar: `uvicorn scripts.api_fenice_saas:app --reload` em `C:\Fenice_bRain\`
