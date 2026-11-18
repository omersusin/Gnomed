# Duolingo — status: READY FOR USER REVIEW

Source geometry: 512 px Play Store icon (`com.duolingo`), traced by `auto.py` (ground
model + Lab k-means regions → gtrace). This is the owl-face icon currently shipped by
Duolingo, not a redraw from memory.

Primary: `duolingo-faithful.svg` — green plate (#58cc02, flat) + the traced face
(#89e219 head, #ffffff eyes, #4b4b4b pupils, #ffc200 lip, #ffde00 highlight,
#f48000 lower beak).

Alternatives:
* `duolingo-disc.svg` — same face on the disc construction.
* `duolingo-rimmed.svg` — Adwaita rim + recessed green disc, mark at 1.1× the default
  rimmed width so it does not look small in the recess.

**Symbol** (`duolingo-symbol.svg`, hand-built in `work/_lib/build_weak.py`, free
adaptation): the owl's head as an object. In the source the head is cut by the tile's
left/right edges; the two straight cuts are closed by one ellipse that meets the measured
contour above and below them, so every measured curve is kept and only the cuts become
convex. Eyes, pupils and beak are the traced parts, moved with the head as one unit; under
the beak the object's side is the beak's dark orange. (The first version shipped without a
Symbol, so the Symbol APK showed Duolingo on a square plate.)

Measured: ssim32 faithful 0.864 / disc 0.869 / rimmed 0.796 (official median 0.82); no
fused gaps at 32 px; visual mass inside the pack's range.

Known weaknesses:
* The traced face keeps the source's geometry, so the tufts are slightly softer than
  the vector original (512 px trace, no APK vector available here).
* The three yellows of the beak (#ffc200 / #ffde00 / #f48000) are kept as measured;
  they may look slightly busy at 32 px but the beak still reads.
* Repeating the mask problem of Shizuku: solved here by not shipping a Symbol.

Not verified: not tested on a real launcher; the ComponentInfo
`ComponentInfo{com.duolingo/com.duolingo.app.LoginActivity}` was verified on the owner's phone
(`cmd package resolve-activity`: `com.duolingo/.app.LoginActivity`).

Files: `duolingo-{faithful,disc,rimmed,symbol}.svg`, `png/duolingo-*-512.png` + `-256.png`,
`review.png`, `styles.png`.
