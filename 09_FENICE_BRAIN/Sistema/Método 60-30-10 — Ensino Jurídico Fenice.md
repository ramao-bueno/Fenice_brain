---
tags: [karpathy-voice-visual, acadêmico, 2026-06-27]
fonte: 2026-06-20-sistema-academico-fenice-brain-design.md
dominio: acadêmico
processado: 2026-06-27
---

# Método 60/30/10 — Ensino Jurídico Fenice

## Definição
Cada matéria no módulo `08_ENSINO` divide o esforço em: 60% questões de banca (prática), 30% teoria/doutrina, 10% revisão/flashcards.

## Fundamentação
Spec Fenice 2026-06-20 §5 · Applied Learning Theory (Bloom's Taxonomy)
Implementado em: `08_ENSINO/Univille/Semestre-N/[materia]/`

| Pasta | % | Conteúdo |
|---|---|---|
| `_60-Questoes/` | 60% | Questões da banca, lei seca, jurisprudência aplicada |
| `_30-Teoria/` | 30% | Doutrina, videoaulas resumidas, PDFs processados |
| `_10-Revisao/` | 10% | Flashcards, mapas mentais, resumos próprios |

## Conexões
- [[Sistema Acadêmico Fenice bRain]]
- [[Univille]]
- [[Fenice Estudos]]

## Aplicação prática
Ao criar pasta de nova matéria: sempre criar as 3 subpastas `_60-Questoes` / `_30-Teoria` / `_10-Revisao` antes de qualquer nota de conteúdo.

> [!NOTE] Origem
> Extraído via Karpathy Voice & Visual do spec 2026-06-20 em 2026-06-27
