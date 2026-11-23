#!/usr/bin/env python3
"""rush_royale - Gnomed redesign: an ORIGINAL logo inspired by the game (owner: "oyunun
logosuna bakarak, esinlenerek yap, direkt kopyalama"). The game's hero: the purple
wizard hat with a gold crown band and a magenta gem, flanked by glowing blue crystals.
Colours measured from the source: purple #af88f4 / #9f78f3 / #4434ac, gold #edc13f /
#c17a0f, gem #f99db5 -> magenta, crystals #89f3fb / #78c3f7."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name


def design():
    ic = gk.Icon("Rush Royale - Gnomed (wizard hat)")
    # brim: wide, with a raised back edge (stands on the baseline: 106 + 6 + chin)
    brim = unary_union([ellipse(64, 96, 58, 15), ellipse(64, 88, 52, 14)])
    solid(ic, brim, face=[(0, "#af88f4"), (0.5, "#8466e8"), (1, "#4434ac")], depth=6, side="#3d2a8a", layer="brim")
    # cone: pointed, leaning slightly right at the tip (like the game's hat)
    t = np.linspace(0, 1, 40)
    tip = (70, 10)
    left = [((1 - u) * 34 + u * tip[0] - 7 * np.sin(np.pi * u), (1 - u) * 90 + u * tip[1]) for u in t]
    right = [((1 - u) * 94 + u * tip[0] + 2 * np.sin(np.pi * u), (1 - u) * 90 + u * tip[1]) for u in t]
    cone = poly(left + right[::-1][1:], 1.5)
    solid(ic, cone, face=[(0, "#c4a6fa"), (0.45, "#9f78f3"), (1, "#5b45c0")], depth=3, side="#4434ac", layer="cone")
    # gold crown band with three points around the cone's base
    band = cone.intersection(box(0, 70, 128, 88))
    crown = unary_union([band, poly([(42, 72), (49, 57), (56, 72)], 1.5), poly([(55, 72), (64, 50), (73, 72)], 1.5),
                         poly([(72, 72), (79, 57), (86, 72)], 1.5)])
    solid(ic, crown, face=[(0, "#f9e27a"), (0.5, "#edc13f"), (1, "#c17a0f")], depth=2.5, side="#986a44", layer="crown")
    # magenta gem in the crown
    gem = poly([(64, 66), (73, 76), (64, 88), (55, 76)], 1.2)
    solid(ic, gem, face=[(0, "#f99db5"), (0.5, "#c061cb"), (1, "#813d9c")], depth=1.5, side="#613583", layer="gem")
    ic.path(geom_d(poly([(64, 67), (70, 75), (64, 76)])), "#ffffff", opacity=0.55, layer_id="gem-facet")
    # two glowing blue crystals in front, lower left and right (secondary objects)
    for side_, cx in (("l", 20), ("r", 108)):
        c = poly([(cx, 82), (cx + 10, 96), (cx, 110), (cx - 10, 96)], 2)
        ic.path(geom_d(c.buffer(4)), ic.radial([(0, "#89f3fb", 0.55), (1, "#89f3fb", 0)], cx, 96, 16), layer_id=f"glow-{side_}")
        solid(ic, c, face=[(0, "#d6fbff"), (0.5, "#89f3fb"), (1, "#3584e4")], depth=2, side="#1c71d8", layer=f"crystal-{side_}")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
