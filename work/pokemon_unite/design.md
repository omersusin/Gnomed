# pokemon_unite - design note (REDESIGN.md)

source: work/pokemon_unite/source.png
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  - store icon (source.png): THREE heroes charging LEFT in a staggered row - an orange dragon
    at the back-left, the yellow electric mouse in the middle-front (red cheek, long ears with
    dark tips), a white rabbit striker with an orange brow at the right; purple sky, orange floor.
  - owner's screenshots (2026-11-21, refs/): key-art = the rabbit striker running, the mouse
    leaping with a glowing yellow energy orb, a GOLD RING with a blue inner face floating (the
    goal hoop); pikachu-select = the mouse in front view, long upright ears with black tips,
    red round cheeks, small eyes; 5v5-teams = purple team vs orange team; game-arena = a round
    arena with purple goals left / orange goals right; lobby, wardrobe, licence = UI only.
    -> composition: three heroes + the goal (gold ring) + energy orb; team colours purple/orange.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the three heroes charging left, the electric mouse in front (red cheek, dark ear tips)
  2. purple / orange team colours
  3. the gold goal ring + yellow energy orb
function object (what the app does, as a physical thing): scoring energy into the goal ring

concepts (work/pokemon_unite/concepts.png) - four different ideas:
  A: the store crop - three heroes in their staggered charge, the mouse in front
  B: the score - the mouse dunks an energy orb into the goal ring, the other two below
  C: round - the arena platform (purple half / orange half) with the three on it
  D: the goal ring as the frame, the three in front of it

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "A" (2026-11-21)
keep: B, C, D - "A,B,C,D,Ne yaparsan yap" (2026-11-21)
final: "Tamam, pakete ekle" (2026-11-21)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - keep: he ticked all and "Ne yaparsan yap"; A is the main, B (the dunk, closest to the
    key art) -> faithful, C (round arena) -> disc, D (goal ring) -> rimmed.
  - the goal is a GOLD ring with a blue inner face (key art), not purple as in the concepts.
techniques used (min. 3): thickness / material gradient / top light / glass (orb) / secondary object
palette (GNOME HIG names): Yellow 1-5, Orange 1-5, Light 1-5, Purple 1-5, Blue 3-5, Red 2-4
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate 30 PASS 1 WARN (faithful mass 0.38); size_audit 0 outside; weak: the dragon neck and rabbit chest in Symbol are blocky, three heads merge at 32 px, B is a bit small.
