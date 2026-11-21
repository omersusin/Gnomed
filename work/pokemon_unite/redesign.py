#!/usr/bin/env python3
"""pokemon_unite - Gnomed redesign: an ORIGINAL logo inspired by the game (REDESIGN.md 3b).
The poster's composition is kept (owner: "üç karakter var, karşı bakıyorlar"): THREE
heroes side by side, all facing left (towards the opponent): an orange dragon (back
left), a white rabbit with tall ears (back right) and the yellow electric hero in front.
Simplified original shapes, not traced. Colours measured from the poster: yellow
#efe60a, red #f01647, orange #ca6950 / #edc13f, cream #ede3db, purple #7a2da9."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
D = -1                      # everybody looks left


def smooth(g, r=1.2):
    return g.buffer(r).buffer(-r).buffer(-r * 0.5).buffer(r * 0.5)


def eye(ic, x, y, rx, ry, iris, name, angry=True):
    e = ellipse(x, y, rx, ry)
    if angry:   # lid cut: lower towards the front (left)
        e = e.intersection(poly([(x - rx * 1.5, y - ry * 0.35), (x + rx * 1.5, y - ry * 1.2), (x + rx * 1.5, y + ry * 2), (x - rx * 1.5, y + ry * 2)]))
    ic.path(geom_d(e), "#ffffff", layer_id=f"{name}-eye")
    ic.path(geom_d(circ(x + D * rx * 0.35, y + ry * 0.15, ry * 0.62).intersection(e)), iris, layer_id=f"{name}-iris")
    ic.path(geom_d(circ(x + D * rx * 0.42, y + ry * 0.15, ry * 0.32).intersection(e)), "#241f31", layer_id=f"{name}-pupil")
    ic.path(geom_d(circ(x + D * rx * 0.15, y - ry * 0.25, ry * 0.18).intersection(e)), "#ffffff", layer_id=f"{name}-glint")


def dragon(ic):
    cx, cy, r = 32, 52, 21
    horns = unary_union([poly([(cx + 8, cy - 14), (cx + 24, cy - 34), (cx + 16, cy - 10)], 2),
                         poly([(cx + 14, cy - 8), (cx + 32, cy - 22), (cx + 20, cy - 2)], 2)])
    solid(ic, horns, face=[(0, "#fff1c8"), (1, "#f9dc9a")], depth=2, side="#c88800", top=False, layer="dragon-horns")
    skull = ellipse(cx + 4, cy, r, r * 0.86)
    snout = ellipse(cx - 12, cy + 7, r * 0.78, r * 0.48)
    head = smooth(unary_union([skull, snout]), 2)
    solid(ic, head, face=[(0, "#ffbe6f"), (0.5, "#ffa348"), (1, "#e66100")], depth=3, side="#c64600", layer="dragon")
    jaw = head.intersection(ellipse(cx - 6, cy + 18, r * 1.05, r * 0.42))
    ic.path(geom_d(jaw), ic.linear([(0, "#fff1c8"), (1, "#f9dc9a")], 0, cy + 8, 0, cy + 26), layer_id="dragon-jaw")
    eye(ic, cx - 2, cy - 3, 5.2, 4.2, "#62a0ea", "dragon")
    ic.path(geom_d(poly([(cx - 8, cy - 9), (cx + 5, cy - 12), (cx + 5, cy - 9.5), (cx - 8, cy - 7)], 1)), "#a5401b", layer_id="dragon-brow")
    ic.path(geom_d(circ(cx - 24, cy + 3, 1.2)), "#a5401b", layer_id="dragon-nostril")


def rabbit(ic):
    cx, cy, r = 98, 50, 20
    ears = unary_union([poly([(cx + 2, cy - 12), (cx + 14, cy - 46), (cx + 20, cy - 44), (cx + 12, cy - 8)], 4),
                        poly([(cx + 10, cy - 8), (cx + 28, cy - 36), (cx + 32, cy - 32), (cx + 18, cy - 2)], 4)])
    solid(ic, ears, face=[(0, "#ffffff"), (1, "#deddda")], depth=2, side="#9a9996", top=False, layer="rabbit-ears")
    inner = unary_union([poly([(cx + 7, cy - 18), (cx + 15, cy - 40), (cx + 16, cy - 20)], 2),
                         poly([(cx + 15, cy - 10), (cx + 26, cy - 31), (cx + 21, cy - 12)], 2)])
    ic.path(geom_d(inner), "#ff7800", layer_id="rabbit-ear-inner")
    head = smooth(unary_union([ellipse(cx, cy, r, r * 0.92), ellipse(cx - 10, cy + 6, r * 0.62, r * 0.46)]), 2)
    solid(ic, head, face=[(0, "#ffffff"), (0.6, "#f6f5f4"), (1, "#c0bfbc")], depth=3, side="#9a9996", layer="rabbit")
    tuft = poly([(cx - 14, cy - 12), (cx - 2, cy - 22), (cx + 8, cy - 18), (cx + 2, cy - 10), (cx - 8, cy - 6)], 3).intersection(head.buffer(2))
    ic.path(geom_d(tuft), ic.linear([(0, "#ffa348"), (1, "#e01b24")], 0, cy - 22, 0, cy - 6), layer_id="rabbit-tuft")
    eye(ic, cx - 6, cy - 1, 4.8, 4.0, "#e01b24", "rabbit")
    ic.path(geom_d(ellipse(cx - 21, cy + 5, 2.4, 1.8)), "#ff7800", layer_id="rabbit-nose")


def electric(ic):
    cx, cy, r = 62, 82, 25
    ears = unary_union([poly([(cx - 4, cy - r * 0.75), (cx - 22, cy - r * 2.05), (cx - 12, cy - r * 0.62)], 3),
                        poly([(cx + 10, cy - r * 0.78), (cx + 20, cy - r * 2.0), (cx + 22, cy - r * 0.6)], 3)])
    tips = unary_union([poly([(cx - 17, cy - r * 1.62), (cx - 22, cy - r * 2.05), (cx - 13, cy - r * 1.72)], 1),
                        poly([(cx + 18, cy - r * 1.62), (cx + 20, cy - r * 2.0), (cx + 22.5, cy - r * 1.55)], 1)])
    face = smooth(unary_union([ellipse(cx, cy, r * 1.04, r * 0.92), ears]), 1.5)
    solid(ic, face, face=[(0, "#f9f06b"), (0.5, "#f6e10a"), (1, "#e5a50a")], depth=4, side="#c88800", layer="electric")
    ic.path(geom_d(tips.intersection(face)), "#3d3846", layer_id="electric-tips")
    for k, (ex, rx) in enumerate(((cx - 13, 5.2), (cx + 8, 4.6))):
        e = ellipse(ex, cy - 4, rx, rx * 1.05)
        ic.path(geom_d(e), "#241f31", layer_id=f"electric-eye{k}")
        ic.path(geom_d(circ(ex - rx * 0.35, cy - 6, rx * 0.36)), "#ffffff", layer_id=f"electric-glint{k}")
    for k, (chx, chr_) in enumerate(((cx - 23, 6.4), (cx + 17, 5.2))):
        ch = circ(chx, cy + 8, chr_).intersection(face)
        ic.path(geom_d(ch), ic.linear([(0, "#f66151"), (1, "#e01b24")], 0, cy + 2, 0, cy + 14), layer_id=f"electric-cheek{k}")
    ic.path(geom_d(poly([(cx - 4.5, cy + 2), (cx - 1.5, cy + 2), (cx - 3, cy + 3.6)])), "#3d3846", layer_id="electric-nose")
    m = unary_union([circ(cx - 6, cy + 8.5, 3.0).difference(circ(cx - 6, cy + 7.2, 2.9)),
                     circ(cx - 0.5, cy + 8.5, 3.0).difference(circ(cx - 0.5, cy + 7.2, 2.9))])
    ic.path(geom_d(m), "#3d3846", layer_id="electric-mouth")


def design():
    ic = gk.Icon("Pokemon UNITE - Gnomed (three heroes)")
    dragon(ic)
    rabbit(ic)
    electric(ic)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"faithful": design()})
