#!/usr/bin/env python3
"""Build script for Bitwarden.   Run:  python3 build.py

Identity geometry: ONE shield definition (SHIELD_OUTER / SHIELD_HOLE below),
fitted to the potrace trace of the user's IconRequest PNG (fit_shield.py:
max deviation 0.29 u outer, 0.13 u hole, 128-u canvas). Every alternative
scales that same definition with gk.xform_d(); nothing is redrawn per variant.

Dropped on purpose: the Material long shadow of the source tile (GNOME: no
shadows outside the silhouette). The square tile shape is the launcher mask,
not identity; its colour is.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_lib"))
import skillpath  # noqa: E402,F401
import gnome_kit as gk  # noqa: E402

OUT = Path(__file__).resolve().parent
NOTE = "geometry: trace of user's IconRequest PNG (192 px), curves fitted to the trace (fit_shield.py)"

BLUE = "#175bd6"        # measured brand blue of the source tile
WHITE = "#ffffff"

# --- identity geometry, source tile coordinates (0..128) -------------------------
_k = 0.5523 * 2.5       # 2.5 u top corner radius (measured)
SHIELD_OUTER = (
    f"M31 30.67C31 {30.67 - _k:.2f} {33.5 - _k:.2f} 28.17 33.5 28.17"
    f"H94.5C{94.5 + _k:.2f} 28.17 97 {30.67 - _k:.2f} 97 30.67"
    "V70.75C97 87.62 80.63 100.49 64 107.5"
    "C47.37 100.49 31 87.62 31 70.75Z"
)
SHIELD_HOLE = "M64 36.81H88.3V70.08C88.3 81.69 76.47 91.16 64 97.8Z"
SRC_BOX = (31.0, 28.17, 97.0, 107.5)  # bbox of the shield in the source


def shield(cx, top, height):
    """Shield scaled to `height`, horizontally centred on cx, top edge at `top`."""
    s = height / (SRC_BOX[3] - SRC_BOX[1])
    ox, oy = 64.0, SRC_BOX[1]
    dx, dy = cx - ox, top - oy
    o = gk.xform_d(SHIELD_OUTER, s, dx, dy, about=(ox, oy))
    h = gk.xform_d(SHIELD_HOLE, s, dx, dy, about=(ox, oy))
    return o, h


def build_faithful():
    """A · Adwaita Faithful - white shield on the brand-blue square template plate."""
    ic = gk.Icon("Bitwarden - Adwaita Faithful", source_note=NOTE)
    face = ic.plate("square", face=BLUE, r=8)            # 12..116, face h 100, 4 px chin
    # source: shield 79.3 tall on a 128 tile, bbox centre 3.8 u below tile centre
    hgt = 79.33 * 0.80
    cy = face["y"] + face["h"] / 2 + 3.0
    o, h = shield(64, cy - hgt / 2, hgt)
    ic.glyph(o + h, fill=WHITE, lift=2, lift_fill="#deddda", fill_rule="evenodd", layer="shield")
    return ic


def build_disc():
    """B · Sound Disc - brand-blue disc, curvature light, soft top light, raised shield."""
    ic = gk.Icon("Bitwarden - Sound Disc", source_note=NOTE)
    ic.disc(face=BLUE, r=59, top_light=0.6)
    hgt = 66.0
    o, h = shield(64, 63 - hgt / 2 + 2.0, hgt)
    ic.glyph(o + h, fill=WHITE, lift=2, lift_fill="#deddda", fill_rule="evenodd", layer="shield")
    return ic


def build_rimmed():
    """C · Rimmed - light Adwaita rim + recessed brand-blue disc, raised shield."""
    ic = gk.Icon("Bitwarden - Rimmed", source_note=NOTE)
    ic.rimmed_disc(inner=BLUE, r=59, rim=5.5)
    hgt = 60.0
    o, h = shield(64, 63 - hgt / 2 + 2.0, hgt)
    ic.glyph(o + h, fill=WHITE, lift=2, lift_fill="#deddda", fill_rule="evenodd", layer="shield")
    return ic


def build_symbol():
    """D · Free Symbol - the shield is the object: blue body (brand-on-white usage),
    the right field a white inset panel, recessed; 4 px chin under the body."""
    ic = gk.Icon("Bitwarden - Free Symbol", source_note=NOTE)
    hgt = 106.0
    o, h = shield(64, 9.0, hgt)
    x0, _, x1, _ = gk.bbox_d(o)
    ic.slab(o, BLUE, bbox=(x0, x1), corner_r=(x1 - x0) * 0.45, depth=4, layer="body")
    with ic.group("field"):
        ic.path(h, WHITE, layer_id="field-face")
        # recess: thin shade under the frame's top/inner edges (Mousai-style crescent)
        ic.path(h + gk.translate_d(h, 0, 1.6), "#000000", layer_id="field-recess",
                opacity=0.12, fill_rule="evenodd")
    return ic


def build_light():
    """F · Light - neutral Adwaita light plate, shield in brand blue (Bitwarden's
    own on-white usage: blue shield, white right field)."""
    ic = gk.Icon("Bitwarden - Light", source_note=NOTE)
    face = ic.plate("square", face="#f6f5f4", r=8)
    hgt = 79.33 * 0.80
    cy = face["y"] + face["h"] / 2 + 3.0
    o, h = shield(64, cy - hgt / 2, hgt)
    ic.glyph(o + h, fill=BLUE, lift=2, lift_fill=gk.shade(BLUE, -0.14), fill_rule="evenodd", layer="shield")
    return ic


ALTS = ["faithful", "disc", "rimmed", "symbol"]   # "light" built, reviewed and dropped (plate vanishes on light wallpapers)

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALTS):
        path = OUT / f"bitwarden-{name}.svg"
        globals()["build_" + name]().save(path)
        print(path)
