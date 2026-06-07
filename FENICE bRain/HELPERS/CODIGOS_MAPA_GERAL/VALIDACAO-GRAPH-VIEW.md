---
tipo: guia
created: 2026-06-02
---

# ✅ Guia de Validação — Graph View

## Passos para Testar Conectividade

### 1. Abrir Graph View
- **Atalho**: `Ctrl+G`
- Você verá uma visualização de nós (círculos) conectados por linhas (wikilinks)

### 2. Interpretar o Resultado
✅ **Bom**: Maioria dos nós conectados em **um único cluster grande**
❌ **Ruim**: Muitos nós soltos (isolados, sem conexões)

### 3. Navegar pelo Grafo
- **Mover**: Clicar + arrastar
- **Zoom**: Scroll do mouse
- **Focar**: Clicar em um nó para destacar suas conexões
- **Abrir arquivo**: Duplo clique em um nó

### 4. Pontos de Validação
1. Verificar que **todos os 97 INDEX files** estão conectados
2. Confirmar que **Livro I, II, III, IV, V** têm sub-nós visíveis
3. Verificar que **Artigos-Críticos** está conectado ao CC
4. Ver que **Jurisprudência** se conecta aos códigos
5. Confirmar **ausência de nós soltos** flutuando sozinhos

### 5. Testes Específicos
- Clicar em `[[02_DIREITO_CIVIL/INDEX|CC INDEX]]` → deve destacar todos os Livros e Títulos
- Clicar em um Título (ex: "Da Posse") → deve conectar a seu Livro pai
- Clicar em `[[02_DIREITO_CIVIL/INDEX-MASTER-DIREITO-CIVIL]]` → deve mostrar toda estrutura CC

---

## Conclusão
Se os 97 INDEX files criados estão formando um **grafo coeso** (nó único, gigante, interconectado), a estrutura está **✅ OPERACIONAL**.

Se ainda há muitos nós soltos, precisamos criar mais INDEX files para as pastas órfãs restantes.
