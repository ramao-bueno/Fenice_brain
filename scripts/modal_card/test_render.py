from pathlib import Path
import subprocess, sys
from PIL import Image

BASE = Path(__file__).parent


def test_render_produces_1080x1440_png():
    png = BASE / "card.png"
    if png.exists():
        png.unlink()
    subprocess.run([sys.executable, str(BASE / "build_card.py")], check=True)
    r = subprocess.run([sys.executable, str(BASE / "render_card.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert png.exists(), "card.png não foi criado"
    w, h = Image.open(png).size
    assert (w, h) == (1080, 1440), f"dimensões erradas: {w}x{h}"
    assert png.stat().st_size > 20000, "PNG suspeito de estar vazio"
