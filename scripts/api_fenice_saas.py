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
import re as _re
import asyncio as _asyncio
import time as _time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Query, Request, Response
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

# RAG Semântico — módulo independente, falha silenciosa se não instalado
try:
    from fenice_rag_semantic import RAGEngine
    _semantic = RAGEngine()
    _SEMANTIC_DISPONIVEL = _semantic._pronto
except Exception:
    _semantic = None
    _SEMANTIC_DISPONIVEL = False


# ---------------------------------------------------------------------------
# Helpers de autenticação
# ---------------------------------------------------------------------------

def _carregar_chaves_premium() -> set[str]:
    """
    Carrega chaves premium da env FENICE_PREMIUM_KEYS (CSV) em tempo de execução.
    Ex: FENICE_PREMIUM_KEYS=fenice_premium_abc123,fenice_premium_xyz789
    """
    raw = os.getenv("FENICE_PREMIUM_KEYS", "")
    chaves = {k.strip() for k in raw.split(",") if k.strip().startswith("fenice_premium_")}
    return chaves


def _is_premium(x_fenice_key: Optional[str]) -> bool:
    """Retorna True se a chave consta na lista autorizada de chaves premium."""
    if not x_fenice_key:
        return False
    chaves = _carregar_chaves_premium()
    # Fallback: aceita qualquer prefixo fenice_premium_ se a lista não estiver configurada
    if not chaves:
        return x_fenice_key.startswith("fenice_premium_")
    return x_fenice_key in chaves


def _exige_premium(x_fenice_key: Optional[str]) -> None:
    """Levanta 403 se a chave não for Premium válida."""
    if not _is_premium(x_fenice_key):
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito. Endpoint Premium — solicite sua chave em fenice.ia.br.",
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


class LeadRequest(BaseModel):
    nome:             str           = Field(..., min_length=2, max_length=120, description="Nome completo")
    telefone:         str           = Field(..., description="Formato: 55XXXXXXXXXXX")
    email:            str           = Field(..., description="E-mail profissional")
    empresa:          Optional[str] = Field(None, max_length=120, description="Escritório ou empresa")
    interesse:        str           = Field(..., min_length=2, max_length=50,
                                           description="Área IVR: b2b|juridico|academico|observatorio|api|filosofia|outros")
    interesse_label:  str           = Field(..., min_length=2, max_length=100,
                                           description="Rótulo legível: 'B2B Corporativo', etc.")
    descricao_outros: Optional[str] = Field(None, max_length=80,
                                           description="Palavras-chave se interesse=outros")


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

_DEBUG = os.getenv("DEBUG", "false").lower() == "true"

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
    # Swagger/ReDoc só visível em modo DEBUG — em produção fecha para xeretas
    docs_url="/docs" if _DEBUG else None,
    redoc_url="/redoc" if _DEBUG else None,
    openapi_url="/openapi.json" if _DEBUG else None,
)

# CORS restrito aos domínios oficiais Fenice
_ALLOWED_ORIGINS = [
    "https://fenice.ia.br",
    "https://fenice-justech.vercel.app",
    "https://observatorio-da-mulher-sfs.com.br",
    "https://violencia-mulher-sfs.vercel.app",
]
if _DEBUG:
    _ALLOWED_ORIGINS += ["http://localhost:8001", "http://localhost:3000", "http://127.0.0.1:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Fenice-Key", "Authorization"],
)

# Rate-limit simples em memória para /auth (por IP, reset a cada cold start)
_auth_tentativas: dict[str, list[float]] = {}
_AUTH_LIMITE = 5       # máx tentativas
_AUTH_JANELA = 300.0   # janela de 5 minutos

def _checar_rate_limit_auth(ip: str) -> None:
    agora = _time.time()
    hist = [t for t in _auth_tentativas.get(ip, []) if agora - t < _AUTH_JANELA]
    if len(hist) >= _AUTH_LIMITE:
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de login. Aguarde 5 minutos.",
            headers={"Retry-After": "300"},
        )
    hist.append(agora)
    _auth_tentativas[ip] = hist


# Middleware de headers de segurança
@app.middleware("http")
async def _security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"]        = "DENY"
    response.headers["X-Robots-Tag"]           = "noindex, nofollow, nosnippet"
    response.headers["Referrer-Policy"]        = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"]     = "geolocation=(), camera=(), microphone=()"
    return response


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
async def auth_login(body: AuthRequest, request: Request):
    """
    Valida usuário/senha. Registra cada tentativa em fenice_access_logs (Supabase).
    Limitado a 5 tentativas por IP a cada 5 minutos.
    """
    ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() \
         or (request.client.host if request.client else "unknown")
    ua = request.headers.get("user-agent", "")[:300]

    _checar_rate_limit_auth(ip)

    site_user = os.getenv("SITE_USER", "admin")
    site_pass = os.getenv("SITE_PASS", "")

    if not site_pass:
        raise HTTPException(status_code=503, detail="SITE_PASS não configurado no servidor.")

    # ── Usuários autorizados ────────────────────────────────────────────────
    _usuarios_validos: dict[str, str] = {
        site_user:   site_pass,
        "visitante": "123456",
        "puff":      "123456",
        "lorena":    "123456",
        "denny":     "123456",
        "ana":       "123456",
        "kaua":      "123456",
        "kaique":    "123456",
        "nelinha":   "123456",
        "tasso":     "123456",
        "modro":     "123456",
        "ricardo":   "123456",
        "diego":     "123456",
        "manoela":   "123456",
        "douglas":   "123456",
    }

    senha_esperada = _usuarios_validos.get(body.usuario.lower())
    sucesso        = senha_esperada is not None and body.senha == senha_esperada

    # ── Log assíncrono em Supabase ──────────────────────────────────────────
    async def _registrar_log(ok: bool, detalhe: str):
        sb_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        sb_key = os.getenv("SUPABASE_SERVICE_KEY", "")
        if not sb_url or not sb_key:
            return
        try:
            import httpx as _httpx
            async with _httpx.AsyncClient(timeout=4) as cli:
                await cli.post(
                    f"{sb_url}/rest/v1/fenice_access_logs",
                    headers={
                        "apikey":        sb_key,
                        "Authorization": f"Bearer {sb_key}",
                        "Content-Type":  "application/json",
                        "Prefer":        "return=minimal",
                    },
                    json={
                        "usuario":    body.usuario.lower(),
                        "ip":         ip,
                        "user_agent": ua,
                        "sucesso":    ok,
                        "detalhe":    detalhe,
                    },
                )
        except Exception:
            pass  # log nunca bloqueia o login

    if not sucesso:
        await _registrar_log(False, "Usuário ou senha incorretos")
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")

    await _registrar_log(True, "Login bem-sucedido")

    secret = os.getenv("SITE_SECRET", "fenice_secret_fallback")
    ts  = str(int(_time.time()))
    sig = _hmac.new(secret.encode(), f"{body.usuario.lower()}:{ts}".encode(), _hashlib.sha256).hexdigest()[:24]
    return {"ok": True, "token": f"fenice_{ts}_{sig}"}


# ---------------------------------------------------------------------------
# GET /admin/logs  — histórico de acesso (somente admin)
# ---------------------------------------------------------------------------

@app.get(
    "/admin/logs",
    tags=["Admin"],
    summary="Histórico de acessos ao painel (requer X-Fenice-Key)",
)
async def admin_logs(
    request: Request,
    limite: int = 100,
    usuario: str | None = None,
    apenas_falhas: bool = False,
):
    """Retorna os últimos registros de fenice_access_logs."""
    key = request.headers.get("x-fenice-key", "")
    if key != os.getenv("FENICE_API_KEY", ""):
        raise HTTPException(status_code=403, detail="Acesso negado.")

    sb_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    sb_key = os.getenv("SUPABASE_SERVICE_KEY", "")
    hdrs   = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}

    params: dict = {
        "select":  "criado_em,usuario,ip,user_agent,sucesso,detalhe",
        "order":   "criado_em.desc",
        "limit":   str(min(limite, 500)),
    }
    if usuario:
        params["usuario"] = f"eq.{usuario.lower()}"
    if apenas_falhas:
        params["sucesso"] = "eq.false"

    import httpx as _httpx
    async with _httpx.AsyncClient(timeout=8) as cli:
        r = await cli.get(f"{sb_url}/rest/v1/fenice_access_logs", headers=hdrs, params=params)
    r.raise_for_status()
    return r.json()


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
            resultados = await rag.buscar_hibrido(body.query, limite=body.limite, modo="fts")
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
            resultado = await rag.responder_com_contexto(
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
            query_filosofica = body.texto[:200].strip()
            resultados = await rag.buscar_hibrido(query_filosofica, limite=body.limite, modo="fts")
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
            resultados = await rag.buscar_hibrido(body.tema, limite=body.limite, modo="fts")
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
# POST /analisar/semantico  (Premium — RAG vetorial)
# ---------------------------------------------------------------------------

@app.post(
    "/analisar/semantico",
    tags=["Premium"],
    summary="Busca semântica com RAG vetorial + Claude Haiku (Premium)",
)
async def analisar_semantico(
    body: AnalisarRequest,
    x_fenice_key: Optional[str] = Header(None, alias="X-Fenice-Key"),
) -> dict:
    """
    Busca semântica por similaridade vetorial (pgvector) + síntese via Claude Haiku.
    Retorna resposta direta com fontes e nível de confiança LGPD.

    Diferente de `/analisar` (que retorna o prompt para o cliente chamar um LLM),
    este endpoint retorna a resposta já sintetizada.

    **Requer** header `X-Fenice-Key: fenice_premium_<chave>`.
    """
    _exige_premium(x_fenice_key)

    if not _SEMANTIC_DISPONIVEL or _semantic is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Motor semântico indisponível neste ambiente. "
                "Instale sentence-transformers e configure ANTHROPIC_API_KEY."
            ),
        )

    return _semantic.query(body.pergunta)


# ---------------------------------------------------------------------------
# POST /leads  — captura de leads do site
# ---------------------------------------------------------------------------

def _smtp_enviar(smtp_user: str, smtp_pass: str, para: str, assunto: str, corpo: str) -> None:
    """Envia e-mail via Office365 SMTP (bloqueante — rodar em executor)."""
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"]    = smtp_user
    msg["To"]      = para
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.office365.com", 587, timeout=15) as s:
        s.ehlo()
        s.starttls(context=ctx)
        s.login(smtp_user, smtp_pass)
        s.sendmail(smtp_user, [para], msg.as_string())


async def _notificar_lead(lead: "LeadRequest") -> None:
    """Dispara N8N fenice-leads webhook em background. Falha silenciosa."""
    from datetime import datetime
    n8n_url = os.environ.get("N8N_WEBHOOK_LEADS", "")
    if not n8n_url:
        print("[leads] N8N_WEBHOOK_LEADS nao configurado — pulando notificacao")
        return
    payload = {
        "evento":           "novo_lead",
        "nome":             lead.nome,
        "telefone":         lead.telefone,
        "email":            lead.email,
        "empresa":          lead.empresa or "",
        "interesse":        lead.interesse,
        "interesse_label":  lead.interesse_label,
        "descricao_outros": lead.descricao_outros or "",
        "origem":           "fenice.ia.br/contato",
        "timestamp":        datetime.utcnow().isoformat() + "Z",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(n8n_url, json=payload)
    except Exception as exc:
        print(f"[leads] N8N webhook falhou: {exc}")


@app.post("/leads", tags=["Free"], summary="Captura de leads (contato comercial)")
async def capturar_lead(body: LeadRequest, background_tasks: BackgroundTasks) -> dict:
    import re as _re_lead
    import httpx

    if not _re_lead.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", body.email):
        raise HTTPException(status_code=422, detail="E-mail invalido.")

    tel = _re_lead.sub(r"[^0-9]", "", body.telefone)
    if len(tel) == 11:
        tel = "55" + tel
    if not _re_lead.match(r"^55\d{10,11}$", tel):
        raise HTTPException(status_code=422, detail="Telefone invalido. Use formato (XX) XXXXX-XXXX.")
    body = body.model_copy(update={"telefone": tel})

    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        raise HTTPException(status_code=503, detail="Banco de dados nao configurado.")

    hdrs = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }
    payload = {
        "numero":  tel,
        "nome":    body.nome,
        "area":    body.interesse,
        "estagio": "lead_site",
        "dados":   {
            "email":            body.email,
            "empresa":          body.empresa,
            "interesse_label":  body.interesse_label,
            "descricao_outros": body.descricao_outros,
        },
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            f"{sb_url}/rest/v1/fenice_tim_contatos",
            headers=hdrs,
            params={"on_conflict": "numero"},
            json=payload,
        )
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"Erro ao salvar lead: {r.text[:200]}")

    background_tasks.add_task(_notificar_lead, body)
    return {"ok": True, "mensagem": "Recebemos seu contato! Em instantes voce recebera uma mensagem no WhatsApp."}


# ---------------------------------------------------------------------------
# GET /estudos/videos  — hub de vídeos de ensino jurídico
# GET /estudos/videos/forte-marechal-luz  — vídeo documentário
# ---------------------------------------------------------------------------

@app.get("/estudos/videos", tags=["Estudos"], summary="Hub de vídeos jurídicos", response_class=HTMLResponse, include_in_schema=False)
async def estudos_videos() -> HTMLResponse:
    html = Path(__file__).parent / "estudos_videos.html"
    return HTMLResponse(content=html.read_text(encoding="utf-8"), status_code=200)


@app.get("/estudos/videos/forte-marechal-luz", tags=["Estudos"], summary="Vídeo: Forte Marechal Luz", response_class=HTMLResponse, include_in_schema=False)
async def video_forte_marechal_luz() -> HTMLResponse:
    html = Path(__file__).parent / "mallet_forte_view.html"
    return HTMLResponse(content=html.read_text(encoding="utf-8"), status_code=200)


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


@app.get("/logo-fenice.png", tags=["Infraestrutura"], include_in_schema=False)
async def logo_fenice():
    """Serve o logotipo Fenice (phoenix) para a landing page."""
    from fastapi.responses import FileResponse
    logo_path = Path(__file__).parent.parent / "docs" / "logo fenice.png"
    if logo_path.exists():
        return FileResponse(str(logo_path), media_type="image/png")
    from fastapi.responses import Response
    return Response(status_code=404)


# ---------------------------------------------------------------------------
# WhatsApp — constantes, rate-limit e helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Fenice_Tim — IVR WhatsApp multi-projeto
# Roteador inteligente: identifica a área de interesse e personaliza o atendimento
# Perfis: Hunter (novos leads agressivos) | Farmer (base existente — fidelização)
# ---------------------------------------------------------------------------

_wapp_rate: dict[str, list[float]] = {}
_wapp_optouts: set[str] = set()
_WAPP_LIMITE = 15       # máx 15 mensagens por número por hora
_WAPP_JANELA = 3600.0

_STOP_WORDS  = {"parar", "stop", "sair", "cancelar"}
_RESET_WORDS = {"menu", "inicio", "início", "voltar", "0", "reiniciar"}

# Mapa de opção → área interna
_MENU_OPCOES: dict[str, str] = {
    "1": "b2b",
    "2": "academico",
    "3": "observatorio",
    "4": "api",
    "5": "juridico",
    "6": "filosofia",
    "0": "humano",
}

_MSG_TIM_BOAS_VINDAS = (
    "🦅 *Fenice IT Justech.IA* — Central de Atendimento\n\n"
    "Olá! Sou o *Tim*, assistente inteligente da Fenice IT. "
    "Para qual área posso direcioná-lo(a)?\n\n"
    "1️⃣  Mercado Corporativo B2B\n"
    "2️⃣  Ensino Acadêmico Jurídico\n"
    "3️⃣  Observatório da Mulher SFS\n"
    "4️⃣  API REST / Desenvolvedores\n"
    "5️⃣  Atendimento Jurídico Individual\n"
    "6️⃣  Filosofia, Teologia e Pensamento _(em breve)_\n"
    "0️⃣  Falar com Especialista Humano\n\n"
    "Digite o *número* da opção desejada.\n\n"
    "_© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno_"
)

_MSG_PARAR = (
    "Atendimento encerrado. Obrigado por contatar a *Fenice IT Justech.IA*! 🙏\n"
    "Quando precisar, é só chamar novamente.\n\n"
    "_© 2026 Fenice IT Justech.IA_"
)

_MSG_HUMANO = (
    "👤 *Atendimento Humano Solicitado*\n\n"
    "Anotamos seu contato! Um especialista da Fenice IT entrará em contato em breve.\n\n"
    "📧 contato@fenice.ia.br\n"
    "🌐 fenice.ia.br\n\n"
    "_© 2026 Fenice IT Justech.IA_"
)

_MSG_FALLBACK = (
    "Nosso assistente está com alta demanda agora. "
    "Tente novamente em 1 minuto ou entre em contato: contato@fenice.ia.br"
)

# System prompts por área — personalizados para cada jornada
_SYSTEM_PROMPTS: dict[str, str] = {
    "b2b": (
        "Você é o assistente comercial B2B da Fenice IT Justech.IA, atendendo via WhatsApp. "
        "Seu foco: apresentar as soluções corporativas da Fenice IT para escritórios de advocacia, "
        "empresas e departamentos jurídicos. "
        "Destaque: API jurídica com RAG, integração com sistemas legados, planos enterprise, SLA. "
        "Seja consultivo e direto. Colete nome, empresa e necessidade do prospect. "
        "Se demonstrar interesse real → ofereça agenda de demo: contato@fenice.ia.br. "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno da Silva Neto"
    ),
    "academico": (
        "Você é o assistente acadêmico da Fenice IT Justech.IA, atendendo via WhatsApp. "
        "Foco: auxiliar estudantes e professores de direito com pesquisa jurídica, TCC, "
        "monografias, artigos científicos. Base: 5685 artigos indexados, súmulas STJ/STF, legislação federal. "
        "Seja didático, cite artigos e súmulas relevantes, incentive a pesquisa autônoma. "
        "Se precisar de acesso premium → direcione para fenice.ia.br/premium. "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno da Silva Neto"
    ),
    "observatorio": (
        "Você é o assistente do Observatório da Mulher SFS (Fenice IT), atendendo via WhatsApp. "
        "Foco: apoio a vítimas de violência doméstica e familiar, informação sobre direitos, "
        "canais de denúncia (190, 197, 180), Lei Maria da Penha (Lei 11.340/2006). "
        "Seja acolhedor, empático e claro. NUNCA minimize o relato. "
        "Em situação de risco → indique IMEDIATAMENTE: ligue 190 (emergência) ou 180 (Central da Mulher). "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA"
    ),
    "api": (
        "Você é o assistente técnico da Fenice IT Justech.IA, atendendo desenvolvedores via WhatsApp. "
        "Foco: API REST fenice.ia.br — endpoints /buscar (Free), /analisar, /hermeneutica, /tcc (Premium). "
        "Auth: header X-Fenice-Key. Stack: FastAPI + Supabase + Groq + pgvector. "
        "Seja técnico e preciso. Forneça exemplos de código em Python/JS quando útil. "
        "Documentação: fenice.ia.br/docs (ativada em modo DEBUG). "
        "Chaves premium: contato@fenice.ia.br. "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno da Silva Neto"
    ),
    "juridico": (
        "Você é o assistente jurídico individual da Fenice IT Justech.IA, atendendo via WhatsApp. "
        "Conhecimento sólido em direito brasileiro: Código Civil, CLT, Código Penal, CF/88, CDC. "
        "Seja profissional, empático e objetivo. Máx. 800 caracteres por resposta (WhatsApp). "
        "Se não tiver certeza jurídica → diga: 'Não temos resposta imediata — posso pesquisar para você.' "
        "Nunca invente leis, artigos ou jurisprudência inexistentes. "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno da Silva Neto"
    ),
    "filosofia": (
        "Você é o assistente de Filosofia, Teologia e Pensamento da Fenice IT Justech.IA, via WhatsApp. "
        "Domínio: filosofia jurídica, hermenêutica, filosofia ocidental e oriental, teologia cristã, islâmica e judaica, "
        "pensamento crítico, ética, metafísica, epistemologia. "
        "Seja reflexivo, profundo e acessível. Cite pensadores relevantes (Aristóteles, Tomás de Aquino, Kant, Hegel, etc.). "
        "Relacione o pensamento filosófico com o direito e a vida prática quando cabível. "
        "Este módulo está em desenvolvimento — convide o cliente para acompanhar o lançamento em fenice.ia.br. "
        "Cliente: {nome}. "
        "© 2026 Fenice IT Justech.IA — Tech Lead: Ramão Bueno da Silva Neto"
    ),
}


def _wapp_rate_ok(numero: str) -> bool:
    """Retorna False se o número excedeu o limite de mensagens por hora."""
    agora = _time.time()
    hist = [t for t in _wapp_rate.get(numero, []) if agora - t < _WAPP_JANELA]
    if len(hist) >= _WAPP_LIMITE:
        return False
    hist.append(agora)
    _wapp_rate[numero] = hist
    return True


async def _enviar_avisa(client: Any, avisa_tkn: str, numero: str, msg: str) -> tuple[int, bool]:
    """Envia mensagem via AvisaAPI. Retorna (http_status, entregue)."""
    try:
        r = await client.post(
            "https://www.avisaapi.com.br/api/actions/sendMessage",
            headers={"Authorization": f"Bearer {avisa_tkn}", "Content-Type": "application/json"},
            json={"number": numero, "message": msg},
        )
        data = r.json() if r.status_code < 300 else {}
        return r.status_code, data.get("status") is True
    except Exception:
        return 0, False


async def _log_whatsapp(
    client: Any, sb_url: str, sb_key: str,
    numero: str, nome: str, session_id: Optional[str], message_id: Optional[str],
    mensagem: str, resposta_ai: str, groq_data: dict,
    entregue: bool, http_st_avisa: int,
) -> None:
    """Registra interação no Supabase (falha silenciosa)."""
    if not sb_url or not sb_key:
        return
    try:
        await client.post(
            f"{sb_url}/rest/v1/interacoes_whatsapp",
            headers={
                "apikey": sb_key,
                "Authorization": f"Bearer {sb_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json={
                "numero_remetente":  numero,
                "nome_remetente":    nome,
                "session_id":        session_id,
                "message_id":        message_id,
                "mensagem_cliente":  mensagem,
                "resposta_ai":       resposta_ai,
                "modelo_ai":         groq_data.get("model", "llama-3.3-70b-versatile"),
                "provider":          "avisa",
                "canal":             "whatsapp",
                "entregue":          entregue,
                "http_status_avisa": http_st_avisa,
            },
            timeout=8.0,
        )
    except Exception:
        pass


async def _historico_conversa(client: Any, numero: str, sb_url: str, sb_key: str) -> list[dict]:
    """Recupera as últimas 5 interações do número para memória conversacional."""
    if not sb_url or not sb_key:
        return []
    try:
        r = await client.get(
            f"{sb_url}/rest/v1/interacoes_whatsapp",
            headers={"apikey": sb_key, "Authorization": f"Bearer {sb_key}"},
            params={
                "select": "mensagem_cliente,resposta_ai",
                "numero_remetente": f"eq.{numero}",
                "order": "created_at.desc",
                "limit": "5",
            },
            timeout=6.0,
        )
        if r.status_code == 200:
            return list(reversed(r.json() or []))
    except Exception:
        pass
    return []


async def _rag_grounding(client: Any, mensagem: str, sb_url: str, sb_key: str) -> str:
    """Busca legislação relevante no Supabase para fundamentar a resposta juridicamente."""
    if not sb_url or not sb_key:
        return ""
    try:
        r = await client.get(
            f"{sb_url}/rest/v1/legislacao_brasileira",
            headers={"apikey": sb_key, "Authorization": f"Bearer {sb_key}"},
            params={
                "select": "numero_ano,ementa",
                "busca_idx": f"plfts(portuguese_unaccent).{mensagem[:150]}",
                "limit": "3",
            },
            timeout=6.0,
        )
        if r.status_code == 200 and r.json():
            linhas = [
                f"• {d['numero_ano']}: {(d.get('ementa') or '')[:200]}"
                for d in r.json()[:3]
            ]
            return "Legislação de referência:\n" + "\n".join(linhas)
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# POST /webhook/avisa  — AvisaAPI WhatsApp inbound webhook
# ---------------------------------------------------------------------------

async def _tim_get_contato(client: Any, numero: str, sb_url: str, sb_key: str) -> dict:
    """Recupera dados do contato no fenice_tim_contatos."""
    if not sb_url or not sb_key:
        return {}
    try:
        r = await client.get(
            f"{sb_url}/rest/v1/fenice_tim_contatos",
            headers={"apikey": sb_key, "Authorization": f"Bearer {sb_key}"},
            params={"select": "*", "numero": f"eq.{numero}", "limit": "1"},
            timeout=5.0,
        )
        if r.status_code == 200 and r.json():
            return r.json()[0]
    except Exception:
        pass
    return {}


async def _tim_upsert_contato(
    client: Any, sb_url: str, sb_key: str,
    numero: str, nome: str, area: Optional[str] = None,
    estagio: str = "prospect", perfil: Optional[str] = None,
) -> None:
    """Cria ou atualiza contato no fenice_tim_contatos."""
    if not sb_url or not sb_key:
        return
    payload: dict = {
        "numero": numero,
        "nome": nome,
        "estagio": estagio,
        "ultimo_contato": datetime.utcnow().isoformat() + "Z",
    }
    if area is not None:
        payload["area"] = area
    if perfil is not None:
        payload["perfil"] = perfil
    try:
        await client.post(
            f"{sb_url}/rest/v1/fenice_tim_contatos",
            headers={
                "apikey": sb_key, "Authorization": f"Bearer {sb_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates,return=minimal",
            },
            json=payload,
            timeout=5.0,
        )
    except Exception:
        pass


async def _processar_mensagem_whatsapp(
    numero: str,
    nome: str,
    mensagem: str,
    session_id: Optional[str],
    message_id: Optional[str],
) -> None:
    """
    Fenice_Tim — roteador inteligente de atendimento WhatsApp.
    Fluxo: identifica área → roteia para prompt especializado → RAG + histórico → Groq → AvisaAPI.
    """
    import httpx

    groq_key  = os.getenv("GROQ_API_KEY", "")
    avisa_tkn = os.getenv("AVISA_API_TOKEN", "")
    sb_url    = os.getenv("SUPABASE_URL", "").rstrip("/")
    sb_key    = os.getenv("SUPABASE_SERVICE_KEY", "")

    msg_lower = mensagem.strip().lower().rstrip("!.?")

    # ── PARAR — opt-out ────────────────────────────────────────────────────
    if msg_lower in _STOP_WORDS:
        async with httpx.AsyncClient(timeout=15.0) as client:
            http_st, entregue = await _enviar_avisa(client, avisa_tkn, numero, _MSG_PARAR)
            await _log_whatsapp(client, sb_url, sb_key, numero, nome, session_id, message_id,
                                mensagem, _MSG_PARAR, {}, entregue, http_st)
            _wapp_optouts.add(numero)
            if sb_url and sb_key:
                try:
                    await client.post(
                        f"{sb_url}/rest/v1/whatsapp_optouts",
                        headers={
                            "apikey": sb_key, "Authorization": f"Bearer {sb_key}",
                            "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates",
                        },
                        json={"numero": numero, "nome": nome},
                        timeout=5.0,
                    )
                except Exception:
                    pass
        return

    try:
        async with httpx.AsyncClient(timeout=35.0) as client:
            # ── Recupera perfil do contato ─────────────────────────────────
            contato = await _tim_get_contato(client, numero, sb_url, sb_key)
            area_atual = contato.get("area")

            # ── RESET — volta ao menu principal ───────────────────────────
            if msg_lower in _RESET_WORDS:
                await _tim_upsert_contato(client, sb_url, sb_key, numero, nome, area=None)
                http_st, entregue = await _enviar_avisa(client, avisa_tkn, numero, _MSG_TIM_BOAS_VINDAS)
                await _log_whatsapp(client, sb_url, sb_key, numero, nome, session_id, message_id,
                                    mensagem, _MSG_TIM_BOAS_VINDAS, {}, entregue, http_st)
                return

            # ── NOVO CONTATO ou sem área definida → exibe menu ────────────
            if not area_atual:
                opcao = msg_lower.strip()
                area_escolhida = _MENU_OPCOES.get(opcao)

                if area_escolhida == "humano":
                    await _tim_upsert_contato(client, sb_url, sb_key, numero, nome,
                                              area="humano", estagio="atendimento")
                    http_st, entregue = await _enviar_avisa(client, avisa_tkn, numero, _MSG_HUMANO)
                    await _log_whatsapp(client, sb_url, sb_key, numero, nome, session_id, message_id,
                                        mensagem, _MSG_HUMANO, {}, entregue, http_st)
                    return

                if area_escolhida == "filosofia":
                    await _tim_upsert_contato(client, sb_url, sb_key, numero, nome,
                                              area="filosofia", estagio="prospect")
                    area_atual = "filosofia"
                elif area_escolhida:
                    await _tim_upsert_contato(client, sb_url, sb_key, numero, nome,
                                              area=area_escolhida, estagio="prospect")
                    area_atual = area_escolhida
                else:
                    # Primeira mensagem (não é número) ou opção inválida → boas-vindas
                    await _tim_upsert_contato(client, sb_url, sb_key, numero, nome)
                    http_st, entregue = await _enviar_avisa(client, avisa_tkn, numero, _MSG_TIM_BOAS_VINDAS)
                    await _log_whatsapp(client, sb_url, sb_key, numero, nome, session_id, message_id,
                                        mensagem, _MSG_TIM_BOAS_VINDAS, {}, entregue, http_st)
                    return

            # ── ÁREA DEFINIDA → resposta especializada ─────────────────────
            template_sistema = _SYSTEM_PROMPTS.get(area_atual or "juridico", _SYSTEM_PROMPTS["juridico"])
            sistema_base = template_sistema.format(nome=nome)

            # RAG jurídico (só para áreas que usam legislação)
            rag_areas = {"juridico", "b2b", "academico", "observatorio"}
            historico, contexto_rag = await _asyncio.gather(
                _historico_conversa(client, numero, sb_url, sb_key),
                _rag_grounding(client, mensagem, sb_url, sb_key) if area_atual in rag_areas else _asyncio.sleep(0),
            )
            sistema = sistema_base
            if contexto_rag and isinstance(contexto_rag, str):
                sistema += f"\n\n{contexto_rag}"

            # Monta histórico conversacional
            messages: list[dict] = [{"role": "system", "content": sistema}]
            for h in (historico or []):
                if h.get("mensagem_cliente"):
                    messages.append({"role": "user", "content": h["mensagem_cliente"]})
                if h.get("resposta_ai"):
                    messages.append({"role": "assistant", "content": h["resposta_ai"]})
            messages.append({"role": "user", "content": mensagem})

            # Groq — gera resposta com retry 429
            groq_data: dict = {}
            for _tentativa in range(3):
                groq_resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.3-70b-versatile", "messages": messages,
                          "max_tokens": 800, "temperature": 0.7},
                )
                if groq_resp.status_code == 429:
                    _wait = int(groq_resp.headers.get("retry-after", 2 * (2 ** _tentativa)))
                    await _asyncio.sleep(_wait)
                    continue
                groq_data = groq_resp.json()
                break

            resposta_ai = (
                groq_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                or _MSG_FALLBACK
            )

            # Atualiza último contato no Tim
            await _tim_upsert_contato(client, sb_url, sb_key, numero, nome, area=area_atual)

            # Envia e registra
            http_st_avisa, entregue = await _enviar_avisa(client, avisa_tkn, numero, resposta_ai)
            await _log_whatsapp(client, sb_url, sb_key, numero, nome, session_id, message_id,
                                mensagem, resposta_ai, groq_data, entregue, http_st_avisa)
    except Exception:
        pass


@app.post(
    "/webhook/avisa",
    tags=["WhatsApp"],
    include_in_schema=False,
    status_code=200,
)
async def webhook_avisa(request: Request):
    """
    Recebe mensagens WhatsApp da AvisaAPI, processa com Groq (+ RAG + histórico)
    e responde ao cliente. Síncrono (await) para garantir execução em Vercel serverless.
    """
    try:
        body = await request.json()
    except Exception:
        return {"ok": True, "status": "ignored"}

    raw_numero = (
        body.get("number") or body.get("from") or body.get("sender") or body.get("phone") or ""
    )
    numero = _re.sub(r"\D", "", str(raw_numero))
    mensagem = (
        body.get("message") or body.get("text") or body.get("body") or body.get("content") or ""
    ).strip()
    nome       = body.get("name") or body.get("pushName") or body.get("from_name") or "Cliente"
    session_id = body.get("session") or body.get("session_id") or body.get("chatId")
    message_id = body.get("id") or body.get("message_id") or body.get("msgId")

    if not numero or not mensagem:
        return {"ok": True, "status": "ignored"}

    # Rate limit por número (10 msgs/hora)
    if not _wapp_rate_ok(numero):
        return {"ok": True, "status": "rate_limited"}

    # Verifica opt-out (ignora números que enviaram PARAR)
    # Usa cache em memória para evitar DB lookup em toda mensagem
    if numero in _wapp_optouts:
        return {"ok": True, "status": "optout"}

    await _processar_mensagem_whatsapp(numero, nome, mensagem, session_id, message_id)
    return {"ok": True, "status": "processed"}


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
