# termux_boot - design note (REDESIGN.md)

source: work/termux_boot/source.png (black tile #000000, white `>_` #ffffff); refs: F-Droid listing
store: Termux:Boot (runs scripts when the device boots)
kind: app
category: dev
ladder: L1 (the >_ prompt) + L2 (starting up: an ignition key, a power button, a boot disc)
characters: no
references: GNOME Console / Builder (a dev object, never a robot).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the `>_` prompt (the family mark; kept on the labels) - source.png
  2. black + white + terminal green - source.png
  3. starting the system: a drive, a power button, a boot disc
function object (what the app does, as a physical thing): an ignition key, the shell prompt, a power
  button, a compact disc.

concepts (work/termux_boot/concepts.png) - four different ideas:
  A: L2 - an ignition key: a dark round bow with the prompt, a steel blade and two teeth (main). (anchors 1, 2)
  B: L1 - the shell prompt itself: the measured mark, white on a thick Termux-black slab (Faithful). (anchors 1, 2)
  C: L2 round - a round power button: steel bezel, dark cap with the prompt, a green LED ring (Disc). (anchors 1, 2)
  D: L2 round - a boot CD with a white label: silver disc, iridescent rim, the prompt on the label, a real centre hole (Rimmed). (anchors 1, 2)

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - no terminal window here (Termux:API has it); booting is shown as the things you boot from
  - the power glyph is drawn as an arc + a bar, not a font
  - four different dominant colours: charcoal (drive), cardboard (package), silver (button),
    blue/violet (disc)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c), Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc),
  Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269), Blue 1-5, Purple 1-5
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - the package is a plain box silhouette (plain_shape WARN): it is a real box, not a plate
