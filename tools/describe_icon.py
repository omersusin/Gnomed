#!/usr/bin/env python3
"""Describe an icon AS TEXT - for models that cannot see images.

    python3 tools/describe_icon.py work/<slug>/<slug>-symbol.svg
    python3 tools/describe_icon.py work/<slug>/source.png
    python3 tools/describe_icon.py <file> --ascii 24      # a finer ASCII preview

Prints, for a 128 x 128 canvas:
  - bounding box of the painted pixels, width/height, bottom edge (the baseline)
  - painted area (mass) and what REDESIGN.md 5 expects
  - the main colours with their nearest GNOME HIG name (e.g. "Blue 3 #3584e4")
  - holes: transparent areas fully enclosed by paint (letter counters, ring centres)
  - the gate's size rules as PASS/WARN lines (the real gate is tools/check_icon.py)
  - a coarse ASCII preview: '#' opaque, '+' half, '.' faint, ' ' transparent; 'o' = hole
You cannot judge beauty from this. Say so, and let the owner be the eye (START-HERE.md).
"""
import argparse
import io
import sys
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, label

HIG = {
    "Blue": ("#99c1f1", "#62a0ea", "#3584e4", "#1c71d8", "#1a5fb4"),
    "Green": ("#8ff0a4", "#57e389", "#33d17a", "#2ec27e", "#26a269"),
    "Yellow": ("#f9f06b", "#f8e45c", "#f6d32d", "#f5c211", "#e5a50a"),
    "Orange": ("#ffbe6f", "#ffa348", "#ff7800", "#e66100", "#c64600"),
    "Red": ("#f66151", "#ed333b", "#e01b24", "#c01c28", "#a51d2d"),
    "Purple": ("#dc8add", "#c061cb", "#9141ac", "#813d9c", "#613583"),
    "Brown": ("#cdab8f", "#b5835a", "#986a44", "#865e3c", "#63452c"),
    "Light": ("#ffffff", "#f6f5f4", "#deddda", "#c0bfbc", "#9a9996"),
    "Dark": ("#77767b", "#5e5c64", "#3d3846", "#241f31"),
}
PALETTE = [(f"{ramp} {i + 1}", h) for ramp, hs in HIG.items() for i, h in enumerate(hs)]


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def load(path, px=512):
    p = Path(path)
    if p.suffix.lower() == ".svg":
        data = cairosvg.svg2png(url=str(p), output_width=px, output_height=px)
        return np.array(Image.open(io.BytesIO(data)).convert("RGBA"))
    return np.array(Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS))


def nearest(c):
    best = min(PALETTE, key=lambda t: float(((rgb(t[1]) - c) ** 2).sum()))
    dist = float(np.sqrt(((rgb(best[1]) - c) ** 2).sum()))
    return best, dist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--ascii", type=int, default=16, help="ASCII preview width (default 16)")
    a = ap.parse_args()
    im = load(a.file)
    px = im.shape[0]
    k = px / 128.0
    alpha = im[..., 3] / 255.0
    paint = alpha > 0.5
    print(f"file: {a.file}   (canvas 128 x 128; numbers below are in that space)")
    if not paint.any():
        print("EMPTY: nothing is painted.")
        return
    # the box is measured like tools/size_audit.py: a 128 px copy, alpha > 40, last painted ROW
    a128 = np.asarray(Image.fromarray(im).resize((128, 128), Image.LANCZOS))[..., 3] > 40
    ys, xs = np.nonzero(a128)
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    w, h = x1 - x0 + 1, y1 - y0 + 1
    mass = float(alpha.mean())
    opaque_tile = mass > 0.9
    print(f"box: x {x0}..{x1}, y {y0}..{y1}  -> {w} wide x {h} tall, bottom row {y1} (the baseline)")
    print(f"painted area (mass): {mass:.2f}   (GNOME icons 0.44..0.69; below ~0.35 looks thin on a phone)")
    if opaque_tile:
        print("NOTE: the whole canvas is painted - this is a source/poster/tile, not a free GNOME object.")

    # colours: quantise the opaque pixels, report the main ones with HIG names
    px_rgb = im[..., :3][alpha > 0.9].reshape(-1, 3).astype(float)
    if len(px_rgb):
        q = (px_rgb // 24).astype(int)
        keys, inv, counts = np.unique(q, axis=0, return_inverse=True, return_counts=True)
        order = np.argsort(-counts)
        print("main colours (share of painted pixels -> nearest GNOME HIG colour):")
        shown = 0
        for idx in order:
            share = counts[idx] / len(px_rgb)
            if share < 0.03 or shown >= 7:
                break
            c = px_rgb[inv.ravel() == idx].mean(0)
            (name, hx), dist = nearest(c)
            hexc = "#%02x%02x%02x" % tuple(int(v) for v in c)
            near = "" if dist < 40 else "  (not close to any HIG colour)"
            print(f"  {share:5.0%}  {hexc}  ~ {name} {hx}{near}")
            shown += 1

    # holes: transparent pixels enclosed by paint
    holes = binary_fill_holes(paint) & ~paint
    lab, n = label(holes)
    big = [(lab == i).sum() for i in range(1, n + 1)]
    big = [b for b in big if b / paint.size >= 0.0005]
    if big:
        print(f"holes: {len(big)} transparent area(s) enclosed by paint, together {sum(big) / paint.size:.1%} of the canvas "
              f"(letter counters, eyes, a ring's centre - REDESIGN.md 5 wants them transparent)")
    else:
        print("holes: none transparent (no transparent area is enclosed by paint). Fine when the mark is printed ON")
        print("  an object (a label, stamp, page shows through its holes) - check_icon's 'holes' line says which.")
    if opaque_tile:
        print("  NOTE: a source tile has no transparency - its holes are painted in the tile colour. The MEASURED")
        print("  holes of a source are the 'holes' part of: python3 -c \"import sys; sys.path.insert(0,'work/_lib');"
              " from obj import describe; print(describe('<slug>'))\"")

    # the gate's size rules (REDESIGN.md 5) - indicative, tools/check_icon.py is the real gate
    print("size rules for a free object (REDESIGN.md 5; the pack-wide check is tools/size_audit.py):")
    print(f"  {'PASS' if 112 <= y1 <= 121 else 'FAIL'}  bottom row {y1} (size_audit allows 112..121; aim for 117..119)")
    print(f"  {'PASS' if max(w, h) >= 96 else 'FAIL'}  larger side {max(w, h)} (size_audit wants >= 96)")
    print(f"  {'PASS' if y0 >= 4 and x0 >= 4 and x1 <= 123 else 'FAIL'}  does not touch the edge (x {x0}..{x1}, top {y0}; keep 4..123)")
    print(f"  {'PASS' if mass >= 0.35 else 'WARN'}  painted area {mass:.2f} (check_icon WARNs below the GNOME range; < 0.35 looks thin)")

    # ASCII preview
    n_ = a.ascii
    step = px // n_
    print(f"ASCII {n_}x{n_} ('#' opaque, '+' half, '.' faint, 'o' hole, ' ' empty); each cell = {128 // n_} px:")
    for r in range(n_):
        row = ""
        for c in range(n_):
            cell = alpha[r * step:(r + 1) * step, c * step:(c + 1) * step].mean()
            hcell = holes[r * step:(r + 1) * step, c * step:(c + 1) * step].mean()
            row += "o" if hcell > 0.5 else "#" if cell > 0.75 else "+" if cell > 0.4 else "." if cell > 0.08 else " "
        print("  |" + row + "|")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        pass
