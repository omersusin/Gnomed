#!/usr/bin/env python3
"""Regenerate every figure of the course from the project's own data.

    python3 docs/course/make_figures.py

"Before" images are REAL: the same app built with the recipe switched off.
"""
import copy
import io
import json
import sys
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
IMG = Path(__file__).resolve().parent / "img"
IMG.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "work/_lib"))
import build_auto as ba  # noqa: E402
import fam  # noqa: E402
from fam import gk  # noqa: E402

try:
    FONT = ImageFont.truetype("DejaVuSans.ttf", 22)
    FONT_S = ImageFont.truetype("DejaVuSans.ttf", 17)
    FONT_B = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
except OSError:
    FONT = FONT_S = FONT_B = ImageFont.load_default()

LIGHT, DARK = (246, 245, 244, 255), (36, 31, 49, 255)


def svg_img(svg, size):
    data = svg if isinstance(svg, str) and svg.lstrip().startswith("<") else None
    png = cairosvg.svg2png(bytestring=data.encode(), output_width=size, output_height=size) if data else \
        cairosvg.svg2png(url=str(svg), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def tile(img, bg, pad=12):
    t = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    t.alpha_composite(img, (pad, pad))
    return t


def caption(img, text, color=(20, 20, 20), h=40, font=None):
    c = Image.new("RGBA", (img.width, img.height + h), (255, 255, 255, 255))
    c.alpha_composite(img, (0, 0))
    ImageDraw.Draw(c).text((8, img.height + 8), text, fill=color, font=font or FONT)
    return c


def hstack(imgs, gap=16, bg=(255, 255, 255, 255)):
    w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    h = max(i.height for i in imgs)
    out = Image.new("RGBA", (w, h), bg)
    x = 0
    for i in imgs:
        out.alpha_composite(i, (x, 0))
        x += i.width + gap
    return out


def vstack(imgs, gap=16, bg=(255, 255, 255, 255)):
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGBA", (w, h), bg)
    y = 0
    for i in imgs:
        out.alpha_composite(i, (0, y))
        y += i.height + gap
    return out


def build_variant(slug, style, override):
    """build `style` of `slug` with OVERRIDES[slug] replaced by `override` -> svg string"""
    saved = copy.deepcopy(ba.OVERRIDES.get(slug))
    ba.OVERRIDES[slug] = override
    try:
        app = ba.App(slug)
        return getattr(app, style)().svg()
    finally:
        if saved is None:
            ba.OVERRIDES.pop(slug, None)
        else:
            ba.OVERRIDES[slug] = saved


def pair(slug, style, before, title, why_bad, why_good, size=200, after_svg=None):
    """BEFORE (recipe off) | AFTER (as shipped), each on light and dark"""
    b = svg_img(before, size)
    a = svg_img(after_svg or ROOT / f"work/{slug}/{slug}-{style}.svg", size)
    src = Image.open(ROOT / f"work/{slug}/source.png").convert("RGBA").resize((size, size))
    cols = [caption(vstack([tile(src, LIGHT)], 0), "source"),
            caption(hstack([tile(b, LIGHT), tile(b, DARK)], 0), "BEFORE - " + why_bad, (190, 20, 20)),
            caption(hstack([tile(a, LIGHT), tile(a, DARK)], 0), "AFTER - " + why_good, (20, 120, 40))]
    head = Image.new("RGBA", (10, 44), (255, 255, 255, 255))
    body = hstack(cols, 24)
    out = Image.new("RGBA", (body.width, body.height + 44), (255, 255, 255, 255))
    ImageDraw.Draw(out).text((8, 8), title, fill=(0, 0, 0), font=FONT_B)
    out.alpha_composite(body, (0, 44))
    del head
    return out


def save(img, name):
    img.convert("RGB").save(IMG / name, optimize=True)
    print("img/" + name)


# ------------------------------------------------------------------ 1. anatomy
def anatomy():
    S = 640
    ic = svg_img(ROOT / "work/bitwarden/bitwarden-faithful.svg", S)
    canvas = Image.new("RGBA", (S + 520, S + 40), (255, 255, 255, 255))
    canvas.alpha_composite(tile(ic, LIGHT, 20), (0, 0))
    d = ImageDraw.Draw(canvas)
    k = S / 128.0
    o = 20

    def arrow(px, py, tx, ty, text):
        X, Y = o + px * k, o + py * k
        d.line([(X, Y), (tx, ty)], fill=(200, 30, 30), width=3)
        d.ellipse([X - 6, Y - 6, X + 6, Y + 6], outline=(200, 30, 30), width=3)
        d.text((tx + 8, ty - 14), text, fill=(0, 0, 0), font=FONT)

    arrow(20, 40, S + 60, 60, "FACE: the plate, flat brand colour\n(square template 104x104, r8)")
    arrow(64, 114.5, S + 60, 230, "CHIN: same shape moved 4 px down,\ndarker; horizontal gradient with\nhighlights only at round corners")
    arrow(50, 60, S + 60, 360, "MARK: the app's own shape\n(measured from the source)")
    arrow(86.5, 73, S + 60, 470, "LIFT: the mark's own side, 2 px down\n(#deddda under white) - not a shadow")
    arrow(74, 60, S + 60, 580, "NEGATIVE SPACE kept: this hole is\nidentity (its inner wall shows at its top)")
    save(canvas, "01-anatomy.png")


# ------------------------------------------------------------------ 2. styles
def styles():
    rows = []
    for slug in ("bitwarden", "discord", "youtube"):
        cells = [caption(tile(Image.open(ROOT / f"work/{slug}/source.png").convert("RGBA").resize((170, 170)), LIGHT), "source")]
        for st, lab in (("faithful", "Faithful"), ("disc", "Disc"), ("rimmed", "Rimmed"), ("symbol", "Symbol")):
            p = ROOT / f"work/{slug}/{slug}-{st}.svg"
            if p.exists():
                im = svg_img(p, 170)
                cells.append(caption(hstack([tile(im, LIGHT), tile(im, DARK)], 0), lab))
        rows.append(hstack(cells, 18))
    save(vstack(rows, 20), "02-four-styles.png")


# ------------------------------------------------------------------ 3. pipeline
def pipeline():
    import gtrace as gt
    slug = "discord"
    a, s = gt.load(ROOT / f"work/{slug}")
    g = json.loads((ROOT / f"work/{slug}/geometry.json").read_text())
    src = Image.open(ROOT / f"work/{slug}/source.png").convert("RGBA").resize((220, 220))
    # mark mask
    m = np.zeros((a.shape[0], a.shape[1], 4), np.uint8)
    w = (a[..., :3].min(-1) > 0.85)
    m[w] = (30, 30, 30, 255)
    m[~w] = (255, 255, 255, 255)
    mask = Image.fromarray(m).resize((220, 220))
    # traced path drawn as outline
    d = g["parts"]["r0"]["d"]
    outline = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><rect width="128" height="128" fill="#fff"/><path d="{d}" fill="#e0e7ff" stroke="#c01c28" stroke-width="0.8" fill-rule="evenodd"/></svg>'
    tr = svg_img(outline, 220)
    built = svg_img(ROOT / f"work/{slug}/{slug}-faithful.svg", 220)
    steps = [caption(src, "1 source.png"), caption(mask, "2 mark mask"), caption(tr, "3 traced path"),
             caption(tile(built, LIGHT, 0), "4 GNOME build")]
    save(hstack(steps, 30), "03-pipeline.png")


# ------------------------------------------------------------------ 4. recipes (before/after)
def recipes():
    ov = ba.OVERRIDES
    figs = [
        ("R1-stripes.png", "exteraless", "symbol", {k: v for k, v in ov["exteraless"].items() if k != "merge_grad"},
         "R1  One gradient cut into stripes  ->  merge_grad", "stripes of flat colour", "one fitted gradient"),
        ("R2-tile-decoration.png", "anker_soundcore", "faithful", {}, "R2  Tile decoration taken as mark  ->  only_white / drop",
         "photo waves traced", "white wordmark only"),
        ("R3-glow.png", "exteraless", "faithful", {"light": True}, "R3  Glow / soft shadow taken as mark  ->  drop",
         "pink glow blob", "glow dropped"),
        ("R4-box-in-plate.png", "plush_iconpack", "faithful", {}, "R4  The app's own tile drawn inside the plate  ->  face + drop",
         "squircle in a plate", "the tile IS the plate"),
        ("R5-pale-tile.png", "pentas", "faithful", {}, "R5  A pale tile colour lost (became white)  ->  keep_ground",
         "peach became white", "peach kept"),
        ("R6-vanishing-symbol.png", "recon", "symbol", {}, "R6  Symbol vanishes on one wallpaper  ->  symbol: margin",
         "white brackets vanish on light", "tile-coloured margin"),
        ("R6b-reddit-symbol.png", "reddit", "symbol", {}, "R6b  Inversion is wrong for this logo  ->  symbol: margin",
         "orange Snoo", "white Snoo, orange margin"),
        ("R8-wrong-ground.png", "enpara", "faithful", {}, "R8  Ground misread (white tile seen as grey gradient)  ->  light",
         "grey gradient plate", "white plate"),
        ("R8b-flat-ground.png", "vortex", "symbol", {}, "R8b  Mark touching the edge skews the tile fit  ->  flat + face + drop",
         "black wedge in the mark", "clean spiral"),
    ]
    for name, slug, st, off, title, bad, good in figs:
        try:
            before = build_variant(slug, st, off)
            save(pair(slug, st, before, title, bad, good), name)
        except Exception as e:  # keep going; report
            print("skip", name, e)


def chatgpt_inverted():
    """the real ChatGPT mistake: only the black lines, shown white on dark"""
    P, _ = fam.geo("chatgpt")
    ic = gk.Icon("bad", "")
    fam.disc(ic, "#241f31", top_light=0.5)
    ds, _ = fam.place([P["knot"]], fam.box_c(64, 63, 86))
    fam.raised(ic, [(ds[0], "#ffffff", "#9a9996")], lift=1.5)
    save(pair("chatgpt", "disc", ic.svg(), "R13  Figure and ground swapped (ChatGPT)  ->  check what is the object",
              "lines only: logo inverted", "white strands + dark lines"), "R13-figure-ground.png")


def gate_example():
    import subprocess
    out = subprocess.run([sys.executable, str(ROOT / "tools/check_icon.py"), "recon"], capture_output=True, text=True).stdout
    (IMG.parent / "examples").mkdir(exist_ok=True)
    (IMG.parent / "examples/check_icon_recon.txt").write_text(out)
    print("examples/check_icon_recon.txt")


if __name__ == "__main__":
    anatomy()
    styles()
    pipeline()
    recipes()
    chatgpt_inverted()
    gate_example()
