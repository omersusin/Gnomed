"""Shared helpers for the gnome-android-icons skill scripts.

Only code-based, deterministic tooling lives here: SVG parsing, rasterising
with CairoSVG (or rsvg-convert as fallback), and small image utilities.
No generative image model is used or called anywhere in this skill.
"""
from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
LIB_ROOT = SKILL_ROOT / "assets" / "reference-library"

# GNOME HIG palette (developer.gnome.org/hig/reference/palette.html, verified
# against HIG-app-icons "GNOME HIG.gpl").  1 = lightest, 5 = darkest.
HIG_PALETTE = {
    "blue":   ["#99c1f1", "#62a0ea", "#3584e4", "#1c71d8", "#1a5fb4"],
    "green":  ["#8ff0a4", "#57e389", "#33d17a", "#2ec27e", "#26a269"],
    "yellow": ["#f9f06b", "#f8e45c", "#f6d32d", "#f5c211", "#e5a50a"],
    "orange": ["#ffbe6f", "#ffa348", "#ff7800", "#e66100", "#c64600"],
    "red":    ["#f66151", "#ed333b", "#e01b24", "#c01c28", "#a51d2d"],
    "purple": ["#dc8add", "#c061cb", "#9141ac", "#813d9c", "#613583"],
    "brown":  ["#cdab8f", "#b5835a", "#986a44", "#865e3c", "#63452c"],
    "light":  ["#ffffff", "#f6f5f4", "#deddda", "#c0bfbc", "#9a9996"],
    "dark":   ["#77767b", "#5e5c64", "#3d3846", "#241f31", "#000000"],
}
HIG_FLAT = {f"{fam}{i+1}": c for fam, cols in HIG_PALETTE.items() for i, c in enumerate(cols)}


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in rgb[:3])


def _srgb_to_lab(rgb):
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(c1, c2) -> float:
    """CIE76 colour distance between two hex strings or rgb tuples."""
    if isinstance(c1, str):
        c1 = hex_to_rgb(c1)
    if isinstance(c2, str):
        c2 = hex_to_rgb(c2)
    a, b = _srgb_to_lab(c1), _srgb_to_lab(c2)
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


def nearest_hig(color) -> tuple[str, str, float]:
    """Return (swatch_name, swatch_hex, deltaE) of the nearest HIG swatch."""
    best = min(HIG_FLAT.items(), key=lambda kv: delta_e(color, kv[1]))
    return best[0], best[1], delta_e(color, best[1])


def render_svg_to_png_bytes(svg_path: str | os.PathLike, size: int) -> bytes:
    """Rasterise an SVG to a square transparent PNG of `size` px.

    Tries CairoSVG first, then rsvg-convert, then Inkscape.  Raises
    RuntimeError if none is available.
    """
    svg_path = str(svg_path)
    try:
        import cairosvg  # type: ignore
        return cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
    except ImportError:
        pass
    except Exception as exc:  # cairosvg can choke on exotic SVG; try the others
        last = exc
    if shutil.which("rsvg-convert"):
        return subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), svg_path],
                              check=True, capture_output=True).stdout
    if shutil.which("inkscape"):
        out = subprocess.run(["inkscape", svg_path, "--export-type=png", f"--export-width={size}",
                              f"--export-height={size}", "--export-filename=-"],
                             check=True, capture_output=True).stdout
        return out
    raise RuntimeError("No SVG rasteriser found: pip install cairosvg, or install rsvg-convert/inkscape")


def render_svg(svg_path, size: int):
    """Return a PIL RGBA image of the SVG at `size` px."""
    from PIL import Image
    return Image.open(io.BytesIO(render_svg_to_png_bytes(svg_path, size))).convert("RGBA")


def load_font(size: int):
    from PIL import ImageFont
    for cand in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/dejavu/DejaVuSans.ttf",
                 "/Library/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def svg_viewbox(svg_path) -> tuple[float, float, float, float] | None:
    txt = Path(svg_path).read_text(encoding="utf-8", errors="replace")[:4000]
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', txt)
    if not m:
        return None
    nums = [float(x) for x in re.split(r"[\s,]+", m.group(1).strip()) if x]
    return tuple(nums) if len(nums) == 4 else None


# ---------------------------------------------------------------- OKLab shading
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delin(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return max(0, min(255, round(c * 255)))


def hex_to_oklab(h):
    r, g, b = (_lin(v) for v in hex_to_rgb(h))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab_to_hex(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return "#%02x%02x%02x" % (_delin(max(0, r)), _delin(max(0, g)), _delin(max(0, bb)))


def shade(h, dl: float, chroma: float = 1.0, hue_deg: float = 0.0):
    """Lighten (dl>0) or darken (dl<0) a colour in OKLab, optionally scaling
    chroma and rotating hue.

    Calibrated on HIG pairs (face -> chin): green3->green5 dL -0.13 chroma x0.77,
    blue3->blue5 dL -0.12 x0.92, orange3->orange5 dL -0.15 hue -9deg,
    yellow3->yellow5 dL -0.11 hue -16deg (warm hues deepen toward red).
    """
    import math
    L, a, b = hex_to_oklab(h)
    if hue_deg:
        t = math.radians(hue_deg)
        a, b = a * math.cos(t) - b * math.sin(t), a * math.sin(t) + b * math.cos(t)
    return oklab_to_hex(max(0, min(1, L + dl)), a * chroma, b * chroma)


def hue_of(h) -> float:
    import math
    _, a, b = hex_to_oklab(h)
    return math.degrees(math.atan2(b, a)) % 360


def hig_step(h, steps: int):
    """Move a HIG swatch along its family (e.g. blue3 +2 -> blue5); falls back to shade()."""
    h = h.lower()
    for fam, cols in HIG_PALETTE.items():
        if h in cols:
            i = max(0, min(4, cols.index(h) + steps))
            return cols[i]
    return shade(h, -0.06 * steps)
