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
    # game posters (archetype H): no clean vector identity element in a 192 px poster
    "clash_royale": {"skip": ["symbol"], "note": "WEAK: posterised trace of the game poster, not a real GNOME conversion; needs a hand-drawn emblem (crown/king) from a better source"},
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
        self.regs = [(self.P[r["name"]], snap(rep.get(r["fill"], r["fill"]))) for r in self.I["regions"]]
        G = self.I["ground"]
        self.gk = G["kind"]
        self.ground = snap(self.o.get("face", G.get("color", "#ffffff")))
        L, C = lch(self.ground) if self.gk != "none" else (1, 0)
        self.light = self.gk == "none" or (L > 0.9 and C < 0.05)
        self.dark_neutral = (not self.light) and is_dark_neutral(self.ground) and self.gk != "gradient"
        if self.light:
            self.ground = "#ffffff"
        if self.o.get("only_white"):
            self.regs = [(d, f) for d, f in self.regs if is_whiteish(f)]
        self.all_neutral = all(is_whiteish(f) or is_dark_neutral(f) for _, f in self.regs)
        self.has_white = any(is_whiteish(f) for _, f in self.regs)
        self.all_dark = all(is_dark_neutral(f) for _, f in self.regs)

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

    def marks(self, box):
        ds = [d for d, _ in self.regs]
        ref = ds if self.o.get("only_white") else [self.P["silhouette"]]
        out, s = place(ds + [self.P["silhouette"]], box, ref=ref)
        return [(d, f) for d, (_, f) in zip(out[:-1], self.regs)], out[-1], s

    def box(self, kind):
        x0, y0, x1, y1 = self.I["mark_bbox"]
        asp = (x1 - x0) / max(y1 - y0, 1e-6)
        sc = self.o.get("scale", 1.0)
        base = {"faithful": (64, 62, 72), "disc": (64, 63, 76), "rimmed": (64, 63, 64), "symbol": (64, 61, 106)}[kind]
        cx, cy, w = base
        w *= sc
        if asp > 1.35:                       # wordmarks / wide marks may use more width
            return box_c(cx, cy, min(w * 1.22, 112 if kind == "symbol" else 96), w)
        return box_c(cx, cy, w)

    def raised(self, ic, items, lift=2):
        fam.raised(ic, [(d, f, side_of(f)) for d, f in items], lift=lift)

    # ---- styles
    def faithful(self):
        ic = gk.Icon(f"{self.slug} - Faithful", fam.note(self.slug))
        if self.gk == "gradient" and not self.light:
            fam.plate(ic, self.ground, self.grad(ic, (12, 12, 116, 112)), self.bottom_color())
        else:
            fam.plate(ic, self.ground)
        items, _, _ = self.marks(self.box("faithful"))
        self.raised(ic, items)
        return ic

    def disc(self):
        ic = gk.Icon(f"{self.slug} - Sound Disc", fam.note(self.slug))
        if self.gk == "gradient" and not self.light:
            fam.disc(ic, self.ground, self.grad(ic, (5, 4, 123, 122)), self.bottom_color())
        else:
            fam.disc(ic, self.ground, top_light=0 if self.light else 0.6)
        items, _, _ = self.marks(self.box("disc"))
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
        items, _, _ = self.marks(self.box("rimmed"))
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
        items, sil, s = self.marks(self.box("symbol"))
        if mode == "margin":
            body = fam.offset_d(sil, 3.5)
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
            for d, f in items:
                faces.append((d, (self.ground if is_whiteish(f) else f), (gfill if is_whiteish(f) else None)))
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
            for i, (d, f) in enumerate(items):
                x0, _, x1, _ = gk.bbox_d(d)
                ic.path(gk.translate_d(d, 0, 4), ic.chin_gradient(f, x0, x1, (x1 - x0) * 0.25),
                        layer_id=f"body-{i}-chin", fill_rule="evenodd")
            for i, (d, f) in enumerate(items):
                ic.path(d, f, layer_id=f"body-{i}-face", fill_rule="evenodd")
        if self.light and "holes" in self.P:
            ref = self.P["silhouette"]
            hd, _ = place([self.P["holes"], ref], self.box("symbol"), ref=[ref])
            ic.path(hd[0], "#ffffff", layer_id="counters", fill_rule="evenodd")
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
    for slug in (sys.argv[1:] or slugs_all()):
        try:
            app = App(slug)
            for st, ic in app.build().items():
                fam.save(ic, slug, st)
            print(slug, "ok", app.gk, "symbol:", app.symbol_mode())
        except Exception as e:
            print(slug, "ERROR", repr(e))
