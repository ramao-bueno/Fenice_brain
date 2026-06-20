---
nivel: ramo
tipo: index
ramo: direito-digital
tags: [direito-digital, index]
created: 2026-06-07
---

# 💻 Direito Digital — INDEX

**Cobertura:** as 4 leis substantivas do ramo + os tipos penais que duas leis
modificativas inseriram no Código Penal — formando o panorama mais completo de
Direito Digital do vault.

> Ver também [[README|README — método de interligação híbrida]] (Canvas + INDEX + YAML),
> escrito antes de este ramo ser populado e cuja proposta orientou a estrutura abaixo.

---

## 📜 Leis Substantivas (atomizadas — pipeline automático)

Extraídas via `pipeline_direito_digital.py` (regex `Art. N`, mesmo padrão validado
em Direito Internacional e Previdenciário):

| Lei | Norma | Artigos | Pasta |
|---|---|---|---|
| Marco Civil da Internet | Lei 12.965/2014 | 32 | [[Artigos/L12965/INDEX\|L12965/]] |
| Lei Geral de Proteção de Dados (LGPD) | Lei 13.709/2018 | 64 | [[Artigos/L13709/INDEX\|L13709/]] |
| Lei do Software | Lei 9.609/1998 | 16 | [[Artigos/L9609/INDEX\|L9609/]] |
| Lei de Direitos Autorais | Lei 9.610/1998 | 115 | [[Artigos/L9610/INDEX\|L9610/]] |

## ⭐ Artigos Críticos — os crimes digitais (atomização via skill)

As leis **modificativas** (L12737 e L14155) têm só 2-4 artigos "invólucro" que
inserem tipos penais no Código Penal — não cabem no pipeline regex. Atomizei
diretamente os tipos penais resultantes, com destaque para uma demonstração rara
de **"lei viva no tempo"** documentada com datas e normas alteradoras:

| Artigo do CP | Tema | Por que é crítico |
|---|---|---|
| [[CP Art. 154-A — Invasão de Dispositivo Informático (evolução 2012-2021)]] | Invasão de dispositivo informático | **Evolução registrada:** pena triplicada entre 2012 (L12737) e 2021 (L14155) |
| [[CP Art. 171 §2º-A — Fraude Eletrônica (Estelionato Digital)]] | Golpes digitais (PIX, phishing, redes sociais) | Tipo penal mais invocado na atual onda de fraudes |

---

## 🕸️ Zendelski Graph — visão consolidada

```
CF/88 Art. 5º (privacidade, liberdade de expressão, intimidade)
        │
        ├──► Marco Civil da Internet (L12965) — "constituição da internet brasileira"
        │            │
        │            └──► Decretos regulamentadores (7.962 — e-commerce; 8.771 — neutralidade)
        │
        ├──► LGPD (L13709) — proteção de dados pessoais
        │            │
        │            └──► dialoga com [[CP Art. 154-A — Invasão de Dispositivo Informático (evolução 2012-2021)|
        │                 invasão de dispositivo]] (vazamento de dados = crime + infração LGPD)
        │
        ├──► Lei do Software (L9609) + Lei de Direitos Autorais (L9610)
        │            └──► propriedade intelectual de bens digitais
        │
        └──► Crimes Digitais no Código Penal (inseridos por leis modificativas)
                     ├─ Art. 154-A — invasão (L12737/2012 → L14155/2021: pena 3x maior)
                     └─ Art. 171, §2º-A — fraude eletrônica/estelionato digital (L14155/2021)
```

> 💡 **Por que o Art. 154-A é a "joia da coroa" deste ramo:** é o primeiro caso, neste
> vault, de uma norma documentada com **linha do tempo explícita de alteração**
> (`vigencia_inicio` + `norma_alteradora` no frontmatter) — exatamente o gap de
> "leis vivas no espaço temporal" identificado na análise inicial do projeto. Use-o
> como modelo ao atomizar qualquer outro dispositivo que tenha sido alterado por
> lei superveniente.

---

## 🔗 Navegação

- **Voltar:** [[../INDEX|Direitos Especializados]]
- **Skill de atomização:** `.claude/skills/atomizar-juridico`
- **Leis "monolíticas" pré-existentes (não-atômicas):**
  [[../../01_LEIS_FUNDAMENTAIS/LEIS_COMPLEMENTARES/LGPD|LGPD — visão geral]] ·
  [[../../01_LEIS_FUNDAMENTAIS/LEIS_ESPECIAIS/Marco-Civil-Internet-INDEX|Marco Civil — visão geral]]
  *(mantidas como resumos de alto nível; os artigos atômicos agora vivem aqui)*

---

**Status:** ✅ 227 artigos via pipeline + 2 artigos críticos (crimes digitais) via skill = 229 notas atômicas
