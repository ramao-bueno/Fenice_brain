# Instalação do MCP Jurídico (jurismcp)

Guia para instalar o `ivancaron/jurismcp` — pesquisa em tempo real de jurisprudência
STJ, STF, TST e TJES via Selenium + Patchright.

## Pré-requisitos

- Python 3.11+
- `uv` (gerenciador de pacotes): `pip install uv`
- Google Chrome instalado

## Instalação

```powershell
# 1. Clonar o repositório
git clone https://github.com/ivancaron/jurismcp C:\ferramentas\jurismcp

# 2. Entrar no diretório
cd C:\ferramentas\jurismcp

# 3. Instalar o Patchright (driver Chrome)
uv run patchright install

# 4. Testar
uv run python -c "from jurismcp import *; print('OK')"
```

## Configuração no Fenice bRain

O arquivo `.mcp.json` na raiz do vault já está configurado:

```json
{
  "mcpServers": {
    "jurismcp": {
      "command": "uv",
      "args": ["--directory", "C:/ferramentas/jurismcp", "run", "serve"]
    }
  }
}
```

## Uso via Claude Code

Após instalação, reiniciar Claude Code. O MCP aparece automaticamente.

Comandos disponíveis:
- `pesquisar_stj "palavra chave"` — busca no STJ
- `pesquisar_stf "palavra chave"` — busca no STF
- `pesquisar_tst "palavra chave"` — busca no TST

## Alternativa sem MCP (scraping direto)

Para consultas pontuais sem instalar o MCP:

```python
# scripts/busca_jurisprudencia_manual.py
import requests

def buscar_stj(termo: str) -> list:
    """Busca simples no SCON/STJ (pode precisar de ajuste por Cloudflare)"""
    url = f"https://scon.stj.jus.br/SCON/pesquisar.jsp?b=ACOR&livre={termo}"
    r = requests.get(url, timeout=20)
    # Parsear HTML...
    return []
```

## Troubleshooting

**Erro: Chrome não encontrado**
```powershell
uv run patchright install chromium
```

**Erro: Cloudflare bloqueando**
- O jurismcp usa Patchright para bypass de bot detection
- Verificar se o Chrome está na versão mais recente

**MCP não aparece no Claude**
- Verificar se `.mcp.json` está na raiz: `C:\Fenice_bRain\.mcp.json`
- Reiniciar Claude Code após qualquer mudança no `.mcp.json`
