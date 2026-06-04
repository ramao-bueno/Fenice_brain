#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera INDEX.md por Titulo CF/88 + atualiza INDEX geral
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import yaml
from pathlib import Path
from datetime import datetime
from config_cf import OUTPUT_BASE, TITULO_MAPEAMENTO, LEI_NOME

PROJECT_ROOT = Path(__file__).parent.parent
CF_ROOT = PROJECT_ROOT / "FENICE bRain" / "00_CONSTITUIÇÃO_FEDERAL"

PLANALTO_ANCORA = {
    "TITULO-I":    "#titulo1",
    "TITULO-II":   "#titulo2",
    "TITULO-III":  "#titulo3",
    "TITULO-IV":   "#titulo4",
    "TITULO-V":    "#titulo5",
    "TITULO-VI":   "#titulo6",
    "TITULO-VII":  "#titulo7",
    "TITULO-VIII": "#titulo8",
    "TITULO-IX":   "#titulo9",
}
PLANALTO_BASE = "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"


def listar_artigos_titulo(titulo: str):
    pasta = OUTPUT_BASE / titulo
    if not pasta.exists():
        return []
    artigos = []
    for f in pasta.glob("Art. *.md"):
        try:
            num_str = f.stem.split(".")[1].strip().split(" ")[0]
            artigos.append((int(num_str), f.stem, f.name))
        except Exception:
            continue
    return sorted(artigos, key=lambda x: x[0])


def gerar_index_titulo(titulo: str) -> str:
    config = TITULO_MAPEAMENTO[titulo]
    nome = config["nome"]
    inicio, fim = config["range"]
    artigos = listar_artigos_titulo(titulo)
    ancora = PLANALTO_ANCORA.get(titulo, "")
    planalto_url = f"{PLANALTO_BASE}{ancora}"

    fm = {
        "titulo": f"INDEX — CF/88 {titulo}",
        "lei": LEI_NOME,
        "titulo_cf": titulo,
        "type": "index",
        "status": "vigente",
        "cf88": True,
        "tags": ["cf88", "constituicao", "index", titulo.lower()],
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    fm_str = yaml.dump(fm, allow_unicode=True,
                       default_flow_style=False, sort_keys=False)

    links = "\n".join(
        f"- [[Art. {num} — CF]] — Art. {num} CF/88"
        for num, stem, fname in artigos
    )

    # Navegacao entre titulos
    lista_titulos = list(TITULO_MAPEAMENTO.keys())
    idx = lista_titulos.index(titulo)
    nav_anterior = f"[[INDEX-{lista_titulos[idx-1]}]]" if idx > 0 else "—"
    nav_seguinte = f"[[INDEX-{lista_titulos[idx+1]}]]" if idx < len(lista_titulos)-1 else "—"

    corpo = f"""# CF/88 {titulo} — {nome}

**Lei:** {LEI_NOME}
**Artigos:** {inicio} a {fim}  ({len(artigos)} artigos)
**Planalto:** [Texto oficial]({planalto_url})

---

## Artigos

{links if links else "_Artigos ainda nao gerados — rode pipeline_cf.py --full_"}

---

## Navegacao

| Anterior | Proximo |
|----------|---------|
| {nav_anterior} | {nav_seguinte} |

## Links Gerais

- [[INDEX — CF/88 Completo]] — Indice geral da CF
- [[PIRÂMIDE-DE-KELSEN]] — Hierarquia normativa
- [[00_NAVIGATOR]] — Busca por codigo

---

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
        "cf88": True,
        "tags": ["cf88", "constituicao", "index", "fenice-brain"],
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    fm_str = yaml.dump(fm, allow_unicode=True,
                       default_flow_style=False, sort_keys=False)
    total = sum(contagens.values())

    linhas_titulos = "\n".join(
        f"- [[INDEX-{t}|{t} — {TITULO_MAPEAMENTO[t]['nome']}]] "
        f"(Arts. {TITULO_MAPEAMENTO[t]['range'][0]}–{TITULO_MAPEAMENTO[t]['range'][1]}, "
        f"{contagens.get(t, 0)} artigos)"
        for t in TITULO_MAPEAMENTO
    )

    corpo = f"""# CF/88 — INDICE COMPLETO

**Status:** VIGENTE  |  **Artigos gerados:** {total}/250  |  **Atualizado:** {datetime.now().strftime("%Y-%m-%d")}
**Planalto:** [Texto oficial]({PLANALTO_BASE})

---

## Metricas

| Metrica | Valor |
|---------|-------|
| **Total de artigos** | {total} |
| **Titulos** | 9 (I–IX) |
| **Emendas** | 127 (EC 1–127) |
| **Hierarquia Kelsen** | Nivel 1 — Norma Fundamental |

---

## Navegacao por Titulo

{linhas_titulos}

---

## Piramide de Kelsen

```
         [ CF/88 ] <- voce esta aqui
              |
   [Leis Complementares] [Emendas Constitucionais]
              |
  [CC]  [CP]  [CPC]  [CPP]  [CLT]  [CTN]  [CTB]
              |
        [Decretos / Portarias]
              |
          [Jurisprudencia STF/STJ]
```

- [[PIRAMIDE-DE-KELSEN]] — Canvas visual interativo
- [[00_NAVIGATOR]] — Busca por codigo (CF + CC + CP + CPC)
- [[Preambulo]] — Valores supremos

---

## Correlacoes Principais (Dataview)

```dataview
TABLE lei, artigo
FROM "FENICE bRain"
WHERE contains(base_constitucional, "CF Art.")
SORT lei ASC
LIMIT 20
```

---

**Fonte oficial:** [planalto.gov.br]({PLANALTO_BASE})
"""
    return f"---\n{fm_str}---\n\n{corpo}"


def main():
    sep = "=" * 60
    print(f"\n{sep}")
    print("GERADOR DE INDEXES CF/88")
    print(f"{sep}\n")

    contagens = {}
    for titulo in TITULO_MAPEAMENTO:
        artigos = listar_artigos_titulo(titulo)
        contagens[titulo] = len(artigos)

        conteudo = gerar_index_titulo(titulo)
        pasta = OUTPUT_BASE / titulo
        pasta.mkdir(parents=True, exist_ok=True)
        path = pasta / f"INDEX-{titulo}.md"
        path.write_text(conteudo, encoding="utf-8")
        print(f"  Criado: {path.name} ({len(artigos)} artigos)")

    # INDEX geral substitui o existente
    index_geral = gerar_index_geral(contagens)
    path_geral = CF_ROOT / "INDEX.md"
    path_geral.write_text(index_geral, encoding="utf-8")
    total = sum(contagens.values())
    print(f"\n  INDEX.md geral atualizado ({total} artigos total)")
    print(f"\n{sep}")
    print("INDEXES GERADOS COM SUCESSO!")
    print(f"{sep}\n")


if __name__ == "__main__":
    main()
