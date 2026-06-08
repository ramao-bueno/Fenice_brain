# 📊 Dashboard STF — Jurisprudência

Dashboard HTML simples para visualizar súmulas vinculantes e temas de repercussão geral do STF.

## 🚀 Quick Start

### 1️⃣ Instalar dependências (primeira vez)

```bash
pip install psycopg2-binary
```

### 2️⃣ Rodar o servidor

```bash
python dashboard_server.py
```

Você verá:
```
📊 Dashboard rodando em http://localhost:8000
Pressione Ctrl+C para parar
```

### 3️⃣ Abrir no navegador

**Opção A: Automático (recomendado)**
```bash
start http://localhost:8000
```

**Opção B: Manual**
- Abra seu navegador (Chrome, Firefox, Edge, Safari)
- Digite na barra de endereço: `http://localhost:8000`
- Pressione Enter

## 📈 O que você verá

- **📊 Estatísticas gerais** — Total de súmulas, com modulação, taxa
- **📌 Gráfico de Modulação** — Pizza chart: Sem vs Com modulação
- **🏛️ Distribuição por Setor** — Bar chart dos principais setores
- **⏰ Últimas Publicações** — Lista das 4 mais recentes

## 🔧 Como funciona

### Arquitetura

```
┌─ dashboard_server.py ─────────────────┐
│ Servidor HTTP em localhost:8000       │
│ • GET /api/stats → Dados gerais      │
│ • GET /api/modulacoes → Modulação    │
│ • GET /api/por-setor → Por setor     │
│ • GET / → Serve dashboard_stf.html   │
└──────────────────────────────────────┘
         ↕ (HTTP JSON)
┌─ dashboard_stf.html ──────────────────┐
│ Dashboard HTML + Chart.js              │
│ • Consome API do servidor            │
│ • Atualiza a cada 30 segundos         │
│ • Gráficos interativos                │
└──────────────────────────────────────┘
         ↕ (psycopg2)
┌─ PostgreSQL ──────────────────────────┐
│ Database fenice_brain (opcional)      │
│ • Se disponível: dados reais          │
│ • Se não: dados de exemplo            │
└──────────────────────────────────────┘
```

## 💾 Dados

### Se PostgreSQL está rodando

O servidor automaticamente se conecta a:
- **Host:** localhost
- **Database:** fenice_brain
- **User:** fenice
- **Password:** fenice_secure_password
- **Port:** 5432

E exibe **dados reais** do banco.

### Se PostgreSQL não está disponível

O servidor usa **dados de exemplo** (mockados) para demonstração.

## 🌐 Acesso remoto

Se quiser acessar de outro computador, edite `dashboard_server.py`:

```python
HOST = '0.0.0.0'  # Em vez de 'localhost'
PORT = 8000
```

Depois acesse: `http://<seu-ip>:8000`

## 🛑 Parar o servidor

Pressione **Ctrl+C** no terminal.

## 🐛 Troubleshooting

### "Erro: conexão recusada"
- Certifique-se de que o servidor está rodando
- Verifique se está na porta 8000
- Tente: `http://localhost:8000` (não `file://`)

### "Desconectado do servidor" no dashboard
- Abra DevTools (F12) → Console
- Verifique se há erros de CORS
- Reinicie o servidor: `Ctrl+C` + `python dashboard_server.py`

### Dados mostram "Carregando..." permanentemente
- Verifique conexão com PostgreSQL
- Se não tiver PostgreSQL, dados de exemplo devem aparecer
- Recarregue a página (F5)

### A página fica em branco
- Abra DevTools (F12) → Console
- Verifique se há erros JavaScript
- Tente em outro navegador

## 📝 Estrutura de arquivos

```
scripts/
├── dashboard_server.py          ← Servidor HTTP
├── dashboard_stf.html           ← Dashboard visual
└── README-DASHBOARD-STF.md      ← Este arquivo
```

## 🎨 Personalização

### Mudar cores

Em `dashboard_stf.html`, procure por:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Mude estes códigos hexadecimais */
```

### Mudar porta do servidor

Em `dashboard_server.py`:
```python
PORT = 8000  # Mude para outra porta
```

### Adicionar mais gráficos

1. Adicione endpoint em `dashboard_server.py`
2. Chame em `dashboard_stf.html` no `loadData()`
3. Renderize com Chart.js

## 📊 Endpoints da API

### GET /api/stats
```json
{
  "total_sumulas": 456,
  "sumulas_com_modulacao": 127,
  "ultimas_publicacoes": [
    {
      "numero_identificador": "SV-45",
      "setor_afetado": "Tributário",
      "data_publicacao": "2024-06-01"
    }
  ]
}
```

### GET /api/modulacoes
```json
{
  "labels": ["Sem Modulação", "Com Modulação"],
  "values": [329, 127]
}
```

### GET /api/por-setor
```json
{
  "labels": ["Tributário", "Administrativo", ...],
  "values": [89, 72, ...]
}
```

## 🔄 Atualização automática

O dashboard atualiza automaticamente a cada **30 segundos**. Para mudar:

Em `dashboard_stf.html`, procure por:
```javascript
setInterval(loadData, 30000);  // 30000 ms = 30 segundos
```

## 📱 Responsivo

Dashboard funciona em:
- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (com layout adaptado)
- ⚠️ Mobile (display reduzido, mas funcional)

## 🚀 Deploy em produção

Para usar em produção:

1. **Use Gunicorn** (em vez de servidor HTTP simples):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 dashboard_server:app
```

2. **Proteja com senha** (adicione autenticação)

3. **Use HTTPS** (com certificado SSL)

4. **Configure firewall** (abra apenas porta 8000 se necessário)

## 📞 Suporte

Se não funcionar:
1. Verifique se Python 3.7+ está instalado: `python --version`
2. Verifique dependências: `pip list | grep psycopg2`
3. Veja logs do servidor: `python dashboard_server.py`
4. Abre DevTools no navegador: F12 → Console

---

**Criado em:** 2026-06-07  
**Versão:** 1.0  
**Status:** ✅ Funcional (com dados de exemplo)
