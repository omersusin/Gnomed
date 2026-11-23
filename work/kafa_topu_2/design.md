# kafa_topu_2 - design note (REDESIGN.md)

source: work/kafa_topu_2/source.png
store: https://play.google.com/store/apps/details?id=com.masomo.headball2&hl=en&gl=US (GAME_SPORTS, fetched 2026-11-22; refs/store/, not in git)
kind: game
category: game
ladder:   (old: scene with characters (made before the objects-only rule))
characters: yes - the game IS its two big heads facing each other; without them it is any football
  game (REDESIGN 3b, owner 2026-11-23 "Oyuna göre sen seç"; the objects-only round 3 - ball, boot,
  stopwatch, cup - was rejected: "İğrenç ... Otun ile alakası yok", 2026-11-23)
redo-started: "Evet, yeni oturumda" (2026-11-21) - objects only (the ball + the boot), no characters (REDESIGN.md 3b) (2026-11-23, old concepts -> concepts-round3/)
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  - store icon (source.png): TWO big-head footballers FACING each other (left: brown hair with
    a blond streak, beard, gritted teeth; right: buzz cut, darker skin, angry), a black/white
    football above them, a yellow "VS" between, blue stadium sky.
  - the owner (2026-11-19): "Kafa Topu oyununda iki kafa olması gerekiyor, böyle karşı karşıya",
    "Kafa topunun karakterleri, ayakkabıları var yani" - in the game each character is a big
    head standing on ONE football boot.
  - in-game screenshots (owner, 2026-11-21, refs/): game-1 = a clown head vs the bearded
    player, each a BIG HEAD standing on ONE boot, facing each other on a green pitch, the ball
    between them at head height, a white goal with a net at each end; game-2 = buzz-cut head
    (blue/yellow boot) vs blue-haired head (red boot) doing a fireball header, goal on the
    right. banner-logo = the two store heads facing, each with ONE big black boot under it,
    the ball in the middle, a round green pitch with a white centre line.
    -> composition: 2 heads, 1 boot each, facing, ball between; goals + pitch are context.
old anchors (before the redo):
  old 1. two big heads facing each other (the duel), each on one football boot
  old 2. the black/white leather football between/above them
  old 3. the yellow VS
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. two big heads facing each other: the bearded one (brown hair, blond streak, red jersey) and the
     buzz-cut one (darker skin, blue jersey) - source.png
  2. the black-and-white leather ball - source.png, refs/store/shot-1.jpg
  3. the yellow-orange VS - source.png
  4. ONE big boot under each head (red / blue-yellow) - refs/game-1-clown-vs-beard.png, refs/banner-logo.png
  5. the round green pitch with its white centre line - refs/banner-logo.png
  6. the goal with its net and the fireball shot ("Use your Super Powers!") - refs/store/shot-2.jpg
old function object (what the app does, as a physical thing): a 1-vs-1 header duel
function object (what the app does, as a physical thing): the ball going in after a header - the ball,
  the boot that strikes it, the referee's clock of the 90 seconds, the cup the match is played for

old concepts (round 3, before the redo):
  old A: the duel scene - two players (head + boot) facing, ball above, VS between
  old B: close to the store icon - two busts facing (jersey shoulders), ball above, VS
  old C: round - the two players and the ball on a round pitch with thickness
  old D: object - the header goal: one player heading the ball into a goal
old concepts (round 4, DeepSeek, objects only - rejected 2026-11-23; archive/kafa_topu_2/*deepseek-objects):
  old A: the match ball with blue panels on the green turf ... old B: a brown boot ... old C: a
  stopwatch ... old D: a winner's cup
concepts (round 5, Claude 2026-11-23) - four different designs, each carrying the game's anchors:
  A: the header - ONE big head (the bearded player) on his red boot, heading the ball (anchors 1, 2, 4)
  B: the store icon without its plate - two busts facing, the VS between, the ball above (anchors 1, 2, 3)
  C: the banner's round pitch - the two players on their boots facing, the ball between (anchors 1, 2, 4, 5)
  D: the super power - the ball flying into the goal's net with a fire trail (anchors 2, 6)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
history-approved: B - "B" (2026-11-21)   [before the redo, concepts-round3/]
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
owner-takeover: "Şimdilik devral bakalım" (2026-11-23) - round 5 drawn by Claude
history-keep: A, C, D - "A,B,C,D,Sen karar ver" (2026-11-21)   [before the redo, concepts-round3/]
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
history-final: "Tamam, pakete ekle" (2026-11-21)   [before the redo, concepts-round3/]
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - round 5 (Claude): characters back (the game's identity); four different designs instead of the
    old round's four duels; rimmed has none of the logo's colours (the fire, the goal and the ball
    carry it) - warn-ok below.
  - redo (objects only, owner 2026-11-21): the two heads are gone; the ball, the boot, the clock and
    the cup carry the four styles. The brands colours survive as the light-blue of the store's
    stadium and the ball's panels (mark_size PASS on all four).
  - the ball is the symbol (the duel is about it); the boot is the faithful (the player's own object,
    closest to the screenshots where each head stands on one boot).
  - keep: he ticked all and "Sen karar ver"; B is the main, so A (the duel, closest to the
    game screenshots) -> faithful, C (round pitch) -> disc, D (goal) -> rimmed.
  - B was moved down/enlarged so the shoulders stand on the baseline (concept floated).
  - rimmed (D): the net is opaque (light mesh, grey threads) - a see-through net FAILed lint
    and read as a blur; the goal is smaller so the players stay legible at 32 px.
  - pack: styles.json had no slots for kafa_topu_2 (Symbol APK showed the faithful PNG), so
    shipping = pack_add (alt1 disc, alt2 rimmed, alt3 symbol) + pack_refresh (faithful).
  - mistake: pack_refresh --dry-run wrote the pack PNG (no dry-run existed); reverted with
    git checkout at once; the tool now has --dry-run.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
warn-ok: mark_size - a game: the rimmed style is the fireball goal of the screenshots; the logo's blue and yellow are in the other three styles
