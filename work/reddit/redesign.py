#!/usr/bin/env python3
"""reddit - Gnomed redesign (Claude, 2026-11-23, batch).

The logo IS Snoo's head (REDESIGN 5 "A mascot logo is still the logo"): every style carries the
MEASURED head (put_mark; the eyes are painted orange like the logo - geometry.json mark_hole_fill,
owner 2026-11-23 "Logodaki gibi boya"), each with a different thing from the app's own screens:
  Symbol   A: the upvote - Reddit's orange up arrow, Snoo's head in front of it (shots 1, 5, 6)
  Faithful B: Snoo's head itself as a solid object - the logo, with thickness
  Disc     C: "Find anything" - the round search lens, Snoo in it on the Reddit orange (shots 2, 3)
  Rimmed   D: a post - the white post card with its photo and vote row, Snoo looking over it (shots 2-5)
"""
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
ORANGE = ("#ff8b60", "#ff6a33", "#ff4500", "#e03d00", "#b83200")       # Reddit orange (source.png)
WHITE_SIDE = "#c0bfbc"


def snoo(ic, box_, depth=5):
    """Snoo's measured head standing free (L1): one grey side under it, the head on top."""
    return put_mark(ic, SLUG, box_, anchor="bottom", body=depth, side=WHITE_SIDE)


def up_arrow(cx, tip, w, head_h, stem_w, bottom, r=5):
    """Reddit's vote arrow: a wide triangle head and a short square stem, all corners rounded."""
    head = Polygon([(cx, tip), (cx + w / 2, tip + head_h), (cx - w / 2, tip + head_h)])
    stem = box(cx - stem_w / 2, tip + head_h - 1, cx + stem_w / 2, bottom)
    return rounded(unary_union([head, stem]), r)


def A():
    """Symbol - the upvote: Reddit's big orange up arrow with thickness, Snoo's head printed on it
    (anchors 1, 2, 3)."""
    ic = gk.Icon("reddit - symbol")
    arrow = up_arrow(64, 6, 116, 60, 54, 112, r=7)
    solid(ic, arrow, face=[(0, ORANGE[0]), (0.5, ORANGE[2]), (1, ORANGE[3])], depth=6, side=ORANGE[4], layer="upvote")
    snoo(ic, (37, 36, 91, 86), depth=3)
    return ic


def B():
    """Faithful - the logo as a die-cut sticker: Snoo's white head on the Reddit orange, cut around
    its outline with an orange margin, a little thickness (anchors 1, 2)."""
    ic = gk.Icon("reddit - faithful")
    from obj import mark_parts, fit
    box_ = (18, 18, 110, 100)
    head = unary_union(fit([g for _, g, _ in mark_parts(SLUG)], box_, anchor="bottom"))
    sticker = rounded(head.buffer(9, quad_segs=24), 4)
    solid(ic, sticker, face=[(0, ORANGE[1]), (0.55, ORANGE[2]), (1, ORANGE[3])], depth=5, side=ORANGE[4], layer="sticker")
    put_mark(ic, SLUG, box_, anchor="bottom")
    return ic


def C():
    """Disc - "Find anything": the round search lens with its steel rim and handle; through the
    glass the Reddit orange with Snoo, as in the search bar (anchors 1, 2, 5)."""
    ic = gk.Icon("reddit - disc")
    cx, cy, R = 56, 56, 46
    handle = LineString([(cx + R * 0.62, cy + R * 0.62), (108, 108)]).buffer(8, cap_style=1)
    solid(ic, handle, face=[(0, "#5e5c64"), (1, "#3d3846")], depth=4, side="#241f31", layer="handle")
    rim = circ(cx, cy, R)
    solid(ic, rim, face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=5, side="#77767b", layer="rim")
    glass = circ(cx, cy, R - 7)
    recess(ic, glass, [(0, ORANGE[1]), (1, ORANGE[3])], wall=3, layer="glass")
    snoo(ic, (cx - 29, cy - 25, cx + 29, cy + 27), depth=3)
    ic.path(geom_d(circ(cx, cy, R - 7).difference(circ(cx + 6, cy + 6, R - 7))), "#ffffff", opacity=0.22,
            layer_id="glass-glint")
    return ic


def D():
    """Rimmed - the conversation ("Join the conversation"): the comments bubble of the post row as a
    solid orange speech bubble, Snoo talking in it (anchors 1, 2, 4)."""
    ic = gk.Icon("reddit - rimmed")
    bub = rounded(box(10, 14, 118, 96), 26)
    tail = Polygon([(28, 86), (18, 116), (54, 90)])
    bubble = rounded(unary_union([bub, tail]), 3)
    solid(ic, bubble, face=[(0, ORANGE[0]), (0.5, ORANGE[2]), (1, ORANGE[3])], depth=5, side=ORANGE[4], layer="bubble")
    snoo(ic, (32, 22, 96, 84), depth=3)
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
