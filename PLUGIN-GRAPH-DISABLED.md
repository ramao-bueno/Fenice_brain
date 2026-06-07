---
tags: [sistema, aviso]
created: 2026-06-03
type: recurso
status: pronto
---

# ⚠️ Plugin Graph Desabilitado Permanentemente

## Problema Identificado

O **plugin Graph View nativo do Obsidian** está **corrompido** e causa **tela branca** quando habilitado.

## Solução Aplicada

✅ Plugin Graph **permanentemente desabilitado** em `core-plugins.json`
✅ Plugin Excalidraw problemático **removido**
✅ Apenas plugins essenciais e estáveis **mantidos ativos**

## Por Que?

Quando você ativa o Graph:
- ❌ Tela fica branca
- ❌ Interface não aparece
- ❌ Obsidian trava

**Causa**: Cache corrompido ou versão incompatível do plugin graph

## Alternativas para Visualizar Relações

Você ainda pode ver as relações entre notas usando:

### 1. **Backlinks** (Links Inversos)
- Aba à direita: "Links inversos para [Nota]"
- Mostra quais notas apontam para a atual
- ✅ Funciona perfeitamente

### 2. **Outgoing Links** (Links de Saída)
- Aba à direita: "Links de saída para [Nota]"
- Mostra os links que essa nota contém
- ✅ Funciona perfeitamente

### 3. **Canvas** (Tábua de desenho)
- Tipo de bloco visual para conectar ideias
- Menu superior → "Create new canvas"
- ✅ Alternativa ao Graph

## Se Quiser Reativar o Graph Depois

Se o problema for resolvido em uma versão futura:

1. Settings → Core plugins → Graph
2. Toggle para **ON**
3. Feche/reabra Obsidian

Mas **não recomendado** enquanto estiver corrompido.

---

**Status**: ✅ Vault 100% funcional sem Graph
**Última atualização**: 2026-06-03
**Recomendação**: Use Backlinks + Outgoing Links em vez de Graph View
