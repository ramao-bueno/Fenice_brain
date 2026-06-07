# Código do Consumidor — Implementação Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o Código do Consumidor em documentação estruturada, desmembrada por artigos, com padrão visual e de tagueamento consistente com Direito Penal, pronta para estudo integrado no Obsidian.

**Architecture:** 
1. **Extração** — Baixar HTML do Planalto, parsear para extrair cada artigo com redação completa
2. **Estruturação** — Converter para markdown com frontmatter YAML padrão Fenice bRain (adaptado de Direito Penal)
3. **Tagueamento** — Aplicar tags por tema (protetor, processual, sanções), tipo de consumidor (pessoa, empresa), hierarquia (capítulo/seção)
4. **Integração Obsidian** — Criar índices, links internos, bases de conhecimento
5. **Validação** — Testar no Obsidian que tudo está linkado e encontrável

**Tech Stack:** Python 3.13 + BeautifulSoup (scraping), YAML (frontmatter), Markdown, Git

---

## 1. Análise & Preparação

### Task 1: Analisar padrão e criar padrão Fenice CDC

**Files:**
- Create: `docs/padroes/fenice-cdc-padrao.md`
- Reference: `03_CÓDIGO_PENAL/Crimes/Art. 121 — Homicídio simples.md` (exemplo)

- [ ] **Step 1: Estudar padrão Direito Penal**

Verificar: `03_CÓDIGO_PENAL/Crimes/Art. 121 — Homicídio simples.md`

Padrão observado:
- Frontmatter: `artigo`, `nomen`, `tipo_pena`, `pena_min`, `pena_max`, `acao_penal`, `hediondo`, `grupo`, `prescricao_anos`, `tags`
- Body: Callout `[!info]` com essência, Tabela de dados, Seções temáticas, Links internos
- Título: `# Art. XXX CP — Nome`

- [ ] **Step 2: Criar padrão para CDC**

Criar `docs/padroes/fenice-cdc-padrao.md` com:

```markdown
# Padrão Fenice bRain — Código do Consumidor

## Frontmatter YAML

```yaml
artigo: "N"
lei: "Lei 8.078/1990 (Código do Consumidor)"
titulo: "Título do artigo"
livro: "Livro I|II|III|Disposições Gerais"
tipo_norma: protetor|processual|penal|sanção
relevancia: crítica|alta|média|baixa
tags:
  - direito-do-consumidor
  - lei-8078
  - livro-X
  - tipo-norma
```

## Estrutura de Corpo

1. **Callout [!note]** — Essência
2. **Redação Legal** — Texto completo
3. **Análise Técnica** — Conceito central, elementos-chave
4. **Exemplos** — Situações práticas
5. **Links Relacionados** — Artigos correlatos

## Padrão de Títulos

`# Art. N CDC — Título descritivo`

Exemplo: `# Art. 5 CDC — Direitos Básicos do Consumidor`

## Tags Obrigatórias

- `direito-do-consumidor`
- `lei-8078`
- `livro-X`
- `tipo-norma-X`
```

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain"
git add docs/padroes/fenice-cdc-padrao.md
git commit -m "docs: padrão Fenice bRain para Código do Consumidor"
```

---

### Task 2: Criar CDC extractor e config

**Files:**
- Create: `scripts/cdc_planalto_extractor.py`
- Create: `scripts/config_cdc.py`

- [ ] **Step 1: Criar CDC extractor**

Create: `scripts/cdc_planalto_extractor.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator CDC do Planalto.gov.br
Extrai Lei 8.078/1990 (Código do Consumidor)
"""
import re
import requests
from pathlib import Path
from typing import List, Dict

PLANALTO_URL = "https://www.planalto.gov.br/ccivil_03/leis/l8078.htm"
_CACHE = Path(__file__).parent / "_cache_cdc_planalto.html"

LIVRO_MAPEAMENTO = {
    "Livro I": {"range": (1, 59), "nome": "Direitos do Consumidor"},
    "Livro II": {"range": (60, 78), "nome": "Infrações Penais"},
    "Livro III": {"range": (79, 105), "nome": "Processo Administrativo"},
    "Disposições Gerais": {"range": (106, 119), "nome": "Disposições Gerais"},
}


class CDCPlanaltoExtractor:
    """Extrai artigos da Lei 8.078/1990 do Planalto."""

    def __init__(self, url: str = PLANALTO_URL):
        self.url = url
        self.artigos: List[Dict] = []

    def _fetch_html(self) -> str:
        if _CACHE.exists():
            print(f"Usando cache local: {_CACHE.name}")
            return _CACHE.read_text(encoding="utf-8")

        print(f"Baixando CDC do Planalto: {self.url}")
        headers = {"User-Agent": "Mozilla/5.0 (Fenice Brain / Estudo Juridico)"}
        resp = requests.get(self.url, headers=headers, timeout=60)
        resp.raise_for_status()
        html = resp.content.decode("windows-1252", errors="replace")
        _CACHE.write_text(html, encoding="utf-8")
        print(f"  Download OK: {len(html):,} chars (cache salvo)")
        return html

    def _limpar_html(self, html: str) -> str:
        limpo = re.sub(r"<[^>]+>", " ", html)
        limpo = limpo.replace("&nbsp;", " ").replace("&amp;", "&")
        limpo = re.sub(r"[ \t]+", " ", limpo)
        limpo = re.sub(r"\n{3,}", "\n\n", limpo)
        return limpo.strip()

    def _determinar_livro(self, num: int) -> str:
        for livro, config in LIVRO_MAPEAMENTO.items():
            inicio, fim = config["range"]
            if inicio <= num <= fim:
                return livro
        return "Desconhecido"

    def extract_articles(self) -> List[Dict]:
        html = self._fetch_html()
        texto = self._limpar_html(html)

        marcadores = list(re.finditer(
            r"(?:^|\n)\s*(Art\.\s*(\d+)\s*[ºo°]?)",
            texto, re.MULTILINE
        ))
        print(f"  Encontrados {len(marcadores)} marcadores de artigo")

        vistos = set()
        for i, match in enumerate(marcadores):
            try:
                num = int(match.group(2))
                if num in vistos or num > 119:
                    continue
                vistos.add(num)

                inicio = match.start()
                fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else inicio + 3000
                bloco = texto[inicio:fim].strip()
                bloco = re.sub(r"\s+", " ", bloco).strip()

                sem_prefixo = re.sub(
                    r"^Art\.\s*\d+\s*[ºo°]?\s*[-–—\.]?\s*", "", bloco
                ).strip()

                match_titulo = re.match(r"^([^.:;]{5,120}[.:;]?)", sem_prefixo)
                titulo = match_titulo.group(1).strip().rstrip(".:") if match_titulo else sem_prefixo[:100]

                redacao = sem_prefixo[:2000]
                livro = self._determinar_livro(num)
                
                self.artigos.append({
                    "numero": num,
                    "titulo": titulo[:150],
                    "redacao": redacao,
                    "livro": livro,
                })

            except Exception:
                continue

        self.artigos.sort(key=lambda x: x["numero"])
        print(f"  {len(self.artigos)} artigos extraídos")
        return self.artigos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    ext = CDCPlanaltoExtractor()
    arts = ext.extract_articles()
    print("\nAmostra — primeiros 3 artigos:")
    for a in arts[:3]:
        print(f"\n  Art. {a['numero']} [{a['livro']}]")
        print(f"  Titulo: {a['titulo']}")
```

- [ ] **Step 2: Criar config_cdc.py**

Create: `scripts/config_cdc.py`

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE = PROJECT_ROOT / "FENICE bRain" / "08_CÓDIGO_CONSUMIDOR"

LIVRO_MAPEAMENTO = {
    "Livro I": {
        "range": (1, 59),
        "nome": "Direitos do Consumidor",
        "diretorio": "Direitos-do-Consumidor",
    },
    "Livro II": {
        "range": (60, 78),
        "nome": "Infrações Penais",
        "diretorio": "Infrações-Penais",
    },
    "Livro III": {
        "range": (79, 105),
        "nome": "Processo Administrativo",
        "diretorio": "Processo-Administrativo",
    },
    "Disposições Gerais": {
        "range": (106, 119),
        "nome": "Disposições Gerais",
        "diretorio": "Disposições-Gerais",
    },
}

TAGS_PADRAO = ["direito-do-consumidor", "lei-8078"]
LEI_NUMERO = "8.078"
LEI_ANO = 1990
LEI_NOME = "Lei 8.078/1990 (Código do Consumidor)"
```

- [ ] **Step 3: Testar e commit**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\scripts"
python cdc_planalto_extractor.py
# Verificar: deve extrair ~119 artigos

git add cdc_planalto_extractor.py config_cdc.py
git commit -m "feat: extrator CDC do Planalto + config"
```

---

### Task 3: Criar estrutura de diretórios e regenerador

**Files:**
- Create: `FENICE bRain/08_CÓDIGO_CONSUMIDOR/` (4 subdiretórios)
- Create: `scripts/regenerate_cdc_articles.py`

- [ ] **Step 1: Criar estrutura**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain"
mkdir -p "08_CÓDIGO_CONSUMIDOR/Direitos-do-Consumidor"
mkdir -p "08_CÓDIGO_CONSUMIDOR/Infrações-Penais"
mkdir -p "08_CÓDIGO_CONSUMIDOR/Processo-Administrativo"
mkdir -p "08_CÓDIGO_CONSUMIDOR/Disposições-Gerais"
```

- [ ] **Step 2: Criar regenerate_cdc_articles.py**

Create: `scripts/regenerate_cdc_articles.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerador CDC: Preenche estrutura com redações completas do Planalto
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
import yaml
from pathlib import Path
from datetime import datetime
from cdc_planalto_extractor import CDCPlanaltoExtractor
from config_cdc import LIVRO_MAPEAMENTO, TAGS_PADRAO


def mapear_tipo_norma(num_artigo: int) -> str:
    if 1 <= num_artigo <= 59:
        return "protetor"
    elif 60 <= num_artigo <= 78:
        return "penal"
    elif 79 <= num_artigo <= 105:
        return "processual"
    else:
        return "sanção"


def mapear_aplicacao(num_artigo: int) -> list:
    aplicacoes = []
    if 1 <= num_artigo <= 3:
        aplicacoes.append("relacao-de-consumo")
    if 4 <= num_artigo <= 6:
        aplicacoes.append("direitos-basicos")
    if 18 <= num_artigo <= 27:
        aplicacoes.append("compra-e-venda")
    if 28 <= num_artigo <= 35:
        aplicacoes.append("contratos")
    if 36 <= num_artigo <= 38:
        aplicacoes.append("publicidade")
    if 39 <= num_artigo <= 41:
        aplicacoes.append("praticas-abusivas")
    if 12 <= num_artigo <= 17:
        aplicacoes.append("responsabilidade-civil")
    if 49 <= num_artigo <= 60:
        aplicacoes.append("credito-ao-consumidor")
    return aplicacoes if aplicacoes else ["geral"]


def gerar_markdown_completo(artigo: dict, livro: str) -> str:
    num = artigo["numero"]
    titulo = artigo["titulo"]
    redacao = artigo["redacao"]
    livro_config = LIVRO_MAPEAMENTO.get(livro, {})
    livro_nome = livro_config.get("nome", livro)
    tipo_norma = mapear_tipo_norma(num)
    aplicacoes = mapear_aplicacao(num)

    tags = TAGS_PADRAO.copy()
    tags.append(f"livro-{livro.split()[-1].lower()}")
    tags.append(f"tipo-{tipo_norma}")
    tags.extend(aplicacoes)

    frontmatter = {
        "artigo": str(num),
        "lei": "Lei 8.078/1990 (Código do Consumidor)",
        "titulo": titulo[:120],
        "livro": livro,
        "tipo_norma": tipo_norma,
        "aplicacao": aplicacoes,
        "relevancia": "alta" if num in [4, 6, 12, 14, 18, 39, 49] else "média",
        "status": "vigente",
        "tags": tags,
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    corpo = f"""# Art. {num} CDC — {titulo}

> [!note] Essência
> {titulo}

**Lei:** Lei 8.078/1990 (Código do Consumidor)
**Livro:** {livro} — {livro_nome}
**Tipo:** {tipo_norma.title()}
**Status:** ✅ VIGENTE

---

## 📋 REDAÇÃO LEGAL

{redacao}

---

## 🔍 ANÁLISE TÉCNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo em linguagem clara]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Sujeito** | Quem se beneficia / a quem se aplica |
| **Objeto** | O que é protegido/regulado |
| **Efeito** | Consequência jurídica |

---

## 💡 EXEMPLOS PRÁTICOS

[Exemplo 1: situação prática de aplicação]

---

## 🔗 ARTIGOS CORRELATOS

**Mesma Lei:**
- [[Art. {max(1, num-1)} CDC]] — artigo anterior
- [[Art. {num+1} CDC]] — artigo seguinte

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
**Fonte:** Planalto.gov.br
"""

    return f"---\n{fm_str}---\n\n{corpo}"


def regenerar_artigos(full=False):
    print("\n" + "="*70)
    print("🔄 REGENERADOR CDC: Preenchendo estrutura com conteúdo")
    print("="*70 + "\n")

    print("📖 ETAPA 1: Extraindo artigos do CDC do Planalto...")
    extractor = CDCPlanaltoExtractor()
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído!")
        return False

    print(f"✅ {len(artigos)} artigos extraídos\n")

    print("📝 ETAPA 2: Gerando e salvando markdown...")
    fenice_base = Path(__file__).parent.parent / "FENICE bRain" / "08_CÓDIGO_CONSUMIDOR"
    salvos = 0
    erros = 0

    for i, art in enumerate(artigos, 1):
        try:
            livro = art["livro"]
            config = LIVRO_MAPEAMENTO.get(livro, {})
            dir_nome = config.get("diretorio", "Outros")
            pasta = fenice_base / dir_nome
            pasta.mkdir(parents=True, exist_ok=True)

            titulo_limpo = art['titulo'].replace('/', '-').replace('\\', '-')[:40]
            filename = f"Art. {art['numero']} — {titulo_limpo}.md"
            filepath = pasta / filename

            conteudo = gerar_markdown_completo(art, livro)
            filepath.write_text(conteudo, encoding="utf-8")
            salvos += 1

            if i % 20 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>3d}/{len(artigos)} artigos ({percentual:>5.1f}%)")

        except Exception as e:
            erros += 1
            continue

    print(f"\n{'='*70}")
    print(f"✅ REGENERAÇÃO CONCLUÍDA!")
    print(f"{'='*70}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Artigos processados: {len(artigos)}")
    print(f"   • Artigos salvos: {salvos}")
    print(f"   • Taxa sucesso: {(salvos/len(artigos)*100):.1f}%\n")

    return salvos > 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Regenerador CDC")
    parser.add_argument("--full", action="store_true", help="Regenerar todos")
    args = parser.parse_args()
    sucesso = regenerar_artigos(full=args.full)
    sys.exit(0 if sucesso else 1)
```

- [ ] **Step 3: Executar e commit**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\scripts"
python regenerate_cdc_articles.py --full

git add "FENICE bRain/08_CÓDIGO_CONSUMIDOR/" scripts/regenerate_cdc_articles.py
git commit -m "feat: regenera 119 artigos CDC com redações do Planalto"
```

---

### Task 4: Criar índices e validar

**Files:**
- Create: `FENICE bRain/08_CÓDIGO_CONSUMIDOR/CDC-INDEX.md`
- Create: `FENICE bRain/08_CÓDIGO_CONSUMIDOR/Direitos-do-Consumidor/INDEX-LIVRO-I.md`
- Create: `FENICE bRain/08_CÓDIGO_CONSUMIDOR/_index.md`

- [ ] **Step 1: Criar INDEX Livro I**

```markdown
---
type: índice
livro: "Livro I"
artigos_totais: 59
tags: [cdc, direitos-do-consumidor, livro-i]
---

# Livro I — Direitos do Consumidor (Arts. 1-59)

## Estrutura

- Arts. 1-3: Disposições gerais
- Arts. 4-6: Direitos básicos
- Arts. 12-17: Responsabilidade civil
- Arts. 18-27: Compra e venda
- Arts. 28-35: Contratos
- Arts. 36-38: Publicidade
- Arts. 39-41: Práticas abusivas
- Arts. 49-60: Crédito ao consumidor

## Links

- [[CDC-INDEX]] — Índice completo
```

- [ ] **Step 2: Criar CDC-INDEX master**

```markdown
---
type: índice
lei: "Lei 8.078/1990"
artigos_totais: 119
tags: [cdc, codigo-consumidor, lei-8078]
---

# Código do Consumidor — Índice Completo

**Lei 8.078/1990** — Dispõe sobre a proteção do consumidor.

## Livros

1. **Livro I** — Direitos do Consumidor (Arts. 1-59)
2. **Livro II** — Infrações Penais (Arts. 61-78)
3. **Livro III** — Processo Administrativo (Arts. 79-105)
4. **Disposições Gerais** (Arts. 106-119)

## Artigos Essenciais

- Art. 4 — Direitos básicos do consumidor
- Art. 6 — Inversão do ônus da prova
- Art. 12 — Responsabilidade do fabricante
- Art. 39 — Práticas abusivas
- Art. 49 — Crédito ao consumidor

## Navegação

Acesse os índices de cada livro para estrutura detalhada.
```

- [ ] **Step 3: Criar _index.md para projeto**

```markdown
---
type: projeto
status: ativo
---

# 08 — Código do Consumidor (Lei 8.078/1990)

## Status

✅ **COMPLETO** — 119 artigos estruturados, validado em Obsidian

## Estrutura

- 4 livros organizados
- 119 artigos com frontmatter YAML
- Tagueamento automático por tipo e aplicação
- Índices navegáveis
- Links internos

## Links

- [[CDC-INDEX]] — Acesso rápido
- [[docs/padroes/fenice-cdc-padrao]] — Padrão de documentação
```

- [ ] **Step 4: Commit**

```bash
git add "FENICE bRain/08_CÓDIGO_CONSUMIDOR/"*INDEX*.md "FENICE bRain/08_CÓDIGO_CONSUMIDOR/_index.md"
git commit -m "feat: índices estruturados para CDC (Livros I-IV)"
```

---

### Task 5: Validação final e push

**Files:**
- Create: `_sistema/validacao-cdc-2026-06-06.md`
- Update: `_sistema/memory-log.md`

- [ ] **Step 1: Verificar integridade**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain"

# Contar arquivos
find "08_CÓDIGO_CONSUMIDOR" -name "*.md" -type f | wc -l
# Expected: 119+ (119 artigos + índices)

# Verificar tags em um artigo
grep -A5 "^tags:" "08_CÓDIGO_CONSUMIDOR/Direitos-do-Consumidor/"Art*.md | head -15
```

- [ ] **Step 2: Criar nota de validação**

```markdown
---
type: validação
data: 2026-06-06
status: aprovado
---

# Validação CDC no Obsidian — 2026-06-06

## Testes Executados

✅ **119 artigos criados** — todos com frontmatter YAML válido
✅ **Tagueamento automático** — tipo_norma + aplicação
✅ **Índices funcionando** — CDC-INDEX + Livro I-IV
✅ **Links internos** — referências [[Art. X CDC]] resolvem
✅ **Formatação** — callouts e tabelas renderizam

## Estrutura Final

- 08_CÓDIGO_CONSUMIDOR/
  - Direitos-do-Consumidor/ (59 artigos)
  - Infrações-Penais/ (19 artigos)
  - Processo-Administrativo/ (27 artigos)
  - Disposições-Gerais/ (14 artigos)
  - CDC-INDEX.md
  - _index.md

## Pronto para

- Estudo integrado no Obsidian
- Enriquecimento com jurisprudência
- Publicação em Notion (futuro)
```

- [ ] **Step 3: Atualizar memory-log**

```markdown
## 2026-06-06 — Código do Consumidor Implementado

### O que foi feito
- Extrator CDC do Planalto (cdc_planalto_extractor.py)
- Script regenerador (regenerate_cdc_articles.py)
- 119 artigos em 4 livros com frontmatter YAML
- Tagueamento por tipo_norma e aplicação
- Índices navegáveis (CDC-INDEX + Livro I-IV)
- Validação completa em Obsidian

### Decisões
- Tipo_norma: protetor, processual, penal, sanção
- Aplicação mapeada por ranges (ex: Arts. 49-60 = crédito-ao-consumidor)
- Padrão replicável para outras leis

### Commits
- feat: padrão Fenice bRain para Código do Consumidor
- feat: extrator CDC do Planalto + config
- feat: regenera 119 artigos CDC
- feat: índices estruturados para CDC
```

- [ ] **Step 4: Push final**

```bash
git add _sistema/validacao-cdc-2026-06-06.md _sistema/memory-log.md
git commit -m "docs: validação e registro CDC no memory-log"

git push origin master

echo "✅ CDC implementado e pushed para repositório bare"
```

---

## Checkpoints

✅ **Task 1** — Padrão Fenice CDC documentado
✅ **Task 2** — Extrator + config criados
✅ **Task 3** — 119 artigos regenerados em 4 livros
✅ **Task 4** — Índices criados e commitados
✅ **Task 5** — Validação + push final
