#!/usr/bin/env python3
"""Phone preview for the final question (REDESIGN.md 7, Q2).

    python3 tools/phone_preview.py <slug>

The app's Symbol (the owner's style; work/<slug>/<slug>-symbol.svg, else Faithful) among
8 Symbol icons of the pack (*_alt3.png, or the primary where an app has no Symbol), on
light, dark and colourful wallpapers, at real launcher size (54 dp x density 2.75).
-> work/<slug>/phone.png   (the candidate is the 2nd icon of the first row)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ND = ROOT / "app/src/main/res/drawable-nodpi"
NEIGHBOURS = ["whatsapp", "telegram", "chatgpt", "discord", "saat", "youtube", "bitwarden", "firefox_beta",
              "instagram", "qobuz", "duolingo", "reddit"]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    w = ROOT / "work" / slug
    cand = w / f"{slug}-symbol.svg"
    if not cand.exists():
        cand = w / f"{slug}-faithful.svg"
    if not cand.exists():
        sys.exit(f"no SVG for {slug}: build it first (python3 tools/make_icon.py {slug})")
    icons = []
    for n in NEIGHBOURS:
        if n == slug:
            continue
        png = ND / f"{n}_alt3.png"
        if not png.exists():
            png = ND / f"{n}.png"
        if png.exists():
            icons.append(f"{png}:{n.replace('_', ' ').title()[:11]}")
        if len(icons) == 8:
            break
    icons.insert(1, f"{cand}:{slug.replace('_', ' ').title()[:11]}")
    out = w / "phone.png"
    r = subprocess.run([sys.executable, str(ROOT / "tools/gnome-android-icons/scripts/launcher_preview.py"), *icons,
                        "--refs", "0", "--icon-dp", "54", "--density", "2.75", "--cols", "3", "--out", str(out)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-800:])
    print(f"phone preview: {out.relative_to(ROOT)}  (Symbol among 8 pack Symbols; light / dark / colour wallpaper)")


if __name__ == "__main__":
    main()
