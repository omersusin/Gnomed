#!/usr/bin/env python3
"""Small-size legibility check: what will close up, vanish or blur at 32 / 48 px.

For each SVG (rendered at 512 = 4 px per icon unit):

  gaps   negative spaces narrower than 1 screen pixel at the target size - between
         pieces of the same colour (a dot and a stem, two letters, a cut-out) or in
         the silhouette. They fuse into one blob. Marked RED.
  thin   parts of a colour region thinner than 0.75 screen px at the target size -
         they fade or vanish. Marked ORANGE. (Glyph lifts and chins are excluded:
         regions under 5 % of the painted area are decoration by definition.)
  ssim   structural similarity of the 32/48 px raster (scaled back up) to the 128 px
         render. Compared with the bundled GNOME app icons (baseline below).

Writes an annotated board (--out) and a JSON report (--json). Exit code 0 always:
the numbers inform the visual review, they do not replace it.

Usage:  legibility_check.py ICON.svg [...] --out work/app/legibility.png [--json r.json] [--sizes 32,48]
        legibility_check.py --baseline     # recompute official baseline (slow, ~1 min)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.cluster.vq import kmeans2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg, load_font, LIB_ROOT  # noqa: E402

R = 512                      # analysis render size
U = R / 128.0                # render px per icon unit
BASELINE_FILE = LIB_ROOT / "legibility-baseline.json"


def disk(r):
    r = max(1, int(round(r)))
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def colour_regions(img, painted, max_k=6):
    px = img[painted][:, :3].astype(float)
    if len(px) < 50:
        return []
    rng = np.random.default_rng(0)
    sample = px[rng.choice(len(px), min(15000, len(px)), replace=False)]
    k = min(max_k, max(1, len(np.unique((sample // 24).astype(int), axis=0))))
    cent, _ = kmeans2(sample, k, minit="++", seed=2) if k > 1 else (sample.mean(0)[None], None)
    # merge near-identical centroids (gradients split into bands)
    merged = []
    for c in cent:
        if not any(np.linalg.norm(c - m) < 28 for m in merged):
            merged.append(c)
    cent = np.array(merged)
    lab = np.argmin(((img[..., None, :3].astype(float) - cent[None, None]) ** 2).sum(-1), axis=-1)
    regions = []
    total = painted.sum()
    for i in range(len(cent)):
        m = (lab == i) & painted
        share = m.sum() / total
        if share >= 0.05:
            regions.append((m, share, cent[i]))
    return regions


def analyse(svg, sizes=(32, 48)):
    img = np.asarray(render_svg(svg, R))
    painted = img[..., 3] > 160
    regions = colour_regions(img, painted)
    res = {"file": str(svg), "sizes": {}}
    overlays = {}
    for S in sizes:
        px_units = 128.0 / S
        gap_w = px_units * U          # 1 screen px in render px
        thin_w = 0.75 * px_units * U
        gaps = np.zeros_like(painted)
        thin = np.zeros_like(painted)
        rgb = img[..., :3].astype(float)
        masks = [(painted, None)] + [(m, c) for m, _, c in regions]
        for m, centroid in masks:
            closed = ndimage.binary_closing(m, structure=disk(gap_w / 2), iterations=1)
            g = closed & ~m
            # ignore the outer background: only gaps enclosed by / between painted pixels of this mask
            g &= ndimage.binary_dilation(m, structure=disk(gap_w / 2))
            if centroid is not None:
                # a "gap" filled with almost the same colour is gradient banding, not a gap
                g &= ~painted | (np.sqrt(((rgb - centroid[None, None]) ** 2).sum(-1)) > 60)
            gaps |= g
        for m, share, _ in regions:
            opened = ndimage.binary_opening(m, structure=disk(thin_w / 2))
            thin |= m & ~opened
        # drop specks (anti-aliasing noise)
        gl, gn = ndimage.label(gaps)
        if gn:
            sizes_ = ndimage.sum(gaps, gl, range(1, gn + 1))
            keep = 1 + np.where(sizes_ > (gap_w * gap_w * 0.35))[0]
            gaps = np.isin(gl, keep)
            gn = len(keep)
        tl, tn = ndimage.label(thin)
        if tn:
            sizes_ = ndimage.sum(thin, tl, range(1, tn + 1))
            keep = 1 + np.where(sizes_ > (thin_w * thin_w * 0.5))[0]
            thin = np.isin(tl, keep)
            tn = len(keep)
        spots = []
        if gn:
            gl, _ = ndimage.label(gaps)
            for sl in ndimage.find_objects(gl)[:12]:
                if sl is None:
                    continue
                cy = (sl[0].start + sl[0].stop) / 2 / U
                cx = (sl[1].start + sl[1].stop) / 2 / U
                spots.append([round(cx, 1), round(cy, 1)])
        # structural similarity of the small raster
        from skimage.metrics import structural_similarity as ssim
        big = np.asarray(render_svg(svg, 128).convert("RGBA")).astype(float)
        small = render_svg(svg, S).resize((128, 128), Image.BILINEAR)
        sm = np.asarray(small.convert("RGBA")).astype(float)

        def flat(a):  # composite on mid grey so transparency counts
            al = a[..., 3:4] / 255.0
            return (a[..., :3] * al + 128 * (1 - al)).mean(-1)
        s = float(ssim(flat(big), flat(sm), data_range=255))
        res["sizes"][S] = {"gap_regions": int(gn), "gap_area_units2": round(float(gaps.sum()) / U / U, 1),
                           "gap_spots_xy": spots, "thin_area_units2": round(float(thin.sum()) / U / U, 1),
                           "ssim": round(s, 3)}
        overlays[S] = (gaps, thin)
    return res, img, overlays


def board(results, out, baseline):
    font, bfont = load_font(12), load_font(15)
    cell_w, cell_h = 600, 330
    W, H = cell_w * min(2, len(results)), 40 + cell_h * ((len(results) + 1) // 2)
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    d.text((14, 10), "Legibility at small sizes - RED: gaps that fuse at 32 px, ORANGE: parts thinner than 0.75 px at 32 px",
           fill=(20, 20, 20), font=bfont)
    for i, (res, img, ov) in enumerate(results):
        x0, y0 = (i % 2) * cell_w + 14, 40 + (i // 2) * cell_h
        base = Image.fromarray(img).resize((256, 256), Image.LANCZOS)
        bg = Image.new("RGBA", (256, 256), (154, 153, 150, 255))
        bg.alpha_composite(base)
        gaps, thin = ov[32]
        over = np.zeros((R, R, 4), np.uint8)
        over[thin] = (255, 150, 0, 200)
        over[gaps] = (230, 0, 40, 230)
        bg.alpha_composite(Image.fromarray(over).resize((256, 256), Image.NEAREST))
        sheet.paste(bg.convert("RGB"), (x0, y0))
        xx = x0 + 270
        for S in (32, 48):
            if S not in res["sizes"]:
                continue
            sm = Image.fromarray(img).resize((S, S), Image.LANCZOS)
            for j, col in enumerate(((246, 245, 244), (36, 31, 49))):
                t = Image.new("RGB", (S * 3 + 4, S * 3 + 4), col)
                t.paste(sm.resize((S * 3, S * 3), Image.NEAREST), (2, 2), sm.resize((S * 3, S * 3), Image.NEAREST))
                sheet.paste(t, (xx + j * (S * 3 + 10), y0 + (0 if S == 32 else 104)))
        name = Path(res["file"]).stem
        d.text((x0, y0 + 262), name[:40], fill=(30, 30, 30), font=font)
        r32, r48 = res["sizes"].get(32, {}), res["sizes"].get(48, {})
        lines = [f"32px: gaps {r32.get('gap_regions')} ({r32.get('gap_area_units2')} u2), thin {r32.get('thin_area_units2')} u2, "
                 f"ssim {r32.get('ssim')}",
                 f"48px: gaps {r48.get('gap_regions')}, thin {r48.get('thin_area_units2')} u2, ssim {r48.get('ssim')}"]
        if baseline:
            b = baseline["ssim32"]
            lines.append(f"official ssim32 p10/median/p90: {b['p10']} / {b['median']} / {b['p90']}")
        for k, line in enumerate(lines):
            d.text((xx, y0 + 262 + k * 15), line, fill=(40, 40, 40), font=font)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)


def compute_baseline():
    cat = json.loads((LIB_ROOT / "catalog.json").read_text())["icons"]
    rows = []
    for e in cat:
        if e["group"] == "adwaita-system":
            continue
        r, _, _ = analyse(LIB_ROOT / e["file"], sizes=(32,))
        rows.append(r["sizes"][32])
    out = {}
    for k, name in (("ssim", "ssim32"), ("gap_regions", "gap_regions32"), ("thin_area_units2", "thin_area32")):
        v = np.array([r[k] for r in rows], float)
        q = np.percentile(v, [10, 25, 50, 75, 90])
        out[name] = dict(p10=round(q[0], 3), p25=round(q[1], 3), median=round(q[2], 3), p75=round(q[3], 3), p90=round(q[4], 3))
    out["n"] = len(rows)
    BASELINE_FILE.write_text(json.dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="*")
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--sizes", default="32,48")
    ap.add_argument("--baseline", action="store_true")
    a = ap.parse_args()
    if a.baseline:
        print(json.dumps(compute_baseline(), indent=1))
        return
    if not a.svgs:
        ap.error("give SVG files")
    baseline = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else None
    sizes = tuple(int(s) for s in a.sizes.split(","))
    results = [analyse(p, sizes) for p in a.svgs]
    for res, _, _ in results:
        print(Path(res["file"]).name)
        for S, r in res["sizes"].items():
            flag = ""
            if baseline and S == 32 and r["ssim"] < baseline["ssim32"]["p10"]:
                flag = "   <-- below 90 % of official icons"
            print(f"  {S:>3}px  gaps {r['gap_regions']:>2} ({r['gap_area_units2']} u2)  thin {r['thin_area_units2']} u2  "
                  f"ssim {r['ssim']}{flag}")
            if r["gap_spots_xy"]:
                print(f"         gap locations (128-unit x,y): {r['gap_spots_xy'][:6]}")
    if baseline:
        b, g = baseline["ssim32"], baseline["gap_regions32"]
        print(f"\nofficial GNOME app icons at 32 px (n={baseline['n']}): ssim p10 {b['p10']} / median {b['median']} / "
              f"p90 {b['p90']}; gap regions median {g['median']} (p90 {g['p90']}).")
        print("Gaps are normal in detailed icons - what matters is whether a gap separates IDENTITY anchors "
              "(two letters, a dot from its stem, a cut-out that carries the brand).")
    if a.out:
        board(results, a.out, baseline)
        print(a.out)
    if a.json:
        Path(a.json).write_text(json.dumps([r for r, _, _ in results], indent=1))


if __name__ == "__main__":
    main()
