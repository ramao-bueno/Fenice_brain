#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerador CF/88: Preenche artigos com conteúdo do Planalto
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
import yaml
from pathlib import Path
from datetime import datetime
from cf_planalto_extractor import CFPlanaltoExtractor
from config_cf import TITULO_MAPEAMENTO, TEMA_POR_TITULO

def gerar_markdown_completo(artigo: dict, titulo: str) -> str:
    """Gera markdown com redação legal preenchida."""

    num = artigo["numero"]
    titulo_art = artigo["titulo"]
    redacao = artigo["texto_completo"] or artigo["redacao"]
    titulo_nome = TITULO_MAPEAMENTO.get(titulo, {}).get("nome", titulo)
    tema = TEMA_POR_TITULO.get(titulo, "")

    # Frontmatter
    frontmatter = {
        "artigo": str(num),
        "lei": "Constituição Federal de 1988",
        "titulo_cf": titulo,
        "parte": titulo_nome,
        "status": "vigente",
        "cf88": True,
        "tags": ["cf88", "constituicao", "vigente", titulo.lower()],
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    if tema:
        frontmatter["tags"].append(tema)

    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Corpo Markdown
    corpo = f"""# CF/88 Art. {num} — {titulo_art}

**Lei:** Constituição Federal de 1988
**Título:** {titulo} — {titulo_nome}
**Status:** VIGENTE

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Sujeito** | A quem se dirige a norma |
| **Objeto** | O que a norma regula |
| **Eficácia** | Aplicabilidade (plena / contida / limitada) |

---

## ARTIGOS CORRELATOS

### Mesma CF
- [[Art. {max(1, num-1)} — CF]] — artigo anterior
- [[Art. {num+1} — CF]] — artigo seguinte

### Legislação Derivada
[Leis ordinárias que regulamentam este artigo]

---

## JURISPRUDENCIA STF

### Teses e Precedentes
[Precedentes do STF sobre este artigo]

---

## EMENDAS CONSTITUCIONAIS

[ECs que modificaram este artigo — verificar no Planalto]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
**Fonte oficial:** [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)
"""

    return f"---\n{fm_str}---\n\n{corpo}"


def regenerar_artigos(full=False):
    """Regenera artigos da CF com conteúdo do Planalto."""

    print("\n" + "="*70)
    print("🔄 REGENERADOR CF/88: Preenchendo artigos com conteúdo")
    print("="*70 + "\n")

    # Extrai artigos do Planalto
    print("📖 ETAPA 1: Extraindo artigos da CF/88 do Planalto...")
    extractor = CFPlanaltoExtractor()
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído!")
        return False

    print(f"✅ {len(artigos)} artigos extraídos\n")

    # Determina pasta base
    fenice_base = Path(__file__).parent.parent / "FENICE bRain" / "00_CONSTITUIÇÃO_FEDERAL" / "Artigos"

    # Processa artigos
    print("📝 ETAPA 2: Gerando e salvando markdown...")
    salvos = 0
    erros = 0

    for i, art in enumerate(artigos, 1):
        try:
            titulo = art["livro"]
            pasta = fenice_base / titulo
            pasta.mkdir(parents=True, exist_ok=True)

            # Cria nome do arquivo
            filename = f"Art. {art['numero']} — CF.md"
            filepath = pasta / filename

            # Gera e salva
            conteudo = gerar_markdown_completo(art, titulo)
            filepath.write_text(conteudo, encoding="utf-8")
            salvos += 1

            if i % 50 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>3d}/{len(artigos)} artigos processados ({percentual:>5.1f}%)")

        except Exception as e:
            erros += 1
            print(f"   ❌ Erro no Art. {art['numero']}: {e}")
            continue

    print(f"\n{'='*70}")
    print(f"✅ REGENERAÇÃO CONCLUÍDA!")
    print(f"{'='*70}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Artigos processados: {len(artigos)}")
    print(f"   • Artigos salvos: {salvos}")
    print(f"   • Erros: {erros}")
    print(f"   • Taxa sucesso: {(salvos/len(artigos)*100):.1f}%")
    print(f"\n📁 Local de saída: {fenice_base}\n")

    return salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Regenerador CF/88")
    parser.add_argument("--full", action="store_true", help="Regenerar todos os artigos")

    args = parser.parse_args()

    sucesso = regenerar_artigos(full=args.full)
    sys.exit(0 if sucesso else 1)
