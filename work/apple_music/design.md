# apple_music - design note (REDESIGN.md)

source: work/apple_music/source.png (dark tile #19191a, white note #f6f6f6); refs/store/icon.png is
  the same mark on a white tile. The measured shape is the two beamed eighth notes.
store: https://play.google.com/store/apps/details?id=com.apple.android.music&hl=en&gl=US
  (MUSIC_AND_AUDIO; refs/store/: 6 screenshots + icon, not in git)
kind: app
category: music
ladder: L1 (the note itself) + L2 (players and instruments that carry the note)
characters: no
references: GNOME Mousai / Amberol (a music object); Apple Music red accent #ba594e -> HIG Red 2/3.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the measured Apple Music note (put_mark) on every style - source.png
  2. the Apple Music red accent (from the app UI; nearest HIG Red 2/3) - refs/store/ (the app's UI)
  3. music playback as a physical thing (a player, the note, a tambourine, a radio)
function object (what the app does, as a physical thing): a pocket music player, the note itself,
  a tambourine, a radio.

concepts (work/apple_music/concepts-round2.png) - four ideas (owner's ara-2 fixes applied,
2026-11-22; round 1 is in concepts-round1/):
  A: L2 - a pocket music player: silver body, dark screen with the note, red click wheel (main). (anchors 1, 2)
  B: L1 - the measured note itself as a thick red-pink object (Faithful, the closest to the logo). (anchors 1, 2)
  C: L2 round - a tambourine: blue wooden rim, cream skin with the note, chrome jingles (Disc). (anchors 1, 2)
  D: L2 - a vintage wooden radio: cream dial, the note on the dark grille, two knobs (Rimmed). (anchors 1, 2)

anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the owner's ara-2 fixes (work/apple_music/fixes.md): the measured note on every style, Faithful
    is the note itself, no cassette (Deezer's) and no record
  - the note is never redrawn: put_mark(ic, SLUG, box) places the measured glyph
  - four different dominant colours: silver (player), red (note), blue/cream (tambourine), wood
    (radio) - so the styles cannot merge (gate slots)
  - a tambourine is round, nameable and not a record: the note sits on its skin
  - the radio is the object the owner liked; only the note on its grille was added
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d),
  Blue 1-5 (#99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4), Brown 1-5 (#cdab8f #b5835a #986a44 #865e3c #63452c),
  Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc), Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate: 39 PASS, 4 WARN (symbol plain_shape, faithful mass 0.24, two same_object lines still read
    the old concepts until this file is saved), 0 FAIL; slots PASS
  - the note glyph is thin by nature: Faithful is the thinnest style (mass 0.24)
