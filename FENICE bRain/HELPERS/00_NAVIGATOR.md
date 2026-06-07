---
tags: [fenice-brain, navigator, index, cf88, cc, cpc, direito-penal]
type: navigator
created: 2026-06-04
---

# FENICE BRAIN — NAVIGATOR JURIDICO

> **Como usar:** `Ctrl+P` → digitar **"Buscar Artigo"** → selecionar o código → digitar o número do artigo → abre automaticamente.
> Ou navegue pela base abaixo filtrando diretamente nas colunas.

---

## NAVEGACAO POR BASE

![[00_NAVIGATOR.base]]

---

## HIERARQUIA KELSENIANA

```
CF/88 → [[INDEX — CF/88 Completo]]
    |
    +-- CC (Codigo Civil)      → [[INDEX Codigo Civil]]
    +-- CP (Codigo Penal)      → [[INDEX — Direito Penal]]
    +-- CPC (Processo Civil)   → [[INDEX CPC]]
    +-- CPP (Processo Penal)   → (a adicionar)
    +-- CLT                    → (a adicionar)
```

---

## ACESSO RAPIDO POR CODIGO

| Codigo | Arts. | Indice | Planalto |
|--------|-------|--------|---------|
| CF/88 | 1–250 | [[INDEX — CF/88 Completo]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm) |
| Codigo Civil | 1–2046 | [[INDEX Codigo Civil]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) |
| Codigo Penal | 121+ | [[INDEX — Direito Penal]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm) |
| CPC | 1–1072 | [[INDEX CPC]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm) |

---

## ULTIMOS ACESSADOS

```dataview
TABLE lei AS "Lei", artigo AS "Art.", file.mtime AS "Ultimo acesso"
FROM "FENICE bRain"
WHERE artigo != null AND artigo != ""
SORT file.mtime DESC
LIMIT 10
```

---

## TOTAIS POR CODIGO

```dataview
TABLE length(rows) AS "Total de Artigos"
FROM "FENICE bRain"
WHERE artigo != null AND artigo != ""
GROUP BY lei
SORT length(rows) DESC
```

---

**Atualizado:** 2026-06-04
**Dica:** Use [[PIRÂMIDE-DE-KELSEN]] para visualizar a hierarquia normativa completa.
