# 🧪 Teste Rápido — STF Súmula Analyzer

**5 minutos para validar o sistema completamente**

---

## ✅ Pré-requisitos

```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Não precisa instalar nada! Só stdlib
```

---

## 🚀 Executar Teste

### 1. Verificar arquivo de entrada

```bash
cd "Fenice bRain\scripts"
ls -la sumulas_input.txt  # Deve existir (9 súmulas de exemplo)
```

### 2. Rodar processador

```bash
python stf_sumula_processor.py
```

### 3. Verificar output

```bash
# Markdown das Súmulas Vinculantes
ls -la ../05_STJ_SUMULAS/STF-SUMULAS-VINCULANTES/
# Output esperado: STF_SV_57.md, STF_SV_33.md, STF_SV_26.md, STF_SV_18.md, STF_SV_37.md

# Markdown das Teses RG
ls -la ../05_STJ_SUMULAS/STF-REPERCUSSAO-GERAL/
# Output esperado: STF_TEMA_69.md, STF_TEMA_220.md, STF_TEMA_834.md, STF_TEMA_457.md, STF_TEMA_762.md

# JSON estruturado
cat exports/stf_sumulas_export.json | python -m json.tool | head -50
```

---

## 📋 Casos de Teste

### Teste 1: SV com análise básica
✅ **Arquivo:** STF_SV_57.md  
✅ **Esperado:**
- Tipo: SUMULA_VINCULANTE
- Número: SV 57
- Processo: RE 574.706
- Setor: ADMINISTRATIVO
- Modulação: NÃO

```bash
cat ../05_STJ_SUMULAS/STF-SUMULAS-VINCULANTES/STF_SV_57.md | grep -A 5 "NÚCLEO"
```

---

### Teste 2: Tema RG com modulação detectada
✅ **Arquivo:** STF_TEMA_69.md  
✅ **Esperado:**
- Tipo: REPERCUSSAO_GERAL
- Número: Tema 69
- Setor: TRIBUTÁRIO
- Modulação: **SIM** ✅ (data de efetividade)
- Impacto: HIGH (exportação de serviços)

```bash
cat ../05_STJ_SUMULAS/STF-REPERCUSSAO-GERAL/STF_TEMA_69.md | grep -A 3 "MODULAÇÃO"
```

---

### Teste 3: JSON com chave primária
✅ **Esperado:** Arquivo `exports/stf_sumulas_export.json` contém:

```bash
python3 << 'EOF'
import json
with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)
    
print(f"✅ Total SV: {len(data['sumulas_vinculantes'])}")
print(f"✅ Total Tema RG: {len(data['teses_repercussao_geral'])}")
print(f"\n✅ Exemplo SV:")
if data['sumulas_vinculantes']:
    sv = data['sumulas_vinculantes'][0]
    print(f"  - Número: {sv['identificacao']['numero_identificador']}")
    print(f"  - Setor: {sv['impacto_business_compliance']['setor_afetado']}")
    print(f"  - Modulação: {sv['modulacao_efeitos']['houve_modulacao']}")
    
print(f"\n✅ Exemplo Tema RG:")
if data['teses_repercussao_geral']:
    tema = data['teses_repercussao_geral'][0]
    print(f"  - Número: {tema['identificacao']['numero_identificador']}")
    print(f"  - Setor: {tema['impacto_business_compliance']['setor_afetado']}")
    print(f"  - Modulação: {tema['modulacao_efeitos']['houve_modulacao']}")
EOF
```

---

### Teste 4: Keywords para RAG
✅ **Esperado:** JSON contém `vetorizacao_keywords` em cada súmula

```bash
python3 << 'EOF'
import json
with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)
    
if data['sumulas_vinculantes']:
    sv = data['sumulas_vinculantes'][0]
    print(f"Keywords de {sv['identificacao']['numero_identificador']}:")
    for kw in sv['vetorizacao_keywords']:
        print(f"  - #{kw}")
EOF
```

---

### Teste 5: Detecção de artigos CF/88
✅ **Esperado:** Cada súmula tem artigos da Constituição

```bash
python3 << 'EOF'
import json
with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)
    
for sv in data['sumulas_vinculantes'][:3]:
    print(f"\n{sv['identificacao']['numero_identificador']}:")
    print("Artigos CF/88:")
    for art in sv['ancoragem_legal']['artigos_crfb88']:
        print(f"  - {art}")
EOF
```

---

### Teste 6: Impacto de Modulação
✅ **Esperado:** SV/Tema com `houve_modulacao = true` também tem `regra_da_modulacao`

```bash
python3 << 'EOF'
import json
with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)
    
for sv in data['sumulas_vinculantes']:
    if sv['modulacao_efeitos']['houve_modulacao']:
        print(f"✅ MODULAÇÃO DETECTADA: {sv['identificacao']['numero_identificador']}")
        print(f"   Regra: {sv['modulacao_efeitos']['regra_da_modulacao'][:100]}...")
        
for tema in data['teses_repercussao_geral']:
    if tema['modulacao_efeitos']['houve_modulacao']:
        print(f"✅ MODULAÇÃO DETECTADA: {tema['identificacao']['numero_identificador']}")
        print(f"   Regra: {tema['modulacao_efeitos']['regra_da_modulacao'][:100]}...")
EOF
```

---

## 📊 Resultado Esperado

```
======================================================================
✅ PROCESSAMENTO COMPLETO!
======================================================================

📊 ESTATÍSTICAS:
   • total_sumulas_vinculantes: 5
   • total_teses_rg: 4
   • total_analisadas: 9
   • total_erros: 0
   • taxa_sucesso: 100.0%
   • arquivos_criados_sv: 5
   • arquivos_criados_rg: 4

📁 OUTPUT:
   • Súmulas Vinculantes: C:\...\Fenice bRain\05_STJ_SUMULAS\STF-SUMULAS-VINCULANTES
   • Teses RG: C:\...\Fenice bRain\05_STJ_SUMULAS\STF-REPERCUSSAO-GERAL
   • JSON Export: C:\...\scripts\exports
```

---

## ✅ Checklist de Validação

- [ ] Arquivo `sumulas_input.txt` existe com 9 súmulas
- [ ] Pasta `STF-SUMULAS-VINCULANTES/` criada com 5 arquivos `.md`
- [ ] Pasta `STF-REPERCUSSAO-GERAL/` criada com 4 arquivos `.md`
- [ ] Arquivo `exports/stf_sumulas_export.json` criado com ~30KB
- [ ] JSON é válido (sem erros de parse)
- [ ] Cada MD tem frontmatter YAML
- [ ] Modulação detectada em 3 documentos (Tema 69, Tema 834, Tema 762)
- [ ] Keywords presentes em todos os arquivos
- [ ] Artigos CF/88 mapeados corretamente
- [ ] Setores identificados (Tributário, Administrativo, Previdenciário, etc)

Se todos os itens ✅, o sistema está **100% funcional**.

---

## 🐛 Se algo não funcionar

| Erro | Solução |
|------|---------|
| `FileNotFoundError: sumulas_input.txt` | Certifique-se de estar no diretório `scripts/` |
| `ModuleNotFoundError: stf_sumula_analyzer` | Mesma solução acima |
| JSON inválido | Verificar se há caracteres especiais não codificados |
| 0 arquivos criados | Verificar se `sumulas_input.txt` tem formato correto (delimitador `---`) |

---

## 🎓 Próximos Passos

Após validar tudo, você pode:

1. ✅ **Abrir em Obsidian**
   ```
   Vault → Fenice bRain/05_STJ_SUMULAS/
   Graph View → Ver conexões entre súmulas
   ```

2. ✅ **Usar JSON para embeddings**
   ```python
   import openai
   # Gerar embeddings com text-embedding-3-small
   ```

3. ✅ **Integrar com seu SaaS**
   - Usar chave primária (STF_SV_57) para lookups SQL
   - Disparar triggers de compliance se `modulacao == true`
   - Expor via API REST para clientes

---

**Tempo estimado:** 5 minutos  
**Resultado:** Sistema STF Súmula Analyzer 100% validado ✅
