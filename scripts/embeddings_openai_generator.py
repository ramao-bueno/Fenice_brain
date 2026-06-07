#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerar embeddings das Súmulas STF usando OpenAI API
Armazena embeddings em PostgreSQL (pgvector)
"""
import json
import os
import time
import psycopg2
import psycopg2.extras
from pathlib import Path
from typing import List, Optional
import argparse
import sys

try:
    from openai import OpenAI
except ImportError:
    print("❌ OpenAI library não instalada. Execute: pip install openai")
    sys.exit(1)

class EmbeddingsGenerator:
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
            raise ValueError("OPENAI_API_KEY não configurada. Use --api-key ou $OPENAI_API_KEY")

        self.client = OpenAI(api_key=self.openai_api_key)
        self.model = "text-embedding-3-small"  # Mais barato e rápido
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
            print(f"✅ Conectado a {self.db_name}@{self.db_host}")
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    def criar_extensao_pgvector(self) -> bool:
        """Ativa extensão pgvector no PostgreSQL."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.conn.commit()
            print("✅ Extensão pgvector criada/ativada")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"⚠️  pgvector já existe ou erro: {e}")
            return True  # Continua mesmo se já existe

    def adicionar_coluna_embedding(self) -> bool:
        """Adiciona coluna de embedding à tabela sumulas."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            ALTER TABLE stf.sumulas
            ADD COLUMN IF NOT EXISTS embedding vector(1536);
            """)
            self.conn.commit()
            print("✅ Coluna embedding adicionada")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"⚠️  Coluna embedding já existe: {e}")
            return True

    def criar_indice_embedding(self) -> bool:
        """Cria índice IVFFLAT para busca eficiente."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sumulas_embedding ON stf.sumulas
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
            """)
            self.conn.commit()
            print("✅ Índice IVFFLAT criado")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"⚠️  Índice já existe: {e}")
            return True

    def gerar_embedding(self, texto: str) -> Optional[List[float]]:
        """Gera embedding para um texto usando OpenAI."""
        try:
            # Limitar tamanho do texto (max 8191 tokens)
            if len(texto) > 25000:
                texto = texto[:25000]

            response = self.client.embeddings.create(
                input=texto,
                model=self.model
            )
            return response.data[0].embedding

        except Exception as e:
            print(f"❌ Erro ao gerar embedding: {e}")
            return None

    def processar_sumulas(
        self,
        batch_size: int = 10,
        delay: float = 0.5,
        force_regenerate: bool = False
    ) -> int:
        """Processa todas as súmulas e gera embeddings."""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Buscar súmulas sem embedding (ou todas se force_regenerate)
            if force_regenerate:
                sql = "SELECT id, numero_identificador, enunciado_original, nucleo_da_tese FROM stf.sumulas ORDER BY id"
            else:
                sql = "SELECT id, numero_identificador, enunciado_original, nucleo_da_tese FROM stf.sumulas WHERE embedding IS NULL ORDER BY id"

            cursor.execute(sql)
            sumulas = cursor.fetchall()
            total = len(sumulas)

            if total == 0:
                print("✅ Todas as súmulas já possuem embeddings!")
                return 0

            print(f"\n📊 Processando {total} súmulas...")
            print("=" * 70)

            processadas = 0
            erros = 0

            for i, sumula in enumerate(sumulas, 1):
                id_sumula = sumula['id']
                numero = sumula['numero_identificador']
                texto = sumula['enunciado_original'] or sumula['nucleo_da_tese'] or numero

                # Gerar embedding
                embedding = self.gerar_embedding(texto)

                if not embedding:
                    erros += 1
                    print(f"❌ [{i}/{total}] {numero} — Erro ao gerar embedding")
                    continue

                # Salvar embedding no banco
                try:
                    update_cursor = self.conn.cursor()
                    update_cursor.execute(
                        "UPDATE stf.sumulas SET embedding = %s WHERE id = %s",
                        (embedding, id_sumula)
                    )
                    self.conn.commit()
                    processadas += 1

                    if i % batch_size == 0 or i == total:
                        pct = (i / total) * 100
                        print(f"✅ [{i}/{total}] ({pct:.1f}%) {numero} — Embedding salvo")

                except psycopg2.Error as e:
                    erros += 1
                    print(f"❌ [{i}/{total}] {numero} — Erro ao salvar: {e}")
                    self.conn.rollback()

                # Rate limiting (OpenAI permite ~60 reqs/min para text-embedding-3-small)
                if i < total:
                    time.sleep(delay)

            print("\n" + "=" * 70)
            print(f"📈 Resultado:")
            print(f"  ✅ Processadas: {processadas}")
            print(f"  ❌ Erros: {erros}")
            print(f"  📊 Taxa de sucesso: {(processadas/total)*100:.1f}%")

            return processadas

        except Exception as e:
            print(f"❌ Erro ao processar súmulas: {e}")
            return 0

    def contar_embeddings(self) -> int:
        """Conta quantas súmulas têm embeddings."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stf.sumulas WHERE embedding IS NOT NULL")
            count = cursor.fetchone()[0]
            return count
        except psycopg2.Error as e:
            print(f"❌ Erro ao contar: {e}")
            return 0

    def fechar(self):
        if self.conn:
            self.conn.close()
            print("✅ Conexão fechada")


def main():
    parser = argparse.ArgumentParser(
        description='Gerar embeddings das Súmulas STF com OpenAI'
    )
    parser.add_argument('--api-key', help='OpenAI API Key (ou $OPENAI_API_KEY)')
    parser.add_argument('--host', default='localhost', help='Host PostgreSQL')
    parser.add_argument('--database', default='fenice_brain', help='Nome do banco')
    parser.add_argument('--user', default='postgres', help='Usuário PostgreSQL')
    parser.add_argument('--password', default='', help='Senha PostgreSQL')
    parser.add_argument('--batch-size', type=int, default=10, help='Tamanho do lote')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay entre requisições (segundos)')
    parser.add_argument('--force', action='store_true', help='Regenerar todos os embeddings')

    args = parser.parse_args()

    print("=" * 70)
    print("🚀 Gerador de Embeddings — Fenice Brain STF")
    print("=" * 70)
    print()

    generator = EmbeddingsGenerator(
        openai_api_key=args.api_key,
        db_host=args.host,
        db_name=args.database,
        db_user=args.user,
        db_password=args.password
    )

    try:
        # Conectar
        if not generator.conectar():
            sys.exit(1)

        # Setup pgvector
        generator.criar_extensao_pgvector()
        generator.adicionar_coluna_embedding()
        generator.criar_indice_embedding()

        # Processar
        print()
        processadas = generator.processar_sumulas(
            batch_size=args.batch_size,
            delay=args.delay,
            force_regenerate=args.force
        )

        # Estatísticas
        total_com_embedding = generator.contar_embeddings()
        print(f"\n📊 Total com embedding: {total_com_embedding}")
        print("\n✅ Embeddings gerados com sucesso!")
        print("\n   Próximos passos:")
        print("   1. Testar busca semântica:")
        print("      SELECT stf.buscar_semanticamente('direito administrativo', 5);")
        print("   2. Usar endpoint da API:")
        print("      POST /sumulas/buscar-semantica?api_key=sua_chave")

    finally:
        generator.fechar()


if __name__ == '__main__':
    main()
