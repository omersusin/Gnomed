#!/usr/bin/env python3
"""kafa_topu_2 - Gnomed redesign (batch redo, objects only - no characters).
Main (Symbol) A: the match ball on the green turf. Faithful B: a football boot kicking the ball.
Disc C: a referee's stopwatch (90-second matches). Rimmed D: the winner's cup on a blue plinth."""
import math as _m
import sys
from pathlib import Path
from shapely import affinity
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
GREEN = RAMP["Green"]
YELLOW = RAMP["Yellow"]
BLUE = RAMP["Blue"]
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
PENT = ("#62a0ea", "#1c71d8")


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - the match ball with blue panels on the green turf, on the white penalty spot: the
    thing the whole game is about, with the leather pentagons and a gloss."""
    ic = gk.Icon("kafa_topu_2 - symbol")
    turf = ellipse(64, 107, 58, 12)
    solid(ic, turf, face=[(0, GREEN[3]), (0.55, "#2aa05f"), (1, "#1b7a3f")], depth=4, side="#125c2e", layer="turf")
    ic.path(geom_d(ellipse(64, 104, 17, 4.2).difference(ellipse(64, 103, 12, 2.7))), "#ffffff", opacity=0.9, layer_id="spot")
    football(ic, 64, 110, 78, name="ball", pent=PENT)
    return ic


def B():
    """Faithful - a brown leather football boot with its studs and white laces, the ball at its
    toe: the game's own gear, the closest style to the source (each player stands on one boot)."""
    ic = gk.Icon("kafa_topu_2 - faithful")
    turf = rr(6, 108, 122, 120, 6)
    solid(ic, turf, face=[(0, GREEN[2]), (0.55, GREEN[3]), (1, GREEN[4])], depth=4, side="#1b7a3f", layer="turf")
    upper = poly([(14, 52), (32, 44), (44, 62), (60, 72), (86, 80), (106, 88), (116, 98), (112, 108), (18, 108), (10, 90)], 9)
    solid(ic, upper, face=[(0, "#d2a679"), (0.45, "#b5835a"), (1, "#7a4f2e")], depth=5, side="#5c3a20", layer="upper")
    toe = ellipse(100, 100, 14, 7).intersection(upper)
    ic.path(geom_d(toe), "#e0b98f", opacity=0.5, layer_id="toe")
    for k in range(3):
        lace = box(44 + k * 2, 66 + k * 9, 74 + k * 3, 68 + k * 9).intersection(upper)
        ic.path(geom_d(lace), "#f6f5f4", opacity=0.8, layer_id=f"lace-{k}")
    collar = rr(12, 46, 34, 57, 5)
    solid(ic, collar, face=[(0, "#c99a6d"), (1, "#7a4f2e")], depth=3, side="#5c3a20", layer="collar")
    sole = rr(10, 100, 114, 111, 4)
    solid(ic, sole, face=[(0, "#3d3846"), (1, "#111114")], depth=3, side="#0b0b0d", layer="sole")
    for k, x in enumerate((22, 44, 76, 98)):
        stud = rr(x, 110, x + 8, 116, 2.5)
        solid(ic, stud, face=[(0, "#77767b"), (1, "#3d3846")], depth=1.5, side="#111114", top=False, layer=f"stud-{k}")
    football(ic, 106, 92, 38, name="ball", pent=PENT)
    return ic


def C():
    """Disc - a referee's stopwatch: steel body, blue bezel, white dial with twelve ticks, a long
    minute hand and a green second hand, a crown and a button. The 90-second match clock."""
    ic = gk.Icon("kafa_topu_2 - disc")
    stem = rr(61, 10, 67, 22, 2)
    solid(ic, stem, face=[(0, "#c0bfbc"), (1, "#77767b")], depth=2, side="#5e5c64", layer="stem")
    button = rr(54, 4, 74, 13, 4)
    solid(ic, button, face=[(0, "#f6f5f4"), (0.6, "#c0bfbc"), (1, "#8a8986")], depth=2.5, side="#5e5c64", layer="button")
    body = circ(64, 72, 48)
    solid(ic, body, face=[(0, "#f6f5f4"), (0.5, "#c0bfbc"), (1, "#8a8986")], depth=4, side="#5e5c64", layer="body")
    bezel = circ(64, 72, 44)
    ic.path(geom_d(bezel), ic.linear([(0, BLUE[0]), (0.5, BLUE[1]), (1, BLUE[2])], 0, 28, 0, 116), layer_id="bezel")
    dial = circ(64, 72, 39)
    solid(ic, dial, face=[(0, "#ffffff"), (0.6, LIGHT[2]), (1, LIGHT[3])], depth=1.5, side=LIGHT[4], top=False, layer="dial")
    for k in range(12):
        a = -_m.pi / 2 + k * _m.pi / 6
        tick = box(64 + _m.cos(a) * 33 - 1.4, 72 + _m.sin(a) * 33 - 1.4,
                   64 + _m.cos(a) * 37 + 1.4, 72 + _m.sin(a) * 37 + 1.4)
        ic.path(geom_d(tick), "#3d3846", layer_id=f"tick-{k}")
    hand = box(61.5, 46, 66.5, 73)
    ic.path(geom_d(hand), "#2a2a2e", layer_id="hand-min")
    sec = affinity.rotate(box(63, 44, 65, 74), 40, origin=(64, 72))
    ic.path(geom_d(sec), GREEN[3], layer_id="hand-sec")
    ic.path(geom_d(circ(64, 72, 4)), "#2a2a2e", layer_id="pin")
    return ic


def D():
    """Rimmed - the winner's cup: a gold bowl with two handles, a stem and a wide light-blue plinth
    with a small gold plate. What the 90 seconds are played for."""
    ic = gk.Icon("kafa_topu_2 - rimmed")
    bowl = poly([(30, 22), (98, 22), (90, 70), (38, 70)], 7)
    solid(ic, bowl, face=[(0, "#ffe08a"), (0.5, YELLOW[2]), (1, "#b5835a")], depth=4, side="#8a6420", layer="bowl")
    ic.path(geom_d(rr(26, 16, 102, 26, 5)), ic.linear([(0, "#ffe08a"), (1, YELLOW[3])], 0, 16, 0, 26), layer_id="rim")
    for k, x in enumerate((24, 104)):
        handle = circ(x, 40, 16).difference(circ(x, 40, 10))
        solid(ic, handle, face=[(0, "#ffe08a"), (1, YELLOW[3])], depth=3, side="#8a6420", layer=f"handle-{k}")
    stem = rr(55, 70, 73, 88, 4)
    solid(ic, stem, face=[(0, "#ffe08a"), (1, YELLOW[3])], depth=3, side="#8a6420", layer="stem")
    base = rr(36, 88, 92, 114, 5)
    solid(ic, base, face=[(0, BLUE[0]), (0.5, BLUE[1]), (1, BLUE[2])], depth=4, side="#1c71d8", layer="base")
    plate = rr(50, 93, 78, 105, 2)
    ic.path(geom_d(plate), "#ffe08a", layer_id="plate")
    ic.path(geom_d(rr(56, 97, 72, 99, 1)), "#8a6420", opacity=0.7, layer_id="plate-line")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
