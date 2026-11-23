"""Rough concepts A/B/C for Telegram (REDESIGN.md step 3). Plane points measured from
work/telegram/geometry.json (holes part, simplified 2 u); blue #31a5df measured."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

OUT = Path(__file__).resolve().parent
# measured plane (source 0..128 coords)
TOPW = [(25.9, 66.1), (90.9, 39.1), (75.7, 52.4), (43.8, 72.2), (28.7, 69.3)]
BODY = [(90.9, 39.1), (92.1, 47.4), (85.4, 89.3), (79.9, 95.0), (54.9, 77.2), (75.7, 52.4)]
FLAP = [(43.8, 72.2), (56.5, 77.0), (50.0, 89.0)]          # fold under the wing (the notch)


def plane_parts(s, dx, dy):
    f = lambda pts: [(x * s + dx, y * s + dy) for x, y in pts]  # noqa: E731
    return poly(f(TOPW), 1.2), poly(f(BODY), 1.2), poly(f(FLAP), 1.0)


def A():
    ic = gk.Icon("telegram concept A - the paper plane as a folded blue paper object")
    tw, bd, fl = plane_parts(1.55, -32, -38)
    solid(ic, fl, face=[(0, "#1c71d8"), (1, "#1a5fb4")], depth=2, layer="flap")
    solid(ic, bd, face=[(0, "#62a0ea"), (1, "#3584e4")], depth=3, layer="body")
    solid(ic, tw, face=[(0, "#99c1f1"), (1, "#62a0ea")], depth=3, layer="wing")
    return ic


def B():
    ic = gk.Icon("telegram concept B - a blue message bubble carrying the plane")
    bub = unary_union([rounded(box(14, 16, 114, 96), 26), poly([(26, 84), (44, 92), (18, 112)], 2)])
    solid(ic, bub, face=[(0, "#62a0ea"), (1, "#3584e4")], depth=8, layer="bubble")
    tw, bd, fl = plane_parts(0.95, 2, -6)
    solid(ic, fl, face=[(0, "#c0bfbc"), (1, "#9a9996")], depth=1.5, layer="flap")
    solid(ic, bd, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=2, layer="body")
    solid(ic, tw, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=2, layer="wing")
    return ic


def C():
    ic = gk.Icon("telegram concept C - blue glass sphere, white paper plane flying out of it")
    orb = circ(50, 60, 40)
    solid(ic, orb, face=[(0, "#99c1f1"), (0.5, "#62a0ea"), (1, "#1c71d8")], depth=2, layer="orb")
    ic.path(geom_d(circ(40, 44, 14).intersection(orb)), ic.radial([(0, "#ffffff", 0.7), (1, "#ffffff", 0)], 40, 44, 14), layer_id="orb-glint")
    tw, bd, fl = plane_parts(1.05, 18, 8)
    solid(ic, fl, face=[(0, "#c0bfbc"), (1, "#9a9996")], depth=2, layer="flap")
    solid(ic, bd, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=3, layer="body")
    solid(ic, tw, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=3, layer="wing")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT.parent / "concepts-round1" / f"{name}.svg")
        print("wrote", name)
