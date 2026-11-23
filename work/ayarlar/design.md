# ayarlar - design note (REDESIGN.md)

source: work/ayarlar/source.png (brown #884c29 gear + white #f5f5f4, real centre hole r 27.2)
store: system app (Android Settings; GNOME Settings is the model)
kind: app
category: system
ladder: L1 (the gear as an object) + L2 (a settings tool)
characters: no
references: Android Settings / GNOME Settings: a gear, a control panel, a knob, a wrench.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the gear with its real centre hole
  2. brown + white (the source palette)
  3. the "control / adjust" idea
function object (what the app does, as a physical thing): a gear, a wrench, a control knob,
  a control panel with sliders.

concepts (work/ayarlar/concepts.png) - four different ideas:
  A: L1 - the plain brown gear as an object (main; the source logo itself).
  B: L2 - a steel wrench crossed over a screwdriver with a fluted brown handle (Faithful).
  C: L2 round - a brown control knob with tick marks and a pointer (Disc).
  D: L2 - a settings panel with two switches and a slider (Rimmed).

approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - system app: the GNOME Settings gear is the metaphor; brown is kept from the source
  - the gear has a real transparent hole (source hole r 27.2 -> transparent)
  - four different objects: gear, crossed tools, knob, switch/slider panel
  - the owner swapped Symbol/Faithful (2026-11-22): the gear is the main, the tools are Faithful
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
