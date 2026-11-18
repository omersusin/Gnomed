#!/usr/bin/env python3
"""Get an app's REAL launcher icon geometry from its APK (source-first, no tracing).

Most modern apps ship their launcher icon as an adaptive icon whose foreground
(and often background / monochrome) layers are VectorDrawable XML - i.e. exact
vector paths drawn by the app's own designers.  This tool:

  1. finds the launcher icon resource in the APK (androguard),
  2. if it is an <adaptive-icon>, resolves background / foreground / monochrome,
  3. converts every VectorDrawable layer to SVG (paths, groups+transforms,
     clip-paths, solid + linear/radial gradient fills, fillType, alpha),
  4. writes  <out>/layers/*.svg , <out>/adaptive-full.svg (108-unit canvas,
     what launchers mask) and <out>/adaptive-visible.svg (inner 72 units),
     or the highest-density PNG/WebP when the icon is a bitmap.

Use the result as SOURCE GEOMETRY for the identity anchors.  The brand's
artwork stays the brand's: it is reference, not a licence to redistribute.

Usage:
  apk_icon.py --apk base.apk --out work/apk-icon       # get APK: find_component.py --pull PKG
  apk_icon.py --vector res/drawable/ic_launcher_foreground.xml --out work/fg.svg  # already-decoded XML
Requires: androguard (pip install androguard) for --apk.  --vector needs only lxml.
Status: the VectorDrawable converter is unit-tested; APK resolution was verified on
real APKs (adaptive icons with vector background/foreground/monochrome layers,
compiled gradient drawables, and bitmap-only launchers). Obfuscated or unusual
resource tables can still fail - the script then says what it could not resolve.
"""
import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

from lxml import etree

A = "{http://schemas.android.com/apk/res/android}"
AAPT = "{http://schemas.android.com/aapt}"


def color(v):
    """#RGB/#ARGB/#RRGGBB/#AARRGGBB -> (hex, opacity)."""
    if v is None:
        return None, 1.0
    v = v.strip()
    if not v.startswith("#"):
        return None, 1.0  # resource refs (@color/..) must be resolved by caller
    h = v[1:]
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) == 8:
        return "#" + h[2:], int(h[:2], 16) / 255
    return "#" + h[:6], 1.0


def num(el, name, default=0.0):
    v = el.get(A + name)
    try:
        return float(v.replace("dip", "").replace("dp", "")) if v is not None else default
    except ValueError:
        return default


class VD2SVG:
    def __init__(self, resolver=None, loader=None):
        self.defs, self.n = [], 0
        self.resolver = resolver or (lambda ref: None)
        self.loader = loader          # path -> decoded XML bytes (APK resources), optional

    def nid(self, p):
        self.n += 1
        return f"{p}{self.n}"

    def gradient(self, g):
        gid = self.nid("vdg")
        typ = g.get(A + "type", "linear")
        stops = []
        items = g.findall("item")
        if items:
            for it in items:
                c, o = color(it.get(A + "color"))
                stops.append((num(it, "offset"), c, o))
        else:
            for k, off in (("startColor", 0), ("centerColor", 0.5), ("endColor", 1)):
                if g.get(A + k):
                    c, o = color(g.get(A + k))
                    stops.append((off, c, o))
        st = "".join(f'<stop offset="{o:g}" stop-color="{c}"' + (f' stop-opacity="{op:.3f}"' if op < 1 else "") + "/>"
                     for o, c, op in stops if c)
        if typ == "radial":
            self.defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{num(g, "centerX"):g}" '
                             f'cy="{num(g, "centerY"):g}" r="{num(g, "gradientRadius"):g}">{st}</radialGradient>')
        else:
            self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{num(g, "startX"):g}" '
                             f'y1="{num(g, "startY"):g}" x2="{num(g, "endX"):g}" y2="{num(g, "endY"):g}">{st}</linearGradient>')
        return f"url(#{gid})"

    def paint(self, el, attr):
        for at in el.findall(AAPT + "attr"):
            if at.get("name") == "android:" + attr:
                g = at.find("gradient")
                if g is not None:
                    return self.gradient(g), 1.0
        v = el.get(A + attr)
        if v and v.startswith("@"):
            target = self.resolver(v)
            # compiled APKs move inline <aapt:attr> gradients into their own drawable XML
            if target and not target.startswith("#") and target.endswith(".xml") and self.loader:
                try:
                    root = etree.fromstring(self.loader(target))
                    if root.tag == "gradient":
                        return self.gradient(root), 1.0
                    if root.tag == "selector" and len(root):
                        v = root[0].get(A + "color")
                except Exception:
                    pass
            else:
                v = target
            v = v or "#000000"
        return color(v)

    def node(self, el, out, ind="  "):
        tag = el.tag
        if tag == "group":
            px, py = num(el, "pivotX"), num(el, "pivotY")
            tr = []
            tx, ty = num(el, "translateX"), num(el, "translateY")
            if tx or ty:
                tr.append(f"translate({tx:g} {ty:g})")
            rot = num(el, "rotation")
            sx, sy = num(el, "scaleX", 1), num(el, "scaleY", 1)
            if rot or sx != 1 or sy != 1:
                tr.append(f"translate({px:g} {py:g})")
                if rot:
                    tr.append(f"rotate({rot:g})")
                if sx != 1 or sy != 1:
                    tr.append(f"scale({sx:g} {sy:g})")
                tr.append(f"translate({-px:g} {-py:g})")
            name = el.get(A + "name")
            out.append(f'{ind}<g' + (f' id={quoteattr(name)}' if name else "") + (f' transform="{" ".join(tr)}"' if tr else "") + ">")
            # Android semantics: a <clip-path> clips the siblings that FOLLOW it
            opened = 0
            for ch in el:
                if ch.tag == "clip-path":
                    clip = self.nid("vdc")
                    self.defs.append(f'<clipPath id="{clip}"><path d="{ch.get(A + "pathData")}"/></clipPath>')
                    out.append(f'{ind} <g clip-path="url(#{clip})">')
                    opened += 1
                else:
                    self.node(ch, out, ind + "  ")
            for _ in range(opened):
                out.append(f"{ind} </g>")
            out.append(f"{ind}</g>")
        elif tag == "path":
            d = el.get(A + "pathData", "")
            fill, fo = self.paint(el, "fillColor")
            stroke, so = self.paint(el, "strokeColor")
            fa = num(el, "fillAlpha", 1) * fo
            sa = num(el, "strokeAlpha", 1) * so
            attrs = [f'd="{d}"', f'fill="{fill or "none"}"']
            if fill and fa < 1:
                attrs.append(f'fill-opacity="{fa:.3f}"')
            if el.get(A + "fillType", "").lower() == "evenodd":
                attrs.append('fill-rule="evenodd"')
            if stroke:
                attrs += [f'stroke="{stroke}"', f'stroke-width="{num(el, "strokeWidth", 0):g}"']
                if sa < 1:
                    attrs.append(f'stroke-opacity="{sa:.3f}"')
                cap, join = el.get(A + "strokeLineCap"), el.get(A + "strokeLineJoin")
                if cap:
                    attrs.append(f'stroke-linecap="{cap}"')
                if join:
                    attrs.append(f'stroke-linejoin="{join}"')
            name = el.get(A + "name")
            if name:
                attrs.insert(0, f"id={quoteattr(name)}")
            out.append(f"{ind}<path {' '.join(attrs)}/>")

    def convert(self, root):
        if root.tag != "vector":
            raise ValueError(f"not a <vector> drawable: <{root.tag}>")
        vw, vh = num(root, "viewportWidth", 24), num(root, "viewportHeight", 24)
        body = []
        for ch in root:
            self.node(ch, body)
        alpha = num(root, "alpha", 1)
        defs = f"  <defs>{''.join(self.defs)}</defs>\n" if self.defs else ""
        op = f' opacity="{alpha:.3f}"' if alpha < 1 else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:g} {vh:g}" width="{vw:g}" height="{vh:g}"{op}>\n'
                + defs + "\n".join(body) + "\n</svg>\n")


def vector_to_svg(xml_bytes, resolver=None, loader=None):
    root = etree.fromstring(xml_bytes)
    return VD2SVG(resolver, loader).convert(root)


def compose_adaptive(layers: dict, out_dir: Path):
    """Stack background + foreground SVG layers in the 108-unit adaptive canvas."""
    parts = []
    for key in ("background", "foreground"):
        L = layers.get(key)
        if L is None:
            continue
        if L.startswith("#"):
            parts.append(f'<rect width="108" height="108" fill="{L}"/>')
        else:
            inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", L, flags=re.S)
            vb = re.search(r'viewBox="([^"]+)"', L).group(1).split()
            sx, sy = 108 / float(vb[2]), 108 / float(vb[3])
            parts.append(f'<g id="{key}" transform="scale({sx:g} {sy:g})">{inner}</g>')
    full = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" width="108" height="108">' + "".join(parts) + "</svg>\n"
    (out_dir / "adaptive-full.svg").write_text(full)
    vis = full.replace('viewBox="0 0 108 108" width="108" height="108"', 'viewBox="18 18 72 72" width="72" height="72"')
    (out_dir / "adaptive-visible.svg").write_text(vis)


def from_apk(apk_path, out_dir: Path):
    try:
        from androguard.core.apk import APK
        from androguard.core.axml import AXMLPrinter
    except ImportError:
        sys.exit("pip install androguard")
    try:  # androguard 4 logs every chunk at DEBUG level through loguru
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level="WARNING")
    except Exception:
        pass
    apk = APK(apk_path)
    res = apk.get_android_resources()
    icon = apk.get_app_icon()
    print("package:", apk.get_package(), "| icon resource:", icon)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "layers").mkdir(exist_ok=True)

    def resolve(ref):
        """@7f0801a2 / @color/x -> file path or colour value (best effort)."""
        try:
            rid = int(ref[1:], 16) if re.match(r"^@[0-9a-fA-F]{8}$", ref) else None
            if rid is None:
                return None
            cfgs = res.get_resolved_res_configs(rid)
            best = sorted(cfgs, key=lambda c: -(c[0].get_density() if hasattr(c[0], "get_density") else 0))
            return best[0][1] if best else None
        except Exception:
            return None

    def load_xml(path):
        return AXMLPrinter(apk.get_file(path)).get_xml()

    if icon.endswith((".png", ".webp", ".jpg")):
        p = out_dir / ("launcher" + Path(icon).suffix)
        p.write_bytes(apk.get_file(icon))
        print("bitmap icon only ->", p, "(use extract_icon.py / trace_source.py on it)")
        return
    root = etree.fromstring(load_xml(icon))
    layers = {}
    if root.tag == "adaptive-icon":
        for key in ("background", "foreground", "monochrome"):
            el = root.find(key)
            if el is None:
                continue
            ref = el.get(A + "drawable")
            target = resolve(ref) if ref else None
            if target and target.startswith("#"):
                layers[key] = color(target)[0]
            elif target and target.endswith(".xml"):
                try:
                    svg = vector_to_svg(load_xml(target), resolve, load_xml)
                    layers[key] = svg
                    (out_dir / "layers" / f"{key}.svg").write_text(svg)
                except ValueError as e:
                    print(f"{key}: {target} is not a plain vector ({e}); inspect it manually")
            elif target:
                (out_dir / "layers" / f"{key}{Path(target).suffix}").write_bytes(apk.get_file(target))
                print(f"{key}: bitmap layer {target}")
            else:
                print(f"{key}: could not resolve {ref}")
        compose_adaptive(layers, out_dir)
        print("wrote", out_dir / "adaptive-full.svg", "and adaptive-visible.svg")
    elif root.tag == "vector":
        (out_dir / "layers" / "icon.svg").write_text(vector_to_svg(load_xml(icon), resolve, load_xml))
        print("wrote", out_dir / "layers" / "icon.svg")
    else:
        print(f"unsupported root <{root.tag}>; decoded XML saved for manual inspection")
        (out_dir / "icon-decoded.xml").write_bytes(load_xml(icon))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--apk")
    g.add_argument("--vector", help="decoded VectorDrawable XML file")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.apk:
        from_apk(a.apk, Path(a.out))
    else:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(vector_to_svg(Path(a.vector).read_bytes()))
        print(a.out)


if __name__ == "__main__":
    main()
