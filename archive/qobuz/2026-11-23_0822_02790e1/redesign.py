#!/usr/bin/env python3
"""qobuz - Gnomed redesign.
Main (Symbol) A: a studio condenser microphone. Faithful B: an album sleeve - white wordmark
on the dark cover, the inner sleeve peeking out. Disc C: a compact disc. Rimmed D: a mixing
console with faders."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
BLUE = RAMP["Blue"]
RED = RAMP["Red"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a studio condenser microphone: silver mesh grille, steel body with the white
    wordmark, a dark shock-mount yoke and foot."""
    ic = gk.Icon("qobuz - symbol")
    grille = rounded(box(40, 16, 88, 62), 21)
    solid(ic, grille, face=[(0, "#ffffff"), (0.55, LIGHT[3]), (1, LIGHT[4])], depth=3, side="#77767b", layer="grille")
    for y in (28, 38, 48):
        mesh = box(42, y, 86, y + 2.4)
        ic.path(geom_d(mesh.intersection(grille)), "#5e5c64", opacity=0.6, layer_id=f"mesh-{y}")
    body = rr(40, 56, 88, 108, 7)
    solid(ic, body, face=[(0, "#77767b"), (0.5, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="body")
    collar = rr(37, 54, 91, 64, 4)
    solid(ic, collar, face=[(0, "#ffffff"), (1, LIGHT[3])], depth=2, side="#77767b", layer="collar")
    yoke = rr(26, 60, 33, 112, 3).union(rr(95, 60, 102, 112, 3))
    solid(ic, yoke, face=[(0, LIGHT[3]), (1, "#5e5c64")], depth=3, side="#3d3846", layer="yoke")
    foot = rr(30, 110, 98, 118, 4)
    solid(ic, foot, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=2, side="#241f31", layer="foot")
    put_mark(ic, SLUG, (42, 72, 86, 104), face="#ffffff")
    return ic


def B():
    """Faithful - an album sleeve: dark cardboard cover with the white wordmark, the pale inner
    sleeve peeking out of the top. Closest to the logo's white-on-black."""
    ic = gk.Icon("qobuz - faithful")
    inner = rr(18, 14, 102, 44, 2)
    solid(ic, inner, face=[(0, "#ffffff"), (1, LIGHT[3])], depth=1.5, side=LIGHT[4], top=False, layer="inner")
    cover = rr(14, 26, 104, 112, 3)
    solid(ic, cover, face=[(0, "#3d3846"), (0.6, DARK[3]), (1, "#1b1a1f")], depth=5, side="#1b1a1f", layer="cover")
    spine = rr(14, 26, 24, 112, 3)
    solid(ic, spine, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=2, side="#1b1a1f", top=False, layer="spine")
    line = box(14, 26, 104, 28).intersection(cover)
    ic.path(geom_d(line), "#ffffff", opacity=0.18, layer_id="cover-edge")
    put_mark(ic, SLUG, (26, 54, 100, 84), face="#ffffff")
    return ic


def C():
    """Disc - a compact disc: metallic silver, a rainbow sheen, the dark wordmark printed across
    it and a real spindle hole."""
    ic = gk.Icon("qobuz - disc")
    full = circ(64, 64, 46)
    disc = full.difference(circ(64, 64, 6.5))
    solid(ic, disc, face=[(0, "#ffffff"), (0.5, LIGHT[2]), (1, LIGHT[4])], depth=5, side=LIGHT[4], layer="disc")
    sheen = box(18, 26, 110, 58).intersection(disc)
    ic.path(geom_d(sheen), ic.linear([(0, BLUE[0]), (0.4, RED[0]), (0.7, YELLOW[0]), (1, BLUE[0])],
                                    18, 64, 110, 64), opacity=0.45, layer_id="sheen")
    hub = circ(64, 64, 18).difference(circ(64, 64, 8))
    solid(ic, hub, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=1, side=LIGHT[4], top=False, layer="hub")
    put_mark(ic, SLUG, (34, 34, 94, 58), face="#241f31")
    return ic


def D():
    """Rimmed - a mixing console: dark board, silver knobs on the top edge, faders below, the
    white wordmark on the front panel."""
    ic = gk.Icon("qobuz - rimmed")
    board = rr(6, 46, 122, 112, 6)
    solid(ic, board, face=[(0, "#5e5c64"), (0.15, "#3d3846"), (1, "#241f31")], depth=6, side="#1b1a1f", layer="board")
    top = rr(6, 46, 122, 66, 5)
    solid(ic, top, face=[(0, "#77767b"), (1, "#3d3846")], depth=2, side="#241f31", top=False, layer="top")
    for i, x in enumerate((22, 40, 58, 76, 94, 110)):
        solid(ic, circ(x, 56, 5), face=[(0, "#ffffff"), (1, LIGHT[4])], depth=2, side="#77767b", top=False, layer=f"knob-{i}")
    for i, x in enumerate((26, 54, 82, 108)):
        slot = rr(x - 2.2, 90, x + 2.2, 108, 2)
        ic.path(geom_d(slot), "#1b1a1f", layer_id=f"slot-{i}")
        cap = rr(x - 6, 94, x + 6, 100, 2)
        solid(ic, cap, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=2, side="#5e5c64", layer=f"cap-{i}")
    put_mark(ic, SLUG, (18, 71, 110, 87), face="#ffffff")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
