#!/usr/bin/env python3
"""Export transparent PNGs from an icon SVG (code rasterisation only).

Default sizes: 512 and 256 (CandyBar recommends 256x256 in drawable-nodpi).
Also verifies: RGBA mode, transparent corners, exact size.

Usage: export_png.py ICON.svg [ICON2.svg ...] --out-dir exports [--name drawable_name] [--sizes 512,256,192,128]
       (several SVGs in one call: one Python start instead of one per file; --name needs exactly one SVG)
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="+")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--name")
    ap.add_argument("--sizes", default="512,256")
    a = ap.parse_args()
    if a.name and len(a.svgs) != 1:
        ap.error("--name needs exactly one SVG")
    for svg in a.svgs:
        export(svg, a.name or Path(svg).stem, Path(a.out_dir), a.sizes)


def export(svg, name, out, sizes):
    out.mkdir(parents=True, exist_ok=True)
    for s in [int(x) for x in sizes.split(",")]:
        im = render_svg(svg, s)
        px = im.load()
        corners = [px[0, 0][3], px[s - 1, 0][3], px[0, s - 1][3], px[s - 1, s - 1][3]]
        assert im.mode == "RGBA" and im.size == (s, s), "unexpected raster format"
        if max(corners) > 0:
            print(f"warning: {s}px corners not transparent {corners}", file=sys.stderr)
        p = out / f"{name}-{s}.png"
        im.save(p, optimize=True)
        print(p)


if __name__ == "__main__":
    main()
