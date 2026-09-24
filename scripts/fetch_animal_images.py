"""
Fetch animal images from Wikipedia REST API.

- Reads src/data/animals.json
- For each animal, queries Wikipedia summary endpoint by wiki_title
- Downloads the thumbnail (auto-upgraded to 512px wide)
- Pillow crops to a 256x256 circle with alpha
- Saves to public/animals/{id}.png

Re-runnable: skips animals whose output PNG already exists unless --force is passed.

Usage:
  python scripts/fetch_animal_images.py
  python scripts/fetch_animal_images.py --force
"""
import io
import json
import os
import re
import sys
import time
import urllib.request
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANIMALS_JSON = os.path.join(ROOT, "src", "data", "animals.json")
OUT_DIR = os.path.join(ROOT, "public", "animals")
TARGET_SIZE = 256
THUMB_WIDTH = 320  # only Wikimedia standard sizes accepted (120/240/320/480/640/800/1024)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 EarthZoo/0.1"
)
MAX_RETRY = 3

os.makedirs(OUT_DIR, exist_ok=True)


def http_get(url: str, accept: str = "*/*") -> bytes:
    last_err = None
    for attempt in range(MAX_RETRY):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": accept},
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise last_err


def get_image_url(wiki_title: str) -> str | None:
    """Query Wikipedia REST API. Prefer the API-supplied thumbnail (allowed size);
    fall back to originalimage if no thumbnail."""
    api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(wiki_title)}"
    try:
        data = json.loads(http_get(api, accept="application/json"))
    except Exception as e:
        print(f"  ! summary failed: {e}")
        return None
    thumb = data.get("thumbnail", {}).get("source")
    if thumb:
        return thumb
    orig = data.get("originalimage", {}).get("source")
    return orig


def make_circular(im: Image.Image, size: int = TARGET_SIZE) -> Image.Image:
    """Center-crop to square, resize, apply circular alpha mask."""
    im = ImageOps.fit(im.convert("RGBA"), (size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    im.putalpha(mask)
    return im


def fetch_one(animal: dict, force: bool) -> bool:
    aid = animal["id"]
    out_path = os.path.join(OUT_DIR, f"{aid}.png")
    if not force and os.path.exists(out_path):
        print(f"[skip] {aid}: already exists")
        return True

    wiki_title = animal.get("wiki_title")
    if not wiki_title:
        print(f"[!!] {aid}: missing wiki_title")
        return False

    print(f"[fetch] {aid}  <-  {wiki_title}")
    url = get_image_url(wiki_title)
    if not url:
        print(f"  ! no image found")
        return False
    try:
        raw = http_get(url)
        im = Image.open(io.BytesIO(raw))
        circ = make_circular(im)
        circ.save(out_path, "PNG", optimize=True)
        size_kb = os.path.getsize(out_path) // 1024
        print(f"  -> {out_path} ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"  ! download/process failed: {e}")
        return False


def main():
    force = "--force" in sys.argv
    with open(ANIMALS_JSON, "r", encoding="utf-8") as f:
        animals = json.load(f)

    print(f"Processing {len(animals)} animals (force={force})")
    print(f"Output: {OUT_DIR}\n")

    ok = 0
    for a in animals:
        if fetch_one(a, force):
            ok += 1
        time.sleep(0.4)  # polite to Wikipedia

    print(f"\nDone: {ok}/{len(animals)} OK")


if __name__ == "__main__":
    main()
