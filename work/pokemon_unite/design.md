# pokemon_unite - design note (REDESIGN.md)

source: work/pokemon_unite/source.png
store: https://play.google.com/store/apps/details?id=jp.pokemon.pokemonunite&hl=en&gl=US (GAME_ACTION, fetched 2026-11-22; refs/store/, not in git)
kind: game
category: game
ladder: game objects - goal ring + energy ball
characters: no
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
  -> rule 2026-11-21 "Karakter yok, oyunun nesnesi": only the OBJECTS: the gold goal ring
     (blue inner face), the glowing yellow energy ball, the two team balls of the UNITE logo
     (orange / purple top, white bottom, dark band); team colours purple / orange.
  history: round 3 (three characters, shipped 2026-11-21) dropped by this rule -> concepts-round3/.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the gold goal ring with the blue inner face
  2. the ball (glowing energy / the team balls)
  3. purple / orange team colours
function object (what the app does, as a physical thing): the ball going into the goal ring

concepts (work/pokemon_unite/concepts.png) - four different ideas, objects only:
  A: the ring standing on its edge, the energy ball in front of it (key art)
  B: the stadium goal: the ring on a metal post, the energy ball dunking into it
  C: round: the arena (purple / orange) with the ring lying on it, the ball above
  D: the ring + the two team balls (orange / purple, from the UNITE logo)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: B - "B" (2026-11-21)
keep: A - "A,A'daki halkanın içindeki mavi hilali kaldır." (2026-11-21)
final: "Tamam, pakete ekle" (2026-11-21)
styles: symbol=B faithful=A disc=B rimmed=B
decisions I made myself (and why; mention them in Q2):
  - A (the only kept one) -> faithful; disc and rimmed get the main B (save_styles fallback).
  - the blue crescent is removed in A only (his words name A); B keeps it.
  - Q2 round 1, owner: "B'deki mavi hilali de kaldır. Simgeyi yaklaşık %10 büyüt, direği biraz
    kalınlaştır (32 px'te kaybolmasın)." -> crescent removed in B; B was already 112 px tall
    (6..118), so the ring grew wider (88 -> 98 px) and taller (80 -> 84 px), the ball 17 -> 19,
    the post shorter; post 10 -> 14 px wide.
techniques used (min. 3): thickness / material gradient / top light / glass / secondary object
palette (GNOME HIG names): Yellow 1-5 + Orange 5 (gold), Blue 3-5, Purple 1-4, Orange 1-4, Light 1-5, Dark 3
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate 28 PASS 3 WARN (mass: faithful 0.29, disc/rimmed 0.37); size_audit 0 outside; weak: A is thin.
