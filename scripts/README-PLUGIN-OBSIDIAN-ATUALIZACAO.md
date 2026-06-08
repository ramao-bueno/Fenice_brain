# Atualização do Plugin Obsidian — Fenice Buscar Artigo v6

## 📋 O que foi Adicionado

✅ **23 Áreas do Direito** (antes eram 9):
- CF/88 — Constituição Federal
- Código Civil (CC) + LINDB + D9830
- Código Penal (CP)
- Código Processo Civil (CPC)
- Código Processo Penal (CPP) ✨ NOVO
- Código Consumidor (CDC)
- Lei Improbidade (L8429) ✨ NOVO
- Lei Anticorrupção (L12846) ✨ NOVO
- Lei Acesso Info (L12527) ✨ NOVO
- Lei Custeio (L8212) — Previdenciário ✨ NOVO
- Lei Benefício (L8213) — Previdenciário ✨ NOVO
- Marco Civil da Internet ✨ NOVO
- LGPD — Lei Proteção Dados ✨ NOVO
- CADH — Convenção Americana Direitos Humanos ✨ NOVO
- CVDT — Convenção Viena Tratados ✨ NOVO
- SV — Súmulas Vinculantes STF
- S-STF — Súmulas Comuns STF
- 📋 Enunciados CJF

✅ **Opção ATOMIZAR** (novo):
- Painel de seleção com 10 áreas para atomizar
- Atalho direto para skill de inteligência artificial
- Emojis para identificar áreas rapidamente

---

## 🔧 Como Atualizar

### Opção 1: Copiar Arquivo Manualmente (Recomendado)

1. **Localizar arquivo atualizado:**
   ```
   scripts/obsidian-plugin-fenice-buscar-artigo-updated.js
   ```

2. **Copiar para Obsidian:**
   ```
   .obsidian/plugins/fenice-buscar-artigo/main.js
   ```

3. **Recarregar Plugin:**
   - Abrir Obsidian
   - Settings → Community plugins → fenice-buscar-artigo → Desabilitar
   - Fechar e reabrir Obsidian
   - Settings → Community plugins → fenice-buscar-artigo → Habilitar

### Opção 2: Substituir via Terminal

```bash
cp scripts/obsidian-plugin-fenice-buscar-artigo-updated.js \
   ".obsidian/plugins/fenice-buscar-artigo/main.js"
```

Depois recarregar Obsidian.

---

## 🎮 Como Usar

### Buscar Artigo (existente)

**Atalho:** `Ctrl+Shift+B` (ou `Cmd+Shift+B` no Mac)

1. Painel abre com 23 áreas jurídicas
2. Escolha a área (ex: "Código Penal")
3. Digite número do artigo (ex: 121)
4. Pronto! Nota abre com estrutura (§ incisos, correlatos, etc)

**Exemplo:**
```
Ctrl+Shift+B
  → Procure: "Penal"
  → Selecione: "Código Penal (CP)"
  → Digite: 121
  → Abre: Art. 121 com estrutura completa
```

### Novo: ATOMIZAR (IA)

**Atalho:** `Ctrl+Shift+B` → escolha "⚡ ATOMIZAR"

1. Painel abre com 10 áreas para atomizar
2. Escolha a área que quer atomizar (ex: "Direito Previdenciário")
3. Clique → vai para INDEX da área
4. Use skill de IA para processar notas

**Exemplo:**
```
Ctrl+Shift+B
  → Procure: "Atomi"
  → Selecione: "⚡ ATOMIZAR — Skill de IA"
  → Painel com áreas aparece
  → Escolha: "💼 Direito Previdenciário"
  → Abre INDEX da área para iniciar atomização
```

### Info do Artigo Atual (existente)

**Atalho:** `Ctrl+Shift+I`

Mostra painel com § incisos, alíneas, correlatos da nota atual.

---

## 📊 Comparativo

| Feature | v5 (Antiga) | v6 (Nova) |
|---------|------------|----------|
| Áreas de Direito | 9 | 23 |
| Opção Atomizar | ❌ | ✅ |
| Código Processo Penal | ❌ | ✅ |
| Direito Administrativo | ❌ (parcial) | ✅ (completo) |
| Direito Previdenciário | ❌ | ✅ |
| Direito Digital | ❌ | ✅ |
| Direito Internacional | ❌ | ✅ |
| Painel Seleção Atomizar | ❌ | ✅ |

---

## 🔑 Código-chave Adicionado

### 1. Novas Áreas no CODIGOS Array

```javascript
// ━━━ DIREITO ADMINISTRATIVO ━━━
{ label: 'Lei Improbidade (L8429)',        tag: 'improbidade',   pasta: '07_DIREITO_ADMINISTRATIVO' },
{ label: 'Lei Anticorrupção (L12846)',     tag: 'anticorrupção', pasta: '07_DIREITO_ADMINISTRATIVO' },
...

// ━━━ DIREITO PREVIDENCIÁRIO ━━━
{ label: 'Lei Custeio (L8212)',            tag: 'previdenciario', pasta: '06_DIREITO_PREVIDENCIÁRIO' },
...

// ━━━ ESPECIAL: ENUNCIADOS ━━━
{ label: '⚡ ATOMIZAR — Skill de IA',     tag: 'atomizar',       pasta: '', codigo: 'ATOM', isAtomizar: true },
```

### 2. Função abrirAtomizar()

```javascript
abrirAtomizar() {
  const areas = [
    { label: '📚 Direito Constitucional', ... },
    { label: '💼 Direito Previdenciário', ... },
    ...
  ];
  // Abre painel de seleção
}
```

### 3. Lógica no iniciarBusca()

```javascript
if (config.isAtomizar) {
  this.abrirAtomizar();
  return;
}
```

---

## ✅ Checklist de Verificação

Após atualizar, verifique:

- [ ] Plugin carregou sem erros (console F12)
- [ ] Ctrl+Shift+B abre painel com 23 áreas ✅
- [ ] Opção "⚡ ATOMIZAR" aparece no final
- [ ] Busca funciona em novas áreas (ex: CPP, L8212)
- [ ] Clicando em ATOMIZAR abre painel com 10 áreas
- [ ] Ctrl+Shift+I ainda funciona normalmente
- [ ] Correlatos ainda aparecem nos painéis

---

## 🐛 Troubleshooting

### Plugin não carrega

```bash
# Abrir console Obsidian (F12)
# Procure por erros como:
# "Fenice Buscar Artigo v6 (EXPANDIDO) — Ctrl+Shift+B | Ctrl+Shift+I"
```

Se não aparecer:
1. Delete `.obsidian/plugins/fenice-buscar-artigo/main.js`
2. Copie arquivo atualizado novamente
3. Recarregue Obsidian completamente (feche e abra)

### Áreas novas não aparecem no painel

1. Verifique que as pastas existem:
   - `07_DIREITO_ADMINISTRATIVO/`
   - `06_DIREITO_PREVIDENCIÁRIO/`
   - `10_DIREITO_DIGITAL/`
   - `11_DIREITO_INTERNACIONAL/`
   - `04_CÓDIGO_PROCESSO_PENAL/`

2. Se não existem, crie os diretórios

### ATOMIZAR não funciona

1. Verifique que você tem skill instalada
2. Verifique pastinhas INDEX existem:
   - `00_CONSTITUIÇÃO_FEDERAL/INDEX`
   - `06_DIREITO_PREVIDENCIÁRIO/INDEX`
   - etc

---

## 📝 Notas Técnicas

- **Versão:** v6 (EXPANDIDO)
- **Tamanho:** ~18 KB (vs ~17 KB antes)
- **Compatibilidade:** Obsidian 1.0+
- **Node:** v14+

---

## 🔄 Próximas Melhorias Planejadas

1. ✅ Adicionar mais áreas de direito
2. ✅ Integrar opção ATOMIZAR
3. ⏳ Integrar com AI para análise automática
4. ⏳ Sugerir artigos correlatos via IA
5. ⏳ Busca semântica (embeddings)

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique console (F12) em Obsidian
2. Confirme arquivo copiado corretamente
3. Recarregue Obsidian completamente
4. Se erro persiste, delete plugin e reinstale

