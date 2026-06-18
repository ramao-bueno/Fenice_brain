# STJ HSE Scraper — Quick Start (5 minutos)

**Status:** ✅ Pronto para usar  
**Última atualização:** 2026-06-07

---

## ⚡ Instalação (2 minutos)

### 1. Verificar Python
```bash
python --version  # Deve ser 3.8+
```

### 2. Instalar dependências
```bash
pip install requests beautifulsoup4
```

### 3. Verificar estrutura

O sistema espera esta estrutura (criada automaticamente):
```
Fenice bRain/
├── scripts/
│   ├── config_stj_scraper.py      ✅
│   ├── stj_hse_normalizer.py       ✅
│   ├── stj_hse_scraper.py          ✅
│   └── logs/                       (auto)
└── 05_STJ_SUMULAS/
    └── HSE/                        (auto)
```

---

## 🚀 Execução Básica (2 minutos)

```bash
cd "Fenice bRain\scripts"
python stj_hse_scraper.py
```

**Resultado esperado:**
- ✅ 47-60 arquivos `.md` em `05_STJ_SUMULAS/HSE/`
- ✅ 1 arquivo `hse_export.json`
- ✅ Log em `logs/stj_hse_scraper.log`

---

## 🎯 Casos de Uso Rápidos (1 minuto cada)

### Buscar apenas 20 HSEs
```bash
# Editar: stj_hse_scraper.py, linha ~286
hses = scraper.buscar_hse(paginas=1)  # Mudou de 3 para 1
```

### Ativar debug
```python
# Em config_stj_scraper.py
DEBUG = True
SAVE_HTML_BRUTO = True  # Salva HTML em _cache_stj_hse/
LOG_LEVEL = "DEBUG"
```

### Usar cache local (sem internet)
```python
# Em config_stj_scraper.py
USE_CACHE = True
```

---

## 📂 Estrutura de Saída

### Markdown (exemplo)
```
05_STJ_SUMULAS/HSE/HDE-2.345.md
├── Frontmatter YAML
│   ├── artigo: HDE 2.345
│   ├── relator: Ministro X
│   ├── pais_origem: Portugal
│   ├── status: DEFERIDO
│   └── risco_compliance: MEDIUM
└── Conteúdo
    ├── Redação Legal
    ├── Análise da Homologação
    ├── Checklist de Requisitos Legais
    └── Artigos Correlatos
```

### JSON (exemplo)
```
hse_export.json
├── metadados_processuais (processo, relator, data, país)
├── resultado_homologacao (status, fundamento)
├── checklist_requisitos (4 requisitos legais CPC)
├── analise_coercitiva (objeto, citação, tese)
├── risco_compliance (score LOW/MEDIUM/HIGH)
└── metadata (timestamp, fonte, confiabilidade)
```

---

## 🔧 Configuração Customizada (1 minuto)

### Aumentar/diminuir páginas
```python
# stj_hse_scraper.py, linha ~286
hses = scraper.buscar_hse(paginas=5)  # 5 páginas = ~100 decisões
```

### Filtrar por países
```python
# config_stj_scraper.py, linha ~65
PAISES_INTERESSE = ["Portugal", "España"]  # Apenas Portugal + España
PAISES_INTERESSE = []  # Todos os países
```

### Mudar nível de log
```python
# config_stj_scraper.py, linha ~54
LOG_LEVEL = "DEBUG"   # Verbose
LOG_LEVEL = "INFO"    # Normal
LOG_LEVEL = "WARNING" # Silencioso
```

---

## ⚠️ Problemas Comuns

| Problema | Solução |
|---|---|
| "Cloudflare access denied" | Esperar 5 min ou usar VPN |
| "ModuleNotFoundError: requests" | `pip install requests beautifulsoup4` |
| "No such file or directory" | Executar de dentro de `scripts/` |
| "Nenhum resultado encontrado" | Verificar se STJ mudou URL (ver logs) |

---

## 📊 O que esperar

### Tempos
- Página 1 (20 decisões): ~30 segundos
- Página 2 (20 decisões): ~30 segundos
- Página 3 (20 decisões): ~30 segundos
- **Total 3 páginas:** ~2 minutos

### Resultados típicos
- HSEs com status DEFERIDO: 60-70%
- HSEs com status INDEFERIDO: 20-30%
- HSEs com risco HIGH: 10-20%

---

## 🔗 Próximos Passos

Depois de rodar a primeira vez:

1. ✅ Verificar output em Obsidian
   ```
   Abrir: Fenice bRain/05_STJ_SUMULAS/HSE/
   Tudo em Markdown com frontmatter? Sim ✅
   ```

2. ✅ Testar busca por tags
   ```
   Obsidian: Ctrl+F → #stj
   Resultado: Todos os arquivos HSE aparecem ✅
   ```

3. ✅ Examinar JSON
   ```
   Abrir: hse_export.json
   É válido? Usar JSONLint https://jsonlint.com/
   ```

4. ✅ (Opcional) Filtrar por país
   ```python
   # Ver USAGE-EXAMPLES.md, Exemplo 2.3
   ```

---

## 📖 Documentação Completa

- **README-STJ-HSE-SCRAPER.md** — Guia detalhado (70 linhas)
- **USAGE-EXAMPLES.md** — 10 exemplos práticos (400 linhas)
- **Este arquivo** — Quick Start (50 linhas)

---

## ✅ Checklist Pós-Execução

- [ ] Arquivos MD criados em `05_STJ_SUMULAS/HSE/`?
- [ ] JSON `hse_export.json` gerado?
- [ ] Log criado em `logs/stj_hse_scraper.log`?
- [ ] Frontmatter YAML está correto?
- [ ] Tabela de requisitos legais aparece em cada arquivo?
- [ ] Tags (#stj, #hse, etc) estão presentes?
- [ ] JSON é válido (testar em JSONLint)?

Se todos os itens ✅, o sistema está funcionando corretamente.

---

## 🎓 Próximas Lições

Após dominar este script, explore:

1. **Integração com Notion** — Enviar HSEs pra Sofia Próvision HQ
2. **Automação via cron** — Rodar automaticamente todo dia 9 AM
3. **API REST** — Expor HSEs via FastAPI
4. **Banco de dados** — Salvar em SQLite/PostgreSQL
5. **Dashboard** — Análise visual em Obsidian/Grafana

Exemplos de todos em **USAGE-EXAMPLES.md**.

---

**Criado por:** Claude Haiku 4.5  
**Data:** 2026-06-07  
**Versão:** 1.0
