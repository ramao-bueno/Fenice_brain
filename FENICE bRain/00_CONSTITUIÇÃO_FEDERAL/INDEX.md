---
titulo: INDEX — CF/88 Completo
lei: Constituição Federal de 1988
type: index
status: vigente
version: '3.0'
cf88: true
tags:
- cf88
- constituicao
- index
- fenice-brain
created: '2026-06-04'
---

# CF/88 — INDICE COMPLETO

**Status:** VIGENTE  |  **Artigos gerados:** 250/250  |  **Atualizado:** 2026-06-04
**Planalto:** [Texto oficial](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)

---

## Metricas

| Metrica | Valor |
|---------|-------|
| **Total de artigos** | 250 |
| **Titulos** | 9 (I–IX) |
| **Emendas** | 127 (EC 1–127) |
| **Hierarquia Kelsen** | Nivel 1 — Norma Fundamental |

---

## Navegacao por Titulo

- [[INDEX-TITULO-I|TITULO-I — Dos Princípios Fundamentais]] (Arts. 1–4, 4 artigos)
- [[INDEX-TITULO-II|TITULO-II — Dos Direitos e Garantias Fundamentais]] (Arts. 5–17, 13 artigos)
- [[INDEX-TITULO-III|TITULO-III — Da Organização do Estado]] (Arts. 18–43, 26 artigos)
- [[INDEX-TITULO-IV|TITULO-IV — Da Organização dos Poderes]] (Arts. 44–135, 92 artigos)
- [[INDEX-TITULO-V|TITULO-V — Da Defesa do Estado e das Instituições Democráticas]] (Arts. 136–144, 9 artigos)
- [[INDEX-TITULO-VI|TITULO-VI — Da Tributação e do Orçamento]] (Arts. 145–169, 25 artigos)
- [[INDEX-TITULO-VII|TITULO-VII — Da Ordem Econômica e Financeira]] (Arts. 170–192, 23 artigos)
- [[INDEX-TITULO-VIII|TITULO-VIII — Da Ordem Social]] (Arts. 193–232, 40 artigos)
- [[INDEX-TITULO-IX|TITULO-IX — Das Disposições Constitucionais Gerais]] (Arts. 233–250, 18 artigos)

---

## Piramide de Kelsen

```
         [ CF/88 ] <- voce esta aqui
              |
   [Leis Complementares] [Emendas Constitucionais]
              |
  [CC]  [CP]  [CPC]  [CPP]  [CLT]  [CTN]  [CTB]
              |
        [Decretos / Portarias]
              |
          [Jurisprudencia STF/STJ]
```

- [[PIRAMIDE-DE-KELSEN]] — Canvas visual interativo
- [[00_NAVIGATOR]] — Busca por codigo (CF + CC + CP + CPC)
- [[Preambulo]] — Valores supremos

---

## Correlacoes Principais (Dataview)

```dataview
TABLE lei, artigo
FROM "FENICE bRain"
WHERE contains(base_constitucional, "CF Art.")
SORT lei ASC
LIMIT 20
```

---

**Fonte oficial:** [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)
