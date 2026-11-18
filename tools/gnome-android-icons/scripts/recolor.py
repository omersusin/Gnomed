#!/usr/bin/env python3
"""Colour sweep: the same finished SVG in every GNOME HIG colour family.

For monochrome or white-only marks (the source has no colour of its own), or
when the user wants to pick the pack colour of an app: every colour of the
SVG whose hue is close to the KEY colour (and all its derived shades: chin,
highlights, gradients) is moved to each target family, keeping the relative
lightness/chroma steps - so face, chin and highlight stay a coherent set.
Neutrals (white, greys) and colours of other hues are left untouched.

Usage:
  recolor.py work/app/app-disc.svg --out-dir work/app/colours [--key '#813d9c']
             [--families blue,green,yellow,orange,red,purple,brown] [--sheet work/app/colours.png]
Default key: the most saturated colour that covers the most of the icon.
"""
import argparse
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import HIG_PALETTE, hex_to_oklab, oklab_to_hex, render_svg  # noqa: E402

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def lch(h):
    L, a, b = hex_to_oklab(h)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def from_lch(L, C, H):
    t = math.radians(H)
    return oklab_to_hex(max(0.0, min(1.0, L)), C * math.cos(t), C * math.sin(t))


def norm(h):
    h = h.lower()
    return "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h


def auto_key(svg_path):
    import numpy as np
    im = np.asarray(render_svg(svg_path, 128)).astype(float)
    px = im[im[..., 3] > 200][:, :3]
    best, score = None, 0
    txt = Path(svg_path).read_text()
    for h in {norm(m.group(0)) for m in HEX.finditer(txt)}:
        L, C, _ = lch(h)
        if C < 0.05:
            continue
        rgb = np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
        cover = (np.sqrt(((px - rgb) ** 2).sum(-1)) < 40).mean() if len(px) else 0
        if cover * C > score:
            best, score = h, cover * C
    return best


def sweep(svg_text, key, target, window=35.0):
    Lk, Ck, Hk = lch(key)
    Lt, Ct, Ht = lch(target)

    def repl(m):
        h = norm(m.group(0))
        L, C, H = lch(h)
        dh = (H - Hk + 180) % 360 - 180
        if C < 0.03 or abs(dh) > window:
            return m.group(0)
        return from_lch(L + (Lt - Lk), min(0.37, C * (Ct / max(Ck, 1e-6))), Ht + dh)
    return HEX.sub(repl, svg_text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--key")
    ap.add_argument("--families", default="blue,green,yellow,orange,red,purple,brown")
    ap.add_argument("--sheet")
    ap.add_argument("--window", type=float, default=35.0, help="hue window (degrees) around the key colour")
    a = ap.parse_args()
    key = norm(a.key) if a.key else auto_key(a.svg)
    if not key:
        sys.exit("no saturated colour found - pass --key '#hex'")
    txt = Path(a.svg).read_text(encoding="utf-8")
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for fam in a.families.split(","):
        target = HIG_PALETTE[fam][2]          # the family's "3" swatch
        if fam == "yellow":
            target = HIG_PALETTE[fam][3]      # yellow3 is too light to carry white marks
        p = out / f"{Path(a.svg).stem}-{fam}.svg"
        p.write_text(sweep(txt, key, target, a.window), encoding="utf-8")
        files.append(str(p))
        print(p)
    print(f"key colour: {key}")
    if a.sheet:
        import subprocess
        subprocess.run([sys.executable, str(Path(__file__).with_name("contact_sheet.py")), a.sheet, a.svg, *files,
                        "--size", "128", "--cols", str(len(files) + 1), "--bg", "both",
                        "--title", f"Colour sweep of {Path(a.svg).name} (key {key})"], check=True)


if __name__ == "__main__":
    main()
