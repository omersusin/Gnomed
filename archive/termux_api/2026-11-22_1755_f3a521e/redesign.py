#!/usr/bin/env python3
"""termux_api - Gnomed redesign.
Main (Symbol) A: a terminal window with a green >_ prompt. Faithful B: a circuit chip (the API).
Disc C: a cable spool. Rimmed D: a red toolbox."""
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
RED = RAMP["Red"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def prompt(ic, x, y, s, colour, layer="prompt"):
    """The >_ mark: a chevron and a bar, drawn as thick strokes."""
    chev = LineString([(x, y), (x + 15 * s, y + 14 * s), (x, y + 28 * s)]).buffer(4.2 * s, cap_style=1, join_style=1)
    bar = rr(x + 21 * s, y + 22 * s, x + 41 * s, y + 28 * s, 2 * s)
    ic.path(geom_d(chev), colour, layer_id=f"{layer}-chev")
    ic.path(geom_d(bar), colour, layer_id=f"{layer}-bar")


def A():
    """Symbol - a terminal window: dark case, title bar with three dots, green prompt."""
    ic = gk.Icon("termux_api - symbol")
    case = rr(8, 24, 120, 116, 9)
    solid(ic, case, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[4])], depth=8, side=LIGHT[4], layer="case")
    toplight(ic, case, width=1.8, opacity=0.4, layer="case")
    bar = rr(8, 24, 120, 40, 9)
    solid(ic, bar, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=1, side=LIGHT[4], top=False, layer="titlebar")
    for i, x in enumerate((22, 34, 46)):
        dot = circ(x, 32, 3.4)
        solid(ic, dot, face=[(0, DARK[1]), (1, DARK[3])], depth=1, side=DARK[3], top=False, layer=f"dot{i}")
    screen = rr(15, 45, 113, 108, 4)
    recess(ic, screen, [(0, "#2b2933"), (1, "#3d3846")], wall=3, layer="screen")
    put_mark(ic, SLUG, (28, 50, 102, 88), face=GREEN[1])
    cur = rr(84, 92, 96, 104, 1.5)
    ic.path(geom_d(cur), GREEN[2], opacity=0.9, layer_id="cursor")
    for i, (x, w) in enumerate(((30, 30), (30, 44))):
        line = rr(x, 88 + i * 10, x + w, 91 + i * 10, 1.5)
        ic.path(geom_d(line), LIGHT[2], opacity=0.3, layer_id=f"line{i}")
    return ic


def B():
    """Faithful - a circuit chip: green board, dark die, silver pins, the prompt printed on it."""
    ic = gk.Icon("termux_api - faithful")
    for k in range(6):
        for side in range(4):
            if side == 0:
                g = rr(44 + k * 8, 16, 48 + k * 8, 32, 1.6)
            elif side == 1:
                g = rr(44 + k * 8, 96, 48 + k * 8, 112, 1.6)
            elif side == 2:
                g = rr(16, 44 + k * 8, 32, 48 + k * 8, 1.6)
            else:
                g = rr(96, 44 + k * 8, 112, 48 + k * 8, 1.6)
            solid(ic, g, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], top=False, layer=f"pin{side}{k}")
    board = rr(28, 28, 100, 100, 7)
    solid(ic, board, face=[(0, GREEN[1]), (0.5, GREEN[2]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="board")
    toplight(ic, board, width=1.6, opacity=0.6, layer="board")
    die = rr(38, 38, 90, 90, 5)
    solid(ic, die, face=[(0, DARK[1]), (0.5, DARK[2]), (1, DARK[3])], depth=5, side=DARK[3], layer="die")
    toplight(ic, die, width=1.4, opacity=0.4, layer="die")
    put_mark(ic, SLUG, (42, 44, 86, 88), face=LIGHT[0])
    for i, (x, y, w) in enumerate(((34, 36, 8), (34, 86, 8), (86, 36, 8), (86, 86, 8))):
        ic.path(geom_d(circ(x + w / 2, y + 4, 2.4)), GREEN[4], layer_id=f"via{i}")
    return ic


def C():
    """Disc - a round power plug: ivory body, two brass prongs, the >_ printed on it."""
    ic = gk.Icon("termux_api - disc")
    body = circ(52, 79, 36)
    solid(ic, body, face=[(0, LIGHT[0]), (0.55, LIGHT[1]), (1, LIGHT[2])], depth=7, side=LIGHT[4], layer="body")
    toplight(ic, body, width=2.0, opacity=0.9, layer="body")
    ring = circ(52, 79, 36).difference(circ(52, 79, 32))
    ic.path(geom_d(ring), LIGHT[3], opacity=0.5, layer_id="rim", fill_rule="evenodd")
    put_mark(ic, SLUG, (30, 58, 74, 98), face=DARK[3])
    for i, y in enumerate((60, 86)):
        prong = rr(88, y, 118, y + 10, 4)
        solid(ic, prong, face=[(0, YELLOW[2]), (0.5, YELLOW[3]), (1, YELLOW[4])], depth=3, side=YELLOW[4], layer=f"prong{i}")
        toplight(ic, prong, width=1.0, opacity=0.7, layer=f"prong{i}")
    relief = rr(10, 72, 22, 86, 5)
    solid(ic, relief, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=3, side=LIGHT[4], layer="relief")
    return ic


def D():
    """Rimmed - a red toolbox: lid, steel handle, a cream label with the prompt, a green stripe."""
    ic = gk.Icon("termux_api - rimmed")
    handle = LineString([(44, 40), (44, 26), (84, 26), (84, 40)]).buffer(4, cap_style=1, join_style=1)
    solid(ic, handle, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="handle")
    body = rr(14, 44, 114, 116, 6)
    solid(ic, body, face=[(0, RED[1]), (0.5, RED[2]), (1, RED[4])], depth=7, side=RED[4], layer="body")
    toplight(ic, body, width=1.6, opacity=0.55, layer="body")
    lid = rr(14, 44, 114, 64, 6)
    solid(ic, lid, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="lid")
    toplight(ic, lid, width=1.4, opacity=0.5, layer="lid")
    strip = rr(18, 62, 110, 67, 2)
    ic.path(geom_d(strip), GREEN[2], opacity=0.9, layer_id="stripe")
    label = rr(24, 72, 104, 112, 4)
    solid(ic, label, face=[(0, LIGHT[0]), (0.6, LIGHT[1]), (1, LIGHT[2])], depth=2, side=LIGHT[4], top=False, layer="label")
    put_mark(ic, SLUG, (30, 76, 98, 108), face=DARK[3])
    for x in (20, 108):
        ic.path(geom_d(circ(x, 70, 2.2)), LIGHT[2], opacity=0.8, layer_id=f"rivet{x}")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
