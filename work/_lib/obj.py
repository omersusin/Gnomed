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

GRADIENTS (a gradient logo: Deezer bars, Instagram, Firefox ...): the measurement splits a
gradient into flat colour BANDS (r1, r2, ... in near colours). Drawn one by one they look
melted/broken. Use regions(slug) instead of parts()+colour(): bands of one gradient come back
merged as ONE shape with a Grad fill (a real gradient, measured from the source pixels):

    for name, g, fill in regions("myapp"):         # fill = "#hex" or Grad (works as a hex too)
        ...
    face = gradient("myapp", some_shape)            # the source's gradient under any shape

THE MARK ON EVERY STYLE (REDESIGN.md 5): put_mark(ic, "myapp", box) draws the measured mark
(mark_parts: without the tile under it) inside a layer named "mark"; gate `mark` checks it.
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
                                  "shape_of", "traced", "cutout", "body", "gradient", "regions", "banded",
                                  "mark_parts", "put_mark"]
__all__ = [n for n in __all__ if n != "poly"] + ["poly"]


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
    r0, r1, ... (colour regions, biggest first), 'silhouette' (the whole mark), 'holes'.
    `silhouette` has NO holes - never draw it as an object; use body()."""
    g = _geometry(slug)
    return {k: shape_of(v["d"]) for k, v in g["parts"].items()}


def body(slug):
    """The mark as ONE object: the union of all colour regions with the source's holes
    cut out (letter counters, eyes, a ring's centre stay transparent - REDESIGN.md 5)."""
    P = parts(slug)
    g = unary_union([v for k, v in P.items() if k not in ("silhouette", "holes")]).buffer(0)
    if "holes" in P and not P["holes"].is_empty:
        g = g.difference(P["holes"])
    return g


def poly(points, r=0, mode="fillet"):
    """A polygon with rounded corners. mode="fillet" (default): every corner gets its own
    arc whose radius is capped by half of the two edges next to it, so convex corners are
    rounded and thin parts (a boot toe, a spike) are NEVER erased. mode="open": the old
    buffer(-r).buffer(r) rounding, which removes parts thinner than 2r."""
    import numpy as _np
    p = Polygon(points).buffer(0)
    if not r:
        return p
    if mode == "open":
        return rounded(p, r)
    pts = [_np.array(q, float) for q in points]
    if len(pts) > 1 and _np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]
    out = []
    n = len(pts)
    for i in range(n):
        prev, cur, nxt = pts[i - 1], pts[i], pts[(i + 1) % n]
        a_, b_ = prev - cur, nxt - cur
        la, lb = _np.linalg.norm(a_), _np.linalg.norm(b_)
        if la < 1e-9 or lb < 1e-9:
            continue
        a_, b_ = a_ / la, b_ / lb
        theta = _np.arccos(_np.clip(a_ @ b_, -1, 1))          # angle between the two edges
        if theta < 1e-3 or abs(theta - _np.pi) < 1e-3:
            out.append(tuple(cur))
            continue
        d = min(r / _np.tan(theta / 2), 0.5 * la, 0.5 * lb)    # tangent distance, capped
        reff = d * _np.tan(theta / 2)
        bis = (a_ + b_) / _np.linalg.norm(a_ + b_)
        c = cur + bis * (reff / _np.sin(theta / 2))
        p1, p2 = cur + a_ * d, cur + b_ * d
        t1, t2 = _np.arctan2(*(p1 - c)[::-1]), _np.arctan2(*(p2 - c)[::-1])
        dt = (t2 - t1 + _np.pi) % (2 * _np.pi) - _np.pi        # the short way round
        for t in _np.linspace(0, 1, 9):
            ang = t1 + dt * t
            out.append((c[0] + reff * _np.cos(ang), c[1] + reff * _np.sin(ang)))
    return Polygon(out).buffer(0)


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
    try:
        groups = [(n, f) for n, _, f in regions(slug) if "+" in n]
    except Exception as e:                      # never let the description fail
        groups, lines = [], lines + [f"  (gradient measurement skipped: {e})"]
    for n, f in groups:
        st = " -> ".join(c for _, c in f.stops) if isinstance(f, Grad) else f
        lines.append(f"GRADIENT: {n.replace('+', ', ')} are bands of ONE gradient ({st}). Never draw them "
                     f"one by one with colour(): use regions({slug!r}) - it gives them as one part "
                     f"named {n!r} with a real gradient (Grad).")
    sb = P["silhouette"].bounds if "silhouette" in P and not P["silhouette"].is_empty else (0, 0, 0, 0)
    if (sb[2] - sb[0]) > 118 and (sb[3] - sb[1]) > 118 and len(info["regions"]) >= 4:
        lines.append("WARNING: the measured parts cover the whole tile - this is a POSTER / game art, "
                     "not a logo. Follow REDESIGN.md 3b: get >= 2 in-game screenshots (ask in Q1 if you "
                     "have none), draw the game's scene with its composition and count, serious "
                     "materials, no toy look; never trace the poster, never draw characters from memory alone.")
    return "\n".join(lines)


def _lab(rgb):
    from skimage.color import rgb2lab
    return rgb2lab(np.clip(rgb, 0, 1).reshape(-1, 1, 3)).reshape(-1, 3)


def _fit_grad(a, s, mask, flat_de=6.0, n_max=40000):
    """Least-squares linear colour plane over the source pixels in `mask` (bool, image size).
    -> (fill, rms_dE, rms_flat): fill = Grad (3 stops along the main direction of change, spanning the
    pixels) or "#hex" when the area is flat (end colours closer than flat_de)."""
    import math
    from scipy import ndimage
    m = mask & (a[..., 3] > 0.5)
    core = ndimage.binary_erosion(m, iterations=2)          # anti-aliased edges are not the gradient
    if core.sum() >= 0.3 * m.sum() and core.sum() > 50:
        m = core
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None, 99.0, 99.0
    if len(xs) > n_max:
        k = np.random.default_rng(0).choice(len(xs), n_max, replace=False)
        ys, xs = ys[k], xs[k]
    X, Y = xs * s, ys * s
    rgb = a[ys, xs, :3].astype(np.float64)
    A = np.c_[X, Y, np.ones_like(X)]
    coef = np.linalg.lstsq(A, rgb, rcond=None)[0]
    L = _lab(rgb)
    rms = float(np.sqrt(np.mean(np.sum((L - _lab(A @ coef)) ** 2, axis=1))))
    rms_flat = float(np.sqrt(np.mean(np.sum((L - L.mean(axis=0)) ** 2, axis=1)))) + 1e-9
    hexc = lambda c: "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in np.clip(c, 0, 1))  # noqa: E731
    J = coef[:2].T
    u = np.linalg.svd(J, full_matrices=False)[2][0]
    if u[1] < -1e-9 or (abs(u[1]) <= 1e-9 and u[0] < 0):
        u = -u                                            # always top->bottom / left->right
    t = X * u[0] + Y * u[1]
    lo, hi = np.percentile(t, 0.5), np.percentile(t, 99.5)
    cx, cy = X.mean(), Y.mean()
    tc = cx * u[0] + cy * u[1]
    at = lambda tt: coef[0] * (cx + (tt - tc) * u[0]) + coef[1] * (cy + (tt - tc) * u[1]) + coef[2]  # noqa: E731
    c0, c1 = at(lo), at(hi)
    if np.linalg.norm(_lab(c0) - _lab(c1)) < flat_de:
        return hexc(rgb.mean(axis=0)), rms, rms_flat
    stops = [(0, hexc(c0)), (0.5, hexc(at((lo + hi) / 2))), (1, hexc(c1))]
    return Grad(stops, math.degrees(math.atan2(u[1], u[0]))), rms, rms_flat


def gradient(slug, shape, flat_de=6.0):
    """The source's colour under `shape` (0..128 source space, e.g. P["r2"] or a union of
    bands) as ONE fill: a Grad when the source has a gradient there, else "#hex".
    Use it as face= of solid()/recess(); it spans whatever shape you draw (after fit())."""
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import gtrace as gt
    a, s = gt.load(ROOT / "work" / slug)
    fill, _, _ = _fit_grad(a, s, gt.render_mask(geom_d(shape), a.shape[0]), flat_de)
    return fill


def regions(slug, flat_de=6.0):
    """The measured mark as drawable parts [(name, shape, fill)], biggest first.
    Touching colour regions that are BANDS OF ONE source gradient (the colour runs on
    smoothly across their border) are merged back into one part (name "r1+r2") whose fill
    is a measured Grad - never draw such bands one by one. A single region with a clear
    gradient inside gets a Grad too. fill is "#hex" or Grad (a str: works as a hex too).
    Cached in work/<slug>/gradients.json (redone when geometry.json changes)."""
    import hashlib
    import json
    gp = ROOT / "work" / slug / "geometry.json"
    key = hashlib.sha1(gp.read_bytes()).hexdigest()[:16] + f"-v3-{flat_de}"
    cache = ROOT / "work" / slug / "gradients.json"
    P = parts(slug)
    names = [r["name"] for r in _geometry(slug)["info"].get("regions", []) if r["name"] in P and not P[r["name"]].is_empty]
    if not names:
        return []                                   # hand-built source without colour regions
    if cache.exists():
        c = json.loads(cache.read_text())
        if c.get("key") == key:
            out = []
            for n, f in c["parts"]:
                g = unary_union([P[k] for k in n.split("+")]).buffer(0)
                out.append((n, g, Grad([tuple(x) for x in f["stops"]], f["angle"]) if isinstance(f, dict) else f))
            return out
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import gtrace as gt
    a, s = gt.load(ROOT / "work" / slug)
    H = a.shape[0]
    opaque = a[..., 3] > 0.5
    mask = lambda g: gt.render_mask(geom_d(g), H) & opaque if not g.is_empty else np.zeros((H, H), bool)  # noqa: E731
    masks = {n: mask(P[n]) for n in names}
    lab_img = None

    def mean_lab(m):
        nonlocal lab_img
        if lab_img is None:
            lab_img = _lab(a[..., :3]).reshape(H, H, 3)
        return lab_img[m].mean(axis=0) if m.sum() >= 20 else None

    def hexlab(h):
        return _lab(np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]))[0]

    parent = {n: n for n in names}

    def root(n):
        while parent[n] != n:
            n = parent[n]
        return n

    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            if root(n1) == root(n2) or P[n1].distance(P[n2]) > 1.0:
                continue
            l1, l2 = hexlab(colour(slug, n1)), hexlab(colour(slug, n2))
            if (l1[1] ** 2 + l1[2] ** 2) ** 0.5 < 12 or (l2[1] ** 2 + l2[2] ** 2) ** 0.5 < 12:
                continue                                    # white / grey / black are never bands
            full = np.linalg.norm(l1 - l2)
            if full < 3 or full > 70:
                continue
            # the pixels on both sides of the shared border: a gradient runs on smoothly
            # (small jump), two different colours jump by their full difference
            z1 = mean_lab(mask(P[n1].intersection(P[n2].buffer(1.5)).difference(P[n2])))
            z2 = mean_lab(mask(P[n2].intersection(P[n1].buffer(1.5)).difference(P[n1])))
            if z1 is None or z2 is None:
                continue
            if np.linalg.norm(z1 - z2) < 0.45 * full:
                parent[root(n2)] = root(n1)
    groups = {}
    for n in names:
        groups.setdefault(root(n), []).append(n)
    out = []
    for members in groups.values():
        members.sort(key=names.index)
        m = np.zeros((H, H), bool)
        for k in members:
            m |= masks[k]
        fill, rms, rms_flat = _fit_grad(a, s, m, flat_de)
        if len(members) == 1 and not (isinstance(fill, Grad) and rms < 0.8 * rms_flat):
            fill = colour(slug, members[0])                 # flat, or no clean gradient inside
        elif fill is None:
            fill = colour(slug, members[0])
        out.append(("+".join(members), unary_union([P[k] for k in members]).buffer(0), fill))
    out.sort(key=lambda t: -t[1].area)
    cache.write_text(json.dumps({"key": key, "parts": [
        [n, {"stops": f.stops, "angle": f.angle} if isinstance(f, Grad) else f] for n, _, f in out]}, indent=1))
    return out


def mark_parts(slug, de=25.0):
    """The app's MARK without the tile under it: regions(slug) minus the parts in the source's
    ground colour (the tile / gradient behind the logo - Soundcore's blue bands). Measured holes
    (letter counters) are cut out. -> [(name, shape, fill)]. This is what the owner wants to
    see on EVERY style (REDESIGN.md 5, 2026-11-22: Apple Music and Soundcore lost it);
    put_mark() draws it, gate `mark` (check_icon.py) looks for it."""
    import numpy as np
    P = parts(slug)
    R = regions(slug)
    if not R:                                      # hand-built source: every measured part
        R = [(k, g, "#241f31") for k, g in P.items() if k not in ("silhouette", "holes") and not g.is_empty]
    gr = _geometry(slug).get("info", {}).get("ground") or {}
    hexes = [gr[k] for k in ("c0", "c1") if isinstance(gr.get(k), str)] or \
        ([gr["color"]] if isinstance(gr.get("color"), str) else [])

    def lab(h):
        h = str.__str__(h)
        return _lab(np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]))[0]
    keep = R
    if hexes:
        a, b = lab(hexes[0]), lab(hexes[-1])

        def dist(p):
            ab = b - a
            t = float(np.clip((p - a) @ ab / max(float(ab @ ab), 1e-9), 0, 1))
            return float(np.linalg.norm(p - (a + t * ab)))
        keep = [r for r in R if dist(lab(r[2])) > de] or R
    skip = {str(n) for n in (gr.get("mark_skip") or [])}
    if skip:                                       # measured ground parts the heuristic missed
        keep = [r for r in keep if not (set(r[0].split("+")) & skip)]
    forced = {str(n) for n in (gr.get("mark_keep") or [])}
    if forced:                                     # a mark the heuristic threw away as ground
        have = {r[0] for r in keep}
        keep += [r for r in R if (set(r[0].split("+")) & forced) and r[0] not in have]
    mb = gr.get("mark_holes")                       # the mark lives in the measured holes (white
    if isinstance(mb, (list, tuple)) and len(mb) == 4:   # letters on a dark object)
        from shapely.geometry import box as _box
        hl = P.get("holes")
        if hl is not None and not hl.is_empty:
            g = hl.intersection(_box(*[float(v) for v in mb]))
            if not g.is_empty:
                return [("holes", g, gr.get("mark_color") or "#ffffff")]
    crop = gr.get("mark_crop")                      # a tile edge / shadow line merged into the mark
    if isinstance(crop, (list, tuple)) and len(crop) == 4:
        from shapely.geometry import box as _box
        c = _box(*[float(v) for v in crop])
        keep = [(n, g.intersection(c), f) for n, g, f in keep]
        keep = [(n, g, f) for n, g, f in keep if not g.is_empty]
    holes = P.get("holes")
    if holes is not None and not holes.is_empty:
        keep = [(n, g.difference(holes), f) for n, g, f in keep]
    return keep


def put_mark(ic, slug, box_, depth=0, anchor="center", face=None, side=None, layer="mark"):
    """Draw the app's measured mark (mark_parts) fitted into box_ = (x0, y0, x1, y1), inside a
    layer named 'mark' - the gate `mark` finds it there and checks size, contrast and shape.
        put_mark(ic, SLUG, record_label(64, 118, 100), face="#ffffff")   # white mark on a label
        put_mark(ic, SLUG, (14, 12, 114, 112), depth=6, anchor="bottom") # L1: the mark IS the object
    face: one colour for every part (a white mark on a dark lid ...); default the measured
    colours. depth > 0: a solid part with a side. -> the placed shapes."""
    M = mark_parts(slug)
    shapes = fit([g for _, g, _ in M], box_, anchor=anchor)
    with ic.group(layer):
        for i, (g, (_, _, f)) in enumerate(zip(shapes, M)):
            fill = face or f
            if depth:
                solid(ic, g, face=fill, depth=depth, side=side, layer=f"{layer}-{i}")
            else:
                ic.path(geom_d(g), _skill._fill(ic, fill, g), layer_id=f"{layer}-{i}", fill_rule="evenodd")
    return shapes


def banded(slug, svg_text, de=8.0):
    """Gradient bands painted flat in an SVG: for every part regions() merged ("r1+r2"),
    the members whose measured colour appears (within dE `de`) as a FLAT fill in svg_text.
    -> [("r1+r2", ["#hex", "#hex"]), ...] - only groups with 2+ members found. Empty = fine.
    Used by tools/check_icon.py (check `bands`) and tools/concepts.py."""
    import re
    flats = sorted(set(h.lower() for h in re.findall(r'fill="(#[0-9a-fA-F]{6})"', svg_text)))
    if not flats:
        return []
    fl = _lab(np.array([[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)] for h in flats]))
    out = []
    for name, _, _ in regions(slug):
        if "+" not in name:
            continue
        found = []
        for k in name.split("+"):
            h = colour(slug, k)
            d = np.linalg.norm(fl - _lab(np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])), axis=1)
            if d.min() < de:
                found.append(flats[int(d.argmin())])
        if len(set(found)) >= 2:
            out.append((name, sorted(set(found))))
    return out


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


def traced(slug, box_, n=6, exclude=(), smooth=0.5, min_share=0.004, keep=None, gradients=True):
    """Trace the recognisable element of a POSTER/illustration straight from the source
    (measurement, not memory): the pixels inside box_ (x0, y0, x1, y1 in the 0..128 source
    space) are reduced to `n` colours and each colour is traced. Colours within dE 18 of
    an `exclude` hex (the background) are skipped; `keep` = a shape: only pixels inside it.
    -> [(shape, fill), ...] biggest first, in source space (place them with fit()).
    gradients=True (default): a gradient in the source is NOT cut into flat bands - each
    connected piece whose colours run on smoothly comes back as ONE shape with a measured
    Grad fill (a str: works as a hex). Draw with solid()/recess()/cutout(), which paint
    Grad as a real gradient (ic.path() would paint only its middle colour)."""
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
    keep_c = [c for c in range(len(cent)) if not any(np.linalg.norm(cent[c] - e) < 18 for e in excl)]
    hexs = {c: "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in
                                       np.clip(lab2rgb(cent[c].reshape(1, 1, 3)).reshape(3), 0, 1)) for c in keep_c}
    pieces = []                                  # (mask, fill)
    if gradients:
        from scipy import ndimage
        fg = m & np.isin(lbl, keep_c)
        comp, nc = ndimage.label(fg)
        for k in range(1, nc + 1):
            cm = comp == k
            if cm.sum() < min_share * m.sum():
                continue
            cs = [c for c in keep_c if (cm & (lbl == c)).sum() >= 0.05 * cm.sum()]
            if len(cs) <= 1:                     # one colour (plus edge pixels): the whole piece
                fill, rms, rms_flat = _fit_grad(a, s, cm)
                dom = max(keep_c, key=lambda c: (cm & (lbl == c)).sum())
                pieces.append((cm, fill if isinstance(fill, Grad) and rms < 0.8 * rms_flat else hexs[dom]))
                continue
            if len(cs) >= 2:
                # several clusters in one piece: one gradient, or really different colours?
                # a gradient runs on smoothly: neighbouring pixels across the cluster borders
                # differ little compared with the clusters' own colour difference
                core = ndimage.binary_erosion(cm, iterations=3)   # not the anti-aliased rim
                sub = lbl * core + (-1) * (~core)
                jumps, fulls = [], []
                for dy, dx in ((0, 1), (1, 0)):
                    a1, a2 = sub[: sub.shape[0] - dy, : sub.shape[1] - dx], sub[dy:, dx:]
                    e = (a1 != a2) & (a1 >= 0) & (a2 >= 0)
                    if e.any():
                        l1 = lab[: lab.shape[0] - dy, : lab.shape[1] - dx][e]
                        l2 = lab[dy:, dx:][e]
                        jumps.append(np.linalg.norm(l1 - l2, axis=1))
                        fulls.append(np.linalg.norm(cent[a1[e]] - cent[a2[e]], axis=1))
                smooth_run = bool(jumps) and np.median(np.concatenate(jumps)) < 0.3 * np.median(np.concatenate(fulls))
                if smooth_run:
                    fill, _, _ = _fit_grad(a, s, cm)
                    pieces.append((cm, fill or hexs[cs[0]]))
                    continue
            for c in cs or keep_c:
                cc = cm & (lbl == c)
                if cc.sum() >= min_share * m.sum():
                    pieces.append((cc, hexs[c]))
    else:
        for c in keep_c:
            cc = m & (lbl == c)
            if cc.sum() >= min_share * m.sum():
                pieces.append((cc, hexs[c]))
    out = []
    for cm, fill in pieces:
        g = shape_of(gt.trace_mask(cm, s, smooth_u=smooth))
        if not g.is_empty:
            out.append((g, fill, int(cm.sum())))
    out.sort(key=lambda t: -t[2])
    return [(g, h) for g, h, _ in out]


def cutout(ic, regions, depth=5, side=None, layer="cut"):
    """Draw traced regions as ONE die-cut object: the union gets a side `depth` px deep
    (colour: `side` or the darkest region darkened), then every region on top, top light.
    A Grad fill (from traced()/regions()) is painted as a real gradient."""
    from gnome_kit import shade
    body = unary_union([g for g, _ in regions]).buffer(0.6).buffer(-0.6)
    dark = side or shade(str.__str__(min((h for _, h in regions), key=lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5)))), -0.25)
    solid(ic, body, face=dark, depth=depth, side=dark, top=False, layer=f"{layer}-body")
    for i, (g, h) in enumerate(regions):
        ic.path(geom_d(g), _skill._fill(ic, h, g), layer_id=f"{layer}-{i}", fill_rule="evenodd")
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
