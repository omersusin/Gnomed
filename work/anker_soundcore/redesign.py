#!/usr/bin/env python3
"""anker_soundcore - Gnomed redesign.
Main (Symbol) A: a wooden bookshelf speaker. Faithful B: an open earbuds case. Disc C: over-ear
headphones. Rimmed D: a soundbar."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
BROWN = RAMP["Brown"]
RED = RAMP["Red"]
CYAN = "#0dc4ed"
CYAN_D = "#0b84a5"
CYAN_DD = "#08546c"


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a wooden bookshelf speaker: brown cabinet, the white wordmark on the baffle, one
    big woofer with a cyan ring."""
    ic = gk.Icon("anker_soundcore - symbol")
    cab = rr(16, 16, 112, 116, 7)
    solid(ic, cab, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[3])], depth=8, side=BROWN[4], layer="cabinet")
    toplight(ic, cab, width=1.8, opacity=0.55, layer="cabinet")
    baffle = rr(24, 24, 104, 108, 5)
    solid(ic, baffle, face=[(0, "#2f2d33"), (1, DARK[3])], depth=2, side=DARK[3], top=False, layer="baffle")
    put_mark(ic, SLUG, (30, 28, 98, 56), face="#ffffff")
    ring = circ(64, 84, 23).difference(circ(64, 84, 18))
    solid(ic, ring, face=[(0, CYAN), (1, CYAN_D)], depth=3, side=CYAN_DD, layer="woofer-ring")
    cone = circ(64, 84, 18)
    solid(ic, cone, face=[(0, DARK[1]), (1, "#1b1a1f")], depth=3, side=DARK[3], top=False, layer="woofer")
    cap = circ(64, 84, 7)
    solid(ic, cap, face=[(0, CYAN_D), (1, CYAN_DD)], depth=2, side=CYAN_DD, top=False, layer="dustcap")
    led = circ(30, 100, 3)
    solid(ic, led, face=[(0, CYAN), (1, CYAN_D)], depth=1, side=CYAN_DD, top=False, layer="led")
    return ic


def B():
    """Faithful - an open earbuds case: the source's blue gradient on the lid with the wordmark,
    two buds in the case."""
    ic = gk.Icon("anker_soundcore - faithful")
    base = rr(18, 54, 110, 112, 16)
    solid(ic, base, face=[(0, CYAN), (0.6, CYAN_D), (1, CYAN_DD)], depth=6, side=CYAN_DD, layer="case")
    for i, x in enumerate((46, 82)):
        bud = circ(x, 84, 14)
        solid(ic, bud, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer=f"bud{i}")
    lid = rr(18, 18, 110, 60, 14)
    solid(ic, lid, face=gradient(SLUG, lid), depth=5, side=CYAN_DD, layer="lid")
    put_mark(ic, SLUG, (29, 21, 99, 49), face="#ffffff")
    return ic


def C():
    """Disc - over-ear headphones: dark band, two dark cups with cyan cushions."""
    ic = gk.Icon("anker_soundcore - disc")
    band = circ(64, 74, 46).difference(circ(64, 74, 37)).intersection(box(0, 0, 128, 76))
    solid(ic, band, face=[(0, DARK[1]), (1, DARK[3])], depth=4, side="#1b1a1f", layer="band")
    toplight(ic, band, width=1.4, opacity=0.4, layer="band")
    pad = rr(24, 18, 104, 48, 12)
    solid(ic, pad, face=[(0, DARK[1]), (0.6, DARK[2]), (1, DARK[3])], depth=4, side="#1b1a1f", layer="headband")
    toplight(ic, pad, width=1.4, opacity=0.4, layer="headband")
    put_mark(ic, SLUG, (32, 22, 96, 46), face="#ffffff")
    for i, x in enumerate((30, 98)):
        cup = circ(x, 86, 22)
        solid(ic, cup, face=[(0, DARK[1]), (0.6, DARK[2]), (1, DARK[3])], depth=6, side="#1b1a1f", layer=f"cup{i}")
        toplight(ic, cup, width=1.6, opacity=0.4, layer=f"cup{i}")
        ring = circ(x, 86, 15).difference(circ(x, 86, 9))
        solid(ic, ring, face=[(0, CYAN), (1, CYAN_D)], depth=3, side=CYAN_DD, layer=f"cushion{i}")
        ic.path(geom_d(circ(x, 86, 9)), "#1b1a1f", layer_id=f"cushion-hole{i}")
        fork = rr(x - 3, 62, x + 3, 74, 1.5)
        solid(ic, fork, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], top=False, layer=f"fork{i}")
    return ic


def D():
    """Rimmed - a hi-fi amplifier: silver face, a dark badge with the white wordmark, two knobs,
    a VU meter and feet."""
    ic = gk.Icon("anker_soundcore - rimmed")
    for x in (28, 100):
        foot = rr(x - 8, 106, x + 8, 118, 3)
        solid(ic, foot, face=[(0, DARK[2]), (1, DARK[3])], depth=2, side="#1b1a1f", layer=f"foot{x}")
    body = rr(8, 44, 120, 110, 5)
    solid(ic, body, face=[(0, LIGHT[0]), (0.55, LIGHT[1]), (1, LIGHT[3])], depth=6, side=LIGHT[4], layer="body")
    toplight(ic, body, width=1.8, opacity=0.9, layer="body")
    badge = rr(26, 54, 102, 80, 2)
    solid(ic, badge, face=[(0, "#2f2d33"), (1, DARK[3])], depth=1.5, side=DARK[3], top=False, layer="badge")
    put_mark(ic, SLUG, (28, 54, 100, 80), face="#ffffff")
    knob1 = circ(32, 94, 12)
    solid(ic, knob1, face=[(0, LIGHT[1]), (0.6, LIGHT[2]), (1, LIGHT[4])], depth=4, side=LIGHT[4], layer="knob1")
    toplight(ic, knob1, width=1.2, opacity=0.8, layer="knob1")
    knob2 = circ(60, 94, 8)
    solid(ic, knob2, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="knob2")
    meter = rr(74, 82, 114, 104, 2)
    recess(ic, meter, [(0, CYAN), (0.6, CYAN_D), (1, CYAN_DD)], wall=2, layer="meter")
    needle = LineString([(94, 100), (102, 86)]).buffer(1.2)
    ic.path(geom_d(needle), RED[1], layer_id="meter-needle")
    led = circ(114, 58, 2.4)
    solid(ic, led, face=[(0, CYAN), (1, CYAN_D)], depth=1, side=CYAN_DD, top=False, layer="led")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
