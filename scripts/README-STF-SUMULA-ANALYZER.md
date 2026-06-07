# STF Súmula Analyzer — Análise Profunda de SV e Teses de RG

**Status:** ✅ Pronto para uso  
**Data:** 2026-06-07  
**Versão:** 1.0

---

## 🎯 O que faz

Analisa **Súmulas Vinculantes (SV)** e **Teses de Repercussão Geral (Tema RG)** do STF e estrutura em:

- **Markdown** com frontmatter YAML (compatível com Obsidian)
- **JSON** com schema jurídico completo (pronto para vetorização/RAG)
- **Chave primária universal** (STF_SV_57, STF_TEMA_69) para lookups rápidos
- **Análise de impacto business** (estimativa de risco financeiro)
- **Detecção automática de modulação** com regra específica
- **Keywords para busca semântica** (RAG/LLM)

---

## 📋 Pré-requisitos

### Dependências Python
```bash
# Nenhuma dependência externa! Tudo é stdlib
python --version  # 3.8+
```

### Estrutura de pastas
```
FENICE bRain/
├── scripts/
│   ├── stf_sumula_analyzer.py      ✅ Existe
│   ├── config_stf_analyzer.py      ✅ Existe
│   ├── stf_sumula_processor.py     ✅ Existe
│   └── logs/                       (criado auto)
│
└── 05_STJ_SUMULAS/
    ├── STF-SUMULAS-VINCULANTES/    (criado auto)
    │   ├── STF_SV_57.md            (output 1)
    │   └── STF_SV_58.md            (output 2)
    │
    ├── STF-REPERCUSSAO-GERAL/      (criado auto)
    │   ├── STF_TEMA_69.md          (output 1)
    │   └── STF_TEMA_70.md          (output 2)
    │
    └── _cache_stf_sumulas/         (debug)
```

---

## 🚀 Uso Básico

### 1. Preparar arquivo de entrada

Criar `sumulas_input.txt` com múltiplas súmulas delimitadas por `---`:

```
Súmula Vinculante 57 — SUPREMO TRIBUNAL FEDERAL

O direito de greve dos servidores públicos será exercido nos termos
e limites definidos em lei complementar federal.

Processo: RE 574.706
Data: 19 de dezembro de 2008

---

Tema 69 de Repercussão Geral

Critério para o reconhecimento da repercussão geral...
[conteúdo]

---
```

### 2. Executar análise

```bash
cd "FENICE bRain\scripts"
python stf_sumula_processor.py
```

### 3. Output

```
05_STJ_SUMULAS/
├── STF-SUMULAS-VINCULANTES/
│   ├── STF_SV_57.md          (markdown com análise)
│   └── STF_SV_58.md
├── STF-REPERCUSSAO-GERAL/
│   ├── STF_TEMA_69.md        (markdown com análise)
│   └── STF_TEMA_70.md
└── exports/
    └── stf_sumulas_export.json   (JSON estruturado)
```

---

## 📊 Estrutura do Output

### Arquivo Markdown (exemplo: STF_SV_57.md)

```markdown
---
identificacao:
  tipo: SUMULA_VINCULANTE
  numero: SV 57
  processo: RE 574.706
  data_publicacao: 2008-12-19
  status: ATIVO
...
---

# SV 57 — Súmula Vinculante

**Processo Paradigma:** RE 574.706
**Data de Publicação:** 2008-12-19
**Chave Primária:** `STF_SV_57`

---

## 📋 ENUNCIADO

> O direito de greve dos servidores públicos será exercido nos termos...

---

## 🎯 NÚCLEO DA TESE

Servidores públicos têm direito de greve, mas sujeito a lei complementar federal...

---

## ⚖️ ANCORAGEM LEGAL

### Dispositivos Constitucionais

- Art. 9 (Direito de Greve)
- Art. 37 (Administração Pública)

### Leis Infraconstitucionais

- Lei Complementar 128/2008

---

## 🔄 MODULAÇÃO DE EFEITOS

**Houve Modulação?** ❌ NÃO

---

## 💼 IMPACTO BUSINESS & COMPLIANCE

**Setor Afetado:** ADMINISTRATIVO
**Potencial de Impacto:** MEDIUM

### Vulnerabilidade de Compliance

Órgãos públicos e entidades de direito público precisam se adequar aos
termos dessa tese. Qualquer restrição ao direito de greve deve estar
fundamentada em lei complementar federal...

---

## 🔍 PALAVRAS-CHAVE

#administrativo #direito-de-greve #servidores-públicos #lei-complementar
```

### JSON (stf_sumulas_export.json)

```json
{
  "sumulas_vinculantes": [
    {
      "identificacao": {
        "tipo": "SUMULA_VINCULANTE",
        "numero_identificador": "SV 57",
        "processo_paradigma": "RE 574.706",
        "data_publicacao_dje": "2008-12-19",
        "status_atual": "ATIVO"
      },
      "conteudo_textual": {
        "enunciado_original": "O direito de greve dos servidores...",
        "nucleo_da_tese": "Servidores públicos têm direito de greve, mas sujeito..."
      },
      "ancoragem_legal": {
        "artigos_crfb88": ["Art. 9", "Art. 37"],
        "leis_infraconstitucionais_afetadas": ["Lei Complementar 128/2008"]
      },
      "modulacao_efeitos": {
        "houve_modulacao": false,
        "regra_da_modulacao": null
      },
      "impacto_business_compliance": {
        "setor_afetado": "ADMINISTRATIVO",
        "vulnerabilidade_compliance": "Órgãos públicos precisam se adequar...",
        "potencial_monetario": "MEDIUM"
      },
      "vetorizacao_keywords": [
        "administrativo",
        "direito-de-greve",
        "servidores-públicos"
      ],
      "metadata": {
        "analisado_em": "2026-06-07T10:30:00",
        "confiabilidade": "0.8",
        "requer_revisao_manual": false
      }
    }
  ],
  "teses_repercussao_geral": [...],
  "metadata": {
    "total_analisadas": 5,
    "total_erros": 0,
    "exportado_em": "2026-06-07T10:35:00",
    "versao": "1.0"
  }
}
```

---

## 🔍 Análises Automáticas

### 1. Tipo de Norma
✅ Detecta automaticamente SV ou Tema RG  
✅ Extrai número (SV 57, Tema 69)  
✅ Busca processo paradigma (RE 574.706, ADI 1.234)  

### 2. Ancoragem Legal
✅ Mapeia artigos CF/88 citados  
✅ Extrai leis infraconstitucionais  
✅ Valida contra lista oficial (não inventa artigos)  

### 3. Modulação de Efeitos
✅ Detecta se houve modulação  
✅ Extrai regra específica (ex: "efeitos a partir de 15/03/2017")  
✅ Flag para trigger de compliance automático  

### 4. Impacto Business
✅ Classifica por setor (Tributário, Trabalhista, Previdenciário, etc)  
✅ Estima potencial financeiro (HIGH/MEDIUM/LOW)  
✅ Gera recomendação de compliance  

### 5. Busca Semântica
✅ Extrai keywords críticas  
✅ Pronto para gerar embeddings (OpenAI, etc)  
✅ Facilita RAG em sistemas de IA jurídica  

---

## ⚙️ Configuração

Editar `config_stf_analyzer.py`:

### Diretórios de saída
```python
STF_OUTPUT_SV = FENICE_BASE / "05_STJ_SUMULAS" / "STF-SUMULAS-VINCULANTES"
STF_OUTPUT_RG = FENICE_BASE / "05_STJ_SUMULAS" / "STF-REPERCUSSAO-GERAL"
```

### Logging
```python
LOG_LEVEL = "DEBUG"   # DEBUG | INFO | WARNING | ERROR
SAVE_TEXTO_BRUTO = True  # Salva texto bruto em _cache_stf_sumulas/
```

### Análise
```python
ANALISAR_MODULACAO = True
ANALISAR_IMPACTO_BUSINESS = True
EXTRAIR_KEYWORDS = True
```

---

## 📌 Chave Primária Universal

Cada súmula/tese tem uma **chave primária única e inteligível**:

```
STF_SV_57          ← Súmula Vinculante 57
STF_TEMA_69        ← Tema 69 de Repercussão Geral
```

**Vantagens:**
- ✅ Fácil de digitar e lembrar
- ✅ Permite lookups rápidos em banco de dados relacional
- ✅ Integração com motor jurídico do seu SaaS
- ✅ Rastreamento de jurisprudência por cliente

**Uso em SQL:**
```sql
SELECT * FROM jurisprudencia WHERE chave_primaria = 'STF_SV_57';

-- Ou para buscar todas as SV de um cliente
SELECT * FROM jurisprudencia 
WHERE chave_primaria LIKE 'STF_SV_%' 
AND cliente_id = 123;
```

---

## 🔗 Integração com Banco de Dados Vetorial

### Usar com OpenAI Embeddings

```python
import openai
import json

# Carregar JSON
with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)

# Para cada súmula
for sumula in data['sumulas_vinculantes']:
    # Gerar embedding
    response = openai.Embedding.create(
        input=sumula['conteudo_textual']['enunciado_original'],
        model="text-embedding-3-small"
    )
    
    embedding = response['data'][0]['embedding']
    chave = f"STF_SV_{sumula['identificacao']['numero_identificador'].split()[-1]}"
    
    # Salvar em banco vetorial (Pinecone, Weaviate, etc)
    # vector_db.upsert(chave, embedding, metadata=sumula)
```

### Busca semântica na prática

```python
# Usuário: "Como fica a greve de servidores públicos?"
# Sistema executa busca semântica com embedding da pergunta
# Retorna: STF_SV_57 como resultado top (porque tem keywords específicas)
```

---

## 🚨 Triggers de Compliance Automático

Se `modulacao_efeitos.houve_modulacao == true`:

```python
# Pseudo-código para seu sistema de compliance
if sumula['modulacao_efeitos']['houve_modulacao']:
    disparar_auditoria({
        'tipo': 'MODULACAO_DETECTADA',
        'sumula': sumula['identificacao']['numero_identificador'],
        'regra': sumula['modulacao_efeitos']['regra_da_modulacao'],
        'acao': 'REVISAR_PROCESSOS_ANTERIORES_AO_MARCO_TEMPORAL'
    })
```

**Impacto prático:** Quando uma súmula com modulação é importada, seu sistema automaticamente:
1. Flags processos em andamento anteriores à data limite
2. Avisa equipe jurídica para revisão
3. Rastreia em relatório de compliance

---

## 💼 Casos de Uso Reais

### Caso 1: SaaS de Due Diligence
Cliente faz DD de empresa tributária. Sistema automaticamente:
1. Busca todas as súmulas de `setor_afetado == "Tributário"`
2. Verifica se há modulação recente
3. Gera relatório de "risco jurídico tributário"

### Caso 2: Consultoria Previdenciária
Advogado que cuida de INSS busca: "greve servidor público"
1. Sistema faz busca semântica nos keywords
2. Retorna STF_SV_57 como resultado
3. Advogado copia análise + impacto compliance

### Caso 3: Automação de Petição
Sistema de geração automática de petições:
1. Advogado digita problema: "meu cliente é servidor e foi impedido de greve"
2. Sistema busca jurisprudência relevante (STF_SV_57)
3. Insere precedente na petição automaticamente

---

## 🔧 Troubleshooting

| Problema | Solução |
|----------|---------|
| "ModuleNotFoundError: stf_sumula_analyzer" | Executar de dentro de `scripts/` ou adicionar ao `sys.path` |
| "Arquivo sumulas_input.txt não encontrado" | Criar arquivo no mesmo diretório que `stf_sumula_processor.py` |
| "Artigos CF/88 não detectados" | Verificar formato do texto (deve citar como "Art. 9" ou "artigo 9") |
| "Modulação não detectada corretamente" | Adicionar padrão regex em `_extrair_modulacao()` |

---

## 📚 Próximos Passos

### Integração com Obsidian
```bash
# Os arquivos MD criados automaticamente aparecem em:
FENICE bRain/05_STJ_SUMULAS/STF-SUMULAS-VINCULANTES/
FENICE bRain/05_STJ_SUMULAS/STF-REPERCUSSAO-GERAL/

# Use Graph View para ver conexões entre súmulas
```

### Integração com Notion
```python
# Ver USAGE-EXAMPLES-STF.md para código de integração
```

### Automação com Cron
```bash
# Buscar novas súmulas automaticamente (requer scraper)
0 9 * * 1 cd /path/to/fenice && python scripts/stf_sumula_processor.py
```

---

## 🎓 Exemplos de Código

### Exemplo 1: Analisar uma súmula
```python
from stf_sumula_analyzer import STFSumulaAnalyzer
import json

texto = """
Súmula Vinculante 57 — ...
[conteúdo]
"""

analyzer = STFSumulaAnalyzer(texto)
schema = analyzer.analisar()
print(json.dumps(schema, indent=2, ensure_ascii=False))
```

### Exemplo 2: Filtrar por setor
```python
import json

with open('exports/stf_sumulas_export.json') as f:
    data = json.load(f)

# Só as súmulas de TRIBUTÁRIO
tributarias = [
    s for s in data['sumulas_vinculantes']
    if 'TRIBUTÁRIO' in s['impacto_business_compliance']['setor_afetado']
]

print(f"Total tributárias: {len(tributarias)}")
```

### Exemplo 3: Detectar modulação
```python
for sumula in data['sumulas_vinculantes']:
    if sumula['modulacao_efeitos']['houve_modulacao']:
        print(f"{sumula['identificacao']['numero_identificador']}: {sumula['modulacao_efeitos']['regra_da_modulacao']}")
```

---

## 📞 Referências

- **Súmulas Vinculantes:** https://portal.stf.jus.br/jurisprudencia/sumulaVinculante.asp
- **Repercussão Geral:** https://portal.stf.jus.br/jurisprudencia/sumulaRepercussao.asp
- **Jurisprudência STF:** https://portal.stf.jus.br/jurisprudencia/

---

**Criado por:** Claude Haiku 4.5  
**Data:** 2026-06-07  
**Versão:** 1.0 (Production Ready)
