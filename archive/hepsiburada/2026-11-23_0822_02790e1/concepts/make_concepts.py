#!/usr/bin/env python3
"""hepsiburada - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/hepsiburada/concepts/make_concepts.py && python3 tools/concepts.py hepsiburada
A parcel, a shop awning sign, a packing-tape roll and a shopping cart - delivery and shop
objects, different from trendyolmilla's bag/tag/hat box/basket."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)
R = regions(SLUG)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]

ORANGE = "#fe5101"
OR_D = "#c64600"
OR_DD = "#9a3500"
BROWN = RAMP["Brown"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a cardboard parcel with a tape strip and an orange label."""
    ic = gk.Icon("hepsiburada concept A")
    boxg = rr(16, 44, 112, 114, 4)
    solid(ic, boxg, face=[(0, BROWN[1]), (1, BROWN[3])], depth=6, side=BROWN[4], layer="parcel")
    tape = box(56, 44, 72, 114).intersection(boxg)
    ic.path(geom_d(tape), "#d6b48a", opacity=0.85, layer_id="tape")
    label = rr(26, 62, 102, 96, 3)
    solid(ic, label, face=[(0, ORANGE), (1, OR_D)], depth=1.5, side=OR_DD, top=False, layer="label")
    put_mark(ic, SLUG, (30, 68, 98, 90), face="#ffffff")
    return ic


def B():
    """Faithful - a shop awning sign: striped canopy over an orange fascia with the wordmark."""
    ic = gk.Icon("hepsiburada concept B")
    fascia = rr(12, 62, 116, 114, 6)
    solid(ic, fascia, face=[(0, ORANGE), (1, OR_D)], depth=5, side=OR_DD, layer="fascia")
    canopy = poly([(6, 26), (122, 26), (112, 62), (16, 62)], 4)
    solid(ic, canopy, face=[(0, ORANGE), (1, OR_D)], depth=4, side=OR_DD, layer="canopy")
    for x in (30, 54, 78, 102):
        stripe = box(x - 5, 26, x + 5, 62)
        ic.path(geom_d(stripe.intersection(canopy)), "#f6f5f4", opacity=0.55, layer_id=f"stripe-{x}")
    put_mark(ic, SLUG, (24, 66, 104, 106), face="#ffffff")
    return ic


def C():
    """Disc - a roll of packing tape: white tape, orange rim, a paper band with the wordmark."""
    ic = gk.Icon("hepsiburada concept C")
    roll = circ(58, 62, 42)
    solid(ic, roll, face=[(0, "#ffffff"), (1, LIGHT[3])], depth=6, side=LIGHT[4], layer="roll")
    rim = circ(58, 62, 42).difference(circ(58, 62, 34))
    ic.path(geom_d(rim), ORANGE, opacity=0.9, layer_id="rim")
    band = rr(18, 46, 98, 80, 4)
    solid(ic, band, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=2, side=LIGHT[4], top=False, layer="band")
    strip = poly([(94, 78), (110, 84), (106, 114), (92, 108)], 2)
    solid(ic, strip, face=[(0, "#ff7a33"), (1, OR_D)], depth=1.5, side=OR_DD, layer="strip")
    put_mark(ic, SLUG, (22, 50, 94, 76), face=ORANGE)
    return ic


def D():
    """Rimmed - a shopping cart: orange basket with the wordmark, grey frame and wheels."""
    ic = gk.Icon("hepsiburada concept D")
    basket = poly([(24, 48), (104, 48), (96, 92), (34, 92)], 5)
    solid(ic, basket, face=[(0, "#ff7a33"), (1, ORANGE)], depth=5, side=OR_DD, layer="basket")
    handle = rounded(box(100, 48, 112, 52).union(box(102, 24, 106, 50)), 2)
    solid(ic, handle, face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=2, side="#5e5c64", layer="handle")
    for x in (46, 88):
        solid(ic, circ(x, 106, 9), face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer=f"wheel-{x}")
    put_mark(ic, SLUG, (36, 58, 92, 82), face="#ffffff")
    return ic


for f in (A, B, C, D):
    f().save(OUT / f"{f.__name__}.svg")
print("wrote", *(f.name for f in OUT.glob("*.svg")))
