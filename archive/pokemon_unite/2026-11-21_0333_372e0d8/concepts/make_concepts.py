"""Pokémon UNITE - concepts traced FROM the poster (round 2). Pikachu's head (the most
recognisable element) is traced from the source crop 32-66 x 0-66 - measured, not drawn
from memory. Purple background excluded."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent


def place(regs, box_):
    shapes = fit([g for g, _ in regs], box_, anchor="bottom")
    return list(zip(shapes, [h for _, h in regs]))

BG = ("#8428b2", "#7a2da9", "#5b2a9a")


def pika():
    return traced(SLUG, (30, 0, 68, 66), n=7, exclude=BG,
                  keep=unary_union([ellipse(51, 44, 17, 21), poly([(38, 30), (44, 4), (52, 28)]), poly([(52, 26), (64, 2), (64, 30)])]))


def A():
    """Pikachu's head cut out as an object."""
    ic = gk.Icon("Pokemon UNITE concept A - Pikachu head")
    cutout(ic, place(pika(), (14, 6, 112, 112)), depth=5, layer="pika")
    return ic


def B():
    """Pikachu's head in front of a purple star (the UNITE purple)."""
    ic = gk.Icon("Pokemon UNITE concept B - head + purple star")
    import numpy as np
    a = np.radians(-90 + np.arange(10) * 36)
    rr = np.where(np.arange(10) % 2 == 0, 56, 30)
    star = poly(list(zip(64 + rr * np.cos(a), 62 + rr * np.sin(a))), 3)
    solid(ic, star, face=[(0, "#c061cb"), (1, "#813d9c")], depth=5, side="#613583", layer="star")
    cutout(ic, place(pika(), (30, 22, 104, 114)), depth=4, layer="pika")
    return ic


def C():
    """the three heroes (the poster) on a purple glass tile (L3)."""
    ic = gk.Icon("Pokemon UNITE concept C - poster tile")
    tile = rounded(box(10, 10, 118, 112), 14)
    solid(ic, tile, face=[(0, "#c061cb"), (1, "#613583")], depth=6, side="#613583", layer="tile")
    scene = traced(SLUG, (0, 0, 128, 104), n=9, exclude=BG)
    for i, (g, h) in enumerate(place(scene, (12, 12, 116, 110))):
        ic.path(geom_d(g.intersection(tile)), h, layer_id=f"s{i}", fill_rule="evenodd")
    return ic

if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)

