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


SLUG_RE = r"[a-z][a-z0-9_]*"
COMP_RE = r"ComponentInfo\{[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+\}"


def registered_slugs():
    tsv = ROOT / "work/_lib/batch_apps.tsv"
    return {l.split("\t")[0] for l in tsv.read_text(encoding="utf-8").splitlines() if l.strip()}


def register(slug, png, label, comp):
    """Validate and register one app; returns an error string or None."""
    if not re.fullmatch(SLUG_RE, slug):
        return "slug must be lowercase a-z0-9_ and start with a letter"
    if not re.fullmatch(COMP_RE, comp):
        return "component must look like ComponentInfo{package/full.activity.Name}"
    if "\t" in label or "\n" in label:
        return "label must be one line"
    listed = slug in registered_slugs()
    if listed and (ROOT / "work" / slug / "source.png").exists():
        return f"{slug} is already registered"
    # listed without a source (a line added by hand / by another tool): only write the source
    im = Image.open(png).convert("RGBA")
    if min(im.size) < 48:
        return f"icon is only {im.size[0]}x{im.size[1]} px - too small to trace"
    out = ROOT / "work" / slug
    out.mkdir(parents=True, exist_ok=True)
    im.resize((512, 512), Image.LANCZOS).save(out / "source.png")
    if not listed:
        with (ROOT / "work/_lib/batch_apps.tsv").open("a", encoding="utf-8") as f:
            f.write(f"{slug}\t{label}\t{comp}\t{slug}\n")
    return None


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    slug, png, label, comp = sys.argv[1:]
    err = register(slug, png, label, comp)
    if err:
        sys.exit(err)
    print(f"ok: work/{slug}/source.png + batch_apps.tsv. Next: python3 tools/next.py {slug}")


if __name__ == "__main__":
    main()
