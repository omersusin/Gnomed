"""Locate the vendored GNOME icon toolkit and put its scripts on sys.path.

The toolkit (the gnome-android-icons Agent Skill) lives in tools/gnome-android-icons.
Override with GNOME_ICONS_SKILL=/path/to/gnome-android-icons if you keep it elsewhere."""
import os
import sys
from pathlib import Path

SKILL = Path(os.environ.get("GNOME_ICONS_SKILL", Path(__file__).resolve().parents[2] / "tools/gnome-android-icons"))
sys.path.insert(0, str(SKILL / "scripts"))
