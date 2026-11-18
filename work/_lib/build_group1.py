#!/usr/bin/env python3
"""Group 1 builds (WhatsApp, Instagram, YouTube, Telefon, Mesajlar, Kamera,
Fotoğraflar, Saat, Ayarlar, ChatGPT).  python3 work/_lib/build_group1.py [slug ...]

Geometry: work/<slug>/geometry.json (measured, see extract_group1.py).
Each style is one construction used across the whole pack:
  faithful = square template plate · disc = brand disc · rimmed = Adwaita rim +
  recessed disc · symbol = the mark itself as the object (no plate).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fam  # noqa: E402
from fam import gk, shade, place, box_c, raised, white_items  # noqa: E402

B = {}


def build(fn):
    B[fn.__name__] = fn
    return fn


# ------------------------------------------------------------------ WhatsApp
@build
def whatsapp():
    P, I = fam.geo("whatsapp")
    G = "#25d366"
    marks = [P["ring"], P["handset"]]
    out = {}

    ic = gk.Icon("WhatsApp - Faithful", fam.note("whatsapp"))
    fam.plate(ic, G)
    ds, _ = place(marks, box_c(64, 62, 78))
    raised(ic, white_items(ds), lift=2)
    out["faithful"] = ic

    ic = gk.Icon("WhatsApp - Sound Disc", fam.note("whatsapp"))
    fam.disc(ic, G)
    ds, _ = place(marks, box_c(64, 63, 82))
    raised(ic, white_items(ds), lift=2)
    out["disc"] = ic

    ic = gk.Icon("WhatsApp - Rimmed", fam.note("whatsapp"))
    fam.rimmed(ic, G)
    ds, _ = place(marks, box_c(64, 63, 72))
    raised(ic, white_items(ds), lift=2)
    out["rimmed"] = ic

    # Symbol: WhatsApp's own standalone logo - green bubble, white ring, white handset.
    ic = gk.Icon("WhatsApp - Free Symbol", fam.note("whatsapp"))
    body = fam.offset_d(P["ring_outer"], 4.5)
    ds, _ = place([body, P["ring"], P["handset"]], box_c(64, 61, 110))
    fam.slab(ic, ds[0], G, depth=4)
    raised(ic, white_items(ds[1:]), lift=1.5)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Instagram
def insta_grad(ic, x0, y0, x1, y1):
    # measured: bottom #ffc800 / #ffb000, centre #ff2a79, top-right #f500cb, top-left #791cff
    return ic.linear([(0, "#ffc300"), (0.42, "#ff2a79"), (0.78, "#d300d9"), (1, "#7a1cff")],
                     x0 + (x1 - x0) * 0.62, y1, x0 + (x1 - x0) * 0.30, y0)


@build
def instagram():
    P, I = fam.geo("instagram")
    marks = [P["frame"], P["lens"], P["dot"]]
    out = {}
    chin_base = "#ff9f1a"   # chin sits under the orange/yellow bottom of the gradient

    ic = gk.Icon("Instagram - Faithful", fam.note("instagram"))
    fam.plate(ic, "#ff2a79", insta_grad(ic, 12, 12, 116, 112), chin_base)
    ds, _ = place(marks, box_c(64, 62, 70))
    raised(ic, white_items(ds), lift=2)
    out["faithful"] = ic

    ic = gk.Icon("Instagram - Sound Disc", fam.note("instagram"))
    fam.disc(ic, "#ff2a79", insta_grad(ic, 5, 4, 123, 122), chin_base, top_light=0.5)
    ds, _ = place(marks, box_c(64, 63, 68))
    raised(ic, white_items(ds), lift=2)
    out["disc"] = ic

    ic = gk.Icon("Instagram - Rimmed", fam.note("instagram"))
    fam.rimmed(ic, "#ff2a79", insta_grad(ic, 10.5, 9.5, 117.5, 116.5))
    ds, _ = place(marks, box_c(64, 63, 60))
    raised(ic, white_items(ds), lift=2)
    out["rimmed"] = ic

    # Symbol: the camera glyph itself as the object, filled with the brand gradient.
    ic = gk.Icon("Instagram - Free Symbol", fam.note("instagram"))
    ds, _ = place(marks, box_c(64, 61, 106))
    g = insta_grad(ic, 11, 8, 117, 114)
    ic.pieces(ds, face=chin_base, face_fill=g, depth=4, corner_r=26)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ YouTube
@build
def youtube():
    P, I = fam.geo("youtube")
    R = I["red"]                      # #ff0033
    R_SIDE = shade(R, -0.16)
    out = {}

    # Symbol (the play button IS the silhouette): red slab, white triangle.
    ic = gk.Icon("YouTube - Free Symbol", fam.note("youtube"))
    ds, _ = place([P["rect"], P["triangle"]], box_c(64, 72, 114, 84), ref=[P["rect"]])
    fam.slab(ic, ds[0], R, depth=4, corner_r=24)
    raised(ic, white_items([ds[1]]), lift=1.5)
    out["symbol"] = ic

    # Faithful: the source tile is white -> light Adwaita plate, raised play button.
    ic = gk.Icon("YouTube - Faithful", fam.note("youtube"))
    fam.plate(ic, fam.PAPER)
    ds, _ = place([P["rect"], P["triangle"]], box_c(64, 61, 84, 62), ref=[P["rect"]])
    raised(ic, [(ds[0], R, R_SIDE)], lift=2.5, layer="button")
    raised(ic, white_items([ds[1]]), lift=1, layer="play")
    out["faithful"] = ic

    ic = gk.Icon("YouTube - Sound Disc", fam.note("youtube"))
    fam.disc(ic, fam.PAPER, top_light=0)
    ds, _ = place([P["rect"], P["triangle"]], box_c(64, 62, 86, 64), ref=[P["rect"]])
    raised(ic, [(ds[0], R, R_SIDE)], lift=2.5, layer="button")
    raised(ic, white_items([ds[1]]), lift=1, layer="play")
    out["disc"] = ic

    # Rimmed: same construction as Disc (white inner, raised play button) - a red disc with
    # a triangle alone would read as YouTube Music.
    ic = gk.Icon("YouTube - Rimmed", fam.note("youtube"))
    ic.rimmed_disc(inner="#ffffff", rim_face="#deddda", rim_chin="#c0bfbc")
    ds, _ = place([P["rect"], P["triangle"]], box_c(64, 62, 78, 58), ref=[P["rect"]])
    raised(ic, [(ds[0], R, R_SIDE)], lift=2.5, layer="button")
    raised(ic, white_items([ds[1]]), lift=1, layer="play")
    out["rimmed"] = ic
    return out


# ------------------------------------------------------------------ Telefon (Fossify Phone)
@build
def telefon():
    P, I = fam.geo("telefon")
    G = I["green"]
    h = [P["handset"]]
    out = {}
    ic = gk.Icon("Telefon - Faithful", fam.note("telefon")); fam.plate(ic, G)
    ds, _ = place(h, box_c(64, 62, 66)); raised(ic, white_items(ds)); out["faithful"] = ic
    ic = gk.Icon("Telefon - Sound Disc", fam.note("telefon")); fam.disc(ic, G)
    ds, _ = place(h, box_c(64, 63, 66)); raised(ic, white_items(ds)); out["disc"] = ic
    ic = gk.Icon("Telefon - Rimmed", fam.note("telefon")); fam.rimmed(ic, G)
    ds, _ = place(h, box_c(64, 63, 58)); raised(ic, white_items(ds)); out["rimmed"] = ic
    ic = gk.Icon("Telefon - Free Symbol", fam.note("telefon"))
    ds, _ = place(h, box_c(64, 61, 104)); fam.slab(ic, ds[0], G, depth=4, corner_r=12); out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Mesajlar (Fossify Messages)
@build
def mesajlar():
    P, I = fam.geo("mesajlar")
    G = I["green"]
    out = {}
    bub = [P["bubble"]]
    for alt, title, base, box in (("faithful", "Faithful", fam.plate, box_c(64, 62, 76)),
                                  ("disc", "Sound Disc", fam.disc, box_c(64, 64, 74)),
                                  ("rimmed", "Rimmed", fam.rimmed, box_c(64, 64, 74))):
        ic = gk.Icon(f"Mesajlar - {title}", fam.note("mesajlar"))
        base(ic, G)
        ds, _ = place(bub, box)
        raised(ic, white_items(ds), lift=2)
        out[alt] = ic
    # Symbol: green bubble object (Polari-like), white lines raised.
    ic = gk.Icon("Mesajlar - Free Symbol", fam.note("mesajlar"))
    ds, _ = place([P["bubble_outer"], P["line0"], P["line1"], P["line2"]], box_c(64, 61, 110),
                  ref=[P["bubble_outer"]])
    fam.slab(ic, ds[0], G, depth=4, corner_r=10)
    raised(ic, white_items(ds[1:]), lift=1.5)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Kamera
@build
def kamera():
    P, I = fam.geo("kamera")
    # measured greys snapped to the HIG darks (dE small); pure black -> Dark4
    LENS, RING1, RING2, DOT = "#241f31", "#3d3846", "#5e5c64", "#ed333b"
    dc, r1o, r1i, r2o, r2i, dot = (I[k] for k in ("disc", "ring1_outer", "ring1_inner",
                                                  "ring2_outer", "ring2_inner", "dot"))

    def lens(ic, cx, cy, s, chin=2, layer="lens", edge=False):
        """Concentric lens from the measured radii, centred on (cx, cy), scale s."""
        R = dc["r"] * s
        c = ic.chin_gradient(LENS, cx - R, cx + R, R * 0.9)
        with ic.group(layer):
            if chin:
                ic.path(gk.circle_d(cx, cy + chin, R), c, layer_id=f"{layer}-chin")
            g = ic.linear([(0, "#3d3846"), (0.55, LENS), (1, "#1a1625")], 0, cy - R, 0, cy + R)
            if edge:   # light lens edge so the dark face separates from dark wallpapers
                ic.path(gk.circle_d(cx, cy, R), "#77767b", layer_id=f"{layer}-edge")
                ic.path(gk.circle_d(cx, cy + 0.6, R - 1.4), g, layer_id=f"{layer}-face")
            else:
                ic.path(gk.circle_d(cx, cy, R), g, layer_id=f"{layer}-face")
            for n, (o, i, col) in enumerate(((r1o, r1i, RING1), (r2o, r2i, RING2))):
                ox, oy = (o["cx"] - dc["cx"]) * s, (o["cy"] - dc["cy"]) * s
                ix, iy = (i["cx"] - dc["cx"]) * s, (i["cy"] - dc["cy"]) * s
                d = gk.circle_d(cx + ox, cy + oy, o["r"] * s) + gk.circle_d(cx + ix, cy + iy, i["r"] * s)
                ic.path(d, col, layer_id=f"{layer}-ring{n + 1}", fill_rule="evenodd")
        return R

    def red_dot(ic, x, y, r):
        c = ic.chin_gradient(DOT, x - r, x + r, r * 0.9)
        with ic.group("dot"):
            ic.path(gk.circle_d(x, y + 1.5, r), c, layer_id="dot-chin")
            ic.path(gk.circle_d(x, y, r), DOT, layer_id="dot-face")

    out = {}
    # composition measured in source units: dot centre relative to lens centre
    ddx, ddy = dot["cx"] - dc["cx"], dot["cy"] - dc["cy"]

    ic = gk.Icon("Kamera - Faithful", fam.note("kamera"))
    fam.plate(ic, fam.PAPER)
    s = 0.62
    cx, cy = 60, 66
    lens(ic, cx, cy, s, chin=2)
    red_dot(ic, cx + ddx * s * 0.82, cy + ddy * s * 0.82, dot["r"] * s)
    out["faithful"] = ic

    ic = gk.Icon("Kamera - Sound Disc", fam.note("kamera"))
    lens(ic, 64, 63, 59 / dc["r"], chin=2, layer="disc", edge=True)
    red_dot(ic, 64 + 31, 63 - 31, 7.5)   # recording light on the lens face, same direction
    out["disc"] = ic

    ic = gk.Icon("Kamera - Rimmed", fam.note("kamera"))
    inner = ic.rimmed_disc(inner=LENS)
    s = inner["r"] / dc["r"]
    with ic.group("rings"):
        for n, (o, i, col) in enumerate(((r1o, r1i, RING1), (r2o, r2i, RING2))):
            d = gk.circle_d(64 + (o["cx"] - dc["cx"]) * s, 63 + (o["cy"] - dc["cy"]) * s, o["r"] * s) + \
                gk.circle_d(64 + (i["cx"] - dc["cx"]) * s, 63 + (i["cy"] - dc["cy"]) * s, i["r"] * s)
            ic.path(d, col, layer_id=f"ring{n + 1}", fill_rule="evenodd")
    red_dot(ic, 64 + 41, 63 - 41, 9)
    out["rimmed"] = ic

    ic = gk.Icon("Kamera - Free Symbol", fam.note("kamera"))
    s = 0.86
    cx, cy = 58, 68
    lens(ic, cx, cy, s, chin=2, edge=True)
    red_dot(ic, cx + ddx * s, cy + ddy * s, dot["r"] * s)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Fotoğraflar (Google Photos)
@build
def foto_raflar():
    P, I = fam.geo("foto_raflar")
    names = ["yellow", "red", "blue", "green"]
    cxy = I["centre"]

    def petals(ic, box, chin=4, side=None, layer="pinwheel"):
        ds, s = place([P[n] for n in names], box)
        ox, oy = cxy
        bx0, by0, bx1, by1 = box
        # gradient per petal: measured inner (centre) colour -> outer colour, Showtime-style planes
        fills, chins = [], []
        for n, d in zip(names, ds):
            x0, y0, x1, y1 = gk.bbox_d(d)
            cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
            fx, fy = (x1 if abs(x1 - cx) > abs(x0 - cx) else x0), (y1 if abs(y1 - cy) > abs(y0 - cy) else y0)
            fills.append(ic.linear([(0, I[n + "_inner"]), (0.55, I[n]), (1, I[n])], cx, cy, fx, fy))
            chins.append(ic.chin_gradient(I[n], x0, x1, 6))
        with ic.group(layer):
            for n, d, c in zip(names, ds, chins):
                ic.path(gk.translate_d(d, 0, chin), c if side is None else side(n), layer_id=f"{n}-side")
            for n, d, f in zip(names, ds, fills):
                ic.path(d, f, layer_id=f"{n}-face")

    out = {}
    ic = gk.Icon("Fotoğraflar - Free Symbol", fam.note("foto_raflar"))
    petals(ic, box_c(64, 62, 110), chin=4)
    out["symbol"] = ic

    ic = gk.Icon("Fotoğraflar - Faithful", fam.note("foto_raflar"))
    fam.plate(ic, "#ffffff")
    petals(ic, box_c(64, 62, 76), chin=2)
    out["faithful"] = ic

    ic = gk.Icon("Fotoğraflar - Sound Disc", fam.note("foto_raflar"))
    fam.disc(ic, "#ffffff", top_light=0)
    petals(ic, box_c(64, 63, 80), chin=2)
    out["disc"] = ic

    ic = gk.Icon("Fotoğraflar - Rimmed", fam.note("foto_raflar"))
    ic.rimmed_disc(inner="#ffffff", rim_face="#deddda", rim_chin="#c0bfbc")
    petals(ic, box_c(64, 63, 72), chin=2)
    out["rimmed"] = ic
    return out


# ------------------------------------------------------------------ Saat (Fossify Clock)
@build
def saat():
    P, I = fam.geo("saat")
    G = I["green"]
    ro, ri = I["ring_outer"], I["ring_inner"]
    out = {}

    ic = gk.Icon("Saat - Faithful", fam.note("saat"))
    fam.plate(ic, G)
    ds, _ = place([P["ring"], P["hands"]], box_c(64, 62, 78), ref=[P["ring"]])
    raised(ic, white_items(ds), lift=2)
    out["faithful"] = ic

    ic = gk.Icon("Saat - Sound Disc", fam.note("saat"))
    fam.disc(ic, G)
    ds, _ = place([P["ring"], P["hands"]], box_c(64, 63, 84), ref=[P["ring"]])
    raised(ic, white_items(ds), lift=2)
    out["disc"] = ic

    # Rimmed = the clock itself: the light rim IS the white ring (ratio kept), green dial, hands.
    ic = gk.Icon("Saat - Rimmed", fam.note("saat"))
    rim = 59 * (1 - ri["r"] / ro["r"])
    ic.rimmed_disc(inner=G, rim=rim)
    s = 59 / ro["r"]
    hands = gk.xform_d(P["hands"], s, 64 - ro["cx"], 63 - ro["cy"], about=(ro["cx"], ro["cy"]))
    raised(ic, white_items([hands]), lift=2)
    out["rimmed"] = ic

    # Symbol: the clock as an object - green case, white face, green hands (inverse use).
    ic = gk.Icon("Saat - Free Symbol", fam.note("saat"))
    case = gk.circle_d(64, 62, 58)
    fam.slab(ic, case, G, depth=3, corner_r=52)
    s = 58 / ro["r"]
    ic.path(gk.circle_d(64, 62, ri["r"] * s), "#ffffff", layer_id="face")
    ic.path(gk.circle_d(64, 62, ri["r"] * s) + gk.circle_d(64, 63.4, ri["r"] * s), "#000000",
            layer_id="face-recess", opacity=0.10, fill_rule="evenodd")
    hands = gk.xform_d(P["hands"], s, 64 - ro["cx"], 62 - ro["cy"], about=(ro["cx"], ro["cy"]))
    raised(ic, [(hands, G, shade(G, -0.06))], lift=1.5)
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ Ayarlar (Settings)
@build
def ayarlar():
    P, I = fam.geo("ayarlar")
    BR = I["brown"]
    gear = [P["gear"]]
    out = {}
    for alt, title, base, box in (("faithful", "Faithful", fam.plate, box_c(64, 62, 80)),
                                  ("disc", "Sound Disc", fam.disc, box_c(64, 63, 80)),
                                  ("rimmed", "Rimmed", fam.rimmed, box_c(64, 63, 70))):
        ic = gk.Icon(f"Ayarlar - {title}", fam.note("ayarlar"))
        base(ic, BR)
        ds, _ = place(gear, box)
        raised(ic, white_items(ds), lift=2)
        out[alt] = ic
    ic = gk.Icon("Ayarlar - Free Symbol", fam.note("ayarlar"))
    ds, _ = place(gear, box_c(64, 61, 110))
    fam.slab(ic, ds[0], BR, depth=4, corner_r=10)   # real hole: its inner wall shows the chin
    out["symbol"] = ic
    return out


# ------------------------------------------------------------------ ChatGPT
@build
def chatgpt():
    P, I = fam.geo("chatgpt")
    k = [P["knot"]]
    INK = "#241f31"
    out = {}
    ic = gk.Icon("ChatGPT - Faithful", fam.note("chatgpt"))
    fam.plate(ic, fam.PAPER)
    ds, _ = place(k, box_c(64, 62, 88))
    ic.glyph(ds[0], fill=INK, lift=1.5, engrave=True, face_hint=fam.PAPER, fill_rule="evenodd", layer="knot")
    out["faithful"] = ic

    ic = gk.Icon("ChatGPT - Sound Disc", fam.note("chatgpt"))
    fam.disc(ic, INK, top_light=0.5)
    ds, _ = place(k, box_c(64, 63, 86))
    raised(ic, [(ds[0], "#ffffff", "#9a9996")], lift=1.5)
    out["disc"] = ic

    ic = gk.Icon("ChatGPT - Rimmed", fam.note("chatgpt"))
    fam.rimmed(ic, INK)
    ds, _ = place(k, box_c(64, 63, 80))
    raised(ic, [(ds[0], "#ffffff", "#9a9996")], lift=1.5)
    out["rimmed"] = ic
    # no Symbol: a colourless knot alone vanishes on dark (ink) or light (white) wallpapers;
    # the Symbol style falls back to Faithful for this app (see pack/styles.json).
    return out


if __name__ == "__main__":
    for slug in (sys.argv[1:] or B):
        for alt, ic in B[slug]().items():
            print(fam.save(ic, slug, alt))
