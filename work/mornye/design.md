# mornye - design note (REDESIGN.md)

source: work/mornye/source.png
kind: app
category: music
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no
store: GitHub (refs/store/store.json "Mobile music utility built with Flutter and Rust. High-quality audio
  management for your personal library."; one screenshot sheet with four screens)
references:
  - source.png: a mint down-arrow between two short mint bars on a deep-teal tile.
  - refs/store/shot-1.jpg: Library (albums with soft blob artwork, dark-green pills), Now Playing
    ("Paper Moons": a magenta flower and a yellow sun, a wavy seek line, "FLAC · 24-bit · 48 kHz",
    maroon play/pause pill), Lyrics (pink), Equalizer ("Bass boost" on, the curve high in the bass,
    "Bit-perfect, Direct USB and exclusive Hi-Res outputs bypass EQ").
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the logo: a mint #bbebec down-arrow between two bars - source.png
  2. the deep teal #1e4d4f - source.png
  3. hi-res playback: "FLAC · 24-bit · 48 kHz", bit-perfect for DAPs - refs/store/shot-1.jpg, refs/store/store.json
  4. the "Paper Moons" art: a magenta flower and a yellow sun on pink, the wavy seek line - refs/store/shot-1.jpg
  5. the equalizer's "Bass boost" curve - refs/store/shot-1.jpg
function object (what the app does, as a physical thing): your own music, played bit-perfect

ideas (docs/METHOD.md §1b):
  description: "Bit-perfect, Direct USB and exclusive Hi-Res outputs" -> a digital audio player (DAP)
  content: "FLAC · 24-bit · 48 kHz" -> a hi-res player's screen
  screen: the "Paper Moons" flower art with the wavy seek line -> the player's screen
  screen: "Bass boost" and the curve -> a hardware equalizer with faders
  content: the volume slider, bit-perfect output -> an aluminium volume knob
  screen: Lyrics, "share them as a card" -> a lyric card (lines lose their detail at 32 px)
  logo: an arrow down into two bars -> the logo itself

worksheet (docs/METHOD.md §2):
  symbol (A):   idea=description  thing=a DAP  logo=mint on its teal body  silhouette=a tall player + wheel  main colour=teal + pink screen
  faithful (B): thing=the logo itself (sticker)  silhouette=the logo  main colour=teal + mint
  disc (C):     thing=a volume knob  logo=on the teal cap  silhouette=round + the scale ticks  main colour=aluminium
  rimmed (D):   thing=a hardware equalizer  logo=on its teal end plate  silhouette=a wide panel  main colour=light grey
  checks: four silhouettes different; no dark styles; no plate; every thing from an idea line

concepts (Claude 2026-11-23, the owner's comparison with Haiku) - four different things, each carrying the measured logo:
  A: "for DAPs" - a teal digital audio player, the flower art and the wavy seek line on its screen, the logo on its body (anchors 1, 2, 3, 4)
  B: the logo itself as a solid object - the mint arrow and bars on their teal die-cut (anchors 1, 2)
  C: bit-perfect volume - an aluminium knob on its mint scale, the logo on the teal cap (anchors 1, 2, 3)
  D: "Bass boost" - a hardware equalizer, four teal faders on the boost curve, the logo on the end plate (anchors 1, 2, 5)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Sen yap bakalım, öyle karar veririz" (2026-11-23) - drawn by Claude for the comparison with Haiku
decisions I made myself (and why; mention them in Q2):
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
