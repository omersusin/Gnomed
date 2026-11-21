"""Pokémon UNITE - redesign, round 4: the game's OBJECTS only (owner 2026-11-21: "Karakter
yok, oyunun nesnesi"). Main = B (the stadium goal: gold ring on a metal post, the energy
ball dunking) -> Symbol (+ disc, rimmed); kept A (ring + energy ball, no blue crescent)
-> faithful. Parts: kit.py; references: refs/."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403,E402
SLUG = "pokemon_unite"


def design_B():
    ic = gk.Icon("Pokémon UNITE")
    stand(ic, 64, 80, 118, 14)
    ring(ic, 64, 50, 49, 42, 14, depth=6, inner=False)
    energy(ic, 64, 44, 19)
    return ic


def design_A():
    ic = gk.Icon("Pokémon UNITE")
    ring(ic, 56, 63, 46, 50, 13, depth=5, inner=False)
    energy(ic, 92, 96, 21)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": design_B(), "faithful": design_A()})
