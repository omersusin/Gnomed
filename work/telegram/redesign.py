#!/usr/bin/env python3
"""telegram - Gnomed redesign.

Approved (design.md): "Select one and make others alt" - the owner let me choose:
  (owner, after the review: "Defaultu o mektup yap" -> faithful = F, symbol = E)
  symbol   = E  a blue volumetric cloud (Telegram is a cloud messenger) with the white
                paper plane flying out of it, in front, lower right (secondary object)
  disc     = D  the blue circle as a thick enamel ring, the paper plane flying through it
  faithful = F  a blue envelope (like GNOME Mail) whose stamp carries the paper plane
Anchors kept: the paper plane (points measured from work/telegram/geometry.json, the
"holes" part), Telegram blue #31a5df -> HIG Blue ramp (#99c1f1 / #62a0ea / #3584e4 /
#1c71d8 / #1a5fb4), the round shape (cloud lobes / ring).

Build:  python3 tools/make_icon.py telegram      (runs this file, then review + gate)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name

# paper plane, measured (source 0..128 coords, simplified 2 u): upper wing, body/keel, the
# fold under the wing (the notch in the source)
TOPW = [(25.9, 66.1), (90.9, 39.1), (75.7, 52.4), (43.8, 72.2), (28.7, 69.3)]
BODY = [(90.9, 39.1), (92.1, 47.4), (85.4, 89.3), (79.9, 95.0), (54.9, 77.2), (75.7, 52.4)]
FLAP = [(43.8, 72.2), (56.5, 77.0), (50.0, 89.0)]

BLUE_FACE = [(0, "#99c1f1"), (0.45, "#62a0ea"), (1, "#3584e4")]


def plane(s, dx, dy):
    f = lambda pts: [(x * s + dx, y * s + dy) for x, y in pts]  # noqa: E731
    return poly(f(TOPW), 1.2), poly(f(BODY), 1.2), poly(f(FLAP), 1.0)


def paper_plane(ic, s, dx, dy, depth=3, layer="plane"):
    """White folded paper: wing lightest, body a step darker, the fold under the wing grey."""
    tw, bd, fl = plane(s, dx, dy)
    solid(ic, fl, face=[(0, "#c0bfbc"), (1, "#9a9996")], depth=max(1.5, depth - 1), top=False, layer=f"{layer}-fold")
    solid(ic, bd, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=depth, side="#c0bfbc", layer=f"{layer}-body")
    solid(ic, tw, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=depth, side="#deddda", layer=f"{layer}-wing")
    return unary_union([tw, bd, fl])


def cloud_shape():
    return unary_union([circ(38, 60, 21), circ(62, 44, 29), circ(89, 56, 22),
                        rounded(box(17, 56, 111, 86), 14)])


def design_cloud():
    """E: cloud + paper plane flying out of it (Weather-like cloud, glossy enamel blue)."""
    ic = gk.Icon("Telegram - Gnomed (cloud + paper plane)")
    c = cloud_shape()
    solid(ic, c, face=BLUE_FACE, depth=6, side="#1c71d8", top=False, layer="cloud")
    glow = circ(56, 34, 20).intersection(c)                   # soft top light on the big lobe
    ic.path(geom_d(glow), ic.radial([(0, "#ffffff", 0.75), (1, "#ffffff", 0)], 56, 34, 20), layer_id="cloud-glow")
    toplight(ic, c, width=1.5, opacity=0.6, layer="cloud")
    # the plane: secondary object in front, lower right, breaking out of the cloud's outline
    paper_plane(ic, 1.0, 26, 20, depth=3)
    return ic


def design_ring():
    """D: thick blue enamel ring (the circle), the plane flies through it."""
    ic = gk.Icon("Telegram - Gnomed (ring + paper plane)")
    cx, cy = 60, 60
    outer, inner = circ(cx, cy, 48), circ(cx, cy, 32)
    ring = outer.difference(inner)
    back = ring.intersection(box(0, 0, 128, cy))
    front = ring.intersection(box(0, cy, 128, 128))
    solid(ic, back, face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=8, side="#1a5fb4", top=False, layer="ring-back")
    ic.path(geom_d(inner.difference(down(inner, 5)).intersection(box(0, 0, 128, cy + 4))), "#1a5fb4",
            opacity=0.55, layer_id="ring-inner-wall")         # inner wall of the ring, in shadow
    paper_plane(ic, 1.22, -6, -10, depth=3)
    solid(ic, front, face=BLUE_FACE, depth=8, side="#1c71d8", top=False, layer="ring-front")
    toplight(ic, back, width=1.5, opacity=0.6, layer="ring")
    return ic


def design_envelope():
    """F: blue envelope (GNOME Mail-like), the stamp carries the paper plane.
    Drawn on a 12..116 x 30..102 grid, then scaled as one unit (T) so the envelope is
    112 wide (8..120) and stands on the GNOME baseline (face bottom 112 + 6 side = 118)."""
    from shapely import affinity
    k, dy = 112 / 104, 112 - (30 + 72 * 112 / 104)
    T = lambda g: affinity.translate(affinity.scale(g, k, k, origin=(64, 30)), 0, dy)  # noqa: E731
    Y = lambda y: 30 + (y - 30) * k + dy                                               # noqa: E731
    X = lambda x: 64 + (x - 64) * k                                                    # noqa: E731
    ic = gk.Icon("Telegram - Gnomed (envelope + paper plane stamp)")
    env = T(rounded(box(12, 30, 116, 102), 7))
    solid(ic, env, face=[(0, "#62a0ea"), (1, "#3584e4")], depth=6, side="#1c71d8", layer="envelope")
    flap = T(poly([(15, 33), (113, 33), (64, 72)], 3))
    ic.path(geom_d(move(flap, 0, 2.5).difference(flap).intersection(env)), "#1a5fb4", opacity=0.35, layer_id="flap-shadow")
    solid(ic, flap, face=[(0, "#99c1f1"), (1, "#62a0ea")], depth=0, top=False, layer="flap")
    # stamp: paper with a perforated edge, the plane printed on it
    st = box(70, 60, 108, 96)
    perf = unary_union([circ(x, y, 1.6) for x in range(72, 108, 5) for y in (60, 96)] +
                       [circ(x, y, 1.6) for y in range(63, 96, 5) for x in (70, 108)])
    stamp = T(st.difference(perf))
    solid(ic, stamp, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=2, side="#deddda", layer="stamp")
    recess(ic, T(box(74, 64, 104, 92)), "#f6f5f4", wall=1.2, wall_opacity=0.12, layer="stamp-print-area")
    # the print: only the paper plane - its exact shape measured from the source
    # (geometry.json "holes"), in Telegram blue on the white stamp, scaled as one unit
    import json
    import fam
    g = json.loads((Path(__file__).resolve().parent / "geometry.json").read_text())["parts"]
    (plane_d,), _ = fam.place([g["holes"]["d"]], (X(76), Y(67), X(102), Y(89)))
    ic.path(plane_d, ic.linear([(0, "#62a0ea"), (1, "#3584e4")], 0, Y(67), 0, Y(89)), layer_id="stamp-print-plane")
    return ic

if __name__ == "__main__":
    # owner: "Defaultu o mektup yap" -> the envelope is the default; the cloud moves to Symbol
    # owner: the default must be the envelope also in the Symbol style he uses ->
    # symbol = envelope too; the cloud stays as a drawing here (telegram-cloud.svg), not in the pack
    design_cloud().save(Path(__file__).resolve().parent / "telegram-cloud.svg")
    save_styles(SLUG, {"faithful": design_envelope(), "disc": design_ring(), "symbol": design_envelope()})
