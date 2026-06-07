#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de leis nacionais de Direito Internacional (HTML local já salvo do Planalto)

Reaproveita o padrão de regex "Art. N" validado em cc/cpc_planalto_extractor —
mas lê o HTML já em cache local (não baixa), pois os arquivos já foram salvos
manualmente em 08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/.
"""
import re
from pathlib import Path
from typing import List, Dict


class LeiNacionalLocalExtractor:
    """Extrai artigos de uma lei nacional a partir de HTML local (padrão Art. N)."""

    def __init__(self, html_path: Path, categoria: str, max_artigo: int):
        self.html_path = Path(html_path)
        self.categoria = categoria
        self.max_artigo = max_artigo
        self.artigos: List[Dict] = []

    def _ler_html(self) -> str:
        # HTMLs salvos do Planalto vêm em windows-1252
        try:
            return self.html_path.read_text(encoding="windows-1252", errors="replace")
        except UnicodeError:
            return self.html_path.read_text(encoding="utf-8", errors="replace")

    def _limpar_html(self, html: str) -> str:
        limpo = re.sub(r"<[^>]+>", " ", html)
        limpo = limpo.replace("&nbsp;", " ").replace("&amp;", "&")
        limpo = re.sub(r"[ \t]+", " ", limpo)
        limpo = re.sub(r"\n{3,}", "\n\n", limpo)
        return limpo.strip()

    def extract_articles(self) -> List[Dict]:
        if not self.html_path.exists():
            print(f"  ERRO: arquivo não encontrado: {self.html_path}")
            return []

        html = self._ler_html()
        texto = self._limpar_html(html)

        marcadores = list(re.finditer(
            r"(?:^|\n)\s*(Art\.\s*(\d+(?:\.\d+)?)\s*[ºo°]?)",
            texto, re.MULTILINE
        ))
        print(f"  Encontrados {len(marcadores)} marcadores de artigo em {self.html_path.name}")

        vistos = set()
        for i, match in enumerate(marcadores):
            try:
                num_str = match.group(2).replace(".", "")
                num = int(num_str)
                if num in vistos or num > self.max_artigo:
                    continue
                vistos.add(num)

                inicio = match.start()
                fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else inicio + 5000
                bloco = texto[inicio:fim].strip()
                bloco = re.sub(r"\s+", " ", bloco).strip()

                sem_prefixo = re.sub(
                    r"^Art\.\s*\d+(?:\.\d+)?\s*[ºo°]?\s*[-–—\.]?\s*", "", bloco
                ).strip()

                match_titulo = re.match(r"^([^.:;]{5,120}[.:;]?)", sem_prefixo)
                titulo = match_titulo.group(1).strip().rstrip(".:") if match_titulo else sem_prefixo[:100]

                redacao = sem_prefixo[:600].strip()
                if len(sem_prefixo) > 600:
                    redacao += "..."

                self.artigos.append({
                    "numero": num,
                    "titulo": titulo[:120],
                    "redacao": redacao,
                    "categoria": self.categoria,
                    "texto_completo": sem_prefixo[:3000],
                })
            except Exception:
                continue

        self.artigos.sort(key=lambda x: x["numero"])
        print(f"  {len(self.artigos)} artigos extraídos de {self.html_path.name}")
        return self.artigos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, str(Path(__file__).parent))
    from config_direito_internacional import LEIS_NACIONAIS

    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"\n=== {sigla} — {cfg['nome']} ===")
        ext = LeiNacionalLocalExtractor(cfg["arquivo"], cfg["categoria"], cfg["max_artigo"])
        arts = ext.extract_articles()
        for a in arts[:2]:
            print(f"  Art. {a['numero']}: {a['titulo'][:70]}")
