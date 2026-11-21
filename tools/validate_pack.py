#!/usr/bin/env python3
"""Check the icon pack files for mistakes that break icons on a phone (standard library only).

    python3 tools/validate_pack.py          # prints ERROR / WARN lines, exit 1 on any ERROR

What it checks (Faithful = app/src/main, the other styles = app/src/<style>):
  ERROR  appfilter.xml in assets/ and res/xml/ differ (launchers read one, CandyBar the other)
  ERROR  drawable.xml in assets/ and res/xml/ differ
  ERROR  a ComponentInfo that is not ComponentInfo{package/activity}
  ERROR  one ComponentInfo mapped to two different drawables in the same appfilter
  ERROR  an appfilter / drawable.xml / styles.json entry points to a PNG that does not exist
         (app icons only; launcher categories like :BROWSER are WARN, see below)
  ERROR  a drawable name that is not lowercase letters, digits and _ (Android resource rule)
  WARN   the CandyBar sample line ComponentInfo{some.app.sample/...} (no PNG; remove only with the owner's OK)
  WARN   the same ComponentInfo listed twice with the same drawable (harmless duplicate)
  WARN   a launcher category (:BROWSER, :CAMERA ...) without its PNG (CandyBar sample leftover)
  WARN   a pack PNG smaller than 192 px (blurry on xxxhdpi launchers)
  WARN   a pack PNG in drawable-nodpi that no appfilter, drawable.xml or styles.json uses

Runs in the PR guard workflow (.github/workflows/pr-guard.yml). Fix every ERROR before a PR.
"""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app/src"
NODPI = APP / "main/res/drawable-nodpi"
COMP_RE = re.compile(r"^ComponentInfo\{[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+\}$")
NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
ITEM_RE = re.compile(r'<item\s+component="([^"]*)"\s+drawable="([^"]*)"\s*/>')
DRAW_RE = re.compile(r'<item\s+drawable="([^"]*)"\s*/>')

errors, warns = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def png_size(p):
    with open(p, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def exists(name):
    return (NODPI / f"{name}.png").exists() or any((APP / "main/res").glob(f"drawable*/{name}.*"))


def check_appfilter(path, label):
    used = set()
    seen = {}
    text = path.read_text(encoding="utf-8")
    for comp, draw in ITEM_RE.findall(text):
        used.add(draw)
        if not NAME_RE.match(draw):
            err(f"{label}: drawable name '{draw}' is not lowercase a-z 0-9 _")
        if comp.startswith(":"):
            if not exists(draw):
                warn(f"{label}: launcher category {comp} -> '{draw}' has no PNG")
            continue
        if not COMP_RE.match(comp):
            err(f"{label}: malformed '{comp}' (must be ComponentInfo{{package/activity}})")
        if comp in seen:
            if seen[comp] != draw:
                err(f"{label}: {comp} -> '{seen[comp]}' AND '{draw}' (one app, two icons)")
            else:
                warn(f"{label}: {comp} listed twice")
        seen[comp] = draw
        if not exists(draw):
            if comp.startswith("ComponentInfo{some.app.sample/"):
                warn(f"{label}: CandyBar sample line {comp} -> '{draw}' (no PNG; harmless, remove only with the owner's OK)")
            else:
                err(f"{label}: {comp} -> '{draw}.png' does not exist in {NODPI.relative_to(ROOT)}")
    return used, len(seen)


def main():
    used = set()
    # 1. assets/ and res/xml/ copies must be identical, per style
    for style_dir in sorted(p for p in APP.iterdir() if p.is_dir()):
        for fname in ("appfilter.xml", "drawable.xml"):
            a, r = style_dir / "assets" / fname, style_dir / "res/xml" / fname
            if a.exists() and r.exists() and a.read_bytes() != r.read_bytes():
                err(f"{style_dir.name}: assets/{fname} and res/xml/{fname} differ - copy one over the other")
    # 2. appfilters
    counts = {}
    for style_dir in sorted(p for p in APP.iterdir() if p.is_dir()):
        af = style_dir / "res/xml/appfilter.xml"
        if af.exists():
            u, n = check_appfilter(af, f"{style_dir.name}/appfilter")
            used |= u
            counts[style_dir.name] = n
    # 3. drawable.xml (the icon list in the app)
    dx = APP / "main/res/xml/drawable.xml"
    if dx.exists():
        for d in DRAW_RE.findall(dx.read_text(encoding="utf-8")):
            used.add(d)
            if not exists(d):
                err(f"drawable.xml: '{d}' has no PNG")
    # 4. styles.json
    sj = ROOT / "pack/styles.json"
    if sj.exists():
        cfg = json.loads(sj.read_text(encoding="utf-8"))
        for prim, per in cfg.get("icons", {}).items():
            for style, d in per.items():
                used.add(d)
                if not exists(d):
                    err(f"styles.json: {prim} -> {style} '{d}' has no PNG")
    # 5. PNG sizes and unused PNGs (a PNG the app itself uses - clock, splash, drawer header - is used)
    src = "\n".join(f.read_text(encoding="utf-8", errors="ignore")
                     for f in APP.rglob("*") if f.suffix in (".xml", ".java", ".kt") and f.is_file())
    for p in sorted(NODPI.glob("*.png")):
        if not NAME_RE.match(p.stem):
            err(f"{p.name}: file name must be lowercase a-z 0-9 _")
        s = png_size(p)
        if s is None:
            err(f"{p.name}: not a PNG file")
        elif min(s) < 192:
            warn(f"{p.name}: {s[0]}x{s[1]} px - use at least 192 px")
        if p.stem not in used and not re.search(rf"[@/\"]{p.stem}\b|R\.drawable\.{p.stem}\b", src):
            warn(f"{p.name}: not used by any appfilter, drawable.xml or styles.json")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    apps = counts.get("main", 0)
    print(f"\nvalidate_pack: {apps} apps in the Faithful appfilter, {len(errors)} ERROR, {len(warns)} WARN")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
