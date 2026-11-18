# Measured style - numbers, not opinions

Generated from the SVG files with `scripts/measure_style.py` (2026-11-05, visual
mass + legibility added 2026-11-07).
Cells are **p10 / median / p90**, nominal 128-px units. Re-run on your icon with
`python3 scripts/measure_style.py my.svg --compare official` to see where it sits.

How the chin is measured: in the central 40 % of columns, the height of the
darker band at the bottom edge of the silhouette (heuristic: it under-reports on
icons whose bottom is not a plain front face, and can over-report on vertical
gradients - read it together with the pictures).

Sets:
- **GNOME apps** = 98 official app icons (52 GNOME core, 14 GNOME games, 32 GNOME
  Circle / GNOME-styled third-party apps) fetched from their GitHub mirrors.
- **MoreWaita** = 516 unique app SVGs, **Adwaita++** = 739 unique app SVGs, from
  the user's archives (community themes, not GNOME policy); their summaries are
  stored in `assets/reference-library/community-summary.json`.

### Official vs community

| metric | GNOME apps (98) | GNOME core (52) | Circle/3rd-party (32) | MoreWaita (516) | Adwaita++ (739) |
|---|---|---|---|---|---|
| visual width (px) | 95.4 / **110.6** / 120.6 | 92.2 / **111.6** / 121.0 | 96.8 / **112.0** / 122.5 | 95.8 / **104.0** / 120.0 | 94.2 / **108.2** / 120.0 |
| visual height | 96.1 / **111.1** / 124.0 | 104.0 / **112.0** / 123.8 | 88.4 / **112.0** / 124.0 | 104.0 / **108.0** / 122.0 | 90.0 / **106.8** / 122.0 |
| bottom edge y | 116.0 / **120.0** / 126.0 | 116.0 / **120.0** / 125.9 | 116.0 / **120.0** / 125.8 | 116.0 / **118.0** / 125.0 | 115.0 / **118.8** / 125.0 |
| fill ratio (of own box) | 0.59 / **0.855** / 0.995 | 0.603 / **0.847** / 0.995 | 0.579 / **0.817** / 0.995 | 0.606 / **0.804** / 0.995 | 0.626 / **0.926** / 0.995 |
| visual mass (painted share of canvas) | 0.444 / **0.624** / 0.692 | 0.449 / **0.624** / 0.705 | 0.448 / **0.605** / 0.685 | 0.408 / **0.657** / 0.708 | 0.454 / **0.629** / 0.705 |
| chin height | 2.0 / **4.0** / 12.0 | 2.0 / **4.0** / 8.6 | 2.1 / **4.5** / 16.0 | 3.8 / **4.0** / 16.9 | 1.8 / **4.0** / 17.8 |
| solid colours | 3.7 / **10.0** / 16.3 | 3.0 / **10.0** / 15.0 | 4.1 / **9.5** / 22.8 | 5.0 / **10.0** / 25.0 | 3.0 / **7.0** / 13.0 |
| % colours on HIG palette | 22.6 / **75.0** / 100.0 | 36.4 / **80.5** / 100.0 | 0.8 / **60.0** / 100.0 | 4.0 / **27.0** / 59.0 | 29.0 / **80.0** / 100.0 |
| linear gradients | 1.0 / **4.0** / 9.6 | 1.0 / **3.5** / 8.9 | 1.0 / **4.0** / 15.7 | 2.0 / **4.0** / 19.0 | 0.0 / **1.0** / 6.0 |
| radial gradients | 0.0 / **0.0** / 3.0 | 0.0 / **0.0** / 3.0 | 0.0 / **0.0** / 1.9 | 0.0 / **0.0** / 4.0 | 0.0 / **0.0** / 1.0 |
| horizontal gradients | 0.0 / **2.0** / 7.3 | 1.0 / **2.0** / 7.0 | 0.0 / **2.0** / 7.9 | 1.5 / **3.0** / 11.0 | 0.0 / **1.0** / 4.0 |
| <path> count | 5.0 / **12.5** / 29.3 | 4.1 / **10.0** / 25.9 | 6.1 / **16.5** / 39.7 | 1.0 / **5.0** / 24.0 | 3.0 / **7.0** / 21.2 |
| stroked elements | 0.0 / **0.0** / 4.0 | 0.0 / **1.0** / 4.0 | 0.0 / **0.0** / 2.9 | 0.0 / **0.0** / 2.5 | 0.0 / **0.0** / 2.0 |

## What the numbers say

1. **Size = template shape, not "fill the square".** Official circles are 120 wide
   (face d118-120 + 2 px chin -> 122 tall, bottom 124-126); squares are 104 x 104
   with bottom 116; portraits 88 x 112 (bottom 120); landscapes 112 x 88 (bottom 116).
   MoreWaita follows exactly the same boxes (its p25/median are 104 and 120).
2. **Chin: 4 px is the norm (median 4.0 in every set); 2 px on discs/spheres;
   up to 8 px only for thick objects (Console, Calculator, Turntable).**
3. **Palette:** official icons take ~75 % of their colours from the 45-swatch HIG
   palette; MoreWaita deliberately keeps brand colours (median 27 %); Adwaita++
   re-colours toward the palette (80 %). Brand colours are legitimate - the
   *shading roles* (face / chin / highlight) are what must be GNOME-like.
4. **Gradients are common but structural:** median 3-4 linear gradients, and 1-2 of
   them are *horizontal* - the chin gradient with corner highlights. Radial
   gradients are rare (median 0): reserve them for lenses, spheres, bulbs.
5. **Strokes are rare (median 0).** Shapes are filled paths; MoreWaita's
   contribution guide forbids strokes outright.
6. **Simplicity:** median ~12 paths official, 5 in MoreWaita. More paths do not
   mean more GNOME.

## Visual mass and small-size legibility (v1.1)

- **Visual mass** = painted share of the 128 canvas. Official app icons: p10
  0.444 / median **0.624** / p90 0.692. A full-bleed square scores ~1.0
  (the classic non-GNOME look); a thin glyph alone ~0.25. `pack_audit.py` flags
  icons outside the official p5-p95 band so a pack keeps one optical size.
- **Legibility at 32 px** (`legibility_check.py`, n=98 official app icons):
  SSIM of the 32 px raster vs. the 128 px render p10 0.751 / median **0.824** /
  p90 0.91; "gap regions" that fuse at 32 px median 3.0
  (p90 11.3). Gaps are normal in detailed GNOME icons - the
  question is whether a gap separates *identity anchors* (two letters, a dot
  from its stem, a brand cut-out).

## Upstream files are not automatically "clean"

8 of the 134 bundled upstream SVGs (Loupe, Yelp, Taquin, Atomix, Blanket and
3 Adwaita devices) embed small base64 PNG masks - export artefacts of soft
effects (catalog flag `embedded_raster`). Study their shapes, never imitate the
raster trick: this pack's rule is pure vector (`lint_svg.py` fails `<image>`).

## Key references (open these first)

| id | kind | shape | w x h | bottom | chin | colours (HIG %) | why it matters |
|---|---|---|---|---|---|---|---|
| `org.gnome.Epiphany` | symbol-object | circle | 120.0 x 122.0 | 125.0 | 2.0 | 12 (17 %) | globe sphere; curved face uses gradients; 2px chin on a sphere |
| `org.gnome.clocks` | disc-object | circle | 120.0 x 122.0 | 125.0 | 2.0 | 10 (90 %) | light rim + dark dial; chin = same circle 2px lower; side-highlight trick |
| `io.github.seadve.Mousai` | disc-emblem | circle | 117.5 x 119.5 | 123.8 | 1.8 | 7 (57 %) | disc with light rim, gradient inner disc, white glyph with 2px lift - closest official analogue of a "Sound Disc" |
| `org.gnome.Snapshot` | disc-object | circle | 120.5 x 122.2 | 126.0 | 1.8 | 11 (91 %) | camera lens (concentric rings, glass gradients) - not a camera body |
| `org.gnome.Totem` | emblem | free | 96.0 x 110.0 | 120.0 | 4.0 | 0 (0 %) | folded play emblem; brand-like abstract mark with overlapping translucent planes |
| `org.gnome.Showtime` | emblem | free | 96.8 x 112.0 | 120.0 | 5.5 | 13 (92 %) | play emblem + film strip; multicolour gradient planes |
| `org.gnome.Meld` | emblem | square | 104.0 x 104.0 | 116.0 | 4.0 | 7 (71 %) | abstract swirl logo on square; chin coloured per region |
| `re.sonny.Tangram` | emblem | square | 104.2 x 104.0 | 116.0 | 4.0 | 9 (33 %) | geometric tangram on square |
| `org.gnome.Polari` | free-glyph | free | 120.0 x 108.0 | 120.0 | 4.0 | 9 (78 %) | two speech bubbles with chins |
| `org.gnome.Calls` | free-glyph | free | 108.0 x 110.2 | 118.2 | 2.0 | 9 (56 %) | handset glyph extruded as an object, no backplate |
| `app.drey.Dialect` | letterform | free | 108.2 x 88.0 | 116.0 | 22.0 | 10 (60 %) | letter D on a folded tag + script glyph |
| `org.gnome.Software.Socialize` | character | circle | 120.0 x 120.0 | 124.0 | 8.0 | 8 (100 %) | emoji smiley face on a disc - a face drawn GNOME-style |
| `com.jeffser.Alpaca` | character | free | 124.0 x 124.0 | 124.0 | 4.0 | 9 (33 %) | alpaca/llama animal - mascot-like character in GNOME style |
| `org.gnome.Robots` | character | circle | 120.0 x 122.0 | 126.0 | None | 11 (91 %) | robot head - character treated as an object |
| `org.gnome.Calendar` | object | square | 104.0 x 104.0 | 117.0 | 2.0 | 12 (75 %) | calendar page; header band; chin gradient |
| `org.gnome.Console` | ui | square | 104.0 x 104.0 | 116.0 | 8.0 | 8 (62 %) | terminal window on square; dark face |
| `org.gnome.Nautilus` | object | portrait | 88.0 x 112.0 | 120.0 | 4.0 | 8 (100 %) | file cabinet portrait |
| `org.gnome.Calculator` | device | portrait | 80.0 x 112.0 | 120.0 | 6.0 | 9 (89 %) | calculator portrait |
| `dev.geopjr.Turntable` | object | landscape | 112.0 x 92.0 | 116.0 | 8.8 | 17 (71 %) | turntable with record |
| `io.github.seadve.Kooha` | device | landscape | 112.0 x 88.0 | 116.0 | 4.0 | 8 (75 %) | screen recorder |
