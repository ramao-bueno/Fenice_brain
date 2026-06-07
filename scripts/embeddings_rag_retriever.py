#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Retriever — Busca Semântica com Embeddings
Integra-se com PostgreSQL + pgvector + OpenAI
"""
import os
import psycopg2
import psycopg2.extras
from typing import List, Optional
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:
    print("❌ OpenAI library não instalada. Execute: pip install openai")
    raise


@dataclass
class SumulaResult:
    numero_identificador: str
    tipo: str
    setor_afetado: Optional[str]
    similarity_score: float
    enunciado_original: Optional[str]
    match_type: str = "SEMANTIC"


class RAGRetriever:
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        db_host: str = 'localhost',
        db_name: str = 'fenice_brain',
        db_user: str = 'postgres',
        db_password: str = ''
    ):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada")

        self.client = OpenAI(api_key=self.openai_api_key)
        self.model = "text-embedding-3-small"

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.conn = None

    def conectar(self) -> bool:
        try:
            self.conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    def gerar_query_embedding(self, query_text: str) -> Optional[List[float]]:
        """Gera embedding para a query de busca."""
        try:
            if len(query_text) > 25000:
                query_text = query_text[:25000]

            response = self.client.embeddings.create(
                input=query_text,
                model=self.model
            )
            return response.data[0].embedding

        except Exception as e:
            print(f"❌ Erro ao gerar embedding da query: {e}")
            return None

    def buscar_semanticamente(
        self,
        query_text: str,
        limite: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[SumulaResult]:
        """Busca semântica usando embeddings."""
        if not self.conn:
            print("❌ Não conectado ao banco de dados")
            return []

        # Gerar embedding da query
        query_embedding = self.gerar_query_embedding(query_text)
        if not query_embedding:
            return []

        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Busca por similaridade (cosine distance)
            # Nota: pgvector usa <-> para cosine distance
            sql = """
            SELECT
                numero_identificador,
                tipo,
                setor_afetado,
                (1 - (embedding <-> %s)) as similarity_score,
                enunciado_original
            FROM stf.sumulas
            WHERE embedding IS NOT NULL
                AND status = 'ATIVO'
                AND (1 - (embedding <-> %s)) >= %s
            ORDER BY embedding <-> %s
            LIMIT %s
            """

            cursor.execute(sql, [
                query_embedding,
                query_embedding,
                similarity_threshold,
                query_embedding,
                limite
            ])

            resultados = []
            for row in cursor.fetchall():
                resultados.append(SumulaResult(
                    numero_identificador=row['numero_identificador'],
                    tipo=row['tipo'],
                    setor_afetado=row['setor_afetado'],
                    similarity_score=row['similarity_score'],
                    enunciado_original=row['enunciado_original'],
                    match_type='SEMANTIC'
                ))

            return resultados

        except psycopg2.Error as e:
            print(f"❌ Erro na busca semântica: {e}")
            return []

    def buscar_hibrida(
        self,
        query_text: str,
        keywords: Optional[List[str]] = None,
        limite: int = 10,
        alpha: float = 0.5
    ) -> List[SumulaResult]:
        """Busca híbrida combinando semântica + keywords."""
        if not self.conn:
            print("❌ Não conectado ao banco de dados")
            return []

        resultados = []

        # 1. Busca semântica (alpha % do peso)
        semanticos = self.buscar_semanticamente(
            query_text,
            limite=limite,
            similarity_threshold=0.5
        )

        # 2. Busca por keywords (se fornecidas)
        if keywords:
            palavras_chave = [kw.lower() for kw in keywords]
            resultados_keywords = self.buscar_por_keywords(
                palavras_chave,
                limite=limite
            )

            # Combinar com pesos
            # Semântica: alpha, Keywords: (1-alpha)
            for r in semanticos:
                r.similarity_score = r.similarity_score * alpha
            for r in resultados_keywords:
                r.similarity_score = r.similarity_score * (1 - alpha)

            # Deduplica por numero_identificador e combina scores
            mapa = {}
            for r in semanticos + resultados_keywords:
                if r.numero_identificador not in mapa:
                    mapa[r.numero_identificador] = r
                else:
                    mapa[r.numero_identificador].similarity_score += r.similarity_score

            resultados = list(mapa.values())
            resultados.sort(key=lambda x: x.similarity_score, reverse=True)
            resultados = resultados[:limite]
        else:
            resultados = semanticos

        return resultados

    def buscar_por_keywords(
        self,
        keywords: List[str],
        limite: int = 10
    ) -> List[SumulaResult]:
        """Busca por palavras-chave (fallback para busca semântica)."""
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = """
            SELECT
                numero_identificador,
                tipo,
                setor_afetado,
                CAST(COUNT(*) AS FLOAT) / %s as similarity_score,
                enunciado_original
            FROM stf.sumulas
            WHERE keywords && %s AND status = 'ATIVO'
            GROUP BY id, numero_identificador, tipo, setor_afetado, enunciado_original
            ORDER BY similarity_score DESC
            LIMIT %s
            """

            cursor.execute(sql, [
                len(keywords),
                keywords,
                limite
            ])

            resultados = []
            for row in cursor.fetchall():
                resultados.append(SumulaResult(
                    numero_identificador=row['numero_identificador'],
                    tipo=row['tipo'],
                    setor_afetado=row['setor_afetado'],
                    similarity_score=row['similarity_score'],
                    enunciado_original=row['enunciado_original'],
                    match_type='KEYWORD'
                ))

            return resultados

        except psycopg2.Error as e:
            print(f"❌ Erro na busca por keywords: {e}")
            return []

    def gerar_contexto_rag(
        self,
        query_text: str,
        num_referencias: int = 3
    ) -> str:
        """Gera contexto para prompt RAG (para LLM)."""
        resultados = self.buscar_semanticamente(
            query_text,
            limite=num_referencias
        )

        if not resultados:
            return "Nenhuma súmula relevante encontrada."

        contexto = "# Contexto Relevante\n\n"
        for i, resultado in enumerate(resultados, 1):
            contexto += f"## {i}. {resultado.numero_identificador}\n"
            contexto += f"**Tipo:** {resultado.tipo}\n"
            contexto += f"**Setor:** {resultado.setor_afetado}\n"
            contexto += f"**Relevância:** {resultado.similarity_score:.2%}\n\n"
            contexto += f"{resultado.enunciado_original}\n\n"
            contexto += "---\n\n"

        return contexto

    def contar_embeddings(self) -> dict:
        """Retorna estatísticas de embeddings."""
        if not self.conn:
            return {}

        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM stf.embedding_stats")
            stats = cursor.fetchone()
            return dict(stats) if stats else {}
        except psycopg2.Error as e:
            print(f"❌ Erro ao contar embeddings: {e}")
            return {}

    def fechar(self):
        if self.conn:
            self.conn.close()


# Exemplo de uso
if __name__ == '__main__':
    retriever = RAGRetriever()

    if not retriever.conectar():
        exit(1)

    print("🚀 RAG Retriever — Busca Semântica")
    print("=" * 70)
    print()

    # Exemplo 1: Busca semântica
    query = "direito de greve dos servidores públicos"
    print(f"📌 Buscando: '{query}'")
    resultados = retriever.buscar_semanticamente(query, limite=3)

    if resultados:
        print(f"\n✅ {len(resultados)} resultados encontrados:\n")
        for r in resultados:
            print(f"  • {r.numero_identificador} ({r.tipo})")
            print(f"    Relevância: {r.similarity_score:.2%}")
            print(f"    Setor: {r.setor_afetado}")
            print()
    else:
        print("❌ Nenhum resultado encontrado.\n")

    # Exemplo 2: Contexto RAG
    print("\n" + "=" * 70)
    print("📚 Contexto RAG gerado:")
    print("=" * 70)
    print()
    contexto = retriever.gerar_contexto_rag(query, num_referencias=2)
    print(contexto)

    # Estatísticas
    stats = retriever.contar_embeddings()
    if stats:
        print("\n" + "=" * 70)
        print("📊 Estatísticas de Embeddings")
        print("=" * 70)
        print(f"Total de súmulas: {stats.get('total_sumulas')}")
        print(f"Com embedding: {stats.get('com_embedding')} ({stats.get('percentual_com_embedding')}%)")
        print(f"Sem embedding: {stats.get('sem_embedding')}")

    retriever.fechar()
