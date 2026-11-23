# saat - design note (REDESIGN.md)

source: work/saat/source.png (green ring #106d1f with dark hands, centre is a real hole)
store: system app (Android Clock; GNOME Clocks is the model)
kind: app
category: system
ladder: L1 (the clock as an object) + L2 (a clock face that carries the mark)
characters: no
references: GNOME Clocks (a clock face), Android Clock (green ring + hands).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the round clock face with hands
  2. green (the source palette)
  3. the source's real centre hole (a skeleton ring)
function object (what the app does, as a physical thing): a clock - alarm clock, desk clock,
  stopwatch, digital clock.

concepts (work/saat/concepts.png) - four different ideas:
  A: L1 - an alarm clock: green body, two bells, legs and a skeleton face (main).
  B: L1 - a desk clock on a stand, round skeleton face (closest to the source ring).
  C: L1 round - a stopwatch: silver case, green skeleton dial, push button on top (Disc).
  D: L2 - a digital clock: green cabinet with a dark screen and 7-segment digits (Rimmed).

redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the source is a ring with hands, so the clock faces are skeleton rings: the centre stays
    transparent (check_icon holes) instead of painting a dial
  - the hands reach the rim so they are attached, not floating
  - four different clock objects: alarm clock, desk clock, stopwatch, digital clock
  - the owner: the Disc looked like a compass, so it is a stopwatch without a stand (2026-11-22)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
