# payload_dumper - design note (REDESIGN.md)

source: work/payload_dumper/source.png
store: refs/store/ (4 screenshots + icon.png from IzzyOnDroid, tools/fetch_refs.py)
kind: app
category: dev
ladder: L1 mark as object (Faithful) / L2 objects carrying the mark
characters: no - the robot is the measured logo, nothing drawn from memory
mark: the measured logo; geometry.json mark_split gives the wrench (grey) and the screwdriver
  (orange) their real colours - the measurement had merged them with the robot's rim
references:
  - source.png: the green Android robot (two antennas, round eyes), a grey wrench at its left, an
    orange screwdriver at its right, on a navy tile.
  - shot-1 the partition list (vendor_dlkm, system_ext "31% - Extracting", vendor_boot, keymaster,
    boot ...) with "Extract" / "Cancel" buttons and progress bars; shot-2 "File URL" + "Load
    Partitions"; shot-3 settings (output directory payload_dumper, verify with SHA-256); shot-4
    a browser with "Download Detected" (an OTA zip).
anchors (2-4 things that make THIS app recognisable, with their colours and where they were seen):
  1. the green Android robot #3ddc84 - source.png
  2. its tools: the grey wrench and the orange screwdriver - source.png
  3. the partitions being extracted, with progress ("31% - Extracting", "47% - Extracting") - refs/store/shot-1.jpg
  4. the navy #2c3e51 of the tile and the dark UI - source.png, refs/store/shot-1.jpg ... shot-3.jpg
function object (what the app does, as a physical thing): it dumps a ROM's payload out into its
  partitions - the name says it: a dumper

concepts (Claude 2026-11-23, batch) - four different things, each carrying the measured logo:
  A: the dumper - a dump truck tipping the partition blocks out of its steel bed, the robot on the bed (anchors 1, 3, 4)
  B: the logo itself as a solid object - the robot with its wrench and screwdriver (anchors 1, 2)
  C: "47% - Extracting" - a round progress dial, the green arc around the robot on navy (anchors 1, 3, 4)
  D: the payload - the ROM's zip as an opened navy zip pouch, the partition blocks coming out, the logo on it (anchors 1, 3, 4)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7)
approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)
keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)
final: "Tamam, pakete ekle" (2026-11-23)
styles: symbol=A faithful=B disc=C rimmed=D
owner-takeover: "Kalanların hepsini yap" (2026-11-23) - drawn by Claude
decisions I made myself (and why; mention them in Q2):
  - a toolbox for Rimmed was termux_api's object (gate same_object): the zip pouch of the payload instead.
  - Symbol from the app's NAME (Payload "Dumper"): a dump truck unloading the partitions.
techniques used (min. 3): thickness / material gradient / top light / recess / secondary object
palette (GNOME HIG names): Android green (brand), navy (brand tile), Light 1-5, Dark 1-4, Orange
review:
