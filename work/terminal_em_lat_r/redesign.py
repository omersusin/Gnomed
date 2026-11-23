#!/usr/bin/env python3
"""terminal_em_lat_r - Gnomed redesign.
Main (Symbol) A: a software package box. Faithful B: the measured "> 1+ Term" mark as a thick
white object. Disc C: an install disc. Rimmed D: a server rack."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
SLATE = "#678390"
SLATE_D = "#4a6674"
SLATE_DD = "#2f4450"
GREEN = "#a6c73d"
GREEN_D = "#7f9c26"
GREEN_DD = "#5d7418"
WHITE = "#fcfdfb"
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a software package: green box, slate lid, a white label with the mark printed
    in slate. The thing you install a terminal from."""
    ic = gk.Icon("terminal_em_lat_r - symbol")
    body = rr(18, 36, 104, 114, 4)
    solid(ic, body, face=[(0, "#b8d95c"), (0.5, GREEN), (1, GREEN_D)], depth=6, side=GREEN_DD, layer="box")
    toplight(ic, body, width=1.6, opacity=0.45, layer="box")
    lid = rr(15, 26, 107, 44, 4)
    solid(ic, lid, face=[(0, SLATE), (1, SLATE_D)], depth=4, side=SLATE_DD, layer="lid")
    label = rr(28, 52, 96, 100, 3)
    solid(ic, label, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="label")
    put_mark(ic, SLUG, (37, 54, 87, 94), face=SLATE)
    return ic


def B():
    """Faithful - the measured mark itself: the white "> 1+ Term" lettering as a thick solid
    object with a slate side, standing on the source's lime-green wave as a low base. The
    closest style to the logo, no plate."""
    ic = gk.Icon("terminal_em_lat_r - faithful")
    base = rr(20, 100, 108, 116, 5)
    solid(ic, base, face=[(0, "#b8d95c"), (0.55, GREEN), (1, GREEN_D)], depth=5, side=GREEN_DD, layer="base")
    put_mark(ic, SLUG, (14, 14, 114, 100), depth=3, anchor="bottom", face=WHITE, side=SLATE_D)
    return ic


def C():
    """Disc - an install disc: silver, a green label ring with the white mark, a real spindle
    hole."""
    ic = gk.Icon("terminal_em_lat_r - disc")
    full = circ(64, 64, 46)
    disc = full.difference(circ(64, 64, 6.5))
    solid(ic, disc, face=[(0, "#ffffff"), (0.55, LIGHT[2]), (1, LIGHT[4])], depth=5, side=LIGHT[4], layer="disc")
    label = circ(64, 64, 35).difference(circ(64, 64, 6.5))
    solid(ic, label, face=[(0, "#b8d95c"), (0.55, GREEN), (1, GREEN_D)], depth=2, side=GREEN_DD, top=False, layer="label")
    hub = circ(64, 64, 10).difference(circ(64, 64, 6.5))
    solid(ic, hub, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=1, side=LIGHT[4], top=False, layer="hub")
    put_mark(ic, SLUG, (34, 40, 94, 88), face="#ffffff")
    return ic


def D():
    """Rimmed - a server rack: a slate cabinet with the white mark on its door and a wide vent
    cut through at the bottom, ringed in lime. The machine a terminal logs into."""
    ic = gk.Icon("terminal_em_lat_r - rimmed")
    cab = rr(8, 4, 120, 118, 6)
    hole = rr(26, 96, 102, 110, 4)
    body = cab.difference(hole)
    solid(ic, body, face=[(0, "#7d99a6"), (0.3, SLATE), (1, "#2f4450")], depth=5, side="#22333c", layer="cabinet")
    toplight(ic, body, width=1.8, opacity=0.35, layer="cabinet")
    put_mark(ic, SLUG, (20, 12, 108, 82), face="#ffffff")
    ring = rr(20, 92, 108, 114, 6).difference(hole)
    solid(ic, ring, face=[(0, "#b8d95c"), (0.55, GREEN), (1, GREEN_D)], depth=3, side=GREEN_DD, layer="vent-ring")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
