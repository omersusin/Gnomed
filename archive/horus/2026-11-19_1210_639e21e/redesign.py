#!/usr/bin/env python3
"""horus - Gnomed redesign.

Approved (design.md): A - the Eye of Horus itself becomes a thick green enamel
amulet (free object, no plate).  Owner fix: the sclera (the almond around the
pupil) stays TRANSPARENT - the wallpaper shows through it, like the source's
background; the pupil stays green.  Shapes measured from work/horus/geometry.json
(r0 = eye + spiral + pupil + brow, holes = the sclera band); brand green #80eb12.

Build:  python3 tools/make_icon.py horus      (runs this file, then review + gate)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

from shapely.geometry import Polygon  # noqa: E402
from svgpathtools import parse_path  # noqa: E402

SLUG = Path(__file__).resolve().parent.name
G = json.loads((Path(__file__).resolve().parent / "geometry.json").read_text())

GREEN, GREEN_TOP, GREEN_SIDE = "#80eb12", "#a8ff5c", "#57b800"


def dg(d, samples=260):
    polys = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        polys.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    u = unary_union([p for p in polys if p.area > 0.01])
    return u.simplify(0.1, preserve_topology=True)


def fit(geoms, box_):
    u = unary_union(geoms)
    x0, y0, x1, y1 = u.bounds
    bx0, by0, bx1, by1 = box_
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    tx = (bx0 + bx1) / 2 - s * (x0 + x1) / 2
    ty = (by0 + by1) / 2 - s * (y0 + y1) / 2
    return ([affinity.translate(affinity.scale(g, s, s, origin=(0, 0)), tx, ty) for g in geoms],
            (s, tx, ty))


def design():
    ic = gk.Icon("Horus - Gnomed (the eye as a thick green enamel amulet)")
    outer = dg(G["parts"]["r0"]["d"])
    band = dg(G["parts"]["holes"]["d"])
    (outer, band), tr = fit([outer, band], (9, 28.4, 119, 113))
    face = outer.difference(band)
    depth = 5
    # side: the outer thickness, with the sclera swept out so the wallpaper shows through
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


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
