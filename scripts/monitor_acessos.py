# -*- coding: utf-8 -*-
"""
monitor_acessos.py — Relatório de acessos fenice.ia.br
Consulta fenice_access_logs no Supabase e exibe resumo no terminal.
Uso: python scripts/monitor_acessos.py
"""
import os, sys, io, json, urllib.request
from datetime import datetime, timezone
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

def _env(key):
    v = os.getenv(key, "")
    if not v:
        sys.exit(f"[ERRO] variável {key} não definida no .env")
    return v

def supabase_get(url, key, query):
    req = urllib.request.Request(
        f"{url}/rest/v1/rpc/fenice_access_logs_report" if False else f"{url}/rest/v1/fenice_access_logs?{query}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

SB_URL = _env("SUPABASE_URL").rstrip("/")
SB_KEY = _env("SUPABASE_SERVICE_KEY")

print("=" * 60)
print("  FENICE IT — Monitor de Acessos")
print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
print("=" * 60)

# Últimos 30 acessos
rows = supabase_get(SB_URL, SB_KEY,
    "select=usuario,sucesso,ip,detalhe,criado_em&order=criado_em.desc&limit=30")

print(f"\n{'USUÁRIO':<12} {'OK':<5} {'IP':<18} {'DATA (UTC)':<22} {'DETALHE'}")
print("-" * 75)
for r in rows:
    ok   = "✅" if r["sucesso"] else "❌"
    dt   = r["criado_em"][:16].replace("T", " ")
    ip   = (r["ip"] or "—")[:17]
    det  = (r["detalhe"] or "")[:30]
    print(f"{r['usuario']:<12} {ok:<5} {ip:<18} {dt:<22} {det}")

# IPs com falhas
falhas = [r for r in rows if not r["sucesso"]]
if falhas:
    print(f"\n⚠️  {len(falhas)} falha(s) nos últimos 30 registros:")
    for f in falhas:
        print(f"   → {f['usuario']} | IP {f['ip']} | {f['criado_em'][:16]}")
else:
    print("\n✅ Nenhuma falha de login nos últimos 30 registros.")

print("\n" + "=" * 60)
print("  Para detalhes completos: https://supabase.com/dashboard")
print("=" * 60)
