"""Pokémon UNITE - the game's OBJECTS (REDESIGN.md 3b, owner 2026-11-21: "Karakter yok,
oyunun nesnesi"). No characters, faces or animals.

References (refs/, the owner's screenshots): the key art shows the GOAL RING - a thick gold
torus with a blue inner face - and a glowing yellow energy ball; the UNITE logo ends in two
team balls (orange left, purple right: a coloured top half, white bottom, dark band, white
button); the arena screenshot shows round score zones, purple team left / orange team right.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_lib"))
from obj import *  # noqa: F401,F403,E402

GOLD = ("#f9f06b", "#f6d32d", "#f5c211", "#e5a50a", "#c64600")
PURPLE = ("#dc8add", "#c061cb", "#9141ac", "#613583")
ORANGE = ("#ffbe6f", "#ffa348", "#ff7800", "#c64600")


def ring(ic, cx, cy, rx, ry, w, depth=5, name="ring", inner=True):
    """The gold goal ring seen at an angle: a torus (outer ellipse minus the hole), the far
    inner wall blue (seen through the top of the hole), the hole itself transparent."""
    outer = ellipse(cx, cy, rx, ry)
    hole_ = ellipse(cx, cy, rx - w, ry - w * 0.8)
    band = outer.difference(hole_)
    solid(ic, band, face=[(0, GOLD[0]), (0.35, GOLD[1]), (0.75, GOLD[3]), (1, GOLD[4])], depth=depth, side=GOLD[4], layer=f"{name}-gold")
    # the inner wall: the far (upper) part of the hole shows the ring's blue inside
    wall = hole_.difference(move(hole_, 0, w * 0.55))
    if inner:
        ic.path(geom_d(wall), ic.linear([(0, "#1a5fb4"), (1, "#3584e4")], 0, cy - ry, 0, cy - ry + w * 1.6), layer_id=f"{name}-inner")
    # metal sheen on the gold: a soft band along the upper left
    sheen = ellipse(cx - rx * 0.05, cy - ry * 0.05, rx - w * 0.35, ry - w * 0.3).difference(
        ellipse(cx + rx * 0.06, cy + ry * 0.06, rx - w * 0.35, ry - w * 0.3)).intersection(band)
    ic.path(geom_d(sheen), "#ffffff", opacity=0.45, layer_id=f"{name}-sheen")
    return band, hole_


def energy(ic, cx, cy, r, name="energy"):
    """The glowing energy ball: a glass sphere, hot centre, a swirl band, a highlight."""
    o = circ(cx, cy, r)
    solid(ic, o, face="#e5a50a", depth=1.5, side="#c64600", top=False, layer=f"{name}-body")
    ic.path(geom_d(o), ic.radial([(0, "#ffffff"), (0.35, "#f9f06b"), (0.75, "#f6d32d"), (1, "#ff7800")], cx - r * 0.1, cy - r * 0.1, r), layer_id=f"{name}-glow")
    swirl = ellipse(cx, cy + r * 0.05, r * 0.95, r * 0.32).difference(ellipse(cx, cy - r * 0.02, r * 0.85, r * 0.24)).intersection(o)
    ic.path(geom_d(swirl), "#ffffff", opacity=0.55, layer_id=f"{name}-swirl")
    ic.path(geom_d(ellipse(cx - r * 0.35, cy - r * 0.45, r * 0.30, r * 0.18)), "#ffffff", opacity=0.9, layer_id=f"{name}-hl")
    return o


def team_ball(ic, cx, cy, r, team, name="ball"):
    """A team ball (from the UNITE logo): coloured top half, white bottom, dark band, button."""
    o = circ(cx, cy, r)
    solid(ic, o, face="#c0bfbc", depth=2.5, side="#77767b", top=False, layer=f"{name}-shell")
    bottom = o.intersection(box(0, cy, 128, 128))
    ic.path(geom_d(bottom), ic.linear([(0, "#ffffff"), (1, "#c0bfbc")], 0, cy, 0, cy + r), layer_id=f"{name}-white")
    top = o.intersection(box(0, 0, 128, cy))
    ic.path(geom_d(top), ic.linear([(0, team[0]), (0.5, team[1]), (1, team[3])], 0, cy - r, 0, cy), layer_id=f"{name}-top")
    band = o.intersection(box(0, cy - r * 0.08, 128, cy + r * 0.08))
    ic.path(geom_d(band), "#3d3846", layer_id=f"{name}-band")
    btn_o = circ(cx, cy, r * 0.30)
    ic.path(geom_d(btn_o), "#3d3846", layer_id=f"{name}-btnrim")
    btn = circ(cx, cy, r * 0.20)
    ic.path(geom_d(btn), ic.linear([(0, "#ffffff"), (1, "#deddda")], 0, cy - r * 0.2, 0, cy + r * 0.2), layer_id=f"{name}-btn")
    ic.path(geom_d(ellipse(cx - r * 0.42, cy - r * 0.55, r * 0.28, r * 0.16)), "#ffffff", opacity=0.6, layer_id=f"{name}-hl")
    toplight(ic, o, layer=name)
    return o


def stand(ic, cx, top_y, base_y, w, name="stand"):
    """Metal goal post on a round pad (the stadium goal)."""
    pad = ellipse(cx, base_y - 6, w * 1.6, 6)
    solid(ic, pad, face=[(0, "#deddda"), (1, "#c0bfbc")], depth=4, side="#9a9996", top=False, layer=f"{name}-pad")
    post = box(cx - w / 2, top_y, cx + w / 2, base_y - 6)
    ic.path(geom_d(post), ic.linear([(0, "#9a9996"), (0.45, "#f6f5f4"), (1, "#77767b")], cx - w / 2, 0, cx + w / 2, 0), layer_id=f"{name}-post")
    return post


def arena(ic, cx, cy, rx, ry, depth=6, name="arena"):
    """Round arena: purple half / orange half, with thickness."""
    a = ellipse(cx, cy, rx, ry)
    solid(ic, a.intersection(box(0, 0, cx, 128)), face=[(0, PURPLE[1]), (1, PURPLE[2])], depth=depth, side=PURPLE[3], top=False, layer=f"{name}-p")
    solid(ic, a.intersection(box(cx, 0, 128, 128)), face=[(0, ORANGE[1]), (1, ORANGE[2])], depth=depth, side=ORANGE[3], top=False, layer=f"{name}-o")
    toplight(ic, a, layer=name)
    return a
