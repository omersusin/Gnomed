#!/usr/bin/env python3
"""Size / baseline audit of every icon in the pack (all styles).

    python3 tools/size_audit.py            # report outliers
    python3 tools/size_audit.py --all      # every icon

Measures each app/src/main/res/drawable-nodpi PNG on the 128 grid (alpha > 40):
bounds, bottom edge, coverage, and compares with the GNOME geometry of its style:
  faithful  (plate 104 + chin)   bottom 114-118, larger side 100-108
  disc / rimmed (disc 118 + chin) bottom 120-125, larger side 112-120
  symbol / redesigned objects   bottom 108-127, larger side >= 88, nothing above y 4 (as check_icon)
                                 (free objects stand on the baseline, ~118)
  any                           coverage >= 18 % (a thin outline alone looks lost)
Redesigned apps (work/<slug>/redesign.py) are objects in every slot -> object rules.
Exit 1 if any icon is outside its range.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ND = ROOT / "app/src/main/res/drawable-nodpi"


def measure(p):
    a = np.asarray(Image.open(p).convert("RGBA").resize((128, 128), Image.LANCZOS))[..., 3] > 40
    ys, xs = np.where(a)
    if not len(xs):
        return None
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                w=int(xs.max() - xs.min() + 1), h=int(ys.max() - ys.min() + 1), cov=float(a.mean()))


RANGES = {"faithful": (114, 118, 100, 108), "disc": (120, 125, 112, 120), "rimmed": (120, 125, 112, 120),
          "object": (108, 127, 88, 120)}   # = check_icon's free-object baseline 108-126.5 (one rule for both, 2026-11-23)


def problems(m, kind):
    b0, b1, s0, s1 = RANGES[kind]
    out = []
    side = max(m["w"], m["h"])
    if m["y1"] < b0:
        out.append(f"floats: bottom {m['y1']} (< {b0})")
    if m["y1"] > b1:
        out.append(f"too low: bottom {m['y1']} (> {b1})")
    if side < s0:
        out.append(f"small: {m['w']}x{m['h']} (< {s0})")
    if side > s1:
        out.append(f"too big: {m['w']}x{m['h']} (> {s1})")
    if m["y0"] < 4 or m["x0"] < 4 or m["x1"] > 123:
        out.append(f"touches edge: x {m['x0']}-{m['x1']} y {m['y0']}-{m['y1']}")
    if m["cov"] < 0.18:
        out.append(f"coverage {m['cov']:.0%}")
    return out


def main():
    styles = json.loads((ROOT / "pack/styles.json").read_text())["icons"]
    names = {}
    for app, st in styles.items():
        names[app] = (app, "faithful")
        for s, d in st.items():
            names[d] = (app, s)
    bad = 0
    for p in sorted(ND.glob("*.png")):
        if p.stem not in names:
            continue
        m = measure(p)
        if m is None:
            continue
        app, st = names[p.stem]
        kind = "object" if (st == "symbol" or (ROOT / f"work/{app}/redesign.py").exists()) else st
        pr = problems(m, kind)
        if pr or "--all" in sys.argv:
            print(f"{p.stem:30s} {st:8s} {m['w']:3d}x{m['h']:<3d} bottom {m['y1']:3d} cov {m['cov']:.0%}  " + "; ".join(pr))
        bad += bool(pr)
    print(f"{bad} icon(s) outside the ranges")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
