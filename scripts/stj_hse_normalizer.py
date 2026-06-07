"""
STJ HSE Normalizer — Converte decisões HSE para schema JSON padronizado
"""

import re
import json
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict

@dataclass
class MetadadosProcessuais:
    numero_processo: str
    relator: str
    orgao_julgador: str
    data_julgamento: str
    pais_de_origem: str

@dataclass
class ResultadoHomologacao:
    status: str  # DEFERIDO | INDEFERIDO | PARCIALMENTE DEFERIDO
    fundamento_principal: str

@dataclass
class ChecklistRequisitos:
    transito_em_julgado_comprovado: bool
    citacao_valida: bool
    violacao_ordem_publica: bool
    incompetencia_absoluta_brasil: bool

@dataclass
class AnalisCoercitiva:
    objeto_da_decisao: str
    detalhe_da_citacao: str
    tese_juridica_fixada: str

@dataclass
class RiscoCompliance:
    score_complexidade: str  # LOW | MEDIUM | HIGH
    observacao_critica: str

class STJHSENormalizer:
    """Normaliza decisões HSE do STJ para schema padronizado"""

    # Meses em português para inglês
    MESES = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
        'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
        'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }

    # Palavras-chave para detecção
    DEFERIDO_KEYWORDS = ['homolog', 'defer', 'foi', 'sentença']
    INDEFERIDO_KEYWORDS = ['indeferir', 'negar', 'não', 'rejeita']
    PARCIAL_KEYWORDS = ['parcial', 'em parte', 'quanto']

    ORDEM_PUBLICA_KEYWORDS = [
        'ordem pública', 'fundamental', 'violação', 'inconstitucional',
        'bons costumes', 'direitos humanos', 'consumidor'
    ]

    INCOMPETENCIA_KEYWORDS = ['competência', 'privativa', 'exclusiva']

    def __init__(self, html_texto: str):
        self.texto = html_texto
        self.texto_limpo = self._limpar_html(html_texto)

    def _limpar_html(self, html: str) -> str:
        """Remove tags HTML e normaliza espaços"""
        import re
        texto = re.sub(r'<[^>]+>', ' ', html)
        texto = re.sub(r'&nbsp;', ' ', texto)
        texto = re.sub(r'&amp;', '&', texto)
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()

    def _extrair_numero_processo(self) -> str:
        """Extrai número da HSE (HDE XXXX)"""
        match = re.search(r'HDE\s*(\d+(?:\.\d+)?)', self.texto_limpo, re.IGNORECASE)
        return f"HDE {match.group(1)}" if match else "SEM_NUMERO"

    def _extrair_relator(self) -> str:
        """Extrai nome do relator"""
        patterns = [
            r'Relator\s*[:\-\s]+([A-Za-z\s\.]+?)(?:;|,|\n|$)',
            r'Min\.\s+([A-Za-z\s\.]+?)(?:;|,|\n|$)'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.texto_limpo, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "SEM_RELATOR"

    def _extrair_data_julgamento(self) -> str:
        """Extrai data do julgamento (DD de mês de YYYY)"""
        pattern = r'(\d{1,2})\s+de\s+([a-záéíóúàâêôãõç]+)\s+de\s+(\d{4})'
        match = re.search(pattern, self.texto_limpo, re.IGNORECASE)

        if match:
            dia, mes_nome, ano = match.groups()
            mes_nome = mes_nome.lower()
            mes_num = self.MESES.get(mes_nome, 1)

            try:
                date = datetime(int(ano), mes_num, int(dia))
                return date.strftime('%Y-%m-%d')
            except:
                return f"{ano}-{mes_num:02d}-{dia:02d}"

        return datetime.now().strftime('%Y-%m-%d')

    def _extrair_pais_origem(self) -> str:
        """Extrai país de origem da decisão estrangeira"""
        # Busca por padrões de país
        patterns = [
            r'(?:em|do|da|de)\s+(?:República\s+)?([A-Z][a-záéíóúàâêôãõç\s]+?)(?:\.|;|,|país)',
            r'(?:estrangeira|exterior).*?(?:em|do)\s+([A-Z][a-záéíóúàâêôãõç\s]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, self.texto_limpo, re.IGNORECASE)
            if match:
                pais = match.group(1).strip()
                # Limpa sufixos comuns
                pais = re.sub(r'\s+(?:de|dos?|da|das)\s+$', '', pais)
                return pais

        return "SEM_PAIS"

    def _extrair_resultado(self) -> str:
        """Detecta se foi DEFERIDO, INDEFERIDO ou PARCIALMENTE DEFERIDO"""
        texto_lower = self.texto_limpo.lower()

        # Verifica PARCIAL primeiro (mais específico)
        for keyword in self.PARCIAL_KEYWORDS:
            if keyword in texto_lower and any(k in texto_lower for k in self.DEFERIDO_KEYWORDS):
                return "PARCIALMENTE DEFERIDO"

        # Verifica DEFERIDO
        for keyword in self.DEFERIDO_KEYWORDS:
            if keyword in texto_lower:
                return "DEFERIDO"

        # Verifica INDEFERIDO
        for keyword in self.INDEFERIDO_KEYWORDS:
            if keyword in texto_lower:
                return "INDEFERIDO"

        return "INDEFINIDO"

    def _extrair_fundamento(self) -> str:
        """Extrai fundamento principal (primeiros 200 chars do texto relevante)"""
        # Busca por seção de fundamentos
        match = re.search(
            r'(?:VISTOS|CONSIDERANDO|FUNDAMENTOS?)[.:]\s*(.{1,300}?)(?:\n\n|$)',
            self.texto_limpo,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            texto = match.group(1).strip()
            return texto[:200] if len(texto) > 200 else texto

        return "Fundamento não extraído"

    def _extrair_checklist(self) -> ChecklistRequisitos:
        """Extrai presença dos 4 requisitos legais"""
        texto_lower = self.texto_limpo.lower()

        # Transito em julgado
        transito = any(kw in texto_lower for kw in ['transito', 'transitado', 'definitivo'])

        # Citação válida
        citacao = any(kw in texto_lower for kw in ['citação', 'citado', 'notificado', 'revelia'])

        # Violação de ordem pública (TRUE = viola)
        violacao = any(kw in texto_lower for kw in self.ORDEM_PUBLICA_KEYWORDS)

        # Incompetência absoluta do Brasil (TRUE = há incompetência)
        incompetencia = any(kw in texto_lower for kw in self.INCOMPETENCIA_KEYWORDS)

        return ChecklistRequisitos(
            transito_em_julgado_comprovado=transito,
            citacao_valida=citacao,
            violacao_ordem_publica=violacao,
            incompetencia_absoluta_brasil=incompetencia
        )

    def _extrair_objeto(self) -> str:
        """Detecta o objeto da decisão (Alimentos, Divórcio, Arbitral, Cobrança)"""
        texto_lower = self.texto_limpo.lower()

        if 'alimento' in texto_lower:
            return "Alimentos"
        elif 'divórcio' in texto_lower or 'dissolução' in texto_lower:
            return "Divórcio Qualificado"
        elif 'arbitr' in texto_lower or 'laudo' in texto_lower:
            return "Sentença Arbitral Comercial"
        elif 'cobrança' in texto_lower or 'dívida' in texto_lower:
            return "Cobrança"
        else:
            return "Outra matéria"

    def _calcular_risco(self, resultado: str, checklist: ChecklistRequisitos) -> str:
        """Calcula score de complexidade LOW/MEDIUM/HIGH"""

        # HIGH: indeferido ou violação de ordem pública
        if resultado == "INDEFERIDO":
            return "HIGH"

        if checklist.violacao_ordem_publica:
            return "HIGH"

        # MEDIUM: parcialmente deferido ou incompetência
        if resultado == "PARCIALMENTE DEFERIDO":
            return "MEDIUM"

        if checklist.incompetencia_absoluta_brasil:
            return "MEDIUM"

        # LOW: tudo ok, deferido sem problemas
        return "LOW"

    def normalizar(self) -> Dict:
        """Converte para schema JSON completo"""

        # Extrai componentes
        numero = self._extrair_numero_processo()
        relator = self._extrair_relator()
        data = self._extrair_data_julgamento()
        pais = self._extrair_pais_origem()
        resultado = self._extrair_resultado()
        fundamento = self._extrair_fundamento()
        checklist = self._extrair_checklist()
        objeto = self._extrair_objeto()
        risco = self._calcular_risco(resultado, checklist)

        # Monta schema
        schema = {
            "metadados_processuais": asdict(MetadadosProcessuais(
                numero_processo=numero,
                relator=relator,
                orgao_julgador="CORTE ESPECIAL",
                data_julgamento=data,
                pais_de_origem=pais
            )),
            "resultado_homologacao": asdict(ResultadoHomologacao(
                status=resultado,
                fundamento_principal=fundamento
            )),
            "checklist_requisitos": asdict(checklist),
            "analise_coercitiva": asdict(AnalisCoercitiva(
                objeto_da_decisao=objeto,
                detalhe_da_citacao="[A extrair do texto completo]",
                tese_juridica_fixada="[A extrair da fundamentação]"
            )),
            "risco_compliance": asdict(RiscoCompliance(
                score_complexidade=risco,
                observacao_critica="Análise automática — revisar manualmente"
            )),
            "metadata": {
                "normalizado_em": datetime.now().isoformat(),
                "fonte": "STJ SCON",
                "confiabilidade": "0.7"  # Score de confiança da extração
            }
        }

        return schema


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    # Teste
    html_teste = """
    HDE 1.234
    Relator: Ministro João Silva
    Julgamento: 15 de junho de 2026
    Origem: Portugal
    VISTOS. Trata-se de homologação de sentença estrangeira...
    HOMOLOGADA a sentença estrangeira...
    """

    normalizer = STJHSENormalizer(html_teste)
    resultado = normalizer.normalizar()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
