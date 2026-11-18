#!/usr/bin/env python3
"""Register a new app for the icon pipeline.

    python3 tools/add_source.py <slug> <icon.png> "<Label>" "ComponentInfo{pkg/pkg.Activity}"

- <slug>: drawable name, lowercase a-z0-9_, must start with a letter (CandyBar rule)
- <icon.png>: the app's icon as exported by an icon request (192 px PNG is fine)
- the component must come from the phone (icon request export / adb / APK) - never guessed

Writes work/<slug>/source.png (Lanczos upscale to 512) and appends the app to
work/_lib/batch_apps.tsv (slug, label, component, original drawable name).
"""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    slug, png, label, comp = sys.argv[1:]
    if not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
        sys.exit("slug must be lowercase a-z0-9_ and start with a letter")
    if not re.fullmatch(r"ComponentInfo\{[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+\}", comp):
        sys.exit("component must look like ComponentInfo{package/full.activity.Name}")
    tsv = ROOT / "work/_lib/batch_apps.tsv"
    if any(l.split("\t")[0] == slug for l in tsv.read_text(encoding="utf-8").splitlines()):
        sys.exit(f"{slug} is already registered")
    out = ROOT / "work" / slug
    out.mkdir(parents=True, exist_ok=True)
    Image.open(png).convert("RGBA").resize((512, 512), Image.LANCZOS).save(out / "source.png")
    with tsv.open("a", encoding="utf-8") as f:
        f.write(f"{slug}\t{label}\t{comp}\t{slug}\n")
    print(f"ok: work/{slug}/source.png + batch_apps.tsv. Next: python3 work/_lib/auto.py {slug}")


if __name__ == "__main__":
    main()
