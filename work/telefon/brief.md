# telefon - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/telefon.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): handset 0.9988
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: A tile glyph (Fossify handset)
- Symbol = Calls-like extruded handset
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- telefon-faithful.svg
- telefon-disc.svg
- telefon-rimmed.svg
- telefon-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Symbol visual mass 0.23 (light); dark green #106d1f low contrast on dark wallpapers

## Android
- drawable: telefon (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
