# Padrão Fenice para Código do Consumidor (Lei 8.078/1990)

## Visão Geral

Este documento define o padrão de estruturação para os 119 artigos da Lei 8.078/1990 (Código do Consumidor) no Fenice bRain. O padrão segue a metodologia consolidada do Fenice, adaptada às especificidades do direito consumerista.

---

## 1. Estrutura do Frontmatter YAML

O frontmatter YAML deve conter os seguintes campos:

```yaml
---
artigo: "número" # String com o número do artigo (ex: "1", "48-A")
lei: "Lei 8.078/1990 (Código do Consumidor)" # Identificação da lei
titulo: "Título descritivo do artigo" # Breve descrição do conteúdo
livro: "LIVRO-I" ou "LIVRO-II" ou "LIVRO-III" ou "DISPOSIÇÕES GERAIS" # Organização
tipo_norma: "protetor" ou "processual" ou "penal" ou "sanção" # Classificação
relevancia: "crítica" ou "alta" ou "média" ou "baixa" # Importância prática
status: "vigente" # Status jurídico (sempre vigente para Lei 8.078/1990)
tags: # Array de tags
  - direito-do-consumidor
  - lei-8078
  - livro-X # (livro-i, livro-ii, livro-iii, disposicoes-gerais)
  - tipo-X # (protetor, processual, penal, sanção)
  - aplicacao-X # (exemplo: consumidor, fornecedor, produto-servico)
created: "2026-06-06" # Data de criação
---
```

### Notas sobre os Campos

**artigo:**
- String com o número do artigo
- Exemplo: "1", "2-A", "48-B"

**lei:**
- Sempre: `Lei 8.078/1990 (Código do Consumidor)`

**titulo:**
- Descrição concisa e clara do tema central
- Extraído diretamente da ementa legal ou paráfrase dela
- Exemplo: "Direitos básicos do consumidor"

**livro:**
- LIVRO-I: Das Disposições Gerais (Arts. 1-8)
- LIVRO-II: Da Proteção ao Consumidor (Arts. 9-108)
- LIVRO-III: Da Defesa do Consumidor em Juízo (Arts. 109-119)
- DISPOSIÇÕES GERAIS: Para artigos fora dos livros

**tipo_norma:**
- `protetor`: Direitos e proteções (ex: Art. 6º — direitos básicos)
- `processual`: Procedimentos e ações (ex: Arts. 109-119 — defesa em juízo)
- `penal`: Infrações e sanções penais (ex: Arts. 61-66 — crimes)
- `sanção`: Sanções administrativas/civis (ex: Arts. 56-60 — sanções)

**relevancia:**
- `crítica`: Artigos fundamentais (direitos básicos, princípios, causas de dano)
- `alta`: Artigos frequentemente aplicados (prazos, direitos específicos)
- `média`: Artigos importantes, mas contextuais
- `baixa`: Artigos complementares ou procedimentais

**tags:**
- `direito-do-consumidor`: Tag geral, presente em todos
- `lei-8078`: Tag geral, presente em todos
- `livro-i`, `livro-ii`, `livro-iii`, `disposicoes-gerais`: Organização
- `protetor`, `processual`, `penal`, `sanção`: Tipo de norma
- `consumidor`, `fornecedor`, `produto-servico`, `credito`, `seguranca`: Aplicação específica

---

## 2. Estrutura do Corpo do Documento

### Título (H1)

```markdown
# CDC Art. X — [Título Descritivo]
```

Formato: `CDC Art. [número] — [título]`

Exemplo: `# CDC Art. 6 — Direitos básicos do consumidor`

---

### Metadados Header

```markdown
**Lei:** Lei 8.078/1990 (Código do Consumidor)
**Livro:** LIVRO-I — Das Disposições Gerais
**Tipo:** Protetor
**Status:** ✅ VIGENTE
**Relevância:** Crítica
```

---

### Seção 1: Redação Legal

```markdown
## 📋 REDAÇÃO LEGAL

> [TEXTO COMPLETO DO ARTIGO]
> § 1º [Parágrafo primeiro, se houver]
> § 2º [Parágrafo segundo, se houver]
> [Incisos e alíneas, se houver]
```

**Notas:**
- Usar blockquote (`>`) para destacar o texto legal
- Incluir TODOS os parágrafos, incisos e alíneas
- Manter formatação com numeração clara

---

### Seção 2: Análise Técnica

```markdown
## 🔍 ANÁLISE TÉCNICA

### Conceito Central

[Parágrafo explicativo sobre o conceito-chave do artigo]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Aspecto 1** | Descrição detalhada |
| **Aspecto 2** | Descrição detalhada |
| **Aspecto 3** | Descrição detalhada |

### Diferenças Práticas

[Se aplicável: tabela ou lista de variações, exceções, aplicações práticas]

### Aplicação Prática

[Cenários reais de aplicação, exemplos de casos]
```

**Exemplo para Art. 6 (Direitos Básicos):**

| Elemento | Descrição |
|----------|-----------|
| **Direito à vida, saúde e segurança** | Produtos/serviços não podem acarretar riscos iminentes |
| **Direito à informação clara** | Fornecedor deve informar preço, características e riscos |
| **Direito de livre escolha** | Consumidor pode recusar oferta sem penalidades |
| **Direito à qualidade** | Produto/serviço deve corresponder à oferta realizada |
| **Direito ao arrependimento** | 7 dias para desistência em compras fora do estabelecimento |

---

### Seção 3: Artigos Correlatos

```markdown
## 🔗 ARTIGOS CORRELATOS

- [[Art. X]] — Direitos básicos (contexto geral)
- [[Art. Y]] — Responsabilidade civil (consequência)
- [[Art. Z]] — Sanções (execução)
```

**Notas:**
- Listar artigos que complementam, explicam ou aplicam o artigo
- Usar links internos Obsidian `[[Art. X]]`
- Máximo 5-7 artigos por seção

---

### Seção 4: Jurisprudência

```markdown
## ⚖️ JURISPRUDÊNCIA

### STF (Supremo Tribunal Federal)

[Precedentes STF, se houver]

### STJ (Superior Tribunal de Justiça)

[Precedentes STJ, se houver]

### Tribunais Regionais

[Precedentes de TRFs, TJs, quando relevantes]
```

**Formato de precedente:**

- **Decisão:** [Número do julgamento] — [Ementa breve]
- **Data:** [Data]
- **Órgão:** STF/STJ/TRF/TJ
- **Relação com Art. X:** [Como interpreta ou aplica o artigo]

---

### Seção 5: Casos Práticos

```markdown
## 📌 CASOS PRÁTICOS

### Caso 1: [Título Descritivo]

**Cenário:** [Descrição do fato]

**Questão jurídica:** [Qual é a questão?]

**Aplicação do CDC:**
- Artigo aplicável: Art. X
- Razão: [Explicação]

**Resultado esperado:** [Conclusão]

---

### Caso 2: [Título Descritivo]

[Mesmo formato]
```

---

### Seção 6: Alterações e Atualizações

```markdown
## 📅 ALTERAÇÕES E ATUALIZAÇÕES

| Data | Alteração | Lei | Situação |
|------|-----------|-----|----------|
| [data] | [descrição da alteração] | [Lei/Decreto] | ✅ Vigente |
```

**Nota:** Incluir apenas se houver alterações legais significativas.

---

### Rodapé (Footer)

```markdown
---

**Última atualização:** 2026-06-06
**Fonte:** Planalto.gov.br
**Vigência:** Confirmada até hoje
**Próxima revisão:** [Data sugerida, se houver]
```

---

## 3. Estrutura Completa: Template Padrão

```markdown
---
artigo: "6"
lei: Lei 8.078/1990 (Código do Consumidor)
titulo: "Direitos básicos do consumidor"
livro: LIVRO-II
tipo_norma: protetor
relevancia: crítica
status: vigente
tags:
  - direito-do-consumidor
  - lei-8078
  - livro-ii
  - protetor
  - direitos-basicos
created: 2026-06-06
---

# CDC Art. 6 — Direitos básicos do consumidor

**Lei:** Lei 8.078/1990 (Código do Consumidor)
**Livro:** LIVRO-II — Da Proteção ao Consumidor
**Tipo:** Protetor
**Status:** ✅ VIGENTE
**Relevância:** Crítica

---

## 📋 REDAÇÃO LEGAL

> São direitos básicos do consumidor:
> I - a proteção da vida, saúde e segurança contra riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou prejudiciais;
> II - a educação e divulgação sobre o consumo adequado dos produtos e serviços, asseguradas a liberdade de escolha e a igualdade nas contratações;
> III - a informação adequada e clara sobre os diferentes produtos e serviços, com especificação correta de quantidade, características, composição, qualidade, preço e riscos que apresentem;
> IV - a proteção contra publicidade enganosa e abusiva, métodos comerciais coercitivos ou desleais, bem como práticas e cláusulas abusivas ou impostas no fornecimento de produtos e serviços;
> V - a proteção contratual, com meios adequados para viabilizar o resgate de direitos;
> VI - a reparação integral dos danos patrimoniais e morais, individual ou coletivamente, por vícios em produtos e serviços oferecidos no mercado de consumo, sem prejuízo de outras fontes de reparação previstas em lei;
> VII - o acesso aos órgãos judiciários e administrativos com vistas à prevenção ou reparação de danos patrimoniais e morais, assegurada a proteção Jurídica, administrativa e técnica aos necessitados;
> VIII - a facilitação da defesa de seus direitos, inclusive a inversão do ônus da prova, a seu favor, no processo civil, quando, a critério do juiz, for verossímil a alegação ou quando for ele hipossuficiente, segundo as regras ordinárias de experiências;
> IX - (Vetado);
> X - a adequada e eficaz prestação dos serviços públicos em geral.

---

## 🔍 ANÁLISE TÉCNICA

### Conceito Central

O Artigo 6º é o coração protetor do CDC, enumerando os direitos fundamentais do consumidor. Diferentemente de direitos patrimoniais tradicionais, estes são direitos existenciais que protegem vida, dignidade e acesso à justiça.

### Elementos-Chave

| Direito | Descrição |
|---------|-----------|
| **Proteção à vida e saúde (Inciso I)** | Produtos/serviços não podem expor a riscos iminentes à vida ou saúde |
| **Educação e liberdade (Inciso II)** | Direito a informações sobre consumo adequado; não pode haver coação |
| **Informação clara (Inciso III)** | Quantidade, características, composição, qualidade, preço e riscos devem ser explicitados |
| **Proteção contra publicidade enganosa (Inciso IV)** | Anúncios devem ser verdadeiros; proibem-se práticas coercitivas ou desleais |
| **Proteção contratual (Inciso V)** | Contratos devem permitir o exercício de direitos efetivamente |
| **Reparação integral (Inciso VI)** | Danos materiais E morais são indenizáveis, individual ou coletivamente |
| **Acesso à justiça (Inciso VII)** | Direito a órgãos judiciários e administrativos; proteção aos hipossuficientes |
| **Inversão do ônus da prova (Inciso VIII)** | Em processo civil, consumidor pode se beneficiar da inversão a seu favor |
| **Serviços públicos (Inciso X)** | Serviços públicos essenciais devem ser prestados adequadamente |

### Aplicação Prática

- **Compra de produto defeituoso:** Consumidor pode exigir reparação integral (danos materiais + morais)
- **Publicidade enganosa:** Empresa não pode anunciar características inexistentes
- **Contrato abusivo:** Cláusula que prejudica direitos do consumidor é nula
- **Serviço inadequado:** Fornecedor responde por falha na prestação

---

## 🔗 ARTIGOS CORRELATOS

- [[Art. 1]] — Conceito e objetivos do CDC
- [[Art. 2]] — Definição de consumidor
- [[Art. 3]] — Definição de fornecedor
- [[Art. 30]] — Informação e publicidade
- [[Art. 35]] — Responsabilidade pelo vício do produto
- [[Art. 56]] — Sanções administrativas

---

## ⚖️ JURISPRUDÊNCIA

### STJ (Superior Tribunal de Justiça)

- **Súmula 383 STJ:** "Da vigência da Lei 8.078/1990, não cabe mais falar em culpa do consumidor, na hipótese de vício do produto ou do serviço"
- **REsp 1.195.995/RJ (2012):** Reafirma o direito à reparação integral de danos morais em caso de publicidade enganosa
- **REsp 1.271.286/RS (2011):** Consumidor tem direito à inversão do ônus da prova quando verossímil sua alegação

---

## 📌 CASOS PRÁTICOS

### Caso 1: Produto Defeituoso com Dano à Saúde

**Cenário:** Consumidor compra medicamento que causa reação alérgica grave não informada na embalagem. Necessita internação.

**Questão jurídica:** Qual é a responsabilidade da empresa? Qual indenização?

**Aplicação do CDC:**
- **Art. 6º, Inciso I:** Proteção à vida e saúde foi violada (risco não informado)
- **Art. 6º, Inciso III:** Informação sobre riscos foi inadequada
- **Art. 6º, Inciso VI:** Direito à reparação integral (danos materiais + morais)

**Resultado esperado:** Indenização por danos patrimoniais (internação, medicamentos) e morais (sofrimento, risco à vida).

---

### Caso 2: Publicidade Enganosa

**Cenário:** Loja anuncia "50% de desconto" em todos os produtos. Consumidor chega à loja e descobre que o desconto só vale para 3 itens específicos.

**Questão jurídica:** Há violação de direitos do consumidor?

**Aplicação do CDC:**
- **Art. 6º, Inciso II:** Liberdade de escolha foi prejudicada (consumidor foi atraído sob falsa promessa)
- **Art. 6º, Inciso IV:** Publicidade enganosa é proibida
- **Art. 37:** Publicidade enganosa é ato ilícito

**Resultado esperado:** Empresa deve cumprir a promoção como anunciada ou indenizar consumidor.

---

## 📅 ALTERAÇÕES E ATUALIZAÇÕES

| Data | Alteração | Lei | Situação |
|------|-----------|-----|----------|
| 1990 | Criação original do CDC | Lei 8.078/90 | ✅ Vigente |
| 1997 | Lei 9.469 — Ação coletiva | Lei 9.469/97 | ✅ Vigente |

---

**Última atualização:** 2026-06-06
**Fonte:** Planalto.gov.br
**Vigência:** Confirmada até hoje
```

---

## 4. Diferenças vs. Código Penal

| Aspecto | Código Penal | CDC |
|--------|-------------|-----|
| **Frontmatter** | `nomen`, `tipo_pena`, `pena_min/max`, `prescricao_anos` | `titulo`, `tipo_norma`, `relevancia`, `aplicacao` |
| **Foco** | Crimes e penas | Direitos e proteções |
| **Tabelas** | Dosimetria, pena-base | Direitos/deveres, elementos-chave |
| **Jurisprudência** | STF/STJ sobre crimes | STF/STJ sobre direito consumerista |
| **Aplicação** | Processual penal | Processual civil |

---

## 5. Diferenças vs. Direito Civil

| Aspecto | Direito Civil | CDC |
|--------|-------------|-----|
| **Frontmatter** | `tipo: direito-civil`, `livro: LIVRO-I/II/III/IV/V` | `tipo_norma: protetor/processual/penal/sanção`, `livro: LIVRO-I/II/III` |
| **Foco** | Relações civis gerais | Relações de consumo específicas |
| **Tags** | `cc`, `direito-civil` | `lei-8078`, `direito-do-consumidor` |
| **Princípios** | Autonomia, liberdade contratual | Proteção ao hipossuficiente, princípio pro-consumidor |

---

## 6. Checklist de Estrutura

Ao criar um artigo do CDC, validar:

- [ ] Frontmatter YAML completo com todos os 7 campos
- [ ] Título H1 no formato `# CDC Art. X — [Título]`
- [ ] Metadados header (Lei, Livro, Tipo, Status, Relevância)
- [ ] Seção 📋 REDAÇÃO LEGAL com texto completo
- [ ] Seção 🔍 ANÁLISE TÉCNICA com Conceito + Elementos + Aplicação
- [ ] Seção 🔗 ARTIGOS CORRELATOS (3-7 artigos)
- [ ] Seção ⚖️ JURISPRUDÊNCIA (STJ, STF, se houver)
- [ ] Seção 📌 CASOS PRÁTICOS (2-3 cenários, se aplicável)
- [ ] Seção 📅 ALTERAÇÕES (se houver mudanças legais)
- [ ] Rodapé com última atualização e fonte

---

## 7. Dicas Práticas

1. **Completude:** Incluir TODOS os parágrafos, incisos e alíneas na seção REDAÇÃO LEGAL
2. **Clareza:** Usar linguagem acessível; explicar termos técnicos
3. **Relevância:** Priorizar jurisprudência STJ sobre CDC (especializada)
4. **Conectividade:** Usar `[[Art. X]]` para criar rede de conhecimento
5. **Atualizações:** Revisar anualmente ou quando houver alterações legais
6. **Exemplos:** Preferir casos reais ao invés de hipotéticos quando possível

---

## 8. Livros da Lei 8.078/1990

- **LIVRO-I — Das Disposições Gerais (Arts. 1-8):** Conceitos, princípios, definições
- **LIVRO-II — Da Proteção ao Consumidor (Arts. 9-108):** Direitos, obrigações, responsabilidade
- **LIVRO-III — Da Defesa do Consumidor em Juízo (Arts. 109-119):** Procedimentos, legitimidade, ações coletivas

---

**Documento de referência:** Padrão Fenice para Código do Consumidor
**Versão:** 1.0
**Última atualização:** 2026-06-06
**Responsável:** Sistema Fenice bRain
