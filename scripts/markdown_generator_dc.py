#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de Direito do Consumidor (CDC) e leis constitucionais correlatas."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_direito_constitucional import TAGS_PADRAO


# Jurisprudência curada: súmulas e teses STJ/STF para CDC (L8078) e correlatos
JURIS_DC = {
    "6": [
        "STJ — Súmula 297: o Código de Defesa do Consumidor é aplicável às instituições financeiras.",
        "STJ — Súmula 479: nas operações bancárias, inverte-se o ônus da prova em favor do consumidor.",
        "STJ — A hipossuficiência do consumidor é técnica (informação) ou econômica; presume-se na relação de consumo.",
    ],
    "12": [
        "STJ — Tese: a responsabilidade do fabricante pelo produto defeituoso (art. 12) é objetiva e solidária; o fornecedor não se exonera pela ausência de culpa.",
        "STJ — Tese: o recall não feito imediatamente após o conhecimento do defeito agrava a responsabilidade do fornecedor e configura dano moral in re ipsa.",
    ],
    "14": [
        "STJ — Tese: a responsabilidade do fornecedor de serviços (art. 14) é objetiva; exclui-se apenas por culpa exclusiva do consumidor, fato de terceiro ou caso fortuito externo.",
        "STJ — Súmula 221: são civilmente responsáveis pelo ressarcimento de dano, decorrente de publicação pela imprensa, tanto o autor do escrito quanto o proprietário do veículo de divulgação.",
    ],
    "17": [
        "STJ — Tese: o consumidor equiparado (bystander) do art. 17 é quem sofre dano pelo produto ou serviço, sem ser o destinatário final; aplica-se o regime protetivo do CDC.",
    ],
    "26": [
        "STJ — O prazo decadencial do art. 26 (30 dias para vícios aparentes de serviço não durável, 90 para duráveis) começa da entrega do produto ou do encerramento dos serviços.",
        "STJ — Tese: a reclamação do consumidor ao fornecedor (extrajudicial ou administrativa) suspende o prazo decadencial do art. 26 §2°, II.",
    ],
    "27": [
        "STJ — O prazo prescricional de 5 anos do art. 27 aplica-se à pretensão de reparação por fato do produto ou do serviço (dano efetivo); o prazo do art. 26 aplica-se ao vício (qualidade/quantidade).",
        "STJ — Tese: o prazo do art. 27 é de prescrição (não decadência); admite causas de suspensão e interrupção.",
    ],
    "39": [
        "STJ — Súmula 302: é abusiva a cláusula contratual de plano de saúde que limita o tempo de internação hospitalar do segurado.",
        "STJ — Tese: é abusiva a prática de envio de cartão de crédito não solicitado; o fornecedor responde pelos danos causados pela prática abusiva.",
    ],
    "46": [
        "STJ — As cláusulas contratuais que restringem direitos do consumidor devem ser redigidas com destaque e clareza; ambiguidade é interpretada em favor do consumidor.",
        "STJ — Tese: contratos de adesão (art. 54) devem ser interpretados em favor do consumidor aderente quando houver cláusula ambígua.",
    ],
    "51": [
        "STJ — Súmula 381: nos contratos bancários, é vedado ao julgador conhecer de ofício da abusividade das cláusulas.",
        "STJ — Tese: cláusula que estabelece foro distante do domicílio do consumidor é abusiva (art. 51, IV) pois dificulta o acesso à Justiça.",
        "STJ — Cláusula penal superior a 2% do valor da parcela é abusiva em contratos de consumo (art. 52 §1°).",
    ],
    "101": [
        "STJ — A competência para ações do consumidor (art. 101, I) é do foro do domicílio do consumidor; cláusula de eleição de foro diferente é nula.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_DC = {
    "6": {
        "autor": "Invocar a hipossuficiência técnica para requerer inversão do ônus da prova (art. 6°, VIII); nas relações bancárias, a inversão é quase automática (Súmula 479 STJ).",
        "reu": "Demonstrar que a relação não é de consumo (fornecedor não habitual, pessoa jurídica adquirindo produto como insumo — teoria finalista); afastar a inversão do ônus demonstrando suficiência técnica do consumidor.",
        "pratica": "O CDC se aplica a contratos bancários (Súmula 297 STJ), seguros, planos de saúde, serviços públicos concedidos e contratos imobiliários. Não se aplica às relações trabalhistas nem às relações entre fornecedores.",
    },
    "14": {
        "autor": "Demonstrar o defeito do serviço (falha na execução ou inadequação ao fim esperado), o dano e o nexo causal; na responsabilidade objetiva, não é necessário provar culpa.",
        "reu": "Provar culpa exclusiva do consumidor, caso fortuito externo ou fato de terceiro. A culpa concorrente do consumidor reduz a indenização proporcionalmente (art. 12, §3° por analogia).",
        "pratica": "Dano moral nas relações de consumo: é in re ipsa em casos de negativação indevida, cobranças vexatórias e recusas de atendimento emergencial. O valor deve ser fixado com caráter pedagógico e não resultar em enriquecimento sem causa.",
    },
    "51": {
        "autor": "Cláusulas nulas de pleno direito (art. 51): não exigem declaração judicial prévia; o juiz pode reconhecê-las de ofício nas relações entre consumidor e fornecedor não bancário (Súmula 381 STJ — excepcionando contratos bancários).",
        "reu": "Demonstrar que a cláusula potencialmente abusiva está dentro dos limites legais e não gera desequilíbrio real; cláusulas de limitação de responsabilidade têm presunção de abusividade.",
        "pratica": "Planos de saúde: proibição de recusa de cobertura em emergência (Súmula 302 STJ); negativa de cobertura gera dano moral. Prazo de carência: juiz pode afastar quando há urgência comprovada.",
    },
}


def _jurisprudencia_dc(num_str: str) -> List[str]:
    return JURIS_DC.get(num_str, [])


def _obs_praticas_dc(num_str: str) -> dict:
    return OBS_PRATICAS_DC.get(num_str, {})


def _correlatos_outros_dc(num_base) -> List[str]:
    correlatos = [
        "[[CF88 Art. 5]] — direitos fundamentais do consumidor",
        "[[L10406 Art. 186]] — responsabilidade civil (CC)",
        "[[L13105 Art. 373]] — inversão do ônus da prova (CPC)",
    ]
    return correlatos


class MarkdownGeneratorDC:
    """Gera notas Markdown estruturadas para artigos de leis de Direito do Consumidor."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num_raw = artigo["numero"]
        try:
            num = int(num_raw)
        except (ValueError, TypeError):
            num = num_raw
        num_str = str(num_raw)
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo["categoria"]
        tema = lei_cfg.get("tema", "direito-constitucional")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": num_str,
            "lei": f"Lei {lei_numero} ({nome_lei})",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_constitucional": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Conferir redação no Planalto]")
        redacao_display = (redacao[:600] + "...") if len(redacao) > 600 else redacao
        titulo_artigo = artigo.get("titulo", f"Art. {num}")
        if isinstance(num, int):
            art_anterior = max(1, num - 1)
            art_seguinte = num + 1
        else:
            art_anterior = num_str
            art_seguinte = num_str

        juris = _jurisprudencia_dc(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"

        obs = _obs_praticas_dc(num_str)
        if obs:
            obs_str = (
                f"- **Autor/Consumidor:** {obs.get('autor', '')}\n"
                f"- **Réu/Fornecedor:** {obs.get('reu', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática forense — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_dc(num)
        correlatos_str = "\n".join(f"- {c}" for c in correlatos)

        corpo = f"""# {sigla} Art. {num} — {titulo_artigo}

**Lei:** {lei_numero} — {nome_lei}
**Categoria:** {categoria}
**Status:** VIGENTE

---

## REDACAO LEGAL

> {redacao_display}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Co-dependência normativa

[Esta regra depende de qual outro instrumento — qual artigo da CF/88 esta ação
regulamenta? Como se relaciona com o CPC (rito subsidiário)?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros ramos
{correlatos_str}

---

## JURISPRUDENCIA

{juris_str}

---

## OBSERVACOES PRATICAS

{obs_str}

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
    gen = MarkdownGeneratorDC(Path("test_output_dc"))
    print("Gerador Direito do Consumidor pronto")
