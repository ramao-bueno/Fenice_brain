---
tags:
  - direito-penal
  - dosimetria
  - fase-1
---

# Fase 1 — Pena-base (Art. 59 CP)

> [!quote] Art. 59 CP
> O juiz, atendendo à culpabilidade, aos antecedentes, à conduta social, à personalidade do agente, aos motivos, às circunstâncias e consequências do crime, bem como ao comportamento da vítima, estabelecerá a pena base.

## Como calcular

1. **Identifique os limites** — pena mínima e máxima do tipo penal (ou da qualificadora)
2. **Ponto médio** = (mínimo + máximo) / 2
3. **Quantum por circunstância** = delta / 8 *(onde delta = máximo − mínimo)*
4. **Ajuste** = (nº circunstâncias desfavoráveis − favoráveis) × quantum
5. **Pena-base** = `CLAMP(médio + ajuste, mínimo, máximo)`

> [!tip] Regra prática
> Sem circunstâncias, a pena-base é fixada no mínimo legal (posição majoritária).
> O ponto médio é o ponto de equilíbrio quando há compensação entre favoráveis e desfavoráveis.

## As 8 circunstâncias do Art. 59

| # | Circunstância |
|---|---|
| 1 | Culpabilidade |
| 2 | Antecedentes |
| 3 | Conduta social |
| 4 | Personalidade do agente |
| 5 | Motivos do crime |
| 6 | Circunstâncias do crime |
| 7 | Consequências do crime |
| 8 | Comportamento da vítima |

## Links

- [[Fase 2 — Agravantes e Atenuantes (Arts. 61-66)]]
- [[INDEX — Direito Penal]]
