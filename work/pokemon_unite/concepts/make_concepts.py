"""Pokémon UNITE - round 4 concepts: the game's OBJECTS only (owner 2026-11-21: "Karakter
yok, oyunun nesnesi"). Goal ring + ball; drawn with work/pokemon_unite/kit.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import *  # noqa: F401,F403,E402
OUT = Path(__file__).resolve().parent


def A():
    """the goal ring standing on its edge, the energy ball in front of it (key art)."""
    ic = gk.Icon("Pokemon UNITE concept A - ring + energy")
    ring(ic, 58, 62, 46, 50, 13)
    energy(ic, 92, 96, 20)
    return ic


def B():
    """the stadium goal: the ring on a metal post, the energy ball dunking into it."""
    ic = gk.Icon("Pokemon UNITE concept B - goal post")
    stand(ic, 64, 70, 118, 8)
    ring(ic, 64, 46, 38, 34, 11)
    energy(ic, 64, 40, 15)
    return ic


def C():
    """round: the arena (purple / orange) with the ring lying on it as the score zone."""
    ic = gk.Icon("Pokemon UNITE concept C - arena")
    arena(ic, 64, 100, 58, 16)
    ring(ic, 64, 96, 34, 10, 6, depth=3)
    energy(ic, 64, 50, 22)
    return ic


def D():
    """the ring + the two team balls (orange and purple, as in the UNITE logo)."""
    ic = gk.Icon("Pokemon UNITE concept D - ring + team balls")
    ring(ic, 64, 54, 46, 44, 12)
    team_ball(ic, 38, 98, 19, ORANGE, "b1")
    team_ball(ic, 90, 98, 19, PURPLE, "b2")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)
