#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Híbrido: Dense (pgvector) + Sparse (FTS tsvector)
Por ora implementa apenas Sparse (FTS) — pgvector será ativado quando houver embeddings.
Interface unificada para quando pgvector for adicionado.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

import psycopg2
import psycopg2.extras


# ---------------------------------------------------------------------------
# Configuração (reutiliza o mesmo mecanismo de planalto_db.py)
# ---------------------------------------------------------------------------

def _cfg() -> Dict:
    """Lê credenciais do .env ou variáveis de ambiente."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

    return {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "dbname":   os.environ.get("DB_NAME", "fenice_brain"),
        "user":     os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "port":     int(os.environ.get("DB_PORT", "5432")),
    }


# ---------------------------------------------------------------------------
# Queries SQL
# ---------------------------------------------------------------------------

_SQL_FTS = """
SELECT
    numero_ano,
    tipo_ato,
    ementa,
    ts_headline(
        'portuguese',
        texto_vigente,
        to_tsquery('portuguese', %(query_ts)s),
        'MaxFragments=3, FragmentDelimiter=" ... ", MaxWords=50, MinWords=10'
    ) AS trecho_relevante,
    ts_rank(busca_idx, to_tsquery('portuguese', %(query_ts)s)) AS relevancia
FROM legislacao_brasileira
WHERE busca_idx @@ to_tsquery('portuguese', %(query_ts)s)
ORDER BY relevancia DESC
LIMIT %(limite)s;
"""

_SQL_KEYWORD = """
SELECT
    numero_ano,
    tipo_ato,
    ementa,
    LEFT(texto_vigente, 500) AS trecho_relevante,
    1.0::float AS relevancia
FROM legislacao_brasileira
WHERE
    numero_ano   ILIKE %(padrao)s
    OR ementa    ILIKE %(padrao)s
    OR texto_vigente ILIKE %(padrao)s
ORDER BY numero_ano
LIMIT %(limite)s;
"""


# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------

class FeniceRAG:
    """
    Motor de recuperação híbrido (FTS + keyword) com interface preparada
    para expansão via pgvector + embeddings OpenAI.

    Uso básico:
        rag = FeniceRAG()
        resultados = rag.buscar_hibrido("prazo prescricional Codigo Civil")
        contexto  = rag.construir_contexto(resultados)
    """

    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None
        self._conectar()

    # ------------------------------------------------------------------
    # Conexão
    # ------------------------------------------------------------------

    def _conectar(self) -> bool:
        """Abre conexão com o banco. Retorna True se bem-sucedido."""
        try:
            self.conn = psycopg2.connect(**_cfg())
            return True
        except psycopg2.Error as exc:
            print(f"[FeniceRAG] Aviso: sem conexão com o banco — {exc}")
            self.conn = None
            return False

    def _exige_conexao(self):
        """Levanta RuntimeError se não há conexão ativa."""
        if self.conn is None:
            raise RuntimeError(
                "FeniceRAG: banco de dados não conectado. "
                "Verifique .env (DB_HOST, DB_NAME, DB_USER, DB_PASS)."
            )

    def fechar(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.fechar()

    # ------------------------------------------------------------------
    # Busca
    # ------------------------------------------------------------------

    def buscar_hibrido(
        self,
        query: str,
        limite: int = 5,
        modo: str = "fts",
    ) -> List[Dict]:
        """
        Busca documentos no banco.

        Parâmetros
        ----------
        query  : termos de busca em linguagem natural
        limite : número máximo de resultados
        modo   :
            "fts"     — Full-Text Search via tsvector GIN (padrão, recomendado)
            "keyword" — ILIKE simples para termos exatos raros (ex: "vicaricídio")
            "hibrido" — reservado para pgvector + embeddings (retorna FTS por ora)

        Retorna
        -------
        Lista de dicts com chaves: numero_ano, tipo_ato, ementa,
        trecho_relevante, relevancia
        """
        self._exige_conexao()

        if modo in ("fts", "hibrido"):
            return self._buscar_fts(query, limite)
        elif modo == "keyword":
            return self._buscar_keyword(query, limite)
        else:
            raise ValueError(f"Modo desconhecido: '{modo}'. Use 'fts', 'keyword' ou 'hibrido'.")

    def _buscar_fts(self, query: str, limite: int) -> List[Dict]:
        """Full-Text Search em português (tsvector GIN)."""
        # Normaliza: une termos com ' & ' para tsquery
        query_ts = " & ".join(
            t for t in query.split() if t
        )
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(_SQL_FTS, {"query_ts": query_ts, "limite": limite})
                return [dict(r) for r in cur.fetchall()]
        except psycopg2.Error as exc:
            # tsquery mal-formada (ex: operadores sem operandos) — tenta keyword
            print(f"[FeniceRAG] FTS falhou ({exc}), tentando keyword como fallback.")
            self.conn.rollback()
            return self._buscar_keyword(query, limite)

    def _buscar_keyword(self, query: str, limite: int) -> List[Dict]:
        """Busca ILIKE para termos exatos — fallback ou termos raros."""
        padrao = f"%{query}%"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(_SQL_KEYWORD, {"padrao": padrao, "limite": limite})
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Construção de contexto para LLM
    # ------------------------------------------------------------------

    def construir_contexto(
        self,
        resultados: List[Dict],
        max_chars: int = 4000,
    ) -> str:
        """
        Formata os resultados como bloco de contexto para injetar no prompt LLM.

        Formato por item:
            --- Lei 14133/2021 ---
            Ementa: Nova Lei de Licitações e Contratos Administrativos.
            [trecho relevante até 500 chars]

        Parâmetros
        ----------
        resultados : lista retornada por buscar_hibrido()
        max_chars  : limite total de caracteres do contexto

        Retorna
        -------
        String pronta para substituir {contexto_juridico} nos prompts.
        """
        if not resultados:
            return "(nenhum resultado encontrado na base de dados)"

        blocos: List[str] = []
        total = 0

        for r in resultados:
            numero_ano     = r.get("numero_ano", "Desconhecido")
            ementa         = r.get("ementa") or ""
            trecho         = r.get("trecho_relevante") or ""

            # Trunca o trecho a 500 chars para controlar tamanho
            trecho_curto = trecho[:500].rstrip()
            if len(trecho) > 500:
                trecho_curto += "..."

            bloco = (
                f"--- {numero_ano} ---\n"
                + (f"Ementa: {ementa}\n" if ementa else "")
                + f"{trecho_curto}\n"
            )

            if total + len(bloco) > max_chars:
                break

            blocos.append(bloco)
            total += len(bloco)

        return "\n".join(blocos)

    # ------------------------------------------------------------------
    # Pipeline completo: busca → contexto → prompt preenchido
    # ------------------------------------------------------------------

    def responder_com_contexto(
        self,
        pergunta: str,
        prompt_template: str,
        limite: int = 5,
        modo: str = "fts",
        max_chars: int = 4000,
    ) -> Dict:
        """
        Busca no banco, constrói contexto e preenche o template de prompt.

        Não chama nenhum LLM — o usuário injeta o prompt_preenchido em
        Claude, GPT, Gemini, etc.

        Parâmetros
        ----------
        pergunta        : dúvida jurídica do usuário
        prompt_template : string com placeholders {contexto_juridico} e {pergunta}
                          (ou {contexto_filosofico}/{texto_juridico} etc.)
        limite          : número de documentos a recuperar
        modo            : "fts" | "keyword" | "hibrido"
        max_chars       : limite de chars do contexto

        Retorna
        -------
        {
            "pergunta"         : str,
            "resultados_banco" : List[Dict],
            "contexto"         : str,
            "prompt_preenchido": str,
        }
        """
        resultados = self.buscar_hibrido(pergunta, limite=limite, modo=modo)
        contexto   = self.construir_contexto(resultados, max_chars=max_chars)

        # Preenche os placeholders conhecidos; ignora os desconhecidos
        prompt_preenchido = prompt_template
        substituicoes = {
            "{contexto_juridico}":   contexto,
            "{contexto_filosofico}": contexto,
            "{vade_mecum_contexto}": contexto,
            "{pergunta}":            pergunta,
        }
        for placeholder, valor in substituicoes.items():
            prompt_preenchido = prompt_preenchido.replace(placeholder, valor)

        return {
            "pergunta":          pergunta,
            "resultados_banco":  resultados,
            "contexto":          contexto,
            "prompt_preenchido": prompt_preenchido,
        }

    # ------------------------------------------------------------------
    # Utilitário: carrega template de arquivo
    # ------------------------------------------------------------------

    @staticmethod
    def carregar_prompt(nome_arquivo: str) -> str:
        """
        Lê um arquivo de template de scripts/prompts/.

        Exemplo:
            template = FeniceRAG.carregar_prompt("grounding_juridico.txt")
        """
        prompts_dir = Path(__file__).parent / "prompts"
        caminho = prompts_dir / nome_arquivo
        if not caminho.exists():
            raise FileNotFoundError(
                f"Template '{nome_arquivo}' não encontrado em {prompts_dir}"
            )
        return caminho.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI de teste rápido
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    termos = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "licitacao dispensa contrato"

    with FeniceRAG() as rag:
        print(f"Buscando: '{termos}' (modo=fts, limite=3)")
        resultados = rag.buscar_hibrido(termos, limite=3)

        if not resultados:
            print("Nenhum resultado encontrado.")
        else:
            for r in resultados:
                print(f"\n  {r['numero_ano']} — {r['tipo_ato']}")
                print(f"  Relevancia: {r['relevancia']:.4f}")
                print(f"  Ementa: {(r['ementa'] or '')[:80]}...")

        print("\n--- CONTEXTO GERADO ---")
        contexto = rag.construir_contexto(resultados)
        print(contexto[:800])
