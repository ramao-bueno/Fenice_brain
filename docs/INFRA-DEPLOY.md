# Fenice IT — Infraestrutura e Deploy
**Tech Lead: Ramão Bueno da Silva Neto**
**© 2026 Fenice IT Justech.ia · Todos os direitos reservados**

---

## Arquitetura de Repositórios

| Repositório GitHub | Diretório Local | Finalidade |
|---|---|---|
| `ramao-bueno/Fenice_brain` | `C:\Fenice_bRain` | Monorepo principal — vault + apps |
| `ramao-bueno/Fenice_site` | `C:\Fenice_site` | Site Quartz (fenicejus.fenice.ia.br) |

> **Regra**: `C:\Fenice_bRain` é o ponto de partida diário. NUNCA trabalhe em `C:\Fenice_Estudos` ou `C:\projects\Fenice_brain` — são clones legados sem remote correto.

---

## Projetos Vercel (equipe: fenice-tech)

### 1. fenice-justech → `fenice.ia.br`
- **Tipo**: Python FastAPI (SaaS jurídico + RAG)
- **Deploy**: **MANUAL** via CLI
- **Acesso ao Obsidian**: `fenice.ia.br` → login `admin` / `fenice@2025`
- **Arquivos-fonte**: `api/index.py`, `scripts/api_fenice_saas.py`, `scripts/fenice_rag.py`

```powershell
# Como deploiar (rodar de C:\Fenice_bRain):
vercel deploy --prod
```

### 2. violencia-mulher-sfs → `observatorio-da-mulher-sfs.com.br`
- **Tipo**: Next.js 16 (App Router)
- **Deploy**: **AUTOMÁTICO** — git push em `main` quando `violencia-mulher-sfs/` muda
- **Ignored Build Step**: `git diff --quiet HEAD^ HEAD -- violencia-mulher-sfs/`
- **Arquivos-fonte**: `violencia-mulher-sfs/` (subdiretório completo)

```powershell
# Como deploiar — apenas faça o commit e push normalmente:
git add violencia-mulher-sfs/
git commit -m "feat(observatorio): ..."
git push github main
```

### 3. B2B (FUTURO) → domínio a definir
- **Tipo**: a definir (Next.js recomendado)
- **Deploy**: AUTOMÁTICO via git push quando `b2b/` muda
- **Pré-requisitos antes de criar**:
  1. Criar subdiretório `b2b/` neste repo
  2. Adicionar `b2b/vercel.json` com buildCommand correto
  3. Descomentar `!/b2b` no `.vercelignore`
  4. Criar projeto no Vercel com `rootDirectory: "b2b"`
  5. Configurar Ignored Build Step: `git diff --quiet HEAD^ HEAD -- b2b/`

---

## Estrutura do Monorepo

```
C:\Fenice_bRain/                    ← raiz do repo (Obsidian vault)
├── .vercelignore                   ← whitelist: expõe só o necessário por projeto
├── vercel.json                     ← config Python para fenice-justech (deploy manual)
├── api/
│   └── index.py                    ← entry point FastAPI
├── scripts/
│   ├── api_fenice_saas.py          ← app FastAPI principal
│   ├── fenice_rag.py               ← motor RAG
│   ├── landing.html                ← SPA do fenice.ia.br
│   └── prompts/                    ← prompts do sistema
├── requirements.txt                ← deps Python para Vercel
├── violencia-mulher-sfs/           ← Observatório da Mulher (Next.js)
│   ├── vercel.json                 ← OBRIGATÓRIO: sobrescreve o vercel.json da raiz
│   ├── app/                        ← App Router
│   └── components/
└── [vault Obsidian — nunca deployado]
```

---

## Permissões

| Plataforma | Usuário | Nível |
|---|---|---|
| Vercel (fenice-tech) | `ramao-bueno` | OWNER (único) |
| GitHub | `ramao-bueno` | Owner |
| Supabase | `oiconsulbrasil@gmail.com` | Owner |

> **Política**: nenhum colaborador externo recebe acesso sem aprovação expressa do Tech Lead. Revogar imediatamente qualquer acesso não autorizado via `vercel team members`.

---

## Rotina Diária — Checklist

```powershell
# 1. Verificar ponto de partida correto
cd C:\Fenice_bRain
git status

# 2. Verificar status dos sites (roda de qualquer lugar)
curl -sI https://fenice.ia.br | head -1
curl -sI https://observatorio-da-mulher-sfs.com.br | head -1

# 3. Se precisar deploiar o fenice.ia.br (Python API):
vercel deploy --prod

# 4. Se precisar deploiar o observatório:
git add violencia-mulher-sfs/
git commit -m "fix/feat(observatorio): ..."
git push github main
```

---

## Regras Anti-Conflito

1. **Cada projeto tem seu próprio `vercel.json` no subdiretório** — nunca deixe o root `vercel.json` sem um `vercel.json` de override no subdir.
2. **`.vercelignore` é whitelist** — qualquer novo diretório de app precisa de `!/nome` aqui.
3. **Ignored Build Step está ativo** — o observatório só rebuilda quando os seus arquivos mudam.
4. **Nunca faça `git add .` na raiz** — pode stagear arquivos de vault com caracteres especiais.
5. **Remote correto**: o remote do repo principal é `github` (não `origin`). Use `git push github main`.
