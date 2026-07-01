from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent


def render(html=BASE / "card_built.html", out=BASE / "card.png") -> Path:
    url = Path(html).resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1440})
        page.goto(url)
        page.locator("#card").screenshot(path=str(out))
        browser.close()
    return Path(out)


if __name__ == "__main__":
    print("card.png gerado:", render())
