#!/usr/bin/env python3
"""Build the four pack styles for the batch apps from work/<slug>/geometry.json
(written by auto.py).   python3 work/_lib/build_auto.py [slug ...]

Same construction as group 1:
  faithful = square plate (tile colour, or its gradient) + the mark raised
  disc     = the tile colour as a disc + the mark raised
  rimmed   = Adwaita rim + recessed disc in the tile colour + the mark raised
  symbol   = the mark itself as the object:
             - white marks on a coloured tile are inverted (mark takes the tile colour,
               enclosed counters become white) - GNOME Calls/Telefon construction;
             - neutral marks on a dark neutral tile keep a tile-coloured margin (WhatsApp
               construction) so they read on light and dark wallpapers;
             - marks on a white/transparent tile keep their own colours.
Per-app decisions go in OVERRIDES (documented there).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fam  # noqa: E402
from fam import gk, shade, place, box_c  # noqa: E402
from gnome_kit import hex_to_oklab  # noqa: E402

WORK = fam.WORK
INK = "#241f31"

# slug -> options. keys:
#   skip: [styles] not built (style falls back to Faithful)       scale: mark size factor
#   symbol: "keep" | "invert" | "margin"   force a symbol mode      face: plate/disc colour override
#   regions: {old_hex: new_hex} colour snaps decided in review       note: text for the brief
OVERRIDES = {
    # waves on the tile are photo-like shading; the identity is the white wordmark
    "anker_soundcore": {"only_white": True, "skip": ["symbol"],
                        "note": "wordmark only (tile waves are photographic shading); no Symbol: a white wordmark alone vanishes on light wallpapers"},
    # face bleeds off the left/right edge of the source tile: a free symbol would be a
    # "mask" with straight cut sides (completing them would invent the head silhouette)
    "duolingo": {"skip": ["symbol"], "rimmed_scale": 1.1,
                 "note": "Symbol is hand-built (build_weak.duolingo closes the tile-cut sides); Rimmed mark enlarged to fill the recess"},
    # game posters (archetype H): no clean vector identity element in a 192 px poster
    "clash_royale": {"skip": ["symbol"], "note": "WEAK: posterised trace of the game poster, not a real GNOME conversion; needs a hand-drawn emblem (crown/king) from a better source"},
    # blurry 192 px source: the pale green region is the blur halo + the semi-transparent mic
    "bcr": {"note": "blurry source: halo around the handset dropped, the separate pale microphone kept (semi-transparent white in the source), traced with 1.6 u smoothing"},
    "databackup": {"keep_ground": True, "note": "peach tile kept (it is the app's colour, not a neutral canvas)"},
    "enpara": {"light": True, "note": "white tile; the colour bars are part of the mark"},
    "exteraless": {"face": "#ffe9e9", "flat": True, "keep_ground": True, "drop": ["#ffdbdb"], "merge_grad": [["#ff8291", "#ff75a1", "#ff937f", "#ffa865", "#ffbb4d"]],
                   "note": "soft pink glow dropped (no glows in GNOME); the chevron is ONE part with its measured pink->orange gradient (no bands)"},
    "bitchord": {"merge_grad": [["#edaeb8", "#f8e3e6"]], "note": "the waves are one white->pink gradient (measured), not two flat bands"},
    "firefox_beta": {"merge_grad": [["#ffc041", "#ff692d", "#c6124b"], ["#962dcc", "#5f44b8"]], "holes_inlay": ["#2cecd3"],
                     "note": "fox flame = one yellow->red gradient, globe = one purple gradient (check_icon: stripes + low trace IoU); BETA badge kept"},
    "firefox_nightly": {"merge_grad": [["#28baf6", "#5d84fe", "#7a4ff4"]],
                        "note": "the fox body is one cyan->violet gradient (no hard edge to the purple belly); tail and globe keep their tones"},
    "reddit": {"symbol": "margin", "note": "Symbol: white Snoo with an orange margin (Reddit's own logo use), not an orange Snoo"},
    "pentas": {"keep_ground": True, "note": "peach tile kept"},
    "t_rk_telekom": {"erase": [(28, 102, 80, 128)], "drop": ["#16719d"], "note": "the dark-blue triangle at the bottom is a blurred background shape, not part of the logo (owner); removed and the mark re-aligned; the rest of that dark-blue region was only blur rims around the triangles (dropped)"},
    "stride": {"merge_grad": [["#83eca0", "#28c79b", "#1f916b"]], "note": "runner is one light-green->teal gradient; the dark track stays separate"},
    "smart_launcher": {"merge_grad": [["#7cc8f7", "#5fbbff", "#668dfe", "#7171ff"]], "note": "the lower layer is one blue->violet gradient"},
    "nuvio": {"merge_grad": [["#3cc3e2", "#2970c7", "#5059d2", "#7744d1", "#b04df0"]], "note": "the play shape is one cyan->violet gradient"},
    "proton_drive": {"merge_grad": [["#754bfc", "#a353e7", "#cb59d6"]], "note": "front of the folder is one violet->magenta gradient; the lighter back flap stays separate"},
    "morphe": {"merge_grad": [["#02afae", "#1085ab", "#1e5aa8"]], "note": "the M is one teal->blue gradient"},
    "today_weather": {"merge_grad": [["#fb564e", "#fd7958", "#fea665"]], "note": "the arc and spiral are one red->orange gradient"},
    "obtainx": {"regions": {"#aaa9d8": "#6a7fb7"}, "note": "the gear is blue-grey in the source (k-means median drifted to lavender)"},
    "proton_vpn": {"merge_grad": [["#b3e9f3", "#46a2e0"]], "note": "the lower tip is one turquoise gradient (measured), not two flat bands"},
    "sd_maid_se": {"symbol": "keep", "split": [("#fdd19d", (20, 10, 62, 52), "#fed73c")], "note": "dark apron measured as its own part (auto THRESH); Symbol keeps the white bow and collar (invert made them dark)"},
    "quarry": {"symbol": "keep", "split": [("#2a91f2", (42, 44, 86, 83), "#303b56")],
               "note": "chart bars are dark slate in the source (k-means folded them into the blue ring part); Symbol keeps the white folder (inverting made it navy)"},
    "hepsiburada": {"skip": ["symbol"], "note": "source: official orange-square logo sent by the owner (the phone shows an outdated poster icon); Symbol hand-built in build_weak"},
    "pix_material_you_light_dark": {"symbol": "margin", "note": "dark mark on a dark slate tile: Symbol keeps a slate margin"},
    "hesap_makinesi": {"skip": ["symbol"], "note": "two-tone tile + long shadow are tangled with the mark; no clean Symbol"},
    "konabess": {"note": "WEAK: line drawing with small text, unreadable below 64 px (source limitation)"},
    "plush_iconpack": {"keep_ground": True, "face": "#347ef3", "drop": ["#145be0", "#347ef3", "#509afc"],
                       "note": "the blue squircle IS the app tile -> becomes the plate/disc colour (no squircle inside a plate); swirl is the mark"},
    "scene": {"drop": ["#4b84db"], "note": "dark-blue fragments (stray edge line, strip under the robot) dropped"},
    "recon": {"symbol": "margin", "note": "white brackets: Symbol keeps a dark tile margin"},
    "shizuku": {"only_white": True, "note": "the white head is the mark; the lighter hexagon is tile decoration"},
    "trendyolmilla": {"only_white": True, "skip": ["symbol"], "note": "white wordmark only (background blobs are tile decoration); no Symbol"},
    "vortex": {"flat": True, "face": "#0d0e0d", "drop": ["#0d0e0d"], "note": "flat black tile (the spiral touching the edge skewed the gradient fit)"},
    "wupp": {"flat": True, "face": "#131c23", "drop": ["#131c23"], "note": "flat dark tile behind the green bubble"},
    "walpy": {"scale": 0.76, "note": "blurry signature: only its sharp core traced (threshold 0.85); kept at the source's ~40 % proportion"},
    "mt_manager": {"scale": 1.18, "note": "folder object larger on the plate (was a small box in a big plate)"},
    "ashell_you": {"margin_w": 7.0, "symbol_scale": 0.86, "note": "black robot: wide white margin so the Symbol still reads on dark wallpapers (check_icon visible_dark)"},
    "survivor_io": {"skip": ["symbol"], "note": "WEAK: posterised trace of the game poster, not a real GNOME conversion"},
}


def lch(h):
    L, a, b = hex_to_oklab(h)
    return L, (a * a + b * b) ** 0.5


def is_white(h):
    L, C = lch(h)
    return L > 0.92 and C < 0.04


def is_whiteish(h):
    """white marks as they come out of small/blurry sources (BCR's handset is #e9f3ea)."""
    L, C = lch(h)
    return L > 0.85 and C < 0.08


def is_dark_neutral(h):
    L, C = lch(h)
    return L < 0.32 and C < 0.05


def snap(h):
    """pure blacks -> Dark4 (GNOME never uses #000 faces)."""
    L, C = lch(h)
    return INK if (L < 0.22 and C < 0.03) else h


def load(slug):
    g = json.loads((WORK / slug / "geometry.json").read_text())
    P = {k: v["d"] for k, v in g["parts"].items()}
    return P, g["info"]


def side_of(fill):
    return "#deddda" if is_white(fill) else shade(fill, -0.14 if lch(fill)[0] > 0.42 else -0.06)


class App:
    def __init__(self, slug):
        self.slug = slug
        self.P, self.I = load(slug)
        self.o = OVERRIDES.get(slug, {})
        rep = self.o.get("regions", {})
        self.I0 = self.I
        self.regs = [(self.P[r["name"]], snap(rep.get(r["fill"], r["fill"]))) for r in self.I["regions"]]
        # "erase": [(x0, y0, x1, y1)] - subpaths lying inside a box are not part of the mark
        # (a blurred background shape traced with it, e.g. Turk Telekom's bottom triangle);
        # removed from every region AND the silhouette, and the mark box is re-measured so
        # the logo is centred/aligned without it
        def _keep(d, boxes):
            subs = ["M" + x for x in d.split("M") if x.strip()]
            inside = lambda b, q: b[0] >= q[0] and b[1] >= q[1] and b[2] <= q[2] and b[3] <= q[3]  # noqa: E731
            return "".join(x for x in subs if not any(inside(gk.bbox_d([x]), q) for q in boxes))
        if self.o.get("erase"):
            boxes = self.o["erase"]
            self.regs = [(_keep(d, boxes), f) for d, f in self.regs]
            self.P = dict(self.P, silhouette=_keep(self.P["silhouette"], boxes))
            if "holes" in self.P:
                self.P["holes"] = _keep(self.P["holes"], boxes) or self.P["holes"]
            self.I = dict(self.I, mark_bbox=list(gk.bbox_d([d for d, _ in self.regs if d])))
        # "split": [(fill, (x0, y0, x1, y1), new_fill)] - subpaths of a region that lie inside
        # the box become their own region (thin parts k-means folded into a bigger colour)
        for fill, (bx0, by0, bx1, by1), new in self.o.get("split", []):
            out = []
            for d, f in self.regs:
                if f != snap(fill):
                    out.append((d, f))
                    continue
                subs = ["M" + x for x in d.split("M") if x.strip()]
                inside = [x for x in subs if (lambda b: b[0] >= bx0 and b[1] >= by0 and b[2] <= bx1 and b[3] <= by1)(gk.bbox_d([x]))]
                rest = [x for x in subs if x not in inside]
                if rest:
                    out.append(("".join(rest), f))
                if inside:
                    out.append(("".join(inside), snap(new)))
            self.regs = out
        G = self.I["ground"]
        self.gk = G["kind"]
        self.ground = snap(self.o.get("face", G.get("color", "#ffffff")))
        if self.o.get("flat"):
            self.gk = "flat"
        L, C = lch(self.ground) if self.gk != "none" else (1, 0)
        self.light = self.gk == "none" or (L > 0.9 and C < 0.05)
        self.dark_neutral = (not self.light) and is_dark_neutral(self.ground) and self.gk != "gradient"
        if self.o.get("flat"):
            self.gk = "flat"
        if self.o.get("light"):
            self.light, self.gk = True, "flat"
        if self.o.get("keep_ground"):
            self.light = False
        if self.light:
            self.ground = "#ffffff"
        self.grads = {}
        for gi, group in enumerate(self.o.get("merge_grad", [])):
            self._merge(gi, group)
        # every other big region whose own source pixels change colour clearly (a gradient in
        # the source) keeps that gradient instead of being flattened to its median colour
        if not self.o.get("flat_regions"):
            gi = len(self.o.get("merge_grad", []))
            for r in list(self.I["regions"]):
                if (r["fill"] in self.grads or r.get("area", 0) < 0.02 or r["fill"] in self.o.get("drop", [])
                        or is_whiteish(r["fill"])):       # white marks stay clean white (GNOME)
                    continue
                if self._merge(gi, [r["fill"]], min_de=10.0):
                    gi += 1
        # "holes_inlay": [fill]: the holes of these regions (letters cut out of a badge) are
        # drawn on top in the tile colour - otherwise the region's own lift side fills them
        names = {r["name"] for r in self.I0["regions"] if r["fill"] in self.o.get("holes_inlay", [])}
        self.inlay_ds = {d for (d, _), r in zip(self.regs, self.I["regions"]) if r.get("name") in names}
        if self.o.get("drop"):
            self.regs = [(d, f) for (d, f), r in zip(self.regs, self.I["regions"]) if r["fill"] not in self.o["drop"]]
        if self.o.get("only_white"):
            self.regs = [(d, f) for d, f in self.regs if is_whiteish(self.base(f))]
        bs = [self.base(f) for _, f in self.regs]
        self.all_neutral = all(is_whiteish(f) or is_dark_neutral(f) for f in bs)
        self.has_white = any(is_whiteish(f) for f in bs)
        self.all_dark = all(is_dark_neutral(f) for f in bs)

    def _merge(self, gi, group, min_de=None):
        """Regions that are bands of ONE source gradient -> one part with a linear gradient
        fitted (least squares, RGB plane over x,y) to the source pixels it covers."""
        import numpy as np
        from build_weak import poly_of, d_of
        from shapely.ops import unary_union
        import gtrace as gt
        idx = [i for i, r in enumerate(self.I["regions"]) if r["fill"] in group]
        if not idx:
            return False
        union = d_of(unary_union([poly_of(self.regs[i][0]) for i in idx]).buffer(0))
        a, s = gt.load(WORK / self.slug)
        m = gt.render_mask(union, a.shape[0]) & (a[..., 3] > 0.5)
        ys, xs = np.nonzero(m)
        X, Y = xs * s, ys * s
        A = np.c_[X, Y, np.ones_like(X)]
        coef = np.linalg.lstsq(A, a[ys, xs, :3], rcond=None)[0]          # 3x3
        J = coef[:2].T                                                     # 3x2 colour change per x,y
        u = np.linalg.svd(J, full_matrices=False)[2][0]
        tproj = X * u[0] + Y * u[1]
        lo, hi = np.percentile(tproj, 2), np.percentile(tproj, 98)
        cxm, cym = X.mean(), Y.mean()
        base_t = cxm * u[0] + cym * u[1]
        p0 = (cxm + (lo - base_t) * u[0], cym + (lo - base_t) * u[1])
        p1 = (cxm + (hi - base_t) * u[0], cym + (hi - base_t) * u[1])
        col = lambda p: np.clip(coef[0] * p[0] + coef[1] * p[1] + coef[2], 0, 1)  # noqa: E731
        hexc = lambda c: "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)  # noqa: E731
        stops = [(0, hexc(col(p0))), (0.5, hexc(col(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)))), (1, hexc(col(p1)))]
        if min_de is not None:
            if any(snap(c) != c for _, c in stops):
                return False        # near-black: GNOME's Dark4 rule wins over the source gradient
            from skimage.color import rgb2lab
            l0, l1 = rgb2lab(np.array([[col(p0), col(p1)]]))[0]
            if np.linalg.norm(l0 - l1) < min_de:
                return False        # (nearly) flat in the source: keep the measured colour
        key = f"grad{gi}"
        self.grads[key] = {"stops": stops, "p0": p0, "p1": p1, "base": stops[1][1]}
        merged = {"name": "merged", "fill": key, "area": sum(self.I["regions"][i].get("area", 0) for i in idx)}
        self.I = dict(self.I)
        if min_de is not None and len(idx) == 1:          # one region: keep its drawing order
            i = idx[0]
            self.regs = self.regs[:i] + [(self.regs[i][0], key)] + self.regs[i + 1:]
            self.I["regions"] = self.I["regions"][:i] + [dict(self.I["regions"][i], fill=key)] + self.I["regions"][i + 1:]
            return True
        keep = [r for i, r in enumerate(self.regs) if i not in idx]
        self.regs = [(union, key)] + keep
        self.I["regions"] = [merged] + [r for i, r in enumerate(self.I["regions"]) if i not in idx]
        return True

    def base(self, f):
        return self.grads[f]["base"] if f in self.grads else f

    def resolve(self, ic, items, s, src_box, box):
        """turn merged-gradient keys into url(#..) placed like the paths (same transform)."""
        out = []
        for d, f in items:
            if f in self.grads:
                g = self.grads[f]
                ref = [self.P["silhouette"]] if not (self.o.get("only_white") or self.o.get("drop")) else None
                mk = lambda p: f"M{p[0]:.2f} {p[1]:.2f}h0.01v0.01h-0.01Z"  # noqa: E731
                ds = [d for d, _ in self.regs] + [self.P["silhouette"], mk(g["p0"]), mk(g["p1"])]
                rr = ref or [d for d, _ in self.regs]
                placed, _ = place(ds, box, ref=rr)
                q0, q1 = gk.bbox_d(placed[-2])[:2], gk.bbox_d(placed[-1])[:2]
                out.append((d, ic.linear(g["stops"], q0[0], q0[1], q1[0], q1[1]), g["base"]))
            else:
                out.append((d, f, f))
        return out

    # ---- faces
    def grad(self, ic, box, dark=0.0):
        G = self.I["ground"]
        x0, y0, x1, y1 = box
        mx = lambda v: x0 + v / 128 * (x1 - x0)   # noqa: E731
        my = lambda v: y0 + v / 128 * (y1 - y0)   # noqa: E731
        c0, c1 = G["c0"], G["c1"]
        if dark:
            c0, c1 = shade(c0, -dark, 0.9), shade(c1, -dark, 0.9)
        return ic.linear([(0, c0), (1, c1)], mx(G["p0"][0]), my(G["p0"][1]), mx(G["p1"][0]), my(G["p1"][1]))

    def bottom_color(self):
        G = self.I["ground"]
        return G["c1"] if G["p1"][1] >= G["p0"][1] else G["c0"]

    def marks(self, box, ic=None):
        ds = [d for d, _ in self.regs]
        ref = ds if (self.o.get("only_white") or self.o.get("drop")) else [self.P["silhouette"]]
        out, s = place(ds + [self.P["silhouette"]], box, ref=ref)
        items = [(d, f) for d, (_, f) in zip(out[:-1], self.regs)]
        if ic is not None:
            items = self.resolve(ic, items, s, None, box)
        else:
            items = [(d, f, self.base(f)) for d, f in items]
        return items, out[-1], s

    def box(self, kind):
        x0, y0, x1, y1 = self.I["mark_bbox"]
        if kind == "symbol" and (self.o.get("only_white") or self.o.get("drop")):
            # the Symbol is placed by the DRAWN parts (marks() ref): size it by them too,
            # otherwise dropped parts make it float above the baseline (Scene)
            x0, y0, x1, y1 = gk.bbox_d([d for d, _ in self.regs])
        asp = (x1 - x0) / max(y1 - y0, 1e-6)
        sc = self.o.get("scale", 1.0) if kind != "symbol" else self.o.get("symbol_scale", 1.0)
        if kind == "rimmed":
            sc *= self.o.get("rimmed_scale", 1.0)
        base = {"faithful": (64, 62, 72), "disc": (64, 63, 76), "rimmed": (64, 63, 64), "symbol": (64, 61, 106)}[kind]
        cx, cy, w = base
        w *= sc
        bw, bh = (min(w * 1.22, 112 if kind == "symbol" else 96), w) if asp > 1.35 else (w, w)
        if kind == "symbol":
            # free objects stand on the GNOME baseline (face bottom ~114 + 4 px chin),
            # instead of floating in the middle when they are wider than tall
            h = min(bh, bw / asp)
            if self.symbol_mode() == "margin":
                # the margin grows outward on every side: object + margin must fit 5..118
                m = self.o.get("margin_w", 3.5)
                k = min(1.0, (109 - 2 * m) / h)
                bw, bh, h = bw * k, bh * k, h * k
                cy = 114 - h / 2 - m                  # margin bottom on the baseline
            else:
                cy = 114 - h / 2
        return box_c(cx, cy, bw, bh)

    def raised(self, ic, items, lift=2):
        fam.raised(ic, [(d, f, side_of(b)) for d, f, b in items], lift=lift)
        self.inlays(ic, items)

    def inlays(self, ic, items):
        if not self.inlay_ds:
            return
        from build_weak import poly_of, d_of
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
        for i, (d, _f, _b) in enumerate(items):
            if i < len(self.regs) and self.regs[i][0] in self.inlay_ds:
                g = poly_of(d)
                holes = [Polygon(r) for p in getattr(g, "geoms", [g]) for r in p.interiors]
                if holes:
                    ic.path(d_of(unary_union(holes)), snap(self.ground), layer_id=f"inlay-{i}", fill_rule="evenodd")

    # ---- styles
    def faithful(self):
        ic = gk.Icon(f"{self.slug} - Faithful", fam.note(self.slug))
        if self.gk == "gradient" and not self.light:
            fam.plate(ic, self.ground, self.grad(ic, (12, 12, 116, 112)), self.bottom_color())
        else:
            fam.plate(ic, self.ground)
        items, _, _ = self.marks(self.box("faithful"), ic)
        self.raised(ic, items)
        return ic

    def disc(self):
        ic = gk.Icon(f"{self.slug} - Sound Disc", fam.note(self.slug))
        if self.gk == "gradient" and not self.light:
            fam.disc(ic, self.ground, self.grad(ic, (5, 4, 123, 122)), self.bottom_color())
        else:
            fam.disc(ic, self.ground, top_light=0 if self.light else 0.6)
        items, _, _ = self.marks(self.box("disc"), ic)
        self.raised(ic, items)
        return ic

    def rimmed(self):
        ic = gk.Icon(f"{self.slug} - Rimmed", fam.note(self.slug))
        if self.light:
            ic.rimmed_disc(inner="#ffffff", rim_face="#deddda", rim_chin="#c0bfbc")
        elif self.gk == "gradient":
            ic.rimmed_disc(inner=self.ground, inner_gradient=self.grad(ic, (10.5, 9.5, 117.5, 116.5)))
        else:
            ic.rimmed_disc(inner=self.ground)
        items, _, _ = self.marks(self.box("rimmed"), ic)
        self.raised(ic, items)
        return ic

    def symbol_mode(self):
        if "symbol" in self.o:
            return self.o["symbol"]
        if self.light:
            return "margin" if self.all_dark else "keep"
        if self.dark_neutral:
            return "keep" if not self.all_neutral else "margin"
        return "invert" if self.has_white else "keep"

    def symbol(self):
        mode = self.symbol_mode()
        ic = gk.Icon(f"{self.slug} - Free Symbol", fam.note(self.slug) + f" | symbol mode: {mode}")
        items, sil, s = self.marks(self.box("symbol"), ic)
        if mode == "margin":
            body = fam.offset_d(sil, self.o.get("margin_w", 3.5))
            if self.light:
                x0, _, x1, _ = gk.bbox_d(body)
                c = ic.chin_gradient("#c0bfbc", x0, x1, (x1 - x0) * 0.3,
                                     colors={"edge": "#9a9996", "base": "#c0bfbc", "highlight": "#deddda"})
                with ic.group("body"):
                    ic.path(gk.translate_d(body, 0, 4), c, layer_id="body-chin")
                    ic.path(body, "#ffffff", layer_id="body-face")
                if "holes" in self.P:
                    ref = self.P["silhouette"]
                    hd, _ = place([self.P["holes"], ref], self.box("symbol"), ref=[ref])
                    ic.path(hd[0], "#ffffff", layer_id="counters", fill_rule="evenodd")
                self.raised(ic, items, lift=1.5)
                return ic
            fam.slab(ic, body, self.ground, depth=4)
            self.raised(ic, items, lift=1.5)
            return ic
        if mode == "invert":
            gfill = None
            if self.gk == "gradient":
                x0, y0, x1, y1 = gk.bbox_d(sil)
                gfill = self.grad(ic, (x0, y0, x1, y1))
            faces = []
            for d, f, b in items:
                faces.append((d, (self.ground if is_whiteish(b) else b), (gfill if is_whiteish(b) else (f if f != b else None))))
            with ic.group("body"):
                for i, (d, f, _g) in enumerate(faces):
                    x0, _, x1, _ = gk.bbox_d(d)
                    ic.path(gk.translate_d(d, 0, 4), ic.chin_gradient(f, x0, x1, (x1 - x0) * 0.25),
                            layer_id=f"body-{i}-chin", fill_rule="evenodd")
                for i, (d, f, g) in enumerate(faces):
                    ic.path(d, g or f, layer_id=f"body-{i}-face", fill_rule="evenodd")
            if "holes" in self.P:
                x0, y0, x1, y1 = self.I["mark_bbox"]
                ref = self.P["silhouette"]
                hd, _ = place([self.P["holes"], ref], self.box("symbol"), ref=[ref])
                ic.path(hd[0], "#ffffff", layer_id="counters", fill_rule="evenodd")
                ic.path(hd[0] + gk.translate_d(hd[0], 0, 1.4), "#000000", layer_id="counters-recess",
                        opacity=0.10, fill_rule="evenodd")
            return ic
        # keep: the mark's own colours, every region extruded (all chins first)
        with ic.group("body"):
            for i, (d, f, b) in enumerate(items):
                x0, _, x1, _ = gk.bbox_d(d)
                ic.path(gk.translate_d(d, 0, 4), ic.chin_gradient(b, x0, x1, (x1 - x0) * 0.25),
                        layer_id=f"body-{i}-chin", fill_rule="evenodd")
            for i, (d, f, b) in enumerate(items):
                ic.path(d, f, layer_id=f"body-{i}-face", fill_rule="evenodd")
        self.inlays(ic, items)
        if (self.light or self.o.get("keep_ground")) and "holes" in self.P:
            ref = self.P["silhouette"]
            hd, _ = place([self.P["holes"], ref], self.box("symbol"), ref=[ref])
            ic.path(hd[0], "#ffffff" if self.light else self.ground, layer_id="counters", fill_rule="evenodd")
        return ic

    def build(self):
        out = {}
        for st in ("faithful", "disc", "rimmed", "symbol"):
            if st in self.o.get("skip", []):
                p = WORK / self.slug / f"{self.slug}-{st}.svg"
                if p.exists():
                    p.unlink()
                continue
            out[st] = getattr(self, st)()
        return out


def slugs_all():
    return [l.split("\t")[0] for l in (WORK / "_lib/batch_apps.tsv").read_text(encoding="utf-8").splitlines()]


if __name__ == "__main__":
    import builders
    hand = builders.hand_slugs()
    for slug in (sys.argv[1:] or slugs_all()):
        if slug in hand:
            # building these here would overwrite the redrawn icon with the automatic draft
            print(slug, "SKIP: hand-built in", builders.builder_of(slug), "- use tools/make_icon.py", slug)
            continue
        try:
            app = App(slug)
            for st, ic in app.build().items():
                fam.save(ic, slug, st)
            print(slug, "ok", app.gk, "symbol:", app.symbol_mode())
        except Exception as e:
            print(slug, "ERROR", repr(e))
