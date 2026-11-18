#!/usr/bin/env python3
"""Where did the measurement change the source's colours?

    python3 tools/region_check.py [<slug> ...]      (default: every automatic app)

Redraws the measured ground (flat or gradient) and every measured region of
work/<slug>/geometry.json in the source's own coordinates and compares it pixel by
pixel with work/<slug>/source.png (dE in Lab). A blob of >= 1.5% of the tile whose
colour differs (dE > 6) means a part of the icon was lost into the background or
got a wrong colour (e.g. SD Maid's dark apron read as tile) -> prints the source
colour, where it is and how big. Exit 1 if any app has such a blob.
"""
import io
import json
import sys
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.color import rgb2lab

ROOT = Path(__file__).resolve().parent.parent
N = 256


def recon_svg(g):
    gr = g["info"].get("ground") or {}
    defs, bg = "", ""
    if gr.get("kind") == "flat":
        bg = f'<rect width="128" height="128" fill="{gr["color"]}"/>'
    elif gr.get("kind") == "gradient":
        (x0, y0), (x1, y1) = gr["p0"], gr["p1"]
        defs = (f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}">'
                f'<stop offset="0" stop-color="{gr["c0"]}"/><stop offset="1" stop-color="{gr["c1"]}"/></linearGradient></defs>')
        bg = '<rect width="128" height="128" fill="url(#g)"/>'
    paths = "".join(f'<path d="{g["parts"][r["name"]]["d"]}" fill="{r["fill"]}" fill-rule="evenodd"/>'
                    for r in sorted(g["info"]["regions"], key=lambda r: -r["area"]) if r["name"] in g["parts"])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{N}" height="{N}">{defs}{bg}{paths}</svg>'


def check(slug):
    gp, sp = ROOT / f"work/{slug}/geometry.json", ROOT / f"work/{slug}/source.png"
    if not (gp.exists() and sp.exists()):
        return []
    g = json.loads(gp.read_text())
    if not (g["info"].get("ground") or {}).get("kind") in ("flat", "gradient"):
        return []
    rec = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=recon_svg(g).encode()))).convert("RGBA")).astype(float) / 255
    src = np.asarray(Image.open(sp).convert("RGBA").resize((N, N), Image.LANCZOS)).astype(float) / 255
    op = src[..., 3] > 0.95
    dE = np.linalg.norm(rgb2lab(src[..., :3]) - rgb2lab(rec[..., :3]), axis=-1)
    bad = ndimage.binary_opening((dE > 6) & op, iterations=2)
    lbl, n = ndimage.label(bad)
    out = []
    for i in range(1, n + 1):
        m = lbl == i
        if m.mean() < 0.015:
            continue
        ys, xs = np.where(m)
        c = np.median(src[m][:, :3], axis=0)
        r = np.median(rec[m][:, :3], axis=0)
        h = lambda v: "#%02x%02x%02x" % tuple(int(round(x * 255)) for x in v)
        out.append(f"source {h(c)} drawn as {h(r)}: {m.mean():.1%} of tile at x{xs.min() // 2}-{xs.max() // 2} y{ys.min() // 2}-{ys.max() // 2}")
    return out


def main():
    slugs = sys.argv[1:] or sorted(p.parent.name for p in (ROOT / "work").glob("*/geometry.json"))
    bad = 0
    for s in slugs:
        for p in check(s):
            print(f"{s:28s} {p}")
            bad += 1
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
