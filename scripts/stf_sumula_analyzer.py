#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STF Súmula Vinculante / Tese de Repercussão Geral Analyzer
Converte texto bruto para JSON estruturado com análise constitucional + impacto business
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# ─── Mapas de Referência ────────────────────────────────────────
ARTIGOS_CRFB88 = {
    r"\bArt\.\s*1\b": "Art. 1 (Fundamentos da República)",
    r"\bArt\.\s*2\b": "Art. 2 (Harmonia entre Poderes)",
    r"\bArt\.\s*3\b": "Art. 3 (Objetivos Fundamentais)",
    r"\bArt\.\s*4\b": "Art. 4 (Princípios nas Relações Internacionais)",
    r"\bArt\.\s*5\b": "Art. 5 (Direitos Fundamentais)",
    r"\bArt\.\s*6\b": "Art. 6 (Direitos Sociais)",
    r"\bArt\.\s*7\b": "Art. 7 (Direitos dos Trabalhadores)",
    r"\bArt\.\s*8\b": "Art. 8 (Associações Profissionais e Sindicatos)",
    r"\bArt\.\s*9\b": "Art. 9 (Direito de Greve)",
    r"\bArt\.\s*10\b": "Art. 10 (Participação de Representantes)",
    r"\bArt\.\s*37\b": "Art. 37 (Administração Pública)",
    r"\bArt\.\s*39\b": "Art. 39 (Servidores Públicos)",
    r"\bArt\.\s*40\b": "Art. 40 (Regime Próprio de Previdência)",
    r"\bArt\.\s*41\b": "Art. 41 (Estabilidade do Servidor)",
    r"\bArt\.\s*88\b": "Art. 88 (Disposição Transitória)",
    r"\bArt\.\s*97\b": "Art. 97 (Princípio da Maioria Absoluta)",
    r"\bArt\.\s*102\b": "Art. 102 (Competência STF)",
    r"\bArt\.\s*103\b": "Art. 103 (Ação Direta de Inconstitucionalidade)",
    r"\bArt\.\s*119\b": "Art. 119 (Superior Tribunal de Justiça)",
    r"\bArt\.\s*133\b": "Art. 133 (Advocacia)",
    r"\bArt\.\s*134\b": "Art. 134 (Defensoria Pública)",
    r"\bArt\.\s*137\b": "Art. 137 (Ministério Público)",
    r"\bArt\.\s*150\b": "Art. 150 (Limitações do Poder de Tributar)",
    r"\bArt\.\s*155\b": "Art. 155 (Impostos dos Estados)",
    r"\bArt\.\s*156\b": "Art. 156 (Impostos dos Municípios)",
    r"\bArt\.\s*194\b": "Art. 194 (Seguridade Social)",
    r"\bArt\.\s*195\b": "Art. 195 (Financiamento da Seguridade)",
    r"\bArt\.\s*196\b": "Art. 196 (Direito à Saúde)",
    r"\bArt\.\s*201\b": "Art. 201 (Regime Geral de Previdência)",
    r"\bArt\.\s*202\b": "Art. 202 (Previdência Privada)",
    r"\bArt\.\s*226\b": "Art. 226 (Família, Criança e Adolescente)",
    r"\bArt\.\s*227\b": "Art. 227 (Proteção à Criança e Adolescente)",
}

SETORES_AFETACAO = {
    "previdenciário": ["INSS", "aposentadoria", "pensão", "benefício previdenciário", "contribuição"],
    "trabalhista": ["celetista", "vínculo", "demissão", "estabilidade", "CLT", "aviso prévio"],
    "tributário": ["IRPJ", "ICMS", "ISS", "IPI", "PIS", "COFINS", "tributo", "imposto", "taxa"],
    "administrativo": ["servidor", "público", "funcionário", "cargo", "função pública"],
    "consumidor": ["consumidor", "fornecedor", "produto", "serviço", "relação de consumo"],
    "penal": ["crime", "delito", "pena", "condenação", "processo criminal"],
    "civil": ["contrato", "obrigação", "responsabilidade", "dano", "indenização"],
    "processual": ["ação", "processo", "recurso", "jurisdição", "competência"],
}

@dataclass
class Identificacao:
    tipo: str  # SUMULA_VINCULANTE | REPERCUSSAO_GERAL
    numero_identificador: str
    processo_paradigma: Optional[str]
    data_publicacao_dje: Optional[str]
    status_atual: str

@dataclass
class ConteudoTextual:
    enunciado_original: str
    nucleo_da_tese: str

@dataclass
class AncoragemLegal:
    artigos_crfb88: List[str]
    leis_infraconstitucionais_afetadas: List[str]

@dataclass
class ModulacaoEfeitos:
    houve_modulacao: bool
    regra_da_modulacao: Optional[str]

@dataclass
class ImpactoBusinessCompliance:
    setor_afetado: str
    vulnerabilidade_compliance: str
    potencial_monetario: str  # HIGH | MEDIUM | LOW

class STFSumulaAnalyzer:
    """Analisador de Súmulas Vinculantes e Teses de RG do STF"""

    def __init__(self, texto_bruto: str):
        self.texto_original = texto_bruto
        self.texto_limpo = self._limpar_texto(texto_bruto)

    def _limpar_texto(self, texto: str) -> str:
        """Remove preâmbulos, nomes de ministros, formatação estranha"""
        # Remove cabeçalho típico do STF
        texto = re.sub(
            r"^.*?(SUPREMO TRIBUNAL FEDERAL|Súmula Vinculante|Tema de Repercussão Geral|RE \d+|ADI \d+)",
            r"\1",
            texto,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove nomes de ministros votantes
        texto = re.sub(
            r"(Relator|Voto|Votação|Ministro|Min\.|Desembargador)\s*[:\s]*[A-Z][a-záéíóúàâêôãõç\s\.]+",
            "",
            texto,
            flags=re.IGNORECASE
        )

        # Remove múltiplos espaços/quebras
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()

    def _detectar_tipo(self) -> str:
        """Detecta se é SV ou Tema de Repercussão Geral"""
        if re.search(r"Súmula Vinculante|SV\s*\d+", self.texto_limpo, re.IGNORECASE):
            return "SUMULA_VINCULANTE"
        elif re.search(r"Tema.*Repercussão Geral|Tema\s*\d+", self.texto_limpo, re.IGNORECASE):
            return "REPERCUSSAO_GERAL"
        return "REPERCUSSAO_GERAL"  # Default

    def _extrair_numero_identificador(self) -> str:
        """Extrai SV XXX ou Tema XXX"""
        # Busca SV
        match = re.search(r"SV\s*(\d+)", self.texto_limpo, re.IGNORECASE)
        if match:
            return f"SV {match.group(1)}"

        # Busca Tema
        match = re.search(r"Tema\s*(\d+)", self.texto_limpo, re.IGNORECASE)
        if match:
            return f"Tema {match.group(1)}"

        return "SEM_NUMERO"

    def _extrair_processo_paradigma(self) -> Optional[str]:
        """Extrai RE XXXX, ADI XXXX, etc"""
        patterns = [
            r"(RE|ADI|AGR|ARE|AI|AP|RvC|SL|MI)\s*(\d+(?:\.\d+)?)",
            r"(Recurso Extraordinário|Ação Direta de Inconstitucionalidade)\s*(\d+(?:\.\d+)?)"
        ]

        for pattern in patterns:
            match = re.search(pattern, self.texto_limpo, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"

        return None

    def _extrair_data_publicacao(self) -> Optional[str]:
        """Extrai data de publicação no DJe"""
        pattern = r"(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})"
        match = re.search(pattern, self.texto_limpo, re.IGNORECASE)

        if match:
            dia, mes_nome, ano = match.groups()
            meses = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
                'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            mes = meses.get(mes_nome.lower(), 1)
            try:
                return f"{ano}-{mes:02d}-{int(dia):02d}"
            except:
                pass

        return None

    def _extrair_artigos_crfb88(self) -> List[str]:
        """Extrai artigos da CF/88 citados"""
        artigos_encontrados = []

        for pattern, descricao in ARTIGOS_CRFB88.items():
            if re.search(pattern, self.texto_limpo, re.IGNORECASE):
                if descricao not in artigos_encontrados:
                    artigos_encontrados.append(descricao)

        return artigos_encontrados if artigos_encontrados else ["Não explicitado"]

    def _extrair_leis_infraconstitucionais(self) -> List[str]:
        """Extrai leis e códigos mencionados"""
        leis = []

        patterns = [
            r"Lei\s*(\d+\.\d+/\d+|\d+/\d+)",
            r"(Lei de Introdução|Código Civil|Código de Processo Civil|CLT|CPC|CC|CP)",
            r"(Código Penal|Lei de Execução Penal|Estatuto do Servidor|Lei 8.112)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, self.texto_limpo, re.IGNORECASE)
            for match in matches:
                lei = match.group(0)
                if lei not in leis:
                    leis.append(lei)

        return leis if leis else ["Não explicitado"]

    def _extrair_modulacao(self) -> Tuple[bool, Optional[str]]:
        """Detecta e extrai modulação de efeitos"""
        modulacao_keywords = [
            r"modulação.*efeitos",
            r"efeitos.*a partir de",
            r"salvaguardadas?.*ações",
            r"ressalvadas?.*ações",
            r"não.*retroage",
            r"prospectivo",
            r"marco temporal",
            r"data da publicação",
            r"data do acórdão",
            r"atos praticados",
        ]

        for keyword in modulacao_keywords:
            if re.search(keyword, self.texto_limpo, re.IGNORECASE):
                # Extrai a regra específica
                pattern = r"((?:modulação|efeitos|salvaguardadas?|ressalvadas?|prospectivo|marco temporal)[^.!?]*(?:[.!?]|$))"
                match = re.search(pattern, self.texto_limpo, re.IGNORECASE)
                if match:
                    regra = match.group(1).strip()
                    return (True, regra[:300])  # Limita a 300 chars
                return (True, "Modulação de efeitos aplicada, detalhes a revisar manualmente")

        return (False, None)

    def _detectar_setor_afetado(self) -> str:
        """Detecta setor afetado pela tese"""
        texto_lower = self.texto_limpo.lower()

        for setor, keywords in SETORES_AFETACAO.items():
            for keyword in keywords:
                if keyword.lower() in texto_lower:
                    return setor.upper()

        return "GERAL"

    def _estimar_potencial_monetario(self) -> str:
        """Estima impacto financeiro"""
        texto_lower = self.texto_limpo.lower()

        # HIGH: tributário, previdenciário, grandes causas
        if any(kw in texto_lower for kw in ['tributo', 'imposto', 'icms', 'irpj', 'pis', 'cofins', 'inss', 'aposentadoria', 'pensão', 'contribuição']):
            return "HIGH"

        # MEDIUM: trabalhista, dano moral, responsabilidade
        if any(kw in texto_lower for kw in ['trabalhista', 'CLT', 'celetista', 'indenização', 'dano', 'responsabilidade']):
            return "MEDIUM"

        # LOW: procedural, direitos políticos, etc
        return "LOW"

    def _extrair_keywords(self) -> List[str]:
        """Extrai palavras-chave para RAG/busca semântica"""
        keywords = set()

        # Palavras jurídicas importantes
        juridicas = [
            r"\b(direito|dever|obrigação|responsabilidade|competência|jurisdição)\b",
            r"\b(constitucional|inconstitucional|nulo|válido|invalidade)\b",
            r"\b(trabalhista|tributário|previdenciário|processual)\b",
            r"\b(modulação|efeitos|vigência|eficácia|aplicação)\b",
        ]

        for pattern in juridicas:
            matches = re.finditer(pattern, self.texto_limpo, re.IGNORECASE)
            for match in matches:
                keywords.add(match.group(1).lower())

        # Artigos mencionados
        for pattern in ["SV", "Tema", "RE", "ADI"]:
            if pattern in self.texto_limpo:
                keywords.add(pattern.lower())

        # Setor afetado
        setor = self._detectar_setor_afetado()
        if setor != "GERAL":
            keywords.add(setor.lower())

        return sorted(list(keywords))

    def _resumo_executivo(self) -> str:
        """Gera resumo executivo da tese em linguagem comercial"""
        # Extrai primeira frase ou parágrafo significativo
        frases = re.split(r'[.!?]\s+', self.texto_limpo)

        if frases:
            # Remove frases muito curtas
            resumo = next((f.strip() for f in frases if len(f) > 50), frases[0])
            # Limita a 200 caracteres
            return resumo[:200] + "..." if len(resumo) > 200 else resumo

        return "Resumo não disponível"

    def analisar(self) -> Dict:
        """Executa análise completa e retorna JSON estruturado"""

        tipo = self._detectar_tipo()
        numero = self._extrair_numero_identificador()
        processo = self._extrair_processo_paradigma()
        data = self._extrair_data_publicacao()
        artigos = self._extrair_artigos_crfb88()
        leis = self._extrair_leis_infraconstitucionais()
        modulacao_bool, modulacao_regra = self._extrair_modulacao()
        setor = self._detectar_setor_afetado()
        potencial = self._estimar_potencial_monetario()
        keywords = self._extrair_keywords()
        resumo = self._resumo_executivo()

        # Construir vulnerabilidade de compliance
        vulnerabilidade = f"Empresas e órgãos públicos afetados pelo setor {setor.lower()} precisam se adequar imediatamente aos termos dessa tese. "
        if modulacao_bool:
            vulnerabilidade += f"Atenção especial: há modulação de efeitos. {modulacao_regra}"
        else:
            vulnerabilidade += "A tese tem eficácia imediata a todos os atos posteriores à publicação."

        # Montar schema
        schema = {
            "identificacao": asdict(Identificacao(
                tipo=tipo,
                numero_identificador=numero,
                processo_paradigma=processo,
                data_publicacao_dje=data,
                status_atual="ATIVO"  # Default, pode ser atualizado
            )),
            "conteudo_textual": asdict(ConteudoTextual(
                enunciado_original=self.texto_original[:500],
                nucleo_da_tese=resumo
            )),
            "ancoragem_legal": asdict(AncoragemLegal(
                artigos_crfb88=artigos,
                leis_infraconstitucionais_afetadas=leis
            )),
            "modulacao_efeitos": asdict(ModulacaoEfeitos(
                houve_modulacao=modulacao_bool,
                regra_da_modulacao=modulacao_regra
            )),
            "impacto_business_compliance": asdict(ImpactoBusinessCompliance(
                setor_afetado=setor,
                vulnerabilidade_compliance=vulnerabilidade,
                potencial_monetario=potencial
            )),
            "vetorizacao_keywords": keywords,
            "metadata": {
                "analisado_em": datetime.now().isoformat(),
                "confiabilidade": "0.8",
                "requer_revisao_manual": modulacao_bool or tipo == "SUMULA_VINCULANTE"
            }
        }

        return schema


if __name__ == "__main__":
    import sys

    # Teste com exemplo de SV
    exemplo_sv = """
    Súmula Vinculante 57 — SUPREMO TRIBUNAL FEDERAL
    Processo: RE 574.706
    Publicado no DJe de 19 de dezembro de 2008

    O direito de greve dos servidores públicos será exercido nos termos e limites
    definidos em lei complementar federal.

    Relator: Ministro Carlos Britto
    """

    analyzer = STFSumulaAnalyzer(exemplo_sv)
    resultado = analyzer.analisar()

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
