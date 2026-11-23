#!/usr/bin/env python3
"""enpara - Gnomed redesign.
Main (Symbol) A: a bank card with the magenta en and a four-colour edge stripe. Faithful B: a
magenta wallet with a white card. Disc C: a coin with the en embossed. Rimmed D: a safe with a dial
and the en on its door."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
MAG = "#aa519e"
MAG_D = "#8a3d80"
MAG_DD = "#6a2c62"
ORANGE = "#faa91a"
ORANGE_D = "#cf8610"
GREEN = "#9ec842"
GREEN_D = "#7ba32c"
BLUE = "#26abe2"
BLUE_D = "#1a86b4"
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a bank card: a white card with the magenta en, a gold chip and a four-colour
    stripe along the bottom edge - the source's palette on a real object."""
    ic = gk.Icon("enpara - symbol")
    card = rr(10, 30, 118, 98, 7)
    solid(ic, card, face=[(0, "#ffffff"), (0.6, LIGHT[2]), (1, LIGHT[3])], depth=5, side=LIGHT[4], layer="card")
    chip = rr(20, 42, 44, 60, 3)
    solid(ic, chip, face=[(0, "#ffe08a"), (1, ORANGE)], depth=1.5, side=ORANGE_D, top=False, layer="chip")
    ic.path(geom_d(rr(20, 47, 44, 49, 1)), "#cf8610", opacity=0.5, layer_id="chip-line")
    put_mark(ic, SLUG, (52, 38, 112, 66), face=MAG)
    stripe = rr(10, 84, 118, 94, 3).intersection(card)
    cols = [MAG, ORANGE, GREEN, BLUE]
    for i, c in enumerate(cols):
        seg = box(10 + i * 27, 84, 10 + (i + 1) * 27, 94).intersection(stripe)
        ic.path(geom_d(seg), c, layer_id=f"stripe-{i}")
    return ic


def B():
    """Faithful - a wallet: magenta leather, pale stitching, a white card with the magenta en
    peeking out of the top. The closest style to the source's colours."""
    ic = gk.Icon("enpara - faithful")
    card = rr(24, 12, 104, 60, 4)
    solid(ic, card, face=[(0, "#ffffff"), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer="card")
    put_mark(ic, SLUG, (32, 20, 96, 46), face=MAG)
    body = rr(14, 50, 114, 116, 8)
    solid(ic, body, face=[(0, "#c06cb2"), (0.5, MAG), (1, MAG_D)], depth=6, side=MAG_DD, layer="wallet")
    toplight(ic, body, width=2.0, opacity=0.4, layer="wallet")
    flap = rr(14, 78, 114, 116, 8)
    solid(ic, flap, face=[(0, "#c06cb2"), (0.55, MAG), (1, MAG_DD)], depth=4, side=MAG_DD, layer="flap")
    stitch = rr(20, 84, 108, 108, 6).difference(rr(23, 87, 105, 105, 5))
    ic.path(geom_d(stitch), "#e8c9e2", opacity=0.5, layer_id="stitch")
    return ic


def C():
    """Disc - a coin: orange-gold, a raised rim, the magenta en embossed in the middle."""
    ic = gk.Icon("enpara - disc")
    coin = circ(64, 64, 47)
    solid(ic, coin, face=[(0, "#ffd06a"), (0.5, ORANGE), (1, ORANGE_D)], depth=6, side="#a86a08", layer="coin")
    rim = circ(64, 64, 47).difference(circ(64, 64, 41))
    ic.path(geom_d(rim), "#a86a08", opacity=0.35, layer_id="rim")
    inner = circ(64, 64, 36)
    recess(ic, inner, [(0, "#ffdf95"), (1, ORANGE)], wall=2, layer="face")
    put_mark(ic, SLUG, (38, 50, 90, 78), face=MAG_D)
    return ic


def D():
    """Rimmed - a safe: a steel-blue body, a thick rimmed door, a big round dial and a handle, the
    magenta en on the door."""
    ic = gk.Icon("enpara - rimmed")
    body = rr(12, 10, 116, 118, 6)
    solid(ic, body, face=[(0, "#7d99a6"), (0.3, "#5b7f92"), (1, "#2f4450")], depth=6, side="#22333c", layer="body")
    door = rr(20, 18, 108, 112, 6)
    solid(ic, door, face=[(0, "#d7dee2"), (0.55, "#a6b6bf"), (1, "#7d94a0")], depth=3, side="#4a6674", layer="door")
    put_mark(ic, SLUG, (32, 26, 96, 54), face=MAG_D)
    dial = circ(64, 88, 14)
    solid(ic, dial, face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=4, side="#5e5c64", layer="dial")
    for a in (0, 90, 180, 270):
        pass
    handle = rr(86, 78, 100, 100, 3)
    solid(ic, handle, face=[(0, "#deddda"), (1, "#77767b")], depth=2, side="#3d3846", layer="handle")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
