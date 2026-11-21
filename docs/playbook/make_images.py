#!/usr/bin/env python3
"""Copy the worked examples' pictures into docs/playbook/img/ (small, cropped).

    python3 docs/playbook/make_images.py
For each example: source, the concept board the owner chose from (the big 256 px row only),
the final styles, the phone preview; rejected rounds where they teach something.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/playbook/img"
EX = {
    "telegram": {"concepts": "concepts.png"},
    "aurex_browser": {"concepts": "concepts.png"},
    "pokemon_unite": {"concepts": "concepts.png", "rejected-characters": "concepts-round3/concepts.png",
                      "rejected-poster": "concepts-round2/concepts.png"},
    "rush_royale": {"concepts": "concepts.png", "rejected-poster": "concepts-round2/concepts.png"},
}


def save(im, path, width):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.convert("RGB").save(path, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, boards in EX.items():
        w = ROOT / "work" / slug
        save(Image.open(w / "source.png"), OUT / f"{slug}-1-source.png", 256)
        for name, rel in boards.items():
            b = Image.open(w / rel)
            top = b.crop((0, 0, b.width, min(b.height, 640)))          # title + the 256 px row (light + dark)
            save(top, OUT / f"{slug}-2-{name}.png", 1000)
        save(Image.open(w / "styles.png"), OUT / f"{slug}-3-styles.png", 1200)
        if (w / "phone.png").exists():
            save(Image.open(w / "phone.png"), OUT / f"{slug}-4-phone.png", 900)
    print("wrote", len(list(OUT.glob("*.png"))), "images to", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
