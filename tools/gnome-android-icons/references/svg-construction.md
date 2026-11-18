# SVG construction (v1.2): obj.py for objects, gnome_kit underneath

## Objects (redesigns) — scripts/obj.py

```python
from obj import *                                   # gk, shapely shapes, solid, recess, hole, toplight
ic = gk.Icon("App - GNOME redesign")
body = rounded(box(18, 22, 110, 106), 12)           # shapes: box, circ, ellipse, poly(points, r), rounded(g, r)
solid(ic, body, face=[(0, "#99c1f1"), (1, "#3584e4")], depth=8, layer="body")   # side + face + top light
recess(ic, rounded(box(30, 34, 98, 80), 6), [(0, "#f6f5f4"), (1, "#deddda")])  # sunk label/screen
hole(ic, circ(64, 96, 6))                            # real hole: dark, darker top wall
solid(ic, circ(94, 96, 16), face="#ff7800", depth=4, layer="badge")             # secondary object in front
ic.save("work/app/app.svg")
```

Boolean shapes (union, difference, offset) are shapely: `a.union(b)`, `a.difference(b)`,
`a.buffer(-4)`; `move`, `scale`, `down`; `geom_d(g)` gives the path. Full examples:
`examples/redesign/build_examples.py` (a cloud + arrow, a steel shield with enamel and keyhole).

## Template treatments and measuring drafts — gnome_kit

`new_icon.py` writes `work/<slug>/build.py`: one `build_<alt>()` per alternative,
starting as an autodraft. Refine those functions with `scripts/gnome_kit.py`.
Output is plain, layered, Inkscape-editable SVG (paths + gradients, named ids).

## Source geometry

```python
import autodraft as ad
SRC = ad.Source(OUT)              # reads source-geometry.svg or source-trace.svg (+ analysis.json)
SRC.ground, SRC.mark              # container part (tile/disc) vs. the mark parts (dicts: id, d, fill, rule, gradient)
SRC.brand_color(), SRC.mark_colors, SRC.ground_gradient   # gradient stops: from flatten (real SVG gradients)
                                                           # or from the trace's gradient pass (data-gradient)
SRC.place(box)                    # mark parts moved into box; ground mapped onto box (keeps source proportions)
SRC.place(box, relative_to_ground=False)   # fit the mark alone
gk.load_parts("x.svg")            # {id: d} of any flat SVG (trace / flatten output)
gk.fit_parts(parts, box=(x0, y0, x1, y1))  # scale/move a set of paths as one unit, aspect kept
gk.bbox_d(d_or_list)
```

## Building

```python
import gnome_kit as gk
ic = gk.Icon("App - Faithful", source_note="geometry: APK vector, ic_launcher_foreground")
face = ic.plate("square", face="#ff6b57", r=20)          # face + 4 px chin + chin gradient; returns the FACE box
face = ic.disc(face="#3584e4", top_light=0.7)            # Sound Disc: 2 px chin, curvature light, soft top light
face = ic.rimmed_disc(inner="#3584e4")                   # Adwaita rim + recessed inner disc
ic.slab(d, face="#33d17a", corner_r=8, depth=4)          # ANY silhouette + its chin (bbox measured)
ic.pieces(parts, face="#33d17a")                         # multi-piece mark: all chins first, then all faces
ic.glyph(d, fill="#ffffff", lift=2, fill_rule="evenodd") # one raised mark (side = Light4 for white)
ic.glyphs(parts, fill="#ffffff", lift=2)                 # several raised pieces, sides first
ic.glyph(d, fill="#1a5fb4", lift=1.5, engrave=True, face_hint="#33d17a")   # engraved look
box = ic.safe_box(face, pad=0.18)                        # where a mark sits on a plate/disc (optically centred)
url = ic.linear([(0, "#hex"), (1, "#hex", 0.5)], x1, y1, x2, y2)   # returns url(#id)
url = ic.chin_gradient(face_hex, x0, x1, corner_r, corners="both|left|right|none")
with ic.group("mark"): ...                               # wrap layers in <g id="mark">
ic.save("work/app/app-faithful.svg")
```

Helpers: `rrect_d`, `circle_d`, `ellipse_d`, `capsule_d`, `polygon_d`,
`rounded_polygon_d(points, radius|[radii])`, `xform_d(d, s, dx, dy, about)`,
`translate_d(d, dx, dy)` (falls back to svgpathtools on unusual syntax),
`sweep_chin_d(d, 4)` (gap-free extrusion for parts thinner than the chin),
`chin_colors(face)` (normal / dark faces / light neutrals), `lift_color(fill)`.

CLI: `gnome_kit.py skeleton disc|rimmed|square|portrait|landscape out.svg --color '#hex'`,
`gnome_kit.py chin '#hex'`.

## Patterns (all present in official icons)

**Chin by copy** - silhouette moved down (4 px slabs / 2 px discs) in the chin
colour, then the face: Clocks, Mousai, Polari.

**Chin gradient** - horizontal, highlights at `r/2w` and `r/w`; only at rounded
corners (`corners=`).

**Holes / inner walls** - one even-odd path (outer + hole); its moved-down copy
shows the hole's inner wall for free. Ground-coloured cut-outs become real holes
when a variant has no plate (autodraft `_cutouts_to_holes`).

**Recessed disc** - inner disc + a 10 % black even-odd crescent (Mousai).

**Per-region chins** - each colour region gets its own chin shade, same depth,
all painted before any face (Meld).

**Figure / ground without a plate** - white figures get the brand colour and
brand-coloured cut-outs turn white (autodraft `_inverted_map`), so a mark never
disappears on a light wallpaper. If the brand colour is a gradient ground, the
mark's face carries that gradient (`_gradient_faces`), the chin stays solid.

**Letters** - never `<text>`: the brand outline (APK vector / flatten / trace).

## Things that break renderers / Android

Filters (blur, drop-shadow) - avoid entirely. `mix-blend-mode`, `<foreignObject>`,
CSS `<style>` - avoid. Huge coordinates / root transforms - keep a clean 0..128.
Strokes on large shapes - convert to fills (`flatten_svg.py` does it for sources).

## Rendering

`export_png.py` (CairoSVG -> rsvg-convert -> Inkscape fallback) - deterministic.
`doctor.py` checks the machine before you start.
