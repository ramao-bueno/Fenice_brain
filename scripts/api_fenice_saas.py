#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST Fenice bRain — SaaS Layer
Tiers: Free (busca keyword) | Premium (busca híbrida + agentes IA)

Iniciar:
    uvicorn api_fenice_saas:app --reload --port 8001

Documentação interativa:
    http://localhost:8001/docs
"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Tentativa de importação das dependências locais
# ---------------------------------------------------------------------------
try:
    from fenice_rag import FeniceRAG
    _RAG_DISPONIVEL = True
except ImportError:
    _RAG_DISPONIVEL = False


# ---------------------------------------------------------------------------
# Helpers de autenticação
# ---------------------------------------------------------------------------

def _is_premium(x_fenice_key: Optional[str]) -> bool:
    """Retorna True se a chave indica tier Premium."""
    if not x_fenice_key:
        return False
    return x_fenice_key.startswith("fenice_premium_")


def _exige_premium(x_fenice_key: Optional[str]) -> None:
    """Levanta 403 se a chave não for Premium."""
    if not _is_premium(x_fenice_key):
        raise HTTPException(
            status_code=403,
            detail=(
                "Endpoint Premium. "
                "Envie o header X-Fenice-Key: fenice_premium_<sua_chave>."
            ),
        )


# ---------------------------------------------------------------------------
# Carregamento de prompts
# ---------------------------------------------------------------------------

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def _carregar_prompt(nome: str) -> str:
    """Lê template de scripts/prompts/. Levanta 503 se não encontrado."""
    caminho = _PROMPTS_DIR / nome
    if not caminho.exists():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Template '{nome}' nao encontrado em {_PROMPTS_DIR}. "
                "Execute o setup inicial do Fenice."
            ),
        )
    return caminho.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Modelos Pydantic — Request / Response
# ---------------------------------------------------------------------------

class BuscarRequest(BaseModel):
    query:  str = Field(..., min_length=2, max_length=500, description="Termos de busca juridica")
    limite: int = Field(10, ge=1, le=50, description="Numero maximo de resultados")


class AnalisarRequest(BaseModel):
    pergunta: str = Field(..., min_length=5, max_length=1000, description="Duvida juridica")
    tier:     str = Field("premium", description="'free' ou 'premium'")
    limite:   int = Field(5, ge=1, le=20, description="Documentos a recuperar do banco")


class HermeneuticaRequest(BaseModel):
    texto:  str = Field(..., min_length=10, max_length=5000, description="Texto juridico para analise filosofica")
    limite: int = Field(5, ge=1, le=20, description="Documentos de contexto a recuperar")


class TccRequest(BaseModel):
    rascunho: str = Field(..., min_length=50, max_length=20000, description="Rascunho do TCC")
    tema:     str = Field(..., min_length=3, max_length=200, description="Tema do TCC para busca contextual")
    limite:   int = Field(5, ge=1, le=20, description="Documentos de suporte a recuperar")


class ResultadoBusca(BaseModel):
    numero_ano:       str
    tipo_ato:         str
    ementa:           Optional[str] = None
    trecho_relevante: Optional[str] = None
    relevancia:       Optional[float] = None


class ContextoResponse(BaseModel):
    contexto:          str
    prompt_preenchido: str
    documentos_base:   int
    aviso:             Optional[str] = None


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Fenice bRain — SaaS API",
    description=(
        "API REST do Vade Mecum Dinamico Fenice bRain.\n\n"
        "**Tiers:**\n"
        "- **Free** — `POST /buscar`: Full-Text Search sem autenticacao\n"
        "- **Premium** — `/analisar`, `/hermeneutica`, `/tcc`: "
        "Requer header `X-Fenice-Key: fenice_premium_<chave>`\n\n"
        "Nenhum endpoint chama LLMs diretamente. "
        "O prompt preenchido e retornado para uso em Claude/GPT/Gemini."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    tags=["Infraestrutura"],
    summary="Status da API e conexao com o banco",
)
async def health() -> Dict[str, Any]:
    """Verifica se a API esta operacional e se o banco responde."""
    db_ok    = False
    db_msg   = "banco nao conectado"
    contagem = 0

    if _RAG_DISPONIVEL:
        try:
            with FeniceRAG() as rag:
                if rag.conn:
                    contagem = rag.contar_leis()
                    db_ok  = True
                    db_msg = f"{contagem} leis indexadas"
        except Exception as exc:
            db_msg = str(exc)

    return {
        "status":         "ok" if db_ok else "degradado",
        "timestamp":      datetime.utcnow().isoformat() + "Z",
        "api_versao":     "1.0.0",
        "banco":          {"ok": db_ok, "detalhe": db_msg},
        "rag_disponivel": _RAG_DISPONIVEL,
    }


# ---------------------------------------------------------------------------
# POST /buscar  (Free)
# ---------------------------------------------------------------------------

@app.post(
    "/buscar",
    response_model=List[ResultadoBusca],
    tags=["Free"],
    summary="Busca FTS na base de legislacao (Free — sem auth)",
)
async def buscar(body: BuscarRequest) -> List[ResultadoBusca]:
    """
    Busca Full-Text Search (FTS) na tabela `legislacao_brasileira`.
    Disponivel sem autenticacao (Free tier).

    Body JSON: `{"query": "licitacao dispensa", "limite": 10}`
    """
    if not _RAG_DISPONIVEL:
        raise HTTPException(
            status_code=503,
            detail="Modulo fenice_rag nao disponivel. Verifique a instalacao.",
        )

    try:
        with FeniceRAG() as rag:
            resultados = rag.buscar_hibrido(body.query, limite=body.limite, modo="fts")
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno: {exc}")

    return [
        ResultadoBusca(
            numero_ano       = r.get("numero_ano", ""),
            tipo_ato         = r.get("tipo_ato", ""),
            ementa           = r.get("ementa"),
            trecho_relevante = r.get("trecho_relevante"),
            relevancia       = float(r.get("relevancia") or 0),
        )
        for r in resultados
    ]


# ---------------------------------------------------------------------------
# POST /analisar  (Premium)
# ---------------------------------------------------------------------------

@app.post(
    "/analisar",
    response_model=ContextoResponse,
    tags=["Premium"],
    summary="Analise juridica com grounding no banco (Premium)",
)
async def analisar(
    body: AnalisarRequest,
    x_fenice_key: Optional[str] = Header(None, alias="X-Fenice-Key"),
) -> ContextoResponse:
    """
    Retorna o prompt `grounding_juridico.txt` preenchido com contexto
    recuperado do banco. Injete o `prompt_preenchido` no LLM de sua escolha.

    **Requer** header `X-Fenice-Key: fenice_premium_<chave>`.

    Body: `{"pergunta": "Qual o prazo prescricional do CC?", "tier": "premium"}`
    """
    _exige_premium(x_fenice_key)

    if not _RAG_DISPONIVEL:
        raise HTTPException(status_code=503, detail="fenice_rag nao disponivel.")

    template = _carregar_prompt("grounding_juridico.txt")

    try:
        with FeniceRAG() as rag:
            resultado = rag.responder_com_contexto(
                pergunta        = body.pergunta,
                prompt_template = template,
                limite          = body.limite,
                modo            = "fts",
            )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    n_docs = len(resultado["resultados_banco"])
    aviso  = None if n_docs > 0 else (
        "Nenhum documento encontrado na base. "
        "O prompt contem contexto vazio — resposta do LLM pode ser imprecisa."
    )

    return ContextoResponse(
        contexto          = resultado["contexto"],
        prompt_preenchido = resultado["prompt_preenchido"],
        documentos_base   = n_docs,
        aviso             = aviso,
    )


# ---------------------------------------------------------------------------
# POST /hermeneutica  (Premium)
# ---------------------------------------------------------------------------

@app.post(
    "/hermeneutica",
    response_model=ContextoResponse,
    tags=["Premium"],
    summary="Analise filosofica hermeneutica (Premium)",
)
async def hermeneutica(
    body: HermeneuticaRequest,
    x_fenice_key: Optional[str] = Header(None, alias="X-Fenice-Key"),
) -> ContextoResponse:
    """
    Retorna o prompt `hermeneutica_filosofica.txt` preenchido com o texto
    juridico submetido e contexto filosofico recuperado do banco.

    **Requer** header `X-Fenice-Key: fenice_premium_<chave>`.

    Body: `{"texto": "Art. 5 CF — todos sao iguais perante a lei"}`
    """
    _exige_premium(x_fenice_key)

    if not _RAG_DISPONIVEL:
        raise HTTPException(status_code=503, detail="fenice_rag nao disponivel.")

    template = _carregar_prompt("hermeneutica_filosofica.txt")

    try:
        with FeniceRAG() as rag:
            # Usa os primeiros 200 chars do texto como query de busca contextual
            query_filosofica = body.texto[:200].strip()
            resultados = rag.buscar_hibrido(query_filosofica, limite=body.limite, modo="fts")
            contexto   = rag.construir_contexto(resultados)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    prompt_preenchido = (
        template
        .replace("{texto_juridico}",     body.texto)
        .replace("{contexto_filosofico}", contexto)
    )

    n_docs = len(resultados)
    aviso  = None if n_docs > 0 else (
        "Nenhum documento encontrado no banco. "
        "A analise filosofica sera feita apenas sobre o texto submetido."
    )

    return ContextoResponse(
        contexto          = contexto,
        prompt_preenchido = prompt_preenchido,
        documentos_base   = n_docs,
        aviso             = aviso,
    )


# ---------------------------------------------------------------------------
# POST /tcc  (Premium)
# ---------------------------------------------------------------------------

@app.post(
    "/tcc",
    response_model=ContextoResponse,
    tags=["Premium"],
    summary="Revisao de rascunho de TCC juridico (Premium)",
)
async def tcc(
    body: TccRequest,
    x_fenice_key: Optional[str] = Header(None, alias="X-Fenice-Key"),
) -> ContextoResponse:
    """
    Retorna o prompt `agente_tcc.txt` preenchido com o rascunho do academico
    e contexto de legislacao recuperado do banco pelo tema.

    **Requer** header `X-Fenice-Key: fenice_premium_<chave>`.

    Body: `{"rascunho": "...", "tema": "responsabilidade civil"}`
    """
    _exige_premium(x_fenice_key)

    if not _RAG_DISPONIVEL:
        raise HTTPException(status_code=503, detail="fenice_rag nao disponivel.")

    template = _carregar_prompt("agente_tcc.txt")

    try:
        with FeniceRAG() as rag:
            resultados = rag.buscar_hibrido(body.tema, limite=body.limite, modo="fts")
            contexto   = rag.construir_contexto(resultados)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    prompt_preenchido = (
        template
        .replace("{vade_mecum_contexto}", contexto)
        .replace("{rascunho_tcc}",        body.rascunho)
    )

    n_docs = len(resultados)
    aviso  = None if n_docs > 0 else (
        "Nenhum documento encontrado para o tema informado. "
        "O agente TCC analisara o rascunho sem suporte da base de dados."
    )

    return ContextoResponse(
        contexto          = contexto,
        prompt_preenchido = prompt_preenchido,
        documentos_base   = n_docs,
        aviso             = aviso,
    )


# ---------------------------------------------------------------------------
# GET /  — info
# ---------------------------------------------------------------------------

@app.get("/", tags=["Infraestrutura"], summary="Info da API")
async def root() -> Dict[str, Any]:
    return {
        "titulo":  "Fenice bRain — SaaS API",
        "versao":  "1.0.0",
        "docs":    "/docs",
        "redoc":   "/redoc",
        "endpoints": {
            "GET  /health":       "Status da API e banco (sem auth)",
            "POST /buscar":       "FTS na base de legislacao (Free — sem auth)",
            "POST /analisar":     "Grounding juridico — prompt preenchido (Premium)",
            "POST /hermeneutica": "Analise filosofica — prompt preenchido (Premium)",
            "POST /tcc":          "Revisao de TCC — prompt preenchido (Premium)",
        },
        "autenticacao": {
            "free":    "sem header",
            "premium": "X-Fenice-Key: fenice_premium_<sua_chave>",
        },
        "nota": (
            "Nenhum endpoint chama LLMs diretamente. "
            "O campo 'prompt_preenchido' deve ser enviado ao LLM de sua escolha."
        ),
    }


# ---------------------------------------------------------------------------
# Entrypoint dev
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    try:
        import uvicorn
    except ImportError:
        print("uvicorn nao encontrado. Instale: pip install uvicorn fastapi")
        sys.exit(1)

    print("=" * 65)
    print("  Fenice bRain — SaaS API  v1.0.0")
    print("=" * 65)
    print("  Docs:   http://localhost:8001/docs")
    print("  Health: http://localhost:8001/health")
    print("=" * 65)

    uvicorn.run(
        "api_fenice_saas:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
    )
