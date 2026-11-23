#!/usr/bin/env python3
"""mesajlar - Gnomed redesign. Main (Symbol) B two chat bubbles; A speech bubble (Faithful);
C round bubble with a notification badge (Disc); D mailbox (Rimmed). Build: python3 tools/make_icon.py mesajlar"""
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


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Faithful - the source's speech bubble with three lines."""
    ic = gk.Icon("mesajlar - faithful")
    b = speech_bubble(ic, 64, 118, 100, ramp=GREEN, name="bubble")
    for i, y in enumerate((48, 62, 76)):
        w = (44, 36, 28)[i]
        line = rr(64 - w / 2, y, 64 + w / 2, y + 5, 2)
        solid(ic, line, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer=f"line{i}")
    return ic


def B():
    """Main - two chat bubbles: a green one behind, a dark one with light lines in front."""
    ic = gk.Icon("mesajlar - symbol")
    speech_bubble(ic, 48, 106, 74, ramp=GREEN, name="bubble-back")
    body = rr(52, 44, 114, 94, 12)
    tail = poly([(94, 92), (110, 92), (104, 108)], 2)
    front = unary_union([body, tail])
    solid(ic, front, face=[(0, DARK[1]), (1, DARK[3])], depth=5, side=DARK[4], layer="bubble-front")
    toplight(ic, front, width=1.5, opacity=0.4, layer="bubble-front")
    for i, (y, w) in enumerate(((56, 44), (68, 36), (80, 26))):
        line = rr(62, y, 62 + w, y + 5, 2)
        solid(ic, line, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1, side=LIGHT[4], top=False, layer=f"line{i}")
    return ic


def C():
    """Disc - a round chat bubble with a red notification badge."""
    ic = gk.Icon("mesajlar - disc")
    outer = unary_union([circ(58, 60, 44), poly([(16, 94), (40, 94), (24, 116)], 2)])
    solid(ic, outer, face=[(0, GREEN[2]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="bubble-rim")
    toplight(ic, outer, width=1.5, opacity=0.5, layer="bubble-rim")
    inner = outer.buffer(-6)
    solid(ic, inner, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], top=False, layer="bubble")
    for i, (y, w) in enumerate(((48, 42), (60, 34), (72, 24))):
        line = rr(36, y, 36 + w, y + 5, 2)
        solid(ic, line, face=[(0, GREEN[3]), (1, GREEN[4])], depth=0, top=False, layer=f"line{i}")
    badge = circ(100, 24, 19)
    solid(ic, badge, face=[(0, RED[1]), (1, RED[3])], depth=5, side=RED[4], layer="badge")
    ic.path(geom_d(circ(100, 24, 6)), LIGHT[0], layer_id="badge-dot")
    return ic


def D():
    """Rimmed - a mailbox on a post: green box, slot, letter, red flag."""
    ic = gk.Icon("mesajlar - rimmed")
    post = rr(60, 86, 68, 118, 3)
    solid(ic, post, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer="post")
    box_ = rr(28, 40, 100, 92, 9)
    solid(ic, box_, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="mailbox")
    toplight(ic, box_, width=2, opacity=0.55, layer="mailbox")
    slot = rr(40, 54, 88, 60, 2)
    recess(ic, slot, [(0, DARK[4]), (1, DARK[2])], wall=2, layer="slot")
    letter = rr(48, 46, 82, 72, 2)
    solid(ic, letter, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer="letter")
    flag_pole = rr(92, 44, 96, 76, 1.6)
    solid(ic, flag_pole, face=[(0, DARK[1]), (1, DARK[3])], depth=2, side=DARK[4], layer="flag-pole")
    flag = poly([(92, 44), (110, 50), (92, 58)], 1)
    solid(ic, flag, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="flag")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
