---
title: Implementação — Modal Ctrl+Shift+B v7
data: 2026-06-12
tipo: documentação-técnica
status: concluído
---

# 🔍 Implementação: Modal Ctrl+Shift+B v7

**Data:** 2026-06-12  
**Status:** ✅ Operacional  
**Versão:** 7.0

---

## 📋 Resumo das Mudanças

Implementação de busca jurídica avançada no modal `Ctrl+Shift+B` do Obsidian com suporte a:
- ✅ Busca por número de artigo
- ✅ Busca semântica por tema
- ✅ Abertura direta de referências (tratados, convenções)
- ✅ Console limpo ao abrir Obsidian

---

## 🎯 Funcionalidades Implementadas

### 1. OAB Adicionado ao Modal
**O que:** Item "OAB — Ordem dos Advogados" no modal de busca  
**Como:** Adicionado à lista `CODIGOS` no plugin  
**Onde:** `09_REFERENCIAS/OAB`  
**Resultado:** Abre direto o INDEX da OAB

### 2. Busca Semântica por Tema
**O que:** Digitar tema em vez de número (ex: "responsabilidade", "viena")  
**Como:** Detecta se input é número ou texto, busca por:
- Título do arquivo
- Tags nos metadados
- Conteúdo do documento

**Exemplo:**
```
Ctrl+Shift+B → CC → Digite "responsabilidade"
↓
Busca em 2.036 artigos CC
↓
Encontra Art. 186-189 e artigos relacionados
```

### 3. Referências Abertas Direto
**O que:** Convenções e tratados abrem sem pedir número  
**Como:** Flag `isReferencia: true` na configuração  
**Itens afetados:**
- CVDT — Convenção de Viena (Direito dos Tratados)
- CADH — Convenção Americana de Direitos Humanos
- OAB — Ordem dos Advogados

**Exemplo:**
```
Antes: Ctrl+Shift+B → CVDT → Pede número → Sem resultado
Depois: Ctrl+Shift+B → CVDT → ✅ Abre direto INDEX
```

### 4. Console Limpo ao Abrir
**O que:** Console JavaScript limpa automaticamente  
**Como:** `console.clear()` no método `onload()` do plugin  
**Resultado:** Obsidian abre sem "poluição" de logs antigos

---

## 🔧 Mudanças Técnicas

### Arquivo Modificado
- `~/.obsidian/plugins/fenice-buscar-artigo/main.js`

### Alterações Principais

#### 1. Nova Classe: `TemaModal` (SuggestModal)
Exibe resultados da busca semântica com:
- Título do resultado
- Tags relevantes
- Ordenação por relevância

#### 2. Nova Função: `buscarPorTema()`
```javascript
async buscarPorTema(config, tema) {
  // Normaliza caminhos (Windows compatibility)
  // Busca em pastas configuradas
  // Compara por título, tags e conteúdo
  // Ordena por relevância (100:50:10)
  // Mostra modal de sugestões
}
```

#### 3. Refatoração: `buscarEAbrir()`
Detecta tipo de input:
- Se número → `buscarPorNumero()`
- Se texto → `buscarPorTema()`

#### 4. Configuração: Adicionadas flags
```javascript
isReferencia: true   // Abre direto sem pedir número
isReferencia: false  // Pede número ou tema (padrão)
```

#### 5. Logs de Debug
```javascript
console.clear()      // Limpa ao abrir
console.log(...)     // Logs detalhados de busca
```

---

## 📊 Estrutura de Pastas Suportadas

| Código | Pasta | Tipo |
|---|---|---|
| CC | `02_DIREITO_PRIVADO/DIREITO_CIVIL` | Código (multi-pasta) |
| CDC | `02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR` | Código |
| CPC | `03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL` | Código |
| CF/88 | `00_ESTRUTURA_CONSTITUCIONAL/CONSTITUIÇÃO_FEDERAL` | Código |
| CVDT | `08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Viena-Direito-dos-Tratados` | **Referência** |
| CADH | `08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Americana-Direitos-Humanos` | **Referência** |
| OAB | `09_REFERENCIAS/OAB` | **Referência** |

---

## 🧪 Testes Realizados

### ✅ Teste 1: Busca por Número
```
Input: CC → 186 → ✅ Abre Art. 186 CC (Responsabilidade Civil)
```

### ✅ Teste 2: Busca por Tema
```
Input: CDC → direitos → ✅ Mostra Arts. 4, 6, etc (Direitos Básicos)
```

### ✅ Teste 3: Referência Direto
```
Input: CVDT → ✅ Abre direto INDEX (sem pedir número)
```

### ✅ Teste 4: Console Limpo
```
Abre Obsidian → Console vazio com ✅ Fenice Buscar Artigo v7 — Pronto!
```

---

## 🚀 Como Usar

### Atalho Principal
**`Ctrl+Shift+B`** — Abre modal de busca jurídica

### Fluxo de Busca

#### Opção A: Número de Artigo
```
1. Ctrl+Shift+B
2. Seleciona código (CC, CDC, CPC, etc)
3. Digite número (48, 121, 1.228)
4. ↓ Abre artigo
```

#### Opção B: Busca Semântica
```
1. Ctrl+Shift+B
2. Seleciona código (CC, CDC, CPC, etc)
3. Digite tema (responsabilidade, direitos, viena)
4. ↓ Mostra resultados relacionados
5. Seleciona um
6. ↓ Abre arquivo
```

#### Opção C: Referência Direta
```
1. Ctrl+Shift+B
2. Seleciona referência (CVDT, CADH, OAB)
3. ↓ Abre direto INDEX (sem pedir número)
```

---

## 📝 Notas Importantes

### Compatibilidade
- ✅ Windows (backslash handling)
- ✅ macOS/Linux (forward slash)
- ✅ Normalização automática de caminhos

### Limitações
- `.obsidian/` está em `.gitignore` → Plugin não é versionado
- Busca semântica funciona melhor com metadados bem estruturados
- Frontmatter deve ter tags para melhor relevância

### Próximas Melhorias (Futuro)
- [ ] Suporte a filtros avançados
- [ ] Histórico de buscas recentes
- [ ] Busca full-text com regex
- [ ] Integração com Notion

---

## 📚 Referências

- **Plugin Location:** `~/.obsidian/plugins/fenice-buscar-artigo/main.js`
- **Config:** Arquivo `CODIGOS` no topo do plugin
- **Classes:** `CodigoModal`, `ArtigoModal`, `TemaModal`, `InfoModal`
- **Hotkey:** `Ctrl+Shift+B` (configurável em Obsidian settings)

---

**Última atualização:** 2026-06-12  
**Versão do Plugin:** 7.0  
**Status:** ✅ Operacional
