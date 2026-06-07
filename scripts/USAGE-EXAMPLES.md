# STJ HSE Scraper — Exemplos de Uso

Guia prático com exemplos de código para usar os 3 scripts em diferentes cenários.

---

## 📌 Exemplo 1: Uso Básico (linha de comando)

### Buscar 60 HSEs (3 páginas padrão)

```bash
cd "FENICE bRain\scripts"
python stj_hse_scraper.py
```

**Resultado:**
- 47-60 arquivos `.md` em `05_STJ_SUMULAS/HSE/`
- 1 arquivo `hse_export.json` com todo o schema
- Log em `logs/stj_hse_scraper.log`

---

## 🐍 Exemplo 2: Uso em Python (integração custom)

### 2.1 Buscar apenas 20 HSEs

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/path/to/fenice/scripts')

from stj_hse_scraper import STJHSEScraper

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=1)  # Apenas 1 página = ~20 decisões

print(f"Extraídas {len(hses)} HSEs")
for hse in hses:
    print(f"  - {hse['metadados_processuais']['numero_processo']}")
```

### 2.2 Normalizar HTML manualmente

```python
from stj_hse_normalizer import STJHSENormalizer

# Ler HTML de arquivo
with open('decision.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Normalizar
normalizer = STJHSENormalizer(html)
schema = normalizer.normalizar()

# Acessar resultados
print(f"Processo: {schema['metadados_processuais']['numero_processo']}")
print(f"Status: {schema['resultado_homologacao']['status']}")
print(f"Risco: {schema['risco_compliance']['score_complexidade']}")
```

### 2.3 Filtrar HSEs por critérios

```python
from stj_hse_scraper import STJHSEScraper
import json

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=2)

# Filtrar apenas deferidas
deferidas = [h for h in hses 
             if h['resultado_homologacao']['status'] == 'DEFERIDO']

# Filtrar apenas de Portugal
portugal = [h for h in hses 
            if 'portugal' in h['metadados_processuais']['pais_de_origem'].lower()]

# Filtrar por risco LOW
low_risk = [h for h in hses 
            if h['risco_compliance']['score_complexidade'] == 'LOW']

print(f"Deferidas: {len(deferidas)}")
print(f"De Portugal: {len(portugal)}")
print(f"Baixo risco: {len(low_risk)}")
```

### 2.4 Exportar para CSV

```python
from stj_hse_scraper import STJHSEScraper
import csv

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=1)

# Salvar como CSV
with open('hses.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'Processo', 'Relator', 'Data', 'País', 'Status', 'Risco'
    ])
    writer.writeheader()
    
    for hse in hses:
        writer.writerow({
            'Processo': hse['metadados_processuais']['numero_processo'],
            'Relator': hse['metadados_processuais']['relator'],
            'Data': hse['metadados_processuais']['data_julgamento'],
            'País': hse['metadados_processuais']['pais_de_origem'],
            'Status': hse['resultado_homologacao']['status'],
            'Risco': hse['risco_compliance']['score_complexidade']
        })

print("Salvo: hses.csv")
```

---

## 🔍 Exemplo 3: Análise de Jurisprudência

### Detectar padrões de risco por país

```python
from stj_hse_scraper import STJHSEScraper
from collections import defaultdict

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=3)

# Agrupar por país
por_pais = defaultdict(list)
for hse in hses:
    pais = hse['metadados_processuais']['pais_de_origem']
    por_pais[pais].append(hse)

# Calcular risco médio por país
for pais, decisoes in sorted(por_pais.items()):
    total = len(decisoes)
    deferidas = len([h for h in decisoes 
                     if h['resultado_homologacao']['status'] == 'DEFERIDO'])
    taxa_sucesso = (deferidas / total * 100) if total > 0 else 0
    
    print(f"{pais:20} | Total: {total:2} | Taxa sucesso: {taxa_sucesso:5.1f}%")
```

### Detectar violação de ordem pública

```python
from stj_hse_scraper import STJHSEScraper

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=2)

violacao = [h for h in hses 
            if h['checklist_requisitos']['violacao_ordem_publica']]

print(f"HSEs com violação de ordem pública: {len(violacao)}")
for hse in violacao:
    print(f"  - {hse['metadados_processuais']['numero_processo']} ({hse['analise_coercitiva']['objeto_da_decisao']})")
```

---

## 🎯 Exemplo 4: Monitoramento Automático

### Script para executar diariamente (Unix/Linux)

**Arquivo: `monitor_hse.py`**

```python
#!/usr/bin/env python3
"""
Script para monitorar novas HSEs diariamente
Salva um relatório com estatísticas
"""

import sys
sys.path.insert(0, '/path/to/fenice/scripts')

from stj_hse_scraper import STJHSEScraper
from datetime import datetime
import json

def gerar_relatorio(hses):
    relatorio = {
        "data": datetime.now().isoformat(),
        "total": len(hses),
        "deferidas": len([h for h in hses 
                         if h['resultado_homologacao']['status'] == 'DEFERIDO']),
        "indeferidas": len([h for h in hses 
                           if h['resultado_homologacao']['status'] == 'INDEFERIDO']),
        "parcial": len([h for h in hses 
                       if h['resultado_homologacao']['status'] == 'PARCIALMENTE DEFERIDO']),
        "risco_high": len([h for h in hses 
                          if h['risco_compliance']['score_complexidade'] == 'HIGH']),
        "objetos": {}
    }
    
    # Agrupar por objeto
    for hse in hses:
        obj = hse['analise_coercitiva']['objeto_da_decisao']
        relatorio["objetos"][obj] = relatorio["objetos"].get(obj, 0) + 1
    
    return relatorio

# Executar
scraper = STJHSEScraper()
print("Iniciando busca HSE...")
hses = scraper.buscar_hse(paginas=1)

# Gerar relatório
relatorio = gerar_relatorio(hses)

# Salvar
with open('relatorio_hse_diario.json', 'w', encoding='utf-8') as f:
    json.dump(relatorio, f, indent=2, ensure_ascii=False)

# Imprimir
print(f"\n✅ Relatório gerado: {relatorio['total']} HSEs")
print(f"   Deferidas: {relatorio['deferidas']}")
print(f"   Indeferidas: {relatorio['indeferidas']}")
print(f"   Parcial: {relatorio['parcial']}")
print(f"   Alto risco: {relatorio['risco_high']}")
```

**Executar diariamente com cron (Linux/Mac):**

```bash
# ~/.bashrc ou similar
0 9 * * * cd /path/to/fenice/scripts && python monitor_hse.py
```

---

## 🧪 Exemplo 5: Testes Unitários

**Arquivo: `test_stj_hse.py`**

```python
import pytest
import sys
sys.path.insert(0, '/path/to/fenice/scripts')

from stj_hse_normalizer import STJHSENormalizer

class TestSTJHSENormalizer:
    
    def test_extrai_numero_processo(self):
        html = "<html>HDE 1.234</html>"
        normalizer = STJHSENormalizer(html)
        assert "HDE" in normalizer._extrair_numero_processo()
    
    def test_extrai_data_julgamento(self):
        html = "<html>15 de junho de 2026</html>"
        normalizer = STJHSENormalizer(html)
        data = normalizer._extrair_data_julgamento()
        assert data == "2026-06-15"
    
    def test_deteccao_resultado_deferido(self):
        html = "<html>HOMOLOGADA a sentença estrangeira</html>"
        normalizer = STJHSENormalizer(html)
        resultado = normalizer._extrair_resultado()
        assert "DEFERIDO" in resultado
    
    def test_calculo_risco_indeferido(self):
        html = "<html>INDEFERIDA a homologação</html>"
        normalizer = STJHSENormalizer(html)
        resultado = normalizer._extrair_resultado()
        from stj_hse_normalizer import ChecklistRequisitos
        checklist = ChecklistRequisitos(True, True, False, False)
        risco = normalizer._calcular_risco(resultado, checklist)
        assert risco == "HIGH"

# Executar testes
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Executar:**

```bash
cd scripts
pytest test_stj_hse.py -v
```

---

## 📊 Exemplo 6: Integração com Banco de Dados

### Salvar HSEs em SQLite

```python
import sqlite3
from stj_hse_scraper import STJHSEScraper

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=1)

# Criar tabela
conn = sqlite3.connect('hse.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS hse (
    id INTEGER PRIMARY KEY,
    numero_processo TEXT UNIQUE,
    relator TEXT,
    data_julgamento DATE,
    pais_origem TEXT,
    status TEXT,
    risco TEXT,
    json_completo TEXT
)''')

# Inserir dados
for hse in hses:
    c.execute('''INSERT OR IGNORE INTO hse VALUES (
        NULL, ?, ?, ?, ?, ?, ?, ?
    )''', (
        hse['metadados_processuais']['numero_processo'],
        hse['metadados_processuais']['relator'],
        hse['metadados_processuais']['data_julgamento'],
        hse['metadados_processuais']['pais_de_origem'],
        hse['resultado_homologacao']['status'],
        hse['risco_compliance']['score_complexidade'],
        str(hse)
    ))

conn.commit()
print(f"Salvo em SQLite: {len(hses)} HSEs")
```

### Consultar dados depois

```python
import sqlite3

conn = sqlite3.connect('hse.db')
c = conn.cursor()

# Buscar HSEs de Portugal
c.execute("SELECT numero_processo, status, risco FROM hse WHERE pais_origem = 'Portugal'")
resultados = c.fetchall()

for numero, status, risco in resultados:
    print(f"{numero} — {status} — Risco: {risco}")
```

---

## 🌐 Exemplo 7: Webhook para Notificação

### Notificar via Discord quando HSE de alto risco é extraída

```python
import requests
from stj_hse_scraper import STJHSEScraper

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID"

scraper = STJHSEScraper()
hses = scraper.buscar_hse(paginas=1)

# Filtrar alto risco
high_risk = [h for h in hses 
             if h['risco_compliance']['score_complexidade'] == 'HIGH']

if high_risk:
    for hse in high_risk:
        msg = f"""
🚨 **HSE DE ALTO RISCO DETECTADA**
Processo: {hse['metadados_processuais']['numero_processo']}
Relator: {hse['metadados_processuais']['relator']}
País: {hse['metadados_processuais']['pais_de_origem']}
Objeto: {hse['analise_coercitiva']['objeto_da_decisao']}
Status: {hse['resultado_homologacao']['status']}
        """
        
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
        print(f"Notificação enviada: {hse['metadados_processuais']['numero_processo']}")
```

---

## 📱 Exemplo 8: API Simples (FastAPI)

**Arquivo: `api_hse.py`**

```python
from fastapi import FastAPI, Query
from stj_hse_scraper import STJHSEScraper
import json

app = FastAPI()
scraper = STJHSEScraper()

@app.get("/hse/buscar")
def buscar_hse(paginas: int = Query(1, le=10)):
    """Buscar HSEs"""
    hses = scraper.buscar_hse(paginas=paginas)
    return {"total": len(hses), "hses": hses}

@app.get("/hse/por-pais")
def por_pais(pais: str):
    """Filtrar por país"""
    hses = scraper.buscar_hse(paginas=1)
    filtrado = [h for h in hses 
                if pais.lower() in h['metadados_processuais']['pais_de_origem'].lower()]
    return {"pais": pais, "total": len(filtrado), "hses": filtrado}

@app.get("/hse/por-risco")
def por_risco(risco: str = Query("HIGH", regex="LOW|MEDIUM|HIGH")):
    """Filtrar por risco"""
    hses = scraper.buscar_hse(paginas=1)
    filtrado = [h for h in hses 
                if h['risco_compliance']['score_complexidade'] == risco]
    return {"risco": risco, "total": len(filtrado)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Usar:**

```bash
# Terminal 1
pip install fastapi uvicorn
python api_hse.py

# Terminal 2
curl "http://localhost:8000/hse/buscar?paginas=1"
curl "http://localhost:8000/hse/por-pais?pais=Portugal"
curl "http://localhost:8000/hse/por-risco?risco=HIGH"
```

---

## 🔗 Exemplo 9: Integração com Obsidian (Dataview)

**Nota em Obsidian: HSE-DASHBOARD.md**

```markdown
# Dashboard HSE

## Estatísticas Gerais

```dataview
TABLE
  status, pais_origem, risco_compliance
FROM "05_STJ_SUMULAS/HSE"
WHERE file.name != "hse_export"
```

## HSEs de Alto Risco

```dataview
TABLE
  relator, pais_origem, file.ctime
FROM "05_STJ_SUMULAS/HSE"
WHERE risco_compliance = "HIGH"
SORT file.ctime DESC
```

## Por País

```dataview
TABLE
  status, risco_compliance
FROM "05_STJ_SUMULAS/HSE"
WHERE pais_origem = "Portugal"
```
```

---

## 🎓 Exemplo 10: Debug e Troubleshooting

### Verificar um HTML específico

```python
from stj_hse_normalizer import STJHSENormalizer

# Ler arquivo bruto
with open('scripts/_cache_stj_hse/decision.html', 'r', encoding='utf-8') as f:
    html = f.read()

normalizer = STJHSENormalizer(html)

# Testar cada extração
print("Número processo:", normalizer._extrair_numero_processo())
print("Relator:", normalizer._extrair_relator())
print("Data:", normalizer._extrair_data_julgamento())
print("País:", normalizer._extrair_pais_origem())
print("Resultado:", normalizer._extrair_resultado())
print("Objeto:", normalizer._extrair_objeto())
print("Checklist:", normalizer._extrair_checklist())
print("Risco:", normalizer._calcular_risco(
    normalizer._extrair_resultado(), 
    normalizer._extrair_checklist()
))
```

---

**Pronto para usar! 🚀**
