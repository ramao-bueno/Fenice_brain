#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser semantico de leis do Planalto.

Baseado em planalto_pipeline.py (funcao parsear_lei).
Separa texto vigente de texto revogado e extrai ementa.
"""
import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from bs4 import BeautifulSoup

PLANALTO_BASE = "https://www.planalto.gov.br"


def parsear_lei(caminho_html: Path) -> Dict:
    """
    Parser semantico que separa texto vigente de texto revogado.
    Extrai ementa, numero, ano da lei e fragmentos revogados.

    Trata as tags do Planalto:
      <s>...</s>           -> texto revogado/riscado
      <strike>...</strike> -> idem (formato antigo)
      <del>...</del>       -> idem (padrao HTML5)
    """
    html = caminho_html.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    titulo_tag = soup.find("title")
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else caminho_html.stem

    num_lei = _extrair_numero_lei(titulo, caminho_html.stem)

    # Extrai o ano do path do cache (ex: _ato2019-2022/2021/lei/l14133.htm)
    caminho_str = str(caminho_html)
    m_ano_path = re.search(r"[/\\](\d{4})[/\\]", caminho_str)
    ano_lei = m_ano_path.group(1) if m_ano_path else _extrair_ano(titulo, caminho_html.stem)

    # Extrai ementa antes de modificar o DOM
    ementa = _extrair_ementa(soup, titulo)

    texto_vigente_blocos: List[str] = []
    fragmentos_revogados: List[str] = []

    corpo = soup.find("body") or soup
    for elem in corpo.find_all(["p", "div", "span", "li"]):
        # Coleta texto revogado das tags de rasura
        for rasura_tag in elem.find_all(["s", "strike", "del"]):
            txt = rasura_tag.get_text(strip=True)
            if txt and len(txt) > 5:
                fragmentos_revogados.append(txt)
            rasura_tag.decompose()

        # O que sobrou e texto vigente
        txt = elem.get_text(separator=" ", strip=True)
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt and len(txt) > 10:
            texto_vigente_blocos.append(txt)

    # Desduplicacao mantendo ordem
    seen = set()
    vigente_unico = []
    for bloco in texto_vigente_blocos:
        if bloco not in seen:
            seen.add(bloco)
            vigente_unico.append(bloco)

    return {
        "arquivo_fonte": caminho_html.name,
        "titulo": titulo,
        "numero": num_lei,
        "ano": ano_lei,
        "ementa": ementa,
        "texto_vigente": "\n\n".join(vigente_unico),
        "fragmentos_revogados": fragmentos_revogados,
        "url_origem": f"{PLANALTO_BASE}/ccivil_03/leis/{ano_lei}/L{num_lei}.htm",
        "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d"),
    }


def _extrair_ementa(soup: BeautifulSoup, titulo: str) -> str:
    """
    Tenta extrair a ementa da lei pelo HTML do Planalto.

    Estrategias (em ordem de prioridade):
      1. Elemento com classe contendo "ementa"
      2. Primeiro <p> longo antes do "Art. 1"
      3. Titulo expandido (fallback)
    """
    # Estrategia 1: classe "ementa" (div ou p)
    for tag in soup.find_all(True, class_=True):
        classes = " ".join(tag.get("class", [])).lower()
        if "ementa" in classes:
            txt = tag.get_text(separator=" ", strip=True)
            txt = re.sub(r"\s+", " ", txt).strip()
            if txt and len(txt) > 20:
                return txt

    # Estrategia 2: primeiro <p> longo antes de "Art. 1"
    corpo = soup.find("body") or soup
    art1_encontrado = False
    for p in corpo.find_all("p"):
        txt = p.get_text(separator=" ", strip=True)
        txt = re.sub(r"\s+", " ", txt).strip()
        # Para ao encontrar o primeiro artigo
        if re.search(r"Art\.\s*1[oº°]?\b", txt):
            art1_encontrado = True
            break
        # Paragrafo longo o suficiente para ser ementa (> 80 chars)
        if len(txt) > 80 and not re.match(r"^(Lei|Decreto|Medida)", txt):
            return txt

    # Se nao achou antes do Art. 1, tenta qualquer p com "Dispoe" / "Institui" / "Estabelece"
    if not art1_encontrado or True:
        for p in corpo.find_all("p"):
            txt = p.get_text(separator=" ", strip=True)
            txt = re.sub(r"\s+", " ", txt).strip()
            if re.match(r"(Disp[oõ]e|Institui|Estabelece|Cria|Altera|Regulamenta)", txt):
                if len(txt) > 30:
                    return txt

    # Fallback: titulo
    return titulo


def _extrair_numero_lei(titulo: str, stem: str) -> str:
    for txt in [titulo, stem]:
        m = re.search(r"(\d{4,6})", txt)
        if m:
            return m.group(1)
    return stem


def _extrair_ano(titulo: str, stem: str) -> str:
    for txt in [titulo, stem]:
        m = re.search(r"(20\d{2}|19\d{2})", txt)
        if m:
            return m.group(1)
    return str(datetime.now().year)
