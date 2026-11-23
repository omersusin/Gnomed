# ki_iler - design note (REDESIGN.md)

source: work/ki_iler/source.png (white person silhouette on a green tile - a face/character, so
  it is NOT drawn: REDESIGN.md 3b says objects only)
store: system app (Android Contacts; GNOME Contacts is the model)
kind: app
category: messaging (fetch_refs; Contacts has no family of its own, so the address-book objects
  below are used and noted here)
ladder: L1 (a contact card) + L2 (an address book that carries the contact)
characters: no (the source's person is deliberately replaced by objects)
references: GNOME Contacts (a card / address book), Android Contacts (green + white).
anchors (2-4 things that make the app recognisable; they must survive):
  1. the "a person's details on a card" idea (without drawing a person)
  2. green + white (the source palette)
  3. an address book / card index
function object (what the app does, as a physical thing): an address book - a contact card,
  an address book, a rolodex, a card file box.

concepts (work/ki_iler/concepts.png) - four different ideas:
  A: L1 - a contact card: green header, three detail lines, a corner tab (closest to the logo).
  B: L2 - an address book: cover, spine, page block, red bookmark, letter tab (main).
  C: L2 round - a rolodex: fanned cards on a round wheel with a base (Disc).
  D: L2 - a card file box: green box with tabbed cards and a front label (Rimmed).

redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: B - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: A, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=B faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the source draws a person (head + shoulders); the rules forbid characters, so the four
    concepts are contact objects instead, and the card keeps an empty header seal (not a face)
  - four different contact objects: card, address book, rolodex, card file box
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
