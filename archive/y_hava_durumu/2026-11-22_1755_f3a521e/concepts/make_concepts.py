#!/usr/bin/env python3
"""y_hava_durumu - concepts A-D (BATCH.md). Run: python3 work/y_hava_durumu/concepts/make_concepts.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
import redesign  # noqa: E402

OUT = Path(__file__).resolve().parent
if __name__ == "__main__":
    for name, fn in (("A", redesign.A), ("B", redesign.B), ("C", redesign.C), ("D", redesign.D)):
        fn().save(OUT / f"{name}.svg")
        print("wrote", (OUT / f"{name}.svg").name)
