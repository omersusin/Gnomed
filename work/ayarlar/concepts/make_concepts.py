#!/usr/bin/env python3
"""ayarlar - FOUR rough concepts A-D (REDESIGN.md step 3). Run:
    python3 work/ayarlar/concepts/make_concepts.py && python3 tools/concepts.py ayarlar
A plain gear (faithful), B gear + wrench (main), C round knob (disc), D slider panel (rimmed)."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
BROWN = RAMP["Brown"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


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


def A():
    """L1 - the plain brown gear, closest to the source logo; real centre hole."""
    ic = gk.Icon("ayarlar concept A")
    g = gear_big(ic, 64, 118, 104, 24, name="gear")
    toplight(ic, g, width=1.5, opacity=0.6, layer="gear")
    return ic


def wrench_shape(cx, cy, s):
    handle = rounded(box(cx - 5 * s, cy - 26 * s, cx + 5 * s, cy + 18 * s), 3 * s)
    ring = circ(cx, cy - 27 * s, 12 * s).difference(circ(cx, cy - 27 * s, 6 * s))
    jaw = box(cx - 13 * s, cy - 43 * s, cx + 13 * s, cy - 33 * s)
    g = unary_union([handle, ring.difference(jaw)])
    return affinity.rotate(g, -38, origin=(cx, cy))


def B():
    """L2 - the gear with a metal wrench in front: settings / adjust (main)."""
    ic = gk.Icon("ayarlar concept B")
    g = gear_big(ic, 58, 118, 96, 22, name="gear")
    toplight(ic, g, width=1.5, opacity=0.6, layer="gear")
    w = wrench_shape(86, 92, 1.15)
    w = fit([w], (70, 54, 110, 118), anchor="bottom")[0]
    solid(ic, w, face=[(0, LIGHT[0]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=4, side=LIGHT[4], layer="wrench")
    toplight(ic, w, width=1.2, opacity=0.6, layer="wrench")
    return ic


def C():
    """L2 round - a brown control knob with a pointer and tick marks (disc)."""
    ic = gk.Icon("ayarlar concept C")
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
    """L2 - a brown control panel with three recessed sliders (rimmed)."""
    ic = gk.Icon("ayarlar concept D")
    panel = rounded(box(28, 22, 100, 114), 12)
    solid(ic, panel, face=[(0, BROWN[0]), (0.5, BROWN[2]), (1, BROWN[4])], depth=8, side=BROWN[4], layer="panel")
    toplight(ic, panel, width=1.5, opacity=0.6, layer="panel")
    for i, y in enumerate((46, 68, 90)):
        track = rounded(box(38, y - 4, 90, y + 4), 4)
        recess(ic, track, [(0, DARK[3]), (1, DARK[1])], wall=2, layer=f"panel-track{i}")
        kx = (52, 78, 64)[i]
        knob = rounded(box(kx - 8, y - 8, kx + 8, y + 8), 5)
        solid(ic, knob, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer=f"panel-knob{i}")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
