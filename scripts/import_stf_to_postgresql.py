#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importar Súmulas STF (SV + RG) do JSON para PostgreSQL
Carrega schema_stf_postgresql.sql e insere dados do stf_sumulas_export.json
"""
import json
import psycopg2
import psycopg2.extras
from pathlib import Path
from datetime import datetime
import argparse
import sys

class STFImporter:
    def __init__(self, host='localhost', database='fenice_brain', user='postgres', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def conectar(self):
        """Conecta ao banco PostgreSQL."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(f"✅ Conectado a {self.database}@{self.host}")
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    def criar_schema(self, schema_file):
        """Executa o arquivo SQL para criar schema."""
        if not Path(schema_file).exists():
            print(f"❌ Arquivo não encontrado: {schema_file}")
            return False

        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            cursor = self.conn.cursor()
            cursor.execute(schema_sql)
            self.conn.commit()
            print(f"✅ Schema criado com sucesso")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"❌ Erro ao criar schema: {e}")
            return False

    def importar_sumulas(self, json_file):
        """Importa súmulas do JSON para o banco."""
        if not Path(json_file).exists():
            print(f"❌ Arquivo não encontrado: {json_file}")
            return 0

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            cursor = self.conn.cursor()
            total_importado = 0

            # Importa Súmulas Vinculantes
            for sv in data.get('sumulas_vinculantes', []):
                total_importado += self._inserir_sumula(cursor, sv)

            # Importa Temas RG
            for tema in data.get('temas_repercussao_geral', []):
                total_importado += self._inserir_sumula(cursor, tema)

            self.conn.commit()
            print(f"✅ {total_importado} súmulas importadas com sucesso")
            return total_importado

        except (json.JSONDecodeError, psycopg2.Error) as e:
            self.conn.rollback()
            print(f"❌ Erro ao importar: {e}")
            return 0

    def _inserir_sumula(self, cursor, sumula):
        """Insere uma súmula individual."""
        try:
            ident = sumula['identificacao']
            conteudo = sumula.get('conteudo_textual', {})
            ancoragem = sumula.get('ancoragem_legal', {})
            modulacao = sumula.get('modulacao_efeitos', {})
            impacto = sumula.get('impacto_business_compliance', {})
            metadata = sumula.get('metadata', {})

            # Extrai número numérico de numero_identificador
            num_str = ident.get('numero_identificador', '').split('_')[-1]
            numero_numerico = int(num_str) if num_str.isdigit() else None

            sql = """
            INSERT INTO stf.sumulas (
                tipo, numero_identificador, numero_numerico, processo_paradigma,
                data_publicacao, status, enunciado_original, nucleo_da_tese,
                artigos_cf88, leis_infraconstitucionais,
                houve_modulacao, regra_modulacao,
                setor_afetado, potencial_monetario, vulnerabilidade_compliance,
                keywords, analizado_em, confiabilidade, requer_revisao_manual
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (numero_identificador) DO UPDATE SET
                analizado_em = CURRENT_TIMESTAMP,
                confiabilidade = EXCLUDED.confiabilidade
            """

            cursor.execute(sql, (
                ident.get('tipo'),
                ident.get('numero_identificador'),
                numero_numerico,
                ident.get('processo_paradigma'),
                ident.get('data_publicacao_dje'),
                ident.get('status_atual', 'ATIVO'),
                conteudo.get('enunciado_original'),
                conteudo.get('nucleo_da_tese'),
                ancoragem.get('artigos_crfb88'),
                ancoragem.get('leis_infraconstitucionais_afetadas'),
                modulacao.get('houve_modulacao', False),
                modulacao.get('regra_da_modulacao'),
                impacto.get('setor_afetado'),
                impacto.get('potencial_monetario', 'LOW'),
                impacto.get('vulnerabilidade_compliance'),
                sumula.get('vetorizacao_keywords'),
                metadata.get('analisado_em'),
                metadata.get('confiabilidade', 0.8),
                metadata.get('requer_revisao_manual', False)
            ))

            return 1

        except psycopg2.Error as e:
            print(f"⚠️  Erro ao inserir {sumula.get('identificacao', {}).get('numero_identificador')}: {e}")
            return 0

    def listar_sumulas(self):
        """Lista contagem de súmulas por tipo."""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("""
            SELECT tipo, COUNT(*) as total, COUNT(CASE WHEN houve_modulacao THEN 1 END) as com_modulacao
            FROM stf.sumulas
            GROUP BY tipo
            """)

            print("\n📊 Estatísticas de Súmulas:")
            print("=" * 60)
            for row in cursor.fetchall():
                print(f"  {row['tipo']:30} | Total: {row['total']:3} | Com Modulação: {row['com_modulacao']}")

            # Súmulas com modulação
            cursor.execute("""
            SELECT numero_identificador, setor_afetado, regra_modulacao
            FROM stf.sumulas
            WHERE houve_modulacao = TRUE AND status = 'ATIVO'
            LIMIT 5
            """)

            print("\n⚠️  Súmulas com Modulação (Críticas - Top 5):")
            print("=" * 60)
            for row in cursor.fetchall():
                print(f"  {row['numero_identificador']} ({row['setor_afetado']})")
                print(f"    Regra: {row['regra_modulacao'][:80]}...")

        except psycopg2.Error as e:
            print(f"❌ Erro ao listar: {e}")

    def fechar(self):
        """Fecha conexão."""
        if self.conn:
            self.conn.close()
            print("✅ Conexão fechada")


def main():
    parser = argparse.ArgumentParser(description='Importar STF Sumulas para PostgreSQL')
    parser.add_argument('--host', default='localhost', help='Host PostgreSQL')
    parser.add_argument('--database', default='fenice_brain', help='Nome do banco')
    parser.add_argument('--user', default='postgres', help='Usuário PostgreSQL')
    parser.add_argument('--password', default='', help='Senha PostgreSQL')
    parser.add_argument('--schema-file', default='schema_stf_postgresql.sql', help='Arquivo schema SQL')
    parser.add_argument('--json-file', default='exports/stf_sumulas_export.json', help='Arquivo JSON')
    parser.add_argument('--skip-schema', action='store_true', help='Pular criação de schema')

    args = parser.parse_args()

    importer = STFImporter(
        host=args.host,
        database=args.database,
        user=args.user,
        password=args.password
    )

    # Conecta
    if not importer.conectar():
        sys.exit(1)

    try:
        # Cria schema (se necessário)
        if not args.skip_schema:
            if not importer.criar_schema(args.schema_file):
                sys.exit(1)

        # Importa dados
        total = importer.importar_sumulas(args.json_file)
        if total == 0:
            sys.exit(1)

        # Lista estatísticas
        importer.listar_sumulas()

        print("\n✅ Importação concluída com sucesso!")
        print("   Próximos passos:")
        print("   1. Rodar: SELECT * FROM stf.sumulas_com_modulacao;")
        print("   2. Rodar: SELECT * FROM stf.sumulas_por_setor;")
        print("   3. Testar busca: SELECT * FROM stf.buscar_por_keywords(ARRAY['administrativo', 'direito']);")

    finally:
        importer.fechar()


if __name__ == '__main__':
    main()
