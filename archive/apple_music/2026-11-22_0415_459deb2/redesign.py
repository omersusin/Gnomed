#!/usr/bin/env python3
"""apple_music - Gnomed redesign.
Main (Symbol) B: a pocket music player, red body, dark screen with the measured note, click wheel.
Kept: A -> Faithful (the note itself as a red object), C -> Rimmed (headphones, note on the cup),
D -> Disc (a round speaker with the note on the grille).
Build:  python3 tools/make_icon.py apple_music"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parent.name
P = parts(SLUG)
R = regions(SLUG)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]

RED = RAMP["Red"]
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]


def note_on(ic, box_, colour="#f6f5f4", layer="mark"):
    """Print the measured note inside box_ (flat; the object shows through its holes)."""
    for g in fit(MARK, box_, anchor="center"):
        solid(ic, g, face=colour, depth=0, top=False, layer=layer)


def A():
    """Faithful - L1: the measured note itself as a red enamel object with thickness."""
    ic = gk.Icon("apple_music - faithful")
    for g in fit(MARK, (16, 8, 112, 110), anchor="bottom"):
        g = g.buffer(4.5)                       # the source note is thin; bold it for 32 px
        solid(ic, g, face=[(0, RED[0]), (0.45, RED[1]), (1, RED[2])], depth=4, side=RED[4], layer="note")
        toplight(ic, g, width=1.4, opacity=0.65, layer="note")
    return ic


def B():
    """Symbol - L2: a pocket music player: red body, recessed dark screen with the note, wheel."""
    ic = gk.Icon("apple_music - symbol")
    body = rounded(box(26, 14, 102, 110), 14)
    solid(ic, body, face=[(0, RED[0]), (0.45, RED[1]), (1, RED[2])], depth=8, side=RED[4], layer="player")
    toplight(ic, body, width=1.5, opacity=0.7, layer="player")
    screen = rounded(box(34, 24, 94, 72), 6)
    recess(ic, screen, [(0, "#241f31"), (1, "#3d3846")], wall=3, layer="player-screen")
    note_on(ic, (40, 28, 88, 68))
    wheel = circ(64, 92, 15)
    solid(ic, wheel, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="player-wheel")
    centre = circ(64, 92, 5.5)
    solid(ic, centre, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=1.5, side=LIGHT[4], top=False, layer="player-button")
    top_btn = rounded(box(57, 9, 71, 16), 3)          # top button / jack: a real player detail
    solid(ic, top_btn, face=[(0, LIGHT[2]), (1, LIGHT[4])], depth=3, side=LIGHT[4], layer="player-top")
    return ic


def C():
    """Rimmed - L2: over-ear headphones, red cups, dark cushions, the note on the right cup."""
    ic = gk.Icon("apple_music - rimmed")
    base, d = 122, 6
    cup_w, cup_h = 40, 60
    cy = base - d - cup_h / 2
    arc_r = 40
    band = circ(64, cy - 2, arc_r).difference(circ(64, cy - 2, arc_r - 11)).intersection(box(0, 0, 128, cy - 2))
    band = unary_union([band, box(64 - arc_r, cy - 3, 64 - arc_r + 11, cy),
                        box(64 + arc_r - 11, cy - 3, 64 + arc_r, cy)])
    solid(ic, band, face=[(0, RED[0]), (1, RED[2])], depth=d * 0.8, side=RED[4], layer="phones-band")
    toplight(ic, band, width=1.4, opacity=0.6, layer="phones-band")
    for sx, pad_box in ((-1, (41, cy - 19, 47, cy + 19)), (1, (81, cy - 19, 87, cy + 19))):
        pad = rounded(box(*pad_box), 4)
        solid(ic, pad, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], top=False, layer=f"phones-pad{sx}")
        x = 64 + sx * (arc_r - 4)
        cup = rounded(box(x - cup_w / 2, cy - cup_h / 2, x + cup_w / 2, cy + cup_h / 2), 8)
        solid(ic, cup, face=[(0, RED[0]), (0.5, RED[1]), (1, RED[2])], depth=d, side=RED[4], layer=f"phones-cup{sx}")
        toplight(ic, cup, width=1.4, opacity=0.6, layer=f"phones-cup{sx}")
    note_on(ic, (88, 63, 118, 111))
    return ic


def D():
    """Disc - L2 round: a round speaker, red cabinet rim, dark grille with the note."""
    ic = gk.Icon("apple_music - disc")
    cab = circ(64, 62, 52)
    solid(ic, cab, face=[(0, RED[0]), (0.5, RED[1]), (1, RED[2])], depth=8, side=RED[4], layer="speaker")
    toplight(ic, cab, width=1.5, opacity=0.7, layer="speaker")
    grille = circ(64, 62, 43)
    recess(ic, grille, [(0, "#241f31"), (1, "#3d3846")], wall=4, layer="speaker-grille")
    for r in (36, 29, 22):
        ring = circ(64, 62, r).difference(circ(64, 62, r - 1.2))
        ic.path(geom_d(ring), "#ffffff", opacity=0.08, layer_id=f"speaker-ring{int(r)}")
    note_on(ic, (46, 38, 82, 86))
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": B(), "faithful": A(), "disc": D(), "rimmed": C()})
