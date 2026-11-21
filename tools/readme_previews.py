#!/usr/bin/env python3
"""Pictures for the README and the app stores, made from the PNGs that are really in the pack
(nothing is drawn here, nothing is retouched). Run after the pack changed:

    python3 tools/readme_previews.py

writes
  docs/images/preview.png       every app icon of the Symbol style, light and dark halves
  docs/images/styles.png        the four styles (Faithful / Disc / Rimmed / Symbol) side by side
  fastlane/metadata/android/en-US/images/phoneScreenshots/<n>.jpg   a phone home screen per
      style on a Gnomed wallpaper: 1 Symbol, 2 Faithful, 3 Disc, 4 Rimmed (README shows them too)
  fastlane/metadata/android/en-US/images/icon.png                   (the app's own icon)

Order: redesigned apps (work/<slug>/redesign.py) first - they are the Gnomed look.
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NODPI = ROOT / "app/src/main/res/drawable-nodpi"
OUT = ROOT / "docs/images"
FASTLANE = ROOT / "fastlane/metadata/android/en-US/images"
STYLES = ("faithful", "disc", "rimmed", "symbol")
LIGHT, DARK = (246, 245, 244), (36, 31, 49)
ITEM_RE = re.compile(r'<item\s+component="(ComponentInfo\{[^"]+\})"\s+drawable="([^"]+)"')


def font(size, bold=False):
    for name in (("Inter-Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Inter-Regular.ttf", "DejaVuSans.ttf")):
        for d in (ROOT / "app/src/main/res/font", Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/share/fonts")):
            hits = list(d.rglob(name)) if d.exists() else []
            if hits:
                return ImageFont.truetype(str(hits[0]), size)
    return ImageFont.load_default()


def apps():
    """[(primary drawable, {style: png path})] for every app in the Faithful appfilter."""
    styles = json.loads((ROOT / "pack/styles.json").read_text())["icons"]
    seen, out = set(), []
    text = (ROOT / "app/src/main/res/xml/appfilter.xml").read_text()
    for comp, d in ITEM_RE.findall(text):
        if d in seen or not (NODPI / f"{d}.png").exists():
            continue
        seen.add(d)
        per = {}
        for st in STYLES:
            name = d if st == "faithful" else styles.get(d, {}).get(st, d)
            p = NODPI / f"{name}.png"
            per[st] = p if p.exists() else NODPI / f"{d}.png"
        out.append((d, per))
    redesigned = {p.parent.name for p in (ROOT / "work").glob("*/redesign.py")}
    # an app the owner wants redone (a redo: line, e.g. Kafa Topu 2 with characters) is not shown first
    redo = {p.parent.name for p in (ROOT / "work").glob("*/design.md")
            if re.search(r"^redo(-started)?:", p.read_text(encoding="utf-8"), re.M)}
    redesigned -= redo
    out.sort(key=lambda t: (t[0] not in redesigned, t[0] in redo, t[0]))
    return out, redesigned


def icon(path, size):
    return Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)


def preview(items):
    cols, cell, pad = 14, 92, 28
    rows = (len(items) + cols - 1) // cols
    W, Hh = cols * cell + 2 * pad, rows * cell + 2 * pad
    im = Image.new("RGB", (W, Hh * 2), LIGHT)
    ImageDraw.Draw(im).rectangle((0, Hh, W, Hh * 2), fill=DARK)
    for half in (0, 1):
        for i, (_, per) in enumerate(items):
            x = pad + (i % cols) * cell + 10
            y = half * Hh + pad + (i // cols) * cell + 10
            ic = icon(per["symbol"], 72)
            im.paste(ic, (x, y), ic)
    im.save(OUT / "preview.png", optimize=True)


def styles_sheet(items, redesigned, n=6):
    pick = [t for t in items if t[0] in redesigned][:n]
    cell, lw, top = 132, 0, 54
    W, H = len(STYLES) * cell * 2 + 40, top + len(pick) * cell + 20
    im = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    d.rectangle((W // 2, 0, W, H), fill=DARK)
    f = font(20, bold=True)
    for half in (0, 1):
        for j, st in enumerate(STYLES):
            x0 = 20 + half * (W // 2) + j * cell
            d.text((x0 + cell // 2, 24), st.capitalize(), font=f, anchor="mm",
                   fill=(36, 31, 49) if half == 0 else (246, 245, 244))
            for r, (_, per) in enumerate(pick):
                ic = icon(per[st], 104)
                im.paste(ic, (x0 + 14, top + r * cell + 10), ic)
    im.save(OUT / "styles.png", optimize=True)


def home(items, style, wallpaper, out):
    W, H = 1080, 2400
    wp = ROOT / "wallpapers" / wallpaper
    im = Image.open(wp).convert("RGB").resize((W, H)) if wp.exists() else Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(im)
    cols, rows, size = 4, 6, 168
    gx, gy = (W - cols * 230) // 2, 420
    f = font(30)
    pick = items[: cols * rows]
    for i, (name, per) in enumerate(pick):
        x = gx + (i % cols) * 230 + (230 - size) // 2
        y = gy + (i // cols) * 280
        ic = icon(per[style], size)
        im.paste(ic, (x, y), ic)
        label = name.replace("_", " ").title()
        label = label if len(label) <= 13 else label[:12] + "…"
        d.text((x + size // 2 + 2, y + size + 34), label, font=f, anchor="mm", fill=(0, 0, 0))
        d.text((x + size // 2, y + size + 32), label, font=f, anchor="mm", fill=(255, 255, 255))
    d.text((W // 2, 200), f"Gnomed · {style.capitalize()}", font=font(64, bold=True), anchor="mm", fill=(255, 255, 255))
    im.save(out, quality=88, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    items, redesigned = apps()
    preview(items)
    styles_sheet(items, redesigned)
    shots = FASTLANE / "phoneScreenshots"
    shots.mkdir(parents=True, exist_ok=True)
    walls = {"symbol": "gnomed-dusk-1080x2400.jpg", "faithful": "gnomed-dark-1080x2400.jpg",
             "disc": "gnomed-graphite-1080x2400.jpg", "rimmed": "gnomed-lavender-1080x2400.jpg"}
    for n, st in enumerate(("symbol", "faithful", "disc", "rimmed"), 1):
        home(items, st, walls[st], shots / f"{n}.jpg")          # README shows these too
    launcher = ROOT / "app/src/main/res/mipmap-xxxhdpi/ic_launcher.png"
    if launcher.exists():
        Image.open(launcher).convert("RGBA").resize((512, 512), Image.LANCZOS).save(FASTLANE / "icon.png")
    print(f"wrote docs/images/ (preview, styles) and fastlane images - {len(items)} apps, "
          f"{len(redesigned & {n for n, _ in items})} redesigned")


if __name__ == "__main__":
    sys.exit(main())
