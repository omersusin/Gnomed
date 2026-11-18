#!/usr/bin/env python3
"""Measure the visual/structural style of SVG app icons.

Run it on the bundled official GNOME library to (re)derive the numbers quoted
in references/measured-style.md, or on your own icon to see where it sits
relative to that distribution.

Usage:
  measure_style.py ICON.svg [...]            # table to stdout
  measure_style.py --library official        # whole bundled official set
  measure_style.py ICON.svg --compare official   # your icon vs. library stats
  measure_style.py ... --json out.json

Metrics (all in nominal 128-px units):
  bbox l/t/r/b, w, h      opaque bounding box (alpha > 32)
  fill                    opaque area / bbox area (circle ~0.79, square ~0.95)
  area                    painted share of the whole 128 canvas (visual mass; official p10-p90
                          ~0.36-0.66, see references/measured-style.md)
  chin                    estimated height of the darker bottom band (the HIG
                          "front face" / chin), median over central columns
  colors, hig%            distinct solid colours and share within dE<=4 of a
                          HIG palette swatch
  lin/rad/hgrad           linear, radial, horizontal-linear gradient counts
  strokes, filters, imgs  structural red flags for app-icon art
"""
import argparse
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import LIB_ROOT, render_svg, nearest_hig, hex_to_rgb  # noqa: E402
import numpy as np  # noqa: E402
from lxml import etree  # noqa: E402

COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def _luma(rgb):
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def pixel_metrics(svg, scale=4):
    S = 128 * scale
    return metrics_from_rgba(np.asarray(render_svg(svg, S)).astype(float))


def image_metrics(path_or_image, size=512):
    """Same pixel metrics for a raster icon (PNG/WebP), e.g. drawables in an icon pack."""
    from PIL import Image
    im = path_or_image if hasattr(path_or_image, "convert") else Image.open(path_or_image)
    im = im.convert("RGBA").resize((size, size), Image.LANCZOS)
    return metrics_from_rgba(np.asarray(im).astype(float))


def metrics_from_rgba(im):
    S = im.shape[0]
    scale = S / 128.0
    a = im[..., 3]
    ys, xs = np.where(a > 32)
    if len(xs) == 0:
        return {}
    l, r, t, b = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    w, h = r - l, b - t
    fill = float((a[t:b, l:r] > 32).sum()) / (w * h)
    lum = _luma(im[..., :3])
    chins = []
    step = max(1, int(round(scale)))
    for x in range(int(l + 0.3 * w), int(r - 0.3 * w)):
        col = np.where(a[:, x] > 200)[0]
        if len(col) < 8:
            continue
        yb = col.max()
        base = lum[yb - step, x]
        y = yb - step
        while y > t and a[y, x] > 200 and abs(lum[y, x] - base) < 10:
            y -= 1
        if a[y, x] > 200 and lum[y, x] - base > 12:   # lighter face above a darker chin
            chins.append((yb - y) / scale)
    chin = float(np.median(chins)) if len(chins) >= 3 else None
    k = 128 / S
    area = float((a / 255.0).sum()) / (S * S)  # alpha-weighted share of the canvas that is painted
    corners = [a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]
    return dict(l=round(l * k, 1), t=round(t * k, 1), r=round(r * k, 1), b=round(b * k, 1),
                w=round(w * k, 1), h=round(h * k, 1), fill=round(fill, 3), area=round(area, 3),
                chin=None if chin is None else round(chin, 1), opaque_corners=int(sum(c > 200 for c in corners)))


def structural_metrics(svg):
    txt = Path(svg).read_text(encoding="utf-8", errors="replace")
    try:
        root = etree.fromstring(txt.encode(), etree.XMLParser(huge_tree=True, recover=True))
    except Exception:
        root = None
    tags = {}
    hgrad = 0
    if root is not None:
        for el in root.iter():
            if not isinstance(el.tag, str):
                continue
            t = el.tag.split("}")[-1]
            tags[t] = tags.get(t, 0) + 1
            if t == "linearGradient":
                try:
                    y1, y2 = float(el.get("y1", "0").rstrip("%")), float(el.get("y2", "0").rstrip("%"))
                    x1, x2 = float(el.get("x1", "0").rstrip("%")), float(el.get("x2", "1").rstrip("%"))
                    if abs(y1 - y2) < 1e-6 and abs(x1 - x2) > 1e-6:
                        hgrad += 1
                except ValueError:
                    pass
    cols = {c.lower() if len(c) == 7 else "#" + "".join(ch * 2 for ch in c[1:]).lower()
            for c in COLOR_RE.findall(txt)}
    cols.discard("#000000")
    near = [nearest_hig(c)[2] for c in cols]
    hig = sum(1 for d in near if d <= 4)
    strokes = len(re.findall(r'stroke\s*[:=]\s*"?(?!none)[#a-zA-Z]', txt))
    return dict(paths=tags.get("path", 0), rects=tags.get("rect", 0), circles=tags.get("circle", 0) + tags.get("ellipse", 0),
                lin=tags.get("linearGradient", 0), rad=tags.get("radialGradient", 0), hgrad=hgrad,
                colors=len(cols), hig=round(100 * hig / len(cols)) if cols else 0,
                strokes=strokes, filters=tags.get("filter", 0), imgs=tags.get("image", 0),
                masks=tags.get("mask", 0) + tags.get("clipPath", 0), kb=round(len(txt) / 1024, 1))


def measure(svg):
    d = {"icon": Path(svg).stem}
    d.update(pixel_metrics(svg))
    d.update(structural_metrics(svg))
    return d


GROUP_ALIASES = {
    "official": {"gnome-core", "gnome-games", "circle-and-third-party"},   # all real app icons
    "apps": {"gnome-core", "gnome-games", "circle-and-third-party"},
    "core": {"gnome-core"}, "games": {"gnome-games"}, "circle": {"circle-and-third-party"},
    "system": {"adwaita-system"},
}


def library_files(name):
    cat = json.loads((LIB_ROOT / "catalog.json").read_text())
    groups = GROUP_ALIASES.get(name, {name})
    files = [str(LIB_ROOT / e["file"]) for e in cat["icons"] if name == "all" or e["group"] in groups]
    if not files:
        raise SystemExit(f"unknown library group '{name}': use official | core | games | circle | system | all")
    return files


def summarize(rows, keys=("w", "h", "b", "fill", "area", "chin", "colors", "hig", "lin", "rad", "hgrad", "paths", "strokes")):
    out = {}
    for k in keys:
        v = [r[k] for r in rows if r.get(k) is not None]
        if v:
            q = np.percentile(v, [10, 25, 50, 75, 90])
            nd = 3 if max(abs(x) for x in q) < 2 else 1
            out[k] = dict(n=len(v), p10=round(q[0], nd), p25=round(q[1], nd), median=round(q[2], nd),
                          p75=round(q[3], nd), p90=round(q[4], nd))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="*")
    ap.add_argument("--library", help="official (all app icons) | core | games | circle | system | all")
    ap.add_argument("--compare", help="library group to compare the given icons against")
    ap.add_argument("--json")
    a = ap.parse_args()
    files = list(a.svgs)
    if a.library:
        files += library_files(a.library)
    rows = [measure(f) for f in files]
    cols = ["icon", "w", "h", "b", "fill", "area", "chin", "colors", "hig", "lin", "rad", "hgrad", "paths", "strokes", "filters", "imgs"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(str(r.get(c, "")) for c in cols))
    result = {"rows": rows, "summary": summarize(rows)}
    if a.compare:
        lib = [measure(f) for f in library_files(a.compare)]
        ls = summarize(lib)
        result["library_summary"] = ls
        print(f"\nCompared with bundled '{a.compare}' library (p10 / median / p90):")
        for r in rows:
            print(f"- {r['icon']}")
            for k in ("w", "h", "b", "fill", "area", "chin", "colors", "hig"):
                if r.get(k) is None or k not in ls:
                    continue
                s = ls[k]
                flag = "" if s["p10"] <= r[k] <= s["p90"] else "   <-- outside p10..p90"
                print(f"    {k:6} {r[k]:>6}   library {s['p10']} / {s['median']} / {s['p90']}{flag}")
    elif len(rows) > 1:
        print("\nSummary (p10 / p25 / median / p75 / p90):")
        for k, s in result["summary"].items():
            print(f"  {k:7} n={s['n']:3}  {s['p10']} / {s['p25']} / {s['median']} / {s['p75']} / {s['p90']}")
    if a.json:
        Path(a.json).write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
