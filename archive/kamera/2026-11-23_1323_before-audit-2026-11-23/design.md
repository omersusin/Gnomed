# kamera - design note (REDESIGN.md)

source: work/kamera/source.png (black lens disc #000000, grey rings #383838 / #5d5d5d, red dot)
store: system app (Android Camera; GNOME Snapshot is the model)
kind: app
category: photo
ladder: L1 (the lens as an object) + L2 (a camera that carries the lens)
characters: no
references: GNOME Snapshot (a camera body), Android Camera (black lens with rings and a red dot).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the big round lens with a blue glass iris
  2. dark grey / black + a red accent
  3. the camera idea (shoot a photo)
function object (what the app does, as a physical thing): a camera - lens, camera body, film roll,
  film strip.

concepts (work/kamera/concepts.png) - four different ideas:
  A: L1 - a telephoto lens with a tripod foot and the red dot (closest to the source).
  B: L2 - a compact camera: body, big lens, red shutter, flash, viewfinder (main).
  C: L2 round - a 35 mm film roll: canister, hub with a real hole, strip coming out (Disc).
  D: L2 - a 35 mm film strip with sprocket holes and three exposures (Rimmed).

approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=B faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the lens keeps the source's black barrel, metal ring and red dot
  - the tripod foot on A keeps the faithful icon from being a plain disc (plain_shape)
  - four different photo objects: lens, camera, film roll, film strip
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names): Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d),
  Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
