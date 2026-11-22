# apple_music - design note (REDESIGN.md)

source: work/apple_music/source.png (dark tile #19191a, white note #f6f6f6, box 27 20 92 108);
  refs/store/icon.png is the same mark on a white tile with a black note. The measured shape is
  the two beamed eighth notes.
store: https://play.google.com/store/apps/details?id=com.apple.android.music&hl=en&gl=US
  (MUSIC_AND_AUDIO, fetched 2026-11-22; refs/store/: 6 screenshots + icon, not in git)
kind: app
category: music
ladder: L1 (the note as an object) and L2 (music objects carrying the note)
characters: no
references: 6 store screenshots (player UI, album grids, lyrics; mostly white/grey with the
  Apple Music red accent #ba594e -> Red ramp). No game screenshots needed.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the two beamed eighth notes (measured from source.png; never a font)
  2. the monochrome mark: white note on a dark field (store icon: black note on white)
  3. the Apple Music red accent (from the app UI; nearest HIG Red 2/3)
  4. one clean, premium object, no plate
function object (what the app does, as a physical thing): music playback - a note, a pocket
  music player, headphones, a speaker.

concepts (work/apple_music/concepts.png) - four different ideas:
  A: L1 - the measured note itself as a red enamel object with thickness and top light.
  B: L2 - a pocket music player: red body, recessed dark screen with the white note, click wheel.
  C: L2 - over-ear headphones: red cups, dark cushions, the white note on the right cup.
  D: L2 - a bookshelf speaker: red cabinet, dark badge with the white note, recessed woofer.

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: B - "Soru 1 cevabım: Ana tasarım B (cep müzik çalar)." (2026-11-22)
keep: A, C, D - "Kalsın: A, C ve D - hepsi. A -> Faithful, C -> Rimmed, D -> Disc." (2026-11-22)
final: "Tamam, pakete ekle." (2026-11-22)
styles: symbol=B faithful=A disc=D rimmed=C
decisions I made myself (and why; mention them in Q2):
  - four DIFFERENT music-family objects; no vinyl record (Deezer already uses it) and no cassette
    (Deezer's Rimmed slot uses it)
  - the note shape comes from source.png; the red is the app's UI accent mapped to HIG Red, not a
    drawn logo from memory
  - the note is white when printed on a dark screen/badge/cup (readable); A uses the red enamel
    version because a pure white note disappears on a light wallpaper (gate visible_light)
  - rough concepts first; only the chosen main + kept ones get polished
  - B is a real pocket player (not a tile): the top button breaks the square silhouette; the
    owner picked it as the main design
  - A's note is buffered +4.5 px so it reads at 32 px; C's note is 48 px on the right cup;
    D's note is 48 px on the round grille
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Red 1-5 (#f66151 #ed333b #e01b24 #c01c28 #a51d2d),
  Dark 1-4 (#77767b #5e5c64 #3d3846 #241f31), Light 1-4 (#ffffff #f6f5f4 #deddda #c0bfbc)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - gate: 36 PASS, 0 WARN, 0 FAIL; all four slots are different designs (slots)
  - visible: symbol light 0.85 / dark 0.76; faithful 0.99 / 1.00; disc 0.92 / 0.59;
    rimmed 0.92 / 1.00
  - baseline: symbol 118, faithful 118.5, disc 122, rimmed 122; mass 0.48 / 0.35 / 0.57 / 0.36
  - holes: the source note has no enclosed transparent holes (0.0% -> 0.0%)
  - weak: faithful is at the 0.35 mass limit (a note is thin); disc legibility 0.739 is close
    to the 0.72 limit; rimmed mass 0.36 is just above the limit; the red is the app's UI
    accent, not the monochrome store icon
