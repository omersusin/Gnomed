#!/usr/bin/env python3
"""Technical lint for a finished icon SVG.  Passing it proves the file is clean,
editable vector art that fits the GNOME canvas - it proves NOTHING about beauty
or GNOME resemblance (that is the visual review's job).

FAIL (must fix):  <image>/data: URIs/raster, <script>, external references,
                  <foreignObject>, missing viewBox 0 0 128 128, content outside canvas,
                  shadow/glow pixels outside the silhouette (blur filters)
WARN (justify):   <text> (fonts are not portable - convert to paths), filters,
                  masks, strokes on large shapes, > 24 colours, low HIG share,
                  bbox far from every template shape, no chin detected,
                  file > 60 KB, empty <title>

Usage: lint_svg.py ICON.svg [...] [--json]
Exit code 1 if any FAIL.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg  # noqa: E402
from measure_style import measure  # noqa: E402
import numpy as np  # noqa: E402

TEMPL = {"circle": (120, 122), "square": (104, 104), "portrait": (88, 112), "landscape": (112, 88)}


def lint(path):
    txt = Path(path).read_text(encoding="utf-8", errors="replace")
    fails, warns = [], []
    low = txt.lower()
    if re.search(r"<image\b", low) or "data:image" in low or re.search(r"base64", low):
        fails.append("embedded raster (<image>/data:/base64) - final art must be real vector paths")
    if "<script" in low:
        fails.append("<script> present")
    if "<foreignobject" in low:
        fails.append("<foreignObject> present")
    for m in re.finditer(r'(?:xlink:)?href\s*=\s*"([^"]+)"', txt):
        if not m.group(1).startswith("#"):
            fails.append(f"external reference: {m.group(1)[:60]}")
    vb = re.search(r'viewBox\s*=\s*"([^"]+)"', txt)
    if not vb or [float(x) for x in re.split(r"[\s,]+", vb.group(1).strip())] != [0, 0, 128, 128]:
        fails.append('viewBox must be "0 0 128 128"')
    if "<text" in low:
        warns.append("<text> element: convert lettering to paths (fonts differ per device)")
    if "fegaussianblur" in low or "fedropshadow" in low:
        fails.append("blur / drop-shadow filter: GNOME icons never cast blurred shadows (the launcher adds context shadow)")
    elif "<filter" in low:
        warns.append("<filter> used: GNOME icons avoid filters; renderers (and Android conversion) differ")
    if "<mask" in low or "<clippath" in low:
        warns.append("mask/clipPath used: fine in moderation, but Android VectorDrawable conversion may need flattening")
    if not re.search(r"<title[^>]*>[^<]+</title>", txt):
        warns.append("no <title>: add the app name")
    kb = len(txt.encode()) / 1024
    if kb > 60:
        warns.append(f"file is {kb:.0f} KB: simplify paths (official median ~12 paths)")
    # pixel checks
    im = np.asarray(render_svg(path, 512)).astype(float)
    a = im[..., 3]
    edge = np.concatenate([a[:2].ravel(), a[-2:].ravel(), a[:, :2].ravel(), a[:, -2:].ravel()])
    if (edge > 8).mean() > 0.02:
        fails.append("artwork touches the canvas edge: keep inside the template shapes")
    semi = ((a > 4) & (a < 200)).sum() / max((a > 4).sum(), 1)
    if semi > 0.10:
        fails.append(f"{semi * 100:.0f}% of painted pixels are semi-transparent: looks like a blurred shadow/glow outside the silhouette")
    m = measure(path)
    best, bestd = None, 1e9
    for k, (tw, th) in TEMPL.items():
        dd = abs(m["w"] - tw) + abs(m["h"] - th)
        if dd < bestd:
            best, bestd = k, dd
    if bestd > 22 and not (m["w"] > 90 and m["h"] > 90):
        warns.append(f"visual size {m['w']}x{m['h']} far from template shapes (closest {best} {TEMPL[best]}): check visual weight next to references")
    if m["b"] > 127 or m["b"] < 110:
        warns.append(f"bottom edge at y={m['b']}: official icons sit on 116-126 (baseline guide 117)")
    if m.get("chin") is None:
        warns.append("no darker front face (chin) detected: OK only for deliberately flat symbols - say why")
    if m["colors"] > 24:
        warns.append(f"{m['colors']} distinct colours: official median is 10")
    if m["strokes"] > 6:
        warns.append(f"{m['strokes']} stroked elements: GNOME/MoreWaita prefer filled paths")
    return {"file": str(path), "fails": fails, "warns": warns, "metrics": m, "closest_template": best}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    results = [lint(p) for p in a.svgs]
    bad = False
    if a.json:
        print(json.dumps(results, indent=1))
    for r in results:
        bad |= bool(r["fails"])
        if not a.json:
            status = "FAIL" if r["fails"] else ("WARN" if r["warns"] else "OK")
            m = r["metrics"]
            print(f"[{status}] {r['file']}  size {m['w']}x{m['h']} bottom {m['b']} chin {m['chin']} colours {m['colors']} (HIG {m['hig']}%)  closest template: {r['closest_template']}")
            for x in r["fails"]:
                print("   FAIL:", x)
            for x in r["warns"]:
                print("   warn:", x)
    if not a.json:
        print("\nReminder: lint checks hygiene only. Visual review against the source and real GNOME icons decides quality.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
