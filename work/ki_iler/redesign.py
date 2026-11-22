#!/usr/bin/env python3
"""ki_iler - Gnomed redesign. Main (Symbol) B address book; A contact card (Faithful);
C rolodex (Disc); D card file box (Rimmed). Build: python3 tools/make_icon.py ki_iler"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity

SLUG = Path(__file__).resolve().parent.name
GREEN = RAMP["Green"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
RED = RAMP["Red"]
BROWN = RAMP["Brown"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Faithful - a contact card: green header, lines, a corner tab (no person drawn)."""
    ic = gk.Icon("ki_iler - faithful")
    card = rr(16, 30, 112, 112, 6)
    solid(ic, card, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=5, side=LIGHT[4], layer="card")
    toplight(ic, card, width=1.5, opacity=0.6, layer="card")
    head = rr(16, 30, 112, 50, 5)
    solid(ic, head, face=[(0, GREEN[2]), (1, GREEN[4])], depth=2, side=GREEN[4], top=False, layer="header")
    seal = circ(34, 40, 5)
    solid(ic, seal, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1, side=LIGHT[4], top=False, layer="seal")
    for i, (y, w) in enumerate(((62, 58), (74, 48), (86, 38))):
        line = rr(30, y, 30 + w, y + 6, 2)
        solid(ic, line, face=[(0, DARK[1]), (1, DARK[2])], depth=0, top=False, layer=f"line{i}")
    tab = rr(96, 98, 112, 110, 3)
    solid(ic, tab, face=[(0, GREEN[2]), (1, GREEN[4])], depth=2, side=GREEN[4], layer="tab")
    return ic


def B():
    """Main - an address book: cover, spine, page block, bookmark, letter tab."""
    ic = gk.Icon("ki_iler - symbol")
    cover = rr(20, 16, 108, 118, 8)
    solid(ic, cover, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=8, side=GREEN[4], layer="cover")
    toplight(ic, cover, width=2, opacity=0.55, layer="cover")
    spine = rr(20, 16, 38, 118, 7)
    solid(ic, spine, face=[(0, GREEN[3]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="spine")
    pages = rr(96, 24, 106, 110, 3)
    solid(ic, pages, face=[(0, LIGHT[0]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="pages")
    for i in range(4):
        y = 30 + i * 20
        line = rr(98, y, 104, y + 12, 1.5)
        ic.path(geom_d(line), LIGHT[4], opacity=0.9, layer_id=f"page{i}")
    label = rr(44, 44, 94, 84, 4)
    solid(ic, label, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer="label")
    for i, (y, w) in enumerate(((52, 40), (62, 32), (72, 24))):
        line = rr(50, y, 50 + w, y + 4, 1.5)
        solid(ic, line, face=[(0, GREEN[3]), (1, GREEN[4])], depth=0, top=False, layer=f"label-line{i}")
    ribbon = poly([(70, 16), (78, 16), (78, 54), (74, 48), (70, 54)], 1)
    solid(ic, ribbon, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="ribbon")
    tab = rr(106, 58, 118, 78, 3)
    solid(ic, tab, face=[(0, GREEN[2]), (1, GREEN[4])], depth=2, side=GREEN[4], layer="tab")
    return ic


def C():
    """Disc - a Rolodex: round card drum, one card in front, a steel crank and a base."""
    ic = gk.Icon("ki_iler - disc")
    base = rr(40, 104, 88, 118, 4)
    solid(ic, base, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer="base")
    drum = circ(64, 60, 40)
    solid(ic, drum, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=8, side=GREEN[4], layer="drum")
    toplight(ic, drum, width=2, opacity=0.55, layer="drum")
    ring = circ(64, 60, 31).difference(circ(64, 60, 27))
    ic.path(geom_d(ring), GREEN[4], opacity=0.5, layer_id="drum-ring", fill_rule="evenodd")
    for i, ang in enumerate((-11, 10)):
        back = rr(36, 34, 92, 84, 3)
        back = affinity.rotate(back, ang, origin=(64, 88))
        solid(ic, back, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer=f"back-card{i}")
    card = rr(38, 40, 90, 88, 3)
    solid(ic, card, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="card")
    for i, (y, w) in enumerate(((48, 40), (58, 34), (68, 26))):
        line = rr(44, y, 44 + w, y + 4, 1.5)
        solid(ic, line, face=[(0, DARK[1]), (1, DARK[2])], depth=0, top=False, layer=f"line{i}")
    crank = LineString([(100, 60), (112, 60)]).buffer(3.2, cap_style=1)
    solid(ic, crank, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer="crank")
    knob = circ(112, 60, 7)
    solid(ic, knob, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="crank-knob")
    return ic


def D():
    """Rimmed - a card catalog drawer: wooden drawer, brass label frame, index cards above."""
    ic = gk.Icon("ki_iler - rimmed")
    for i, (x0, x1, top) in enumerate(((26, 54, 36), (44, 72, 28), (62, 90, 40))):
        card = rr(x0, top, x1, 80, 2)
        solid(ic, card, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer=f"card{i}")
        tab = rr(x0 + 3, top - 7, x0 + 15, top + 2, 2)
        solid(ic, tab, face=[(0, GREEN[2]), (1, GREEN[4])], depth=2, side=GREEN[4], layer=f"tab{i}")
    drawer = rr(12, 66, 116, 118, 5)
    solid(ic, drawer, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[3])], depth=6, side=BROWN[4], layer="drawer")
    toplight(ic, drawer, width=2, opacity=0.55, layer="drawer")
    frame = rr(28, 76, 100, 102, 3)
    solid(ic, frame, face=[(0, YELLOW[2]), (1, YELLOW[4])], depth=2, side=YELLOW[4], layer="label-frame")
    label = rr(32, 80, 96, 98, 2)
    solid(ic, label, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1, side=LIGHT[4], top=False, layer="label")
    for i, (y, w) in enumerate(((85, 50), (92, 36))):
        line = rr(39, y, 39 + w, y + 4, 1.5)
        solid(ic, line, face=[(0, GREEN[3]), (1, GREEN[4])], depth=0, top=False, layer=f"label-line{i}")
    pull = rr(50, 107, 78, 113, 3)
    solid(ic, pull, face=[(0, YELLOW[2]), (1, YELLOW[4])], depth=2, side=YELLOW[4], layer="pull")
    for x in (54, 74):
        ic.path(geom_d(circ(x, 110, 1.4)), BROWN[4], layer_id=f"screw{x}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
