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

**No Symbol** (`skip: ["symbol"]`, falls back to Faithful): in the source the face
bleeds off the tile's left/right edges, so a free face stands on straight cut sides and
reads as a mask. Completing that silhouette would invent the shape of the head, which
the project forbids; inverting it turned the white eyes into tile-green sockets.

Measured: ssim32 faithful 0.864 / disc 0.869 / rimmed 0.796 (official median 0.82); no
fused gaps at 32 px; visual mass inside the pack's range.

Known weaknesses:
* The traced face keeps the source's geometry, so the tufts are slightly softer than
  the vector original (512 px trace, no APK vector available here).
* The three yellows of the beak (#ffc200 / #ffde00 / #f48000) are kept as measured;
  they may look slightly busy at 32 px but the beak still reads.
* Repeating the mask problem of Shizuku: solved here by not shipping a Symbol.

Not verified: not tested on a real launcher; the ComponentInfo
`ComponentInfo{com.duolingo/com.duolingo.app.LoginActivity}` comes from published
icon-pack appfilters (materialos/android-icon-pack, baitmooth/snow, varlesh/theia),
not from the APK manifest — no APK was available on this device.

Files: `duolingo-{faithful,disc,rimmed}.svg`, `png/duolingo-*-512.png` + `-256.png`,
`review.png`, `styles.png`.
