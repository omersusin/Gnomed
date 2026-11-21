"""Pokémon UNITE - round 3 concepts (REDESIGN 3b). Every concept keeps the identity:
THREE heroes (dragon / electric mouse / rabbit striker) charging left + the team goal.
Drawn with work/pokemon_unite/kit.py from the store icon (no tracing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import *  # noqa: F401,F403,E402
OUT = Path(__file__).resolve().parent


def A():
    """the store crop: the three heroes in their staggered charge, the mouse in front."""
    ic = gk.Icon("Pokemon UNITE concept A - charge")
    dragon(ic, 36, 46, 19)
    rabbit(ic, 92, 66, 21)
    mouse(ic, 58, 70, 21, body=True)
    return ic


def B():
    """the score: the mouse dunks an energy orb into the purple goal; the other two below."""
    ic = gk.Icon("Pokemon UNITE concept B - dunk")
    goal(ic, 82, 118, 22, 66)
    orb(ic, 70, 44, 9)
    mouse(ic, 48, 50, 17)
    dragon(ic, 30, 98, 14)
    rabbit(ic, 100, 100, 14)
    return ic


def C():
    """round: the arena (purple half / orange half) with the three heroes on it."""
    ic = gk.Icon("Pokemon UNITE concept C - arena")
    arena(ic, 64, 104, 56, 14)
    dragon(ic, 34, 78, 15)
    rabbit(ic, 96, 82, 15)
    mouse(ic, 62, 66, 18, body=True)
    return ic


def D():
    """the goal ring as the frame: the three heroes seen through/in front of it."""
    ic = gk.Icon("Pokemon UNITE concept D - goal ring")
    ring, inner = goal(ic, 64, 120, 40, 62)
    dragon(ic, 38, 96, 14)
    rabbit(ic, 92, 98, 14)
    mouse(ic, 62, 72, 16)
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)
