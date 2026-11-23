#!/usr/bin/env python3
"""saat - Gnomed redesign. Main (Symbol) A alarm clock; B desk clock (Faithful);
C stopwatch (Disc); D digital clock (Rimmed). Build: python3 tools/make_icon.py saat"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
OUT = Path(__file__).resolve().parent
GREEN = RAMP["Green"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def hand(cx, cy, length, width, angle, colour=DARK[3]):
    g = rounded(box(cx - width / 2, cy - length, cx + width / 2, cy + 2), width * 0.40)
    return affinity.rotate(g, angle, origin=(cx, cy))


def face(ic, cx, cy, r, depth=6, hole=0.0):
    """Clock face. hole=0 -> solid dial; hole=0.6 -> skeleton ring (the source's centre is a hole)."""
    body = circ(cx, cy, r)
    if hole:
        body = body.difference(circ(cx, cy, r * hole))
    solid(ic, body, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=depth, side=GREEN[4], layer="clock-body")
    toplight(ic, body, width=1.5, opacity=0.6, layer="clock-body")
    if not hole:
        recess(ic, circ(cx, cy, r * 0.82), [(0, LIGHT[0]), (1, LIGHT[2])], wall=3, layer="clock-face")
        tick_r, tick_col = r * 0.68, DARK[3]
    else:
        tick_r, tick_col = r * (hole + (1 - hole) * 0.45), GREEN[0]
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        x, y = cx + math.cos(a) * tick_r, cy + math.sin(a) * tick_r
        tick = affinity.rotate(box(x - 1.3, y - 4, x + 1.3, y + 4), math.degrees(a) + 90, origin=(x, y))
        ic.path(geom_d(tick), tick_col, opacity=0.85, layer_id=f"tick{k}")
    hlen, mlen = (r * 0.94, r * 0.99) if hole else (r * 0.50, r * 0.70)

    def hand2(length, width, angle, layer):
        out = hand(cx, cy, length, width + 2.6, angle)
        solid(ic, out, face=DARK[4], depth=1.2, side=DARK[4], top=False, layer=f"{layer}-out")
        inn = hand(cx, cy, length, width, angle)
        solid(ic, inn, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.2, side=LIGHT[4], top=False, layer=layer)

    hand2(hlen, 4.6, -55, "hour")
    hand2(mlen, 3.4, 35, "minute")
    solid(ic, circ(cx, cy, 5.2), face=DARK[4], depth=1.2, side=DARK[4], top=False, layer="pin-out")
    solid(ic, circ(cx, cy, 3.6), face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.2, side=LIGHT[4], top=False, layer="pin")
    return body


def A():
    """Main - an alarm clock: green body, two bells, legs, white face."""
    ic = gk.Icon("saat concept A")
    for x in (42, 86):
        bell = circ(x, 26, 11)
        solid(ic, bell, face=[(0, GREEN[1]), (0.5, GREEN[2]), (1, GREEN[4])], depth=4, side=GREEN[4], layer=f"bell{x}")
        toplight(ic, bell, width=1.2, opacity=0.6, layer=f"bell{x}")
    for x in (42, 86):
        leg = rounded(box(x - 4, 104, x + 4, 118), 2)
        solid(ic, leg, face=[(0, GREEN[2]), (1, GREEN[4])], depth=2, side=GREEN[4], top=False, layer=f"leg{x}")
    hammer = rounded(box(59, 16, 69, 28), 3)
    solid(ic, hammer, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=3, side=LIGHT[4], layer="hammer")
    face(ic, 64, 70, 42, hole=0.60)
    return ic


def B():
    """Faithful - a desk clock: round face on a stand (not a plain disc)."""
    ic = gk.Icon("saat concept B")
    stand = rounded(box(46, 101, 82, 115), 4)
    solid(ic, stand, face=[(0, GREEN[1]), (1, GREEN[4])], depth=3, side=GREEN[4], layer="stand")
    face(ic, 64, 66, 46, hole=0.70)
    return ic


def C():
    """Disc - a stopwatch: silver case, green skeleton dial, push button on top, side pusher."""
    ic = gk.Icon("saat concept C")
    push = rounded(box(52, 8, 76, 22), 4)
    solid(ic, push, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="pusher")
    toplight(ic, push, width=1.2, opacity=0.6, layer="pusher")
    stem = rounded(box(60, 20, 68, 32), 2)
    solid(ic, stem, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="stem")
    side = LineString([(96, 36), (108, 24)]).buffer(5.5, cap_style=1)
    solid(ic, side, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="side-pusher")
    case = circ(64, 68, 46).difference(circ(64, 68, 37))
    solid(ic, case, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=8, side=LIGHT[4], layer="case")
    toplight(ic, case, width=2, opacity=0.6, layer="case")
    face(ic, 64, 68, 37, depth=5, hole=0.78)
    return ic


SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd",
       "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}


def digit(ic, x, y, w, h, t, segs, colour):
    rr = t * 0.38
    a = rounded(box(x, y, x + w, y + t), rr)
    b = rounded(box(x + w - t, y, x + w, y + h / 2), rr)
    c = rounded(box(x + w - t, y + h / 2, x + w, y + h), rr)
    d = rounded(box(x, y + h - t, x + w, y + h), rr)
    e = rounded(box(x, y + h / 2, x + t, y + h), rr)
    f = rounded(box(x, y, x + t, y + h / 2), rr)
    g = rounded(box(x, y + h / 2 - t / 2, x + w, y + h / 2 + t / 2), rr)
    for name, s in zip("abcdefg", (a, b, c, d, e, f, g)):
        if name in segs:
            solid(ic, s, face=colour, depth=0, top=False, layer=f"seg-{name}")


def D():
    """Rimmed - a digital desk clock: wide cabinet on two feet, dark screen, 7-segment 10:10."""
    ic = gk.Icon("saat concept D")
    for x in (34, 84):
        foot = rounded(box(x, 98, x + 10, 116), 3)
        solid(ic, foot, face=[(0, GREEN[2]), (1, GREEN[4])], depth=3, side=GREEN[4], layer=f"foot{x}")
    body = rounded(box(16, 30, 112, 102), 10)
    solid(ic, body, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=8, side=GREEN[4], layer="cabinet")
    toplight(ic, body, width=1.5, opacity=0.6, layer="cabinet")
    screen = rounded(box(24, 38, 104, 86), 4)
    recess(ic, screen, [(0, "#241f31"), (1, DARK[2])], wall=3, layer="screen")
    digital_display(ic, "10:10", (28, 48, 100, 76), color=GREEN[1])
    for i, (x, col) in enumerate(((34, GREEN[2]), (64, LIGHT[3]), (94, GREEN[2]))):
        led = circ(x, 93, 3)
        solid(ic, led, face=[(0, col), (1, GREEN[4])], depth=1, side=GREEN[4], top=False, layer=f"led{i}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
