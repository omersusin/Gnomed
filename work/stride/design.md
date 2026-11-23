# stride - design note (REDESIGN.md)

source: work/stride/source.png
kind: app
category: health
ladder: L2 object carries the mark (A, C, D) + L1 the logo itself (B)
characters: no
references: source.png + refs/store/shot-1..6.jpg (the dark/light step screen, the wavy goal
  ring, the weekly bars, the awards/streak screen, the walk map)

anchors (2-4 things that make THIS app recognisable, seen in source.png and the screenshots in
  work/stride/refs/store/ - each with its real colour and WHERE you saw it; they must survive):
  1. the runner - the mint-green running figure with a wave under its feet (gradient #a4f19b -> #58d89a -> #0dbf9a, dark-teal outline #12503d) - source.png / refs/store/icon.png
  2. the wavy goal ring - the scalloped mint ring (#76d2c5) around "6,842 of 8,000 steps" on the near-black card (#0b0f0f), deep teal (#00554e) in the light theme - refs/store/shot-2.jpg, refs/store/shot-3.jpg
  3. the awards/streak badge - the 15-day ring, the olive-lime progress bars and the flame on the cream card (#e1eae2) - refs/store/shot-5.jpg
  4. the walk map - the light-blue water (#a6d0dc) and cream land (#f6f5f4) map with the route and the lime "Start a walk" pill (#b7ce74) - refs/store/shot-6.jpg
function object (what the app does, as a physical thing): a running shoe that counts every step;
  the daily step goal as a wavy-ring medal; a folded walking map.

ideas (docs/METHOD.md §1b - at least 6 lines, from different sources; QUOTE the words you read):
  slogan: "Every step, counted" -> a running shoe, the thing that takes the step
  slogan: "Streaks that keep you going" -> the 15-day award rosette (wavy ring + ribbon)
  screen: the scalloped goal ring around "6,842 of 8,000 steps" -> a goal medal
  screen: "Your week at a glance" -> the seven olive bars of the week
  screen: "Track your walks" -> a folded map with the route and a pin
  content: "6,842 of 8,000 steps" and "1,158 steps to go" -> the goal ring / a medal
  name: "Stride" (a long step) -> the running shoe / its long sole
  description: "Step counter & pedometer: track steps, calories, walks, runs and daily goals" -> a shoe
  logo: the mint runner with the wave -> the runner itself (Faithful)

worksheet (docs/METHOD.md §2 - fill it BEFORE drawing; one line per style):
  symbol (A):   idea=slogan "Every step, counted"  thing=a running shoe, its sole the wavy goal ring  logo=on the dark ankle panel  silhouette=shoe  main colour=mint green #58d89a
  faithful (B): thing=the logo itself (put_mark body=7)  silhouette=the runner  main colour=the logo's green gradient
  disc (C):     thing=the goal ring as an award rosette (wavy edge + ribbon)  logo=in the near-black centre  silhouette=round + ribbon tails  main colour=mint #76d2c5
  rimmed (D):   thing=a folded walking map with the route and a pin  logo=on the dark map label  silhouette=paper map  main colour=cream + light blue
  checks: four different silhouettes? yes (shoe / runner / rosette / map). at most two main colours
  black/charcoal? no style is all-black (the rosette's centre and the shoe's panel are small dark
  parts). NO plain plate (disc, tile, kite, shield) behind the logo? no. every thing named by an
  anchor? yes. no UI card / list / screen drawn small? no.

concepts (work/stride/concepts.png) - four different ideas, EACH carrying anchors (cite them):
  A: a mint running shoe with the wavy goal-ring sole, the logo on the dark ankle patch (anchors 1, 2)
  B: the logo itself as a solid object - the mint runner with its wave and dark-teal side (anchors 1, 2)
  C: the wavy goal ring as an award rosette with a ribbon, the logo in its near-black centre (anchors 1, 2, 3)
  D: a folded walking map with a route and a lime pin, the logo on its dark label (anchors 1, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-23)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-23)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - main = A (the running shoe): "Every step, counted" is the first store headline and the shoe is the
    boldest non-round thing of a step counter; its wavy sole carries the app's signature goal ring.
  - the Disc is an award rosette, not a plain disc: the wavy edge is the app's goal ring and the ribbon
    breaks the circle (a medal, from the Awards screen).
  - the Rimmed is the walk map, not a second step device: "Track your walks" is the app's fourth
    feature and gives a different silhouette and the map's blue/green.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
  thickness, material gradients, top light, recess (collar, medal centre, map label), a curled map corner.
palette (GNOME HIG names):
  Green 2-4 (#57e389, #33d17a, #2ec27e), mint/teal #76d2c5, Dark 3-4 (#3d3846, #241f31),
  Light 1-3 (#ffffff, #f6f5f4, #deddda), lime #b7ce74, Blue 1-2 (#99c1f1, #62a0ea)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  Light + dark both read: the shoe's mint upper, the faithful's green runner on its deep-teal
  die-cut sticker, the medal's mint band and the map's cream paper keep their shape. Baselines:
  shoe 118, faithful 118.5, disc 119.5 (ribbon tails 118), map 118. Holes: none in the source, none
  painted over the mark. Weak: the shoe's high ankle reads a little boot-like at 32 px; the medal's
  two ribbon tails are small at 32 px; the map's fold lines and water patch fade at 32 px (the route,
  pin and dark label carry it).
