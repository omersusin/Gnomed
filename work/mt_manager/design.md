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
  1. the white "MT" letters (measured from the holes of the dark folder) - source.png
  2. the charcoal folder with a coral corner and the little blue Android head - source.png
  3. a file manager that opens APKs and archives - storage and editing on the phone
function object (what the app does, as a physical thing): a cabinet of files you open and edit

concepts (work/mt_manager/concepts.png) - four different ideas:
  A: a filing cabinet: charcoal drawers, a white label plate with MT (Symbol) (anchors 1, 2)
  B: a charcoal folder with a raised tab, the coral sheet behind and MT on the front flap (Faithful) (anchors 1, 2)
  C: a round archive tin: charcoal cylinder, silver lid, coral base band, MT on the front label (Disc) (anchors 1, 2)
  D: a USB flash drive: charcoal body, coral stripe, steel connector, lanyard hole, MT on the body (Rimmed) (anchors 1, 2)
shape-ok: the Symbol is a filing cabinet and the Faithful is a folder - real box objects of the files
  family, not a plate with the logo on it; the plain_shape WARNs stay on purpose (2026-11-23).


# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   anchors-added: Claude 2026-11-23 (audit) - the styles carry the measured mark and the source colours; anchors 1, 2 say so
redo: "Deepseekin yaptıkları daha doğrusu senin yapmadıkların simgeleri göster ki yeniden yaptirayim" (2026-11-23) - redo with docs/METHOD.md
approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
decisions I made myself (and why; mention them in Q2):
  - the folder, filing cabinet, archive box and hard drive are all free in this category, so this
    app takes one of each (same_object) and never shares a shape with another file app.
  - the measured "MT" is white lettering INSIDE the dark folder, i.e. in the source's holes - not a
    coloured part. geometry.json `mark_holes` crops the two robot-eye dots away and keeps MT.
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object
palette (GNOME HIG names): Dark 3 #3d3846, Dark 4 #241f31, Light 2 #f6f5f4, Orange 2 #ffbe6f, Blue 3 #3584e4
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
