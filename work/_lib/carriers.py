"""CARRIERS - whole styles that carry the app's measured logo (Claude, 2026-11-23).

Why: the owner liked the group-4 icons; other models chose the right THING but could not draw it
(Haiku's sneaker became a block, Sonnet put the logo on dark plates). These are those group-4
objects as one-line functions. Each draws a complete style on the 128 canvas and puts the
MEASURED logo in the right place, at a size and contrast the gate accepts:

    from carriers import *
    def A(): ic = gk.Icon("x - symbol"); arrow(ic, SLUG, brand="#ff4500"); return ic

Pick each by the app's OWN anchor (docs/METHOD.md §1-2), never by the category alone.
`brand` = the app's main colour (hex, measured from source.png or the screenshots). The logo goes
on a light part when it is coloured or dark, on the brand colour when it is white.
The catalogue with every carrier: docs/kit.png (python3 tools/kit_sheet.py redraws it).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from objects import *  # noqa: F401,F403,E402
from obj import mark_parts, fit  # noqa: E402
from shapely import affinity  # noqa: E402
from shapely.geometry import LineString  # noqa: E402

LIGHT = ("#ffffff", "#f6f5f4", "#deddda", "#c0bfbc", "#9a9996")
STEEL = ("#ffffff", "#deddda", "#c0bfbc", "#9a9996", "#77767b")
DARK = ("#77767b", "#5e5c64", "#3d3846", "#241f31", "#1b1a1f")
GOLD = ("#fff1b8", "#f9d97a", "#f0b90b", "#d9a200", "#a87b00")


# ------------------------------------------------------------------ colours
def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _hex(c):
    return "#" + "".join(f"{max(0, min(255, round(v * 255))):02x}" for v in c)


def _mix(a, b, t):
    return _hex([x + (y - x) * t for x, y in zip(_rgb(a), _rgb(b))])


def ramp(base):
    """5 steps light -> dark around one brand colour (a tuple of 5 passes through)."""
    if isinstance(base, (tuple, list)):
        return tuple(base)
    return (_mix(base, "#ffffff", 0.45), _mix(base, "#ffffff", 0.2), base, _mix(base, "#000000", 0.18), _mix(base, "#000000", 0.38))


def _lum(h):
    r, g, b = _rgb(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def logo_tone(slug):
    """'light' (a white/pale logo: Snoo, a white wordmark), 'dark' (black: ChatGPT) or 'colour'"""
    parts = mark_parts(slug)
    tot = sum(g.area for _, g, _ in parts) or 1
    lum = sum(g.area * _lum(str(f) if str(f).startswith("#") else "#808080") for _, g, f in parts) / tot
    sat = 0.0
    for _, g, f in parts:
        r, gg, b = _rgb(str(f) if str(f).startswith("#") else "#808080")
        sat += g.area * (max(r, gg, b) - min(r, gg, b))
    sat /= tot
    if lum > 0.82 and sat < 0.25:
        return "light"
    if lum < 0.22 and sat < 0.25:
        return "dark"
    return "colour"


def face(r):
    return [(0, r[0]), (0.5, r[2]), (1, r[3])]


def logo(ic, slug, box_, on=None, body=0, side=None, anchor="center"):
    """the measured logo in box_. on='brand' + a light logo -> its own colours; a dark logo on a
    dark part -> white (put_mark face)."""
    tone = logo_tone(slug)
    fc = "#ffffff" if (on == "dark" and tone == "dark") else None
    return put_mark(ic, slug, box_, face=fc, body=body, side=side, anchor=anchor)


def logo_free(ic, slug, box_, margin_colour, anchor="bottom", margin=5):
    """the logo standing free in front of something: a white or black logo gets a die-cut margin in
    margin_colour so it reads on both wallpapers; a coloured logo stands with its own side."""
    tone = logo_tone(slug)
    if tone == "colour":
        main = max(mark_parts(slug), key=lambda p: p[1].area)[2]
        return put_mark(ic, slug, box_, anchor=anchor, body=4, side=_mix(str(main), "#000000", 0.35))
    shapes = fit([g for _, g, _ in mark_parts(slug)], box_, anchor=anchor)
    mg = rounded(unary_union(shapes).buffer(margin, quad_segs=24), 2)
    m = ramp(margin_colour)
    solid(ic, mg, face=face(m), depth=3, side=m[4], layer="logo-margin")
    return put_mark(ic, slug, box_, anchor=anchor)


def label(ic, shape, layer="label", depth=1.5):
    """a white label/plate printed or stuck on a part - where a coloured logo reads best"""
    solid(ic, shape, face=[(0, "#ffffff"), (1, "#eeeeec")], depth=depth, side="#c0bfbc", layer=layer)


# ------------------------------------------------------------------ the logo itself
def logo_object(ic, slug, brand=None, side=None):
    """FAITHFUL - the logo itself as a solid object (METHOD §2). A white or black logo gets a
    die-cut sticker margin in the brand colour (it would melt into one wallpaper)."""
    tone = logo_tone(slug)
    if tone in ("light", "dark") and brand:
        return sticker(ic, slug, brand)
    if side is None:
        main = max(mark_parts(slug), key=lambda p: p[1].area)[2]
        side = _mix(str(main) if str(main).startswith("#") else "#808080", "#000000", 0.35)
    return put_mark(ic, slug, (14, 10, 114, 110), anchor="bottom", body=7, side=side)


def sticker(ic, slug, brand, margin=9):
    """FAITHFUL for a white/black logo: a die-cut sticker - the logo on its brand-colour margin."""
    r = ramp(brand) if logo_tone(slug) != "colour" else LIGHT
    box_ = (20, 18, 108, 100)
    shapes = fit([g for _, g, _ in mark_parts(slug)], box_, anchor="bottom")
    # closed: the margin fills the gaps between the logo's parts - an open gap between two bars
    # read as two dark eyes (Haiku's Mornye test, 2026-11-23)
    st = rounded(unary_union(shapes).buffer(margin + 6, quad_segs=24).buffer(-6, quad_segs=24), 4)
    solid(ic, st, face=face(r), depth=5, side=r[4], layer="sticker")
    return logo(ic, slug, box_, on="brand", anchor="bottom")


# ------------------------------------------------------------------ symbol-sized things
def arrow(ic, slug, brand, direction="up"):
    """a big rounded arrow (up-vote, upload / download, growth) with the logo on its body"""
    r = ramp(brand)
    head = Polygon([(64, 6), (122, 66), (6, 66)])
    stem = box(37, 64, 91, 112)
    g = rounded(unary_union([head, stem]), 7)
    if direction == "down":
        g = affinity.scale(g, 1, -1, origin=(64, 60))
    solid(ic, g, face=face(r), depth=6, side=r[4], layer="arrow")
    y0 = 36 if direction == "up" else 30
    if logo_tone(slug) == "light":
        logo(ic, slug, (40, y0 + 2, 88, y0 + 50), on="brand", body=3, side="#c0bfbc")
    else:
        lab = circ(64, y0 + 27, 29.5)
        label(ic, lab)
        logo(ic, slug, (64 - 19, y0 + 8, 64 + 19, y0 + 46))
    return g


def flame(ic, slug, brand=None):
    """a big flame (a streak, hot, fast, burn) with the logo standing in front of its lower right.
    ALWAYS fire colours (yellow -> orange): a flame in the brand's mint or blue reads as a water drop
    (Haiku's Stride test, 2026-11-23) - `brand` is ignored."""
    r = ramp("#ff9600")

    def shape(cx, base, w, h, lean):
        rr_ = w / 2
        belly = circ(cx, base - rr_, rr_)
        body_ = unary_union([belly, Polygon([(cx - rr_ * 0.92, base - rr_ * 1.1), (cx + lean, base - h), (cx + rr_ * 0.96, base - rr_ * 1.05)])])
        tongue = unary_union([circ(cx - rr_ * 0.55, base - rr_ * 1.25, rr_ * 0.32),
                              Polygon([(cx - rr_ * 0.86, base - rr_ * 1.2), (cx - rr_ * 0.78, base - h * 0.72), (cx - rr_ * 0.22, base - rr_ * 1.3)])])
        return rounded(unary_union([body_, tongue]), 3)
    fl = shape(50, 112, 78, 104, 6)
    solid(ic, fl, face=[(0, _mix(r[0], "#ffd75e", 0.5)), (0.45, r[2]), (1, r[3])], depth=4, side=r[4], layer="flame")
    core = shape(48, 106, 38, 52, 4)
    ic.path(geom_d(core), ic.linear([(0, "#fff4b0"), (1, _mix(r[1], "#ffd75e", 0.5))], 0, 54, 0, 106), layer_id="flame-core")
    return logo_free(ic, slug, (62, 60, 116, 110), margin_colour=r[3] if logo_tone(slug) == "light" else "#ffffff")


def bag(ic, slug, brand, handles=None):
    """a shopping bag (stores, app stores - GNOME Software's own object) with the logo on its label"""
    r = ramp(brand)
    hr = ramp(handles) if handles else STEEL
    cx, base, w = 64, 118, 100
    h = w * 0.85 - 6
    top = base - 6 - h
    hd = unary_union([ellipse(x, top, w * 0.13, h * 0.26).exterior.buffer(3.2).intersection(box(0, 0, 128, top)) for x in (cx - w * 0.2, cx + w * 0.2)])
    solid(ic, hd, face=[(0, hr[1]), (1, hr[3])], depth=2, side=hr[4], layer="bag-handles")
    g = poly([(cx - w * 0.44, top), (cx + w * 0.44, top), (cx + w / 2, top + h), (cx - w / 2, top + h)], w * 0.05)
    solid(ic, g, face=face(r), depth=6, side=r[4], layer="bag")
    ic.path(geom_d(box(cx - w * 0.44, top, cx + w * 0.44, top + 7).intersection(g)), "#ffffff", opacity=0.25, layer_id="bag-fold")
    if logo_tone(slug) == "light":
        logo(ic, slug, (cx - 28, top + 16, cx + 28, top + h - 10), on="brand")
    else:
        label(ic, rounded(box(cx - 30, top + 14, cx + 30, top + h - 7), 6))
        logo(ic, slug, (cx - 25, top + 19, cx + 25, top + h - 12))
    return g


def envelope(ic, slug, brand):
    """a sent message / request / mail: an envelope in the brand colour, the logo on its stamp"""
    r = ramp(brand)
    env = rounded(box(8, 28, 120, 108), 7)
    solid(ic, env, face=face(r), depth=4, side=r[4], layer="envelope")
    ic.path(geom_d(rounded(Polygon([(10, 30), (118, 30), (64, 72)]), 3)), ic.linear([(0, _mix(r[0], "#ffffff", 0.4)), (1, r[1])], 0, 30, 0, 72), layer_id="flap")
    for a, b in (((12, 104), (52, 70)), ((116, 104), (76, 70))):
        ic.path(geom_d(LineString([a, b]).buffer(1)), "#000000", opacity=0.12, layer_id=f"fold-{a[0]}")
    solid(ic, rounded(box(62, 40, 114, 104), 2.5), face=[(0, "#ffffff"), (1, "#deddda")], depth=1.5, side="#9a9996", layer="stamp")
    if logo_tone(slug) == "light":
        recess(ic, rounded(box(66, 44, 110, 100), 2), [(0, r[1]), (1, r[3])], wall=1.5, layer="stamp-print")
        logo(ic, slug, (69, 48, 107, 96), on="brand")
    else:
        logo(ic, slug, (68, 46, 108, 98))
    return env


def wallet(ic, slug, coin=GOLD, body=DARK, extra="#e0323f"):
    """money, payments, crypto: a wallet with a coin carrying the logo (and a second coin) sticking out"""
    cr = ramp(coin)
    if extra:
        er = ramp(extra)
        solid(ic, circ(92, 42, 19), face=face(er), depth=4, side=er[4], layer="coin-2")
    solid(ic, circ(50, 39, 33), face=[(0, cr[0]), (0.5, cr[2]), (1, cr[3])], depth=5, side=cr[4], layer="coin")
    ic.path(geom_d(circ(50, 39, 33).difference(circ(50, 39, 29))), cr[3], opacity=0.55, layer_id="coin-rim")
    put_mark(ic, slug, (32, 21, 68, 57), face=cr[4])
    br = ramp(body)
    w = rounded(box(10, 62, 118, 116), 12)
    solid(ic, w, face=[(0, br[0]), (0.5, br[1]), (1, br[3])], depth=5, side=br[4], layer="wallet")
    fl = rounded(box(70, 76, 124, 106), 10).intersection(box(0, 0, 118, 128))
    solid(ic, rounded(fl, 1), face=[(0, br[0]), (1, br[2])], depth=2, side=br[4], layer="flap")
    solid(ic, circ(84, 91, 5.5), face=[(0, cr[0]), (1, cr[3])], depth=1.5, side=cr[4], layer="snap")
    return w


def chip(ic, slug, lid):
    """the phone's processor (performance, root, kernel, benchmark): an SoC chip, gold pins, the logo on its lid"""
    pins = []
    for t in (38, 64, 90):
        pins += [box(t - 6, 10, t + 6, 24), box(t - 6, 104, t + 6, 118), box(10, t - 6, 24, t + 6), box(104, t - 6, 118, t + 6)]
    solid(ic, unary_union(pins), face=[(0, GOLD[1]), (1, GOLD[2])], depth=1.5, side=GOLD[3], layer="pins")
    solid(ic, rounded(box(18, 18, 110, 110), 8), face=[(0, DARK[1]), (1, DARK[2])], depth=5, side=DARK[3], layer="chip")
    tone = logo_tone(slug)
    lr = ramp(lid) if tone == "light" else LIGHT
    solid(ic, rounded(box(26, 26, 102, 102), 7), face=face(lr), depth=2, side=lr[4], layer="lid")
    return logo(ic, slug, (34, 34, 94, 94), on="brand")


def phone(ic, slug, brand):
    """the app open on a phone ("Update all", "Install", a big button): the logo and a brand pill"""
    r = ramp(brand)
    solid(ic, rounded(box(28, 8, 100, 118), 12), face=[(0, DARK[1]), (1, DARK[2])], depth=4, side=DARK[3], layer="phone")
    recess(ic, rounded(box(33, 15, 95, 108), 7), [(0, "#ffffff"), (1, "#f2f2f2")], wall=2, layer="screen")
    if logo_tone(slug) == "light":
        solid(ic, rounded(box(38, 20, 90, 74), 10), face=face(r), depth=1.5, side=r[4], layer="app-tile")
        logo(ic, slug, (42, 24, 86, 70), on="brand")
    else:
        logo(ic, slug, (40, 22, 88, 72))
    solid(ic, rounded(box(38, 80, 90, 98), 8.5), face=[(0, r[1]), (1, r[3])], depth=2, side=r[4], layer="button")
    ic.path(geom_d(unary_union([box(61, 82.5, 67, 90), Polygon([(56, 89), (72, 89), (64, 96)])])), "#ffffff", layer_id="button-arrow")


def shield(ic, slug, brand):
    """protection, checks, privacy: a shield with a brand rim, the logo on its face"""
    r = ramp(brand)
    sh = rounded(unary_union([box(16, 8, 112, 58), Polygon([(16, 56), (112, 56), (64, 118)])]).buffer(0), 12)
    solid(ic, sh, face=face(r), depth=5, side=r[4], layer="shield-rim")
    inner = sh.buffer(-6)
    if logo_tone(slug) == "light":
        ic.path(geom_d(inner), ic.linear([(0, r[3]), (1, r[4])], 0, 8, 0, 118), layer_id="shield-face")
        logo(ic, slug, (38, 20, 90, 84), on="brand")
    else:
        ic.path(geom_d(inner), ic.linear([(0, "#ffffff"), (1, "#e8e6e3")], 0, 8, 0, 118), layer_id="shield-face")
        logo(ic, slug, (40, 20, 88, 84))
    return sh


def bubble(ic, slug, brand):
    """comments, chat, conversation, support: a solid speech bubble with the logo"""
    r = ramp(brand)
    g = rounded(unary_union([rounded(box(10, 14, 118, 96), 26), Polygon([(28, 86), (18, 116), (54, 90)])]), 3)
    if logo_tone(slug) == "light":
        solid(ic, g, face=face(r), depth=5, side=r[4], layer="bubble")
        logo(ic, slug, (32, 22, 96, 86), on="brand", body=3, side="#c0bfbc")
    else:
        solid(ic, g, face=[(0, "#ffffff"), (1, "#eeeeec")], depth=5, side=r[3], layer="bubble")
        ic.path(geom_d(g.difference(g.buffer(-3))), r[2], layer_id="bubble-rim")
        logo(ic, slug, (34, 24, 94, 86))
    return g


# ------------------------------------------------------------------ round things (Disc)
def lens(ic, slug, glass):
    """search, find, look closer: a magnifier - steel rim, handle, the logo seen through the glass"""
    cx, cy, R = 56, 56, 46
    solid(ic, LineString([(cx + R * 0.62, cy + R * 0.62), (108, 108)]).buffer(8, cap_style=1), face=[(0, DARK[1]), (1, DARK[2])], depth=4, side=DARK[3], layer="handle")
    solid(ic, circ(cx, cy, R), face=[(0, "#ffffff"), (0.5, "#deddda"), (1, "#9a9996")], depth=5, side="#77767b", layer="rim")
    g = ramp(glass) if logo_tone(slug) == "light" else ("#ffffff", "#eef5fd", "#dbe8f8", "#c3d6ee", "#a8c2e2")
    recess(ic, circ(cx, cy, R - 7), [(0, g[1]), (1, g[3])], wall=3, layer="glass")
    logo(ic, slug, (cx - 27, cy - 25, cx + 27, cy + 27), on="brand")
    ic.path(geom_d(circ(cx, cy, R - 7).difference(circ(cx + 6, cy + 6, R - 7))), "#ffffff", opacity=0.22, layer_id="glint")


def dial(ic, slug, arc, percent=0.75):
    """progress, health, score, battery %: a round dial - steel rim, light face, the arc, the logo"""
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, DARK[1]), (1, DARK[2])], depth=5, side=DARK[3], layer="rim")
    recess(ic, circ(cx, cy, R - 6), [(0, "#ffffff"), (1, "#deddda")], wall=3, layer="face")
    ic.path(geom_d(circ(cx, cy, R - 11).difference(circ(cx, cy, R - 21))), "#c0bfbc", layer_id="track")
    a1 = -90 + 360 * percent
    r = ramp(arc)
    line = LineString([(cx + (R - 16) * math.cos(math.radians(a)), cy + (R - 16) * math.sin(math.radians(a))) for a in range(-90, int(a1) + 1, 3)])
    ic.path(geom_d(line.buffer(5, cap_style=1)), ic.linear([(0, r[0]), (1, r[3])], cx, cy - R, cx, cy + R), layer_id="arc")
    if logo_tone(slug) == "light":
        solid(ic, circ(cx, cy, 29), face=face(r), depth=2, side=r[4], layer="centre")
    logo(ic, slug, (cx - 19, cy - 19, cx + 19, cy + 19), on="brand")


def radar(ic, slug, ring):
    """nearby, scan, find devices, signal: a round radar - dark screen, rings, a sweep, the logo on a light hub"""
    r = ramp(ring)
    cx, cy, R = 64, 62, 54
    solid(ic, circ(cx, cy, R), face=[(0, DARK[1]), (1, DARK[2])], depth=5, side=DARK[3], layer="case")
    recess(ic, circ(cx, cy, R - 6), [(0, DARK[2]), (1, DARK[3])], wall=3, layer="screen")
    ic.path(geom_d(circ(cx, cy, 40).exterior.buffer(1.8)), r[1], opacity=0.6, layer_id="ring")
    sweep = Polygon([(cx, cy)] + [(cx + (R - 6) * math.cos(math.radians(a)), cy + (R - 6) * math.sin(math.radians(a))) for a in range(-90, -29, 3)]).difference(circ(cx, cy, 33))
    ic.path(geom_d(sweep), ic.linear([(0, r[1], 0.0), (1, r[1], 0.55)], cx, cy - 40, cx + 40, cy - 20), layer_id="sweep")
    for bx, by in ((96, 38), (34, 88)):
        ic.path(geom_d(circ(bx, by, 4.5)), r[0], layer_id=f"blip-{bx}")
    hub = ramp(ring) if logo_tone(slug) == "light" else LIGHT
    solid(ic, circ(cx, cy, 29), face=face(hub), depth=2, side=hub[4], layer="hub")
    logo(ic, slug, (cx - 19, cy - 19, cx + 19, cy + 19), on="brand")


def fan(ic, slug, blades):
    """cooling, temperature, speed, wind: a round fan - housing, blades, the logo on the hub"""
    cx, cy, R = 64, 62, 54
    b = ramp(blades)
    solid(ic, circ(cx, cy, R), face=[(0, "#deddda"), (1, "#9a9996")], depth=5, side="#77767b", layer="housing")
    recess(ic, circ(cx, cy, R - 6), [(0, DARK[2]), (1, DARK[3])], wall=3, layer="duct")
    for k in range(7):
        a0 = k * 360 / 7
        pts = [(cx + (24 + t * 2.3) * math.cos(math.radians(a0 + t * 4.2)), cy + (24 + t * 2.3) * math.sin(math.radians(a0 + t * 4.2))) for t in range(11)]
        pts += [(cx + (24 + t * 2.3) * math.cos(math.radians(a0 + t * 4.2 + 26 - t * 0.6)), cy + (24 + t * 2.3) * math.sin(math.radians(a0 + t * 4.2 + 26 - t * 0.6))) for t in range(10, -1, -1)]
        ic.path(geom_d(rounded(Polygon(pts).buffer(0), 2)), ic.linear([(0, b[0]), (1, b[3])], cx, cy - R, cx, cy + R), layer_id=f"blade-{k}")
    hub = b if logo_tone(slug) == "light" else LIGHT
    solid(ic, circ(cx, cy, 29), face=face(hub), depth=3, side=hub[4], layer="hub")
    logo(ic, slug, (cx - 19, cy - 19, cx + 19, cy + 19), on="brand")


def coin(ic, slug, metal=GOLD):
    """money, tokens, rewards, points: a thick coin with a milled edge, the logo embossed"""
    m = ramp(metal)
    cx, cy, R = 64, 60, 52
    solid(ic, circ(cx, cy, R), face=[(0, m[1]), (0.5, m[2]), (1, m[3])], depth=8, side=m[4], layer="coin")
    teeth = unary_union([LineString([(cx + (R - 1) * math.cos(a), cy + (R - 1) * math.sin(a)), (cx + (R - 5) * math.cos(a), cy + (R - 5) * math.sin(a))]).buffer(1.1)
                         for a in [math.radians(t) for t in range(0, 360, 9)]])
    ic.path(geom_d(teeth), m[3], opacity=0.7, layer_id="milling")
    recess(ic, circ(cx, cy, R - 8), [(0, m[0]), (0.6, m[1]), (1, m[2])], wall=3, layer="face")
    ic.path(geom_d(circ(cx, cy, R - 7).exterior.buffer(1.3)), m[4], layer_id="rim-edge")   # the raised rim's crisp edge
    put_mark(ic, slug, (cx - 28, cy - 28, cx + 28, cy + 28), face=m[4])


def cup(ic, slug):
    """coffee, breaks, cafés, mornings: a cup seen from above on its saucer, the logo in the foam"""
    solid(ic, circ(64, 64, 54), face=[(0, "#ffffff"), (1, "#deddda")], depth=4, side="#9a9996", layer="saucer")
    solid(ic, rounded(box(94, 56, 118, 72), 7), face=[(0, "#ffffff"), (1, "#deddda")], depth=3, side="#9a9996", layer="handle")
    solid(ic, circ(62, 64, 41), face=[(0, "#ffffff"), (1, "#e8e6e3")], depth=4, side="#9a9996", layer="cup")
    recess(ic, circ(62, 64, 34), [(0, "#c8a27a"), (1, "#a77c52")], wall=3, layer="coffee")
    ic.path(geom_d(circ(62, 65, 30)), ic.linear([(0, "#fff7ea"), (1, "#f1dfc6")], 0, 35, 0, 95), layer_id="foam")
    put_mark(ic, slug, (43, 46, 81, 84), face="#865e3c" if logo_tone(slug) == "light" else None)


# ------------------------------------------------------------------ the fourth thing (Rimmed)
def gauge(ic, slug, arc=("#33d17a", "#f6d32d", "#e01b24")):
    """performance, speed, FPS, level: a white gauge, its arc green -> yellow -> red, the needle high"""
    cx, cy = 64, 62
    body = unary_union([circ(cx, cy, 54).intersection(box(0, 0, 128, cy)), rounded(box(10, cy - 10, 118, 116), 12)])
    solid(ic, rounded(body, 4), face=[(0, "#ffffff"), (0.6, "#f2f2f2"), (1, "#c0bfbc")], depth=6, side="#5e5c64", layer="dial")
    for k, col in enumerate(arc):
        seg = LineString([(cx + 41 * math.cos(math.radians(a)), cy + 41 * math.sin(math.radians(a))) for a in range(186 + k * 56, 186 + (k + 1) * 56 + 1, 4)])
        ic.path(geom_d(seg.buffer(6, cap_style=2)), col, layer_id=f"arc-{k}")
    na = math.radians(-38)
    ic.path(geom_d(Polygon([(cx + 36 * math.cos(na), cy + 36 * math.sin(na)), (cx + 4.5 * math.cos(na + math.pi / 2), cy + 4.5 * math.sin(na + math.pi / 2)),
                            (cx + 4.5 * math.cos(na - math.pi / 2), cy + 4.5 * math.sin(na - math.pi / 2))])), "#c01c28", layer_id="needle")
    solid(ic, circ(cx, cy, 6), face=[(0, "#5e5c64"), (1, "#241f31")], depth=1.5, side="#000000", layer="pivot")
    if logo_tone(slug) == "light":
        solid(ic, rounded(box(34, 68, 94, 110), 8), face=face(ramp(arc[0])), depth=1.5, side=ramp(arc[0])[4], layer="badge")
    logo(ic, slug, (37, 72, 91, 106) if logo_tone(slug) == "light" else (37, 69, 91, 108), on="brand")


def monitor(ic, slug, bars=("#0ecb81", "#f6465d", "#0ecb81", "#0ecb81")):
    """trading, charts, stats, dashboards: a screen on its stand - the logo and bold candles/bars"""
    solid(ic, unary_union([Polygon([(56, 92), (72, 92), (76, 108), (52, 108)]), rounded(box(38, 106, 90, 114), 3)]), face=[(0, "#deddda"), (1, "#9a9996")], depth=3, side="#77767b", layer="stand")
    solid(ic, rounded(box(8, 16, 120, 96), 8), face=[(0, "#5e5c64"), (1, "#3d3846")], depth=4, side="#241f31", layer="monitor")
    light = logo_tone(slug) != "light"
    recess(ic, rounded(box(13, 21, 115, 91), 4), [(0, "#ffffff"), (1, "#eeeeec")] if light else [(0, "#2b3139"), (1, "#181a20")], wall=2, layer="screen")
    logo(ic, slug, (17, 27, 59, 85), on="brand")
    for k, ((y0, y1), col) in enumerate(zip(((58, 82), (44, 72), (30, 60)), (bars[0], bars[1], bars[3]))):
        x = 72 + k * 14
        ic.path(geom_d(rounded(box(x - 5, y0, x + 5, y1), 2)), col, layer_id=f"bar-{k}")


def pouch(ic, slug, brand, items=("#3ddc84", "#9a9996", "#f08a24")):
    """packages, archives, files, unpacking: an opened zip pouch, things coming out, the logo on its label"""
    r = ramp(brand)
    for n, (x, y, a, col) in enumerate(((44, 40, -14, items[0]), (66, 34, 4, items[1]), (88, 40, 16, items[2]))):
        blk = affinity.rotate(rounded(box(x - 10, y - 16, x + 10, y + 16), 3), a, origin=(x, y))
        solid(ic, blk, face=[(0, "#ffffff"), (0.25, col), (1, col)], depth=3, layer=f"item-{n}")
    p = rounded(box(10, 46, 118, 114), 14)
    solid(ic, p, face=face(r), depth=6, side=r[4], layer="pouch")
    ic.path(geom_d(box(16, 48, 112, 52.5)), r[4], layer_id="zip-track")
    ic.path(geom_d(unary_union([box(x, 47.5, x + 2.2, 53) for x in range(20, 108, 4)])), "#c0bfbc", layer_id="zip-teeth")
    solid(ic, unary_union([rounded(box(104, 45, 114, 56), 2), rounded(box(106, 55, 112, 68), 2.5)]), face=[(0, "#ffffff"), (1, "#9a9996")], depth=1.5, side="#5e5c64", layer="zip-pull")
    if logo_tone(slug) == "light":
        logo(ic, slug, (36, 60, 92, 108), on="brand")
    else:
        label(ic, rounded(box(34, 60, 94, 108), 6))
        logo(ic, slug, (39, 64, 89, 104))


def book(ic, slug, brand):
    """reading, learning, notes, docs: a closed book - brand cover, page block, ribbon, the logo on a label"""
    r = ramp(brand)
    solid(ic, rounded(box(26, 14, 112, 116), 5), face=[(0, "#ffffff"), (1, "#deddda")], depth=3, side="#9a9996", layer="pages")
    cover = rounded(box(16, 10, 104, 112), 7)
    solid(ic, cover, face=face(r), depth=5, side=r[4], layer="cover")
    ic.path(geom_d(box(16, 10, 26, 112).intersection(cover)), "#000000", opacity=0.15, layer_id="spine")
    solid(ic, Polygon([(80, 108), (90, 108), (90, 124), (85, 119), (80, 124)]).intersection(box(0, 0, 128, 120)), face="#e01b24", depth=1, side="#a51d2d", layer="ribbon")
    if logo_tone(slug) == "light":
        logo(ic, slug, (36, 30, 96, 92), on="brand")
    else:
        label(ic, rounded(box(34, 28, 98, 94), 6))
        logo(ic, slug, (39, 33, 93, 89))


def card(ic, slug, brand):
    """payments, banking, membership: a bank card - brand face, gold chip, the logo"""
    r = ramp(brand)
    g = rounded(box(8, 28, 120, 100), 9)
    solid(ic, g, face=[(0, r[1]), (0.6, r[2]), (1, r[3])], depth=4, side=r[4], layer="card")
    solid(ic, rounded(box(20, 50, 40, 66), 3), face=[(0, GOLD[1]), (1, GOLD[3])], depth=1, side=GOLD[4], layer="chip")
    ic.path(geom_d(box(8, 84, 120, 88).intersection(g)), "#ffffff", opacity=0.25, layer_id="stripe")
    if logo_tone(slug) == "light":
        logo(ic, slug, (56, 36, 112, 80), on="brand")
    else:
        label(ic, rounded(box(54, 36, 112, 80), 6))
        logo(ic, slug, (58, 40, 108, 76))
    return g


KIT = [
    # (function, what it is FOR - pick by the app's own anchor, METHOD §2), style it suits
    ("logo_object", "Faithful: the logo itself (a white/black logo gets a brand sticker margin)", "faithful"),
    ("sticker", "Faithful for a white or black logo: die-cut sticker", "faithful"),
    ("arrow", "up-vote, upload / download, growth, sending", "symbol"),
    ("flame", "a streak, hot, fast, burning, energy", "symbol"),
    ("bag", "a store, an app store, shopping", "symbol"),
    ("envelope", "mail, a request, an invitation, sending", "symbol"),
    ("wallet", "money, payments, crypto, balance", "symbol"),
    ("chip", "processor, performance, root, kernel, hardware - only for a SIMPLE logo (fine pins cost legibility)", "symbol"),
    ("phone", "the app open on the phone: install, update, a big button", "rimmed"),
    ("shield", "protection, a health check, privacy, verified", "rimmed"),
    ("bubble", "comments, chat, conversation, support", "rimmed"),
    ("lens", "search, find, look closer, inspect - ROUND: the Disc only", "disc"),
    ("dial", "progress, a score, health %, battery % - ROUND: the Disc only", "disc"),
    ("radar", "nearby, scan, discover, signal - ROUND: the Disc only", "disc"),
    ("fan", "cooling, temperature, speed, wind - ROUND: the Disc only", "disc"),
    ("coin", "money, tokens, rewards, points - ROUND: the Disc only", "disc"),
    ("cup", "coffee, cafés, breaks, mornings - ROUND: the Disc only", "disc"),
    ("gauge", "performance, speed, FPS, a level", "rimmed"),
    ("monitor", "trading, charts, stats, dashboards", "rimmed"),
    ("pouch", "packages, archives, unpacking, files", "rimmed"),
    ("book", "reading, learning, notes, docs", "rimmed"),
    ("card", "payments, banking, a membership", "rimmed"),
]

__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "sys", "Path")]
