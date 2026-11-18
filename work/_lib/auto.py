#!/usr/bin/env python3
"""Automatic measurement for the remaining apps (batch pipeline).

For work/<slug>/source.png (IconRequest PNG upscaled to 512):
  * ground: the tile colour measured on the outer border ring - flat, linear
    gradient (least-squares RGB plane over x, y) or none (transparent corners);
  * mark: every pixel that differs from the ground model;
  * colour regions of the mark: k-means in Lab, merged when closer than dE 14,
    tiny regions folded into their nearest neighbour;
  * each region traced (gtrace: Lanczos x4, smoothing, potrace) -> parts.
Writes work/<slug>/geometry.json in the same format as extract_group1.py
(parts + info) plus the region list used by build_auto.py.

Nothing is drawn from memory; overrides for individual apps live in build_auto.py.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.cluster.vq import kmeans2
from skimage.color import rgb2lab

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtrace as gt  # noqa: E402

WORK = Path(__file__).resolve().parent.parent


# blurry sources need stronger smoothing before tracing (128-units)
SMOOTH = {"bcr": 1.6}
HALO = {"bcr"}
THRESH = {"walpy": 0.85}
SMOOTH["walpy"] = 0.8


def hexc(rgb):
    return "#%02x%02x%02x" % tuple(int(round(min(max(v, 0), 1) * 255)) for v in rgb)


def ground_model(a):
    h, w = a.shape[:2]
    Y, X = np.mgrid[0:h, 0:w] / np.array([h, w])[:, None, None]
    ring = np.zeros((h, w), bool)
    b = int(0.035 * h)
    ring[:b], ring[-b:], ring[:, :b], ring[:, -b:] = True, True, True, True
    op = a[..., 3] > 0.9
    sel = ring & op
    if sel.sum() < 0.3 * ring.sum():
        return {"kind": "none"}, None
    A = np.c_[X[sel], Y[sel], np.ones(sel.sum())]
    coef = np.linalg.lstsq(A, a[sel][:, :3], rcond=None)[0]       # 3x3: x, y, 1
    model = np.einsum("hwk,kc->hwc", np.dstack([X, Y, np.ones_like(X)]), coef)
    resid = np.linalg.norm(a[..., :3] - model, axis=-1)
    # robust: refit on border pixels that agree with the model (drops marks touching the edge)
    good = sel & (resid < 0.12)
    if good.sum() > 0.25 * ring.sum():
        A = np.c_[X[good], Y[good], np.ones(good.sum())]
        coef = np.linalg.lstsq(A, a[good][:, :3], rcond=None)[0]
        model = np.einsum("hwk,kc->hwc", np.dstack([X, Y, np.ones_like(X)]), coef)
    gx, gy = coef[0], coef[1]
    span = float(np.linalg.norm(gx) + np.linalg.norm(gy))
    c_mid = coef[2] + 0.5 * gx + 0.5 * gy
    if span < 0.10:
        return {"kind": "flat", "color": hexc(c_mid)}, model
    # gradient: endpoints along the strongest direction
    d = np.array([np.linalg.norm(gx), np.linalg.norm(gy)])
    d = d / (d.sum() + 1e-9)
    sgn = np.sign([np.dot(gx, gx + gy) or 1, np.dot(gy, gx + gy) or 1])
    dx, dy = d[0] * sgn[0], d[1] * sgn[1]
    p0 = np.array([0.5 - dx / 2, 0.5 - dy / 2])
    p1 = np.array([0.5 + dx / 2, 0.5 + dy / 2])
    c0 = coef[2] + gx * p0[0] + gy * p0[1]
    c1 = coef[2] + gx * p1[0] + gy * p1[1]
    return {"kind": "gradient", "color": hexc(c_mid), "c0": hexc(c0), "c1": hexc(c1),
            "p0": [round(float(v) * 128, 2) for v in p0], "p1": [round(float(v) * 128, 2) for v in p1]}, model


def regions(a, mark, max_k=6, merge_de=14.0):
    lab = rgb2lab(np.clip(a[..., :3], 0, 1))
    # cluster only "core" pixels where the colour is locally stable: antialiased
    # edges between two colours otherwise become fake regions of their own
    gm = sum(np.hypot(ndimage.sobel(lab[..., c], 0), ndimage.sobel(lab[..., c], 1)) for c in range(3))
    core = mark & (gm < 4.0) & ndimage.binary_erosion(mark, iterations=6)
    if core.sum() < 200:
        core = mark
    pix = lab[core]
    if len(pix) < 50:
        return [], None
    rng = np.random.default_rng(0)
    sample = pix[rng.choice(len(pix), min(len(pix), 40000), replace=False)]
    k = min(max_k, max(1, len(sample) // 200))
    cent, _ = kmeans2(sample.astype(np.float64), k, minit="++", seed=0)
    # merge close centres
    cent = list(cent)
    changed = True
    while changed and len(cent) > 1:
        changed = False
        best = None
        for i in range(len(cent)):
            for j in range(i + 1, len(cent)):
                dE = np.linalg.norm(cent[i] - cent[j])
                if dE < merge_de and (best is None or dE < best[0]):
                    best = (dE, i, j)
        if best:
            _, i, j = best
            cent[i] = (cent[i] + cent[j]) / 2
            cent.pop(j)
            changed = True
    cent = np.array(cent)
    lab_m = lab.reshape(-1, 3)
    dist = np.linalg.norm(lab_m[:, None, :] - cent[None], axis=-1)
    lbl = dist.argmin(1).reshape(mark.shape)
    lbl[~mark] = -1
    # a region is real if it owns enough STABLE core pixels; antialias blends own
    # (almost) none and are folded into the nearest real centre
    real = [c for c in range(len(cent)) if ((lbl == c) & core).sum() >= 0.0006 * mark.size]
    if not real:
        real = [int(np.bincount(lbl[mark]).argmax())]
    for c in range(len(cent)):
        if c not in real:
            others = sorted(real, key=lambda r: np.linalg.norm(cent[r] - cent[c]))
            lbl[lbl == c] = others[0]
    out = []
    for c in np.unique(lbl[lbl >= 0]):
        m = lbl == c
        rgb = np.median(a[m][:, :3], axis=0)
        out.append((m, hexc(rgb)))
    out.sort(key=lambda t: -t[0].sum())
    return out, lbl


def analyse(slug):
    a, s = gt.load(WORK / slug)
    g, model = ground_model(a)
    op = a[..., 3] > 0.5
    if g["kind"] == "none":
        mark = op
    else:
        resid = np.linalg.norm(a[..., :3] - model, axis=-1)
        mark = op & (resid > THRESH.get(slug, 0.16))
    # drop specks (< 0.05 % of the canvas) and the thin antialias rim at the tile edge
    lab, n = ndimage.label(mark, structure=np.ones((3, 3)))
    if n:
        sizes = ndimage.sum(mark, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes > 0.0005 * mark.size
        mark = keep[lab]
    # drop thin pieces hugging the tile edge (edge highlights / rim artefacts, not the mark)
    lab2, n2 = ndimage.label(mark, structure=np.ones((3, 3)))
    if n2:
        h = mark.shape[0]
        band = int(0.07 * h)
        inner = np.zeros_like(mark)
        inner[band:-band, band:-band] = True
        for i in range(1, n2 + 1):
            comp = lab2 == i
            if (comp & inner).sum() < 0.15 * comp.sum():
                mark &= ~comp
    regs, _ = regions(a, mark)
    parts, info = {}, {"ground": g}
    plist = []
    if slug in HALO:
        # blurry source: the pale region is mostly the halo around the white mark; keep only
        # its pieces that stand apart from the white core (e.g. BCR's microphone)
        white = [m for m, c in regs if c.lower() in ("#ffffff", "#fefefe", "#fdfdfd")]
        if white:
            core = ndimage.binary_dilation(white[0], iterations=24)
            new = []
            for m, c in regs:
                if m is white[0]:
                    new.append((m, c))
                    continue
                lab3, n3 = ndimage.label(m, structure=np.ones((3, 3)))
                keep = np.zeros_like(m)
                for j in range(1, n3 + 1):
                    comp = lab3 == j
                    if (comp & core).sum() < 0.3 * comp.sum() and comp.sum() > 0.0008 * m.size:
                        keep |= comp
                if keep.any():
                    new.append((keep, c))
            regs = new
    for i, (m, col) in enumerate(regs):
        m2 = ndimage.binary_dilation(m, iterations=3)       # overlap seams between regions
        d = gt.trace_mask(m2, s, smooth_u=SMOOTH.get(slug, 0.45))
        if not d:
            continue
        name = f"r{i}"
        parts[name] = {"d": d, "iou": round(float(gt.iou_masks(gt.render_mask(d, m.shape[0]), m2)), 4)}
        plist.append({"name": name, "fill": col, "area": round(float(m.mean()), 4)})
    sil = ndimage.binary_fill_holes(mark)
    parts["silhouette"] = {"d": gt.trace_mask(sil, s, smooth_u=SMOOTH.get(slug, 0.45)), "iou": 1.0}
    holes = sil & ~mark
    holes = ndimage.binary_opening(holes, iterations=2)
    if holes.sum() > 0.001 * holes.size:
        parts["holes"] = {"d": gt.trace_mask(holes, s), "iou": 1.0}
    info["regions"] = plist
    info["mark_bbox"] = [round(float(v), 2) for v in gt.bbox(mark, s)] if mark.any() else None
    out = {"slug": slug, "source": f"work/{slug}/source.png (IconRequest PNG)",
           "method": "auto.py: ground model + Lab k-means regions -> gtrace", "parts": parts, "info": info}
    (WORK / slug / "geometry.json").write_text(json.dumps(out, indent=1))
    return g["kind"], [(p["fill"], p["area"]) for p in plist]


if __name__ == "__main__":
    slugs = sys.argv[1:] or [l.split("\t")[0] for l in (WORK / "_lib/batch_apps.tsv").read_text(encoding="utf-8").splitlines()]
    for s_ in slugs:
        try:
            k, regs = analyse(s_)
            print(s_, k, regs, flush=True)
        except Exception as e:  # report and continue with the batch
            print(s_, "ERROR", repr(e), flush=True)
