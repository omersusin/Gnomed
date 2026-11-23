#!/usr/bin/env python3
"""kafa_topu_2 (Head Ball 2) - Gnomed redesign, round 4 (Claude, 2026-11-23).

Characters: YES - the game IS its two big heads facing each other (REDESIGN 3b, owner 2026-11-23
"Oyuna göre sen seç"; 2026-11-19 "iki kafa karşı karşıya"). Every style carries the game's own
anchors (design.md), each a different design:
  Symbol   A: the header - ONE big head on its boot heading the black-and-white ball
  Faithful B: the store icon - two busts facing, the yellow VS between, the ball above
  Disc     C: the round pitch of the banner - the two players on their boots, the ball between
  Rimmed   D: the super power - the ball flying into the goal's net with a fire trail
Parts (heads, boots, ball, VS, goal, pitch): kit.py.
"""
import sys
from pathlib import Path

from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403,E402

SLUG = "kafa_topu_2"
SP = 12                                               # net mesh (units)


def A():
    """Symbol - the header: the bearded player (the logo's left one) on his red boot, heading the
    leather ball. One character, big: it reads at 32 px."""
    ic = gk.Icon("kafa_topu_2 - symbol")
    player(ic, 47, 116, 29, +1, LEFT_SKIN, "swept", RED, "p1")
    ball(ic, 84, 33, 18, depth=3)              # touching the forehead: the header
    return ic


def B():
    """Faithful - the store icon without its plate: the two players' busts facing each other, the
    yellow VS between them and the black-and-white ball above."""
    ic = gk.Icon("kafa_topu_2 - faithful")
    ball(ic, 64, 30, 17, depth=3)
    bust(ic, 34, 82, 24, +1, LEFT_SKIN, "swept", RED, "p1")
    bust(ic, 94, 82, 24, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    vs(ic, 48, 94, 1.0)
    return ic


def C():
    """Disc - the banner's round green pitch with its centre line; the two players stand on their
    boots facing each other, the ball between them at head height."""
    ic = gk.Icon("kafa_topu_2 - disc")
    pitch(ic, 64, 99, 57, 16)
    player(ic, 36, 106, 18, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 92, 106, 18, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    ball(ic, 64, 36, 13, depth=2.5)
    return ic


def D():
    """Rimmed - "Use your Super Powers!": the fireball shot - the ball flying into the goal's net
    with a fire trail behind it (refs/store/shot-2.jpg). The goal is small and calm behind it, the
    ball and its fire are the subject (legible at 32 px)."""
    ic = gk.Icon("kafa_topu_2 - rimmed")
    turf = rounded(box(8, 102, 120, 114), 5)              # r < half the height, or rounded() returns nothing
    solid(ic, turf, face=[(0, "#8ff0a4"), (0.5, "#57e389"), (1, "#2ec27e")], depth=4, side="#26a269", layer="turf")
    net = box(58, 30, 112, 102)
    ic.path(geom_d(net), ic.linear([(0, "#ffffff"), (1, "#deddda")], 0, 30, 0, 102), layer_id="goal-netfill")
    threads = unary_union([LineString([(x, 30), (x, 102)]).buffer(0.8) for x in range(58 + SP, 112, SP)] +
                          [LineString([(58, y), (112, y)]).buffer(0.8) for y in range(30 + SP, 102, SP)]).intersection(net)
    ic.path(geom_d(threads), "#c0bfbc", layer_id="goal-net")
    frame = unary_union([box(54, 26, 116, 31), box(54, 26, 59, 102), box(111, 26, 116, 102)])
    solid(ic, frame, face=[(0, "#ffffff"), (1, "#deddda")], depth=2.5, side="#9a9996", layer="goal-frame")
    bx, by, br = 62, 60, 21
    tail = unary_union([circ(10 + t * (bx - 10), 104 + t * (by - 104), 2 + t * (br - 4)) for t in
                        [k / 24 for k in range(25)]]).buffer(0.5)
    ic.path(geom_d(tail), ic.linear([(0, "#f9f06b", 0.0), (0.35, "#ffbe6f", 0.8), (0.8, "#ff7800"), (1, "#e66100")],
                                    10, 104, bx, by), layer_id="fire")
    core = unary_union([circ(24 + t * (bx - 24), 94 + t * (by - 94), 1.2 + t * (br * 0.55 - 1.2)) for t in
                        [k / 20 for k in range(21)]]).buffer(0.3)
    ic.path(geom_d(core), ic.linear([(0, "#f9f06b", 0.0), (0.6, "#f9f06b", 0.9), (1, "#ffffff")], 24, 94, bx, by),
            layer_id="fire-core")
    ball(ic, bx, by, br, depth=3)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
