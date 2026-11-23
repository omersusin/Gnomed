#!/usr/bin/env python3
"""mt_manager - Gnomed redesign.
Main (Symbol) A: a filing cabinet with a white MT label. Faithful B: an open folder with a white
MT card. Disc C: a hard-disk platter with an MT label band. Rimmed D: an archive box with a coral
lid, a real handle slot and an MT label."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
CHAR = "#474747"
CHAR_D = "#343434"
CHAR_DD = "#232323"
CORAL = "#ff8a65"
CORAL_D = "#e0674a"
CORAL_DD = "#b04a30"
LIGHT = RAMP["Light"]
BLUE = "#5b85fa"


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a filing cabinet: a charcoal two-drawer cabinet, a coral top, two handle bars and
    a white label plate with the dark MT on the top drawer."""
    ic = gk.Icon("mt_manager - symbol")
    body = rr(22, 22, 106, 118, 5)
    solid(ic, body, face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=6, side=CHAR_DD, layer="cabinet")
    toplight(ic, body, width=1.8, opacity=0.4, layer="cabinet")
    top = rr(20, 18, 108, 30, 4)
    solid(ic, top, face=[(0, "#ffa183"), (1, CORAL_D)], depth=3, side=CORAL_DD, layer="top")
    for i, (y0, y1) in enumerate(((34, 72), (78, 112))):
        drawer = rr(28, y0, 100, y1, 3)
        solid(ic, drawer, face=[(0, "#525252"), (1, "#2e2e2e")], depth=2, side=CHAR_DD, top=False, layer=f"drawer-{i}")
        bar = rr(46, (y0 + y1) / 2 + 6, 82, (y0 + y1) / 2 + 12, 3)
        solid(ic, bar, face=[(0, LIGHT[3]), (1, LIGHT[4])], depth=2, side="#5e5c64", layer=f"bar-{i}")
    plate = rr(32, 40, 96, 66, 3)
    solid(ic, plate, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="plate")
    put_mark(ic, SLUG, (36, 44, 92, 62), face="#3d3846")
    return ic


def B():
    """Faithful - an open folder: a charcoal back panel with a coral tab and a low front flap, a
    white card with the dark MT standing clear. The closest style to the source's folder."""
    ic = gk.Icon("mt_manager - faithful")
    back = rr(14, 44, 114, 112, 4).union(rr(14, 26, 62, 52, 4))
    solid(ic, back, face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=5, side=CHAR_DD, layer="back")
    card = rr(24, 40, 94, 92, 3)
    solid(ic, card, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=2, side=LIGHT[4], layer="card")
    put_mark(ic, SLUG, (30, 52, 86, 80), face="#3d3846")
    front = poly([(12, 86), (116, 86), (116, 116), (12, 116)], 4)
    solid(ic, front, face=[(0, "#ffa183"), (0.55, CORAL), (1, CORAL_D)], depth=5, side=CORAL_DD, layer="front")
    ic.path(geom_d(rr(12, 86, 116, 90, 2)), "#ffffff", opacity=0.18, layer_id="front-lip")
    tab = rr(92, 28, 112, 50, 3)
    solid(ic, tab, face=[(0, "#ffa183"), (1, CORAL_D)], depth=3, side=CORAL_DD, layer="tab")
    return ic


def C():
    """Disc - a hard-disk platter: a silver disc with a real spindle hole, an actuator arm and a
    white label band carrying the dark MT."""
    ic = gk.Icon("mt_manager - disc")
    full = circ(64, 62, 46)
    platter = full.difference(circ(64, 62, 7))
    solid(ic, platter, face=[(0, "#6f6f6f"), (0.45, "#555555"), (1, "#2f2f2f")], depth=5, side=CHAR_DD, layer="platter")
    sheen = box(20, 22, 108, 46).intersection(platter)
    ic.path(geom_d(sheen), "#ffffff", opacity=0.14, layer_id="sheen")
    hub = circ(64, 62, 15).difference(circ(64, 62, 7))
    solid(ic, hub, face=[(0, "#deddda"), (1, "#9a9996")], depth=2, side="#5e5c64", top=False, layer="hub")
    arm = poly([(96, 16), (108, 18), (92, 52), (82, 64), (74, 56), (86, 42)], 3)
    solid(ic, arm, face=[(0, "#ffa183"), (0.55, CORAL), (1, CORAL_D)], depth=3, side=CORAL_DD, layer="arm")
    pivot = circ(100, 20, 7)
    solid(ic, pivot, face=[(0, "#5e5e5e"), (1, CHAR_D)], depth=2, side=CHAR_DD, layer="pivot")
    band = rr(22, 70, 106, 96, 4)
    band = band.intersection(box(14, 70, 114, 96))
    solid(ic, band, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="band")
    put_mark(ic, SLUG, (32, 74, 96, 92), face="#3d3846")
    return ic


def D():
    """Rimmed - an archive box: a charcoal box, a coral rimmed lid, a real handle slot cut through
    the front and a white MT label."""
    ic = gk.Icon("mt_manager - rimmed")
    boxg = rr(18, 42, 110, 118, 4)
    handle = rr(50, 94, 78, 106, 4)
    solid(ic, boxg.difference(handle), face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=6, side=CHAR_DD, layer="box")
    toplight(ic, boxg.difference(handle), width=1.8, opacity=0.4, layer="box")
    lid = rr(12, 26, 116, 52, 4)
    solid(ic, lid, face=[(0, "#ffa183"), (0.55, CORAL), (1, CORAL_D)], depth=4, side=CORAL_DD, layer="lid")
    rim = rr(14, 48, 114, 54, 2)
    ic.path(geom_d(rim), "#ffffff", opacity=0.22, layer_id="rim")
    label = rr(28, 60, 100, 88, 3)
    solid(ic, label, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="label")
    put_mark(ic, SLUG, (32, 64, 96, 84), face="#3d3846")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
