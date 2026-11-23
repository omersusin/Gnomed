# y_hava_durumu - design note (REDESIGN.md)

source: work/y_hava_durumu/source.png (an orange-red umbrella #ff5739 with a dark handle on a
  light blue tile; the source's two dark arcs are dropped - no faces)
store: system app (Android Weather; GNOME Weather is the model)
kind: app
category: weather
ladder: L1 (a weather object) + L2 (a sky that carries the weather)
characters: no
references: GNOME Weather (sun + cloud), Android Weather (orange umbrella on light blue).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the orange-red umbrella (the source mark)
  2. red-orange + light blue (the source palette)
  3. the weather: sun, cloud, rain, temperature
function object (what the app does, as a physical thing): weather - umbrella, cloud + sun, sun,
  thermometer.

concepts (work/y_hava_durumu/concepts.png) - four different ideas:
  A: L1 - the source umbrella: red canopy with scallops, ribs and a dark J handle (closest).
  B: L2 - a sunset: a red sun behind a blue cloud (main).
  C: L1 round - a red sun: disc, eight rays, a light ring (Disc).
  D: L2 - a thermometer: scale plate, glass tube, big red bulb, ticks (Rimmed).

redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=B faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the source umbrella has two dark arcs that read as eyes; they are not drawn (no faces)
  - every style keeps a red element (the app's mark colour) at >= 36 px: canopy, sun, sun, bulb
  - four different weather objects: umbrella, cloud + sun, sun, thermometer
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d),
  Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
