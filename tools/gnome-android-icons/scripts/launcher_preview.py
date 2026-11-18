#!/usr/bin/env python3
"""Android home-screen preview: icons at real launcher size, with labels, on
light / dark / colourful wallpapers - optionally also as launchers show them
when "force icon shape" / "wrap non-adaptive icons" is ON.

Real-size math (default POCO F5-like phone): 1080 x 2400 px, density 2.75
(440 dpi); launcher icon 54 dp -> ~149 px; folder preview icons are ~1/3 of
that (~50 px) - which is why the 32/48 px checks still matter on a phone.

Usage:
  launcher_preview.py ICON.svg[:Label] [ICON2.png[:Label] ...] --out work/app/launcher.png
      [--refs 8] [--shape none|circle|squircle|rounded|all] [--icon-dp 54] [--density 2.75] [--cols 4]

--refs N   fills the grid with N real GNOME icons from the bundled library so the
           candidates are judged next to the family they must belong to.
"""
import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg, load_font, LIB_ROOT  # noqa: E402

W, H = 1080, 2400
WALLS = {
    "light": [(0, (246, 245, 244)), (1, (222, 221, 218))],
    "dark": [(0, (61, 56, 70)), (1, (36, 31, 49))],
    "colour": [(0, (26, 95, 180)), (0.55, (145, 65, 172)), (1, (230, 97, 0))],
}


def wallpaper(kind):
    stops = WALLS[kind]
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0) if t1 > t0 else 0
                col = tuple(int(c0[i] + (c1[i] - c0[i]) * u) for i in range(3))
                break
        for x in range(0, W, 1):
            px[x, y] = col
    if kind == "colour":  # soft blobs so it looks like a real wallpaper, not a flat gradient
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.ellipse([-200, 300, 700, 1200], fill=(255, 190, 111, 90))
        d.ellipse([500, 1400, 1400, 2300], fill=(87, 227, 137, 70))
        im = Image.alpha_composite(im.convert("RGBA"), ov.filter(ImageFilter.GaussianBlur(120))).convert("RGB")
    return im


def load_icon(spec, size):
    path, _, label = spec.partition(":") if not spec.lower().startswith(("c:", "d:")) else (spec, "", "")
    p = Path(path)
    if p.suffix.lower() == ".svg":
        im = render_svg(p, size)
    else:
        im = Image.open(p).convert("RGBA").resize((size, size), Image.LANCZOS)
    return im, (label or p.stem.replace("_", " ").replace("-", " ")[:14])


def shape_wrap(icon, size, shape):
    """What launchers do with non-adaptive icons when a shape is forced:
    white shape behind, icon scaled down to fit."""
    if shape == "none":
        return icon
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    if shape == "circle":
        d.ellipse([0, 0, size - 1, size - 1], fill=255)
    elif shape == "rounded":
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
    else:  # squircle (superellipse n=4)
        n, r = 4.0, size / 2
        pts = []
        for k in range(360):
            t = math.radians(k)
            c, s = math.cos(t), math.sin(t)
            x = r + r * math.copysign(abs(c) ** (2 / n), c)
            y = r + r * math.copysign(abs(s) ** (2 / n), s)
            pts.append((x, y))
        d.polygon(pts, fill=255)
    white = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    base.paste(white, (0, 0), m)
    inner = icon.resize((int(size * 0.72), int(size * 0.72)), Image.LANCZOS)
    o = (size - inner.width) // 2
    base.alpha_composite(inner, (o, o))
    return base


def phone(icons, kind, shape, icon_px, cols, font, full=False):
    im = wallpaper(kind).convert("RGBA")
    d = ImageDraw.Draw(im)
    light = kind == "light"
    cell_w = W // cols
    top = 260
    row_h = icon_px + 110
    dock = icons[-cols:] if len(icons) > cols * 2 else []
    grid = icons[: len(icons) - len(dock)]
    for i, (ic, label) in enumerate(grid):
        r, c = divmod(i, cols)
        x = c * cell_w + (cell_w - icon_px) // 2
        y = top + r * row_h
        im.alpha_composite(shape_wrap(ic, icon_px, shape), (x, y))
        tw = d.textlength(label, font=font)
        tx, ty = c * cell_w + (cell_w - tw) / 2, y + icon_px + 16
        if light:
            d.text((tx, ty), label, fill=(46, 52, 54), font=font)
        else:
            d.text((tx + 2, ty + 2), label, fill=(0, 0, 0, 140), font=font)
            d.text((tx, ty), label, fill=(255, 255, 255), font=font)
    if dock:
        y = H - icon_px - 170
        bar = Image.new("RGBA", (W - 80, icon_px + 70), (255, 255, 255, 60 if not light else 110))
        im.alpha_composite(bar, (40, y - 35))
        for c, (ic, _) in enumerate(dock):
            x = c * cell_w + (cell_w - icon_px) // 2
            im.alpha_composite(shape_wrap(ic, icon_px, shape), (x, y))
    # status bar line, nothing more (this is a review tool, not a mockup)
    d.text((60, 60), "12:00", fill=(46, 52, 54) if light else (255, 255, 255), font=font)
    im = im.convert("RGB")
    if full or not dock:
        return im
    # compact: cut the empty wallpaper between the grid and the dock
    rows_used = (len(grid) + cols - 1) // cols
    grid_bottom = min(H, top + rows_used * row_h + 40)
    dock_top = H - icon_px - 240
    if dock_top <= grid_bottom:
        return im
    out = Image.new("RGB", (W, grid_bottom + (H - dock_top) + 12), (255, 255, 255))
    out.paste(im.crop((0, 0, W, grid_bottom)), (0, 0))
    out.paste(im.crop((0, dock_top, W, H)), (0, grid_bottom + 12))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("icons", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--refs", type=int, default=8)
    ap.add_argument("--shape", default="none", choices=["none", "circle", "squircle", "rounded", "all"])
    ap.add_argument("--icon-dp", type=float, default=54)
    ap.add_argument("--density", type=float, default=2.75)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--full", action="store_true", help="show the whole screen height (default: cut empty wallpaper)")
    a = ap.parse_args()
    px = int(round(a.icon_dp * a.density))
    font = load_font(int(13 * a.density))
    cand = [load_icon(s, px) for s in a.icons]
    refs = []
    if a.refs:
        cat = [e for e in json.loads((LIB_ROOT / "catalog.json").read_text())["icons"] if e["group"] != "adwaita-system"]
        step = max(1, len(cat) // a.refs)
        for e in cat[3::step][: a.refs]:
            refs.append((render_svg(LIB_ROOT / e["file"], px), e["id"].split(".")[-1][:12]))
    # interleave: candidates spread between references
    items = []
    k = 0
    for i in range(len(cand) + len(refs)):
        if k < len(cand) and (i % 3 == 1 or not refs):
            items.append(cand[k])
            k += 1
        elif refs:
            items.append(refs.pop(0))
    items += cand[k:] + refs
    shapes = ["none", "circle", "squircle"] if a.shape == "all" else [a.shape]
    rows = []
    for sh in shapes:
        phones = [phone(items, kind, sh, px, a.cols, font, a.full) for kind in ("light", "dark", "colour")]
        ph = max(p.height for p in phones)
        row = Image.new("RGB", (W * 3 + 80, ph + 120), (255, 255, 255))
        for i, p in enumerate(phones):
            row.paste(p, (20 + i * (W + 20), 100))
        ImageDraw.Draw(row).text((30, 30), f"forced shape: {sh}  |  icon {a.icon_dp:g} dp x {a.density:g} = {px} px on 1080 x 2400",
                                 fill=(30, 30, 30), font=load_font(44))
        rows.append(row)
    out = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (255, 255, 255))
    y = 0
    for r in rows:
        out.paste(r, (0, y))
        y += r.height
    out = out.resize((out.width // 2, out.height // 2), Image.LANCZOS)  # viewable size
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
