#!/usr/bin/env python3
"""Concept board for one app (REDESIGN.md step 3).

    python3 tools/concepts.py <slug>

Renders work/<slug>/concepts/*.svg next to the source at 256 / 64 / 48 / 32 px and
between real GNOME object icons -> work/<slug>/concepts.png.  Concepts are rough
(flat shapes are fine): this board is for choosing a direction, not for polish.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / "tools/gnome-android-icons/scripts"
REFS = "org.gnome.Calls,org.gnome.FileRoller,org.gnome.Maps,org.gnome.Seahorse,org.gnome.Snapshot,io.github.seadve.Mousai"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    w = ROOT / "work" / slug
    svgs = sorted((w / "concepts").glob("*.svg"))
    if not svgs:
        sys.exit(f"no concepts: draw work/{slug}/concepts/A.svg, B.svg, C.svg first (REDESIGN.md step 3)")
    out = w / "concepts.png"
    r = subprocess.run([sys.executable, str(SK / "preview_sheet.py"), *map(str, svgs), "--source", str(w / "source.png"),
                        "--title", f"{slug} - concepts", "--ref-ids", REFS, "--out", str(out)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-800:])
    sys.path.insert(0, str(ROOT / "tools"))
    from stamps import write_board_stamp
    write_board_stamp(slug)
    print(f"board: {out.relative_to(ROOT)}  - open it, then ask the human which concept (REDESIGN.md step 4)")


if __name__ == "__main__":
    main()
