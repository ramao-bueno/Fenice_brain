import base64, sys
from pathlib import Path

BASE = Path(__file__).parent
ASSETS = Path(r"C:\Fenice_site\TIM")
MAP = {
    "IMG_TEO":    "téo.jpeg",
    "IMG_FENICE": "logo fenice emoji.jpeg",
    "IMG_TIM":    "emoji tim.jpeg",
    "IMG_ACAD":   "Acadêmico Ciências Jurídicas.jpeg",
    "IMG_OBS":    "mulheres.jpeg",
    "IMG_API":    "api e desenvolvedores.jpeg",
    "IMG_JUR":    "consultoria jurídica.jpeg",
    "IMG_FILO":   "filosofia.jpeg",
    "IMG_ESP":    "especialista.jpeg",
}


def _data_uri(p: Path) -> str:
    b = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b}"


def build(template=BASE / "card_template.html", assets=ASSETS, out=BASE / "card_built.html") -> Path:
    html = Path(template).read_text(encoding="utf-8")
    for key, fname in MAP.items():
        src = Path(assets) / fname
        if not src.exists():
            raise FileNotFoundError(f"asset ausente: {src}")
        html = html.replace("{{" + key + "}}", _data_uri(src))
    Path(out).write_text(html, encoding="utf-8")
    return Path(out)


if __name__ == "__main__":
    p = build()
    print("card_built.html gerado:", p)
