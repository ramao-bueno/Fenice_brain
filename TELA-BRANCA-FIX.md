# 🔧 FIX: Tela Branca do Obsidian

## O Que Fiz

Limpei completamente a configuração do Obsidian para resetar para padrão:

✅ Deletei `workspace.json` (será recriado automaticamente)
✅ Resetei `app.json` para padrão
✅ Desabilitei todos os plugins problemáticos
✅ Resetei `graph.json` para padrão
✅ Atualizei `core-plugins.json` com apenas plugins essenciais

## Como Resolver a Tela Branca

### Passo 1: Feche o Obsidian COMPLETAMENTE
- Não apenas minimize
- Feche a janela completamente
- Certifique-se que não há processo do Obsidian rodando

### Passo 2: Delete a Pasta de Cache (opcional, mas recomendado)
Abra PowerShell e execute:

```powershell
rm -r "C:\Users\oicon\AppData\Roaming\Obsidian\Local Storage"
rm -r "C:\Users\oicon\AppData\Roaming\Obsidian\Cache"
```

> **Nota**: Isso apaga o cache local, mas não afeta suas notas. O Obsidian recria automaticamente.

### Passo 3: Reabra o Obsidian

Agora o Obsidian vai:
1. Detectar que faltam arquivos de config
2. Reconstruir `workspace.json` automaticamente
3. Começar como um vault novo (limpo)
4. Mostrar o explorador de arquivos normalmente

### Passo 4: Verifique se Está Funcionando

Você deve ver:
- ✅ Explorador de arquivos à esquerda (com suas pastas)
- ✅ Área de edição branca (não branca vazia!)
- ✅ Painel de tags/backlinks à direita

Se ainda vir tela branca:

## Plano B: Reset Nuclear

1. Feche Obsidian completamente
2. Delete a pasta `.obsidian` inteira:
   ```powershell
   rm -r "C:\Stand Alone Legaltech\Fenice brain\.obsidian"
   ```
3. Reabra o Obsidian
4. Ele vai criar `.obsidian` do zero com configurações padrão

> ⚠️ **Aviso**: Isso deleta TODAS as customizações de themes/plugins, mas as notas permanecem intactas.

---

## Problemas Conhecidos (Soluções Rápidas)

| Problema | Solução |
|----------|---------|
| Tela branca ao abrir | Feche/reabra ou delete cache |
| Explorador não aparece | Clique no ícone de pasta à esquerda |
| Notas não aparecem | Use Ctrl+P (switcher) para buscar |
| Plugins causando erro | Todos foram desabilitados — reabra |

---

**Status**: Configuração resetada para padrão
**Próxima etapa**: Reabrir Obsidian
**Esperado**: Vault funciona normalmente
