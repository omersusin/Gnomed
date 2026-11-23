# qobuz - design note (REDESIGN.md)

source: work/qobuz/source.png
store: https://play.google.com/store/apps/details?id=com.qobuz.music&hl=en&gl=US (MUSIC_AND_AUDIO, fetched 2026-11-23; refs/store/, not in git)
kind: app
category: music
ladder: L2 - hi-fi studio objects carry the white wordmark
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): black hi-res player screens, large album artwork, white
  type on black; no characters, no mascot.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the lowercase white wordmark "qobuz" (measured, round geometric letters) - source.png
  2. black and white, no brand colour - the artwork brings the colour - source.png
  3. hi-fi / studio listening: better than streaming, lossless
function object (what the app does, as a physical thing): a studio microphone - music, recorded and played back in full quality

concepts (work/qobuz/concepts.png) - four different ideas:
  A: a studio condenser microphone on a shock mount, wordmark on its body (Symbol) (anchors 1, 2)
  B: an album sleeve: the white paper inner sleeve pulled half out of the dark cover, round die-cut window, wordmark on the smaller cover (Faithful) (anchors 1, 2)
shape-ok: the Faithful is an album sleeve (a real cardboard cover with the paper inner sleeve
  half out) - a flat square object, not a plate with the logo on it; the plain_shape WARN stays on
  purpose (2026-11-23).
  C: a compact disc: iridescent silver, dark label band with the wordmark (Disc) (anchors 1, 2)
  D: a mixing console: faders and knobs, white wordmark on the front panel (Rimmed) (anchors 1, 2)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the vinyl record, cassette, speaker, headphones, radio and pocket player are already used
    by deezer, anker_soundcore and apple_music; qobuz gets studio objects instead: microphone,
    album sleeve, CD, mixing console (same_object).
  - the CD's dark label band is the logo's white-on-black applied to a real disc.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 4 #241f31, Light 2 #f6f5f4, Light 4 #c0bfbc, Blue 1 #99c1f1, Red 1 #f66151
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
