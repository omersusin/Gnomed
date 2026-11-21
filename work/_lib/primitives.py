"""Generic object primitives for free adaptations (REDESIGN.md, docs/MISTAKES.md §2):
a football, a lightning bolt, a star, a wizard hat, a faceted gem. Generic objects only -
never a brand logo or a character from memory. Colours are passed in (measured)."""
import numpy as np
from obj import *  # noqa: F401,F403


def regular(cx, cy, r, n, rot=-90):
    a = np.radians(rot + np.arange(n) * 360 / n)
    return poly(list(zip(cx + r * np.cos(a), cy + r * np.sin(a))))


def star(cx, cy, r, inner=0.45, n=5, rot=-90):
    a = np.radians(rot + np.arange(2 * n) * 180 / n)
    rr = np.where(np.arange(2 * n) % 2 == 0, r, r * inner)
    return poly(list(zip(cx + rr * np.cos(a), cy + rr * np.sin(a))), 1.0)


def football(cx, cy, r):
    """-> (ball, patches): white ball + dark pentagon patches clipped to the ball."""
    ball = circ(cx, cy, r)
    pats = [regular(cx, cy, r * 0.33, 5)]
    for k in range(5):
        ang = np.radians(-90 + k * 72)
        pats.append(regular(cx + np.cos(ang) * r * 0.95, cy + np.sin(ang) * r * 0.95, r * 0.30, 5, rot=90 + k * 72))
    return ball, unary_union(pats).intersection(ball)


def bolt(x0, y0, w, h):
    pts = [(0.62, 0), (0.12, 0.56), (0.46, 0.56), (0.30, 1), (0.88, 0.36), (0.52, 0.36), (0.74, 0)]
    return poly([(x0 + u * w, y0 + v * h) for u, v in pts], 1.5)


def wizard_hat(cx, base_y, w, h):
    """-> (brim, cone, band): a wide brim, a cone with a bent tip, the band."""
    brim = ellipse(cx, base_y, w / 2, h * 0.16)
    cone = poly([(cx - w * 0.30, base_y - h * 0.04), (cx - w * 0.08, base_y - h * 0.62), (cx + w * 0.06, base_y - h),
                 (cx + w * 0.10, base_y - h * 0.62), (cx + w * 0.30, base_y - h * 0.04)], 3)
    band = cone.intersection(box(cx - w, base_y - h * 0.30, cx + w, base_y - h * 0.10))
    return brim, cone, band


def gem(cx, cy, r):
    """-> (outline, upper facet): a cut gem."""
    g = poly([(cx - r, cy - r * 0.35), (cx - r * 0.55, cy - r), (cx + r * 0.55, cy - r), (cx + r, cy - r * 0.35), (cx, cy + r)], 1.0)
    top = poly([(cx - r, cy - r * 0.35), (cx - r * 0.55, cy - r), (cx + r * 0.55, cy - r), (cx + r, cy - r * 0.35)], 0.5)
    return g, top
