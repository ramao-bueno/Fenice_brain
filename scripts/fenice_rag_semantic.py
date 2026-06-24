#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenice RAG Semântico — motor de busca vetorial + síntese Claude Haiku
Módulo independente: não altera fenice_rag.py nem api_fenice_saas.py existentes.
"""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

MODELO_HAIKU   = "claude-haiku-4-5-20251001"
MODELO_EMBED   = "intfloat/multilingual-e5-large"
THRESHOLD_MIN  = 0.70   # abaixo: sem base legal suficiente → sem Claude
THRESHOLD_ALTA = 0.85
TOP_K          = 5

PROMPT_SISTEMA = (
    "Você é o Motor de Inteligência Analítica da Fenice IA, "
    "um interpretador jurídico de alto rigor técnico.\n\n"
    "REGRAS ABSOLUTAS:\n"
    "1. Responda SOMENTE com base nos artigos fornecidos abaixo.\n"
    "2. NUNCA invente artigos, parágrafos ou leis fora do contexto.\n"
    "3. Se o contexto não for suficiente para responder com certeza, "
    "diga EXATAMENTE: "
    "'Não temos resposta bate-pronto para isso — posso pesquisar.'\n"
    "4. Cite sempre a fonte: [Art. X do CÓDIGO].\n"
    "5. Responda em português jurídico claro, sem enrolação."
)

_RESPOSTA_SEM_BASE = "Não temos resposta bate-pronto para isso — posso pesquisar."

# ---------------------------------------------------------------------------
# RAGEngine
# ---------------------------------------------------------------------------

class RAGEngine:
    """
    Motor RAG semântico com camada de confiança LGPD.
    Inicialização lazy: não lança exceção no import mesmo se keys faltarem.
    """

    def __init__(self):
        self._pronto = False
        self._erro_init: str | None = None

        sb_url = os.environ.get("SUPABASE_URL", "")
        sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        ant_key = os.environ.get("ANTHROPIC_API_KEY", "")

        if not sb_url or not sb_key or not ant_key:
            faltando = [k for k, v in {
                "SUPABASE_URL": sb_url,
                "SUPABASE_SERVICE_KEY": sb_key,
                "ANTHROPIC_API_KEY": ant_key,
            }.items() if not v]
            self._erro_init = f"Variáveis ausentes no .env: {', '.join(faltando)}"
            return

        try:
            from supabase import create_client
            from anthropic import Anthropic
            from sentence_transformers import SentenceTransformer

            self._supabase = create_client(sb_url, sb_key)
            self._anthropic = Anthropic(api_key=ant_key)

            print(f"[RAGEngine] Carregando {MODELO_EMBED} na CPU...")
            self._model = SentenceTransformer(MODELO_EMBED, device="cpu")

            self._pronto = True
            print("[RAGEngine] Motor semântico pronto.")

        except ImportError as exc:
            self._erro_init = f"Dependência não instalada: {exc}"

    # -----------------------------------------------------------------------

    def _embed_query(self, pergunta: str) -> list[float]:
        """Prefixo 'query: ' obrigatório para o modelo E5 em consultas."""
        return self._model.encode(
            f"query: {pergunta.strip()}",
            normalize_embeddings=True,
        ).tolist()

    def _nivel_confianca(self, score: float) -> str:
        if score >= THRESHOLD_ALTA:
            return "alta"
        if score >= THRESHOLD_MIN:
            return "média"
        return "insuficiente"

    # -----------------------------------------------------------------------

    def query(self, pergunta: str) -> dict:
        """Ponto de entrada principal — retorna resposta estruturada."""

        hoje = date.today().isoformat()

        if not self._pronto:
            return {
                "resposta":     "Motor semântico indisponível: " + (self._erro_init or "erro de inicialização"),
                "fontes":       [],
                "confianca":    "erro",
                "vigente_em":   hoje,
                "modelo_usado": MODELO_HAIKU,
            }

        try:
            # 1. Embedding da pergunta
            vetor = self._embed_query(pergunta)

            # 2. Busca vetorial no Supabase via RPC match_chunks
            res = self._supabase.rpc(
                "match_chunks",
                {
                    "query_embedding": vetor,
                    "match_threshold": THRESHOLD_MIN,
                    "match_count": TOP_K,
                },
            ).execute()

            chunks = res.data or []

            # 3. Camada LGPD — sem chunks suficientes, sem Claude
            if not chunks:
                return {
                    "resposta":     _RESPOSTA_SEM_BASE,
                    "fontes":       [],
                    "confianca":    "insuficiente",
                    "vigente_em":   hoje,
                    "modelo_usado": MODELO_HAIKU,
                }

            score_medio = sum(c["similarity"] for c in chunks) / len(chunks)
            confianca = self._nivel_confianca(score_medio)

            # 4. Monta contexto e fontes
            blocos_contexto: list[str] = []
            fontes: list[dict] = []

            for c in chunks:
                status = "Vigente" if c.get("vigente", True) else "REVOGADO"
                blocos_contexto.append(
                    f"[{c['codigo']} — {c['artigo']}] ({status})\n{c['conteudo']}"
                )
                fontes.append({
                    "codigo":     c["codigo"],
                    "artigo":     c["artigo"],
                    "similarity": round(c["similarity"], 4),
                    "vigente":    c.get("vigente", True),
                })

            contexto = "\n\n".join(blocos_contexto)

            # 5. Síntese com Claude Haiku (temperatura mínima = determinismo)
            msg = self._anthropic.messages.create(
                model=MODELO_HAIKU,
                max_tokens=1024,
                temperature=0.05,
                system=PROMPT_SISTEMA,
                messages=[{
                    "role":    "user",
                    "content": f"ARTIGOS DISPONÍVEIS:\n{contexto}\n\nPERGUNTA: {pergunta}",
                }],
            )

            resposta = msg.content[0].text

            # Se o Haiku mesmo assim declinou, atualiza confiança
            if _RESPOSTA_SEM_BASE.lower() in resposta.lower():
                confianca = "insuficiente"

            return {
                "resposta":     resposta,
                "fontes":       fontes,
                "confianca":    confianca,
                "vigente_em":   hoje,
                "modelo_usado": MODELO_HAIKU,
            }

        except Exception as exc:
            return {
                "resposta":     "Erro interno no motor semântico.",
                "fontes":       [],
                "confianca":    "erro",
                "detalhe":      str(exc),
                "vigente_em":   hoje,
                "modelo_usado": MODELO_HAIKU,
            }


# ---------------------------------------------------------------------------
# CLI de teste rápido
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    pergunta = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "Quais as consequências de um contrato verbal sem testemunhas?"

    engine = RAGEngine()
    resultado = engine.query(pergunta)

    print(f"\nPERGUNTA: {pergunta}")
    print(f"CONFIANÇA: {resultado['confianca']}")
    print(f"RESPOSTA:\n{resultado['resposta']}")
    print(f"\nFONTES ({len(resultado['fontes'])}):")
    for f in resultado["fontes"]:
        print(f"  {f['codigo']} {f['artigo']} — similarity: {f['similarity']} — vigente: {f['vigente']}")
