#!/usr/bin/env python3
"""scene - Gnomed redesign (Claude, 2026-11-23, batch).

Scene (HoshinoScene) tunes a phone's performance: CPU/GPU frequency, temperature control, FPS
monitor, for Snapdragon and Dimensity chips (store.json). The logo: the green Android head with
the yellow gear above it in a dark-blue circle, on blue. Every style carries the MEASURED logo
(put_mark: head + gear), each on a different thing:
  Symbol   A: the phone's processor - an SoC chip with gold pins, the logo on its blue lid
  Faithful B: the logo itself as an object - the Android head and the gear in its dark-blue circle
  Disc     C: temperature control - a round cooling fan, the logo on its hub
  Rimmed   D: the performance gauge - a dial from green to red, the needle up high, the logo on it
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
BLUE = ("#8ab8ff", "#5ba2fc", "#5191ef", "#4780e1", "#3565b8")        # the tile (source.png)
NAVY = "#3d6fc9"                                                      # the gear's circle (source.png)
GREEN = ("#7cf0b2", "#32de84", "#26b86b", "#1d9156")                  # the Android head (source.png)
GOLD = ("#fff1b8", "#f9d97a", "#e5a50a", "#b8860b")


def A():
    """Symbol - the processor: an SoC chip with gold pins on four sides and a blue heat-spreader
    lid carrying the logo (anchors 1, 2, 3, 4)."""
    ic = gk.Icon("scene - symbol")
    pins = []
    for k in range(6):
        t = 30 + k * 13.6
        pins += [box(t - 3, 10, t + 3, 24), box(t - 3, 104, t + 3, 118), box(10, t - 3, 24, t + 3), box(104, t - 3, 118, t + 3)]
    solid(ic, unary_union(pins), face=[(0, GOLD[1]), (1, GOLD[2])], depth=1.5, side=GOLD[3], layer="pins")
    chip = rounded(box(18, 18, 110, 110), 8)
    solid(ic, chip, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="chip")
    lid = rounded(box(28, 28, 100, 100), 6)
    solid(ic, lid, face=[(0, BLUE[1]), (0.5, BLUE[2]), (1, BLUE[3])], depth=2, side=BLUE[4], layer="lid")
    put_mark(ic, SLUG, (38, 36, 90, 92))
    return ic


def B():
    """Faithful - the logo itself as an object: the green Android head with its antennas and the
    yellow gear above it in the dark-blue circle, with thickness (anchors 1, 2, 3)."""
    ic = gk.Icon("scene - faithful")
    from obj import mark_parts, fit
    box_ = (12, 10, 116, 110)
    placed = fit([g for _, g, _ in mark_parts(SLUG)], box_, anchor="bottom")
    gear = [g for (n, _, _), g in zip(mark_parts(SLUG), placed) if n == "r1"][0]
    (gx0, gy0, gx1, gy1) = gear.bounds
    ring = circ((gx0 + gx1) / 2, (gy0 + gy1) / 2, (gx1 - gx0) * 0.86)
    solid(ic, ring, face=[(0, BLUE[2]), (1, NAVY)], depth=4, side=BLUE[4], layer="gear-circle")
    put_mark(ic, SLUG, box_, anchor="bottom", body=6, side=GREEN[3])
    return ic


def C():
    """Disc - temperature control: a round cooling fan - grey housing, blue blades, the logo on its
    white hub (anchors 1, 2, 4)."""
    ic = gk.Icon("scene - disc")
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, "#deddda"), (1, "#9a9996")], depth=5, side="#77767b", layer="housing")
    recess(ic, circ(cx, cy, R - 6), [(0, "#3d3846"), (1, "#241f31")], wall=3, layer="duct")
    for k in range(7):
        a0 = k * 360 / 7
        pts = []
        for t in range(0, 11):
            a = math.radians(a0 + t * 4.2)
            r = 24 + t * 2.3
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        for t in range(10, -1, -1):
            a = math.radians(a0 + t * 4.2 + 26 - t * 0.6)
            r = 24 + t * 2.3
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        blade = rounded(Polygon(pts).buffer(0), 2)
        ic.path(geom_d(blade), ic.linear([(0, BLUE[0]), (1, BLUE[3])], cx, cy - R, cx, cy + R), layer_id=f"blade-{k}")
    hub = circ(cx, cy, 27)
    solid(ic, hub, face=[(0, "#ffffff"), (1, "#deddda")], depth=3, side="#9a9996", layer="hub")
    put_mark(ic, SLUG, (cx - 19, cy - 20, cx + 19, cy + 18))
    return ic


def D():
    """Rimmed - the performance gauge (frequency, FPS): a white dial with its arc from green to
    yellow to red, the needle up high, the logo under the needle (anchors 1, 2, 4)."""
    ic = gk.Icon("scene - rimmed")
    cx, cy = 64, 58
    body = unary_union([circ(cx, cy, 56).intersection(box(0, 0, 128, cy)), rounded(box(8, cy - 10, 120, 116), 12)])
    solid(ic, rounded(body, 4), face=[(0, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="case")
    face = unary_union([circ(cx, cy, 49).intersection(box(0, 0, 128, cy)), rounded(box(15, cy - 10, 113, 109), 8)])
    recess(ic, rounded(face, 3), [(0, "#ffffff"), (1, "#deddda")], wall=2, layer="dial")
    for k, col in enumerate((GREEN[1], "#f6d32d", "#e01b24")):
        seg = LineString([(cx + 38 * math.cos(math.radians(a)), cy + 38 * math.sin(math.radians(a)))
                          for a in range(186 + k * 56, 186 + (k + 1) * 56 + 1, 4)]).buffer(6, cap_style=2)
        ic.path(geom_d(seg), col, layer_id=f"arc-{k}")
    na = math.radians(-38)
    needle = Polygon([(cx + 38 * math.cos(na), cy + 38 * math.sin(na)),
                      (cx + 4.5 * math.cos(na + math.pi / 2), cy + 4.5 * math.sin(na + math.pi / 2)),
                      (cx + 4.5 * math.cos(na - math.pi / 2), cy + 4.5 * math.sin(na - math.pi / 2))])
    ic.path(geom_d(needle), "#c01c28", layer_id="needle")
    solid(ic, circ(cx, cy, 6), face=[(0, "#5e5c64"), (1, "#241f31")], depth=1.5, side="#000000", layer="pivot")
    put_mark(ic, SLUG, (38, 68, 90, 105))
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
