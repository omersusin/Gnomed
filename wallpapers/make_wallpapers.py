#!/usr/bin/env python3
"""Gnomed wallpapers - calm, low-contrast backdrops for the icon pack (code-drawn SVG,
no image-generation model). Motifs live only in the top and bottom bands; the middle,
where the icon grid sits, stays a plain soft gradient so every icon reads.

    python3 wallpapers/make_wallpapers.py

Writes wallpapers/<name>.svg, grained JPEGs 1080x2400 / 1440x3200, thumbs/<name>.jpg
(360x800) and wallpapers.json. Nothing is embedded in the APK: the app reads
wallpapers.json from the repository's main branch (res/values/dashboard_configurations.xml
-> wallpaper_json) and loads the images from there, so new wallpapers need no app update.
"""
import json
import math
from pathlib import Path

import cairosvg
from PIL import Image

HERE = Path(__file__).resolve().parent
# where the app downloads from (raw files of the main branch)
RAW = "https://raw.githubusercontent.com/omersusin/Gnomed/main/wallpapers"
W, H = 1080, 2400


def wave(y, amp, phase, down, n=3):
    pts = [(W * i / n, y + amp * ((-1) ** (i + phase)) * 0.5) for i in range(n + 1)]
    d = f"M0 {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cx = (x0 + x1) / 2
        d += f" C{cx:.0f} {y0:.0f} {cx:.0f} {y1:.0f} {x1:.0f} {y1:.0f}"
    e = H if down else 0
    return d + f" L{W} {e} L0 {e} Z"


def hill(cx, top, half_w):
    """a single soft hill rising from the bottom edge"""
    return (f"M{cx - half_w:.0f} {H} C{cx - half_w * 0.45:.0f} {top:.0f} {cx + half_w * 0.45:.0f} {top:.0f} "
            f"{cx + half_w:.0f} {H} Z")


def arcs(cx, cy, radii):
    return [f"M{cx - r:.0f} {cy:.0f} A{r:.0f} {r:.0f} 0 0 1 {cx + r:.0f} {cy:.0f} A{r:.0f} {r:.0f} 0 0 1 {cx - r:.0f} {cy:.0f} Z"
            for r in radii]


def plane(y_left, y_right, down):
    e = H if down else 0
    return f"M0 {y_left:.0f} L{W} {y_right:.0f} L{W} {e} L0 {e} Z"


def svg(top, bottom, shapes):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            + "".join(f'<path d="{d}" fill="{c}"/>' for d, c in shapes) + "</svg>")


def waves(top, bottom, tb, bb):
    return svg(top, bottom, [(wave(y, a, i, False), c) for i, (y, a, c) in enumerate(tb)]
               + [(wave(y, a, i + 1, True), c) for i, (y, a, c) in enumerate(bb)])


VARIANTS = {
    "gnomed-light": ("Adwaita Light", waves("#eef2f7", "#d8e2ec",
                     [(330, 70, "#e3eaf2"), (210, 60, "#dae4ee")],
                     [(1980, 70, "#cfdbe7"), (2120, 60, "#c3d2e1"), (2260, 50, "#b7c9da")])),
    "gnomed-dark": ("Adwaita Dark", waves("#2b303b", "#1c2028",
                    [(330, 70, "#303644"), (210, 60, "#353c4b")],
                    [(1980, 70, "#232833"), (2120, 60, "#272d39"), (2260, 50, "#2c3340")])),
    "gnomed-sand": ("Sand Hills", svg("#f7f2eb", "#ece2d4", [
        (hill(260, 1900, 620), "#e4d6c3"), (hill(860, 1960, 560), "#dccbb4"), (hill(520, 2080, 700), "#d2bea4")])),
    "gnomed-sage": ("Sage Rings", svg("#eef3ed", "#dde7dc",
        [(d, c) for d, c in zip(arcs(W, H, [760, 600, 440]), ["#d6e2d5", "#cbdbca", "#c0d3bf"])]
        + [(d, c) for d, c in zip(arcs(0, 0, [420, 290]), ["#e6eee5", "#dfe9de"])])),
    "gnomed-lavender": ("Lavender Planes", svg("#f3f0f9", "#e3ddf1", [
        (plane(2000, 1840, True), "#dcd4ee"), (plane(2120, 2010, True), "#d2c8e8"), (plane(2260, 2190, True), "#c8bce2"),
        (plane(300, 420, False), "#ebe6f5")])),
    "gnomed-dusk": ("Dusk Hills", svg("#2f2b4d", "#1b1930", [
        (hill(260, 1880, 620), "#26233f"), (hill(860, 1950, 560), "#2a2746"), (hill(520, 2080, 700), "#312d52")])),
    "gnomed-ocean": ("Ocean Rings", svg("#213241", "#121d27",
        [(d, c) for d, c in zip(arcs(W, H, [760, 600, 440]), ["#182633", "#1c2c3a", "#213343"])]
        + [(d, c) for d, c in zip(arcs(0, 0, [420, 290]), ["#26394a", "#2a4052"])])),
    "gnomed-graphite": ("Graphite Planes", svg("#323238", "#1f1f24", [
        (plane(2000, 1840, True), "#28282e"), (plane(2120, 2010, True), "#2c2c33"), (plane(2260, 2190, True), "#313139"),
        (plane(300, 420, False), "#38383f")])),
}

def grain(png_path, out_path, size=None, sigma=1.6, seed=0, quality=92):
    """Fine monochrome film grain (gaussian, ~1.6 of 255 levels): breaks the 8-bit steps of
    the soft gradients (banding) without being visible as texture. JPEG, because grain does
    not compress in PNG."""
    import numpy as np
    im = Image.open(png_path).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    n = np.random.default_rng(seed).normal(0, sigma, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a + n, 0, 255).round().astype(np.uint8)).save(out_path, quality=quality, subsampling=0)


if __name__ == "__main__":
    (HERE / "thumbs").mkdir(exist_ok=True)
    index = []
    for name, (title, s) in VARIANTS.items():
        (HERE / f"{name}.svg").write_text(s)
        big = HERE / f".{name}-3200.png"
        cairosvg.svg2png(bytestring=s.encode(), write_to=str(big), output_width=1440, output_height=3200)
        grain(big, HERE / f"{name}-1440x3200.jpg")
        grain(big, HERE / f"{name}-1080x2400.jpg", size=(1080, 2400), seed=1)
        big.unlink()
        # small JPEG thumb for the app's wallpaper grid
        Image.open(HERE / f"{name}-1080x2400.jpg").resize((360, 800), Image.LANCZOS).save(
            HERE / f"thumbs/{name}.jpg", quality=88)
        index.append({"name": title, "author": "Gnomed",
                      "url": f"{RAW}/{name}-1440x3200.jpg", "thumbUrl": f"{RAW}/thumbs/{name}.jpg"})
        print(name)
    (HERE / "wallpapers.json").write_text(json.dumps(index, indent=1) + "\n")
