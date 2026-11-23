# enpara - design note (REDESIGN.md)

source: work/enpara/source.png
store: https://play.google.com/store/apps/details?id=com.enparabank.retail&hl=en&gl=US (FINANCE, fetched 2026-11-23; refs/store/, not in git)
kind: app
category: finance
ladder: L2 - a bank card, a wallet, a coin and a safe carry the magenta "en"
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): a white banking app with a magenta "en" and four colour bars;
  no characters, no mascot.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the magenta "en" wordmark (measured, rounded geometric letters)
  2. the four-colour palette: magenta #aa519e, orange #faa91a, green #9ec842, blue #26abe2
  3. a digital bank: a card, a wallet, money - not a branch building
function object (what the app does, as a physical thing): a bank card you pay with

concepts (work/enpara/concepts.png) - four different ideas:
  A: a bank card: white card, magenta en, a chip and a four-colour edge stripe (Symbol)
  B: the measured en as one solid magenta object standing on the source's four-colour stripe (Faithful)
  C: a coin: golden rim, magenta en embossed, a milled edge (Disc)
  D: a safe door: steel door, two dark hinges, a big round dial with ticks, a handle, the en on a small plate (Rimmed)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the card, wallet, coin and safe are all free in this category, so this app takes one of each
    (same_object) - no other finance app has to give up its object.
  - the source's bottom colour bar becomes the four-colour stripe on the card edge (A), not a
    plate: the app's palette survives on a real object.
  - the measured "en" sits inside the purple ring segment of the source; geometry.json
  - the Faithful's four-colour stripe is the source's own bottom bar; the Rimmed safe carries the en
    on a small white plate so the door, not the wordmark, is the object (REDESIGN 5, cover-the-mark).

    `mark_keep` r1 + `mark_crop` keeps the two letters and drops the ring arc and the colour bar.
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Purple 3 #9141ac, Orange 2 #ffbe6f, Green 3 #8ff0a4, Blue 3 #3584e4, Light 2 #f6f5f4
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
