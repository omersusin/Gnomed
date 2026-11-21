"""Pokémon UNITE - shared parts for the concepts and the redesign (REDESIGN.md 3b).

Reference: the store icon (source.png) - three heroes charging LEFT in a staggered row
(an orange dragon at the back-left, the yellow electric mouse in the middle-front, a white
rabbit striker with an orange brow at the right), purple sky behind, orange floor.
The game: two teams (purple / orange) score by carrying energy to the rival goal zones.
Serious, not a toy: real thickness, light from the top, small eyes, no outlines.
All heads face LEFT (as in the store icon).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_lib"))
from obj import *  # noqa: F401,F403,E402

YELLOW = ("#f9f06b", "#f6d32d", "#f5c211", "#e5a50a")
ORANGE = ("#ffbe6f", "#ffa348", "#ff7800", "#c64600")
WHITE = ("#ffffff", "#f6f5f4", "#deddda", "#9a9996")
PURPLE = ("#dc8add", "#c061cb", "#9141ac", "#613583")
TEAM_O = ("#ffbe6f", "#ff7800", "#e66100", "#c64600")


def _eye(ic, ex, ey, w, h, iris, name):
    e = ellipse(ex, ey, w, h)
    ic.path(geom_d(e), "#241f31", layer_id=f"{name}-eye")
    if iris:
        ic.path(geom_d(ellipse(ex - w * 0.15, ey + h * 0.15, w * 0.6, h * 0.6).intersection(e)), iris, layer_id=f"{name}-iris")
    ic.path(geom_d(circ(ex - w * 0.25, ey - h * 0.4, max(0.9, w * 0.35))), "#ffffff", layer_id=f"{name}-glint")


# ------------------------------------------------------------------ yellow electric mouse
def mouse(ic, cx, cy, r, name="mouse", body=False):
    """Head (3/4 view, facing left) with two long ears (dark tips), red cheek, small eye."""
    lt, mid, sh, side = YELLOW
    if body:
        b = poly([(cx - r * 0.75, cy + r * 0.55), (cx + r * 0.80, cy + r * 0.55), (cx + r * 0.95, cy + r * 1.75),
                  (cx - r * 0.85, cy + r * 1.75)], r * 0.35)
        solid(ic, b, face=[(0, mid), (1, sh)], depth=3, side=side, layer=f"{name}-body")
        arm = poly([(cx - r * 0.55, cy + r * 0.85), (cx - r * 1.15, cy + r * 0.95), (cx - r * 1.15, cy + r * 1.20),
                    (cx - r * 0.45, cy + r * 1.20)], r * 0.14)
        solid(ic, arm, face=[(0, lt), (1, mid)], depth=2, side=side, layer=f"{name}-arm")
    ears = []
    for k, (bx, tip) in enumerate((((cx + r * 0.55), (cx + r * 1.45, cy - r * 2.15)),
                                   ((cx - r * 0.10), (cx + r * 0.25, cy - r * 2.45)))):
        ear = poly([(bx - r * 0.34, cy - r * 0.55), tip, (bx + r * 0.36, cy - r * 0.45)], r * 0.10)
        ears.append(ear)
        solid(ic, ear, face=[(0, lt), (1, mid)] if k else [(0, mid), (1, sh)], depth=2, side=side, layer=f"{name}-ear{k}")
        tipg = ear.intersection(circ(*tip, r * 0.62))
        ic.path(geom_d(tipg), ic.linear([(0, "#3d3846"), (1, "#241f31")], 0, tip[1], 0, tip[1] + r * 0.6), layer_id=f"{name}-tip{k}")
    head = unary_union([ellipse(cx, cy, r, r * 0.88), ellipse(cx - r * 0.12, cy + r * 0.30, r * 0.92, r * 0.62)])
    solid(ic, head, face=[(0, lt), (0.5, mid), (1, sh)], depth=2.5, side=side, layer=f"{name}-head")
    _eye(ic, cx - r * 0.52, cy - r * 0.08, r * 0.12, r * 0.17, None, name)
    cheek = circ(cx + r * 0.18, cy + r * 0.12, r * 0.30)
    ic.path(geom_d(cheek), ic.linear([(0, "#ed333b"), (1, "#c01c28")], 0, cy - r * 0.2, 0, cy + r * 0.45), layer_id=f"{name}-cheek")
    mouth = poly([(cx - r * 0.86, cy + r * 0.36), (cx - r * 0.50, cy + r * 0.40), (cx - r * 0.64, cy + r * 0.62)], r * 0.06)
    ic.path(geom_d(mouth), "#a51d2d", layer_id=f"{name}-mouth")
    ic.path(geom_d(circ(cx - r * 0.64, cy + r * 0.54, r * 0.07).intersection(mouth)), "#f66151", layer_id=f"{name}-tongue")
    return head


# ------------------------------------------------------------------ white rabbit striker
def rabbit(ic, cx, cy, r, name="rabbit"):
    """White head facing left, a long ear swept back, orange brow band, red-ringed eye."""
    lt, mid, sh, side = WHITE
    ear = poly([(cx + r * 0.05, cy - r * 0.60), (cx + r * 0.55, cy - r * 2.05), (cx + r * 0.95, cy - r * 2.0),
                (cx + r * 0.75, cy - r * 0.45)], r * 0.30)
    solid(ic, ear, face=[(0, lt), (1, sh)], depth=2, side=side, layer=f"{name}-ear")
    inner = poly([(cx + r * 0.30, cy - r * 0.75), (cx + r * 0.62, cy - r * 1.80), (cx + r * 0.72, cy - r * 0.70)], r * 0.12)
    ic.path(geom_d(inner.intersection(ear)), ic.linear([(0, ORANGE[1]), (1, ORANGE[2])], 0, cy - r * 1.8, 0, cy - r * 0.7), layer_id=f"{name}-inner")
    head = unary_union([ellipse(cx, cy, r * 0.92, r * 0.85),
                        poly([(cx - r * 0.55, cy - r * 0.10), (cx - r * 1.15, cy + r * 0.35), (cx - r * 0.45, cy + r * 0.70)], r * 0.2)])
    solid(ic, head, face=[(0, lt), (0.6, mid), (1, sh)], depth=2.5, side=side, layer=f"{name}-head")
    brow = head.intersection(poly([(cx - r * 1.2, cy - r * 0.10), (cx - r * 0.2, cy - r * 1.0), (cx + r * 0.4, cy - r * 1.0),
                                   (cx - r * 0.1, cy - r * 0.35), (cx - r * 1.2, cy + r * 0.12)]))
    ic.path(geom_d(brow), ic.linear([(0, ORANGE[1]), (1, ORANGE[3])], 0, cy - r, 0, cy), layer_id=f"{name}-brow")
    ring = ellipse(cx - r * 0.40, cy + r * 0.05, r * 0.24, r * 0.28)
    ic.path(geom_d(ring), "#e01b24", layer_id=f"{name}-ring")
    _eye(ic, cx - r * 0.42, cy + r * 0.07, r * 0.12, r * 0.17, "#1c71d8", name)
    mouth = poly([(cx - r * 1.0, cy + r * 0.40), (cx - r * 0.55, cy + r * 0.45), (cx - r * 0.70, cy + r * 0.68)], r * 0.05)
    ic.path(geom_d(mouth), "#a51d2d", layer_id=f"{name}-mouth")
    return head


# ------------------------------------------------------------------ orange dragon
def dragon(ic, cx, cy, r, name="dragon"):
    """Orange head facing left: long snout, a horn swept back, small teal eye, a fang,
    cream lower jaw."""
    lt, mid, sh, side = ORANGE
    horn = poly([(cx + r * 0.30, cy - r * 0.55), (cx + r * 1.30, cy - r * 1.10), (cx + r * 0.75, cy - r * 0.20)], r * 0.12)
    solid(ic, horn, face=[(0, lt), (1, mid)], depth=2, side=side, layer=f"{name}-horn")
    head = unary_union([ellipse(cx + r * 0.10, cy - r * 0.05, r * 0.80, r * 0.70),
                        poly([(cx - r * 0.20, cy - r * 0.45), (cx - r * 1.35, cy - r * 0.05), (cx - r * 1.40, cy + r * 0.45),
                              (cx - r * 0.10, cy + r * 0.55)], r * 0.28)])
    solid(ic, head, face=[(0, lt), (0.5, mid), (1, sh)], depth=2.5, side=side, layer=f"{name}-head")
    jaw = head.intersection(box(0, cy + r * 0.28, 128, 128))
    ic.path(geom_d(jaw), ic.linear([(0, "#f6f5f4"), (1, "#deddda")], 0, cy + r * 0.28, 0, cy + r * 0.6), layer_id=f"{name}-jaw")
    fang = poly([(cx - r * 1.05, cy + r * 0.26), (cx - r * 0.80, cy + r * 0.26), (cx - r * 0.93, cy + r * 0.50)], r * 0.03)
    ic.path(geom_d(fang), "#ffffff", layer_id=f"{name}-fang")
    _eye(ic, cx - r * 0.05, cy - r * 0.22, r * 0.14, r * 0.16, "#2ec27e", name)
    ic.path(geom_d(circ(cx - r * 1.15, cy + r * 0.02, r * 0.05)), "#c64600", layer_id=f"{name}-nostril")
    return head


# ------------------------------------------------------------------ the goal + energy
GOLD = ("#f9f06b", "#f6d32d", "#f5c211", "#c64600")


def goal(ic, cx, base_y, r, h, team=GOLD, name="goal"):
    """The team goal: a thick ring on a pillar standing on a round pad. Ring centre = hole."""
    lt, mid, sh, side = team
    pad = ellipse(cx, base_y - r * 0.30, r * 1.25, r * 0.30)
    solid(ic, pad, face=[(0, "#deddda"), (1, "#c0bfbc")], depth=4, side="#9a9996", top=False, layer=f"{name}-pad")
    ring_cy = base_y - h
    pillar = box(cx - r * 0.18, ring_cy + r * 0.6, cx + r * 0.18, base_y - r * 0.30)
    ic.path(geom_d(pillar), ic.linear([(0, "#9a9996"), (0.45, "#f6f5f4"), (1, "#9a9996")], cx - r * 0.18, 0, cx + r * 0.18, 0), layer_id=f"{name}-pillar")
    ring = circ(cx, ring_cy, r).difference(circ(cx, ring_cy, r * 0.62))
    solid(ic, ring, face=[(0, lt), (0.5, mid), (1, sh)], depth=4, side=side, layer=f"{name}-ring")
    inner = circ(cx, ring_cy, r * 0.62).difference(circ(cx, ring_cy - r * 0.10, r * 0.58)).difference(circ(cx, ring_cy, r * 0.5))
    ic.path(geom_d(inner), ic.linear([(0, "#1a5fb4"), (1, "#3584e4")], 0, ring_cy - r * 0.6, 0, ring_cy + r * 0.6), layer_id=f"{name}-inner")
    return ring, circ(cx, ring_cy, r * 0.62)


def orb(ic, cx, cy, r, name="orb"):
    """Glowing energy: a glass sphere, deep centre, soft highlight."""
    o = circ(cx, cy, r)
    ic.path(geom_d(o), ic.radial([(0, "#f9f06b"), (0.55, "#f6d32d"), (1, "#e5a50a")], cx, cy + r * 0.2, r), layer_id=f"{name}-face")
    ic.path(geom_d(ellipse(cx - r * 0.3, cy - r * 0.4, r * 0.38, r * 0.22)), "#ffffff", opacity=0.8, layer_id=f"{name}-hl")
    return o


def arena(ic, cx, cy, rx, ry, depth=6, name="arena"):
    """Round arena platform: purple half / orange half, with thickness."""
    a = ellipse(cx, cy, rx, ry)
    solid(ic, a.intersection(box(0, 0, cx, 128)), face=[(0, PURPLE[1]), (1, PURPLE[2])], depth=depth, side=PURPLE[3], top=False, layer=f"{name}-p")
    solid(ic, a.intersection(box(cx, 0, 128, 128)), face=[(0, TEAM_O[1]), (1, TEAM_O[2])], depth=depth, side=TEAM_O[3], top=False, layer=f"{name}-o")
    toplight(ic, a, layer=name)
    return a
