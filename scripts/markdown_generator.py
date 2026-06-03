import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config import TAGS_PADRAO, LEI_NOME, LIVRO_MAPEAMENTO

class MarkdownGenerator:
    """Gera notas Markdown estruturadas para artigos do CPC."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)
        self.template_frontmatter = {
            "artigo": "",
            "lei": LEI_NOME,
            "tipo": "processo-civil",
            "livro": "",
            "status": "vigente",
            "tags": TAGS_PADRAO.copy(),
            "created": datetime.now().strftime("%Y-%m-%d")
        }

    def gerar_nota_artigo(self, artigo: Dict, livro: str) -> str:
        """Gera conteúdo Markdown completo de um artigo."""

        num = artigo["numero"]
        titulo = artigo["titulo"]
        redacao = artigo["redacao"]
        livro_nome = LIVRO_MAPEAMENTO.get(livro, {}).get("nome", livro)

        # Frontmatter
        frontmatter = self.template_frontmatter.copy()
        frontmatter["artigo"] = str(num)
        frontmatter["livro"] = livro
        # Adiciona tags únicas (evita duplicatas)
        tags_adicionais = [livro.lower(), f"art-{num}"]
        for tag in tags_adicionais:
            if tag not in frontmatter["tags"]:
                frontmatter["tags"].append(tag)

        fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # Corpo Markdown
        corpo = f"""# CPC Art. {num} — {titulo}

**Lei:** {LEI_NOME}
**Livro:** {livro} — {livro_nome}
**Status:** ✅ VIGENTE

---

## 📋 REDAÇÃO LEGAL

> {redacao}

---

## 🔍 ANÁLISE TÉCNICA

### Conceito Central

[Análise do artigo em linguagem jurídica clara e acessível]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Aspecto 1** | Descrição do elemento |
| **Aspecto 2** | Descrição do elemento |

---

## 🔗 ARTIGOS CORRELATOS

- [[Art. {max(1, num-1)}]] — Artigo anterior
- [[Art. {num+1}]] — Artigo seguinte

---

## ⚖️ JURISPRUDÊNCIA

### STF/STJ Precedentes
[Jurisprudência relacionada a ser adicionada]

---

## 📚 Referência Rápida

**Tipo de Norma:** Processual Civil
**Hierarquia:** Lei Ordinária
**Fonte:** Planalto.gov.br
**Vigência:** Confirmada em 2026-06-03

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
"""

        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_artigo(self, artigo: Dict, conteudo: str, livro: str) -> Path:
        """Salva artigo em arquivo Markdown."""
        pasta = self.output_base / livro
        pasta.mkdir(parents=True, exist_ok=True)

        # Cria nome do arquivo seguro
        titulo_limpo = artigo['titulo'].replace('/', '-').replace('\\', '-')[:50]
        filename = f"Art. {artigo['numero']} — {titulo_limpo}.md"

        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"❌ Erro ao salvar {filename}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGenerator(Path("test_output"))
    print("✅ Gerador Markdown pronto para usar")
