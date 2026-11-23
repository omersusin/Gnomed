#!/usr/bin/env python3
"""duolingo - FOUR concepts A-D (batch mode: all four are used), drawn from redesign.py."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("duolingo_redesign", HERE.parent / "redesign.py")
RD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RD
SPEC.loader.exec_module(RD)

for name, fn in RD.CONCEPTS.items():
    fn().save(HERE / f"{name}.svg")
print("wrote", *(f.name for f in sorted(HERE.glob("*.svg"))))
