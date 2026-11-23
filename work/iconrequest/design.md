# iconrequest - design note (REDESIGN.md)

source: work/iconrequest/source.png
store: https://play.google.com/store/apps/details?id=de.kaiserdragon.iconrequest (TOOLS; refs/store/, 6 screenshots)
kind: app
category: system
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no - the robot is the measured logo
references:
  - source.png: a green robot head with two ears and yellow eyes over a green body; on the body a
    drafting compass (yellow head with a black pivot, grey legs) drawing a white arc; navy tile.
  - shot-1 home: "New Icon Request - Select apps and share" (a big green card with +), Health
    Check (shield), Compare; shot-2 the app list with checkboxes; shot-3 "Filter by Icon Pack";
    shot-4 Comparison (Lawnicons vs Arcticons); shot-5 "Health Status 99%" (yellow), duplicates,
    broken links; shot-6 settings (Pure XML Export).
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the green robot #00c763 with yellow eyes #efb100 - source.png
  2. the drafting compass: yellow head, grey legs, the white arc it draws - source.png
  3. "New Icon Request - Select apps and share" - refs/store/shot-1.jpg
  4. the list of apps with checkboxes, the ones the pack misses - refs/store/shot-2.jpg
  5. "Health Status 99%" in yellow - refs/store/shot-5.jpg
  6. "Health Check" with its shield - refs/store/shot-1.jpg
function object (what the app does, as a physical thing): a request for the icons a pack is missing

concepts (Claude 2026-11-23, batch) - four different things, each carrying the measured logo:
  A: "Select apps and share" - the request sent: a green envelope, the logo on its navy stamp (anchors 1, 2, 3)
  B: the logo itself as a solid object - the robot with the compass on its body (anchors 1, 2)
  C: "Health Status 99%" - a round dial with the yellow ring almost full, the logo in it (anchors 1, 5)
  D: "Health Check" - the check's shield, navy with a green rim, the logo on it (anchors 1, 2, 6)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - drawn by Claude
decisions I made myself (and why; mention them in Q2):
  - a clipboard with the app list lost its details at 32 px (ssim 0.67-0.71): the shield of Health Check instead.
  - every style is the app's own: its request list, its health score, its "share"; no generic icon object.
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): IconRequest green + navy + yellow (brand), Light 1-5, Dark 1-4, Blue 3, Orange 4
review:
