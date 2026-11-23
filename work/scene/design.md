# scene - design note (REDESIGN.md)

source: work/scene/source.png
store: https://github.com/xingyeovo/HoshinoScene-oss (refs/store/store.json: "星野Scene - Android performance
  tuning: CPU/GPU frequency, temperature control, FPS monitor; Snapdragon and Dimensity"); no screenshots found
kind: app
category: system
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no - the Android head is the measured logo
references:
  - source.png: a blue tile with a darker dome at the top and a band across; in the middle a
    dark-blue circle with a yellow gear; the green Android head (antennas, white eyes) rising from
    the bottom edge.
  - refs/store/store.json: what it does - CPU/GPU frequency scaling, thermal control, FPS monitor.
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the green Android head #32de84 with antennas and white eyes - source.png
  2. the yellow gear #ffcc4b in its dark-blue circle - source.png
  3. the blue #5191ef of the tile - source.png
  4. what it tunes: the processor's frequency, its temperature, the FPS - refs/store/store.json
function object (what the app does, as a physical thing): a tuner for the phone's processor

concepts (Claude 2026-11-23, batch) - four different things, each carrying the measured logo:
  A: the processor - an SoC chip with gold pins, the logo on its blue lid (anchors 1, 2, 3, 4)
  B: the logo itself as an object - the Android head and the gear in its dark-blue circle (anchors 1, 2, 3)
  C: temperature control - a round cooling fan with blue blades, the logo on its hub (anchors 1, 2, 4)
  D: the performance gauge - a dial from green to red, the needle up high, the logo under it (anchors 1, 2, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - drawn by Claude
decisions I made myself (and why; mention them in Q2):
  - no screenshots exist (GitHub only): the anchors come from the logo and the app's description.
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Scene blue, Android green, gold (pins), Light 1-5, Dark 1-4, Red 3
review:
