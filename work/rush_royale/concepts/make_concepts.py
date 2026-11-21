"""Rush Royale - round 3 concepts: the game's OBJECTS only (REDESIGN 3b). Hat with the
gold crown band and gem, ice crystals, the green tile board. Drawn with kit.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import *  # noqa: F401,F403,E402
OUT = Path(__file__).resolve().parent


def A():
    """the wizard hat alone, a real object (felt, gold band, gem)."""
    ic = gk.Icon("Rush Royale concept A - hat")
    hat(ic, 64, 118, 104)
    return ic


def B():
    """the hat as a piece standing on the green tile board."""
    ic = gk.Icon("Rush Royale concept B - board + hat")
    board(ic, 10, 72, 118, 112)
    hat(ic, 64, 98, 84)
    return ic


def C():
    """the hat with the two glowing crystals in front (the store icon's objects)."""
    ic = gk.Icon("Rush Royale concept C - hat + crystals")
    hat(ic, 64, 104, 96)
    crystal(ic, 24, 98, 13)
    crystal(ic, 104, 98, 13)
    return ic


def D():
    """round: a round green tile with the hat on it and one crystal."""
    ic = gk.Icon("Rush Royale concept D - round tile")
    t = ellipse(64, 102, 56, 16)
    solid(ic, t, face=[(0, "#57e389"), (1, "#2ec27e")], depth=6, side="#26a269", top=False, layer="tile")
    hat(ic, 58, 108, 86)
    crystal(ic, 104, 92, 11)
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)
