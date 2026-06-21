---
nivel: sistema
tipo: llm-wiki-index
modulo: 06_JURISCONSULTOS
tags: [index, llm-wiki, jurisconsultos]
created: 2026-06-21
---

# Index — 06_JURISCONSULTOS

> Índice navegável do LLM Wiki. O agente lê este arquivo primeiro, depois aprofunda nas páginas relevantes.
> Target: 2–4k tokens por página de entidade. Limite do módulo: 60k tokens (≈20 jurisconsultos).

---

## Jurisconsultos Indexados

### Constitucional
- [[Alexandre de Moraes]] — Direito Constitucional, ministro STF
- [[Gilmar Mendes]] — Controle de Constitucionalidade, ministro STF
- [[José Afonso da Silva]] — Curso de Direito Constitucional Positivo
- [[Luís Roberto Barroso]] — Neoconstitucionalismo, presidente STF

### Teoria Geral / Filosofia do Direito
- (pendente — ingestão via check_source.py)

### Civil / Privado
- (pendente)

### Penal
- (pendente)

### Processual
- (pendente)

---

## Estrutura de Cada Página

Cada `NomeJurisconsulto.md` deve conter:

```markdown
---
tipo: jurisconsulto
area: [constitucional | civil | penal | ...]
obras_canonicas: [lista de obras primárias ingeridas]
cobertura: parcial | canonica
ultima_atualizacao: AAAA-MM-DD
---

# Nome do Jurisconsulto

## Tese Central
## Obras Principais
## Conceitos Fundamentais
## Posição na Dogmática Brasileira
## Conexões [[wikilink]]
## Fontes Ingeridas
```

---

## Log de Ingestão

→ Ver [[log]] (log.md neste diretório)

---

## Gatekeeping GIGO

Antes de atualizar qualquer página, rodar:

```bash
python scripts/llm-wiki/check_source.py \
  --autor "Nome Completo" \
  --tipo primaria \
  --titulo "Nome da Obra" \
  --modulo jurisconsultos \
  --cobertura parcial \
  --commit
```

Status `rejeitado` → não ingerir.
