"""Which script builds an app's SVGs. One place, used by every tool.

Hand-built apps (a function decorated with @build in build_weak.py or build_group1.py)
must NEVER be built by build_auto.py - that silently replaces the redrawn icon with the
automatic draft (it happened once: 6 apps in the pack were downgraded this way).
"""
import re
from pathlib import Path

LIB = Path(__file__).resolve().parent
HAND_FILES = ("build_weak.py", "build_group1.py")


def _hand(fname):
    return set(re.findall(r"@build\s*\ndef (\w+)\(", (LIB / fname).read_text(encoding="utf-8")))


def builder_of(slug):
    """-> 'work/_lib/<script>.py' that builds this slug."""
    for f in HAND_FILES:
        if slug in _hand(f):
            return f"work/_lib/{f}"
    return "work/_lib/build_auto.py"


def hand_built(slug):
    return builder_of(slug) != "work/_lib/build_auto.py"


def hand_slugs():
    return set().union(*(_hand(f) for f in HAND_FILES))
