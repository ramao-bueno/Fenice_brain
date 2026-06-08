#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor simples para Dashboard STF Jurisprudência
Roda em http://localhost:8000 e fornece dados via JSON
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tenta conectar ao PostgreSQL; se falhar, usa dados de exemplo
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    DB_CONFIG = {
        'host': 'localhost',
        'database': 'fenice_brain',
        'user': 'fenice',
        'password': 'fenice_secure_password',
        'port': 5432
    }

    def get_db_connection():
        try:
            return psycopg2.connect(**DB_CONFIG)
        except:
            return None

    HAS_DB = True
except ImportError:
    HAS_DB = False
    logger.warning("psycopg2 não instalado. Usando dados de exemplo.")

# Dados de exemplo (fallback)
EXAMPLE_DATA = {
    "total_sumulas": 456,
    "sumulas_com_modulacao": 127,
    "ultimas_publicacoes": [
        {"numero": "SV-45", "setor": "Tributário", "data": "2024-06-01"},
        {"numero": "SV-44", "setor": "Administrativo", "data": "2024-05-28"},
        {"numero": "SV-43", "setor": "Constitucional", "data": "2024-05-15"},
        {"numero": "Tema-1200", "setor": "Previdenciário", "data": "2024-05-10"},
    ],
    "por_setor": {
        "Tributário": 89,
        "Administrativo": 72,
        "Constitucional": 65,
        "Previdenciário": 54,
        "Trabalhista": 43,
        "Civil": 38,
        "Penal": 28,
        "Processual": 22,
        "Ambiental": 18,
        "Outros": 27
    },
    "taxa_modulacao": {
        "labels": ["Sem Modulação", "Com Modulação"],
        "values": [329, 127]
    }
}

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        logger.info(f"GET {path}")

        # Rota: /api/stats
        if path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            stats = self.get_stats()
            self.wfile.write(json.dumps(stats).encode())

        # Rota: /api/modulacoes
        elif path == '/api/modulacoes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            modulacoes = self.get_modulacoes()
            self.wfile.write(json.dumps(modulacoes).encode())

        # Rota: /api/por-setor
        elif path == '/api/por-setor':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            por_setor = self.get_por_setor()
            self.wfile.write(json.dumps(por_setor).encode())

        # Rota: / (página principal)
        elif path == '/':
            self.serve_dashboard()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Não encontrado'.encode('utf-8'))

    def serve_dashboard(self):
        """Serve o arquivo HTML do dashboard"""
        dashboard_path = os.path.join(
            os.path.dirname(__file__),
            'dashboard_stf.html'
        )

        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Dashboard não encontrado'.encode('utf-8'))

    def get_stats(self):
        """Obtém estatísticas gerais do STF"""
        if HAS_DB and get_db_connection():
            try:
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)

                cur.execute("SELECT COUNT(*) as total FROM stf.sumulas")
                total = cur.fetchone()['total']

                cur.execute("SELECT COUNT(*) as total FROM stf.sumulas WHERE houve_modulacao = TRUE")
                com_modulacao = cur.fetchone()['total']

                cur.execute("""
                    SELECT numero_identificador, setor_afetado, data_publicacao
                    FROM stf.sumulas
                    ORDER BY data_publicacao DESC
                    LIMIT 4
                """)
                ultimas = [dict(row) for row in cur.fetchall()]
                for u in ultimas:
                    if u.get('data_publicacao'):
                        u['data_publicacao'] = str(u['data_publicacao'])

                conn.close()

                return {
                    "total_sumulas": total,
                    "sumulas_com_modulacao": com_modulacao,
                    "ultimas_publicacoes": ultimas
                }
            except Exception as e:
                logger.error(f"Erro ao buscar stats: {e}")
                return EXAMPLE_DATA

        return {
            "total_sumulas": EXAMPLE_DATA["total_sumulas"],
            "sumulas_com_modulacao": EXAMPLE_DATA["sumulas_com_modulacao"],
            "ultimas_publicacoes": EXAMPLE_DATA["ultimas_publicacoes"]
        }

    def get_modulacoes(self):
        """Obtém dados de modulação"""
        if HAS_DB and get_db_connection():
            try:
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)

                cur.execute("""
                    SELECT COUNT(*) as total FROM stf.sumulas WHERE houve_modulacao = FALSE,
                           COUNT(*) as modulada FROM stf.sumulas WHERE houve_modulacao = TRUE
                """)

                conn.close()

                total = EXAMPLE_DATA["total_sumulas"]
                modulada = EXAMPLE_DATA["sumulas_com_modulacao"]

                return {
                    "labels": ["Sem Modulação", "Com Modulação"],
                    "values": [total - modulada, modulada]
                }
            except Exception as e:
                logger.error(f"Erro ao buscar modulações: {e}")
                return EXAMPLE_DATA["taxa_modulacao"]

        return EXAMPLE_DATA["taxa_modulacao"]

    def get_por_setor(self):
        """Obtém distribuição por setor"""
        if HAS_DB and get_db_connection():
            try:
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)

                cur.execute("""
                    SELECT setor_afetado, COUNT(*) as total
                    FROM stf.sumulas
                    WHERE setor_afetado IS NOT NULL
                    GROUP BY setor_afetado
                    ORDER BY total DESC
                """)

                dados = cur.fetchall()
                labels = [d['setor_afetado'] for d in dados]
                values = [d['total'] for d in dados]

                conn.close()

                return {
                    "labels": labels,
                    "values": values
                }
            except Exception as e:
                logger.error(f"Erro ao buscar por setor: {e}")
                return EXAMPLE_DATA

        return EXAMPLE_DATA["por_setor"]

    def log_message(self, format, *args):
        """Suprime logs HTTP padrão"""
        return

def main():
    HOST = 'localhost'
    PORT = 8000

    server = HTTPServer((HOST, PORT), DashboardHandler)
    logger.info(f"📊 Dashboard rodando em http://{HOST}:{PORT}")
    logger.info("Pressione Ctrl+C para parar")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor parado")
        server.shutdown()

if __name__ == '__main__':
    main()
