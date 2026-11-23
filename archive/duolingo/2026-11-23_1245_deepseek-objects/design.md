# duolingo - design note (REDESIGN.md)

source: work/duolingo/source.png
kind: app
category: learning
ladder: L2 - the lesson's objects (cards, book, globe, chalkboard)
characters: no
mark: none - the logo is Duolingo's owl, a mascot; no character/face is drawn (HIG, REDESIGN 3b).
  The brand colours (Duolingo green #58cc02 / #89e219, orange) carry the identity instead, so
  mark_size still measures them.
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  - store icon: the green owl mascot on a green tile (a face - not drawn; mascots are dropped).
  - screenshots: white lesson cards on a very pale background, Duolingo green buttons, orange and
    yellow accents, a green progress bar.
anchors (2-4 things that make the app recognisable; they must survive):
  1. Duolingo green (#58cc02 / #89e219) - the brand, on every object
  2. the lesson card with "Aa" - a language exercise (the owl is a mascot: dropped)
  3. short, playful lessons and the world's languages
function object (what the app does, as a physical thing): a language lesson you hold: flash cards
  you turn, the dictionary of words, the globe of languages, the classroom chalkboard

concepts (work/duolingo/concepts.png) - four different ideas (objects only, no mascot):
  A: a fan of flash cards, the front green one with white "Aa" (the lesson itself)
  B: a green dictionary - thick cover, white page block, orange bookmark, index tabs (the words)
  C: a globe - light-blue ocean, green continents, steel meridian arc and round base (the languages)
  D: a classroom chalkboard - green board in a wooden frame, chalk tray, orange chalk, eraser
shape-ok: the Faithful dictionary is a real closed book (green cover, white page block on the
  right, spine, orange bookmark, index tabs) - a square object, not a plate with a logo on it;
  the plain_shape WARN stays on purpose (2026-11-23).

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - no owl: the store logo is a mascot; objects only (REDESIGN 3b / HIG). The "Aa" on the card and
    the chalk A are generic lesson content, not a logo from memory.
  - the four styles use four different learning objects (cards / book / globe / board) so a category
    of vocabulary apps can share them out later.
  - mark: none - gate mark is skipped on purpose; the green brand colour is in every style and
    mark_size measures it.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
