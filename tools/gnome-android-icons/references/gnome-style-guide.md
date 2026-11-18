# GNOME / Adwaita app-icon style guide (offline, evidence-based)

Sources: GNOME HIG "App Icons" page, Tobias Bernard's "Designing an Icon for
Your App" (GNOME design team), the HIG-app-icons `template.svg`, and **98 real
app SVGs** in `assets/reference-library/` measured with `scripts/measure_style.py`
and dissected with `scripts/inspect_svg.py`. Numbers come from
`measured-style.md`. Each rule names the reference icons that prove it - open
them (`inspect_svg.py <file>`) instead of trusting prose.

Tag legend: **[HIG]** official guideline · **[MEASURED]** observed in the
official SVGs · **[PROJECT]** this pack's own art direction (user feedback).

---

## 1. Canvas, grid, sizes

| Rule | Tag | Detail |
|---|---|---|
| 128 x 128 canvas, `viewBox="0 0 128 128"` | HIG | Design for **64 px**, check **32 px**; nothing that disappears at 32 |
| 2 px detail grid (8 px squares in the template) | HIG | Orthogonal edges on the grid -> sharp at 64/32. Curves may be optical |
| Do **not** fill the canvas | HIG | Match the template shape for your proportions and the visual weight of neighbours |
| Template shapes | MEASURED | circle **d120** (face 4..124, centre 64,63-64) · square **104** (12..116, r 8) · portrait **88 x 112** (20..108 x 8..120) · landscape **112 x 88** (8..120 x 28..116) |
| Bottom edge | MEASURED | squares/landscapes end at **y=116**, portraits **120**, discs **124-126** (baseline guide at 117) |
| Avoid extreme aspect ratios | HIG | narrow/tall glyphs (< 0.6 or > 1.6) look lighter: compensate with mass, or put them on a plate |

| Visual mass | MEASURED | painted share of the canvas: p10 0.44 / median **0.62** / p90 0.69 for official apps - and MoreWaita/Adwaita++ match it (0.66 / 0.63). One optical size across a pack; `pack_audit.py` flags outliers |

`gnome_kit.TEMPLATES` holds these numbers. `lint_svg.py` warns when you drift.

## 2. Perspective: the chin (front face)

GNOME icons are **not flat**. They fold the top view and the front view of the
same object into one drawing: the front face (the "chin") is a band at the
**bottom** of the silhouette, darker than the top face because light comes from
above. [HIG] It is *not* a drop shadow and not an outline.

| Property | Value | Evidence |
|---|---|---|
| Height | **4 px** typical (median 4.0 in all sets); **2 px** on discs/spheres; 6-8 px only for thick objects | Calendar, Meld, Polari (4); clocks, Mousai, Epiphany (2); Console, Calculator (6-8) |
| Construction | the face silhouette **copied and moved down** by the chin height, painted *under* the face | clocks: face circle at cy 63, chin circle at cy 65; Mousai: same |
| Colour | 1-2 palette steps darker than the face, slightly less saturated; warm hues deepen toward red | Blue3 -> Blue5, Green3 -> Green5, Purple3 -> Purple5, Yellow3 -> Yellow5 (see `chin_colors()`) |
| Corner highlight | chin gets a **horizontal** gradient: edge-dark -> highlight -> base ... mirrored. Stops at ~`r/2w` and `r/w` (r = corner radius, w = width) | Polari `0 dark, .05 light, .10 base ... .875 base, .9375 light, 1 dark`; Calendar `.038/.077`; Console `.05/.10` |
| Holes | a hole through the object shows its **inner wall**: the chin copy (moved down) shows through the top of the hole automatically if face and chin are even-odd paths | any ring/donut; demo `simit-character` |
| Never | top/back folding (the chin on top), chin on every edge, chin floating detached, chin wider than the face, blurred shadow below | Tobias Bernard "common mistakes" |
| Dark faces | a darker chin under a near-black face disappears on dark wallpapers: keep the chin close to the face and make its corner highlights *lighter* (`chin_colors()` does this below OKLab L 0.42) | Console, Turntable keep readable edges |
| Sharp corners | chin corner highlights only where the silhouette's bottom corner is rounded (`chin_gradient(..., corners="left"/"right"/"none")`) | split panels, notches |

Code: `Icon.slab()`, `Icon.plate()`, `Icon.disc()` build face + chin + chin
gradient in one call. `sweep_chin_d()` for shapes thinner than the chin.

## 3. Light, gradients, materials

| Rule | Tag | Detail / evidence |
|---|---|---|
| Light from straight above | HIG | shading only top-lighter / bottom-darker |
| Flat surfaces = flat colour | HIG | Calendar page, Meld planes, Polari bubbles |
| Curved surfaces = gradient | HIG | Epiphany sphere, Snapshot lens, Mousai disc face (diagonal brand gradient), Weather sun |
| No shadows outside the silhouette | HIG | the desktop/launcher adds context shadows; `lint_svg.py` fails semi-transparent fringes |
| Internal shadow only for contrast | HIG | e.g. 20 % black under clock hands; Mousai's 10-12 % crescent inside the rim makes the disc read as recessed |
| Materials (wood, metal, glass) only when the metaphor *is* that object | HIG | Turntable wood, Snapshot glass; never "make the logo glass" |
| Gloss / specular | MEASURED | rare; only on genuinely glossy objects (lens, vinyl). A white arc on every icon is NOT GNOME |
| Radial gradients | MEASURED | median 0; use for lenses, bulbs, spheres |

**The user's "Sound Disc" taste [PROJECT]:** a calm disc face with *curvature*
light (top slightly lighter, bottom slightly darker), a broad soft top light
(`disc(top_light=...)`, never a glossy blob or hard arc), mark slightly raised
or engraved, 2 px chin. That is consistent with the HIG rule "curved surface ->
gradient" and with Mousai/clocks. It is one family option - **not** a mandate
to make every icon round.

## 4. Glyphs on faces ("lift")

A symbol sitting on a coloured face is itself a thin raised object. Official
icons give it its own 1-2 px darker copy below (its side), not a blur:

- white glyph -> side `#c0bfbc` (Light4) or `#deddda` - Mousai notes, Software icons, clocks hands
- coloured glyph -> side = glyph colour darkened (`shade(c, -0.14)`)
- recessed/engraved mark (dark mark on a light face) -> a lighter line below,
  ~50 % opacity (`glyph(..., engrave=True)`) - the look the user liked in Sound Disc
- lift distance stays 1-2 px **after scaling**: use `xform_d()` / `fit_parts()` to
  scale paths, not `<g transform>` (which would scale the lift too)
- several pieces (letters, dots, a face): paint ALL sides first, then ALL faces
  (`ic.glyphs()` / `ic.pieces()`), so no side covers a neighbour

## 5. Colour

- Start from the 45-swatch HIG palette (`scripts/_common.py: HIG_PALETTE`,
  `assets/template/gnome-hig-palette.gpl`). Official icons take ~75 % of colours
  from it.
- For **third-party brands keep the brand hue** (MoreWaita does; users recognise
  apps by colour). Optionally nudge toward the nearest HIG swatch when it is
  within dE ~10 and recognition survives. `analyze_source.py` reports both.
- What must become GNOME-like is the **role system**: face, chin (darker, a bit
  less saturated), chin highlight, glyph side, neutral rims (`#f6f5f4` face /
  `#d5d3cf` chin / `#deddda` highlight).
- Neutral greys in GNOME are warm (Light2 `#f6f5f4`, Dark3 `#3d3846`); avoid
  pure `#808080`-type cold greys and pure black faces (Dark4 `#241f31` instead).
- Dark brand tiles: keep them dark but lift them off pure black (`#241f31`,
  `#3d3846`) and give them a light outer edge or chin highlight so they separate
  from dark wallpapers (demo `lale-record`).

## 6. Shape language

- Simple geometric primitives: rectangles (rounded), circles, capsules, clean
  Beziers. [HIG] Corner radius on template rects: 8 px (larger allowed for
  softer objects: Software 16-20).
- Unique silhouette beats a generic container. [HIG] A bare symbol with a chin
  (Calls handset, Polari bubbles, Totem play-fold) is fully GNOME.
- Overlapping planes may use translucency (Totem, Showtime), but planes must
  stay coherent - no random layer soup.
- Detail budget: typical 5-30 paths. Fine lines < 2 px at 128 disappear at 32.

## 7. Metaphor (and what it means for brand icons)

HIG metaphors: (1) an object tied to the function, (2) an older analog object
from the domain, (3) a domain symbol (play triangle), (4) a stylised version of
the app's distinctive UI. HIG avoids mascots and style-dependent logos **for
GNOME's own apps**. A themed icon pack has the opposite job: users must still
find *their* app. Therefore [PROJECT]:

- identity anchors from the real app outrank HIG metaphor purity;
- a GNOME metaphor (object) is an *alternative*, allowed only when the brand's
  anchors survive on it - never a TV/camera/speaker wrapper around an unrelated
  logo (user-rejected, see `lessons-and-rejections.md`);
- mascots stay mascots (anatomy unchanged) and receive GNOME *rendering*: flat
  faces, chins, simple shading, no out-of-silhouette shadows (Alpaca, Robots,
  Software.Socialize prove characters can be drawn the GNOME way).

## 8. What GNOME never does (fast reject list)

Drop shadows / outer glow · bevel-and-emboss on every edge · thick dark outlines ·
glossy white arcs or "glass" over a logo · noise/texture · photographic detail ·
text labels · forcing every icon into a squircle / circle / screen / camera ·
perspective that is not top+front · inconsistent light direction · chin on top ·
mismatched visual weight (tiny glyph floating in a huge plate, or vice-versa).

## 9. Symbolic icons (if ever needed)

16 x 16, single colour, 2 px strokes mostly, outermost 1 px empty, same metaphor.
Android icon packs rarely need them (themed-icon/monochrome layers excepted).
