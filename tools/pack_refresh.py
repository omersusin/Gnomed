#!/usr/bin/env python3
"""Re-render the pack PNGs (and artwork/ SVG copies) of apps that are ALREADY in the pack,
after their build was improved. XML is not touched.

    python3 tools/pack_refresh.py <slug> [<slug> ...] [--dry-run]

--dry-run rebuilds the work/ SVGs only and lists the pack files it would overwrite.

Each app is first rebuilt with ITS builder (work/_lib/builders.py: hand-built apps with
build_weak.py / build_group1.py, the rest with build_auto.py), so the pack always gets
the current design and never a stale or wrongly built SVG.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools/gnome-android-icons/scripts"))
from _common import render_svg  # noqa: E402
sys.path.insert(0, str(ROOT / "work/_lib"))
import builders  # noqa: E402


def main():
    styles = json.loads((ROOT / "pack/styles.json").read_text())["icons"]
    dry = "--dry-run" in sys.argv[1:]
    bad = [a for a in sys.argv[1:] if a.startswith("-") and a != "--dry-run"]
    slugs = [a for a in sys.argv[1:] if not a.startswith("-")]
    if bad or not slugs:
        sys.exit(__doc__)
    for slug in slugs:
        names = {"faithful": slug, **styles.get(slug, {})}
        if not dry:                  # the icons that shipped go to archive/<slug>/ first (tools/archive.py)
            subprocess.run([sys.executable, str(ROOT / "tools/archive.py"), "pack", slug,
                            "--label", "pack-before-refresh", "--quiet"], cwd=ROOT)
        builder = builders.builder_of(slug)
        if subprocess.run([sys.executable, builder, slug], cwd=ROOT).returncode:
            sys.exit(f"{slug}: {builder} failed - nothing refreshed")
        for st, name in names.items():
            svg = ROOT / f"work/{slug}/{slug}-{st}.svg"
            png = ROOT / f"app/src/main/res/drawable-nodpi/{name}.png"
            if not png.exists():
                sys.exit(f"{name}.png is not in the pack - use tools/pack_add.py for new apps")
            if svg.exists() and dry:
                print(f"would overwrite {png.relative_to(ROOT)} + artwork/{name}.svg  <- {svg.relative_to(ROOT)}")
            elif svg.exists():
                render_svg(str(svg), 256).save(png, optimize=True)
                shutil.copy(svg, ROOT / f"artwork/{name}.svg")
                print("refreshed", name)


if __name__ == "__main__":
    main()
