"""Object-building helpers for Gnomed REDESIGNS (REDESIGN.md).

Everything comes from the vendored skill (tools/gnome-android-icons/scripts/obj.py:
solid, recess, hole, toplight, shapely shapes, geom_d); this file only adds the
repository part: save_styles() for work/<slug>/<slug>-<style>.svg.

    from obj import *
    ic = gk.Icon("App - Gnomed")
    solid(ic, rounded(box(20, 30, 108, 110), 10), face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=6)
    save_styles("myapp", {"faithful": ic})

Using the MEASURED source (never draw a logo from memory):

    P = parts("myapp")              # {"r0": shape, "r1": ..., "silhouette": ..., "holes": ...}
    print(describe("myapp"))        # every part: colour, size, position (text, no image needed)
    a, b = fit([P["r0"], P["r1"]], (24, 30, 104, 110))   # scale+move together, aspect kept
    solid(ic, a, face=colour("myapp", "r0"), depth=4)
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_SK = ROOT / "tools/gnome-android-icons/scripts"
sys.path.insert(0, str(_SK))
_spec = importlib.util.spec_from_file_location("_skill_obj", _SK / "obj.py")
_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_skill)
globals().update({k: getattr(_skill, k) for k in _skill.__all__})

__all__ = list(_skill.__all__) + ["save_styles", "ROOT", "parts", "colour", "describe", "fit",
                                  "shape_of"]


def shape_of(d, samples=400):
    """An SVG path 'd' (from geometry.json) -> one shapely shape (holes kept)."""
    from svgpathtools import parse_path
    rings = []
    for sp in parse_path(d).continuous_subpaths():
        pts = [sp.point(i / samples) for i in range(samples)]
        p = Polygon([(q.real, q.imag) for q in pts]).buffer(0)
        if p.area > 0.01:
            rings.append(p)
    # even-odd: a ring inside another is a hole
    out = None
    for r in sorted(rings, key=lambda g: -g.area):
        out = r if out is None else (out.difference(r) if out.contains(r.representative_point()) and out.covers(r) else out.union(r))
    return out if out is not None else Polygon()


def _geometry(slug):
    import json
    gp = ROOT / "work" / slug / "geometry.json"
    if not gp.exists():
        raise SystemExit(f"work/{slug}/geometry.json missing - run: python3 tools/new_redesign.py {slug}")
    return json.loads(gp.read_text())


def parts(slug):
    """Every measured part of the source as a shapely shape in the source's 0..128 space:
    r0, r1, ... (colour regions, biggest first), 'silhouette' (the whole mark), 'holes'."""
    g = _geometry(slug)
    return {k: shape_of(v["d"]) for k, v in g["parts"].items()}


def colour(slug, name):
    """The measured colour (#hex) of part `name` (e.g. 'r0')."""
    for r in _geometry(slug)["info"]["regions"]:
        if r["name"] == name:
            return r["fill"]
    raise KeyError(f"{slug} has no part {name}")


def describe(slug):
    """Text description of the measured source - for models that cannot see images."""
    g = _geometry(slug)
    info = g["info"]
    gr = info.get("ground") or {}
    lines = [f"{slug}: tile = {gr.get('kind', 'none')} {gr.get('color', '')}"
             + (f" ({gr.get('c0')} -> {gr.get('c1')})" if gr.get("kind") == "gradient" else ""),
             "parts (source space 0..128, x0 y0 x1 y1):"]
    P = parts(slug)
    for r in info["regions"]:
        b = P[r["name"]].bounds
        lines.append(f"  {r['name']:10s} {r['fill']}  {r['area'] * 100:4.1f}% of tile  box {b[0]:.0f} {b[1]:.0f} {b[2]:.0f} {b[3]:.0f}")
    for k in ("silhouette", "holes"):
        if k in P and not P[k].is_empty:
            b = P[k].bounds
            lines.append(f"  {k:10s}           box {b[0]:.0f} {b[1]:.0f} {b[2]:.0f} {b[3]:.0f}")
    sb = P["silhouette"].bounds if "silhouette" in P and not P["silhouette"].is_empty else (0, 0, 0, 0)
    if (sb[2] - sb[0]) > 118 and (sb[3] - sb[1]) > 118 and len(info["regions"]) >= 4:
        lines.append("WARNING: the measured parts cover the whole tile - this is a POSTER / illustration, "
                     "not a logo. Stop and ask the owner (AGENTS.md B): free adaptation of ONE element "
                     "he names, built from primitives in the measured colours.")
    return "\n".join(lines)


def fit(shapes, box_, keep_aspect=True, anchor="center"):
    """Scale + move `shapes` TOGETHER (one unit, layout kept) so their union fits
    box_ = (x0, y0, x1, y1). anchor="center" centres it (a mark ON an object);
    anchor="bottom" puts its bottom on the box's bottom edge (a free object standing on
    the baseline: use a box bottom of 118 minus the side depth). Same order returned."""
    u = unary_union([s for s in shapes if not s.is_empty])
    x0, y0, x1, y1 = u.bounds
    bx0, by0, bx1, by1 = box_
    sx, sy = (bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0)
    if keep_aspect:
        sx = sy = min(sx, sy)
    tx = (bx0 + bx1) / 2 - sx * (x0 + x1) / 2
    ty = (by0 + by1) / 2 - sy * (y0 + y1) / 2
    if anchor == "bottom":
        ty = by1 - sy * y1
    return [affinity.translate(affinity.scale(s, sx, sy, origin=(0, 0)), tx, ty) for s in shapes]


def save_styles(slug, icons):
    """Write work/<slug>/<slug>-<style>.svg for the given styles.  A style NOT given is
    overwritten with the primary ONLY if an old (pre-redesign) SVG of it exists, so no
    old logo-on-plate version survives in the pack after tools/pack_refresh.py."""
    w = ROOT / "work" / slug
    primary = icons.get("faithful") or next(iter(icons.values()))
    for st in ("faithful", "disc", "rimmed", "symbol"):
        out = w / f"{slug}-{st}.svg"
        if st in icons:
            icons[st].save(out)
        elif out.exists():
            primary.save(out)
        else:
            continue
        print("wrote", out.relative_to(ROOT))
