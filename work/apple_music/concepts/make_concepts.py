#!/usr/bin/env python3
"""apple_music - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/apple_music/concepts/make_concepts.py && python3 tools/concepts.py apple_music
The app's mark is the measured Apple Music note (white in source.png); the brand red is the
nearest HIG Red ramp. Four different music objects: note, pocket player, headphones, speaker."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)
R = regions(SLUG)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]

RED = RAMP["Red"]
DARK = RAMP["Dark"]
LIGHT = RAMP["Light"]


def note_on(ic, box_, colour="#f6f5f4", depth=0.0, layer="mark"):
    """Print the measured note inside box_ (flat; the object shows through its holes)."""
    for g in fit(MARK, box_, anchor="center"):
        solid(ic, g, face=colour, depth=depth, side=LIGHT[4], top=False, layer=layer)


def A():
    """L1 - the note itself becomes the object: red enamel, thickness, top light, no plate."""
    ic = gk.Icon("apple_music concept A")
    for g in fit(MARK, (18, 8, 110, 112), anchor="bottom"):
        solid(ic, g, face=[(0, RED[0]), (0.45, RED[1]), (1, RED[2])], depth=6, side=RED[4], layer="note")
        toplight(ic, g, width=1.4, opacity=0.65, layer="note")
    return ic


def B():
    """L2 - a pocket music player: red body, recessed dark screen carrying the note, click wheel."""
    ic = gk.Icon("apple_music concept B")
    body = rounded(box(22, 14, 106, 110), 16)
    solid(ic, body, face=[(0, RED[0]), (0.45, RED[1]), (1, RED[2])], depth=8, side=RED[4], layer="player")
    screen = rounded(box(32, 24, 96, 74), 6)
    recess(ic, screen, [(0, "#241f31"), (1, "#3d3846")], wall=3, layer="player-screen")
    note_on(ic, (38, 28, 90, 70))
    wheel = circ(64, 93, 16)
    solid(ic, wheel, face=[(0, LIGHT[0]), (1, LIGHT[2])], depth=3, side=LIGHT[4], layer="player-wheel")
    centre = circ(64, 93, 6)
    solid(ic, centre, face=[(0, LIGHT[1]), (1, LIGHT[3])], depth=1.5, side=LIGHT[4], top=False, layer="player-button")
    return ic


def C():
    """L2 - over-ear headphones: red cups, dark cushions, the note on the right cup."""
    ic = gk.Icon("apple_music concept C")
    base, d = 118, 6
    cup_w, cup_h = 32, 50
    cy = base - d - cup_h / 2
    arc_r = 44
    band = circ(64, cy - 2, arc_r).difference(circ(64, cy - 2, arc_r - 10)).intersection(box(0, 0, 128, cy - 2))
    band = unary_union([band, box(64 - arc_r, cy - 3, 64 - arc_r + 10, cy),
                        box(64 + arc_r - 10, cy - 3, 64 + arc_r, cy)])
    solid(ic, band, face=[(0, RED[0]), (1, RED[2])], depth=d * 0.8, side=RED[4], layer="phones-band")
    for sx, pad_box in ((-1, (36, cy - 19, 44, cy + 19)), (1, (84, cy - 19, 92, cy + 19))):
        pad = rounded(box(*pad_box), 4)
        solid(ic, pad, face=[(0, DARK[1]), (1, DARK[3])], depth=3, side=DARK[4], top=False, layer=f"phones-pad{sx}")
        x = 64 + sx * (arc_r - 4)
        cup = rounded(box(x - cup_w / 2, cy - cup_h / 2, x + cup_w / 2, cy + cup_h / 2), 12)
        solid(ic, cup, face=[(0, RED[0]), (0.5, RED[1]), (1, RED[2])], depth=d, side=RED[4], layer=f"phones-cup{sx}")
    note_on(ic, (92, cy - 18, 116, cy + 18))
    return ic


def D():
    """L2 - a bookshelf speaker: red cabinet, dark badge with the note, recessed woofer."""
    ic = gk.Icon("apple_music concept D")
    cab = rounded(box(20, 16, 108, 110), 10)
    solid(ic, cab, face=[(0, RED[0]), (0.45, RED[1]), (1, RED[2])], depth=8, side=RED[4], layer="speaker")
    badge = rounded(box(30, 22, 98, 70), 6)
    recess(ic, badge, [(0, "#241f31"), (1, "#3d3846")], wall=3, layer="speaker-badge")
    note_on(ic, (36, 26, 92, 66))
    wc = (64, 92)
    recess(ic, circ(*wc, 17), [(0, DARK[3]), (1, DARK[1])], wall=3, layer="speaker-woofer")
    ic.path(geom_d(circ(*wc, 10.5)), ic.radial([(0, DARK[0]), (1, DARK[3])], wc[0], wc[1] - 4, 12),
            layer_id="speaker-cone")
    solid(ic, circ(*wc, 4), face=[(0, DARK[0]), (1, DARK[2])], depth=1.5, side=DARK[3], top=False, layer="speaker-cap")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
