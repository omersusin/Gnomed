#!/usr/bin/env python3
"""terminal_em_lat_r - Gnomed redesign.
Main (Symbol) A: a software package box. Faithful B: the measured "> 1+ Term" mark as a slate
object standing on a lime plinth. Disc C: an install disc with a lime label. Rimmed D: a rack server
front with drive caddies, LEDs and a small mark label."""
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
    base = rr(10, 92, 118, 120, 6)
    solid(ic, base, face=[(0, "#b8d95c"), (0.55, GREEN), (1, GREEN_D)], depth=5, side=GREEN_DD, layer="base")
    put_mark(ic, SLUG, (12, 10, 116, 94), depth=3, anchor="bottom", face=SLATE, side=WHITE)
    return ic


def C():
    """Disc - an install disc: a big silver disc with a real spindle hole and a bright rim, a lime
    label carrying the white mark above the hub, and a soft shine across the top left."""
    ic = gk.Icon("terminal_em_lat_r - disc")
    full = circ(64, 64, 50)
    disc = full.difference(circ(64, 64, 7))
    solid(ic, disc, face=[(0, "#ffffff"), (0.55, LIGHT[2]), (1, LIGHT[4])], depth=5, side=LIGHT[4], layer="disc")
    rim = full.difference(circ(64, 64, 46))
    ic.path(geom_d(rim), "#b5b3b0", opacity=0.7, layer_id="rim")
    shine = circ(48, 44, 44).difference(circ(55, 51, 44)).intersection(disc)
    ic.path(geom_d(shine), "#ffffff", opacity=0.45, layer_id="shine")
    label = circ(64, 64, 46).difference(circ(64, 64, 7))
    solid(ic, label, face=[(0, "#c9e06f"), (0.55, GREEN), (1, GREEN_D)], depth=2, side=GREEN_DD, top=False, layer="label")
    hub = circ(64, 64, 10).difference(circ(64, 64, 7))
    solid(ic, hub, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=1.5, side=LIGHT[4], top=False, layer="hub")
    put_mark(ic, SLUG, (44, 24, 84, 56), face="#ffffff")
    return ic


def D():
    """Rimmed - a rack server seen from the front: a slate chassis with a lime bezel line, a dark
    drive-bay recess holding two light caddies with their handles, two status LEDs and a steel
    label with the mark in the lower corner."""
    ic = gk.Icon("terminal_em_lat_r - rimmed")
    cab = rr(8, 18, 120, 114, 7)
    solid(ic, cab, face=[(0, "#7d99a6"), (0.35, SLATE), (1, SLATE_D)], depth=5, side=SLATE_DD, layer="chassis", top=False)
    ic.path(geom_d(rr(8, 26, 120, 32, 2)), GREEN, layer_id="bezel")
    ic.path(geom_d(rr(14, 36, 68, 94, 4)), "#22333c", layer_id="bay-recess")
    for k, y in enumerate((40, 64)):
        ic.path(geom_d(rr(18, y, 64, y + 26, 3)), "#e9edee", layer_id=f"caddy-{k}")
        ic.path(geom_d(rr(20, y + 10, 28, y + 24, 2)), "#5b7482", opacity=0.7, layer_id=f"handle-{k}")
    ic.path(geom_d(circ(78, 70, 3)), GREEN, layer_id="led-0")
    ic.path(geom_d(circ(87, 70, 3)), "#c9a227", layer_id="led-1")
    label = rr(44, 74, 116, 112, 4)
    solid(ic, label, face=[(0, "#ffffff"), (0.7, LIGHT[2]), (1, LIGHT[3])], depth=2, side=LIGHT[4], layer="label", top=False)
    put_mark(ic, SLUG, (47, 76, 113, 110), face=SLATE)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
