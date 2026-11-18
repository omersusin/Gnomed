"""Shared GNOME construction helpers for Gnomed builds (on top of gnome_kit).

Every mark is passed as SOURCE geometry (work/<slug>/geometry.json, 0..128
coordinates of the source tile) and only scaled/moved as one unit here, so all
four styles of an app share exactly the same identity geometry.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/.claude/skills/gnome-android-icons/scripts")
import gnome_kit as gk  # noqa: E402
from gnome_kit import shade  # noqa: E402,F401

WORK = Path(__file__).resolve().parent.parent
PAPER, PAPER_SIDE, WHITE_SIDE = "#f6f5f4", "#d5d3cf", "#deddda"
SQUARE_FACE = dict(x=12, y=12, w=104, h=100)   # plate("square") face box
DISC = dict(cx=64, cy=63, r=59)


def geo(slug):
    g = json.loads((WORK / slug / "geometry.json").read_text())
    return {k: v["d"] for k, v in g["parts"].items()}, g["info"]


def note(slug):
    return (f"geometry: {slug} IconRequest PNG, colour-mask potrace "
            f"(work/_lib/gtrace.py, IoU >= 0.99 per part); GNOME construction: Gnomed")


def place(ds, box, ref=None):
    """Scale + move the paths `ds` (list) as ONE unit so `ref` paths' bbox (default:
    all of ds) fits `box` (x0, y0, x1, y1), centred, aspect kept."""
    ref = ref or ds
    x0, y0, x1, y1 = gk.bbox_d(ref)
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    ox, oy = (x0 + x1) / 2, (y0 + y1) / 2
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    return [gk.xform_d(d, s, cx - ox, cy - oy, about=(ox, oy)) for d in ds], s


def box_c(cx, cy, w, h=None):
    h = w if h is None else h
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def raised(ic, items, lift=2.0, layer="mark"):
    """items: list of (d, fill, side_fill). All sides first, then all faces (evenodd)."""
    with ic.group(layer):
        if lift:
            for i, (d, _f, side) in enumerate(items):
                if side:
                    ic.path(gk.translate_d(d, 0, lift), side, layer_id=f"{layer}-{i}-side", fill_rule="evenodd")
        for i, (d, f, _s) in enumerate(items):
            ic.path(d, f, layer_id=f"{layer}-{i}-face", fill_rule="evenodd")


def white_items(ds, side=WHITE_SIDE, fill="#ffffff"):
    return [(d, fill, side) for d in ds]


def plate(ic, face, face_fill=None, chin_base=None):
    """Square template plate; face may be a gradient (face_fill) with chin from chin_base."""
    if face_fill:
        chin = ic.chin_gradient(chin_base or face, 12, 116, 8)
        ic.plate("square", face=face_fill, r=8, chin=chin)
    else:
        ic.plate("square", face=face, r=8)
    return SQUARE_FACE


def disc(ic, face, face_fill=None, chin_base=None, top_light=0.6):
    if face_fill:
        chin = ic.chin_gradient(chin_base or face, 5, 123, 59 * 0.9)
        ic.disc(face=face_fill, chin=chin, top_light=top_light)
    else:
        ic.disc(face=face, top_light=top_light)
    return DISC


def rimmed(ic, inner, inner_fill=None):
    if inner_fill:
        return ic.rimmed_disc(inner=inner, inner_gradient=inner_fill)
    return ic.rimmed_disc(inner=inner)


def slab(ic, d, face, depth=4, face_fill=None, layer="body", corner_r=None):
    x0, _, x1, _ = gk.bbox_d(d)
    chin = ic.chin_gradient(face, x0, x1, corner_r if corner_r is not None else (x1 - x0) * 0.3)
    with ic.group(layer):
        ic.path(gk.translate_d(d, 0, depth), chin, layer_id=f"{layer}-chin", fill_rule="evenodd")
        ic.path(d, face_fill or face, layer_id=f"{layer}-face", fill_rule="evenodd")


def offset_d(d, dist, samples=900):
    """Outline offset of a closed path (round joins) -> polygon path d. Used for an
    outer margin that the source shows as ground colour around a mark."""
    from shapely.geometry import Polygon
    from svgpathtools import parse_path
    polys = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        polys.append(Polygon([(p.real, p.imag) for p in pts]).buffer(0))
    from shapely.ops import unary_union
    # union of every piece (letters, brackets ...), not just the largest one
    poly = unary_union([p for p in polys if p.area > 0.5]).buffer(dist, join_style=1, resolution=24)
    geoms = getattr(poly, "geoms", [poly])
    out = []
    for g in geoms:
        coords = list(g.exterior.coords)
        out.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in coords[:-1]) + "Z")
    return "".join(out)


def save(ic, slug, alt):
    return ic.save(WORK / slug / f"{slug}-{alt}.svg")
