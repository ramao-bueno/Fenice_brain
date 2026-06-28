"""
Analisa um vídeo e remove automaticamente:
  - Segmentos com pessoas (detecção de faces e corpo)
  - Frames virados (câmera de cabeça para baixo)
  - Frames de baixa qualidade (borrado, escuro)

Saída: vídeo limpo em _cleaned.mp4
"""
import cv2
import numpy as np
import subprocess
import json
import sys
import os
from pathlib import Path

# ── Parâmetros ─────────────────────────────────────────────────
VIDEO_IN = r"C:\Fenice_bRain\09_FENICE_BRAIN\Videos\2026-06-27\20260627_100146.mp4"
VIDEO_OUT = r"C:\Fenice_bRain\09_FENICE_BRAIN\Videos\2026-06-27\20260627_100146_cleaned.mp4"

SAMPLE_EVERY_N_FRAMES = 15       # analisa 1 frame a cada 0.5s (30fps / 15)
FACE_SCALE = 1.1
FACE_MIN_NEIGHBORS = 4
FACE_MIN_SIZE = (60, 60)
BLUR_THRESHOLD = 60.0            # Laplacian var < threshold → borrado
DARK_THRESHOLD = 20.0            # luminância média < threshold → escuro
UPSIDE_THRESHOLD = 0.15          # diferença relativa top vs bottom
MARGIN_SEC = 2.0                 # segundos de margem ao redor de segmento ruim
MIN_BAD_DURATION = 0.5           # descarta detecções menores que 0.5s

def load_cascades():
    # Path sem acento para evitar bug do OpenCV com caracteres especiais
    data = r"C:\opencv_data"
    face_front = cv2.CascadeClassifier(os.path.join(data, "haarcascade_frontalface_default.xml"))
    face_profile = cv2.CascadeClassifier(os.path.join(data, "haarcascade_profileface.xml"))
    body = cv2.CascadeClassifier(os.path.join(data, "haarcascade_upperbody.xml"))
    if face_front.empty() or face_profile.empty() or body.empty():
        raise RuntimeError(f"Falha ao carregar cascades de {data}")
    return face_front, face_profile, body

def is_upside_down(gray):
    """Verifica se frame está de cabeça para baixo comparando luminância top vs bottom."""
    h = gray.shape[0]
    top = gray[:h//3, :].mean()
    bottom = gray[2*h//3:, :].mean()
    # Em cenas normais, céu/luz costuma estar acima → top >= bottom.
    # Se bottom >> top de forma significativa, pode estar invertido.
    if top < 10 and bottom < 10:
        return False  # frame escuro — não dá pra dizer
    if top + bottom == 0:
        return False
    diff = (bottom - top) / (top + bottom + 1e-6)
    return diff > UPSIDE_THRESHOLD

def is_blurry(gray):
    return cv2.Laplacian(gray, cv2.CV_64F).var() < BLUR_THRESHOLD

def is_dark(gray):
    return gray.mean() < DARK_THRESHOLD

def has_person(frame, gray, face_front, face_profile, body):
    faces_f = face_front.detectMultiScale(gray, FACE_SCALE, FACE_MIN_NEIGHBORS, minSize=FACE_MIN_SIZE)
    if len(faces_f) > 0:
        return True
    faces_p = face_profile.detectMultiScale(gray, FACE_SCALE, FACE_MIN_NEIGHBORS, minSize=FACE_MIN_SIZE)
    if len(faces_p) > 0:
        return True
    bodies = body.detectMultiScale(gray, 1.05, 3, minSize=(80, 80))
    if len(bodies) > 0:
        return True
    return False

def analyse(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total / fps
    print(f"Vídeo: {total} frames, {fps:.2f} fps, {duration:.1f}s ({duration/60:.1f} min)")

    face_front, face_profile, body = load_cascades()

    bad_frames = set()
    reasons = {}
    frame_idx = 0
    analysed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % SAMPLE_EVERY_N_FRAMES == 0:
            small = cv2.resize(frame, (640, 360))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

            r = []
            if is_dark(gray):
                r.append("dark")
            if not r and is_blurry(gray):
                r.append("blur")
            if not r and is_upside_down(gray):
                r.append("upside")
            if not r and has_person(frame, gray, face_front, face_profile, body):
                r.append("person")

            if r:
                # marca todos os N frames deste intervalo como ruins
                for fi in range(frame_idx, min(frame_idx + SAMPLE_EVERY_N_FRAMES, total)):
                    bad_frames.add(fi)
                reasons[frame_idx] = r

            analysed += 1
            if analysed % 100 == 0:
                pct = frame_idx / total * 100
                print(f"  {pct:.0f}% — {frame_idx}/{total} frames | ruins até agora: {len(reasons)}")

        frame_idx += 1

    cap.release()
    print(f"\nAnálise concluída: {len(reasons)} intervalos ruins detectados")
    return bad_frames, reasons, fps, total, duration

def frames_to_segments(bad_frames, fps, total, margin_sec):
    """Converte conjunto de frames ruins em segmentos (start_s, end_s)."""
    if not bad_frames:
        return []

    margin = int(margin_sec * fps)
    expanded = set()
    for f in bad_frames:
        for fi in range(max(0, f - margin), min(total, f + margin + 1)):
            expanded.add(fi)

    segments = []
    sorted_frames = sorted(expanded)
    start = sorted_frames[0]
    prev = sorted_frames[0]

    for f in sorted_frames[1:]:
        if f > prev + 1:
            segments.append((start / fps, prev / fps))
            start = f
        prev = f
    segments.append((start / fps, prev / fps))

    # filtra segmentos muito curtos
    return [(s, e) for s, e in segments if (e - s) >= MIN_BAD_DURATION]

def build_keep_list(bad_segments, duration):
    """Inverte os segmentos ruins para obter segmentos a manter."""
    keep = []
    cursor = 0.0
    for start, end in bad_segments:
        if cursor < start:
            keep.append((cursor, start))
        cursor = end
    if cursor < duration:
        keep.append((cursor, duration))
    return [(s, e) for s, e in keep if (e - s) >= 1.0]

def run_ffmpeg(video_in, video_out, keep_segments, fps):
    """Concatena segmentos usando FFmpeg concat demuxer."""
    env = os.environ.copy()
    ffmpeg_paths = [
        r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
    ]
    ffmpeg = "ffmpeg"
    for p in ffmpeg_paths:
        if os.path.exists(p):
            ffmpeg = p
            break

    if not keep_segments:
        print("AVISO: nenhum segmento bom encontrado! Nada a exportar.")
        return

    # Cria arquivo de lista concat
    concat_file = VIDEO_OUT.replace(".mp4", "_concat.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for i, (start, end) in enumerate(keep_segments):
            f.write(f"file '{video_in.replace(chr(92), '/')}'\n")
            f.write(f"inpoint {start:.4f}\n")
            f.write(f"outpoint {end:.4f}\n")

    cmd = [
        ffmpeg, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        video_out
    ]

    print("\nExecutando FFmpeg...")
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERRO FFmpeg:", result.stderr[-2000:])
    else:
        size = Path(video_out).stat().st_size / 1024**2
        print(f"\n✅ Exportado: {video_out} ({size:.0f} MB)")

    os.remove(concat_file)

def main():
    print("=" * 60)
    print("Fenice — Limpador de Vídeo")
    print("=" * 60)

    bad_frames, reasons, fps, total, duration = analyse(VIDEO_IN)

    if reasons:
        print("\nMotivos de exclusão encontrados:")
        counts = {}
        for r_list in reasons.values():
            for r in r_list:
                counts[r] = counts.get(r, 0) + 1
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            pct = v * SAMPLE_EVERY_N_FRAMES / total * 100
            print(f"  {k:10s}: {v:4d} amostras (~{pct:.0f}% do vídeo)")

    bad_segments = frames_to_segments(bad_frames, fps, total, MARGIN_SEC)
    print(f"\nSegmentos ruins (com margem): {len(bad_segments)}")
    for i, (s, e) in enumerate(bad_segments[:20]):
        print(f"  [{i+1:3d}] {s:7.1f}s – {e:7.1f}s  ({e-s:.1f}s)")
    if len(bad_segments) > 20:
        print(f"  ... e mais {len(bad_segments) - 20} segmentos")

    keep = build_keep_list(bad_segments, duration)
    keep_total = sum(e - s for s, e in keep)
    print(f"\nSegmentos a manter: {len(keep)} ({keep_total:.0f}s / {keep_total/60:.1f} min)")
    for i, (s, e) in enumerate(keep[:20]):
        print(f"  [{i+1:3d}] {s:7.1f}s – {e:7.1f}s")

    if not keep:
        print("\nNenhum segmento bom encontrado. Vídeo não alterado.")
        return

    # Salva relatório JSON
    report_path = VIDEO_OUT.replace(".mp4", "_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "bad_segments": bad_segments,
            "keep_segments": keep,
            "reasons": {str(k): v for k, v in reasons.items()},
            "original_duration": duration,
            "final_duration": keep_total,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nRelatório salvo: {report_path}")

    run_ffmpeg(VIDEO_IN, VIDEO_OUT, keep, fps)

if __name__ == "__main__":
    main()
