# terminal_em_lat_r - design note (REDESIGN.md)

source: work/terminal_em_lat_r/source.png
store: https://play.google.com/store/apps/details?id=com.termoneplus&hl=en&gl=US (DEV, fetched 2026-11-23; refs/store/, not in git)
kind: app
category: dev
ladder: L2 - a software package and a server rack carry the white mark
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): a dark terminal with green prompt text; no characters.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white "> 1+" prompt line and the "Term" word under it (measured)
  2. the slate #678390 and lime #a6c73d of the source tile
  3. a terminal app for Android: a package you install, a machine you log into
function object (what the app does, as a physical thing): a terminal session on a machine - a box you open and a server you connect to

concepts (work/terminal_em_lat_r/concepts.png) - four different ideas:
  A: a software package box with the white mark on its label (Symbol)
  B: the measured "> 1+ Term" mark itself as a slate object standing on a wide lime plinth (Faithful)
  C: an install disc: silver disc, rim and shine, spindle hole and hub, the mark on the lime label (Disc)
  D: a rack server front: slate chassis, lime bezel, dark bay recess with two caddies, LEDs, mark on a small label (Rimmed)
shape-ok: the Symbol is a software package box - a real box object you install from, not a plate with
  the logo on it; the plain_shape WARN stays on purpose (2026-11-23).


# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the terminal window, circuit chip and toolbox/wrench are all taken by termux_api; this app
    gets the package box, the mark itself, an install disc and a server rack (same_object).
  - the measured mark is the white "> 1+ Term" lettering; the slate body and the green wave are
    the tile, so geometry.json lists them as ground (mark_skip r0/r1) and forces the white text
    in (mark_keep r2) - without it the gate compared the tile.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 2 #5e5c64, Light 2 #f6f5f4, Green 3 #8ff0a4, Blue 3 #3584e4
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
