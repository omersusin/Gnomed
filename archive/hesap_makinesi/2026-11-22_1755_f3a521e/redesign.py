#!/usr/bin/env python3
"""hesap_makinesi - Gnomed redesign. Main (Symbol) B abacus; A pocket calculator (Faithful);
C circular slide rule (Disc); D adding machine with paper roll (Rimmed)."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
BLUE = RAMP["Blue"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
RED = RAMP["Red"]
GREEN = RAMP["Green"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd",
       "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd", " ": ""}


def digit(ic, x, y, w, h, t, segs, colour, layer="seg"):
    r = t * 0.38
    a = rounded(box(x, y, x + w, y + t), r)
    b = rounded(box(x + w - t, y, x + w, y + h / 2), r)
    c = rounded(box(x + w - t, y + h / 2, x + w, y + h), r)
    d = rounded(box(x, y + h - t, x + w, y + h), r)
    e = rounded(box(x, y + h / 2, x + t, y + h), r)
    f = rounded(box(x, y, x + t, y + h / 2), r)
    g = rounded(box(x, y + h / 2 - t / 2, x + w, y + h / 2 + t / 2), r)
    for name, s in zip("abcdefg", (a, b, c, d, e, f, g)):
        if name in segs:
            solid(ic, s, face=colour, depth=0, top=False, layer=f"{layer}-{name}")


def key(ic, x, y, w, h, label, face, layer):
    k = rr(x, y, x + w, y + h, min(3, h * 0.3))
    solid(ic, k, face=face, depth=2.5, side=DARK[2], layer=layer)
    cx, cy = (x + x + w) / 2, (y + y + h) / 2
    if label == "+":
        solid(ic, rr(cx - 6, cy - 1.6, cx + 6, cy + 1.6, 1.2), face=LIGHT[0], depth=0, top=False, layer=f"{layer}-h")
        solid(ic, rr(cx - 1.6, cy - 6, cx + 1.6, cy + 6, 1.2), face=LIGHT[0], depth=0, top=False, layer=f"{layer}-v")
    elif label == "=":
        for dy in (-3.2, 3.2):
            solid(ic, rr(cx - 6, cy + dy - 1.5, cx + 6, cy + dy + 1.5, 1.2), face=LIGHT[0], depth=0, top=False,
                  layer=f"{layer}-{dy}")
    elif label == "x":
        g = unary_union([rr(cx - 6, cy - 1.4, cx + 6, cy + 1.4, 1.2),
                         rr(cx - 1.4, cy - 6, cx + 1.4, cy + 6, 1.2)])
        ic.path(geom_d(affinity.rotate(g, 45, origin=(cx, cy))), LIGHT[0], layer_id=f"{layer}-x")


def A():
    """Faithful - a pocket calculator with a yellow LCD and big + / = keys."""
    ic = gk.Icon("hesap_makinesi - faithful")
    body = rr(24, 18, 104, 118, 9)
    solid(ic, body, face=[(0, "#78909c"), (0.5, "#546e7a"), (1, "#445964")], depth=7, side=DARK[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    screen = rr(32, 26, 96, 54, 3)
    recess(ic, screen, [(0, "#d4c915"), (1, "#b8ad10")], wall=2.5, layer="screen")
    digit(ic, 44, 32, 11, 16, 2.8, SEG["4"], "#3d4a1a", layer="d4")
    digit(ic, 60, 32, 11, 16, 2.8, SEG["2"], "#3d4a1a", layer="d2")
    for i, (x, y) in enumerate(((32, 60), (58, 60), (84, 60), (32, 79), (58, 79), (84, 79))):
        key(ic, x, y, 22, 15, "", face=[(0, LIGHT[1]), (1, LIGHT[3])], layer=f"key{i}")
    key(ic, 32, 98, 40, 15, "+", face=[(0, BLUE[1]), (1, BLUE[3])], layer="plus")
    key(ic, 78, 98, 28, 15, "=", face=[(0, RED[1]), (1, RED[3])], layer="equals")
    return ic


def B():
    """Main - an abacus: blue-grey frame, three rods, four big beads each."""
    ic = gk.Icon("hesap_makinesi - symbol")
    frame = rr(12, 22, 116, 118, 7)
    solid(ic, frame, face=[(0, "#78909c"), (0.5, "#546e7a"), (1, "#445964")], depth=7, side=DARK[4], layer="frame")
    toplight(ic, frame, width=2, opacity=0.55, layer="frame")
    inner = rr(20, 30, 108, 110, 4)
    recess(ic, inner, [(0, "#1b262c"), (1, "#445964")], wall=3, layer="window")
    for row, y in enumerate((52, 90)):
        rod = rr(24, y - 2, 104, y + 2, 1.5)
        solid(ic, rod, face=LIGHT[4], depth=0, top=False, layer=f"rod{row}")
        for k in range(3):
            x = 42 + k * 22
            bead = ellipse(x, y, 10.6, 13.0)
            col = (BLUE, RED, GREEN)[row]
            solid(ic, bead, face=[(0, col[1]), (1, col[3])], depth=3, side=col[4], layer=f"bead{row}{k}")
    return ic


def C():
    """Disc - a round pocket calculator: yellow LCD, round keys, red = key."""
    ic = gk.Icon("hesap_makinesi - disc")
    body = circ(64, 62, 48)
    solid(ic, body, face=[(0, "#78909c"), (0.5, "#546e7a"), (1, "#445964")], depth=8, side=DARK[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    screen = rr(36, 28, 92, 54, 4)
    recess(ic, screen, [(0, "#d4c915"), (1, "#b8ad10")], wall=2.5, layer="screen")
    digit(ic, 46, 34, 12, 15, 2.8, SEG["4"], "#3d4a1a", layer="d4")
    digit(ic, 64, 34, 12, 15, 2.8, SEG["2"], "#3d4a1a", layer="d2")
    for i, (x, y) in enumerate(((46, 66), (64, 66), (82, 66), (46, 84), (64, 84))):
        k = circ(x, y, 7.2)
        solid(ic, k, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2.5, side=LIGHT[4], layer=f"key{i}")
    eq = circ(82, 84, 9)
    solid(ic, eq, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="equals")
    for dy in (-2.6, 2.6):
        solid(ic, rr(78, 84 + dy - 1.3, 86, 84 + dy + 1.3, 1.1), face=LIGHT[0], depth=0, top=False, layer=f"eq{dy}")
    return ic


def D():
    """Rimmed - an adding machine: body, keypad, paper roll, red crank wheel."""
    ic = gk.Icon("hesap_makinesi - rimmed")
    body = rr(20, 54, 108, 118, 7)
    solid(ic, body, face=[(0, "#78909c"), (0.5, "#546e7a"), (1, "#445964")], depth=6, side=DARK[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    tape = rr(40, 12, 86, 48, 2)
    solid(ic, tape, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer="tape")
    for i, (y, w) in enumerate(((19, 32), (25, 26), (31, 32), (37, 20))):
        line = rr(47, y, 47 + w, y + 2.8, 1.2)
        solid(ic, line, face=DARK[2], depth=0, top=False, layer=f"print{i}")
    roll = rr(36, 44, 90, 58, 7)
    solid(ic, roll, face=[(0, LIGHT[0]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="roll")
    for i, (x, y) in enumerate(((30, 66), (48, 66), (66, 66), (30, 82), (48, 82), (66, 82), (30, 98), (48, 98))):
        key(ic, x, y, 14, 11, "", face=[(0, LIGHT[1]), (1, LIGHT[3])], layer=f"key{i}")
    key(ic, 66, 98, 14, 11, "+", face=[(0, BLUE[1]), (1, BLUE[3])], layer="plus")
    rod = rr(102, 66, 107, 92, 2)
    solid(ic, rod, face=[(0, DARK[1]), (1, DARK[3])], depth=2, side=DARK[4], layer="crank-rod")
    wheel = circ(104, 68, 18)
    solid(ic, wheel, face=[(0, RED[1]), (1, RED[3])], depth=4, side=RED[4], layer="crank")
    ic.path(geom_d(circ(104, 68, 6)), LIGHT[1], layer_id="crank-hub")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
