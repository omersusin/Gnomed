#!/usr/bin/env python3
"""payload_dumper - Gnomed redesign (Claude, 2026-11-23, batch).

The logo: the green Android robot with a grey wrench and an orange screwdriver, on navy. The app
unpacks an OTA payload into its partitions (boot, vendor_boot, system_ext ... shot-1, "Extract").
Every style carries the MEASURED logo (put_mark; geometry.json mark_split gives the tools their
real colours), each on a different thing:
  Symbol   A: the dumper - a navy dump truck tipping out the partition blocks, the robot on its bed
  Faithful B: the logo itself as a solid object - the robot with its wrench and screwdriver
  Disc     C: "47% - Extracting" - a round progress dial, the green arc around the robot (shot-1)
  Rimmed   D: the payload - the ROM's zip as an opened navy zip pouch, the partitions coming out
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402
from obj import mark_parts, fit  # noqa: E402

SLUG = Path(__file__).resolve().parent.name
GREEN = ("#7af0b0", "#5ce69c", "#3ddc84", "#2fb56b", "#238a52")       # the robot (source.png)
NAVY = ("#4a6580", "#3a5169", "#2c3e51", "#22303f", "#18222d")        # the tile / dark UI (source.png)
ORANGE = "#f08a24"                                                    # the screwdriver (source.png)


def A():
    """Symbol - the dumper: a dump truck (navy cab, steel bed) with its bed tipped up, the partition
    blocks (green, grey, orange) sliding out of the back; the green robot on the bed (anchors 1, 3, 4)."""
    ic = gk.Icon("payload_dumper - symbol")
    k, org = 1.06, (62.5, 113)

    def T(g):                                   # the truck drawn at 100 %, shown at 120 %
        return affinity.scale(g, k, k, origin=org)
    hinge = (92, 84)
    for n, (x, y, a, col) in enumerate(((99, 99, 14, GREEN[2]), (107, 88, -8, "#9a9996"), (101, 77, 20, ORANGE))):
        blk = affinity.rotate(rounded(box(x - 8, y - 5.5, x + 8, y + 5.5), 2), a, origin=(x, y))
        solid(ic, T(blk), face=col, depth=3, layer=f"block-{n}")
    chassis = rounded(box(10, 80, 96, 91), 3)
    solid(ic, T(chassis), face=[(0, "#6f8aa6"), (1, NAVY[2])], depth=3, side=NAVY[4], layer="chassis")
    bed = affinity.rotate(rounded(box(34, 44, 96, 82), 4), -20, origin=hinge)
    solid(ic, T(bed), face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#b5b3b0")], depth=5, side="#77767b", layer="bed")
    M = mark_parts(SLUG)
    shapes = fit([g for _, g, _ in M], (44, 47, 88, 80))
    with ic.group("mark"):
        for n, (g, (_, _, f)) in enumerate(zip(shapes, M)):
            ic.path(geom_d(T(affinity.rotate(g, -20, origin=hinge))), f, layer_id=f"mark-{n}", fill_rule="evenodd")
    cab = rounded(Polygon([(10, 91), (10, 63), (18, 53), (34, 53), (34, 91)]), 3)
    solid(ic, T(cab), face=[(0, "#6f8aa6"), (0.5, NAVY[0]), (1, NAVY[2])], depth=4, side=NAVY[4], layer="cab")
    win = rounded(Polygon([(14, 67), (20, 58), (30, 58), (30, 67)]), 1.5)
    ic.path(geom_d(T(win)), ic.linear([(0, "#99c1f1"), (1, "#62a0ea")], 0, 50, 0, 70), layer_id="cab-window")
    for wx in (27, 78):
        solid(ic, T(circ(wx, 98, 11)), face=[(0, "#3d3846"), (1, "#241f31")], depth=2, side="#000000", top=False,
              layer=f"wheel-{wx}")
        ic.path(geom_d(T(circ(wx, 98, 4.5))), "#9a9996", layer_id=f"hub-{wx}")
    return ic


def B():
    """Faithful - the logo as a solid object: the green robot with its antennas, the grey wrench
    and the orange screwdriver at its sides, each with thickness (anchors 1, 2)."""
    ic = gk.Icon("payload_dumper - faithful")
    put_mark(ic, SLUG, (10, 10, 118, 112), anchor="bottom", body=6, side=GREEN[4])
    return ic


def C():
    """Disc - "47% - Extracting": a round progress dial - steel rim, navy face, the green progress
    arc on its grey track, the robot in the middle (anchors 1, 3, 4)."""
    ic = gk.Icon("payload_dumper - disc")
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=5, side="#77767b", layer="rim")
    recess(ic, circ(cx, cy, R - 6), [(0, NAVY[1]), (1, NAVY[3])], wall=3, layer="face")
    ring = circ(cx, cy, R - 11).difference(circ(cx, cy, R - 20))
    ic.path(geom_d(ring), "#5e5c64", layer_id="track")
    arc = LineString([(cx + (R - 15.5) * math.cos(math.radians(a)), cy + (R - 15.5) * math.sin(math.radians(a)))
                      for a in range(-90, 80, 3)]).buffer(4.5, cap_style=1)
    ic.path(geom_d(arc), ic.linear([(0, GREEN[0]), (1, GREEN[3])], cx, cy - R, cx, cy + R), layer_id="progress")
    put_mark(ic, SLUG, (cx - 24, cy - 24, cx + 24, cy + 24))
    return ic


def D():
    """Rimmed - the payload: the ROM's zip as a navy zip pouch, opened - the partitions (green, grey,
    orange blocks) come out of its zipper, the logo printed on its front (anchors 1, 3, 4)."""
    ic = gk.Icon("payload_dumper - rimmed")
    for n, (x, y, a, col) in enumerate(((44, 40, -14, GREEN[2]), (66, 34, 4, "#9a9996"), (88, 40, 16, ORANGE))):
        blk = affinity.rotate(rounded(box(x - 10, y - 16, x + 10, y + 16), 3), a, origin=(x, y))
        solid(ic, blk, face=[(0, "#ffffff"), (0.25, col), (1, col)], depth=3, layer=f"partition-{n}")
    pouch = rounded(box(10, 46, 118, 114), 14)
    solid(ic, pouch, face=[(0, NAVY[0]), (0.5, NAVY[2]), (1, NAVY[3])], depth=6, side=NAVY[4], layer="pouch")
    teeth = unary_union([box(x, 47.5, x + 2.2, 53) for x in range(20, 108, 4)])
    ic.path(geom_d(box(16, 48, 112, 52.5)), NAVY[4], layer_id="zip-track")
    ic.path(geom_d(teeth), "#c0bfbc", layer_id="zip-teeth")
    pull = unary_union([rounded(box(104, 45, 114, 56), 2), rounded(box(106, 55, 112, 68), 2.5)])
    solid(ic, pull, face=[(0, "#ffffff"), (1, "#9a9996")], depth=1.5, side="#5e5c64", layer="zip-pull")
    put_mark(ic, SLUG, (34, 60, 94, 108))
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()})
