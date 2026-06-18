"""
extrair_jurisprudencia.py
Lê os HTMLs de jurisprudência em scripts/jurisprudencia/html/{codigo}/{artigo}.html
e gera scripts/jurisprudencia_index.json consumido pelo plugin fenice-buscar-artigo.

Estrutura de entrada:
  scripts/jurisprudencia/html/
    cc/166.html
    cc/167.html
    cpc/489.html
    cf88/5.html
    ...

HTML esperado:
  <article class="juri">
    <span class="tribunal">STJ</span>
    <span class="numero">REsp 1.234.567/SP</span>
    <span class="relator">Min. Nancy Andrighi</span>
    <span class="data">22/08/2023</span>
    <div  class="ementa">Texto da ementa...</div>
    <a    class="link" href="https://...">fonte</a>
  </article>

Saída: scripts/jurisprudencia_index.json
  {
    "cc:166": [
      {"tribunal":"STJ","numero":"REsp 1.234.567/SP","relator":"Min. Nancy Andrighi",
       "data":"2023-08-22","ementa":"...","link":"https://..."},
      ...
    ],
    ...
  }
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Instale: pip install beautifulsoup4")
    sys.exit(1)

RAIZ       = Path(__file__).parent
HTML_DIR   = RAIZ / "jurisprudencia" / "html"
OUTPUT     = RAIZ / "jurisprudencia_index.json"
MAX_JURIS  = 2   # máximo de entradas por artigo


def normalizar_data(texto: str) -> str:
    """Converte DD/MM/AAAA ou AAAA-MM-DD para YYYY-MM-DD. Retorna '' se inválido."""
    texto = texto.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(texto, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return texto  # devolve como está se não reconhecer


def texto_limpo(tag) -> str:
    """Extrai texto de uma tag BeautifulSoup, normalizando espaços."""
    if tag is None:
        return ""
    return re.sub(r"\s+", " ", tag.get_text()).strip()


def parsear_juri(article) -> dict:
    """Extrai campos de um <article class='juri'>."""
    return {
        "tribunal": texto_limpo(article.find(class_="tribunal")),
        "numero":   texto_limpo(article.find(class_="numero")),
        "relator":  texto_limpo(article.find(class_="relator")),
        "data":     normalizar_data(texto_limpo(article.find(class_="data"))),
        "ementa":   texto_limpo(article.find(class_="ementa")),
        "link":     (article.find(class_="link") or {}).get("href", "").strip(),
    }


def processar_html(arquivo: Path) -> list[dict]:
    """Retorna lista de até MAX_JURIS entradas de um arquivo HTML."""
    soup = BeautifulSoup(arquivo.read_text(encoding="utf-8"), "html.parser")
    artigos = soup.select("article.juri")[:MAX_JURIS]
    entradas = []
    for art in artigos:
        entrada = parsear_juri(art)
        if entrada["tribunal"] and entrada["ementa"]:   # mínimo obrigatório
            entradas.append(entrada)
    return entradas


def main():
    if not HTML_DIR.exists():
        print(f"Pasta não encontrada: {HTML_DIR}")
        print("Crie a estrutura: scripts/jurisprudencia/html/{codigo}/{artigo}.html")
        sys.exit(0)

    index = {}
    total_arquivos = 0
    total_entradas = 0

    for codigo_dir in sorted(HTML_DIR.iterdir()):
        if not codigo_dir.is_dir():
            continue
        codigo = codigo_dir.name                  # ex: "cc", "cpc", "cf88"

        for html_file in sorted(codigo_dir.glob("*.html")):
            artigo = html_file.stem               # ex: "166"
            chave  = f"{codigo}:{artigo}"         # ex: "cc:166"

            try:
                entradas = processar_html(html_file)
            except Exception as e:
                print(f"  ⚠ Erro em {html_file.name}: {e}")
                continue

            if entradas:
                index[chave] = entradas
                total_entradas += len(entradas)
                total_arquivos += 1

    OUTPUT.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Gerado: {OUTPUT}")
    print(f"   {total_arquivos} artigos | {total_entradas} entradas de jurisprudência")


if __name__ == "__main__":
    main()
