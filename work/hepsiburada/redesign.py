#!/usr/bin/env python3
"""hepsiburada - Gnomed redesign.
Main (Symbol) A: an orange shopping cart. Faithful B: a shop front at night. Disc C: a round price
tag. Rimmed D: a receipt."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
ORANGE = RAMP["Orange"]
YELLOW = RAMP["Yellow"]
RED = RAMP["Red"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a shopping cart: orange basket, steel frame, two wheels."""
    ic = gk.Icon("hepsiburada - symbol")
    frame = LineString([(16, 26), (30, 26), (44, 76), (104, 76)]).buffer(3.4, cap_style=1, join_style=1)
    solid(ic, frame, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="frame")
    basket = poly([(38, 40), (110, 40), (102, 74), (46, 74)], 4)
    solid(ic, basket, face=[(0, ORANGE[1]), (0.5, ORANGE[2]), (1, ORANGE[4])], depth=6, side=ORANGE[4], layer="basket")
    toplight(ic, basket, width=1.8, opacity=0.6, layer="basket")
    for k in range(4):
        x = 52 + k * 15
        line = LineString([(x, 44), (x + 3, 72)]).buffer(1.6)
        ic.path(geom_d(line), ORANGE[4], opacity=0.5, layer_id=f"wire{k}")
    lip = LineString([(38, 40), (110, 40)]).buffer(3.2, cap_style=1)
    solid(ic, lip, face=[(0, ORANGE[1]), (1, ORANGE[3])], depth=2, side=ORANGE[4], top=False, layer="lip")
    for i, x in enumerate((58, 96)):
        wheel = circ(x, 98, 10)
        solid(ic, wheel, face=[(0, DARK[1]), (1, DARK[3])], depth=4, side="#1b1a1f", layer=f"wheel{i}")
        ic.path(geom_d(circ(x, 98, 3.4)), LIGHT[2], opacity=0.8, layer_id=f"hub{i}")
    leg = LineString([(102, 74), (102, 90)]).buffer(3)
    solid(ic, leg, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer="leg")
    return ic


def B():
    """Faithful - a shop front at night: dark facade, lit windows, an orange striped awning."""
    ic = gk.Icon("hepsiburada - faithful")
    wall = rr(12, 34, 116, 118, 6)
    solid(ic, wall, face=[(0, DARK[1]), (0.5, DARK[2]), (1, DARK[3])], depth=7, side="#1b1a1f", layer="facade")
    toplight(ic, wall, width=1.6, opacity=0.4, layer="facade")
    for i, (x0, x1) in enumerate(((20, 58), (66, 108))):
        win = rr(x0, 64, x1, 100, 3)
        solid(ic, win, face=[(0, "#ffe9b8"), (1, YELLOW[2])], depth=2, side=YELLOW[4], top=False, layer=f"window{i}")
        ic.path(geom_d(rr(x0 + 3, 68, x1 - 3, 72, 2)), LIGHT[0], opacity=0.5, layer_id=f"win-shine{i}")
    door = rr(52, 74, 76, 118, 3)
    solid(ic, door, face=[(0, "#3d3846"), (1, "#2b2732")], depth=2, side="#1b1a1f", top=False, layer="door")
    knob = circ(70, 96, 2.4)
    solid(ic, knob, face=[(0, YELLOW[2]), (1, YELLOW[4])], depth=1, side=YELLOW[4], top=False, layer="knob")
    sign = rr(20, 40, 108, 58, 3)
    solid(ic, sign, face=[(0, ORANGE[1]), (1, ORANGE[3])], depth=2, side=ORANGE[4], layer="sign")
    for k in range(6):
        x0 = 20 + k * 14.7
        seg = poly([(x0, 40), (x0 + 7.3, 40), (x0 + 7.3, 58), (x0, 58)], 0).intersection(sign)
        if k % 2 == 0:
            ic.path(geom_d(seg), LIGHT[0], opacity=0.85, layer_id=f"awning{k}")
    ic.path(geom_d(rr(20, 56, 108, 59, 1.5)), ORANGE[4], opacity=0.6, layer_id="sign-edge")
    return ic


def C():
    """Disc - a round price tag: yellow disc, a punched hole, a string, a price."""
    ic = gk.Icon("hepsiburada - disc")
    string = LineString([(88, 34), (106, 20), (116, 24)]).buffer(2.6, cap_style=1, join_style=1)
    solid(ic, string, face=[(0, "#e8d8bd"), (1, "#c9b48f")], depth=2, side="#a08a63", layer="string")
    tag = circ(60, 70, 42).difference(circ(88, 40, 7))
    solid(ic, tag, face=[(0, YELLOW[1]), (0.6, YELLOW[2]), (1, YELLOW[3])], depth=6, side=YELLOW[4], layer="tag")
    toplight(ic, tag, width=2, opacity=0.8, layer="tag")
    inner = circ(60, 70, 33).difference(circ(60, 70, 31))
    ic.path(geom_d(inner), ORANGE[3], opacity=0.55, layer_id="tag-ring", fill_rule="evenodd")
    bar1 = rr(40, 58, 66, 67, 2.5)
    solid(ic, bar1, face=[(0, ORANGE[2]), (1, ORANGE[4])], depth=1.5, side=ORANGE[4], top=False, layer="price-bar")
    dot = circ(73, 62, 3.4)
    solid(ic, dot, face=[(0, ORANGE[2]), (1, ORANGE[4])], depth=1, side=ORANGE[4], top=False, layer="price-dot")
    bar2 = rr(40, 74, 80, 83, 2.5)
    solid(ic, bar2, face=[(0, ORANGE[2]), (1, ORANGE[4])], depth=1.5, side=ORANGE[4], top=False, layer="price-bar2")
    return ic


def D():
    """Rimmed - a receipt: a long paper roll, orange lines, a total, a torn bottom edge."""
    ic = gk.Icon("hepsiburada - rimmed")
    paper = poly([(34, 12), (94, 12), (94, 112), (86, 118), (78, 112), (70, 118), (62, 112),
                  (54, 118), (46, 112), (34, 118)], 2)
    solid(ic, paper, face=[(0, LIGHT[0]), (0.6, LIGHT[1]), (1, LIGHT[2])], depth=4, side=LIGHT[4], layer="paper")
    toplight(ic, paper, width=1.4, opacity=0.9, layer="paper")
    head = rr(42, 20, 86, 28, 2)
    ic.path(geom_d(head), ORANGE[3], opacity=0.9, layer_id="head")
    for k in range(6):
        y = 38 + k * 8
        w = 40 if k % 3 else 30
        ic.path(geom_d(rr(42, y, 42 + w, y + 3.4, 1.6)), DARK[1], opacity=0.45, layer_id=f"line{k}")
    rule = rr(42, 86, 86, 88, 1)
    ic.path(geom_d(rule), DARK[2], opacity=0.5, layer_id="rule")
    total = rr(54, 94, 86, 103, 2)
    solid(ic, total, face=[(0, ORANGE[2]), (1, ORANGE[4])], depth=1.5, side=ORANGE[4], top=False, layer="total")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
