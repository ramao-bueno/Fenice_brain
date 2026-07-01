from pathlib import Path
import subprocess, sys

BASE = Path(__file__).parent


def test_build_produces_html_without_placeholders():
    out = BASE / "card_built.html"
    if out.exists():
        out.unlink()
    r = subprocess.run([sys.executable, str(BASE / "build_card.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists(), "card_built.html não foi criado"
    html = out.read_text(encoding="utf-8")
    assert "{{" not in html, "restaram placeholders não substituídos"
    assert html.count("data:image/") >= 9, "esperados >=9 assets embutidos em base64"
    assert "by Tech Lead Ramão Bueno" in html
