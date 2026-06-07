#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de Processo Penal."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_codigo_processo_penal import TAGS_PADRAO


class MarkdownGeneratorCPP:
    """Gera notas Markdown estruturadas para artigos de processo penal."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "PROCESSO_PENAL"))
        tema = lei_cfg.get("tema", "processo-penal")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": str(num),
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "processo_penal": True,
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

### Conceito Processual Penal

[Síntese do conceito processual penal: qual é a regra ou princípio que este artigo estabelece?
Exemplo: direitos do acusado, princípios processuais, procedimentos, provas, recursos, etc.]

### Fase Processual

[Em qual fase do processo penal este artigo atua?
(Inquérito, oferecimento de denúncia, recebimento, instrução probatória, sentença, recursos?)]

### Conexão com Direito Material

[Como este artigo de processo se articula com o direito penal material (CP)?
Qual conduta criminosa este procedimento visa a punir ou proteger?]

### Co-dependência normativa

[Qual outro dispositivo do CPP, CP, CPC ou leis especiais depende desta regra?
Jurisprudência que desenvolve ou relativiza este artigo?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros ramos
[Dispositivos do CP, CPC, leis especiais (Maria da Penha, Lei de Drogas, Tortura)
que dialogam com este artigo]

---

## JURISPRUDENCIA

[Precedentes do STF/STJ sobre este artigo — jurisprudência pacífica e controvérsias]

---

## OBSERVACOES PRATICAS

[Aplicação concreta na prática forense: como promotores, defensores, juízes
utilizam este artigo em procedimentos penais?]

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
    gen = MarkdownGeneratorCPP(Path("test_output_cpp"))
    print("Gerador Código de Processo Penal pronto")
