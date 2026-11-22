#!/usr/bin/env python3
"""kamera - Gnomed redesign. Main (Symbol) B compact camera; A lens (Faithful);
C film roll (Disc); D film strip (Rimmed). Build: python3 tools/make_icon.py kamera"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
RED = RAMP["Red"]


def lens(ic, cx, cy, r, depth=8):
    """A camera lens: dark barrel, metal ring, dark glass with a blue iris."""
    barrel = circ(cx, cy, r)
    solid(ic, barrel, face=[(0, DARK[1]), (0.55, DARK[2]), (1, DARK[3])], depth=depth, side=DARK[4], layer="lens-barrel")
    toplight(ic, barrel, width=2, opacity=0.5, layer="lens-barrel")
    ring = circ(cx, cy, r * 0.82).difference(circ(cx, cy, r * 0.72))
    ic.path(geom_d(ring), LIGHT[2], opacity=0.9, layer_id="lens-ring", fill_rule="evenodd")
    glass = circ(cx, cy, r * 0.70)
    hole(ic, glass, color=("#241f31", "#3d3846"), wall=r * 0.10, layer="lens-glass")
    ic.path(geom_d(circ(cx, cy, r * 0.46)), ic.radial([(0, "#99c1f1"), (0.55, "#3584e4"), (1, "#1a5fb4")], cx, cy, r * 0.46),
            layer_id="lens-iris")
    ic.path(geom_d(ellipse(cx - r * 0.20, cy - r * 0.24, r * 0.15, r * 0.10)), "#ffffff", opacity=0.8, layer_id="lens-glint")


def A():
    """Faithful - a telephoto lens with a tripod foot and the source's red dot."""
    ic = gk.Icon("kamera - faithful")
    foot = rounded(box(48, 100, 80, 118), 4)
    solid(ic, foot, face=[(0, DARK[1]), (1, DARK[3])], depth=4, side=DARK[4], layer="lens-foot")
    lens(ic, 64, 58, 46, depth=8)
    dot = circ(99, 29, 7.5)
    solid(ic, dot, face=[(0, RED[1]), (1, RED[3])], depth=2, side=RED[4], layer="red-dot")
    return ic


def B():
    """Main - a compact camera: body, big lens, red shutter, flash, viewfinder."""
    ic = gk.Icon("kamera - symbol")
    body = rounded(box(14, 34, 114, 110), 10)
    solid(ic, body, face=[(0, DARK[1]), (0.5, DARK[2]), (1, DARK[3])], depth=6, side=DARK[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    flash = rounded(box(22, 20, 48, 34), 3)
    solid(ic, flash, face=[(0, LIGHT[0]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="flash")
    shutter = rounded(box(92, 20, 108, 36), 5)
    solid(ic, shutter, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="shutter")
    view = rounded(box(84, 44, 106, 58), 3)
    recess(ic, view, [(0, "#241f31"), (1, DARK[2])], wall=2, layer="viewfinder")
    lens(ic, 56, 72, 31, depth=5)
    return ic


def C():
    """Disc - a camera aperture: silver ring, six blades, a small hexagonal opening."""
    ic = gk.Icon("kamera - disc")
    outer = circ(64, 62, 48)
    solid(ic, outer, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=8, side=LIGHT[4], layer="outer-ring")
    toplight(ic, outer, width=2, opacity=0.6, layer="outer-ring")
    barrel = circ(64, 62, 41)
    solid(ic, barrel, face=[(0, DARK[2]), (1, DARK[4])], depth=2, side=DARK[4], top=False, layer="barrel")
    hexpts = [(64 + 18 * math.cos(math.pi / 6 + k * math.pi / 3),
               62 + 18 * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
    opening = poly(hexpts, 1)
    blades = circ(64, 62, 38).difference(opening)
    solid(ic, blades, face=[(0, DARK[1]), (0.55, DARK[2]), (1, DARK[3])], depth=3, side=DARK[4], layer="blades")
    for k in range(6):
        a = math.pi / 6 + k * math.pi / 3
        p0 = (64 + 18 * math.cos(a), 62 + 18 * math.sin(a))
        p1 = (64 + 37 * math.cos(a + 0.42), 62 + 37 * math.sin(a + 0.42))
        seam = LineString([p0, p1]).buffer(1.2, cap_style=1)
        ic.path(geom_d(seam), DARK[4], opacity=0.75, layer_id=f"seam{k}")
    ic.path(geom_d(opening), ic.radial([(0, "#99c1f1"), (0.6, "#3584e4"), (1, "#1a5fb4")], 60, 54, 20),
            layer_id="opening")
    ic.path(geom_d(circ(64, 62, 38).difference(circ(64, 62, 35))), LIGHT[2], opacity=0.8,
            layer_id="inner-ring", fill_rule="evenodd")
    for k in range(3):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        x, y = 64 + math.cos(a) * 44, 62 + math.sin(a) * 44
        ic.path(geom_d(circ(x, y, 2.4)), LIGHT[4], layer_id=f"screw{k}")
    return ic


def D():
    """Rimmed - a 35 mm film strip with sprocket holes and three frames."""
    ic = gk.Icon("kamera - rimmed")
    strip = rounded(box(8, 54, 120, 114), 6)
    solid(ic, strip, face=[(0, DARK[1]), (1, DARK[3])], depth=4, side=DARK[4], layer="strip")
    toplight(ic, strip, width=1.5, opacity=0.5, layer="strip")
    holes = []
    for i in range(9):
        x = 14 + i * 12
        holes.append(rounded(box(x, 59, x + 6, 65), 1.5))
        holes.append(rounded(box(x, 103, x + 6, 109), 1.5))
    for i, (x0, x1) in enumerate(((14, 44), (50, 78), (84, 114))):
        holes.append(rounded(box(x0, 70, x1, 98), 3))
    for i, h in enumerate(holes):
        ic.path(geom_d(h), DARK[4], layer_id=f"frame{i}")
    for i, (x0, x1) in enumerate(((14, 44), (50, 78), (84, 114))):
        col = (RAMP["Blue"], RAMP["Green"], RED)[i]
        win = rounded(box(x0, 70, x1, 98), 3)
        ic.path(geom_d(win), ic.linear([(0, col[1]), (1, col[4])], x0, 70, x1, 98), layer_id=f"photo{i}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
