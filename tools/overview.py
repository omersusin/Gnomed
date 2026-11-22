#!/usr/bin/env python3
"""One picture of several apps in all four styles - for the owner's batch review (docs/BATCH.md).

    python3 tools/overview.py <slug> <slug> ... --out ~/Downloads/gnomed/overview-1.png

One row per app, columns Symbol / Faithful / Disc / Rimmed, the light wallpaper on the left and
the dark one on the right. It shows the NEW builds (work/<slug>/<slug>-<style>.svg); an app
without a build is shown with its current pack PNG and marked "(pack)". A style that repeats
another style's design is marked "=" under it (the owner wants four different designs).
"""
import io
import json
import sys
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
STYLES = ("symbol", "faithful", "disc", "rimmed")
NODPI = ROOT / "app/src/main/res/drawable-nodpi"


def font(size, bold=False):
    for d in (ROOT / "app/src/main/res/font", Path("/usr/share/fonts")):
        for name in (("bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("regular.ttf", "DejaVuSans.ttf")):
            hits = list(d.rglob(name)) if d.exists() else []
            if hits:
                return ImageFont.truetype(str(hits[0]), size)
    return ImageFont.load_default()


def icons(slug):
    """-> ({style: (RGBA image, bytes key)}, from_pack)"""
    w = ROOT / "work" / slug
    out = {}
    for st in STYLES:
        svg = w / f"{slug}-{st}.svg"
        if svg.exists():
            data = svg.read_bytes()
            png = cairosvg.svg2png(bytestring=data, output_width=128, output_height=128)
            out[st] = (Image.open(io.BytesIO(png)).convert("RGBA"), data)
    if out:
        return out, False
    styles = json.loads((ROOT / "pack/styles.json").read_text()).get("icons", {})
    for st in STYLES:
        name = slug if st == "faithful" else styles.get(slug, {}).get(st, slug)
        p = NODPI / f"{name}.png"
        if p.exists():
            out[st] = (Image.open(p).convert("RGBA").resize((128, 128), Image.LANCZOS), p.read_bytes())
    return out, True


def main():
    argv = sys.argv[1:]
    out = Path(argv[argv.index("--out") + 1]).expanduser() if "--out" in argv else ROOT / "overview.png"
    slugs = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--out")]
    if not slugs:
        sys.exit(__doc__)
    cell, lw, top = 150, 190, 54
    half = cell * 4 + 12
    W, H = lw + 2 * half + 10, top + cell * len(slugs) + 10
    im = Image.new("RGB", (W, H), (246, 245, 244))
    d = ImageDraw.Draw(im)
    d.rectangle((lw + half, 0, W, H), fill=(36, 31, 49))
    fb, fr, fs = font(19, True), font(17), font(14)
    for h in (0, 1):
        for j, st in enumerate(STYLES):
            d.text((lw + h * half + j * cell + cell // 2, 26), st.capitalize(), font=fb, anchor="mm",
                   fill=(36, 31, 49) if h == 0 else (246, 245, 244))
    for i, slug in enumerate(slugs):
        y = top + i * cell
        got, from_pack = icons(slug)
        d.text((12, y + cell // 2 - 10), slug, font=fr, anchor="lm", fill=(36, 31, 49))
        if from_pack:
            d.text((12, y + cell // 2 + 14), "(pack - not rebuilt)", font=fs, anchor="lm", fill=(192, 28, 40))
        seen = {}
        for j, st in enumerate(STYLES):
            if st not in got:
                continue
            ic, key = got[st]
            for h in (0, 1):
                x = lw + h * half + j * cell + 11
                im.paste(ic, (x, y + 6), ic)
                if key in seen:
                    d.text((x + 64, y + cell - 12), f"= {seen[key]}", font=fs, anchor="mm",
                           fill=(192, 28, 40) if h == 0 else (246, 97, 81))
            seen.setdefault(key, st)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print(f"wrote {out} ({len(slugs)} apps)")


if __name__ == "__main__":
    main()
