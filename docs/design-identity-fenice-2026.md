# Fenice bRain — Identidade Visual 2026

> Documento de design produzido em 2026-06-24  
> Referência: imagem de exemplo fornecida pelo usuário (hero com logotipos e nova tipografia)

---

## Paleta de Cores

| Token        | Hex       | Uso                                    |
|-------------|-----------|----------------------------------------|
| `--gold`    | `#f59e0b` | Destaque, "Fenice" no título, accent   |
| `--gold2`   | `#fbbf24` | Hover states, shimmer highlight        |
| `--gold-dim`| `#d97706` | Shimmer sombra, bordas                 |
| `--seal-gold`| `#c9a227` | Selo jurídico, ornamentos              |
| `--bg`      | `#04080f` | Fundo principal                        |
| `--surface` | `#0b1525` | Superfícies elevadas                   |
| `--text`    | `#f1f5f9` | Texto principal, "bRain"               |
| `--muted`   | `#94a3b8` | Texto secundário, subtítulos           |

---

## Tipografia

### Kit Adobe Fonts

```html
<!-- Kit antigo (body: acumin-pro, adelle) -->
<link rel="stylesheet" href="https://use.typekit.net/ajp1gxj.css">
<!-- Kit novo (display: sloop-script-one, caprizant, skeena-display) -->
<link rel="stylesheet" href="https://use.typekit.net/cmr1ivs.css">
```

### Hierarquia Tipográfica

| Papel                      | Fonte                              | Peso | Uso                                   |
|---------------------------|------------------------------------|------|---------------------------------------|
| **Display "Fenice"**      | `sloop-script-one` (Sloop Script One) | 400 | Título principal — palavra "Fenice"   |
| **Display "bRain"**       | `skeena-display`                   | 700  | Título principal — palavra "bRain"    |
| **Subtítulos / Labels**   | `caprizant` (Caprizant)            | 400  | `hero-sub`, `section-label`, `hero-sabedoria` |
| **Corpo de texto**        | `acumin-pro`                       | 400  | Parágrafos, descrições                |
| **Seções / Stats**        | `skeena-display`                   | 700  | Números de destaque, títulos de seção |
| **Adorno / Label formal** | `adelle`                           | 700  | Rótulos de endpoints, badges          |

### Motivação

- **Sloop Script One** — script de caligrafia elegante, evoca autoridade jurídica clássica,  
  combina com a identidade "Filosofia e Direito" do selo. Contrasta com o display tech do "bRain".
- **Caprizant** — elegância histórica britânica (estilo herdado), ideal para labels e subtítulos  
  formais em letras espaçadas (`letter-spacing: 0.18em`).
- **Skeena Display Bold** — moderno, forte, tech — âncora o "bRain" no universo SaaS/API.

---

## Logotipos

### 1. Phoenix Fenice (principal)
- **Arquivo**: `docs/logo fenice.png`
- **Servido via**: `/logo-fenice.png` (endpoint FastAPI)
- **Uso no site**: nav (33×33px circular), hero (opcional como fundo decorativo)
- **Fundo**: dark circular frame, pena/fênix dourada

### 2. Selo Jurídico "Filosofia e Direito"
- **Formato**: SVG inline no `landing.html` (`.hero-seal`)
- **Texto**: "FILOSOFIA E DIREITO" (arco superior) + "EST. MCMLXII" (inferior) + "Sabedoria e Justiça"
- **Ícones internos**: Balança da Justiça + Coruja (sabedoria) + Coluna (firmeza)
- **Cor**: `#c9a227` (seal-gold) sobre fundo `#04080f`
- **Animação**: `sealGlow` — pulsação dourada suave (5s loop)

---

## Componentes Atualizados

### Nav

```html
<a href="/" class="nav-logo">
  <img class="nav-seal" src="/logo-fenice.png" alt="Fenice" width="33" height="33"
       onerror="this.style.display='none'">
  <span class="fenice-word">Fenice</span> <span>bRain</span>
</a>
```

```css
.nav-logo .fenice-word {
  font-family: "sloop-script-one", cursive;
  font-weight: 400;
  font-size: 1.55rem;
  color: var(--gold);
}
```

### Hero Title

```html
<h1>
  <span class="shimmer-text">Fenice</span>
  <span class="brain-text">bRain</span>
</h1>
```

```css
.shimmer-text {
  font-family: "sloop-script-one", cursive;
  font-weight: 400;
  font-size: clamp(4rem, 11vw, 8.5rem);
  /* shimmer dourado animado */
}
.brain-text {
  font-family: "skeena-display", serif;
  font-weight: 700;
  color: var(--text);
  font-size: clamp(3rem, 8.5vw, 7rem);
}
```

---

## Fila de Execução

- [x] Adicionar kit Adobe Fonts `cmr1ivs` (Sloop Script, Caprizant, Skeena Display)
- [x] Atualizar `.shimmer-text` → `sloop-script-one` + tamanho ajustado
- [x] Criar `.brain-text` → `skeena-display` bold branco
- [x] Atualizar `.fenice-word` no nav → `sloop-script-one`
- [x] Atualizar `hero-sub`, `section-label`, `hero-sabedoria` → `caprizant`
- [x] Adicionar endpoint `/logo-fenice.png` na API FastAPI
- [x] Integrar `<img class="nav-seal">` com logo Fenice no nav
- [ ] **PRÓXIMO**: Criar versão Adobe Express do poster/identidade para redes sociais
- [ ] **PRÓXIMO**: Aplicar identidade visual ao site violencia-mulher-sfs (Observatório)
- [ ] **PRÓXIMO**: Criar favicon a partir do logo fenice.png
- [ ] **PRÓXIMO**: Adicionar endpoint `/favicon.ico` na API

---

## Referência Visual

Baseado na imagem de exemplo do usuário (hero Fenice bRain):
- Logo circular Fenice no canto superior esquerdo
- Selo central "Filosofia e Direito — Sabedoria e Justiça — Est. MCMLXII"
- "Fenice" em script cursivo laranja (Sloop Script One)
- "bRain" em bold display branco (Skeena Display)
- "VADE MECUM DINÂMICO · SAAS API JURÍDICA" em maiúsculas espaçadas (Caprizant)
- Fundo escuro (#04080f) com efeito ember/brasa dourado
