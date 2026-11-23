# anker_soundcore - design note (REDESIGN.md)

source: work/anker_soundcore/source.png (dark tile #000303, cyan glow #0dc4ed -> #08546c, white
  "ANKER soundcore" wordmark); the source's own colours are the cyan gradient
store: Soundcore (the companion app for Anker Soundcore speakers and earbuds)
kind: app
category: music
ladder: L1 (the wordmark on every style) + L2 (the audio gear the app controls)
characters: no
references: GNOME Mousai / Amberol (an audio object); the brand's cyan #0dc4ed.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the measured white "ANKER soundcore" wordmark on every style (put_mark) - source.png
  2. the brand cyan #0dc4ed (the source's own colour, kept on every style) - source.png
  3. the audio gear itself: a speaker, an earbuds case, headphones, an amplifier
function object (what the app does, as a physical thing): a speaker, an earbuds case, headphones,
  an amplifier.

concepts (work/anker_soundcore/concepts.png) - four different ideas (owner's ara-2 fixes applied,
2026-11-22):
  A: L2 - a wooden bookshelf speaker: brown cabinet, the wordmark on the baffle, one cyan-ringed (anchors 1, 2)
    woofer (main).
  B: L2 - an open earbuds case: the source's blue gradient on the lid with the wordmark, two white (anchors 1, 2)
    buds (Faithful).
  C: L2 round - over-ear headphones: dark band with a padded headband carrying the wordmark, two (anchors 1, 2)
    dark cups with cyan cushions (Disc).
  D: L2 - a hi-fi amplifier: silver face, a dark badge with the wordmark, two knobs, a cyan VU (anchors 1, 2)
    meter, feet (Rimmed).

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the owner's ara-2 fixes (work/anker_soundcore/fixes.md): the measured white wordmark (both
    lines) on every object, the source's blue gradient on the case lid, and a new Rimmed object
    (the soundbar was not recognisable) - an amplifier with knobs and a VU meter
  - the store lists this app under TOOLS; it is an audio-gear app, so the category is `music`
    (speaker, earbuds, headphones, amplifier), not a gear/settings object
  - the wordmark is never retyped: put_mark(ic, SLUG, box, face="#ffffff") places the measured glyph
  - the cyan #0dc4ed appears big on every style (gate mark_size: the app's own colour must read);
    on the amplifier it is the lit VU meter
  - four different dominant colours: brown (speaker), cyan (case), charcoal (headphones),
    silver (amplifier)
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31),
  brand cyan #0dc4ed / #0b84a5 / #08546c
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - the speaker and the case are plain square silhouettes (plain_shape WARN): both are real
    objects (a cabinet, a case), not plates
  - the wordmark costs small-size detail: the case is at 0.72 legibility32 (the limit); the buds
    are kept big and simple so it still reads at 32 px
