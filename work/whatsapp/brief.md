# whatsapp - icon brief (status: READY FOR USER REVIEW)

## Source
- Input: IconRequest export (IconRequest_1794963383391.zip) -> icons/whatsapp.png, 192 px RGBA
- Geometry origin: trace of the user's image - colour masks of source.png, Lanczos x4, potrace (work/_lib/gtrace.py, extract_group1.py)
- Trace fidelity (IoU path vs mask): ring 0.9982, ring_outer 0.9997, handset 0.9982
- Licence / ownership: the logo is a trademark of its owner; personal icon-pack use

## Archetype + decisions
- Archetype: A tile glyph (bubble ring + handset)
- Symbol = WhatsApp's own standalone logo: green bubble with a 4.5 u green margin around the white ring (margin added so the white ring does not touch a light wallpaper)
- Construction per pack style: faithful = square plate 104 r8, 4 px chin · disc = d118, 2 px chin, curvature light · rimmed = Adwaita rim + recessed disc · symbol = the mark as the object

## Alternatives
- whatsapp-faithful.svg
- whatsapp-disc.svg
- whatsapp-rimmed.svg
- whatsapp-symbol.svg

## Review
- lint: no FAIL · boards: review.png, legibility.png, work/_group1/launcher-<style>.png
- Known weaknesses: rimmed lowest at 32 px (ssim 0.78) - ring + rim compete

## Android
- drawable: whatsapp (+ _alt1.. for the other styles), ComponentInfo from the phone's IconRequest appfilter.xml (not adb/APK-verified)
