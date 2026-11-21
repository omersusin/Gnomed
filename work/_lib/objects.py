"""Ready GNOME objects for Gnomed redesigns - compose these instead of drawing from scratch.

    import sys; sys.path.insert(0, "work/_lib")
    from objects import *            # also gives everything from obj.py (gk, solid, circ ...)
    ic = gk.Icon("My app")
    shield(ic, 64, 118, 90, ramp=RAMP["Blue"])     # stands on the baseline y=118, 90 wide
    coin(ic, 96, 118, 34, ramp=RAMP["Yellow"])     # secondary object, lower right
    ic.save("work/<slug>/concepts/A.svg")

THE CONVENTION (every function):
    f(ic, cx, base, size, ramp=..., name=...) -> the object's shapely outline
    cx    = horizontal centre (0..128)
    base  = the object's BOTTOM edge INCLUDING its side/thickness (use 118 = the baseline)
    size  = the object's WIDTH (its larger side for tall objects is said in the docstring)
    ramp  = a 5-colour GNOME HIG ramp: RAMP["Blue"], RAMP["Green"] ... (1 = lightest)
Every object has thickness (a side), light from the top and HIG colours, so it passes
REDESIGN.md 5. Catalogue with pictures: docs/redesign/objects.png; as text:
docs/redesign/OBJECTS.md (regenerate both: python3 docs/redesign/make_objects_sheet.py).

Brand marks are NOT here: an app's own mark always comes from parts(slug) / body(slug).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from obj import *  # noqa: F401,F403,E402
from shapely import affinity  # noqa: E402
from shapely.geometry import LineString  # noqa: E402

RAMP = {
    "Blue": ("#99c1f1", "#62a0ea", "#3584e4", "#1c71d8", "#1a5fb4"),
    "Green": ("#8ff0a4", "#57e389", "#33d17a", "#2ec27e", "#26a269"),
    "Yellow": ("#f9f06b", "#f8e45c", "#f6d32d", "#f5c211", "#e5a50a"),
    "Orange": ("#ffbe6f", "#ffa348", "#ff7800", "#e66100", "#c64600"),
    "Red": ("#f66151", "#ed333b", "#e01b24", "#c01c28", "#a51d2d"),
    "Purple": ("#dc8add", "#c061cb", "#9141ac", "#813d9c", "#613583"),
    "Brown": ("#cdab8f", "#b5835a", "#986a44", "#865e3c", "#63452c"),
    "Light": ("#ffffff", "#f6f5f4", "#deddda", "#c0bfbc", "#9a9996"),
    "Dark": ("#77767b", "#5e5c64", "#3d3846", "#241f31", "#241f31"),
}
DARK = "#3d3846"


def _face(r):
    """top light / face / shadow stops of a ramp (REDESIGN 5: 3 steps of one ramp)."""
    return [(0, r[0]), (0.5, r[1]), (1, r[3])]


def _star(cx, cy, r_out, r_in, n=5):
    pts = []
    for k in range(2 * n):
        a = -math.pi / 2 + k * math.pi / n
        r = r_out if k % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ====================================================================== everyday objects
def speech_bubble(ic, cx, base, size, ramp=RAMP["Green"], name="bubble"):
    """Rounded chat bubble with a tail at the lower left. Height ~0.8 * size."""
    w, h, d = size, size * 0.70, max(4, size * 0.06)
    top = base - d - size * 0.80
    b = rounded(box(cx - w / 2, top, cx + w / 2, top + h), h * 0.32)
    tail = poly([(cx - w * 0.30, top + h - 2), (cx - w * 0.42, base - d), (cx - w * 0.08, top + h - 2)], 2)
    g = unary_union([b, tail])
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    return g


def shield(ic, cx, base, size, ramp=RAMP["Blue"], name="shield"):
    """Heraldic shield (security, VPN, password apps). Height ~1.15 * size."""
    w, d = size, max(4, size * 0.06)
    h = size * 1.15 - d
    top = base - d - h
    g = poly([(cx - w / 2, top), (cx + w / 2, top), (cx + w / 2, top + h * 0.45),
              (cx, top + h), (cx - w / 2, top + h * 0.45)], size * 0.10)
    g = move(g, 0, (base - d) - g.bounds[3])          # the rounded point still stands on the baseline
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    half = g.intersection(box(cx, 0, 128, 128))
    ic.path(geom_d(half), "#ffffff", opacity=0.18, layer_id=f"{name}-light-half")
    return g


def card(ic, cx, base, size, ramp=RAMP["Blue"], name="card"):
    """Bank / ID card seen from the front: chip + stripe. Height ~0.63 * size."""
    w, d = size, max(3, size * 0.04)
    h = size * 0.63 - d
    top = base - d - h
    g = rounded(box(cx - w / 2, top, cx + w / 2, top + h), size * 0.07)
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    chip = rounded(box(cx - w * 0.38, top + h * 0.30, cx - w * 0.18, top + h * 0.58), 2)
    solid(ic, chip, face=[(0, "#f9f06b"), (1, "#e5a50a")], depth=1, side="#c64600", top=False, layer=f"{name}-chip")
    for k in range(3):
        ic.path(geom_d(rounded(box(cx - w * 0.38 + k * w * 0.16, top + h * 0.75, cx - w * 0.25 + k * w * 0.16, top + h * 0.82), 1)),
                "#ffffff", opacity=0.7, layer_id=f"{name}-digits{k}")
    return g


def coin(ic, cx, base, size, ramp=RAMP["Yellow"], name="coin"):
    """Coin standing on its edge, seen from the front (round face, thick rim)."""
    d = max(3, size * 0.10)
    r = (size) / 2
    cy = base - d - r
    g = circ(cx, cy, r)
    solid(ic, g, face=[(0, ramp[0]), (0.5, ramp[2]), (1, ramp[4])], depth=d, side="#c64600" if ramp is RAMP["Yellow"] else ramp[4], layer=name)
    inner = circ(cx, cy, r * 0.72)
    recess(ic, inner, [(0, ramp[3]), (1, ramp[1])], wall=max(1.2, r * 0.08), layer=f"{name}-inner")
    return g


def gear(ic, cx, base, size, ramp=RAMP["Light"], teeth=8, name="gear"):
    """Metal cog with a REAL hole in the middle (settings, tools)."""
    d = max(3, size * 0.07)
    r = size / 2
    cy = base - d - r
    body_ = circ(cx, cy, r * 0.78)
    tooth = [affinity.translate(affinity.rotate(box(-r * 0.14, -r, r * 0.14, 0), 360 * k / teeth, origin=(0, 0)), cx, cy)
             for k in range(teeth)]
    g = unary_union([body_] + tooth).buffer(0.8).buffer(-0.8).difference(circ(cx, cy, r * 0.30))
    solid(ic, g, face=[(0, ramp[0]), (0.5, ramp[2]), (1, ramp[4])], depth=d, side=RAMP["Dark"][0], layer=name)
    return g


def folder(ic, cx, base, size, ramp=RAMP["Blue"], name="folder"):
    """File folder (back sheet with tab + front flap). Height ~0.8 * size."""
    w, d = size, max(4, size * 0.05)
    h = size * 0.80 - d
    top = base - d - h
    back = unary_union([rounded(box(cx - w / 2, top + h * 0.10, cx + w / 2, top + h), 5),
                        rounded(box(cx - w / 2, top, cx - w * 0.08, top + h * 0.3), 5)])
    solid(ic, back, face=[(0, ramp[2]), (1, ramp[4])], depth=0, top=False, layer=f"{name}-back")
    paper = rounded(box(cx - w * 0.42, top + h * 0.12, cx + w * 0.42, top + h * 0.6), 2)
    solid(ic, paper, face=[(0, "#ffffff"), (1, "#deddda")], depth=0, top=False, layer=f"{name}-paper")
    front = rounded(box(cx - w / 2, top + h * 0.30, cx + w / 2, top + h), 5)
    solid(ic, front, face=_face(ramp), depth=d, side=ramp[4], layer=f"{name}-front")
    return unary_union([back, front])


def camera_lens(ic, cx, base, size, ramp=RAMP["Dark"], name="lens"):
    """Round lens barrel with glass (camera, scanner, Snapshot-like). Glass has rings."""
    d = max(4, size * 0.08)
    r = size / 2
    cy = base - d - r
    g = circ(cx, cy, r)
    solid(ic, g, face=[(0, RAMP["Light"][2]), (1, RAMP["Light"][4])], depth=d, side=RAMP["Dark"][1], layer=f"{name}-barrel")
    glass = circ(cx, cy, r * 0.74)
    hole(ic, glass, color=("#241f31", "#3d3846"), wall=r * 0.08, layer=f"{name}-glass")
    ic.path(geom_d(circ(cx, cy, r * 0.48)), ic.radial([(0, "#99c1f1"), (0.6, "#3584e4"), (1, "#241f31")], cx, cy, r * 0.48),
            layer_id=f"{name}-iris")
    ic.path(geom_d(ellipse(cx - r * 0.22, cy - r * 0.25, r * 0.16, r * 0.10)), "#ffffff", opacity=0.85, layer_id=f"{name}-glint")
    return g


def play_button(ic, cx, base, size, ramp=RAMP["Red"], name="play"):
    """Rounded rectangle with a white play triangle (video, media)."""
    w, d = size, max(4, size * 0.06)
    h = size * 0.70 - d
    top = base - d - h
    g = rounded(box(cx - w / 2, top, cx + w / 2, top + h), h * 0.28)
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    tri = poly([(cx - w * 0.12, top + h * 0.28), (cx + w * 0.18, top + h * 0.5), (cx - w * 0.12, top + h * 0.72)], 2)
    solid(ic, tri, face=[(0, "#ffffff"), (1, "#deddda")], depth=1.5, side="#c0bfbc", top=False, layer=f"{name}-triangle")
    return g


def book(ic, cx, base, size, ramp=RAMP["Red"], name="book"):
    """Closed book standing, cover + page block on the right (reading, docs, learning)."""
    w, d = size, max(6, size * 0.12)
    h = size * 1.15 - 4
    top = base - 4 - h
    pages = box(cx - w / 2 + d, top + 3, cx + w / 2, top + h + 1)
    ic.path(geom_d(pages), ic.linear([(0, "#ffffff"), (1, "#deddda")], cx - w / 2, 0, cx + w / 2, 0), layer_id=f"{name}-pages")
    cover = rounded(box(cx - w / 2, top, cx + w / 2 - d * 0.6, top + h), 4)
    solid(ic, cover, face=_face(ramp), depth=4, side=ramp[4], layer=f"{name}-cover")
    spine = box(cx - w / 2, top, cx - w / 2 + d * 0.6, top + h).intersection(cover)
    ic.path(geom_d(spine), ramp[4], opacity=0.5, layer_id=f"{name}-spine")
    return cover


def music_note(ic, cx, base, size, ramp=RAMP["Purple"], name="note"):
    """Two beamed eighth notes (music apps). size = width; height ~1.1 * size."""
    d = max(3, size * 0.06)
    hr = size * 0.18
    y1 = base - d - hr
    x0, x1 = cx - size * 0.28, cx + size * 0.30
    heads = unary_union([ellipse(x0, y1, hr * 1.2, hr), ellipse(x1, y1 - size * 0.12, hr * 1.2, hr)])
    stems = unary_union([box(x0 + hr * 0.9, y1 - size * 0.82, x0 + hr * 1.2 + 2, y1),
                         box(x1 + hr * 0.9, y1 - size * 0.94, x1 + hr * 1.2 + 2, y1 - size * 0.12)])
    beam = poly([(x0 + hr * 0.9, y1 - size * 0.82), (x1 + hr * 1.2 + 2, y1 - size * 0.94),
                 (x1 + hr * 1.2 + 2, y1 - size * 0.78), (x0 + hr * 0.9, y1 - size * 0.66)], 1)
    g = unary_union([heads, stems, beam])
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    return g


def lock(ic, cx, base, size, ramp=RAMP["Yellow"], name="lock"):
    """Padlock: metal shackle (real hole inside) + body with a keyhole. Height ~1.2 * size."""
    w, d = size, max(5, size * 0.08)
    bh = size * 0.70
    btop = base - d - bh
    shackle = circ(cx, btop, w * 0.34).difference(circ(cx, btop, w * 0.22)).intersection(box(0, 0, 128, btop + 2))
    sh = unary_union([shackle, box(cx - w * 0.34, btop, cx - w * 0.22, btop + 4), box(cx + w * 0.22, btop, cx + w * 0.34, btop + 4)])
    solid(ic, sh, face=[(0, "#deddda"), (0.5, "#ffffff"), (1, "#9a9996")], depth=3, side="#77767b", layer=f"{name}-shackle")
    body_ = rounded(box(cx - w / 2, btop, cx + w / 2, btop + bh), w * 0.10)
    solid(ic, body_, face=_face(ramp), depth=d, side="#c64600" if ramp is RAMP["Yellow"] else ramp[4], layer=f"{name}-body")
    kh = unary_union([circ(cx, btop + bh * 0.42, w * 0.08), box(cx - w * 0.035, btop + bh * 0.42, cx + w * 0.035, btop + bh * 0.72)])
    hole(ic, kh, wall=1.5, layer=f"{name}-keyhole")
    return unary_union([sh, body_])


def key(ic, cx, base, size, ramp=RAMP["Yellow"], name="key"):
    """Key lying flat, bow on the left with a real hole, bit on the right. Height ~0.4 * size."""
    d = max(3, size * 0.05)
    r = size * 0.20
    cy = base - d - r
    x0 = cx - size / 2 + r
    bow = circ(x0, cy, r).difference(circ(x0, cy, r * 0.45))
    shaft = box(x0 + r * 0.8, cy - r * 0.22, cx + size / 2, cy + r * 0.22)
    bit = unary_union([box(cx + size * 0.25, cy, cx + size * 0.32, cy + r * 0.8), box(cx + size * 0.38, cy, cx + size * 0.45, cy + r * 0.6)])
    g = unary_union([bow, shaft, bit])
    solid(ic, g, face=_face(ramp), depth=d, side="#c64600" if ramp is RAMP["Yellow"] else ramp[4], layer=name)
    return g


def phone_handset(ic, cx, base, size, ramp=RAMP["Green"], name="handset"):
    """Classic phone handset lying diagonally: a curved handle, an ear cup at the top left and
    a mouth cup at the bottom right, both turned inwards (calls). About size x size."""
    d = max(4, size * 0.07)
    s = size / 100
    ox, oy = cx - 50 * s, base - d - 100 * s
    P = lambda x, y: (ox + x * s, oy + y * s)  # noqa: E731
    ccx, ccy, R = 88, 12, 70                     # centre of the handle's curve (upper right)
    angs = [math.radians(a) for a in range(108, 163, 3)]
    handle = LineString([P(ccx + R * math.cos(a), ccy + R * math.sin(a)) for a in angs]).buffer(11 * s, cap_style=1)
    cups = []
    for a in (angs[0], angs[-1]):
        ex, ey = ccx + R * math.cos(a), ccy + R * math.sin(a)
        nx, ny = -math.cos(a), -math.sin(a)      # towards the centre (the cups face inwards)
        c = rounded(box(-17, -9, 17, 9), 7)
        c = affinity.rotate(c, math.degrees(a) + 90, origin=(0, 0))
        c = affinity.scale(affinity.translate(c, ex + nx * 9, ey + ny * 9), s, s, origin=(0, 0))
        cups.append(affinity.translate(c, ox, oy))
    g = unary_union([handle] + cups).buffer(1.5 * s).buffer(-1.5 * s)
    (g,) = fit([g], (cx - size / 2, base - d - size, cx + size / 2, base - d), anchor="bottom")
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    return g


def globe(ic, cx, base, size, ramp=RAMP["Blue"], name="globe"):
    """Glass globe with meridians and a parallel (web, language, maps)."""
    d = max(2, size * 0.04)
    r = size / 2
    cy = base - d - r
    g = circ(cx, cy, r)
    solid(ic, g, face=[(0, ramp[0]), (0.5, ramp[2]), (1, ramp[4])], depth=d, side=ramp[4], layer=name)
    lines = unary_union([ellipse(cx, cy, r * 0.45, r).exterior.buffer(0.9), LineString([(cx, cy - r), (cx, cy + r)]).buffer(0.9),
                         LineString([(cx - r, cy), (cx + r, cy)]).buffer(0.9),
                         ellipse(cx, cy - r * 0.45, r * 0.85, r * 0.12).exterior.buffer(0.7)]).intersection(g)
    ic.path(geom_d(lines), "#ffffff", opacity=0.55, layer_id=f"{name}-lines")
    ic.path(geom_d(ellipse(cx - r * 0.35, cy - r * 0.45, r * 0.28, r * 0.16)), "#ffffff", opacity=0.8, layer_id=f"{name}-glint")
    return g


def battery(ic, cx, base, size, ramp=RAMP["Green"], level=0.7, name="battery"):
    """Upright battery with a charge level. size = width; height ~1.6 * size."""
    w, d = size, max(4, size * 0.08)
    h = size * 1.6 - d
    top = base - d - h
    cap = rounded(box(cx - w * 0.2, top, cx + w * 0.2, top + h * 0.10), 2)
    solid(ic, cap, face=[(0, "#deddda"), (1, "#9a9996")], depth=2, side="#77767b", layer=f"{name}-cap")
    shell = rounded(box(cx - w / 2, top + h * 0.08, cx + w / 2, top + h), w * 0.16)
    solid(ic, shell, face=[(0, "#f6f5f4"), (1, "#c0bfbc")], depth=d, side="#9a9996", layer=f"{name}-shell")
    inner_top = top + h * 0.16 + (1 - level) * h * 0.76
    fill = rounded(box(cx - w * 0.36, inner_top, cx + w * 0.36, top + h * 0.92), w * 0.08)
    recess(ic, fill, _face(ramp), wall=2, layer=f"{name}-charge")
    return shell


def calendar_page(ic, cx, base, size, ramp=RAMP["Red"], name="calendar"):
    """Desk calendar page: coloured header with two rings, white page with a day grid."""
    w, d = size, max(4, size * 0.06)
    h = size * 0.95 - d
    top = base - d - h
    page = rounded(box(cx - w / 2, top, cx + w / 2, top + h), w * 0.10)
    solid(ic, page, face=[(0, "#ffffff"), (1, "#deddda")], depth=d, side="#9a9996", layer=f"{name}-page")
    head = page.intersection(box(0, 0, 128, top + h * 0.28))
    ic.path(geom_d(head), ic.linear(_face(ramp), 0, top, 0, top + h * 0.28), layer_id=f"{name}-head")
    for x in (cx - w * 0.22, cx + w * 0.22):
        solid(ic, rounded(box(x - 2.6, top - 5, x + 2.6, top + 8), 1.8), face=[(0, "#deddda"), (1, "#77767b")], depth=1, top=False,
              layer=f"{name}-ring{int(x)}")
    cells = unary_union([rounded(box(cx - w * 0.36 + i * w * 0.25, top + h * (0.40 + j * 0.19),
                                     cx - w * 0.36 + i * w * 0.25 + w * 0.16, top + h * (0.40 + j * 0.19) + h * 0.12), 1.5)
                         for i in range(3) for j in range(3)])
    ic.path(geom_d(cells), "#c0bfbc", layer_id=f"{name}-days")
    return page


def envelope(ic, cx, base, size, ramp=RAMP["Blue"], stamp=True, name="envelope"):
    """Letter envelope with a closed flap and an optional white stamp (mail, messengers).
    Height ~0.7 * size. Put the app's mark on the stamp: envelope_stamp(cx, base, size)
    gives the stamp's printable box."""
    w, d = size, max(4, size * 0.055)
    h = size * 0.70 - d
    top = base - d - h
    env = rounded(box(cx - w / 2, top, cx + w / 2, top + h), w * 0.065)
    solid(ic, env, face=[(0, ramp[1]), (1, ramp[2])], depth=d, side=ramp[3], layer=name)
    flap = poly([(cx - w * 0.47, top + 3), (cx + w * 0.47, top + 3), (cx, top + h * 0.55)], 3)
    ic.path(geom_d(move(flap, 0, 2.5).difference(flap).intersection(env)), ramp[4], opacity=0.35, layer_id=f"{name}-flap-shadow")
    solid(ic, flap, face=[(0, ramp[0]), (1, ramp[1])], depth=0, top=False, layer=f"{name}-flap")
    if stamp:
        st = box(cx + w * 0.06, top + h * 0.42, cx + w * 0.42, top + h * 0.92)
        solid(ic, st, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=2, side="#deddda", layer=f"{name}-stamp")
    return env


def envelope_stamp(cx, base, size):
    """(x0, y0, x1, y1) of the printable area on envelope()'s stamp - fit() the mark into it."""
    w, d = size, max(4, size * 0.055)
    h = size * 0.70 - d
    top = base - d - h
    return (cx + w * 0.09, top + h * 0.47, cx + w * 0.39, top + h * 0.87)


def paper_plane(ic, cx, base, size, name="plane"):
    """White folded paper plane flying up-right (send, messages). Height ~0.85 * size.
    Shape measured from Telegram's source (work/telegram/redesign.py)."""
    s = size / 66.2
    f = lambda pts: [(cx - size / 2 + (x - 25.9) * s, base - 3 - (95.0 - y) * s) for x, y in pts]  # noqa: E731
    topw = poly(f([(25.9, 66.1), (90.9, 39.1), (75.7, 52.4), (43.8, 72.2), (28.7, 69.3)]), 1.2)
    bodyp = poly(f([(90.9, 39.1), (92.1, 47.4), (85.4, 89.3), (79.9, 95.0), (54.9, 77.2), (75.7, 52.4)]), 1.2)
    flap = poly(f([(43.8, 72.2), (56.5, 77.0), (50.0, 89.0)]), 1.0)
    solid(ic, flap, face=[(0, "#c0bfbc"), (1, "#9a9996")], depth=2, top=False, layer=f"{name}-fold")
    solid(ic, bodyp, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=3, side="#c0bfbc", layer=f"{name}-body")
    solid(ic, topw, face=[(0, "#ffffff"), (1, "#f6f5f4")], depth=3, side="#deddda", layer=f"{name}-wing")
    return unary_union([topw, bodyp, flap])


def cloud(ic, cx, base, size, ramp=RAMP["Blue"], name="cloud"):
    """Volumetric cloud of three lobes (sync, storage, weather). Height ~0.6 * size."""
    s = size / 94.0
    d = max(4, 6 * s)
    ox, oy = cx - 64 * s, base - d - 86 * s
    T = lambda x, y: (ox + x * s, oy + y * s)  # noqa: E731
    g = unary_union([circ(*T(38, 60), 21 * s), circ(*T(62, 44), 29 * s), circ(*T(89, 56), 22 * s),
                     rounded(box(*T(17, 56), *T(111, 86)), 14 * s)])
    solid(ic, g, face=[(0, ramp[0]), (0.45, ramp[1]), (1, ramp[2])], depth=d, side=ramp[3], top=False, layer=name)
    toplight(ic, g, width=1.5, opacity=0.6, layer=name)
    return g


def browser_window(ic, cx, base, size, ramp=RAMP["Blue"], name="window"):
    """Browser window: enamel body, three title-bar dots, a recessed page (put the mark on
    the page: browser_page(cx, base, size) gives its box). Height ~0.9 * size."""
    w, d = size, max(4, size * 0.055)
    h = size * 0.88 - d
    top = base - d - h
    win = rounded(box(cx - w / 2, top, cx + w / 2, top + h), w * 0.10)
    solid(ic, win, face=[(0, ramp[1]), (0.5, ramp[2]), (1, ramp[4])], depth=d, side=ramp[4], layer=name)
    for i in range(3):
        x = cx - w / 2 + w * (0.10 + 0.08 * i)
        solid(ic, circ(x, top + h * 0.10, w * 0.025), face="#ffffff", depth=0.8, side=ramp[0], top=False, layer=f"{name}-dot{i}")
    page = rounded(box(cx - w / 2 + w * 0.06, top + h * 0.20, cx + w / 2 - w * 0.06, top + h * 0.94), w * 0.05)
    recess(ic, page, [(0, ramp[0]), (1, ramp[1])], wall=3, layer=f"{name}-page")
    return win


def browser_page(cx, base, size):
    """(x0, y0, x1, y1) of browser_window()'s page - fit() the mark into it (anchor="bottom")."""
    w, d = size, max(4, size * 0.055)
    h = size * 0.88 - d
    top = base - d - h
    return (cx - w / 2 + w * 0.14, top + h * 0.26, cx + w / 2 - w * 0.14, top + h * 0.90)


# ====================================================================== game objects
def goal_ring(ic, cx, base, size, ramp=RAMP["Yellow"], inner_wall=False, name="ring"):
    """Thick gold torus on a metal post and a round pad (a goal, a target, a prize ring).
    The ring's centre is a real hole. Height ~1.15 * size. (Pokémon UNITE B)"""
    s = size / 98.0
    pad_h = 6 * s
    pad = ellipse(cx, base - 4 - pad_h, 14 * s * 1.6, pad_h)
    solid(ic, pad, face=[(0, "#deddda"), (1, "#c0bfbc")], depth=4, side="#9a9996", top=False, layer=f"{name}-pad")
    rcy = base - 4 - 68 * s
    post = box(cx - 7 * s, rcy + 30 * s, cx + 7 * s, base - 4 - pad_h)
    ic.path(geom_d(post), ic.linear([(0, "#9a9996"), (0.45, "#f6f5f4"), (1, "#77767b")], cx - 7 * s, 0, cx + 7 * s, 0), layer_id=f"{name}-post")
    rx, ry, w = 49 * s, 42 * s, 14 * s
    outer, hole_ = ellipse(cx, rcy, rx, ry), ellipse(cx, rcy, rx - w, ry - w * 0.8)
    band = outer.difference(hole_)
    solid(ic, band, face=[(0, ramp[0]), (0.35, ramp[2]), (0.75, ramp[4]), (1, "#c64600")], depth=6 * s, side="#c64600", layer=f"{name}-band")
    if inner_wall:
        wall = hole_.difference(move(hole_, 0, w * 0.55))
        ic.path(geom_d(wall), ic.linear([(0, "#1a5fb4"), (1, "#3584e4")], 0, rcy - ry, 0, rcy - ry + w * 1.6), layer_id=f"{name}-inner")
    sheen = ellipse(cx - rx * 0.05, rcy - ry * 0.05, rx - w * 0.35, ry - w * 0.3).difference(
        ellipse(cx + rx * 0.06, rcy + ry * 0.06, rx - w * 0.35, ry - w * 0.3)).intersection(band)
    ic.path(geom_d(sheen), "#ffffff", opacity=0.45, layer_id=f"{name}-sheen")
    return band


def goal_ring_centre(cx, base, size):
    """(x, y) of goal_ring()'s hole centre - put a ball there."""
    return cx, base - 4 - 68 * size / 98.0


def energy_ball(ic, cx, base, size, name="energy"):
    """Glowing glass ball: hot white centre, yellow -> orange edge, swirl, highlight."""
    r = size / 2
    cy = base - 1.5 - r
    o = circ(cx, cy, r)
    solid(ic, o, face="#e5a50a", depth=1.5, side="#c64600", top=False, layer=f"{name}-body")
    ic.path(geom_d(o), ic.radial([(0, "#ffffff"), (0.35, "#f9f06b"), (0.75, "#f6d32d"), (1, "#ff7800")], cx - r * 0.1, cy - r * 0.1, r),
            layer_id=f"{name}-glow")
    swirl = ellipse(cx, cy + r * 0.05, r * 0.95, r * 0.32).difference(ellipse(cx, cy - r * 0.02, r * 0.85, r * 0.24)).intersection(o)
    ic.path(geom_d(swirl), "#ffffff", opacity=0.55, layer_id=f"{name}-swirl")
    ic.path(geom_d(ellipse(cx - r * 0.35, cy - r * 0.45, r * 0.30, r * 0.18)), "#ffffff", opacity=0.9, layer_id=f"{name}-hl")
    return o


def wizard_hat(ic, cx, base, size, ramp=("#b39af5", "#8f6ff0", "#6a4fd6", "#4434ac"), gem=("#f8a5d4", "#e0379c", "#a51d6e"),
               name="hat"):
    """Wizard hat: wide brim curled up at both ends, pointed crown, gold crown band with a
    gem in a diamond setting. size = brim width; height ~1.0 * size. (Rush Royale C)"""
    s = size / 100.0
    t = [i * math.pi / 39 for i in range(40)]
    front = [(cx - 50 * s * math.cos(a), base - 4 * s - 30 * s * math.cos(a) ** 4) for a in t]
    back = [(cx + 42 * s * math.cos(a), base - 24 * s - 8 * s * math.sin(a) - 22 * s * math.cos(a) ** 4) for a in t]
    brim = poly(front + back, 3 * s)
    solid(ic, brim, face=[(0, ramp[0]), (0.45, ramp[1]), (1, ramp[2])], depth=4 * s, side=ramp[3], layer=f"{name}-brim")
    for dd in (-1, 1):
        ic.path(geom_d(ellipse(cx + dd * 46 * s, base - 38 * s, 7 * s, 6 * s).intersection(brim)), ramp[3], opacity=0.55,
                layer_id=f"{name}-curl{dd}")
    ic.path(geom_d(ellipse(cx, base - 17 * s, 30 * s, 6 * s)), ramp[3], opacity=0.35, layer_id=f"{name}-shade")
    cone = poly([(cx - 26 * s, base - 16 * s), (cx - 14 * s, base - 60 * s), (cx + 4 * s, base - 96 * s),
                 (cx + 12 * s, base - 62 * s), (cx + 26 * s, base - 16 * s)], 4 * s).union(ellipse(cx, base - 16 * s, 26 * s, 6 * s))
    ic.path(geom_d(cone), ic.linear([(0, ramp[3]), (0.35, ramp[1]), (0.7, ramp[0]), (1, ramp[2])], cx - 26 * s, 0, cx + 26 * s, 0),
            layer_id=f"{name}-cone")
    toplight(ic, cone, layer=f"{name}-cone")
    band = poly([(cx - 26 * s, base - 18 * s), (cx - 24 * s, base - 34 * s), (cx - 13 * s, base - 30 * s), (cx, base - 44 * s),
                 (cx + 13 * s, base - 30 * s), (cx + 24 * s, base - 34 * s), (cx + 26 * s, base - 18 * s), (cx, base - 12 * s)], 2 * s)
    solid(ic, band, face=[(0, "#f9f06b"), (0.5, "#f6d32d"), (1, "#e5a50a")], depth=2 * s, side="#c64600", layer=f"{name}-band")
    ic.path(geom_d(poly([(cx, base - 40 * s), (cx + 10 * s, base - 27 * s), (cx, base - 15 * s), (cx - 10 * s, base - 27 * s)], 1.5 * s)),
            "#e5a50a", layer_id=f"{name}-setting")
    g = poly([(cx, base - 36 * s), (cx + 7 * s, base - 27 * s), (cx, base - 19 * s), (cx - 7 * s, base - 27 * s)], 1 * s)
    ic.path(geom_d(g), ic.linear([(0, gem[0]), (0.45, gem[1]), (1, gem[2])], 0, base - 36 * s, 0, base - 19 * s), layer_id=f"{name}-gem")
    return brim.union(cone)


def crystal(ic, cx, base, size, name="crystal"):
    """Glowing ice crystal: a rounded diamond of blue glass with a bright facet.
    size = width; height ~1.25 * size."""
    r = size / 2
    cy = base - 2 - r * 1.25
    d = poly([(cx, cy - r * 1.25), (cx + r, cy), (cx, cy + r * 1.25), (cx - r, cy)], r * 0.25)
    dy = (base - 2) - d.bounds[3]                      # the rounded tip stands on the baseline
    d, cy = move(d, 0, dy), cy + dy
    solid(ic, d, face=[(0, "#99c1f1"), (1, "#3584e4")], depth=2, side="#1a5fb4", top=False, layer=f"{name}-body")
    ic.path(geom_d(d), ic.radial([(0, "#ffffff"), (0.45, "#99c1f1", 0.9), (1, "#3584e4", 0.9)], cx, cy - r * 0.2, r * 1.2), layer_id=f"{name}-glow")
    ic.path(geom_d(poly([(cx, cy - r * 0.55), (cx + r * 0.42, cy), (cx, cy + r * 0.55), (cx - r * 0.42, cy)], r * 0.08)), "#ffffff",
            opacity=0.9, layer_id=f"{name}-facet")
    toplight(ic, d, layer=name)
    return d


def football(ic, cx, base, size, name="ball"):
    """Leather match ball: white panels, dark pentagons, gloss (sport games)."""
    r = size / 2
    cy = base - 2.5 - r
    b = circ(cx, cy, r)
    solid(ic, b, face=[(0, "#ffffff"), (0.55, "#f6f5f4"), (1, "#c0bfbc")], depth=2.5, side="#9a9996", top=False, layer=name)
    pents = [poly(_star(cx, cy, r * 0.30, r * 0.30 * 0.81, 5)[::2], 0.5)]
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        pents.append(poly(_star(cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92, r * 0.27, r * 0.22, 5)[::2], 0.5))
    pent = unary_union(pents).intersection(b)
    ic.path(geom_d(pent), ic.linear([(0, "#5e5c64"), (1, "#241f31")], 0, cy - r, 0, cy + r), layer_id=f"{name}-pentagons")
    ic.path(geom_d(ellipse(cx - r * 0.38, cy - r * 0.42, r * 0.34, r * 0.22).intersection(b)), "#ffffff", opacity=0.7, layer_id=f"{name}-gloss")
    return b


def team_ball(ic, cx, base, size, ramp=RAMP["Orange"], name="tball"):
    """Two-colour game ball: coloured top half, white bottom, dark band, white button."""
    r = size / 2
    cy = base - 2.5 - r
    o = circ(cx, cy, r)
    solid(ic, o, face="#c0bfbc", depth=2.5, side="#77767b", top=False, layer=f"{name}-shell")
    ic.path(geom_d(o.intersection(box(0, cy, 128, 128))), ic.linear([(0, "#ffffff"), (1, "#c0bfbc")], 0, cy, 0, cy + r), layer_id=f"{name}-white")
    ic.path(geom_d(o.intersection(box(0, 0, 128, cy))), ic.linear([(0, ramp[0]), (0.5, ramp[1]), (1, ramp[3])], 0, cy - r, 0, cy),
            layer_id=f"{name}-top")
    ic.path(geom_d(o.intersection(box(0, cy - r * 0.08, 128, cy + r * 0.08))), DARK, layer_id=f"{name}-band")
    ic.path(geom_d(circ(cx, cy, r * 0.30)), DARK, layer_id=f"{name}-btnrim")
    ic.path(geom_d(circ(cx, cy, r * 0.20)), "#f6f5f4", layer_id=f"{name}-btn")
    toplight(ic, o, layer=name)
    return o


def die(ic, cx, base, size, ramp=RAMP["Red"], pips=5, name="die"):
    """Solid die seen from the front-top (board games, luck). Like GNOME Tali."""
    d = max(6, size * 0.12)
    top = base - d - size
    g = rounded(box(cx - size / 2, top, cx + size / 2, top + size), size * 0.18)
    solid(ic, g, face=_face(ramp), depth=d, side=ramp[4], layer=name)
    q = size * 0.25
    spots = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
             5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[pips]
    for i, (a, b) in enumerate(spots):
        recess(ic, circ(cx + a * q, top + size / 2 + b * q, size * 0.075), [(0, "#deddda"), (1, "#ffffff")], wall=1.5, layer=f"{name}-pip{i}")
    return g


def board_tiles(ic, cx, base, size, ramp=RAMP["Green"], n=3, m=2, name="board"):
    """Checkered game board with thickness, seen from the front (n x m tiles).
    Height ~size * m / n."""
    d = max(5, size * 0.06)
    h = size * m / n
    top = base - d - h
    g = rounded(box(cx - size / 2, top, cx + size / 2, top + h), 6)
    solid(ic, g, face=ramp[2], depth=d, side=ramp[4], top=False, layer=name)
    tw = size / n
    light = unary_union([box(cx - size / 2 + i * tw, top + j * h / m, cx - size / 2 + (i + 1) * tw, top + (j + 1) * h / m)
                         for i in range(n) for j in range(m) if (i + j) % 2 == 0]).intersection(g)
    ic.path(geom_d(light), ramp[1], layer_id=f"{name}-light")
    toplight(ic, g, layer=name)
    return g


CATALOGUE = [
    # (function, call args for the contact sheet, one-line use)
    ("speech_bubble", dict(ramp=RAMP["Green"]), "chat, messages, comments"),
    ("envelope", dict(ramp=RAMP["Blue"]), "mail, messengers (mark on the stamp)"),
    ("paper_plane", dict(), "send, messages"),
    ("cloud", dict(ramp=RAMP["Blue"]), "sync, storage, weather"),
    ("browser_window", dict(ramp=RAMP["Blue"]), "browsers, web apps (mark on the page)"),
    ("globe", dict(ramp=RAMP["Blue"]), "web, languages, maps"),
    ("shield", dict(ramp=RAMP["Blue"]), "security, VPN, passwords"),
    ("lock", dict(ramp=RAMP["Yellow"]), "security, vaults"),
    ("key", dict(ramp=RAMP["Yellow"]), "passwords, 2FA"),
    ("card", dict(ramp=RAMP["Blue"]), "banks, payments, wallets"),
    ("coin", dict(ramp=RAMP["Yellow"]), "finance, crypto, shops"),
    ("gear", dict(ramp=RAMP["Light"]), "settings, tools, system"),
    ("folder", dict(ramp=RAMP["Blue"]), "files, backup"),
    ("camera_lens", dict(), "camera, scanner, photos"),
    ("play_button", dict(ramp=RAMP["Red"]), "video, media players"),
    ("music_note", dict(ramp=RAMP["Purple"]), "music, audio"),
    ("book", dict(ramp=RAMP["Red"]), "reading, docs, learning"),
    ("phone_handset", dict(ramp=RAMP["Green"]), "calls, dialer"),
    ("battery", dict(ramp=RAMP["Green"]), "power, battery tools"),
    ("calendar_page", dict(ramp=RAMP["Red"]), "calendar, planner"),
    ("goal_ring", dict(), "game: a goal / target ring (Pokémon UNITE)"),
    ("energy_ball", dict(), "game: glowing ball / power orb"),
    ("wizard_hat", dict(), "game: magic, wizards (Rush Royale)"),
    ("crystal", dict(), "game: gems, ice, mana"),
    ("football", dict(), "game: football / sport"),
    ("team_ball", dict(ramp=RAMP["Orange"]), "game: a two-colour team ball"),
    ("die", dict(ramp=RAMP["Red"]), "game: dice, board games"),
    ("board_tiles", dict(ramp=RAMP["Green"]), "game: a board / grid of tiles"),
]

__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "sys", "Path", "affinity")]
