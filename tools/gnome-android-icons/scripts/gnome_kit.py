#!/usr/bin/env python3
"""gnome_kit - build GNOME/Adwaita-style app icons as clean, editable SVG.

A small construction library that encodes what the official GNOME icons
actually do (measured in references/measured-style.md):

  * 128 x 128 canvas, template shapes: circle d120, square 104 (r8),
    portrait 88x112, landscape 112x88; baseline guide at y=117
  * the "chin": a darker copy of the silhouette shifted DOWN (4 px on slabs,
    2 px on discs) painted under the face - never a blurred drop shadow
  * the chin gradient: horizontal, darker edge -> highlight at the rounded
    corners -> base -> ... mirrored (official stops ~0, r/2w, r/w)
  * glyph lift: a symbol on a face gets its own 1-2 px darker copy below it
    (#c0bfbc for white glyphs, like Mousai, Clocks, Software)
  * flat fills on flat faces; gradients only on curved faces
  * no filters, no blur, no raster, no text, no strokes for big shapes

Everything produced is plain <path>/<linearGradient>/<radialGradient> with
named layers, so a human can open it in Inkscape and keep editing.

Library use (write a small build script per icon - new_icon.py scaffolds one):

    from gnome_kit import Icon, fit_parts, rrect_d
    ic = Icon("Example", source_note="geometry: traced from user's PNG")
    box = ic.plate("square", face="#3584e4", r=16)          # face + 4 px chin
    parts = fit_parts(MARK_PARTS, box=ic.safe_box(box))     # scale traced mark into the plate
    ic.glyphs(parts, fill="#ffffff", lift=2)                # every piece raised 2 px
    ic.save("work/example-faithful.svg")

CLI:  gnome_kit.py skeleton disc|rimmed|square|portrait|landscape OUT.svg [--color #hex]
      gnome_kit.py chin '#hex'          (chin colours derived from a face colour)
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import shade, hue_of, hex_to_oklab, HIG_PALETTE  # noqa: E402

# ----------------------------------------------------------------- constants
CANVAS = 128
BASELINE = 117
TEMPLATES = {
    "circle": dict(cx=64, cy=64, r=60),
    "square": dict(x=12, y=12, w=104, h=104, r=8),
    "portrait": dict(x=20, y=8, w=88, h=112, r=8),
    "landscape": dict(x=8, y=28, w=112, h=88, r=8),
}
NEUTRAL = {"white": "#ffffff", "paper": "#f6f5f4", "rim_chin": "#d5d3cf", "lift": "#c0bfbc",
           "light3": "#deddda", "dark": "#241f31", "dark3": "#3d3846"}

_ARITY = dict(M=2, L=2, H=1, V=1, C=6, S=4, Q=4, T=2, A=7, Z=0)


# ----------------------------------------------------------------- number / path helpers
def f(v: float) -> str:
    return ("%.3f" % v).rstrip("0").rstrip(".")


def _round_d(d: str, nd: int = 3) -> str:
    return re.sub(r"-?\d+\.\d+(?:e-?\d+)?", lambda m: f(round(float(m.group(0)), nd)), d)


def rrect_d(x, y, w, h, r) -> str:
    r = min(r, w / 2, h / 2)
    return (f"M{f(x + r)} {f(y)}H{f(x + w - r)}A{f(r)} {f(r)} 0 0 1 {f(x + w)} {f(y + r)}"
            f"V{f(y + h - r)}A{f(r)} {f(r)} 0 0 1 {f(x + w - r)} {f(y + h)}"
            f"H{f(x + r)}A{f(r)} {f(r)} 0 0 1 {f(x)} {f(y + h - r)}V{f(y + r)}"
            f"A{f(r)} {f(r)} 0 0 1 {f(x + r)} {f(y)}Z")


def circle_d(cx, cy, r) -> str:
    return (f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)}Z")


def ellipse_d(cx, cy, rx, ry, rot=0.0) -> str:
    """Ellipse as a path (optionally rotated, degrees)."""
    if not rot:
        return (f"M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 1 {f(cx + rx)} {f(cy)}"
                f"A{f(rx)} {f(ry)} 0 1 1 {f(cx - rx)} {f(cy)}Z")
    t = math.radians(rot)
    x1, y1 = cx - rx * math.cos(t), cy - rx * math.sin(t)
    x2, y2 = cx + rx * math.cos(t), cy + rx * math.sin(t)
    return (f"M{f(x1)} {f(y1)}A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(x2)} {f(y2)}"
            f"A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(x1)} {f(y1)}Z")


def capsule_d(x1, y1, x2, y2, w) -> str:
    """Rounded stroke-like bar from (x1,y1) to (x2,y2) with width w, as a filled path."""
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    r = w / 2
    return (f"M{f(x1 + nx)} {f(y1 + ny)}L{f(x2 + nx)} {f(y2 + ny)}"
            f"A{f(r)} {f(r)} 0 0 0 {f(x2 - nx)} {f(y2 - ny)}L{f(x1 - nx)} {f(y1 - ny)}"
            f"A{f(r)} {f(r)} 0 0 0 {f(x1 + nx)} {f(y1 + ny)}Z")


def polygon_d(points, close=True) -> str:
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in points)
    return d + ("Z" if close else "")


def rounded_polygon_d(points, radius) -> str:
    """Polygon with rounded corners (quadratic joins). `radius` may be one value or one per point."""
    n = len(points)
    rs = radius if isinstance(radius, (list, tuple)) else [radius] * n
    out = []
    for i in range(n):
        p0, p1, p2 = points[i - 1], points[i], points[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        r = min(rs[i], l1 / 2, l2 / 2)
        a = (p1[0] + v1[0] / l1 * r, p1[1] + v1[1] / l1 * r)
        b = (p1[0] + v2[0] / l2 * r, p1[1] + v2[1] / l2 * r)
        out.append(("M" if i == 0 else "L") + f"{f(a[0])} {f(a[1])}Q{f(p1[0])} {f(p1[1])} {f(b[0])} {f(b[1])}")
    return "".join(out) + "Z"


def xform_d(d: str, s: float = 1.0, dx: float = 0.0, dy: float = 0.0, about=(64.0, 64.0),
            sy: float | None = None) -> str:
    """Scale a path about a point and translate it, writing new absolute coordinates.

    Use this (not a <g transform>) for glyphs that get a lift/chin, so the
    2-4 px depth stays 2-4 px regardless of the glyph's scale.
    """
    from svgpathtools import parse_path
    p = parse_path(d)
    ax, ay = about
    sy = s if sy is None else sy
    p = p.translated(complex(-ax, -ay)).scaled(s, sy).translated(complex(ax + dx, ay + dy))
    return _round_d(p.d())


def translate_d(d: str, dx: float, dy: float) -> str:
    """Translate a path. Keeps the original commands (absolute coordinates shifted,
    relative ones untouched); falls back to svgpathtools for unusual syntax
    (e.g. compact arc flags like 'a1 1 0 011 1')."""
    toks = re.findall(r"[MLHVCSQTAZmlhvcsqtaz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    out, groups = [], []
    cmd, args = None, []
    for t in toks:
        if t.isalpha():
            if cmd is not None:
                groups.append((cmd, args))
            cmd, args = t, []
        else:
            args.append(float(t))
    if cmd is not None:
        groups.append((cmd, args))
    first = True
    for cmd, vals in groups:
        n = _ARITY[cmd.upper()]
        if n == 0:
            out.append(cmd)
            continue
        if len(vals) % n:
            return xform_d(d, 1.0, dx, dy)  # unusual syntax -> safe path
        chunks = [vals[k:k + n] for k in range(0, len(vals), n)]
        res = []
        for j, ch in enumerate(chunks):
            ch = list(ch)
            up = cmd.upper()
            if cmd.isupper():
                if up in "MLCSQT":
                    ch = [v + (dx if i % 2 == 0 else dy) for i, v in enumerate(ch)]
                elif up == "H":
                    ch[0] += dx
                elif up == "V":
                    ch[0] += dy
                elif up == "A":
                    if ch[3] not in (0, 1) or ch[4] not in (0, 1):
                        return xform_d(d, 1.0, dx, dy)
                    ch[5] += dx
                    ch[6] += dy
            elif cmd == "m" and first and j == 0:
                ch[0] += dx
                ch[1] += dy
            res.append(" ".join(f(v) for v in ch))
        first = False
        out.append(cmd + " ".join(res))
    return "".join(out)


def bbox_d(d: str):
    """(x0, y0, x1, y1) of one path or an iterable of paths."""
    from svgpathtools import parse_path
    ds = [d] if isinstance(d, str) else list(d)
    xs0, ys0, xs1, ys1 = [], [], [], []
    for one in ds:
        x0, x1, y0, y1 = parse_path(one).bbox()
        xs0.append(x0), xs1.append(x1), ys0.append(y0), ys1.append(y1)
    return min(xs0), min(ys0), max(xs1), max(ys1)


def fit_parts(parts, box=None, cx=64.0, cy=63.0, max_w=72.0, max_h=72.0):
    """Scale + move a set of paths (dict or list) as ONE unit so its bounding box
    fits `box` (x0, y0, x1, y1) or a max_w x max_h area centred on (cx, cy).
    Proportions are preserved (identity geometry is never distorted)."""
    items = list(parts.items()) if isinstance(parts, dict) else list(enumerate(parts))
    x0, y0, x1, y1 = bbox_d([d for _, d in items])
    if box:
        bx0, by0, bx1, by1 = box
        cx, cy, max_w, max_h = (bx0 + bx1) / 2, (by0 + by1) / 2, bx1 - bx0, by1 - by0
    s = min(max_w / (x1 - x0), max_h / (y1 - y0))
    ox, oy = (x0 + x1) / 2, (y0 + y1) / 2
    moved = [(k, xform_d(d, s, cx - ox, cy - oy, about=(ox, oy))) for k, d in items]
    return dict(moved) if isinstance(parts, dict) else [d for _, d in moved]


# ----------------------------------------------------------------- colour roles
def chin_colors(face: str, depth: str = "normal") -> dict:
    """Chin colours derived from a face colour, calibrated on official icons.

    normal faces : green3 #33d17a -> base #26a269-ish, edge darker, highlight ~ face
    dark faces   : (OKLab L < 0.42, e.g. #3d3846) a darker chin would vanish on dark
                   wallpapers, so the base stays close and the corner highlights get
                   LIGHTER - the way Console/Turntable keep their edges readable
    light neutral: (#f6f5f4 paper) uses the official rim greys #d5d3cf / #deddda
    """
    k = {"soft": 0.7, "normal": 1.0, "strong": 1.3}[depth]
    L, a, b = hex_to_oklab(face)
    chroma = math.hypot(a, b)
    if L < 0.42:
        return {"edge": shade(face, -0.08 * k), "base": shade(face, -0.05 * k),
                "highlight": shade(face, 0.20)}
    if L > 0.88 and chroma < 0.03:
        return {"edge": shade(face, -0.16 * k), "base": shade(face, -0.11 * k),
                "highlight": shade(face, -0.07 * k)}
    hue = hue_of(face)
    warm = -10.0 if 40 <= hue <= 115 else (-5.0 if hue < 40 or hue > 340 else 0.0)  # warm hues deepen to red
    return {"edge": shade(face, -0.19 * k, 0.76, warm * 1.2),
            "base": shade(face, -0.115 * k, 0.86, warm),
            "highlight": shade(face, -0.02, 0.97)}


def lift_color(glyph_fill: str, face: str | None = None) -> str:
    """Side colour of a raised glyph: white/paper glyph -> Light4 #c0bfbc;
    otherwise the glyph colour darkened (its own side, not a shadow)."""
    if glyph_fill.lower() in ("#ffffff", "#fff", "#f6f5f4", "#fafafa"):
        return NEUTRAL["lift"]
    L, _, _ = hex_to_oklab(glyph_fill)
    return shade(glyph_fill, -0.14 if L > 0.42 else -0.06)


# ----------------------------------------------------------------- icon builder
class Icon:
    def __init__(self, title: str, source_note: str = "", license: str = "", author: str = ""):
        self.title, self.source_note, self.license, self.author = title, source_note, license, author
        self.defs: list[str] = []
        self.layers: list[str] = []
        self._gid = 0

    # -- low level
    def _id(self, stem):
        self._gid += 1
        return f"{stem}{self._gid}"

    def raw(self, svg: str, layer: str | None = None):
        self.layers.append(svg if layer is None else f'<g id="{layer}">{svg}</g>')

    def path(self, d, fill, layer_id=None, opacity=None, fill_rule=None, extra=""):
        a = f' id="{layer_id}"' if layer_id else ""
        o = f' opacity="{f(opacity)}"' if opacity is not None and opacity < 1 else ""
        fr = f' fill-rule="{fill_rule}"' if fill_rule else ""
        self.layers.append(f'<path{a} d="{d}" fill="{fill}"{o}{fr}{extra}/>')

    def group(self, layer: str):
        """Context manager: with ic.group("mark"): ... wraps layers in <g id=...>."""
        ic = self

        class _G:
            def __enter__(self_):
                ic.layers.append(f'<g id="{layer}">')

            def __exit__(self_, *exc):
                ic.layers.append("</g>")
        return _G()

    @staticmethod
    def _stops(stops):
        out = []
        for s in stops:
            o, c, op = (s + (None,))[:3] if len(s) == 2 else s
            out.append(f'<stop offset="{f(o)}" stop-color="{c}"' + (f' stop-opacity="{f(op)}"' if op is not None else "") + "/>")
        return "".join(out)

    def linear(self, stops, x1, y1, x2, y2, gid=None) -> str:
        gid = gid or self._id("g")
        self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" '
                         f'x2="{f(x2)}" y2="{f(y2)}">{self._stops(stops)}</linearGradient>')
        return f"url(#{gid})"

    def radial(self, stops, cx, cy, r, fx=None, fy=None, gid=None) -> str:
        gid = gid or self._id("r")
        fxy = (f' fx="{f(fx)}"' if fx is not None else "") + (f' fy="{f(fy)}"' if fy is not None else "")
        self.defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" '
                         f'r="{f(r)}"{fxy}>{self._stops(stops)}</radialGradient>')
        return f"url(#{gid})"

    def chin_gradient(self, face: str, x0: float, x1: float, corner_r: float, depth="normal",
                      colors: dict | None = None, corners: str = "both") -> str:
        """The official horizontal chin gradient with corner highlights.

        corners: "both" | "left" | "right" | "none" - put highlights only where the
        silhouette really has a rounded bottom corner (a sharp inner corner, e.g. at
        a split, must not get one).
        """
        c = colors or chin_colors(face, depth)
        w = max(x1 - x0, 1)
        p1 = min(0.45, corner_r * 0.5 / w)
        p2 = min(0.48, corner_r / w)
        left = [(0, c["edge"]), (p1, c["highlight"]), (p2, c["base"])] if corners in ("both", "left") else [(0, c["base"])]
        right = [(1 - p2, c["base"]), (1 - p1, c["highlight"]), (1, c["edge"])] if corners in ("both", "right") else [(1, c["base"])]
        return self.linear(left + right, x0, 0, x1, 0)

    def safe_box(self, face_box: dict, pad: float = 0.18):
        """Inner area of a plate/disc face where a mark should sit (fraction `pad` per side).
        Optically centred 1 px above the geometric centre, like official icons."""
        if "r" in face_box and "cx" in face_box:
            r = face_box["r"] * (1 - pad) * 0.86
            return (face_box["cx"] - r, face_box["cy"] - r - 1, face_box["cx"] + r, face_box["cy"] + r - 1)
        x, y, w, h = face_box["x"], face_box["y"], face_box["w"], face_box["h"]
        return (x + w * pad, y + h * pad - 1, x + w * (1 - pad), y + h * (1 - pad) - 1)

    # -- high level building blocks
    def slab(self, d: str, face, bbox=None, corner_r=8, depth=4, chin=None, layer="slab", depth_style="normal",
             fill_rule=None, corners="both"):
        """Any silhouette + its chin: the shape copied `depth` px down (chin gradient), face on top.
        bbox: (x0, x1) for the chin gradient; measured from the path when omitted."""
        if bbox is None:
            x0, _, x1, _ = bbox_d(d)
            bbox = (x0, x1)
        base_hex = face if face.startswith("#") else "#888888"
        chin_fill = chin or self.chin_gradient(base_hex, bbox[0], bbox[1], corner_r, depth_style, corners=corners)
        with self.group(layer):
            self.path(translate_d(d, 0, depth), chin_fill, layer_id=f"{layer}-chin", fill_rule=fill_rule)
            self.path(d, face, layer_id=f"{layer}-face", fill_rule=fill_rule)

    def pieces(self, parts, face, depth=4.0, chin=None, corner_r=8, layer="mark", fill_rule="evenodd",
               face_fill=None):
        """Extrude a multi-piece mark coherently: ALL chins first, then ALL faces, so
        no piece's chin is painted over a neighbour's face (letters, dots, antennae).
        parts: dict name->d or list of d. face: hex used to derive the chin.
        face_fill: optional fill for the faces (e.g. a gradient url) - defaults to face."""
        items = list(parts.items()) if isinstance(parts, dict) else [(f"p{i}", d) for i, d in enumerate(parts)]
        x0, _, x1, _ = bbox_d([d for _, d in items])
        chin_fill = chin or self.chin_gradient(face, x0, x1, corner_r)
        with self.group(layer):
            for k, d in items:
                self.path(translate_d(d, 0, depth), chin_fill, layer_id=f"{layer}-{k}-chin", fill_rule=fill_rule)
            for k, d in items:
                self.path(d, face_fill or face, layer_id=f"{layer}-{k}-face", fill_rule=fill_rule)

    def plate(self, shape="square", face="#3584e4", depth=4, chin=None, r=None, layer="plate", **over):
        """Template plate (square/portrait/landscape) with chin; returns the FACE box."""
        t = dict(TEMPLATES[shape])
        t.update(over)
        if shape == "circle":
            return self.disc(face=face, chin=chin, r=t["r"] - 1, layer=layer)
        rr = t["r"] if r is None else r
        h = t["h"] - depth
        d = rrect_d(t["x"], t["y"], t["w"], h, rr)
        self.slab(d, face, (t["x"], t["x"] + t["w"]), corner_r=rr, depth=depth, chin=chin, layer=layer)
        return dict(x=t["x"], y=t["y"], w=t["w"], h=h, r=rr)

    def disc(self, face="#3584e4", r=59, cx=64, cy=63, chin=None, chin_dy=2.0, layer="disc",
             curvature=True, top_light=0.0):
        """GNOME disc: chin circle 2 px lower, face circle on top; returns the face circle.

        curvature : subtle top-to-bottom light falloff allowed on curved faces
        top_light : 0..1 strength of a broad soft top light (the 'Sound Disc' look)
        """
        base_hex = face if face.startswith("#") else "#888888"
        chin_fill = chin or self.chin_gradient(base_hex, cx - r, cx + r, r * 0.9)
        with self.group(layer):
            self.path(circle_d(cx, cy + chin_dy, r), chin_fill, layer_id=f"{layer}-chin")
            fill = face
            if curvature and face.startswith("#"):
                fill = self.linear([(0, shade(face, 0.035)), (0.55, face), (1, shade(face, -0.03))],
                                   0, cy - r, 0, cy + r)
            self.path(circle_d(cx, cy, r), fill, layer_id=f"{layer}-face")
            if top_light > 0:
                g = self.radial([(0, "#ffffff", 0.20 * top_light), (0.6, "#ffffff", 0.06 * top_light), (1, "#ffffff", 0)],
                                cx, cy - r * 0.75, r * 1.15)
                self.path(circle_d(cx, cy, r), g, layer_id=f"{layer}-sheen")
        return dict(cx=cx, cy=cy, r=r)

    def rimmed_disc(self, inner="#3584e4", r=59, rim=5.5, cx=64, cy=63, rim_face=NEUTRAL["paper"],
                    rim_chin=NEUTRAL["rim_chin"], layer="rim", inner_shadow=0.10, inner_gradient=None):
        """Clocks/Mousai construction: light rim with chin + recessed coloured inner disc."""
        with self.group(layer):
            cg = self.chin_gradient(rim_chin, cx - r, cx + r, r * 0.9,
                                    colors={"edge": shade(rim_chin, -0.06), "base": rim_chin, "highlight": NEUTRAL["light3"]})
            self.path(circle_d(cx, cy + 2, r), cg, layer_id=f"{layer}-chin")
            self.path(circle_d(cx, cy, r), rim_face, layer_id=f"{layer}-face")
            ri = r - rim
            fill = inner_gradient or (self.linear([(0, shade(inner, 0.03)), (1, shade(inner, -0.04))], 0, cy - ri, 0, cy + ri)
                                      if inner.startswith("#") else inner)
            self.path(circle_d(cx, cy, ri), fill, layer_id=f"{layer}-inner")
            if inner_shadow:
                d = circle_d(cx, cy, ri) + circle_d(cx, cy + 1.2, ri)
                self.path(d, "#000000", layer_id=f"{layer}-recess", opacity=inner_shadow, fill_rule="evenodd")
        return dict(cx=cx, cy=cy, r=ri)

    def glyph(self, d, fill="#ffffff", lift=2.0, lift_fill=None, layer="glyph", transform=None, engrave=False,
              face_hint=None, fill_rule=None):
        """A symbol on a face. lift>0: its side, `lift` px below (raised mark).
        engrave=True: a lighter copy below at 55 % (recessed/engraved mark).
        fill_rule="evenodd" for marks with counters (letters, rings, cut-outs)."""
        t = f' transform="{transform}"' if transform else ""
        fr = f' fill-rule="{fill_rule}"' if fill_rule else ""
        self.layers.append(f'<g id="{layer}"{t}>')
        if lift:
            if lift_fill is None:
                lift_fill = (shade(face_hint, 0.10) if (engrave and face_hint) else "#ffffff") if engrave \
                    else lift_color(fill, face_hint)
            op = ' opacity="0.55"' if engrave else ""
            self.layers.append(f'<path id="{layer}-lift" d="{translate_d(d, 0, lift)}" fill="{lift_fill}"{op}{fr}/>')
        self.layers.append(f'<path id="{layer}-face" d="{d}" fill="{fill}"{fr}/>')
        self.layers.append("</g>")

    def glyphs(self, parts, fill="#ffffff", lift=2.0, lift_fill=None, layer="mark", fill_rule="evenodd"):
        """Several raised pieces sharing one look: all sides first, then all faces."""
        items = list(parts.items()) if isinstance(parts, dict) else [(f"p{i}", d) for i, d in enumerate(parts)]
        lf = lift_fill or lift_color(fill)
        fr = f' fill-rule="{fill_rule}"' if fill_rule else ""
        with self.group(layer):
            if lift:
                for k, d in items:
                    self.layers.append(f'<path id="{layer}-{k}-lift" d="{translate_d(d, 0, lift)}" fill="{lf}"{fr}/>')
            for k, d in items:
                self.layers.append(f'<path id="{layer}-{k}-face" d="{d}" fill="{fill}"{fr}/>')

    # -- output
    def svg(self) -> str:
        meta = escape(" | ".join(x for x in [self.source_note, f"licence: {self.license}" if self.license else "",
                                             f"author: {self.author}" if self.author else ""] if x))
        head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">\n'
                f'  <title>{escape(self.title)}</title>\n')
        if meta:
            head += f"  <desc>{meta}</desc>\n"
        defs = "  <defs>\n    " + "\n    ".join(self.defs) + "\n  </defs>\n" if self.defs else ""
        body = "\n".join("  " + layer for layer in self.layers)
        return head + defs + body + "\n</svg>\n"

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.svg(), encoding="utf-8")
        return path


# ----------------------------------------------------------------- sweep chin (thin shapes)
def sweep_chin_d(d: str, depth: float = 4.0, step: float = 0.5, samples: int = 64) -> str:
    """Exact extrusion chin for shapes with parts thinner than `depth`.

    Flattens the path (svgpathtools), unions translated copies (shapely) and
    returns a polygon path. Use only when translate_d() leaves visible gaps
    (check with legibility_check.py or by zooming the render).
    """
    from svgpathtools import parse_path
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from shapely import affinity

    p = parse_path(d)
    polys = []
    for sub in p.continuous_subpaths():
        pts = []
        for seg in sub:
            for k in range(samples):
                z = seg.point(k / samples)
                pts.append((z.real, z.imag))
        if len(pts) > 2:
            polys.append(Polygon(pts).buffer(0))
    shape = polys[0]
    for q in polys[1:]:
        shape = shape.symmetric_difference(q)  # even-odd
    copies = [affinity.translate(shape, 0, t) for t in [i * step for i in range(int(depth / step) + 1)]]
    u = unary_union(copies).simplify(0.05)
    geoms = getattr(u, "geoms", [u])
    out = []
    for g in geoms:
        out.append(polygon_d(list(g.exterior.coords)[:-1]))
        for hole in g.interiors:
            out.append(polygon_d(list(hole.coords)[:-1]))
    return "".join(out)


# ----------------------------------------------------------------- SVG part loading
def load_parts(svg_path: str, prefix: str = "") -> dict:
    """Read every <path d> (in document order) of a trace/official SVG into a dict
    {id or pN: d}. Transforms on parents are NOT applied - use it on flat files
    such as trace_source.py / apk_icon.py output, or flatten first in Inkscape."""
    txt = Path(svg_path).read_text(encoding="utf-8", errors="replace")
    parts = {}
    for i, m in enumerate(re.finditer(r"<path\b([^>]*)>", txt)):
        attrs = m.group(1)
        dm = re.search(r'\sd="([^"]+)"', attrs)
        if not dm:
            continue
        im = re.search(r'\sid="([^"]+)"', attrs)
        key = prefix + (im.group(1) if im else f"p{i}")
        parts[key] = dm.group(1)
    return parts


# ----------------------------------------------------------------- CLI skeletons
def skeleton(kind: str, color: str) -> Icon:
    ic = Icon(f"{kind} skeleton", source_note="gnome-android-icons starter skeleton (CC0)")
    glyph = rrect_d(44, 40, 40, 44, 8)
    if kind == "disc":
        ic.disc(face=color)
        ic.glyph(glyph)
    elif kind == "rimmed":
        ic.rimmed_disc(inner=color)
        ic.glyph(glyph)
    else:
        b = ic.plate(kind, face=color)
        ic.glyph(rrect_d(b["x"] + b["w"] / 2 - 20, b["y"] + b["h"] / 2 - 22, 40, 44, 8))
    return ic


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("skeleton")
    s.add_argument("kind", choices=["disc", "rimmed", "square", "portrait", "landscape"])
    s.add_argument("out")
    s.add_argument("--color", default=HIG_PALETTE["blue"][2])
    c = sub.add_parser("chin", help="print chin colours derived from a face colour")
    c.add_argument("face")
    a = ap.parse_args()
    if a.cmd == "skeleton":
        skeleton(a.kind, a.color).save(a.out)
        print(a.out)
    elif a.cmd == "chin":
        print(chin_colors(a.face))


if __name__ == "__main__":
    main()
