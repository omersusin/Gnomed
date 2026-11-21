"""Rush Royale - the game's OBJECTS (REDESIGN.md 3b: no characters, faces or animals).

Reference: the store icon (source.png): a purple wizard hat (wide brim, pointed crown)
with a gold crown band and a magenta gem in a diamond setting, two glowing ice-blue
crystals, on a green checkered board (the game's grid of tiles).
Colours measured: purple #af88f4 / #9f78f3 / #4434ac, gold #edc13f / #c17a0f,
gem #f99db5 -> magenta, crystals #89f3fb / #78c3f7.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_lib"))
from obj import *  # noqa: F401,F403,E402

PURPLE = ("#dc8add", "#9141ac", "#813d9c", "#613583")
VIOLET = ("#b39af5", "#8f6ff0", "#6a4fd6", "#4434ac")   # the hat's blue-violet (measured)
GOLD = ("#f9f06b", "#f6d32d", "#e5a50a", "#c64600")
GREEN = ("#8ff0a4", "#57e389", "#33d17a", "#26a269")


def hat(ic, cx, base_y, w, name="hat", brim=58):
    """Wizard hat standing on its brim: wide brim with thickness, a pointed crown leaning
    a little, a gold crown band with points and a magenta gem. base_y = brim bottom."""
    s = w / 100.0
    # wide brim, the left and right edges curled up (as in the store icon), the front dipping
    import numpy as _np
    t = _np.linspace(0, _np.pi, 40)
    front = [(cx - brim * s * _np.cos(a), base_y - 4 * s - 30 * s * _np.cos(a) ** 4) for a in t]
    back = [(cx + (brim - 8) * s * _np.cos(a), base_y - 24 * s - 8 * s * _np.sin(a) - 22 * s * _np.cos(a) ** 4) for a in t]
    brim_g = poly(front + back, 3 * s)
    solid(ic, brim_g, face=[(0, VIOLET[0]), (0.45, VIOLET[1]), (1, VIOLET[2])], depth=4 * s, side=VIOLET[3], layer=f"{name}-brim")
    # the curls: the brim's underside shows at the raised tips
    for d in (-1, 1):
        under = ellipse(cx + d * (brim - 4) * s, base_y - 38 * s, 7 * s, 6 * s).intersection(brim_g)
        ic.path(geom_d(under), VIOLET[3], opacity=0.55, layer_id=f"{name}-curl{d}")
    shade = ellipse(cx, base_y - 17 * s, 30 * s, 6 * s)
    ic.path(geom_d(shade), VIOLET[3], opacity=0.35, layer_id=f"{name}-shade")
    cone = poly([(cx - 26 * s, base_y - 16 * s), (cx - 14 * s, base_y - 60 * s), (cx + 4 * s, base_y - 96 * s),
                 (cx + 12 * s, base_y - 62 * s), (cx + 26 * s, base_y - 16 * s)], 4 * s)
    cone = cone.union(ellipse(cx, base_y - 16 * s, 26 * s, 6 * s))
    ic.path(geom_d(cone), ic.linear([(0, VIOLET[3]), (0.35, VIOLET[1]), (0.7, VIOLET[0]), (1, VIOLET[2])],
                                     cx - 26 * s, 0, cx + 26 * s, 0), layer_id=f"{name}-cone")
    toplight(ic, cone, layer=f"{name}-cone")
    # gold crown band: a curved band with three points
    band = poly([(cx - 26 * s, base_y - 18 * s), (cx - 24 * s, base_y - 34 * s), (cx - 13 * s, base_y - 30 * s),
                 (cx, base_y - 44 * s), (cx + 13 * s, base_y - 30 * s), (cx + 24 * s, base_y - 34 * s),
                 (cx + 26 * s, base_y - 18 * s), (cx, base_y - 12 * s)], 2 * s)
    solid(ic, band, face=[(0, GOLD[0]), (0.5, GOLD[1]), (1, GOLD[2])], depth=2 * s, side=GOLD[3], layer=f"{name}-band")
    # gem in a diamond setting
    setting = poly([(cx, base_y - 40 * s), (cx + 10 * s, base_y - 27 * s), (cx, base_y - 15 * s), (cx - 10 * s, base_y - 27 * s)], 1.5 * s)
    ic.path(geom_d(setting), GOLD[2], layer_id=f"{name}-setting")
    gem = poly([(cx, base_y - 36 * s), (cx + 7 * s, base_y - 27 * s), (cx, base_y - 19 * s), (cx - 7 * s, base_y - 27 * s)], 1 * s)
    ic.path(geom_d(gem), ic.linear([(0, "#f8a5d4"), (0.45, "#e0379c"), (1, "#a51d6e")], 0, base_y - 36 * s, 0, base_y - 19 * s),
            layer_id=f"{name}-gem")
    facet = poly([(cx - 1 * s, base_y - 33 * s), (cx + 3 * s, base_y - 28 * s), (cx - 2 * s, base_y - 27 * s)], 0.5 * s)
    ic.path(geom_d(facet), "#ffffff", opacity=0.8, layer_id=f"{name}-facet")
    return brim_g.union(cone)


def crystal(ic, cx, cy, r, name="crystal"):
    """Glowing ice crystal: a rounded diamond of blue glass, a bright inner facet."""
    d = poly([(cx, cy - r * 1.25), (cx + r, cy), (cx, cy + r * 1.25), (cx - r, cy)], r * 0.25)
    solid(ic, d, face=[(0, "#99c1f1"), (1, "#3584e4")], depth=2, side="#1a5fb4", top=False, layer=f"{name}-body")
    ic.path(geom_d(d), ic.radial([(0, "#ffffff"), (0.45, "#99c1f1", 0.9), (1, "#3584e4", 0.9)], cx, cy - r * 0.2, r * 1.2), layer_id=f"{name}-glow")
    inner = poly([(cx, cy - r * 0.55), (cx + r * 0.42, cy), (cx, cy + r * 0.55), (cx - r * 0.42, cy)], r * 0.08)
    ic.path(geom_d(inner), "#ffffff", opacity=0.9, layer_id=f"{name}-facet")
    toplight(ic, d, layer=name)
    return d


def board(ic, x0, y0, x1, y1, n=3, m=2, depth=6, name="board"):
    """The green tile board (checkered), with thickness."""
    g = rounded(box(x0, y0, x1, y1), 6)
    solid(ic, g, face=GREEN[2], depth=depth, side=GREEN[3], top=False, layer=name)
    tw, th = (x1 - x0) / n, (y1 - y0) / m
    light = unary_union([box(x0 + i * tw, y0 + j * th, x0 + (i + 1) * tw, y0 + (j + 1) * th)
                         for i in range(n) for j in range(m) if (i + j) % 2 == 0]).intersection(g)
    ic.path(geom_d(light), GREEN[1], layer_id=f"{name}-light")
    toplight(ic, g, layer=name)
    return g
