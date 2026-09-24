"""
Sync animals.json sound field with what's actually on disk.
- If public/sounds/{id}.{ext} doesn't exist, remove the sound field.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = os.path.join(ROOT, "src", "data", "animals.json")
SDIR = os.path.join(ROOT, "public", "sounds")

with open(J, "r", encoding="utf-8") as f:
    items = json.load(f)

changed = 0
for a in items:
    s = a.get("sound")
    if s:
        p = os.path.join(SDIR, f"{a['id']}.{s}")
        if not os.path.exists(p):
            a.pop("sound", None)
            print(f"[fix] {a['id']}: sound field removed (file missing)")
            changed += 1

with open(J, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
print(f"Done. {changed} entries fixed.")
