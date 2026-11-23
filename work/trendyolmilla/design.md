# trendyolmilla - design note (REDESIGN.md)

source: work/trendyolmilla/source.png
store: https://play.google.com/store/apps/details?id=com.trendyol.milla.android&hl=en&gl=US (SHOPPING, fetched 2026-11-22; refs/store/, not in git)
kind: app
category: shopping
ladder: L2 - everyday shopping objects carry the white wordmark
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): women's coats, dresses and knitwear on pale pink and white
  pages, the purple brand header; no characters, no mascot.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white uppercase wordmark in two lines: TRENDYOL / MILLA (measured, DotGothic-like M with a dot) - source.png
  2. the brand gradient: magenta-purple -> blue-violet -> light lavender (source tile) - source.png
  3. fashion: clothes, not groceries - a paper bag, a woven label, a hat box, a basket
function object (what the app does, as a physical thing): a shopping bag with new clothes in it

concepts (work/trendyolmilla/concepts.png) - four different ideas:
  A: a purple paper shopping bag with the white wordmark on its front (Symbol) (anchors 1, 2)
  B: a price tag - the wordmark itself, white on the brand gradient, a punched hole (Faithful) (anchors 1, 2)
  C: a round millinery case, lid band carrying the wordmark (Disc) (anchors 1, 2)
  D: a wicker willow carrier with a fabric tag carrying the wordmark (Rimmed) (anchors 1, 2)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the source is a gradient tile with the wordmark; mark_parts first kept the light lavender
    wash at the bottom-right as part of the mark, so geometry.json marks r2 as ground
    (`mark_skip`) - the mark is the white wordmark only.
  - Faithful is a real woven label, not the plain tile: stitched hem + folded corner keep it
    an object (REDESIGN.md 1: no logo on a plate).
  - no parcel box: hepsiburada is the parcel of this category (same_object).
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Purple 5 #613583, Purple 3 #9141ac, Purple 1 #dc8add, Light 2 #f6f5f4, Dark 4 #241f31
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
