#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código de Processo Civil."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_codigo_processo_civil import TAGS_PADRAO


class MarkdownGeneratorCPC:
    """Gera notas Markdown estruturadas para artigos do CPC."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "CODIGO_PROCESSO_CIVIL"))
        tema = lei_cfg.get("tema", "processo-civil")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        # Detectar livro/parte do CPC (arts. 1-77: Disposições Preliminares, etc.)
        livro_info = self._detectar_livro_cpc(num) if sigla == "L13105" else None

        frontmatter = {
            "artigo": str(num),
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente" if "13105" in sigla else "revogado",
            "processo_civil": True,
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
**Status:** {'VIGENTE' if '13105' in sigla else 'REVOGADO'}

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Processual

[Síntese do conceito processual: qual é a regra ou princípio que este artigo estabelece?
Exemplo: litispendência, coisa julgada, competência, legitimidade, etc.]

### Função no Processo

[Como este artigo estrutura o procedimento? Qual etapa do processo ele disciplina?
(Fase postulatória, probatória, executória?)]

### Co-dependência normativa

[Qual outro dispositivo do CPC depende desta regra? CF/88? Lei especial?
Como se articula com Código Civil, Código Penal, ou procedimentos especiais?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros ramos
[Dispositivos do CC, CP, leis especiais (Consumidor, Ambiental, Públicas, etc.)
que dialogam com este artigo de processo]

---

## JURISPRUDENCIA

[Precedentes do STF/STJ sobre este artigo — jurisprudência pacífica e controvérsias]

---

## OBSERVACOES PRATICAS

[Aplicação concreta no tribunal: como este artigo é utilizado na prática forense?
Publicações, comunicações, prazos, formalizações?]

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
    def _detectar_livro_cpc(num: int) -> Dict:
        """Detecta qual livro/parte do CPC o artigo pertence."""
        if 1 <= num <= 77:
            return {"livro": "Preliminar", "titulo": "Disposições Preliminares"}
        elif 78 <= num <= 139:
            return {"livro": "I", "titulo": "Da Tutela Jurisdicional"}
        elif 140 <= num <= 295:
            return {"livro": "II", "titulo": "Da Composição e Competência"}
        elif 296 <= num <= 516:
            return {"livro": "III", "titulo": "Das Partes e dos Procuradores"}
        elif 517 <= num <= 771:
            return {"livro": "IV", "titulo": "Dos Atos Processuais"}
        elif 772 <= num <= 1072:
            return {"livro": "V", "titulo": "Do Processo de Conhecimento"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCPC(Path("test_output_cpc"))
    print("Gerador Código de Processo Civil pronto")
