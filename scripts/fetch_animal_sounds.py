"""
Fetch animal calls from Wikipedia.

For each animal in animals.json:
  1. Query Wikipedia page/media-list to list audio files in the article.
  2. Pick the first .ogg / .mp3 / .wav (skip .ogv videos).
  3. Resolve the actual URL via Commons imageinfo API.
  4. Download to public/sounds/{id}.{ext}.

Updates animals.json adding a "sound" field with the file extension found
(or null if no audio is available for that species — many mammals lack it).

Usage:
  python scripts/fetch_animal_sounds.py
  python scripts/fetch_animal_sounds.py --force
"""
import io
import json
import os
import sys
import time
import urllib.request
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANIMALS_JSON = os.path.join(ROOT, "src", "data", "animals.json")
OUT_DIR = os.path.join(ROOT, "public", "sounds")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 EarthZoo/0.1"
)
MAX_RETRY = 3
MAX_BYTES = 1_500_000  # 1.5 MB — skip very large files (e.g. full video soundtracks)
AUDIO_EXTS = (".ogg", ".oga", ".mp3", ".wav", ".m4a")

os.makedirs(OUT_DIR, exist_ok=True)


def http_get(url: str, accept: str = "*/*") -> bytes:
    last = None
    for i in range(MAX_RETRY):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": USER_AGENT, "Accept": accept}
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(1 + i)
    raise last


def list_audio_titles(wiki_title: str) -> list[str]:
    url = f"https://en.wikipedia.org/api/rest_v1/page/media-list/{quote(wiki_title)}"
    try:
        data = json.loads(http_get(url, "application/json"))
    except Exception as e:
        print(f"  ! media-list failed: {e}")
        return []
    titles = []
    for it in data.get("items", []):
        if it.get("type") != "audio":
            continue
        t = it.get("title", "")
        if t.lower().endswith(AUDIO_EXTS):
            titles.append(t)
    return titles


def resolve_url(file_title: str) -> str | None:
    """Commons imageinfo -> real upload.wikimedia.org URL."""
    api = (
        "https://commons.wikimedia.org/w/api.php"
        f"?action=query&titles={quote(file_title)}"
        "&prop=imageinfo&iiprop=url&format=json"
    )
    try:
        data = json.loads(http_get(api, "application/json"))
    except Exception as e:
        print(f"  ! imageinfo failed: {e}")
        return None
    pages = data.get("query", {}).get("pages", {})
    for p in pages.values():
        infos = p.get("imageinfo", [])
        if infos:
            return infos[0].get("url")
    return None


def fetch_one(animal: dict, force: bool) -> str | None:
    aid = animal["id"]
    wt = animal.get("wiki_title")
    if not wt:
        return None
    # Skip if any sound file already exists for this id
    if not force:
        for ext in AUDIO_EXTS:
            p = os.path.join(OUT_DIR, f"{aid}{ext}")
            if os.path.exists(p):
                print(f"[skip] {aid}: already has {ext}")
                return ext.lstrip(".")

    print(f"[scan] {aid}  <-  {wt}")
    titles = list_audio_titles(wt)
    if not titles:
        print(f"  - no audio in article")
        return None

    for ft in titles:
        url = resolve_url(ft)
        time.sleep(0.3)
        if not url:
            continue
        ext = os.path.splitext(url)[1].lower().lstrip(".")
        out_path = os.path.join(OUT_DIR, f"{aid}.{ext}")
        try:
            raw = http_get(url)
            if len(raw) > MAX_BYTES:
                print(f"  - skip {ft}: {len(raw)//1024} KB > limit")
                continue
            with open(out_path, "wb") as f:
                f.write(raw)
            kb = os.path.getsize(out_path) // 1024
            print(f"  -> {out_path} ({kb} KB)  [{ft}]")
            return ext
        except Exception as e:
            print(f"  ! download {ft} failed: {e}")
            continue
    return None


def main():
    force = "--force" in sys.argv
    with open(ANIMALS_JSON, "r", encoding="utf-8") as f:
        animals = json.load(f)

    print(f"Processing {len(animals)} animals (force={force})")
    print(f"Output: {OUT_DIR}\n")

    found = 0
    changed = False
    for a in animals:
        ext = fetch_one(a, force)
        if a.get("sound") != ext:
            a["sound"] = ext  # may be None
            changed = True
        if ext:
            found += 1
        time.sleep(0.4)

    if changed:
        with open(ANIMALS_JSON, "w", encoding="utf-8") as f:
            json.dump(animals, f, ensure_ascii=False, indent=2)
        print(f"\nUpdated {ANIMALS_JSON} with sound fields")

    print(f"\nDone: {found}/{len(animals)} have audio")


if __name__ == "__main__":
    main()
