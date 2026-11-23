# reddit - design note (REDESIGN.md)

source: work/reddit/source.png
store: refs/store/ (6 screenshots + icon.png, tools/fetch_refs.py)
kind: app
category: social
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no - but the LOGO is Snoo's head, so the measured head is the mark on every style
  (REDESIGN 5 "A mascot logo is still the logo"); no body drawn from memory.
mark: the measured head; its eyes are holes in the source (the orange tile shows through), painted
  orange again: geometry.json mark_hole_fill #ff4500
painted-holes: "Logodaki gibi boya" (2026-11-23) - Snoo's eyes are orange like the logo, not see-through
references:
  - source.png: Snoo's white head with two ears, the antenna (black stalk, white ball), orange eyes,
    a black smile, on the Reddit orange tile.
  - shots 1, 6: posters with vote pills (orange up arrow + score "214"), green "r/soccer" and pink
    "r/parenting" tags; shot-2 search "is Korean skincare better?" + "Ask"; shot-3 the search bar
    "Find anything" with Snoo in an orange circle, a "Match Thread: USA vs Paraguay" photo (a ball on
    the grass); shots 4, 5 white post cards with comment threads, the vote row (up 186k, down) and
    the comments bubble.
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. Snoo's head: white, antenna with a ball, orange eyes, black smile - source.png
  2. Reddit orange #ff4500 - source.png (the tile), the background of every screenshot (refs/store/shot-1.jpg ... shot-6.jpg)
  3. the vote arrow: orange up arrow #ff4500, grey down arrow - refs/store/shot-1.jpg, shot-5.jpg, shot-6.jpg
  4. the comment threads: the comments bubble in every post row, "Join the conversation" - refs/store/shot-3.jpg, shot-4.jpg, shot-5.jpg
  5. search "Find anything" with Snoo in the orange circle - refs/store/shot-2.jpg, shot-3.jpg
function object (what the app does, as a physical thing): posts people vote up, and a search for
  real opinions

concepts (Claude 2026-11-23, batch) - four different things, each carrying Snoo:
  A: the upvote - Reddit's big orange up arrow with Snoo's head printed on it (anchors 1, 2, 3)
  B: the logo as a die-cut sticker - Snoo's white head on its orange margin, with thickness (anchors 1, 2)
  C: the search lens - steel rim and handle, through the glass the Reddit orange with Snoo (anchors 1, 2, 5)
  D: the conversation - the comments bubble as a solid orange speech bubble, Snoo talking in it (anchors 1, 2, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - drawn by Claude
decisions I made myself (and why; mention them in Q2):
  - Snoo in every style: it is the logo (owner 2026-11-23: "Oyunlarda ve uygulamalarda hassas olmalı").
  - the search lens, not a plain orange disc: an orange disc with Snoo is the logo on a plate.
  - Rimmed: a post card (avatar, upvote, match photo) lost its details at 32 px (ssim 0.63-0.69); the
    comments bubble is the same anchor, bolder.
techniques used (min. 3): thickness / material gradient / top light / recess / glass / secondary object
palette (GNOME HIG names): Reddit orange (brand), Light 1-4, Dark 1-3, Green 1-5
review:
