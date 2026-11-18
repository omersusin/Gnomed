#!/usr/bin/env python3
"""Hand-built redraws of the ten apps the batch pipeline handled badly.
   python3 work/_lib/build_weak.py [slug ...]

Every shape is measured from work/<slug>/source.png (masks -> fits / traces via
gtrace); nothing is drawn from memory. Per app, the docstring says which identity
element was kept and what was dropped.
"""
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage
from shapely.geometry import Polygon, Point, LineString, box as sbox
from shapely.ops import unary_union
from svgpathtools import parse_path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fam  # noqa: E402
import gtrace as gt  # noqa: E402
from fam import gk, shade, place, box_c  # noqa: E402

WORK = fam.WORK
INK = "#241f31"
B = {}


def build(fn):
    B[fn.__name__] = fn
    return fn


# ------------------------------------------------------------------ geometry helpers
def poly_of(d, n=500):
    """even-odd path -> shapely geometry (outer rings minus holes by parity)."""
    rings = []
    for sp in parse_path(d).continuous_subpaths():
        k = max(24, int(sp.length() * 2))
        pts = [sp.point(i / k) for i in range(k)]
        p = Polygon([(z.real, z.imag) for z in pts]).buffer(0)
        if p.area > 0.05:
            rings.append(p)
    g = None
    for p in sorted(rings, key=lambda q: -q.area):
        g = p if g is None else g.symmetric_difference(p)
    return g if g is not None else Polygon()


def d_of(geom):
    out = []
    for g in getattr(geom, "geoms", [geom]):
        if g.is_empty or g.geom_type != "Polygon":
            continue
        for ring in [g.exterior, *g.interiors]:
            c = list(ring.coords)[:-1]
            out.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in c) + "Z")
    return "".join(out)


def xf(d, s, dx, dy, about=(0.0, 0.0)):
    return gk.xform_d(d, s, dx, dy, about=about)


def tile_to(d, x0, y0, size):
    """map source-tile coordinates (0..128) onto a square at (x0, y0) of `size`."""
    s = size / 128.0
    return gk.xform_d(d, s, x0, y0, about=(0, 0))


def face_shape(kind):
    if kind == "plate":
        return poly_of(gk.rrect_d(12, 12, 104, 100, 8))
    if kind == "disc":
        return Point(64, 63).buffer(59, resolution=64)
    if kind == "rimmed":
        return Point(64, 63).buffer(53.5, resolution=64)


def clip(d, kind):
    return d_of(poly_of(d).intersection(face_shape(kind)))


def mask(slug, pred, smooth=None):
    a, s = gt.load(WORK / slug)
    m = pred(a)
    return m, s, a


def trace(m, s, **kw):
    return gt.trace_mask(m, s, **kw)


def lum(a):
    return a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)


def hexc(rgb):
    return "#%02x%02x%02x" % tuple(int(round(min(max(v, 0), 1) * 255)) for v in rgb)


def side(f):
    return "#deddda" if f.lower() in ("#ffffff", "#f6f5f4") else shade(f, -0.14)


def raised(ic, items, lift=2, layer="mark"):
    fam.raised(ic, [(d, f, side(f)) for d, f in items], lift=lift, layer=layer)


def note(slug, extra):
    return fam.note(slug) + " | redraw: " + extra


# ------------------------------------------------------------------ Terminal Emulator
@build
def terminal_em_lat_r():
    """The grey screen IS the icon (no screen-on-a-plate): the screen becomes the plate,
    the lime area keeps its measured curve, '> 1+ Term' is the traced lettering."""
    P = gk.load_parts(str(WORK / "terminal_em_lat_r/source-geometry.svg")) if False else None  # noqa: F841
    a, s = gt.load(WORK / "terminal_em_lat_r")
    grey = gt.near(a, "#678390", "#d2dbdf") & gt.opaque(a)
    lime = gt.near(a, "#a6c73d", "#678390") & (a[..., 1] > a[..., 2] + 0.15)
    white = (lum(a) > 0.93) & ndimage.binary_fill_holes(grey | lime)
    screen = ndimage.binary_fill_holes(gt.components(grey | lime | white)[0])
    sd, ld, wd = trace(screen, s), trace(gt.components(lime)[0], s), trace(white, s)
    x0, y0, x1, y1 = gt.bbox(screen, s)
    GREY, LIME = "#678390", "#a6c73d"

    def contents(ic, size, cx, cy, kind):
        sc = size / (x1 - x0)
        m = lambda d: gk.xform_d(d, sc, cx - (x0 + x1) / 2, cy - (y0 + y1) / 2, about=((x0 + x1) / 2, (y0 + y1) / 2))  # noqa: E731
        lime_d = m(ld)
        if kind:
            lime_d = clip(lime_d, kind)
        ic.path(lime_d, LIME, layer_id="lime")
        raised(ic, [(m(wd), "#ffffff")], lift=1.5, layer="text")

    out = {}
    ic = gk.Icon("Terminal Emulator - Faithful", note("terminal_em_lat_r", "screen = plate"))
    fam.plate(ic, GREY)
    # the lime area runs to the screen edge: clip it to the plate face
    contents(ic, 104, 64, 62, "plate")
    out["faithful"] = ic
    for st, title, base, kind, size in (("disc", "Sound Disc", lambda i: fam.disc(i, GREY), "disc", 104),
                                        ("rimmed", "Rimmed", lambda i: fam.rimmed(i, GREY), "rimmed", 94)):
        ic = gk.Icon(f"Terminal Emulator - {title}", note("terminal_em_lat_r", "screen colours on the disc"))
        base(ic)
        contents(ic, size, 64, 63, kind)
        out[st] = ic
    # Symbol: the screen as a device (Console-like 6 px front)
    ic = gk.Icon("Terminal Emulator - Free Symbol", note("terminal_em_lat_r", "screen as object"))
    ds, sc = place([sd, ld, wd], box_c(64, 60, 108), ref=[sd])
    fam.slab(ic, ds[0], GREY, depth=6, corner_r=14)
    ic.path(ds[1], LIME, layer_id="lime")
    raised(ic, [(ds[2], "#ffffff")], lift=1.5, layer="text")
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Shizuku
@build
def shizuku():
    """The white head peeks in from the bottom-left corner of the tile - that crop IS the
    design, so the head is clipped to each face shape exactly as the tile clips it.
    Dropped: the faint lighter hexagon (tile decoration). No Symbol (a cropped head
    cannot stand alone)."""
    a, s = gt.load(WORK / "shizuku")
    head = (a[..., :3].min(-1) > 0.82) & gt.opaque(a)
    head = gt.components(head)[0]
    hd = trace(head, s)             # eyes stay as holes (even-odd) -> they show the face colour
    BLUE0, BLUE1 = "#7380ca", "#4153b7"
    out = {}
    for st, title, kind, (x0, y0, size) in (("faithful", "Faithful", "plate", (12, 112 - 104, 104)),
                                            ("disc", "Sound Disc", "disc", (5, 4, 118)),
                                            ("rimmed", "Rimmed", "rimmed", (10.5, 9.5, 107))):
        ic = gk.Icon(f"Shizuku - {title}", note("shizuku", "head clipped by the face like the tile clips it"))
        if kind == "plate":
            g = ic.linear([(0, "#8e98d6"), (1, BLUE1)], 20, 112, 116, 12)
            fam.plate(ic, BLUE0, g, BLUE1)
        elif kind == "disc":
            g = ic.linear([(0, "#8e98d6"), (1, BLUE1)], 15, 115, 115, 10)
            fam.disc(ic, BLUE0, g, BLUE1, top_light=0)
        else:
            g = ic.linear([(0, "#8e98d6"), (1, BLUE1)], 18, 110, 110, 15)
            ic.rimmed_disc(inner=BLUE0, inner_gradient=g)
        d = clip(tile_to(hd, x0, y0, size), kind)
        ic.path(d, "#eef0fa", layer_id="head")
        out[st] = ic
    return out


# ------------------------------------------------------------------ Pix Material You
@build
def pix_material_you_light_dark():
    """Black line mark on a dark slate tile: kept dark, but ENGRAVED - a light lower edge
    (the slate catching light) separates the lines from the face, so the mark reads on
    the dark tile and on dark wallpapers. Symbol: slate-margin object."""
    a, s = gt.load(WORK / "pix_material_you_light_dark")
    ink = (lum(a) < 0.07) & gt.opaque(a)
    md = trace(gt.components(ink)[0] | ink, s)
    SLATE, LINE, EDGE = "#243240", "#0b1016", "#56687a"
    out = {}

    def mark(ic, box):
        ds, _ = place([md], box)
        with ic.group("mark"):
            ic.path(gk.translate_d(ds[0], 0, 1.4), EDGE, layer_id="mark-edge", fill_rule="evenodd")
            ic.path(ds[0], LINE, layer_id="mark-face", fill_rule="evenodd")

    ic = gk.Icon("Pix - Faithful", note("pix_material_you_light_dark", "engraved lines")); fam.plate(ic, SLATE)
    mark(ic, box_c(64, 62, 76)); out["faithful"] = ic
    ic = gk.Icon("Pix - Sound Disc", note("pix_material_you_light_dark", "engraved lines")); fam.disc(ic, SLATE)
    mark(ic, box_c(64, 63, 80)); out["disc"] = ic
    ic = gk.Icon("Pix - Rimmed", note("pix_material_you_light_dark", "engraved lines")); fam.rimmed(ic, SLATE)
    mark(ic, box_c(64, 63, 70)); out["rimmed"] = ic
    ic = gk.Icon("Pix - Free Symbol", note("pix_material_you_light_dark", "slate object"))
    ds, _ = place([md], box_c(64, 60, 104))
    body = fam.offset_d(d_of(poly_of(ds[0]).buffer(0)), 4.0)
    fam.slab(ic, d_of(poly_of(body).buffer(0)), SLATE, depth=4)
    with ic.group("mark"):
        ic.path(gk.translate_d(ds[0], 0, 1.2), EDGE, layer_id="mark-edge", fill_rule="evenodd")
        ic.path(ds[0], LINE, layer_id="mark-face", fill_rule="evenodd")
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Walpy
def walpy_skeleton_unused():
    """Blurry 192 px signature: its centre line (skeleton of the stroke core) is redrawn
    with one even, measured stroke width - a clean pen line instead of a glow blob."""
    from skimage.morphology import skeletonize, disk, binary_dilation
    a, s = gt.load(WORK / "walpy")
    # skeleton of the stroke (generous mask), width from the SHARP core only (no glow)
    body = gt.components((lum(a) > 0.55) & gt.opaque(a))[0]
    sharp = body & (lum(a) > 0.88)
    sk = skeletonize(body)
    width_px = sharp.sum() / max(sk.sum(), 1)                 # area / length = mean stroke width
    stroke = binary_dilation(sk, disk(max(2, int(round(width_px / 2)))))
    sd = gt.trace_mask(stroke, s, smooth_u=0.9)
    NAVY, W = "#1b242e", "#f2f3f4"
    out = {}
    # the signature covers ~40 % of the source tile: keep that proportion (larger reads as a blob)
    for st, title, base, bx in (("faithful", "Faithful", lambda i: fam.plate(i, NAVY), box_c(64, 62, 56)),
                                ("disc", "Sound Disc", lambda i: fam.disc(i, NAVY), box_c(64, 63, 60)),
                                ("rimmed", "Rimmed", lambda i: fam.rimmed(i, NAVY), box_c(64, 63, 52))):
        ic = gk.Icon(f"Walpy - {title}", note("walpy", f"skeleton re-stroked, width {width_px * s:.1f} u"))
        base(ic)
        ds, _ = place([sd], bx)
        raised(ic, [(ds[0], W)], lift=2)
        out[st] = ic
    ic = gk.Icon("Walpy - Free Symbol", note("walpy", "navy margin object"))
    ds, _ = place([sd], box_c(64, 76, 92, 76))
    fam.slab(ic, fam.offset_d(ds[0], 4.0), NAVY, depth=4)
    raised(ic, [(ds[0], W)], lift=1.5)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ KonaBess
@build
def konabess():
    """Measured emblem: prohibition ring + slash (circle/line fits of the thick strokes),
    the chip as a clean outline square with its pin-1 dot and the traced '888 5G'.
    Dropped: the 'Qualcomm Snapdragon' scribble (unreadable at any icon size)."""
    a, s = gt.load(WORK / "konabess")
    dark = (lum(a) < 0.45) & gt.opaque(a)
    disc_m = ndimage.binary_fill_holes(gt.opaque(a))
    cx, cy, R = gt.circle_fit(gt.components(disc_m)[0], s)
    dt = ndimage.distance_transform_edt(dark) * s
    thick = dark & (dt > 1.6)
    thick = ndimage.binary_dilation(thick, iterations=int(1.6 / s))
    H, W_ = dark.shape
    Y, X = np.mgrid[0:H, 0:W_]
    rr = np.hypot(X * s - cx, Y * s - cy)
    ring_px = thick & (rr > R * 0.72)
    r_in = np.percentile(rr[ring_px], 3)
    r_out = np.percentile(rr[ring_px], 99.5)
    sl = thick & (rr < r_in - 1)
    ys, xs = np.nonzero(sl)
    pts = np.c_[xs * s, ys * s]
    c0 = pts.mean(0)
    u = np.linalg.svd(pts - c0, full_matrices=False)[2][0]
    perp = np.abs((pts - c0) @ np.array([-u[1], u[0]]))
    half_w = np.percentile(perp, 95)
    thin = dark & ~thick & (rr < r_in - 1)
    # chip = the square the thin ink fills (outline + text): robust percentile box of all
    # thin ink inside the ring, away from the slash band
    ty_, tx_ = np.nonzero(thin & (np.abs((np.c_[X.ravel(), Y.ravel()].reshape(H, W_, 2) * s - c0) @ np.array([-u[1], u[0]])) > half_w + 2))
    tx0, tx1 = np.percentile(tx_ * s, [3, 97])
    ty0, ty1 = np.percentile(ty_ * s, [3, 97])
    lw = max(1.6, float(np.median(dt[thin & (dt > 0)])) * 2)
    # text: thin ink in the chip's top-right area, away from the slash
    tm = thin.copy()
    tm[: int(ty0 / s + (ty1 - ty0) * 0.08 / s)] = False
    tm[int((ty0 + (ty1 - ty0) * 0.45) / s):] = False
    tm[:, : int((tx0 + (tx1 - tx0) * 0.55) / s)] = False
    text_d = trace(tm, s)

    def emblem():
        ring = Point(cx, cy).buffer(r_out, resolution=96).difference(Point(cx, cy).buffer(r_in, resolution=96))
        line = LineString([tuple(c0 - u * R), tuple(c0 + u * R)]).buffer(half_w, cap_style=2)
        slash = line.intersection(Point(cx, cy).buffer(r_in + 0.5, resolution=96))
        chip = sbox(tx0, ty0, tx1, ty1).buffer(2.0, join_style=1).difference(
            sbox(tx0 + lw, ty0 + lw, tx1 - lw, ty1 - lw).buffer(2.0 - lw if lw < 2 else 0.2, join_style=1))
        pin = Point(tx0 + (tx1 - tx0) * 0.2, ty0 + (ty1 - ty0) * 0.2)
        pin_ring = pin.buffer((tx1 - tx0) * 0.1).difference(pin.buffer((tx1 - tx0) * 0.1 - lw))
        disc_bg = Point(cx, cy).buffer(r_out, resolution=96)
        return d_of(disc_bg), d_of(ring), d_of(slash), d_of(unary_union([chip, pin_ring])), text_d

    bg, ring, slash, chip, text = emblem()
    out = {}

    def put(ic, box, lift=2, slab_=False):
        ds, _ = place([bg, ring, slash, chip, text], box, ref=[bg])
        if slab_:
            x0, _, x1, _ = gk.bbox_d(ds[0])
            c = ic.chin_gradient(INK, x0, x1, (x1 - x0) * 0.45, colors={"edge": INK, "base": "#3d3846", "highlight": "#5e5c64"})
            ic.path(gk.translate_d(ds[0], 0, 3), c, layer_id="emblem-chin")
        ic.path(ds[0], "#ffffff", layer_id="emblem-face")
        ic.path(ds[3], "#5e5c64", layer_id="chip", fill_rule="evenodd")
        ic.path(ds[4], "#5e5c64", layer_id="chip-text", fill_rule="evenodd")
        ic.path(ds[1], INK, layer_id="ring", fill_rule="evenodd")
        ic.path(ds[2], INK, layer_id="slash")

    ic = gk.Icon("KonaBess - Faithful", note("konabess", "ring/slash/chip measured; scribble dropped")); fam.plate(ic, fam.PAPER)
    put(ic, box_c(64, 62, 84)); out["faithful"] = ic
    ic = gk.Icon("KonaBess - Sound Disc", note("konabess", "the white disc is the source's own"));
    ds, _ = place([bg, ring, slash, chip, text], box_c(64, 63, 118), ref=[bg])
    c = ic.chin_gradient(INK, 5, 123, 53, colors={"edge": INK, "base": "#3d3846", "highlight": "#5e5c64"})
    ic.path(gk.circle_d(64, 65, 59), c, layer_id="disc-chin")
    put(ic, box_c(64, 63, 118)); out["disc"] = ic
    ic = gk.Icon("KonaBess - Rimmed", note("konabess", "emblem in the rim")); ic.rimmed_disc(inner="#ffffff", rim_face="#deddda", rim_chin="#c0bfbc")
    put(ic, box_c(64, 63, 96)); out["rimmed"] = ic
    ic = gk.Icon("KonaBess - Free Symbol", note("konabess", "emblem as object"))
    put(ic, box_c(64, 61, 110), slab_=True); out["symbol"] = ic
    return out


# ------------------------------------------------------------------ BCR
@build
def bcr():
    """Blurry source: handset + microphone from the analysis (halo removed), but the
    microphone drawn white like the handset (it is semi-transparent white in the source,
    which reads as a smudge at icon size)."""
    import json
    g = json.loads((WORK / "bcr/geometry.json").read_text())
    P = {k: v["d"] for k, v in g["parts"].items()}
    regs = [(P[r["name"]], r["fill"]) for r in g["info"]["regions"]]
    hand = [d for d, f in regs if f.lower() == "#ffffff"][0]
    mic_src = [d for d, f in regs if f.lower() != "#ffffff"][0]
    # the source mic (blurred) shows capsule + U-holder + stem; rebuild those three
    # primitives inside the mic's measured bounding box
    mx0, my0, mx1, my1 = gk.bbox_d(mic_src)
    mw, mh = mx1 - mx0, my1 - my0
    mcx = (mx0 + mx1) / 2
    cap_w, cap_h = mw * 0.42, mh * 0.55
    capsule = gk.rrect_d(mcx - cap_w / 2, my0, cap_w, cap_h, cap_w / 2)
    lw = max(1.2, mw * 0.14)
    arc_r = mw * 0.40
    ay = my0 + cap_h * 0.62
    holder = Point(mcx, ay).buffer(arc_r).difference(Point(mcx, ay).buffer(arc_r - lw)).intersection(
        sbox(mcx - arc_r - 1, ay, mcx + arc_r + 1, ay + arc_r + 1))
    stem = sbox(mcx - lw / 2, ay + arc_r - lw, mcx + lw / 2, my1)
    mic = d_of(unary_union([poly_of(capsule), holder, stem]))
    ds_src = [hand, mic]
    G = "#44a148"
    out = {}
    for st, title, base, bx in (("faithful", "Faithful", lambda i: fam.plate(i, G), box_c(64, 62, 70)),
                                ("disc", "Sound Disc", lambda i: fam.disc(i, G), box_c(64, 63, 74)),
                                ("rimmed", "Rimmed", lambda i: fam.rimmed(i, G), box_c(64, 63, 64))):
        ic = gk.Icon(f"BCR - {title}", note("bcr", "white handset + white mic"))
        base(ic)
        ds, _ = place(ds_src, bx)
        raised(ic, [(d, "#ffffff") for d in ds], lift=2)
        out[st] = ic
    ic = gk.Icon("BCR - Free Symbol", note("bcr", "green handset + mic objects"))
    ds, _ = place(ds_src, box_c(64, 62, 104))
    with ic.group("body"):
        for i, d in enumerate(ds):
            x0, _, x1, _ = gk.bbox_d(d)
            ic.path(gk.translate_d(d, 0, 4), ic.chin_gradient(G, x0, x1, 12), layer_id=f"b{i}-chin", fill_rule="evenodd")
        for i, d in enumerate(ds):
            ic.path(d, G, layer_id=f"b{i}-face", fill_rule="evenodd")
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Hesap Makinesi
@build
def hesap_makinesi():
    """Calculator + stationery: the two calculator keys (measured split x 63.9 / top 62.3,
    colours #78909c / #546e7a) become raised keys with the traced '+' and '=', the
    stationery (traced colour regions above the keys) stands on them. Dropped: the long
    diagonal shadow. Symbol: the key block as the object, stationery standing on it."""
    a, s = gt.load(WORK / "hesap_makinesi")
    KT, SX = 62.3, 63.9
    TOP, LK, RK = "#455a64", "#78909c", "#546e7a"
    H = a.shape[0]
    Y = np.mgrid[0:H, 0:H][0] * s
    top_area = (Y < KT - 0.5) & gt.opaque(a)
    diff = np.linalg.norm(a[..., :3] - gt.hexrgb(TOP), axis=-1) > 0.18
    items = []
    for col in ("#d4c915", "#ef4336", "#24b6cf", "#8bc34a", "#e3ebef"):
        c = gt.hexrgb(col)
        m = top_area & diff & (np.linalg.norm(a[..., :3] - c, axis=-1) < 0.22)
        m = ndimage.binary_opening(m, iterations=2)
        if m.sum() > 0.0015 * m.size:
            items.append((trace(ndimage.binary_dilation(m, iterations=3), s), col))
    keys_area = (Y >= KT + 1) & gt.opaque(a)
    sym = keys_area & (lum(a) > 0.85)
    sym_d = trace(sym, s)
    lkey = gk.rrect_d(0, KT, SX, 128 - KT, 6)
    rkey = gk.rrect_d(SX, KT, 128 - SX, 128 - KT, 6)

    def compose(ic, x0, y0, size, gap=2.0, depth=3):
        sc = size / 128
        m = lambda d: gk.xform_d(d, sc, x0, y0, about=(0, 0))  # noqa: E731
        lk = m(gk.rrect_d(gap, KT, SX - 1.5 * gap, 128 - KT - gap, 6))
        rk = m(gk.rrect_d(SX + gap / 2, KT, 128 - SX - 1.5 * gap, 128 - KT - gap, 6))
        with ic.group("keys"):
            for n, (d, c) in enumerate(((lk, LK), (rk, RK))):
                x_0, _, x_1, _ = gk.bbox_d(d)
                ic.path(gk.translate_d(d, 0, depth), ic.chin_gradient(c, x_0, x_1, 6), layer_id=f"key{n}-chin")
                ic.path(d, c, layer_id=f"key{n}-face")
        raised(ic, [(m(sym_d), "#ffffff")], lift=1, layer="ops")
        raised(ic, [(m(d), c) for d, c in items], lift=1.5, layer="stationery")

    out = {}
    ic = gk.Icon("Hesap Makinesi - Faithful", note("hesap_makinesi", "raised keys, no long shadow")); fam.plate(ic, TOP)
    compose(ic, 12 + 6, 12 + 4, 92); out["faithful"] = ic
    ic = gk.Icon("Hesap Makinesi - Sound Disc", note("hesap_makinesi", "keys + stationery in the disc")); fam.disc(ic, TOP)
    compose(ic, 64 - 41.5, 63 - 43.5, 83); out["disc"] = ic
    ic = gk.Icon("Hesap Makinesi - Rimmed", note("hesap_makinesi", "keys + stationery in the rim")); fam.rimmed(ic, TOP)
    compose(ic, 64 - 37.5, 63 - 39.5, 75); out["rimmed"] = ic
    ic = gk.Icon("Hesap Makinesi - Free Symbol", note("hesap_makinesi", "key block as the object"))
    compose(ic, 64 - 56, 118 - 112 - 4, 112, depth=5); out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Clash Royale
@build
def clash_royale():
    """A 128 px icon cannot hold the two-king poster (archetype H). Kept: the left king's
    gold crown with its blue band (traced), the blue-vs-red split of the two kings
    (measured #06a1ff / #fe0c0c) divided along the measured lightning centre line."""
    a, s = gt.load(WORK / "clash_royale")
    H = a.shape[0]
    Y, X = np.mgrid[0:H, 0:H] * s
    r, g_, b = a[..., 0], a[..., 1], a[..., 2]
    gold_all = (r > 0.70) & (g_ > 0.40) & (g_ < 0.92) & (b < 0.55) & (X < 70) & (Y < 55)
    comps = gt.components(ndimage.binary_opening(gold_all, iterations=2))
    gold = comps[0]
    gx0, gy0, gx1, gy1 = gt.bbox(gold, s)
    # blue band: the rows just under the gold crown, within its width
    band = (b > r + 0.25) & (b > 0.55) & (X > gx0 - 3) & (X < gx1 + 3) & (Y > gy1 - 3) & (Y < gy1 + 13)
    band = gt.components(ndimage.binary_opening(ndimage.binary_fill_holes(band), iterations=3))[0]
    # jewel: the gold diamond sitting on the band
    jewel = [c for c in comps[1:6] if (c & ndimage.binary_dilation(band, iterations=6)).any() and c.sum() > 0.0004 * c.size]
    jewel = jewel[0] if jewel else np.zeros_like(gold)
    crown_gold = trace(gold, s, smooth_u=0.8)
    # the band is one strip; hair overlapping it in the poster bites notches -> convex hull
    crown_band = d_of(poly_of(trace(band, s, smooth_u=1.0)).convex_hull)
    crown_jewel = trace(jewel, s, smooth_u=0.6) if jewel.any() else ""
    # lightning centre line: brightest cyan-white pixels in the middle columns, per row
    bolt = (lum(a) > 0.86) & (b > 0.85) & (X > 40) & (X < 90)
    pts = []
    for yy in range(0, 129, 8):
        rows = (Y > yy - 4) & (Y < yy + 4) & bolt
        if rows.sum() > 20:
            pts.append((float(np.median(X[rows])), float(yy)))
    if len(pts) < 3:
        pts = [(64, 0), (64, 128)]
    pts = [(pts[0][0], -10)] + pts + [(pts[-1][0], 140)]
    BL, RD = "#1ea7ff", "#f5262c"

    def split(ic, shape, mapf):
        line = [mapf(x, y) for x, y in pts]
        left = Polygon([(-50, line[0][1]), *line, (-50, line[-1][1])]).buffer(0)
        ic.path(d_of(shape.intersection(left)), BL, layer_id="blue")
        ic.path(d_of(shape.difference(left)), RD, layer_id="red")
        ic.path(d_of(LineString(line).buffer(1.8).intersection(shape)), "#d0fdff", layer_id="bolt")

    def crown(ic, box, depth=2):
        src = [crown_gold, crown_band] + ([crown_jewel] if crown_jewel else [])
        ds, _ = place(src, box, ref=[crown_gold, crown_band])
        GOLD = "#f6b833"
        with ic.group("crown"):
            ic.path(gk.translate_d(ds[0], 0, depth), shade(GOLD, -0.18), layer_id="crown-side", fill_rule="evenodd")
            ic.path(gk.translate_d(ds[1], 0, depth), shade("#3f6fd8", -0.12), layer_id="band-side", fill_rule="evenodd")
            ic.path(ds[0], GOLD, layer_id="crown-gold", fill_rule="evenodd")
            ic.path(ds[1], "#3f6fd8", layer_id="crown-band", fill_rule="evenodd")
            if len(ds) > 2:
                ic.path(gk.translate_d(ds[2], 0, 1), shade(GOLD, -0.18), layer_id="jewel-side")
                ic.path(ds[2], "#ffcf5c", layer_id="jewel")

    out = {}
    ic = gk.Icon("Clash Royale - Faithful", note("clash_royale", "crown emblem on the blue/red split"))
    chin = ic.chin_gradient(RD, 12, 116, 8)
    with ic.group("plate"):
        ic.path(gk.rrect_d(12, 16, 104, 100, 8), chin, layer_id="plate-chin")
    split(ic, face_shape("plate"), lambda x, y: (12 + x * 104 / 128, 12 + y * 100 / 128))
    crown(ic, box_c(64, 60, 72, 56)); out["faithful"] = ic
    for st, title, kind in (("disc", "Sound Disc", "disc"), ("rimmed", "Rimmed", "rimmed")):
        ic = gk.Icon(f"Clash Royale - {title}", note("clash_royale", "crown emblem on the blue/red split"))
        if kind == "disc":
            ic.path(gk.circle_d(64, 65, 59), ic.chin_gradient(RD, 5, 123, 53), layer_id="disc-chin")
            split(ic, face_shape("disc"), lambda x, y: (5 + x * 118 / 128, 4 + y * 118 / 128))
            crown(ic, box_c(64, 60, 76, 58))
        else:
            ic.rimmed_disc(inner=RD)
            split(ic, face_shape("rimmed"), lambda x, y: (10.5 + x * 107 / 128, 9.5 + y * 107 / 128))
            crown(ic, box_c(64, 61, 66, 50))
        out[st] = ic
    ic = gk.Icon("Clash Royale - Free Symbol", note("clash_royale", "the crown alone"))
    crown(ic, box_c(64, 70, 110, 90), depth=4); out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Survivor.io
@build
def survivor_io():
    """Archetype H: the poster is reduced to its hero's head (witch hat, ears, face) - the
    head region's colour regions traced flat (5 colours) on the measured purple, cut by the
    face shape like an avatar. Dropped: coins, pumpkin, publisher badge. No Symbol."""
    import auto
    a, s = gt.load(WORK / "survivor_io")
    H = a.shape[0]
    Y, X = np.mgrid[0:H, 0:H] * s
    g, model = auto.ground_model(a)
    resid = np.linalg.norm(a[..., :3] - model, axis=-1)
    crop = (X > 22) & (X < 106) & (Y < 82)
    m = gt.opaque(a) & (resid > 0.20) & crop
    m = gt.components(ndimage.binary_closing(m, iterations=2))[0]
    regs, _ = auto.regions(a, m, max_k=5, merge_de=16)
    parts = [(trace(ndimage.binary_dilation(mm, iterations=3), s), auto.hexc(np.median(a[mm][:, :3], 0)) if False else c)
             for mm, c in regs]
    P1, P2 = "#521874", "#2e0a4a"

    def snapc(c):
        return INK if fam.gk.hex_to_oklab(c)[0] < 0.2 else c

    out = {}
    for st, title, kind, (x0, y0, size) in (("faithful", "Faithful", "plate", (12 - 6, 12, 116)),
                                            ("disc", "Sound Disc", "disc", (0, 6, 128)),
                                            ("rimmed", "Rimmed", "rimmed", (8, 12, 112))):
        ic = gk.Icon(f"Survivor.io - {title}", note("survivor_io", "hero head emblem"))
        if kind == "plate":
            fam.plate(ic, P1, ic.linear([(0, P2), (1, P1)], 0, 12, 0, 112), P1)
        elif kind == "disc":
            fam.disc(ic, P1, ic.linear([(0, P2), (1, P1)], 0, 4, 0, 122), P1, top_light=0)
        else:
            ic.rimmed_disc(inner=P1, inner_gradient=ic.linear([(0, P2), (1, P1)], 0, 10, 0, 117))
        sc = size / 84.0
        for i, (d, c) in enumerate(parts):
            dd = gk.xform_d(d, sc, x0 - 22 * sc, y0, about=(0, 0))
            ic.path(clip(dd, kind), snapc(c), layer_id=f"head{i}", fill_rule="evenodd")
        out[st] = ic
    return out


if __name__ == "__main__":
    for slug in (sys.argv[1:] or B):
        try:
            for st, ic in B[slug]().items():
                fam.save(ic, slug, st)
            for st in ("faithful", "disc", "rimmed", "symbol"):
                p = WORK / slug / f"{slug}-{st}.svg"
                if st not in B[slug].__code__.co_consts and False:
                    pass
            print(slug, "ok")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(slug, "ERROR", repr(e))
