"""Aurex Browser - round 3 (round 2 'hiç benzemiyor'): the anchors are the BLUE field,
the white A and the cyan ball together. Measured parts r0/r1 (A), r3 (ball), blue
#53a2fa -> #305fde."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent


def place(regs, box_):
    shapes = fit([g for g, _ in regs], box_, anchor="bottom")
    return list(zip(shapes, [h for _, h in regs]))

P = parts(SLUG)


def A_ball(box_):
    a_, ball = fit([unary_union([P["r0"], P["r1"]]), P["r3"]], box_, anchor="bottom")
    return a_, ball


def A():
    """L3: a thick blue glass tile (the source's field, as material) with the thick white A
    and the glass bead - the source composition, built."""
    ic = gk.Icon("Aurex concept A - blue glass tile + A")
    tile = rounded(box(10, 10, 118, 112), 22)
    solid(ic, tile, face=[(0, "#62a0ea"), (0.5, "#4281ec"), (1, "#305fde")], depth=6, side="#1e57c4", layer="tile")
    ic.path(geom_d(circ(40, 30, 30).intersection(tile)), ic.radial([(0, "#ffffff", 0.45), (1, "#ffffff", 0)], 40, 30, 30), layer_id="glint")
    a_, ball = A_ball((26, 20, 102, 102))
    solid(ic, a_, face=[(0, "#ffffff"), (0.6, "#e6f1fd"), (1, "#b1cff5")], depth=5, side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c4fff8"), (0.5, "#59e6dd"), (1, "#2fb9c9")], depth=2, side="#2a9fb0", layer="ball")
    return ic


def B():
    """L1: the A in Aurex blue (the field becomes the letter's material), white top face."""
    ic = gk.Icon("Aurex concept B - blue A")
    a_, ball = A_ball((14, 10, 114, 110))
    solid(ic, a_, face=[(0, "#99c1f1"), (0.5, "#53a2fa"), (1, "#305fde")], depth=8, side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c4fff8"), (0.5, "#59e6dd"), (1, "#2fb9c9")], depth=3, side="#2a9fb0", layer="ball")
    return ic


def C():
    """L2: a blue browser window, the white A on its page, the bead in front."""
    ic = gk.Icon("Aurex concept C - blue window + A")
    win = rounded(box(8, 16, 120, 108), 10)
    solid(ic, win, face=[(0, "#62a0ea"), (1, "#305fde")], depth=6, side="#1e57c4", layer="win")
    for i, x in enumerate((18, 26, 34)):
        ic.path(geom_d(circ(x, 25, 2.4)), "#ffffff", opacity=0.9, layer_id=f"dot{i}")
    a_, ball = A_ball((34, 34, 94, 102))
    solid(ic, a_, face=[(0, "#ffffff"), (1, "#b1cff5")], depth=4, side="#1e57c4", layer="A")
    solid(ic, ball, face=[(0, "#c4fff8"), (1, "#2fb9c9")], depth=2, side="#2a9fb0", layer="ball")
    return ic

if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)

