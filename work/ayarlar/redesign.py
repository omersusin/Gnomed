#!/usr/bin/env python3
"""ayarlar - Gnomed redesign.
Main (Symbol) A: the brown gear. Kept: B -> Faithful (crossed wrench + screwdriver),
C -> Disc (round control knob), D -> Rimmed (switch/slider panel).
Build:  python3 tools/make_icon.py ayarlar"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
SLUG = Path(__file__).resolve().parent.name
BROWN = RAMP["Brown"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
GREEN = RAMP["Green"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def gear_big(ic, cx, base, size, hole_r, ramp=BROWN, name="gear"):
    """Gear with the source's big centre hole (the stock gear() hole is too small)."""
    d = max(3, size * 0.07)
    r = size / 2
    cy = base - d - r
    body_ = circ(cx, cy, r * 0.78)
    tooth = [affinity.translate(affinity.rotate(box(-r * 0.14, -r, r * 0.14, 0), 360 * k / 8, origin=(0, 0)), cx, cy)
             for k in range(8)]
    g = unary_union([body_] + tooth).buffer(0.8).buffer(-0.8).difference(circ(cx, cy, hole_r))
    solid(ic, g, face=[(0, ramp[0]), (0.5, ramp[2]), (1, ramp[4])], depth=d, side=RAMP["Dark"][0], layer=name)
    return g


def wrench_shape(cx, cy, s):
    handle = rounded(box(cx - 5 * s, cy - 26 * s, cx + 5 * s, cy + 18 * s), 3 * s)
    ring = circ(cx, cy - 27 * s, 12 * s).difference(circ(cx, cy - 27 * s, 6 * s))
    jaw = box(cx - 13 * s, cy - 43 * s, cx + 13 * s, cy - 33 * s)
    return affinity.rotate(unary_union([handle, ring.difference(jaw)]), -38, origin=(cx, cy))


def A():
    ic = gk.Icon("ayarlar - faithful")
    g = gear_big(ic, 64, 118, 104, 24, name="gear")
    toplight(ic, g, width=1.5, opacity=0.6, layer="gear")
    return ic


def screwdriver(cx, cy, s):
    """A screwdriver: fluted brown handle, steel ferrule and shaft, flat tip."""
    handle = rr(cx - 8 * s, cy - 46 * s, cx + 8 * s, cy - 12 * s, 6 * s)
    ferrule = rr(cx - 5.5 * s, cy - 15 * s, cx + 5.5 * s, cy - 9 * s, 2 * s)
    shaft = unary_union([box(cx - 2.6 * s, cy - 10 * s, cx + 2.6 * s, cy + 22 * s),
                         box(cx - 4.5 * s, cy + 22 * s, cx + 4.5 * s, cy + 27 * s)])
    grooves = unary_union([box(cx - 8 * s, cy - (43 - 9 * k) * s, cx + 8 * s, cy - (40 - 9 * k) * s)
                           for k in range(3)]).intersection(handle)
    return handle, ferrule, shaft, grooves


def B():
    """Faithful - crossed tools: a steel wrench over a screwdriver with a fluted handle."""
    ic = gk.Icon("ayarlar - faithful")
    h, fer, shaft, gr = screwdriver(70, 56, 1.0)
    h = affinity.rotate(h, 48, origin=(70, 56))
    fer = affinity.rotate(fer, 48, origin=(70, 56))
    shaft = affinity.rotate(shaft, 48, origin=(70, 56))
    gr = affinity.rotate(gr, 48, origin=(70, 56))
    w = wrench_shape(58, 72, 1.12)
    h, fer, shaft, gr, w = fit([h, fer, shaft, gr, w], (8, 8, 120, 120), anchor="center")
    solid(ic, shaft, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="screwdriver")
    solid(ic, fer, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="ferrule")
    solid(ic, h, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[4])], depth=5, side=BROWN[4], layer="handle")
    toplight(ic, h, width=1.5, opacity=0.6, layer="handle")
    ic.path(geom_d(gr), BROWN[4], opacity=0.55, layer_id="handle-grooves")
    solid(ic, w, face=[(0, LIGHT[0]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=5, side=LIGHT[4], layer="wrench")
    toplight(ic, w, width=1.5, opacity=0.6, layer="wrench")
    return ic


def C():
    ic = gk.Icon("ayarlar - disc")
    base, r = 122, 52
    cy = base - 8 - r
    body = circ(64, cy, r)
    solid(ic, body, face=[(0, BROWN[0]), (0.5, BROWN[2]), (1, BROWN[4])], depth=8, side=BROWN[4], layer="knob")
    toplight(ic, body, width=1.5, opacity=0.6, layer="knob")
    face = circ(64, cy, r * 0.82)
    recess(ic, face, [(0, BROWN[3]), (1, BROWN[1])], wall=4, layer="knob-face")
    pointer = rounded(box(60.5, cy - r * 0.72, 67.5, cy + 4), 2.5)
    solid(ic, pointer, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.2, side=LIGHT[4], top=False, layer="knob-pointer")
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        x, y = 64 + math.cos(a) * r * 0.90, cy + math.sin(a) * r * 0.90
        tick = affinity.rotate(rounded(box(x - 1.4, y - 4, x + 1.4, y + 4), 1.4), math.degrees(a) + 90, origin=(x, y))
        ic.path(geom_d(tick), LIGHT[2], opacity=0.85, layer_id=f"knob-tick{k}")
    return ic


def D():
    """Rimmed - a settings panel: two switches (one on, one off) and a slider."""
    ic = gk.Icon("ayarlar - rimmed")
    panel = rr(22, 18, 106, 116, 11)
    solid(ic, panel, face=[(0, DARK[1]), (0.5, DARK[2]), (1, DARK[3])], depth=8, side=DARK[4], layer="panel")
    toplight(ic, panel, width=1.5, opacity=0.55, layer="panel")
    for i, (y, on) in enumerate(((40, True), (64, False))):
        label = rr(32, y - 3, 56, y + 3, 1.5)
        ic.path(geom_d(label), LIGHT[2], opacity=0.75, layer_id=f"label{i}")
        track = rr(62, y - 9, 96, y + 9, 8)
        solid(ic, track, face=[(0, GREEN[1]), (1, GREEN[3])] if on else [(0, LIGHT[2]), (1, LIGHT[4])],
              depth=2, side=GREEN[4] if on else LIGHT[4], layer=f"track{i}")
        kx = 87 if on else 71
        knob = circ(kx, y, 7.5)
        solid(ic, knob, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer=f"knob{i}")
    sy = 90
    label = rr(32, sy - 3, 56, sy + 3, 1.5)
    ic.path(geom_d(label), LIGHT[2], opacity=0.75, layer_id="label2")
    rail = rr(62, sy - 3, 96, sy + 3, 2.6)
    recess(ic, rail, [(0, DARK[4]), (1, DARK[2])], wall=1.6, layer="slider-rail")
    active = rr(62, sy - 2.2, 82, sy + 2.2, 2)
    ic.path(geom_d(active), GREEN[3], layer_id="slider-active")
    for k in range(4):
        x = 66 + k * 8
        ic.path(geom_d(rr(x - 1, sy + 6, x + 1, sy + 9, 1)), LIGHT[3], opacity=0.8, layer_id=f"tick{k}")
    sk = circ(82, sy, 8.5)
    solid(ic, sk, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="slider-knob")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
