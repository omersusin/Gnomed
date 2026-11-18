#!/usr/bin/env python3
"""Isolate an app icon from a phone screenshot / photo-viewer capture / logo PNG.

What it removes (deterministic image processing, no AI):
  * the photo-viewer letterbox (black/grey bands), status bar, back arrow and
    other UI chrome around the displayed image;
  * a neutral canvas around the logo (white, black, grey) -> real transparency
    with anti-aliased, colour-decontaminated edges.

What it keeps by default:
  * a *saturated* full-bleed tile colour (e.g. a logo printed on a brand-coloured
    square), because that colour is often part of the identity.  The report says
    so; pass --remove-bg to strip it anyway, or --keep-bg to keep any canvas.

Usage:
  extract_icon.py SCREENSHOT.png --out work/source.png [--report work/source.json]
                  [--size 512] [--crop X,Y,W,H] [--remove-bg | --keep-bg] [--tol 22]

Always LOOK at the result: the script reports what it decided, it cannot know
your intent.  If the decision is wrong, rerun with --crop / --keep-bg / --remove-bg.
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


def mode_color(pixels: np.ndarray) -> np.ndarray:
    q = (pixels // 8).astype(np.int32)
    keys = q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    k = vals[np.argmax(counts)]
    sel = pixels[keys == k]
    return sel.mean(axis=0)


def dist(img: np.ndarray, color: np.ndarray) -> np.ndarray:
    return np.sqrt(((img[..., :3].astype(float) - color[None, None, :3]) ** 2).sum(-1))


def longest_run(flags: np.ndarray):
    best, cur, start, bstart = 0, 0, 0, 0
    for i, f in enumerate(flags):
        if f:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best, bstart = cur, start
        else:
            cur = 0
    return (bstart, bstart + best) if best else None


def find_content_rect(rgb: np.ndarray, tol: float):
    """Locate the displayed image inside a viewer screenshot, or the icon on a plain canvas."""
    H, W, _ = rgb.shape
    top_skip = int(H * 0.06)  # status bar zone
    border = np.concatenate([rgb[top_skip:, :4].reshape(-1, 3), rgb[top_skip:, -4:].reshape(-1, 3),
                             rgb[-4:, :].reshape(-1, 3)])
    viewer = mode_color(border.astype(float))
    differs = dist(rgb, viewer) > tol
    # a photo viewer shows the image edge to edge (full width in portrait, full height
    # in landscape) between letterbox bands; anything narrower is an icon on a canvas
    row_frac = differs.mean(axis=1)
    rows = longest_run(row_frac > 0.6)
    if rows and (rows[1] - rows[0]) > H * 0.12:
        y0, y1 = rows
        cols = longest_run(differs[y0:y1].mean(axis=0) > 0.6) or (0, W)
        if cols[1] - cols[0] >= 0.9 * W:
            return viewer, (cols[0], y0, cols[1] - cols[0], y1 - y0), "dense-band"
    cols = longest_run(differs.mean(axis=0) > 0.6)
    if cols and (cols[1] - cols[0]) > W * 0.12:
        x0, x1 = cols
        rows = longest_run(differs[:, x0:x1].mean(axis=1) > 0.6) or (0, H)
        if rows[1] - rows[0] >= 0.9 * H:
            return viewer, (x0, rows[0], x1 - x0, rows[1] - rows[0]), "dense-band"
    # icon on a plain canvas (or a screenshot with chrome): the largest region that differs
    # from the canvas, plus the pieces next to it (separate letters, a detached dot),
    # padded so the crop keeps a rim of canvas for the background removal
    lab, n = ndimage.label(differs)
    if n == 0:
        return viewer, (0, 0, W, H), "none"
    sizes = ndimage.sum(differs, lab, range(1, n + 1))
    objs = ndimage.find_objects(lab)
    order = np.argsort(sizes)[::-1]
    main = None
    for idx in order:
        sl = objs[idx]
        if sl[0].stop <= top_skip * 1.5:
            continue
        main = idx
        break
    if main is None:
        return viewer, (0, 0, W, H), "none"
    y0, y1, x0, x1 = objs[main][0].start, objs[main][0].stop, objs[main][1].start, objs[main][1].stop
    gy, gx = (y1 - y0) * 0.2, (x1 - x0) * 0.2
    for idx in order:
        if idx == main or sizes[idx] < 0.01 * sizes[main]:
            continue
        sl = objs[idx]
        if (sl[0].start >= y0 - gy and sl[0].stop <= y1 + gy and sl[1].start >= x0 - gx and sl[1].stop <= x1 + gx):
            y0, y1 = min(y0, sl[0].start), max(y1, sl[0].stop)
            x0, x1 = min(x0, sl[1].start), max(x1, sl[1].stop)
    pad = max(4, int(0.03 * max(y1 - y0, x1 - x0)))
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(W, x1 + pad), min(H, y1 + pad)
    return viewer, (x0, y0, x1 - x0, y1 - y0), "component"


def saturation(c):
    mx, mn = max(c) / 255.0, min(c) / 255.0
    return 0.0 if mx == 0 else (mx - mn) / mx


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--report")
    ap.add_argument("--size", type=int, default=512, help="output square size (default 512)")
    ap.add_argument("--crop", help="manual crop X,Y,W,H in input pixels (skips viewer detection)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--remove-bg", action="store_true", help="always strip the canvas colour, even if saturated")
    g.add_argument("--keep-bg", action="store_true", help="never strip the canvas colour")
    ap.add_argument("--tol", type=float, default=22.0, help="colour tolerance (0-441) for viewer/canvas detection")
    a = ap.parse_args()

    im = Image.open(a.input)
    report = {"input": a.input, "input_size": im.size}
    rgba = np.asarray(im.convert("RGBA")).astype(float)
    rgb = rgba[..., :3]
    has_alpha = (rgba[..., 3] < 250).mean() > 0.02

    if has_alpha:
        report["mode"] = "already-transparent"
        out = rgba.copy()
        cx = (0, 0, rgb.shape[1], rgb.shape[0])
    else:
        if a.crop:
            x, y, w, h = (int(v) for v in a.crop.split(","))
            cx, how, viewer = (x, y, w, h), "manual", None
        else:
            viewer, cx, how = find_content_rect(rgb, a.tol)
        report["viewer_bg"] = None if viewer is None else rgb_to_hex(viewer)
        report["content_rect"] = list(map(int, cx))
        report["content_detection"] = how
        x, y, w, h = cx
        crop = rgb[y:y + h, x:x + w]
        edge = np.concatenate([crop[:3].reshape(-1, 3), crop[-3:].reshape(-1, 3),
                               crop[:, :3].reshape(-1, 3), crop[:, -3:].reshape(-1, 3)])
        canvas = mode_color(edge)
        edge_d = dist(edge[None], canvas)[0]
        uniform = float((edge_d < a.tol).mean())
        sat = saturation(canvas)
        report["canvas_color"] = rgb_to_hex(canvas)
        report["canvas_uniformity"] = round(uniform, 3)
        report["canvas_saturation"] = round(sat, 3)
        remove = uniform > 0.85 and (a.remove_bg or (not a.keep_bg and sat < 0.25))
        alpha = np.ones(crop.shape[:2])
        col = crop.copy()
        if remove:
            d = dist(crop, canvas)
            lo, hi = a.tol * 0.5, a.tol * 2.2
            near = d < hi
            lab, n = ndimage.label(near)
            border_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
            region = np.isin(lab, list(border_labels))
            region = ndimage.binary_dilation(region, iterations=1) & near
            a_soft = np.clip((d - lo) / (hi - lo), 0, 1)
            alpha = np.where(region, a_soft, 1.0)
            # colour decontamination of the anti-aliased rim
            aa = np.clip(alpha, 1e-3, 1)[..., None]
            col = np.where(alpha[..., None] < 1, (crop - (1 - aa) * canvas[None, None]) / aa, crop)
            col = np.clip(col, 0, 255)
            report["background"] = "removed (neutral canvas)" if sat < 0.25 else "removed (forced by --remove-bg)"
            report["removed_fraction"] = round(float((alpha < 0.5).mean()), 3)
        else:
            report["background"] = ("kept: canvas is a saturated full-bleed tile, probably part of the identity "
                                     "(use --remove-bg to strip)" if uniform > 0.85 and not a.keep_bg
                                     else "kept")
        out = np.dstack([col, alpha * 255])

    # trim + square pad
    al = out[..., 3]
    ys, xs = np.where(al > 8)
    if len(xs) == 0:
        sys.exit("nothing left after background removal; try --keep-bg or --crop")
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = out.shape[:2]
    side = max(h, w)
    canvas_img = np.zeros((side, side, 4))
    canvas_img[(side - h) // 2:(side - h) // 2 + h, (side - w) // 2:(side - w) // 2 + w] = out
    img = Image.fromarray(canvas_img.astype(np.uint8), "RGBA")
    if side < a.size / 2:
        report["warning"] = f"source is only {side}px; upscaled x{a.size / side:.1f} - use it as reference, not as artwork"
    img = img.resize((a.size, a.size), Image.LANCZOS)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    img.save(a.out)
    report["output"] = a.out
    report["trimmed_size_px"] = [int(w), int(h)]
    report["aspect"] = round(w / h, 3)
    # dominant colours of the visible icon
    px = np.asarray(img).reshape(-1, 4)
    px = px[px[:, 3] > 200][:, :3].astype(float)
    if len(px):
        q = (px // 12).astype(int)
        keys = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
        vals, counts = np.unique(keys, return_counts=True)
        top = []
        for k in vals[np.argsort(counts)[::-1][:6]]:
            c = px[keys == k].mean(axis=0)
            share = float((keys == k).mean())
            if share < 0.01:
                continue
            nm, hx, de = nearest_hig(tuple(c))
            top.append({"hex": rgb_to_hex(c), "share": round(share, 3), "nearest_hig": nm, "hig_hex": hx, "dE": round(de, 1)})
        report["dominant_colors"] = top
    if a.report:
        Path(a.report).write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
