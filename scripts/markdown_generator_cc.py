#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código Civil."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_codigo_civil import TAGS_PADRAO


class MarkdownGeneratorCC:
    """Gera notas Markdown estruturadas para artigos do Código Civil."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "CODIGO_CIVIL"))
        tema = lei_cfg.get("tema", "direito-civil")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        # Detectar livro do CC (Art. 1-232: Pessoa | 233-709: Obrigação | etc.)
        livro_info = self._detectar_livro_cc(num) if sigla == "L10406" else None

        frontmatter = {
            "artigo": str(num),
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_civil": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        if livro_info:
            frontmatter.update(livro_info)

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

### Função no Sistema

[Como este artigo se relaciona com o sistema de Direito Civil — que direito ele
tutela? Qual obrigação, responsabilidade ou direito real ele estrutura?]

### Co-dependência normativa

[Qual outro dispositivo este artigo depende? CF/88? Código de Processo Civil?
Códigos especiais (Consumer Protection, Lei de Incorporação, etc.)?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros ramos
[Dispositivos do CPC, CPP, leis especiais que dialogam com este artigo]

---

## JURISPRUDENCIA

[Precedentes do STF/STJ e jurisprudência pacífica sobre este artigo]

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

    @staticmethod
    def _detectar_livro_cc(num: int) -> Dict:
        """Detecta qual livro do CC o artigo pertence."""
        if 1 <= num <= 232:
            return {"livro": "I", "titulo": "Das Pessoas"}
        elif 233 <= num <= 709:
            return {"livro": "II", "titulo": "Do Direito das Obrigações"}
        elif 710 <= num <= 1.227:
            return {"livro": "III", "titulo": "Do Direito das Coisas"}
        elif 1.228 <= num <= 1.626:
            return {"livro": "IV", "titulo": "Do Direito de Família"}
        elif 1.627 <= num <= 2.046:
            return {"livro": "V", "titulo": "Do Direito das Sucessões"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCC(Path("test_output_cc"))
    print("Gerador Código Civil pronto")
