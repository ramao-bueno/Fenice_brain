---
tags: [sistema, configuracao, graph-view]
created: 2026-06-03
type: recurso
status: pronto
---

# Correção: Graph View (Visualização em Gráfico)

## Problema Identificado

A visualização em gráfico não estava funcionando porque:

1. **`"close": true`** — O gráfico estava fechado por padrão
2. **`"textFadeMultiplier": 0`** — O texto dos nós era invisível
3. **Filtros desabilitados** — Controles estavam ocultos

## Solução Aplicada

Atualizei `graph.json` com as seguintes correções:

| Configuração | Antes | Depois | Impacto |
|---|---|---|---|
| `close` | `true` | `false` | Gráfico agora fica visível |
| `textFadeMultiplier` | 0 | 1 | Texto dos nós fica legível |
| `collapse-display` | `true` | `false` | Controles de visualização visíveis |
| `collapse-filter` | `true` | `false` | Filtros acessíveis |
| `showTags` | `false` | `true` | Tags aparecem no gráfico |
| `showArrow` | `false` | `true` | Setas de direção visíveis |

## Como Usar o Graph View

### Acessar
1. Abra o Obsidian
2. Clique no ícone **Graph** na ribbon esquerda
3. Ou use o comando: `Ctrl+Shift+G` (ou `Cmd+Shift+G` no Mac)

### Filtrar e Navegar
- **Buscar**: Use o campo de pesquisa para encontrar notas
- **Filtros**: Configure quais tipos de nós aparecem (notas, tags, anexos)
- **Zoom**: Scroll do mouse ou gesto de zoom
- **Mover**: Arraste o gráfico para navegar
- **Clicar em nó**: Abre a nota correspondente

### Interpretar Cores e Formas
- **Círculos grandes** = Notas com muitos links
- **Círculos pequenos** = Notas isoladas
- **Linhas** = Conexões/links entre notas
- **Cores diferentes** = Tags diferentes (se habilitado)

## Plugins Relacionados

Você tem instalados:
- `backlink-cache` — Melhora o desempenho de backlinks
- `dataview` — Cria visualizações de dados
- `metadata-extractor` — Processa metadados

Estes podem impactar a visualização do gráfico. Se ainda houver lentidão, desabilite-os temporariamente em **Settings → Community plugins**.

## Próximos Passos

1. **Feche e reabra o Obsidian** para aplicar as mudanças
2. **Teste o Graph View** — deve aparecer normalmente agora
3. **Configure conforme necessário** — ajuste cores, filtros e zoom
4. **Crie links** entre suas notas para ver o gráfico crescer

---

**Status**: ✅ Corrigido
**Data**: 2026-06-03
**Teste**: Abra o Obsidian e acesse o Graph View (ícone de gráfico na esquerda)
