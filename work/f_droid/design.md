# f_droid - design note (REDESIGN.md)

source: work/f_droid/source.png
store: refs/store/ (6 screenshots + icon.png, tools/fetch_refs.py)
kind: app
category: system
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no - the logo's robot head is part of the measured mark, nothing drawn from memory
references:
  - source.png: the Android robot's lime head (two antennas, white eyes) on a blue box with the
    copyleft sign, on a black tile.
  - shot-1 "Latest": app cards; shot-2 "Categories" with coloured category banners; shot-3 "Nearby":
    "No Internet? Get apps from people near you", "Find people nearby"; shot-4 "Updates": the blue
    "Update all" pill; shot-5 "Settings"; shot-6 search results with round blue download buttons.
    A lime-green search button (shots 1, 2); the bottom bar Latest / Categories / Nearby / Updates / Settings.
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the robot's lime head #aeea00 with antennas and white eyes - source.png
  2. the blue box #1976d2 / #0d47a1 with the copyleft sign - source.png
  3. the blue buttons and download arrows ("Update all", round download buttons) - refs/store/shot-4.jpg, shot-6.jpg
  4. Nearby - "Find people nearby", apps from phones around you - refs/store/shot-3.jpg
function object (what the app does, as a physical thing): a store of free apps you take home

concepts (Claude 2026-11-23, batch) - four different things, each carrying the measured logo:
  A: the app store as GNOME draws it - a blue shopping bag, lime handles, the logo on its label (anchors 1, 2)
  B: the logo itself as a solid object - robot head on its box, with thickness (anchors 1, 2)
  C: the Nearby radar - dark screen, lime rings and sweep, two phones found, the logo at the centre (anchors 1, 2, 4)
  D: "Update all" - an Android phone with F-Droid open: the logo and the blue pill with a lime arrow (anchors 1, 2, 3)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final:
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - drawn by Claude
decisions I made myself (and why; mention them in Q2):
  - Symbol is GNOME Software's own object (a shopping bag) in F-Droid's colours: an app store.
  - an open parcel was tried for Rimmed: next to the bag it was a twin container; the phone is not.
techniques used (min. 3): thickness / material gradient / top light / recess / glass / secondary object
palette (GNOME HIG names): F-Droid blue + lime (brand), Light 1-4, Dark 1-4
review:
