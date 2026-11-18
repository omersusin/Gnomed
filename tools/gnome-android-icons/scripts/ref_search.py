#!/usr/bin/env python3
"""Search the bundled GNOME reference library (offline).

Usage:
  ref_search.py --kind emblem,disc-emblem        # by metaphor kind
  ref_search.py --shape circle                   # circle | square | portrait | landscape | free
  ref_search.py --text "play"                    # id / notes substring
  ref_search.py --group gnome-games              # gnome-core | gnome-games | circle-and-third-party | adwaita-system
  ref_search.py --kinds                          # list kinds with counts
  add --sheet out.png to render the hits; --paths to print file paths only
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import LIB_ROOT  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind")
    ap.add_argument("--shape")
    ap.add_argument("--text")
    ap.add_argument("--group")
    ap.add_argument("--kinds", action="store_true")
    ap.add_argument("--sheet")
    ap.add_argument("--paths", action="store_true")
    a = ap.parse_args()
    cat = json.loads((LIB_ROOT / "catalog.json").read_text())["icons"]
    if a.kinds:
        for k, n in Counter(e["kind"] for e in cat).most_common():
            print(f"{k:14} {n}")
        return
    hits = cat
    if a.kind:
        ks = set(a.kind.split(","))
        hits = [e for e in hits if e["kind"] in ks]
    if a.shape:
        ss = set(a.shape.split(","))
        hits = [e for e in hits if e["shape"] in ss]
    if a.group:
        hits = [e for e in hits if e["group"] == a.group]
    if a.text:
        t = a.text.lower()
        hits = [e for e in hits if t in e["id"].lower() or t in e["notes"].lower()]
    for e in hits:
        p = LIB_ROOT / e["file"]
        if a.paths:
            print(p)
        else:
            m = e["metrics"]
            print(f"{e['id']:42} {e['kind']:12} {e['shape']:9} {m['w']}x{m['h']} chin {m['chin']}  {e['notes'][:70]}")
    if a.sheet and hits:
        subprocess.run([sys.executable, str(Path(__file__).with_name("contact_sheet.py")), a.sheet,
                        *[str(LIB_ROOT / e["file"]) for e in hits], "--size", "112", "--cols", "8", "--bg", "both"], check=True)


if __name__ == "__main__":
    main()
