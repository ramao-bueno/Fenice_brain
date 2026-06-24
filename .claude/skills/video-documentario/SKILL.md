---
name: video-documentario
description: This skill should be used when the user asks to "criar um vídeo documentário", "gerar vídeo MP4 com fotos", "montar slideshow com Ken Burns", "produzir um documentário", "gerar preview do vídeo", "criar vídeo institucional" or any task involving creating documentary-style MP4 videos from static photos. Covers the full production pipeline — slide planning, HTML preview, Python MP4 generation (H.264 1920×1080), audio recording guidance, and post-production assembly. Enforce LGPD compliance: only public-domain or free-license images from external sources.
---

# SuperpowerFenice-08 — Produtor de Vídeo Documentário

Pipeline completo para criar vídeos documentários MP4 a partir de fotos estáticas, com efeito Ken Burns, transições, overlays de texto e créditos institucionais.

---

## Stack Técnica

| Componente | Uso |
|---|---|
| `Pillow` | Carregamento de imagens, overlays de texto (PIL.ImageDraw + ImageFont) |
| `opencv-python` (cv2) | Resize de frames — 5× mais rápido que PIL.BICUBIC |
| `imageio-ffmpeg` | Encode H.264 via FFmpeg embutido; sem instalação separada |
| `numpy` | Operações de frame (Ken Burns crop, blend, gradiente) |
| HTML/CSS/JS | Preview local do vídeo antes de gerar o MP4 |

Instalar dependências:
```
pip install Pillow imageio-ffmpeg opencv-python numpy
```

---

## Fluxo de Produção (5 etapas)

### 1 — Planejamento de Slides

Definir para cada slide:
- `src`: caminho local (`foto 1.jpeg`) ou URL pública (Wikimedia Commons)
- `dur`: duração em segundos
- `seg`: nome do segmento (exibido na legenda gold)
- `label`: legenda principal (branca, italic)
- `credit`: crédito de fonte (opcional — usar para imagens externas)

**Timings sugeridos para documentário de 8 min:**

| Segmento | Duração |
|---|---|
| Abertura épica | 60s |
| Bloco biográfico | 90–120s |
| Evento histórico | 60–90s |
| Local / patrimônio | 75–90s |
| Legado / conclusão | 60–75s |
| Encerramento | 45–60s |
| Créditos | 10s |

### 2 — LGPD: Fontes de Imagem Permitidas

Usar apenas imagens **livres**:
- **Fotos próprias** — acervo do projeto (sem restrição)
- **Wikimedia Commons** — filtrar por "Domínio Público" ou CC0
  - URL base: `https://upload.wikimedia.org/wikipedia/commons/`
  - Verificar licença na página da imagem antes de usar
- **Pixabay / Unsplash** — imagens CC0 (verificar individualmente)

Incluir nos créditos do vídeo a URL exata de cada imagem externa usada.

### 3 — Preview HTML (`preview_video.html`)

Gerar o arquivo HTML antes do MP4 para validar a sequência de slides, textos e tempos. Abrir no Chrome para testar.

Estrutura do HTML:
- `<div id="stage">` com slides empilhados via CSS `position: absolute`
- CSS `animation: kenburns` com `scale()` e `translate()` na tag `<img>`
- Transição via `opacity` CSS (crossfade)
- JavaScript auto-advance com `requestAnimationFrame` e array de slides
- Tela de créditos final com URLs das fontes Wikimedia

### 4 — Geração do MP4 (`generate_video.py`)

O script Python segue este pipeline interno:

```
download_web_images() → preload() → make_text_overlay() → encode loop
```

**Ken Burns com OpenCV (rápido):**
```python
import cv2, numpy as np

KB_W, KB_H = int(W * 1.09), int(H * 1.09)   # canvas 9% maior

def preload(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR→RGB
    scale = max(KB_W / img.shape[1], KB_H / img.shape[0])
    nw, nh = int(img.shape[1]*scale), int(img.shape[0]*scale)
    big = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC)
    cx = (nw - KB_W)//2; cy = (nh - KB_H)//2
    return big[cy:cy+KB_H, cx:cx+KB_W]          # numpy array RGB uint8

def ken_burns(base, progress, idx):
    zoom_in = (idx % 2 == 0)
    zoom    = 1.0 + 0.08*(progress if zoom_in else 1-progress)
    cw, ch  = int(W/zoom), int(H/zoom)
    bw, bh  = base.shape[1], base.shape[0]
    cx = (bw - cw)//2; cy = (bh - ch)//2
    cropped = base[cy:cy+ch, cx:cx+cw]
    return cv2.resize(cropped, (W, H), interpolation=cv2.INTER_CUBIC)
```

**Encode com imageio-ffmpeg:**
```python
import imageio_ffmpeg

writer = imageio_ffmpeg.write_frames(
    OUTPUT, size=(W, H), fps=30,
    codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p", quality=None,
    output_params=["-profile:v","high","-crf","18","-preset","medium","-movflags","+faststart"],
)
writer.send(None)          # prime o generator
writer.send(frame.tobytes())   # enviar cada frame como bytes RGB24
writer.close()
```

**Configurações de exportação (H.264 HD):**
- Contêiner: MP4
- Codec de vídeo: H.264 · perfil High · CRF 18 · preset medium
- Codec de áudio: AAC-LC 48kHz 320kbps (adicionar em pós-produção)
- Resolução: 1920×1080 · 16:9 · 30fps constante
- `+faststart`: move metadados para o início (streaming imediato)

**Tempo estimado de geração:**
- Com OpenCV: ~8–15 min para 8 min de vídeo (40–80 fps de geração)
- Com PIL apenas: ~35–45 min (5 fps de geração)

### 5 — Áudio e Pós-Produção

**Gravação de narração:**
- App recomendado: **Dolby On** (Android/iOS) — EQ automático, redução de ruído
- Gravar um arquivo por segmento (facilita encaixe no vídeo)
- Formato: MP4 ou WAV, mínimo 44.1kHz

**Montagem final (app gratuito):**
| App | Plataforma | Uso |
|---|---|---|
| CapCut | Windows/Android | Importar MP4 + áudios, ajustar tempos |
| DaVinci Resolve | Windows | Editor profissional gratuito |
| Adobe Express | Web/Desktop | Importar via Adobe CC |

**Fluxo no CapCut/DaVinci:**
1. Importar `video_mallet.mp4` como trilha de vídeo
2. Importar cada arquivo de narração (por segmento) na trilha de áudio
3. Alinhar narração com os slides correspondentes
4. Exportar como MP4 H.264 com áudio AAC-LC 48kHz

---

## Créditos Institucionais Padrão

Tela final (fundo escuro `#0a0a18`, barra gold no topo):

```
[TÍTULO DO DOCUMENTÁRIO]
[Subtítulo em itálico]

Direção e Roteiro  |  [Nome do professor/diretor]
Instituição        |  [Universidade / Campus]
Financiamento      |  [Fundo / Edital]
Período            |  [Mês a Mês de Ano]

FONTES HISTÓRICAS — WIKIMEDIA COMMONS (DOMÍNIO PÚBLICO)
• [Descrição da imagem] — [URL completa da página do Wikimedia]
• ...
```

---

## Checklist de Entrega

- [ ] Todas as imagens externas verificadas como domínio público ou CC0
- [ ] URLs das fontes incluídas na tela de créditos
- [ ] `preview_video.html` testado no Chrome antes de gerar o MP4
- [ ] MP4 gerado com CRF ≤ 18 e perfil High
- [ ] Áudio gravado por segmento com Dolby On
- [ ] Montagem final com áudio sincronizado

---

## Referência de Arquivos

Para projetos baseados neste workflow:

- `preview_video.html` — slideshow de preview (abrir no Chrome)
- `generate_video.py` — script de geração do MP4 (Python 3.10+)
- `video_mallet.mp4` — saída final sem áudio
- `cache_*.jpg` — imagens históricas baixadas automaticamente
- `video_log.txt` / `video_err.txt` — log de progresso e erros
