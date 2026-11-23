# walpy - design note (REDESIGN.md)

source: work/walpy/source.png (flat navy tile #1b242e, white squiggle #f4f4f5, 6.8% of the
  tile); the squiggle is the measured mark on every style
store: Walpy - Wallpapers (a new Unsplash wallpaper every day; Google Play, PERSONALIZATION)
kind: app
category: photo
ladder: L1 (the squiggle) + L2 (wallpaper as a physical thing: a roller, a roll of paper, prints)
characters: no
references: GNOME Loupe / Snapshot (a photo object); the source's navy + white.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the measured white squiggle on every style (put_mark) - source.png
  2. the source's navy #1b242e - source.png
  3. wallpaper as a physical thing: a paint roller, a roll of wallpaper, prints on a line
function object (what the app does, as a physical thing): a paint roller, a roll of wallpaper,
  a photo print, prints drying on a line.

concepts (work/walpy/concepts.png) - four different ideas (owner's ara-2 fixes applied,
2026-11-22):
  A: L2 - a paint roller: navy roller with the squiggle, steel arm, wooden handle (main). (anchors 1, 2)
  B: L2 - a photo print: white border, navy image with the squiggle, a caption line (Faithful). (anchors 1, 2)
  C: L2 round - the end of a wallpaper roll: yellow spiral, cardboard core with a real hole, the (anchors 1, 2)
    squiggle on the wrap, a peeling flap (Disc).
  D: L2 - prints drying on a line: brown rope, three kraft prints, the big centre print carries (anchors 1, 2)
    the squiggle (Rimmed).

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the store labels this app PERSONALIZATION; a wallpaper app is a photo app (Unsplash
    wallpapers), so the category is `photo` and the objects are photo/wallpaper objects
  - the owner's ara-2 fixes (work/walpy/fixes.md): the unnameable blue cylinder became a paint
    roller, the film canister became the end of a wallpaper roll (round, with a real core hole)
  - the squiggle is never retyped: put_mark(ic, SLUG, box, face=...) places the measured glyph
  - the Rimmed line keeps the prints, but only the big centre print carries the mark: three
    small copies broke the mark gate (shape match 0.25)
  - four different dominant colours: navy (roller), white (photo print), yellow (roll end),
    kraft brown (prints on the line)
  - Faithful and Rimmed share the photo-print object with foto_raflar/kamera (same_object WARN):
    allowed by REDESIGN.md 3 - walpy's navy + the measured squiggle >= 42 px make them read as
    a different app, and the owner's fix list keeps those two styles unchanged
techniques used (min. 3): thickness / material gradient / top light / hole / secondary object
palette (GNOME HIG names): Yellow 1-5 (#f9f06b #f8e45c #f6d32d #f5c211 #e5a50a),
  Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c), Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc),
  Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31), source navy #1b242e / #2c3d56
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - the photo print is a plain square silhouette (plain_shape WARN): it is a real flat print
    with a border, not a plate
  - the disc's mark is 38 px, just over the mark_size floor; the spiral is subtle by design
  - the symbol's handle ends at 118 + 5 depth = 123, inside the 108-126 free-object baseline
warn-ok: same_object - "the owner's fix list keeps Faithful and Rimmed as they are (a photo print and prints on a line); walpy's navy and the measured 42-56 px squiggle make both read as this app, not foto_raflar/kamera."
