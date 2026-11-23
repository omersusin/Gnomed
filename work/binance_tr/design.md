# binance_tr - design note (REDESIGN.md)

source: work/binance_tr/source.png
store: Google Play "Binance TR: Crypto Trading" (FINANCE; refs/store/, 6 screenshots, tools/fetch_refs.py)
kind: app
category: finance
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no
references:
  - source.png: the yellow Binance diamond (four corner pieces around a small centre square) and
    "TR" under it, on black.
  - shot-1 "Turkey's leading cryptocurrency platform" with floating 3D coins (Bitcoin orange, the
    yellow coin with the Binance logo, Ethereum purple); shot-2 "Start with ₺10": "Kolay Al/Sat",
    BTC with a green/red candlestick chart, the "Al" / "Sat" tabs; shot-3 "İşlem Başarılı" (a green
    check); shot-4 "Browse 200+ crypto assets, purchase in Turkish lira": coins - the red ₺ coin,
    Bitcoin, Ethereum, the yellow logo coin; shot-5 24/7 support; shot-6 the lite menu: "Cüzdan
    1,234.78 TRY", round menu icons.
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the yellow Binance diamond #f0b90b with TR - source.png
  2. Binance black #1e2329 with the yellow - source.png, every screenshot (refs/store/shot-2.jpg ... shot-6.jpg)
  3. the floating 3D coins: the yellow coin with the logo, the red Turkish-lira coin - refs/store/shot-1.jpg, shot-4.jpg
  4. the candlestick chart, green and red ("Kolay Al/Sat") - refs/store/shot-2.jpg
  5. the wallet: "Cüzdan 1,234.78 TRY" - refs/store/shot-6.jpg
function object (what the app does, as a physical thing): buying crypto with Turkish lira and
  keeping it in a wallet

concepts (Claude 2026-11-23, the owner's comparison with Sonnet) - four different things, each carrying the measured logo:
  A: the wallet - a black wallet, the yellow coin with the logo and the red lira coin sticking out (anchors 1, 2, 3, 5)
  B: the logo itself as a solid object - the diamond and TR in Binance yellow with a deep-gold side (anchors 1, 2)
  C: the yellow coin of the screenshots - thick milled gold edge, the logo embossed on its face (anchors 1, 3)
  D: "Kolay Al/Sat" - a trading screen on its stand, the logo and green and red candles climbing (anchors 1, 2, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Önce sen yap binance için, compare edecem" (2026-11-23) - drawn by Claude on branch compare/binance_tr-claude
warn-ok: same_object - the yellow coin is Binance's own (its logo coin floats in shots 1 and 4); enpara's coin is a gold coin with a magenta en - the logo and colours tell them apart
decisions I made myself (and why; mention them in Q2):
  - Symbol is the wallet with the coins: the screenshots are coins and "Cüzdan"; a coin alone is the Disc.
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Binance yellow + black (brand), lira red, candle green/red, Light 2-5, Dark 1-4
review:
