#!/usr/bin/env python3
"""duolingo - Gnomed redesign, round 2 (Claude, 2026-11-23).

The logo IS Duo's face (REDESIGN 5 "A mascot logo is still the logo"): every style carries the
MEASURED face (put_mark; geometry.json keeps the light-green head: mark_keep r0, mark_round 10),
each on a different thing from the app's own screens (design.md anchors):
  Symbol   A: the daily streak - the orange streak flame with Duo in front of it (shot-6)
  Faithful B: Duo's head itself as a solid object - the logo, with thickness
  Disc     C: the cafe lessons - a cup of coffee from above on its saucer, Duo in the foam (shot-4, 5)
  Rimmed   D: a lesson - the white speech bubble with the blue sound button, Duo speaking it (shot-2, 4, 5)
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString, Point

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
GREEN = ("#89e219", "#7ad61a", "#58cc02", "#46a302", "#3a8702")       # Duolingo greens (source.png)
FLAME = ("#ffc800", "#ffb100", "#ff9600", "#e07c00", "#b85f00")       # streak orange (shot-6)
BLUE = ("#5fd0ff", "#1cb0f6", "#1899d6", "#1482b8")                   # sound button (shot-2, 4, 5)


def mark_with_side(ic, box_, depth, side=GREEN[3], anchor="bottom"):
    """Duo's measured face as a solid thing (L1): one side under its outline, the face on top."""
    return put_mark(ic, SLUG, box_, anchor=anchor, body=depth, side=side)


def flame_shape(cx, base, w, h, lean=6):
    """Duolingo's streak flame: a round belly, a tip leaning right and a small tongue on the left."""
    r = w / 2
    belly = Point(cx, base - r).buffer(r, quad_segs=48)
    tip = (cx + lean, base - h)
    body = unary_union([belly, Polygon([(cx - r * 0.92, base - r * 1.1), tip, (cx + r * 0.96, base - r * 1.05)])])
    tongue = unary_union([Point(cx - r * 0.55, base - r * 1.25).buffer(r * 0.32, quad_segs=24),
                          Polygon([(cx - r * 0.86, base - r * 1.2), (cx - r * 0.78, base - h * 0.72),
                                   (cx - r * 0.22, base - r * 1.3)])])
    return rounded(unary_union([body, tongue]), 3)


def A():
    """Symbol - the daily streak: the big orange streak flame with its yellow core, Duo's face in
    front of its lower right, as on the streak screen (anchors 1, 3)."""
    ic = gk.Icon("duolingo - symbol")
    fl = flame_shape(52, 110, 76, 100)
    solid(ic, fl, face=[(0, FLAME[0]), (0.45, FLAME[2]), (1, FLAME[3])], depth=4, side=FLAME[4], layer="flame")
    core = flame_shape(50, 104, 38, 52, lean=4)
    ic.path(geom_d(core), ic.linear([(0, "#fff4b0"), (1, FLAME[0])], 0, 52, 0, 104), layer_id="flame-core")
    mark_with_side(ic, (50, 58, 120, 114), depth=4)
    return ic


def B():
    """Faithful - Duo's head itself, the logo as a solid object: the light-green head with its
    tufts, the white eyes and the orange beak, the Duolingo green as its thickness (anchors 1, 2)."""
    ic = gk.Icon("duolingo - faithful")
    mark_with_side(ic, (10, 22, 118, 110), depth=8, side=GREEN[2])
    return ic


def C():
    """Disc - the cafe lessons ("¡Necesito más café!", "Je voudrais un café"): a cup of coffee
    seen from above on its round saucer, Duo's face drawn in the foam (anchors 1, 5)."""
    ic = gk.Icon("duolingo - disc")
    saucer = circ(64, 64, 54)
    solid(ic, saucer, face=[(0, "#ffffff"), (1, "#deddda")], depth=4, side="#9a9996", layer="saucer")
    ic.path(geom_d(circ(64, 64, 44).difference(circ(64, 64, 41))), "#000000", opacity=0.07, layer_id="saucer-ring")
    handle = rounded(box(92, 56, 116, 72), 7)
    solid(ic, handle, face=[(0, "#ffffff"), (1, "#deddda")], depth=3, side="#9a9996", layer="cup-handle")
    cup = circ(62, 64, 38)
    solid(ic, cup, face=[(0, "#ffffff"), (1, "#e8e6e3")], depth=4, side="#9a9996", layer="cup")
    coffee = circ(62, 64, 31)
    recess(ic, coffee, [(0, "#c8a27a"), (1, "#a77c52")], wall=3, layer="coffee")
    foam = circ(62, 65, 26)
    ic.path(geom_d(foam), ic.linear([(0, "#fff7ea"), (1, "#f1dfc6")], 0, 39, 0, 91), layer_id="foam")
    put_mark(ic, SLUG, (39, 48, 85, 82))
    return ic


def speaker_glyph(cx, cy, s):
    """The sound button's white speaker: the body, its cone and two sound waves."""
    body = box(cx - s * 0.62, cy - s * 0.24, cx - s * 0.30, cy + s * 0.24)
    cone = Polygon([(cx - s * 0.32, cy - s * 0.24), (cx + s * 0.02, cy - s * 0.52),
                    (cx + s * 0.02, cy + s * 0.52), (cx - s * 0.32, cy + s * 0.24)])
    waves = []
    for r in (s * 0.32, s * 0.58):
        arc = LineString([(cx + 0.02 * s + r * math.cos(a), cy + r * math.sin(a))
                          for a in [math.radians(t) for t in range(-50, 51, 5)]])
        waves.append(arc.buffer(s * 0.075, cap_style=1))
    return rounded(unary_union([body, cone]), s * 0.06).union(unary_union(waves))


def D():
    """Rimmed - a lesson: the white speech bubble with the blue sound button and the sentence's
    grey lines, Duo's face speaking it from below (anchors 1, 4)."""
    ic = gk.Icon("duolingo - rimmed")
    bub = rounded(box(36, 12, 118, 74), 16)
    tail = Polygon([(50, 70), (40, 88), (66, 70)])
    bubble = rounded(unary_union([bub, tail]), 2)
    solid(ic, bubble, face=[(0, "#ffffff"), (1, "#f2f2f2")], depth=3, side="#c0bfbc", layer="bubble")
    ic.path(geom_d(bubble.difference(bubble.buffer(-2.2))), "#e5e5e5", layer_id="bubble-edge")
    btn = rounded(box(46, 24, 72, 50), 7)
    solid(ic, btn, face=[(0, BLUE[0]), (0.5, BLUE[1]), (1, BLUE[2])], depth=3, side=BLUE[3], layer="sound-button")
    ic.path(geom_d(speaker_glyph(60, 37, 15)), "#ffffff", layer_id="sound-glyph")
    for i, (x1, y) in enumerate(((108, 30), (100, 44), (90, 58))):
        x0 = 80 if i < 2 else 46
        ic.path(geom_d(LineString([(x0, y), (x1, y)]).buffer(2.6, cap_style=1)), "#afafaf", layer_id=f"text-{i}")
    mark_with_side(ic, (8, 66, 70, 116), depth=4)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
