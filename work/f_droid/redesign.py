#!/usr/bin/env python3
"""f_droid - Gnomed redesign (Claude, 2026-11-23, batch).

F-Droid's logo is the Android robot's lime head on a blue box with the copyleft sign: the free
software repository. Every style carries the MEASURED logo (put_mark), each on a different thing
from the app (design.md anchors):
  Symbol   A: the app store as GNOME draws it - a shopping bag in F-Droid blue, lime handles, the
              white logo printed on it
  Faithful B: the logo itself as a solid object - robot head on its box, with thickness
  Disc     C: "Find people nearby" - the round Nearby radar, the logo at its centre (shot-3)
  Rimmed   D: "Update all" - an Android phone with F-Droid open: the logo and the blue pill button
              with a lime download arrow (shot-4, shot-6)
"""
import math
import sys
from pathlib import Path

from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
BLUE = ("#42a5f5", "#1e88e5", "#1976d2", "#1565c0", "#0d47a1")        # F-Droid blue (source.png)
LIME = ("#d4ff5c", "#c6f432", "#aeea00", "#93c600", "#76a000")        # the robot's lime (source.png)


def A():
    """Symbol - the app store: a shopping bag (GNOME Software's object) in F-Droid blue with lime
    handles, the white F-Droid logo printed on its front (anchors 1, 2)."""
    ic = gk.Icon("f_droid - symbol")
    cx, base, size = 64, 118, 100
    w, d = size, 6
    h = size * 0.85 - d
    top = base - d - h
    handles = unary_union([ellipse(x, top, w * 0.13, h * 0.26).exterior.buffer(3.2).intersection(box(0, 0, 128, top))
                           for x in (cx - w * 0.2, cx + w * 0.2)])
    solid(ic, handles, face=[(0, LIME[1]), (1, LIME[3])], depth=2, side=LIME[4], layer="bag-handles")
    bag = poly([(cx - w * 0.44, top), (cx + w * 0.44, top), (cx + w / 2, top + h), (cx - w / 2, top + h)], w * 0.05)
    solid(ic, bag, face=[(0, BLUE[1]), (0.5, BLUE[2]), (1, BLUE[3])], depth=d, side=BLUE[4], layer="bag")
    ic.path(geom_d(box(cx - w * 0.44, top, cx + w * 0.44, top + 7).intersection(bag)), "#ffffff", opacity=0.25,
            layer_id="bag-fold")
    label = rounded(box(cx - 30, top + 14, cx + 30, top + h - 7), 6)
    solid(ic, label, face=[(0, "#ffffff"), (1, "#deddda")], depth=1.5, side="#9a9996", layer="label")
    put_mark(ic, SLUG, (cx - 25, top + 19, cx + 25, top + h - 12))
    return ic


def B():
    """Faithful - the logo as a solid object: the lime robot head with its antennas and white
    eyes on the blue box with the copyleft sign, the dark blue as its thickness (anchors 1, 2)."""
    ic = gk.Icon("f_droid - faithful")
    put_mark(ic, SLUG, (14, 10, 114, 110), anchor="bottom", body=8, side=BLUE[4])
    return ic


def C():
    """Disc - "Find people nearby": the round Nearby radar - dark glass, lime rings and the sweep,
    two phones found as blips, the F-Droid logo at the centre (anchors 1, 2, 4)."""
    ic = gk.Icon("f_droid - disc")
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="radar-case")
    screen = circ(cx, cy, R - 6)
    recess(ic, screen, [(0, "#3d3846"), (1, "#241f31")], wall=3, layer="radar-screen")
    for r in (40,):
        ic.path(geom_d(circ(cx, cy, r).exterior.buffer(1.3)), LIME[2], opacity=0.45, layer_id=f"ring-{r}")
    sweep = Polygon([(cx, cy)] + [(cx + (R - 6) * math.cos(math.radians(a)), cy + (R - 6) * math.sin(math.radians(a)))
                                  for a in range(-90, -29, 3)]).difference(circ(cx, cy, 33))
    ic.path(geom_d(sweep), ic.linear([(0, LIME[2], 0.0), (1, LIME[2], 0.45)], cx, cy - 40, cx + 40, cy - 20),
            layer_id="sweep")
    for bx, by in ((96, 38), (34, 88)):
        ic.path(geom_d(circ(bx, by, 4.5)), LIME[0], layer_id=f"blip-{bx}")
    put_mark(ic, SLUG, (cx - 24, cy - 25, cx + 24, cy + 25), anchor="center")
    return ic


def D():
    """Rimmed - "Update all": an Android phone with F-Droid open - the logo on the white screen and
    the app's blue pill button under it with a lime download arrow (anchors 1, 2, 3)."""
    ic = gk.Icon("f_droid - rimmed")
    body = rounded(box(28, 8, 100, 118), 12)
    solid(ic, body, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=4, side="#241f31", layer="phone")
    screen = rounded(box(33, 15, 95, 108), 7)
    recess(ic, screen, [(0, "#ffffff"), (1, "#f2f2f2")], wall=2, layer="screen")
    put_mark(ic, SLUG, (40, 22, 88, 72))
    pill = rounded(box(38, 80, 90, 98), 9)
    solid(ic, pill, face=[(0, BLUE[1]), (1, BLUE[3])], depth=2, side=BLUE[4], layer="update-all")
    arrow = unary_union([box(61, 82.5, 67, 90), Polygon([(56, 89), (72, 89), (64, 96)])])
    ic.path(geom_d(arrow), LIME[1], layer_id="update-arrow")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
