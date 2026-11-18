#!/usr/bin/env python3
"""Two INVENTED apps (no real brand), three versions each:
  1. the flat source logo,
  2. what the old pipeline makes: the logo on a plate with a chin  -> NOT a redesign,
  3. a real GNOME redesign: the idea built as physical objects     -> the target.
Read this file before writing your first redesign.py (references/redesign.md).
    python3 examples/redesign/build_examples.py     (writes the SVGs + examples/redesign/target.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from obj import *  # noqa: F401,F403,E402


# ---------- shared shapes ----------
def cloud(cx, cy, s=1.0):
    return unary_union([circ(cx - 26 * s, cy + 8 * s, 20 * s), circ(cx - 2 * s, cy - 6 * s, 27 * s),
                        circ(cx + 26 * s, cy + 6 * s, 21 * s),
                        rounded(box(cx - 44 * s, cy + 8 * s, cx + 46 * s, cy + 28 * s), 12 * s)])


def arrow(cx, top, w_head, h_head, w_shaft, bottom):
    return poly([(cx, top), (cx + w_head / 2, top + h_head), (cx + w_shaft / 2, top + h_head),
                 (cx + w_shaft / 2, bottom), (cx - w_shaft / 2, bottom), (cx - w_shaft / 2, top + h_head),
                 (cx - w_head / 2, top + h_head)], 3.2)


def shield(cx=64, top=12, w=96, h=104):
    t = np.linspace(0, 1, 40)
    right = [(cx + (w / 2) * (1 - u) ** 1.25 * np.cos(u * np.pi / 2) ** 0.35, top + h * 0.42 + h * 0.58 * u) for u in t]
    left = [(2 * cx - x, y) for x, y in reversed(right)]
    return poly([(cx - w / 2, top), (cx + w / 2, top)] + right + left[1:], 9)


def keyhole(cx, cy, s=1.0):
    return unary_union([circ(cx, cy, 9 * s),
                        poly([(cx - 4.5 * s, cy + 2 * s), (cx + 4.5 * s, cy + 2 * s),
                              (cx + 7.5 * s, cy + 24 * s), (cx - 7.5 * s, cy + 24 * s)], 1.5 * s)])


# ---------- 1 + 2: flat source and logo-on-plate (what NOT to ship) ----------
def flat_source(name, tile, mark):
    ic = gk.Icon(f"{name} - flat source logo (invented)")
    ic.path(gk.rrect_d(4, 4, 120, 120, 28), tile)
    ic.path(geom_d(mark), "#ffffff", fill_rule="evenodd")
    return ic


def logo_on_plate(name, tile, mark):
    ic = gk.Icon(f"{name} - logo on a plate: NOT a redesign")
    ic.plate("square", face=tile)
    ic.glyph(geom_d(scale(mark, 0.86, (64, 66))), fill="#ffffff", lift=2, fill_rule="evenodd")
    return ic


# ---------- 3: the redesigns ----------
def bulut_gnome():
    """Concept L2 (metaphor): a soft volumetric cloud (like GNOME Weather) with a solid
    blue arrow standing IN FRONT of it. Two objects, real thickness, light from the top."""
    ic = gk.Icon("Bulut Yedek - GNOME redesign")
    c = cloud(64, 46)
    solid(ic, c, face=[(0, "#ffffff"), (0.55, "#f6f9fe"), (1, "#dce8f8")], side="#c6d7ee", depth=6,
          top=False, layer="cloud")
    glow = circ(58, 34, 18).intersection(c)                      # soft top light, not a line
    ic.path(geom_d(glow), ic.radial([(0, "#ffffff", 1), (1, "#ffffff", 0)], 58, 34, 18), layer_id="cloud-glow")
    a = arrow(64, 54, 50, 26, 20, 112)                            # secondary object, in front
    solid(ic, a, face=[(0, "#62a0ea"), (0.45, "#3584e4"), (1, "#2a74d6")], side="#1c71d8", depth=5,
          layer="arrow")
    return ic


def kasa_gnome():
    """Concept L1 (the mark becomes an object): a steel shield with real thickness, a
    recessed green enamel inlay and a keyhole that is a real hole."""
    ic = gk.Icon("Kasa - GNOME redesign")
    sh = shield()
    x0, _, x1, _ = sh.bounds
    ic.path(geom_d(side_of(sh, 6)), ic.linear([(0, "#9a9996"), (0.12, "#c0bfbc"), (0.5, "#deddda"),
                                                (0.88, "#c0bfbc"), (1, "#9a9996")], x0, 0, x1, 0),
            layer_id="steel-side")                               # steel side: lighter in the middle
    ic.path(geom_d(sh), ic.linear([(0, "#ffffff"), (0.35, "#f6f5f4"), (1, "#deddda")], 0, sh.bounds[1], 0, sh.bounds[3]),
            layer_id="steel-face")
    toplight(ic, sh, opacity=1.0, layer="steel")
    inner = sh.buffer(-9, quad_segs=24)
    recess(ic, inner, [(0, "#57e389"), (0.5, "#33d17a"), (1, "#26a269")], wall=3, layer="enamel")
    kh = keyhole(64, 50, 1.25)
    ic.path(geom_d(kh.buffer(1.2)), "#1f7a4c", opacity=0.55, layer_id="keyhole-bevel")
    hole(ic, kh, layer="keyhole")
    return ic


def main():
    out = {}
    bul_mark = cloud(64, 58, 0.92).difference(arrow(64, 48, 30, 17, 11, 84))
    kas_mark = move(scale(shield(), 0.62), 0, 2).difference(keyhole(64, 52, 0.75))
    out["bulut-1-source"] = flat_source("Bulut Yedek", "#2b7de9", bul_mark)
    out["bulut-2-plate"] = logo_on_plate("Bulut Yedek", "#2b7de9", bul_mark)
    out["bulut-3-redesign"] = bulut_gnome()
    out["kasa-1-source"] = flat_source("Kasa", "#2ec27e", kas_mark)
    out["kasa-2-plate"] = logo_on_plate("Kasa", "#2ec27e", kas_mark)
    out["kasa-3-redesign"] = kasa_gnome()
    for k, ic in out.items():
        ic.save(HERE / f"{k}.svg")
    board()


def board():
    from PIL import Image, ImageDraw
    from _common import render_svg, load_font
    C, P = 230, 20
    cols = [("1 · source logo", (119, 118, 123)), ("2 · on a plate: WRONG", (192, 28, 40)),
            ("3 · object: TARGET", (38, 135, 90))]
    f_t, f_h, f_s = load_font(28), load_font(19), load_font(16)
    W = P + 3 * (C + P) + 3 * 60 + 2 * P
    img = Image.new("RGBA", (W, 92 + 2 * (C + 56) + 40), (250, 250, 249, 255))
    d = ImageDraw.Draw(img)
    d.text((P, 14), "What a GNOME redesign is", font=f_t, fill=(36, 31, 49))
    for i, (t, c) in enumerate(cols):
        d.text((P + i * (C + P), 56), t, font=f_h, fill=c)
    d.text((P + 3 * (C + P) + 6, 56), "48 / 32 px", font=f_h, fill=(119, 118, 123))
    y = 92
    for app in ("bulut", "kasa"):
        for i, v in enumerate(("1-source", "2-plate", "3-redesign")):
            im = render_svg(str(HERE / f"{app}-{v}.svg"), C)
            img.alpha_composite(im, (P + i * (C + P), y))
            img.alpha_composite(render_svg(str(HERE / f"{app}-{v}.svg"), 48), (P + 3 * (C + P) + i * 60, y + 60))
            img.alpha_composite(render_svg(str(HERE / f"{app}-{v}.svg"), 32), (P + 3 * (C + P) + i * 60 + 8, y + 130))
        y += C + 56
    d.text((P, y - 30), "Invented apps. Code: examples/redesign/build_examples.py", font=f_s, fill=(119, 118, 123))
    img.save(HERE / "target.png")
    print("wrote", HERE / "target.png")


if __name__ == "__main__":
    main()
