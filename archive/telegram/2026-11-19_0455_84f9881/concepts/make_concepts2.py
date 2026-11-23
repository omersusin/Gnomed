"""Round 2 concepts D/E/F for Telegram (round 1 A/B/C rejected: 'Hiçbiri, yeniden dene').
Plane points measured from work/telegram/geometry.json; blue #31a5df measured."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_concepts import plane_parts  # noqa: E402

OUT = Path(__file__).resolve().parent
BLUE = [(0, "#99c1f1"), (0.5, "#62a0ea"), (1, "#3584e4")]


def white_plane(ic, s, dx, dy, d=3):
    tw, bd, fl = plane_parts(s, dx, dy)
    solid(ic, fl, face=[(0, "#c0bfbc"), (1, "#9a9996")], depth=d - 1, layer="flap")
    solid(ic, bd, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=d, layer="body")
    solid(ic, tw, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=d, layer="wing")


def D():
    ic = gk.Icon("telegram concept D - plane flying through a thick blue ring")
    ring = ellipse(56, 62, 44, 44).difference(ellipse(56, 62, 30, 30))
    back = ring.intersection(box(0, 0, 128, 62))
    front = ring.intersection(box(0, 62, 128, 128))
    solid(ic, back, face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=8, layer="ring-back")
    white_plane(ic, 1.15, -2, -6)
    solid(ic, front, face=BLUE, depth=8, layer="ring-front")
    return ic


def E():
    ic = gk.Icon("telegram concept E - blue cloud, white plane flying out in front")
    c = unary_union([circ(40, 62, 22), circ(64, 46, 30), circ(90, 60, 22), rounded(box(18, 60, 112, 86), 13)])
    solid(ic, c, face=[(0, "#99c1f1"), (0.6, "#62a0ea"), (1, "#3584e4")], depth=6, layer="cloud")
    ic.path(geom_d(circ(56, 36, 16).intersection(c)), ic.radial([(0, "#ffffff", 0.6), (1, "#ffffff", 0)], 56, 36, 16), layer_id="cloud-glow")
    white_plane(ic, 0.95, 26, 22)
    return ic


def F():
    ic = gk.Icon("telegram concept F - blue envelope, the paper plane is its stamp")
    env = rounded(box(12, 30, 116, 104), 7)
    solid(ic, env, face=[(0, "#62a0ea"), (1, "#3584e4")], depth=6, layer="envelope")
    flap = poly([(14, 32), (114, 32), (64, 74)], 3)
    solid(ic, flap, face=[(0, "#99c1f1"), (1, "#62a0ea")], depth=2, layer="flap")
    stamp = rounded(box(70, 62, 108, 96), 3)
    solid(ic, stamp, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=2, layer="stamp")
    tw, bd, fl = plane_parts(0.42, 64, 51)
    for g, c in ((fl, "#1a5fb4"), (bd, "#3584e4"), (tw, "#62a0ea")):
        ic.path(geom_d(g), c, layer_id="stamp-print")
    return ic


for name, fn in (("D", D), ("E", E), ("F", F)):
    fn().save(OUT / f"{name}.svg")
    print("wrote", name)
