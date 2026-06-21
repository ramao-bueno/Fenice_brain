#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai metadados de revogação das tags <s> do HTML do Planalto.

Para cada fragmento revogado, tenta identificar:
  - Qual artigo foi revogado (sobe na árvore DOM até cabeçalho de artigo)
  - Qual lei posterior causou a revogação (regex nas proximidades do elemento)
  - A data da modificação (mencionada no HTML próximo, se disponível)

Uso standalone:
  python planalto_temporal.py caminho/para/lei.htm

Uso programático:
  from planalto_temporal import extrair_revogacoes
  revogacoes = extrair_revogacoes(Path("scripts/_cache_planalto/l14133.htm"))
"""
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag

# ── Constantes ────────────────────────────────────────────────────────────────

# Regex para lei modificadora: "Lei n.º 14.133/2021", "Lei 14133/2021",
# "Decreto-Lei nº 2.848/1940", "LC 123/2006", "MP 1.186/2023"
_RE_LEI = re.compile(
    r"(?:Decreto-?Lei|Lei\s+(?:Complementar\s+)?|Medida\s+Provis[oó]ria|LC|MP)\s*"
    r"n[º°.oa]?\s*[\d.,]+[/\-]\d{4}",
    re.IGNORECASE,
)

# Regex para artigo: "Art. 927", "Art 5º", "Artigo 122"
_RE_ARTIGO = re.compile(
    r"Art(?:igo)?\.?\s*\d+[-\w]*[º°]?",
    re.IGNORECASE,
)

# Regex para data de revogação/alteração: "(Redação dada pela Lei ... de DD/MM/AAAA)"
_RE_DATA = re.compile(
    r"\b(\d{1,2}[./]\d{1,2}[./]\d{4}|\d{4}-\d{2}-\d{2})\b"
)

# Quantidade de caracteres de contexto para busca de lei modificadora
_CONTEXTO_CHARS = 300

# Tags HTML que marcam texto revogado no Planalto
_TAGS_RASURA = ("s", "strike", "del")


# ── Funções auxiliares ────────────────────────────────────────────────────────

def _texto_proximo(elemento: Tag, n_chars: int = _CONTEXTO_CHARS) -> str:
    """
    Retorna texto das proximidades de um elemento no HTML:
    concatena até n_chars de texto dos irmãos anteriores e posteriores
    (e do elemento pai imediato) para buscar menção à lei modificadora.
    """
    fragmentos: List[str] = []

    # Texto do pai
    pai = elemento.parent
    if pai:
        fragmentos.append(pai.get_text(separator=" ", strip=True))

    # Irmãos anteriores (até 3)
    anterior = elemento.previous_sibling
    count = 0
    while anterior and count < 3:
        if hasattr(anterior, "get_text"):
            t = anterior.get_text(separator=" ", strip=True)
            if t:
                fragmentos.insert(0, t)
        count += 1
        anterior = anterior.previous_sibling

    # Irmãos posteriores (até 3)
    posterior = elemento.next_sibling
    count = 0
    while posterior and count < 3:
        if hasattr(posterior, "get_text"):
            t = posterior.get_text(separator=" ", strip=True)
            if t:
                fragmentos.append(t)
        count += 1
        posterior = posterior.next_sibling

    contexto = " ".join(fragmentos)
    # Limita ao redor do centro aproximado
    return contexto[:n_chars * 2]


def detectar_artigo_contexto(soup_element: Tag) -> str:
    """
    Sobe na árvore DOM a partir de soup_element até encontrar o
    cabeçalho de artigo mais próximo (texto que começa com 'Art. N').

    Retorna a string identificadora (ex: 'Art. 927') ou '' se não encontrado.
    """
    no = soup_element
    visited = set()

    while no:
        node_id = id(no)
        if node_id in visited:
            break
        visited.add(node_id)

        # Verifica irmãos anteriores no mesmo nível
        candidato = no.previous_sibling
        while candidato:
            if hasattr(candidato, "get_text"):
                txt = candidato.get_text(strip=True)
                m = _RE_ARTIGO.match(txt)
                if m:
                    return m.group(0).strip()
            candidato = candidato.previous_sibling

        # Sobe para o pai
        pai = getattr(no, "parent", None)
        if pai is None or pai == no:
            break

        # Verifica se o pai em si tem texto de artigo
        if hasattr(pai, "get_text"):
            txt_pai = pai.get_text(strip=True)
            m = _RE_ARTIGO.match(txt_pai)
            if m:
                return m.group(0).strip()

        no = pai

    return ""


def _extrair_lei_modificadora(contexto: str) -> str:
    """Extrai a primeira menção a uma lei modificadora no texto de contexto."""
    m = _RE_LEI.search(contexto)
    if m:
        # Normaliza: remove espaços internos múltiplos
        return re.sub(r"\s+", " ", m.group(0)).strip()
    return ""


def _extrair_data(contexto: str) -> str:
    """Extrai a primeira data mencionada no contexto."""
    m = _RE_DATA.search(contexto)
    return m.group(1) if m else ""


# ── Função principal ──────────────────────────────────────────────────────────

def extrair_revogacoes(caminho_html: Path) -> List[Dict]:
    """
    Abre o HTML do Planalto e extrai metadados de cada fragmento revogado.

    Para cada tag <s>/<strike>/<del> encontrada:
      1. Captura o texto revogado
      2. Detecta o artigo afetado (subindo na árvore DOM)
      3. Busca nas proximidades (irmãos/pai) por menção à lei modificadora
      4. Extrai data de modificação, se mencionada

    Retorna lista de dicts com:
      - texto_revogado    (str) — conteúdo da tag de rasura
      - artigo_afetado    (str) — 'Art. 927' ou '' se não identificado
      - lei_modificadora  (str) — 'Lei 14133/2021' ou '' se não encontrada
      - data_modificacao  (str) — 'DD/MM/AAAA' ou '' se não encontrada
      - contexto_html     (str) — trecho de HTML próximo (para auditoria)
    """
    if not caminho_html.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_html}")

    html = caminho_html.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    revogacoes: List[Dict] = []
    vistos: set = set()  # evita duplicatas de texto idêntico

    for tag in soup.find_all(_TAGS_RASURA):
        texto = tag.get_text(separator=" ", strip=True)

        # Ignora fragmentos muito curtos (pontuação, espaços, etc.)
        if not texto or len(texto) < 5:
            continue

        # Deduplicação por conteúdo exato
        chave = texto[:200]
        if chave in vistos:
            continue
        vistos.add(chave)

        artigo = detectar_artigo_contexto(tag)
        contexto = _texto_proximo(tag)
        lei_mod = _extrair_lei_modificadora(contexto)
        data_mod = _extrair_data(contexto)

        revogacoes.append({
            "texto_revogado":   texto,
            "artigo_afetado":   artigo,
            "lei_modificadora": lei_mod,
            "data_modificacao": data_mod,
            "contexto_html":    contexto[:500],  # limita para não inflar o retorno
        })

    return revogacoes


# ── Integração com banco de dados ─────────────────────────────────────────────

def salvar_revogacoes_db(
    revogacoes: List[Dict],
    numero_ano: str,
    lei_id: Optional[str] = None,
) -> int:
    """
    Insere as revogações extraídas na tabela legislacao_historico.

    Parâmetros:
      revogacoes  — resultado de extrair_revogacoes()
      numero_ano  — ex: 'Lei 10406/2002'
      lei_id      — UUID da linha em legislacao_brasileira (opcional)

    Retorna o número de linhas inseridas.
    """
    import os
    import psycopg2
    import psycopg2.extras

    # Lê config do .env
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for linha in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in linha and not linha.strip().startswith("#"):
                k, _, v = linha.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

    cfg = {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "dbname":   os.environ.get("DB_NAME", "fenice_brain"),
        "user":     os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "port":     int(os.environ.get("DB_PORT", "5432")),
    }

    INSERT_SQL = """
    INSERT INTO legislacao_historico (
        lei_id, numero_ano, artigo,
        texto_original, texto_vigente,
        lei_modificadora, data_modificacao, tipo_modificacao
    ) VALUES (
        %(lei_id)s, %(numero_ano)s, %(artigo)s,
        %(texto_original)s, NULL,
        %(lei_modificadora)s, %(data_modificacao)s, 'revogacao'
    )
    ON CONFLICT DO NOTHING;
    """

    inseridos = 0
    try:
        conn = psycopg2.connect(**cfg)
        with conn:
            with conn.cursor() as cur:
                for rev in revogacoes:
                    # Converte data para formato ISO ou None
                    data_str = rev["data_modificacao"] or None
                    if data_str:
                        # Tenta converter DD/MM/AAAA para AAAA-MM-DD
                        m = re.match(r"(\d{1,2})[./](\d{1,2})[./](\d{4})", data_str)
                        if m:
                            data_str = f"{m.group(3)}-{m.group(2):0>2}-{m.group(1):0>2}"

                    cur.execute(INSERT_SQL, {
                        "lei_id":          lei_id,
                        "numero_ano":      numero_ano,
                        "artigo":          rev["artigo_afetado"] or None,
                        "texto_original":  rev["texto_revogado"],
                        "lei_modificadora": rev["lei_modificadora"] or None,
                        "data_modificacao": data_str,
                    })
                    inseridos += cur.rowcount
        conn.close()
    except psycopg2.Error as e:
        print(f"  Erro ao salvar revogacoes: {e}", file=sys.stderr)

    return inseridos


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Uso: python planalto_temporal.py <caminho_html> [--salvar]")
        print()
        print("Exemplos:")
        print("  python planalto_temporal.py scripts/_cache_planalto/l14133.htm")
        print("  python planalto_temporal.py scripts/_cache_planalto/l10406.htm --salvar")
        sys.exit(1)

    caminho = Path(sys.argv[1])
    salvar = "--salvar" in sys.argv

    print(f"Analisando: {caminho}")
    print("-" * 60)

    revogacoes = extrair_revogacoes(caminho)

    if not revogacoes:
        print("Nenhum fragmento revogado encontrado.")
        return

    print(f"{len(revogacoes)} fragmento(s) revogado(s) detectado(s):\n")
    for i, rev in enumerate(revogacoes, 1):
        print(f"[{i}] Artigo: {rev['artigo_afetado'] or '(nao identificado)'}")
        print(f"    Lei modificadora: {rev['lei_modificadora'] or '(nao identificada)'}")
        print(f"    Data: {rev['data_modificacao'] or '(nao identificada)'}")
        print(f"    Texto: {rev['texto_revogado'][:100]}{'...' if len(rev['texto_revogado']) > 100 else ''}")
        print()

    if salvar:
        # Tenta inferir numero_ano do nome do arquivo
        stem = caminho.stem.lower()
        m = re.search(r"l(\d+)", stem)
        numero_lei = m.group(1) if m else stem
        numero_ano = f"Lei {numero_lei}"

        print(f"Salvando no banco como '{numero_ano}'...")
        n = salvar_revogacoes_db(revogacoes, numero_ano)
        print(f"  {n} registro(s) inserido(s) em legislacao_historico.")


if __name__ == "__main__":
    main()
