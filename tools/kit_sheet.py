#!/usr/bin/env python3
"""Draw the carrier kit (work/_lib/carriers.py) with real logos -> docs/kit.png, and measure every
cell with the gate's own measures (logo size, contrast, how it sits, legibility at 32 px).

    python3 tools/kit_sheet.py                    # docs/kit.png with reddit / f_droid / chatgpt logos
    python3 tools/kit_sheet.py --logos a,b,c      # other apps' logos
    python3 tools/kit_sheet.py --check            # also print the measures (slow)

A model picks carriers by LOOKING at docs/kit.png (docs/METHOD.md §2): each row is one carrier,
the columns show it with a white logo, a coloured logo and a black logo.
"""
import importlib.util
import io
import sys
import tempfile
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "work/_lib"))
import carriers as C  # noqa: E402

BRAND = {"reddit": "#ff4500", "f_droid": "#1976d2", "chatgpt": "#10a37f", "duolingo": "#58cc02",
         "binance_tr": "#f0b90b", "payload_dumper": "#2c3e51", "scene": "#5191ef", "iconrequest": "#00c763"}


def call(fn, slug):
    ic = C.gk.Icon(f"{fn} {slug}")
    b = BRAND.get(slug, "#3584e4")
    f = getattr(C, fn)
    kw = {"logo_object": dict(brand=b), "sticker": dict(brand=b), "arrow": dict(brand=b), "flame": dict(),
          "bag": dict(brand=b), "envelope": dict(brand=b), "wallet": dict(), "chip": dict(lid=b), "phone": dict(brand=b),
          "shield": dict(brand=b), "bubble": dict(brand=b), "lens": dict(glass=b), "dial": dict(arc=b), "radar": dict(ring=b),
          "fan": dict(blades=b), "coin": dict(), "cup": dict(), "gauge": dict(), "monitor": dict(), "pouch": dict(brand=b),
          "book": dict(brand=b), "card": dict(brand=b)}.get(fn, {})
    f(ic, slug, **kw)
    return ic


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main(argv):
    logos = argv[argv.index("--logos") + 1].split(",") if "--logos" in argv else ["reddit", "f_droid", "chatgpt"]
    check = "--check" in argv
    out = ROOT / "docs/kit.png"
    S, LW, TW = 112, 250, 128
    rows = C.KIT
    W = LW + len(logos) * 2 * TW + 10
    H = 40 + len(rows) * (S + 14)
    sheet = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(sheet)
    d.text((10, 10), "Gnomed carrier kit - work/_lib/carriers.py (light and dark wallpaper; logos: " + ", ".join(logos) + ")",
           fill="#241f31", font=font(15))
    if check:
        spec = importlib.util.spec_from_file_location("ci", ROOT / "tools/check_icon.py")
        ci = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ci)
        leg = ci._legibility()
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        for r, (fn, what, style) in enumerate(rows):
            y = 40 + r * (S + 14)
            d.text((10, y + 8), fn, fill="#241f31", font=font(16))
            d.text((10, y + 32), style, fill="#c01c28", font=font(12))
            words, line, yy = what.split(), "", y + 52
            for wd in words:
                if len(line) + len(wd) > 30:
                    d.text((10, yy), line, fill="#5e5c64", font=font(11)); yy += 14; line = ""
                line += wd + " "
            d.text((10, yy), line, fill="#5e5c64", font=font(11))
            for k, slug in enumerate(logos):
                svg = Path(tmp) / f"{fn}-{slug}.svg"
                try:
                    call(fn, slug).save(svg)
                except Exception as e:  # noqa: BLE001
                    problems.append(f"{fn} {slug}: ERROR {e}")
                    continue
                for j, bg in enumerate(("#f6f5f4", "#241f31")):
                    x = LW + (k * 2 + j) * TW
                    d.rectangle([x, y, x + TW - 1, y + S + 13], fill=bg)
                    im = Image.open(io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=S, output_height=S))).convert("RGBA")
                    sheet.paste(im, (x + (TW - S) // 2, y + 6), im)
                if check:
                    side, con, shp, seen = ci.mark_layer_measure(slug, svg)
                    fit = ci.mark_fit_measure(svg)
                    ss = float(leg.cached_analyse(svg)["sizes"][32]["ssim"])
                    bad = []
                    need = 44 if style == "faithful" else 36
                    if side < need:
                        bad.append(f"logo {side:.0f}px")
                    if con < 25 or seen < 0.6:
                        bad.append(f"contrast {con:.0f} seen {seen:.0%}")
                    if fit and (fit["cross"] > 0.01 or fit["margin"] < 1.0 or fit["covered"] > 0.03):
                        bad.append(f"fit cross {fit['cross']:.0%} room {fit['margin']:.1f} covered {fit['covered']:.0%}")
                    if ss < 0.72:
                        bad.append(f"legibility {ss:.2f}")
                    if bad:
                        problems.append(f"{fn:12s} {slug:10s} " + "; ".join(bad))
    sheet.save(out)
    print(f"wrote {out.relative_to(ROOT)} ({len(rows)} carriers x {len(logos)} logos)")
    for p in problems:
        print("  " + p)
    if check:
        print(f"{len(problems)} cell(s) with problems")


if __name__ == "__main__":
    main(sys.argv[1:])
