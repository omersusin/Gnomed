#!/usr/bin/env python3
"""hepsiburada - Gnomed redesign.
Main (Symbol) A: a cardboard parcel with an orange label. Faithful B: a shop awning sign -
orange fascia with the white wordmark under a striped canopy. Disc C: a round hanging shop sign -
white enamel disc, orange rim, steel bracket and links. Rimmed D: a shopping cart with the wordmark
on its basket."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
ORANGE = "#fe5101"
OR_L = "#ff7a33"
OR_D = "#c64600"
OR_DD = "#9a3500"
BROWN = RAMP["Brown"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - an orange delivery van: cargo box, cab, dark windscreen and wheels, the white
    wordmark on the side panel. The app's function on the road."""
    ic = gk.Icon("hepsiburada - symbol")
    cargo = rr(8, 42, 92, 106, 6)
    cab = poly([(90, 58), (108, 58), (120, 74), (120, 106), (90, 106)], 5)
    solid(ic, cargo.union(cab), face=[(0, OR_L), (0.6, ORANGE), (1, OR_D)], depth=6, side=OR_DD, layer="van")
    glass = poly([(95, 63), (107, 63), (115, 75), (95, 75)], 3)
    solid(ic, glass, face=[(0, "#5e5c64"), (1, DARK[4])], depth=1.5, side=DARK[4], top=False, layer="glass")
    panel = rr(18, 54, 84, 96, 4)
    solid(ic, panel, face=[(0, OR_D), (1, "#b23c00")], depth=2, side=OR_DD, top=False, layer="panel")
    put_mark(ic, SLUG, (22, 60, 80, 92), face="#ffffff", depth=1.2, side="#ffffff")
    for x in (30, 98):
        solid(ic, circ(x, 108, 10.5), face=[(0, DARK[1]), (1, "#1b1a1f")], depth=3, side="#1b1a1f", layer=f"wheel-{x}")
        solid(ic, circ(x, 108, 4), face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=1, side="#5e5c64", top=False, layer=f"hub-{x}")
    light = rr(112, 82, 120, 92, 3)
    solid(ic, light, face=[(0, "#f9e56b"), (1, "#e5a50a")], depth=1.5, side="#c64600", top=False, layer="headlight")
    return ic


def B():
    """Faithful - a cardboard parcel with an orange label carrying the white wordmark: the
    closest style to the orange logo, applied to the thing the app delivers."""
    ic = gk.Icon("hepsiburada - faithful")
    boxg = rr(14, 42, 114, 114, 4)
    solid(ic, boxg, face=[(0, BROWN[1]), (0.55, BROWN[2]), (1, BROWN[3])], depth=6, side=BROWN[4], layer="parcel")
    tape = box(56, 42, 72, 114).intersection(boxg)
    ic.path(geom_d(tape), "#e2c7a4", opacity=0.9, layer_id="tape")
    toplight(ic, boxg, width=1.6, opacity=0.4, layer="parcel")
    label = rr(22, 60, 106, 98, 3)
    solid(ic, label, face=[(0, OR_L), (1, OR_D)], depth=1.5, side=OR_DD, top=False, layer="label")
    put_mark(ic, SLUG, (26, 64, 102, 94), face="#ffffff", depth=1.2, side="#ffffff")
    return ic


def C():
    """Disc - a round hanging shop sign: a white enamel disc with an orange rim, hung from a
    steel bracket by two links, the orange wordmark on its face and a soft shadow below."""
    ic = gk.Icon("hepsiburada - disc")
    arm = rr(50, 6, 78, 12, 3)
    solid(ic, arm, face=[(0, "#9a9996"), (1, "#5e5c64")], depth=2, side="#3d3846", layer="bracket")
    post = rr(61, 10, 67, 22, 2)
    solid(ic, post, face=[(0, "#9a9996"), (1, "#5e5c64")], depth=2, side="#3d3846", layer="post")
    for k, x in enumerate((52, 64, 76)):
        link = circ(x, 16, 3.4).difference(circ(x, 16, 1.8))
        ic.path(geom_d(link), "#77767b", layer_id=f"link-{k}")
    shadow = ellipse(64, 118, 40, 5)
    ic.path(geom_d(shadow), "#000000", opacity=0.10, layer_id="shadow")
    disc = circ(64, 72, 42)
    solid(ic, disc, face=[(0, "#ffffff"), (0.7, LIGHT[2]), (1, LIGHT[3])], depth=5, side=LIGHT[4], layer="disc")
    rim = circ(64, 72, 42).difference(circ(64, 72, 37))
    ic.path(geom_d(rim), ORANGE, layer_id="rim")
    inner = circ(64, 72, 36)
    toplight(ic, inner, width=2.4, opacity=0.5, layer="disc")
    put_mark(ic, SLUG, (36, 57, 92, 87), face=ORANGE)
    holder = rr(60, 28, 68, 36, 2)
    ic.path(geom_d(holder), "#77767b", layer_id="holder")
    return ic


def D():
    """Rimmed - a shopping cart: orange wire basket with the white wordmark, a grey handle and
    two wheels."""
    ic = gk.Icon("hepsiburada - rimmed")
    basket = poly([(14, 36), (112, 36), (100, 94), (26, 94)], 5)
    solid(ic, basket, face=[(0, OR_L), (0.5, ORANGE), (1, OR_D)], depth=5, side=OR_DD, layer="basket")
    for y in (42, 88):
        rib = box(18, y, 108, y + 3).intersection(basket)
        ic.path(geom_d(rib), "#f6f5f4", opacity=0.55, layer_id=f"rib-{y}")
    handle = rounded(box(102, 32, 118, 38).union(box(108, 6, 114, 36)), 3)
    solid(ic, handle, face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=2.5, side="#5e5c64", layer="handle")
    for x in (40, 92):
        leg = box(x - 2.4, 94, x + 2.4, 106)
        solid(ic, leg, face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=2, side="#5e5c64", top=False, layer=f"leg-{x}")
        solid(ic, circ(x, 110, 11), face=[(0, DARK[1]), (1, DARK[3])], depth=3, side="#1b1a1f", layer=f"wheel-{x}")
    put_mark(ic, SLUG, (32, 52, 96, 80), face="#ffffff")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
