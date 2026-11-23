#!/usr/bin/env python3
"""saat - FOUR rough concepts A-D (BATCH.md). Run:
    python3 work/saat/concepts/make_concepts.py && python3 tools/concepts.py saat
A alarm clock (main), B desk clock (faithful), C pocket watch (disc), D digital clock (rimmed)."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
GREEN = RAMP["Green"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def hand(cx, cy, length, width, angle, colour=DARK[3]):
    g = rounded(box(cx - width / 2, cy - length, cx + width / 2, cy + 2), width / 2)
    return affinity.rotate(g, angle, origin=(cx, cy))


def face(ic, cx, cy, r, depth=6, skeleton=False):
    body = circ(cx, cy, r)
    if skeleton:
        body = body.difference(circ(cx, cy, r * 0.82))      # source ring centre is a real hole
    solid(ic, body, face=[(0, GREEN[0]), (0.5, GREEN[2]), (1, GREEN[4])], depth=depth, side=GREEN[4], layer="clock-body")
    toplight(ic, body, width=1.5, opacity=0.6, layer="clock-body")
    if not skeleton:
        inner = circ(cx, cy, r * 0.82)
        recess(ic, inner, [(0, LIGHT[0]), (1, LIGHT[2])], wall=3, layer="clock-face")
    hand_col = GREEN[3] if skeleton else DARK[3]
    tick_col = GREEN[3] if skeleton else DARK[3]
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        x, y = cx + math.cos(a) * r * 0.68, cy + math.sin(a) * r * 0.68
        tick = affinity.rotate(box(x - 1.2, y - 4, x + 1.2, y + 4), math.degrees(a) + 90, origin=(x, y))
        ic.path(geom_d(tick), tick_col, opacity=0.85, layer_id=f"tick{k}")
    solid(ic, hand(cx, cy, r * 0.50, 5.5, -55), face=hand_col, depth=1.2, side=GREEN[4], top=False, layer="hour")
    solid(ic, hand(cx, cy, r * 0.70, 4.0, 35), face=hand_col, depth=1.2, side=GREEN[4], top=False, layer="minute")
    solid(ic, circ(cx, cy, 4.2), face=hand_col, depth=1.2, side=GREEN[4], top=False, layer="pin")
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
    face(ic, 64, 70, 42)
    return ic


def B():
    """Faithful - a desk clock: round face on a stand (not a plain disc)."""
    ic = gk.Icon("saat concept B")
    stand = rounded(box(46, 104, 82, 118), 4)
    solid(ic, stand, face=[(0, GREEN[1]), (1, GREEN[4])], depth=3, side=GREEN[4], layer="stand")
    face(ic, 64, 66, 46, skeleton=True)
    return ic


def C():
    """Disc - a pocket watch: round case, crown and a ring with a real hole."""
    ic = gk.Icon("saat concept C")
    ring = circ(64, 12, 8).difference(circ(64, 12, 4))
    solid(ic, ring, face=[(0, LIGHT[0]), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer="watch-ring")
    crown = rounded(box(57, 18, 71, 28), 3)
    solid(ic, crown, face=[(0, GREEN[1]), (1, GREEN[4])], depth=3, side=GREEN[4], layer="watch-crown")
    face(ic, 64, 68, 48, depth=8, skeleton=True)
    return ic


SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd",
       "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}


def digit(ic, x, y, w, h, t, segs, colour):
    a = rounded(box(x, y, x + w, y + t), t / 2)
    b = rounded(box(x + w - t, y, x + w, y + h / 2), t / 2)
    c = rounded(box(x + w - t, y + h / 2, x + w, y + h), t / 2)
    d = rounded(box(x, y + h - t, x + w, y + h), t / 2)
    e = rounded(box(x, y + h / 2, x + t, y + h), t / 2)
    f = rounded(box(x, y, x + t, y + h / 2), t / 2)
    g = rounded(box(x, y + h / 2 - t / 2, x + w, y + h / 2 + t / 2), t / 2)
    for name, s in zip("abcdefg", (a, b, c, d, e, f, g)):
        if name in segs:
            solid(ic, s, face=colour, depth=0, top=False, layer=f"seg-{name}")


def D():
    """Rimmed - a digital clock: green cabinet, dark screen, green 7-segment digits."""
    ic = gk.Icon("saat concept D")
    screen = rounded(box(34, 36, 94, 92), 4)
    body = rounded(box(26, 28, 102, 114), 10).difference(screen)
    solid(ic, body, face=[(0, GREEN[0]), (0.5, GREEN[2]), (1, GREEN[4])], depth=8, side=GREEN[4], layer="cabinet")
    toplight(ic, body, width=1.5, opacity=0.6, layer="cabinet")
    for x, ch in ((38, "1"), (50, "0"), (66, "1"), (78, "0")):
        digit(ic, x, 50, 10, 28, 2.8, SEG[ch], GREEN[1])
    for y in (58, 66):
        solid(ic, circ(62, y, 1.8), face=GREEN[1], depth=0, top=False, layer=f"colon{y}")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
