---
tags: [sistema, dashboard]
created: 2026-06-03
type: recurso
---

# Dashboards — Dataview Queries

Queries dinâmicas para visualizar o estado do vault em tempo real.

## 📋 Tarefas Abertas

```dataview
TASK
WHERE !completed
GROUP BY file.link
SORT due ASC
```

## 🎯 Projetos Ativos

```dataview
LIST file.link
FROM "01 - Projetos"
WHERE type = "projeto" AND (status = "em-progresso" OR status = "planejamento")
SORT file.name ASC
```

## 🧠 Decisões Recentes

```dataview
LIST file.link, created
FROM "01 - Projetos", "02 - Áreas"
WHERE type = "decisão"
SORT created DESC
LIMIT 10
```

## 📝 Notas no Inbox

```dataview
LIST file.link, created
FROM "00 - Inbox"
SORT created DESC
```

## 🏷️ Notas por Tag

```dataview
TABLE tags
FROM ""
WHERE tags
GROUP BY tags
```

## 📊 Estatísticas

```dataview
TABLE file.name as Arquivo, file.size as Tamanho, file.cday as Criado
FROM ""
LIMIT 20
SORT file.cday DESC
```

---

**Dica**: Abra este arquivo no Obsidian pra ver as queries funcionando em tempo real!
