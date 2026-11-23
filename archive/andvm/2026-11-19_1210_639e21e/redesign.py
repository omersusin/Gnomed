#!/usr/bin/env python3
"""andvm - Gnomed redesign.

Approved (design.md): A - the two peaks themselves become thick enamel objects
(free object, no plate).  The back peak (teal) stands behind the front peak
(green); both on the 118 baseline.  Shapes measured from work/andvm/geometry.json
(r1 = back, r0 = front); brand colours #39bb7c / #1e5566.

Build:  python3 tools/make_icon.py andvm      (runs this file, then review + gate)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

from shapely.geometry import Polygon  # noqa: E402
from svgpathtools import parse_path  # noqa: E402

SLUG = Path(__file__).resolve().parent.name
G = json.loads((Path(__file__).resolve().parent / "geometry.json").read_text())

GREEN, GREEN_TOP, GREEN_SIDE = "#39bb7c", "#5cd99a", "#2a9a63"
TEAL, TEAL_TOP, TEAL_SIDE = "#1e5566", "#2f849c", "#174a57"


def dg(d, samples=240):
    polys = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        polys.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    u = unary_union([p for p in polys if p.area > 0.01])
    return u.simplify(0.12, preserve_topology=True)


def placed(geoms, box_):
    u = unary_union(geoms)
    x0, y0, x1, y1 = u.bounds
    bx0, by0, bx1, by1 = box_
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    tx = (bx0 + bx1) / 2 - s * (x0 + x1) / 2
    ty = (by0 + by1) / 2 - s * (y0 + y1) / 2
    return [affinity.translate(affinity.scale(g, s, s, origin=(0, 0)), tx, ty) for g in geoms]


def design():
    ic = gk.Icon("AndVM - Gnomed (two peaks as thick objects)")
    back = dg(G["parts"]["r1"]["d"])
    front = dg(G["parts"]["r0"]["d"])
    b, f = placed([back, front], (9, 27, 119, 112))
    solid(ic, b, face=[(0, TEAL_TOP), (1, TEAL)], depth=5, side=TEAL_SIDE, layer="back")
    solid(ic, f, face=[(0, GREEN_TOP), (1, GREEN)], depth=6, side=GREEN_SIDE, layer="front")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
