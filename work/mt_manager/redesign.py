#!/usr/bin/env python3
"""mt_manager - Gnomed redesign.
Main (Symbol) A: a filing cabinet with a white MT label. Faithful B: a charcoal folder with a
raised tab, a coral sheet behind and the white MT on the front flap. Disc C: a round archive tin -
charcoal cylinder, silver lid, coral base band, MT on the label. Rimmed D: a USB flash drive -
charcoal body, coral stripe, steel connector, lanyard hole and MT on the body."""
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
    """Faithful - a dark folder, the closest style to the source: a charcoal back panel with a
    raised tab, a salmon sheet peeking out behind it, and a low front flap carrying the white MT."""
    ic = gk.Icon("mt_manager - faithful")
    sheet = rr(20, 16, 108, 46, 3)
    solid(ic, sheet, face=[(0, "#ffb39a"), (0.6, CORAL), (1, CORAL_D)], depth=2, side=CORAL_DD, layer="sheet")
    back = rr(12, 40, 116, 114, 4)
    tab = poly([(12, 40), (12, 24), (54, 24), (60, 40)], 3)
    solid(ic, back.union(tab), face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=5, side=CHAR_DD, layer="back")
    front = poly([(8, 66), (120, 60), (120, 116), (8, 116)], 4)
    solid(ic, front, face=[(0, "#565656"), (0.55, "#434343"), (1, CHAR_DD)], depth=5, side="#1c1c1c", layer="front")
    ic.path(geom_d(poly([(8, 66), (120, 60), (120, 65), (8, 71)], 2)), "#ffffff", opacity=0.16, layer_id="lip")
    put_mark(ic, SLUG, (28, 76, 100, 104), face="#ffffff")
    return ic


def C():
    """Disc - a round archive tin: a charcoal cylinder with a silver lid seen from above, a real
    rim, a small lid handle and a white MT label on the front band. Not a record player."""
    ic = gk.Icon("mt_manager - disc")
    body = rr(18, 44, 110, 110, 7)
    solid(ic, body, face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=5, side=CHAR_DD, layer="body")
    lid = ellipse(64, 44, 48, 14)
    solid(ic, lid, face=[(0, "#f6f5f4"), (0.55, "#d6d5d2"), (1, "#a9a8a5")], depth=3, side="#77767b", layer="lid")
    rim = rr(16, 42, 112, 56, 7).difference(rr(20, 46, 108, 52, 5))
    ic.path(geom_d(rim), "#f6f5f4", opacity=0.55, layer_id="rim")
    knob = ellipse(64, 42, 16, 4.5)
    solid(ic, knob, face=[(0, "#ffffff"), (1, "#b5b3b0")], depth=1.5, side="#77767b", top=False, layer="knob")
    base = rr(18, 98, 110, 110, 6)
    ic.path(geom_d(base.intersection(body)), CORAL, layer_id="base-band")
    label = rr(28, 64, 100, 96, 3)
    solid(ic, label, face=[(0, "#ffffff"), (1, LIGHT[2])], depth=1.5, side=LIGHT[4], top=False, layer="label")
    put_mark(ic, SLUG, (32, 68, 96, 92), face="#3d3846")
    return ic


def D():
    """Rimmed - a USB flash drive: a charcoal body with a coral stripe, a steel connector with
    two contact slots and a real lanyard hole at the back, the white MT on the body."""
    ic = gk.Icon("mt_manager - rimmed")
    body = rr(10, 36, 94, 104, 10)
    hole_g = circ(23, 70, 6.5)
    solid(ic, body.difference(hole_g), face=[(0, "#5e5e5e"), (0.5, CHAR), (1, CHAR_D)], depth=5, side=CHAR_DD, layer="body")
    hole(ic, hole_g, color=(CHAR_DD, "#1c1c1c"), wall=2.5, layer="lanyard")
    strip = rr(36, 36, 94, 48, 5).intersection(body)
    ic.path(geom_d(strip), CORAL, layer_id="stripe")
    put_mark(ic, SLUG, (36, 56, 88, 92), face="#ffffff")
    conn = rr(90, 52, 122, 88, 4)
    solid(ic, conn, face=[(0, "#f6f5f4"), (0.55, "#c0bfbc"), (1, "#8a8986")], depth=4, side="#5e5c64", layer="connector")
    for k in range(2):
        slot = rr(100, 58 + k * 14, 120, 62 + k * 14, 2)
        ic.path(geom_d(slot), "#77767b", opacity=0.6, layer_id=f"slot-{k}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
