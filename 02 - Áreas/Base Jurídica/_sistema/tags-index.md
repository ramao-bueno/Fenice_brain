---
type: índice
created: 2026-06-06
updated: 2026-06-06
status: ativo
---

# 🏷️ TAGS-INDEX — Índice Centralizado de Tags

**Última atualização:** 2026-06-06
**Função:** Descoberta de conteúdo por tema + navegação de conhecimento

---

## 📚 TAGS POR ÁREA DE CONHECIMENTO

### Direito — Códigos Principais

#### Código Civil (CC) — Lei 10.406/2002
- `cc` — Referências gerais
- `lei-10406` — Identificador
- `direito-civil` — Área
- `livro-i` a `livro-v` — Livros (Parte Geral, Obrigações, Coisas, Família, Sucessões)
- `cc-art-{numero}` — Artigos específicos

#### Constituição Federal (CF/88)
- `cf88` — Identificador
- `constituicao` — Área
- `titulo-i` a `titulo-ix` — Títulos (Princípios, Direitos, Organização, Poderes, Defesa, Tributação, Ordem Econômica, Ordem Social, Disposições Gerais)
- `cf-art-{numero}` — Artigos específicos
- `principios-fundamentais`, `direitos-fundamentais`, `organizacao-estado`, `organizacao-poderes`, `defesa-estado`, `tributacao`, `ordem-economica`, `ordem-social`, `disposicoes-gerais` — Temas

#### Código de Processo Civil (CPC) — Lei 13.105/2015
- `cpc` — Identificador
- `lei-13105` — Identificador
- `processo-civil` — Área
- `livro-i` a `livro-iv` — Livros (Normas Processuais, Conhecimento, Execução, Especiais)
- `cpc-art-{numero}` — Artigos específicos

#### Código do Consumidor (CDC) — Lei 8.078/1990 ⭐ NOVO
- `cdc` — Identificador
- `lei-8078` — Identificador
- `direito-do-consumidor` — Área
- `livro-i` a `livro-iv` — Livros (Direitos, Infrações Penais, Processo, Disposições Gerais)
- `cdc-art-{numero}` — Artigos específicos
- Aplicações temáticas:
  - `relacao-de-consumo` — Arts. 1-3
  - `direitos-basicos` — Arts. 4-6
  - `compra-e-venda` — Arts. 18-27
  - `contratos` — Arts. 28-35
  - `publicidade` — Arts. 36-38
  - `praticas-abusivas` — Arts. 39-41
  - `responsabilidade-civil` — Arts. 12-17
  - `credito-ao-consumidor` — Arts. 49-60
  - `infrações-penais` — Arts. 61-78
  - `processo-administrativo` — Arts. 79-105

#### Código Penal (CP) — Lei 8.072/1940
- `cp` — Identificador
- `direito-penal` — Área
- `crime` — Tipo de norma
- Grupos: `crimes-contra-a-vida`, `crimes-contra-a-honra`, `crimes-contra-propriedade`, etc.

#### Código de Processo Penal (CPP)
- `cpp` — Identificador
- `processo-penal` — Área

### Análise de Normas

#### Tipo de Norma
- `protetor` — Protege direitos/interesses (ex: CDC Art. 4)
- `processual` — Regula procedimentos (ex: CPC, CPP)
- `penal` — Define crimes/infrações
- `sanção` — Consequências jurídicas
- `principiologico` — Estabelece princípios (ex: CF, Lei 8.078 Art. 4)
- `substantivo` — Direito material
- `adjetivo` — Direito processual

#### Aplicação Prática
- `relacao-de-consumo` — Transações consumidor-fornecedor
- `compra-e-venda` — Vendas de produtos/serviços
- `prestacao-servico` — Prestação de serviços
- `publicidade` — Publicidade e marketing
- `garantia-e-durabilidade` — Garantias de produtos
- `credito-ao-consumidor` — Financiamento/crédito
- `responsabilidade-civil` — Indenizações
- `protecao-dados` — LGPD e privacidade
- `prazo-prescricao` — Prazos legais
- `acao-coletiva` — Ação coletiva/difusa

### Hierarquia Jurídica

- `constituicao` — Nível 1 (supremo)
- `lei-ordinaria` — Nível 2
- `decreto` — Nível 3
- `resolucao` — Regulamentação

---

## 🔍 COMO BUSCAR

### Por Lei
```
Busca: #lei-8078
Resultado: Todos os 119 artigos do CDC
```

### Por Tema
```
Busca: #credito-ao-consumidor
Resultado: Arts. 49-60 CDC (crédito ao consumidor)

Busca: #compra-e-venda
Resultado: Arts. 18-27 CDC + Arts. relevantes CC
```

### Por Tipo
```
Busca: #tipo-protetor
Resultado: Artigos que protegem direitos

Busca: #tipo-penal
Resultado: Artigos que definem crimes
```

### Pesquisa Integrada
```
Busca: #cc #responsabilidade-civil
Resultado: Artigos sobre responsabilidade civil no CC

Busca: #cdc #cpc
Resultado: Artigos do CDC que referem CPC (processo)
```

---

## 📊 COBERTURA ATUAL

| Lei | Artigos | Tags | Status |
|---|---|---|---|
| **CF/88** | 250 | ✅ Completo | 🟢 Ativo |
| **CC** | 2.036 | ✅ Completo | 🟢 Ativo |
| **CPC** | 1.072 | ✅ Completo | 🟢 Ativo |
| **CDC** | 119 | ✅ Completo | 🟢 **NOVO** |
| **CP** | ~400 | ✅ Parcial | 🟡 Parcial |
| **LINDB** | 30 | ✅ Completo | 🟢 Ativo |
| **STF Súmulas** | 736 | ✅ Completo | 🟢 Ativo |
| **CJF Enunciados** | 262 | ✅ Completo | 🟢 Ativo |

---

## 🔄 ROTINA DE REINDEXAÇÃO

### Atualização Automática
- **Frequência**: A cada novo artigo criado
- **Trigger**: Script de regeneração (Python)
- **Ação**: Aplica tags automáticas + atualiza índices
- **Validação**: Lint de tags via script

### Manual (Ad-hoc)
```bash
# Verificar tags órfãs
grep -r "^tags:" . | grep -v "#direito\|#lei\|#codigo" | head -20

# Reindexar seção específica (ex: CDC)
find "08_CÓDIGO_CONSUMIDOR" -name "*.md" | xargs grep -h "^tags:" | sort -u
```

---

## 📋 TAGS OBRIGATÓRIAS

Cada nota deve ter minimamente:
1. **Identificador da lei** (`#lei-XXXXX`, `#cc`, `#cf88`, etc)
2. **Área de conhecimento** (`#direito-civil`, `#processo-civil`, `#direito-do-consumidor`)
3. **Localização** (`#livro-X`, `#titulo-X`, `#capitulo-X`)
4. **Tipo de norma** (`#tipo-protetor`, `#tipo-penal`, `#tipo-processual`)

---

## 🎯 TAGS RECOMENDADAS (Aplicação)

Adicione conforme relevante:
- `#relacao-de-consumo` — Se menciona relação consumidor-fornecedor
- `#compra-e-venda` — Se é sobre venda de produto/serviço
- `#responsabilidade-civil` — Se aborda indenização
- `#credito-ao-consumidor` — Se é sobre financiamento/crédito
- `#publicidade` — Se menciona publicidade/marketing
- `#garantia-e-durabilidade` — Se trata de garantia
- `#acao-coletiva` — Se habilita ação coletiva/difusa
- `#prazo-prescricao` — Se estabelece prazo/prescrição

---

## 🔗 RELACIONAMENTOS

Tags vinculadas automaticamente (Obsidian Graph):
- `#cc` ↔️ `#responsabilidade-civil` (CC Arts. 186-188 base)
- `#cc` ↔️ `#garantia-e-durabilidade` (CC Arts. 441-460)
- `#cpc` ↔️ `#acao-coletiva` (CPC Arts. 81-150)
- `#cdc` ↔️ `#cc` (CDC se aplica subsidiariamente)
- `#cdc` ↔️ `#cpc` (Processo do CDC segue CPC)
- `#cf88` ↔️ `#direitos-fundamentais` (CF Arts. 5-17)

---

## 📝 ÚLTIMA ATUALIZAÇÃO

- **Data**: 2026-06-06 23:30 UTC
- **Adição**: Integração CDC (119 artigos + tags temáticas)
- **Responsável**: Claude Haiku 4.5
- **Próxima revisão**: 2026-07-06

---

**Usar este índice para:**
1. ✅ Descobrir artigos por tema
2. ✅ Navegar o graph de conhecimento
3. ✅ Validar tagueamento
4. ✅ Planejar integração de novas leis
