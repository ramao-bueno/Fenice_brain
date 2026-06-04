# CF/88 + Navigator Kelseniano — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Desmembrar a Constituição Federal de 1988 artigo por artigo no vault Fenice Brain, com Navigator universal por código e Canvas visual da Pirâmide de Kelsen integrada ao Planalto.gov.br.

**Architecture:** Pipeline Python reutiliza CPCExtractor com override de TITULO_MAPEAMENTO; MarkdownGeneratorCF gera template CF-específico com planalto_url e base_constitucional; Navigator usa Obsidian Bases + Templater para busca interativa; Canvas Kelsen é o hub visual do ordenamento jurídico.

**Tech Stack:** Python 3 (pdfplumber, yaml, re, pathlib), Obsidian Bases (.base), Obsidian Canvas (.canvas), Templater plugin, QuickAdd plugin, Dataview plugin.

---

## Mapeamento de Arquivos

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `scripts/config_cf.py` | Criar | Caminhos + TITULO_MAPEAMENTO + constantes CF |
| `scripts/markdown_generator_cf.py` | Criar | Template Markdown CF com planalto_url |
| `scripts/pipeline_cf.py` | Criar | Orquestra extração PDF → artigos .md |
| `scripts/enrich_cf_tags.py` | Criar | Adiciona paragrafo-N, inciso-i, alinea-a |
| `scripts/generate_cf_indexes.py` | Criar | INDEX por Título + INDEX geral CF |
| `FENICE bRain/00_NAVIGATOR.base` | Criar | Obsidian Bases multi-código |
| `FENICE bRain/00_NAVIGATOR.md` | Criar | Dashboard com bases embutidas + dataview |
| `FENICE bRain/05_Templates/buscar-artigo.md` | Criar | Templater diálogo 2 passos |
| `FENICE bRain/00_CONSTITUIÇÃO_FEDERAL/PIRÂMIDE-DE-KELSEN.canvas` | Substituir | Canvas visual hierarquia Kelsen |

---

## Task 1: config_cf.py

**Files:**
- Create: `scripts/config_cf.py`

- [ ] **Criar config_cf.py com TITULO_MAPEAMENTO**

```python
# scripts/config_cf.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PDF_PATH = PROJECT_ROOT / "FENICE bRain" / "00_CONSTITUIÇÃO_FEDERAL" / "Constituição.pdf"
OUTPUT_BASE = PROJECT_ROOT / "FENICE bRain" / "00_CONSTITUIÇÃO_FEDERAL" / "Artigos"

TITULO_MAPEAMENTO = {
    "TITULO-I":   {"range": (1,   4),   "nome": "Dos Princípios Fundamentais"},
    "TITULO-II":  {"range": (5,   17),  "nome": "Dos Direitos e Garantias Fundamentais"},
    "TITULO-III": {"range": (18,  43),  "nome": "Da Organização do Estado"},
    "TITULO-IV":  {"range": (44,  135), "nome": "Da Organização dos Poderes"},
    "TITULO-V":   {"range": (136, 144), "nome": "Da Defesa do Estado e das Instituições Democráticas"},
    "TITULO-VI":  {"range": (145, 169), "nome": "Da Tributação e do Orçamento"},
    "TITULO-VII": {"range": (170, 192), "nome": "Da Ordem Econômica e Financeira"},
    "TITULO-VIII":{"range": (193, 232), "nome": "Da Ordem Social"},
    "TITULO-IX":  {"range": (233, 250), "nome": "Das Disposições Constitucionais Gerais"},
}

TAGS_PADRAO = ["cf88", "constituicao", "vigente"]
LEI_NOME = "Constituição Federal de 1988"
PLANALTO_BASE_URL = "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"

TEMA_POR_TITULO = {
    "TITULO-I":   "principios-fundamentais",
    "TITULO-II":  "direitos-fundamentais",
    "TITULO-III": "organizacao-estado",
    "TITULO-IV":  "organizacao-poderes",
    "TITULO-V":   "defesa-estado",
    "TITULO-VI":  "tributacao",
    "TITULO-VII": "ordem-economica",
    "TITULO-VIII":"ordem-social",
    "TITULO-IX":  "disposicoes-gerais",
}
```

- [ ] **Validar**

```bash
cd "C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\scripts"
python config_cf.py
```
Esperado: sem erros (arquivo importável).

- [ ] **Commit**
```bash
git add scripts/config_cf.py
git commit -m "feat: config CF/88 com TITULO_MAPEAMENTO e planalto_url"
```

---

## Task 2: markdown_generator_cf.py

**Files:**
- Create: `scripts/markdown_generator_cf.py`

- [ ] **Criar gerador com template CF**

```python
# scripts/markdown_generator_cf.py
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_cf import (TAGS_PADRAO, LEI_NOME, TITULO_MAPEAMENTO,
                       PLANALTO_BASE_URL, TEMA_POR_TITULO)

class MarkdownGeneratorCF:
    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, titulo: str) -> str:
        num = artigo["numero"]
        titulo_nome = TITULO_MAPEAMENTO.get(titulo, {}).get("nome", titulo)
        tema = TEMA_POR_TITULO.get(titulo, "constituicao")
        planalto_url = f"{PLANALTO_BASE_URL}#art{num}"

        tags = TAGS_PADRAO.copy()
        tags += [titulo.lower().replace("_", "-"), f"art-{num}", tema]

        frontmatter = {
            "artigo": str(num),
            "lei": LEI_NOME,
            "titulo_cf": titulo,
            "parte": titulo_nome,
            "status": "vigente",
            "cf88": True,
            "emendas": [],
            "planalto_url": planalto_url,
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Redação a ser conferida no Planalto]")
        titulo_artigo = artigo.get("titulo", f"Art. {num}")

        corpo = f"""# CF/88 Art. {num} — {titulo_artigo}

**Lei:** {LEI_NOME}
**Título:** {titulo} — {titulo_nome}
**Status:** ✅ VIGENTE
**🔗 Planalto:** [Texto oficial]({planalto_url})

---

## 📋 REDAÇÃO LEGAL

> {redacao}

---

## 🔍 ANÁLISE TÉCNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Sujeito** | A quem se dirige |
| **Objeto** | O que regula |
| **Sanção/Efeito** | Consequência jurídica |

---

## 🔗 ARTIGOS CORRELATOS

### Mesma CF
- [[Art. {max(1, num-1)} — CF]] — artigo anterior
- [[Art. {num+1} — CF]] — artigo seguinte

### Legislação Derivada
[Leis ordinárias que regulamentam este artigo]

---

## ⚖️ JURISPRUDÊNCIA STF

### Teses e Precedentes
[Precedentes do STF sobre este artigo]

---

## 📜 EMENDAS CONSTITUCIONAIS

[ECs que modificaram este artigo — verificar no Planalto]

---

## 🕸️ RELACIONAMENTOS (Dataview)

```dataview
LIST FROM "FENICE bRain/02_DIREITO_CIVIL" 
  OR "FENICE bRain/03_CÓDIGO_PENAL"
  OR "FENICE bRain/01_CÓDIGO_PROCESSO_CIVIL"
WHERE contains(base_constitucional, "CF Art. {num}")
```

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
**Fonte oficial:** [planalto.gov.br]({planalto_url})
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_artigo(self, artigo: Dict, conteudo: str, titulo: str) -> Path:
        pasta = self.output_base / titulo
        pasta.mkdir(parents=True, exist_ok=True)

        titulo_limpo = artigo.get("titulo", f"Art. {artigo['numero']}")
        titulo_limpo = titulo_limpo.replace("/", "-").replace("\\", "-")[:60]
        filename = f"Art. {artigo['numero']} — CF.md"

        filepath = pasta / filename
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"❌ Erro ao salvar {filename}: {e}")
            return None
```

- [ ] **Commit**
```bash
git add scripts/markdown_generator_cf.py
git commit -m "feat: gerador Markdown CF/88 com planalto_url e dataview correlatos"
```

---

## Task 3: pipeline_cf.py

**Files:**
- Create: `scripts/pipeline_cf.py`

- [ ] **Criar pipeline_cf.py**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline CF: PDF Constituição Federal → Markdown estruturado

Uso:
    python pipeline_cf.py              # 5 primeiros artigos (teste)
    python pipeline_cf.py --full       # Todos os artigos
    python pipeline_cf.py --limit 20   # Primeiros 20
"""
import sys
from pathlib import Path
from config_cf import PDF_PATH, OUTPUT_BASE, TITULO_MAPEAMENTO, LEI_NOME

from pdf_extractor import CPCExtractor
import pdf_extractor as px_module
px_module.LIVRO_MAPEAMENTO = TITULO_MAPEAMENTO

from markdown_generator_cf import MarkdownGeneratorCF


def pipeline_cf(limit=None):
    print("\n" + "="*60)
    print("🏛️  PIPELINE CF/88: PDF → Markdown")
    print("="*60 + "\n")

    print("📖 ETAPA 1: Extraindo artigos do PDF...")
    extractor = CPCExtractor(str(PDF_PATH))
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído!")
        return False

    if limit:
        artigos = artigos[:limit]
        print(f"⚠️  Limitado a {limit} artigos para teste")

    print(f"✅ {len(artigos)} artigos prontos\n")

    print("📝 ETAPA 2: Gerando notas Markdown...")
    gerador = MarkdownGeneratorCF(OUTPUT_BASE)

    salvos = 0
    erros = 0
    for i, art in enumerate(artigos, 1):
        try:
            conteudo = gerador.gerar_nota_artigo(art, art["livro"])
            filepath = gerador.salvar_artigo(art, conteudo, art["livro"])
            if filepath:
                salvos += 1
            if i % 50 == 0 or i == len(artigos):
                print(f"   ✅ {i:>4d}/{len(artigos)} ({(i/len(artigos)*100):.0f}%)")
        except Exception as e:
            erros += 1
            continue

    print(f"\n{'='*60}")
    print(f"✅ PIPELINE CF/88 CONCLUÍDO!")
    print(f"   • Salvos: {salvos} | Erros: {erros}")
    print(f"   • Saída: {OUTPUT_BASE}\n")
    return salvos > 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    sucesso = pipeline_cf(limit=None if args.full else args.limit)
    sys.exit(0 if sucesso else 1)
```

- [ ] **Testar com 5 artigos**
```bash
cd scripts && python pipeline_cf.py --limit 5
```
Esperado: `✅ 5 artigos salvos` em `FENICE bRain/00_CONSTITUIÇÃO_FEDERAL/Artigos/TITULO-I/`

- [ ] **Rodar completo**
```bash
python pipeline_cf.py --full
```
Esperado: ~200-250 artigos salvos.

- [ ] **Commit**
```bash
git add scripts/pipeline_cf.py
git commit -m "feat: pipeline CF/88 PDF → 250 artigos Markdown"
```

---

## Task 4: enrich_cf_tags.py

**Files:**
- Create: `scripts/enrich_cf_tags.py`

- [ ] **Criar enriquecedor de tags CF**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enriquecedor de Tags CF: Adiciona paragrafo-N, inciso-i, alinea-a
"""
import re
import yaml
from pathlib import Path

class EnriquecedorTagsCF:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.tags_adicionadas = 0

    def extrair_paragrafos(self, texto: str):
        return [f"paragrafo-{m}" for m in re.findall(r"§\s*(\d+)", texto)]

    def extrair_incisos(self, texto: str):
        romanos = ["I","II","III","IV","V","VI","VII","VIII","IX","X",
                   "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX",
                   "XXI","XXII","XXIII","XXIV","XXV","XXVI","XXVII","XXVIII"]
        return [
            f"inciso-{r.lower()}"
            for r in romanos
            if re.search(rf"\b{r}\s*[—\-\.]|inciso\s+{r}", texto, re.IGNORECASE)
        ]

    def extrair_alineas(self, texto: str):
        return [
            f"alinea-{a}"
            for a in "abcdefgh"
            if re.search(rf"{a}\)\s|alínea\s+{a}", texto, re.IGNORECASE)
        ]

    def enriquecer_arquivo(self, path: Path) -> bool:
        try:
            conteudo = path.read_text(encoding="utf-8")
            match = re.match(r"^---\n([\s\S]*?)\n---\n\n([\s\S]*)", conteudo)
            if not match:
                return False
            fm = yaml.safe_load(match.group(1))
            if not fm:
                return False
            corpo = match.group(2)

            novas = (self.extrair_paragrafos(corpo)
                     + self.extrair_incisos(corpo)
                     + self.extrair_alineas(corpo))

            if novas:
                fm.setdefault("tags", [])
                for tag in novas:
                    if tag not in fm["tags"]:
                        fm["tags"].append(tag)

                fm_novo = yaml.dump(fm, allow_unicode=True,
                                    default_flow_style=False, sort_keys=False)
                path.write_text(f"---\n{fm_novo}---\n\n{corpo}", encoding="utf-8")
                self.tags_adicionadas += len(novas)
                return True
        except Exception as e:
            print(f"❌ {path.name}: {e}")
        return False

    def processar_todos(self, limit=None):
        print("\n" + "="*60)
        print("🔧  ENRIQUECEDOR TAGS CF/88")
        print("="*60)

        arquivos = [a for a in self.base_path.rglob("*.md")
                    if "INDEX" not in a.name]
        if limit:
            arquivos = arquivos[:limit]

        enriquecidos = 0
        for i, arq in enumerate(arquivos, 1):
            if self.enriquecer_arquivo(arq):
                enriquecidos += 1
            if i % 50 == 0 or i == len(arquivos):
                print(f"   ✅ {i}/{len(arquivos)} ({(i/len(arquivos)*100):.0f}%)")

        print(f"\n✅ {enriquecidos} artigos enriquecidos | {self.tags_adicionadas} tags adicionadas\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    base = Path(r"C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\00_CONSTITUIÇÃO_FEDERAL\Artigos")
    e = EnriquecedorTagsCF(base)
    e.processar_todos(limit=None if args.full else args.limit)
```

- [ ] **Rodar enriquecedor**
```bash
python enrich_cf_tags.py --full
```

- [ ] **Commit**
```bash
git add scripts/enrich_cf_tags.py
git commit -m "feat: enriquecedor tags CF paragrafo/inciso/alinea"
```

---

## Task 5: generate_cf_indexes.py

**Files:**
- Create: `scripts/generate_cf_indexes.py`

- [ ] **Criar gerador de INDEXes por Título**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera INDEX.md por Título CF + atualiza INDEX geral"""
import yaml
from pathlib import Path
from datetime import datetime
from config_cf import OUTPUT_BASE, TITULO_MAPEAMENTO, LEI_NOME

PROJECT_ROOT = Path(__file__).parent.parent
CF_ROOT = PROJECT_ROOT / "FENICE bRain" / "00_CONSTITUIÇÃO_FEDERAL"

PLANALTO_URLS = {
    "TITULO-I":   "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo1",
    "TITULO-II":  "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo2",
    "TITULO-III": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo3",
    "TITULO-IV":  "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo4",
    "TITULO-V":   "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo5",
    "TITULO-VI":  "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo6",
    "TITULO-VII": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo7",
    "TITULO-VIII":"https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo8",
    "TITULO-IX":  "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#titulo9",
}


def listar_artigos_titulo(titulo: str):
    pasta = OUTPUT_BASE / titulo
    if not pasta.exists():
        return []
    artigos = []
    for f in sorted(pasta.glob("Art. *.md"),
                    key=lambda x: int(x.stem.split(".")[1].strip().split(" ")[0])):
        num = f.stem.split(".")[1].strip().split(" ")[0]
        artigos.append((int(num), f.stem, f.name))
    return artigos


def gerar_index_titulo(titulo: str) -> str:
    config = TITULO_MAPEAMENTO[titulo]
    nome = config["nome"]
    inicio, fim = config["range"]
    artigos = listar_artigos_titulo(titulo)
    planalto_url = PLANALTO_URLS.get(titulo, "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm")

    fm = {
        "titulo": f"INDEX — CF/88 {titulo}",
        "lei": LEI_NOME,
        "titulo_cf": titulo,
        "type": "index",
        "status": "vigente",
        "tags": ["cf88", "constituicao", "index", titulo.lower()],
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    links = "\n".join(
        f"- [[Art. {num} — CF]] — Art. {num}"
        for num, stem, fname in artigos
    )

    corpo = f"""# 📑 {titulo} — {nome}

**Lei:** {LEI_NOME}
**Artigos:** {inicio} a {fim} ({len(artigos)} artigos)
**🔗 Planalto:** [Texto oficial]({planalto_url})

---

## Artigos

{links if links else "_Artigos ainda não gerados_"}

---

## Links
- [[INDEX — CF/88]] — Índice geral
- [[PIRÂMIDE-DE-KELSEN]] — Hierarquia normativa
- [[00_NAVIGATOR]] — Busca por código

**Atualizado:** {datetime.now().strftime("%Y-%m-%d")}
"""
    return f"---\n{fm_str}---\n\n{corpo}"


def gerar_index_geral(contagens: dict) -> str:
    fm = {
        "titulo": "INDEX — CF/88 Completo",
        "lei": LEI_NOME,
        "type": "index",
        "status": "vigente",
        "version": "3.0",
        "tags": ["cf88", "constituicao", "index", "fenice-brain"],
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    total = sum(contagens.values())
    linhas_titulos = "\n".join(
        f"- [[INDEX-{t}|{t} — {TITULO_MAPEAMENTO[t]['nome']}]] ({contagens.get(t,0)} artigos)"
        for t in TITULO_MAPEAMENTO
    )

    corpo = f"""# 🏛️ CONSTITUIÇÃO FEDERAL DE 1988 — ÍNDICE COMPLETO

**Status:** ✅ Vigente | **Artigos gerados:** {total} | **Atualizado:** {datetime.now().strftime("%Y-%m-%d")}

---

## 📊 Métricas

| Métrica | Valor |
|---------|-------|
| **Total de artigos** | {total} |
| **Títulos** | 9 + ADCT |
| **Emendas** | 127 (EC 1–127) |
| **Hierarquia Kelsen** | Nível 1 — Norma Fundamental |

---

## 📑 Navegação por Título

{linhas_titulos}

---

## 🔗 Navegação Rápida

- [[PIRÂMIDE-DE-KELSEN]] — Hierarquia normativa completa
- [[00_NAVIGATOR]] — Busca por código (CF + CC + CP + CPC)
- [[Preâmbulo]] — Valores supremos

---

## 📊 Pirâmide de Kelsen

```
         [ CF/88 ] ← você está aqui
              ↓
   [Leis Complementares] [Emendas Constitucionais]
              ↓
  [CC]   [CP]   [CPC]   [CPP]   [CLT]   [CTN]
              ↓
        [Decretos / Portarias]
              ↓
          [Jurisprudência STF/STJ]
```

---

**Fonte oficial:** [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)
"""
    return f"---\n{fm_str}---\n\n{corpo}"


def main():
    print("\n" + "="*60)
    print("📑  GERADOR DE INDEXES CF/88")
    print("="*60 + "\n")

    contagens = {}
    for titulo in TITULO_MAPEAMENTO:
        artigos = listar_artigos_titulo(titulo)
        contagens[titulo] = len(artigos)

        conteudo = gerar_index_titulo(titulo)
        pasta = OUTPUT_BASE / titulo
        pasta.mkdir(parents=True, exist_ok=True)
        path = pasta / f"INDEX-{titulo}.md"
        path.write_text(conteudo, encoding="utf-8")
        print(f"   ✅ {path.name} ({len(artigos)} artigos)")

    index_geral = gerar_index_geral(contagens)
    path_geral = CF_ROOT / "INDEX.md"
    path_geral.write_text(index_geral, encoding="utf-8")
    print(f"\n   ✅ INDEX.md geral atualizado ({sum(contagens.values())} artigos total)")


if __name__ == "__main__":
    main()
```

- [ ] **Rodar**
```bash
python generate_cf_indexes.py
```

- [ ] **Commit**
```bash
git add scripts/generate_cf_indexes.py
git commit -m "feat: gera INDEX por Título CF/88 + INDEX geral"
```

---

## Task 6: 00_NAVIGATOR.base

**Files:**
- Create: `FENICE bRain/00_NAVIGATOR.base`

- [ ] **Criar Obsidian Bases multi-código**

```yaml
filters:
  and:
    - 'artigo != ""'
    - 'status == "vigente"'

formulas:
  codigo_icon: 'if(file.hasTag("cf88"), "🏛️ CF", if(file.hasTag("cc"), "📘 CC", if(file.hasTag("direito-penal"), "⚖️ CP", if(file.hasTag("cpc"), "📋 CPC", "📄 Outro"))))'
  num_artigo: 'if(artigo, artigo, "")'

properties:
  formula.codigo_icon:
    displayName: "Código"
  formula.num_artigo:
    displayName: "Artigo"
  lei:
    displayName: "Lei"

views:
  - type: table
    name: "🔍 Busca Universal"
    order:
      - formula.codigo_icon
      - formula.num_artigo
      - file.name
      - lei
      - status

  - type: table
    name: "🏛️ CF/88 — Constituição"
    filters:
      and:
        - file.hasTag("cf88")
    groupBy:
      property: titulo_cf
      direction: ASC
    order:
      - formula.num_artigo
      - file.name
      - titulo_cf

  - type: table
    name: "📘 Código Civil"
    filters:
      and:
        - file.hasTag("cc")
    groupBy:
      property: livro
      direction: ASC
    order:
      - formula.num_artigo
      - file.name

  - type: table
    name: "⚖️ Código Penal"
    filters:
      and:
        - file.hasTag("direito-penal")
    order:
      - formula.num_artigo
      - file.name

  - type: table
    name: "📋 CPC"
    filters:
      and:
        - file.hasTag("cpc")
    order:
      - formula.num_artigo
      - file.name

  - type: cards
    name: "📊 Todos por Código"
    order:
      - formula.codigo_icon
      - file.name
      - formula.num_artigo
```

- [ ] **Commit**
```bash
git add "FENICE bRain/00_NAVIGATOR.base"
git commit -m "feat: navigator Obsidian Bases multi-código CF/CC/CP/CPC"
```

---

## Task 7: 00_NAVIGATOR.md

**Files:**
- Create: `FENICE bRain/00_NAVIGATOR.md`

- [ ] **Criar dashboard navigator**

```markdown
---
tags: [fenice-brain, navigator, index, cf88, cc, cpc, direito-penal]
type: navigator
created: 2026-06-04
---

# 🔍 FENICE BRAIN — NAVIGATOR JURÍDICO

> **Como usar:** `Ctrl+P` → `Buscar Artigo` para diálogo interativo por código + número.
> Ou navegue pela base abaixo filtrando diretamente nas colunas.

---

## 📊 NAVEGAÇÃO POR BASE

![[00_NAVIGATOR.base]]

---

## 🏔️ HIERARQUIA KELSENIANA

```
🏛️ CF/88 → [[INDEX — CF/88 Completo]]
    ↓
📘 Código Civil  → [[INDEX Código Civil]]
⚖️ Código Penal  → [[INDEX Direito Penal]]
📋 CPC           → [[INDEX CPC]]
```

---

## ⚡ ACESSO RÁPIDO POR CÓDIGO

| Código | Artigos | Índice | Planalto |
|--------|---------|--------|---------|
| 🏛️ CF/88 | Arts. 1-250 | [[INDEX — CF/88 Completo]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm) |
| 📘 Código Civil | Arts. 1-2046 | [[INDEX Código Civil]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) |
| ⚖️ Código Penal | Arts. 121+ | [[INDEX — Direito Penal]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm) |
| 📋 CPC | Arts. 1-1072 | [[INDEX CPC]] | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm) |

---

## 🔎 ARTIGOS MAIS ACESSADOS

```dataview
TABLE lei, artigo, file.mtime as "Último acesso"
FROM "FENICE bRain"
WHERE artigo != ""
SORT file.mtime DESC
LIMIT 10
```

---

## 📈 TOTAIS POR CÓDIGO

```dataview
TABLE length(rows) as "Total de Artigos"
FROM "FENICE bRain"
WHERE artigo != ""
GROUP BY lei
```

---

**Atualizado:** 2026-06-04
```

- [ ] **Commit**
```bash
git add "FENICE bRain/00_NAVIGATOR.md"
git commit -m "feat: dashboard navigator com bases embutidas e dataview"
```

---

## Task 8: buscar-artigo.md (Templater)

**Files:**
- Create: `FENICE bRain/05_Templates/buscar-artigo.md`

- [ ] **Criar template Templater interativo**

```markdown
<%*
// FENICE BRAIN — Buscar Artigo
// Uso: Ctrl+P → "Buscar Artigo"

const CODIGOS = {
  "🏛️ CF/88 — Constituição Federal": { tag: "cf88", pasta: "00_CONSTITUIÇÃO_FEDERAL/Artigos", prefixo: "CF" },
  "📘 Código Civil (CC)": { tag: "cc", pasta: "02_DIREITO_CIVIL/Artigos", prefixo: "CC" },
  "⚖️ Código Penal (CP)": { tag: "direito-penal", pasta: "03_CÓDIGO_PENAL", prefixo: "CP" },
  "📋 CPC — Processo Civil": { tag: "cpc", pasta: "01_CÓDIGO_PROCESSO_CIVIL", prefixo: "CPC" },
};

// Passo 1: selecionar código
const codigoNome = await tp.system.suggester(
  Object.keys(CODIGOS),
  Object.keys(CODIGOS),
  true,
  "1. Selecione o Código:"
);
if (!codigoNome) { tR = ""; return; }

const config = CODIGOS[codigoNome];

// Passo 2: número do artigo
const numArtigo = await tp.system.prompt(
  `2. Número do Artigo (${codigoNome.split("—")[0].trim()}):`,
  "",
  true
);
if (!numArtigo) { tR = ""; return; }

// Buscar arquivo no vault
const allFiles = app.vault.getFiles();
const found = allFiles.find(f => {
  if (!f.path.includes(config.pasta)) return false;
  const meta = app.metadataCache.getFileCache(f)?.frontmatter;
  return meta && String(meta.artigo) === String(numArtigo).trim();
});

if (found) {
  // Abre o arquivo encontrado
  const leaf = app.workspace.getLeaf(false);
  await leaf.openFile(found);
  new Notice(`✅ Art. ${numArtigo} (${codigoNome.split("—")[0].trim()}) aberto!`);
} else {
  new Notice(`⚠️ Art. ${numArtigo} não encontrado em ${codigoNome}. Verifique se o pipeline foi executado.`);
}

tR = ""; // Template não insere conteúdo — só navega
%>
```

- [ ] **Configurar QuickAdd** (instrução para o usuário)
  1. Abrir Obsidian → Settings → QuickAdd
  2. Criar novo macro "Buscar Artigo"
  3. Tipo: Template
  4. Selecionar: `05_Templates/buscar-artigo.md`
  5. Ativar "Add to Command Palette"
  6. Definir atalho: `Ctrl+Shift+B`

- [ ] **Commit**
```bash
git add "FENICE bRain/05_Templates/buscar-artigo.md"
git commit -m "feat: template Templater buscar-artigo com diálogo interativo"
```

---

## Task 9: PIRÂMIDE-DE-KELSEN.canvas

**Files:**
- Replace: `FENICE bRain/00_CONSTITUIÇÃO_FEDERAL/PIRÂMIDE-DE-KELSEN.canvas`

- [ ] **Criar Canvas Kelsen com hierarquia visual e links para todos os INDEXes**

(Canvas JSON gerado com nós file para cada INDEX existente + texto descritivo por nível)

- [ ] **Commit**
```bash
git add "FENICE bRain/00_CONSTITUIÇÃO_FEDERAL/PIRÂMIDE-DE-KELSEN.canvas"
git commit -m "feat: canvas Pirâmide de Kelsen com links para todos os códigos"
```

---

## Task 10: Execução e validação final

- [ ] Confirmar artigos gerados: `ls "FENICE bRain/00_CONSTITUIÇÃO_FEDERAL/Artigos/TITULO-II/"` → Art. 5, 6, 7... presentes
- [ ] Abrir Obsidian → `00_NAVIGATOR.base` → verificar views por código
- [ ] Testar `Ctrl+P → Buscar Artigo` → selecionar CF/88 → digitar 5 → abre Art. 5
- [ ] Verificar backlinks no Art. 5 → mostrar relacionamentos com CC, CP
- [ ] Abrir Canvas Kelsen → confirmar todos os links ativos
- [ ] **Commit final**
```bash
git add -A
git commit -m "feat: CF/88 completo + Navigator + Canvas Kelsen no Fenice Brain"
```
