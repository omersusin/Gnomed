# hesap_makinesi - design note (REDESIGN.md)

source: work/hesap_makinesi/source.png (blue-grey calculator with white + and = keys, plus a row
  of stationery: ruler, pen, compass, highlighter, pencil)
store: system app (Android Calculator; GNOME Calculator is the model)
kind: app
category: system
ladder: L1 (a calculating object) + L2 (a machine that calculates)
characters: no
references: GNOME Calculator (a keypad), Android Calculator (blue-grey + big + / = keys).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the + and = keys (the source's two big keys)
  2. blue-grey + white (the source palette)
  3. calculating: keys, beads, scales
function object (what the app does, as a physical thing): a calculator - pocket calculator,
  abacus, circular slide rule, adding machine.

concepts (work/hesap_makinesi/concepts.png) - four different ideas:
  A: L1 - a pocket calculator with a green display and big + / = keys (closest to the logo).
  B: L1 - an abacus: blue-grey frame, three rods, five beads each (main).
  C: L1 round - a circular slide rule: scales, ticks, red cursor, hub (Disc).
  D: L2 - an adding machine: keypad, paper roll with printed tape, red crank (Rimmed).

redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=B faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the source's stationery row (ruler, pencil ...) is not the calculator's function, so it is
    dropped; the + and = keys and the blue-grey palette stay
  - four different calculating objects: calculator, abacus, circular slide rule, adding machine
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d), Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
