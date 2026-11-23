"""Rough concepts A/B/C for aurex_browser (REDESIGN.md step 3).

Measured masks from work/aurex_browser/geometry.json: r0/r1 = the white A faces,
r2 = its dark blue side, r3 = the cyan sphere, holes = the counter.
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

LIGHT, MID, DARK, CYAN = "#e6f1fd", "#b1cff5", "#1e57c4", "#59e6dd"


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


def a_parts(box):
    geoms = [dg(G["parts"][k]["d"]) for k in ("r0", "r1", "r2")]
    ball = dg(G["parts"]["r3"]["d"])
    ps = placed(geoms + [ball], box)
    return ps[:3], ps[3]


def A():
    """L1: the white A and the cyan ball themselves become thick objects (no plate)."""
    ic = gk.Icon("aurex_browser A - the A and the glass ball as thick objects")
    (r0, r1, r2), ball = a_parts((19, 8, 109, 113))
    face = unary_union([r0, r1])
    solid(ic, face, face=[(0, "#ffffff"), (0.6, "#e6f1fd"), (1, "#b1cff5")], depth=5,
          side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c9fff9"), (0.5, CYAN), (1, "#2fb9c9")], depth=2, side="#2a9fb0",
          layer="ball")
    glint = circ(60, 78, 5.5).intersection(ball)
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], 60, 78, 5.5),
            layer_id="ball-glint")
    return ic


def B():
    """L2: a blue glass globe (the web) carrying the white A, the cyan ball in its counter."""
    ic = gk.Icon("aurex_browser B - the A and ball on a blue glass globe")
    globe = circ(64, 67, 48)
    solid(ic, globe, face=[(0, "#99c1f1"), (0.45, "#3584e4"), (1, "#1c71d8")], depth=3,
          side="#1a5fb4", layer="globe")
    glint = circ(46, 38, 20).intersection(globe)
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.85), (1, "#ffffff", 0)], 46, 38, 20),
            layer_id="globe-glint")
    for r, op in ((36, 0.2), (26, 0.14)):
        ic.path(geom_d(circ(64, 67, r).difference(circ(64, 67, r - 1.6))), "#ffffff",
                opacity=op, layer_id=f"glass-ring{r}")
    (r0, r1, r2), ball = a_parts((34, 33, 94, 101))
    face = unary_union([r0, r1])
    solid(ic, face, face=[(0, "#ffffff"), (0.55, "#eef6ff"), (1, "#cfe0f5")], depth=2,
          side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c9fff9"), (0.5, CYAN), (1, "#2fb9c9")], depth=2, side="#2a9fb0",
          layer="ball")
    glint2 = circ(60, 82, 4.6).intersection(ball)
    ic.path(geom_d(glint2), ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], 60, 82, 4.6),
            layer_id="ball-glint")
    return ic


def C():
    """L3: the source's blue as a physical enamel tile carrying the raised A and ball."""
    ic = gk.Icon("aurex_browser C - the blue tile with the raised A and ball")
    tile = rounded(box(12, 12, 116, 112), 8)
    solid(ic, tile, face=[(0, "#53a2fa"), (0.5, "#4281ec"), (1, "#305fde")], depth=4,
          side="#1c4fb8", layer="tile")
    (r0, r1, r2), ball = a_parts((24, 16, 104, 104))
    face = unary_union([r0, r1])
    solid(ic, face, face=[(0, "#ffffff"), (0.6, "#e6f1fd"), (1, "#b1cff5")], depth=4,
          side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c9fff9"), (0.5, CYAN), (1, "#2fb9c9")], depth=2, side="#2a9fb0",
          layer="ball")
    glint = circ(60, 72, 5).intersection(ball)
    ic.path(geom_d(glint), ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], 60, 72, 5),
            layer_id="ball-glint")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(HERE / f"{name}.svg")
        print("wrote", name)
