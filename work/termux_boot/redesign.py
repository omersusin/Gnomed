#!/usr/bin/env python3
"""termux_boot - Gnomed redesign.
Main (Symbol) A: an external hard drive. Faithful B: a cardboard package. Disc C: a round power
button. Rimmed D: a boot compact disc."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]
GREEN = RAMP["Green"]
BROWN = RAMP["Brown"]
BLUE = RAMP["Blue"]
PURPLE = RAMP["Purple"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - an ignition key: dark round bow with the >_, steel blade and two teeth."""
    ic = gk.Icon("termux_boot - symbol")
    bow = circ(64, 38, 26)
    solid(ic, bow, face=[(0, DARK[1]), (0.5, DARK[2]), (1, DARK[3])], depth=6, side="#1b1a1f", layer="bow")
    toplight(ic, bow, width=1.6, opacity=0.45, layer="bow")
    put_mark(ic, SLUG, (42, 16, 86, 60), face="#ffffff")
    collar = rr(54, 60, 74, 70, 3)
    solid(ic, collar, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="collar")
    blade = rr(58, 64, 70, 114, 3)
    solid(ic, blade, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[4])], depth=4, side=LIGHT[4], layer="blade")
    toplight(ic, blade, width=1.2, opacity=0.8, layer="blade")
    for i, (y0, y1, w) in enumerate(((92, 101, 86), (106, 115, 82))):
        tooth = rr(70, y0, w, y1, 2)
        solid(ic, tooth, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer=f"tooth{i}")
    return ic


def B():
    """Faithful - the >_ prompt itself: the measured mark, white on a thick Termux-black slab."""
    ic = gk.Icon("termux_boot - faithful")
    slab = rr(10, 16, 118, 118, 18)
    solid(ic, slab, face=[(0, "#2b2a30"), (0.55, "#1b1a1f"), (1, "#111014")], depth=7, side="#0c0b0e", layer="tile")
    toplight(ic, slab, width=2.2, opacity=0.3, layer="tile")
    rim = slab.buffer(-2).difference(slab.buffer(-5))
    ic.path(geom_d(rim), GREEN[3], opacity=0.55, layer_id="green-rim")
    put_mark(ic, SLUG, (20, 32, 108, 104), face="#ffffff")
    return ic


def C():
    """Disc - a round power button: steel bezel, dark cap with the measured prompt, a green LED
    ring at the cap's edge."""
    ic = gk.Icon("termux_boot - disc")
    bezel = circ(64, 66, 46)
    solid(ic, bezel, face=[(0, LIGHT[1]), (0.5, LIGHT[2]), (1, LIGHT[3])], depth=8, side=LIGHT[4], layer="bezel")
    toplight(ic, bezel, width=2.2, opacity=0.7, layer="bezel")
    cap = circ(64, 66, 36)
    solid(ic, cap, face=[(0, DARK[1]), (0.6, DARK[2]), (1, DARK[3])], depth=4, side=DARK[3], top=False, layer="cap")
    put_mark(ic, SLUG, (42, 44, 86, 88), face="#ffffff")
    led = circ(64, 66, 34).difference(circ(64, 66, 32))
    ic.path(geom_d(led), GREEN[2], layer_id="led-ring", fill_rule="evenodd")
    return ic


def D():
    """Rimmed - a boot CD with a white label: silver disc, iridescent rim, the prompt printed on
    the label, a real centre hole."""
    ic = gk.Icon("termux_boot - rimmed")
    disc = circ(64, 62, 46).difference(circ(64, 62, 8))
    solid(ic, disc, face=[(0, "#f2f0f7"), (0.5, "#c6d2ea"), (1, "#94a6cc")], depth=5, side=LIGHT[4], layer="disc")
    toplight(ic, disc, width=1.8, opacity=0.8, layer="disc")
    for k, (r0, r1, ramp, op) in enumerate(((45, 40, BLUE, 0.55), (40, 36, PURPLE, 0.45))):
        band = circ(64, 62, r0).difference(circ(64, 62, r1))
        ic.path(geom_d(band), ramp[2], opacity=op, layer_id=f"sheen{k}", fill_rule="evenodd")
    label = circ(64, 62, 38).difference(circ(64, 62, 8))
    solid(ic, label, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="label")
    put_mark(ic, SLUG, (44, 24, 88, 60), face=DARK[3])
    hub = circ(64, 62, 12).difference(circ(64, 62, 8))
    solid(ic, hub, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=2, side=LIGHT[4], top=False, layer="hub")
    rim = circ(64, 62, 46).difference(circ(64, 62, 43))
    ic.path(geom_d(rim), "#6d7fa6", opacity=0.55, layer_id="outer-rim", fill_rule="evenodd")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
