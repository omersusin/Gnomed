# termux_widget - design note (REDESIGN.md)

source: work/termux_widget/source.png (black tile #000000, white `>_` #ffffff); refs: GitHub
store: Termux:Widget (puts Termux shortcuts on the home screen)
kind: app
category: productivity
ladder: L1 (a note/panel object) + L2 (the widget as a thing you stick on a surface)
characters: no
references: GNOME Notes / Text Editor (a note object); the source's `>_` mark.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the `>_` prompt (the family mark, written on every style)
  2. black + white + terminal green
  3. a small panel you stick on the home screen
function object (what the app does, as a physical thing): a sticky note, a clipboard, a rubber
  stamp, a notebook.

concepts (work/termux_widget/concepts.png) - four different ideas:
  A: L2 - a yellow sticky note with a curled corner and the prompt written on it (main).
  B: L2 - a clipboard: brown board, steel clip, white sheet with the prompt (Faithful).
  C: L2 round - a round rubber stamp seen from above: light dial, wood knob, dark prompt (Disc).
  D: L2 - a blue notebook with the prompt on its cover and a yellow ribbon (Rimmed).

approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the store calls this app PRODUCTIVITY, so it takes the note family (sticky note, clipboard,
    stamp, notebook) while Termux:API and Termux:Boot take the dev family
  - the notebook is blue, not green (ChatGPT's notebook is green - no look-alike in the batch)
  - four different dominant colours: yellow (note), brown (clipboard), charcoal (stamp), blue (book)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Yellow 1-5 (#f9f06b #f8e45c #f6d32d #f5c211 #e5a50a),
  Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - the sticky note and the clipboard are plain square silhouettes (plain_shape WARN): both are
    real objects (a note, a board), not plates
