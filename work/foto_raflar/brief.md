# foto_raflar - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/foto_raflar.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): yellow 0.9985, red 0.999, blue 0.9979, green 0.9961
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: E multicolour geometric mark (4 petals)
- petals split at the measured centre; each petal a linear plane from its measured inner colour to outer colour (Showtime-like), per-petal chin colour (Meld)
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- foto_raflar-faithful.svg
- foto_raflar-disc.svg
- foto_raflar-rimmed.svg
- foto_raflar-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Symbol visual mass 0.37; source's translucent overlap at the centre simplified to per-petal gradients

## Android
- drawable: foto_raflar (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
