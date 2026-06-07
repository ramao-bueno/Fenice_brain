#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API FastAPI para Fenice Brain — STF Jurisprudência
Endpoints para buscar Súmulas Vinculantes e Temas de Repercussão Geral
"""
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
import os
from datetime import datetime

# =====================================================================
# Configuração
# =====================================================================
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'fenice_brain')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
API_KEY = os.getenv('API_KEY', 'sua_chave_secreta_aqui')

# =====================================================================
# Models Pydantic
# =====================================================================
class SumulaResponse(BaseModel):
    numero_identificador: str
    tipo: str
    processo_paradigma: Optional[str]
    data_publicacao: Optional[str]
    setor_afetado: Optional[str]
    houve_modulacao: bool
    potencial_monetario: Optional[str]
    keywords: Optional[List[str]]
    status: str

    class Config:
        from_attributes = True


class SumulaDetalheResponse(SumulaResponse):
    enunciado_original: Optional[str]
    nucleo_da_tese: Optional[str]
    artigos_cf88: Optional[List[str]]
    regra_modulacao: Optional[str]
    vulnerabilidade_compliance: Optional[str]
    confiabilidade: float
    requer_revisao_manual: bool


class AlertaResponse(BaseModel):
    numero_identificador: str
    setor_afetado: Optional[str]
    regra_modulacao: Optional[str]
    acao_necessaria: str


class SetorStats(BaseModel):
    setor_afetado: str
    total: int
    com_modulacao: int
    ultima_alteracao: Optional[str]


# =====================================================================
# Contexto de DB
# =====================================================================
@contextmanager
def get_db_connection():
    """Gerenciador de contexto para conexão PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        yield conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    finally:
        if conn:
            conn.close()


def verificar_api_key(api_key: str = Query(..., description="API Key para autenticação")):
    """Verifica API Key."""
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")
    return api_key


# =====================================================================
# Inicializar FastAPI
# =====================================================================
app = FastAPI(
    title="Fenice Brain — STF API",
    description="API de Jurisprudência STF (Súmulas Vinculantes + Temas RG)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# Endpoints
# =====================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check da API."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stf.sumulas")
            count = cursor.fetchone()[0]
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "sumulas_total": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/sumulas",
    response_model=List[SumulaResponse],
    tags=["Súmulas"],
    summary="Listar todas as Súmulas Vinculantes e Temas RG"
)
async def listar_sumulas(
    tipo: Optional[str] = Query(None, description="SUMULA_VINCULANTE ou TEMA_REPERCUSSAO_GERAL"),
    setor: Optional[str] = Query(None, description="Filtrar por setor"),
    modulacao: Optional[bool] = Query(None, description="Filtrar por modulação"),
    limit: int = Query(50, ge=1, le=1000, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    api_key: str = Depends(verificar_api_key)
):
    """Listar súmulas com filtros opcionais."""
    sql = "SELECT numero_identificador, tipo, processo_paradigma, data_publicacao, setor_afetado, houve_modulacao, potencial_monetario, keywords, status FROM stf.sumulas WHERE 1=1"
    params = []

    if tipo:
        sql += " AND tipo = %s"
        params.append(tipo)
    if setor:
        sql += " AND setor_afetado = %s"
        params.append(setor)
    if modulacao is not None:
        sql += " AND houve_modulacao = %s"
        params.append(modulacao)

    sql += f" ORDER BY numero_numerico LIMIT {limit} OFFSET {offset}"

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/sumulas/{numero_id}",
    response_model=SumulaDetalheResponse,
    tags=["Súmulas"],
    summary="Obter detalhes de uma Súmula"
)
async def obter_sumula(
    numero_id: str,
    api_key: str = Depends(verificar_api_key)
):
    """Obter detalhes completos de uma súmula."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "SELECT * FROM stf.sumulas WHERE numero_identificador = %s",
                [numero_id]
            )
            row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Súmula não encontrada")

        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/sumulas/buscar",
    response_model=List[SumulaResponse],
    tags=["Busca"],
    summary="Busca Semântica por Palavras-Chave (RAG)"
)
async def buscar_por_keywords(
    keywords: List[str] = Query(..., description="Lista de palavras-chave para busca"),
    limite: int = Query(10, ge=1, le=100),
    api_key: str = Depends(verificar_api_key)
):
    """Buscar súmulas por palavras-chave usando função RAG."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "SELECT numero_identificador, tipo, processo_paradigma, data_publicacao, setor_afetado, houve_modulacao, potencial_monetario, keywords, status FROM stf.buscar_por_keywords(%s, %s)",
                [keywords, limite]
            )
            rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/sumulas/com-modulacao",
    response_model=List[SumulaResponse],
    tags=["Alertas"],
    summary="Listar Súmulas com Modulação de Efeitos (Críticas)"
)
async def sumulas_com_modulacao(
    api_key: str = Depends(verificar_api_key)
):
    """Súmulas que tiveram modulação de efeitos — críticas para compliance."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM stf.sumulas_com_modulacao")
            rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/sumulas/por-setor",
    response_model=List[SetorStats],
    tags=["Estatísticas"],
    summary="Estatísticas por Setor"
)
async def sumulas_por_setor(
    api_key: str = Depends(verificar_api_key)
):
    """Agrupar súmulas por setor afetado com contagens."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM stf.sumulas_por_setor")
            rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/alertas/compliance",
    response_model=List[AlertaResponse],
    tags=["Alertas"],
    summary="Alertas de Compliance (Modulações Críticas)"
)
async def alertas_compliance(
    api_key: str = Depends(verificar_api_key)
):
    """Alertas para compliance — súmulas que requerem revisão manual."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM stf.alertar_modulacoes()")
            rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/estatisticas",
    tags=["Estatísticas"],
    summary="Estatísticas Gerais"
)
async def estatisticas_gerais(
    api_key: str = Depends(verificar_api_key)
):
    """Estatísticas gerais da base de dados."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Total por tipo
            cursor.execute("""
            SELECT tipo, COUNT(*) as total,
                   COUNT(CASE WHEN houve_modulacao THEN 1 END) as com_modulacao
            FROM stf.sumulas
            GROUP BY tipo
            """)
            stats = cursor.fetchall()

            return {
                "timestamp": datetime.now().isoformat(),
                "sumulas": [dict(row) for row in stats],
                "total_geral": sum(row['total'] for row in stats)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# Root
# =====================================================================
class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="Texto para busca semântica", min_length=3, max_length=500)
    limite: int = Field(10, ge=1, le=50, description="Número de resultados")
    threshold: float = Field(0.5, ge=0.0, le=1.0, description="Limite mínimo de similaridade")


class SemanticSearchResult(BaseModel):
    numero_identificador: str
    tipo: str
    setor_afetado: Optional[str]
    similarity_score: float
    enunciado_original: Optional[str]
    match_type: str = "SEMANTIC"


@app.post(
    "/sumulas/buscar-semantica",
    response_model=List[SemanticSearchResult],
    tags=["RAG"],
    summary="Busca Semântica com Embeddings (OpenAI)"
)
async def buscar_semantica(
    request: SemanticSearchRequest,
    api_key: str = Depends(verificar_api_key)
):
    """
    Busca semântica usando embeddings OpenAI + pgvector.
    Requer que embeddings tenham sido gerados com embeddings_openai_generator.py
    """
    try:
        from embeddings_rag_retriever import RAGRetriever

        retriever = RAGRetriever()
        if not retriever.conectar():
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")

        resultados = retriever.buscar_semanticamente(
            request.query,
            limite=request.limite,
            similarity_threshold=request.threshold
        )

        retriever.fechar()

        return [
            SemanticSearchResult(
                numero_identificador=r.numero_identificador,
                tipo=r.tipo,
                setor_afetado=r.setor_afetado,
                similarity_score=r.similarity_score,
                enunciado_original=r.enunciado_original,
                match_type=r.match_type
            )
            for r in resultados
        ]

    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="RAG Retriever não disponível. Execute: pip install openai && python embeddings_openai_generator.py"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/sumulas/buscar-hibrida",
    response_model=List[SemanticSearchResult],
    tags=["RAG"],
    summary="Busca Híbrida (Semântica + Keywords)"
)
async def buscar_hibrida(
    request: SemanticSearchRequest,
    keywords: Optional[List[str]] = Query(None, description="Palavras-chave adicionais"),
    alpha: float = Query(0.5, ge=0.0, le=1.0, description="Peso da busca semântica (0-1)"),
    api_key: str = Depends(verificar_api_key)
):
    """
    Busca combinando semântica (embeddings) e busca por keywords.
    - alpha=1.0: 100% semântica
    - alpha=0.5: 50/50 semântica e keywords
    - alpha=0.0: 100% keywords
    """
    try:
        from embeddings_rag_retriever import RAGRetriever

        retriever = RAGRetriever()
        if not retriever.conectar():
            raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")

        resultados = retriever.buscar_hibrida(
            request.query,
            keywords=keywords,
            limite=request.limite,
            alpha=alpha
        )

        retriever.fechar()

        return [
            SemanticSearchResult(
                numero_identificador=r.numero_identificador,
                tipo=r.tipo,
                setor_afetado=r.setor_afetado,
                similarity_score=r.similarity_score,
                enunciado_original=r.enunciado_original,
                match_type=r.match_type
            )
            for r in resultados
        ]

    except ImportError:
        raise HTTPException(status_code=503, detail="RAG Retriever não disponível")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/embeddings/stats",
    tags=["RAG"],
    summary="Estatísticas de Embeddings"
)
async def embeddings_stats(
    api_key: str = Depends(verificar_api_key)
):
    """Verificar quantos embeddings foram gerados."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM stf.embedding_stats")
            row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Nenhum embedding encontrado")

        return dict(row)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", tags=["Info"])
async def root():
    """Info da API."""
    return {
        "title": "Fenice Brain — STF Jurisprudência API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "sumulas": "/sumulas",
            "buscar": "/sumulas/buscar (POST)",
            "buscar_semantica": "/sumulas/buscar-semantica (POST) — Requer embeddings",
            "buscar_hibrida": "/sumulas/buscar-hibrida (POST) — Semântica + Keywords",
            "embeddings_stats": "/embeddings/stats",
            "modulacoes": "/sumulas/com-modulacao",
            "setores": "/sumulas/por-setor",
            "alertas": "/alertas/compliance",
            "stats": "/estatisticas"
        },
        "autenticacao": "Passar ?api_key=sua_chave em todos os endpoints",
        "versao": "2.0.0 com RAG/Embeddings"
    }


# =====================================================================
# Main
# =====================================================================
if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("🚀 Fenice Brain — STF API")
    print("=" * 70)
    print()
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔌 API: http://localhost:8000")
    print()
    print("⚙️  Variáveis de ambiente:")
    print(f"  DB_HOST: {DB_HOST}")
    print(f"  DB_NAME: {DB_NAME}")
    print(f"  DB_USER: {DB_USER}")
    print(f"  API_KEY: {API_KEY}")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
