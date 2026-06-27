---
tags: [karpathy-voice-visual, técnico, jurídico, 2026-06-27]
fonte: 2026-06-20-sistema-academico-fenice-brain-design.md
dominio: técnico
processado: 2026-06-27
---

# Migração Kelseniana — 10 Fases

## Definição
Plano sequencial para reestruturar o vault de estrutura ad-hoc para hierarquia kelseniana, sem quebrar wikilinks existentes (nomes únicos de arquivo sobrevivem à mudança de path).

## Fundamentação
Spec Fenice 2026-06-20 §4 · Obsidian resolve wikilinks por nome de arquivo, não por path — arquivos com nomes únicos (ex: `DEL2848 Art. 121.md`) são seguros durante migração.

## Fases

| Fase | Ação |
|---|---|
| 1 | Criar estrutura de pastas nova (sem mover nada) |
| 2 | Mover `Fenice bRain/` → domínios (fonte canônica) |
| 3 | Mesclar pastas `⚖️` raiz (verificar exclusivos → mover → deletar) |
| 4 | Consolidar `02 - Áreas/` → deletar |
| 5 | Consolidar pastas numeradas (00-Inbox a 06-NotebookLM) → `_SISTEMA/` |
| 6 | Atualizar plugin: array `CODIGOS` em `main.js` (novos paths) |
| 7 | Atualizar scripts: paths de extratores e backup |
| 8 | `git commit` estrutural |
| 9 | Verificar wikilinks (Graph View + broken links) |
| 10 | Testar plugin completo (DomainModal + todos os códigos) |

## Conexões
- [[Sistema Acadêmico Fenice bRain]]
- [[Plugin buscar-artigo]]
- [[Pirâmide Kelseniana — Aplicação ao Vault]]

## Aplicação prática
Executar em ordem: Fases 1–4 → Fase 5 → Fases 6–7 → Fase 8 → Fases 9–10.
**Nunca pular a Fase 9** — Graph View identifica wikilinks quebrados antes de fazer push.

> [!WARNING] Atenção
> Antes da Fase 3: verificar arquivos com nomes genéricos (`INDEX.md`, `README.md`) — esses PODEM ter conflito de wikilink após mover.

> [!NOTE] Origem
> Extraído via Karpathy Voice & Visual do spec 2026-06-20 em 2026-06-27
