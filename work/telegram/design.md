# telegram - design note (REDESIGN.md)

source: work/telegram/source.png
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white paper plane (measured from source.png: tip right-top, notch under the wing)
  2. Telegram blue #31a5df (between HIG Blue 2 and 3)
  3. the round shape (the blue circle)
function object (what the app does, as a physical thing): a message flying off - paper plane / message bubble

concepts (work/telegram/concepts.png):
  A (L1 the mark becomes an object): the paper plane as a folded blue paper object, no circle
  B (L2 a GNOME object that carries the mark): thick blue message bubble with a raised white paper plane
  C (L2): the circle as a blue glass sphere, a white paper plane flying out of it in front

  round 1 A/B/C rejected ("Hiçbiri, yeniden dene"); kept in concepts-round1/
  D (L2): the circle as a thick blue ring, the white paper plane flying through it
  E (L2): a blue volumetric cloud (cloud messenger), the white plane flying out in front
  F (L2): a blue envelope (like GNOME Mail), the paper plane is its stamp

approved: F - "Defaultu o mektup yap" (2026-11-19); in his Symbol style too: "Varsayılan mektup değil ama. Düzelt lütfen" (2026-11-19)
keep: D - "Select one and make others alt" (2026-11-19)   [D = ring -> Disc; his Q1 answer let me pick, I chose and he approved the board]
final: "Tamam" (2026-11-19)   [answer to the final board before the envelope became the default]
styles: faithful=F envelope, disc=D ring, symbol=F envelope (rimmed falls back to faithful) - owner: "Defaultu o mektup yap", then "Varsayılan mektup değil ama" (he uses the Symbol style); cloud kept only as work/telegram/telegram-cloud.svg
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names): Blue 1-5, Light 1-5 (paper plane)
review (48/32 px, light + dark wallpaper, what is still weak):
shape-note: the envelope is a box object; the owner chose it ("Defaultu o mektup yap") but never spoke about the square silhouette, so this is NOT a shape-ok (the gate keeps its WARN)
