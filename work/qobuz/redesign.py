#!/usr/bin/env python3
"""qobuz - Gnomed redesign.
Main (Symbol) A: a big broadcast studio microphone. Faithful B: an album sleeve with its open mouth
and the inner sleeve peeking out. Disc C: a compact disc. Rimmed D: a mixing console with faders."""
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
    """Symbol - a big broadcast studio microphone: a wide silver grille in a ring shock mount,
    a broad steel body with the white wordmark, a thin stand and a round foot."""
    ic = gk.Icon("qobuz - symbol")
    stand = rr(60, 102, 68, 117, 3)
    solid(ic, stand, face=[(0, "#9a9996"), (1, "#5e5c64")], depth=2, side="#3d3846", layer="stand")
    foot = ellipse(64, 117, 26, 5)
    solid(ic, foot, face=[(0, "#77767b"), (1, "#3d3846")], depth=2, side="#241f31", layer="foot")
    body = rr(30, 72, 98, 112, 9)
    solid(ic, body, face=[(0, "#77767b"), (0.5, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="body")
    put_mark(ic, SLUG, (33, 82, 95, 106), face="#ffffff")
    mount = rr(56, 54, 72, 70, 3)
    solid(ic, mount, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=3, side="#241f31", layer="mount")
    ring = circ(64, 42, 34).difference(circ(64, 42, 28))
    solid(ic, ring, face=[(0, "#f6f5f4"), (0.5, "#c0bfbc"), (1, "#8a8986")], depth=3, side="#5e5c64", layer="ring")
    grille = circ(64, 42, 28)
    solid(ic, grille, face=[(0, "#ffffff"), (0.6, LIGHT[3]), (1, LIGHT[4])], depth=2, side="#77767b", layer="grille")
    for y in (26, 36, 46, 56):
        mesh = box(34, y, 94, y + 2.6).intersection(grille)
        ic.path(geom_d(mesh), "#5e5c64", opacity=0.55, layer_id=f"mesh-{y}")
    return ic


def B():
    """Faithful - an album sleeve with its white paper inner sleeve pulled half out of the top: the
    sleeve has a round die-cut window, the dark cardboard cover sits lower with the white wordmark
    and the sleeve's fold shadow falls on it. No record: a vinyl is Deezer's object (same_object)."""
    ic = gk.Icon("qobuz - faithful")
    cover = rr(14, 34, 114, 118, 3)
    solid(ic, cover, face=[(0, "#3d3846"), (0.6, DARK[3]), (1, "#1b1a1f")], depth=5, side="#141317", layer="cover")
    inner = rr(20, 8, 108, 74, 2).difference(circ(64, 46, 13))
    solid(ic, inner, face="#ffffff", depth=1, side="#e6e5e2", layer="inner-sleeve")
    ic.path(geom_d(circ(64, 46, 13).difference(circ(64, 46, 11))), "#b5b3b0", opacity=0.55, layer_id="window-rim")
    ic.path(geom_d(rr(18, 74, 110, 79, 2)), "#000000", opacity=0.26, layer_id="fold-shadow")
    put_mark(ic, SLUG, (22, 86, 106, 114), face="#ffffff")
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
