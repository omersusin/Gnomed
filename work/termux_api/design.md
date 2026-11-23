# termux_api - design note (REDESIGN.md)

source: work/termux_api/source.png (black tile #000000, white `>_` #ffffff); refs: Uptodown listing
store: Termux:API (a Termux add-on that exposes Android APIs to the shell)
kind: app
category: dev
ladder: L1 (a dev object) + L2 (the terminal that carries the `>_`)
characters: no
references: GNOME Console / Builder / Sysprof (a dev object, never a robot).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the `>_` prompt (the source mark, drawn as thick strokes) - source.png
  2. black + white + terminal green - source.png
  3. the shell / the API to the device
function object (what the app does, as a physical thing): a terminal window, a circuit chip,
  a power plug (the socket the API plugs into), a toolbox.

concepts (work/termux_api/concepts.png) - four different ideas:
  A: L2 - a terminal window: light case, title bar, green `>_` on a dark screen (main). (anchors 1, 2)
  B: L2 - a circuit chip: green board, silver pins, dark die with `>_` (Faithful). (anchors 1, 2)
  C: L2 round - a round power plug: ivory body, two brass prongs, a strain relief, the prompt on it (Disc). (anchors 1, 2)
  D: L2 - a red toolbox with a steel handle and a green stripe (Rimmed). (anchors 1, 2)

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - Termux:API, Termux:Boot and Termux:Widget are three apps of one family, so they share the
    `dev` object family but take different objects (no terminal twice)
  - the `>_` mark is drawn with strokes, never a font
  - four different dominant colours: charcoal (window), green (chip), silver (spool), red (toolbox)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269), Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc),
  Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - the terminal window is a plain box silhouette (plain_shape WARN): it is a real window, not a plate
