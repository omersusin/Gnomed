# instagram - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/instagram.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): frame 0.9963, lens 0.9963, dot 0.9938
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: A tile glyph on a brand gradient
- gradient = one linear ramp through the measured colours (bottom #ffc800 -> centre #ff2a79 -> top #cc09ee/#791cff); Disc follows the user's Sound-Disc preference for Instagram
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- instagram-faithful.svg
- instagram-disc.svg
- instagram-rimmed.svg
- instagram-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Symbol is an open outline: visual mass 0.34 (below official p10 0.44); gradient simplified from the source's radial blend

## Android
- drawable: instagram (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
