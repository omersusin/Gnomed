"""Kafa Topu 2 - round 3 concepts (REDESIGN 3b; refs/ = store icon + 2 game screenshots +
the banner). Every concept keeps the identity: TWO big heads facing each other, each on ONE
boot, and the ball between them. Drawn with work/kafa_topu_2/kit.py (no tracing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import *  # noqa: F401,F403,E402
OUT = Path(__file__).resolve().parent


def A():
    """the duel: two players (head + boot) facing, the ball above between them."""
    ic = gk.Icon("Kafa Topu 2 concept A - duel")
    ball(ic, 64, 28, 15)
    player(ic, 33, 117, 20, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 95, 117, 20, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    return ic


def B():
    """close to the store icon: two busts facing, the ball above, the VS between."""
    ic = gk.Icon("Kafa Topu 2 concept B - busts + VS")
    bust(ic, 34, 70, 22, +1, LEFT_SKIN, "swept", RED, "p1")
    bust(ic, 94, 70, 22, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    ball(ic, 64, 26, 15)
    vs(ic, 49, 86, 0.95)
    return ic


def C():
    """round: the two players and the ball on a round pitch with thickness."""
    ic = gk.Icon("Kafa Topu 2 concept C - pitch")
    pitch(ic, 64, 100, 56, 15)
    ball(ic, 64, 40, 12)
    player(ic, 36, 106, 16, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 92, 106, 16, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    return ic


def D():
    """the header duel in front of the goal: both heads rise to the same ball."""
    ic = gk.Icon("Kafa Topu 2 concept D - goal")
    goal(ic, 14, 12, 114, 70)
    player(ic, 36, 117, 18, +1, LEFT_SKIN, "swept", RED, "p1")
    player(ic, 92, 117, 18, -1, RIGHT_SKIN, "buzz", BLUE, "p2")
    ball(ic, 64, 54, 12)
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)
