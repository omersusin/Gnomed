#!/usr/bin/env python3
"""apple_music - Gnomed redesign (batch redo, 2026-11-22).
Main (Symbol) A: a pocket music player with the note on its screen. Faithful B: the note itself,
a solid red-pink object. Disc C: a tambourine with the note on its skin. Rimmed D: a wooden
vintage radio with the note on its grille."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from shapely import affinity
from shapely.geometry import LineString

SLUG = Path(__file__).resolve().parent.name
RED = RAMP["Red"]
LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
BROWN = RAMP["Brown"]
BLUE = RAMP["Blue"]
YELLOW = RAMP["Yellow"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a pocket music player: silver body, dark screen with the note, red click wheel."""
    ic = gk.Icon("apple_music - symbol")
    body = rr(26, 8, 102, 114, 11)
    solid(ic, body, face=[(0, LIGHT[0]), (0.5, LIGHT[1]), (1, LIGHT[3])], depth=7, side=LIGHT[4], layer="body")
    toplight(ic, body, width=1.8, opacity=0.85, layer="body")
    screen = rr(34, 16, 94, 66, 4)
    solid(ic, screen, face=[(0, "#2b2a2e"), (1, DARK[3])], depth=2, side=DARK[3], top=False, layer="screen")
    put_mark(ic, SLUG, (40, 20, 88, 62), face="#ffffff")
    wheel = circ(64, 94, 22)
    solid(ic, wheel, face=[(0, LIGHT[1]), (0.6, LIGHT[2]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="wheel")
    toplight(ic, wheel, width=1.4, opacity=0.8, layer="wheel")
    ring = circ(64, 94, 22).difference(circ(64, 94, 17))
    ic.path(geom_d(ring), RED[2], opacity=0.9, layer_id="wheel-ring", fill_rule="evenodd")
    centre = circ(64, 94, 8)
    solid(ic, centre, face=[(0, RED[1]), (1, RED[3])], depth=2, side=RED[4], layer="centre")
    for i, (x, y) in enumerate(((64, 74), (44, 94), (84, 94), (64, 114))):
        ic.path(geom_d(circ(x, y, 1.8)), LIGHT[4], opacity=0.55, layer_id=f"menu{i}")
    return ic


def B():
    """Faithful - the note itself: the measured glyph as a thick red-pink object."""
    ic = gk.Icon("apple_music - faithful")
    shapes = put_mark(ic, SLUG, (14, 10, 114, 108), depth=9,
                      face=[(0, RED[1]), (0.5, RED[2]), (1, RED[3])], side=RED[4])
    for g in shapes:
        toplight(ic, g, width=2.2, opacity=0.35, layer="mark")
    return ic


def C():
    """Disc - a tambourine: blue wooden rim, cream skin with the note, chrome jingles."""
    ic = gk.Icon("apple_music - disc")
    rim = circ(64, 64, 44).difference(circ(64, 64, 33))
    solid(ic, rim, face=[(0, BLUE[1]), (0.5, BLUE[2]), (1, BLUE[4])], depth=8, side=BLUE[4], layer="rim")
    toplight(ic, rim, width=2.0, opacity=0.6, layer="rim")
    skin = circ(64, 64, 34)
    solid(ic, skin, face=[(0, "#fff6e0"), (0.7, "#f4e6c2"), (1, "#e6d3a8")], depth=3, side="#c9b48f", layer="skin")
    toplight(ic, skin, width=1.8, opacity=0.8, layer="skin")
    for k in range(6):
        a = -math.pi / 2 + k * math.pi / 3
        cx, cy = 64 + 38.5 * math.cos(a), 64 + 38.5 * math.sin(a)
        for j, off in enumerate((-2.4, 2.4)):
            jg = rr(cx - 2.6, cy + off - 1.4, cx + 2.6, cy + off + 1.4, 1.4)
            jg = affinity.rotate(jg, math.degrees(a) + 90, origin=(cx, cy))
            solid(ic, jg, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=1.5, side=LIGHT[4], top=False,
                  layer=f"jingle{k}{j}")
    put_mark(ic, SLUG, (42, 42, 86, 86), face=RED[2])
    hole = circ(64, 21, 3.2)
    ic.path(geom_d(hole), "#3d3846", opacity=0.9, layer_id="grip-hole")
    return ic


def D():
    """Rimmed - a vintage wooden radio: wood case, cream dial, the note on the dark grille."""
    ic = gk.Icon("apple_music - rimmed")
    case = rr(12, 34, 116, 116, 8)
    solid(ic, case, face=[(0, BROWN[1]), (0.5, BROWN[2]), (1, BROWN[4])], depth=7, side=BROWN[4], layer="case")
    toplight(ic, case, width=1.6, opacity=0.55, layer="case")
    dial = rr(20, 40, 108, 62, 4)
    recess(ic, dial, [(0, "#f6e6c4"), (1, "#e8d3a4")], wall=2.5, layer="dial")
    for k in range(11):
        x = 27 + k * 7.4
        tick = rr(x - 0.7, 43, x + 0.7, 43 + (8 if k % 5 == 0 else 5), 0.7)
        ic.path(geom_d(tick), BROWN[4], opacity=0.7, layer_id=f"tick{k}")
    needle = rr(58, 41.5, 60.4, 60.5, 1.2)
    solid(ic, needle, face=[(0, RED[1]), (1, RED[3])], depth=1, side=RED[4], top=False, layer="needle")
    grille = rr(20, 68, 80, 112, 5)
    solid(ic, grille, face=[(0, DARK[1]), (1, DARK[3])], depth=2, side=DARK[3], top=False, layer="grille")
    for k in range(6):
        y = 73 + k * 6.2
        slot = rr(25, y, 75, y + 2.6, 1.3)
        ic.path(geom_d(slot), BROWN[1], opacity=0.45, layer_id=f"slot{k}")
    put_mark(ic, SLUG, (28, 72, 76, 110), face="#ffffff")
    knob1 = circ(96, 80, 9)
    solid(ic, knob1, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="knob1")
    knob2 = circ(96, 102, 6)
    solid(ic, knob2, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=3, side=LIGHT[4], layer="knob2")
    return ic


save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
