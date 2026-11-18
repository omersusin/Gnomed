# Icon archetypes - classify first, then treat

Classify the *source* icon before drawing anything. The class decides which
alternatives make sense, which official references to open, and which
mistakes are likely. Use `analyze_source.py` facts (silhouette class, colours,
holes, thinnest feature) plus your eyes.

Reference ids are in `assets/reference-library/catalog.json`
(`scripts/ref_search.py --kind ...` lists them).

---

## A. Brand glyph on a tile (white/flat mark on a coloured square or squircle)
*Examples of the class: messaging, social, store apps.* Demo: `marti`.

- Anchors: the glyph's silhouette and negative spaces, the tile colour, glyph/tile contrast.
- The tile is usually the platform's mask, not identity -> its **colour** is identity, its **shape** is negotiable.
- Treatments: Faithful plate (square 104, r 8-20) · Sound Disc · Rimmed · Free Symbol (glyph becomes the silhouette, coloured, with chin).
- References: `org.gnome.Polari`, `org.gnome.Calls`, `io.github.seadve.Mousai`, `org.gnome.Meld`, `re.sonny.Tangram`.
- Pitfalls: shrinking the glyph to a stamp in a big plate; grey "lift" that reads as a dirty shadow (use the glyph's side colour, 2 px); losing small counters at 32 px.

## B. Circular brand mark (the logo itself is a disc)
*Examples: many browsers, music and messaging logos.* Demo: `lale`.

- Anchors: the circle + inner glyph/segments, gradient direction if the brand uses one.
- Primary treatment is usually the **Sound Disc** (disc face d118, 2 px chin, curvature light) - it is the faithful option here.
- Alternatives: Rimmed (Clocks/Mousai construction) · Free Symbol (inner glyph alone) · Object (if a domain object can *carry* the disc: record label, lens...).
- References: `io.github.seadve.Mousai`, `org.gnome.clocks`, `org.gnome.Epiphany`, `org.gnome.Snapshot`.
- Pitfalls: adding a rim *and* a sheen *and* a ring (stacked effects); breaking the brand's segment geometry; disc too small (must be ~118-120 wide).

## C. Free glyph / symbol (no container in the source)
*Examples: a play-fold, a handset, a single letter, an abstract swoosh.*

- Anchors: the silhouette itself.
- Primary: Free Symbol - extrude the glyph (chin 4 px, chin gradient), keep brand colours, fit visual weight (~96-112 box).
- Alternatives: Faithful plate (glyph on a light or brand plate) · Disc.
- References: `org.gnome.Totem`, `org.gnome.Showtime`, `org.gnome.Calls`, `org.gnome.Weather`.
- Pitfalls: thin glyphs (< 0.6 aspect) look weak - check family row in `preview_sheet.py`; translating a thin glyph down for the chin leaves gaps - use `sweep_chin_d()`.

## D. Letterform / wordmark initial
*Examples: single-letter streaming, office or social logos.* Ref: `app.drey.Dialect`.

- Anchors: letter skeleton (stroke contrast, cuts, folds, ribbons), colour.
- Treat the letter as a physical object: a folded ribbon gets real fold faces (darker inner folds, as Totem's planes); a solid letter gets a chin.
- Never re-type the letter in a font: copy the brand's own outline (official SVG / APK vector / trace).
- Alternatives: Free Symbol (letter alone) · Faithful plate (letter on brand tile, dark tiles lifted to `#241f31`/`#3d3846`) · Disc.

## E. Multicolour geometric mark (segments, rings, tiles in several hues)
*Examples: browser rings, workspace logos, puzzle-like marks.* Refs: `re.sonny.Tangram`, `org.gnome.Meld`, `org.gnome.baobab`.

- Anchors: segment count, angles, colour order, centre element.
- GNOME treatment: each segment is a flat plane; the chin under each segment takes **that segment's** darker shade (Meld's chin changes colour per region). One coherent chin, not one per piece floating apart.
- Pitfalls: re-drawing the segment angles from memory (always measure from source), per-segment bevels, gradients on flat segments.

## F. Radial / organic / starburst abstract marks
*Examples: sparkle, burst, flower, swirl marks.*

- Anchors: ray/petal count, ray profile (tapered? rounded tips? irregular?), symmetry or deliberate asymmetry, centre weight.
- Count and measure rays on the trace; keep irregularities that are part of the brand (hand-made looking tips) - do not "clean" them into a perfect star.
- Treat as Free Symbol with a 2-4 px chin, or as a mark on a brand plate/disc. Small rays: check 32 px; merge or thicken optically rather than dropping rays.

## G. Character / mascot
*Demo: `simit`. Refs: `com.jeffser.Alpaca`, `org.gnome.Robots`, `org.gnome.Software.Socialize`.*

- Anchors: pose, limb count and attachment points, face layout (eye spacing, mouth), head/body ratio, signature accessories, colours.
- **Define the anatomy once** (one function / one set of paths from the source), reuse it in every alternative by scaling with `xform_d()`. Never redraw limbs per variant.
- GNOME rendering: flat body faces, 2-4 px chins under body parts, the part *in front* paints last, simple 2-tone eyes with one glint, no outlines unless the source is line-art (then keep its line weight consistent, filled shapes).
- Alternatives: Character (free silhouette) · Disc/badge (mascot on brand disc, scaled 0.8-0.9) · Object (only a domain object the mascot naturally sits on).
- Verification: overlay the source trace on the result (`preview_sheet.py` large row) and check every limb; see `identity-preservation.md` section 5.

## H. Game art / poster (illustrated scene, several characters)
*Examples: game launcher icons with heroes, crowns, weapons.*

- A 128-px icon cannot hold a poster. Choose **one** identity element the community knows (the crown, the main hero's face, the logo emblem) and render that as a mascot (G) or emblem (C/E). State which element and why in the brief.
- Offer 3+ alternatives built on *different* identity elements so the user picks.
- Refs: `org.gnome.Chess`, `org.gnome.Software.Play`, `page.kramo.Cartridges`, games group sheet.

## I. Object / UI-derived (the source already is an object or a UI picture)
*Examples: calculator, camera, notes, file managers, launchers showing a screen.*

- GNOME's home turf: redraw the object in GNOME materials (most of the core library).
- A screen is OK only when the app's identity *is* a screen UI (terminal, monitor); otherwise no screens.
- Refs: core sheet (`assets/reference-library/sheets/gnome-core.png`), `adwaita-system` devices.

## J. Photographic / heavy-gradient / 3D-rendered logos
- Extract the flat identity (main shapes + 2-4 colours) from the trace; rebuild with flat planes + chin. Keep the brand gradient only where it is identity (e.g. a well-known two-colour sweep), as one smooth linear gradient across the face.

## K. Logo lockup (symbol + wordmark / initials in one mark)
*Example from this project: a channel logo = robot head + two-letter wordmark.*

- At 32 px letters, dots and bars FUSE (`legibility_check.py` marks them red): the
  wordmark is the weakest part of the icon, the symbol carries recognition.
- Keep the full lockup in Faithful/Disc/Rimmed (users know it), but offer one
  alternative that drops or enlarges parts: **symbol only** (the head without
  letters) or **letters only, larger** - built from the same traced parts, never
  redrawn. Say which parts were dropped.
- Free Symbol (pieces extruded, no plate) usually reads best at small sizes for
  lockups: the pieces get the whole canvas.
- Check gaps between letters/dots at 32 and 48 px; widen gaps optically (+1-2 units)
  only if the source spacing is not itself an anchor.

## L. Monochrome / white-only marks (the source has no colour of its own)
- The mark is identity; the colour is not given. Do not invent a "brand colour"
  and present it as the app's: offer a choice. Faithful = how the mark is
  actually used (often white on dark: plate `#3d3846`, chin with lighter corners -
  `chin_colors()` does this for dark faces), the other alternatives in HIG colours.
- `recolor.py ALT.svg --out-dir work/<app>/colours --sheet work/<app>/colours.png`
  renders the chosen alternative in all 7 HIG families so the user picks.
- White marks never stand alone (Free Symbol): they vanish on light wallpapers -
  colour the pieces instead (autodraft does this).

---

## Choosing the primary alternative (default order)

| Source class | Primary | Then |
|---|---|---|
| A tile glyph | Faithful plate | Disc, Rimmed, Symbol |
| B circular mark | Sound Disc | Rimmed, Symbol, Object |
| C free glyph | Free Symbol | Faithful plate, Disc |
| D letterform | Free Symbol | Faithful plate, Disc |
| E multicolour geometric | Faithful (own shape) | Disc, Rimmed |
| F radial/abstract | Free Symbol or Faithful plate | Disc, Rimmed |
| G mascot | Character | Disc/badge, Object |
| H game art | Mascot/emblem element #1 | elements #2, #3 |
| I object/UI | GNOME object | Faithful, Light |
| J photo/3D | Faithful (flattened) | Disc, Symbol |
| K lockup | Faithful (full lockup) | Free Symbol, symbol-only / letters-only variant, Disc |
| L monochrome mark | Faithful (as used, e.g. white on dark) | Disc / Rimmed / Symbol in HIG colours (colour sweep) |

The user may always override; record overrides in the brief and, if they are
standing preferences, in `lessons-and-rejections.md` of the skill copy you use.
