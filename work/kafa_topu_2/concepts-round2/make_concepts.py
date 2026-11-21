"""Kafa Topu 2 - concepts traced FROM the poster (round 2; round 1 = generic primitives,
rejected: 'hiç benzemiyor'). Crops in source space: ball 34-94 x 0-58, VS 48-82 x 62-84,
left player's head 0-46 x 24-112; sky blue excluded."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent


def place(regs, box_):
    shapes = fit([g for g, _ in regs], box_, anchor="bottom")
    return list(zip(shapes, [h for _, h in regs]))

SKY = ("#146af5", "#197bf7", "#3eb4fd", "#2a7ff6", "#4dc3f7", "#5fd0fa", "#62c6f8")


def ball():
    return traced(SLUG, (34, 0, 94, 58), n=4, exclude=SKY, keep=circ(64.5, 27.5, 28.5))


def vs():
    return traced(SLUG, (48, 62, 82, 84), n=4, exclude=SKY)


def head():
    return traced(SLUG, (0, 24, 46, 112), n=8, exclude=SKY, keep=ellipse(22, 64, 22, 36))


def A():
    """the ball and the VS badge, both cut out as objects."""
    ic = gk.Icon("Kafa Topu 2 concept A - ball + VS")
    cutout(ic, place(ball(), (18, 8, 98, 84)), depth=5, layer="ball")
    cutout(ic, place(vs(), (58, 74, 120, 112)), depth=4, layer="vs")
    return ic


def B():
    """the game's moment: the big-head player heading the ball."""
    ic = gk.Icon("Kafa Topu 2 concept B - player + ball")
    cutout(ic, place(head(), (8, 34, 78, 114)), depth=5, layer="head")
    cutout(ic, place(ball(), (62, 8, 118, 60)), depth=4, layer="ball")
    return ic


def C():
    """the whole poster scene on a thick blue glass tile (L3, the source composition)."""
    ic = gk.Icon("Kafa Topu 2 concept C - scene tile")
    tile = rounded(box(10, 10, 118, 112), 14)
    solid(ic, tile, face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=6, side="#1a5fb4", layer="tile")
    scene = traced(SLUG, (0, 0, 128, 128), n=9, exclude=SKY)
    for i, (g, h) in enumerate(place(scene, (12, 12, 116, 110))):
        ic.path(geom_d(g.intersection(tile)), h, layer_id=f"s{i}", fill_rule="evenodd")
    return ic

if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)

