# rush_royale - design note (REDESIGN.md)

source: work/rush_royale/source.png
store: https://play.google.com/store/apps/details?id=com.my.defense&hl=en&gl=US (GAME_STRATEGY, fetched 2026-11-22; refs/store/, not in git)
kind: game
category: game
ladder: game objects - wizard hat + ice crystals
characters: no
references (games: store icon + >= 2 in-game screenshots; objects only, REDESIGN 3b):
  - store icon: a purple wizard hat (wide brim, pointed crown) with a gold crown band and a
    magenta gem in a diamond setting, two glowing ice-blue crystals, a green checkered board.
  - in-game screenshots: none yet (asked in Q1).
  history: the earlier "approved:" line was written by the agent, not the owner (MISTAKES 10);
    round 1-2 concepts -> concepts-round1/, concepts-round2/.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the purple wizard hat
  2. the gold crown band with the magenta gem
  3. the ice-blue crystals / the green tile board
function object (what the app does, as a physical thing): the hat as a game piece on the board

concepts (work/rush_royale/concepts.png) - four different ideas, objects only:
  A: the wizard hat alone (felt, gold band, gem)
  B: the hat standing on the green tile board
  C: the hat with the two glowing crystals
  D: round: a round green tile with the hat and one crystal

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: C - "C" (2026-11-21)
keep: D - "D,Şapkanın kenarını kaynaktaki gibi daha geniş ve kıvrık yap, ortadaki taş pembe/macenta olsun." (2026-11-21)
final: "Tamam, pakete ekle" (2026-11-21)
styles: symbol=C faithful=C disc=D rimmed=C
decisions I made myself (and why; mention them in Q2):
  - Q2 round 1, owner: "Simgeyi yaklaşık %10 büyüt; şapka ve kristaller telefonda komşuları
    kadar dolu görünsün." -> hat 100 -> 110 (brim width kept inside 8..120), crystals 15 -> 17,
    D hat 88 -> 96, crystal 11 -> 13.
  - D is round -> disc; faithful and rimmed get the main C.
  - his Q1 note: brim wider and curled like the source, the gem pink/magenta -> done in C and D
    (gem #f8a5d4 -> #e0379c -> #a51d6e: no magenta ramp in the HIG, between Purple and Red).
techniques used (min. 3): thickness / material gradient / top light / glass / secondary object
palette (GNOME HIG names): Purple + measured violet #4434ac..#b39af5, Yellow 1-5 (gold), Blue 1-5, Green 1-5
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate 28 PASS 3 WARN (mass 0.36 / disc 0.39); size_audit 0 outside; weak: a wide, low object looks a little thin; the magenta gem is outside the HIG palette.
