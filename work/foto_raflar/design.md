# foto_raflar - design note (REDESIGN.md)

source: work/foto_raflar/source.png (the Photos pinwheel: yellow, red, blue and green petals on
  white; measured parts: yellow, red, blue, green)
store: system app (Android Photos; GNOME Loupe / Shotwell are the models)
kind: app
category: photo
ladder: L1 (a photo as an object) + L2 (a frame / loupe that carries the photo)
characters: no
references: GNOME Loupe (a loupe), Shotwell (a photo print), Android Photos (four-colour pinwheel).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the four pinwheel colours (blue, green, yellow, red) inside the photos
  2. a photo print with a white border
  3. looking at / keeping photos
function object (what the app does, as a physical thing): a photo - print, picture frame, loupe,
  stack of prints.

concepts (work/foto_raflar/concepts.png) - four different ideas:
  A: L1 - a photo print: white border and a landscape (closest to the logo's photo idea).
  B: L2 - a picture frame: blue frame, white mat, landscape (main).
  C: L2 round - a loupe over a photo: dark ring, glass, handle (Disc).
  D: L2 - a stack of prints fanned, the top one a landscape, a red clip (Rimmed).

approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=B faithful=A disc=C rimmed=D
warn-ok: same_object - photo prints are the gallery's own thing (GNOME Loupe); walpy keeps its print by the owner's fix list (work/walpy/fixes.md), and walpy's navy + squiggle tell the two apart
decisions I made myself (and why; mention them in Q2):
  - the source is a four-colour pinwheel (not an object); the four colours live on in the photos
  - camera lens and film roll already belong to kamera, so this app uses print/frame/loupe/stack
  - four different photo objects: print, picture frame, loupe, stack of prints
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4),
  Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269),
  Yellow 1-5 (#f9f06b #f8e45c #f6d32d #f5c211 #e5a50a),
  Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
