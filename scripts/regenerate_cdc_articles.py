#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerador CDC: Preenche artigos com conteúdo do Planalto

Uso:
    python regenerate_cdc_articles.py --full    # Regenera TODOS os 119 artigos
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
import yaml
from pathlib import Path
from datetime import datetime
from cdc_planalto_extractor import CDCPlanaltoExtractor
from config_cdc import LIVRO_MAPEAMENTO


def mapear_tipo_norma(num_artigo: int) -> str:
    """
    Mapeia o número do artigo para o tipo de norma.

    - Arts. 1-59: "protetor"
    - Arts. 60-78: "penal"
    - Arts. 79-105: "processual"
    - Arts. 106-119: "sanção"
    """
    if 1 <= num_artigo <= 59:
        return "protetor"
    elif 60 <= num_artigo <= 78:
        return "penal"
    elif 79 <= num_artigo <= 105:
        return "processual"
    elif 106 <= num_artigo <= 119:
        return "sanção"
    return "geral"


def mapear_aplicacao(num_artigo: int) -> list:
    """
    Mapeia o número do artigo para areas de aplicação.

    Retorna lista de tags de aplicacao.
    """
    aplicacoes = []

    # Arts. 1-3: relacao-de-consumo
    if 1 <= num_artigo <= 3:
        aplicacoes.append("relacao-consumo")

    # Arts. 4-6: direitos-basicos
    if 4 <= num_artigo <= 6:
        aplicacoes.append("direitos-basicos")

    # Arts. 12-17: responsabilidade-civil
    if 12 <= num_artigo <= 17:
        aplicacoes.append("responsabilidade-civil")

    # Arts. 18-27: compra-e-venda
    if 18 <= num_artigo <= 27:
        aplicacoes.append("compra-venda")

    # Arts. 28-35: contratos
    if 28 <= num_artigo <= 35:
        aplicacoes.append("contratos")

    # Arts. 36-38: publicidade
    if 36 <= num_artigo <= 38:
        aplicacoes.append("publicidade")

    # Arts. 39-41: praticas-abusivas
    if 39 <= num_artigo <= 41:
        aplicacoes.append("praticas-abusivas")

    # Arts. 49-60: credito-ao-consumidor
    if 49 <= num_artigo <= 60:
        aplicacoes.append("credito")

    return aplicacoes if aplicacoes else ["geral"]


def mapear_relevancia(num_artigo: int) -> str:
    """
    Mapeia o número do artigo para nível de relevância.

    Artigos críticos: 4, 6, 12, 14, 18, 39, 49
    """
    artigos_criticos = {4, 6, 12, 14, 18, 39, 49}
    if num_artigo in artigos_criticos:
        return "alta"
    return "média"


def mapear_pasta_saida(num_artigo: int) -> str:
    """
    Mapeia o número do artigo para a pasta de saída.

    Retorna nome da subpasta em 08_CÓDIGO_CONSUMIDOR/
    """
    if 1 <= num_artigo <= 59:
        return "Direitos-do-Consumidor"
    elif 60 <= num_artigo <= 78:
        return "Infrações-Penais"
    elif 79 <= num_artigo <= 105:
        return "Processo-Administrativo"
    elif 106 <= num_artigo <= 119:
        return "Disposições-Gerais"
    return "Disposições-Gerais"


def gerar_markdown_completo(artigo: dict, livro: str) -> str:
    """Gera markdown com redação legal preenchida."""

    num = artigo["numero"]
    titulo = artigo["titulo"]
    redacao = artigo["texto_completo"] or artigo["redacao"]
    livro_nome = LIVRO_MAPEAMENTO.get(livro, {}).get("nome", livro)
    tipo_norma = mapear_tipo_norma(num)
    aplicacoes = mapear_aplicacao(num)
    relevancia = mapear_relevancia(num)

    # Frontmatter
    tags = [
        "direito-do-consumidor",
        "lei-8078",
        f"livro-{livro.lower().replace('-', '')}",
        f"tipo-{tipo_norma}",
    ]
    tags.extend([f"aplicacao-{app}" for app in aplicacoes])

    frontmatter = {
        "artigo": str(num),
        "lei": "Lei 8.078/1990 (Código do Consumidor)",
        "titulo": titulo,
        "livro": livro,
        "tipo_norma": tipo_norma,
        "aplicacao": aplicacoes,
        "relevancia": relevancia,
        "status": "vigente",
        "tags": tags,
        "created": datetime.now().strftime("%Y-%m-%d")
    }

    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Corpo Markdown
    corpo = f"""# CDC Art. {num} — {titulo}

**Lei:** Lei 8.078/1990 (Código do Consumidor)
**Livro:** {livro} — {livro_nome}
**Tipo:** {tipo_norma.title()}
**Status:** ✅ VIGENTE
**Relevância:** {relevancia.title()}

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
    """Regenera artigos do CDC com conteúdo do Planalto."""

    print("\n" + "="*70)
    print("🔄 REGENERADOR CDC: Preenchendo 119 artigos com conteúdo")
    print("="*70 + "\n")

    # Extrai artigos do Planalto
    print("📖 ETAPA 1: Extraindo artigos do Planalto...")
    extractor = CDCPlanaltoExtractor()
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído!")
        return False

    print(f"✅ {len(artigos)} artigos extraídos\n")

    # Determina pasta base
    fenice_base = Path(__file__).parent.parent / "FENICE bRain" / "08_CÓDIGO_CONSUMIDOR"

    # Processa artigos
    print("📝 ETAPA 2: Gerando e salvando markdown...")
    salvos = 0
    erros = 0

    for i, art in enumerate(artigos, 1):
        try:
            livro = art["livro"]
            subfolder = mapear_pasta_saida(art["numero"])
            pasta = fenice_base / subfolder
            pasta.mkdir(parents=True, exist_ok=True)

            # Cria nome do arquivo
            filename = f"Art. {art['numero']} — {art['titulo'][:50]}.md".replace("/", "-")
            filepath = pasta / filename

            # Gera e salva
            conteudo = gerar_markdown_completo(art, livro)
            filepath.write_text(conteudo, encoding="utf-8")
            salvos += 1

            if i % 20 == 0 or i == len(artigos):
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

    parser = argparse.ArgumentParser(description="Regenerador CDC")
    parser.add_argument("--full", action="store_true", help="Regenerar todos os 119 artigos")

    args = parser.parse_args()

    sucesso = regenerar_artigos(full=args.full)
    sys.exit(0 if sucesso else 1)
