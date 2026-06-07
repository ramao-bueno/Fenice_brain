#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de leis de Direito Digital."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_direito_digital import TAGS_PADRAO


class MarkdownGeneratorDD:
    """Gera notas Markdown estruturadas para artigos de leis de Direito Digital."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo["categoria"]
        tema = lei_cfg.get("tema", "direito-digital")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": str(num),
            "lei": f"Lei {lei_numero} ({nome_lei})",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_digital": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Conferir redação no Planalto]")
        titulo_artigo = artigo.get("titulo", f"Art. {num}")
        art_anterior = max(1, num - 1)
        art_seguinte = num + 1

        corpo = f"""# {sigla} Art. {num} — {titulo_artigo}

**Lei:** {lei_numero} — {nome_lei}
**Categoria:** {categoria}
**Status:** VIGENTE

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Co-dependência normativa
[Esta regra depende de qual outro instrumento — CF Art. 5º (privacidade/liberdade de
expressão), Código Civil, Código Penal, outra lei de Direito Digital? Ver
`atomizar-juridico` para mapeamento relacional completo]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outras leis de Direito Digital
[Ligar aqui dispositivos correlatos em outras leis do ramo — ex.: LGPD ↔ Marco Civil
↔ Lei do Software ↔ Lei de Direitos Autorais frequentemente se cruzam em casos reais]

---

## JURISPRUDENCIA

[Precedentes do STF/STJ sobre este artigo — área em rápida formação jurisprudencial]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_artigo(self, artigo: Dict, conteudo: str, sigla: str) -> Path:
        pasta = self.output_base / sigla
        pasta.mkdir(parents=True, exist_ok=True)

        filename = f"{sigla} Art. {artigo['numero']}.md"
        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"Erro ao salvar {filename}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGeneratorDD(Path("test_output_dd"))
    print("Gerador Direito Digital pronto")
