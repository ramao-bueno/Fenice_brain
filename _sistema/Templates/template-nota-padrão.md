---
tags: [template]
created: <% tp.date.now("YYYY-MM-DD") %>
type: <% await tp.system.prompt("Tipo de nota", "nota|projeto|recurso|ideia|decisão") %>
status: rascunho
related: 
---

# <% await tp.system.prompt("Título da nota") %>

## Contexto
O que motivou esta nota, por que existe.

## Conteúdo
Conteúdo principal.

## Próximos Passos
O que fazer com essa informação (se aplicável).

## Links
- [[Notas relacionadas]]
