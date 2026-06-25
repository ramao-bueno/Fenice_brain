# ☁️ REZA DO DIA — Fenice IT
**Tech Lead: Ramão Bueno da Silva Neto**
**© 2026 Fenice IT Justech.ia · Todos os direitos reservados**

---

## 🔒 PERMISSÕES

> **Ninguém altera uma vírgula sem o meu consentimento.**

- Vercel → equipe `fenice-tech` → **só `ramao-bueno` como OWNER**
- GitHub → `ramao-bueno` → Owner único
- Supabase → `oiconsulbrasil@gmail.com` → Owner único
- Qualquer colaborador externo → revogar imediatamente se não autorizado

---

## 📂 PONTO DE PARTIDA

```
C:\Fenice_bRain   ← aqui e só aqui
git push github main
```

> Esqueça `C:\Fenice_Estudos` e `C:\projects\Fenice_brain` — são clones mortos.

---

## 🚀 DEPLOY — COMO SUBIR CADA PROJETO

| Site | Como deploiar |
|---|---|
| `fenice.ia.br` | `vercel deploy --prod` (de `C:\Fenice_bRain`) |
| `observatorio-da-mulher-sfs.com.br` | `git push github main` (auto, só se `violencia-mulher-sfs/` mudar) |
| B2B (futuro) | `git push github main` (auto, só se `b2b/` mudar) |

---

## ⚔️ REGRAS ANTI-CONFLITO

1. **Cada projeto tem seu `vercel.json` dentro do próprio subdiretório** — nunca depender só do root
2. **`.vercelignore` é whitelist** — novo projeto = nova linha `!/nome-do-projeto`
3. **Ignored Build Step está ativo** — observatório só rebuilda quando o código dele muda
4. **`git add` sempre por arquivo ou subdir** — nunca `git add .` na raiz (vault tem 23k arquivos com acentos)
5. **Antes de qualquer push**: `git status` e `curl -sI https://dominio | head -1`

---

## 🏷️ COPYRIGHT PADRÃO

```
© 2026 Fenice IT Justech.ia · Todos os direitos reservados · Developed by Ramão Bueno da Silva Neto / Tech Lead
```

> Vai em TODO rodapé, toda tela de login, todo documento publicado.

---

## ✅ CHECKLIST DIÁRIO

```powershell
# Situação dos sites
curl -sI https://fenice.ia.br | head -1
curl -sI https://observatorio-da-mulher-sfs.com.br | head -1

# Estado do repo
git status
git log --oneline -3
```

---

## 📖 REFERÊNCIAS RÁPIDAS

- Manual completo de infra → `docs/INFRA-DEPLOY.md`
- Credenciais do site → memória `project-site-auth`
- Skills carregadas → `C:\skills\`
- Supabase projeto → `qcfdssnpjzvjbvemhrik`
