# mt_manager - design note (REDESIGN.md)

source: work/mt_manager/source.png
store: https://mt-manager.en.uptodown.com/android (FILES, fetched 2026-11-23; refs/store/, not in git)
kind: app
category: files
ladder: L2 - storage objects carry the white "MT" wordmark
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
  store screenshots (refs/store/): a dark file browser with an APK editor; no characters.
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white "MT" letters (measured from the holes of the dark folder)
  2. the charcoal folder with a coral corner and the little blue Android head
  3. a file manager that opens APKs and archives - storage and editing on the phone
function object (what the app does, as a physical thing): a cabinet of files you open and edit

concepts (work/mt_manager/concepts.png) - four different ideas:
  A: a filing cabinet: charcoal drawers, a white label plate with MT (Symbol)
  B: an open folder: charcoal back and front, coral tab, a white card with MT (Faithful)
  C: a hard-disk platter: silver disc, spindle and actuator arm, a white MT label (Disc)
  D: an archive box: charcoal box with a rimmed coral lid, white label with MT (Rimmed)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the folder, filing cabinet, archive box and hard drive are all free in this category, so this
    app takes one of each (same_object) and never shares a shape with another file app.
  - the measured "MT" is white lettering INSIDE the dark folder, i.e. in the source's holes - not a
    coloured part. geometry.json `mark_holes` crops the two robot-eye dots away and keeps MT.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 3 #3d3846, Dark 4 #241f31, Light 2 #f6f5f4, Orange 2 #ffbe6f, Blue 3 #3584e4
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
