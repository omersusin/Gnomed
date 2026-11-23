"""Rough concepts A/B/C for horus (REDESIGN.md step 3).

Measured masks from work/horus/geometry.json: r0 = the green eye + spiral + pupil
and the brow (3 subpaths), holes = the dark almond ring around the pupil.
Green #80eb12, ground #17231a.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

from shapely import affinity  # noqa: E402
from shapely.geometry import LineString, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402
from svgpathtools import parse_path  # noqa: E402

HERE = Path(__file__).resolve().parent
G = json.loads((HERE.parent / "geometry.json").read_text())

GREEN, GREEN_TOP, GREEN_SIDE = "#80eb12", "#a8ff5c", "#57b800"
DARK1, DARK2 = "#173a1c", "#2a5a33"


def dg(d, samples=700):
    polys = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        polys.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    return unary_union([p for p in polys if p.area > 0.01])


def fit(geoms, box):
    u = unary_union(geoms)
    x0, y0, x1, y1 = u.bounds
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    tx = (bx0 + bx1) / 2 - s * (x0 + x1) / 2
    ty = (by0 + by1) / 2 - s * (y0 + y1) / 2
    return ([affinity.translate(affinity.scale(g, s, s, origin=(0, 0)), tx, ty) for g in geoms],
            (s, tx, ty))


def T(pt, tr):
    s, tx, ty = tr
    return (s * pt[0] + tx, s * pt[1] + ty)


def A():
    """L1: the eye itself as a thick green enamel amulet (the sclera is a real hole)."""
    ic = gk.Icon("horus A - the eye as a thick green enamel amulet")
    outer = dg(G["parts"]["r0"]["d"])
    band = dg(G["parts"]["holes"]["d"])
    (outer, band), tr = fit([outer, band], (16, 26, 112, 102))
    face = outer.difference(band)
    depth = 5
    side = side_of(outer, depth).difference(side_of(band, depth))
    x0, _, x1, _ = outer.bounds
    ic.path(geom_d(side), ic.chin_gradient(GREEN_SIDE, x0, x1, min(12, (x1 - x0) / 4)),
            layer_id="eye-side", fill_rule="evenodd")
    ic.path(geom_d(face), ic.linear([(0, GREEN_TOP), (0.55, GREEN), (1, GREEN_SIDE)],
                                    0, face.bounds[1], 0, face.bounds[3]),
            layer_id="eye-face", fill_rule="evenodd")
    toplight(ic, face, width=1.3, opacity=0.5, layer="eye")
    s, tx, ty = tr
    pc = (58.65 * s + tx, 49.1 * s + ty)
    glint = circ(pc[0] - 3.2, pc[1] - 3.4, 4.2).intersection(face)
    ic.path(geom_d(glint), ic.radial([(0, "#f4ffe0", 0.9), (1, "#ffffff", 0)],
                                     pc[0] - 3.2, pc[1] - 3.4, 4.2), layer_id="pupil-glint")
    return ic


def B():
    """L2: a loupe: a green glass lens in a dark ring, the eye's spiral as the handle."""
    ic = gk.Icon("horus B - the eye as a green glass loupe")
    t = np.linspace(0, 3.4 * np.pi, 160)
    rr = 2 + 1.75 * t
    hx = 100 + rr * np.cos(t)
    hy = 95 + rr * np.sin(t)
    handle = LineString(list(zip(hx, hy))).buffer(4.2, cap_style=1, join_style=1)
    solid(ic, handle, face=[(0, GREEN_TOP), (1, GREEN)], depth=3, side="#2ec27e", layer="handle")
    ring = circ(62, 58, 40).difference(circ(62, 58, 31))
    solid(ic, ring, face=[(0, "#3d3846"), (0.5, "#241f31"), (1, "#1a1620")], depth=6,
          side="#111018", layer="ring")
    lens = circ(62, 58, 31)
    solid(ic, lens, face=[(0, "#b6ffc4"), (0.4, GREEN), (1, "#1f8a4a")], depth=2,
          side="#1a6e3c", layer="lens")
    for r, op in ((23, 0.22), (15, 0.16)):
        ic.path(geom_d(circ(62, 58, r).difference(circ(62, 58, r - 1.5))), "#ffffff",
                opacity=op, layer_id=f"glass-ring{r}")
    hole(ic, circ(62, 58, 10), color=(DARK1, DARK2), wall=3, layer="pupil")
    glint = circ(50, 45, 8).intersection(lens)
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.8), (1, "#ffffff", 0)], 50, 45, 8),
            layer_id="lens-glint")
    return ic


def C():
    """L2: a camera lens with the eye reflected in the green glass."""
    ic = gk.Icon("horus C - a camera lens with the eye reflected in the glass")
    ring = circ(64, 62, 44).difference(circ(64, 62, 34))
    solid(ic, ring, face=[(0, "#5e5c64"), (0.5, "#3d3846"), (1, "#241f31")], depth=6,
          side="#241f31", layer="ring")
    lens = circ(64, 62, 34)
    solid(ic, lens, face=[(0, "#7dffa0"), (0.45, GREEN), (1, "#1f7a44")], depth=2,
          side="#1a6e3c", layer="lens")
    almond = ellipse(64, 61, 25, 8).difference(ellipse(64, 61, 25, 6))
    brow = ellipse(64, 49, 28, 5.5).difference(ellipse(64, 49, 28, 4.2))
    refl = unary_union([almond, brow, circ(59, 61, 6.5)]).intersection(lens)
    ic.path(geom_d(refl), "#e6ffe9", opacity=0.6, layer_id="eye-reflection")
    for r, op in ((25, 0.2), (17, 0.14)):
        ic.path(geom_d(circ(64, 62, r).difference(circ(64, 62, r - 1.5))), "#ffffff",
                opacity=op, layer_id=f"glass-ring{r}")
    glint = circ(50, 47, 9).intersection(lens)
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.8), (1, "#ffffff", 0)], 50, 47, 9),
            layer_id="lens-glint")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(HERE / f"{name}.svg")
        print("wrote", name)
