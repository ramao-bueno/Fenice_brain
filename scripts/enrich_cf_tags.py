#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enriquecedor de Tags CF/88

Adiciona tags estruturais aos artigos gerados:
  - paragrafo-1, paragrafo-2, ...  (§ 1º, § 2º, ...)
  - inciso-i, inciso-ii, ...       (I -, II -, ...)
  - alinea-a, alinea-b, ...        (a), b), ...)
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import re
import yaml
from pathlib import Path


class EnriquecedorTagsCF:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.tags_adicionadas = 0

    def extrair_paragrafos(self, texto: str):
        tags = [f"paragrafo-{m}" for m in re.findall(r"§\s*(\d+)", texto)]
        if re.search(r"[Pp]ar[áa]grafo\s+[úu]nico", texto):
            if "paragrafo-unico" not in tags:
                tags.append("paragrafo-unico")
        return tags

    def extrair_incisos(self, texto: str):
        romanos = [
            "I","II","III","IV","V","VI","VII","VIII","IX","X",
            "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX",
            "XXI","XXII","XXIII","XXIV","XXV","XXVI","XXVII","XXVIII",
        ]
        return [
            f"inciso-{r.lower()}"
            for r in romanos
            if re.search(rf"(?:^|\n|\s){r}\s*[-–—\.]|inciso\s+{r}", texto, re.IGNORECASE)
        ]

    def extrair_alineas(self, texto: str):
        return [
            f"alinea-{a}"
            for a in "abcdefghij"
            if re.search(rf"\b{a}\)\s|alínea\s+{a}\b", texto, re.IGNORECASE)
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

            novas = (
                self.extrair_paragrafos(corpo)
                + self.extrair_incisos(corpo)
                + self.extrair_alineas(corpo)
            )

            if novas:
                fm.setdefault("tags", [])
                adicionadas = 0
                for tag in novas:
                    if tag not in fm["tags"]:
                        fm["tags"].append(tag)
                        adicionadas += 1

                if adicionadas > 0:
                    fm_novo = yaml.dump(fm, allow_unicode=True,
                                        default_flow_style=False, sort_keys=False)
                    path.write_text(f"---\n{fm_novo}---\n\n{corpo}", encoding="utf-8")
                    self.tags_adicionadas += adicionadas
                    return True
        except Exception as e:
            print(f"  Erro em {path.name}: {e}")
        return False

    def processar_todos(self, limit=None):
        sep = "=" * 60
        print(f"\n{sep}")
        print("ENRIQUECEDOR TAGS CF/88")
        print(f"{sep}\n")

        arquivos = [
            a for a in self.base_path.rglob("Art. *.md")
            if "INDEX" not in a.name
        ]
        if limit:
            arquivos = arquivos[:limit]

        print(f"  Processando {len(arquivos)} artigos...\n")

        enriquecidos = 0
        for i, arq in enumerate(arquivos, 1):
            if self.enriquecer_arquivo(arq):
                enriquecidos += 1
            if i % 50 == 0 or i == len(arquivos):
                pct = (i / len(arquivos)) * 100
                print(f"  {i:>4d}/{len(arquivos)} ({pct:.0f}%)")

        print(f"\n{sep}")
        print("ENRIQUECIMENTO CONCLUIDO!")
        print(f"{sep}")
        print(f"\n  Artigos enriquecidos : {enriquecidos}")
        print(f"  Tags adicionadas     : {self.tags_adicionadas}")
        print(f"  Tags: paragrafo-N, inciso-i/ii/..., alinea-a/b/...\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enriquecedor Tags CF/88")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    base = Path(
        r"C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech"
        r"\Fenice brain\FENICE bRain\00_CONSTITUIÇÃO_FEDERAL\Artigos"
    )
    e = EnriquecedorTagsCF(base)
    e.processar_todos(limit=None if args.full else args.limit)
