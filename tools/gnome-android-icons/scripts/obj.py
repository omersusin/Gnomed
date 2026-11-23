"""Object-building helpers for GNOME REDESIGNS (references/redesign.md).

A GNOME app icon is a physical object seen from the front: every part has a FACE
(lit from the top, curved faces get a gradient), a SIDE (its thickness, visible
below the face) and often a thin TOP LIGHT on its upper edge. Holes and recesses
show an inner wall at the top. These helpers build exactly that from shapely
geometry, so a redesign.py is short and readable.

    from obj import *            # gk, shapes, solid(), recess(), hole(), toplight()
    ic = gk.Icon("App - GNOME redesign")
    body = rounded(box(20, 30, 108, 110), 10)
    solid(ic, body, face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=6, layer="body")
    hole(ic, circ(64, 64, 10), layer="lens")
    ic.save("work/app/app.svg")

Units: the 128 x 128 GNOME canvas. Palette: GNOME HIG (references/redesign.md).
Worked examples: examples/redesign/build_examples.py.
"""
import sys
from pathlib import Path

import numpy as np
from shapely import affinity
from shapely.geometry import Point, Polygon, box  # noqa: F401  (re-exported)
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gnome_kit as gk  # noqa: E402

__all__ = ["gk", "Point", "Polygon", "box", "unary_union", "affinity", "np",
           "geom_d", "rounded", "circ", "ellipse", "poly", "down", "move", "scale", "side_of",
           "solid", "recess", "hole", "toplight", "Grad"]


# ---------- shapes ----------
def _ring(coords):
    pts = list(coords)
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts[:-1]) + "Z"


def geom_d(g):
    """shapely (Multi)Polygon -> SVG path d (draw with fill-rule evenodd for holes)."""
    if g.is_empty:
        return ""
    polys = [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
    return "".join(_ring(p.exterior.coords) + "".join(_ring(h.coords) for h in p.interiors) for p in polys)


def rounded(g, r):
    """Round every corner of a shape by r (convex and concave).
    A part thinner than 2r used to VANISH (an 18-unit pill with r 9, a 12-unit turf strip with r 6 -
    2026-11-23, gate empty_layer): then r shrinks until the part survives (a full pill end)."""
    out = g.buffer(-r, quad_segs=24).buffer(2 * r, quad_segs=24).buffer(-r, quad_segs=24)
    while out.is_empty and not g.is_empty and r > 0.05:
        r *= 0.8
        out = g.buffer(-r, quad_segs=24).buffer(2 * r, quad_segs=24).buffer(-r, quad_segs=24)
    return out


def circ(cx, cy, r):
    return Point(cx, cy).buffer(r, quad_segs=48)


def ellipse(cx, cy, rx, ry):
    return affinity.scale(Point(cx, cy).buffer(1, quad_segs=48), rx, ry)


def poly(points, r=0):
    p = Polygon(points).buffer(0)
    return rounded(p, r) if r else p


def down(g, dy):
    return affinity.translate(g, 0, dy)


def move(g, dx, dy):
    return affinity.translate(g, dx, dy)


def scale(g, s, about=(64, 64)):
    return affinity.scale(g, s, s, origin=about)


def side_of(g, depth):
    """The visible thickness: the shape swept down by `depth` (starts at 0.8 so no
    halo of the side colour appears along the face's top edge)."""
    return unary_union([affinity.translate(g, 0, t) for t in np.linspace(0.8, depth, 10)])


# ---------- fills ----------
class Grad(str):
    """A linear gradient in any direction that still works everywhere a hex colour does
    (its value IS the middle colour, so shade(), comparisons and old code keep working).
    solid()/recess() draw it as a real SVG gradient across the drawn shape:

        face = Grad([(0, "#ffa11e"), (0.5, "#f25d4b"), (1, "#c01c28")], angle=90)
        angle: 90 = top -> bottom, 0 = left -> right, 45 = top-left -> bottom-right.

    Never paint a gradient as several flat bands (two or more touching shapes in
    near colours): that looks melted/broken. One shape + one Grad."""

    def __new__(cls, stops, angle=90.0):
        stops = [(float(o), c) for o, c in stops]
        o = str.__new__(cls, stops[len(stops) // 2][1])
        o.stops, o.angle = stops, float(angle)
        return o

    def __reduce__(self):
        return (Grad, (self.stops, self.angle))


def _grad_ends(g, angle):
    """The two end points of a gradient at `angle` that spans shape g exactly."""
    import math
    u = np.array([math.cos(math.radians(angle)), math.sin(math.radians(angle))])
    geoms = getattr(g, "geoms", [g])
    pts = np.array([c for q in geoms for c in q.exterior.coords])
    t = pts @ u
    c = np.array(g.centroid.coords[0])
    tc = c @ u
    return c + (t.min() - tc) * u, c + (t.max() - tc) * u


def _fill(ic, f, g, vertical=True):
    if isinstance(f, Grad):
        p0, p1 = _grad_ends(g, f.angle)
        return ic.linear(f.stops, p0[0], p0[1], p1[0], p1[1])
    if isinstance(f, str):
        return f
    x0, y0, x1, y1 = g.bounds
    return ic.linear(f, 0, y0, 0, y1) if vertical else ic.linear(f, x0, 0, x1, 0)


# ---------- parts ----------


def solid(ic, g, face, depth=4, side=None, top=True, layer="part"):
    """One physical part.  face: hex, gradient stops [(0, '#hex'), (1, '#hex')] (top->bottom),
    or Grad(stops, angle) for a gradient in any direction (a measured brand gradient).
    side: hex the side colours are derived from (default: the face's last stop);
    depth: thickness in px (GNOME: 2 for discs/thin parts, 4 for plates, 6-12 for boxes)."""
    x0, _, x1, _ = g.bounds
    base = side or (face if isinstance(face, str) else face[-1][1])
    if depth:
        ic.path(geom_d(side_of(g, depth)), ic.chin_gradient(base, x0, x1, min(12, (x1 - x0) / 4)),
                layer_id=f"{layer}-side", fill_rule="evenodd")
    ic.path(geom_d(g), _fill(ic, face, g), layer_id=f"{layer}-face", fill_rule="evenodd")
    if top:
        toplight(ic, g, layer=layer)


def toplight(ic, g, width=1.4, color="#ffffff", opacity=0.55, layer="part"):
    """Thin light along the upper edges (light comes from the top)."""
    rim = g.difference(down(g, width))
    ic.path(geom_d(rim), color, opacity=opacity, layer_id=f"{layer}-toplight", fill_rule="evenodd")


def recess(ic, g, face, wall=3.0, wall_opacity=0.16, layer="recess"):
    """A part sunk INTO the surface (screen, enamel inlay, label): its top inner wall shows."""
    ic.path(geom_d(g), _fill(ic, face, g), layer_id=f"{layer}-face", fill_rule="evenodd")
    ic.path(geom_d(g.difference(down(g, wall))), "#000000", opacity=wall_opacity,
            layer_id=f"{layer}-wall", fill_rule="evenodd")


def hole(ic, g, color=("#241f31", "#3d3846"), wall=4.0, layer="hole"):
    """A real hole (keyhole, lens, slot): dark body, darker top wall."""
    recess(ic, g, [(0, color[0]), (1, color[1])], wall=wall, wall_opacity=0.45, layer=layer)
