#!/usr/bin/env python3
"""A zip for a model WITHOUT the repository (a chat: claude.ai, any app) - owner 2026-11-23:
"Sen dokümanı yaz. Ben Claude Sonnet'ten ekleyeyim bir tane ... test amaçlı".

    python3 tools/chat_bundle.py <slug>                 # -> ~/Downloads/gnomed/<slug>-chat.zip
    python3 tools/chat_bundle.py <slug> --out x.zip

The zip keeps the repository's layout, so every command in docs/METHOD.md works inside it:
docs/METHOD.md + REDESIGN.md + PLAYBOOK, the app (logo, measurement, screenshots, design.md and
redesign.py templates), the drawing library (work/_lib + the skill scripts), the gate
(tools/check_icon.py), the overview, four worked examples (reddit, duolingo, scene, f_droid),
every design.md (gate same_object compares with the other apps) and CHAT.md - the steps for the
chat model. It returns work/<slug>/redesign.py + design.md; the owner (or DeepSeek) copies them in
and runs tools/make_icon.py <slug> + tools/next.py <slug> as usual.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ("reddit", "duolingo", "scene", "f_droid", "binance_tr")
SKIP = ("__pycache__", ".pyc", "/png/", "build-stamp.txt")

CHAT = """# CHAT.md - make the Gnomed icon for `{slug}` (you have no repository, only this zip)

You are drawing an Android icon-pack icon in the GNOME/Adwaita style, in CODE (Python -> SVG).
Never use an image generator. The owner writes Turkish: answer him in Turkish, short.

## 0. Set up (once)
    unzip {slug}-chat.zip -d gnomed && cd gnomed
    pip install shapely cairosvg svgpathtools scikit-image scipy numpy pillow
(no network for pip? say so to the owner and continue with steps 1-3 by reading the code.)

## 1. Read, in this order
1. docs/METHOD.md - HOW to think: the app's own things + its measured logo, four different things.
   Then LOOK at docs/kit.png: the ready carriers (work/_lib/carriers.py) - one line per style.
2. REDESIGN.md §5 - the rules.
3. One worked example completely: work/reddit/redesign.py + work/reddit/design.md
   (also work/duolingo, work/scene, work/f_droid).

## 2. Look at the app
- work/{slug}/source.png (the logo), work/{slug}/refs/store/sheet.jpg and every shot-N.jpg,
  work/{slug}/refs/store/store.json (the description).
- Render the measured logo alone (METHOD.md §3, step 1) and look at it. Fix geometry.json if it
  is wrong (METHOD.md §3, step 2) - and say what you changed.

## 3. Write and check
- Fill work/{slug}/design.md (anchors with sources, four concept lines citing them,
  `approved: A - "batch: Biz onayladıktan sonra hepsini yapsın" (2026-11-22)`,
  `keep: B, C, D - "batch: hepsi kullanılsın" (2026-11-22)`, `styles: symbol=A faithful=B disc=C rimmed=D`).
- Write work/{slug}/redesign.py: the template already imports the kit - pick a carrier per style.
- Run:
      python3 work/{slug}/redesign.py
      python3 tools/check_icon.py {slug} --no-cache
      python3 tools/overview.py {slug} --out {slug}-overview.png
  Fix every FAIL and the WARNs METHOD.md §5 lists, LOOK at {slug}-overview.png, answer the five
  questions of METHOD.md §5, fix, run again.

## 4. Return to the owner
- work/{slug}/redesign.py, work/{slug}/design.md (and geometry.json if you changed it),
  {slug}-overview.png, and the last `summary:` line of check_icon.
- A short Turkish note: the four things you chose and why (which anchors), what is still weak.
The owner puts the files into the repository (work/{slug}/) and runs
`python3 tools/make_icon.py {slug}` and `python3 tools/next.py {slug}`.
"""


def files_for(slug):
    out = []

    def add(p):
        p = Path(p)
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            out.extend(q for q in p.rglob("*") if q.is_file())
    for f in ("docs/METHOD.md", "docs/kit.png", "REDESIGN.md", "docs/PLAYBOOK.md", "pack/styles.json",
              "tools/check_icon.py", "tools/overview.py", "tools/describe_icon.py",
              "work/_lib", "tools/gnome-android-icons/scripts", "app/src/main/res/font"):
        add(ROOT / f)
    for s in (slug,) + EXAMPLES:
        add(ROOT / "work" / s)
    out += list((ROOT / "work").glob("*/design.md"))
    keep = []
    for p in sorted(set(out)):
        r = p.relative_to(ROOT).as_posix()
        if any(k in "/" + r for k in SKIP):
            continue
        keep.append(p)
    return keep


def main(argv):
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    slug = argv[0]
    w = ROOT / "work" / slug
    if not (w / "source.png").exists():
        sys.exit(f"no work/{slug}/source.png - not an app of the pack")
    if not (w / "refs" / "store").is_dir():                 # the screenshots (not in git)
        subprocess.run([sys.executable, str(ROOT / "tools/fetch_refs.py"), slug], cwd=ROOT)
    if not (w / "redesign.py").exists() or not (w / "design.md").exists():
        subprocess.run([sys.executable, str(ROOT / "tools/new_redesign.py"), slug], cwd=ROOT)
    out = Path(argv[argv.index("--out") + 1]).expanduser() if "--out" in argv else \
        Path.home() / "Downloads" / "gnomed" / f"{slug}-chat.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    files = files_for(slug)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("CHAT.md", CHAT.format(slug=slug))
        for p in files:
            z.write(p, p.relative_to(ROOT).as_posix())
    shots = len(list((w / "refs" / "store").glob("shot-*"))) if (w / "refs" / "store").is_dir() else 0
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(files) + 1} files, {shots} screenshots)")
    print(f"Give the chat model the zip and one line: \"CHAT.md'yi oku ve {slug} simgesini yap.\"")


if __name__ == "__main__":
    main(sys.argv[1:])
