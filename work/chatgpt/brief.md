# chatgpt - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/chatgpt.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): knot 0.9967
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: L monochrome mark (knot)
- black -> Dark4 #241f31; Faithful = dark knot engraved on a light plate (as used in the source), Disc/Rimmed = white knot on dark
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- chatgpt-faithful.svg
- chatgpt-disc.svg
- chatgpt-rimmed.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: fixed 2026-11-18 - the first build inverted the logo (only the black lines were used, shown white on dark). Now: white knot object (silhouette IoU 0.998) with the dark lines inlaid; side colour = the dark outline, so no light layer peeks out. Symbol added. 32 px: strands thin but recognisable.

## Android
- drawable: chatgpt (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
