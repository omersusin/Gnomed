#!/usr/bin/env python3
"""enpara - FOUR concepts A-D (REDESIGN.md step 3). The rough ideas were drawn straight in
redesign.py (batch mode: all four are used), so this board is made from those four functions."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.parent.name
SPEC = importlib.util.spec_from_file_location("enpara_redesign", HERE.parent / "redesign.py")
RD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RD
SPEC.loader.exec_module(RD)

for name in ("A", "B", "C", "D"):
    getattr(RD, name)().save(HERE / f"{name}.svg")
print("wrote", *(f.name for f in HERE.glob("*.svg")))
