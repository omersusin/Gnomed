#!/usr/bin/env python3
"""stride - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/stride/concepts/make_concepts.py && python3 tools/concepts.py stride
Each function is ONE different idea from the ladder; flat shapes are fine. REPLACE the example bodies.
The app's mark always comes from P (measured), never from memory. Ready objects: from objects import *
(catalogue: docs/redesign/OBJECTS.md). NEVER the logo on a plain tile/square or disc (REDESIGN.md 1)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402   (objects.py + obj.py: gk, solid, parts, fit, RAMP ...)
from shapely.geometry import LineString, Polygon

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)        # r0, r1 ... = colour regions; "holes" = what the mark ENCLOSES (a letter's
                       # counter, or a figure inside a ring - e.g. Telegram's plane). Which is which:
                       # print(describe(SLUG)) - colour + box of every part.
R = regions(SLUG)      # the coloured parts [(name, shape, fill)]. Bands of ONE source gradient come
                       # back merged ("r1+r2") with a real gradient fill (Grad) - never colour() per band:
                       # flat bands look melted (docs/PLAYBOOK.md#gradients)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]
# THE MARK ON EVERY STYLE (REDESIGN.md 5, gate `mark`): put_mark(ic, SLUG, box, face=...) draws the
# measured mark WITHOUT the tile under it, inside a layer named "mark" - the gate finds it there.

MINT = ("#a4f19b", "#7fe0a0", "#58d89a", "#2ec27e", "#1f9c72")     # the logo's green (source.png)
TEAL = ("#2c7a66", "#1f5a48", "#13342b", "#0b241e", "#071a15")     # the app's dark cards (shot-1/2)
CREAM = ("#ffffff", "#f6f5f4", "#e1eae2", "#c8d8cc", "#a9bfb1")    # the light theme (shot-3)
LIME = ("#d7e8a0", "#c8dc88", "#b7ce74", "#93a94f", "#6f8138")     # Start button / bars (shot-6)
INK = ("#1b1a1f", "#0b0f0f", "#060807", "#000000")                 # the near-black screens


def wavy_disc(cx, cy, r, amp, n=14):
    """The app's scalloped goal ring as a closed wavy disc (shot-2/3)."""
    pts = []
    for k in range(240):
        a = 2 * math.pi * k / 240
        rr = r + amp * math.cos(n * a)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return Polygon(pts)


def shoe(ic):
    """A mint running shoe, side view: high ankle, dark ankle patch for the mark, cream laces,
    cream toe cap and a deep-teal sole whose top edge is the app's wavy goal ring."""
    upper = rounded(Polygon([(12, 102), (12, 46), (16, 34), (24, 30), (52, 30), (60, 36),
                             (66, 50), (72, 62), (86, 68), (100, 76), (112, 84), (120, 92),
                             (120, 102)]), 6)
    solid(ic, upper, face=[(0, MINT[0]), (0.5, MINT[2]), (1, MINT[3])], depth=5,
          side=MINT[4], layer="shoe-upper")
    # cream toe cap
    toe = rounded(Polygon([(104, 80), (114, 87), (120, 94), (120, 102), (100, 102)]), 4)
    solid(ic, toe, face=[(0, CREAM[0]), (1, CREAM[2])], depth=2, side=CREAM[4], top=False,
          layer="shoe-toe")
    # dark ankle patch (the mark goes on it)
    patch = rounded(box(14, 42, 54, 94), 7)
    solid(ic, patch, face=[(0, INK[0]), (0.5, INK[1]), (1, INK[2])], depth=2, side=INK[3],
          top=False, layer="shoe-patch")
    put_mark(ic, SLUG, (16, 44, 52, 92))
    # padded collar (a real recess) and the tongue + laces
    recess(ic, ellipse(37, 36, 14, 6.5), [(0, TEAL[3]), (1, TEAL[2])], wall=2, layer="shoe-collar")
    tongue = rounded(box(52, 32, 68, 66), 5)
    solid(ic, tongue, face=[(0, CREAM[0]), (1, CREAM[2])], depth=2, side=CREAM[4], top=False,
          layer="shoe-tongue")
    for i, y in enumerate((39, 46, 53, 60)):
        ic.path(geom_d(rounded(box(50, y, 70, y + 2.8), 1.4)), CREAM[0], layer_id=f"shoe-lace-{i}")
    # heel tab
    tab = rounded(box(12, 23, 23, 34), 3)
    solid(ic, tab, face=[(0, LIME[0]), (1, LIME[2])], depth=1.5, side=LIME[4], top=False,
          layer="shoe-tab")
    # the sole, its top edge the wavy goal ring
    sole = rounded(Polygon([(8, 104), (18, 99), (28, 104), (38, 99), (48, 104), (58, 99),
                            (68, 104), (78, 99), (88, 104), (98, 99), (108, 104), (118, 100),
                            (120, 110), (118, 118), (10, 118), (8, 112)]), 4)
    solid(ic, sole, face=[(0, TEAL[0]), (0.5, TEAL[2]), (1, TEAL[4])], depth=4, side=TEAL[4],
          layer="shoe-sole")
    wave = LineString([(10, 106), (18, 101), (28, 106), (38, 101), (48, 106), (58, 101),
                       (68, 106), (78, 101), (88, 106), (98, 101), (108, 106), (117, 102)])
    ic.path(geom_d(wave.buffer(1.5, cap_style=1)), "#76d2c5", layer_id="sole-wave")


def A():
    """Symbol - the running shoe ("Every step, counted"): a mint sneaker with a dark ankle patch
    carrying the logo, cream laces and the app's wavy goal ring as its sole (anchors 1, 2)."""
    ic = gk.Icon("stride concept A")
    shoe(ic)
    return ic


def B():
    """Faithful - the logo itself as a solid object: the mint runner with its wave and the
    dark-teal side (anchors 1, 2)."""
    ic = gk.Icon("stride concept B")
    put_mark(ic, SLUG, (12, 10, 116, 112), body=7, side=TEAL[3], anchor="bottom")
    return ic


def C():
    """Disc - the wavy goal ring as an award rosette: mint scalloped band, near-black centre with
    the runner, two lime ribbon tails (anchors 1, 2, 3)."""
    ic = gk.Icon("stride concept C")
    for pts in ([(40, 84), (58, 84), (48, 118), (38, 110), (28, 118)],
                [(70, 84), (88, 84), (100, 118), (90, 110), (80, 118)]):
        tail = rounded(Polygon(pts), 2)
        solid(ic, tail, face=[(0, LIME[0]), (0.5, LIME[2]), (1, LIME[3])], depth=3,
              side=LIME[4], top=False, layer="medal-ribbon")
    outer = wavy_disc(64, 54, 46, 2.4, 14)
    solid(ic, outer, face=[(0, "#a7efe2"), (0.5, "#76d2c5"), (1, "#3aa89b")], depth=6,
          side="#1f6e66", layer="medal")
    recess(ic, circ(64, 54, 36.5), [(0, INK[0]), (0.5, INK[1]), (1, INK[2])], wall=3,
           layer="medal-centre")
    put_mark(ic, SLUG, (42, 31, 86, 80))
    return ic


def D():
    """Rimmed - the walk map ("Track your walks"): a folded paper map with the light-blue water,
    a deep-teal route, a lime pin and the logo on the dark map label (anchors 1, 4)."""
    ic = gk.Icon("stride concept D")
    body = rounded(Polygon([(10, 36), (46, 30), (82, 36), (118, 30), (118, 114), (114, 118),
                            (14, 118), (10, 114)]), 4)
    solid(ic, body, face=[(0, CREAM[0]), (0.5, CREAM[1]), (1, "#e8e6e3")], depth=4,
          side=CREAM[3], layer="map")
    for x in (46, 82):
        ic.path(geom_d(LineString([(x, 32), (x, 116)]).buffer(0.8, cap_style=1)), CREAM[2],
                layer_id=f"map-fold-{x}")
    water = rounded(Polygon([(14, 40), (40, 38), (44, 54), (34, 70), (16, 66)]), 4)
    ic.path(geom_d(water), ic.linear([(0, "#c8e8ee"), (1, "#a6d0dc")], 0, 38, 0, 70),
            layer_id="map-water")
    route = LineString([(60, 92), (68, 86), (76, 78), (84, 68), (90, 59), (94, 53)]).buffer(1.8, cap_style=1)
    ic.path(geom_d(route), TEAL[2], layer_id="map-route")
    pin = unary_union([circ(94, 48, 9), Polygon([(86.5, 52), (101.5, 52), (94, 64)])])
    solid(ic, pin, face=[(0, LIME[0]), (0.5, LIME[2]), (1, LIME[3])], depth=3, side=LIME[4],
          layer="map-pin")
    ic.path(geom_d(circ(94, 48, 3.2)), TEAL[2], layer_id="map-pin-hole")
    label = rounded(box(14, 72, 58, 114), 5)
    solid(ic, label, face=[(0, TEAL[1]), (0.5, TEAL[2]), (1, TEAL[3])], depth=3, side=TEAL[4],
          top=False, layer="map-label")
    put_mark(ic, SLUG, (17, 75, 55, 111))
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
