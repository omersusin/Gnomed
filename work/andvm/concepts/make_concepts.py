"""Rough concepts A/B/C for andvm (REDESIGN.md step 3).

Shapes are the measured potrace masks from work/andvm/geometry.json (r1 = back peak,
r0 = front peak).  Colours measured: green #39bb7c, teal #1e5566, ground #0b2f3a.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

from shapely import affinity  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402
from svgpathtools import parse_path  # noqa: E402

HERE = Path(__file__).resolve().parent
G = json.loads((HERE.parent / "geometry.json").read_text())

GREEN, GREEN_TOP, GREEN_SIDE = "#39bb7c", "#5cd99a", "#2a9a63"
TEAL, TEAL_TOP, TEAL_SIDE = "#1e5566", "#2f849c", "#174a57"
LIGHT_TEAL = "#4aa7bf"


def dg(d, samples=700):
    polys = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        polys.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    return unary_union([p for p in polys if p.area > 0.01])


def placed(geoms, box):
    u = unary_union(geoms)
    x0, y0, x1, y1 = u.bounds
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    tx = (bx0 + bx1) / 2 - s * (x0 + x1) / 2
    ty = (by0 + by1) / 2 - s * (y0 + y1) / 2
    return [affinity.translate(affinity.scale(g, s, s, origin=(0, 0)), tx, ty) for g in geoms]


def peaks(box):
    back = dg(G["parts"]["r1"]["d"])
    front = dg(G["parts"]["r0"]["d"])
    b, f = placed([back, front], box)
    return b, f


def A():
    """L1: the two peaks themselves become thick enamel objects."""
    ic = gk.Icon("andvm A - the two peaks as thick objects")
    b, f = peaks((16, 44, 112, 118))
    solid(ic, b, face=[(0, TEAL_TOP), (1, TEAL)], depth=6, side=TEAL_SIDE, layer="back")
    solid(ic, f, face=[(0, GREEN_TOP), (1, GREEN)], depth=7, side=GREEN_SIDE, layer="front")
    return ic


def B():
    """L2: a VM box (device) carrying the two peaks embossed on its front."""
    ic = gk.Icon("andvm B - a VM box with the peaks on the front")
    body = rounded(box(16, 38, 104, 108), 10)
    solid(ic, body, face=[(0, TEAL_TOP), (1, TEAL)], depth=10, side=TEAL_SIDE, layer="box")
    lid = rounded(box(16, 30, 104, 44), 7)
    solid(ic, lid, face=[(0, LIGHT_TEAL), (1, TEAL_TOP)], depth=5, side=TEAL_SIDE, layer="lid")
    b, f = peaks((34, 54, 94, 100))
    solid(ic, b, face=[(0, LIGHT_TEAL), (1, TEAL_TOP)], depth=3, side=TEAL_SIDE, layer="mark-back")
    solid(ic, f, face=[(0, GREEN_TOP), (1, GREEN)], depth=4, side=GREEN_SIDE, layer="mark-front")
    return ic


def C():
    """L2: a glass globe (a VM sandbox) holding the two peaks."""
    ic = gk.Icon("andvm C - a glass globe holding the peaks")
    orb = circ(64, 62, 42)
    solid(ic, orb, face=[(0, "#c9f2f5"), (0.5, "#7fd8e2"), (1, "#3fb3c4")], depth=3,
          side="#2a8fa0", layer="orb")
    b, f = peaks((38, 60, 92, 98))
    solid(ic, b, face=[(0, TEAL_TOP), (1, TEAL)], depth=3, side=TEAL_SIDE, layer="island-back")
    solid(ic, f, face=[(0, GREEN_TOP), (1, GREEN)], depth=4, side=GREEN_SIDE, layer="island-front")
    glow = circ(50, 40, 15).intersection(orb)
    ic.path(geom_d(glow), ic.radial([(0, "#ffffff", 0.85), (1, "#ffffff", 0)], 50, 40, 15),
            layer_id="orb-glint")
    rim = orb.difference(down(orb, 2.2))
    ic.path(geom_d(rim), "#ffffff", opacity=0.5, layer_id="orb-rim")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(HERE / f"{name}.svg")
        print("wrote", name)
