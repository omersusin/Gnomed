# mesajlar - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/mesajlar.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): bubble 0.9987, bubble_outer 0.9994, line0 0.9969, line1 0.998, line2 0.9971
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: A tile glyph (Fossify bubble with 3 lines)
- Symbol = green bubble object with raised white lines (Polari-like)
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- mesajlar-faithful.svg
- mesajlar-disc.svg
- mesajlar-rimmed.svg
- mesajlar-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Rimmed ssim 0.72 at 32 px - lines get thin; readable on the board

## Android
- drawable: mesajlar (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
