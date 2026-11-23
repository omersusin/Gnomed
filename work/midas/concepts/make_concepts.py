#!/usr/bin/env python3
"""midas - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/midas/concepts/make_concepts.py && python3 tools/concepts.py midas
Each function is ONE different idea from the ladder; flat shapes are fine. REPLACE the example bodies.
The app's mark always comes from P (measured), never from memory. Ready objects: from objects import *
(catalogue: docs/redesign/OBJECTS.md). NEVER the logo on a plain tile/square or disc (REDESIGN.md 1)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402   (objects.py + obj.py: gk, solid, parts, fit, RAMP ...)

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)        # r0, r1 ... = colour regions; "holes" = what the mark ENCLOSES (a letter's
                       # counter, or a figure inside a ring - e.g. Telegram's plane). Which is which:
                       # print(describe(SLUG)) - colour + box of every part.
R = regions(SLUG)      # the coloured parts [(name, shape, fill)]. Bands of ONE source gradient come
                       # back merged ("r1+r2") with a real gradient fill (Grad) - never colour() per band:
                       # flat bands look melted (docs/PLAYBOOK.md#gradients)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]
# THE MARK ON EVERY STYLE (REDESIGN.md 5, gate `mark`): put_mark(ic, SLUG, box, face=...) draws the
# measured mark WITHOUT the tile under it, inside a layer named "mark" - the gate finds it there.


def A():
    """L1 - the mark itself becomes the object (thickness, light), no plate.
    If one region is only the logo's BACKGROUND (a tile or circle behind the figure), leave it out."""
    ic = gk.Icon("midas concept A")
    put_mark(ic, SLUG, (14, 12, 114, 112), body=6, anchor="bottom")    # L1: bottom 112 + side 6 = 118
    return ic


def B():
    """L2 - a GNOME object that carries the mark (the app's FUNCTION as a thing).
    EXAMPLE: an envelope with the mark on its stamp - REPLACE envelope/envelope_stamp with the
    app's object from docs/redesign/OBJECTS.md (bottle + bottle_label, browser_window + browser_page,
    shopping_bag + bag_front, ...). Not a plain rounded square with the logo on it."""
    ic = gk.Icon("midas concept B")
    envelope(ic, 64, 118, 108, ramp=RAMP["Blue"])
    put_mark(ic, SLUG, envelope_stamp(64, 118, 108))      # face="#ffffff" for a white mark on a dark part
    return ic


def C():
    """a second, DIFFERENT object idea (another L2 object, or L1 with a secondary object in front)."""
    ic = gk.Icon("midas concept C")
    put_mark(ic, SLUG, (16, 12, 112, 115), depth=3, anchor="bottom")   # bottom 115 + side 3 = 118
    return ic


def D():
    """a fourth, different idea - e.g. a ROUND object (it can fill the Disc slot): a coin, a lens,
    a globe ... with the mark. L3 (a material tile) only for a pure wordmark when L1/L2 fail."""
    ic = gk.Icon("midas concept D")
    put_mark(ic, SLUG, (24, 22, 104, 114), depth=4, anchor="bottom")     # bottom 114 + side 4 = 118
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
