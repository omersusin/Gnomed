#!/usr/bin/env python3
"""Print the painting order of an SVG as a compact, readable layer list.

For every visible shape (in z-order, bottom first) prints:
  index, element, id, fill (solid hex or gradient stops), opacity,
  bounding box in viewBox units (transforms applied) and size.

Use it to *learn how a real GNOME icon is built* (chin under face, glyph lift,
side highlight gradients ...) without reading thousands of lines of Inkscape
XML, and to audit your own SVG before rendering.

Usage:  inspect_svg.py ICON.svg [--all]      (--all also lists invisible/defs)
Requires: svgelements (pip install svgelements)
"""
import argparse
import sys

try:
    import svgelements as se
except ImportError:  # pragma: no cover
    sys.exit("pip install svgelements")


def paint(p, svg_root):
    if p is None or p.value is None:
        return "none"
    try:
        return p.hex
    except Exception:
        return str(p)


def grad_desc(el, attr):
    """Describe url(#id) gradients by their stops."""
    raw = el.values.get(attr) if hasattr(el, "values") else None
    if raw and "url(" in str(raw):
        return str(raw)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    doc = se.SVG.parse(a.svg, reify=True)
    # index gradients
    grads = {}
    for el in doc.elements():
        tag = getattr(el, "values", {}).get("tag") if hasattr(el, "values") else None
    raw = open(a.svg, encoding="utf-8", errors="replace").read()
    import re
    from lxml import etree
    root = etree.fromstring(raw.encode(), etree.XMLParser(huge_tree=True, recover=True))
    ns = {"s": "http://www.w3.org/2000/svg", "x": "http://www.w3.org/1999/xlink"}

    def stops_of(gid, depth=0):
        g = root.find(f".//*[@id='{gid}']")
        if g is None or depth > 4:
            return []
        st = []
        for s in g:
            if not isinstance(s.tag, str) or not s.tag.endswith("stop"):
                continue
            style = s.get("style", "")
            col = s.get("stop-color") or (re.search(r"stop-color:\s*([^;]+)", style) or [None, None])[1]
            op = s.get("stop-opacity") or (re.search(r"stop-opacity:\s*([^;]+)", style) or [None, None])[1]
            st.append(f"{col}{'' if op in (None, '1') else '@' + str(op)}")
        if not st:
            href = g.get("{http://www.w3.org/1999/xlink}href") or g.get("href")
            if href:
                st = stops_of(href.lstrip("#"), depth + 1)
        kind = g.tag.split("}")[-1].replace("Gradient", "")
        return [kind] + st if st and not st[0] in ("linear", "radial") else st

    print(f"{'#':>3} {'element':8} {'id':18} {'fill':34} {'op':>4}  bbox(x0,y0,x1,y1)          w x h")
    i = 0
    for el in doc.elements():
        if not isinstance(el, se.Shape):
            continue
        vis = el.values.get("visibility") != "hidden" and el.values.get("display") != "none"
        if not vis and not a.all:
            continue
        fill_raw = el.values.get("fill") or ""
        m = re.search(r"url\(#([^)]+)\)", str(fill_raw))
        if m:
            fill = "grad[" + " > ".join(stops_of(m.group(1))) + "]"
        else:
            fill = paint(el.fill, doc)
        stroke_raw = el.values.get("stroke") or ""
        if stroke_raw and stroke_raw != "none":
            ms = re.search(r"url\(#([^)]+)\)", str(stroke_raw))
            sdesc = ("grad" if ms else str(el.stroke)) + f" w{el.values.get('stroke-width', '1')}"
            fill = (fill if fill != "none" else "") + f" stroke:{sdesc}"
        op = el.values.get("opacity", "1")
        fo = el.values.get("fill-opacity", "1")
        try:
            opv = float(op) * float(fo)
        except ValueError:
            opv = 1.0
        bb = el.bbox()
        if bb is None:
            continue
        x0, y0, x1, y1 = bb
        name = type(el).__name__.lower()[:8]
        eid = (el.id or "")[:18]
        print(f"{i:>3} {name:8} {eid:18} {fill[:34]:34} {opv:>4.2f}  ({x0:6.1f},{y0:6.1f},{x1:6.1f},{y1:6.1f})  {x1 - x0:5.1f} x {y1 - y0:5.1f}")
        i += 1


if __name__ == "__main__":
    main()
