#!/usr/bin/env python3
"""aurex_browser - Gnomed redesign.

Approved (design.md): B - the white A and the cyan ball on a blue glass globe
(free object, no plate).  The globe is the web; the A is the measured source mark
(r0/r1 face, r2 = its dark-blue side colour, holes = the counter); the cyan ball
(r3) sits in the A's lower opening.  Owner fix: the measured r2 band drawn as a
separate path looked cut/crooked, so the A now gets its clean side from the
object's own thickness.

Build:  python3 tools/make_icon.py aurex_browser   (runs this file, then review + gate)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

from shapely.geometry import Polygon  # noqa: E402
from svgpathtools import parse_path  # noqa: E402

SLUG = Path(__file__).resolve().parent.name
G = json.loads((Path(__file__).resolve().parent / "geometry.json").read_text())

GROUND, GROUND_DARK, SIDE = "#53a2fa", "#305fde", "#1e57c4"
A_TOP, A_BOTTOM = "#e6f1fd", "#b1cff5"
BALL, BALL_DARK, BALL_SIDE = "#59e6dd", "#2fb9c9", "#2a9fb0"


def dg(d, samples=260):
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


def a_parts(box_):
    geoms = [dg(G["parts"][k]["d"]) for k in ("r0", "r1")]
    ball = dg(G["parts"]["r3"]["d"])
    ps = placed(geoms + [ball], box_)
    return ps[:2], ps[2]


def design():
    ic = gk.Icon("Aurex Browser - Gnomed (the A and ball on a blue glass globe)")
    globe = circ(64, 67, 48)
    solid(ic, globe, face=[(0, GROUND), (0.45, "#4281ec"), (1, GROUND_DARK)], depth=3,
          side=SIDE, layer="globe")
    glint = circ(46, 38, 20).intersection(globe).difference(globe.difference(globe.buffer(-2.0)))
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.8), (1, "#ffffff", 0)], 46, 38, 20),
            layer_id="globe-glint")
    for r, op in ((36, 0.16), (26, 0.1)):
        ic.path(geom_d(circ(64, 67, r).difference(circ(64, 67, r - 1.5))), "#ffffff",
                opacity=op, layer_id=f"glass-ring{r}")
    (r0, r1), ball = a_parts((34, 33, 94, 101))
    face = unary_union([r0, r1])
    solid(ic, face, face=[(0, A_TOP), (0.6, A_TOP), (1, A_BOTTOM)], depth=2, side=SIDE,
          layer="A")
    solid(ic, ball, face=[(0, "#7fe9e1"), (0.25, "#c4fff8"), (0.55, BALL), (1, BALL_DARK)],
          depth=2, side=BALL_SIDE, top=False, layer="ball")
    bx, by = ball.centroid.x, ball.centroid.y
    br = (ball.bounds[2] - ball.bounds[0]) / 2
    gx, gy, gr = bx - br * 0.5, by - br * 0.45, br * 0.22
    ic.path(geom_d(circ(gx, gy, gr).intersection(ball)),
            ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], gx, gy, gr),
            layer_id="ball-glint")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
