#!/usr/bin/env python3
"""Review board: source vs. candidate icons vs. real GNOME references.

Sections
  1. Large: source (if given) and every candidate at 256 px, light + dark.
  2. Small sizes: each item at true 64 / 48 / 32 px (1:1) on light and dark,
     plus the 32 px raster magnified x3 (nearest) so pixel mush is visible.
  3. Family check: each candidate in a launcher-like row between real GNOME
     icons at 72 px, on a light and a dark wallpaper.

References: --refs FILE.svg ... or catalog filters --ref-kind / --ref-shape /
--ref-ids (comma lists).  Default: 6 refs matching the candidates' shapes.

Usage:
  preview_sheet.py --out work/review.png --source work/source.png \
      work/alt-a.svg work/alt-b.svg ... [--ref-kind emblem,disc-emblem] [--title "App"]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg, load_font, LIB_ROOT  # noqa: E402
from measure_style import measure  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

LIGHT, DARK = (246, 245, 244), (36, 31, 49)
WALL_L, WALL_D = ((222, 221, 218), (246, 245, 244)), ((61, 56, 70), (36, 31, 49))


def load(item, size):
    if item.lower().endswith(".svg"):
        return render_svg(item, size)
    im = Image.open(item).convert("RGBA")
    return im.resize((size, size), Image.LANCZOS)


def gradient(w, h, top, bottom):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return im


def pick_refs(a, cand_shapes):
    cat = json.loads((LIB_ROOT / "catalog.json").read_text())["icons"]
    if a.refs:
        return a.refs
    by_id = {e["id"]: e for e in cat}
    if a.ref_ids:
        # explicit ids: keep the user's order, allow every group (incl. adwaita-system)
        missing = [i for i in a.ref_ids.split(",") if i not in by_id]
        if missing:
            print("unknown reference ids (see ref_search.py):", ", ".join(missing), file=sys.stderr)
        return [str(LIB_ROOT / by_id[i]["file"]) for i in a.ref_ids.split(",") if i in by_id]
    sel = cat
    if a.ref_kind:
        ks = set(a.ref_kind.split(","))
        sel = [e for e in sel if e["kind"] in ks]
    if a.ref_shape:
        ss = set(a.ref_shape.split(","))
        sel = [e for e in sel if e["shape"] in ss]
    if not a.ref_kind and not a.ref_shape:
        sel = [e for e in cat if e["shape"] in cand_shapes]
    # automatic picks prefer app icons over Adwaita system icons
    sel = [e for e in sel if e["group"] != "adwaita-system"] or sel or cat
    step = max(1, len(sel) // a.n_refs)
    return [str(LIB_ROOT / e["file"]) for e in sel[::step][:a.n_refs]]


def checker(w, h, c1, c2, cell=12):
    im = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(im)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            if (x // cell + y // cell) % 2:
                d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=c2)
    return im


def shape_of(svg):
    m = measure(svg)
    if abs(m["w"] - m["h"]) < 6 and 0.74 < m["fill"] < 0.84 and m["w"] > 110:
        return "circle"
    if abs(m["w"] - m["h"]) < 6 and m["fill"] > 0.9:
        return "square"
    return "free"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("candidates", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--source")
    ap.add_argument("--title", default="")
    ap.add_argument("--refs", nargs="*")
    ap.add_argument("--ref-kind")
    ap.add_argument("--ref-shape")
    ap.add_argument("--ref-ids")
    ap.add_argument("--n-refs", type=int, default=6)
    a = ap.parse_args()

    cands = a.candidates
    shapes = {shape_of(c) for c in cands}
    refs = pick_refs(a, shapes)
    items = ([("source", a.source)] if a.source else []) + [(Path(c).stem, c) for c in cands]
    font, bfont, tfont = load_font(13), load_font(15), load_font(22)
    W = max(40 + len(items) * 276, 40 + (len(refs) + 1) * 84 * 2 + 60, 900)
    blocks = []

    # 1. large
    big = Image.new("RGB", (W, 2 * 276 + 40), (255, 255, 255))
    d = ImageDraw.Draw(big)
    d.text((20, 8), "1 · Source vs candidates (256 px)", fill=(20, 20, 20), font=bfont)
    for i, (lab, it) in enumerate(items):
        for j, bg in enumerate((LIGHT, DARK)):
            x, y = 20 + i * 276, 34 + j * 266
            if lab == "source" and j == 0:
                big.paste(checker(261, 261, (154, 153, 150), (119, 118, 123)), (x, y))
            else:
                d.rectangle([x, y, x + 260, y + 260], fill=bg)
            im = load(it, 256)
            big.paste(im, (x + 2, y + 2), im)
        d.text((20 + i * 276, 34 + 2 * 266 - 2), lab[:34], fill=(40, 40, 40), font=font)
    blocks.append(big)

    # 2. small sizes
    rowh = 150
    sm = Image.new("RGB", (W, 34 + rowh * len(items)), (255, 255, 255))
    d = ImageDraw.Draw(sm)
    d.text((20, 8), "2 · True small sizes 64 / 48 / 32 px (1:1) on light and dark + 32 px magnified x3", fill=(20, 20, 20), font=bfont)
    for i, (lab, it) in enumerate(items):
        y = 34 + i * rowh
        d.text((20, y + 60), lab[:22], fill=(40, 40, 40), font=font)
        x = 200
        for bg in ((154, 153, 150) if lab == "source" else LIGHT, DARK):
            d.rectangle([x - 6, y, x + 64 + 48 + 32 + 30, y + 70], fill=bg)
            xx = x
            for s in (64, 48, 32):
                im = load(it, s)
                sm.paste(im, (xx, y + 3 + (64 - s)), im)
                xx += s + 10
            x += 64 + 48 + 32 + 50
        for bg in ((154, 153, 150) if lab == "source" else LIGHT, DARK):
            im = load(it, 32).resize((96, 96), Image.NEAREST)
            tile = Image.new("RGB", (100, 100), bg)
            tile.paste(im, (2, 2), im)
            sm.paste(tile, (x, y))
            x += 110
    blocks.append(sm)

    # 3. family (every icon labelled, so the board explains itself)
    small = load_font(11)

    def short(path):
        stem = Path(path).stem
        return stem.split(".")[-1][:13] if "." in stem else stem[:13]
    fam_rows = []
    for lab, it in items:
        if lab == "source":
            continue
        row = Image.new("RGB", (W, 140), (255, 255, 255))
        half = (W - 60) // 2
        for k, (top, bot) in enumerate((WALL_L, WALL_D)):
            wall = gradient(half, 122, top, bot)
            wd = ImageDraw.Draw(wall)
            seq = refs[: len(refs) // 2] + [it] + refs[len(refs) // 2:]
            gap = (half - 20) // max(len(seq), 1)
            for j, r in enumerate(seq):
                im = load(r, 72)
                wall.paste(im, (10 + j * gap, 12), im)
                name = "> candidate" if r == it else short(r)
                col = ((30, 30, 30) if k == 0 else (240, 240, 240)) if r != it else ((200, 0, 30) if k == 0 else (255, 120, 120))
                wd.text((10 + j * gap, 92), name, fill=col, font=small)
            row.paste(wall, (20 + k * (half + 20), 14))
        ImageDraw.Draw(row).text((24, 0), lab[:40], fill=(90, 90, 90), font=font)
        fam_rows.append(row)
    fam = Image.new("RGB", (W, 34 + 140 * len(fam_rows)), (255, 255, 255))
    ImageDraw.Draw(fam).text((20, 8), "3 · Family fit: candidate between real GNOME icons (72 px, names under each icon)",
                             fill=(20, 20, 20), font=bfont)
    for i, r in enumerate(fam_rows):
        fam.paste(r, (0, 34 + i * 140))
    blocks.append(fam)

    head = Image.new("RGB", (W, 50 if a.title else 0), (255, 255, 255))
    if a.title:
        ImageDraw.Draw(head).text((20, 12), a.title, fill=(0, 0, 0), font=tfont)
    H = sum(b.height for b in blocks) + head.height
    out = Image.new("RGB", (W, H), (255, 255, 255))
    y = 0
    for b in [head] + blocks:
        out.paste(b, (0, y))
        y += b.height
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
