#!/usr/bin/env python3
"""kafa_topu_2 - Gnomed redesign: an ORIGINAL logo inspired by the game (REDESIGN.md 3b).
The game's composition is kept (owner: "iki kafa olması gerekiyor, karşı karşıya"):
two big-head footballers FACING each other, the ball above them, the yellow VS between.
Each character is the game's own figure: a big head standing on ONE football boot
(owner: "karakterlerin ayakkabıları var"). Left: brown hair with a blond streak, beard,
red boot; right: buzz cut, darker skin, blue boot. Colours measured from the source (skin #d48154, hair #281a1a / #705254,
ball #e2e5e5 + #281a1a) and mapped to GNOME ramps."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name


def smooth(g, r=1.2):
    return g.buffer(r).buffer(-r).buffer(-r * 0.5).buffer(r * 0.5)


def regular(cx, cy, r, n, rot=-90):
    a = np.radians(rot + np.arange(n) * 360 / n)
    return poly(list(zip(cx + r * np.cos(a), cy + r * np.sin(a))))


def head(ic, cx, cy, r, d, skin, hair_kind, collar, name):
    """A big cartoon head looking towards d (+1 = right, -1 = left)."""
    s_light, s_mid, s_dark, s_side = skin
    # the game's character is a big head standing on ONE football boot (toe towards the
    # opponent): upper in the team colour with a white stripe, dark sole with studs
    bx0 = cx - d * r * 0.50          # heel side
    def bp(u, v):                    # boot-local (u: heel 0 -> toe 1, v: down) -> canvas
        return (bx0 + d * u * r * 1.85, cy + r * 0.78 + v * r)
    upper = poly([bp(0.0, -0.05), bp(0.36, -0.05), bp(0.50, 0.12), bp(0.80, 0.20), bp(0.97, 0.30), bp(1.0, 0.42),
                  bp(0.96, 0.50), bp(0.03, 0.50)], 1.5)
    sole = poly([bp(-0.01, 0.46), bp(1.0, 0.46), bp(0.97, 0.58), bp(0.01, 0.58)], 0.8)
    studs = unary_union([poly([bp(u - 0.035, 0.56), bp(u + 0.035, 0.56), bp(u + 0.025, 0.66), bp(u - 0.025, 0.66)], 0.6)
                         for u in (0.10, 0.28, 0.62, 0.84)])
    solid(ic, studs, face="#5e5c64", depth=0, top=False, layer=f"{name}-studs")
    solid(ic, sole, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=1.5, side="#241f31", top=False, layer=f"{name}-sole")
    solid(ic, upper, face=[(0, collar[0]), (1, collar[1])], depth=2, side=collar[2], layer=f"{name}-boot")
    stripe = poly([bp(0.42, 0.16), bp(0.52, 0.14), bp(0.78, 0.44), bp(0.68, 0.46)], 0.5).intersection(upper)
    lace = unary_union([box(*bp(0.56 + 0.08 * k, 0.12 + 0.03 * k)[:1], 0, 0, 0) for k in range(0)])  # (no laces: too small)
    ic.path(geom_d(stripe), "#ffffff", opacity=0.9, layer_id=f"{name}-stripe")
    # far ear, then the head
    ear = ellipse(cx - d * r * 0.92, cy + 2, r * 0.17, r * 0.24)
    solid(ic, ear, face=[(0, s_mid), (1, s_dark)], depth=2, side=s_side, top=False, layer=f"{name}-ear")
    h = ellipse(cx, cy, r, r * 1.04)
    solid(ic, h, face=[(0, s_light), (0.55, s_mid), (1, s_dark)], depth=3, side=s_side, layer=f"{name}-head")
    # hair
    if hair_kind == "swept":
        top = h.intersection(box(0, 0, 128, cy - r * 0.32))
        quiff = ellipse(cx + d * r * 0.25, cy - r * 0.80, r * 0.78, r * 0.40)     # swept towards the opponent
        back = ellipse(cx - d * r * 0.55, cy - r * 0.40, r * 0.50, r * 0.55)
        hair = smooth(unary_union([top, quiff, back.intersection(h.buffer(1.5))]).intersection(ellipse(cx + d * 2, cy - 2, r * 1.10, r * 1.18)), 1.5)
        hair = hair.difference(box(0, cy + r * 0.05, 128, 128))
        solid(ic, hair, face=[(0, "#86603f"), (0.5, "#5e4034"), (1, "#3d2a22")], depth=1.5, side="#281a1a", top=False, layer=f"{name}-hair")
        crest = ellipse(cx + d * r * 0.2, cy - r * 0.62, r * 0.80, r * 0.50)
        streak = crest.difference(move(crest, d * 2.5, 3.5)).intersection(hair).intersection(
            box(cx - r * 0.7, 0, cx + r * 0.9, 128) if d > 0 else box(cx - r * 0.9, 0, cx + r * 0.7, 128))
        ic.path(geom_d(streak), ic.linear([(0, "#f9e27a"), (1, "#d9a83a")], 0, cy - r * 1.2, 0, cy - r * 0.6), layer_id=f"{name}-streak")
        toplight(ic, hair, layer=f"{name}-hair")
    else:  # buzz cut
        cap = smooth(h.intersection(box(0, 0, 128, cy - r * 0.42)).union(
            h.intersection(box(cx - d * r * 1.2, 0, cx - d * r * 0.55, cy + r * 0.05) if d > 0 else box(cx - d * r * 0.55, 0, cx - d * r * 1.2, cy + r * 0.05))), 1.0)
        ic.path(geom_d(cap), "#3d2a22", opacity=0.82, layer_id=f"{name}-buzz")
    # beard (left player only)
    if hair_kind == "swept":
        beard = smooth(h.intersection(ellipse(cx + d * 3, cy + r * 0.45, r * 0.98, r * 0.66)).difference(
            ellipse(cx + d * 5, cy + r * 0.10, r * 0.82, r * 0.50)), 1.0)
        ic.path(geom_d(beard), ic.linear([(0, "#5e4034"), (1, "#3d2a22")], 0, cy, 0, cy + r), layer_id=f"{name}-beard")
    # eyes (both shifted towards the other player), angry brows lowered towards the nose
    nose_x = cx + d * r * 0.42
    for k, ex in enumerate((cx + d * r * 0.12, cx + d * r * 0.66)):
        ey = cy - r * 0.10
        rx = r * (0.20 if k == 0 else 0.17)
        inner = ex + (d if ex < nose_x * d * d and d > 0 else -d) * 0  # placeholder (unused)
        to_nose = 1 if nose_x > ex else -1
        eye = ellipse(ex, ey, rx, r * 0.15)
        brow_line = poly([(ex - to_nose * rx * 1.4, ey - r * 0.30), (ex + to_nose * rx * 1.3, ey - r * 0.10),
                          (ex + to_nose * rx * 1.3, ey + r * 0.40), (ex - to_nose * rx * 1.4, ey + r * 0.40)])
        eye = eye.intersection(brow_line)
        ic.path(geom_d(eye), "#ffffff", layer_id=f"{name}-eye{k}")
        ic.path(geom_d(circ(ex + d * rx * 0.35, ey + 0.6, r * 0.085).intersection(eye)), "#26a269", layer_id=f"{name}-iris{k}")
        ic.path(geom_d(circ(ex + d * rx * 0.40, ey + 0.6, r * 0.045).intersection(eye)), "#241f31", layer_id=f"{name}-pupil{k}")
        brow = poly([(ex - to_nose * rx * 1.45, ey - r * 0.34), (ex + to_nose * rx * 1.35, ey - r * 0.14),
                     (ex + to_nose * rx * 1.35, ey - r * 0.04), (ex - to_nose * rx * 1.45, ey - r * 0.22)], 1.2)
        ic.path(geom_d(brow), "#3d2a22", layer_id=f"{name}-brow{k}")
    nose = ellipse(nose_x + d * r * 0.06, cy + r * 0.12, r * 0.13, r * 0.10)
    ic.path(geom_d(nose), s_dark, opacity=0.55, layer_id=f"{name}-nose")
    # gritted teeth with lips
    mx, my = cx + d * r * 0.40, cy + r * 0.42
    lips = rounded(box(mx - r * 0.42, my - r * 0.18, mx + r * 0.42, my + r * 0.18), r * 0.14)
    ic.path(geom_d(lips), "#8f3b2a", layer_id=f"{name}-lips")
    teeth = rounded(box(mx - r * 0.36, my - r * 0.12, mx + r * 0.36, my + r * 0.12), r * 0.08)
    ic.path(geom_d(teeth), ic.linear([(0, "#ffffff"), (1, "#deddda")], 0, my - r * 0.12, 0, my + r * 0.12), layer_id=f"{name}-teeth")
    gaps = unary_union([box(mx - r * 0.36 + i * r * 0.144 - 0.35, my - r * 0.12, mx - r * 0.36 + i * r * 0.144 + 0.35, my + r * 0.12)
                        for i in range(1, 5)] + [box(mx - r * 0.36, my - 0.35, mx + r * 0.36, my + 0.35)]).intersection(teeth)
    ic.path(geom_d(gaps), "#c0bfbc", layer_id=f"{name}-gaps")
    return h


def design():
    ic = gk.Icon("Kafa Topu 2 - Gnomed (two big heads face to face)")
    left_skin = ("#f4c19c", "#e39a6c", "#c0703f", "#8e4c25")
    right_skin = ("#d99a6a", "#b87445", "#8a5230", "#5e3519")
    r = 22.5
    head(ic, 31, 76, r, +1, left_skin, "swept", ("#ed333b", "#c01c28", "#7a1520"), "left")
    head(ic, 97, 77, r, -1, right_skin, "buzz", ("#62a0ea", "#1c71d8", "#1a5fb4"), "right")
    # the ball above, between them (the header)
    bx, by, br = 64, 26, 20
    ball = circ(bx, by, br)
    solid(ic, ball, face=[(0, "#ffffff"), (0.6, "#f6f5f4"), (1, "#c0bfbc")], depth=3, side="#9a9996", layer="ball")
    pats = [regular(bx, by, br * 0.34, 5)]
    for k in range(5):
        a = np.radians(-90 + k * 72)
        pats.append(regular(bx + np.cos(a) * br * 0.96, by + np.sin(a) * br * 0.96, br * 0.30, 5, rot=90 + k * 72))
    ic.path(geom_d(unary_union(pats).intersection(ball)), "#3d3846", layer_id="ball-patches")
    ic.path(geom_d(circ(bx - 7, by - 8, 7).intersection(ball)), ic.radial([(0, "#ffffff", 0.9), (1, "#ffffff", 0)], bx - 7, by - 8, 7), layer_id="ball-glint")
    # VS between the heads
    v = poly([(51, 52), (57, 52), (60.5, 63), (64, 52), (70, 52), (63.5, 70), (57.5, 70)], 1.2)
    s_ = unary_union([rounded(box(70, 52, 81, 56.5), 2), rounded(box(70, 52, 74.5, 62.5), 2), rounded(box(70, 59, 81, 63.5), 2),
                      rounded(box(76.5, 59, 81, 70), 2), rounded(box(70, 65.5, 81, 70), 2)])
    vs = move(unary_union([v, s_]), -2, 4)
    solid(ic, vs, face=[(0, "#f9f06b"), (0.5, "#f6d32d"), (1, "#f5c211")], depth=3, side="#c64600", layer="vs")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
