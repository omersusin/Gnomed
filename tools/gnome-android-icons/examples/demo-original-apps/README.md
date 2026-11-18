# Worked example - three invented apps (CC0)

None of these is a real brand; they were invented to exercise the whole
pipeline without reproducing anyone's logo. `build_demos.py` is the reference
for writing your own `build.py`: identity geometry defined once, every
alternative built from it with `gnome_kit`.

```bash
python3 build_demos.py                     # -> svg/*.svg
python3 ../../scripts/lint_svg.py svg/*.svg
python3 ../../scripts/preview_sheet.py svg/marti-*.svg --source svg/marti-source.svg --out review/marti-review.png
```

## Martı - messaging (archetype A: glyph on a tile)
Source: coral tile, white speech bubble with a gull cut-out.

| file | family | review notes |
|---|---|---|
| `marti-faithful.svg` | A Faithful (primary) | square 104 r20, 4 px chin, bubble lifted 2 px; gull hole shows its inner wall. Closest to source |
| `marti-disc.svg` | B Sound Disc | soft top light, reads well at 32 px |
| `marti-rimmed.svg` | C Rimmed | rim nearly invisible on light wallpapers (same as GNOME Clocks) - best on dark |
| `marti-symbol.svg` | D Free Symbol | bubble is the silhouette, Polari-like; tail makes it asymmetric - deliberate |

## Lale - music (archetype B: circular mark)
Source: violet->magenta disc with a white "tulip-note" (tulip head, stem, leaf = note flag, note head).

| file | family | review notes |
|---|---|---|
| `lale-disc.svg` | B Sound Disc (primary) | gradient face kept (curved surface), 2 px chin, note lifted |
| `lale-rimmed.svg` | C Rimmed | Mousai construction; strongest on dark wallpapers |
| `lale-record.svg` | E Metaphor: vinyl record | label carries the mark; **weak at 32 px** (tulip mushes) |
| `lale-symbol.svg` | D Free Symbol | aspect 0.45: **light visual weight next to GNOME icons** (lint warns) - weakest variant, kept to show the trade-off |

## Simit - recipes with a mascot (archetype G)
Source: sesame-ring character with face, waving arm, legs, on a mint disc.

| file | family | review notes |
|---|---|---|
| `simit-character.svg` | Character (primary) | free silhouette; ring hole shows inner wall; most legible face at 32 px |
| `simit-disc.svg` | B Disc/badge | mascot at 0.86 scale: face becomes 2 dots at 32 px |
| `simit-plate.svg` | E Metaphor: ceramic plate | food-app object; same anatomy, scaled 0.8 |

Anatomy check: all three use `simit_parts()` unchanged (same limbs, face,
11 sesame seeds) - only `xform_d` scale/offset differ.

## Measured at 32 px (`review/legibility.png`, `legibility.json`)

| icon | ssim32 | RED gaps | reading |
|---|---|---|---|
| lale-disc | 0.906 | 1 | above the official median (0.824) |
| lale-record | 0.796 | 5 | between p10 and median; the tulip mushes inside the label - matches the review note |
| lale-rimmed | 0.838 | 2 | |
| lale-symbol | 0.959 | 0 | highest score, yet the lightest icon in the launcher row: SSIM rewards detail, not weight |
| marti-disc / faithful / rimmed / symbol | 0.893 / 0.909 / 0.828 / 0.928 | 2 each | the gull's wing tips are the 2 gaps; the gull still reads |
| simit-character / disc / plate | 0.889 / 0.872 / 0.762 | 13 / 13 / 16 | the gaps are the 11 sesame seeds merging - decoration, not an anchor; plate is near p10 (mascot too small) |

Official GNOME app icons (n=98): ssim32 p10 0.751 / median 0.824 / p90 0.91;
gap regions median 3 (p90 11). Numbers point at risks; the boards decide.

`png/` holds 512 and 256 px transparent exports; `review/` the boards
(`*-review.png` per app, `legibility.png`, `launcher.png` = all eleven on a phone
home screen at real size with forced icon shapes).
