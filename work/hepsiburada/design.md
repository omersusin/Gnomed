# hepsiburada - design note (REDESIGN.md)

source: work/hepsiburada/source.png
store: https://play.google.com/store/apps/details?id=com.pozitron.hepsiburada&hl=en&gl=US (SHOPPING, fetched 2026-11-22; refs/store/, not in git)
kind: app
category: shopping
ladder: L2 - delivery and shop objects carry the white wordmark
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): a dark product grid and white product pages with orange
  price and buy buttons; no characters, no mascot.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white lowercase wordmark "hepsi burada" in two lines (measured, rounded letters)
  2. the orange #fe5101 ground of the source tile
  3. a marketplace: parcels and a cart - everything for the home, not only clothes
function object (what the app does, as a physical thing): a parcel you ordered, on its way to your door

concepts (work/hepsiburada/concepts.png) - four different ideas:
  A: an orange delivery van with the white wordmark on its side panel (Symbol)
  B: a cardboard parcel with an orange label carrying the white wordmark (Faithful)
  C: a roll of packing tape: white tape, orange rim, a paper band with the wordmark (Disc)
  D: a shopping cart with the wordmark on its basket (Rimmed)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the shopping bag, price tag, hat box and wicker basket are trendyolmilla's; this app gets
    the delivery objects: parcel, shop sign, packing tape, cart (same_object).
  - Faithful is the parcel (its orange label is the logo applied to a real box); Symbol is the van - the app delivers.
  - the cart is deliberately large (a thin wire cart measured 0.30 mass on the phone).
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Orange 4 #e66100, Orange 5 #c64600, Light 2 #f6f5f4, Brown 3 #986a44, Dark 3 #3d3846
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
