#!/usr/bin/env python3
"""Concept board: rough concept SVGs next to the source and real GNOME object icons
(references/redesign.md, step 3).

    concepts.py work/<slug>                 # reads work/<slug>/concepts/*.svg + source.png
    concepts.py A.svg B.svg C.svg --source source.png --out concepts.png

Shows each concept at 256 px on light + dark, true 64/48/32 px, and in a row between
real GNOME object icons (Calls, FileRoller, Maps, Seahorse, Snapshot, Mousai).
Concepts are rough on purpose: this board is for choosing a DIRECTION with the human.
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = "org.gnome.Calls,org.gnome.FileRoller,org.gnome.Maps,org.gnome.Seahorse,org.gnome.Snapshot,io.github.seadve.Mousai"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="a work folder, or concept SVG files")
    ap.add_argument("--source")
    ap.add_argument("--out")
    ap.add_argument("--title")
    ap.add_argument("--ref-ids", default=REFS)
    a = ap.parse_args()
    first = Path(a.inputs[0])
    if len(a.inputs) == 1 and first.is_dir():
        svgs = sorted((first / "concepts").glob("*.svg"))
        source = a.source or (first / "source.png" if (first / "source.png").exists() else None)
        out = Path(a.out) if a.out else first / "concepts.png"
        title = a.title or f"{first.name} - concepts"
    else:
        svgs = [Path(p) for p in a.inputs]
        source, out, title = a.source, Path(a.out or "concepts.png"), a.title or "concepts"
    if not svgs:
        sys.exit(f"no concepts: draw {first}/concepts/A.svg, B.svg, C.svg first (references/redesign.md step 3)")
    cmd = [sys.executable, str(HERE / "preview_sheet.py"), *map(str, svgs), "--title", title,
           "--ref-ids", a.ref_ids, "--out", str(out)]
    if source:
        cmd += ["--source", str(source)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-800:])
    print(f"board: {out}  - look at it, then ask the human which direction (references/redesign.md step 4)")


if __name__ == "__main__":
    main()
