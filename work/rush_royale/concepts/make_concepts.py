"""Rush Royale - concepts traced FROM the poster (round 2): the mascot (hat with crown and
gem, crystals) traced from the source; green board excluded."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent


def place(regs, box_):
    shapes = fit([g for g, _ in regs], box_, anchor="bottom")
    return list(zip(shapes, [h for _, h in regs]))

GREEN = ("#92c934", "#96c833", "#aed545", "#a3cf3c")


def mascot():
    return traced(SLUG, (8, 2, 120, 122), n=9, exclude=GREEN)


def hat():
    return traced(SLUG, (14, 2, 114, 66), n=7, exclude=GREEN)


def A():
    """the whole mascot cut out as one object."""
    ic = gk.Icon("Rush Royale concept A - mascot")
    cutout(ic, place(mascot(), (8, 6, 120, 112)), depth=5, layer="m")
    return ic


def B():
    """only the hat with its crown and gem, big."""
    ic = gk.Icon("Rush Royale concept B - hat")
    cutout(ic, place(hat(), (8, 12, 120, 112)), depth=6, layer="hat")
    return ic


def C():
    """the mascot standing on a green board tile (the game's board, L2)."""
    ic = gk.Icon("Rush Royale concept C - mascot on the board")
    board = ellipse(64, 100, 58, 16)
    solid(ic, board, face=[(0, "#aed545"), (1, "#92c934")], depth=6, side="#5e8a1e", layer="board")
    cutout(ic, place(mascot(), (16, 4, 112, 102)), depth=4, layer="m")
    return ic

if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)

