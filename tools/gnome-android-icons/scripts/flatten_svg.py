#!/usr/bin/env python3
"""Flatten any SVG into "geometry" form: one absolute <path> per visible shape,
transforms applied, solid fills, fitted into the 128 x 128 icon space.

Why: official/brand/community SVGs come with nested groups, transforms, <use>,
rects/circles and gradients. gnome_kit works on plain path data, so this step
turns a real source vector into reusable identity geometry WITHOUT redrawing it.

  * every shape -> <path id="..." d="..." fill="#hex"> in paint order
  * transforms (incl. viewBox scaling) are baked into the coordinates
  * gradient fills -> the average of their stops (recorded in data-gradient="..."),
    because the GNOME rebuild decides shading anyway
  * strokes become filled outlines (shapely buffer of the centre line, with the
    stroke's cap/join) - reported, since curves are flattened to polylines
  * placement: by default the source viewBox is mapped onto 0..128 (official 128-px
    icons keep their exact coordinates); --box X0,Y0,X1,Y1 fits the content instead
  * <mask>/<clipPath>/<pattern>/<marker> contents and display:none layers are
    removed (they are not painted); masked elements are kept unclipped + reported

Usage:  flatten_svg.py in.svg --out work/app/source-geometry.svg [--box 4,4,124,124]
Requires: svgelements
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import svgelements as se
except ImportError:  # pragma: no cover
    sys.exit("pip install svgelements")


def _avg_hex(cols):
    rgb = [(int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)) for c in cols if re.match(r"^#[0-9a-fA-F]{6}$", c)]
    if not rgb:
        return None
    return "#%02x%02x%02x" % tuple(round(sum(v[i] for v in rgb) / len(rgb)) for i in range(3))


def _gradient_stops(raw_svg: str, gid: str, depth=0):
    m = re.search(r'<(?:\w+:)?(linearGradient|radialGradient)\b[^>]*\bid="' + re.escape(gid) + r'"[^>]*?(/>|>(.*?)</(?:\w+:)?\1>)',
                  raw_svg, re.S)
    if not m:
        return []
    body = m.group(3) or ""
    cols = []
    for st in re.finditer(r"<(?:\w+:)?stop\b([^>]*)/?>", body):
        a = st.group(1)
        c = re.search(r'stop-color\s*[:=]\s*"?\s*([^;"]+)', a)
        if c:
            try:
                h = se.Color(c.group(1).strip()).hex[:7]
            except Exception:
                continue
            cols.append(h.lower())
    if not cols and depth < 4:
        href = re.search(r'(?:xlink:)?href="#([^"]+)"', m.group(0))
        if href:
            return _gradient_stops(raw_svg, href.group(1), depth + 1)
    return cols


def _paint(el, raw, attr):
    """(hex or None, gradient-stops note) for fill/stroke of an element."""
    v = str(el.values.get(attr, "") or "")
    g = re.search(r"url\(#([^)]+)\)", v)
    if g:
        stops = _gradient_stops(raw, g.group(1))
        return (_avg_hex(stops) or "#888888"), " ".join(stops)
    obj = el.fill if attr == "fill" else el.stroke
    if obj is None or obj.value is None:
        return None, ""
    h = obj.hex
    return (h[:7] if h and len(h) == 9 else h), ""


def _stroke_outline(path, width, cap="butt", join="miter", samples=48):
    """Filled outline of a stroked path (shapely buffer of the flattened centre line)."""
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    caps = {"butt": "flat", "round": "round", "square": "square"}
    joins = {"miter": "mitre", "round": "round", "bevel": "bevel"}
    lines = []
    for sub in path.as_subpaths():
        pts = []
        for seg in sub:
            if isinstance(seg, se.Move):
                continue
            for k in range(samples + 1):
                z = seg.point(k / samples)
                pts.append((z[0], z[1]))
        if len(pts) >= 2:
            lines.append(LineString(pts).buffer(width / 2, cap_style=caps.get(cap, "flat"),
                                                join_style=joins.get(join, "mitre"), mitre_limit=4))
    if not lines:
        return None
    u = unary_union(lines).simplify(0.02)
    out = []
    for g in getattr(u, "geoms", [u]):
        if g.is_empty:
            continue
        out.append("M" + "L".join(f"{x:.3f} {y:.3f}" for x, y in list(g.exterior.coords)[:-1]) + "Z")
        for hole in g.interiors:
            out.append("M" + "L".join(f"{x:.3f} {y:.3f}" for x, y in list(hole.coords)[:-1]) + "Z")
    return "".join(out) or None


def _strip_non_painting(raw: str):
    """Remove <mask>, <clipPath>, <pattern>, <marker> content (their shapes are not
    painted) and Inkscape-hidden layers; returns (svg_text, notes)."""
    from lxml import etree
    root = etree.fromstring(raw.encode("utf-8"), etree.XMLParser(huge_tree=True, recover=True, remove_comments=True))
    notes = []
    for tag in ("mask", "clipPath", "pattern", "marker"):
        for el in root.iter("{http://www.w3.org/2000/svg}" + tag):
            el.getparent().remove(el)
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        st = el.get("style", "")
        if el.get("display") == "none" or re.search(r"display\s*:\s*none", st):
            el.getparent().remove(el) if el.getparent() is not None else None
            continue
        if el.get("mask") or el.get("clip-path"):
            notes.append(f"{el.get('id') or el.tag.split('}')[-1]}: mask/clip ignored - geometry kept unclipped")
    return etree.tostring(root, encoding="unicode"), notes


def flatten(src: str, box=None, min_area=0.5, strokes=True):
    """box=None keeps the source's own viewBox placement (scaled to 128) - right for
    official 128-px icons; pass a box (x0,y0,x1,y1) to fit the content instead."""
    import io
    raw0 = Path(src).read_text(encoding="utf-8", errors="replace")
    raw, warnings = _strip_non_painting(raw0)
    doc = se.SVG.parse(io.StringIO(raw), reify=True)
    vb = doc.viewbox
    shapes = []
    for el in doc.elements():
        if not isinstance(el, se.Shape):
            continue
        if el.values.get("visibility") == "hidden" or el.values.get("display") == "none":
            continue
        try:
            path = se.Path(el)
            path.reify()
            bb = path.bbox()
        except Exception:
            continue
        if bb is None:
            continue
        try:
            opacity = float(el.values.get("opacity", "1"))
        except ValueError:
            opacity = 1.0
        rule = "evenodd" if str(el.values.get("fill-rule", "")).lower() == "evenodd" else None
        fill, note = _paint(el, raw, "fill")
        try:
            fo = opacity * float(el.values.get("fill-opacity", "1"))
        except ValueError:
            fo = opacity
        x0, y0, x1, y1 = bb
        if fill and fill != "none" and fo >= 0.05 and (x1 - x0) * (y1 - y0) >= min_area * 1e-4:
            shapes.append(dict(id=el.id, d=path.d(), bbox=bb, fill=fill.lower(), grad=note, rule=rule, op=fo))
        stroke, snote = _paint(el, raw, "stroke")
        sw = getattr(el, "implicit_stroke_width", None) or float(el.values.get("stroke-width", 1) or 0)
        if stroke and stroke != "none" and sw > 0:
            if not strokes:
                warnings.append(f"{el.id}: stroke ignored (--no-strokes)")
                continue
            d = _stroke_outline(path, sw, str(el.values.get("stroke-linecap", "butt")), str(el.values.get("stroke-linejoin", "miter")))
            if d:
                try:
                    so = opacity * float(el.values.get("stroke-opacity", "1"))
                except ValueError:
                    so = opacity
                from svgelements import Path as _P
                sbb = _P(d).bbox()
                shapes.append(dict(id=(el.id or "shape") + "-stroke", d=d, bbox=sbb, fill=stroke.lower(), grad=snote,
                                   rule="nonzero", op=so))
                warnings.append(f"{el.id or type(el).__name__}: stroke converted to a filled outline (flattened curves)")
    if not shapes:
        raise SystemExit("no filled shapes found")
    if box is None and vb is not None and vb.width and vb.height:
        # keep native placement: map the viewBox square onto 0..128
        X0, Y0, X1, Y1 = 0, 0, max(doc.width, doc.height), max(doc.width, doc.height)
        box = (0, 0, 128, 128)
    else:
        box = box or (4, 4, 124, 124)
        X0 = min(s["bbox"][0] for s in shapes)
        Y0 = min(s["bbox"][1] for s in shapes)
        X1 = max(s["bbox"][2] for s in shapes)
        Y1 = max(s["bbox"][3] for s in shapes)
    bx0, by0, bx1, by1 = box
    sc = min((bx1 - bx0) / (X1 - X0), (by1 - by0) / (Y1 - Y0))
    ox = bx0 + ((bx1 - bx0) - (X1 - X0) * sc) / 2 - X0 * sc
    oy = by0 + ((by1 - by0) - (Y1 - Y0) * sc) / 2 - Y0 * sc
    out = []
    for i, s in enumerate(shapes):
        p = se.Path(s["d"]) * se.Matrix(f"translate({ox},{oy}) scale({sc})")
        p.reify()
        d = re.sub(r"-?\d+\.\d+(?:e-?\d+)?", lambda m: ("%.3f" % float(m.group(0))).rstrip("0").rstrip("."), p.d())
        sid = re.sub(r"[^A-Za-z0-9_-]", "_", s["id"] or f"shape{i:02d}")
        extra = f' data-gradient="{s["grad"]}"' if s["grad"] else ""
        rule = f' fill-rule="{s["rule"]}"' if s["rule"] and s["rule"] != "nonzero" else ""
        opa = f' opacity="{s["op"]:.2f}"' if s["op"] < 0.99 else ""
        out.append(f'  <path id="g{i:02d}-{sid}" fill="{s["fill"]}"{rule}{opa}{extra} d="{d}"/>')
    svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">\n'
           f'  <title>Flattened geometry of {Path(src).name} - reference, not final artwork</title>\n'
           + "\n".join(out) + "\n</svg>\n")
    return svg, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("--out", required=True)
    ap.add_argument("--box", help="fit content into X0,Y0,X1,Y1 (default: keep the source viewBox placement)")
    ap.add_argument("--no-strokes", action="store_true", help="drop strokes instead of outlining them")
    a = ap.parse_args()
    box = tuple(float(v) for v in a.box.split(",")) if a.box else None
    svg, warns = flatten(a.svg, box, strokes=not a.no_strokes)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(svg, encoding="utf-8")
    print(f"{a.out}: {svg.count('<path')} shapes")
    for w in warns:
        print("warning:", w)


if __name__ == "__main__":
    main()
