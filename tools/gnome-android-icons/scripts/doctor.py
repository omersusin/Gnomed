#!/usr/bin/env python3
"""Check that this machine / agent sandbox can run the skill, and say how to fix it.

Usage:  python3 scripts/doctor.py            (exit code 1 if a REQUIRED piece is missing)
"""
import importlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED = [("cairosvg", "cairosvg"), ("PIL", "pillow"), ("numpy", "numpy"), ("scipy", "scipy"),
            ("skimage", "scikit-image"), ("lxml", "lxml"), ("svgpathtools", "svgpathtools"),
            ("shapely", "shapely"), ("potrace", "potracer"), ("svgelements", "svgelements")]
OPTIONAL = [("androguard", "androguard", "APK icon extraction / --apk component lookup")]
TOOLS = [("adb", "phone component lookup + APK pull (Android platform-tools)"),
         ("rsvg-convert", "fallback SVG rasteriser"), ("inkscape", "manual editing / fallback rasteriser"),
         ("aapt", "APK manifest fallback")]


def main():
    ok = True
    print(f"python {platform.python_version()} on {platform.system()} {platform.machine()}")
    if sys.version_info < (3, 9):
        print("  [MISSING] Python 3.9+ required")
        ok = False
    missing = []
    for mod, pkg in REQUIRED:
        try:
            importlib.import_module(mod)
            print(f"  [ok] {pkg}")
        except Exception as e:  # cairosvg raises OSError when libcairo is absent
            print(f"  [MISSING] {pkg}: {type(e).__name__}: {str(e)[:90]}")
            missing.append(pkg)
            ok = False
    for mod, pkg, why in OPTIONAL:
        try:
            importlib.import_module(mod)
            print(f"  [ok] {pkg} (optional)")
        except Exception:
            print(f"  [optional] {pkg} not installed - needed for {why}")
    for tool, why in TOOLS:
        print(f"  [{'ok' if shutil.which(tool) else 'optional'}] {tool}{'' if shutil.which(tool) else ' not found - ' + why}")
    # rasteriser smoke test
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _common import render_svg, load_font
        tmp = Path(__file__).resolve().parent.parent / "assets" / "starter-kits" / "disc.svg"
        im = render_svg(tmp, 64)
        assert im.size == (64, 64) and im.getpixel((32, 32))[3] == 255
        print("  [ok] SVG rasterisation works")
        f = load_font(12)
        if type(f).__name__ != "FreeTypeFont":
            print("  [note] no TrueType font found: review boards use PIL's bitmap font (install fonts-dejavu)")
    except Exception as e:
        print(f"  [MISSING] SVG rasterisation failed: {e}")
        ok = False
    if missing:
        flag = " --break-system-packages" if sys.platform.startswith("linux") else ""
        print(f"\nfix: {sys.executable} -m pip install{flag} " + " ".join(missing))
        if "cairosvg" in missing:
            print("     cairosvg needs the Cairo C library: apt install libcairo2 | brew install cairo | "
                  "Windows: use MSYS2 or install rsvg-convert/inkscape (the scripts fall back to them)")
    try:
        r = subprocess.run([sys.executable, "-c", "import potrace; potrace.Bitmap"], capture_output=True)
        if r.returncode:
            print("note: 'potrace' import resolved to a different package - install potracer, not pypotrace")
    except Exception:
        pass
    print("\nresult:", "READY" if ok else "NOT READY")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
