# duolingo - design note (REDESIGN.md)

source: work/duolingo/source.png
kind: app
category: learning
ladder: L2 - the lesson's objects (cards, book, globe, chalkboard)
characters: no - but the LOGO is Duo's face, so the measured face is the mark on every style
  (REDESIGN 5 "A mascot logo is still the logo"); no body, no pose drawn from memory.
mark: the measured face - geometry.json keeps the light-green head (mark_keep r0, mark_round 10:
  the source tile cuts the head at both sides, the cut corners are rounded)
store: refs/store/ (6 screenshots + icon.png, fetched by tools/fetch_refs.py)
references:
  - source.png: Duo's face - light-green head with two tufts, big white eyes with dark pupils,
    an orange beak - on the Duolingo green tile.
  - shot-1 courses list; shot-2 "Select the correct image" (white answer cards, blue sound button,
    green progress bar); shot-3 chess puzzle; shot-4 "Translate this sentence" (a character's white
    speech bubble with the blue sound button, "I need more coffee!"); shot-5 a cafe ("Je voudrais un
    café"); shot-6 the streak: a big orange flame with Duo beside it, "3 day streak".
old anchors (DeepSeek, round 1): Duolingo green; a lesson card with "Aa"; languages
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. Duo's face: light-green head #89e219 with tufts, white eyes, dark pupils #4b4b4b, orange beak
     #ffc200 / #f48000 - source.png
  2. Duolingo green #58cc02 - source.png (the tile), the buttons and progress bars of refs/store/shot-2.jpg
  3. the streak flame: orange #ff9600 with a yellow core, "day streak" - refs/store/shot-6.jpg
  4. the white speech bubble with the blue sound button #1cb0f6 - refs/store/shot-2.jpg, shot-4.jpg, shot-5.jpg
  5. coffee - the cafe lessons ("¡Necesito más café!", "Je voudrais un café") - refs/store/shot-4.jpg, shot-5.jpg
function object (what the app does, as a physical thing): a short daily lesson you keep a streak of

old concepts (round 1, DeepSeek, objects only, no owl; archive/duolingo/*deepseek-objects):
  old A: flash cards with "Aa"  old B: a green dictionary  old C: a globe  old D: a chalkboard
concepts (round 2, Claude 2026-11-23) - four different things, each carrying Duo's face:
  A: the daily streak - the orange streak flame with its yellow core, Duo's face in front (anchors 1, 3)
  B: Duo's head itself as a solid object, the Duolingo green as its thickness (anchors 1, 2)
  C: a cup of coffee from above on its saucer, Duo's face in the foam (anchors 1, 5)
  D: the white speech bubble with the blue sound button, Duo's face speaking it (anchors 1, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - redrawn by Claude with the logo
decisions I made myself (and why; mention them in Q2):
  - Duo's face in every style: it is the logo (the owner: "Oyunlarda ve uygulamalarda hassas olmalı",
    2026-11-23); the old round drew school objects any learning app could have.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
