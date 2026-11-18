#!/usr/bin/env python3
"""Measure an extracted source icon (transparent PNG) and draft its identity sheet.

Reports, as JSON + readable text:
  silhouette   : bbox aspect, fill ratio, circularity, best-matching GNOME template
                 shape (circle / square / portrait / landscape / free)
  symmetry     : left-right mirror IoU of the alpha mask
  colours      : dominant colours with share and nearest GNOME HIG swatch (dE)
  detail       : thinnest feature (px at 64 and 32 px display) -> what will vanish
  holes        : number of enclosed counter-shapes (negative space) in the mark

It cannot tell you *why* the icon is recognisable; it writes a draft
identity sheet (work/identity.md) with the measured facts and empty slots the
agent MUST fill by looking: silhouette, anchors, negative space, colour
relations, must-not-change list.

Usage: analyze_source.py work/source.png [--out-md work/identity.md] [--json work/analysis.json]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import rgb_to_hex, nearest_hig  # noqa: E402

TEMPLATES = {  # GNOME HIG template guide shapes (nominal 128 canvas)
    "circle": (120, 120), "square": (104, 104), "portrait": (88, 112), "landscape": (112, 88),
}


def analyze(path):
    im = Image.open(path).convert("RGBA")
    if im.size[0] != 512:
        im = im.resize((512, 512), Image.LANCZOS)
    arr = np.asarray(im).astype(float)
    a = arr[..., 3] > 128
    ys, xs = np.where(a)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    w, h = x1 - x0, y1 - y0
    m = a[y0:y1, x0:x1]
    area = m.sum()
    fill = area / (w * h)
    from skimage.measure import perimeter
    per = perimeter(m)
    circ = 4 * np.pi * area / max(per, 1) ** 2
    mirror = m[:, ::-1]
    iou = (m & mirror).sum() / max((m | mirror).sum(), 1)
    filled = ndimage.binary_fill_holes(a)
    holes_mask = filled & ~a
    _, n_holes = ndimage.label(holes_mask)
    # interior colour regions -> internal holes of the main colour are negative space
    aspect = w / h
    if 0.92 < aspect < 1.08 and 0.74 < fill < 0.83:
        shape = "circle"
    elif 0.92 < aspect < 1.08 and fill > 0.9:
        shape = "square (rounded)" if fill < 0.985 else "square (sharp)"
    elif fill > 0.9 and aspect < 0.92:
        shape = "portrait"
    elif fill > 0.9 and aspect > 1.08:
        shape = "landscape"
    else:
        shape = "free silhouette"
    # colour clusters (k-means, merges gradient shades) + thinnest feature per cluster
    from scipy.cluster.vq import kmeans2
    rgb = arr[..., :3]
    px = rgb[a]
    rng = np.random.default_rng(0)
    sample = px[rng.choice(len(px), min(20000, len(px)), replace=False)]
    best = None
    for k in (2, 3, 4, 5, 6):
        cent, lab = kmeans2(sample, k, minit="++", seed=1)
        err = np.sqrt(((sample - cent[lab]) ** 2).sum(-1)).mean()
        if best is None or err < best[0] * 0.8:
            best = (err, cent)
        if err < 14:
            break
    cent = best[1]
    full = np.argmin(((rgb[..., None, :] - cent[None, None]) ** 2).sum(-1), axis=-1)
    colours, thin = [], []
    for ci in np.argsort([-(full[a] == i).sum() for i in range(len(cent))]):
        reg = (full == ci) & a
        share = reg.sum() / a.sum()
        if share < 0.01:
            continue
        c = rgb[reg].mean(axis=0)
        nm, hx, de = nearest_hig(tuple(c))
        reg_o = ndimage.binary_opening(reg, iterations=2)
        labl, n = ndimage.label(reg_o)
        if n:
            sizes = ndimage.sum(reg_o, labl, range(1, n + 1))
            keep = np.isin(labl, 1 + np.where(sizes > 0.002 * a.sum())[0])
            dt = ndimage.distance_transform_edt(keep)
            mx = ndimage.maximum_filter(dt, size=7)
            ridge = (dt == mx) & (dt > 2.5)
            if ridge.sum() > 20:
                thin.append(2 * np.percentile(dt[ridge], 5))
        colours.append({"hex": rgb_to_hex(c), "share": round(float(share), 3), "nearest_hig": nm,
                        "hig_hex": hx, "dE": round(float(de), 1)})
    thinnest512 = float(min(thin)) if thin else None
    side = max(w, h)
    def at(px):
        return None if thinnest512 is None else round(thinnest512 * px / side, 2)
    res = {
        "file": str(path),
        "bbox_px_at_512": [int(x0), int(y0), int(w), int(h)],
        "aspect_w_over_h": round(float(aspect), 3),
        "fill_ratio": round(float(fill), 3),
        "circularity": round(float(circ), 3),
        "mirror_symmetry_iou": round(float(iou), 3),
        "enclosed_holes": int(n_holes),
        "silhouette_class": shape,
        "suggested_template": {"circle": "circle", "square (rounded)": "square", "square (sharp)": "square",
                               "portrait": "portrait", "landscape": "landscape"}.get(shape, "free (fit visual weight)"),
        "dominant_colours": colours,
        "thinnest_feature_px": {"at_64": at(64), "at_48": at(48), "at_32": at(32)},
    }
    warn = []
    if res["thinnest_feature_px"]["at_32"] is not None and res["thinnest_feature_px"]["at_32"] < 1.0:
        warn.append("some features are thinner than 1px at 32px: thicken them optically or accept loss at 32")
    if len(colours) > 6:
        warn.append("many colour regions: decide which are identity colours and which are decoration")
    res["warnings"] = warn
    return res


IDENTITY_MD = """# Identity sheet — {name}

Measured by analyze_source.py (facts) — fill the TODO slots by *looking* at the source.

| Fact | Value |
|---|---|
| Silhouette class | {silhouette_class} (aspect {aspect_w_over_h}, fill {fill_ratio}, circularity {circularity}) |
| Suggested GNOME template | {suggested_template} |
| Mirror symmetry (IoU) | {mirror_symmetry_iou} |
| Enclosed negative spaces | {enclosed_holes} |
| Thinnest feature | {thin} |

## Colours (dominant first)
{colours}

## TODO — identity anchors (2-4 things that make it recognisable at 32 px)
1. TODO silhouette / outline:
2. TODO key shape(s) + their exact proportions/angles:
3. TODO negative space that must survive:
4. TODO colour relationship (which colour is ground, which is figure, gradient direction):

## TODO — must not change
- TODO (e.g. pose, number of elements, orientation, tilt angle, corner style)

## TODO — what may be GNOME-ified
- TODO (e.g. flatten gloss to flat planes, add 4 px chin, move brand hues toward HIG swatches by <= dE 10, simplify sub-32px detail)

## Archetype (see references/archetypes.md)
- TODO: brand-glyph-on-tile | free-glyph | letterform | multicolour-geometric | object | character/mascot | game-art | ui-derived

## Source geometry
- TODO: official SVG / APK vector / trace (trace_source.py) / none. Record origin + licence.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("png")
    ap.add_argument("--out-md")
    ap.add_argument("--json")
    ap.add_argument("--name", default="app")
    a = ap.parse_args()
    r = analyze(a.png)
    print(json.dumps(r, indent=1))
    if a.json:
        Path(a.json).write_text(json.dumps(r, indent=1))
    if a.out_md:
        cols = "\n".join(f"- `{c['hex']}` {c['share'] * 100:.0f}% -> nearest HIG {c['nearest_hig']} `{c['hig_hex']}` (dE {c['dE']})"
                         for c in r["dominant_colours"])
        t = r["thinnest_feature_px"]
        Path(a.out_md).write_text(IDENTITY_MD.format(name=a.name, colours=cols,
                                                     thin=f"{t['at_64']} px @64, {t['at_32']} px @32", **r))


if __name__ == "__main__":
    main()
