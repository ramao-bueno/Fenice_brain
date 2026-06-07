#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STF Súmula Processor — Processa múltiplas súmulas/teses e gera output estruturado
Entrada: arquivo com múltiplas súmulas (delimitadas por ---)
Saída: Markdown + JSON em diretórios estruturados
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from stf_sumula_analyzer import STFSumulaAnalyzer
from config_stf_analyzer import (
    STF_OUTPUT_SV, STF_OUTPUT_RG, LOG_FILE, LOG_LEVEL,
    STF_EXPORTS, DEBUG, SAVE_TEXTO_BRUTO, STF_CACHE,
    gerar_chave_primaria, TEMPLATE_MARKDOWN_SV
)

# ─── Logging ────────────────────────────────────────────────────
def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()


class STFSumulaProcessor:
    """Processa múltiplas súmulas/teses do STF"""

    def __init__(self):
        self.sumulas = []
        self.teses_rg = []
        self.total_analisadas = 0
        self.total_erros = 0

    def processar_arquivo(self, caminho_arquivo: Path) -> List[Dict]:
        """
        Processa arquivo com múltiplas súmulas separadas por ---

        Formato esperado:
        ```
        Súmula Vinculante 57 — ...
        [conteúdo]
        ---
        Tema 69 de Repercussão Geral — ...
        [conteúdo]
        ---
        ```
        """
        logger.info(f"Processando arquivo: {caminho_arquivo}")

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            return []

        # Dividir por delimitador ---
        blocos = conteudo.split('---')
        resultados = []

        for idx, bloco in enumerate(blocos, 1):
            bloco = bloco.strip()
            if not bloco:
                continue

            logger.info(f"Processando bloco {idx}...")
            resultado = self._processar_bloco(bloco)
            if resultado:
                resultados.append(resultado)

        logger.info(f"Total processados: {len(resultados)}")
        return resultados

    def _processar_bloco(self, texto: str) -> Optional[Dict]:
        """Analisa um bloco individual de súmula/tese"""
        try:
            analyzer = STFSumulaAnalyzer(texto)
            schema = analyzer.analisar()

            # Salvar texto bruto se em debug
            if SAVE_TEXTO_BRUTO:
                self._salvar_texto_bruto(texto, schema['identificacao']['numero_identificador'])

            # Salvar arquivo markdown
            self._salvar_markdown(schema)

            # Adicionar à lista
            if schema['identificacao']['tipo'] == 'SUMULA_VINCULANTE':
                self.sumulas.append(schema)
            else:
                self.teses_rg.append(schema)

            self.total_analisadas += 1
            logger.info(f"✅ Processada: {schema['identificacao']['numero_identificador']}")

            return schema

        except Exception as e:
            self.total_erros += 1
            logger.error(f"Erro ao processar bloco: {e}")
            return None

    def _salvar_markdown(self, schema: Dict):
        """Salva súmula em formato Markdown com frontmatter"""
        tipo = schema['identificacao']['tipo']
        numero = schema['identificacao']['numero_identificador']
        chave_primaria = gerar_chave_primaria(tipo, numero)

        # Determinar diretório de saída
        if tipo == 'SUMULA_VINCULANTE':
            output_dir = STF_OUTPUT_SV
            tipo_format = "Súmula Vinculante"
        else:
            output_dir = STF_OUTPUT_RG
            tipo_format = "Tema de Repercussão Geral"

        # Filename
        filename = f"{chave_primaria}.md"
        filepath = output_dir / filename

        # Montar conteúdo markdown
        artigos_lista = "\n".join(
            [f"- {art}" for art in schema['ancoragem_legal']['artigos_crfb88']]
        ) or "- Não explicitado"

        leis_lista = "\n".join(
            [f"- {lei}" for lei in schema['ancoragem_legal']['leis_infraconstitucionais_afetadas']]
        ) or "- Não explicitado"

        modulacao_condicional = ""
        if schema['modulacao_efeitos']['houve_modulacao']:
            modulacao_condicional = f"""
### ⚠️ REGRA DA MODULAÇÃO

{schema['modulacao_efeitos']['regra_da_modulacao']}

**Impacto:** Empresas/órgãos públicos devem revisar atos praticados ANTES dessa data
para compliance. Possível trigger: auditar processos em andamento.
"""

        keywords_lista = ", ".join(
            [f"#{kw}" for kw in schema['vetorizacao_keywords']]
        ) if schema['vetorizacao_keywords'] else "#stf #jurisprudencia"

        corpo = f"""# {numero} — {tipo_format}

**Processo Paradigma:** {schema['identificacao']['processo_paradigma'] or "N/A"}
**Data de Publicação:** {schema['identificacao']['data_publicacao_dje'] or "N/A"}
**Chave Primária:** `{chave_primaria}`

---

## 📋 ENUNCIADO

> {schema['conteudo_textual']['enunciado_original'][:300]}...

---

## 🎯 NÚCLEO DA TESE

{schema['conteudo_textual']['nucleo_da_tese']}

---

## ⚖️ ANCORAGEM LEGAL

### Dispositivos Constitucionais

{artigos_lista}

### Leis Infraconstitucionais

{leis_lista}

---

## 🔄 MODULAÇÃO DE EFEITOS

**Houve Modulação?** {"✅ SIM" if schema['modulacao_efeitos']['houve_modulacao'] else "❌ NÃO"}

{modulacao_condicional if schema['modulacao_efeitos']['houve_modulacao'] else "Nenhuma modulação especial. A tese vale para todos os casos posteriores à publicação."}

---

## 💼 IMPACTO BUSINESS & COMPLIANCE

**Setor Afetado:** {schema['impacto_business_compliance']['setor_afetado']}
**Potencial de Impacto:** {schema['impacto_business_compliance']['potencial_monetario']}

### Vulnerabilidade de Compliance

{schema['impacto_business_compliance']['vulnerabilidade_compliance']}

---

## 🔍 PALAVRAS-CHAVE (RAG/Busca Semântica)

{keywords_lista}

---

**Análise gerada em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Confiabilidade:** {schema['metadata']['confiabilidade']}
**Status:** {schema['identificacao']['status_atual']}
**Revisar manualmente:** {"SIM" if schema['metadata']['requer_revisao_manual'] else "NÃO"}
"""

        try:
            filepath.write_text(corpo, encoding='utf-8')
            logger.info(f"Salvo: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar {filepath}: {e}")

    def _salvar_texto_bruto(self, texto: str, numero: str):
        """Salva texto bruto para debug"""
        nome = numero.replace(' ', '_')[:50] + '.txt'
        filepath = STF_CACHE / nome

        try:
            filepath.write_text(texto, encoding='utf-8')
        except Exception as e:
            logger.warning(f"Erro ao salvar texto bruto: {e}")

    def exportar_json_completo(self, nome_arquivo: str = "stf_sumulas_export.json"):
        """Exporta todas as súmulas em um JSON único"""
        filepath = STF_EXPORTS / nome_arquivo

        dados_combinadas = {
            "sumulas_vinculantes": self.sumulas,
            "teses_repercussao_geral": self.teses_rg,
            "metadata": {
                "total_analisadas": self.total_analisadas,
                "total_erros": self.total_erros,
                "exportado_em": datetime.now().isoformat(),
                "versao": "1.0"
            }
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dados_combinadas, f, indent=2, ensure_ascii=False)

            logger.info(f"JSON exportado: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")
            return None

    def relatorio_resumido(self) -> Dict:
        """Gera relatório resumido de processamento"""
        return {
            "total_sumulas_vinculantes": len(self.sumulas),
            "total_teses_rg": len(self.teses_rg),
            "total_analisadas": self.total_analisadas,
            "total_erros": self.total_erros,
            "taxa_sucesso": f"{(self.total_analisadas - self.total_erros) / max(self.total_analisadas, 1) * 100:.1f}%",
            "arquivos_criados_sv": len(list(STF_OUTPUT_SV.glob('*.md'))),
            "arquivos_criados_rg": len(list(STF_OUTPUT_RG.glob('*.md'))),
            "processado_em": datetime.now().isoformat()
        }


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("📊 STF SÚMULA PROCESSOR — Análise em Massa de SV + RG")
    print("="*70 + "\n")

    processor = STFSumulaProcessor()

    # Buscar arquivo de entrada
    arquivo_entrada = Path("sumulas_input.txt")
    if not arquivo_entrada.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        print(f"   Crie um arquivo 'sumulas_input.txt' com súmulas delimitadas por ---")
        return False

    # Processar
    resultados = processor.processar_arquivo(arquivo_entrada)

    # Exportar JSON
    processor.exportar_json_completo()

    # Relatório
    relatorio = processor.relatorio_resumido()

    print(f"\n{'='*70}")
    print(f"✅ PROCESSAMENTO COMPLETO!")
    print(f"{'='*70}")
    print(f"\n📊 ESTATÍSTICAS:")
    for chave, valor in relatorio.items():
        print(f"   • {chave.replace('_', ' ').title()}: {valor}")

    print(f"\n📁 OUTPUT:")
    print(f"   • Súmulas Vinculantes: {STF_OUTPUT_SV}")
    print(f"   • Teses RG: {STF_OUTPUT_RG}")
    print(f"   • JSON Export: {STF_EXPORTS}\n")

    return len(resultados) > 0


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
