#!/usr/bin/env python3
"""Render many SVG icons into one labelled contact sheet (PNG).

Usage:
  contact_sheet.py OUT.png ICON.svg [ICON.svg ...] [--size 96] [--cols 8]
                   [--bg light|dark|both] [--title "text"]

Used to study the bundled GNOME reference library side by side and to put a
new icon next to its references.  Pure rasterisation; nothing is generated.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg, load_font  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

BGS = {"light": (250, 250, 250), "dark": (36, 31, 49)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("icons", nargs="+")
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--bg", choices=["light", "dark", "both"], default="light")
    ap.add_argument("--title", default="")
    ap.add_argument("--label-chars", type=int, default=18)
    a = ap.parse_args()

    icons = [p for p in a.icons if p.lower().endswith(".svg")]
    bgs = ["light", "dark"] if a.bg == "both" else [a.bg]
    s, pad, lab = a.size, 14, 30
    cell_w, cell_h = s + pad * 2, s * len(bgs) + pad * 2 + lab
    rows = (len(icons) + a.cols - 1) // a.cols
    top = 40 if a.title else 0
    sheet = Image.new("RGB", (cell_w * a.cols, cell_h * rows + top), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    font, tfont = load_font(11), load_font(18)
    if a.title:
        d.text((10, 10), a.title, fill=(30, 30, 30), font=tfont)
    for i, p in enumerate(icons):
        r, c = divmod(i, a.cols)
        x0, y0 = c * cell_w, r * cell_h + top
        for j, bg in enumerate(bgs):
            yb = y0 + pad + j * s
            d.rectangle([x0 + pad - 4, yb, x0 + pad + s + 4, yb + s], fill=BGS[bg])
            try:
                im = render_svg(p, s)
                sheet.paste(im, (x0 + pad, yb), im)
            except Exception as exc:  # keep going, mark failure
                d.text((x0 + pad, yb + s // 2), "render fail", fill=(200, 0, 0), font=font)
                print(f"render failed: {p}: {exc}", file=sys.stderr)
        name = Path(p).stem
        for k, line in enumerate([name[:a.label_chars], name[a.label_chars:a.label_chars * 2]]):
            if line:
                d.text((x0 + 6, y0 + pad + s * len(bgs) + 3 + k * 12), line, fill=(60, 60, 60), font=font)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
