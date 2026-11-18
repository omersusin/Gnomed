#!/usr/bin/env python3
"""Gnomed wallpapers - calm, low-contrast backdrops for the icon pack (code-drawn SVG).
Waves only in the top and bottom bands; the middle (where the icon grid sits) stays a
plain soft gradient so every icon reads. python3 make_wallpapers.py"""
import cairosvg

W, H = 1080, 2400


def wave(y, amp, phase, depth):
    """closed band from a smooth wave at height y down (depth>0) or up (depth<0) to the edge."""
    pts = []
    n = 3
    for i in range(n + 1):
        x = W * i / n
        pts.append((x, y + amp * ((-1) ** (i + phase)) * 0.5))
    d = f"M0 {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cx = (x0 + x1) / 2
        d += f" C{cx:.0f} {y0:.0f} {cx:.0f} {y1:.0f} {x1:.0f} {y1:.0f}"
    edge = H if depth > 0 else 0
    return d + f" L{W} {edge} L0 {edge} Z"


def svg(top, bottom, bands_bottom, bands_top):
    body = [f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>']
    shapes = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    for i, (y, amp, col) in enumerate(bands_top):
        shapes.append(f'<path d="{wave(y, amp, i, -1)}" fill="{col}"/>')
    for i, (y, amp, col) in enumerate(bands_bottom):
        shapes.append(f'<path d="{wave(y, amp, i + 1, 1)}" fill="{col}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{"".join(body)}</defs>{"".join(shapes)}</svg>')


VARIANTS = {
    # soft Adwaita-blue light: colourful icons pop, nothing competes with them
    "gnomed-light": svg("#eef2f7", "#d8e2ec",
                        [(1980, 70, "#cfdbe7"), (2120, 60, "#c3d2e1"), (2260, 50, "#b7c9da")],
                        [(330, 70, "#e3eaf2"), (210, 60, "#dae4ee")]),
    # dark slate (Adwaita dark tones): for dark mode; icon chins and edges stay visible
    "gnomed-dark": svg("#2b303b", "#1c2028",
                       [(1980, 70, "#232833"), (2120, 60, "#272d39"), (2260, 50, "#2c3340")],
                       [(330, 70, "#303644"), (210, 60, "#353c4b")]),
}

if __name__ == "__main__":
    for name, s in VARIANTS.items():
        open(f"{name}.svg", "w").write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{name}-1080x2400.png", output_width=1080, output_height=2400)
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{name}-1440x3200.png", output_width=1440, output_height=3200)
        print(name)
