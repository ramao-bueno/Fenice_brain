#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para Enunciados CJF."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_enunciados_cjf import TAGS_PADRAO, JORNADAS


class MarkdownGeneratorEnunciadosCJF:
    """Gera notas Markdown estruturadas para Enunciados CJF."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_enunciado(self, enunciado: Dict) -> str:
        num = enunciado["num"]
        jornada = enunciado["jornada"]
        texto = enunciado["texto"]
        norma_id = enunciado["norma_id"]
        artigo_ref = enunciado["artigo"]

        # Categoriza por tipo de jornada
        tema = "jurisprudencia"
        for jornada_nome, categoria in JORNADAS.items():
            if jornada_nome.lower() in jornada.lower():
                tema = categoria.lower().replace(" ", "-")
                break

        tags = TAGS_PADRAO.copy()
        tags.extend([f"enunciado-{num}", tema, "cjf"])

        frontmatter = {
            "enunciado": str(num),
            "jornada": jornada,
            "artigo_referencia": artigo_ref,
            "norma_id": norma_id,
            "tipo": "enunciado_cjf",
            "status": "ativo",
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        # Limpar texto de lixo do Planalto
        texto_limpo = texto.replace(
            "Conselho da Justiça Federal Setor de Clubes Esportivos Sul - SCES Trecho III - Polo 8 - Lote 9 - Brasília/DF CEP: 70200-003 - Fone: (0xx61) 3022-7000 Atendimento ao público: das 11 às 19 horas Javascript utilizados para a manipulação das referências legislativas",
            ""
        ).strip()

        corpo = f"""# Enunciado CJF {num}

**Jornada:** {jornada}
**Artigo Referência:** {artigo_ref}
**Status:** ATIVO

---

## TEXTO DO ENUNCIADO

> {texto_limpo}

---

## ANALISE

### Orientação Jurisprudencial

[Qual é a orientação do CJF com este enunciado?
Qual é a posição que o Conselho adota sobre interpretação do artigo referenciado?]

### Aplicação Prática

[Como este enunciado é aplicado na prática forense?
Qual é a repercussão em sentenças e decisões?]

### Artigo Correlato

**Art. {artigo_ref}** — Ver nota relacionada para compreender o dispositivo interpretado.

---

## JURISPRUDENCIA RELACIONADA

[Decisões do STF/STJ que dialogam com este enunciado — jurisprudência mais recente
que confirma, afasta ou relativiza a orientação do CJF]

---

## OBSERVACOES

[Críticas, limitações ou exceções à orientação deste enunciado]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_enunciado(self, enunciado: Dict, conteudo: str) -> Path:
        # Organiza por jornada
        jornada_nome = enunciado["jornada"]
        # Extrai nome mais simples da jornada
        jornada_pasta = jornada_nome.split("-")[0].strip()  # Ex: "I Jornada de Direito Civil"

        pasta = self.output_base / jornada_pasta
        pasta.mkdir(parents=True, exist_ok=True)

        filename = f"Enunciado {enunciado['num']:03d}.md"
        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"Erro ao salvar enunciado {enunciado['num']}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGeneratorEnunciadosCJF(Path("test_output_cjf"))
    print("Gerador Enunciados CJF pronto")
