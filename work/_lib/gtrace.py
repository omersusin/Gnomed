"""Small helpers for Gnomed icon builds (used by work/<app>/build.py).

mask_d(): one clean compound path for every pixel of source.png that matches a
colour predicate. The source (IconRequest PNG, 192 px, upscaled to 512 by
extract_icon.py) is upscaled again with Lanczos, thresholded at the half-way
point between the colours, and traced with potrace - so antialiased edges land
on the true edge instead of producing halo layers. Output is in 0..128 units.

Everything here MEASURES the source; nothing is drawn from memory.
"""
from pathlib import Path

import numpy as np
import potrace
from PIL import Image

UP = 4  # extra upscale before tracing


def load(slug_dir):
    im = Image.open(Path(slug_dir) / "source.png").convert("RGBA")
    w, h = im.size
    big = im.resize((w * UP, h * UP), Image.LANCZOS)
    a = np.asarray(big).astype(np.float32) / 255.0
    return a, 128.0 / (w * UP)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255.0


def near(a, color, other, alpha_min=0.5):
    """True where the pixel is closer to `color` than to `other` (both hex)."""
    c, o = hexrgb(color), hexrgb(other)
    rgb = a[..., :3]
    dc = ((rgb - c) ** 2).sum(-1)
    do = ((rgb - o) ** 2).sum(-1)
    return (dc < do) & (a[..., 3] >= alpha_min)


def opaque(a, alpha_min=0.5):
    return a[..., 3] >= alpha_min


def luma_above(a, t, alpha_min=0.5):
    y = a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    return (y > t) & (a[..., 3] >= alpha_min)


def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def trace_mask(mask, scale, turdsize=None, alphamax=1.0, opttolerance=0.4, smooth_u=0.45):
    """Potrace a boolean mask -> SVG path d (even-odd compound) in 128 units.

    smooth_u: Gaussian smoothing (in 128-units, ~half a pixel of the 192 px source)
    before thresholding - removes the source's pixel staircase that otherwise shows
    up as wobbly edges at large sizes, without moving straight edges or curves."""
    if smooth_u:
        from scipy import ndimage
        mask = ndimage.gaussian_filter(mask.astype(np.float32), smooth_u / scale) > 0.5
    if turdsize is None:
        turdsize = int((1.2 / scale) ** 2)  # drop specks smaller than ~1.2 u square
    bm = potrace.Bitmap(~mask.astype(bool))  # potracer traces the False pixels
    path = bm.trace(turdsize=turdsize, alphamax=alphamax, opticurve=True, opttolerance=opttolerance)
    out = []
    for curve in path:
        sx, sy = curve.start_point.x, curve.start_point.y
        seg = [f"M{_f(sx * scale)} {_f(sy * scale)}"]
        for s in curve.segments:
            if s.is_corner:
                seg.append(f"L{_f(s.c.x * scale)} {_f(s.c.y * scale)}"
                           f"L{_f(s.end_point.x * scale)} {_f(s.end_point.y * scale)}")
            else:
                seg.append(f"C{_f(s.c1.x * scale)} {_f(s.c1.y * scale)} {_f(s.c2.x * scale)} {_f(s.c2.y * scale)} "
                           f"{_f(s.end_point.x * scale)} {_f(s.end_point.y * scale)}")
        seg.append("Z")
        out.append("".join(seg))
    return "".join(out)


def mask_d(slug_dir, predicate, **kw):
    a, scale = load(slug_dir)
    return trace_mask(predicate(a), scale, **kw)


def components(mask):
    """Label connected components (8-connectivity) -> list of boolean masks, largest first."""
    from scipy import ndimage
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    order = np.argsort(-sizes)
    return [lab == (i + 1) for i in order]


def fill_holes(mask):
    from scipy import ndimage
    return ndimage.binary_fill_holes(mask)


def circle_fit(mask, scale):
    """Least-squares circle through the boundary of a mask -> (cx, cy, r) in 128 units."""
    from scipy import ndimage
    edge = mask & ~ndimage.binary_erosion(mask)
    ys, xs = np.nonzero(edge)
    A = np.c_[2 * xs, 2 * ys, np.ones_like(xs)]
    b = xs ** 2 + ys ** 2
    cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]
    r = np.sqrt(c + cx ** 2 + cy ** 2)
    return cx * scale, cy * scale, r * scale


def bbox(mask, scale):
    ys, xs = np.nonzero(mask)
    return xs.min() * scale, ys.min() * scale, (xs.max() + 1) * scale, (ys.max() + 1) * scale


def iou_masks(m1, m2):
    return (m1 & m2).sum() / max((m1 | m2).sum(), 1)


def render_mask(d, size, fill_rule="evenodd"):
    """Rasterise a path (128 units) to a boolean mask of size x size for IoU checks."""
    import io
    import cairosvg
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 128 128">'
           f'<path d="{d}" fill="#000" fill-rule="{fill_rule}"/></svg>')
    im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    return np.asarray(im)[..., 3] > 127
