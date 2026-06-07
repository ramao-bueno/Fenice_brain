#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STJ HSE Scraper — Extrai Homologações de Sentença Estrangeira do STJ
Busca: https://www.stj.jus.br/SCON
Normaliza: schema JSON + salva em Fenice Brain
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import requests
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import time

# Imports locais
from config_stj_scraper import (
    STJ_SCON_SEARCH, HEADERS, TIMEOUT_REQUEST, MAX_RETRIES, RETRY_DELAY,
    RESULTADOS_POR_PAGINA, MAX_PAGINAS, HSE_OUTPUT, HSE_CACHE,
    LOG_FILE, LOG_LEVEL, USE_CACHE, CACHE_EXPIRY_DAYS, SAVE_HTML_BRUTO
)
from stj_hse_normalizer import STJHSENormalizer


# ─── Logging ────────────────────────────────────────────────
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


class STJHSEScraper:
    """Scraper para HSE do STJ"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.hse_list = []

    def buscar_hse(self, filtros: Optional[Dict] = None, paginas: int = 1) -> List[Dict]:
        """
        Busca HSE no STJ SCON

        Args:
            filtros: dict com filtros de busca (opcional)
            paginas: número de páginas a buscar

        Returns:
            List de decisões HSE normalizadas
        """
        logger.info(f"Iniciando busca HSE — {paginas} páginas")

        for pagina in range(1, min(paginas + 1, MAX_PAGINAS + 1)):
            logger.info(f"Buscando página {pagina}...")

            try:
                # Monta URL com parâmetros
                params = {
                    'b': 'VERDICTBRS',
                    'livre': 'HDE',
                    'tipo': 'ACRDO',
                    'p': pagina,
                    'n': RESULTADOS_POR_PAGINA,
                    'ordem': 'DESC'
                }

                # Faz requisição
                response = self.session.get(
                    STJ_SCON_SEARCH,
                    params=params,
                    timeout=TIMEOUT_REQUEST
                )
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Busca links de decisões
                links_decisoes = self._extrair_links_decisoes(soup)
                logger.info(f"Página {pagina}: encontrados {len(links_decisoes)} resultados")

                if not links_decisoes:
                    logger.warning(f"Nenhum resultado na página {pagina}, parando...")
                    break

                # Para cada link, busca e normaliza
                for idx, link in enumerate(links_decisoes, 1):
                    logger.info(f"  [{idx}/{len(links_decisoes)}] Buscando {link}...")
                    self._buscar_e_normalizar(link)
                    time.sleep(1)  # Rate limiting

            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao buscar página {pagina}: {e}")
                continue

        logger.info(f"Busca completa: {len(self.hse_list)} HSEs extraídas")
        return self.hse_list

    def _extrair_links_decisoes(self, soup: BeautifulSoup) -> List[str]:
        """Extrai links de decisões da página de resultados"""
        links = []

        # Procura por links no formato do STJ
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            # Links de decisão contêm '/SCON/' e 'p='
            if '/SCON/' in href and 'p=' in href:
                if href not in links:  # Evita duplicatas
                    links.append(href)

        return links

    def _buscar_e_normalizar(self, url: str):
        """Busca uma decisão específica e normaliza"""
        try:
            # Trata URL relativa
            if not url.startswith('http'):
                url = f"https://www.stj.jus.br{url}"

            # Busca com retry
            response = None
            for tentativa in range(MAX_RETRIES):
                try:
                    response = self.session.get(url, timeout=TIMEOUT_REQUEST)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if tentativa < MAX_RETRIES - 1:
                        logger.warning(f"Tentativa {tentativa + 1} falhou, retry...")
                        time.sleep(RETRY_DELAY)
                    else:
                        raise

            if not response:
                return

            # Salva HTML bruto (para debug)
            if SAVE_HTML_BRUTO:
                self._salvar_html_bruto(url, response.text)

            # Normaliza
            normalizer = STJHSENormalizer(response.text)
            schema = normalizer.normalizar()

            # Salva arquivo MD
            self._salvar_hse_markdown(schema)

            # Adiciona à lista
            self.hse_list.append(schema)

            logger.info(f"✅ Normalizada: {schema['metadados_processuais']['numero_processo']}")

        except Exception as e:
            logger.error(f"Erro ao processar {url}: {e}")

    def _salvar_hse_markdown(self, schema: Dict):
        """Salva HSE em formato Markdown com frontmatter"""
        numero = schema['metadados_processuais']['numero_processo'].replace(' ', '-')
        filename = f"{numero}.md"
        filepath = HSE_OUTPUT / filename

        # Monta frontmatter YAML
        frontmatter = f"""---
artigo: {schema['metadados_processuais']['numero_processo']}
lei: "Superior Tribunal de Justiça — HSE"
tipo: homologacao-sentenca-estrangeira
relator: {schema['metadados_processuais']['relator']}
pais_origem: {schema['metadados_processuais']['pais_de_origem']}
data_julgamento: {schema['metadados_processuais']['data_julgamento']}
status: {schema['resultado_homologacao']['status']}
risco_compliance: {schema['risco_compliance']['score_complexidade']}
tags:
  - stj
  - hse
  - homologacao
  - sentenca-estrangeira
  - {schema['analise_coercitiva']['objeto_da_decisao'].lower().replace(' ', '-')}
created: {datetime.now().strftime('%Y-%m-%d')}
---

"""

        # Monta corpo
        corpo = f"""# {schema['metadados_processuais']['numero_processo']} — HSE

**Relator:** {schema['metadados_processuais']['relator']}
**Data:** {schema['metadados_processuais']['data_julgamento']}
**País de Origem:** {schema['metadados_processuais']['pais_de_origem']}
**Status:** {schema['resultado_homologacao']['status']}

---

## 📋 REDAÇÃO LEGAL

> {schema['resultado_homologacao']['fundamento_principal']}

---

## ⚖️ ANÁLISE DA HOMOLOGAÇÃO

### Requisitos Legais

| Requisito | Status |
|---|---|
| Trânsito em Julgado | {"✅" if schema['checklist_requisitos']['transito_em_julgado_comprovado'] else "❌"} |
| Citação Válida | {"✅" if schema['checklist_requisitos']['citacao_valida'] else "❌"} |
| Não Viola Ordem Pública | {"✅" if not schema['checklist_requisitos']['violacao_ordem_publica'] else "❌"} |
| Competência do Brasil | {"✅" if not schema['checklist_requisitos']['incompetencia_absoluta_brasil'] else "❌"} |

### Objeto da Decisão

{schema['analise_coercitiva']['objeto_da_decisao']}

### Risco de Compliance

**Score:** {schema['risco_compliance']['score_complexidade']}

{schema['risco_compliance']['observacao_critica']}

---

## 🔗 ARTIGOS CORRELATOS

- [[CPC Arts. 960-965]] — Homologação de sentença estrangeira
- [[CC Arts. 1-10]] — Aplicabilidade de lei estrangeira
- [[CF/88 Art. 5]] — Ordem pública (direitos fundamentais)

---

**Extraído em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (automático)
**Confiabilidade:** {schema['metadata']['confiabilidade']}
"""

        # Escreve arquivo
        try:
            filepath.write_text(frontmatter + corpo, encoding='utf-8')
            logger.info(f"Salvo: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar {filepath}: {e}")

    def _salvar_html_bruto(self, url: str, html: str):
        """Salva HTML bruto para debugging"""
        nome = url.split('/')[-1][:50] + '.html'
        filepath = HSE_CACHE / nome

        try:
            filepath.write_text(html, encoding='utf-8')
        except Exception as e:
            logger.warning(f"Erro ao salvar HTML bruto: {e}")

    def salvar_json_completo(self, filename: str = "hse_export.json"):
        """Salva todas as HSEs em um JSON único"""
        filepath = HSE_OUTPUT / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.hse_list, f, indent=2, ensure_ascii=False)

            logger.info(f"Exportado JSON: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("🔍 STJ HSE SCRAPER — Homologação de Sentença Estrangeira")
    print("="*70 + "\n")

    scraper = STJHSEScraper()

    # Busca 3 páginas de HSE (60 resultados)
    hses = scraper.buscar_hse(paginas=3)

    print(f"\n{'='*70}")
    print(f"✅ SCRAPING COMPLETO!")
    print(f"{'='*70}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • HSEs extraídas: {len(hses)}")
    print(f"   • Arquivos salvos: {len(list(HSE_OUTPUT.glob('HDE-*.md')))}")
    print(f"   • Output: {HSE_OUTPUT}\n")

    # Salva JSON também
    if hses:
        scraper.salvar_json_completo()

    return len(hses) > 0


if __name__ == "__main__":
    import sys
    sucesso = main()
    sys.exit(0 if sucesso else 1)
