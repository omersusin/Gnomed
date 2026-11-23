#!/usr/bin/env python3
"""telefon - Gnomed redesign. Main (Symbol) B smartphone; A handset (Faithful);
C rotary dial (Disc); D walkie-talkie (Rimmed). Build: python3 tools/make_icon.py telefon"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity

SLUG = Path(__file__).resolve().parent.name
GREEN = RAMP["Green"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]


def A():
    """Faithful - the source's white handset, in the app's green."""
    ic = gk.Icon("telefon - faithful")
    h = phone_handset(ic, 64, 118, 104, ramp=GREEN, name="handset")
    toplight(ic, h, width=1.5, opacity=0.6, layer="handset")
    return ic


def B():
    """Main - a smartphone: green body, glass screen, speaker slit, camera dot."""
    ic = gk.Icon("telefon - symbol")
    body = rounded(box(26, 10, 102, 118), 11)
    solid(ic, body, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    screen = rounded(box(32, 20, 96, 104), 6)
    recess(ic, screen, [(0, "#1a5e2a"), (1, "#0b3d1a")], wall=3, layer="screen")
    ic.path(geom_d(rounded(box(32, 20, 96, 104), 6)),
            ic.linear([(0, GREEN[2]), (1, "#0b3d1a")], 32, 20, 96, 104), layer_id="screen-glass", opacity=0.55)
    speaker = rounded(box(54, 14, 74, 17), 1.2)
    solid(ic, speaker, face=DARK[3], depth=1, side=DARK[4], top=False, layer="speaker")
    cam = circ(88, 15, 2.2)
    solid(ic, cam, face=DARK[3], depth=1, side=DARK[4], top=False, layer="camera")
    bar = rounded(box(52, 109, 76, 112), 1.2)
    solid(ic, bar, face=LIGHT[1], depth=1, side=LIGHT[4], top=False, layer="bar")
    return ic


def C():
    """Disc - a rotary dial: green plate, light dial with ten real finger holes."""
    ic = gk.Icon("telefon - disc")
    plate = circ(64, 62, 50)
    solid(ic, plate, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=8, side=GREEN[4], layer="plate")
    toplight(ic, plate, width=2, opacity=0.55, layer="plate")
    dial = circ(64, 62, 42)
    solid(ic, dial, face=[(0, LIGHT[0]), (1, LIGHT[3])], depth=4, side=LIGHT[4], layer="dial")
    holes = [circ(64 + math.cos(math.radians(a)) * 29, 62 + math.sin(math.radians(a)) * 29, 5.2)
             for a in range(-108, 252, 36)]
    finger = unary_union(holes)
    ic.path(geom_d(finger), DARK[3], layer_id="finger-holes", fill_rule="evenodd")
    for i, h in enumerate(holes):
        rim = h.buffer(1.6).difference(h)
        ic.path(geom_d(rim), LIGHT[2], opacity=0.9, layer_id=f"finger-rim{i}", fill_rule="evenodd")
    hub = circ(64, 62, 11)
    solid(ic, hub, face=[(0, GREEN[2]), (1, GREEN[4])], depth=3, side=GREEN[4], layer="hub")
    stop = rounded(box(93, 44, 100, 56), 3)
    solid(ic, stop, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer="stop")
    return ic


def D():
    """Rimmed - a walkie-talkie: body, antenna, speaker grille, green PTT button."""
    ic = gk.Icon("telefon - rimmed")
    ant = rounded(box(84, 6, 92, 50), 3.2)
    solid(ic, ant, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer="antenna")
    body = rounded(box(30, 40, 96, 118), 8)
    solid(ic, body, face=[(0, GREEN[1]), (0.5, GREEN[3]), (1, GREEN[4])], depth=6, side=GREEN[4], layer="body")
    toplight(ic, body, width=2, opacity=0.55, layer="body")
    knob = rounded(box(36, 34, 48, 46), 4)
    solid(ic, knob, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], layer="knob")
    screen = rounded(box(40, 48, 86, 64), 3)
    recess(ic, screen, [(0, "#0b3d1a"), (1, GREEN[4])], wall=2, layer="screen")
    for i in range(3):
        y = 72 + i * 9
        slot = rounded(box(44, y, 82, y + 4), 1.5)
        recess(ic, slot, [(0, DARK[4]), (1, DARK[2])], wall=1.5, layer=f"grille{i}")
    ptt = rounded(box(16, 58, 30, 92), 5)
    solid(ic, ptt, face=[(0, GREEN[2]), (1, GREEN[4])], depth=4, side=GREEN[4], layer="ptt")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": C(), "rimmed": D()})
