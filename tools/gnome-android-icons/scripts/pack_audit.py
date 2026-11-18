#!/usr/bin/env python3
"""Audit a whole icon pack: XML integrity + visual family consistency.

XML (CandyBar-style project, --project):
  ERROR  appfilter drawable with no resource in res/drawable*/ (launcher shows nothing)
  ERROR  drawable.xml item with no resource (dashboard gap / crash on some versions)
  ERROR  one component mapped to two different drawables
  ERROR  malformed ComponentInfo / invalid resource names / unparsable XML
  WARN   res/xml and assets copies of appfilter.xml or drawable.xml differ
  WARN   resource in drawable-nodpi that no XML references (invisible orphan)
  INFO   gallery-only drawables (not in appfilter) - expected for *_altN alternatives

Visual (PNG/WebP in drawable-nodpi, or --icons DIR of SVG/PNG):
  size/format (RGBA, 192..512 px), opaque corners (a square background crept in),
  visual mass (painted canvas share) and box vs. the official GNOME distribution,
  bottom edge (chin baseline) outliers. Writes a family sheet with outliers framed red.

Usage:
  pack_audit.py --project ~/IconPack [--module app] [--sheet audit.png] [--json audit.json]
  pack_audit.py --icons work/exports --sheet audit.png
Exit code 1 when any ERROR is found.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import LIB_ROOT, render_svg, load_font  # noqa: E402
from measure_style import image_metrics, pixel_metrics  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
COMP_RE = re.compile(r"^(ComponentInfo\{[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+\}|:[A-Z_]+)$")
RES_EXT = (".png", ".webp", ".xml", ".jpg")


def official_band():
    cat = json.loads((LIB_ROOT / "catalog.json").read_text())["icons"]
    apps = [e["metrics"] for e in cat if e["group"] != "adwaita-system"]
    import numpy as np

    def band(k, lo=10, hi=90):
        v = [m[k] for m in apps if m.get(k) is not None]
        return float(np.percentile(v, lo)), float(np.percentile(v, hi))
    out = {k: band(k) for k in ("w", "h", "b")}
    out["area"] = band("area", 5, 95) if all("area" in m for m in apps) else (0.33, 0.72)
    return out


def parse_items(text, attr):
    return re.findall(r"<item\b([^>]*)/?>", text), attr


def audit_project(root: Path, module: str):
    issues = []  # (level, message)
    main = root / module / "src" / "main"
    res = main / "res"
    if not main.exists():
        sys.exit(f"{main} not found (use --module)")
    resources = {}
    for d in res.glob("drawable*"):
        for f in d.iterdir():
            if f.suffix.lower() in RES_EXT:
                resources.setdefault(f.stem, []).append(f)
    files = {k: [p for p in (main / "res/xml" / f"{k}.xml", main / "assets" / f"{k}.xml") if p.exists()]
             for k in ("appfilter", "drawable")}
    texts = {}
    for k, ps in files.items():
        for p in ps:
            t = p.read_text(encoding="utf-8")
            texts[p] = t
            try:
                from lxml import etree
                etree.fromstring(t.encode("utf-8"))
            except Exception as e:
                issues.append(("ERROR", f"{p.relative_to(root)}: XML does not parse: {e}"))
        if len(ps) == 2 and texts[ps[0]].strip() != texts[ps[1]].strip():
            issues.append(("WARN", f"{k}.xml: res/xml and assets copies differ (launchers read different ones)"))
        if not ps:
            issues.append(("WARN" if k == "drawable" else "ERROR", f"{k}.xml not found in res/xml or assets"))
    mapping = defaultdict(set)
    appfilter_drawables = set()
    if files["appfilter"]:
        t = texts[files["appfilter"][0]]
        for comp, dr in re.findall(r'<item\s+component="([^"]+)"\s+drawable="([^"]+)"', t):
            mapping[comp].add(dr)
            appfilter_drawables.add(dr)
            if not COMP_RE.match(comp):
                issues.append(("ERROR", f"appfilter: malformed component {comp}"))
            elif re.match(r"^ComponentInfo\{[^/]+/\.", comp):
                issues.append(("WARN", f"appfilter: relative activity in {comp} - write the full class name"))
        for comp, drs in mapping.items():
            if len(drs) > 1:
                issues.append(("ERROR", f"appfilter: {comp} mapped to several drawables {sorted(drs)}"))
        for tag in ("iconback", "iconmask", "iconupon", "scale"):
            m = re.search(rf"<{tag}\b[^>]*>", t)
            if m:
                issues.append(("INFO", f"appfilter fallback: {m.group(0)} (affects only unthemed apps)"))
    gallery, categories = [], []
    if files["drawable"]:
        t = texts[files["drawable"][0]]
        cur = "(none)"
        for m in re.finditer(r'<category\s+title="([^"]*)"\s*/>|<item\s+drawable="([^"]+)"(?:\s+name="([^"]*)")?', t):
            if m.group(1) is not None:
                cur = m.group(1)
                categories.append(cur)
            else:
                gallery.append((m.group(2), cur, m.group(3)))
    seen = set()
    for dr, cat, _ in gallery:
        if dr in seen:
            issues.append(("WARN", f"drawable.xml: '{dr}' listed more than once"))
        seen.add(dr)
        if dr not in resources:
            issues.append(("ERROR", f"drawable.xml: '{dr}' ({cat}) has no resource file"))
    for dr in sorted(appfilter_drawables):
        if not NAME_RE.match(dr):
            issues.append(("ERROR", f"appfilter: invalid resource name '{dr}'"))
        if dr not in resources:
            issues.append(("ERROR", f"appfilter: drawable '{dr}' has no resource file"))
    gallery_names = {g[0] for g in gallery}
    special = {"iconback", "iconmask", "iconupon", "clock_bg", "clock_hour", "clock_minute", "clock_second",
               "home_image", "ic_splash_screen", "ic_launcher"}
    nodpi = [p for p in (res / "drawable-nodpi").glob("*") if p.suffix.lower() in RES_EXT] if (res / "drawable-nodpi").exists() else []
    for p in nodpi:
        n = p.stem
        if n in special:
            continue
        if not NAME_RE.match(n):
            issues.append(("ERROR", f"invalid resource name: {p.name}"))
        if n not in gallery_names and n not in appfilter_drawables:
            issues.append(("WARN", f"orphan resource (in no XML): {p.name}"))
    gallery_only = sorted(g for g in gallery_names - appfilter_drawables if g in resources)
    alts = [g for g in gallery_only if re.search(r"_alt\d+$", g)]
    if gallery_only:
        issues.append(("INFO", f"{len(gallery_only)} gallery-only drawables ({len(alts)} are _altN alternatives): "
                               + ", ".join(gallery_only[:12]) + (" ..." if len(gallery_only) > 12 else "")))
    summary = dict(components=len(mapping), appfilter_drawables=len(appfilter_drawables), gallery=len(gallery),
                   categories=len(categories), resources=len(resources))
    icons = []
    order = [g[0] for g in gallery] + sorted(appfilter_drawables - gallery_names)
    for n in order:
        for f in resources.get(n, []):
            if f.suffix.lower() in (".png", ".webp") and n not in special:
                icons.append((n, f))
                break
    return issues, summary, icons


def visual_audit(icons, band):
    issues, rows = [], []
    for name, f in icons:
        try:
            if f.suffix.lower() == ".svg":
                m = pixel_metrics(f)
                size = None
            else:
                im = Image.open(f)
                size = im.size
                if im.mode not in ("RGBA", "LA", "P"):
                    issues.append(("WARN", f"{f.name}: no alpha channel ({im.mode}) - square background will show"))
                if size[0] != size[1]:
                    issues.append(("ERROR", f"{f.name}: not square {size}"))
                elif size[0] < 192:
                    issues.append(("WARN", f"{f.name}: {size[0]} px - blurry on xxhdpi launchers (CandyBar: 256)"))
                elif size[0] > 512:
                    issues.append(("INFO", f"{f.name}: {size[0]} px - larger than needed, increases APK size"))
                m = image_metrics(im)
        except Exception as e:
            issues.append(("ERROR", f"{f.name}: cannot read ({e})"))
            continue
        flags = []
        if not m:
            issues.append(("ERROR", f"{f.name}: fully transparent"))
            continue
        if m.get("opaque_corners", 0) >= 3:
            flags.append("opaque corners (full square background)")
        lo, hi = band["area"]
        if m["area"] < lo * 0.9:
            flags.append(f"light visual mass {m['area']:.2f} (official {lo:.2f}-{hi:.2f})")
        elif m["area"] > hi * 1.08:
            flags.append(f"heavy visual mass {m['area']:.2f} (official {lo:.2f}-{hi:.2f})")
        if max(m["w"], m["h"]) > 125:
            flags.append(f"touches the canvas edge ({m['w']:.0f}x{m['h']:.0f})")
        if max(m["w"], m["h"]) < 84:
            flags.append(f"small box {m['w']:.0f}x{m['h']:.0f} (template shapes are 104-120)")
        if m["b"] < 110 or m["b"] > 127:
            flags.append(f"bottom edge y={m['b']:.0f} (official 116-126)")
        for fl in flags:
            issues.append(("WARN", f"{f.name}: {fl}"))
        rows.append(dict(name=name, file=str(f), size=size, flags=flags, **{k: m[k] for k in ("w", "h", "b", "area", "chin")}))
    return issues, rows


def family_sheet(rows, out, cols=10, s=96):
    font = load_font(11)
    pad = 16
    cw, ch = s + pad * 2, s + pad * 2 + 26
    n = len(rows)
    sheet = Image.new("RGB", (cw * cols, ch * ((n + cols - 1) // cols) + 40), (246, 245, 244))
    d = ImageDraw.Draw(sheet)
    d.text((10, 12), f"Pack family check - {n} icons (red frame = outlier, see report)", fill=(20, 20, 20), font=load_font(16))
    for i, r in enumerate(rows):
        x, y = (i % cols) * cw, 40 + (i // cols) * ch
        f = Path(r["file"])
        im = render_svg(f, s) if f.suffix.lower() == ".svg" else Image.open(f).convert("RGBA").resize((s, s), Image.LANCZOS)
        if r["flags"]:
            d.rectangle([x + 4, y + 4, x + cw - 4, y + s + pad * 2 - 4], outline=(224, 27, 36), width=3)
        sheet.paste(im, (x + pad, y + pad), im)
        d.text((x + 6, y + s + pad * 2 - 2), r["name"][:16], fill=(60, 60, 60), font=font)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--module", default="app")
    ap.add_argument("--icons", help="folder of SVG/PNG icons (no XML checks)")
    ap.add_argument("--sheet")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not a.project and not a.icons:
        ap.error("--project or --icons")
    band = official_band()
    issues, summary, icons = [], {}, []
    if a.project:
        issues, summary, icons = audit_project(Path(a.project), a.module)
    if a.icons:
        icons += [(p.stem, p) for p in sorted(Path(a.icons).glob("*")) if p.suffix.lower() in (".svg", ".png", ".webp")]
    vis_issues, rows = visual_audit(icons, band)
    issues += vis_issues
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    issues.sort(key=lambda t: order[t[0]])
    if summary:
        print("project:", ", ".join(f"{k} {v}" for k, v in summary.items()))
    print(f"icons measured: {len(rows)} | official visual-mass band (p5-p95): {band['area'][0]:.2f}-{band['area'][1]:.2f}")
    for lvl, msg in issues:
        print(f"[{lvl}] {msg}")
    n_err = sum(1 for lvl, _ in issues if lvl == "ERROR")
    print(f"\n{n_err} errors, {sum(1 for lvl, _ in issues if lvl == 'WARN')} warnings")
    if a.sheet and rows:
        family_sheet(rows, a.sheet)
        print(a.sheet)
    if a.json:
        Path(a.json).write_text(json.dumps(dict(summary=summary, issues=issues, icons=rows), indent=1, default=float))
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
