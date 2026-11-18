#!/usr/bin/env python3
"""Automatic quality gate for one app - usable WITHOUT looking at images.

    python3 tools/check_icon.py <slug>          # human-readable report
    python3 tools/check_icon.py <slug> --json   # machine-readable

Every check prints PASS / WARN / FAIL, a number, and - when it is not PASS - the
FIX to apply (a key from docs/course/04-recipes.md). Exit code: 0 = no FAIL,
1 = at least one FAIL. A model that cannot see images MUST still run this and fix
every FAIL; a model that can see images must ALSO look at work/<slug>/styles.png.

Checks (per style that exists):
  lint          lint_svg.py result (raster/text/filters/edge contact) ......... FAIL
  visible       plated styles: must read on at least one of light #f6f5f4 / dark #241f31 .. FAIL < 0.55
  visible_light Symbol only: must read on a light wallpaper ...... WARN < 0.55, FAIL < 0.25
  visible_dark  Symbol only: must read on a dark wallpaper ....... WARN < 0.55, FAIL < 0.25
  mass          painted share of the canvas (official GNOME 0.44-0.69) ........ WARN
  baseline      bottom edge: plates 114-118, discs 120-126, symbols 108-124 ... WARN
  legibility32  structure kept at 32 px (official median SSIM 0.82) ........... WARN < 0.72, FAIL < 0.62
  box_in_plate  Faithful: one region covering most of the plate (a tile/disc
                drawn inside the plate) ........................................ FAIL
Per app (from geometry.json):
  stripes       3+ regions of near-identical hue = one gradient cut into bands . WARN -> merge_grad
  trace_iou     traced parts match their masks: WARN < 0.90; FAIL if a part >= 3 % of the canvas < 0.75
  faithful      a Faithful SVG must exist (every other style falls back to it)  FAIL
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / "tools/gnome-android-icons/scripts"
sys.path.insert(0, str(SK))
from skimage.color import rgb2lab  # noqa: E402

LIGHT, DARK = (0xf6, 0xf5, 0xf4), (0x24, 0x1f, 0x31)
STYLES = ("faithful", "disc", "rimmed", "symbol")


def render(svg, size=256):
    im = Image.open(io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=size, output_height=size))).convert("RGBA")
    return np.asarray(im).astype(np.float32) / 255.0


def visible(a, bg):
    """share of the icon's painted pixels that differ clearly (dE > 10) from the wallpaper"""
    al = a[..., 3]
    painted = al > 0.5
    if painted.sum() == 0:
        return 0.0
    bgc = np.array(bg, np.float32) / 255
    comp = a[..., :3] * al[..., None] + bgc * (1 - al[..., None])
    d = np.linalg.norm(rgb2lab(comp) - rgb2lab(bgc[None, None, :]), axis=-1)
    return float(((d > 10) & painted).sum() / painted.sum())


def mass_and_bottom(a):
    al = a[..., 3] > 0.5
    ys = np.nonzero(al.any(1))[0]
    return float(al.mean()), (float(ys.max() + 1) * 128 / a.shape[0]) if len(ys) else 0.0


def hue(h):
    import colorsys
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss, ll


def main():
    slug = sys.argv[1]
    as_json = "--json" in sys.argv
    w = ROOT / "work" / slug
    res = []

    def add(scope, check, status, value, fix=""):
        res.append({"scope": scope, "check": check, "status": status, "value": value, "fix": fix})

    svgs = {st: w / f"{slug}-{st}.svg" for st in STYLES if (w / f"{slug}-{st}.svg").exists()}
    add("app", "faithful", "PASS" if "faithful" in svgs else "FAIL", "faithful" in svgs,
        "" if "faithful" in svgs else "build the app first: python3 tools/make_icon.py " + slug)
    for st, svg in svgs.items():
        out = subprocess.run([sys.executable, str(SK / "lint_svg.py"), str(svg)], capture_output=True, text=True).stdout
        fail = "[FAIL]" in out
        add(st, "lint", "FAIL" if fail else "PASS", "FAIL" if fail else "ok",
            "read the lint message; edge contact -> smaller scale (recipe R10)" if fail else "")
        a = render(svg)
        vl, vd = visible(a, LIGHT), visible(a, DARK)
        if st == "symbol":
            # no plate: the object itself must read on BOTH wallpapers
            for name, v, rec in (("visible_light", vl, "R6: symbol mode margin, or skip the symbol"),
                                 ("visible_dark", vd, "R6: symbol mode margin / light edge, or skip the symbol")):
                stt = "PASS" if v >= 0.55 else ("WARN" if v >= 0.25 else "FAIL")
                add(st, name, stt, round(v, 2), "" if stt == "PASS" else rec)
        else:
            # a light plate on a light wallpaper (or dark on dark) is fine in GNOME - its chin and
            # edge separate it; it must read clearly on at least ONE of the two
            v = max(vl, vd)
            stt = "PASS" if v >= 0.55 else "FAIL"
            add(st, "visible", stt, f"light {vl:.2f} / dark {vd:.2f}", "" if stt == "PASS" else "R6: plate colour too close to both wallpapers / mark too faint")
        m, bottom = mass_and_bottom(a)
        lo, hi = (0.20, 0.75) if st == "symbol" else (0.40, 0.75)
        add(st, "mass", "PASS" if lo <= m <= hi else "WARN", round(m, 2), "" if lo <= m <= hi else "R10 scale")
        blo, bhi = {"faithful": (114, 118.5), "disc": (120, 126.5), "rimmed": (120, 126.5), "symbol": (108, 124.5)}[st]
        add(st, "baseline", "PASS" if blo <= bottom <= bhi else "WARN", round(bottom, 1), "" if blo <= bottom <= bhi else "R9 baseline")
        leg = subprocess.run([sys.executable, str(SK / "legibility_check.py"), str(svg)], capture_output=True, text=True).stdout
        ssim = None
        for line in leg.splitlines():
            if "32px" in line and "ssim" in line:
                try:
                    ssim = float(line.split("ssim")[1].split()[0])
                except ValueError:
                    pass
        if ssim is not None:
            stt = "PASS" if ssim >= 0.72 else ("WARN" if ssim >= 0.62 else "FAIL")
            add(st, "legibility32", stt, ssim, "" if stt == "PASS" else "R11 (bigger mark, drop tiny details, thicker strokes)")
    # box inside the plate: a big single region whose colour differs from the plate
    gp = w / "geometry.json"
    if gp.exists():
        g = json.loads(gp.read_text())
        regs = g["info"].get("regions", [])
        if "faithful" in svgs and regs:
            biggest = max(r["area"] for r in regs)
            bb = g["info"].get("mark_bbox") or [0, 0, 0, 0]
            span = min(bb[2] - bb[0], bb[3] - bb[1]) / 128
            src = open(svgs["faithful"]).read()
            dropped = '"drop"' in src  # not reliable; real check below
            stt = "FAIL" if (biggest > 0.40 and span > 0.70) else "PASS"
            # an override that turned the region into the plate colour clears it
            ov = (ROOT / "work/_lib/build_auto.py").read_text()
            hand = (ROOT / "work/_lib/build_weak.py").read_text()
            if f'"{slug}"' in ov and ('"face"' in ov.split(f'"{slug}"')[1].split("\n")[0] or "only_white" in ov.split(f'"{slug}"')[1].split("\n")[0]):
                stt = "PASS"
            if f"def {slug}(" in hand:
                stt = "PASS"
            del dropped
            add("faithful", "box_in_plate", stt, round(biggest, 2),
                "" if stt == "PASS" else "R4: the big region is the app's TILE -> face=<its colour>, drop=[<its colour>], keep_ground=True")
        # stripes: several regions with near-identical hue (only regions the build uses)
        sys.path.insert(0, str(ROOT / "work/_lib"))
        import build_auto as ba
        o = ba.OVERRIDES.get(slug, {})
        used_regs = [r for r in regs if r["fill"] not in o.get("drop", [])
                     and (not o.get("only_white") or ba.is_whiteish(r["fill"]))]
        hs = [(hue(r["fill"]), r["fill"]) for r in used_regs if r["fill"].startswith("#")]
        coloured = [(h, f) for (h, s_, l_), f in [((a_[0][0], a_[0][1], a_[0][2]), a_[1]) for a_ in hs] if s_ > 0.25 and 0.15 < l_ < 0.9]
        groups = []
        for hh, f in sorted(coloured):
            if groups and abs(hh - groups[-1][-1][0]) < 28:
                groups[-1].append((hh, f))
            else:
                groups.append([(hh, f)])
        striped = [grp for grp in groups if len(grp) >= 3]
        ov = (ROOT / "work/_lib/build_auto.py").read_text()
        merged = f'"{slug}"' in ov and "merge_grad" in ov.split(f'"{slug}"')[1].split("\n")[0]
        if striped and not merged:
            add("app", "stripes", "WARN", [f for _, f in striped[0]],
                f'R1: python: OVERRIDES["{slug}"] = {{"merge_grad": [{[f for _, f in striped[0]]}]}}')
        else:
            add("app", "stripes", "PASS", 0)
        # thin parts (bands, lines) lose IoU to smoothing without visible harm: only a LARGE
        # part that matches badly is a failure; hand-built apps do not use these regions
        if f"def {slug}(" in (ROOT / "work/_lib/build_weak.py").read_text():
            add("app", "trace_iou", "PASS", "hand-built")
        else:
            sys.path.insert(0, str(ROOT / "work/_lib"))
            import build_auto as ba
            o = ba.OVERRIDES.get(slug, {})
            merged = {c for grp in o.get("merge_grad", []) for c in grp}
            used = [r for r in regs if r["fill"] not in o.get("drop", [])
                    and (not o.get("only_white") or ba.is_whiteish(r["fill"]))
                    and r["fill"] not in merged]          # merged parts are rebuilt as one fitted part
            areas = {r["name"]: r["area"] for r in used}
            low = {k: v["iou"] for k, v in g["parts"].items() if k in areas and v.get("iou", 1) < 0.90}
            big = {k: i for k, i in low.items() if areas.get(k, 0) >= 0.03 and i < 0.75}
            stt = "FAIL" if big else ("WARN" if low else "PASS")
            add("app", "trace_iou", stt, big or low or "all >= 0.90",
                "" if stt == "PASS" else "R12: re-run with --remeasure; if still low the region is noise -> drop it")
    if as_json:
        print(json.dumps(res, indent=1))
    else:
        for r in res:
            line = f'{r["status"]:4}  {r["scope"]:9} {r["check"]:14} {r["value"]}'
            if r["fix"]:
                line += f'   -> FIX: {r["fix"]}'
            print(line)
        n = {s: sum(r["status"] == s for r in res) for s in ("PASS", "WARN", "FAIL")}
        print(f'\nsummary: {n["PASS"]} PASS, {n["WARN"]} WARN, {n["FAIL"]} FAIL  '
              f'({"OK to continue" if n["FAIL"] == 0 else "fix every FAIL, then run again"})')
    sys.exit(1 if any(r["status"] == "FAIL" for r in res) else 0)


if __name__ == "__main__":
    main()
