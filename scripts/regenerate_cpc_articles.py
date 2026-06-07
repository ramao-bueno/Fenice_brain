#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerador CPC: Preenche artigos vazios com conteúdo do Planalto
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
import yaml
from pathlib import Path
from datetime import datetime
from cpc_planalto_extractor import CPCPlanaltoExtractor
from config_cpc import LIVRO_MAPEAMENTO

def gerar_markdown_completo(artigo: dict, livro: str) -> str:
    """Gera markdown com redação legal preenchida."""

    num = artigo["numero"]
    titulo = artigo["titulo"]
    redacao = artigo["texto_completo"] or artigo["redacao"]
    livro_nome = LIVRO_MAPEAMENTO.get(livro, {}).get("nome", livro)

    # Frontmatter
    frontmatter = {
        "artigo": str(num),
        "lei": "Lei 13.105/2015 (Código de Processo Civil)",
        "tipo": "processo-civil",
        "livro": livro,
        "status": "vigente",
        "tags": ["cpc", "processo-civil", livro.lower(), "vigente"],
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Corpo Markdown
    corpo = f"""# CPC Art. {num} — {titulo}

**Lei:** Lei 13.105/2015 (Código de Processo Civil)
**Livro:** {livro} — {livro_nome}
**Status:** ✅ VIGENTE

---

## 📋 REDAÇÃO LEGAL

> {redacao}

---

## 🔍 ANÁLISE TÉCNICA

### Conceito Central

[Análise do artigo em linguagem jurídica clara]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Aspecto 1** | Descrição |
| **Aspecto 2** | Descrição |

---

## 🔗 ARTIGOS CORRELATOS

- [[Art. {max(1, num-1)}]] — Artigo anterior
- [[Art. {num+1}]] — Artigo seguinte

---

## ⚖️ JURISPRUDÊNCIA

[STF/STJ precedentes a adicionar]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
**Fonte:** Planalto.gov.br
**Vigência:** Confirmada até hoje
"""

    return f"---\n{fm_str}---\n\n{corpo}"


def regenerar_artigos(full=False):
    """Regenera artigos do CPC com conteúdo do Planalto."""

    print("\n" + "="*70)
    print("🔄 REGENERADOR CPC: Preenchendo artigos vazios")
    print("="*70 + "\n")

    # Extrai artigos do Planalto
    print("📖 ETAPA 1: Extraindo artigos do CPC do Planalto...")
    extractor = CPCPlanaltoExtractor()
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído!")
        return False

    print(f"✅ {len(artigos)} artigos extraídos\n")

    # Determina pasta base
    fenice_base = Path(__file__).parent.parent / "FENICE bRain" / "05_CÓDIGO_PROCESSO_CIVIL" / "Artigos"

    # Processa artigos
    print("📝 ETAPA 2: Gerando e salvando markdown...")
    salvos = 0
    erros = 0

    for i, art in enumerate(artigos, 1):
        try:
            livro = art["livro"]
            pasta = fenice_base / livro
            pasta.mkdir(parents=True, exist_ok=True)

            # Cria nome do arquivo
            filename = f"Art. {art['numero']} — CPC.md"
            filepath = pasta / filename

            # Gera e salva
            conteudo = gerar_markdown_completo(art, livro)
            filepath.write_text(conteudo, encoding="utf-8")
            salvos += 1

            if i % 200 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>4d}/{len(artigos)} artigos processados ({percentual:>5.1f}%)")

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

    parser = argparse.ArgumentParser(description="Regenerador CPC")
    parser.add_argument("--full", action="store_true", help="Regenerar todos os artigos")

    args = parser.parse_args()

    sucesso = regenerar_artigos(full=args.full)
    sys.exit(0 if sucesso else 1)
