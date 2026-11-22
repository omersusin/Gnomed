#!/usr/bin/env python3
"""Write the Gnomed colour palette (the GNOME HIG palette, Dark 5 = pure black left out)
for every drawing program, from ONE source: RAMP in work/_lib/objects.py.

    python3 tools/make_palettes.py        # -> docs/palette/*

  gnomed.gpl   GIMP, Inkscape (Edit > Swatches; copy to ~/.config/inkscape/palettes/), Krita, Karbon
  gnomed.ase   Adobe Illustrator / Photoshop, Affinity Designer, Pixelmator
  gnomed.json  {"Blue": ["#99c1f1", ...], ...} for code and AI agents
  gnomed.css   CSS custom properties (--blue-1 ... --dark-4)
  palette.svg / palette.png   the sheet with names and hex values (README, people)

Rules (REDESIGN.md §5): pick ONE ramp per part, 3 steps of it (top light / face / side);
map a brand colour to the nearest ramp and keep its lightness; never pure black (#000000):
Dark 4 (#241f31) is the darkest colour Gnomed uses.
"""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/palette"
sys.path.insert(0, str(ROOT / "work/_lib"))


def ramps():
    import objects as O
    out = {}
    for name, steps in O.RAMP.items():
        seen = []
        for h in steps:
            if h not in seen:          # Dark 5 repeats Dark 4 (no pure black in Gnomed)
                seen.append(h)
        out[name] = seen
    return out


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def write_gpl(R):
    lines = ["GIMP Palette", "Name: Gnomed (GNOME HIG)", "Columns: 5", "#"]
    for name, steps in R.items():
        for i, h in enumerate(steps, 1):
            r, g, b = rgb(h)
            lines.append(f"{r:3d} {g:3d} {b:3d}\t{name} {i}")
    (OUT / "gnomed.gpl").write_text("\n".join(lines) + "\n")


def _ase_name(s):
    s = s + "\0"
    return struct.pack(">H", len(s)) + s.encode("utf-16-be")


def write_ase(R):
    blocks = []
    for name, steps in R.items():
        body = _ase_name(name)
        blocks.append(struct.pack(">HI", 0xC001, len(body)) + body)          # group start
        for i, h in enumerate(steps, 1):
            r, g, b = (v / 255 for v in rgb(h))
            body = _ase_name(f"{name} {i}") + b"RGB " + struct.pack(">fffH", r, g, b, 2)
            blocks.append(struct.pack(">HI", 0x0001, len(body)) + body)      # colour (normal)
        blocks.append(struct.pack(">HI", 0xC002, 0))                         # group end
    data = b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks)) + b"".join(blocks)
    (OUT / "gnomed.ase").write_bytes(data)


def write_json_css(R):
    (OUT / "gnomed.json").write_text(json.dumps(R, indent=1) + "\n")
    css = [":root {"]
    for name, steps in R.items():
        for i, h in enumerate(steps, 1):
            css.append(f"  --{name.lower()}-{i}: {h};")
    css.append("}")
    (OUT / "gnomed.css").write_text("\n".join(css) + "\n")


def write_sheet(R):
    cw, ch, lw, top = 112, 64, 84, 56
    W = lw + cw * 5 + 16
    H = top + ch * len(R) + 16
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<style>text{font-family:Inter,Cantarell,DejaVu Sans,sans-serif}</style>',
           '<text x="16" y="26" font-size="15" font-weight="700" fill="#241f31">Gnomed palette (GNOME HIG)</text>']
    for i in range(5):
        out.append(f'<text x="{lw + cw * i + cw / 2}" y="{top - 4}" font-size="11" fill="#5e5c64" text-anchor="middle">{i + 1}</text>')
    for r, (name, steps) in enumerate(R.items()):
        y = top + ch * r
        out.append(f'<text x="16" y="{y + ch / 2 + 4}" font-size="13" fill="#241f31">{name}</text>')
        for i, h in enumerate(steps):
            x = lw + cw * i
            L = sum(c * w for c, w in zip(rgb(h), (0.299, 0.587, 0.114)))
            fg = "#241f31" if L > 150 else "#ffffff"
            out.append(f'<rect x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="8" fill="{h}" '
                       'stroke="#000000" stroke-opacity="0.08"/>')
            out.append(f'<text x="{x + cw / 2}" y="{y + ch / 2 + 4}" font-size="12" fill="{fg}" '
                       f'text-anchor="middle">{h}</text>')
    out.append("</svg>")
    svg = "\n".join(out) + "\n"
    (OUT / "palette.svg").write_text(svg)
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "palette.png"), output_width=W * 2)
    except ImportError:
        print("cairosvg missing: palette.png not written")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    R = ramps()
    write_gpl(R)
    write_ase(R)
    write_json_css(R)
    write_sheet(R)
    print(f"wrote docs/palette/: gnomed.gpl .ase .json .css, palette.svg/.png ({sum(map(len, R.values()))} colours)")


if __name__ == "__main__":
    main()
