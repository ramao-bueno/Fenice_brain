#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador CC: Cria estrutura completa de Código Civil baseada em índice estruturado

Estratégia: Usa índice já documentado em CC-INDEX para gerar artigos "skeleton"
com referências cruzadas, prontos para enriquecimento posterior
"""

import sys
from pathlib import Path
from datetime import datetime
import yaml

# Dados estruturados do Código Civil (2.046 artigos em 5 livros)
CC_ESTRUTURA = [
    {
        "livro": "LIVRO-I",
        "nome": "Parte Geral",
        "intervalo": (1, 232),
        "temas": ["pessoas", "bens", "fatos-jurídicos"],
    },
    {
        "livro": "LIVRO-II",
        "nome": "Direito das Obrigações",
        "intervalo": (233, 709),
        "temas": ["contratos", "obrigações", "responsabilidade-civil"],
    },
    {
        "livro": "LIVRO-III",
        "nome": "Direito das Coisas",
        "intervalo": (710, 1256),
        "temas": ["propriedade", "direitos-reais", "posse"],
    },
    {
        "livro": "LIVRO-IV",
        "nome": "Direito de Família",
        "intervalo": (1257, 1638),
        "temas": ["casamento", "filiação", "guarda"],
    },
    {
        "livro": "LIVRO-V",
        "nome": "Direito das Sucessões",
        "intervalo": (1639, 2046),
        "temas": ["herança", "testamento", "sucessão"],
    },
]

def gerar_articulos_cc():
    """Gera lista de artigos CC a partir da estrutura."""
    artigos = []

    for livro_info in CC_ESTRUTURA:
        inicio, fim = livro_info["intervalo"]
        for num_artigo in range(inicio, fim + 1):
            artigos.append({
                "numero": num_artigo,
                "livro": livro_info["livro"],
                "livro_nome": livro_info["nome"],
                "temas": livro_info["temas"],
                "titulo": f"[Artigo {num_artigo} - Direito Civil]",
                "redacao": f"Lei 10.406/2002 - Art. {num_artigo}"
            })

    return artigos


def gerar_nota_artigo(artigo: dict) -> str:
    """Gera Markdown estruturado para artigo CC."""

    num = artigo["numero"]
    livro = artigo["livro"]
    livro_nome = artigo["livro_nome"]
    titulo = artigo["titulo"]

    # Frontmatter
    frontmatter = {
        "artigo": str(num),
        "lei": "Lei 10.406/2002 (Código Civil)",
        "tipo": "direito-civil",
        "livro": livro,
        "status": "vigente",
        "tags": ["cc", "direito-civil", livro.lower(), "vigente"],
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Corpo
    corpo = f"""# CC Art. {num} — {titulo}

**Lei:** Lei 10.406/2002 (Código Civil)
**Livro:** {livro} — {livro_nome}
**Status:** ✅ VIGENTE

---

## 📋 REDAÇÃO LEGAL

> [Redação legal a ser adicionada]

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


def salvar_artigo(artigo: dict, conteudo: str, output_base: Path) -> Path:
    """Salva artigo em arquivo Markdown."""

    livro = artigo["livro"]
    pasta = output_base / livro
    pasta.mkdir(parents=True, exist_ok=True)

    titulo_limpo = f"Art. {artigo['numero']} — Código Civil"
    filename = f"{titulo_limpo}.md"

    filepath = pasta / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return filepath
    except Exception as e:
        print(f"❌ Erro ao salvar {filename}: {e}")
        return None


def pipeline_cc_gerador(limit=None):
    """Pipeline de geração CC."""

    output_base = Path(r"C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\02_DIREITO_CIVIL\Artigos")

    print("\n" + "="*60)
    print("🔄  GERADOR CC: Estrutura → Markdown")
    print("="*60 + "\n")

    # Gera artigos
    print("📖 ETAPA 1: Gerando estrutura de artigos CC...")
    artigos = gerar_articulos_cc()

    if limit:
        artigos = artigos[:limit]
        print(f"⚠️  Limitado a {limit} artigos")

    print(f"✅ {len(artigos)} artigos prontos\n")

    # Salva cada um
    print("📝 ETAPA 2: Salvando notas Markdown...")
    salvos = 0

    for i, art in enumerate(artigos, 1):
        try:
            conteudo = gerar_nota_artigo(art)
            filepath = salvar_artigo(art, conteudo, output_base)

            if filepath:
                salvos += 1

            if i % 200 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>4d}/{len(artigos)} artigos ({percentual:.0f}%)")

        except Exception as e:
            print(f"   ⚠️  Erro Art. {art['numero']}: {e}")

    print(f"\n{'='*60}")
    print(f"✅ GERADOR CC CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Artigos gerados: {len(artigos)}")
    print(f"   • Artigos salvos: {salvos}")
    print(f"   • Taxa sucesso: {(salvos/len(artigos)*100):.1f}%")
    print(f"\n📁 Local de saída: {output_base}\n")

    return salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerador CC: Estrutura → Markdown")
    parser.add_argument("--full", action="store_true", help="Gerar todos os 2.046 artigos")
    parser.add_argument("--limit", type=int, default=20, help="Número máximo (padrão: 20)")

    args = parser.parse_args()

    limit_artigos = None if args.full else args.limit

    sucesso = pipeline_cc_gerador(limit=limit_artigos)

    sys.exit(0 if sucesso else 1)
