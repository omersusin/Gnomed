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
                                  "shape_of", "traced", "cutout"]


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
        lines.append("WARNING: the measured parts cover the whole tile - this is a POSTER / game art, "
                     "not a logo. Follow REDESIGN.md 3b: get >= 2 in-game screenshots (ask in Q1 if you "
                     "have none), draw the game's scene with its composition and count, serious "
                     "materials, no toy look; never trace the poster, never draw characters from memory alone.")
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


def traced(slug, box_, n=6, exclude=(), smooth=0.5, min_share=0.004, keep=None):
    """Trace the recognisable element of a POSTER/illustration straight from the source
    (measurement, not memory): the pixels inside box_ (x0, y0, x1, y1 in the 0..128 source
    space) are reduced to `n` colours and each colour is traced. Colours within dE 18 of
    an `exclude` hex (the background) are skipped; `keep` = a shape: only pixels inside it.
    -> [(shape, "#hex"), ...] biggest first, in source space (place them with fit())."""
    import numpy as np
    from scipy.cluster.vq import kmeans2
    from skimage.color import rgb2lab, lab2rgb
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import gtrace as gt
    a, s = gt.load(ROOT / "work" / slug)
    H, W = a.shape[:2]
    x0, y0, x1, y1 = [int(round(v / s)) for v in box_]
    m = np.zeros((H, W), bool)
    m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = True
    m &= a[..., 3] > 0.5
    if keep is not None:
        from shapely import affinity as _af
        km = gt.render_mask(geom_d(_af.scale(keep, 1, 1, origin=(0, 0))), H)
        m &= km
    lab = rgb2lab(np.clip(a[..., :3], 0, 1))
    pix = lab[m]
    rng = np.random.default_rng(0)
    sample = pix[rng.choice(len(pix), min(len(pix), 30000), replace=False)].astype(np.float64)
    cent, _ = kmeans2(sample, n, minit="++", seed=0)
    lbl = np.argmin(np.linalg.norm(lab[..., None, :] - cent[None, None], axis=-1), axis=-1)
    excl = [rgb2lab(np.array([[[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0] for h in exclude]
    out = []
    for c in range(len(cent)):
        if any(np.linalg.norm(cent[c] - e) < 18 for e in excl):
            continue
        cm = m & (lbl == c)
        if cm.sum() < min_share * m.sum():
            continue
        rgb = np.clip(lab2rgb(cent[c].reshape(1, 1, 3)).reshape(3), 0, 1)
        hx = "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in rgb)
        g = shape_of(gt.trace_mask(cm, s, smooth_u=smooth))
        if not g.is_empty:
            out.append((g, hx, int(cm.sum())))
    out.sort(key=lambda t: -t[2])
    return [(g, h) for g, h, _ in out]


def cutout(ic, regions, depth=5, side=None, layer="cut"):
    """Draw traced regions as ONE die-cut object: the union gets a side `depth` px deep
    (colour: `side` or the darkest region darkened), then every region on top, top light."""
    from gnome_kit import shade
    body = unary_union([g for g, _ in regions]).buffer(0.6).buffer(-0.6)
    dark = side or shade(min((h for _, h in regions), key=lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5))), -0.25)
    solid(ic, body, face=dark, depth=depth, side=dark, top=False, layer=f"{layer}-body")
    for i, (g, h) in enumerate(regions):
        ic.path(geom_d(g), h, layer_id=f"{layer}-{i}", fill_rule="evenodd")
    toplight(ic, body, layer=layer)
    return body


def save_styles(slug, icons):
    """Write work/<slug>/<slug>-<style>.svg for ALL four slots (REDESIGN.md 6):
    icons = {"symbol": main, "faithful": kept, "disc": kept, "rimmed": kept} - the MAIN
    design (symbol; or faithful when no symbol is given) also fills every slot without a
    design of its own, so an app in the pack loses its old plate/disc/rim versions."""
    w = ROOT / "work" / slug
    main = icons.get("symbol") or icons.get("faithful") or next(iter(icons.values()))
    for st in ("faithful", "disc", "rimmed", "symbol"):
        out = w / f"{slug}-{st}.svg"
        (icons.get(st) or main).save(out)
        print("wrote", out.relative_to(ROOT), "" if st in icons else "(= main design)")
