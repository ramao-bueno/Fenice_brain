#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de webhook AvisaAPI para testar o workflow N8N da Fenice.

Uso:
    python test_avisa_n8n.py
    python test_avisa_n8n.py --url https://seu-n8n/webhook/avisa-whatsapp
    python test_avisa_n8n.py --mensagem "Tenho dúvidas sobre rescisão de contrato"
    python test_avisa_n8n.py --suite  # roda todos os casos de teste
"""
import json
import sys
import time
import argparse
import requests
from datetime import datetime
from pathlib import Path

# Carregar .env
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / '.env')
except ImportError:
    pass

import os

# Cor terminal
RED   = "\033[91m"
GREEN = "\033[92m"
YELL  = "\033[93m"
BLUE  = "\033[94m"
RESET = "\033[0m"

NUMERO_TESTE = os.getenv("AVISA_WHATSAPP_NUMBER", "5521976531414")

CASOS_TESTE = [
    {
        "nome": "Consulta trabalhista",
        "mensagem": "Fui demitido sem justa causa e não recebi o FGTS. O que posso fazer?"
    },
    {
        "nome": "Consulta contratual",
        "mensagem": "Preciso de um contrato de prestação de serviços de TI"
    },
    {
        "nome": "Pergunta geral",
        "mensagem": "Qual é o prazo para entrar com recurso em processo administrativo?"
    },
    {
        "nome": "Mensagem vazia (deve ignorar)",
        "mensagem": ""
    },
]


def simular_webhook(n8n_url: str, numero: str, mensagem: str, nome: str = "Teste Fenice") -> dict:
    """Envia payload simulado de webhook AvisaAPI para o N8N."""
    ts = datetime.now()
    payload = {
        # Campos testados em múltiplos formatos — o Code node aceita todos
        "number":    numero,
        "from":      numero,
        "name":      nome,
        "pushName":  nome,
        "message":   mensagem,
        "text":      mensagem,
        "body":      mensagem,
        "session":   f"session-test-{ts.strftime('%Y%m%d%H%M%S')}",
        "id":        f"msg-test-{int(ts.timestamp())}",
        "chatId":    f"{numero}@s.whatsapp.net",
        "timestamp": ts.isoformat(),
        "type":      "text"
    }

    print(f"\n{BLUE}▶ Enviando para {n8n_url}{RESET}")
    print(f"  Número : {numero}")
    print(f"  Mensagem: {mensagem or '(vazia)'}")

    try:
        inicio = time.time()
        response = requests.post(
            n8n_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed = (time.time() - inicio) * 1000

        cor = GREEN if response.status_code in (200, 201, 202) else RED
        print(f"  {cor}HTTP {response.status_code}{RESET}  ({elapsed:.0f} ms)")

        try:
            body = response.json()
            print(f"  Resposta: {json.dumps(body, ensure_ascii=False)}")
        except Exception:
            print(f"  Resposta: {response.text[:200]}")

        return {"ok": response.status_code < 300, "status": response.status_code, "elapsed_ms": elapsed}

    except requests.exceptions.ConnectionError:
        print(f"  {RED}❌ Sem conexão com {n8n_url}{RESET}")
        print(f"     Verifique se o N8N está rodando e o workflow está ATIVO.")
        return {"ok": False, "status": 0, "error": "connection_refused"}

    except requests.exceptions.Timeout:
        print(f"  {RED}❌ Timeout (>30s){RESET}")
        return {"ok": False, "status": 0, "error": "timeout"}

    except Exception as e:
        print(f"  {RED}❌ Erro: {e}{RESET}")
        return {"ok": False, "status": 0, "error": str(e)}


def verificar_avisa_api() -> bool:
    """Verifica se o token AvisaAPI está configurado e o endpoint responde."""
    token = os.getenv("AVISA_API_TOKEN", "")
    url   = os.getenv("AVISA_SEND_URL", "https://www.avisaapi.com.br/api/actions/sendMessage")

    print(f"\n{BLUE}=== Verificação AvisaAPI ==={RESET}")
    print(f"  Token : {'configurado ✓' if token else 'NÃO configurado ✗'}")
    print(f"  URL   : {url}")

    if not token:
        print(f"  {YELL}Configure AVISA_API_TOKEN no .env{RESET}")
        return False

    # Chamada real — enviará mensagem de teste para o número da conta
    print(f"\n  {YELL}Enviando mensagem de verificação para {NUMERO_TESTE}...{RESET}")
    try:
        resp = requests.post(
            url,
            json={"number": NUMERO_TESTE, "message": "🤖 Fenice N8N — verificação de integração OK"},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=15
        )
        cor = GREEN if resp.status_code < 300 else RED
        print(f"  {cor}HTTP {resp.status_code}{RESET}")
        print(f"  Resposta: {resp.text[:300]}")
        return resp.status_code < 300
    except Exception as e:
        print(f"  {RED}Erro: {e}{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Teste do workflow AvisaAPI → N8N → Fenice")
    parser.add_argument("--url", default=os.getenv("N8N_WEBHOOK_URL", ""), help="URL webhook N8N")
    parser.add_argument("--numero", default=NUMERO_TESTE, help="Número WhatsApp (formato 55DDD...)")
    parser.add_argument("--mensagem", default="", help="Mensagem de teste personalizada")
    parser.add_argument("--nome", default="Teste Fenice", help="Nome do remetente simulado")
    parser.add_argument("--suite", action="store_true", help="Executar todos os casos de teste")
    parser.add_argument("--verificar-avisa", action="store_true", help="Verificar token e envio AvisaAPI direto")
    args = parser.parse_args()

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  Fenice — Teste AvisaAPI + N8N Workflow{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    if args.verificar_avisa:
        ok = verificar_avisa_api()
        sys.exit(0 if ok else 1)

    n8n_url = args.url
    if not n8n_url or "SEU-N8N-HOST" in n8n_url:
        print(f"\n{RED}❌ URL do N8N não configurada.{RESET}")
        print("   Use: python test_avisa_n8n.py --url https://seu-n8n/webhook/avisa-whatsapp")
        print("   OU:  configure N8N_WEBHOOK_URL no .env")
        sys.exit(1)

    resultados = []

    if args.suite:
        print(f"\n{BLUE}Rodando suite completa ({len(CASOS_TESTE)} casos){RESET}")
        for i, caso in enumerate(CASOS_TESTE, 1):
            print(f"\n{YELL}[{i}/{len(CASOS_TESTE)}] {caso['nome']}{RESET}")
            r = simular_webhook(n8n_url, args.numero, caso["mensagem"], args.nome)
            resultados.append({"caso": caso["nome"], **r})
            if i < len(CASOS_TESTE):
                time.sleep(2)

        print(f"\n{BLUE}=== Resultado da Suite ==={RESET}")
        for r in resultados:
            cor = GREEN if r["ok"] else RED
            print(f"  {cor}{'✓' if r['ok'] else '✗'}{RESET} {r['caso']}")

    else:
        mensagem = args.mensagem or "Preciso de um parecer jurídico sobre rescisão de contrato de trabalho"
        r = simular_webhook(n8n_url, args.numero, mensagem, args.nome)
        resultados.append(r)

    print(f"\n{BLUE}=== O que verificar agora ==={RESET}")
    print("  1. N8N respondeu 200 imediatamente ✓")
    print("  2. Mensagem de resposta chegou no WhatsApp (aguardar 5-30s)")
    print("  3. Supabase → tabela interacoes_whatsapp → novo registro")
    print("  4. N8N → Executions → verificar se todos os nodes passaram")
    print()


if __name__ == "__main__":
    main()
