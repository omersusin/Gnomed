"""Content stamps: is a build / concept board current?  (used by make_icon.py, concepts.py, next.py)

work/<slug>/build-stamp.txt  = sha1 of redesign.py (+ kit.py), written after make_icon.py
work/<slug>/concepts/board-stamp.txt = sha1 of the concept SVGs, written after concepts.py
File times cannot be used: a fresh git clone gives every file the same time.
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _sha(paths):
    h = hashlib.sha1()
    for p in paths:
        if p.exists():
            h.update(p.name.encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def build_sources(slug):
    w = ROOT / "work" / slug
    return [w / "redesign.py", w / "kit.py"]


def write_build_stamp(slug):
    (ROOT / "work" / slug / "build-stamp.txt").write_text(_sha(build_sources(slug)) + "\n")


def build_current(slug):
    """True / False, or None when there is no stamp (an app built before stamps existed)."""
    p = ROOT / "work" / slug / "build-stamp.txt"
    if not p.exists():
        return None
    return p.read_text().strip() == _sha(build_sources(slug))


def board_sources(slug):
    return sorted((ROOT / "work" / slug / "concepts").glob("*.svg"))


def write_board_stamp(slug):
    (ROOT / "work" / slug / "concepts" / "board-stamp.txt").write_text(_sha(board_sources(slug)) + "\n")


def board_current(slug):
    p = ROOT / "work" / slug / "concepts" / "board-stamp.txt"
    if not p.exists():
        return None
    return p.read_text().strip() == _sha(board_sources(slug))
