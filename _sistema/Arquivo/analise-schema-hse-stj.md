---
type: análise-técnica
projeto: Fenice-Brain
tema: Homologação-Sentença-Estrangeira
tags: [hse, stj, jurisprudência, legaltech, schema-json]
created: 2026-06-07
status: ativo
---

# 📋 ANÁLISE DO SCHEMA JSON — HOMOLOGAÇÃO DE SENTENÇA ESTRANGEIRA (HSE)

**Data da Análise:** 2026-06-07
**Contexto:** Estruturação de dados para jurisprudência processual internacional

---

## 🎯 PROPÓSITO DO SCHEMA

Este JSON schema foi **projetado para estruturar decisões de Homologação de Sentença Estrangeira (HSE)** do Superior Tribunal de Justiça (STJ), permitindo:

1. ✅ **Captura sistematizada** de dados processuais
2. ✅ **Análise automática** de requisitos legais
3. ✅ **Rastreamento de compliance** em operações transnacionais
4. ✅ **Integração com sistemas de IA** (análise de risco, classificação)

---

## 🔍 DECOMPOSIÇÃO DO SCHEMA

### 1️⃣ **`metadados_processuais`** — Identificação

```json
{
  "numero_processo": "HDE 1.234",      // Homologação de Decisão Estrangeira
  "relator": "Ministro X",              // Responsável pela relatoria
  "orgao_julgador": "CORTE ESPECIAL",   // Colegiado que julgou
  "data_julgamento": "YYYY-MM-DD",      // Data da decisão
  "pais_de_origem": "Portugal"          // Jurisdição estrangeira
}
```

**Propósito:** Rastreabilidade + citação jurídica
**Aplicação Fenice:** Ligar a HSE ao artigo do [[CPC Arts. 960-965]] (ação de homologação)

---

### 2️⃣ **`resultado_homologacao`** — Desfecho

```json
{
  "status": "DEFERIDO | INDEFERIDO | PARCIALMENTE DEFERIDO",
  "fundamento_principal": "string resumida"
}
```

**O que significa:**
- **DEFERIDO** → Decisão estrangeira é executável no Brasil (tem força de título executivo)
- **INDEFERIDO** → Decidiu-se que a decisão viola direito brasileiro
- **PARCIALMENTE DEFERIDO** → Homologa apenas parte da decisão

**Conexão com CDC:** Se a decisão estrangeira é sobre direitos do consumidor, CDC Arts. 1-6 (direitos básicos) + Art. 80 (ação coletiva) precisam ser considerados!

---

### 3️⃣ **`checklist_requisitos`** — Gatekeeping Jurídico ⭐

Este é o **coração** do schema. Representa os **4 requisitos legais para HSE**:

```json
{
  "transito_em_julgado_comprovado": boolean,    // ✓ Decisão é definitiva no país de origem?
  "citacao_valida": boolean,                    // ✓ Réu foi citado validamente?
  "violacao_ordem_publica": boolean,            // ✗ Viola ordem pública brasileira?
  "incompetencia_absoluta_brasil": boolean      // ✗ Matéria de competência exclusiva do Brasil?
}
```

**Mapeamento para CPC:**
- **Trânsito em julgado** → CPC Art. 501 (definição)
- **Citação válida** → CPC Arts. 344-360 (notificação processual)
- **Ordem pública** → CPC Art. 966 III (motivo de indeferimento)
- **Incompetência absoluta** → CPC Arts. 63-76 (competência do juiz)

**Decisão:** Se **qualquer campo é FALSE**, a HSE deve ser **INDEFERIDA** (exceto ordem_publica e incompetencia_absoluta, que se TRUE levam ao indeferimento).

---

### 4️⃣ **`analise_coercitiva`** — Análise Material

```json
{
  "objeto_da_decisao": "Alimentos | Divórcio Qualificado | Sentença Arbitral | Cobrança",
  "detalhe_da_citacao": "Como réu foi notificado (validade formal + revelia)",
  "tese_juridica_fixada": "Entendimento adotado pela Corte sobre o tema"
}
```

**Por que "coercitiva"?** Porque avalia se a decisão estrangeira:
- ✅ É **executável** (tem caráter de sentença condenatória)
- ✅ **Não viola** direito brasileiro
- ✅ **Pode gerar** execução forçada (penhora, até desapropriação)

**Aplicação prática:**
- Divórcio com alimentos: executável no Brasil (CPC Art. 515 II)
- Sentença arbitral comercial: executável se não violar ordem pública
- Cobrança: executável se crédito é documentado

---

### 5️⃣ **`risco_compliance`** — Avaliação para LegalTech ⚠️

```json
{
  "score_complexidade": "LOW | MEDIUM | HIGH",
  "observacao_critica": "Tendências / alertas para sistemas"
}
```

**Scoring proposto:**

| Complexidade | Critérios | Exemplo |
|---|---|---|
| **LOW** | Requisitos claros, consenso entre ministros | Cobrança simples, citação irretocável |
| **MEDIUM** | Um requisito divergente, jurisprudência mista | Alimentos com cálculo controverso |
| **HIGH** | Questão de ordem pública, conflito de ministros | Divórcio + guarda com sistema diferente |

**Alertas críticos para compliance:**
- ⚠️ **Ordem pública pode ser questionada** → Risco de execução ser suspensa
- ⚠️ **Divergência de ministros** → Precedente pode mudar (baixa segurança jurídica)
- ⚠️ **Matéria nova** → Sem jurisprudência consolidada

---

## 🔗 CONEXÃO COM FENICE BRAIN

### **Mapeamento: HSE ↔ Códigos Estruturados**

```
HSE (STJ)
  ├─ CPC (1.072 artigos)
  │   ├── Arts. 960-965 — Homologação de sentença estrangeira ⭐
  │   ├── Arts. 344-360 — Citação (validação de req. 3)
  │   ├── Arts. 63-76 — Competência (validação de req. 4)
  │   └── Arts. 515-526 — Títulos executivos
  │
  ├─ CC (2.036 artigos)
  │   ├── Arts. 1-10 — Introdução (aplicabilidade lei estrangeira)
  │   ├── Art. 4 — Direitos básicos (ordem pública)
  │   └── Arts. 1.511-1.638 — Direito de Família (divórcio, alimentos)
  │
  ├─ CF/88 (250 artigos)
  │   ├── Art. 5 II — Direitos fundamentais (ordem pública)
  │   └── Art. 102 II a — Competência STF
  │
  └─ CDC (119 artigos) ⭐ NOVO
      ├── Art. 4 — Direitos básicos do consumidor (ordem pública)
      ├── Art. 6 VI — Inversão de ônus (em HSE de consumo)
      └── Art. 80-105 — Ação coletiva (aplicável a sentença estrangeira coletiva)
```

---

## ⚡ MELHORIAS SUGERIDAS PARA O SCHEMA

### Adição 1: **Tipo de HSE**

```json
"tipo_hse": "SENTENÇA_ESTRANGEIRA | SENTENÇA_ARBITRAL | LAUDO_ARBITRAL_COMERCIAL"
```

**Motivo:** Cada tipo tem requisitos ligeiramente diferentes (CPC Arts. 960-965 vs 965-A para arbitrais).

---

### Adição 2: **Vinculação com Precedentes STJ**

```json
"jurisprudencia": {
  "precedente_aplicavel": "REsp 1.234.567/XX",
  "orientacao_stj": "HSE deferida quando...",
  "divergencia_possivel": boolean
}
```

**Motivo:** HSE segue jurisprudência consolidada; sistema LegalTech precisa rastrear mudanças.

---

### Adição 3: **Risco de Revisão**

```json
"risco_revisao": {
  "possibilidade_recurso": "NENHUMA | EMBARGOS_DIVERGENCIA | EXTRAORDINARIO",
  "prazo_prescricao_execucao": "dias",
  "estabilidade_precedente": "CONSOLIDADO | PENDENTE | CONFLITUOSO"
}
```

**Motivo:** Executar uma HSE com recurso possível é risco operacional para o cliente.

---

### Adição 4: **Integração com CDC** (SE aplicável)

```json
"direito_do_consumidor": {
  "aplica_cdc": boolean,
  "artigos_cdc_relevantes": ["Art. 4", "Art. 6 VI", "Art. 80"],
  "conflito_com_ordem_publica_cdc": "descrição"
}
```

**Motivo:** Se a HSE é sobre sentença estrangeira que afeta direitos de consumidor brasileiro, CDC é obrigatório!

---

## 📊 CASOS DE USO DO SCHEMA

### Caso 1: **Alimentos de Estrangeiro (Portugal → Brasil)**

```json
{
  "metadados_processuais": {
    "numero_processo": "HDE 2.345",
    "relator": "Ministro João",
    "data_julgamento": "2026-06-01",
    "pais_de_origem": "Portugal"
  },
  "resultado_homologacao": {
    "status": "DEFERIDO",
    "fundamento_principal": "Requisitos preenchidos; alimentos não violam ordem pública"
  },
  "checklist_requisitos": {
    "transito_em_julgado_comprovado": true,
    "citacao_valida": true,
    "violacao_ordem_publica": false,
    "incompetencia_absoluta_brasil": false
  },
  "analise_coercitiva": {
    "objeto_da_decisao": "Alimentos",
    "detalhe_da_citacao": "Notificação pessoal ao réu; sem revelia",
    "tese_juridica_fixada": "Alimentos estrangeiros são executáveis no Brasil se validados os requisitos"
  },
  "risco_compliance": {
    "score_complexidade": "MEDIUM",
    "observacao_critica": "Valor e prazo de execução podem ser contestados em ação de execução"
  }
}
```

**Vinculação Fenice:**
- CPC Arts. 960-965 (HSE)
- CPC Arts. 910-925 (execução de alimentos)
- [[CC Arts. 1.694-1.710]] (alimentos)

---

### Caso 2: **Sentença Arbitral Comercial (China → Brasil)**

```json
{
  "tipo_hse": "SENTENÇA_ARBITRAL",
  "objeto_da_decisao": "Sentença Arbitral Comercial",
  "resultado_homologacao": {
    "status": "PARCIALMENTE DEFERIDO",
    "fundamento_principal": "Cláusula arbitral válida, mas lucros cessantes violam ordem pública"
  },
  "checklist_requisitos": {
    "transito_em_julgado_comprovado": true,
    "citacao_valida": true,
    "violacao_ordem_publica": true,  // ⚠️ VIOLAÇÃO DETECTADA
    "incompetencia_absoluta_brasil": false
  },
  "risco_compliance": {
    "score_complexidade": "HIGH",
    "observacao_critica": "Possível embargos de divergência; executar apenas capital"
  }
}
```

**Vinculação Fenice:**
- CPC Arts. 965-A (sentença arbitral estrangeira)
- Lei 9.307/96 (Lei de Arbitragem)
- [[CF/88 Art. 5]] (ordem pública = direitos fundamentais)

---

## 🎓 APRENDIZADO PARA FENICE BRAIN

Este schema demonstra que **jurisprudência processual complexa** requer:

1. ✅ **Metadados estruturados** — Quem, quando, onde
2. ✅ **Checklist automático** — Requisitos legais binários
3. ✅ **Análise material** — O que significa juridicamente
4. ✅ **Scoring de risco** — Para sistemas de IA

**Aplicação ao CDC:**
- CDC Arts. 1-6 (direitos básicos) = "ordem pública" do direito consumerista
- CDC Art. 4 VI (inversão ônus da prova) = princípio processual que pode afetar HSE
- CDC Art. 80 (ação coletiva) = HSE de sentença coletiva estrangeira (raro, mas possível)

---

## 🚀 PRÓXIMOS PASSOS PARA FENICE

1. **Criar schema para outros processos coletivos** (ação civil pública, ação popular)
2. **Integrar CDC** ao análise de ordem pública em HSE de consumo
3. **Estruturar jurisprudência STJ** sobre HSE + CDC
4. **Automatizar scoring** baseado em padrões de decisão

---

**Análise realizada por:** Claude Haiku 4.5
**Data:** 2026-06-07
**Categoria:** Análise técnica para LegalTech
