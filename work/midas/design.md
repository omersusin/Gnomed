# midas - design note (REDESIGN.md)

source: work/midas/source.png
kind: app
category: finance
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no
store: Google Play "Midas: Borsa Hisse Alım Satım" (FINANCE; refs/store/, 6 screenshots)
references:
  - source.png: a white dot and two slanted bars on Midas blue.
  - shot-1 "Midas'ta tüm yatırımların tek ekranda" (the portfolio ₺534.833, TL/USD/EUR, BIST
    shares); shot-2 "Dakikalar içinde kaydol, ₺100 ile yatırıma başla"; shot-3 "Borsa İstanbul'da
    ₺0 komisyon ve sıfır masraf" ("İşlem Ücreti: Ücretsiz"); shot-4 "ABD & Avrupa şirketlerine
    düşük komisyonla yatırım yap"; shot-5 "Petrol, altın gibi emtiaların ETF'lerine yatırım yap"
    (a candlestick chart); shot-6 "En popüler TEFAS fonlarını keşfet" - the first fund theme is
    "Altın" with a photo of gold bars.
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the logo: a white dot and two slanted bars - source.png
  2. Midas blue #4959ea - source.png, the screens' blue (refs/store/shot-2.jpg, shot-4.jpg, shot-6.jpg)
  3. gold - "Petrol, altın gibi emtiaların ETF'lerine" (refs/store/shot-5.jpg), the "Altın" fund (refs/store/shot-6.jpg), and the name: Midas
  4. US and European shares - "ABD & Avrupa şirketlerine" (refs/store/shot-4.jpg)
  5. the portfolio: "tüm yatırımların tek ekranda" (refs/store/shot-1.jpg)
function object (what the app does, as a physical thing): your investments, kept together

ideas (docs/METHOD.md §1b):
  name: "Midas" -> gold: the Midas touch -> gold bars
  slogan: "Petrol, altın gibi emtiaların ETF'lerine yatırım yap" -> gold bars, an oil barrel
  screen: the "Altın" fund theme, a photo of gold bars -> gold bars
  slogan: "ABD & Avrupa şirketlerine düşük komisyonla" -> a globe with the two continents
  slogan: "Midas'ta tüm yatırımların tek ekranda" -> the portfolio: a briefcase
  slogan: "₺100 ile yatırıma başla" -> a lira coin (a coin is Binance's and Enpara's)
  content: a candlestick chart -> a trading screen (Binance's)
  logo: a dot and two bars -> the logo itself

worksheet (docs/METHOD.md §2):
  symbol (A):   idea=name  thing=gold bars  logo=stamped in Midas blue on the top bar  silhouette=a stack  main colour=gold
  faithful (B): thing=the logo itself  silhouette=the logo  main colour=Midas blue + white
  disc (C):     thing=a globe on a gold meridian  logo=on the ocean  silhouette=round + the meridian and stand  main colour=blue
  rimmed (D):   thing=a briefcase  logo=on its front  silhouette=a case with a handle  main colour=deep blue
  checks: four silhouettes different (stack, logo, globe, case); no dark styles; no plate; every thing from an idea line

concepts (Claude 2026-11-23, the owner's comparison with Haiku) - four different things, each carrying the measured logo:
  A: Midas = gold - three gold bars stacked, the logo stamped in Midas blue on the top bar (anchors 1, 2, 3)
  B: the logo itself as a solid object - the white dot and bars on their Midas-blue die-cut (anchors 1, 2)
  C: a Midas-blue globe with the Americas and Europe on a gold meridian, the logo on the ocean (anchors 1, 2, 4)
  D: the portfolio - a deep-blue leather briefcase, gold clasps, the logo on its front (anchors 1, 2, 5)

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
