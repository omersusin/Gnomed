#!/usr/bin/env python3
"""mornye - Gnomed redesign (Claude, 2026-11-23, the owner's comparison with Haiku).

Mornye: a music player for your own library - FLAC, bit-perfect USB and AAudio output for DAPs,
an equalizer ("Bass boost"), lyrics. The logo: a mint down-arrow between two bars on deep teal.
The screens: album art made of soft blobs (the "Paper Moons" flower), a wavy seek line,
"FLAC · 24-bit · 48 kHz", the equalizer's bass-boost curve.
  Symbol   A: "for DAPs" - a teal digital audio player, the flower album art on its screen, the
              mint logo on its body, a volume wheel
  Faithful B: the logo itself - the mint arrow and bars on their teal die-cut
  Disc     C: bit-perfect volume - an aluminium knob with its mint scale, the logo on the teal cap
  Rimmed   D: "Bass boost" - a hardware equalizer, four teal faders on the boost curve, the logo
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from carriers import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
TEAL = ("#3f7f80", "#2c6668", "#1e4d4f", "#173d3f", "#0f2a2c")       # the tile (source.png)
MINT = ("#e6fbfb", "#bbebec", "#8fd8da", "#62bfc2")                   # the logo (source.png)
PINK = ("#ffd6e0", "#f7a8bf", "#c2185b", "#8e1046")                   # the "Paper Moons" art (shot)
SUN = "#f9b208"


def A():
    """Symbol - "for DAPs": a teal digital audio player - the "Paper Moons" flower art on its
    screen with the wavy seek line, the mint logo on the body, a volume wheel on its side
    (anchors 1, 2, 3, 4)."""
    ic = gk.Icon("mornye - symbol")
    wheel = rounded(box(94, 30, 106, 54), 4)
    solid(ic, wheel, face=[(0, "#ffffff"), (0.5, "#c0bfbc"), (1, "#77767b")], depth=2, side="#5e5c64", layer="wheel")
    for y in range(33, 52, 4):
        ic.path(geom_d(box(100, y, 106, y + 1.4)), "#5e5c64", opacity=0.5, layer_id=f"knurl-{y}")
    body = rounded(box(26, 8, 100, 118), 13)
    solid(ic, body, face=[(0, TEAL[0]), (0.5, TEAL[2]), (1, TEAL[3])], depth=5, side=TEAL[4], layer="body")
    scr = rounded(box(33, 15, 93, 63), 6)
    recess(ic, scr, [(0, PINK[0]), (1, PINK[1])], wall=2, layer="screen")
    art = scr.buffer(-1)
    ic.path(geom_d(circ(48, 44, 11).intersection(art)), SUN, layer_id="art-sun")
    petals = unary_union([circ(70 + 11 * math.cos(math.radians(a)), 36 + 11 * math.sin(math.radians(a)), 8) for a in range(0, 360, 60)] + [circ(70, 36, 9)])
    ic.path(geom_d(petals.intersection(art)), ic.linear([(0, "#e0306f"), (1, PINK[3])], 0, 20, 0, 52), layer_id="art-flower")
    wave = LineString([(38 + t, 57 + 2.2 * math.sin(t / 3.2)) for t in range(0, 34)] + [(72, 57), (88, 57)]).buffer(1.6, cap_style=1)
    ic.path(geom_d(wave.intersection(art)), "#ffffff", layer_id="seek")
    put_mark(ic, SLUG, (46, 70, 80, 110))
    return ic


def B():
    """Faithful - the logo itself: the mint down-arrow and its two bars on their teal die-cut - the
    app icon's own colours as a solid object (anchors 1, 2)."""
    ic = gk.Icon("mornye - faithful")
    sticker(ic, SLUG, TEAL[2])
    return ic


def C():
    """Disc - bit-perfect volume: a brushed aluminium knob with a knurled rim on its mint scale,
    the mint logo on the teal cap (anchors 1, 2, 3)."""
    ic = gk.Icon("mornye - disc")
    cx, cy = 64, 62
    scale = unary_union([LineString([(cx + 50 * math.cos(math.radians(a)), cy + 50 * math.sin(math.radians(a))),
                                     (cx + 56 * math.cos(math.radians(a)), cy + 56 * math.sin(math.radians(a)))]).buffer(1.8, cap_style=1)
                         for a in range(135, 406, 27)])
    ic.path(geom_d(scale), MINT[3], layer_id="scale")
    solid(ic, circ(cx, cy, 45), face=[(0, "#ffffff"), (0.5, "#c0bfbc"), (1, "#77767b")], depth=6, side="#5e5c64", layer="knob")
    knurl = unary_union([LineString([(cx + 41 * math.cos(math.radians(a)), cy + 41 * math.sin(math.radians(a))),
                                     (cx + 45 * math.cos(math.radians(a)), cy + 45 * math.sin(math.radians(a)))]).buffer(0.9)
                         for a in range(0, 360, 10)])
    ic.path(geom_d(knurl), "#5e5c64", opacity=0.45, layer_id="knurl")
    solid(ic, circ(cx, cy, 34), face=[(0, TEAL[0]), (1, TEAL[3])], depth=2, side=TEAL[4], layer="cap")
    pointer = LineString([(cx + 30 * math.cos(math.radians(-50)), cy + 30 * math.sin(math.radians(-50))),
                          (cx + 40 * math.cos(math.radians(-50)), cy + 40 * math.sin(math.radians(-50)))]).buffer(2.4, cap_style=1)
    ic.path(geom_d(pointer), MINT[1], layer_id="pointer")
    put_mark(ic, SLUG, (cx - 18, cy - 24, cx + 18, cy + 24))
    return ic


def D():
    """Rimmed - "Bass boost": a hardware equalizer - a light panel, four teal faders standing on the
    bass-boost curve (high on the left), the mint logo on its teal end plate (anchors 1, 2, 5)."""
    ic = gk.Icon("mornye - rimmed")
    panel = rounded(box(8, 24, 120, 108), 10)
    solid(ic, panel, face=[(0, "#ffffff"), (1, "#deddda")], depth=6, side="#9a9996", layer="panel")
    plate = rounded(box(14, 30, 52, 102), 7)
    solid(ic, plate, face=[(0, TEAL[1]), (1, TEAL[3])], depth=2, side=TEAL[4], layer="plate")
    put_mark(ic, SLUG, (19, 42, 47, 90))
    for k, (x, y) in enumerate(((64, 44), (80, 52), (96, 64), (110, 66))):
        ic.path(geom_d(LineString([(x, 36), (x, 96)]).buffer(2.2, cap_style=1)), "#9a9996", layer_id=f"track-{k}")
        solid(ic, rounded(box(x - 6, y - 5, x + 6, y + 5), 2.5), face=[(0, TEAL[0]), (1, TEAL[3])], depth=2, side=TEAL[4], layer=f"fader-{k}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
