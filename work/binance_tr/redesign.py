#!/usr/bin/env python3
"""binance_tr - Gnomed redesign.  Concept: <write the approved concept from design.md>.
Build:  python3 tools/make_icon.py binance_tr      (runs this file, then review + gate)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402   (objects.py + obj.py: envelope, bottle, fit, solid, save_styles ...)
SLUG = Path(__file__).resolve().parent.name
P = parts(SLUG)               # measured parts: P["r0"], P["r1"], ..., P["silhouette"], P["holes"]
R = regions(SLUG)             # the same parts ready to draw: [(name, shape, fill)]; gradient bands merged
                              # into one part with a real gradient (Grad) - use these fills, not colour()
# print(describe(SLUG))       # colours / sizes / positions / GRADIENT lines as text


def design():
    ic = gk.Icon("binance_tr - Gnomed")
    # Copy the APPROVED concept from concepts/make_concepts.py here, then polish:
    # thickness (solid depth), light from the top (gradient + toplight), recess / hole,
    # a secondary object. Object inside 8..120, bottom edge (side included) 116..120.
    raise SystemExit("copy the approved concept here (concepts/make_concepts.py), then remove this line")
    return ic


if __name__ == "__main__":
    # REDESIGN.md 6: the MAIN design -> symbol (and every slot without its own design);
    # kept concepts -> faithful (closest to the original) / disc (a round one) / rimmed
    save_styles(SLUG, {"symbol": design()})
