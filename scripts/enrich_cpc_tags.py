#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enriquecedor de Tags CPC: Adiciona tags específicas para parágrafos, incisos e alíneas

Busca por padrões no conteúdo do artigo e adiciona tags como:
- paragrafo-1, paragrafo-2, etc (§1, §2)
- inciso-i, inciso-ii, inciso-iii, inciso-iv (I, II, III, IV)
- alinea-a, alinea-b, alinea-c (a, b, c)
"""

import re
import yaml
from pathlib import Path
from typing import List

class EnriquecedorTagsCPC:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.artigos_processados = 0
        self.tags_adicionadas = 0

    def extrair_paragrafos(self, redacao: str) -> List[str]:
        """Extrai números de parágrafos (§1, §2, etc)"""
        pattern = r"§\s*(\d+)"
        matches = re.findall(pattern, redacao)
        return [f"paragrafo-{m}" for m in matches]

    def extrair_incisos(self, redacao: str) -> List[str]:
        """Extrai números de incisos romanos (I, II, III, IV)"""
        incisos_romanos = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        tags = []

        for inciso in incisos_romanos:
            # Procura por padrões como "I —", "II.", "inciso I", etc
            if re.search(rf"\b{inciso}\s*[—\-\.]|inciso\s+{inciso}", redacao, re.IGNORECASE):
                tags.append(f"inciso-{inciso.lower()}")

        return tags

    def extrair_alineas(self, redacao: str) -> List[str]:
        """Extrai alíneas (a), b), c), etc)"""
        alineas = ["a", "b", "c", "d", "e", "f", "g", "h"]
        tags = []

        for alinea in alineas:
            if re.search(rf"{alinea}\)\s|alínea\s+{alinea}", redacao, re.IGNORECASE):
                tags.append(f"alinea-{alinea}")

        return tags

    def enriquecer_arquivo(self, arquivo_path: Path) -> bool:
        """Enriquece um arquivo com tags adicionais"""
        try:
            with open(arquivo_path, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Separa frontmatter do corpo
            match = re.match(r"^---\n([\s\S]*?)\n---\n\n([\s\S]*)", conteudo)
            if not match:
                return False

            fm_str = match.group(1)
            corpo = match.group(2)

            # Parse YAML
            frontmatter = yaml.safe_load(fm_str)
            if not frontmatter:
                return False

            # Extrai tags novas
            tags_novas = []
            tags_novas.extend(self.extrair_paragrafos(corpo))
            tags_novas.extend(self.extrair_incisos(corpo))
            tags_novas.extend(self.extrair_alineas(corpo))

            # Adiciona tags se houver novas
            if tags_novas:
                if "tags" not in frontmatter:
                    frontmatter["tags"] = []

                # Evita duplicatas
                for tag in tags_novas:
                    if tag not in frontmatter["tags"]:
                        frontmatter["tags"].append(tag)

                # Reescreve arquivo
                fm_novo = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)
                conteudo_novo = f"---\n{fm_novo}---\n\n{corpo}"

                with open(arquivo_path, "w", encoding="utf-8") as f:
                    f.write(conteudo_novo)

                self.tags_adicionadas += len(tags_novas)
                return True

            return False

        except Exception as e:
            print(f"❌ Erro ao processar {arquivo_path.name}: {e}")
            return False

    def processar_todos(self, limit=None):
        """Processa todos os arquivos CPC"""
        print("\n" + "="*60)
        print("🔧  ENRIQUECEDOR DE TAGS CPC")
        print("="*60 + "\n")

        # Encontra todos os arquivos
        arquivos = list(self.base_path.rglob("*.md"))
        arquivos = [a for a in arquivos if "INDEX" not in a.name]  # Exclui INDEXes

        if limit:
            arquivos = arquivos[:limit]

        print(f"📝 Processando {len(arquivos)} artigos...\n")

        enriquecidos = 0
        for i, arquivo in enumerate(arquivos, 1):
            if self.enriquecer_arquivo(arquivo):
                enriquecidos += 1

            if i % 100 == 0 or i == len(arquivos):
                percentual = (i / len(arquivos)) * 100
                print(f"   ✅ {i:>4d}/{len(arquivos)} processados ({percentual:.0f}%)")

        print(f"\n{'='*60}")
        print(f"✅ ENRIQUECIMENTO CONCLUÍDO!")
        print(f"{'='*60}")
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   • Artigos processados: {len(arquivos)}")
        print(f"   • Artigos enriquecidos: {enriquecidos}")
        print(f"   • Tags adicionadas: {self.tags_adicionadas}")
        print(f"\n✅ Tags adicionadas:")
        print(f"   - paragrafo-1, paragrafo-2, ... (§1, §2, ...)")
        print(f"   - inciso-i, inciso-ii, ... (I, II, III, ...)")
        print(f"   - alinea-a, alinea-b, ... (a), b), ...)\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enriquecedor de Tags CPC")
    parser.add_argument("--full", action="store_true", help="Processar todos os artigos")
    parser.add_argument("--limit", type=int, default=20, help="Limite de artigos (padrão: 20)")

    args = parser.parse_args()

    base = Path(r"C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\03_PROCESSO_CIVIL\CÓDIGO_PROCESSO_CIVIL\Artigos")

    enriquecedor = EnriquecedorTagsCPC(base)
    limit_artigos = None if args.full else args.limit
    enriquecedor.processar_todos(limit=limit_artigos)
