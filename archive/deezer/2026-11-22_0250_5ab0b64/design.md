# deezer - design note (REDESIGN.md)

source: work/deezer/source.png - the owner's OG Deezer logo (multicolour equaliser bars +
  white lowercase "deezer" wordmark on black), from the URL he gave on 2026-11-22. This
  replaces the purple-circle icon used earlier and the 2023 heart from the request zip.
kind: app
ladder: L1 / L2 - the measured multicolour bars as objects, or a music object carrying them
characters: no
references (games only): -
anchors (2-4 things that make the app recognisable; they must survive):
  1. the multicolour equaliser bars: 10 measured bars in 4 columns, box 17..111 x 17..79, stair silhouette (right column tallest, left column shortest)
  2. the OG palette: orange, red, magenta, blue, green, yellow (nearest HIG ramps)
  3. the white lowercase "deezer" wordmark on black - NOT used at icon size (unreadable at 32 px); the white labels in C/D echo it
function object (what the app does, as a physical thing): music playback - an equaliser
  sculpture, a speaker, a record, a cassette

concepts (work/deezer/concepts.png) - four different ideas:
  A: L1 - the measured multicolour bars, each bar one piece with one smooth gradient, no plate, on the baseline
  B: L2 - a deep-blue bookshelf speaker: light tweeter ring, multicolour bars as the grille
  C: L2 round - a vinyl record: dark grooves, a light rim ring, white label carrying the 5 measured columns, spindle hole
  D: L2 - a cassette tape: dark shell, two light reels, white label carrying the 5 measured columns

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: C - "Soru 1 cevabım: Ana tasarım C (plak)." (2026-11-22)
keep: A, D - "Kalsın: A ve D. B kalmasın." (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-22)
styles: symbol=C faithful=A disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - used the OG icon the owner asked for: the multicolour bars + white wordmark on black,
    not the purple circle or the 2023 heart from the request zip
  - the icon uses the bars, not the wordmark: the wordmark would be unreadable at 32 px
  - the owner's gradient fix: A uses regions(SLUG) + gradient(SLUG, bar), never parts() +
    colour() bands; every bar is one piece with one smooth source gradient
  - C got a light silver rim ring so the dark record does not disappear on a dark wallpaper;
    the label bars are enlarged (43..85 x 52..77) and use one gradient per column
  - layout from the owner: C = Symbol, A = Faithful, D = Rimmed, Disc = C; B is dropped
  - owner's change (2026-11-22): "Plağın ortasındaki beyaz etiketi ve içindeki renkli
    çubukları biraz büyüt, küçük boyutta da çubuklar seçilsin. Başka hiçbir şeyi
    değiştirme." -> C label radius 26 -> 30, bars box 48..92 x 58..82 -> 46..94 x 56..84;
    A, D, the sleeve and the rim are unchanged
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Orange 1-5, Red 1-5, Purple 1-5, Blue 1-5, Green 1-5,
  Yellow 1-5, Light 1-3 (#ffffff #f6f5f4 #deddda), Dark 3-4 (#3d3846 #241f31)
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
  - light: the white sleeve + silver rim read clearly; the label and coloured bars are bright
  - dark: the sleeve + rim keep the record visible (visible_dark 0.78); the dark record face
    is still subtle on a very dark wallpaper, but the outline is clear
  - holes: the spindle hole is transparent; no source holes to preserve in the bars
  - baseline: symbol/disc 120.0, faithful/rimmed 118.0 - inside the GNOME range
  - weak: A (Faithful) is a little thin (mass 0.30, one WARN); C's label is now larger
    (r=30) and its four coloured columns are readable at 32 px, but the bars are still a
    small cluster next to the sleeve/rim; D's visible_dark is 0.56, close to the threshold
  - decision: C got a light record sleeve behind it (not only the rim ring) so it is a real
    object, not a plain disc, and so it keeps its light mass on a dark wallpaper
  - owner's final change: the white label and the coloured bars were enlarged (label r=30,
    bars 46..94 x 56..84); A, D, the sleeve and the rim are unchanged
