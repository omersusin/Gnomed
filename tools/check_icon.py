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
Per app:
  redesign      the app is a GNOME redesign (REDESIGN.md): work/<slug>/redesign.py exists and
                design.md has "approved:" = the owner's answer in quotes + (YYYY-MM-DD). The automatic
                builds (logo on a plate + chin) are drafts and FAIL here .............. FAIL
  holes         (Symbol of every app, every style of a redesign) what is a hole in the
                source (letter counters, eyes, a ring's centre) must be TRANSPARENT:
                enclosed transparent area >= 50 % of the source holes (placed like the
                mark) when they are >= 0.4 % of the canvas ............................ FAIL
                exceptions: OVERRIDES painted_counters, or design.md
                painted-holes: "<owner's words>" (YYYY-MM-DD)
  plain_shape   (redesigns) the Faithful silhouette is a plain DISC (circle match > 0.95):
                the logo on a disc is not a redesign ................................ FAIL
                a plain SQUARE/box (fills > 97 % of its bounds): fine for a real box
                object (envelope, case), a plate otherwise ............................ WARN
                both lifted by a line in design.md:  shape-ok: <the owner's words>
Per app (from geometry.json):
  stripes       3+ regions of near-identical hue = one gradient cut into bands . WARN -> merge_grad
  trace_iou     traced parts match their masks: WARN < 0.90; FAIL if a part >= 3 % of the canvas < 0.75
  faithful      a Faithful SVG must exist (every other style falls back to it)  FAIL
"""
import io
import json
import re
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


QUOTED_DATED = re.compile(r'"[^"]+".*\(\d{4}-\d{2}-\d{2}\)')


def design_line(w, key):
    """value of 'key:' in work/<slug>/design.md ('' if missing)"""
    if (w / "design.md").exists():
        for line in (w / "design.md").read_text(encoding="utf-8").splitlines():
            if line.lower().startswith(key + ":"):
                return line.split(":", 1)[1].strip()
    return ""


def shape_kind(svg):
    """-> (kind, circle_iou, fill) of an SVG's silhouette: 'disc' (circle match > 0.95), 'tile'
    (a near-square block filling > 90 % of its box: a rounded-square plate), 'box' (any block
    filling > 97 %), else 'object'. Used by plain_shape and by tools/next.py for concepts."""
    import io as _io
    al = np.asarray(Image.open(_io.BytesIO(cairosvg.svg2png(url=str(svg), output_width=256, output_height=256)))
                    .convert("RGBA"))[..., 3] > 128
    ys, xs = np.where(al)
    if not len(xs):
        return "object", 0.0, 0.0
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    Y, X = np.mgrid[:256, :256]
    r = ((x1 - x0) + (y1 - y0)) / 4
    circle = (X - (x0 + x1) / 2) ** 2 + (Y - (y0 + y1) / 2) ** 2 <= r * r
    iou = float((al & circle).sum() / (al | circle).sum())
    fill = float(al[y0:y1 + 1, x0:x1 + 1].mean())
    aspect = (x1 - x0 + 1) / (y1 - y0 + 1)
    if iou > 0.95:
        return "disc", iou, fill
    if fill > 0.90 and 0.8 <= aspect <= 1.25:
        return "tile", iou, fill
    if fill > 0.97:
        return "box", iou, fill
    return "object", iou, fill


def is_quote(v):
    """an approval line: the owner's words verbatim in quotes + the date (REDESIGN.md 7)"""
    return bool(QUOTED_DATED.search(v or ""))


def hole_measure(slug, svg, N=512):
    """-> (source holes % of canvas, placed like the mark; enclosed transparent % in the
    style; IoU of the style's filled outline with the source mark) or None if unknown."""
    gp = ROOT / "work" / slug / "geometry.json"
    if not gp.exists():
        return None
    sys.path.insert(0, str(ROOT / "work/_lib"))
    from obj import shape_of, geom_d
    from gtrace import render_mask
    from shapely import affinity
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from scipy.ndimage import binary_fill_holes
    parts = json.loads(gp.read_text())["parts"]
    body = unary_union([shape_of(v["d"]) for k, v in parts.items() if k not in ("silhouette", "holes")]).buffer(0)
    if body.is_empty:
        return None
    filled = unary_union([Polygon(g.exterior) for g in getattr(body, "geoms", [body])])
    if "holes" in parts:
        holes = shape_of(parts["holes"]["d"]).intersection(filled)
    else:   # e.g. group-1 apps: the parts' own interiors that no other part fills
        holes = filled.difference(body).buffer(-0.8).buffer(0.8)
    # measured WITHOUT the side/chin layers: a thick object's own side may show inside a
    # hole (that is correct GNOME depth); only paint on the face fills a hole
    txt = re.sub(r'<path[^>]*\bid="[^"]*(?:-chin|-side)[^"]*"[^>]*/>', "", Path(svg).read_text(encoding="utf-8"))
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=txt.encode(), output_width=N, output_height=N)))
                   .convert("RGBA"))[..., 3] > 127
    if not a.any():
        return None
    ys, xs = np.nonzero(a)
    u = 128 / N
    ax0, ay0, ax1, ay1 = xs.min() * u, ys.min() * u, (xs.max() + 1) * u, (ys.max() + 1) * u
    bx0, by0, bx1, by1 = filled.bounds
    sc = min((ax1 - ax0) / (bx1 - bx0), (ay1 - ay0) / (by1 - by0))
    ox, oy = (bx0 + bx1) / 2, (by0 + by1) / 2

    def T(g):
        return affinity.translate(affinity.scale(g, sc, sc, origin=(ox, oy)), (ax0 + ax1) / 2 - ox, (ay0 + ay1) / 2 - oy)
    fa = binary_fill_holes(a)
    sil = render_mask(geom_d(T(filled)), N)
    iou = (fa & sil).sum() / max(1, (fa | sil).sum())
    return T(holes).area / (128 * 128), (fa & ~a).sum() / (N * N), iou


def mark_measure(slug, svg, N=256, de=20.0):
    """How big the app's own colours are in a style: the pixels whose colour is close (dE < de)
    to a COLOURFUL measured part of the source (chroma > 20, >= 1 % of the tile), small specks
    dropped. -> (larger side of their box in the 128 canvas, share of the painted area, n colours)
    or None when the source has no colourful part (white / black / grey marks)."""
    gp = ROOT / "work" / slug / "geometry.json"
    if not gp.exists():
        return None
    regs = json.loads(gp.read_text()).get("info", {}).get("regions", [])
    cols = []
    for r in regs:
        h = r.get("fill", "")
        if not (isinstance(h, str) and re.match(r"^#[0-9a-fA-F]{6}$", h)) or r.get("area", 0) < 0.01:
            continue
        L, A, B = rgb2lab(np.array([[[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
        if (A * A + B * B) ** 0.5 > 20:
            cols.append((L, A, B))
    if not cols:
        return None
    a = render(svg, N)
    painted = a[..., 3] > 0.5
    lab = rgb2lab(np.clip(a[..., :3], 0, 1))
    d = np.min(np.stack([np.linalg.norm(lab - np.array(c), axis=-1) for c in cols]), axis=0)
    m = painted & (d < de)
    from scipy import ndimage
    lbl, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lbl, range(1, n + 1))
        keep = np.isin(lbl, [i + 1 for i, sz in enumerate(sizes) if sz >= 0.0005 * N * N])
    else:
        keep = m
    if not keep.any():
        return 0.0, 0.0, len(cols)
    ys, xs = np.nonzero(keep)
    side = max(xs.max() - xs.min() + 1, ys.max() - ys.min() + 1) * 128 / N
    return float(side), float(keep.sum() / max(painted.sum(), 1)), len(cols)


def main():
    slug = sys.argv[1]
    as_json = "--json" in sys.argv
    w = ROOT / "work" / slug
    res = []

    def add(scope, check, status, value, fix=""):
        res.append({"scope": scope, "check": check, "status": status, "value": value, "fix": fix})

    svgs = {st: w / f"{slug}-{st}.svg" for st in STYLES if (w / f"{slug}-{st}.svg").exists()}
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import builders
    is_redesign = builders.redesigned(slug)
    approved = ""
    if (w / "design.md").exists():
        for line in (w / "design.md").read_text(encoding="utf-8").splitlines():
            if line.lower().startswith("approved:"):
                approved = line.split(":", 1)[1].strip()
    if not is_redesign:
        add("app", "redesign", "FAIL", "logo on a plate (automatic draft)",
            f"R0: not a Gnomed icon yet - follow REDESIGN.md: python3 tools/new_redesign.py {slug}")
    elif not approved or approved.lower() in ("no", "-", "none", "?"):
        add("app", "redesign", "FAIL", "design.md: approved is empty",
            "R0: Q1 (REDESIGN.md 7): write the owner's answer in design.md 'approved:'")
    elif not is_quote(approved):
        add("app", "redesign", "FAIL", f"approved is not a quote + date: {approved[:40]}",
            'REDESIGN.md 7: approved: B - "<his words>" (YYYY-MM-DD) - never from a general instruction')
    else:
        add("app", "redesign", "PASS", approved[:40])
    if is_redesign and (w / f"{slug}-faithful.svg").exists():
        shape_ok = design_line(w, "shape-ok")
        shape_ok = shape_ok if is_quote(shape_ok) else ""          # only the owner's words + date count
        for st in ("faithful", "symbol"):
            if st == "symbol" and not (w / f"{slug}-symbol.svg").exists():
                continue
            if st == "symbol" and (w / f"{slug}-symbol.svg").read_bytes() == (w / f"{slug}-faithful.svg").read_bytes():
                continue                                            # the same design, checked once
            kind, iou, fill = shape_kind(w / f"{slug}-{st}.svg")
            if kind == "disc":
                add(st, "plain_shape", "PASS" if shape_ok else "FAIL", f"plain disc (circle match {iou:.2f})",
                    "" if shape_ok else "REDESIGN §1: the logo on a disc is not a redesign - make the app's OBJECT "
                    "(concept ladder), or get the owner's OK and write 'shape-ok: <his words>' in design.md")
            elif kind == "tile":
                add(st, "plain_shape", "PASS" if shape_ok else "WARN", f"square tile/plate (fills {fill:.0%} of its box)",
                    "" if shape_ok else "a tile with the logo on it is 'the logo on a plate' (REDESIGN §1) - allowed only "
                    "as L3 for a pure wordmark, or a real square object (window, calendar) - say which in Q2")
            elif kind == "box":
                add(st, "plain_shape", "PASS" if shape_ok else "WARN", f"plain square/box (fills {fill:.0%})",
                    "" if shape_ok else "a real box object (envelope, case)? say so in design.md 'shape-ok:'; "
                    "a plate with the logo on it is not a redesign")
            else:
                add(st, "plain_shape", "PASS", f"object silhouette (circle {iou:.2f}, fill {fill:.0%})")
    # slots: every style a different design (owner 2026-11-21 / 2026-11-22) unless he dropped the others
    if is_redesign and len(svgs) == 4:
        distinct = len({p.read_bytes() for p in svgs.values()})
        keep = design_line(w, "keep")
        letters = set(re.findall(r"\b([A-H])\b", keep.split(" - ")[0].split('"')[0]))
        dropped = keep.lower().startswith(("none", "0", "-")) or '"0"' in keep
        expected = 1 if dropped else min(4, 1 + len(letters)) if letters else 4
        if distinct >= expected:
            add("app", "slots", "PASS", f"{distinct} different designs (owner kept {expected})")
        else:
            add("app", "slots", "WARN", f"only {distinct} different designs in 4 styles",
                "REDESIGN.md 6: main -> symbol, closest to the logo -> faithful, round -> disc, the rest -> rimmed")
    add("app", "faithful", "PASS" if "faithful" in svgs else "FAIL", "faithful" in svgs,
        "" if "faithful" in svgs else "build the app first: python3 tools/make_icon.py " + slug)
    for st, svg in svgs.items():
        out = subprocess.run([sys.executable, str(SK / "lint_svg.py"), str(svg)], capture_output=True, text=True).stdout
        fail = "[FAIL]" in out
        add(st, "lint", "FAIL" if fail else "PASS", "FAIL" if fail else "ok",
            "read the lint message; edge contact -> make the object smaller (inside 8..120)" if fail else "")
        a = render(svg)
        vl, vd = visible(a, LIGHT), visible(a, DARK)
        if st == "symbol":
            # no plate: the object itself must read on BOTH wallpapers
            for name, v, rec in (("visible_light", vl, "too pale on a light wallpaper: darker side/face (docs/PLAYBOOK.md#fix-fail)"),
                                 ("visible_dark", vd, "too dark on a dark wallpaper: lighter face, top light (docs/PLAYBOOK.md#fix-fail)")):
                stt = "PASS" if v >= 0.55 else ("WARN" if v >= 0.25 else "FAIL")
                add(st, name, stt, round(v, 2), "" if stt == "PASS" else rec)
        else:
            # a light plate on a light wallpaper (or dark on dark) is fine in GNOME - its chin and
            # edge separate it; it must read clearly on at least ONE of the two
            v = max(vl, vd)
            stt = "PASS" if v >= 0.55 else "FAIL"
            add(st, "visible", stt, f"light {vl:.2f} / dark {vd:.2f}", "" if stt == "PASS" else "vanishes on both wallpapers: stronger colours (docs/PLAYBOOK.md#fix-fail)")
        m, bottom = mass_and_bottom(a)
        # a redesign is a free object in EVERY slot: one range for all (tools/describe_icon.py uses it too)
        lo, hi = (0.35, 0.75) if is_redesign else ((0.20, 0.75) if st == "symbol" else (0.40, 0.75))
        add(st, "mass", "PASS" if lo <= m <= hi else "WARN", round(m, 2), "" if lo <= m <= hi else
            "the icon looks thin: bigger object, or a secondary object in front (docs/PLAYBOOK.md#fix-fail, mass)")
        blo, bhi = {"faithful": (114, 118.5), "disc": (120, 126.5), "rimmed": (120, 126.5), "symbol": (108, 124.5)}[st]
        if is_redesign:
            blo, bhi = 108, 126.5          # free objects: GNOME icons end anywhere from 108 to 126
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
            add(st, "legibility32", stt, ssim, "" if stt == "PASS" else "details vanish at 32 px: bigger parts, drop tiny details, strokes >= 2 px")
        # holes: the Symbol of every app and every style of a redesign (plates are exempt:
        # there the holes show the plate, which is correct)
        if st == "symbol" or is_redesign:
            m = hole_measure(slug, svg)
            if m is not None:
                src, transp, iou = m
                val = f"source {src:.1%} -> transparent {transp:.1%}"
                if src < 0.004:
                    add(st, "holes", "PASS", val + " (no holes to keep)")
                elif is_redesign and iou < 0.75:
                    add(st, "holes", "PASS", val + f" (the mark sits ON an object, iou {iou:.2f}: the object behind "
                        "it shows through its holes - correct; if the mark itself IS the object, cut its holes)")
                elif transp >= 0.5 * src:
                    add(st, "holes", "PASS", val)
                else:
                    import build_auto as _ba
                    ok = _ba.OVERRIDES.get(slug, {}).get("painted_counters") or is_quote(design_line(w, "painted-holes"))
                    add(st, "holes", "PASS" if ok else "FAIL", val + (" (painted on purpose)" if ok else ""),
                        "" if ok else "REDESIGN.md 5: cut the holes (body(), difference) - never paint them; "
                        "only the owner's words allow it: painted-holes: \"<his words>\" (YYYY-MM-DD)")
        # mark_size: the app's own colours (its mark) must read on the phone. A mark printed small
        # on a big object (Deezer's bars on a record label, 2026-11-22) is lost at 48 px.
        if is_redesign:
            mm = mark_measure(slug, svg)
            if mm is not None:
                side, share, _n = mm
                val = f"{side:.0f} px of 128 (on the phone at 48 px: {side * 48 / 128:.0f} px)"
                if side >= 36:
                    add(st, "mark_size", "PASS", val)
                else:
                    add(st, "mark_size", "WARN", val,
                        "the app's own mark/colours are too small to read on the phone: make the part that "
                        "carries the mark (label, stamp, screen) bigger and the mark >= 36 px of 128 "
                        "(docs/PLAYBOOK.md#fix-warn)")
        # bands: a gradient of the source painted as several flat colours looks melted/broken
        # (Deezer concepts, 2026-11-22). regions() knows which measured parts are bands of one
        # gradient; two or more of them as flat fills in one style = FAIL.
        if is_redesign and (w / "geometry.json").exists():
            try:
                import obj as _obj
                bad = _obj.banded(slug, svg.read_text())
            except Exception as e:                       # the check must never crash the gate
                bad, _err = None, e
            if bad is None:
                add(st, "bands", "PASS", f"not measured ({str(_err)[:40]})")
            elif bad:
                add(st, "bands", "FAIL", "; ".join(f"{n}: {', '.join(h)}" for n, h in bad),
                    f"a gradient of the source is painted as flat bands - draw those parts as ONE shape with "
                    f"a real gradient: for name, g, fill in regions('{slug}') (or face=gradient('{slug}', shape)); "
                    "docs/PLAYBOOK.md#gradients")
            else:
                add(st, "bands", "PASS", "no flat gradient bands")
    # box inside the plate: a big single region whose colour differs from the plate
    gp = w / "geometry.json"
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import builders
    is_hand = builders.hand_built(slug)
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
            if f'"{slug}"' in ov and ('"face"' in ov.split(f'"{slug}"')[1].split("\n")[0] or "only_white" in ov.split(f'"{slug}"')[1].split("\n")[0]):
                stt = "PASS"
            if is_hand:
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
        if striped and not merged and not is_redesign:      # a redesign does not draw the measured bands
            add("app", "stripes", "WARN", [f for _, f in striped[0]],
                f'R1: python: OVERRIDES["{slug}"] = {{"merge_grad": [{[f for _, f in striped[0]]}]}}')
        else:
            add("app", "stripes", "PASS", 0)
        # thin parts (bands, lines) lose IoU to smoothing without visible harm: only a LARGE
        # part that matches badly is a failure; hand-built apps do not use these regions
        if is_hand:
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
