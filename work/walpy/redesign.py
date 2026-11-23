#!/usr/bin/env python3
"""walpy - Gnomed redesign.
Main (Symbol) A: a wallpaper roll. Faithful B: a photo print with the mark. Disc C: a film
canister. Rimmed D: prints drying on a line."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
YELLOW = RAMP["Yellow"]
BROWN = RAMP["Brown"]
BLUE = RAMP["Blue"]

NAVY = "#1e2a3d"
NAVY2 = "#2c3d56"
ROLL1 = "#62a0ea"
ROLL2 = "#3584e4"
ROLL3 = "#1c71d8"


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def squiggle(box_):
    g = parts("walpy")["r0"]
    (g,) = fit([g], box_)
    return g


def A():
    """Symbol - a paint roller: navy roller with the squiggle, steel frame, wooden handle."""
    ic = gk.Icon("walpy - symbol")
    roller = rr(8, 28, 102, 82, 20)          # inside 8..120 (size_audit: the grip touched x 125)
    solid(ic, roller, face=[(0, NAVY2), (0.5, NAVY), (1, "#16202e")], depth=7, side="#141c29", layer="roller")
    toplight(ic, roller, width=2.0, opacity=0.45, layer="roller")
    put_mark(ic, SLUG, (24, 36, 86, 76), face="#ffffff")
    rod = LineString([(100, 55), (110, 55), (110, 86)]).buffer(3.4, cap_style=1, join_style=1)
    solid(ic, rod, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="rod")
    grip = rr(98, 84, 120, 118, 8)
    solid(ic, grip, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[3])], depth=5, side=BROWN[4], layer="grip")
    toplight(ic, grip, width=1.4, opacity=0.6, layer="grip")
    return ic


def B():
    """Faithful - a photo print: white border, navy image with the mark, a caption line."""
    ic = gk.Icon("walpy - faithful")
    frame = rr(20, 12, 108, 118, 4)
    solid(ic, frame, face=[(0, LIGHT[0]), (0.6, LIGHT[1]), (1, LIGHT[2])], depth=5, side=LIGHT[4], layer="frame")
    toplight(ic, frame, width=1.6, opacity=0.8, layer="frame")
    img = rr(28, 20, 100, 94, 2)
    solid(ic, img, face=[(0, NAVY2), (1, NAVY)], depth=2, side="#141c29", top=False, layer="image")
    put_mark(ic, SLUG, (36, 38, 92, 86), face="#ffffff")
    for i, (y, w) in enumerate(((104, 44), (110, 30))):
        ic.path(geom_d(rr(34, y, 34 + w, y + 3, 1.5)), LIGHT[4], opacity=0.5, layer_id=f"caption{i}")
    return ic


def C():
    """Disc - the end of a wallpaper roll: yellow spiral, cardboard core with a real hole, the
    squiggle on the wrap, a peeling flap."""
    ic = gk.Icon("walpy - disc")
    roll = circ(60, 64, 50).difference(circ(60, 64, 7))
    solid(ic, roll, face=[(0, YELLOW[1]), (0.55, YELLOW[2]), (1, YELLOW[3])], depth=7, side=YELLOW[4], layer="roll")
    toplight(ic, roll, width=2.0, opacity=0.8, layer="roll")
    for k, r in enumerate((44, 35, 26, 18)):           # the spiral stops where the squiggle is printed
        ring = circ(60, 64, r).difference(circ(60, 64, r - 1.6)).difference(box(34, 17, 86, 52))
        ic.path(geom_d(ring), BROWN[3], opacity=0.35, layer_id=f"spiral{k}", fill_rule="evenodd")
    core = circ(60, 64, 12).difference(circ(60, 64, 7))
    solid(ic, core, face=[(0, BROWN[0]), (1, BROWN[2])], depth=3, side=BROWN[4], layer="core")
    put_mark(ic, SLUG, (41, 19, 79, 51), face=NAVY)  # on the face above the core (mark_fit)
    flap = poly([(92, 86), (114, 94), (106, 110), (88, 100)], 3)
    solid(ic, flap, face=[(0, YELLOW[1]), (1, YELLOW[3])], depth=4, side=YELLOW[4], layer="flap")
    toplight(ic, flap, width=1.2, opacity=0.8, layer="flap")
    return ic


def D():
    """Rimmed - prints drying on a line: brown rope, three kraft prints, wooden pegs; the big
    centre print carries the measured squiggle."""
    ic = gk.Icon("walpy - rimmed")
    rope = LineString([(8, 42), (64, 48), (120, 42)]).buffer(2.6, cap_style=1, join_style=1)
    solid(ic, rope, face=[(0, BROWN[2]), (1, BROWN[4])], depth=2, side=BROWN[4], layer="rope")
    for i, (cx, top, w, h) in enumerate(((26, 52, 24, 44), (64, 46, 50, 72), (102, 52, 24, 44))):
        pr = rr(cx - w / 2, top, cx + w / 2, top + h, 2)
        solid(ic, pr, face=[(0, BROWN[0]), (1, BROWN[2])], depth=3, side=BROWN[4], layer=f"print{i}")
        win = rr(cx - w / 2 + 4, top + 4, cx + w / 2 - 4, top + h - 8, 1)
        ic.path(geom_d(win), NAVY, opacity=0.95, layer_id=f"win{i}")
        peg = rr(cx - 3.5, top - 5, cx + 3.5, top + 7, 1.5)
        solid(ic, peg, face=[(0, BROWN[1]), (1, BROWN[3])], depth=2, side=BROWN[4], layer=f"peg{i}")
    put_mark(ic, SLUG, (45, 57, 83, 101), face="#ffffff")  # inside the print window with room
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
