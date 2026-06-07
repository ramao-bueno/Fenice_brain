---
nivel: ramo
tipo: index
ramo: direito-previdenciario
tags: [direito-previdenciario, index]
created: 2026-06-07
---

# 🛡️ Direito Previdenciário — INDEX

**Cobertura:** as "leis gêmeas" de 1991 — custeio (8.212) e benefícios (8.213) — que
formam o núcleo do Regime Geral de Previdência Social (RGPS), regulamentando o
[[Art. 201 — CF|Art. 201]] e o [[Art. 195 — CF|Art. 195]] da CF/88.

---

## 📜 Leis Nacionais (atomizadas — pipeline automático)

Extraídas via `pipeline_direito_previdenciario.py` (regex `Art. N`, padrão validado
em Direito Internacional e nos demais códigos):

| Lei | Norma | Artigos | Pasta |
|---|---|---|---|
| Lei Orgânica da Seguridade Social (Custeio) | Lei 8.212/1991 | 105 | [[Artigos/L8212/INDEX\|L8212/]] |
| Lei dos Planos de Benefícios da Previdência Social | Lei 8.213/1991 | 156 | [[Artigos/L8213/INDEX\|L8213/]] |

## ⭐ Artigos Críticos (atomização via skill)

Quatro dispositivos que formam o **"ciclo completo"** do sistema previdenciário —
do financiamento ao acesso ao benefício e sua proteção no tempo — atomizados com
Notas Atômicas + Zendelski Graph + Vetor de Negócio:

| Artigo | Tema | Por que é crítico |
|---|---|---|
| [[L8212 Art. 22 — Contribuições da Empresa sobre Folha de Pagamento]] | Como o sistema é financiado | Núcleo do contencioso tributário-previdenciário corporativo |
| [[L8213 Art. 18 — Rol de Prestações do RGPS]] | O que o sistema oferece | "Índice geral" — ponto de partida de qualquer triagem |
| [[L8213 Art. 25 — Período de Carência]] | Requisito de acesso | Conceito mais litigado — maior volume de demandas |
| [[L8213 Art. 102 — Perda da Qualidade de Segurado]] | Proteção do direito no tempo | Base das teses de revisão de benefício mais vantajoso |

---

## 🕸️ Zendelski Graph — o "ciclo fechado" do sistema previdenciário

```
CF/88 Art. 195 (financiamento)         CF/88 Art. 201 (cobertura)
        │                                       │
        ▼                                       ▼
L8212 Art. 22 ────────────────────────► L8213 Art. 18
(contribuição patronal                  (rol de prestações —
 sobre folha = 20%)                      o "índice" do sistema)
        │                                       │
        │         "sinalagma" (Art. 195,§5º    │
        │          CF — sem custeio, sem        │
        └────────► benefício") ◄────────────────┤
                                                 ▼
                                        L8213 Art. 25
                                        (carência — conta as
                                         contribuições do Art. 22)
                                                 │
                                                 ▼
                                        L8213 Art. 102
                                        (uma vez cumprido tudo,
                                         o direito não se perde —
                                         Direito Adquirido, CF Art. 5º, XXXVI)
```

> 💡 **O fio que conecta tudo:** o Art. 195, §5º, da CF ("nenhum benefício será criado,
> majorado ou estendido sem a correspondente fonte de custeio") é o elo lógico entre
> os dois lados do sistema — toda prestação do Art. 18 só existe porque o Art. 22
> a financia, e toda contagem de carência do Art. 25 mede exatamente as contribuições
> que o Art. 22 instituiu.

---

## 🔗 Navegação

- **Voltar:** [[../INDEX|Direitos Especializados]]
- **Skill de atomização:** `.claude/skills/atomizar-juridico`
- **Fundamento constitucional:** [[Art. 201 — CF]] · [[Art. 195 — CF]]

---

**Status:** ✅ 261 artigos via pipeline + 4 artigos críticos via skill = 265 notas atômicas
