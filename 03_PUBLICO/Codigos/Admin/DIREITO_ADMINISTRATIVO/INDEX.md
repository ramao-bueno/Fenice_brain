---
nivel: ramo
tipo: index
ramo: direito-administrativo
tags: [direito-administrativo, index]
created: 2026-06-07
---

# 🏛️ Direito Administrativo — INDEX

**Cobertura:** as 4 leis de maior densidade de litígio/compliance do ramo —
Improbidade, Processo Administrativo Federal, Anticorrupção e Acesso à Informação
— regulamentando o [[Art. 37 — CF|Art. 37 da CF/88]] (princípios da Administração Pública).

> 📌 **Pendência registrada:** Estatuto dos Servidores (L8112, ~250 arts) e Nova
> Lei de Licitações (L14133, 194 arts) já têm HTML salvo aqui, mas ficaram fora
> desta rodada por volume — candidatas naturais a uma próxima leva do pipeline.

---

## 📜 Leis Nacionais (atomizadas — pipeline automático)

Extraídas via `pipeline_direito_administrativo.py` (regex `Art. N`, mesmo padrão
validado em Direito Internacional, Previdenciário e Digital):

| Lei | Norma | Artigos | Pasta |
|---|---|---|---|
| Lei de Improbidade Administrativa | Lei 8.429/1992 | 25 | [[Artigos/L8429/INDEX\|L8429/]] |
| Lei do Processo Administrativo Federal | Lei 9.784/1999 | 70 | [[Artigos/L9784/INDEX\|L9784/]] |
| Lei Anticorrupção (Empresa Limpa) | Lei 12.846/2013 | 31 | [[Artigos/L12846/INDEX\|L12846/]] |
| Lei de Acesso à Informação (LAI) | Lei 12.527/2011 | 47 | [[Artigos/L12527/INDEX\|L12527/]] |

## ⭐ Artigos Críticos (atomização via skill — 2ª demonstração de "lei viva")

Três dispositivos que registram a **reforma mais impactante do Direito
Administrativo recente** (Lei 14.230/2021) — com linha do tempo explícita
(`vigencia_inicio` + `norma_alteradora`), seguindo o modelo inaugurado em
[[../../08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos-Criticos/CP Art. 154-A — Invasão de Dispositivo Informático (evolução 2012-2021)|CP Art. 154-A]]:

| Artigo | Tema | O que a reforma de 2021 mudou |
|---|---|---|
| [[L8429 Art. 9 — Enriquecimento Ilícito (evolução pré e pós-Lei 14.230-2021)]] | Enriquecimento ilícito | Passou a exigir **DOLO** específico — Tema 1.199/STF (retroatividade) |
| [[L8429 Art. 11 — Violação a Princípios (evolução pré e pós-Lei 14.230-2021)]] | Violação a princípios | Exigiu dolo + **revogou inciso I** + suprimiu "lealdade às instituições" |
| [[L12846 Art. 2 — Responsabilidade Objetiva das Pessoas Jurídicas]] | Compliance corporativo | *(contraponto)* regime **objetivo** — sem exigência de dolo, em espelho invertido com a Improbidade reformada |

---

## 🕸️ Zendelski Graph — o "duplo padrão" de imputação (achado central)

```
                    CF/88 Art. 37 (princípios da Administração Pública)
                              │
              ┌───────────────┴────────────────┐
              ▼                                 ▼
    Lei de Improbidade (L8429)          Lei Anticorrupção (L12846)
    [agente PÚBLICO]                    [pessoa jurídica PRIVADA]
              │                                 │
   pós-reforma 2021 (L14230):          desde 2013 (Art. 2):
   regime SUBJETIVO                    regime OBJETIVO
   exige DOLO específico        ◄─────► dispensa dolo/culpa —
   (Tema 1.199 STF)             ESPELHO  basta "interesse ou
                                INVERTIDO benefício"
              │                                 │
              ▼                                 ▼
   Onda de revisão de processos        Mercado de Compliance/
   em curso (extinção por falta         Programas de Integridade
   de prova de dolo)                    (mitigação do risco objetivo)
```

> 💡 **Por que esse "espelho invertido" é o achado mais valioso deste ramo:**
> o legislador escolheu, propositalmente, regimes de imputação OPOSTOS para o
> agente público (cada vez mais protegido — exige dolo) e para a empresa privada
> (cada vez mais exposta — responsabilidade objetiva). Em qualquer escândalo que
> envolva os dois lados simultaneamente, as defesas seguem lógicas jurídicas
> diametralmente diferentes — um "tensionamento estrutural" que só a atomização
> lado a lado revela.

---

## 🔗 Navegação

- **Skill de atomização:** `.claude/skills/atomizar-juridico`
- **Fundamento constitucional:** [[Art. 37 — CF]]
- **Espelho da "lei viva" no Direito Digital:** [[../../08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos-Criticos/CP Art. 154-A — Invasão de Dispositivo Informático (evolução 2012-2021)|CP Art. 154-A]]

---

**Status:** ✅ 173 artigos via pipeline + 3 artigos críticos via skill = 176 notas atômicas
