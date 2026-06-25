#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notifier — Enviar alertas via Discord, Slack, Email, Custom Webhooks
"""
import json
import time
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@dataclass
class WebhookPayload:
    evento: str
    numero_identificador: str
    tipo: str
    setor_afetado: Optional[str]
    regra_modulacao: Optional[str]
    potencial_monetario: Optional[str]
    vulnerabilidade_compliance: Optional[str]
    data_detectada: str


class WebhookNotifier:
    """Envia notificações via webhooks para múltiplos canais."""

    def __init__(self):
        self.timeout = 10
        self.max_retries = 3

    def notificar(
        self,
        webhook_url: str,
        webhook_tipo: str,
        payload: Dict[str, Any],
        headers: Optional[Dict] = None,
        api_key: Optional[str] = None
    ) -> tuple[bool, int, str]:
        """Envia notificação para o webhook com retry. Retorna: (sucesso, http_status, response_text)."""
        ultimo_status = 500
        ultimo_msg = "Falha desconhecida"

        for tentativa in range(1, self.max_retries + 1):
            try:
                if webhook_tipo == "DISCORD":
                    sucesso, status, msg = self._notificar_discord(webhook_url, payload)
                elif webhook_tipo == "SLACK":
                    sucesso, status, msg = self._notificar_slack(webhook_url, payload)
                elif webhook_tipo == "EMAIL":
                    sucesso, status, msg = self._notificar_email(payload)
                elif webhook_tipo == "CUSTOM":
                    sucesso, status, msg = self._notificar_custom(webhook_url, payload, headers, api_key)
                else:
                    return False, 400, f"Tipo de webhook desconhecido: {webhook_tipo}"

                if sucesso:
                    return sucesso, status, msg

                ultimo_status, ultimo_msg = status, msg
                if tentativa < self.max_retries:
                    time.sleep(2 ** tentativa)  # backoff: 2s, 4s

            except Exception as e:
                ultimo_status, ultimo_msg = 500, str(e)
                if tentativa < self.max_retries:
                    time.sleep(2 ** tentativa)

        return False, ultimo_status, ultimo_msg

    def _notificar_discord(self, webhook_url: str, payload: Dict) -> tuple[bool, int, str]:
        """Envia notificação para Discord."""
        try:
            # Formatar como embed Discord
            cor_urgencia = self._cor_urgencia(payload)
            embed = {
                "title": f"🚨 {payload['evento']}",
                "description": f"**{payload['numero_identificador']}** ({payload['tipo']})",
                "color": cor_urgencia,
                "fields": [
                    {
                        "name": "Setor Afetado",
                        "value": payload.get('setor_afetado', 'N/A'),
                        "inline": True
                    },
                    {
                        "name": "Potencial Monetário",
                        "value": payload.get('potencial_monetario', 'LOW'),
                        "inline": True
                    },
                    {
                        "name": "Regra de Modulação",
                        "value": payload.get('regra_modulacao', 'N/A')[:200],
                        "inline": False
                    },
                    {
                        "name": "Vulnerabilidade Compliance",
                        "value": payload.get('vulnerabilidade_compliance', 'N/A')[:200],
                        "inline": False
                    }
                ],
                "timestamp": payload['data_detectada'],
                "footer": {
                    "text": "Fenice Brain — STF Alertas"
                }
            }

            data = {"embeds": [embed]}

            response = requests.post(
                webhook_url,
                json=data,
                timeout=self.timeout
            )

            sucesso = response.status_code in [200, 204]
            return sucesso, response.status_code, response.text or "OK"

        except Exception as e:
            return False, 500, str(e)

    def _notificar_slack(self, webhook_url: str, payload: Dict) -> tuple[bool, int, str]:
        """Envia notificação para Slack."""
        try:
            # Formatar como message Slack
            cor_urgencia = self._cor_urgencia_slack(payload)
            blocks = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 {payload['evento']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Número:*\n{payload['numero_identificador']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Tipo:*\n{payload['tipo']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Setor:*\n{payload.get('setor_afetado', 'N/A')}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Monetário:*\n{payload.get('potencial_monetario', 'LOW')}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Regra:*\n{payload.get('regra_modulacao', 'N/A')[:200]}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"Detectada em {payload['data_detectada']}"
                            }
                        ]
                    }
                ]
            }

            response = requests.post(
                webhook_url,
                json=blocks,
                timeout=self.timeout
            )

            sucesso = response.status_code == 200
            return sucesso, response.status_code, response.text or "OK"

        except Exception as e:
            return False, 500, str(e)

    def _notificar_email(self, payload: Dict) -> tuple[bool, int, str]:
        """Envia notificação por Email (simulado)."""
        # Para uso real, configure SMTP
        assunto = f"[ALERTA] {payload['numero_identificador']} — {payload['evento']}"
        corpo = f"""
        <html>
            <body>
                <h2>{payload['evento']}</h2>
                <p><strong>Súmula:</strong> {payload['numero_identificador']}</p>
                <p><strong>Tipo:</strong> {payload['tipo']}</p>
                <p><strong>Setor:</strong> {payload.get('setor_afetado', 'N/A')}</p>
                <p><strong>Potencial Monetário:</strong> {payload.get('potencial_monetario', 'LOW')}</p>
                <hr/>
                <p><strong>Regra de Modulação:</strong></p>
                <p>{payload.get('regra_modulacao', 'N/A')}</p>
                <hr/>
                <p><strong>Vulnerabilidade Compliance:</strong></p>
                <p>{payload.get('vulnerabilidade_compliance', 'N/A')}</p>
                <hr/>
                <small>Enviado em {payload['data_detectada']}</small>
            </body>
        </html>
        """

        # TODO: Implementar SMTP real
        return True, 200, "Email enviado (simulado)"

    def _notificar_custom(
        self,
        webhook_url: str,
        payload: Dict,
        headers: Optional[Dict] = None,
        api_key: Optional[str] = None
    ) -> tuple[bool, int, str]:
        """Envia para webhook customizado."""
        try:
            custom_headers = headers or {}
            if api_key:
                custom_headers['Authorization'] = f'Bearer {api_key}'

            response = requests.post(
                webhook_url,
                json=payload,
                headers=custom_headers,
                timeout=self.timeout
            )

            sucesso = response.status_code in [200, 201, 202, 204]
            return sucesso, response.status_code, response.text or "OK"

        except Exception as e:
            return False, 500, str(e)

    def _cor_urgencia(self, payload: Dict) -> int:
        """Retorna cor Discord baseada em urgência."""
        monetario = payload.get('potencial_monetario', 'LOW')
        if monetario == 'HIGH':
            return 0xFF0000  # Vermelho
        elif monetario == 'MEDIUM':
            return 0xFFA500  # Laranja
        else:
            return 0xFFFF00  # Amarelo

    def _cor_urgencia_slack(self, payload: Dict) -> str:
        """Retorna cor Slack baseada em urgência."""
        monetario = payload.get('potencial_monetario', 'LOW')
        if monetario == 'HIGH':
            return 'danger'
        elif monetario == 'MEDIUM':
            return 'warning'
        else:
            return 'good'


class WebhookManager:
    """Gerencia webhooks no banco de dados."""

    def __init__(self, db_host='localhost', db_name='fenice_brain', db_user='postgres', db_password=''):
        import psycopg2

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.conn = None
        self.psycopg2 = psycopg2

    def conectar(self) -> bool:
        try:
            self.conn = self.psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    def criar_webhook(
        self,
        nome: str,
        url: str,
        tipo: str,
        eventos: list,
        filtro_setor: Optional[str] = None,
        filtro_tipo: Optional[str] = None,
        api_key: Optional[str] = None,
        headers: Optional[Dict] = None
    ) -> bool:
        """Registra novo webhook."""
        try:
            cursor = self.conn.cursor()

            cursor.execute("""
            INSERT INTO stf.webhooks (nome, url, tipo, eventos, filtro_setor, filtro_tipo, api_key, headers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nome,
                url,
                tipo,
                eventos,
                filtro_setor,
                filtro_tipo,
                api_key,
                json.dumps(headers) if headers else None
            ))

            self.conn.commit()
            print(f"✅ Webhook '{nome}' criado")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"❌ Erro ao criar webhook: {e}")
            return False

    def listar_webhooks(self) -> list:
        """Lista todos os webhooks."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM stf.listar_webhooks_com_stats()")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao listar: {e}")
            return []

    def deletar_webhook(self, webhook_id: int) -> bool:
        """Remove webhook."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM stf.webhooks WHERE id = %s", (webhook_id,))
            self.conn.commit()
            print(f"✅ Webhook {webhook_id} deletado")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Erro ao deletar: {e}")
            return False

    def ativar_webhook(self, webhook_id: int) -> bool:
        """Ativa webhook."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE stf.webhooks SET ativo = TRUE WHERE id = %s", (webhook_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def desativar_webhook(self, webhook_id: int) -> bool:
        """Desativa webhook."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE stf.webhooks SET ativo = FALSE WHERE id = %s", (webhook_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def fechar(self):
        if self.conn:
            self.conn.close()


# Exemplo de uso
if __name__ == '__main__':
    notifier = WebhookNotifier()

    # Payload de exemplo
    payload = {
        'evento': 'MODULACAO_DETECTADA',
        'numero_identificador': 'STF_SV_57',
        'tipo': 'SUMULA_VINCULANTE',
        'setor_afetado': 'ADMINISTRATIVO',
        'regra_modulacao': 'Efeitos a partir de 15/03/2017',
        'potencial_monetario': 'HIGH',
        'vulnerabilidade_compliance': 'Requer revisão imediata',
        'data_detectada': '2026-06-07T20:45:00'
    }

    # Testar Discord (substituir URL real)
    print("📨 Testando Discord...")
    sucesso, status, msg = notifier.notificar(
        "https://discord.com/api/webhooks/seu_webhook_discord_aqui",
        "DISCORD",
        payload
    )
    print(f"Status: {status}, Sucesso: {sucesso}")

    # Testar Slack
    print("\n📨 Testando Slack...")
    sucesso, status, msg = notifier.notificar(
        "https://hooks.slack.com/services/seu_webhook_slack_aqui",
        "SLACK",
        payload
    )
    print(f"Status: {status}, Sucesso: {sucesso}")

    # Testar Custom
    print("\n📨 Testando Custom...")
    sucesso, status, msg = notifier.notificar(
        "https://seu-api.com/webhooks/stf",
        "CUSTOM",
        payload,
        api_key="sua-api-key"
    )
    print(f"Status: {status}, Sucesso: {sucesso}")
