#!/usr/bin/env python3
"""duolingo - Gnomed redesign (batch, no mascot).
Main (Symbol) A: a fan of flash cards, the front one green with white "Aa". Faithful B: a green
dictionary with white pages and an orange bookmark. Disc C: a globe with green continents on a
steel stand. Rimmed D: a green classroom chalkboard in a wooden frame with chalk and an eraser."""
import sys
from pathlib import Path
from shapely import affinity
from shapely.geometry import LineString
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
DGREEN = ("#89e219", "#7ad61a", "#58cc02", "#46a302", "#3a8702")
ORANGE = RAMP["Orange"]
BROWN = RAMP["Brown"]
WOOD = ("#b5835a", "#a06a3f", "#8a5c38", "#6f4526", "#5c3a20")


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def glyph_A(cx, y0, y1, w=6.6):
    """A bold geometric capital A: a thick chevron plus the crossbar."""
    c = LineString([(cx - 12, y1), (cx, y0), (cx + 12, y1)]).buffer(w / 2, quad_segs=2, cap_style=1, join_style=1)
    bar = box(cx - 9, y1 - 13, cx + 9, y1 - 13 + w)
    return c.union(bar)


def glyph_a(cx, y0, y1, w=6.0):
    """A single-storey bold a: a round bowl with its counter and a straight stem on the right."""
    bowl = circ(cx - 2.5, y0 + 11, 10.5)
    counter = circ(cx - 3.5, y0 + 11, 4.4)
    stem = box(cx + 7, y0, cx + 7 + w, y1)
    return bowl.union(stem).difference(counter)


def A():
    """Symbol - a fan of three flash cards; the front green card carries the white "Aa"."""
    ic = gk.Icon("duolingo - symbol")
    back = affinity.rotate(rr(22, 26, 100, 112, 6), -8, origin=(61, 106))
    solid(ic, back, face=[(0, "#ffffff"), (0.6, "#f6f5f4"), (1, "#deddda")], depth=2.5, side="#b5b3b0", layer="card-back")
    mid = affinity.rotate(rr(26, 22, 104, 108, 6), 7, origin=(63, 104))
    solid(ic, mid, face=[(0, "#ffffff"), (0.6, "#f6f5f4"), (1, "#c0bfbc")], depth=2.5, side="#9a9996", layer="card-mid")
    front = rr(24, 18, 104, 110, 6)
    solid(ic, front, face=[(0, DGREEN[0]), (0.5, DGREEN[2]), (1, DGREEN[3])], depth=3, side=DGREEN[4], layer="card-front")
    ic.path(geom_d(rr(24, 18, 104, 24, 4).intersection(front)), "#ffffff", opacity=0.3, layer_id="card-light")
    ic.path(geom_d(glyph_A(52, 54, 88)), "#ffffff", layer_id="glyph-A")
    ic.path(geom_d(glyph_a(76, 64, 88)), "#ffffff", layer_id="glyph-a")
    return ic


def B():
    """Faithful - a dictionary: a thick green cover, the white page block and an orange bookmark
    hanging out of the bottom; two white index tabs on the fore-edge (the closest to the logo:
    the app's green, and the book of words it teaches)."""
    ic = gk.Icon("duolingo - faithful")
    w, d = 96, 20
    h = 106
    cx, base = 64, 118
    top = base - 4 - h
    pages = box(cx - w / 2 + d, top + 3, cx + w / 2, top + h + 1)
    ic.path(geom_d(pages), ic.linear([(0, "#ffffff"), (1, "#deddda")], cx - w / 2, 0, cx + w / 2, 0), layer_id="pages")
    for k in range(3):
        y = top + 16 + k * 32
        ic.path(geom_d(box(cx + 2, y, cx + w / 2 - 5, y + 2)), "#c0bfbc", opacity=0.6, layer_id=f"page-line-{k}")
    cover = rr(cx - w / 2, top, cx + w / 2 - d * 0.6, top + h, 4)
    solid(ic, cover, face=[(0, DGREEN[0]), (0.5, DGREEN[2]), (1, DGREEN[3])], depth=5, side=DGREEN[4], layer="cover")
    spine = box(cx - w / 2, top, cx - w / 2 + 8, top + h).intersection(cover)
    ic.path(geom_d(spine), DGREEN[4], opacity=0.45, layer_id="spine")
    ribbon = poly([(cx + 14, top + 4), (cx + 28, top + 4), (cx + 28, base - 10), (cx + 21, base - 2), (cx + 14, base - 10)], 1)
    solid(ic, ribbon, face=[(0, ORANGE[1]), (1, ORANGE[2])], depth=1.5, side=ORANGE[3], layer="bookmark")
    for k, y in enumerate((top + 26, top + 58)):
        tab = rr(cx + w / 2 - d * 0.7, y, cx + w / 2 + 3, y + 14, 2)
        ic.path(geom_d(tab), "#f6f5f4", layer_id=f"tab-{k}")
    return ic


def C():
    """Disc - a globe: a light-blue ocean sphere with green brand continents, a white glint, a
    steel meridian arc and a round base. The languages of the world."""
    ic = gk.Icon("duolingo - disc")
    base = 122
    r = 47
    cy = base - 6 - r
    bx = ellipse(64, base - 6, 30, 5)
    solid(ic, bx, face=[(0, "#77767b"), (1, "#3d3846")], depth=2, side="#1b1a1f", layer="base")
    arc = circ(64, cy, r + 4).difference(circ(64, cy, r + 1))
    solid(ic, arc, face=[(0, "#c0bfbc"), (1, "#77767b")], depth=2, side="#5e5c64", layer="arm")
    ball = circ(64, cy, r)
    solid(ic, ball, face=[(0, "#cfe0f5"), (0.55, "#a9c2e8"), (1, "#62a0ea")], depth=2.5, side="#3584e4", top=False, layer="ocean")
    land = unary_union([
        poly([(36, 46), (46, 40), (54, 46), (58, 56), (54, 66), (48, 76), (42, 88), (34, 92),
              (28, 84), (32, 72), (30, 58)], 6),
        poly([(64, 52), (76, 50), (86, 56), (88, 68), (84, 80), (76, 90), (66, 88), (62, 76),
              (62, 64)], 7),
        poly([(74, 30), (84, 32), (88, 40), (82, 46), (72, 44), (68, 36)], 4),
        poly([(44, 96), (52, 96), (54, 104), (48, 108), (42, 104)], 3),
    ]).intersection(ball)
    ic.path(geom_d(land), ic.linear([(0, DGREEN[0]), (1, DGREEN[3])], 0, cy - r, 0, cy + r), layer_id="land")
    ic.path(geom_d(ellipse(46, 34, 12, 6).intersection(ball)), "#ffffff", opacity=0.55, layer_id="glint")
    return ic


def D():
    """Rimmed - a classroom chalkboard: dark-green board in a wooden frame, a chalk tray with an
    orange chalk stick and a white eraser, and a big white chalk "A" on the board."""
    ic = gk.Icon("duolingo - rimmed")
    frame = rr(10, 14, 118, 108, 4)
    solid(ic, frame, face=[(0, WOOD[0]), (0.5, WOOD[2]), (1, WOOD[4])], depth=5, side=WOOD[4], layer="frame")
    board = rr(17, 21, 111, 101, 2)
    solid(ic, board, face=[(0, DGREEN[0]), (0.55, DGREEN[2]), (1, DGREEN[3])], depth=2, side=DGREEN[4], top=False, layer="board")
    ic.path(geom_d(glyph_A(58, 38, 84, 8)), "#f6f5f4", opacity=0.95, layer_id="chalk-A")
    ic.path(geom_d(box(42, 88, 80, 91)), "#f6f5f4", opacity=0.75, layer_id="chalk-line")
    tray = rr(14, 100, 114, 112, 3)
    solid(ic, tray, face=[(0, WOOD[0]), (1, WOOD[2])], depth=3, side=WOOD[4], layer="tray")
    chalk = rr(26, 96, 58, 102, 3)
    solid(ic, chalk, face=[(0, ORANGE[1]), (1, ORANGE[2])], depth=2, side=ORANGE[3], layer="chalk")
    eraser = rr(70, 92, 104, 102, 2)
    solid(ic, eraser, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=3, side="#9a9996", layer="eraser")
    ic.path(geom_d(box(70, 97, 104, 100)), "#77767b", opacity=0.5, layer_id="eraser-felt")
    return ic


CONCEPTS = {"A": A, "B": B, "C": C, "D": D}

if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
