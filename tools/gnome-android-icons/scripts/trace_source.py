#!/usr/bin/env python3
"""Trace a raster source icon into *reference* vector layers (potrace, no AI).

Why: when no official SVG exists, tracing the user's own source image gives the
real contours (ear angles, tail sweep, negative spaces, limb overlaps) instead
of curves guessed from memory.  The result is REFERENCE GEOMETRY to build on:
clean it, simplify it, snap it to the 2 px grid, re-shade it the GNOME way.
It is not a finished icon and must never be delivered as one.

Pipeline: k-means colour quantisation -> one bitmap per colour -> potrace ->
cubic Bezier paths in a 128x128 viewBox, ordered largest-area first.
Detail pass (default): the first trace is rendered and compared with the source
(OKLab); small, sharp regions it lost (eyes, cheeks, seeds, a highlight) get
their own colour / are kept below --min-area.
Gradient pass (default): neighbouring layers whose shared border is smooth in the
source (no edge, just a colour ramp) are one gradient surface split by the colour
quantiser; they are merged back into one shape with fill = mean colour and
data-gradient="stop stop ..." (same convention as flatten_svg.py, read by autodraft).
What is still missing (too small, smooth shading) goes to <out>.json for the brief.
  --stack  (default) fills each layer's holes so lower layers stay whole shapes
           (more editable: a disc stays a full disc under its glyph)
  --exact  exact partition (no overlaps)

Usage:
  trace_source.py work/source.png --out work/source-trace.svg [--colors 4]
                  [--min-area 0.0015] [--smooth 1.0] [--exact] [--no-details] [--no-gradients]
Requires: potracer (pip install potracer), numpy, pillow, scipy
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.cluster.vq import kmeans2

try:
    import potrace
except ImportError:  # pragma: no cover
    sys.exit("pip install potracer")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import rgb_to_hex, render_svg  # noqa: E402


def curve_to_d(curve, s):
    def f(p):
        return f"{p.x * s:.2f} {p.y * s:.2f}"
    d = [f"M{f(curve.start_point)}"]
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f"L{f(seg.c)}L{f(seg.end_point)}")
        else:
            d.append(f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
    d.append("Z")
    return "".join(d)


_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]])
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660]])


def oklab(rgb):
    """sRGB 0..255 (..., 3) -> OKLab (..., 3), vectorised."""
    c = np.asarray(rgb, float) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return np.cbrt(c @ _M1.T) @ _M2.T


def edge_map(lab_img):
    """Edge strength of the source in OKLab units (Sobel of a sigma-1 blur)."""
    tot = np.zeros(lab_img.shape[:2])
    for ch in range(lab_img.shape[2]):            # per channel: ndimage.sobel would also smooth across channels
        sm = ndimage.gaussian_filter(lab_img[..., ch], sigma=1)
        tot += ndimage.sobel(sm, axis=1) ** 2 + ndimage.sobel(sm, axis=0) ** 2
    return np.sqrt(tot)


def _step_response():
    """Edge-map value of a unit colour step (calibrates edge_map)."""
    st = np.zeros((24, 24, 3))
    st[:, 12:, 0] = 1.0
    return float(edge_map(st).max())


C_STEP = _step_response()


def _grow(sl, pad, shape):
    return tuple(slice(max(0, s.start - pad), min(n, s.stop + pad)) for s, n in zip(sl, shape))


def assign(arr, alpha, cent, sure=28.0, reach=3):
    """Label every opaque pixel with a colour layer.  Pixels close to a layer colour
    take it; blended pixels (anti-aliasing, resampling) may only take a colour that
    is actually present within `reach` px, so the white-to-dark edge of an eye
    highlight never becomes a ring of some third colour that happens to lie between."""
    cent = np.asarray(cent, float)
    d2 = ((arr[..., None, :3] - cent[None, None]) ** 2).sum(-1)
    lab = d2.argmin(-1)
    ok = d2.min(-1) <= sure ** 2
    allowed = np.zeros(d2.shape, bool)
    for i in range(len(cent)):
        allowed[..., i] = ndimage.binary_dilation(ok & (lab == i), iterations=reach)
    lab2 = np.where(allowed, d2, np.inf).argmin(-1)
    keep = ok | ~allowed.any(-1)
    lab2[keep] = lab[keep]
    lab2[~alpha] = -1
    return lab2


def components(labels, ncol, keep):
    """Connected regions of every colour label (after a 3x3 opening that removes
    anti-aliasing slivers), filtered by keep(mask, colour_index)."""
    comps = []
    for i in range(ncol):
        m = labels == i
        body = ndimage.binary_opening(m, iterations=1)
        # the body plus 1 px around it: drops long 1-2 px slivers but keeps a thin bridge
        # between two bodies (the dark rim between an eye highlight and the eye's edge)
        m = m & ndimage.binary_dilation(body, iterations=1)
        lab, n = ndimage.label(m)
        for j, sl in enumerate(ndimage.find_objects(lab), 1):
            if sl is None:
                continue
            raw = lab == j
            if not (raw[sl] & body[sl]).any():
                continue
            if keep(raw, i):
                comps.append({"i": i, "raw": raw, "sl": sl})
    return comps


def merge_gradients(comps, cent, mag, max_de=0.22, max_ratio=0.25):
    """Group neighbouring regions whose shared border has no edge in the source:
    they are bands of one gradient, split by the colour quantiser."""
    n = len(comps)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    shape = mag.shape
    dil = []
    for c in comps:
        sl = _grow(c["sl"], 3, shape)
        dil.append((sl, ndimage.binary_dilation(c["raw"][sl], iterations=2)))
    labc = oklab(np.asarray(cent))
    for a in range(n):
        for b in range(a + 1, n):
            ia, ib = comps[a]["i"], comps[b]["i"]
            if ia == ib:
                continue
            de = float(np.linalg.norm(labc[ia] - labc[ib]))
            if de > max_de:
                continue
            (sa, da), (sb, db) = dil[a], dil[b]
            sl = tuple(slice(max(x.start, y.start), min(x.stop, y.stop)) for x, y in zip(sa, sb))
            if any(q.start >= q.stop for q in sl):
                continue
            ra = da[tuple(slice(q.start - x.start, q.stop - x.start) for q, x in zip(sl, sa))]
            rb = db[tuple(slice(q.start - x.start, q.stop - x.start) for q, x in zip(sl, sb))]
            band = ra & rb
            if band.sum() < 12:
                continue
            ratio = float(np.percentile(mag[sl][band], 80)) / (C_STEP * de)
            if ratio < max_ratio:
                parent[find(a)] = find(b)
    groups = {}
    for k in range(n):
        groups.setdefault(find(k), []).append(k)
    return list(groups.values())


def _close(mask, r):
    """Binary closing with radius r that also works at the image border (keeps mask)."""
    pad = r + 1
    c = ndimage.binary_closing(np.pad(mask, pad), iterations=r)[pad:-pad, pad:-pad]
    return c | mask


def build_parts(comps, groups, cent, exact):
    """One output part per group: union mask, fill, gradient stops (if merged)."""
    parts = []
    for g in groups:
        raw = np.zeros_like(comps[g[0]]["raw"])
        for k in g:
            raw |= comps[k]["raw"]
        # stack mode: close small notches first (anti-aliasing bites, a rim lost between a
        # highlight and the edge of an eye); small shapes get a slightly larger radius
        if exact:
            shape = raw
        else:
            r = int(np.clip(round(0.1 * np.sqrt(raw.sum())), 2, 6)) if raw.sum() < 0.02 * raw.size else 2
            shape = ndimage.binary_fill_holes(_close(raw, r))
        idx = []
        for k in g:
            if comps[k]["i"] not in idx:
                idx.append(comps[k]["i"])
        if len(idx) == 1:
            fill, stops = rgb_to_hex(cent[idx[0]]), None
        else:
            # stops ordered bottom-left -> top-right (the diagonal autodraft rebuilds on curved faces)
            w, pos = [], []
            for i in idx:
                m = np.zeros_like(raw)
                for k in g:
                    if comps[k]["i"] == i:
                        m |= comps[k]["raw"]
                ys, xs = np.nonzero(m)
                w.append(len(xs))
                pos.append(xs.mean() - ys.mean())
            order = [idx[j] for j in np.argsort(pos)]
            stops = [rgb_to_hex(cent[i]) for i in order]
            labm = (oklab(np.asarray([cent[i] for i in idx])) * np.asarray(w)[:, None]).sum(0) / sum(w)
            from _common import oklab_to_hex
            fill = oklab_to_hex(*labm)
        ys, xs = np.nonzero(raw)
        parts.append({"area": int(shape.sum()), "mask": shape, "raw": raw, "fill": fill, "stops": stops,
                      "box": (ys.min(), xs.min(), ys.max() + 1, xs.max() + 1)})
    # nested shapes always have a smaller filled area than their container,
    # so largest-first painting keeps eyes, centres and counters visible
    parts.sort(key=lambda t: -t["area"])
    if not exact and len(parts) > 1:
        # a smaller shape that sits mostly inside a larger one (a highlight inside an eye,
        # even one touching the eye's edge) is part of that shape's silhouette: the eye
        # stays a whole ellipse under its highlight instead of getting a bite out of it
        rings = []
        for q in parts:
            y0, x0, y1, x1 = q["box"]
            sl = (slice(max(0, y0 - 3), y1 + 3), slice(max(0, x0 - 3), x1 + 3))
            r = ndimage.binary_dilation(q["raw"][sl], iterations=2) & ~q["mask"][sl]
            rings.append((sl, r, max(1, int(r.sum()))))
        for k, p in enumerate(parts):
            grown = False
            for m in range(k + 1, len(parts)):
                sl, r, n = rings[m]
                if (r & p["raw"][sl]).sum() >= 0.6 * n:
                    p["mask"] = p["mask"] | parts[m]["mask"]
                    grown = True
            if grown:   # close the anti-aliasing crack left between the two
                p["mask"] = ndimage.binary_fill_holes(_close(p["mask"], 3))
    if not exact and len(parts) > 1:
        # trapping: every shape reaches 2 px under the shapes painted above it, so
        # abutting shapes leave no anti-aliasing seam (invisible in the stacked render)
        above = np.zeros_like(parts[0]["mask"])
        for p in reversed(parts):
            if above.any():
                p["mask"] = p["mask"] | (ndimage.binary_dilation(p["mask"], iterations=2) & above)
            above |= p["mask"]
    return parts


def _potrace(mask, smooth):
    bm = potrace.Bitmap(~mask)  # potracer traces False pixels
    try:
        return bm.trace(turdsize=2, alphamax=smooth, opticurve=True, opttolerance=0.2)
    except (ValueError, ZeroDivisionError):
        # potracer's curve optimiser can hit a math domain error on some outlines;
        # the unoptimised curve is the same shape with a few more segments
        return bm.trace(turdsize=2, alphamax=smooth, opticurve=False)


def write_svg(parts, out, title, smooth, work_size):
    s = 128.0 / work_size
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">',
             f'  <title>{title}</title>']
    used = []
    for k, p in enumerate(parts):
        d = "".join(curve_to_d(cv, s) for cv in _potrace(p["mask"], smooth))
        if not d:
            continue
        used.append(p["fill"])
        grad = f' data-gradient="{" ".join(p["stops"])}"' if p["stops"] else ""
        lines.append(f'  <path id="trace-{k:02d}-{p["fill"][1:]}" fill="{p["fill"]}"{grad} fill-rule="evenodd" d="{d}"/>')
    lines.append("</svg>")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(lines))
    return used


def _is_blend(ring_rgb, c_rgb, tol=30.0):
    """True when colour c lies between the two colours on either side of it (an
    anti-aliasing / resampling / JPEG blend), False for a colour of its own (a detail).
    Tested in gamma-encoded RGB, the space renderers and JPEG blend in."""
    r = np.asarray(ring_rgb, float)
    centred = r - r.mean(0)
    axis = np.linalg.svd(centred, full_matrices=False)[2][0]
    t = centred @ axis
    lo, hi = np.percentile(t, 20), np.percentile(t, 80)
    A, B = r[t <= lo].mean(0), r[t >= hi].mean(0)
    ab = B - A
    n2 = float(ab @ ab)
    if n2 < 20.0 ** 2:
        return False                     # one colour around it: whatever differs is a detail
    u = np.clip(float((np.asarray(c_rgb, float) - A) @ ab) / n2, 0, 1)
    return float(np.linalg.norm(A + u * ab - c_rgb)) < tol and 0.05 < u < 0.95


def noise_level(arr, alpha, mag):
    """Robust per-channel RGB noise of the source (JPEG, resampling) in flat areas."""
    flat = alpha & (mag < 0.02)
    if flat.sum() < 500:
        return 0.0
    med = np.stack([ndimage.median_filter(arr[..., c], size=3) for c in range(3)], -1)
    dev = np.abs(arr[..., :3] - med)[flat].max(-1)
    return float(1.4826 * np.median(dev))


def missed_regions(arr, alpha, lab_src, mag, out_svg, total, lo, hi=0.02, miss_de=0.05, noise=0.0):
    """Regions of the source the rendered trace does not reproduce.
    Returns (sharp, smooth): sharp = small regions with a real edge around them
    (lost details: eyes, cheeks, seeds); smooth = differences without an edge
    (gradient / shading that flat layers cannot carry)."""
    h = arr.shape[0]
    tr = np.asarray(render_svg(out_svg, h)).astype(float)
    de = np.linalg.norm(lab_src - oklab(tr[..., :3]), axis=-1)
    miss = alpha & ((de > miss_de) | (tr[..., 3] < 128))
    miss = ndimage.binary_opening(miss, iterations=1)
    interior = ndimage.binary_erosion(alpha, iterations=3)
    lab, n = ndimage.label(miss)
    sharp, smooth = [], []
    s = 128.0 / h
    for j, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None:
            continue
        big = _grow(sl, 9, lab.shape)
        comp = lab[big] == j
        area = int(comp.sum())
        if area < lo * total:
            continue
        # surroundings sampled 3-7 px away: past the blur / anti-aliasing zone of the border
        ring = (ndimage.binary_dilation(comp, iterations=7) & ~ndimage.binary_dilation(comp, iterations=3)
                & alpha[big] & ~miss[big])
        # colour of the region's core (away from its anti-aliased border): a highlight
        # inside a dark eye is white, not the grey average of highlight + edge
        dt = ndimage.distance_transform_edt(comp)
        core = dt >= max(1.0, 0.6 * dt.max())
        col = np.median(arr[big][..., :3][core], axis=0)
        ref = (np.median(arr[big][..., :3][ring], axis=0) if ring.sum() >= 4
               else np.median(tr[big][..., :3][comp], axis=0))
        contrast = float(np.linalg.norm(oklab(col) - oklab(ref)))
        # is there a real edge along the region's border?  median over a 3 px band, inside the
        # icon only (the icon outline and a neighbouring shape touch just part of the border)
        band = (ndimage.binary_dilation(comp, iterations=1) & ~ndimage.binary_erosion(comp, iterations=1)
                & interior[big])
        edge = float(np.median(mag[big][band])) / (C_STEP * max(contrast, 0.03)) if band.sum() >= 8 else 0.0
        ys, xs = np.nonzero(comp)
        info = {"colour": rgb_to_hex(col), "area_px128": round(area * s * s, 1),
                "bbox128": [round((xs.min() + big[1].start) * s, 1), round((ys.min() + big[0].start) * s, 1),
                            round((xs.max() + 1 + big[1].start) * s, 1), round((ys.max() + 1 + big[0].start) * s, 1)],
                "contrast": round(contrast, 3), "edge": round(edge, 2)}
        # a detail has a body: inscribed radius >= ~0.6 px at 128 (JPEG halos and
        # resampling rims around shapes are thinner than that)
        thick = dt.max() >= 3.5 * h / 768
        blend = (_is_blend(arr[big][..., :3][ring], col, tol=30.0 + 3 * noise)
                 if ring.sum() >= 8 else False)
        info["blend"] = bool(blend)
        if blend:
            continue        # anti-aliasing zone between two traced colours (contour off by a pixel), not a detail
        if contrast > 0.04 + noise / 400 and edge > 0.3 and area <= hi * total and thick:
            full = np.zeros_like(alpha)
            full[big] = comp
            sharp.append((info, col, full))
        elif edge <= 0.3 and contrast > 0.02 and area > 4 * lo * total:
            smooth.append((info, col, None))
        # else: a thin sliver along a traced edge (contour off by a pixel) - not worth reporting
    sharp.sort(key=lambda t: -t[0]["area_px128"])
    smooth.sort(key=lambda t: -t[0]["area_px128"])
    return sharp, smooth


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("png")
    ap.add_argument("--out", required=True)
    ap.add_argument("--colors", type=int, default=0, help="number of colour layers (0 = auto 2..8)")
    ap.add_argument("--min-area", type=float, default=0.0015, help="drop specks smaller than this fraction")
    ap.add_argument("--detail-area", type=float, default=0.0002,
                    help="smallest lost detail the detail pass restores (fraction of the icon area)")
    ap.add_argument("--no-details", action="store_true", help="skip the detail pass")
    ap.add_argument("--no-gradients", action="store_true", help="keep gradient bands as separate flat layers")
    ap.add_argument("--smooth", type=float, default=1.0, help="potrace alphamax (0 = polygons, 1.33 = smoothest)")
    ap.add_argument("--exact", action="store_true", help="exact partition instead of stacked layers")
    ap.add_argument("--work-size", type=int, default=512)
    a = ap.parse_args()

    im = Image.open(a.png).convert("RGBA").resize((a.work_size, a.work_size), Image.LANCZOS)
    arr = np.asarray(im).astype(float)
    alpha = arr[..., 3] > 127
    px = arr[..., :3][alpha]
    if not len(px):
        sys.exit(f"{a.png}: no opaque pixels - run extract_icon.py first")
    rng = np.random.default_rng(0)
    sample = px[rng.choice(len(px), min(30000, len(px)), replace=False)]
    total = int(alpha.sum())
    forced = bool(a.colors)
    lab_src = oklab(arr[..., :3])
    mag = edge_map(np.where(alpha[..., None], lab_src, 0.0))
    noise = noise_level(arr, alpha, mag)

    def far_share(cent):
        """Share of opaque pixels far (> 60) from every centroid, measured in image
        space after a 3x3 opening: 1-2 px anti-aliased edge blends do not count,
        small but real details (eyes, dots, a bolt) do."""
        d2 = ((arr[..., None, :3] - np.asarray(cent)[None, None]) ** 2).sum(-1).min(-1)
        far = (d2 > 60 ** 2) & alpha
        return float(ndimage.binary_opening(far, iterations=1).sum()) / max(1, total)

    spread = np.percentile(np.sqrt(((sample - sample.mean(axis=0)) ** 2).sum(-1)), 95)
    if not a.colors and spread < 20 and far_share(sample.mean(axis=0)[None]) <= 0.003:
        a.colors = 1  # single-colour mark (e.g. a white logo): one layer, no split anti-aliasing
    ks = [a.colors] if a.colors else [2, 3, 4, 5, 6, 7, 8]
    best = None
    for k in ks:
        if k == 1:
            cent = sample.mean(axis=0)[None]
            lab = np.zeros(len(sample), int)
        else:
            cent, lab = kmeans2(sample, k, minit="++", seed=3)
        dist = np.sqrt(((sample - cent[lab]) ** 2).sum(-1))
        err = dist.mean()
        # small but distinct details (eyes, dots, a lightning bolt) must get their own colour:
        # keep adding clusters while > 0.3 % of pixels are far from every centroid
        outliers = far_share(cent)
        if best is None or err < best[0] * 0.8 or a.colors or best[2] > 0.003:
            best = (err, cent, outliers)
        if not a.colors and err < 14 and outliers <= 0.003:
            break
    cent = np.asarray(best[1], float)
    labels = assign(arr, alpha, cent)
    title = f"Reference trace of {Path(a.png).name} (potrace) - NOT final artwork"
    comps = components(labels, len(cent), lambda c, i: c.sum() >= a.min_area * total)
    report = {"source": str(a.png), "work_size": a.work_size, "noise_rgb": round(noise, 2),
              "detail_pass": None, "gradient_parts": []}

    def grouped(comps, cent):
        return [[k] for k in range(len(comps))] if a.no_gradients else merge_gradients(comps, cent, mag)

    if not a.no_details:
        write_svg(build_parts(comps, grouped(comps, cent), cent, a.exact), a.out, title, a.smooth, a.work_size)
        sharp, _ = missed_regions(arr, alpha, lab_src, mag, a.out, total, a.detail_area, noise=noise)
        if sharp:
            # group lost details by colour; reuse an existing layer colour when close
            groups = []
            for info, col, mask in sharp:
                lab_c = oklab(col)
                for g in groups:
                    if np.linalg.norm(g["lab"] - lab_c) < 0.04:
                        g["cols"].append((col, info["area_px128"]))
                        g["mask"] |= mask
                        break
                else:
                    groups.append({"lab": lab_c, "cols": [(col, info["area_px128"])], "mask": mask.copy()})
            cent2 = list(cent)
            detail_mask = np.zeros_like(alpha)
            added = []
            for g in groups:
                w = np.array([x[1] for x in g["cols"]])
                col = (np.array([x[0] for x in g["cols"]]) * w[:, None]).sum(0) / w.sum()
                near = np.linalg.norm(oklab(np.asarray(cent2)) - oklab(col), axis=-1)
                if near.min() >= 0.04 and not forced:
                    cent2.append(col)
                    added.append(rgb_to_hex(col))
                # else: an existing layer colour that only the size filter dropped
                detail_mask |= g["mask"]
            cent = np.asarray(cent2, float)
            inside = ndimage.binary_dilation(detail_mask, iterations=2) & alpha
            labels[inside] = assign(arr, alpha, cent)[inside]

            def keep(c, i):
                area = c.sum()
                if area >= a.min_area * total:
                    return True
                return area >= a.detail_area * total and (c & detail_mask).sum() >= 0.5 * area

            comps = components(labels, len(cent), keep)
            report["detail_pass"] = {"regions": len(sharp), "colours_added": added}
            print(f"detail pass: restored {len(sharp)} small region(s)"
                  + (f", new colour(s) {', '.join(added)}" if added else ""))

    parts = build_parts(comps, grouped(comps, cent), cent, a.exact)
    used = write_svg(parts, a.out, title, a.smooth, a.work_size)
    report["gradient_parts"] = [{"fill": p["fill"], "stops": p["stops"]} for p in parts if p["stops"]]
    if report["gradient_parts"]:
        print(f"gradient pass: {len(report['gradient_parts'])} part(s) rebuilt from colour bands -> data-gradient "
              + "; ".join(" ".join(g["stops"]) for g in report["gradient_parts"]))
    sharp, smooth = missed_regions(arr, alpha, lab_src, mag, a.out, total, a.detail_area / 4, noise=noise)
    report["missed_details"] = [x[0] for x in sharp[:12]]
    report["smooth_shading"] = [x[0] for x in smooth[:6]]
    if sharp:
        print(f"still missing: {len(sharp)} small detail(s) (largest {sharp[0][0]['area_px128']} px2 at 128, "
              f"colour {sharp[0][0]['colour']}) - redraw by hand if they carry identity")
    if smooth:
        print(f"smooth shading not in the flat layers: {len(smooth)} region(s)"
              + (" (gradient recorded as data-gradient)" if report["gradient_parts"] else ""))
    report.update({"shapes": len(used), "colours": sorted(set(used))})
    Path(a.out).with_suffix(".json").write_text(json.dumps(report, indent=1))
    print(f"{a.out}: {len(used)} shapes, colours: " + ", ".join(sorted(set(used))))


if __name__ == "__main__":
    main()
