#!/usr/bin/env python3
"""Measure identity geometry for group 1 from each work/<slug>/source.png.

Writes work/<slug>/geometry.json: named parts (SVG path d in 0..128 source
coordinates), measured colours and primitive fits, plus the IoU of every traced
part against its mask (trace fidelity). Run:  python3 work/_lib/extract_group1.py
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtrace as gt  # noqa: E402

WORK = Path(__file__).resolve().parent.parent


def superellipse_d(cx, cy, a, b, n, k=240):
    import math
    pts = []
    for i in range(k):
        th = 2 * math.pi * i / k
        c, s_ = math.cos(th), math.sin(th)
        x = cx + a * math.copysign(abs(c) ** (2 / n), c)
        y = cy + b * math.copysign(abs(s_) ** (2 / n), s_)
        pts.append(f"{x:.2f} {y:.2f}")
    return "M" + "L".join(pts) + "Z"


def gk_rounded_polygon(points, r):
    sys.path.insert(0, "/root/.claude/skills/gnome-android-icons/scripts")
    import gnome_kit
    return gnome_kit.rounded_polygon_d(points, r)


def luma(a):
    return a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)


def part(masks, name, mask, scale, **kw):
    d = gt.trace_mask(mask, scale, **kw)
    # fidelity: rasterise the path at the mask's resolution and compare
    r = gt.render_mask(d, mask.shape[0])
    masks[name] = {"d": d, "iou": round(float(gt.iou_masks(r, mask)), 4)}
    return d


def circ(mask, scale):
    cx, cy, r = gt.circle_fit(mask, scale)
    return {"cx": round(cx, 2), "cy": round(cy, 2), "r": round(r, 2)}


def median_hex(a, mask):
    c = np.median(a[mask][:, :3], axis=0)
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def run(slug, fn):
    a, scale = gt.load(WORK / slug)
    parts, info = {}, {}
    fn(a, scale, parts, info)
    out = {"slug": slug, "source": "work/%s/source.png (IconRequest PNG)" % slug,
           "method": "colour mask -> Lanczos x4 -> potrace (work/_lib/gtrace.py)",
           "parts": parts, "info": info}
    (WORK / slug / "geometry.json").write_text(json.dumps(out, indent=1))
    print(slug, {k: v["iou"] for k, v in parts.items()}, info)


def whatsapp(a, s, P, I):
    white = gt.near(a, "#ffffff", "#27d467")
    comps = gt.components(white)
    ring, hand = comps[0], comps[1]
    part(P, "ring", ring, s)
    part(P, "ring_outer", gt.fill_holes(ring), s)
    part(P, "handset", hand, s)
    I["green"] = median_hex(a, ~white & gt.opaque(a))


def instagram(a, s, P, I):
    white = (a[..., :3].min(-1) > 0.80) & gt.opaque(a)
    c = gt.components(white)
    part(P, "frame", c[0], s)
    part(P, "lens", c[1], s)
    part(P, "dot", c[2], s)
    I["frame_outer"] = list(map(lambda v: round(v, 2), gt.bbox(c[0], s)))


def youtube(a, s, P, I):
    red = gt.near(a, "#ff0033", "#ffffff") & gt.opaque(a)
    rect = gt.fill_holes(gt.components(red)[0])
    tri = rect & ~red
    # The play button is a superellipse with slightly convex sides; fit it instead of
    # tracing so its edges are clean (the 192 px source gives a stair-stepped trace).
    x0, y0, x1, y1 = gt.bbox(rect, s)
    cx, cy, ax, by = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    best = None
    for n in np.arange(2.5, 8.01, 0.1):
        d = superellipse_d(cx, cy, ax, by, n)
        iou = gt.iou_masks(gt.render_mask(d, rect.shape[0]), rect)
        if best is None or iou > best[0]:
            best = (iou, n, d)
    P["rect"] = {"d": best[2], "iou": round(float(best[0]), 4)}
    I["rect_superellipse_n"] = round(float(best[1]), 2)
    part(P, "triangle", gt.components(tri)[0], s)   # smoothed trace (IoU ~0.998)
    I["red"] = median_hex(a, red)
    I["rect_bbox"] = [round(v, 2) for v in gt.bbox(rect, s)]


def telefon(a, s, P, I):
    white = gt.near(a, "#ffffff", "#106d1f")
    part(P, "handset", gt.components(white)[0], s)
    I["green"] = median_hex(a, ~white & gt.opaque(a))


def mesajlar(a, s, P, I):
    white = gt.near(a, "#ffffff", "#116d20")
    bub = gt.components(white)[0]
    outer = gt.fill_holes(bub)
    part(P, "bubble", bub, s)
    part(P, "bubble_outer", outer, s)
    lines = outer & ~bub
    for i, m in enumerate(sorted(gt.components(lines)[:3], key=lambda m: np.nonzero(m)[0].mean())):
        part(P, f"line{i}", m, s)
    I["green"] = median_hex(a, ~white & gt.opaque(a))


def kamera(a, s, P, I):
    op = gt.opaque(a)
    red = gt.near(a, "#ff0000", "#000000") & op & (a[..., 0] > 0.6)
    disc = gt.components(op & ~red)[0]
    disc = gt.fill_holes(disc)
    I["disc"] = circ(disc, s)
    y = luma(a)
    r1 = disc & (y > 0.16) & (y < 0.30)
    r2 = disc & (y >= 0.30) & (y < 0.6)
    for n, m in (("ring1", r1), ("ring2", r2)):
        m = gt.components(m)[0]
        I[n + "_outer"] = circ(gt.fill_holes(m), s)
        hole = gt.fill_holes(m) & ~m
        I[n + "_inner"] = circ(gt.components(hole)[0], s)
        I[n + "_color"] = median_hex(a, m)
    rd = gt.components(red)[0]
    I["dot"] = circ(rd, s)
    I["dot_color"] = median_hex(a, rd)
    part(P, "disc", disc, s)


def foto(a, s, P, I):
    op = gt.opaque(a)
    sat = a[..., :3].max(-1) - a[..., :3].min(-1)
    ink = op & (sat > 0.18)
    ink = gt.components(ink)[0] if False else ink
    ys, xs = np.nonzero(ink)
    h, w = ink.shape
    # pinwheel centre: where the four petals meet = centre of the ink bbox
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    I["centre"] = [round(cx * s, 2), round(cy * s, 2)]
    Y, X = np.mgrid[0:h, 0:w]
    quads = {"yellow": (X < cx) & (Y < cy), "red": (X >= cx) & (Y < cy),
             "blue": (X >= cx) & (Y >= cy), "green": (X < cx) & (Y >= cy)}
    for n, q in quads.items():
        m = gt.components(ink & q)[0]
        part(P, n, m, s)
        # outer (saturated) colour of the petal: pixels far from the centre
        far = m & (((X - cx) ** 2 + (Y - cy) ** 2) > (0.6 * (xs.max() - xs.min()) / 2) ** 2)
        I[n] = median_hex(a, far if far.sum() > 50 else m)
        I[n + "_inner"] = median_hex(a, m & (((X - cx) ** 2 + (Y - cy) ** 2) < (0.25 * (xs.max() - xs.min()) / 2) ** 2)) if (m & (((X - cx) ** 2 + (Y - cy) ** 2) < (0.25 * (xs.max() - xs.min()) / 2) ** 2)).sum() > 20 else I[n]


def saat(a, s, P, I):
    white = gt.near(a, "#ffffff", "#106d1f")
    c = gt.components(white)
    ring, hands = c[0], c[1]
    I["ring_outer"] = circ(gt.fill_holes(ring), s)
    I["ring_inner"] = circ(gt.components(gt.fill_holes(ring) & ~ring)[0], s)
    part(P, "ring", ring, s)
    part(P, "hands", hands, s)
    I["green"] = median_hex(a, ~white & gt.opaque(a))


def ayarlar(a, s, P, I):
    white = gt.near(a, "#f5f5f5", "#915129")
    gear = gt.components(white)[0]
    outer = gt.fill_holes(gear)
    part(P, "gear", gear, s)
    part(P, "gear_outer", outer, s)
    I["hole"] = circ(gt.components(outer & ~gear)[0], s)
    I["brown"] = median_hex(a, ~white & gt.opaque(a))
    I["white"] = median_hex(a, gear)


def chatgpt(a, s, P, I):
    knot = (luma(a) < 0.5) & gt.opaque(a)
    part(P, "knot", knot, s, opttolerance=0.25)
    # the logo is WHITE strands outlined in black: the silhouette (outline + strands) is the object
    part(P, "silhouette", gt.fill_holes(gt.components(knot)[0]), s)
    I["bbox"] = [round(v, 2) for v in gt.bbox(knot, s)]


JOBS = {"whatsapp": whatsapp, "instagram": instagram, "youtube": youtube, "telefon": telefon,
        "mesajlar": mesajlar, "kamera": kamera, "foto_raflar": foto, "saat": saat,
        "ayarlar": ayarlar, "chatgpt": chatgpt}

if __name__ == "__main__":
    for slug in (sys.argv[1:] or JOBS):
        run(slug, JOBS[slug])
