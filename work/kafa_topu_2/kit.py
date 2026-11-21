"""Kafa Topu 2 - shared parts for the concepts and the final redesign (REDESIGN.md 3b).

Serious, not a toy: a stitched leather ball, leather boots on rubber soles with studs,
heads with proportionate features (small almond eyes, a determined grin), real light from
the top and thickness. No outlines, no googly eyes. Colours from the store icon (skin
#d48154, hair #281a1a / #705254) mapped to GNOME ramps.
"""
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_lib"))
from obj import *  # noqa: F401,F403,E402

LEFT_SKIN = ("#f2c29f", "#e2a073", "#c27a4b", "#8e4c25")      # top light / face / shadow / side
RIGHT_SKIN = ("#d9a27a", "#b97a4e", "#8c5532", "#5e3519")
RED = ("#ed333b", "#c01c28", "#a51d2d", "#7a1520")
BLUE = ("#62a0ea", "#1c71d8", "#1a5fb4", "#14457f")


def regular(cx, cy, r, n, rot=-90):
    a = np.radians(rot + np.arange(n) * 360 / n)
    return Polygon(list(zip(cx + r * np.cos(a), cy + r * np.sin(a))))


# ------------------------------------------------------------------ the ball
def ball(ic, cx, cy, r, name="ball", depth=2.5):
    """Leather match ball: white panels, dark pentagons, stitched seams, gloss."""
    b = circ(cx, cy, r)
    solid(ic, b, face=[(0, "#ffffff"), (0.55, "#f6f5f4"), (1, "#c0bfbc")], depth=depth, side="#9a9996", top=False, layer=name)
    centre = regular(cx + r * 0.04, cy + r * 0.06, r * 0.30, 5)
    pents = [centre]
    for k in range(5):
        a = np.radians(-90 + k * 72)
        pents.append(regular(cx + np.cos(a) * r * 0.92, cy + np.sin(a) * r * 0.92, r * 0.27, 5, rot=90 + k * 72))
    pent = unary_union(pents).intersection(b)
    ic.path(geom_d(pent), ic.linear([(0, "#5e5c64"), (1, "#241f31")], 0, cy - r, 0, cy + r), layer_id=f"{name}-pentagons")
    # seams: from the centre pentagon's corners outwards (stitched panels)
    cc = list(centre.exterior.coords)[:-1]
    seams = []
    for (x, y) in cc:
        vx, vy = x - cx, y - cy
        n = np.hypot(vx, vy)
        seams.append(LineString([(x, y), (cx + vx / n * r * 0.66, cy + vy / n * r * 0.66)]).buffer(r * 0.025))
    ic.path(geom_d(unary_union(seams).intersection(b).difference(pent)), "#9a9996", opacity=0.8, layer_id=f"{name}-seams")
    gl = ellipse(cx - r * 0.38, cy - r * 0.42, r * 0.34, r * 0.22).intersection(b)
    ic.path(geom_d(gl), ic.radial([(0, "#ffffff", 0.95), (1, "#ffffff", 0)], cx - r * 0.38, cy - r * 0.42, r * 0.34), layer_id=f"{name}-gloss")
    return b


# ------------------------------------------------------------------ a boot
def boot(ic, heel_x, sole_y, length, d, team, name):
    """A football boot in side view, toe towards d (+1 right / -1 left); sole bottom at sole_y."""
    L = length

    def P(u, v):                    # u: heel 0 -> toe 1, v: height above the sole bottom (in L)
        return (heel_x + d * u * L, sole_y - v * L)
    upper = poly([P(0.02, 0.10), P(0.00, 0.40), P(0.10, 0.46), P(0.42, 0.44), P(0.62, 0.32), P(0.88, 0.24),
                  P(1.00, 0.17), P(0.99, 0.10)], L * 0.06)
    sole = poly([P(-0.02, 0.0), P(1.01, 0.0), P(1.02, 0.11), P(-0.01, 0.11)], L * 0.03).difference(box(0, 0, 0, 0))
    studs = unary_union([poly([P(u - 0.04, 0.02), P(u + 0.04, 0.02), P(u + 0.03, -0.07), P(u - 0.03, -0.07)], L * 0.01)
                         for u in (0.10, 0.27, 0.60, 0.84)])
    solid(ic, studs, face="#5e5c64", depth=0, top=False, layer=f"{name}-studs")
    solid(ic, sole, face=[(0, "#77767b"), (1, "#3d3846")], depth=1.5, side="#241f31", top=False, layer=f"{name}-sole")
    solid(ic, upper, face=[(0, team[0]), (0.45, team[1]), (1, team[2])], depth=2, side=team[3], layer=f"{name}-upper")
    # heel counter + laces in white, a sheen on the leather
    heel = poly([P(0.0, 0.12), P(0.0, 0.40), P(0.12, 0.42), P(0.14, 0.12)], L * 0.03).intersection(upper)
    ic.path(geom_d(heel), "#ffffff", opacity=0.92, layer_id=f"{name}-heel")
    laces = unary_union([LineString([P(0.40 + 0.07 * k, 0.42 - 0.04 * k), P(0.45 + 0.07 * k, 0.33 - 0.04 * k)]).buffer(L * 0.018)
                         for k in range(4)]).intersection(upper)
    ic.path(geom_d(laces), "#ffffff", layer_id=f"{name}-laces")
    sheen = poly([P(0.20, 0.30), P(0.55, 0.36), P(0.80, 0.22), P(0.55, 0.30)], L * 0.02).intersection(upper)
    ic.path(geom_d(sheen), "#ffffff", opacity=0.35, layer_id=f"{name}-sheen")
    return upper


# ------------------------------------------------------------------ a head
def head(ic, cx, cy, r, d, skin, kind, name):
    """A big footballer head in 3/4 view looking towards d. kind: 'swept' (brown hair with a
    blond streak + beard) or 'buzz' (buzz cut). Features proportionate, no outlines."""
    lt, mid, sh, side = skin
    ear = ellipse(cx - d * r * 0.90, cy + r * 0.05, r * 0.15, r * 0.22)
    solid(ic, ear, face=[(0, mid), (1, sh)], depth=1.5, side=side, top=False, layer=f"{name}-ear")
    h = ellipse(cx, cy, r, r * 1.05)
    solid(ic, h, face=[(0, lt), (0.5, mid), (1, sh)], depth=2.5, side=side, layer=f"{name}-head")
    # cheek shadow on the far side (the head is round)
    far = ellipse(cx - d * r * 0.55, cy + r * 0.15, r * 0.55, r * 0.85).intersection(h)
    ic.path(geom_d(far), sh, opacity=0.25, layer_id=f"{name}-shade")
    if kind == "swept":
        cap = h.intersection(box(0, 0, 128, cy - r * 0.30))
        quiff = ellipse(cx + d * r * 0.20, cy - r * 0.82, r * 0.80, r * 0.36)
        hair = unary_union([cap, quiff, ellipse(cx - d * r * 0.55, cy - r * 0.40, r * 0.48, r * 0.52).intersection(h.buffer(1))])
        hair = hair.intersection(ellipse(cx + d * 2, cy - 2, r * 1.08, r * 1.16)).difference(box(0, cy + r * 0.05, 128, 128)).buffer(0)
        solid(ic, hair, face=[(0, "#8f6a4a"), (0.5, "#5e4034"), (1, "#3d2a22")], depth=1.2, side="#241f31", top=False, layer=f"{name}-hair")
        crest = ellipse(cx + d * r * 0.18, cy - r * 0.64, r * 0.82, r * 0.50)
        streak = crest.difference(move(crest, d * 2.2, 3.2)).intersection(hair)
        ic.path(geom_d(streak), ic.linear([(0, "#f9e27a"), (1, "#d9a83a")], 0, cy - r * 1.2, 0, cy - r * 0.5), layer_id=f"{name}-streak")
        toplight(ic, hair, layer=f"{name}-hair")
        beard = h.intersection(ellipse(cx + d * 3, cy + r * 0.48, r * 0.98, r * 0.64)).difference(
            ellipse(cx + d * 5, cy + r * 0.12, r * 0.82, r * 0.50))
        ic.path(geom_d(beard), ic.linear([(0, "#5e4034"), (1, "#3d2a22")], 0, cy, 0, cy + r), layer_id=f"{name}-beard")
    else:
        cap = h.intersection(box(0, 0, 128, cy - r * 0.40)).union(
            h.intersection(box(min(cx - d * r * 1.2, cx - d * r * 0.55), 0, max(cx - d * r * 1.2, cx - d * r * 0.55), cy - r * 0.05)))
        ic.path(geom_d(cap), "#3d2a22", opacity=0.78, layer_id=f"{name}-buzz")
    # eyes: small almond shapes looking at the opponent, brows lowered towards the nose
    nose_x = cx + d * r * 0.46
    for k, ex in enumerate((cx + d * r * 0.10, cx + d * r * 0.66)):
        ey = cy - r * 0.08
        w = r * (0.15 if k == 0 else 0.12)
        eye = ellipse(ex, ey, w, r * 0.075)
        ic.path(geom_d(eye), "#f6f5f4", layer_id=f"{name}-eye{k}")
        ic.path(geom_d(circ(ex + d * w * 0.35, ey, r * 0.06).intersection(eye)), "#3d3846", layer_id=f"{name}-iris{k}")
        tn = 1 if nose_x > ex else -1
        brow = poly([(ex - tn * w * 1.5, ey - r * 0.22), (ex + tn * w * 1.25, ey - r * 0.11),
                     (ex + tn * w * 1.25, ey - r * 0.04), (ex - tn * w * 1.5, ey - r * 0.14)], r * 0.03)
        ic.path(geom_d(brow), "#3d2a22", layer_id=f"{name}-brow{k}")
    nose = poly([(nose_x - d * r * 0.04, cy - r * 0.02), (nose_x + d * r * 0.16, cy + r * 0.20), (nose_x - d * r * 0.04, cy + r * 0.22)], r * 0.05)
    ic.path(geom_d(nose), sh, opacity=0.7, layer_id=f"{name}-nose")
    # determined grin (gritted teeth)
    mx, my = cx + d * r * 0.38, cy + r * 0.44
    lips = rounded(box(mx - r * 0.34, my - r * 0.14, mx + r * 0.34, my + r * 0.14), r * 0.12)
    ic.path(geom_d(lips), "#8f3b2a", layer_id=f"{name}-lips")
    teeth = rounded(box(mx - r * 0.28, my - r * 0.09, mx + r * 0.28, my + r * 0.09), r * 0.06)
    ic.path(geom_d(teeth), ic.linear([(0, "#ffffff"), (1, "#deddda")], 0, my - r * 0.1, 0, my + r * 0.1), layer_id=f"{name}-teeth")
    gap = box(mx - r * 0.28, my - 0.3, mx + r * 0.28, my + 0.3).intersection(teeth)
    ic.path(geom_d(gap), "#c0bfbc", layer_id=f"{name}-gap")
    return h


def player(ic, cx, sole_y, r, d, skin, kind, team, name):
    """A big head standing on ONE boot (the game's character)."""
    L = r * 2.05
    boot(ic, cx - d * r * 0.85, sole_y, L, d, team, f"{name}-boot")
    return head(ic, cx, sole_y - L * 0.34 - r * 0.98, r, d, skin, kind, name)


def bust(ic, cx, cy, r, d, skin, kind, team, name):
    """Head + jersey shoulders (the store icon's crop)."""
    sh = poly([(cx - r * 0.70, cy + r * 0.62), (cx + r * 0.70, cy + r * 0.62), (cx + r * 1.02, cy + r * 1.25),
               (cx - r * 1.02, cy + r * 1.25)], r * 0.25)
    solid(ic, sh, face=[(0, team[0]), (1, team[2])], depth=3, side=team[3], layer=f"{name}-jersey")
    collar = poly([(cx - r * 0.34, cy + r * 0.62), (cx + r * 0.34, cy + r * 0.62), (cx, cy + r * 0.95)], r * 0.05)
    ic.path(geom_d(collar), "#ffffff", opacity=0.9, layer_id=f"{name}-collar")
    return head(ic, cx, cy, r, d, skin, kind, name)


# ------------------------------------------------------------------ VS
def vs(ic, x, y, s=1.0, name="vs"):
    """The yellow VS: thick enamel letters with an orange side."""
    v = poly([(x, y), (x + 6 * s, y), (x + 9.5 * s, y + 11 * s), (x + 13 * s, y), (x + 19 * s, y), (x + 12.5 * s, y + 18 * s),
              (x + 6.5 * s, y + 18 * s)], 1.0 * s)
    sx = x + 20 * s
    S = unary_union([rounded(box(sx, y, sx + 12 * s, y + 4.6 * s), 2 * s), rounded(box(sx, y, sx + 4.6 * s, y + 10.5 * s), 2 * s),
                     rounded(box(sx, y + 6.8 * s, sx + 12 * s, y + 11.4 * s), 2 * s), rounded(box(sx + 7.4 * s, y + 6.8 * s, sx + 12 * s, y + 18 * s), 2 * s),
                     rounded(box(sx, y + 13.4 * s, sx + 12 * s, y + 18 * s), 2 * s)])
    g = unary_union([v, S])
    solid(ic, g, face=[(0, "#f9f06b"), (0.5, "#f6d32d"), (1, "#f5c211")], depth=2.5 * s, side="#c64600", layer=name)
    return g


# ------------------------------------------------------------------ goal + pitch
def goal(ic, x0, y0, x1, y1, name="goal"):
    """White metal goal frame with a net, seen from the front-side."""
    frame = unary_union([box(x0, y0, x1, y0 + 4), box(x0, y0, x0 + 4, y1)])
    net = box(x0 + 4, y0 + 4, x1, y1)
    lines = unary_union([LineString([(x, y0 + 4), (x, y1)]).buffer(0.5) for x in np.arange(x0 + 11, x1, 8)] +
                        [LineString([(x0 + 4, y), (x1, y)]).buffer(0.5) for y in np.arange(y0 + 11, y1, 8)])
    ic.path(geom_d(net), ic.linear([(0, "#f6f5f4"), (1, "#deddda")], 0, y0, 0, y1), layer_id=f"{name}-netfill")
    ic.path(geom_d(lines.intersection(net)), "#c0bfbc", layer_id=f"{name}-net")
    solid(ic, frame, face=[(0, "#ffffff"), (1, "#deddda")], depth=2, side="#9a9996", layer=f"{name}-frame")
    return frame


def pitch(ic, cx, cy, rx, ry, name="pitch"):
    """A round pitch with thickness: mown turf stripes, white centre line and circle."""
    turf = ellipse(cx, cy, rx, ry)
    solid(ic, turf, face=[(0, "#8ff0a4"), (0.5, "#57e389"), (1, "#2ec27e")], depth=5, side="#26a269", top=False, layer=name)
    stripes = unary_union([box(cx - rx + k * rx / 3, cy - ry, cx - rx + (k + 0.5) * rx / 3, cy + ry) for k in range(6)]).intersection(turf)
    ic.path(geom_d(stripes), "#26a269", opacity=0.18, layer_id=f"{name}-stripes")
    lines = unary_union([LineString([(cx, cy - ry), (cx, cy + ry)]).buffer(0.6),
                         ellipse(cx, cy, rx * 0.30, ry * 0.30).difference(ellipse(cx, cy, rx * 0.30 - 1.2, ry * 0.30 - 0.8))]).intersection(turf)
    ic.path(geom_d(lines), "#ffffff", opacity=0.85, layer_id=f"{name}-lines")
    return turf
