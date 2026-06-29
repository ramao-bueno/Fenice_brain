---
tipo: controle-operacional
modulo: acesso
atualizado: 2026-06-29
tags: [controle, logins, acesso, lgpd, segurança]
---

# Controle de Logins — Fenice Acadêmico

> [!NOTE] LGPD
> Dados de acesso registrados conforme Art. 6º Lei 13.709/2018 — finalidade legítima, necessidade e segurança. Acesso restrito ao Tech Lead.

---

## Usuários Cadastrados

| Login | Nome | Perfil | WhatsApp | Status |
|-------|------|--------|----------|--------|
| `admin` | Ramão Bueno | Tech Lead / Admin | 5547991041414 | ✅ Ativo |
| `visitante` | Visitante | Acesso público | — | ✅ Ativo |
| `puff` | Puff | — | — | ✅ Ativo |
| `lorena` | Lorena | — | — | ✅ Ativo |
| `denny` | Denny | — | — | ✅ Ativo |
| `ana` | Ana | — | — | ✅ Ativo |
| `kaua` | Dr. Kauã | Acadêmico Direito | 5541984759558 | ✅ Ativo |
| `kaique` | Dr. Kaique | Acadêmico Direito | 5549998349001 | ✅ Ativo |
| `nelinha` | Dra. Emanuelle Bueno | Acadêmico Direito | 5547991048100 | ✅ Ativo |
| `tasso` | Ms. Dr. Tasso | Acadêmico Direito | 5547997032838 | ✅ Ativo |
| `modro` | Ms. Dr. Modro | Acadêmico Direito | 5547991651366 | ✅ Ativo |
| `ricardo` | Ms. Dr. Ricardo | Acadêmico Direito | 5547999180316 | ✅ Ativo |
| `diego` | Dr. Diego | Acadêmico Direito | 5547984171611 | ✅ Ativo |

---

## Monitoramento de Acessos — Supabase `fenice_access_logs`

> [!TIP] Como consultar
> Rodar a query abaixo no Supabase SQL Editor ou via script `scripts/monitor_acessos.py`

```sql
-- Resumo por usuário
SELECT
  usuario,
  COUNT(*) FILTER (WHERE sucesso = true)  AS logins_ok,
  COUNT(*) FILTER (WHERE sucesso = false) AS falhas,
  MAX(criado_em)                           AS ultimo_acesso,
  COUNT(DISTINCT ip)                       AS ips_distintos
FROM fenice_access_logs
GROUP BY usuario
ORDER BY ultimo_acesso DESC;

-- Últimos 50 acessos
SELECT usuario, sucesso, ip, detalhe, criado_em
FROM fenice_access_logs
ORDER BY criado_em DESC
LIMIT 50;

-- IPs suspeitos (mais de 3 falhas)
SELECT ip, COUNT(*) AS falhas
FROM fenice_access_logs
WHERE sucesso = false
GROUP BY ip
HAVING COUNT(*) > 3
ORDER BY falhas DESC;
```

---

## Relatório — 2026-06-29

| Usuário | Logins OK | Falhas | Último Acesso (UTC) | IPs Distintos |
|---------|-----------|--------|---------------------|---------------|
| admin | 10 | 0 | 2026-06-29 01:19 | 1 |
| nelinha | 1 | 0 | 2026-06-29 13:46 | 1 |
| lorena | 3 | 1 | 2026-06-28 09:56 | 2 |
| visitante | 1 | 0 | 2026-06-27 21:46 | 1 |

> [!WARNING] Observação
> `lorena` registrou 1 falha em 2026-06-27 — pode ter digitado senha errada. Sem padrão de ataque.

---

## Regras de Segurança (LGPD + sistema)

- Rate limit: **5 tentativas por IP a cada 5 minutos**
- IPs com mais de 3 falhas consecutivas → investigar
- Logs mantidos no Supabase — não expor via API pública
- Senhas armazenadas apenas no Vercel (env var `SITE_PASS`) — nunca no vault
- Atualizar este arquivo a cada novo cadastro ou suspeita
