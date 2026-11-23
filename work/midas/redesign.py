#!/usr/bin/env python3
"""midas - Gnomed redesign (Claude, 2026-11-23, the owner's comparison with Haiku).

Midas: Turkish stocks, US and European shares, funds, gold ("Petrol, altın gibi emtiaların
ETF'lerine yatırım yap"; the fund themes start with "Altın" - gold bars). The logo: a white dot
and two slanted bars on Midas blue. And the name: Midas, whose touch turned things to gold.
  Symbol   A: Midas = gold - a stack of gold bars, the logo stamped in Midas blue on the top bar
  Faithful B: the logo itself - the white dot and bars on their Midas-blue die-cut
  Disc     C: "ABD & Avrupa şirketleri" - a Midas-blue globe on a gold meridian, the logo on it
  Rimmed   D: "tüm yatırımların tek ekranda" - the portfolio: a blue leather briefcase, gold clasps
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from carriers import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
BLUE = ("#8f9af5", "#6b78f0", "#4959ea", "#3443c4", "#24309a")       # Midas blue (source.png)
GOLD = ("#fff3c4", "#f9dc7a", "#eec04a", "#d4a12a", "#a67a12")


def ingot(ic, x0, x1, base, h, name):
    """one gold bar seen from the front and a little above: the sloping front, the lit top"""
    inset, top_h = (x1 - x0) * 0.10, h * 0.30
    front = Polygon([(x0, base), (x1, base), (x1 - inset, base - h + top_h), (x0 + inset, base - h + top_h)])
    top = Polygon([(x0 + inset, base - h + top_h), (x1 - inset, base - h + top_h), (x1 - inset * 2, base - h), (x0 + inset * 2, base - h)])
    solid(ic, front, face=[(0, GOLD[2]), (1, GOLD[3])], depth=4, side=GOLD[4], top=False, layer=f"{name}-front")
    ic.path(geom_d(top), ic.linear([(0, GOLD[0]), (1, GOLD[1])], 0, base - h, 0, base - h + top_h), layer_id=f"{name}-top")
    ic.path(geom_d(front.intersection(box(x0, base - h + top_h, x1, base - h + top_h + 2.2))), "#ffffff", opacity=0.45,
            layer_id=f"{name}-edge")
    return front


def A():
    """Symbol - Midas = gold: three gold bars stacked, the logo stamped in Midas blue on the top
    bar's front (anchors 1, 2, 3)."""
    ic = gk.Icon("midas - symbol")
    ingot(ic, 8, 64, 114, 34, "bar-l")
    ingot(ic, 64, 120, 114, 34, "bar-r")
    ingot(ic, 24, 104, 82, 44, "bar-top")
    put_mark(ic, SLUG, (40, 56, 88, 80), face=BLUE[3])
    return ic


def B():
    """Faithful - the logo itself: the white dot and the two slanted bars on their Midas-blue
    die-cut margin - the app icon's own colours, as a solid object (anchors 1, 2)."""
    ic = gk.Icon("midas - faithful")
    sticker(ic, SLUG, BLUE[2])
    return ic


def C():
    """Disc - "ABD & Avrupa şirketlerine": a Midas-blue globe with light continents (the Americas,
    Europe and Africa) in a gold meridian on its stand, the white logo on the ocean (anchors 1, 4)."""
    ic = gk.Icon("midas - disc")
    cx, cy, R = 64, 56, 44
    solid(ic, rounded(box(42, 108, 86, 116), 3), face=[(0, GOLD[1]), (1, GOLD[3])], depth=3, side=GOLD[4], layer="base")
    solid(ic, box(61, 96, 67, 110), face=[(0, GOLD[2]), (1, GOLD[3])], depth=1, side=GOLD[4], top=False, layer="post")
    ring = LineString([(cx + (R + 7) * math.cos(math.radians(a)), cy + (R + 7) * math.sin(math.radians(a))) for a in range(-40, 141, 4)])
    solid(ic, ring.buffer(3.2, cap_style=1), face=[(0, GOLD[1]), (1, GOLD[3])], depth=2, side=GOLD[4], layer="meridian")
    g = circ(cx, cy, R)
    solid(ic, g, face=[(0, BLUE[1]), (0.55, BLUE[2]), (1, BLUE[3])], depth=3, side=BLUE[4], layer="globe")
    land = unary_union([
        rounded(Polygon([(24, 30), (40, 24), (44, 36), (36, 50), (40, 66), (34, 86), (28, 80), (26, 60), (20, 46)]), 4),
        rounded(Polygon([(86, 24), (102, 28), (100, 40), (92, 44), (104, 54), (100, 76), (90, 86), (86, 66), (84, 50), (80, 40)]), 4),
    ]).intersection(g.buffer(-2))
    ic.path(geom_d(land), ic.linear([(0, "#e6f0ff"), (1, "#b9c6f7")], 0, 12, 0, 100), layer_id="continents")
    ic.path(geom_d(g.difference(affinity.translate(g, 6, 7))), "#ffffff", opacity=0.25, layer_id="globe-light")
    put_mark(ic, SLUG, (44, 43, 84, 69))
    return ic


def D():
    """Rimmed - "tüm yatırımların tek ekranda", the portfolio: a deep-blue leather briefcase, its
    handle, two gold clasps, the white logo on its front (anchors 1, 2, 5)."""
    ic = gk.Icon("midas - rimmed")
    handle = LineString([(48, 42), (48, 28), (80, 28), (80, 42)]).buffer(4.2, join_style=1, cap_style=1)
    solid(ic, handle, face=[(0, BLUE[3]), (1, BLUE[4])], depth=2, side="#18206b", layer="handle")
    case = rounded(box(10, 40, 118, 114), 11)
    solid(ic, case, face=[(0, BLUE[1]), (0.45, BLUE[2]), (1, BLUE[3])], depth=6, side=BLUE[4], layer="case")
    ic.path(geom_d(box(10, 56, 118, 59).intersection(case)), "#000000", opacity=0.22, layer_id="lid-seam")
    for x in (30, 98):
        solid(ic, rounded(box(x - 6, 50, x + 6, 64), 2.5), face=[(0, GOLD[0]), (1, GOLD[3])], depth=2, side=GOLD[4], layer=f"clasp-{x}")
    put_mark(ic, SLUG, (36, 68, 92, 104))
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
