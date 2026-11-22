#!/usr/bin/env python3
"""deezer - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts).

The owner's OG Deezer logo (work/deezer/source.png) is the multicolour equaliser bars +
white "deezer" wordmark on black.  The bars are the icon mark; the wordmark is left out (it
would be unreadable at 32 px).  The measured gradient bands are merged with regions(SLUG)
and every bar gets ONE source gradient (docs/PLAYBOOK.md#gradients) - never flat bands.
"""
import sys
from pathlib import Path
from shapely import affinity
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402   (objects.py + obj.py: gk, solid, parts, fit, Grad ...)

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent

# The measured colour regions, with gradient bands merged back into one part.
# r0 is the white wordmark; the bars are everything else.
R = regions(SLUG)
MARK = unary_union([g for n, g, _ in R if n != "r0"]).buffer(0)

# The source's 10 bars: the gradient bands touch, so their union gives one polygon per bar.
BARS = sorted([g for g in (MARK.geoms if MARK.geom_type == "MultiPolygon" else [MARK])
               if g.area > 50], key=lambda g: (g.bounds[1], g.bounds[0]))
BAR_FILLS = [gradient(SLUG, g) for g in BARS]

# The 4 columns of the equaliser (bars grouped by x centre); one bar per column on a label.
COLUMN_SHAPES = []
for g in BARS:
    cx = (g.bounds[0] + g.bounds[2]) / 2
    for col in COLUMN_SHAPES:
        ccx = (col.bounds[0] + col.bounds[2]) / 2
        if abs(ccx - cx) < 7:
            COLUMN_SHAPES[COLUMN_SHAPES.index(col)] = unary_union([col, g])
            break
    else:
        COLUMN_SHAPES.append(g)
COLUMN_SHAPES.sort(key=lambda g: g.bounds[0])
COLUMN_FILLS = [gradient(SLUG, g) for g in COLUMN_SHAPES]

LIGHT = RAMP["Light"]
DARK = RAMP["Dark"]
BLUE = RAMP["Blue"]


def _dark(h, factor=0.62):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * factor), int(g * factor), int(b * factor))


def _side(f):
    """A darker side colour for a measured Grad or hex face."""
    base = f.stops[-1][1] if isinstance(f, Grad) else f
    return _dark(base)


def draw_bars(ic, box_, depth=5.0, layer="bars", top=True):
    """All 10 measured bars, each one piece with one source gradient."""
    fitted = fit(BARS, box_, anchor="bottom")
    for i, (g, f) in enumerate(zip(fitted, BAR_FILLS)):
        solid(ic, g, face=f, depth=depth, side=_side(f), top=top, layer=f"{layer}{i}")


def simple_bars(ic, box_, depth=0.0, layer="bars"):
    """One bar per measured column - legible on a label (record, cassette, speaker grille)."""
    fitted = fit(COLUMN_SHAPES, box_, anchor="center")
    for i, (g, f) in enumerate(zip(fitted, COLUMN_FILLS)):
        x0, y0, x1, y1 = g.bounds
        bar = rounded(box(x0, y0, x1, y1), min(1.2, (x1 - x0) / 2.5))
        solid(ic, bar, face=f, depth=depth, side=_side(f), top=False, layer=f"{layer}{i}")


def A():
    """L1 - the measured multicolour bars as thick objects, each bar one smooth gradient."""
    ic = gk.Icon("deezer concept A")
    draw_bars(ic, (8, 8, 120, 112), depth=6, layer="bars")
    return ic


def B():
    """L2 - a deep-blue bookshelf speaker: the measured bars as the grille, tweeter above."""
    ic = gk.Icon("deezer concept B")
    cab = rounded(box(18, 20, 110, 112), 9)
    solid(ic, cab, face=[(0, BLUE[1]), (0.5, BLUE[3]), (1, BLUE[4])], depth=7, side=BLUE[4], layer="cabinet")
    baffle = rounded(box(24, 26, 104, 106), 6)
    recess(ic, baffle, [(0, "#1a5fb4"), (1, "#1462b8")], wall=2.0, wall_opacity=0.22, layer="baffle")
    # tweeter: light metal ring around a dark dome
    ring = circ(64, 46, 15).difference(circ(64, 46, 10))
    solid(ic, ring, face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=2, side="#77767b", top=False, layer="tweeter-ring")
    dome = circ(64, 46, 10)
    solid(ic, dome, face=[(0, "#3d3846"), (1, "#241f31")], depth=1, side="#241f31", top=False, layer="tweeter-dome")
    toplight(ic, dome, width=1.0, opacity=0.30, layer="tweeter-dome")
    # grille: dark recess, one gradient bar per measured column
    grille = rounded(box(30, 64, 98, 102), 4)
    recess(ic, grille, [(0, "#241f31"), (1, "#3d3846")], wall=2.0, wall_opacity=0.35, layer="grille")
    simple_bars(ic, (33, 67, 95, 99), depth=1.0, layer="grille-bars")
    hole(ic, circ(64, 107, 2.2), color=("#241f31", "#3d3846"), wall=1.0, layer="bass-port")
    return ic


def C():
    """L2 round - a vinyl record half out of its sleeve, with a light rim ring."""
    ic = gk.Icon("deezer concept C")
    # the sleeve behind the record: a real object, not a plate, and a light mass on dark
    sleeve = affinity.rotate(rounded(box(14, 14, 106, 106), 5), -7, origin=(60, 60))
    solid(ic, sleeve, face=[(0, "#ffffff"), (0.5, "#f6f5f4"), (1, "#deddda")],
          depth=2, side="#c0bfbc", layer="sleeve")
    spine = sleeve.intersection(box(0, 0, 24, 128))
    ic.path(geom_d(spine.difference(move(spine, 1.4, 0))), "#9a9996", opacity=0.45,
            layer_id="sleeve-spine")
    # the record: a lighter charcoal so it still reads on a dark wallpaper
    cx, cy = 70, 69.5
    rim = circ(cx, cy, 49).difference(circ(cx, cy, 45.5))
    solid(ic, rim, face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")],
          depth=1.5, side="#77767b", top=False, layer="rim")
    disc = circ(cx, cy, 46)
    solid(ic, disc, face=[(0, "#5e5c64"), (0.5, "#3d3846"), (1, "#241f31")], depth=3,
          side="#241f31", top=False, layer="disc")
    # white label, bars larger so they still read at 32 px
    label = circ(cx, cy, 30)
    recess(ic, label, [(0, "#ffffff"), (0.5, "#f6f5f4"), (1, "#deddda")],
           wall=1.2, wall_opacity=0.14, layer="label")
    simple_bars(ic, (46, 56, 94, 84), depth=0.8, layer="label-bars")
    hole(ic, circ(cx, cy, 2.8), color=("#241f31", "#3d3846"), wall=1.2, layer="spindle")
    toplight(ic, disc, width=1.2, opacity=0.25, layer="disc")
    return ic


def D():
    """L2 - a cassette tape: dark shell, light reels, the measured columns on its label."""
    ic = gk.Icon("deezer concept D")
    shell = rounded(box(12, 32, 116, 110), 8)
    solid(ic, shell, face=[(0, "#5e5c64"), (0.5, "#3d3846"), (1, "#241f31")], depth=6,
          side="#241f31", layer="shell")
    label = rounded(box(20, 38, 108, 60), 3)
    solid(ic, label, face=[(0, "#ffffff"), (0.5, "#f6f5f4"), (1, "#deddda")], depth=0, top=False, layer="label")
    recess(ic, label, [(0, "#f6f5f4"), (1, "#deddda")], wall=1.0, wall_opacity=0.12, layer="label-recess")
    simple_bars(ic, (28, 41, 100, 57), depth=0.6, layer="label-bars")
    window = rounded(box(32, 64, 96, 96), 4)
    recess(ic, window, [(0, "#241f31"), (1, "#3d3846")], wall=2.0, wall_opacity=0.40, layer="window")
    for cx in (48, 80):
        hub = circ(cx, 80, 9)
        solid(ic, hub, face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=1, side="#77767b", top=False, layer=f"hub-{cx}")
        hole(ic, circ(cx, 80, 3), color=("#241f31", "#3d3846"), wall=1.2, layer=f"reel-hole-{cx}")
    for cx in (20, 108):
        solid(ic, circ(cx, 101, 1.6), face=[(0, "#deddda"), (1, "#9a9996")], depth=0, top=False, layer=f"screw-{cx}")
    toplight(ic, shell, width=1.4, opacity=0.35, layer="shell")
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
