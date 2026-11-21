"""Rush Royale - redesign, round 3: the game's OBJECTS only (REDESIGN 3b). Main = C (the
wizard hat with the gold crown band + magenta gem, two glowing ice crystals) -> Symbol
(+ faithful, rimmed); kept D (round green tile + hat + crystal) -> disc. Parts: kit.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import *  # noqa: F401,F403,E402
SLUG = "rush_royale"


def design_C():
    ic = gk.Icon("Rush Royale")
    hat(ic, 64, 114, 110, brim=50)
    crystal(ic, 24, 98, 17)
    crystal(ic, 104, 98, 17)
    return ic


def design_D():
    ic = gk.Icon("Rush Royale")
    t = ellipse(64, 99, 57, 15)
    solid(ic, t, face=[(0, "#57e389"), (1, "#2ec27e")], depth=6, side="#26a269", top=False, layer="tile")
    hat(ic, 58, 105, 96, brim=54)
    crystal(ic, 107, 84, 13)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": design_C(), "disc": design_D()})
