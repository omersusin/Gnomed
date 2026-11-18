#!/usr/bin/env python3
"""Build script for chatgpt - the construction lives in work/_lib/build_group1.py
(shared with the rest of group 1); geometry in geometry.json (extract_group1.py)."""
import subprocess, sys
from pathlib import Path
lib = Path(__file__).resolve().parent.parent / "_lib"
subprocess.run([sys.executable, str(lib / "build_group1.py"), "chatgpt"], check=True)
