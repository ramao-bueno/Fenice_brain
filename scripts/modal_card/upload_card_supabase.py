import os, sys, json, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent  # C:\Fenice_bRain

BUCKET = "modal"
DEFAULT_FILE = BASE / "card_final.jpg"
DEFAULT_OBJECT = "modal_teo.jpg"


def _env():
    e = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip()
    return e


def _req(url, method, key, data=None, ctype="application/json"):
    h = {"Authorization": f"Bearer {key}", "apikey": key, "Content-Type": ctype}
    return urllib.request.Request(url, data=data, headers=h, method=method)


def main(src=DEFAULT_FILE, obj=DEFAULT_OBJECT):
    src = Path(src)
    ctype = "image/jpeg" if src.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    e = _env()
    base = e["SUPABASE_URL"].rstrip("/")
    key = e["SUPABASE_SERVICE_KEY"]
    # 1) garantir bucket público (ignora erro se já existe)
    try:
        urllib.request.urlopen(_req(f"{base}/storage/v1/bucket", "POST", key,
            json.dumps({"id": BUCKET, "name": BUCKET, "public": True}).encode()), timeout=20)
        print("[bucket] criado")
    except urllib.error.HTTPError as ex:
        print("[bucket] já existe (", ex.code, ")")
    # 2) upload (upsert)
    img = src.read_bytes()
    up = _req(f"{base}/storage/v1/object/{BUCKET}/{obj}", "POST", key, img, ctype)
    up.add_header("x-upsert", "true")
    try:
        urllib.request.urlopen(up, timeout=45)
        print("[upload] ok", len(img), "bytes")
    except urllib.error.HTTPError as ex:
        print("[upload] ERRO", ex.code, ex.read().decode()[:300])
        sys.exit(1)
    # 3) URL pública + validação
    public = f"{base}/storage/v1/object/public/{BUCKET}/{obj}"
    r = urllib.request.urlopen(public, timeout=20)
    ok = r.status == 200 and r.headers.get("Content-Type", "").startswith("image")
    assert ok, f"URL pública inválida: {r.status} {r.headers.get('Content-Type')}"
    print("PUBLIC_URL:", public)


if __name__ == "__main__":
    main(*sys.argv[1:])
