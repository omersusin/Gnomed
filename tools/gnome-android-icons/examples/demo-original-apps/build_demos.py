#!/usr/bin/env python3
"""Worked example: three ORIGINAL, invented apps (no real brand) converted with
gnome_kit into several GNOME/Adwaita alternatives each.

  marti  - messaging app: white speech bubble with a gull cut-out on a coral tile
  lale   - music app: "tulip-note" (tulip head + note stem/flag/head) on a purple disc
  simit  - recipe app with a mascot: a sesame-ring character with face, arms, legs

For each app this writes  <app>-source.svg  (the flat "brand" logo we pretend the
user handed us) and the alternatives.  The identity geometry is defined ONCE
(the SOURCE_* functions) and reused by every alternative - exactly the rule the
skill demands for real apps: never redraw anatomy per variant.

Run:  python3 build_demos.py   (writes into ./svg/)
All artwork in this folder: CC0 (original, made for this skill).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from gnome_kit import (Icon, rrect_d, circle_d, ellipse_d, capsule_d, xform_d,  # noqa: E402
                       translate_d, chin_colors, NEUTRAL)
from _common import shade  # noqa: E402

OUT = HERE / "svg"
CC0 = "original artwork made for the gnome-android-icons skill demo"

# =============================================================== MARTI (messaging)
MARTI = "#ff6b57"          # invented brand coral


def marti_bubble():
    # speech bubble, tail bottom-left; drawn on a 64x52 body centred near (64,60)
    return ("M55 32H73A25 25 0 0 1 98 57A25 25 0 0 1 73 82H58"
            "L42.5 94.2Q36.6 98.6 37.1 91.5L37.3 74.7A25 25 0 0 1 30 57A25 25 0 0 1 55 32Z")


def marti_gull():
    # gull wings: two shallow arcs meeting in a dip; taper to points
    return ("M38 60C44 49 56 46 64 57C72 46 84 49 90 60C83 55 73 56 64 66C55 56 45 55 38 60Z")


def marti_glyph_evenodd(s=1.0, dx=0.0, dy=0.0):
    return xform_d(marti_bubble(), s, dx, dy) + xform_d(marti_gull(), s, dx, dy)


def marti_source():
    ic = Icon("Marti (source logo)", source_note=CC0, license="CC0-1.0")
    ic.path(rrect_d(4, 4, 120, 120, 28), MARTI, "tile")
    ic.path(marti_bubble(), "#ffffff", "bubble")
    ic.path(marti_gull(), MARTI, "gull")
    return ic


def marti_faithful():
    ic = Icon("Marti - Adwaita Faithful", source_note=CC0, license="CC0-1.0")
    ic.plate("square", face=MARTI, r=20)
    ic.glyph(marti_glyph_evenodd(0.92, 0, -2), fill="#ffffff", lift=2, layer="mark", fill_rule="evenodd")
    return ic


def marti_disc():
    ic = Icon("Marti - Sound Disc", source_note=CC0, license="CC0-1.0")
    ic.disc(face=MARTI, top_light=1.0)
    ic.glyph(marti_glyph_evenodd(1.0, 0, -1), fill="#ffffff", lift=2, layer="mark", fill_rule="evenodd")
    return ic


def marti_rimmed():
    ic = Icon("Marti - Rimmed", source_note=CC0, license="CC0-1.0")
    ic.rimmed_disc(inner=MARTI)
    ic.glyph(marti_glyph_evenodd(0.88, 0, -1), fill="#ffffff", lift=2, layer="mark", fill_rule="evenodd")
    return ic


def marti_symbol():
    """No backplate: the bubble is the silhouette (Polari-like), gull inlaid in white."""
    ic = Icon("Marti - Free Symbol", source_note=CC0, license="CC0-1.0")
    b = xform_d(marti_bubble(), 1.5, 3, -2, about=(64, 64))
    g = xform_d(marti_gull(), 1.5, 3, -2, about=(64, 64))
    ic.slab(b, MARTI, (12, 116), corner_r=34, depth=4, layer="bubble")
    ic.glyph(g, fill="#ffffff", lift=2, layer="gull")
    return ic


# =============================================================== LALE (music)
LALE_A, LALE_B = "#6a35d9", "#d63a8f"   # invented brand gradient (violet -> magenta)


def lale_tulip():
    # tulip head: three pointed petals over a round cup (rounded joins via Q)
    return ("M51 23Q52 21.5 53.5 23L59 30L64.6 17.8Q66 15.6 67.4 17.8L73 30L78.5 23Q80 21.5 81 23"
            "L81 35C81 44 74.5 51 66 51C57.5 51 51 44 51 35Z")


def lale_stem():
    return "M63.5 49H68.5V91H63.5Z"


def lale_flag():
    # the leaf that doubles as the eighth-note flag
    return "M68.5 56C77 58 85 64 86 76C82 70 76 68 68.5 69Z"


def lale_head():
    return ellipse_d(57.5, 91, 10.5, 7.6, -22)


def lale_note(s=1.0, dx=0.0, dy=0.0):
    return "".join(xform_d(p, s, dx, dy) for p in (lale_tulip(), lale_stem(), lale_flag(), lale_head()))


def lale_grad(ic, cx=64, cy=63, r=59):
    return ic.linear([(0, LALE_A), (1, LALE_B)], cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7)


def lale_source():
    ic = Icon("Lale (source logo)", source_note=CC0, license="CC0-1.0")
    ic.path(circle_d(64, 64, 60), lale_grad(ic, 64, 64, 60), "disc")
    ic.path(lale_note(), "#ffffff", "note")
    return ic


def lale_disc():
    ic = Icon("Lale - Sound Disc", source_note=CC0, license="CC0-1.0")
    mid = "#a03ab8"
    ic.disc(face=lale_grad(ic), chin=ic.chin_gradient(mid, 5, 123, 50), top_light=0.0)
    # curvature light on the gradient face (curved surface -> gradient allowed)
    ic.path(circle_d(64, 63, 59), ic.linear([(0, "#ffffff", 0.16), (0.5, "#ffffff", 0.0), (1, "#000000", 0.08)], 0, 4, 0, 122), "disc-light")
    ic.glyph(lale_note(0.98, 0, -1), fill="#ffffff", lift=2.2, layer="note")
    return ic


def lale_rimmed():
    ic = Icon("Lale - Rimmed", source_note=CC0, license="CC0-1.0")
    ic.rimmed_disc(inner=LALE_A, inner_gradient=lale_grad(ic, 64, 63, 53.5))
    ic.glyph(lale_note(0.84, 0, -1), fill="#ffffff", lift=2, layer="note")
    return ic


def lale_record():
    """GNOME metaphor: a vinyl record (music domain object) whose label carries the mark."""
    ic = Icon("Lale - Record (object)", source_note=CC0, license="CC0-1.0")
    vinyl = "#3d3846"
    ic.disc(face=vinyl, chin=ic.chin_gradient(vinyl, 5, 123, 50, colors={"edge": "#000000", "base": "#241f31", "highlight": "#5e5c64"}),
            curvature=False)
    # grooves: very low contrast rings (detail that may vanish at 32 px by design)
    for r in (52, 46, 40):
        ic.path(circle_d(64, 63, r) + circle_d(64, 63, r - 1), "#ffffff", f"groove{r}", opacity=0.07, fill_rule="evenodd")
    # outer edge so the dark record still separates from dark wallpapers
    ic.path(circle_d(64, 63, 59) + circle_d(64, 63, 57.5), "#77767b", "edge", fill_rule="evenodd")
    # soft diagonal sheen of the glossy material (gradient, not hard wedges)
    ic.path(circle_d(64, 63, 57.5), ic.linear([(0, "#ffffff", 0.0), (0.42, "#ffffff", 0.10), (0.5, "#ffffff", 0.0),
                                               (0.58, "#ffffff", 0.07), (1, "#ffffff", 0.0)], 20, 20, 108, 106), "sheen")
    ic.path(circle_d(64, 63, 30), lale_grad(ic, 64, 63, 30), "label")
    ic.glyph(lale_note(0.56, 0, -1), fill="#ffffff", lift=1.2, layer="note")
    return ic


def lale_symbol():
    """The tulip-note itself as the icon silhouette, extruded."""
    ic = Icon("Lale - Free Symbol", source_note=CC0, license="CC0-1.0")
    s = 1.25
    parts = [xform_d(p, s, -3, 6.4) for p in (lale_tulip(), lale_stem(), lale_flag(), lale_head())]
    face = ic.linear([(0, LALE_A), (1, LALE_B)], 30, 116, 100, 10)
    chin = ic.chin_gradient("#8a37c4", 30, 104, 14)
    ic.pieces(parts, face="#8a37c4", face_fill=face, chin=chin, layer="note", fill_rule=None)
    return ic


# =============================================================== SIMIT (mascot)
DOUGH = "#d08c3c"          # invented brand golden-brown
TEAL = "#2ec2b3"


def simit_parts(s=1.0, dx=0.0, dy=0.0):
    """The mascot defined once: every alternative scales this, never redraws it."""
    X = lambda d: xform_d(d, s, dx, dy)  # noqa: E731
    return {
        "arm_l": X(capsule_d(36, 72, 24, 86, 7.5)),
        "hand_l": X(circle_d(23, 87.5, 5.2)),
        "arm_r": X(capsule_d(92, 62, 104, 46, 7.5)),
        "hand_r": X(circle_d(105, 44.5, 5.2)),
        "leg_l": X(capsule_d(55, 94, 53, 106, 7.5)),
        "leg_r": X(capsule_d(73, 94, 75, 106, 7.5)),
        "foot_l": X(ellipse_d(50.5, 107.5, 6.5, 4)),
        "foot_r": X(ellipse_d(77.5, 107.5, 6.5, 4)),
        "ring": X(circle_d(64, 62, 36)) + X(circle_d(64, 56, 12.5)),
        "eye_l": X(ellipse_d(54, 80, 3.4, 4.4)),
        "eye_r": X(ellipse_d(74, 80, 3.4, 4.4)),
        "glint_l": X(circle_d(55.2, 78.4, 1.3)),
        "glint_r": X(circle_d(75.2, 78.4, 1.3)),
        "mouth": X("M58.5 86.5Q64 89 69.5 86.5Q69 92.5 64 92.5Q59 92.5 58.5 86.5Z"),
        "cheek_l": X(ellipse_d(47, 86, 4, 2.6)),
        "cheek_r": X(ellipse_d(81, 86, 4, 2.6)),
        "sesame": [X(ellipse_d(x, y, 2.2, 1.2, r)) for x, y, r in
                   [(44, 46, -40), (52, 34, -15), (64, 30.5, 0), (76, 34, 15), (84, 46, 40), (90, 60, 80),
                    (38, 60, -80), (45, 64, -60), (82, 66, 60), (58, 40, -10), (70, 40, 10)]],
    }


def simit_draw(ic, s=1.0, dx=0.0, dy=0.0, flat=False):
    p = simit_parts(s, dx, dy)
    limb = shade(DOUGH, -0.05)
    cc = chin_colors(DOUGH)
    ic.layers.append('<g id="simit">')
    for k in ("arm_l", "hand_l", "leg_l", "leg_r", "foot_l", "foot_r", "arm_r", "hand_r"):
        if not flat:
            ic.path(translate_d(p[k], 0, 2), cc["base"], f"{k}-chin")
        ic.path(p[k], limb, k)
    if flat:
        ic.path(p["ring"], DOUGH, "ring", fill_rule="evenodd")
    else:
        # torus: chin 4 px (also shows the inner wall at the top of the hole), gentle top light
        ic.path(translate_d(p["ring"], 0, 4), ic.chin_gradient(DOUGH, 28 * s + dx + 64 * (1 - s), 100 * s + dx + 64 * (1 - s), 30),
                "ring-chin", fill_rule="evenodd")
        ring_face = ic.linear([(0, shade(DOUGH, 0.06)), (0.6, DOUGH), (1, shade(DOUGH, -0.03))], 0, 26 * s + dy + 64 * (1 - s), 0, 98 * s + dy + 64 * (1 - s))
        ic.path(p["ring"], ring_face, "ring", fill_rule="evenodd")
    for k, d in enumerate(p["sesame"]):
        if not flat:
            ic.path(translate_d(d, 0, 0.8), shade(DOUGH, -0.12), f"sesame{k}-side")
        ic.path(d, "#fff4dc", f"sesame{k}")
    for k in ("cheek_l", "cheek_r"):
        ic.path(p[k], "#f66151", k, opacity=0.45)
    for k in ("eye_l", "eye_r", "mouth"):
        ic.path(p[k], "#241f31", k)
    for k in ("glint_l", "glint_r"):
        ic.path(p[k], "#ffffff", k)
    ic.layers.append("</g>")


def simit_source():
    ic = Icon("Simit (source logo)", source_note=CC0, license="CC0-1.0")
    ic.path(circle_d(64, 64, 60), "#bfeee6", "backdrop")
    simit_draw(ic, 0.92, 0, 2, flat=True)
    return ic


def simit_character():
    ic = Icon("Simit - Character (free silhouette)", source_note=CC0, license="CC0-1.0")
    simit_draw(ic, 1.12, 0, -2)
    return ic


def simit_disc():
    ic = Icon("Simit - Disc", source_note=CC0, license="CC0-1.0")
    ic.disc(face=TEAL, top_light=0.5)
    simit_draw(ic, 0.86, 0, -1)
    return ic


def simit_plate():
    """GNOME metaphor for a recipe app: the mascot sitting on a ceramic plate."""
    ic = Icon("Simit - Plate (object)", source_note=CC0, license="CC0-1.0")
    ic.rimmed_disc(inner="#e6f6f3", rim=9, rim_face="#ffffff", rim_chin="#d5d3cf", inner_shadow=0.08,
                   inner_gradient=ic.linear([(0, "#cfeee8"), (1, "#eaf8f5")], 0, 14, 0, 112))
    simit_draw(ic, 0.8, 0, -2)
    return ic


BUILD = {
    "marti-source": marti_source, "marti-faithful": marti_faithful, "marti-disc": marti_disc,
    "marti-rimmed": marti_rimmed, "marti-symbol": marti_symbol,
    "lale-source": lale_source, "lale-disc": lale_disc, "lale-rimmed": lale_rimmed,
    "lale-record": lale_record, "lale-symbol": lale_symbol,
    "simit-source": simit_source, "simit-character": simit_character, "simit-disc": simit_disc,
    "simit-plate": simit_plate,
}

if __name__ == "__main__":
    only = sys.argv[1:]
    OUT.mkdir(exist_ok=True)
    for name, fn in BUILD.items():
        if only and not any(name.startswith(o) for o in only):
            continue
        fn().save(OUT / f"{name}.svg")
        print(OUT / f"{name}.svg")
