#!/usr/bin/env python3
"""y_hava_durumu - Gnomed redesign. Main (Symbol) B cloud + red sun; A umbrella (Faithful);
C red sun (Disc); D thermometer (Rimmed). Build: python3 tools/make_icon.py y_hava_durumu"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
RED = RAMP["Red"]
BLUE = RAMP["Blue"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Faithful - the source's umbrella: red canopy with scallops, ribs, dark J handle."""
    ic = gk.Icon("y_hava_durumu - faithful")
    dome = circ(64, 66, 50).intersection(box(14, 16, 114, 70))
    canopy = dome.difference(unary_union([circ(40, 70, 12), circ(64, 70, 12), circ(88, 70, 12)]))
    solid(ic, canopy, face=[(0, RED[1]), (0.5, RED[2]), (1, RED[3])], depth=6, side=RED[4], layer="canopy")
    toplight(ic, canopy, width=2, opacity=0.55, layer="canopy")
    for x in (40, 64, 88):
        rib = LineString([(64, 18), (x, 69)]).buffer(1.2)
        ic.path(geom_d(rib), RED[4], opacity=0.55, layer_id=f"rib{x}")
    ferrule = rr(62, 10, 66, 22, 1.6)
    solid(ic, ferrule, face=[(0, DARK[1]), (1, DARK[3])], depth=2, side=DARK[4], layer="ferrule")
    handle = LineString([(64, 66), (64, 102), (66, 110), (72, 116), (80, 116), (86, 110)]).buffer(3.6, cap_style=1)
    solid(ic, handle, face=[(0, DARK[1]), (1, DARK[3])], depth=2, side=DARK[4], layer="handle")
    return ic


def B():
    """Main - a sunset: a yellow-orange sun() behind a blue cloud."""
    ic = gk.Icon("y_hava_durumu - symbol")
    sun(ic, 86, 84, 70, rays=10, name="sun")
    cloud(ic, 52, 120, 96, ramp=BLUE, name="cloud")
    return ic


def C():
    """Disc - the sun itself: a big yellow-orange sun() with eight rounded rays."""
    ic = gk.Icon("y_hava_durumu - disc")
    sun(ic, 64, 118, 104, rays=8, name="sun")
    return ic


def D():
    """Rimmed - a thermometer: scale plate, glass tube, big red bulb, ticks."""
    ic = gk.Icon("y_hava_durumu - rimmed")
    plate = rr(42, 18, 86, 112, 7)
    solid(ic, plate, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=4, side=LIGHT[4], layer="plate")
    toplight(ic, plate, width=1.5, opacity=0.6, layer="plate")
    for i in range(6):
        y = 34 + i * 12
        tick = rr(48, y, 56 if i % 2 == 0 else 53, y + 2, 1)
        solid(ic, tick, face=DARK[2], depth=0, top=False, layer=f"tick{i}")
    tube = rr(58, 26, 70, 96, 5.5)
    solid(ic, tube, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="tube")
    column = rr(61.5, 52, 66.5, 98, 2.2)
    solid(ic, column, face=[(0, RED[1]), (1, RED[3])], depth=1, side=RED[4], top=False, layer="column")
    bulb = circ(64, 98, 18)
    solid(ic, bulb, face=[(0, RED[1]), (0.5, RED[2]), (1, RED[3])], depth=4, side=RED[4], layer="bulb")
    ic.path(geom_d(ellipse(58, 92, 3.4, 4.6)), "#ffffff", opacity=0.6, layer_id="bulb-hl")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
