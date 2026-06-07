# STJ HSE Scraper — Sistema de Extração de Homologações de Sentença Estrangeira

**Status:** ✅ Pronto para uso  
**Última atualização:** 2026-06-07  
**Componentes:** 3 scripts Python (config + normalizer + scraper)

---

## 🎯 O que faz

Extrai **Homologações de Sentença Estrangeira (HSE)** do **STJ SCON** e as estrutura em:
- Arquivos Markdown com frontmatter YAML (compatível com Obsidian)
- JSON normalizado com schema padrão (metadados + checklist legal + risco)
- Logging detalhado para monitoramento

Resultado: 50-200 decisões HSE prontas para análise jurídica, integração com Fenice Brain, e IA.

---

## 📋 Pré-requisitos

### Dependências Python
```bash
pip install requests beautifulsoup4
```

### Estrutura de pastas (criar se não existir)
```
FENICE bRain/
├── scripts/
│   ├── config_stj_scraper.py      ✅ Existe
│   ├── stj_hse_normalizer.py       ✅ Existe
│   ├── stj_hse_scraper.py          ✅ Existe
│   └── logs/                       (criado automaticamente)
│       └── stj_hse_scraper.log     (criado na 1ª execução)
│
└── 05_STJ_SUMULAS/
    └── HSE/                        (criado automaticamente)
        ├── HDE-1234.md             (output 1)
        ├── HDE-1235.md             (output 2)
        └── hse_export.json         (export completo)
```

---

## 🚀 Uso Básico

### 1. Execução Padrão (60 resultados, 3 páginas)

```bash
cd "FENICE bRain\scripts"
python stj_hse_scraper.py
```

**Output esperado:**
```
======================================================================
🔍 STJ HSE SCRAPER — Homologação de Sentença Estrangeira
======================================================================

Buscando página 1...
  [1/20] Buscando /SCON/...
  ✅ Normalizada: HDE 1.234
  Salvo: C:\...\FENICE bRain\05_STJ_SUMULAS\HSE\HDE-1.234.md
...

======================================================================
✅ SCRAPING COMPLETO!
======================================================================

📊 ESTATÍSTICAS:
   • HSEs extraídas: 47
   • Arquivos salvos: 47
   • Output: C:\...\FENICE bRain\05_STJ_SUMULAS\HSE\
```

---

## ⚙️ Configuração

Editar `config_stj_scraper.py` para customizar:

### Número de páginas a buscar
```python
MAX_PAGINAS = 10  # Máximo 10 (= 200 decisões por run)
                  # Padrão no main(): 3 páginas (60 decisões)
```

Mudar na função `main()` de `stj_hse_scraper.py`:
```python
hses = scraper.buscar_hse(paginas=3)  # ← mudar aqui
```

### Países de interesse
```python
PAISES_INTERESSE = [
    "Portugal", "España", "USA", "China", "Japão", "Itália",
    "França", "Alemanha", "Bélgica", "Suíça"
]
```
Deixe vazio `[]` para buscar todos os países.

### Logging
```python
LOG_LEVEL = "INFO"  # DEBUG | INFO | WARNING | ERROR
SAVE_HTML_BRUTO = False  # True para debug (salva HTML bruto em _cache_stj_hse/)
```

### Cache
```python
USE_CACHE = True
CACHE_EXPIRY_DAYS = 7  # Redownload se cache > 7 dias
```

---

## 📊 Estrutura do Output

### Arquivo Markdown (exemplo: HDE-2.345.md)

```markdown
---
artigo: HDE 2.345
lei: "Superior Tribunal de Justiça — HSE"
tipo: homologacao-sentenca-estrangeira
relator: Ministro João Silva
pais_origem: Portugal
data_julgamento: 2026-06-01
status: DEFERIDO
risco_compliance: MEDIUM
tags:
  - stj
  - hse
  - homologacao
  - sentenca-estrangeira
  - alimentos
created: 2026-06-07
---

# HDE 2.345 — HSE

**Relator:** Ministro João Silva
**Data:** 2026-06-01
**País de Origem:** Portugal
**Status:** DEFERIDO

---

## 📋 REDAÇÃO LEGAL

> Requisitos preenchidos; alimentos não violam ordem pública...

---

## ⚖️ ANÁLISE DA HOMOLOGAÇÃO

### Requisitos Legais

| Requisito | Status |
|---|---|
| Trânsito em Julgado | ✅ |
| Citação Válida | ✅ |
| Não Viola Ordem Pública | ✅ |
| Competência do Brasil | ✅ |

### Objeto da Decisão

Alimentos

### Risco de Compliance

**Score:** MEDIUM

Possível execução suspensa se houver contestação.

---

## 🔗 ARTIGOS CORRELATOS

- [[CPC Arts. 960-965]] — Homologação de sentença estrangeira
- [[CC Arts. 1-10]] — Aplicabilidade de lei estrangeira
- [[CF/88 Art. 5]] — Ordem pública (direitos fundamentais)

---

**Extraído em:** 2026-06-07 10:30:45 (automático)
**Confiabilidade:** 0.7
```

### JSON (hse_export.json)

```json
[
  {
    "metadados_processuais": {
      "numero_processo": "HDE 2.345",
      "relator": "Ministro João Silva",
      "orgao_julgador": "CORTE ESPECIAL",
      "data_julgamento": "2026-06-01",
      "pais_de_origem": "Portugal"
    },
    "resultado_homologacao": {
      "status": "DEFERIDO",
      "fundamento_principal": "Requisitos preenchidos; alimentos não violam ordem pública..."
    },
    "checklist_requisitos": {
      "transito_em_julgado_comprovado": true,
      "citacao_valida": true,
      "violacao_ordem_publica": false,
      "incompetencia_absoluta_brasil": false
    },
    "analise_coercitiva": {
      "objeto_da_decisao": "Alimentos",
      "detalhe_da_citacao": "[A extrair do texto completo]",
      "tese_juridica_fixada": "[A extrair da fundamentação]"
    },
    "risco_compliance": {
      "score_complexidade": "MEDIUM",
      "observacao_critica": "Análise automática — revisar manualmente"
    },
    "metadata": {
      "normalizado_em": "2026-06-07T10:30:45.123456",
      "fonte": "STJ SCON",
      "confiabilidade": "0.7"
    }
  }
]
```

---

## 🔍 Checklist Legal (Automático)

O scraper detecta automaticamente os 4 requisitos legais para HSE (CPC Arts. 960-965):

| Requisito | Detectado por |
|---|---|
| **Trânsito em Julgado** | Palavras-chave: "transitado", "definivo", "trânsito" |
| **Citação Válida** | Palavras-chave: "citação", "citado", "notificado", "revelia" |
| **Não Viola Ordem Pública** | Palavras-chave: "ordem pública", "violação", "inconstitucional", "direitos humanos", "consumidor" |
| **Competência do Brasil** | Palavras-chave: "competência", "privativa", "exclusiva" |

⚠️ **Nota:** Detecção por regex é heurística. Sempre revisar manualmente para operações críticas.

---

## 📈 Scoring de Risco

Calculado automaticamente baseado em resultado + checklist:

| Score | Critério | Ação |
|---|---|---|
| **LOW** | Deferido + todos requisitos OK | ✅ Executável, baixo risco |
| **MEDIUM** | Parcialmente deferido OU incompetência absoluta | ⚠️ Revisar, pode ter recursos |
| **HIGH** | Indeferido OU viola ordem pública | ❌ Não executável, alto risco |

---

## 🛠️ Troubleshooting

### Erro: "Cloudflare access denied"

STJ usa Cloudflare. Se bloqueado:

**Opção 1:** Usar VPN ou esperar alguns minutos antes de retry
```bash
# Retry manual
python stj_hse_scraper.py
```

**Opção 2:** Usar HTML salvo manualmente
1. Acesse https://www.stj.jus.br/SCON
2. Busque "HDE" manualmente
3. Salve página em `scripts/_cache_stj_hse/decision.html`
4. Adapte código para ler arquivo local

### Erro: "Filename too long" (Windows)

Já corrigido com:
```bash
git config core.longpaths true
```

Se ainda aparecer, reduzir tamanho de nomes de país ou objeto.

### Sem resultados encontrados

**Verificar:**
```bash
# Ver logs detalhados
type logs\stj_hse_scraper.log

# Verificar URL
echo "STJ_SCON_SEARCH: https://www.stj.jus.br/SCON/SearchBRS?baseName=VERDICTBRS"
```

Possível: STJ mudou URL ou formato de resposta. Atualizar regex em `config_stj_scraper.py`.

### JSON muito grande

Se `hse_export.json` > 50 MB:
```python
# Em config_stj_scraper.py, reduzir:
MAX_PAGINAS = 5  # Ao invés de 10
```

---

## 📚 Integração com Fenice Brain

### Links Automáticos

O scraper cria links para:
- `[[CPC Arts. 960-965]]` — Lei de HSE
- `[[CC Arts. 1-10]]` — Lei estrangeira
- `[[CF/88 Art. 5]]` — Ordem pública

Criar essas notas no Obsidian para que os links funcionem.

### Tags para Busca

```
Ctrl+Shift+F em Obsidian:
- #stj — Todas as HSEs
- #hse — Todas as HSEs
- #alimentos — Apenas HSEs sobre alimentos
- #portugal — Apenas de Portugal
- #deferido — Apenas deferidas
- #high-risk — Apenas HIGH risk
```

### Graph View

No Obsidian, ativar Graph View para ver:
- Conexões entre HSEs
- Relação com CPC/CC/CF/CDC
- Cluster de países

---

## 🔄 Automação Futura

### Agendar scraping semanal (Linux/Mac)

```bash
# Adicionar ao crontab
0 9 * * 1 cd /path/to/fenice && python scripts/stj_hse_scraper.py

# Resultado: Toda segunda-feira às 9 AM, nova busca HSE
```

### Agendar scraping semanal (Windows)

```powershell
# Task Scheduler
$Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "scripts\stj_hse_scraper.py"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
Register-ScheduledTask -TaskName "STJ HSE Scraper" -Action $Action -Trigger $Trigger
```

---

## 📝 Próximos Passos (Opcional)

- [ ] Criar Obsidian plugin para buscar HSE por filtros (país, objeto, risco)
- [ ] Integrar HSE com análise de jurisprudência relacionada (REsp)
- [ ] Exportar HSEs para Notion (Sofia Próvision)
- [ ] Criar relatório automático de novas HSEs por semana
- [ ] Implementar detecção de mudança de jurisprudência (comparar decisões antigas vs novas)

---

## 📞 Referências

- **CPC Arts. 960-965** — Homologação de sentença estrangeira
- **Lei 9.307/96** — Lei de Arbitragem (para sentença arbitral estrangeira)
- **STJ SCON** — https://www.stj.jus.br/SCON

---

**Criado por:** Claude Haiku 4.5  
**Data:** 2026-06-07  
**Versão:** 1.0 (Pronto para produção)
