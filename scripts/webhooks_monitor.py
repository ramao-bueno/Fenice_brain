#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Webhooks — Processa alertas pendentes e dispara notificações
Execute em background: nohup python webhooks_monitor.py > webhooks_monitor.log 2>&1 &
"""
import psycopg2
import psycopg2.extras
import json
import time
import argparse
import sys
import signal
from datetime import datetime
from typing import List, Dict, Any

from webhooks_notifier import WebhookNotifier, WebhookManager


class WebhookMonitor:
    """Monitor que processa alertas pendentes e dispara webhooks."""

    def __init__(
        self,
        db_host: str = 'localhost',
        db_name: str = 'fenice_brain',
        db_user: str = 'postgres',
        db_password: str = '',
        intervalo: int = 30
    ):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.intervalo = intervalo
        self.conn = None
        self.notifier = WebhookNotifier()
        self.running = True

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

    def buscar_alertas_pendentes(self) -> List[Dict[str, Any]]:
        """Busca alertas que ainda não foram disparados."""
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = """
            SELECT
                h.id,
                h.webhook_id,
                h.evento,
                h.numero_sumula,
                h.payload,
                w.url,
                w.tipo,
                w.api_key,
                w.headers
            FROM stf.webhook_history h
            JOIN stf.webhooks w ON h.webhook_id = w.id
            WHERE h.sucesso IS NULL
                AND h.acionado_em > NOW() - INTERVAL '1 day'
            ORDER BY h.acionado_em ASC
            LIMIT 100
            """

            cursor.execute(sql)
            return cursor.fetchall()

        except psycopg2.Error as e:
            print(f"❌ Erro ao buscar alertas: {e}")
            return []

    def disparar_webhook(self, alerta: Dict) -> bool:
        """Dispara um webhook e registra o resultado."""
        try:
            payload = json.loads(alerta['payload']) if isinstance(alerta['payload'], str) else alerta['payload']
            headers = json.loads(alerta['headers']) if alerta['headers'] else None

            # Disparar notificação
            tempo_inicio = time.time()
            sucesso, status, response = self.notifier.notificar(
                webhook_url=alerta['url'],
                webhook_tipo=alerta['tipo'],
                payload=payload,
                headers=headers,
                api_key=alerta['api_key']
            )
            tempo_ms = int((time.time() - tempo_inicio) * 1000)

            # Registrar resultado
            cursor = self.conn.cursor()
            cursor.execute("""
            UPDATE stf.webhook_history
            SET
                sucesso = %s,
                http_status = %s,
                response_body = %s,
                tempo_ms = %s
            WHERE id = %s
            """, (sucesso, status, response[:500], tempo_ms, alerta['id']))

            # Atualizar webhook com último status
            cursor.execute("""
            UPDATE stf.webhooks
            SET
                ultimo_acionamento = NOW(),
                total_acionamentos = total_acionamentos + 1,
                ultimo_status = %s
            WHERE id = %s
            """, (status, alerta['webhook_id']))

            self.conn.commit()

            resultado = "✅" if sucesso else "❌"
            print(f"{resultado} [{alerta['tipo']}] {alerta['numero_sumula']} "
                  f"→ {alerta['url'][:50]}... (HTTP {status}, {tempo_ms}ms)")

            return sucesso

        except Exception as e:
            print(f"❌ Erro ao disparar webhook {alerta['id']}: {e}")
            return False

    def processar_ciclo(self) -> int:
        """Processa um ciclo de alertas pendentes."""
        alertas = self.buscar_alertas_pendentes()

        if not alertas:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Nenhum alerta pendente")
            return 0

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📨 Processando {len(alertas)} alertas...")
        sucessos = 0

        for alerta in alertas:
            if self.disparar_webhook(alerta):
                sucessos += 1

        print(f"✅ {sucessos}/{len(alertas)} alertas disparados com sucesso\n")
        return sucessos

    def executar(self, max_ciclos: int = None):
        """Executa o monitor continuamente."""
        if not self.conectar():
            sys.exit(1)

        print("=" * 70)
        print("🚀 Monitor de Webhooks — Fenice Brain STF")
        print("=" * 70)
        print(f"Intervalo: {self.intervalo}s")
        print(f"Conectado: {self.db_name}@{self.db_host}")
        print()
        print("Sinais:")
        print("  Ctrl+C = Parar")
        print("=" * 70)
        print()

        # Registrar handler para Ctrl+C
        signal.signal(signal.SIGINT, self._handle_sigint)

        ciclo = 0
        while self.running:
            try:
                ciclo += 1
                self.processar_ciclo()

                if max_ciclos and ciclo >= max_ciclos:
                    print(f"\n✅ Atingido limite de {max_ciclos} ciclos")
                    break

                time.sleep(self.intervalo)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erro no ciclo: {e}")
                time.sleep(self.intervalo)

        self.fechar()

    def _handle_sigint(self, signum, frame):
        """Handler para Ctrl+C."""
        print("\n\n🛑 Parando monitor...")
        self.running = False

    def fechar(self):
        if self.conn:
            self.conn.close()
            print("✅ Conexão fechada")


def main():
    parser = argparse.ArgumentParser(
        description='Monitor de Webhooks — Dispara alertas STF'
    )
    parser.add_argument('--host', default='localhost', help='Host PostgreSQL')
    parser.add_argument('--database', default='fenice_brain', help='Nome do banco')
    parser.add_argument('--user', default='postgres', help='Usuário PostgreSQL')
    parser.add_argument('--password', default='', help='Senha PostgreSQL')
    parser.add_argument('--intervalo', type=int, default=30, help='Intervalo entre ciclos (segundos)')
    parser.add_argument('--ciclos', type=int, default=None, help='Número máximo de ciclos (None = infinito)')
    parser.add_argument('--uma-vez', action='store_true', help='Executar apenas uma vez')

    args = parser.parse_args()

    monitor = WebhookMonitor(
        db_host=args.host,
        db_name=args.database,
        db_user=args.user,
        db_password=args.password,
        intervalo=args.intervalo if not args.uma_vez else 0
    )

    if args.uma_vez:
        monitor.conectar()
        monitor.processar_ciclo()
        monitor.fechar()
    else:
        monitor.executar(max_ciclos=args.ciclos)


if __name__ == '__main__':
    main()
