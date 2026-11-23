#!/usr/bin/env python3
"""iconrequest - Gnomed redesign (Claude, 2026-11-23, batch).

Icon Request collects the apps an icon pack is missing and shares the request; it also checks a
pack's health and compares packs (store screenshots). The logo: a green robot with yellow eyes,
a drafting compass (yellow head, grey legs) drawing a white arc on its body, on navy. Every style
carries the MEASURED logo (put_mark), each on a different thing:
  Symbol   A: "Select apps and share" - the request sent: an envelope, the logo as its stamp (shot-1)
  Faithful B: the logo itself as a solid object
  Disc     C: "Health Status 99%" - a round dial with the yellow ring almost full (shot-5)
  Rimmed   D: "Health Check" - the check's shield, navy with a green rim, the logo on it (shot-1)
"""
import math
import sys
from pathlib import Path

from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parent.name
NAVY = ("#2a5aa8", "#1a4590", "#0d3275", "#002867", "#001c4a")        # the tile (source.png)
GREEN = ("#5ce69c", "#22d77a", "#00c763", "#00a352", "#007a3d")       # the robot (source.png)
YELLOW = ("#ffd75e", "#f5c211", "#efb100", "#c88f00")                 # the compass head, eyes (source.png)


def A():
    """Symbol - "New Icon Request - Select apps and share": the request sent - a green envelope with
    its flap, the logo printed on a white-edged navy stamp (anchors 1, 2, 3)."""
    ic = gk.Icon("iconrequest - symbol")
    env = rounded(box(8, 28, 120, 108), 7)
    solid(ic, env, face=[(0, GREEN[1]), (1, GREEN[3])], depth=4, side=GREEN[4], layer="envelope")
    flap = Polygon([(10, 30), (118, 30), (64, 72)])
    ic.path(geom_d(rounded(flap, 3)), ic.linear([(0, "#a8f5cb"), (1, GREEN[1])], 0, 30, 0, 72), layer_id="flap")
    ic.path(geom_d(LineString([(12, 104), (52, 70)]).buffer(1)), "#000000", opacity=0.12, layer_id="fold-l")
    ic.path(geom_d(LineString([(116, 104), (76, 70)]).buffer(1)), "#000000", opacity=0.12, layer_id="fold-r")
    stamp = rounded(box(68, 46, 112, 100), 2.5)
    solid(ic, stamp, face=[(0, "#ffffff"), (1, "#deddda")], depth=1.5, side="#9a9996", layer="stamp")
    recess(ic, rounded(box(72, 50, 108, 96), 2), [(0, NAVY[1]), (1, NAVY[3])], wall=1.5, layer="stamp-print")
    put_mark(ic, SLUG, (76, 54, 104, 92))
    return ic


def B():
    """Faithful - the logo itself as a solid object: the green robot with its yellow eyes, the
    compass and its white arc on the body, the dark green as its thickness (anchors 1, 2)."""
    ic = gk.Icon("iconrequest - faithful")
    put_mark(ic, SLUG, (20, 10, 108, 110), anchor="bottom", body=7, side=GREEN[4])
    return ic


def C():
    """Disc - "Health Status 99%": a round dial - steel rim, white face, the yellow ring almost
    full on its grey track, the logo in the middle (anchors 1, 5)."""
    ic = gk.Icon("iconrequest - disc")
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, "#5e5c64"), (1, "#3d3846")], depth=5, side="#241f31", layer="rim")
    recess(ic, circ(cx, cy, R - 6), [(0, "#ffffff"), (1, "#deddda")], wall=3, layer="face")
    track = circ(cx, cy, R - 11).difference(circ(cx, cy, R - 21))
    ic.path(geom_d(track), "#c0bfbc", layer_id="track")
    arc = LineString([(cx + (R - 16) * math.cos(math.radians(a)), cy + (R - 16) * math.sin(math.radians(a)))
                      for a in range(-90, 255, 3)]).buffer(5, cap_style=1)
    ic.path(geom_d(arc), ic.linear([(0, YELLOW[0]), (1, YELLOW[3])], cx, cy - R, cx, cy + R), layer_id="health")
    put_mark(ic, SLUG, (cx - 19, cy - 22, cx + 19, cy + 22))
    return ic


def D():
    """Rimmed - "Health Check - find duplicate mappings and missing drawables": the check's shield in
    the app's navy with a green rim, the logo on it (anchors 1, 2, 5)."""
    ic = gk.Icon("iconrequest - rimmed")
    w, top, bot = 96, 8, 118
    sh = unary_union([box(64 - w / 2, top, 64 + w / 2, top + 50),
                      Polygon([(64 - w / 2, top + 48), (64 + w / 2, top + 48), (64, bot)])])
    sh = rounded(sh.buffer(0), 12)
    solid(ic, sh, face=[(0, GREEN[1]), (1, GREEN[3])], depth=5, side=GREEN[4], layer="shield-rim")
    inner = sh.buffer(-6)
    ic.path(geom_d(inner), ic.linear([(0, NAVY[1]), (1, NAVY[3])], 0, top, 0, bot), layer_id="shield-face")
    put_mark(ic, SLUG, (40, 20, 88, 86))
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
