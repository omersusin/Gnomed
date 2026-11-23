#!/usr/bin/env python3
"""binance_tr - Gnomed redesign (Claude, 2026-11-23, for the owner's comparison with Sonnet).

Binance TR: the yellow Binance diamond with "TR" on black; the store screenshots are black and
yellow, full of floating 3D coins (the yellow coin with the logo, Bitcoin, Ethereum, the red
Turkish-lira coin), a candlestick chart ("Kolay Al/Sat"), the wallet ("Cüzdan 1,234.78 TRY").
Every style carries the MEASURED logo (put_mark), each on a different thing:
  Symbol   A: the wallet ("Cüzdan") - black wallet, the yellow coin with the logo and the red lira
              coin sticking out
  Faithful B: the logo itself as a solid object - the diamond and TR in Binance yellow
  Disc     C: the yellow coin of the screenshots - thick gold edge, the logo embossed
  Rimmed   D: "Kolay Al/Sat" - a trading screen on its stand, the logo and the green/red candles
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
GOLD = ("#ffe27a", "#fcd535", "#f0b90b", "#d9a200", "#a87b00")       # Binance yellow (source.png)
BLACK = ("#474d57", "#2b3139", "#1e2329", "#181a20", "#0b0e11")       # Binance black (screenshots)
RED = ("#ff8a80", "#f6465d", "#e0323f", "#b3202c")                    # the lira coin, red candles
GREEN = ("#5ee0a8", "#2ebd85", "#0ecb81", "#089e61")                  # green candles, success


def lira(cx, cy, s):
    """The Turkish-lira sign: a stem with a foot curving right and two slanted bars."""
    stem = LineString([(cx - s * 0.18, cy - s * 0.55), (cx - s * 0.18, cy + s * 0.45),
                       (cx + s * 0.10, cy + s * 0.42), (cx + s * 0.38, cy + s * 0.10)]).buffer(s * 0.11, cap_style=1, join_style=1)
    bars = unary_union([LineString([(cx - s * 0.45, cy - s * 0.02 + k * s * 0.24), (cx + s * 0.18, cy - s * 0.24 + k * s * 0.24)])
                        .buffer(s * 0.09, cap_style=1) for k in (0, 1)])
    return stem.union(bars)


def A():
    """Symbol - the wallet ("Cüzdan"): a black wallet; the yellow coin with the logo and the red
    Turkish-lira coin stick out of it (anchors 1, 2, 3, 5)."""
    ic = gk.Icon("binance_tr - symbol")
    red = circ(90, 36, 19)
    solid(ic, red, face=[(0, RED[0]), (0.5, RED[1]), (1, RED[3])], depth=4, side="#7a1520", layer="coin-lira")
    ic.path(geom_d(lira(90, 36, 17)), "#ffffff", layer_id="lira-sign")
    gold = circ(50, 36, 29)
    solid(ic, gold, face=[(0, GOLD[0]), (0.5, GOLD[2]), (1, GOLD[3])], depth=5, side=GOLD[4], layer="coin-bnb")
    ic.path(geom_d(circ(50, 36, 29).difference(circ(50, 36, 25))), GOLD[3], opacity=0.55, layer_id="coin-bnb-rim")
    put_mark(ic, SLUG, (36, 14, 64, 51), face=GOLD[4])
    wallet = rounded(box(10, 56, 118, 116), 12)
    solid(ic, wallet, face=[(0, BLACK[0]), (0.5, BLACK[1]), (1, BLACK[3])], depth=5, side=BLACK[4], layer="wallet")
    ic.path(geom_d(LineString([(16, 62), (112, 62)]).buffer(0.8)), "#ffffff", opacity=0.10, layer_id="wallet-stitch")
    flap = rounded(box(70, 72, 124, 104), 10).intersection(box(0, 0, 118, 128))
    solid(ic, rounded(flap, 1), face=[(0, BLACK[0]), (1, BLACK[2])], depth=2, side=BLACK[4], layer="flap")
    solid(ic, circ(84, 88, 5.5), face=[(0, GOLD[0]), (1, GOLD[3])], depth=1.5, side=GOLD[4], layer="snap")
    return ic


def B():
    """Faithful - the logo itself as a solid object: the Binance diamond (its four corners and the
    centre) and TR, Binance yellow with a deep-gold thickness (anchors 1, 2)."""
    ic = gk.Icon("binance_tr - faithful")
    put_mark(ic, SLUG, (24, 10, 104, 112), anchor="bottom", body=7, side=GOLD[4])
    return ic


def C():
    """Disc - the coin of the screenshots: a thick yellow coin with a milled gold edge, the logo
    embossed in deeper gold on its face (anchors 1, 2, 3)."""
    ic = gk.Icon("binance_tr - disc")
    cx, cy, R = 64, 60, 52
    solid(ic, circ(cx, cy, R), face=[(0, GOLD[1]), (0.5, GOLD[2]), (1, GOLD[3])], depth=8, side=GOLD[4], layer="coin")
    teeth = unary_union([LineString([(cx + (R - 1) * math.cos(a), cy + (R - 1) * math.sin(a)),
                                     (cx + (R - 5) * math.cos(a), cy + (R - 5) * math.sin(a))]).buffer(1.1)
                         for a in [math.radians(t) for t in range(0, 360, 9)]])
    ic.path(geom_d(teeth), GOLD[3], opacity=0.7, layer_id="milling")
    face = circ(cx, cy, R - 8)
    recess(ic, face, [(0, GOLD[0]), (0.6, GOLD[1]), (1, GOLD[2])], wall=3, layer="face")
    put_mark(ic, SLUG, (cx - 26, cy - 32, cx + 26, cy + 33), face=GOLD[4])
    return ic


def D():
    """Rimmed - "Kolay Al/Sat": a trading screen on its stand - the dark Binance screen with the
    logo and bold green and red candles climbing (anchors 1, 2, 4)."""
    ic = gk.Icon("binance_tr - rimmed")
    stand = unary_union([Polygon([(56, 92), (72, 92), (76, 108), (52, 108)]), rounded(box(38, 106, 90, 114), 3)])
    solid(ic, stand, face=[(0, "#deddda"), (1, "#9a9996")], depth=3, side="#77767b", layer="stand")
    body = rounded(box(8, 16, 120, 96), 8)
    solid(ic, body, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=4, side="#241f31", layer="monitor")
    screen = rounded(box(13, 21, 115, 91), 4)
    recess(ic, screen, [(0, BLACK[2]), (1, BLACK[4])], wall=2, layer="screen")
    put_mark(ic, SLUG, (20, 30, 50, 82))
    candles = ((62, 62, 76, GREEN), (74, 54, 70, RED), (86, 46, 64, GREEN), (98, 34, 54, GREEN))
    for k, (x, y0, y1, col) in enumerate(candles):
        ic.path(geom_d(LineString([(x, y0 - 5), (x, y1 + 5)]).buffer(1.2)), col[2], layer_id=f"wick-{k}")
        ic.path(geom_d(rounded(box(x - 4.5, y0, x + 4.5, y1), 1.5)), col[1], layer_id=f"candle-{k}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
