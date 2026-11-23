"""Pokémon UNITE - redesign (Part E, round 3). Main = A (three heroes charging) -> Symbol;
kept: B dunk into the gold goal ring -> faithful, C round arena -> disc, D goal ring -> rimmed.
Parts: kit.py; references: refs/ (owner's screenshots) + source.png."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403,E402
SLUG = "pokemon_unite"


def torso(ic, pts, ramp, name, r=6):
    g = poly(pts, r)
    solid(ic, g, face=[(0, ramp[1]), (1, ramp[2])], depth=3, side=ramp[3], layer=name)
    return g


def design_A():
    ic = gk.Icon("Pokémon UNITE")
    # back-left: the dragon, its neck and shoulder down to the baseline
    torso(ic, [(26, 58), (46, 56), (44, 84), (52, 116), (12, 116), (24, 86)], ORANGE, "dragon-neck", 8)
    dragon(ic, 36, 46, 20)
    # right: the rabbit striker, white chest down to the baseline
    torso(ic, [(90, 74), (106, 72), (104, 92), (116, 116), (80, 116), (92, 94)], WHITE, "rabbit-chest", 8)
    scarf = poly([(88, 90), (108, 88), (110, 98), (86, 100)], 3)
    solid(ic, scarf, face=[(0, "#3584e4"), (1, "#1a5fb4")], depth=2, side="#14457f", layer="rabbit-scarf")
    rabbit(ic, 96, 62, 21)
    # front: the electric mouse, standing on the baseline
    mouse(ic, 60, 76, 22, body=True)
    return ic


def design_B():
    ic = gk.Icon("Pokémon UNITE")
    goal(ic, 86, 115, 26, 70)
    orb(ic, 68, 40, 11)
    mouse(ic, 42, 54, 20)
    dragon(ic, 30, 96, 17)
    rabbit(ic, 104, 96, 16)
    return ic


def design_C():
    ic = gk.Icon("Pokémon UNITE")
    arena(ic, 64, 99, 58, 14)
    dragon(ic, 30, 70, 18)
    rabbit(ic, 100, 74, 18)
    mouse(ic, 62, 58, 21, body=True)
    return ic


def design_D():
    ic = gk.Icon("Pokémon UNITE")
    goal(ic, 64, 115, 42, 62)
    dragon(ic, 36, 94, 15)
    rabbit(ic, 94, 96, 15)
    mouse(ic, 62, 70, 17)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": design_A(), "faithful": design_B(), "disc": design_C(), "rimmed": design_D()})
