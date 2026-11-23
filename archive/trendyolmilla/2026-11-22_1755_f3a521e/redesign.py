#!/usr/bin/env python3
"""trendyolmilla - Gnomed redesign.
Main (Symbol) A: a shopping bag in the brand gradient. Faithful B: a clothes hanger. Disc C: a
round hat box. Rimmed D: a parcel box."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
BROWN = RAMP["Brown"]
BLUE = RAMP["Blue"]
PURPLE = RAMP["Purple"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a shopping bag: the brand's blue-violet-pink gradient, a big handle."""
    ic = gk.Icon("trendyolmilla - symbol")
    handle = circ(64, 52, 25).difference(circ(64, 52, 18)).intersection(box(0, 0, 128, 54))
    solid(ic, handle, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=3, side=PURPLE[4], layer="handle")
    body = rr(20, 48, 108, 116, 7)
    solid(ic, body, face=[(0, "#3a1dda"), (0.45, "#9b0c85"), (1, "#d05fa0")], depth=7, side=PURPLE[4], layer="bag")
    toplight(ic, body, width=1.8, opacity=0.5, layer="bag")
    top = rr(20, 48, 108, 58, 5)
    solid(ic, top, face=[(0, "#5a35e8"), (1, "#7a2bc0")], depth=2, side=PURPLE[4], top=False, layer="fold")
    for i, x in enumerate((36, 92)):
        ic.path(geom_d(rr(x - 1, 52, x + 1, 60, 1)), LIGHT[0], opacity=0.35, layer_id=f"fold-line{i}")
    ic.path(geom_d(rr(30, 78, 98, 84, 3)), LIGHT[0], opacity=0.22, layer_id="shine")
    return ic


def B():
    """Faithful - a clothes hanger: blue shoulders, steel hook, a trouser bar."""
    ic = gk.Icon("trendyolmilla - faithful")
    hook = LineString([(64, 30), (64, 22), (70, 16), (76, 22), (72, 28)]).buffer(3.4, cap_style=1, join_style=1)
    solid(ic, hook, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="hook")
    body = poly([(64, 40), (22, 74), (26, 84), (64, 58), (102, 84), (106, 74)], 5)
    solid(ic, body, face=[(0, BLUE[1]), (0.5, BLUE[2]), (1, BLUE[4])], depth=6, side=BLUE[4], layer="hanger")
    toplight(ic, body, width=1.6, opacity=0.6, layer="hanger")
    bar = LineString([(28, 84), (100, 84)]).buffer(4.4, cap_style=1)
    solid(ic, bar, face=[(0, BLUE[1]), (1, BLUE[3])], depth=4, side=BLUE[4], layer="bar")
    toplight(ic, bar, width=1.2, opacity=0.6, layer="bar")
    for x in (28, 100):
        ic.path(geom_d(circ(x, 84, 4.4)), BLUE[4], opacity=0.5, layer_id=f"joint{x}")
    return ic


def C():
    """Disc - a round hat box: light lid, band and body, a violet ribbon and bow."""
    ic = gk.Icon("trendyolmilla - disc")
    body = rr(24, 54, 104, 114, 12)
    solid(ic, body, face=[(0, LIGHT[0]), (0.6, "#f3e3ef"), (1, "#e4c6dc")], depth=7, side="#c9a2bf", layer="body")
    toplight(ic, body, width=1.8, opacity=0.8, layer="body")
    lid = ellipse(64, 54, 42, 12)
    solid(ic, lid, face=[(0, LIGHT[0]), (1, "#efd6e6")], depth=4, side="#c9a2bf", layer="lid")
    rim = ellipse(64, 54, 42, 12).difference(ellipse(64, 54, 36, 8))
    ic.path(geom_d(rim), PURPLE[2], opacity=0.45, layer_id="lid-rim", fill_rule="evenodd")
    band = rr(56, 58, 72, 114, 2)
    solid(ic, band, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=2, side=PURPLE[4], top=False, layer="ribbon")
    bow_l = ellipse(52, 66, 9, 6)
    bow_r = ellipse(76, 66, 9, 6)
    solid(ic, bow_l, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=3, side=PURPLE[4], layer="bow-l")
    solid(ic, bow_r, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=3, side=PURPLE[4], layer="bow-r")
    ic.path(geom_d(circ(64, 66, 4)), PURPLE[4], layer_id="knot")
    return ic


def D():
    """Rimmed - a parcel box: cardboard, tape strip, a shipping label, a this-way-up arrow."""
    ic = gk.Icon("trendyolmilla - rimmed")
    box_ = rr(16, 40, 112, 116, 4)
    solid(ic, box_, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[3])], depth=7, side=BROWN[4], layer="box")
    toplight(ic, box_, width=1.8, opacity=0.5, layer="box")
    lid = rr(16, 40, 112, 62, 4)
    solid(ic, lid, face=[(0, BROWN[1]), (1, BROWN[2])], depth=3, side=BROWN[4], layer="lid")
    ic.path(geom_d(rr(16, 58, 112, 60.5, 1)), BROWN[4], opacity=0.55, layer_id="lid-edge")
    tape = rr(56, 40, 72, 116, 1.5)
    ic.path(geom_d(tape), "#e8d8bd", opacity=0.85, layer_id="tape")
    label = rr(24, 68, 52, 92, 3)
    solid(ic, label, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="label")
    for i, (y, w) in enumerate(((74, 20), (81, 16), (88, 12))):
        ic.path(geom_d(rr(28, y, 28 + w, y + 3, 1)), DARK[2], opacity=0.6, layer_id=f"label-line{i}")
    arrow = poly([(84, 84), (98, 84), (98, 78), (108, 88), (98, 98), (98, 92), (84, 92)], 1.5)
    ic.path(geom_d(arrow), PURPLE[2], opacity=0.85, layer_id="arrow")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
