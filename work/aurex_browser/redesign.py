#!/usr/bin/env python3
"""aurex_browser - Gnomed redesign.

Approved (design.md): C - a blue browser window (the app's function as an object) with
the white A standing on its page and the cyan glass bead (owner, round 3 of concepts;
the earlier 'A on a blue disc' build was the logo on a disc and is replaced).
Measured: A = parts r0+r1 (#e6f1fd / #b1cff5), its side r2 #1e57c4, bead r3 #59e6dd,
blue field #53a2fa -> #305fde.

Build:  python3 tools/make_icon.py aurex_browser"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
P = parts(SLUG)


def design():
    ic = gk.Icon("Aurex Browser - Gnomed (browser window + A)")
    # the window: blue enamel body, 6 px side, standing on the baseline (112 + 6 = 118)
    win = rounded(box(8, 14, 120, 112), 11)
    solid(ic, win, face=[(0, "#62a0ea"), (0.5, "#4281ec"), (1, "#305fde")], depth=6, side="#1e57c4", layer="window")
    # title bar dots (white, slightly raised)
    for i, x in enumerate((19, 28, 37)):
        solid(ic, circ(x, 24, 2.8), face="#ffffff", depth=0.8, side="#99c1f1", top=False, layer=f"dot{i}")
    # the page: a lighter blue recess
    page = rounded(box(15, 33, 113, 106), 6)
    recess(ic, page, [(0, "#99c1f1"), (1, "#62a0ea")], wall=3, layer="page")
    # the A (measured) standing on the page, the cyan bead in its opening
    # the A is solid: the small counter above the bead is filled (owner: "orijinalinde boşluk yok")
    a_, bead = fit([unary_union([P["r0"], P["r1"], P["holes"]]), P["r3"]], (34, 38, 94, 101), anchor="bottom")
    bcy = (bead.bounds[1] + bead.bounds[3]) / 2
    gap = a_.convex_hull.difference(a_).intersection(box(0, 0, 128, bcy))   # open space above the bead
    a_ = unary_union([a_, gap]).buffer(0.3).buffer(-0.3)
    solid(ic, a_, face=[(0, "#ffffff"), (0.6, "#e6f1fd"), (1, "#b1cff5")], depth=4, side="#1e57c4", layer="A")
    solid(ic, bead, face=[(0, "#c4fff8"), (0.5, "#59e6dd"), (1, "#2fb9c9")], depth=1.5, side="#2a9fb0", top=False, layer="bead")
    bx, by, bx1, _ = bead.bounds
    r = (bx1 - bx) / 2
    ic.path(geom_d(circ(bx + r * 0.7, by + r * 0.7, r * 0.45).intersection(bead)),
            ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], bx + r * 0.7, by + r * 0.7, r * 0.45), layer_id="bead-glint")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
