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

import hashlib as _hashlib
import hmac as _hmac
import os
import time as _time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).parent.parent / ".env")

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

class AuthRequest(BaseModel):
    usuario: str = Field(..., min_length=1, max_length=64, description="Nome de usuário")
    senha:   str = Field(..., min_length=1, max_length=128, description="Senha")


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
# POST /auth  — login do painel
# ---------------------------------------------------------------------------

@app.post(
    "/auth",
    tags=["Acesso"],
    summary="Autenticação do painel (modal de login)",
)
async def auth_login(body: AuthRequest):
    """
    Valida usuário/senha contra as variáveis de ambiente `SITE_USER` e `SITE_PASS`.
    Retorna um token de sessão a ser armazenado no client (sessionStorage).
    """
    site_user = os.getenv("SITE_USER", "admin")
    site_pass = os.getenv("SITE_PASS", "")

    if not site_pass:
        raise HTTPException(status_code=503, detail="SITE_PASS não configurado no servidor.")

    if body.usuario != site_user or body.senha != site_pass:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")

    secret = os.getenv("SITE_SECRET", "fenice_secret_fallback")
    ts = str(int(_time.time()))
    sig = _hmac.new(secret.encode(), f"{body.usuario}:{ts}".encode(), _hashlib.sha256).hexdigest()[:24]
    return {"ok": True, "token": f"fenice_{ts}_{sig}"}


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
# GET /lei  — texto completo de uma lei pelo numero_ano (Free)
# ---------------------------------------------------------------------------

@app.get(
    "/lei",
    tags=["Free"],
    summary="Texto completo de uma lei pelo numero_ano",
)
async def get_lei(numero_ano: str):
    """
    Retorna ementa e texto_vigente de uma lei específica.
    Exemplo: /lei?numero_ano=Lei+Federal+13105/2015
    """
    import requests as _req
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Supabase não configurado.")
    try:
        hdrs = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}
        r = _req.get(
            f"{sb_url}/rest/v1/legislacao_brasileira",
            headers=hdrs,
            params={"select": "numero_ano,tipo_ato,ementa,texto_vigente",
                    "numero_ano": f"eq.{numero_ano}", "limit": "1"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            raise HTTPException(status_code=404, detail="Lei não encontrada.")
        return data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# GET /artigo  — texto de um artigo específico (indexed, Free)
# ---------------------------------------------------------------------------

@app.get("/artigo", tags=["Free"], summary="Texto de um artigo pelo número")
async def get_artigo(lei: str, numero: int):
    """
    Retorna o texto de um artigo específico da tabela `artigos`.
    Exemplo: /artigo?lei=Lei+Federal+13105/2015&numero=235
    """
    import requests as _req
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Supabase não configurado.")
    try:
        hdrs = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}
        r = _req.get(
            f"{sb_url}/rest/v1/artigos",
            headers=hdrs,
            params={"select": "numero,texto", "lei": f"eq.{lei}",
                    "numero": f"eq.{numero}", "limit": "1"},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            raise HTTPException(status_code=404, detail="Artigo não encontrado.")
        return data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# GET /lei_info  — metadados de artigos de uma lei (Free)
# ---------------------------------------------------------------------------

@app.get("/lei_info", tags=["Free"], summary="Metadados de artigos de uma lei")
async def get_lei_info(lei: str):
    """
    Retorna total de artigos indexados e maior número de artigo de uma lei.
    Exemplo: /lei_info?lei=Lei+Federal+13105/2015
    """
    import requests as _req
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Supabase não configurado.")
    try:
        hdrs = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}",
                "Prefer": "count=exact"}
        r = _req.get(
            f"{sb_url}/rest/v1/artigos",
            headers=hdrs,
            params={"select": "numero", "lei": f"eq.{lei}",
                    "order": "numero.desc", "limit": "1"},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        total = int(r.headers.get("content-range", "0/0").split("/")[-1] or 0)
        max_num = data[0]["numero"] if data else 0
        return {"lei": lei, "total": total, "max_numero": max_num}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# GET /leis  — lista de leis disponíveis no banco (Free)
# ---------------------------------------------------------------------------

@app.get(
    "/leis",
    tags=["Free"],
    summary="Lista todas as leis indexadas",
)
async def listar_leis(tipo: Optional[str] = None):
    """
    Lista numero_ano e tipo_ato de todas as leis (ou filtra por tipo).
    Exemplo: /leis?tipo=Lei+Federal
    """
    import requests as _req
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Supabase não configurado.")
    try:
        hdrs = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}
        params: dict = {"select": "numero_ano,tipo_ato,ementa",
                        "order": "numero_ano", "limit": "500"}
        if tipo:
            params["tipo_ato"] = f"eq.{tipo}"
        r = _req.get(f"{sb_url}/rest/v1/legislacao_brasileira",
                     headers=hdrs, params=params, timeout=15)
        r.raise_for_status()
        return r.json() or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
# GET /grafo  — Graph View data
# ---------------------------------------------------------------------------

@app.get("/grafo", tags=["Free"], summary="Dados do grafo jurídico para visualização D3")
async def get_grafo(limite: int = Query(400, ge=20, le=800)):
    """
    Retorna nós e arestas para renderização do Graph View estilo Obsidian.
    Combina o Knowledge Graph (grafo_nos/grafo_arestas) com nós sintetizados
    da tabela legislacao_brasileira, agrupados por domínio jurídico.
    """
    import requests as _req

    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Supabase não configurado.")

    hdrs = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
    }

    def _get(table: str, params: dict) -> list:
        r = _req.get(f"{sb_url}/rest/v1/{table}", headers=hdrs, params=params, timeout=15)
        r.raise_for_status()
        return r.json() or []

    try:
        # ── Knowledge Graph explícito ──────────────────────────────────────
        nos_kg = _get("grafo_nos", {"select": "id,tipo,identificador,titulo,descricao"})
        arestas_kg = _get("grafo_arestas", {
            "select": "id,no_origem_id,no_destino_id,tipo_relacao,peso"
        })

        # ── Amostragem de legislação por tipo ─────────────────────────────
        quota = str(min(limite // 3, 140))
        amostras = [
            ("Súmula STJ",  "stj", min(int(quota), 140)),
            ("Súmula STF",  "stf", min(int(quota), 140)),
            ("Lei Federal", "lei", 60),
            ("Decreto-Lei", "lei", 15),
            ("Decreto",     "lei", 10),
        ]

        nos_leg:     list[dict] = []
        arestas_leg: list[dict] = []
        hub_seen:    set[str]   = set()

        for tipo_ato, grupo, n in amostras:
            rows = _get("legislacao_brasileira", {
                "select":   "numero_ano,ementa",
                "tipo_ato": f"eq.{tipo_ato}",
                "limit":    str(n),
            })
            if not rows:
                continue

            hub_id = f"hub-{tipo_ato.replace(' ', '_').lower()}"
            if hub_id not in hub_seen:
                hub_seen.add(hub_id)
                nos_leg.append({
                    "id": hub_id, "tipo": f"hub-{grupo}",
                    "titulo": tipo_ato, "descricao": f"{len(rows)} documentos",
                    "grupo": grupo, "tamanho": "hub",
                })

            for row in rows:
                nid = "l-" + row["numero_ano"].replace(" ", "_").replace("/", "-")
                nos_leg.append({
                    "id": nid, "tipo": grupo,
                    "titulo": row["numero_ano"],
                    "descricao": (row.get("ementa") or "")[:100],
                    "grupo": grupo, "tamanho": "doc",
                })
                arestas_leg.append({
                    "id": f"ae-{hub_id[:10]}-{nid[-10:]}",
                    "origem": hub_id, "destino": nid,
                    "tipo": "contém", "peso": 0.8,
                })

        # ── Normalizar nós do KG ───────────────────────────────────────────
        _COR_KG = {
            "filosofo": "#ec4899", "artigo": "#f59e0b",
            "conceito": "#06b6d4", "lei":    "#8b5cf6",
        }
        nos_final: list[dict] = [
            {
                "id":        str(n["id"]),
                "tipo":      n["tipo"],
                "titulo":    n.get("titulo") or n.get("identificador") or "",
                "descricao": n.get("descricao") or "",
                "grupo":     n["tipo"],
                "tamanho":   "conceito" if n["tipo"] == "conceito" else "doc",
                "cor":       _COR_KG.get(n["tipo"], "#94a3b8"),
            }
            for n in nos_kg
        ] + nos_leg

        arestas_final: list[dict] = [
            {
                "id":      str(a["id"]),
                "origem":  str(a["no_origem_id"]),
                "destino": str(a["no_destino_id"]),
                "tipo":    a.get("tipo_relacao") or "related",
                "peso":    float(a.get("peso") or 1.0),
            }
            for a in arestas_kg
        ] + arestas_leg

        return {
            "nos":           nos_final,
            "arestas":       arestas_final,
            "total_nos":     len(nos_final),
            "total_arestas": len(arestas_final),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /  — info
# ---------------------------------------------------------------------------

@app.get("/", tags=["Infraestrutura"], summary="Landing page", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve a landing page visual da API Fenice bRain."""
    landing = Path(__file__).parent / "landing.html"
    if landing.exists():
        return HTMLResponse(content=landing.read_text(encoding="utf-8"), status_code=200)
    # fallback JSON se o arquivo não estiver disponível
    from fastapi.responses import JSONResponse
    return JSONResponse({
        "titulo": "Fenice bRain — SaaS API",
        "versao": "1.0.0",
        "docs":   "/docs",
    })


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
