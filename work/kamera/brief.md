# kamera - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/kamera.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): disc 0.9995
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: I object (lens) with a recording dot
- measured lens radii; pure black -> Dark4 #241f31, rings snapped to HIG darks #3d3846/#5e5c64, dot #ff0000 -> HIG red #ed333b; Disc/Symbol get a 1.4 u light lens edge for dark wallpapers
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- kamera-faithful.svg
- kamera-disc.svg
- kamera-rimmed.svg
- kamera-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: Disc and Symbol are close to each other; dark lens still subdued on dark wallpapers

## Android
- drawable: kamera (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
