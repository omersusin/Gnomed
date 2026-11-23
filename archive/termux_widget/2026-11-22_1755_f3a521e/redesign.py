#!/usr/bin/env python3
"""termux_widget - Gnomed redesign.
Main (Symbol) A: a yellow sticky note. Faithful B: a clipboard. Disc C: a round rubber stamp.
Rimmed D: a blue notebook."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
GREEN = RAMP["Green"]
YELLOW = RAMP["Yellow"]
BLUE = RAMP["Blue"]
BROWN = RAMP["Brown"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def prompt(ic, x, y, s, colour, layer="prompt"):
    chev = LineString([(x, y), (x + 13 * s, y + 12 * s), (x, y + 24 * s)]).buffer(3.6 * s, cap_style=1, join_style=1)
    bar = rr(x + 18 * s, y + 19 * s, x + 35 * s, y + 24 * s, 1.8 * s)
    ic.path(geom_d(chev), colour, layer_id=f"{layer}-chev")
    ic.path(geom_d(bar), colour, layer_id=f"{layer}-bar")


def A():
    """Symbol - a sticky note: yellow square, curled corner, the prompt written on it."""
    ic = gk.Icon("termux_widget - symbol")
    note = poly([(20, 18), (104, 18), (104, 100), (86, 118), (20, 118)], 4)
    solid(ic, note, face=[(0, YELLOW[1]), (0.6, YELLOW[2]), (1, YELLOW[3])], depth=4, side=YELLOW[4], layer="note")
    toplight(ic, note, width=1.6, opacity=0.7, layer="note")
    curl = poly([(86, 118), (104, 100), (104, 118)], 3)
    solid(ic, curl, face=[(0, YELLOW[3]), (1, YELLOW[4])], depth=2, side=YELLOW[4], layer="curl")
    put_mark(ic, SLUG, (32, 34, 96, 72), face=DARK[2])
    for i, (y, w) in enumerate(((78, 46), (88, 34))):
        line = rr(34, y, 34 + w, y + 5, 2)
        ic.path(geom_d(line), BROWN[3], opacity=0.55, layer_id=f"line{i}")
    return ic


def B():
    """Faithful - a clipboard: brown board, steel clip, white sheet with the prompt."""
    ic = gk.Icon("termux_widget - faithful")
    board = rr(20, 24, 108, 118, 6)
    solid(ic, board, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[3])], depth=6, side=BROWN[4], layer="board")
    toplight(ic, board, width=1.6, opacity=0.55, layer="board")
    sheet = rr(30, 44, 98, 110, 3)
    solid(ic, sheet, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], top=False, layer="sheet")
    put_mark(ic, SLUG, (37, 46, 97, 90), face=DARK[2])
    for i, (y, w) in enumerate(((90, 44), (98, 32))):
        line = rr(40, y, 40 + w, y + 4, 1.6)
        ic.path(geom_d(line), DARK[1], opacity=0.4, layer_id=f"line{i}")
    clip = rr(44, 14, 84, 38, 5)
    solid(ic, clip, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=4, side=LIGHT[4], layer="clip")
    toplight(ic, clip, width=1.2, opacity=0.75, layer="clip")
    ic.path(geom_d(rr(56, 24, 72, 29, 2.4)), DARK[1], opacity=0.5, layer_id="clip-slot")
    return ic


def C():
    """Disc - a round rubber stamp seen from above: wood knob, dark body, white prompt."""
    ic = gk.Icon("termux_widget - disc")
    body = circ(64, 70, 44)
    solid(ic, body, face=[(0, LIGHT[0]), (0.55, LIGHT[1]), (1, LIGHT[2])], depth=7, side=LIGHT[4], layer="body")
    toplight(ic, body, width=2, opacity=0.9, layer="body")
    ring = circ(64, 70, 37).difference(circ(64, 70, 33))
    ic.path(geom_d(ring), LIGHT[4], opacity=0.5, layer_id="rim", fill_rule="evenodd")
    put_mark(ic, SLUG, (40, 50, 88, 92), face=DARK[3])
    knob = circ(64, 26, 16)
    solid(ic, knob, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[4])], depth=5, side=BROWN[4], layer="knob")
    toplight(ic, knob, width=1.6, opacity=0.6, layer="knob")
    neck = rr(52, 34, 76, 44, 4)
    solid(ic, neck, face=[(0, BROWN[2]), (1, BROWN[4])], depth=2, side=BROWN[4], top=False, layer="neck")
    return ic


def D():
    """Rimmed - a blue notebook: cover with the prompt, page block, yellow ribbon."""
    ic = gk.Icon("termux_widget - rimmed")
    cover = book(ic, 64, 118, 92, ramp=BLUE, name="book")
    toplight(ic, cover, width=1.6, opacity=0.5, layer="book")
    put_mark(ic, SLUG, (36, 36, 92, 76), face=LIGHT[0])
    band = rr(20, 104, 92, 112, 2)
    ic.path(geom_d(band), BLUE[4], opacity=0.5, layer_id="band")
    ribbon = rr(84, 104, 92, 122, 2)
    solid(ic, ribbon, face=[(0, YELLOW[2]), (1, YELLOW[4])], depth=2, side=YELLOW[4], layer="ribbon")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
