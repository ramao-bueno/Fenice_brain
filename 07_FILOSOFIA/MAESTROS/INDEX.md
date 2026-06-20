---
nivel: sistema
tipo: maestros
tags: [maestros, sistema, doutrina]
created: 2026-06-02
papel: hub-de-doutrina
---

# 👨‍🏫 MAESTROS — Hub de Doutrina (Centralização de Fontes)

**Objetivo:** Este é o pilar de "Centralização de Fontes" do método PKM de Dr. Mateus Zendelski —
o ponto onde **doutrina** convive com **lei seca** e **jurisprudência** no mesmo ecossistema,
permitindo que uma tese de um jurisconsulto se conecte por `[[link]]` direto ao artigo de lei
ou à súmula que ela comenta/critica/expande.

> Use a skill `atomizar-juridico` para processar um capítulo/trecho de doutrina bruta e gerar
> as notas atômicas + Mapeamento Relacional (Zendelski Graph) prontas para salvar aqui.

---

## 📂 ESTRUTURA (1 pasta por jurisconsulto)

Cada jurista recebe sua própria subpasta. Dentro dela, **notas atômicas** — uma tese/conceito
por nota — nunca um resumo monolítico de capítulo:

```
MAESTROS/
├─ Mateus-Zendelski/      (método PKM + doutrina aplicada)
├─ Miguel-Reale/          (Teoria Tridimensional do Direito)
├─ Pontes-de-Miranda/     (Tratado de Direito Privado)
└─ <Novo-Jurista>/
```

Cada nota de doutrina deve linkar de volta ao dispositivo legal que comenta, por ex.:
`[[Art. 421 — Código Civil]]`, `[[Súmula Vinculante 13]]` — fechando o ciclo bidirecional do
Graph View.

## 🏷️ Frontmatter padrão para notas de doutrina

```yaml
---
jurista: Nome do Jurisconsulto
obra: Nome da obra/capítulo de origem
tese_central: resumo de uma frase
relacionados: ["Art. X — Código Y", "Súmula Z"]
tags: [doutrina, <ramo-do-direito>]
---
```

---

## 🔗 NAVEGAÇÃO

- **Voltar:** [[FENICE bRain/INDEX|FENICE bRain INDEX]]
- **Skill de processamento:** `.claude/skills/atomizar-juridico`
- **Ver também:** [[PIRÂMIDE-DE-KELSEN]] (hierarquia normativa que ancora as tese doutrinárias)

---

**Status:** 🔄 Estrutura pronta — aguardando população de conteúdo doutrinário
