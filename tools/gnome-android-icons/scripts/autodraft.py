#!/usr/bin/env python3
"""autodraft - first-draft alternatives from REAL source geometry.

new_icon.py writes a build.py that calls these helpers. They do the mechanical
part the same way every time:

  * load the source geometry (source-geometry.svg from an SVG/XML/APK input, or
    source-trace.svg from a raster) as ordered parts with their own colours
  * detect a GROUND (tile / disc / container behind the mark) vs the MARK
  * place the mark on each GNOME construction with gnome_kit, keeping the
    mark's proportions (and, for Faithful, its exact size relative to the ground)

The drafts are a STARTING POINT ("level 0-1" in references/identity-preservation.md):
recognisable and correctly constructed, but not yet designed. You still have to
look at them, apply the archetype guidance, refine, and review honestly.

    import autodraft as ad
    src = ad.Source(WORK_DIR)
    ad.draft_faithful(src).save(...)

CLI (inspect what autodraft sees):  autodraft.py WORK_DIR
"""
from __future__ import annotations

import io
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gnome_kit as gk  # noqa: E402
from _common import hex_to_oklab, HIG_PALETTE  # noqa: E402

DEFAULT_COLOR = HIG_PALETTE["blue"][2]      # used when the source has no colour at all
DARK_PLATE = "#3d3846"


def _is_light(h: str) -> bool:
    L, a, b = hex_to_oklab(h)
    return L > 0.9 and math.hypot(a, b) < 0.04


def _is_dark(h: str) -> bool:
    return hex_to_oklab(h)[0] < 0.42


def _area(d: str, rule: str | None = None) -> float:
    """Painted area of one path in 128 units^2 (rasterised, so even-odd/curves are exact enough)."""
    import cairosvg
    import numpy as np
    from PIL import Image
    fr = f' fill-rule="{rule}"' if rule else ""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="256" height="256"><path d="{d}"{fr}/></svg>'
    im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    return float((np.asarray(im)[..., 3] > 127).sum()) / 4.0


class Source:
    """Ordered source parts + ground/mark split + colours, read from a work folder."""

    def __init__(self, work_dir, geometry: str | None = None):
        self.dir = Path(work_dir)
        cand = [geometry] if geometry else ["source-geometry.svg", "source-trace.svg"]
        path = next((self.dir / c for c in cand if c and (self.dir / c).exists()), None)
        if path is None:
            raise FileNotFoundError(f"no source geometry in {self.dir} (run new_icon.py with --input, or trace_source.py)")
        self.geometry_file = path
        txt = path.read_text(encoding="utf-8")
        self.parts = []   # list of dict(id, d, fill, rule)
        for m in re.finditer(r"<path\b([^>]*)/?>", txt):
            at = m.group(1)
            d = re.search(r'\sd="([^"]+)"', at)
            if not d:
                continue
            fill = re.search(r'\sfill="(#[0-9a-fA-F]{6})"', at)
            rule = re.search(r'\sfill-rule="([a-z]+)"', at)
            op = re.search(r'\sopacity="([\d.]+)"', at)
            if op and float(op.group(1)) < 0.5:
                continue   # faint shading layers are not identity geometry
            pid = re.search(r'\sid="([^"]+)"', at)
            grad = re.search(r'\sdata-gradient="([^"]+)"', at)
            stops = [c for c in grad.group(1).split() if re.match(r"^#[0-9a-f]{6}$", c)] if grad else []
            self.parts.append(dict(id=re.sub(r"[^A-Za-z0-9_-]", "_", pid.group(1)) if pid else f"p{len(self.parts)}",
                                   d=d.group(1), fill=(fill.group(1).lower() if fill else "#000000"),
                                   rule=rule.group(1) if rule else None,
                                   gradient=stops if len(set(stops)) > 1 else None))
        if not self.parts:
            raise ValueError(f"{path} has no usable paths")
        self.analysis = {}
        aj = self.dir / "analysis.json"
        if aj.exists():
            self.analysis = json.loads(aj.read_text())
        self._split()

    # ------------------------------------------------------------------ ground / mark
    def _split(self):
        boxes = [gk.bbox_d(p["d"]) for p in self.parts]
        X0, Y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        X1, Y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        self.bbox = (X0, Y0, X1, Y1)
        first, fb = self.parts[0], boxes[0]
        W, H = X1 - X0, Y1 - Y0
        covers = (abs(fb[0] - X0) < 0.04 * W and abs(fb[2] - X1) < 0.04 * W and
                  abs(fb[1] - Y0) < 0.04 * H and abs(fb[3] - Y1) < 0.04 * H)
        self.ground = None
        if covers and len(self.parts) > 1:
            fill_ratio = _area(first["d"], first["rule"]) / max((fb[2] - fb[0]) * (fb[3] - fb[1]), 1)
            if fill_ratio > 0.70:
                self.ground = first
                self.ground_shape = "circle" if (fill_ratio < 0.83 and abs((fb[2] - fb[0]) - (fb[3] - fb[1])) < 0.05 * W) else "square"
                # corner radius of a rounded square: fill = 1 - (4 - pi) r^2 / w^2
                w = fb[2] - fb[0]
                self.ground_radius = w * math.sqrt(max(0.0, 1 - fill_ratio) / (4 - math.pi)) if self.ground_shape == "square" else w / 2
        self.mark = [p for p in self.parts if p is not self.ground]
        self.mark_bbox = gk.bbox_d([p["d"] for p in self.mark])

    # ------------------------------------------------------------------ colours
    @property
    def ground_color(self) -> str | None:
        return self.ground["fill"] if self.ground else None

    @property
    def ground_gradient(self) -> list | None:
        """Gradient stops of the ground when the source used one (flatten_svg keeps them)."""
        return self.ground.get("gradient") if self.ground else None

    def ground_fill(self, ic, box):
        """Fill for a face that stands in for the ground: the source gradient rebuilt as a
        diagonal (bottom-left -> top-right, as on curved GNOME faces) or the flat colour."""
        g = self.ground_gradient
        if not g:
            return self.ground_color
        x0, y0, x1, y1 = box
        n = len(g) - 1
        return ic.linear([(i / n, c) for i, c in enumerate(g)], x0 + (x1 - x0) * 0.15, y1 - (y1 - y0) * 0.15,
                         x1 - (x1 - x0) * 0.15, y0 + (y1 - y0) * 0.15)

    @property
    def mark_colors(self) -> list:
        seen = []
        for p in self.mark:
            if p["fill"] not in seen:
                seen.append(p["fill"])
        return seen

    @property
    def mark_is_light(self) -> bool:
        return all(_is_light(c) for c in self.mark_colors)

    def brand_color(self) -> str:
        """The colour that identifies the app: ground if any, else the first saturated mark colour."""
        if self.ground and not _is_light(self.ground_color):
            return self.ground_color
        for c in self.mark_colors:
            if not _is_light(c) and not _is_dark(c):
                return c
        return DEFAULT_COLOR

    # ------------------------------------------------------------------ placement
    def mark_parts(self, fill_override: str | None = None):
        return {p["id"]: (p["d"], fill_override or p["fill"]) for p in self.mark}

    def place(self, target_box, relative_to_ground=True, max_fill=1.0):
        """Mark parts transformed into target_box (x0,y0,x1,y1).

        relative_to_ground: the GROUND is mapped onto target_box, so the mark keeps its
        original size relative to its tile/disc (Faithful). Otherwise the mark alone is
        fitted into the box (times max_fill)."""
        tx0, ty0, tx1, ty1 = target_box
        if relative_to_ground and self.ground is not None:
            gx0, gy0, gx1, gy1 = gk.bbox_d(self.ground["d"])
            s = min((tx1 - tx0) / (gx1 - gx0), (ty1 - ty0) / (gy1 - gy0))
            ocx, ocy = (gx0 + gx1) / 2, (gy0 + gy1) / 2
        else:
            mx0, my0, mx1, my1 = self.mark_bbox
            s = min((tx1 - tx0) / (mx1 - mx0), (ty1 - ty0) / (my1 - my0)) * max_fill
            ocx, ocy = (mx0 + mx1) / 2, (my0 + my1) / 2
        cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
        return {p["id"]: (gk.xform_d(p["d"], s, cx - ocx, cy - ocy, about=(ocx, ocy)), p["fill"], p["rule"])
                for p in self.mark}

    def describe(self) -> str:
        g = (f"ground: {self.ground['id']} {self.ground_color} ({self.ground_shape}, r~{self.ground_radius:.1f})"
             if self.ground else "ground: none (free mark)")
        return (f"geometry: {self.geometry_file.name} | parts: {len(self.parts)} | {g} | "
                f"mark parts: {len(self.mark)} colours {self.mark_colors} | brand colour {self.brand_color()}")


# ---------------------------------------------------------------------- drafting helpers
def _on_plate_map(src: Source, plate_col: str) -> dict:
    """Mark colours on a plate of plate_col: a mark that is ENTIRELY the plate colour
    would vanish -> make it white. Parts that merely share the plate colour next to
    other colours are cut-outs (they should show the plate) -> keep."""
    cols = set(src.mark_colors)
    return {plate_col: "#ffffff"} if cols == {plate_col} else {}


def _cutouts_to_holes(placed: dict, ground_color: str | None) -> dict:
    """Parts painted in the GROUND colour inside another part are cut-outs (a ring's
    hole, a letter's counter). Without the ground behind them they must become real
    holes: merge them into their container with fill-rule evenodd."""
    if not ground_color:
        return placed
    out = dict(placed)
    boxes = {k: gk.bbox_d(v[0]) for k, v in placed.items()}
    for k, (d, fill, rule) in placed.items():
        if fill != ground_color:
            continue
        bx = boxes[k]
        cands = [c for c, (cd, cf, _) in placed.items() if c != k and cf != ground_color and c in out
                 and boxes[c][0] <= bx[0] and boxes[c][1] <= bx[1] and boxes[c][2] >= bx[2] and boxes[c][3] >= bx[3]]
        if not cands:
            continue
        c = min(cands, key=lambda c: (boxes[c][2] - boxes[c][0]) * (boxes[c][3] - boxes[c][1]))
        cd, cf, _ = out[c]
        out[c] = (cd + d, cf, "evenodd")
        del out[k]
    return out


def _inverted_map(src: Source, col: str) -> dict:
    """Without a coloured plate (Free Symbol, Light): light parts take the brand colour
    and brand-coloured cut-outs become white, so figure/ground stays readable."""
    m = {c: col for c in src.mark_colors if _is_light(c)}
    if m:
        m.update({c: "#ffffff" for c in src.mark_colors if c == col})
    return m



def _raised(ic, placed, lift=2.0, recolor=None, layer="mark", face_fill=None):
    """All sides first, then all faces; per-part colours (recolor maps old->new;
    face_fill maps a final colour to a gradient url for the faces only)."""
    with ic.group(layer):
        for k, (d, fill, rule) in placed.items():
            c = (recolor or {}).get(fill, fill)
            fr = f' fill-rule="{rule}"' if rule else ""
            if lift:
                ic.layers.append(f'<path id="{layer}-{k}-lift" d="{gk.translate_d(d, 0, lift)}" fill="{gk.lift_color(c)}"{fr}/>')
        for k, (d, fill, rule) in placed.items():
            c = (recolor or {}).get(fill, fill)
            c = (face_fill or {}).get(c, c)
            fr = f' fill-rule="{rule}"' if rule else ""
            ic.layers.append(f'<path id="{layer}-{k}-face" d="{d}" fill="{c}"{fr}/>')


def _gradient_faces(ic, src: Source, placed, colours) -> dict:
    """When the source ground is a gradient and a mark takes the ground colour (no plate
    variants), the mark carries that gradient: for gradient brands the ramp is identity."""
    if not src.ground_gradient or src.ground_color not in colours:
        return {}
    box = gk.bbox_d([d for d, _, _ in placed.values()])
    return {src.ground_color: src.ground_fill(ic, box)}


def _note(src: Source) -> str:
    return f"DRAFT by autodraft from {src.geometry_file.name} - refine before release"


def draft_faithful(src: Source, title="Adwaita Faithful"):
    """A: source proportions on the matching template shape, brand colours, chin, lifted mark."""
    ic = gk.Icon(title, source_note=_note(src))
    if src.ground is not None and src.ground_shape == "circle":
        box = (5, 4, 123, 122)
        face = ic.disc(face=src.ground_fill(ic, box), chin=ic.chin_gradient(src.ground_color, 5, 123, 53))
        box = (face["cx"] - face["r"], face["cy"] - face["r"], face["cx"] + face["r"], face["cy"] + face["r"])
        _raised(ic, src.place(box))
        return ic
    if src.ground is not None:
        gw = src.bbox[2] - src.bbox[0]
        r = max(8.0, min(28.0, src.ground_radius * 104 / gw))
        face = ic.plate("square", face=src.ground_fill(ic, (12, 12, 116, 112)),
                        chin=ic.chin_gradient(src.ground_color, 12, 116, r), r=r)
        _raised(ic, src.place((face["x"], face["y"], face["x"] + face["w"], face["y"] + face["h"])))
        return ic
    # free mark: light marks need a plate to be visible; coloured marks get the brand-coloured plate
    plate = DARK_PLATE if src.mark_is_light else src.brand_color()
    recolor = _on_plate_map(src, plate)
    face = ic.plate("square", face=plate, r=20)
    _raised(ic, src.place(ic.safe_box(face, 0.16), relative_to_ground=False), recolor=recolor)
    return ic


def draft_disc(src: Source, title="Sound Disc", top_light=0.7):
    """B: disc face (brand colour), mark scaled to sit inside the circle."""
    ic = gk.Icon(title, source_note=_note(src))
    col = src.brand_color()
    fill = src.ground_fill(ic, (5, 4, 123, 122)) if (src.ground is not None and col == src.ground_color) else col
    face = ic.disc(face=fill, chin=ic.chin_gradient(col, 5, 123, 53), top_light=top_light)
    recolor = _on_plate_map(src, col)
    _raised(ic, _inside_circle(src, face["cx"], face["cy"], face["r"] * 0.78), recolor=recolor)
    return ic


def draft_rimmed(src: Source, title="Rimmed"):
    """C: light Adwaita rim + recessed brand disc."""
    ic = gk.Icon(title, source_note=_note(src))
    col = src.brand_color()
    grad = src.ground_fill(ic, (10.5, 9.5, 117.5, 116.5)) if (src.ground is not None and col == src.ground_color
                                                             and src.ground_gradient) else None
    face = ic.rimmed_disc(inner=col, inner_gradient=grad)
    recolor = _on_plate_map(src, col)
    _raised(ic, _inside_circle(src, face["cx"], face["cy"], face["r"] * 0.80), recolor=recolor)
    return ic


def draft_symbol(src: Source, title="Free Symbol"):
    """D: the mark itself is the silhouette (no plate), every piece extruded 4 px."""
    ic = gk.Icon(title, source_note=_note(src))
    placed = src.place((12, 10, 116, 112), relative_to_ground=False)
    col = src.brand_color()
    remap = _inverted_map(src, col)
    if not remap:
        placed = _cutouts_to_holes(placed, src.ground_color)
    grad = _gradient_faces(ic, src, placed, {remap.get(f, f) for _, f, _ in placed.values()})
    with ic.group("mark"):
        for k, (d, fill, rule) in placed.items():
            c = remap.get(fill, fill)
            if c == "#ffffff":
                continue   # white inlays sit ON a coloured piece: no chin of their own
            x0, _, x1, _ = gk.bbox_d(d)
            ic.path(gk.translate_d(d, 0, 4), ic.chin_gradient(c, x0, x1, 6), f"mark-{k}-chin", fill_rule=rule)
        for k, (d, fill, rule) in placed.items():
            c = remap.get(fill, fill)
            if c == "#ffffff":
                ic.path(gk.translate_d(d, 0, 1.5), gk.lift_color(c), f"mark-{k}-lift", fill_rule=rule)
            ic.path(d, grad.get(c, c), f"mark-{k}-face", fill_rule=rule)
    return ic


def draft_light(src: Source, title="Light"):
    """F: paper plate, mark in brand colour (light marks become brand-coloured)."""
    ic = gk.Icon(title, source_note=_note(src))
    face = ic.plate("square", face=gk.NEUTRAL["paper"], r=20)
    col = src.brand_color()
    recolor = _inverted_map(src, col if not _is_light(col) else "#3d3846")
    if src.ground is not None:
        placed = src.place((face["x"], face["y"], face["x"] + face["w"], face["y"] + face["h"]))
    else:
        placed = src.place(ic.safe_box(face, 0.16), relative_to_ground=False)
    if not recolor:
        placed = _cutouts_to_holes(placed, src.ground_color)
    grad = _gradient_faces(ic, src, placed, {recolor.get(f, f) for _, f, _ in placed.values()})
    _raised(ic, placed, recolor=recolor, face_fill=grad)
    return ic


def _inside_circle(src: Source, cx, cy, r):
    """Fit the mark so its bounding box corners stay within radius r."""
    mx0, my0, mx1, my1 = src.mark_bbox
    w, h = mx1 - mx0, my1 - my0
    half_diag = math.hypot(w, h) / 2
    s = r / half_diag
    return src.place((cx - w * s / 2, cy - h * s / 2, cx + w * s / 2, cy + h * s / 2), relative_to_ground=False)


DRAFTS = {"faithful": draft_faithful, "disc": draft_disc, "rimmed": draft_rimmed,
          "symbol": draft_symbol, "light": draft_light}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: autodraft.py WORK_DIR")
    print(Source(sys.argv[1]).describe())
