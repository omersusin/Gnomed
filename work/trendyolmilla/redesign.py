#!/usr/bin/env python3
"""trendyolmilla - Gnomed redesign.
Main (Symbol) A: a paper shopping bag in the brand gradient. Faithful B: a price tag - the
wordmark itself, white on the gradient, a real hole and a string. Disc C: a round hat box.
Rimmed D: a wicker shopping basket with a fabric tag."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
PURPLE = RAMP["Purple"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
BROWN = RAMP["Brown"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a white paper shopping bag: a purple-gradient printed panel with the white
    wordmark, a folded top, grey rope handles."""
    ic = gk.Icon("trendyolmilla - symbol")
    body = poly([(18, 52), (110, 52), (106, 116), (22, 116)], 5)
    handles = unary_union([ellipse(x, 52, 10, 14).exterior.buffer(2.6).intersection(box(0, 0, 128, 53))
                           for x in (43, 85)])
    solid(ic, handles, face=[(0, "#9a9996"), (1, "#5e5c64")], depth=1.5, side="#3d3846", top=False, layer="handles")
    solid(ic, body, face=[(0, "#ffffff"), (0.6, LIGHT[3]), (1, LIGHT[4])], depth=6, side="#77767b", layer="bag")
    fold = box(18, 52, 110, 62).intersection(body)
    ic.path(geom_d(fold), "#5e5c64", opacity=0.16, layer_id="bag-fold")
    panel = rr(26, 66, 102, 108, 4)
    solid(ic, panel, face=gradient(SLUG, panel), depth=2, side=PURPLE[4], top=False, layer="panel")
    put_mark(ic, SLUG, (30, 76, 98, 100), face="#ffffff")
    return ic


def B():
    """Faithful - a price tag: the wordmark big and white on the brand gradient, a cut corner,
    a real punched hole and a thick string loop. Closest to the logo, still a real object."""
    ic = gk.Icon("trendyolmilla - faithful")
    tag = poly([(18, 42), (84, 42), (106, 64), (106, 106), (98, 114), (20, 114), (12, 106), (12, 50)], 7)
    hole_c = (30, 52)
    tag = tag.difference(circ(hole_c[0], hole_c[1], 5.4))
    string = circ(30, 52, 16).difference(circ(30, 52, 11.5)).intersection(box(0, 0, 32, 128))
    solid(ic, string, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=1, side=LIGHT[4], top=False, layer="string")
    solid(ic, tag, face=gradient(SLUG, tag), depth=5, side=PURPLE[4], layer="tag")
    solid(ic, circ(hole_c[0], hole_c[1], 8.6).difference(circ(hole_c[0], hole_c[1], 5.4)),
          face=[(0, LIGHT[1]), (1, "#9a9996")], depth=2, side="#77767b", top=False, layer="grommet")
    put_mark(ic, SLUG, (28, 72, 100, 102), face="#ffffff")
    return ic


def C():
    """Disc - a round hat box: a purple cylinder with a wide lid, a ribbon round its middle tied
    in a bow, and the wordmark on a paper label on the front."""
    ic = gk.Icon("trendyolmilla - disc")
    body = rr(20, 56, 108, 114, 12)
    solid(ic, body, face=gradient(SLUG, body), depth=6, side=PURPLE[4], layer="body")
    lid = rr(12, 40, 116, 66, 10)
    solid(ic, lid, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=5, side=PURPLE[4], layer="lid")
    top = ellipse(64, 42, 52, 8)
    solid(ic, top, face=[(0, "#f3ebf8"), (0.6, PURPLE[1]), (1, PURPLE[2])], depth=3, side=PURPLE[3], layer="lid-top")
    label = rr(22, 72, 106, 108, 3)
    solid(ic, label, face=gradient(SLUG, label), depth=2, side=PURPLE[4], top=False, layer="label")
    put_mark(ic, SLUG, (30, 77, 98, 101), face="#ffffff")
    knot = rr(102, 52, 116, 66, 4)
    solid(ic, knot, face=[(0, "#efe6f6"), (1, PURPLE[2])], depth=2, side=PURPLE[4], layer="bow-knot")
    tail = poly([(104, 64), (100, 100), (107, 94), (113, 102), (112, 64)], 2)
    solid(ic, tail, face=[(0, "#efe6f6"), (1, PURPLE[2])], depth=2.5, side=PURPLE[4], layer="bow-tail")
    return ic


def D():
    """Rimmed - a wicker shopping basket: brown weave, an arc handle, a fabric tag with the
    wordmark hanging on the front."""
    ic = gk.Icon("trendyolmilla - rimmed")
    body = poly([(14, 56), (114, 56), (102, 116), (26, 116)], 8)
    solid(ic, body, face=[(0, "#d0a568"), (0.55, "#b07f45"), (1, "#8b5a2b")], depth=6, side="#5b3a1a", layer="basket")
    for y, h in ((68, 3.0), (84, 3.0), (100, 3.0)):
        band = box(16, y, 112, y + h).intersection(body)
        ic.path(geom_d(band), "#5b3a1a", opacity=0.45, layer_id=f"weave-{y}")
    for x in (36, 56, 76, 96):
        rib = box(x - 1.5, 58, x + 1.5, 116).intersection(body)
        ic.path(geom_d(rib), "#f6f5f4", opacity=0.18, layer_id=f"rib-{x}")
    handle = circ(64, 58, 36).difference(circ(64, 58, 29)).intersection(box(0, 0, 128, 59))
    solid(ic, handle, face=[(0, "#d0a568"), (1, "#8b5a2b")], depth=5, side="#5b3a1a", layer="handle")
    tag = rr(30, 60, 98, 100, 3)
    solid(ic, tag, face=gradient(SLUG, tag), depth=2, side=PURPLE[4], layer="tag")
    put_mark(ic, SLUG, (34, 64, 94, 96), face="#ffffff")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
