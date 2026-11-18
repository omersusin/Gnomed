# Review protocol (the quality gate)

Technical checks prove hygiene. Measurements point at risks. Only looking
proves design. Do all three, in this order, for every alternative.

## 1. Hygiene (automatic, must pass)

```bash
python3 scripts/lint_svg.py work/<app>/<app>-*.svg        # FAIL = must fix, warn = justify in brief.md
python3 scripts/measure_style.py work/<app>/<app>-<alt>.svg --compare official
```

## 2. Measurements (automatic, read them - do not obey them blindly)

```bash
python3 scripts/legibility_check.py work/<app>/<app>-*.svg --out work/<app>/legibility.png
```

| Number | What it means | Official GNOME app icons (n=98) |
|---|---|---|
| `ssim` at 32 px | how much structure survives at 32 px (1 = identical) | p10 0.75 / median 0.82 / p90 0.91 - below p10 = losing more than almost every GNOME icon |
| `gaps` at 32 px (RED) | negative spaces < 1 screen px: pieces FUSE | median 3 (p90 11) - normal in detailed icons; a problem only when the gap separates identity anchors (two letters, a dot from its stem, a brand cut-out) |
| `thin` at 32 px (ORANGE) | parts < 0.75 screen px: they fade | orange on chin corners / lifts is decoration - ignore it |
| visual mass (`measure_style`, `pack_audit`) | painted share of the canvas | p10 0.44 / median 0.62 / p90 0.69 - outside: the icon looks heavier/lighter than its neighbours |

SSIM rewards detail retention, not presence: a thin, light glyph can score
high and still look weak in a launcher (demo `lale-symbol`: ssim 0.96, yet the
lightest icon in its row). That is why step 3 exists.

## 3. Look (mandatory - with your own eyes / image viewer)

```bash
python3 scripts/preview_sheet.py work/<app>/<app>-*.svg --source work/<app>/source.png \
    --ref-ids <3-6 catalog ids of the same archetype> --title "<App>" --out work/<app>/review.png
python3 scripts/launcher_preview.py work/<app>/<app>-*.svg --refs 10 --shape all --out work/<app>/launcher.png
```

`review.png`: 1 = source vs candidates at 256 (light/dark; the source sits on a
checkerboard so white/transparent marks stay visible), 2 = true 64/48/32 px +
32 px magnified, 3 = family row with every icon named. `launcher.png`: real
phone size (54 dp x 2.75 = ~149 px on 1080 x 2400) on light / dark / colourful
wallpapers, plus what launchers do when "force icon shape" is on.

Answer, per alternative, in `brief.md`:

| # | Question | Fail examples |
|---|---|---|
| 1 | **Identity at 32 px** (review row 2 + legibility RED marks): would the user find the app instantly? | glyph mush, letters fused, colour order lost |
| 2 | **Anchors intact** at 256 vs source: silhouette, angles, counts, negative spaces; every "NOT traced" detail from the brief's Trace notes redrawn or consciously dropped | extra/missing ray, limb, cut, eye highlight |
| 3 | **GNOME construction**: chin at the bottom only, flat planes, gradients only on curved faces, no outer shadow | bevel, gloss arc, blur |
| 4 | **Visual weight** in the family row and the launcher grid | too small / large / light |
| 5 | **Wallpapers**: readable on light, dark *and* colourful | dark icon disappears, white glyph vanishes |
| 6 | **Layering**: nothing pokes out, no seams between face and chin | slivers, gaps under thin parts (use `sweep_chin_d`) |
| 7 | **Restraint**: could anything be removed without losing identity? | ornaments, stacked rims |
| 8 | **History**: does it repeat a rejected pattern (`lessons-and-rejections.md`)? | TV wrapper, toy camera, logo + shadow only |

If something fails: fix the *structure* (geometry, construction, mark size,
colour roles), re-render, re-look. Never answer a structural critique with
decoration. Drop an alternative that cannot be fixed - three good beat five weak.

For high-stakes batches, have a second agent (or the user) review the boards
without seeing your reasoning.

## 4. Pack level (when icons are in the project)

```bash
python3 scripts/pack_audit.py --project ~/IconPack --sheet work/pack-audit.png
```
Fix every ERROR (missing resources, duplicate mappings, broken XML) before
building; look at the family sheet for weight outliers (red frames).

## 5. Report honestly (template)

```
<App> - status: DRAFT | READY FOR USER REVIEW | APPROVED BY USER
Source geometry: <APK vector | official SVG | trace of user image | community ref adapted (licence)>
Primary: <file> - <one-line why>
Alternatives: <file> - <why> ...
Measured: ssim32 <x> (official median 0.82), gaps at anchors: <none | where>, visual mass <x>
Known weaknesses: <e.g. 32 px: dot fuses with the p; light plate faint on light wallpaper>  (never empty unless truly none)
Not verified: <e.g. not tested on a real launcher; ComponentInfo unknown; Gradle build not run>
Files: SVG (editable), PNG 512/256 (transparent), review.png, legibility.png, launcher.png
```

Only the user moves a design to APPROVED.
