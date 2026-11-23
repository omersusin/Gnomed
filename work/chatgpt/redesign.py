#!/usr/bin/env python3
"""chatgpt - Gnomed redesign.
Main (Symbol) A: a lit lightbulb. Faithful B: the knot as a solid object. Disc C: a round chat
bubble with a spark. Rimmed D: a notebook with the knot on its cover."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString, Polygon

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
GREEN = RAMP["Green"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def knot(box_):
    g = parts("chatgpt")["knot"]
    (g,) = fit([g], box_)
    return g


def A():
    """Symbol - a lit lightbulb: yellow glass, glowing filament, steel screw base."""
    ic = gk.Icon("chatgpt - symbol")
    bulb = unary_union([circ(64, 46, 28),
                        poly([(50, 66), (78, 66), (73, 82), (55, 82)], 3)])
    solid(ic, bulb, face=[(0, "#fffbe0"), (0.45, YELLOW[1]), (1, YELLOW[2])],
          depth=5, side=YELLOW[3], layer="glass")
    toplight(ic, bulb, width=2, opacity=0.8, layer="glass")
    glow = circ(64, 48, 17)
    ic.path(geom_d(glow), YELLOW[1], opacity=0.55, layer_id="glow")
    put_mark(ic, SLUG, (40, 22, 88, 70), face="#241f31")
    base = rr(55, 80, 73, 106, 4)
    solid(ic, base, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[4])], depth=4, side=LIGHT[4], layer="screw")
    toplight(ic, base, width=1.2, opacity=0.7, layer="screw")
    for k in range(3):
        y = 86 + k * 6
        thread = rr(54, y, 74, y + 2.4, 1.2)
        ic.path(geom_d(thread), LIGHT[4], opacity=0.75, layer_id=f"thread{k}")
    tip = rr(60, 104, 68, 112, 3)
    solid(ic, tip, face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=2, side=LIGHT[4], layer="contact")
    return ic


def B():
    """Faithful - the ChatGPT knot as a thick dark object with light edges."""
    ic = gk.Icon("chatgpt - faithful")
    g = knot((14, 14, 114, 112))
    with ic.group("mark"):
        solid(ic, g, face=[(0, LIGHT[3]), (0.5, LIGHT[4]), (1, DARK[0])], depth=7, side=DARK[1], layer="knot")  # mid grey: reads on both wallpapers
        toplight(ic, g, width=2.2, opacity=0.45, layer="knot")
    return ic


def C():
    """Disc - a round chat bubble with the measured knot printed on it; the knot's counters are
    real holes through the bubble (the wallpaper shows)."""
    ic = gk.Icon("chatgpt - disc")
    k = knot((32, 20, 96, 84))
    filled = unary_union([Polygon(g.exterior) for g in getattr(k, "geoms", [k])])
    holes = filled.difference(k)
    body = unary_union([circ(64, 52, 43), poly([(30, 80), (54, 80), (36, 114)], 3)])
    body = body.difference(holes)
    solid(ic, body, face=[(0, LIGHT[0]), (0.6, LIGHT[1]), (1, LIGHT[2])], depth=6, side=LIGHT[4], layer="bubble")
    toplight(ic, body, width=1.8, opacity=0.8, layer="bubble")
    with ic.group("mark"):
        ic.path(geom_d(k), DARK[3], layer_id="knot", fill_rule="evenodd")
    return ic


def D():
    """Rimmed - a notebook: green cover, the knot printed on it, a page block and a ribbon."""
    ic = gk.Icon("chatgpt - rimmed")
    cover = book(ic, 64, 118, 92, ramp=GREEN, name="book")
    toplight(ic, cover, width=1.6, opacity=0.5, layer="book")
    k = knot((30, 34, 82, 86))
    with ic.group("mark"):
        ic.path(geom_d(k), LIGHT[0], opacity=0.92, layer_id="cover-knot", fill_rule="evenodd")
    band = rr(20, 104, 92, 112, 2)
    ic.path(geom_d(band), GREEN[4], opacity=0.55, layer_id="band")
    ribbon = rr(52, 108, 60, 124, 2)
    solid(ic, ribbon, face=[(0, YELLOW[2]), (1, YELLOW[4])], depth=2, side=YELLOW[4], layer="ribbon")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
