#!/usr/bin/env python3
"""enpara - Gnomed redesign.
Main (Symbol) A: a bank card with the magenta en and a four-colour edge stripe. Faithful B: the
measured en as one solid object standing on the source's four-colour stripe. Disc C: a coin with the
en embossed. Rimmed D: a safe door with hinges, a dial and a handle, the en on a small plate."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity

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
    card = rr(10, 36, 118, 104, 7)
    solid(ic, card, face=[(0, "#ffffff"), (0.6, LIGHT[2]), (1, LIGHT[3])], depth=5, side=LIGHT[4], layer="card")
    chip = rr(20, 48, 44, 66, 3)
    solid(ic, chip, face=[(0, "#ffe08a"), (1, ORANGE)], depth=1.5, side=ORANGE_D, top=False, layer="chip")
    ic.path(geom_d(rr(20, 53, 44, 55, 1)), "#cf8610", opacity=0.5, layer_id="chip-line")
    put_mark(ic, SLUG, (52, 44, 112, 72), face=MAG)
    stripe = rr(10, 90, 118, 100, 3).intersection(card)
    cols = [MAG, ORANGE, GREEN, BLUE]
    for i, c in enumerate(cols):
        seg = box(10 + i * 27, 90, 10 + (i + 1) * 27, 100).intersection(stripe)
        ic.path(geom_d(seg), c, layer_id=f"stripe-{i}")
    return ic


def B():
    """Faithful - the logo as one solid object (L1): the measured "en", extruded in the brand
    magenta, standing on the source's four-colour stripe. No plate, nothing clipped."""
    ic = gk.Icon("enpara - faithful")
    shadow = ellipse(64, 94, 44, 5)
    ic.path(geom_d(shadow), "#000000", opacity=0.14, layer_id="shadow")
    stripe = rr(14, 94, 114, 116, 5)
    solid(ic, stripe, face=[(0, "#ffffff"), (1, LIGHT[3])], depth=4, side=LIGHT[4], layer="stripe")
    cols = [MAG, ORANGE, GREEN, BLUE]
    for i, c in enumerate(cols):
        seg = box(14 + i * 25, 94, 14 + (i + 1) * 25, 116).intersection(stripe)
        ic.path(geom_d(seg), c, layer_id=f"stripe-{i}")
    put_mark(ic, SLUG, (20, 34, 108, 88), depth=6, anchor="bottom", face=MAG, side=MAG_DD)
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
    """Rimmed - a safe door: a heavy steel door with two dark hinges, a big round dial with tick
    marks and a shaded face, a steel handle at the edge - the en on a small white plate."""
    ic = gk.Icon("enpara - rimmed")
    door = rr(10, 10, 118, 116, 8)
    solid(ic, door, face="#c3cfd6", depth=4, side="#8fa8b4", layer="door", top=False)
    for k, y in enumerate((30, 74)):
        hinge = rr(10, y, 26, y + 22, 4)
        solid(ic, hinge, face="#3f5866", depth=3, side="#2b3d47", layer=f"hinge-{k}", top=False)
    plate = rr(30, 22, 98, 52, 3)
    ic.path(geom_d(plate), "#ffffff", layer_id="plate")
    put_mark(ic, SLUG, (35, 26, 93, 48), face=MAG)
    dial = circ(60, 84, 24)
    ic.path(geom_d(dial), ic.radial([(0, "#ffffff"), (1, "#b5b3b0")], 60, 84, 24), layer_id="dial")
    for k in range(4):
        a = 45 + k * 90
        tick = affinity.rotate(box(-3.2, -24, 3.2, -16), a, origin=(0, 0))
        tick = affinity.translate(tick, 60, 84)
        ic.path(geom_d(tick), "#5e5c64", layer_id=f"tick-{k}")
    handle = rr(104, 62, 118, 104, 7)
    solid(ic, handle, face="#8fa8b4", depth=3, side="#5b7482", layer="handle", top=False)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
