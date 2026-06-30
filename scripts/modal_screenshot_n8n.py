#!/usr/bin/env python3
"""
Modal Screenshot & N8N Integration
Converte modal_preview.html em screenshot e envia via Evolution API

Uso:
  python modal_screenshot_n8n.py [numero] [--deploy]

Exemplos:
  python modal_screenshot_n8n.py 5521967531414
  python modal_screenshot_n8n.py 5521967531414 --deploy
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from typing import Optional

# Config
EVOLUTION_URL = "https://evolution-api-9fbw.srv1784289.hstgr.cloud"
EVOLUTION_API_KEY = "XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7"
EVOLUTION_INSTANCE = "fenice-tim-prod"

DEFAULT_NUMBER = "5547991041414"  # Corporativo — Principal
MODAL_FILE = Path(__file__).parent / "modal_preview.html"
SCREENSHOT_FILE = Path(__file__).parent / "modal_screenshot.png"

class ModalN8N:
    def __init__(self, numero: str = DEFAULT_NUMBER):
        self.numero = numero
        self.headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

    def send_text_message(self, text: str) -> bool:
        """Enviar mensagem de texto via Evolution API"""
        payload = {
            "number": self.numero,
            "text": text
        }

        try:
            resp = requests.post(
                f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}",
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if resp.status_code in [200, 201]:
                print(f"✅ Mensagem enviada: {self.numero}")
                return True
            else:
                print(f"❌ Erro {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False

    def send_image_message(self, image_path: Path, caption: str = "") -> bool:
        """Enviar imagem via Evolution API"""
        if not image_path.exists():
            print(f"❌ Arquivo não encontrado: {image_path}")
            return False

        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            base64_img = base64.b64encode(image_data).decode("utf-8")

            payload = {
                "number": self.numero,
                "mediaurl": f"data:image/png;base64,{base64_img}",
                "caption": caption or "Ver modal de atendimento"
            }

            resp = requests.post(
                f"{EVOLUTION_URL}/message/sendImage/{EVOLUTION_INSTANCE}",
                json=payload,
                headers=self.headers,
                timeout=15
            )

            if resp.status_code in [200, 201]:
                print(f"✅ Imagem enviada: {self.numero}")
                return True
            else:
                print(f"❌ Erro {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            print(f"❌ Erro ao enviar imagem: {e}")
            return False

    def send_modal_preview(self) -> bool:
        """Enviar preview do modal ao WhatsApp"""
        caption = (
            "👤 *Teo — Intelligence Concierge* 🤖\n\n"
            "Novo modal de atendimento da Fenice IT!\n\n"
            "Escolha uma opção:\n\n"
            "1️⃣ TIM Br.\n"
            "2️⃣ Estude Ciências Jurídicas\n"
            "3️⃣ Observatório da Mulher SFS\n"
            "👤 Interagir direto com especialista\n\n"
            "© 2026 Fenice IT · Justech.IA"
        )

        return self.send_image_message(SCREENSHOT_FILE, caption)

    def deploy_to_n8n(self) -> dict:
        """Gerar configuração N8N para integração"""
        config = {
            "node_name": "Modal Preview - Evolution API",
            "endpoint": f"/message/sendImage/{EVOLUTION_INSTANCE}",
            "method": "POST",
            "headers": self.headers,
            "payload": {
                "number": self.numero,
                "mediaurl": "{{ data:image/png;base64,<IMAGE_CONTENT> }}",
                "caption": (
                    "👤 *Teo — Intelligence Concierge* 🤖\n\n"
                    "Escolha como deseja prosseguir:\n\n"
                    "1️⃣ TIM Br.\n"
                    "2️⃣ Estude Ciências Jurídicas\n"
                    "3️⃣ Observatório da Mulher SFS\n"
                    "👤 Interagir direto com especialista\n\n"
                    "© 2026 Fenice IT · Justech.IA"
                )
            }
        }
        return config


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Modal Screenshot & N8N Integration")
    parser.add_argument("numero", nargs="?", default=DEFAULT_NUMBER, help=f"Número WhatsApp (default: {DEFAULT_NUMBER})")
    parser.add_argument("--deploy", action="store_true", help="Gerar config para N8N deploy")
    parser.add_argument("--test", action="store_true", help="Enviar mensagem de teste antes")

    args = parser.parse_args()

    print("🎯 Fenice IT — Modal N8N Integration")
    print("=" * 50)
    print()

    # Validar
    if not MODAL_FILE.exists():
        print(f"❌ Modal não encontrado: {MODAL_FILE}")
        sys.exit(1)

    # Init
    modal = ModalN8N(args.numero)

    # Teste
    if args.test:
        print("📨 Enviando mensagem de teste...")
        test_msg = (
            "🔔 *Teste N8N — Modal Preview*\n\n"
            "Sistema de integração ativo!\n\n"
            "© 2026 Fenice IT · Justech.IA"
        )
        modal.send_text_message(test_msg)
        print()

    # Deploy
    if args.deploy:
        print("📋 Configuração N8N:")
        print()
        config = modal.deploy_to_n8n()
        print(json.dumps(config, indent=2, ensure_ascii=False))
        print()
        print("📌 Use esta configuração no workflow:")
        print("   https://feniceit.app.n8n.cloud")
        print()

    # Enviar modal
    print(f"📱 Enviando modal para: {args.numero}")
    print(f"🔌 Instância: {EVOLUTION_INSTANCE}")
    print()

    if SCREENSHOT_FILE.exists():
        modal.send_modal_preview()
    else:
        print(f"⚠️  Screenshot não encontrado: {SCREENSHOT_FILE}")
        print("   Use Playwright para gerar screenshot antes:")
        print("   python modal_screenshot_n8n.py --screenshot")

        # Fallback: enviar mensagem com link
        fallback_msg = (
            "👤 *Teo — Intelligence Concierge* 🤖\n\n"
            "Novo modal interativo! Visualize aqui:\n"
            "https://fenice.ia.br/modal/preview\n\n"
            "© 2026 Fenice IT · Justech.IA"
        )
        modal.send_text_message(fallback_msg)

    print()
    print("✨ Integração concluída!")


if __name__ == "__main__":
    main()
