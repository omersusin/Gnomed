#!/usr/bin/env python3
"""foto_raflar - Gnomed redesign. Main (Symbol) B picture frame; A photo print (Faithful);
C loupe over a photo (Disc); D stack of prints (Rimmed)."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
BLUE = RAMP["Blue"]
GREEN = RAMP["Green"]
YELLOW = RAMP["Yellow"]
RED = RAMP["Red"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def landscape(ic, x0, y0, x1, y1, layer):
    """A flat printed photo: blue sky, green hill, yellow sun, one red flower."""
    w, h = x1 - x0, y1 - y0
    sky = rr(x0, y0, x1, y1, 2)
    ic.path(geom_d(sky), ic.linear([(0, BLUE[1]), (1, BLUE[2])], x0, y0, x0, y1), layer_id=f"{layer}-sky")
    hill = ellipse(x0 + w * 0.45, y1 + h * 0.22, w * 0.62, h * 0.52).intersection(sky)
    ic.path(geom_d(hill), ic.linear([(0, GREEN[2]), (1, GREEN[4])], x0, y0 + h * 0.5, x0, y1), layer_id=f"{layer}-hill")
    sun = circ(x0 + w * 0.74, y0 + h * 0.26, h * 0.13)
    ic.path(geom_d(sun), YELLOW[3], layer_id=f"{layer}-sun")
    flower = circ(x0 + w * 0.30, y0 + h * 0.72, h * 0.045)
    ic.path(geom_d(flower), RED[3], layer_id=f"{layer}-flower")


def A():
    """Faithful - a photo album: green cover, white-bordered landscape, a title line."""
    ic = gk.Icon("foto_raflar - faithful")
    cover = book(ic, 62, 118, 86, ramp=GREEN, name="album")
    toplight(ic, cover, width=1.5, opacity=0.55, layer="album")
    ph = rr(30, 28, 90, 80, 2)
    solid(ic, ph, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer="photo-border")
    landscape(ic, 34, 32, 86, 76, "photo")
    for i, (y, w) in enumerate(((88, 48), (98, 34))):
        line = rr(34, y, 34 + w, y + 5, 2)
        solid(ic, line, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1, side=LIGHT[4], top=False, layer=f"title{i}")
    return ic


def B():
    """Main - a picture frame: blue frame, white mat, a landscape."""
    ic = gk.Icon("foto_raflar - symbol")
    frame = rr(12, 16, 116, 116, 8)
    solid(ic, frame, face=[(0, BLUE[1]), (0.5, BLUE[3]), (1, BLUE[4])], depth=8, side=BLUE[4], layer="frame")
    toplight(ic, frame, width=2, opacity=0.55, layer="frame")
    mat = rr(22, 26, 106, 106, 4)
    solid(ic, mat, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="mat")
    landscape(ic, 30, 34, 98, 98, "photo")
    return ic


def C():
    """Disc - a loupe over a photo: photo card, dark ring, glass, handle."""
    ic = gk.Icon("foto_raflar - disc")
    card = rr(20, 28, 108, 114, 5)
    solid(ic, card, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=5, side=LIGHT[4], layer="card")
    landscape(ic, 26, 34, 102, 106, "photo")
    handle = LineString([(76, 78), (104, 106)]).buffer(7.0, cap_style=1)
    solid(ic, handle, face=[(0, DARK[1]), (1, DARK[3])], depth=4, side=DARK[4], layer="handle")
    ring = circ(58, 60, 30)
    solid(ic, ring, face=[(0, DARK[1]), (1, DARK[3])], depth=5, side=DARK[4], layer="ring")
    lens = circ(58, 60, 23)
    solid(ic, lens, face=[(0, BLUE[1]), (1, BLUE[3])], depth=2, side=BLUE[4], top=False, layer="lens")
    hill = ellipse(58, 84, 26, 16).intersection(circ(58, 60, 23))
    ic.path(geom_d(hill), GREEN[3], layer_id="lens-hill")
    ic.path(geom_d(ellipse(50, 50, 5, 7)), "#ffffff", opacity=0.6, layer_id="lens-hl")
    return ic


def D():
    """Rimmed - a stack of prints: three prints fanned, the top one a landscape."""
    ic = gk.Icon("foto_raflar - rimmed")
    for i, (ang, dx) in enumerate(((-9, -4), (8, 5))):
        p = rr(22, 26, 106, 110, 4)
        p = affinity.rotate(p, ang, origin=(64, 108))
        p = affinity.translate(p, dx, 0)
        solid(ic, p, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=4, side=LIGHT[4], layer=f"back{i}")
        toplight(ic, p, width=1.5, opacity=0.6, layer=f"back{i}")
    top = rr(18, 22, 110, 114, 4)
    solid(ic, top, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=5, side=LIGHT[4], layer="top")
    toplight(ic, top, width=1.5, opacity=0.6, layer="top")
    landscape(ic, 26, 30, 102, 104, "photo")
    clip = rr(76, 10, 90, 30, 4)
    solid(ic, clip, face=[(0, RED[1]), (1, RED[3])], depth=3, side=RED[4], layer="clip")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
