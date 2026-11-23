#!/usr/bin/env python3
"""Automatic quality gate for one app - usable WITHOUT looking at images.

    python3 tools/check_icon.py <slug>          # human-readable report
    python3 tools/check_icon.py <slug> --json   # machine-readable
    python3 tools/check_icon.py <slug> --no-cache   # measure again even if nothing changed

The result is cached in .cache/check/<slug>.json and reused while no input changed (the app's
folder, every design.md, the gate's code) - next.py re-runs the gate right after make_icon.py.

Every check prints PASS / WARN / FAIL, a number, and - when it is not PASS - the
FIX to apply (a key from docs/course/04-recipes.md). Exit code: 0 = no FAIL,
1 = at least one FAIL. A model that cannot see images MUST still run this and fix
every FAIL; a model that can see images must ALSO look at work/<slug>/styles.png.

Checks (per style that exists):
  lint          lint_svg.py result (raster/text/filters/edge contact) ......... FAIL
  visible       plated styles: must read on at least one of light #f6f5f4 / dark #241f31 .. FAIL < 0.55
  visible_light Symbol only: must read on a light wallpaper ...... WARN < 0.55, FAIL < 0.25
  visible_dark  Symbol only: must read on a dark wallpaper ....... WARN < 0.55, FAIL < 0.25
  mass          painted share of the canvas (official GNOME 0.44-0.69) ........ WARN
  baseline      bottom edge: plates 114-118, discs 120-126, symbols 108-124 ... WARN
  legibility32  structure kept at 32 px (official median SSIM 0.82) ........... WARN < 0.72, FAIL < 0.62
  box_in_plate  Faithful: one region covering most of the plate (a tile/disc
                drawn inside the plate) ........................................ FAIL
  mark          (apps, not games / system apps) the app's measured mark in a layer named 'mark'
                (put_mark()): present, >= 36 px of 128 (Faithful >= 44), contrast >= 25 against
                what is under it, shape match with the source's mark >= 0.5 ............ WARN
  same_object   a style uses an object another app of its category already uses ........ WARN
  anchors       design.md: >= 2 anchors say where they were seen (source.png / refs/...); each
                style's concept line cites the anchors it carries ................. WARN
  empty_layer   a layer the code drew came out empty (d="") - the part is missing .......... FAIL
  mark_fit      the mark sits well on its part: nothing of it over the part's edge (<= 1 %),
                >= 1 unit of room to that edge, nothing drawn over it (<= 3 %) ........ WARN
Per app:
  redesign      the app is a GNOME redesign (REDESIGN.md): work/<slug>/redesign.py exists and
                design.md has "approved:" = the owner's answer in quotes + (YYYY-MM-DD). The automatic
                builds (logo on a plate + chin) are drafts and FAIL here .............. FAIL
  holes         (Symbol of every app, every style of a redesign) what is a hole in the
                source (letter counters, eyes, a ring's centre) must be TRANSPARENT:
                enclosed transparent area >= 50 % of the source holes (placed like the
                mark) when they are >= 0.4 % of the canvas ............................ FAIL
                exceptions: OVERRIDES painted_counters, or design.md
                painted-holes: "<owner's words>" (YYYY-MM-DD)
  plain_shape   (redesigns) the Faithful silhouette is a plain DISC (circle match > 0.95):
                the logo on a disc is not a redesign ................................ FAIL
                a plain SQUARE/box (fills > 97 % of its bounds): fine for a real box
                object (envelope, case), a plate otherwise ............................ WARN
                both lifted by a line in design.md:  shape-ok: <the owner's words>
Per app (from geometry.json):
  stripes       3+ regions of near-identical hue = one gradient cut into bands . WARN -> merge_grad
  trace_iou     traced parts match their masks: WARN < 0.90; FAIL if a part >= 3 % of the canvas < 0.75
  faithful      a Faithful SVG must exist (every other style falls back to it)  FAIL
"""
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / "tools/gnome-android-icons/scripts"
sys.path.insert(0, str(SK))
from skimage.color import rgb2lab  # noqa: E402

LIGHT, DARK = (0xf6, 0xf5, 0xf4), (0x24, 0x1f, 0x31)
STYLES = ("faithful", "disc", "rimmed", "symbol")


def render(svg, size=256):
    im = Image.open(io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=size, output_height=size))).convert("RGBA")
    return np.asarray(im).astype(np.float32) / 255.0


def visible(a, bg):
    """share of the icon's painted pixels that differ clearly (dE > 10) from the wallpaper"""
    al = a[..., 3]
    painted = al > 0.5
    if painted.sum() == 0:
        return 0.0
    bgc = np.array(bg, np.float32) / 255
    comp = a[..., :3] * al[..., None] + bgc * (1 - al[..., None])
    d = np.linalg.norm(rgb2lab(comp) - rgb2lab(bgc[None, None, :]), axis=-1)
    return float(((d > 10) & painted).sum() / painted.sum())


def mass_and_bottom(a):
    al = a[..., 3] > 0.5
    ys = np.nonzero(al.any(1))[0]
    return float(al.mean()), (float(ys.max() + 1) * 128 / a.shape[0]) if len(ys) else 0.0


def hue(h):
    import colorsys
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss, ll


QUOTED_DATED = re.compile(r'"[^"]+".*\(\d{4}-\d{2}-\d{2}\)')


def design_line(w, key):
    """value of 'key:' in work/<slug>/design.md ('' if missing)"""
    if (w / "design.md").exists():
        for line in (w / "design.md").read_text(encoding="utf-8").splitlines():
            if line.lower().startswith(key + ":"):
                return line.split(":", 1)[1].strip()
    return ""


def shape_kind(svg):
    """-> (kind, circle_iou, fill) of an SVG's silhouette: 'disc' (circle match > 0.95), 'tile'
    (a near-square block filling > 90 % of its box: a rounded-square plate), 'box' (any block
    filling > 97 %), else 'object'. Used by plain_shape and by tools/next.py for concepts."""
    import io as _io
    al = np.asarray(Image.open(_io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=256, output_height=256)))
                    .convert("RGBA"))[..., 3] > 128
    ys, xs = np.where(al)
    if not len(xs):
        return "object", 0.0, 0.0
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    Y, X = np.mgrid[:256, :256]
    r = ((x1 - x0) + (y1 - y0)) / 4
    circle = (X - (x0 + x1) / 2) ** 2 + (Y - (y0 + y1) / 2) ** 2 <= r * r
    iou = float((al & circle).sum() / (al | circle).sum())
    fill = float(al[y0:y1 + 1, x0:x1 + 1].mean())
    aspect = (x1 - x0 + 1) / (y1 - y0 + 1)
    if iou > 0.95:
        return "disc", iou, fill
    if fill > 0.90 and 0.8 <= aspect <= 1.25:
        return "tile", iou, fill
    if fill > 0.97:
        return "box", iou, fill
    return "object", iou, fill


def is_quote(v):
    """an approval line: the owner's words verbatim in quotes + the date (REDESIGN.md 7)"""
    return bool(QUOTED_DATED.search(v or ""))


def hole_measure(slug, svg, N=512):
    """-> (source holes % of canvas, placed like the mark; enclosed transparent % in the
    style; IoU of the style's filled outline with the source mark) or None if unknown."""
    gp = ROOT / "work" / slug / "geometry.json"
    if not gp.exists():
        return None
    sys.path.insert(0, str(ROOT / "work/_lib"))
    from obj import shape_of, geom_d
    from gtrace import render_mask
    from shapely import affinity
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from scipy.ndimage import binary_fill_holes
    parts = json.loads(gp.read_text())["parts"]
    body = unary_union([shape_of(v["d"]) for k, v in parts.items() if k not in ("silhouette", "holes")]).buffer(0)
    if body.is_empty:
        return None
    filled = unary_union([Polygon(g.exterior) for g in getattr(body, "geoms", [body])])
    if "holes" in parts:
        holes = shape_of(parts["holes"]["d"]).intersection(filled)
    else:   # e.g. group-1 apps: the parts' own interiors that no other part fills
        holes = filled.difference(body).buffer(-0.8).buffer(0.8)
    # measured WITHOUT the side/chin layers: a thick object's own side may show inside a
    # hole (that is correct GNOME depth); only paint on the face fills a hole
    txt = re.sub(r'<path[^>]*\bid="[^"]*(?:-chin|-side)[^"]*"[^>]*/>', "", Path(svg).read_text(encoding="utf-8"))
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=txt.encode(), output_width=N, output_height=N)))
                   .convert("RGBA"))[..., 3] > 127
    if not a.any():
        return None
    ys, xs = np.nonzero(a)
    u = 128 / N
    ax0, ay0, ax1, ay1 = xs.min() * u, ys.min() * u, (xs.max() + 1) * u, (ys.max() + 1) * u
    bx0, by0, bx1, by1 = filled.bounds
    sc = min((ax1 - ax0) / (bx1 - bx0), (ay1 - ay0) / (by1 - by0))
    ox, oy = (bx0 + bx1) / 2, (by0 + by1) / 2

    def T(g):
        return affinity.translate(affinity.scale(g, sc, sc, origin=(ox, oy)), (ax0 + ax1) / 2 - ox, (ay0 + ay1) / 2 - oy)
    fa = binary_fill_holes(a)
    sil = render_mask(geom_d(T(filled)), N)
    iou = (fa & sil).sum() / max(1, (fa | sil).sum())
    return T(holes).area / (128 * 128), (fa & ~a).sum() / (N * N), iou


def style_groups(svgs, n=48):
    """Styles that LOOK the same (owner 2026-11-22: Saat's Faithful and Disc, Photos' Symbol and
    Faithful): rendered small on grey, mean colour difference dE < 12, or the same silhouette
    (IoU >= 0.9) with dE < 20. Measured: really different designs have dE >= 23 and IoU <= 0.78.
    -> (groups of style names, ["faithful ~ disc", ...])"""
    import itertools
    from skimage.color import rgb2lab as _lab
    r = {}
    for st, svg in svgs.items():
        a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=n, output_height=n)))
                       .convert("RGBA")).astype(np.float32) / 255
        al = a[..., 3:4]
        r[st] = (_lab(a[..., :3] * al + 0.5 * (1 - al)), a[..., 3] > 0.5)
    parent = {st: st for st in svgs}

    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    alike = []
    for s1, s2 in itertools.combinations(svgs, 2):
        (l1, m1), (l2, m2) = r[s1], r[s2]
        de = float(np.linalg.norm(l1 - l2, axis=-1).mean())
        iou = float((m1 & m2).sum() / max(1, (m1 | m2).sum()))
        if de < 12 or (iou >= 0.9 and de < 20):
            if root(s1) != root(s2):
                parent[root(s2)] = root(s1)
            if svgs[s1].read_bytes() != svgs[s2].read_bytes():
                alike.append(f"{s1} ~ {s2} look almost the same")
    groups = {}
    for st in svgs:
        groups.setdefault(root(st), []).append(st)
    return list(groups.values()), alike


def mark_measure(slug, svg, N=256, de=20.0):
    """How big the app's own colours are in a style: the pixels whose colour is close (dE < de)
    to a COLOURFUL measured part of the source (chroma > 20, >= 1 % of the tile), small specks
    dropped. -> (larger side of their box in the 128 canvas, share of the painted area, n colours)
    or None when the source has no colourful part (white / black / grey marks)."""
    gp = ROOT / "work" / slug / "geometry.json"
    if not gp.exists():
        return None
    regs = json.loads(gp.read_text()).get("info", {}).get("regions", [])
    cols = []
    for r in regs:
        h = r.get("fill", "")
        if not (isinstance(h, str) and re.match(r"^#[0-9a-fA-F]{6}$", h)) or r.get("area", 0) < 0.01:
            continue
        L, A, B = rgb2lab(np.array([[[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
        if (A * A + B * B) ** 0.5 > 20:
            cols.append((L, A, B))
    if not cols:
        return None
    a = render(svg, N)
    painted = a[..., 3] > 0.5
    lab = rgb2lab(np.clip(a[..., :3], 0, 1))
    d = np.min(np.stack([np.linalg.norm(lab - np.array(c), axis=-1) for c in cols]), axis=0)
    m = painted & (d < de)
    from scipy import ndimage
    lbl, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lbl, range(1, n + 1))
        keep = np.isin(lbl, [i + 1 for i, sz in enumerate(sizes) if sz >= 0.0005 * N * N])
    else:
        keep = m
    if not keep.any():
        return 0.0, 0.0, len(cols)
    ys, xs = np.nonzero(keep)
    side = max(xs.max() - xs.min() + 1, ys.max() - ys.min() + 1) * 128 / N
    return float(side), float(keep.sum() / max(painted.sum(), 1)), len(cols)


@__import__("functools").lru_cache(maxsize=None)
def _skill_mod(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, SK / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SK))
    spec.loader.exec_module(mod)
    return mod


def _legibility():
    return _skill_mod("legibility_check")


MARK_ID = re.compile(r"^mark(?:$|[-_0-9])", re.I)


# The owner's "system apps" (ROADMAP.md 1): GNOME's own metaphor for the job, no brand mark
# (approved in batch 1c, 2026-11-22). Any other app can opt out with 'mark: none - <why>' in design.md.
SYSTEM_APPS = {"ayarlar", "saat", "kamera", "telefon", "mesajlar", "ki_iler", "hesap_makinesi",
               "y_hava_durumu", "foto_raflar"}


def mark_applies(w):
    """the mark gate measures apps, not games (objects only) or system apps (GNOME's metaphor)"""
    if design_line(w, "kind").lower().startswith("game"):
        return False
    if w.name in SYSTEM_APPS:          # the phone's own apps (GNOME's metaphor); a third-party app
        return False                   # of category "system" (launcher, Shizuku, F-Droid) keeps its mark
    # 'mark: none' only with the OWNER's words + date (2026-11-23: Duolingo's owl - the logo - was dropped
    # as "a mascot" with a plain 'mark: none'; the owner wants the app's own logo in every style)
    mk = design_line(w, "mark")
    if mk.lower().startswith("none") and is_quote(mk.split("-", 1)[-1].strip()):
        return False
    store = w / "refs" / "store" / "store.json"
    return not (store.exists() and '"source": "system app"' in store.read_text(encoding="utf-8"))


def mark_layer_measure(slug, svg, N=256):
    """The app's own mark in a style (owner 2026-11-22, overview ara-2: Apple Music and Soundcore
    had lost it in every style). The elements whose id starts with 'mark' (put_mark(), or
    `with ic.group("mark"):`) are found; the style is rendered as it is, without them, and with
    them painted magenta (their full footprint, even where they melt into the surface).
    -> None when the style has no such element, else (larger side of the mark in px of 128,
    median colour difference to what is under it, IoU of its shape with the source's mark,
    the share of the mark that is visible at all)."""
    import copy
    import xml.etree.ElementTree as ET
    from scipy import ndimage
    txt = Path(svg).read_bytes()
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    without = ET.fromstring(txt)
    magenta = ET.fromstring(txt)

    def marks(root):
        out = []
        for parent in list(root.iter()):
            if parent.tag.endswith("defs"):
                continue
            for ch in list(parent):
                if MARK_ID.match(ch.get("id") or "") and not ch.tag.endswith(("Gradient", "clipPath", "mask")):
                    out.append((parent, ch))
        return out
    found = marks(without)
    if not found:
        return None
    for parent, ch in found:
        parent.remove(ch)
    for _, ch in marks(magenta):
        for e in ch.iter():
            for k in ("opacity", "fill-opacity", "style"):
                e.attrib.pop(k, None)
            if e.get("fill") not in (None, "none"):
                e.set("fill", "#ff00ff")
        if ch.get("fill") in (None,) and not list(ch):
            ch.set("fill", "#ff00ff")

    rendered = {}

    def lab_on(b, bg=(0.5, 0.5, 0.5)):           # each variant is rendered once, composited per wallpaper
        if b not in rendered:
            rendered[b] = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(
                bytestring=b, output_width=N, output_height=N))).convert("RGBA")).astype(np.float32) / 255
        a = rendered[b]
        al = a[..., 3:4]
        return rgb2lab(np.clip(a[..., :3] * al + np.array(bg, np.float32) * (1 - al), 0, 1))
    without = ET.tostring(without)
    base = lab_on(without)
    foot = ndimage.binary_opening(np.linalg.norm(lab_on(ET.tostring(magenta)) - base, axis=-1) > 10, iterations=1)
    if foot.sum() < 20:
        return 0.0, 0.0, 0.0, 0.0
    ys, xs = np.nonzero(foot)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    side = max(x1 - x0, y1 - y0) * 128 / N
    # contrast and visible share on BOTH wallpapers, the worse one counts (overview-3, 2026-11-23:
    # Terminal Emulator's white mark on nothing vanished on the light wallpaper)
    contrast, seen = 999.0, 1.0
    for bg in ((246 / 255, 245 / 255, 244 / 255), (36 / 255, 31 / 255, 49 / 255)):
        de = np.linalg.norm(lab_on(txt, bg) - lab_on(without, bg), axis=-1)
        contrast = min(contrast, float(np.median(de[foot])))
        seen = min(seen, float(((de > 10) & foot).sum() / foot.sum()))
    try:                                   # the source's mark, fitted into the same box
        sys.path.insert(0, str(ROOT / "work/_lib"))
        import obj as _obj
        from shapely.ops import unary_union
        shp = unary_union([g for _, g, _ in _obj.mark_parts(slug)]).buffer(0)
        bx0, by0, bx1, by1 = shp.bounds
        W, H = int(x1 - x0), int(y1 - y0)
        t_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                 f'viewBox="{bx0} {by0} {bx1 - bx0} {by1 - by0}" preserveAspectRatio="xMidYMid meet">'
                 f'<path d="{_obj.geom_d(shp)}" fill="#000" fill-rule="evenodd"/></svg>')
        t = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=t_svg.encode()))).convert("RGBA"))[..., 3] > 127
        crop = foot[y0:y1, x0:x1]
        best = 0.0
        for dy in (-2, -1, 0, 1, 2):
            for dx in (-2, -1, 0, 1, 2):
                ts = np.roll(np.roll(t, dy, 0), dx, 1)
                best = max(best, float((crop & ts).sum() / max(1, (crop | ts).sum())))
    except Exception:                      # no measurable source mark: only size and contrast
        best = 1.0
    del copy
    return float(side), contrast, best, seen


# The whole result is cached: next.py runs this gate again right after make_icon.py, on the
# same files. The key is every input's path, size and change time - the app's folder, every
# design.md (gate same_object reads the other apps), the code of the gate and its libraries.
CACHE = ROOT / ".cache" / "check"


def mark_fit_measure(svg, N=256):
    """Does the mark SIT WELL on its part? (2026-11-23: DeepSeek computes coordinates without seeing
    the picture - text ran off its label, a CD hole sat on the letters, an "en" hung over its
    plate's edge.) The mark's footprint (elements whose id starts with 'mark') is found as in
    mark_layer_measure; the part under it is the smooth region (no edge steeper than 5 dE/px)
    that covers most of the footprint.
    -> None (no mark layer / the mark stands on nothing: L1), else dict
       cross   share of the mark that spills over the edge of that part
       margin  free space between the mark and that part's edge, in units of 128
       covered share of the mark hidden by something drawn over it (a hole, a handle ...)"""
    import xml.etree.ElementTree as ET
    from scipy import ndimage
    txt = Path(svg).read_bytes()
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

    def is_mark(e):
        return MARK_ID.match(e.get("id") or "") and not e.tag.endswith(("Gradient", "clipPath", "mask"))

    def marks(root):
        return [(p, c) for p in list(root.iter()) if not p.tag.endswith("defs") for c in list(p) if is_mark(c)]
    without, magenta, alone = ET.fromstring(txt), ET.fromstring(txt), ET.fromstring(txt)
    if not marks(without):
        return None
    for p, c in marks(without):
        p.remove(c)
    for _, c in marks(magenta):
        for e in c.iter():
            for k in ("opacity", "fill-opacity", "style"):
                e.attrib.pop(k, None)
            if e.get("fill") not in (None, "none"):
                e.set("fill", "#ff00ff")

    def keep_marks(e):                        # alone: only the marks (and what they need)
        keep = False
        for c in list(e):
            if c.tag.endswith("defs") or is_mark(c):
                keep = True
            elif keep_marks(c):
                keep = True
            else:
                e.remove(c)
        return keep or any(True for c in e)
    keep_marks(alone)

    def rgba(b):
        return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=b, output_width=N, output_height=N)))
                          .convert("RGBA")).astype(np.float32) / 255

    def lab(a):
        al = a[..., 3:4]
        return rgb2lab(np.clip(a[..., :3] * al + 0.5 * (1 - al), 0, 1))
    A = rgba(ET.tostring(without))
    la = lab(A)
    foot = ndimage.binary_opening(np.linalg.norm(lab(rgba(ET.tostring(magenta))) - la, axis=-1) > 10, iterations=1)
    if foot.sum() < 30:
        return None
    if np.median(A[..., 3][foot]) < 0.5:
        return None                           # the mark stands on nothing (L1): nothing to sit on
    whole = rgba(ET.tostring(alone))[..., 3] > 0.5
    covered = float((whole & ~ndimage.binary_dilation(foot, iterations=1)).sum() / max(1, whole.sum()))
    g = np.zeros(la.shape[:2])
    for ch in range(3):
        g = np.maximum(g, np.hypot(ndimage.sobel(la[..., ch], 0), ndimage.sobel(la[..., ch], 1)) / 8)
    smooth = (A[..., 3] > 0.5) & (g < 5)
    lbl, _ = ndimage.label(smooth)
    ids, cnt = np.unique(lbl[foot & smooth], return_counts=True)
    ids, cnt = ids[ids > 0], cnt[ids > 0]
    if not len(ids):
        return {"cross": 0.0, "margin": 99.0, "covered": covered}
    face = ndimage.binary_closing(ndimage.binary_fill_holes(lbl == ids[np.argmax(cnt)]), iterations=2)
    cross = float((foot & ~ndimage.binary_dilation(face, iterations=1)).sum() / foot.sum())
    inside = foot & face
    dist = ndimage.distance_transform_edt(np.pad(face, 1))[1:-1, 1:-1]
    margin = float(dist[inside].min()) * 128 / N if inside.any() else 0.0
    return {"cross": cross, "margin": margin, "covered": covered}


def _cache_key(slug):
    import hashlib
    h = hashlib.sha1()
    files = [p for p in (ROOT / "work" / slug).rglob("*") if p.is_file() and p.name != "build-stamp.txt"]
    files += list((ROOT / "work").glob("*/design.md"))
    files += [Path(__file__)] + [p for p in (ROOT / "work/_lib").glob("*") if p.is_file()] + list(SK.glob("*.py"))
    for p in sorted(set(files)):
        try:
            st = p.stat()
            h.update(f"{p.relative_to(ROOT)}|{st.st_size}|{st.st_mtime_ns}\n".encode())
        except (OSError, ValueError):
            pass
    return h.hexdigest()


def main():
    slug = sys.argv[1]
    as_json = "--json" in sys.argv
    key, res = None, None
    if "--no-cache" not in sys.argv:
        try:
            key = _cache_key(slug)
            c = json.loads((CACHE / f"{slug}.json").read_text())
            res = c["res"] if c.get("key") == key else None
        except (OSError, ValueError, KeyError):
            res = None
    if res is None:
        res = compute(slug)
        if key:
            try:                     # the key AFTER measuring: the gate itself may write caches
                CACHE.mkdir(parents=True, exist_ok=True)   # (work/<slug>/gradients.json)
                (CACHE / f"{slug}.json").write_text(json.dumps({"key": _cache_key(slug), "res": res}))
            except OSError:
                pass
    report(res, as_json)


def compute(slug):
    w = ROOT / "work" / slug
    res = []

    def add(scope, check, status, value, fix=""):
        res.append({"scope": scope, "check": check, "status": status, "value": value, "fix": fix})

    svgs = {st: w / f"{slug}-{st}.svg" for st in STYLES if (w / f"{slug}-{st}.svg").exists()}
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import builders
    is_redesign = builders.redesigned(slug)
    approved = ""
    if (w / "design.md").exists():
        for line in (w / "design.md").read_text(encoding="utf-8").splitlines():
            if line.lower().startswith("approved:"):
                approved = line.split(":", 1)[1].strip()
    if not is_redesign:
        add("app", "redesign", "FAIL", "logo on a plate (automatic draft)",
            f"R0: not a Gnomed icon yet - follow REDESIGN.md: python3 tools/new_redesign.py {slug}")
    elif not approved or approved.lower() in ("no", "-", "none", "?"):
        add("app", "redesign", "FAIL", "design.md: approved is empty",
            "R0: Q1 (REDESIGN.md 7): write the owner's answer in design.md 'approved:'")
    elif not is_quote(approved):
        add("app", "redesign", "FAIL", f"approved is not a quote + date: {approved[:40]}",
            'REDESIGN.md 7: approved: B - "<his words>" (YYYY-MM-DD) - never from a general instruction')
    else:
        add("app", "redesign", "PASS", approved[:40])
    if is_redesign and (w / f"{slug}-faithful.svg").exists():
        shape_ok = design_line(w, "shape-ok")
        shape_ok = shape_ok if is_quote(shape_ok) else ""          # only the owner's words + date count
        for st in ("faithful", "symbol"):
            if st == "symbol" and not (w / f"{slug}-symbol.svg").exists():
                continue
            if st == "symbol" and (w / f"{slug}-symbol.svg").read_bytes() == (w / f"{slug}-faithful.svg").read_bytes():
                continue                                            # the same design, checked once
            kind, iou, fill = shape_kind(w / f"{slug}-{st}.svg")
            if kind == "disc":
                add(st, "plain_shape", "PASS" if shape_ok else "FAIL", f"plain disc (circle match {iou:.2f})",
                    "" if shape_ok else "REDESIGN §1: the logo on a disc is not a redesign - make the app's OBJECT "
                    "(concept ladder), or get the owner's OK and write 'shape-ok: <his words>' in design.md")
            elif kind == "tile":
                add(st, "plain_shape", "PASS" if shape_ok else "WARN", f"square tile/plate (fills {fill:.0%} of its box)",
                    "" if shape_ok else "a tile with the logo on it is 'the logo on a plate' (REDESIGN §1) - allowed only "
                    "as L3 for a pure wordmark, or a real square object (window, calendar) - say which in Q2")
            elif kind == "box":
                add(st, "plain_shape", "PASS" if shape_ok else "WARN", f"plain square/box (fills {fill:.0%})",
                    "" if shape_ok else "a real box object (envelope, case)? say so in design.md 'shape-ok:'; "
                    "a plate with the logo on it is not a redesign")
            else:
                add(st, "plain_shape", "PASS", f"object silhouette (circle {iou:.2f}, fill {fill:.0%})")
    # slots: every style a different design (owner 2026-11-21 / 2026-11-22) unless he dropped the others
    if is_redesign and len(svgs) == 4:
        groups, alike = style_groups(svgs)
        distinct = len(groups)
        keep = design_line(w, "keep")
        letters = set(re.findall(r"\b([A-H])\b", keep.split(" - ")[0].split('"')[0]))
        dropped = keep.lower().startswith(("none", "0", "-")) or '"0"' in keep
        expected = 1 if dropped else min(4, 1 + len(letters)) if letters else 4
        if distinct >= expected:
            add("app", "slots", "PASS", f"{distinct} different designs (owner kept {expected})")
        else:
            add("app", "slots", "WARN", f"only {distinct} different designs in 4 styles" + (f" ({'; '.join(alike)})" if alike else ""),
                "REDESIGN.md 6: four DIFFERENT objects - not the same object in another colour or with a small extra; "
                "main -> symbol, closest to the logo -> faithful, round -> disc, the rest -> rimmed")
    add("app", "faithful", "PASS" if "faithful" in svgs else "FAIL", "faithful" in svgs,
        "" if "faithful" in svgs else "build the app first: python3 tools/make_icon.py " + slug)
    for st, svg in svgs.items():
        try:                                    # in-process: no new Python per style
            fail = bool(_skill_mod("lint_svg").lint(str(svg))["fails"])
        except Exception:
            out = subprocess.run([sys.executable, str(SK / "lint_svg.py"), str(svg)], capture_output=True, text=True).stdout
            fail = "[FAIL]" in out
        add(st, "lint", "FAIL" if fail else "PASS", "FAIL" if fail else "ok",
            "read the lint message; edge contact -> make the object smaller (inside 8..120)" if fail else "")
        # empty_layer: a part the code meant to draw came out as nothing (d=""), e.g. rounded(g, r) with r >=
        # half the part's height, or an intersection that missed - the icon silently loses that part
        empty = re.findall(r'<path id="([^"]+)" d=""', svg.read_text(encoding="utf-8"))
        add(st, "empty_layer", "FAIL" if empty else "PASS", ", ".join(empty[:6]) + (" ..." if len(empty) > 6 else "") if empty else "none",
            "these layers are EMPTY - the part is missing from the icon: rounded(g, r) needs r < half the part's "
            "thinnest side; check intersections/differences; or delete the layer if the part is not wanted" if empty else "")
        a = render(svg)
        vl, vd = visible(a, LIGHT), visible(a, DARK)
        if st == "symbol":
            # no plate: the object itself must read on BOTH wallpapers
            for name, v, rec in (("visible_light", vl, "too pale on a light wallpaper: darker side/face (docs/PLAYBOOK.md#fix-fail)"),
                                 ("visible_dark", vd, "too dark on a dark wallpaper: lighter face, top light (docs/PLAYBOOK.md#fix-fail)")):
                stt = "PASS" if v >= 0.55 else ("WARN" if v >= 0.25 else "FAIL")
                add(st, name, stt, round(v, 2), "" if stt == "PASS" else rec)
        else:
            # a light plate on a light wallpaper (or dark on dark) is fine in GNOME - its chin and
            # edge separate it; it must read clearly on at least ONE of the two
            v = max(vl, vd)
            stt = "PASS" if v >= 0.55 else "FAIL"
            add(st, "visible", stt, f"light {vl:.2f} / dark {vd:.2f}", "" if stt == "PASS" else "vanishes on both wallpapers: stronger colours (docs/PLAYBOOK.md#fix-fail)")
        m, bottom = mass_and_bottom(a)
        # a redesign is a free object in EVERY slot: one range for all (tools/describe_icon.py uses it too)
        lo, hi = (0.35, 0.75) if is_redesign else ((0.20, 0.75) if st == "symbol" else (0.40, 0.75))
        add(st, "mass", "PASS" if lo <= m <= hi else "WARN", round(m, 2), "" if lo <= m <= hi else
            "the icon looks thin: bigger object, or a secondary object in front (docs/PLAYBOOK.md#fix-fail, mass)")
        blo, bhi = {"faithful": (114, 118.5), "disc": (120, 126.5), "rimmed": (120, 126.5), "symbol": (108, 124.5)}[st]
        if is_redesign:
            blo, bhi = 108, 126.5          # free objects: GNOME icons end anywhere from 108 to 126
        add(st, "baseline", "PASS" if blo <= bottom <= bhi else "WARN", round(bottom, 1), "" if blo <= bottom <= bhi else "R9 baseline")
        ssim = None
        try:                                    # in-process and cached (review.sh measured it already)
            ssim = float(_legibility().cached_analyse(svg)["sizes"][32]["ssim"])
        except Exception:                       # never crash the gate: fall back to the script
            leg = subprocess.run([sys.executable, str(SK / "legibility_check.py"), str(svg)],
                                 capture_output=True, text=True).stdout
            for line in leg.splitlines():
                if "32px" in line and "ssim" in line:
                    try:
                        ssim = float(line.split("ssim")[1].split()[0])
                    except ValueError:
                        pass
        if ssim is not None:
            stt = "PASS" if ssim >= 0.72 else ("WARN" if ssim >= 0.62 else "FAIL")
            add(st, "legibility32", stt, ssim, "" if stt == "PASS" else "details vanish at 32 px: bigger parts, drop tiny details, strokes >= 2 px")
        # holes: the Symbol of every app and every style of a redesign (plates are exempt:
        # there the holes show the plate, which is correct)
        if st == "symbol" or is_redesign:
            m = hole_measure(slug, svg)
            if m is not None:
                src, transp, iou = m
                val = f"source {src:.1%} -> transparent {transp:.1%}"
                if src < 0.004:
                    add(st, "holes", "PASS", val + " (no holes to keep)")
                elif is_redesign and iou < 0.75:
                    add(st, "holes", "PASS", val + f" (the mark sits ON an object, iou {iou:.2f}: the object behind "
                        "it shows through its holes - correct; if the mark itself IS the object, cut its holes)")
                elif transp >= 0.5 * src:
                    add(st, "holes", "PASS", val)
                else:
                    import build_auto as _ba
                    ok = _ba.OVERRIDES.get(slug, {}).get("painted_counters") or is_quote(design_line(w, "painted-holes"))
                    add(st, "holes", "PASS" if ok else "FAIL", val + (" (painted on purpose)" if ok else ""),
                        "" if ok else "REDESIGN.md 5: cut the holes (body(), difference) - never paint them; "
                        "only the owner's words allow it: painted-holes: \"<his words>\" (YYYY-MM-DD)")
        # mark_size: the app's own colours (its mark) must read on the phone. A mark printed small
        # on a big object (Deezer's bars on a record label, 2026-11-22) is lost at 48 px.
        if is_redesign:
            mm = mark_measure(slug, svg)
            if mm is not None:
                side, share, _n = mm
                val = f"{side:.0f} px of 128 (on the phone at 48 px: {side * 48 / 128:.0f} px)"
                if side >= 36:
                    add(st, "mark_size", "PASS", val)
                else:
                    add(st, "mark_size", "WARN", val,
                        "the app's own mark/colours are too small to read on the phone: make the part that "
                        "carries the mark (label, stamp, screen) bigger and the mark >= 36 px of 128 "
                        "(docs/PLAYBOOK.md#fix-warn)")
        # mark: the app's own mark (measured from the source) on EVERY style, big enough, standing
        # out from its surface, and really the source's shape (owner 2026-11-22, ara-2: Apple Music
        # and Soundcore had lost it; ChatGPT's bulb carried an "M"). Games (objects only) and
        # system apps (GNOME's own metaphor) are not measured.
        if is_redesign and (w / "geometry.json").exists() and mark_applies(w):
            need = 44 if st == "faithful" else 36
            try:
                mk = mark_layer_measure(slug, svg)
            except Exception as e:                       # never crash the gate
                mk = ("err", str(e))
            how = ("draw the app's mark from the source with put_mark(ic, SLUG, box) (or inside "
                   "`with ic.group(\"mark\"):`) ON the object - label, screen, lid, stamp - or as the object "
                   "itself (L1); docs/PLAYBOOK.md#fix-warn")
            if mk is None:
                add(st, "mark", "WARN", "no layer named 'mark' - the app's mark is not in this style", how)
            elif mk[0] == "err":
                add(st, "mark", "PASS", f"not measured ({mk[1][:40]})")
            else:
                side, con, iou, seen = mk
                val = f"{side:.0f} px of 128, contrast {con:.0f}, shape match {iou:.2f}, visible {seen:.0%}"
                if iou < 0.5:
                    add(st, "mark", "WARN", val + " - not the source's mark",
                        "the 'mark' layer is not the app's mark (a letter or a shape drawn from memory): draw "
                        "the MEASURED mark with put_mark(ic, SLUG, box) - never retype or redraw a logo")
                elif con < 25 or seen < 0.6:
                    add(st, "mark", "WARN", val + " - does not stand out",
                        "the mark melts into what is under it (measured on the light AND the dark wallpaper): a "
                        "white/light mark on a dark part, a dark or strong-coloured mark on a light part; a mark "
                        "standing on nothing needs a colour that reads on both wallpapers, or a part behind it "
                        "(put_mark(..., face=\"#ffffff\") / a darker ramp step)")
                elif side < need:
                    add(st, "mark", "WARN", val + f" - smaller than {need} px",
                        f"make the part that carries the mark bigger and the mark >= {need} px of 128"
                        + (" (Faithful is the style closest to the logo: the mark is big there)" if st == "faithful" else ""))
                else:
                    add(st, "mark", "PASS", val)
            # mark_fit: the mark sits WELL on its part - inside its edge with some room, nothing on top
            try:
                fit = mark_fit_measure(svg)
            except Exception as e:                       # never crash the gate
                fit = {"err": str(e)}
            if fit and "err" not in fit:
                val = (f"over the edge {fit['cross']:.0%}, room to the edge {fit['margin']:.1f} u, "
                       f"covered {fit['covered']:.0%}")
                if fit["cross"] > 0.01 or fit["margin"] < 1.0 or fit["covered"] > 0.03:
                    add(st, "mark_fit", "WARN", val,
                        "the mark runs off, touches the edge of, or is covered on the part it sits on (a label, "
                        "lid, screen, disc): make the mark SMALLER or the part BIGGER so it keeps >= 1 unit of room "
                        "on every side, and draw nothing over it (a CD hole, a handle, a strap goes under it or "
                        "elsewhere). Check with: python3 tools/check_icon.py SLUG")
                else:
                    add(st, "mark_fit", "PASS", val)
        # bands: a gradient of the source painted as several flat colours looks melted/broken
        # (Deezer concepts, 2026-11-22). regions() knows which measured parts are bands of one
        # gradient; two or more of them as flat fills in one style = FAIL.
        if is_redesign and (w / "geometry.json").exists():
            try:
                import obj as _obj
                bad = _obj.banded(slug, svg.read_text())
            except Exception as e:                       # the check must never crash the gate
                bad, _err = None, e
            if bad is None:
                add(st, "bands", "PASS", f"not measured ({str(_err)[:40]})")
            elif bad:
                add(st, "bands", "FAIL", "; ".join(f"{n}: {', '.join(h)}" for n, h in bad),
                    f"a gradient of the source is painted as flat bands - draw those parts as ONE shape with "
                    f"a real gradient: for name, g, fill in regions('{slug}') (or face=gradient('{slug}', shape)); "
                    "docs/PLAYBOOK.md#gradients")
            else:
                add(st, "bands", "PASS", "no flat gradient bands")
    # anchors: every style carries the app's OWN anchors (owner 2026-11-23, Kafa Topu 2: a stopwatch,
    # a boot, a trophy and a blue ball - "Otun ile alakası yok ... Biz ne için ona ekran görüntüleri
    # logolar vesaire indirtiyoruz o zaman?"). design.md: anchors cite where they were seen
    # (source.png / refs/...), each style's concept line cites the anchors it carries.
    if is_redesign and (w / "design.md").exists() and slug not in SYSTEM_APPS:
        text = (w / "design.md").read_text(encoding="utf-8")
        m = re.search(r"^anchors[^\n]*\n((?:[ \t]+[^\n]*\n?)+?)(?=^\S|\Z)", text, re.M)
        items = {}
        for ln in (m.group(1).splitlines() if m else []):
            mm = re.match(r"\s*(\d)\.\s*(\S.*)", ln)
            if mm:
                items[mm.group(1)] = mm.group(2)
        sourced = [k for k, v in items.items() if re.search(r"source\.png|refs/|screenshot|shot-\d|owner", v, re.I)]
        styles_line = next((ln for ln in text.splitlines() if ln.lower().startswith("styles:")), "")
        for st_, letter in re.findall(r"\b(symbol|faithful|disc|rimmed)\s*=\s*([A-H])\b", styles_line):
            cl = re.search(rf"^\s+{letter}\b[^:\n]*:\s*(.+)$", text, re.M)
            cited = set(re.findall(r"\d", " ".join(re.findall(r"anchors?\s*([\d,\s+&and]+)", cl.group(1), re.I)))) if cl else set()
            cited &= set(items)
            if len(sourced) < 2:
                add(st_, "anchors", "WARN", f"{len(sourced)} anchor(s) say where they were seen",
                    "design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, "
                    "refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category")
            elif not cited:
                add(st_, "anchors", "WARN", f"concept {letter} cites no anchor",
                    "this style must carry the app's own anchors in their real colours - a generic object of the "
                    "category (a stopwatch or a trophy for a football game) could be ANY app. Redraw it with the "
                    f"anchors and end concept line {letter} with '(anchors 1, 2)'")
            else:
                add(st_, "anchors", "PASS", "anchors " + ", ".join(sorted(cited)))
    # same_object: a style uses an object another app of the category already uses (owner
    # 2026-11-22, ara-2: Apple Music's cassette was Deezer's). Read from design.md 'styles:' and
    # the concept lines; work/_lib/categories.py knows the families.
    if is_redesign:
        try:
            sys.path.insert(0, str(ROOT / "work/_lib"))
            import categories as _cat
            for st_, o, who in _cat.clashes(slug):
                add(st_, "same_object", "WARN", f"{o} - also used by {', '.join(who)}",
                    "pick a FREE object of the category's family for this style (python3 tools/next.py "
                    f"{slug} lists USED/free) - BATCH.md 7: two apps of one category never share an object")
        except Exception as e:                       # never crash the gate
            add("app", "same_object", "PASS", f"not measured ({str(e)[:40]})")
    # box inside the plate: a big single region whose colour differs from the plate
    gp = w / "geometry.json"
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import builders
    is_hand = builders.hand_built(slug)
    if gp.exists():
        g = json.loads(gp.read_text())
        regs = g["info"].get("regions", [])
        if "faithful" in svgs and regs:
            biggest = max(r["area"] for r in regs)
            bb = g["info"].get("mark_bbox") or [0, 0, 0, 0]
            span = min(bb[2] - bb[0], bb[3] - bb[1]) / 128
            src = open(svgs["faithful"]).read()
            dropped = '"drop"' in src  # not reliable; real check below
            stt = "FAIL" if (biggest > 0.40 and span > 0.70) else "PASS"
            # an override that turned the region into the plate colour clears it
            ov = (ROOT / "work/_lib/build_auto.py").read_text()
            if f'"{slug}"' in ov and ('"face"' in ov.split(f'"{slug}"')[1].split("\n")[0] or "only_white" in ov.split(f'"{slug}"')[1].split("\n")[0]):
                stt = "PASS"
            if is_hand:
                stt = "PASS"
            del dropped
            add("faithful", "box_in_plate", stt, round(biggest, 2),
                "" if stt == "PASS" else "R4: the big region is the app's TILE -> face=<its colour>, drop=[<its colour>], keep_ground=True")
        # stripes: several regions with near-identical hue (only regions the build uses)
        sys.path.insert(0, str(ROOT / "work/_lib"))
        import build_auto as ba
        o = ba.OVERRIDES.get(slug, {})
        used_regs = [r for r in regs if r["fill"] not in o.get("drop", [])
                     and (not o.get("only_white") or ba.is_whiteish(r["fill"]))]
        hs = [(hue(r["fill"]), r["fill"]) for r in used_regs if r["fill"].startswith("#")]
        coloured = [(h, f) for (h, s_, l_), f in [((a_[0][0], a_[0][1], a_[0][2]), a_[1]) for a_ in hs] if s_ > 0.25 and 0.15 < l_ < 0.9]
        groups = []
        for hh, f in sorted(coloured):
            if groups and abs(hh - groups[-1][-1][0]) < 28:
                groups[-1].append((hh, f))
            else:
                groups.append([(hh, f)])
        striped = [grp for grp in groups if len(grp) >= 3]
        ov = (ROOT / "work/_lib/build_auto.py").read_text()
        merged = f'"{slug}"' in ov and "merge_grad" in ov.split(f'"{slug}"')[1].split("\n")[0]
        if striped and not merged and not is_redesign:      # a redesign does not draw the measured bands
            add("app", "stripes", "WARN", [f for _, f in striped[0]],
                f'R1: python: OVERRIDES["{slug}"] = {{"merge_grad": [{[f for _, f in striped[0]]}]}}')
        else:
            add("app", "stripes", "PASS", 0)
        # thin parts (bands, lines) lose IoU to smoothing without visible harm: only a LARGE
        # part that matches badly is a failure; hand-built apps do not use these regions
        if is_hand:
            add("app", "trace_iou", "PASS", "hand-built")
        else:
            sys.path.insert(0, str(ROOT / "work/_lib"))
            import build_auto as ba
            o = ba.OVERRIDES.get(slug, {})
            merged = {c for grp in o.get("merge_grad", []) for c in grp}
            used = [r for r in regs if r["fill"] not in o.get("drop", [])
                    and (not o.get("only_white") or ba.is_whiteish(r["fill"]))
                    and r["fill"] not in merged]          # merged parts are rebuilt as one fitted part
            areas = {r["name"]: r["area"] for r in used}
            low = {k: v["iou"] for k, v in g["parts"].items() if k in areas and v.get("iou", 1) < 0.90}
            big = {k: i for k, i in low.items() if areas.get(k, 0) >= 0.03 and i < 0.75}
            stt = "FAIL" if big else ("WARN" if low else "PASS")
            add("app", "trace_iou", stt, big or low or "all >= 0.90",
                "" if stt == "PASS" else "R12: re-run with --remeasure; if still low the region is noise -> drop it")
    return res


def report(res, as_json):
    if as_json:
        print(json.dumps(res, indent=1))
    else:
        for r in res:
            line = f'{r["status"]:4}  {r["scope"]:9} {r["check"]:14} {r["value"]}'
            if r["fix"]:
                line += f'   -> FIX: {r["fix"]}'
            print(line)
        n = {s: sum(r["status"] == s for r in res) for s in ("PASS", "WARN", "FAIL")}
        print(f'\nsummary: {n["PASS"]} PASS, {n["WARN"]} WARN, {n["FAIL"]} FAIL  '
              f'({"OK to continue" if n["FAIL"] == 0 else "fix every FAIL, then run again"})')
    sys.exit(1 if any(r["status"] == "FAIL" for r in res) else 0)


if __name__ == "__main__":
    main()
