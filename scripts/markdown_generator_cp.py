#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código Penal."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_codigo_penal import TAGS_PADRAO


class MarkdownGeneratorCP:
    """Gera notas Markdown estruturadas para artigos do Código Penal."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "DIREITO_PENAL"))
        tema = lei_cfg.get("tema", "direito-penal")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        # Detectar parte do CP (arts. 1-84: Parte Geral, 85-302: Parte Especial)
        parte_info = self._detectar_parte_cp(num) if sigla == "DEL2848" else None

        frontmatter = {
            "artigo": str(num),
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_penal": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        if parte_info:
            frontmatter.update(parte_info)

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

### Bem Jurídico Tutelado

[Qual bem jurídico penal este artigo protege?
Exemplo: vida, liberdade, honra, patrimônio, segurança pública, etc.]

### Tipo Penal

[Síntese do tipo penal: sujeitos do crime (ativo/passivo), conduta, resultado, nexo causal]

### Dolo/Culpa

[Qual é a forma de imputação? Dolo direto? Dolo eventual? Culpa?
Há tipificação culposa em outro artigo?]

### Tentativa e Consumação

[Qual é o momento de consumação?
A tentativa é punível conforme art. 14 do CP?]

### Penas Cominadas

[Qual é a pena? Isolada ou cumulativa?
Há circunstâncias agravantes/atenuantes?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros crimes
[Dispositivos do CP que se relacionam — crimes conexos, concurso de crimes,
causas de exclusão de ilicitude ou culpabilidade]

---

## JURISPRUDENCIA

[Precedentes do STF/STJ sobre este crime — jurisprudência pacífica, controvérsias,
mudanças de orientação]

---

## OBSERVACOES PRATICAS

[Aplicação na prática forense: como MP, defesa e tribunais utilizam este artigo
em denúncias, defesas, sentenças?]

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
    def _detectar_parte_cp(num: int) -> Dict:
        """Detecta qual parte do CP o artigo pertence."""
        if 1 <= num <= 84:
            return {"parte": "Geral", "titulo": "Disposições Gerais"}
        elif 85 <= num <= 302:
            return {"parte": "Especial", "titulo": "Dos Crimes"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCP(Path("test_output_cp"))
    print("Gerador Código Penal pronto")
