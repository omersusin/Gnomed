#!/usr/bin/env python3
"""docs/redesign/gnome-objects.png: real GNOME app icons (from the vendored reference
library) labelled with the technique each one shows.  python3 docs/redesign/make_refs.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools/gnome-android-icons/assets/reference-library"
sys.path.insert(0, str(ROOT / "tools/gnome-android-icons/scripts"))
from PIL import Image, ImageDraw  # noqa: E402
from _common import render_svg, load_font  # noqa: E402

PICKS = [("Calls", "a mark made into an object", "no plate behind it"),
         ("FileRoller", "a thick object: tall side", "material: cardboard"),
         ("Maps", "two objects overlap", "the front one is smaller"),
         ("Seahorse", "object pair: key in front", "of a card"),
         ("Snapshot", "glass: rings, deep centre", "soft highlights"),
         ("Flatseal", "cylinder: big side face", "metal gradient"),
         ("Software", "an object that carries", "brand-like shapes"),
         ("Mousai", "Sound Disc done right:", "rim + recessed disc")]


def main():
    icons = {v["id"].split(".")[-1]: v for v in json.loads((LIB / "catalog.json").read_text())["icons"]}
    C, P = 200, 22
    f_t, f_h, f_s = load_font(26), load_font(16), load_font(15)
    img = Image.new("RGBA", (P + 4 * (C + P), 70 + 2 * (C + 92)), (250, 250, 249, 255))
    d = ImageDraw.Draw(img)
    d.text((P, 16), "Real GNOME app icons: objects, not logos on plates", font=f_t, fill=(36, 31, 49))
    for k, (name, l1, l2) in enumerate(PICKS):
        x, y = P + (k % 4) * (C + P), 64 + (k // 4) * (C + 92)
        img.alpha_composite(render_svg(str(LIB / icons[name]["file"]), C), (x, y))
        d.text((x, y + C + 4), name, font=f_h, fill=(36, 31, 49))
        d.text((x, y + C + 25), l1, font=f_s, fill=(94, 92, 100))
        d.text((x, y + C + 44), l2, font=f_s, fill=(119, 118, 123))
    img.save(Path(__file__).parent / "gnome-objects.png")
    print("wrote docs/redesign/gnome-objects.png")


if __name__ == "__main__":
    main()
