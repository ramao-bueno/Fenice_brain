---
tags: [stj, sumula, jurisprudencia, index, pendente]
type: index
status: pendente
created: 2026-06-04
---

# INDEX — Súmulas do STJ (Pendente)

**Status:** ⏳ A implementar manualmente
**Total estimado:** ~670 súmulas (STJ 1–670)
**Fonte oficial:** [scon.stj.jus.br](https://scon.stj.jus.br/SCON/sumulas/toc.jsp?b=SUMU)

---

## Como adicionar as Súmulas STJ

### Opção 1 — Via script (recomendada)

1. Abra no seu navegador:
   ```
   https://scon.stj.jus.br/SCON/sumulas/toc.jsp?b=SUMU&livre=%40docn&p=true&t=&l=700&i=1
   ```
2. Salve a página: `Ctrl+S` → salve como `_stj_sumulas_page.html`
3. Coloque o arquivo em `scripts/`
4. Rode:
   ```bash
   python scripts/generate_stj_sumulas.py --from-html scripts/_stj_sumulas_page.html
   ```

### Opção 2 — Manual (súmula por súmula)

Crie arquivos no formato:
```
FENICE bRain/03_PROCESSO_CIVIL/STF_SUMULAS/STJ/Sumula-STJ-{NNNN}.md
```

Com frontmatter:
```yaml
---
sumula: "1"
lei: STJ — Superior Tribunal de Justiça
tipo: sumula-stj
tribunal: STJ
status: vigente
tags: [stj, sumula-stj, sumula-1, jurisprudencia, vigente]
created: YYYY-MM-DD
---
```

---

## Links

- [[INDEX-SV-STF]] — Súmulas Vinculantes STF (63)
- [[INDEX-Sumulas-STF]] — Súmulas Comuns STF (736)
- [[INDEX-ENUNCIADOS]] — Enunciados CJF (262)
- [[00_NAVIGATOR]] — Busca por código
