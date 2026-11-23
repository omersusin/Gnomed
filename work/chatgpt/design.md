# chatgpt - design note (REDESIGN.md)

source: work/chatgpt/source.png (white field #ffffff, black knot #040404; the traced knot is in
  work/chatgpt/geometry.json -> parts.knot, and it has real enclosed holes)
store: https://play.google.com/store/apps/details?id=com.openai.chatgpt (AI assistant; Play lists it
  under PRODUCTIVITY, the object family here is `ai` - it is an assistant, not an office tool)
kind: app
category: ai
ladder: L1 (the knot as an object) + L2 (the assistant's objects: bulb, bubble, notebook)
characters: no
references: GNOME Newelle / Alpaca (an assistant as an object); OpenAI's knot mark.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the measured knot (never redrawn from memory; geometry.json parts.knot) - source.png
  2. monochrome black + white (the source palette) - source.png
  3. asking and getting an answer: a bulb, a bubble, a notebook
function object (what the app does, as a physical thing): an assistant - a lightbulb (an idea), a
  chat bubble (an answer), a notebook (notes), the knot itself.

concepts (work/chatgpt/concepts.png) - four different ideas:
  A: L2 - a lit lightbulb: yellow glass, the measured knot on the bulb, steel screw base (main). (anchors 1, 2)
  B: L1 - the measured knot as a thick dark object with light edges (Faithful, closest to the logo). (anchors 1, 2)
  C: L2 round - a round chat bubble with the measured knot printed on it, its counters real holes (Disc). (anchors 1, 2)
  D: L2 - a green notebook with the knot printed on its cover (Rimmed). (anchors 1, 2)

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the store calls it PRODUCTIVITY; it is an assistant, so the `ai` family (bulb, crystal, bubble,
    notebook) fits the app's function better than a notebook-only family
  - the knot is never drawn from memory: it comes from the traced source (parts.knot); on the
    bulb it replaces the old filament (the owner read the zigzag as an "M", ara-2)
  - the Disc is a bubble with the knot cut OUT (a real hole): the source knot has big enclosed
    holes, so a solid bubble in the mark's place would paint over them (gate holes)
  - four different dominant colours: yellow (bulb), charcoal (knot), white (bubble), green (notebook)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Yellow 1-5 (#f9f06b #f8e45c #f6d32d #f5c211 #e5a50a),
  Green 1-5 (#8ff0a4 #57e389 #33d17a #2ec27e #26a269),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate: see the build line below; the bulb is the thinnest style (mass ~0.21)
  - the knot as a hole in the bubble keeps the source's real holes transparent
