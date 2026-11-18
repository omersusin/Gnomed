# youtube - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/youtube.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): rect 0.9995, triangle 0.998
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: C free glyph (the red play button is the silhouette)
- source tile is white -> Faithful/Disc/Rimmed use a light plate with the raised red button; Rimmed is NOT a red disc (would read as YouTube Music)
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- youtube-faithful.svg
- youtube-disc.svg
- youtube-rimmed.svg
- youtube-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Disc/Rimmed: button smaller than in Symbol; light plates are faint on light wallpapers (chin edge only)

## Android
- drawable: youtube (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
