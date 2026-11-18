# Bitwarden - icon brief  (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/bitwarden.png, 192 px RGBA  (raster route; see source.json / source-geometry.svg / source-trace.svg)
- Geometry origin: trace of the user's image; shield curves least-squares fitted to the trace (fit_shield.py, max dev 0.29 u outer / 0.13 u hole, IoU 0.990)
- Licence / ownership notes: Bitwarden logo is a trademark of Bitwarden Inc.; personal icon-pack use

## Trace notes (source-trace.json - check against source.png)
- Detail pass restored 1 small region(s) (new colours #134eb9)

## Identity (from identity.md)
- Anchors: shield silhouette (flat top, straight sides, pointed bottom); vertical split - left half solid, right half a framed hollow; white/blue relation
- Must not change: split position (centre), frame thickness (~8.6 u at 128), shield proportions 66 x 79

## Archetype + references
- Archetype: A - brand glyph on a tile (tile shape = launcher mask; tile colour = identity). Material long shadow dropped (no outer shadows in GNOME)
- GNOME references compared: org.gnome.Seahorse, org.gnome.Calls, org.gnome.Polari, io.github.seadve.Mousai
- Community refs looked at (not policy): none (MoreWaita/Adwaita++ archives not available in this session)

## Alternatives
| Alternative | File | Rationale | Status |
|---|---|---|---|
| A · Adwaita Faithful | bitwarden-faithful.svg | primary: closest to source, square plate 104 r8 | READY FOR USER REVIEW |
| B · Sound Disc | bitwarden-disc.svg | compact centred mark; user's liked family | READY FOR USER REVIEW |
| C · Rimmed | bitwarden-rimmed.svg | best separation on blue/colourful wallpapers | READY FOR USER REVIEW |
| D · Free Symbol | bitwarden-symbol.svg | shield as object, blue body + white recessed field (brand's on-white usage) | READY FOR USER REVIEW |
| F · Light | (dropped) | light plate vanished on light wallpaper, mark small at 32 px | DROPPED |

## Review (fill after review.png, legibility.png, launcher.png)
- 32 px: no fused gaps in any; ssim 0.88/0.895/0.794/0.903   - 48/64 px: clean   - family fit: mass 0.66/0.68/0.68/0.51 (official median 0.62)   - launcher: Faithful/Disc blend into blue wallpapers; Rimmed separates
- Known defects (do not hide): source only 192 px (no vector); Rimmed lowest ssim at 32 px (rim eats pixels); Symbol narrow (w 88.5, below p10 width)

## Android
- drawable name: bitwarden
- ComponentInfo: ComponentInfo{com.x8bit.bitwarden/com.x8bit.bitwarden.MainActivity} - from the phone's IconRequest appfilter.xml (not adb/APK-verified here)
