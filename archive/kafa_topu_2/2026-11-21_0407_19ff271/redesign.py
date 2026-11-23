"""Kafa Topu 2 - redesign (Part E, round 3). Main = B (busts facing + ball + VS) -> Symbol;
kept: A duel -> faithful, C round pitch -> disc, D goal -> rimmed. Parts: kit.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403,E402
SLUG = "kafa_topu_2"


def design_B():
    ic = gk.Icon("Kafa Topu 2")
    ball(ic, 64, 31, 17, depth=3)
    bust(ic, 34, 83, 24, +1, LEFT_SKIN, "swept", RED, "p1")
    bust(ic, 94, 83, 24, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    vs(ic, 48, 95, 1.0)
    return ic


def design_A():
    ic = gk.Icon("Kafa Topu 2")
    ball(ic, 64, 27, 16, depth=3)
    player(ic, 33, 115, 21, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 95, 115, 21, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    return ic


def design_C():
    ic = gk.Icon("Kafa Topu 2")
    pitch(ic, 64, 99, 56, 15)
    ball(ic, 64, 30, 14, depth=3)
    player(ic, 36, 105, 18, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 92, 105, 18, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    return ic


def design_D():
    ic = gk.Icon("Kafa Topu 2")
    goal(ic, 20, 14, 108, 66)
    player(ic, 33, 115, 21, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 95, 115, 21, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    ball(ic, 64, 46, 14, depth=3)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": design_B(), "faithful": design_A(), "disc": design_C(), "rimmed": design_D()})
