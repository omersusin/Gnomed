#!/usr/bin/env python3
"""Start the REDESIGN of one app (REDESIGN.md step 1).

    python3 tools/new_redesign.py <slug>

Needs work/<slug>/source.png (tools/add_source.py or tools/import_request.py made it).
Does, only what is missing (nothing existing is overwritten):
  work/<slug>/geometry.json  - MEASURES the source (work/_lib/auto.py): colour parts r0, r1 ...
  work/<slug>/design.md      - the design note; the gate reads its "approved:" line
  work/<slug>/concepts/make_concepts.py - a WORKING template for the 3 rough concepts
                               (run it: it writes concepts/A.svg B.svg C.svg)
  work/<slug>/redesign.py    - the final build (template; uses the measured parts)
and prints the measured parts as text (colour, size, position) - no image needed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DESIGN = """# {slug} - design note (REDESIGN.md)

source: work/{slug}/source.png
anchors (2-4 things that make the app recognisable; they must survive):
  1.
  2.
function object (what the app does, as a physical thing):

concepts (work/{slug}/concepts.png):
  A (L1 the mark becomes an object):
  B (L2 a GNOME object that carries the mark):
  C (L3 material tile, only if A and B fail):

approved:
styles: faithful=?
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (48/32 px, light + dark wallpaper, what is still weak):
"""

TEMPLATE = '''#!/usr/bin/env python3
"""{slug} - Gnomed redesign.  Concept: <write the approved concept from design.md>.
Build:  python3 tools/make_icon.py {slug}      (runs this file, then review + gate)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402
SLUG = Path(__file__).resolve().parent.name
P = parts(SLUG)               # measured parts: P["r0"], P["r1"], ..., P["silhouette"], P["holes"]
# print(describe(SLUG))       # colours / sizes / positions as text


def design():
    ic = gk.Icon("{slug} - Gnomed")
    # Copy the APPROVED concept from concepts/make_concepts.py here, then polish:
    # thickness (solid depth), light from the top (gradient + toplight), recess / hole,
    # a secondary object. Object inside 8..120, bottom edge (side included) 116..120.
    raise SystemExit("copy the approved concept here (concepts/make_concepts.py), then remove this line")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {{"faithful": design()}})   # add "disc"/"rimmed"/"symbol" only for user-approved alternatives
'''

CONCEPTS = '''#!/usr/bin/env python3
"""{slug} - 3 ROUGH concepts (REDESIGN.md step 3). Run:
    python3 work/{slug}/concepts/make_concepts.py && python3 tools/concepts.py {slug}
Each function is ONE idea from the ladder; flat shapes are fine. Replace the example
bodies. Every shape of the app's mark comes from P (measured), never from memory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from obj import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)
MARK = [P[k] for k in sorted(P) if k.startswith("r")]          # the coloured parts
COL = [colour(SLUG, k) for k in sorted(P) if k.startswith("r")]


def A():
    """L1 - the mark itself becomes the object (thickness, light), no plate."""
    ic = gk.Icon("{slug} concept A")
    for g, c in zip(fit(MARK, (14, 12, 114, 112), anchor="bottom"), COL):   # bottom 112 + side 6 = 118
        solid(ic, g, face=c, depth=6)
    return ic


def B():
    """L2 - a GNOME object that carries the mark (the app's function as a thing).
    EXAMPLE object: a rounded box; REPLACE it with the app's object (envelope, cloud,
    device, book, camera ...) - never a plain disc or square with the logo on it."""
    ic = gk.Icon("{slug} concept B")
    body = rounded(box(18, 30, 110, 108), 10)                 # bottom 108 + side 10 = 118
    solid(ic, body, face=[(0, "#f6f5f4"), (1, "#deddda")], depth=10)
    for g, c in zip(fit(MARK, (36, 42, 92, 94)), COL):
        solid(ic, g, face=c, depth=2)
    return ic


def C():
    """another idea (a second L1/L2 idea; L3 material tile only if A and B fail)."""
    ic = gk.Icon("{slug} concept C")
    for g, c in zip(fit(MARK, (16, 12, 112, 115), anchor="bottom"), COL):   # bottom 115 + side 3 = 118
        solid(ic, g, face=c, depth=3)
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C)):
        fn().save(OUT / f"{{name}}.svg")
        print("wrote", (OUT / f"{{name}}.svg").name)
'''


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    w = ROOT / "work" / slug
    if not (w / "source.png").exists():
        sys.exit(f"work/{slug}/source.png missing - run tools/add_source.py or tools/import_request.py first")
    (w / "concepts").mkdir(exist_ok=True)
    if not (w / "geometry.json").exists():
        import subprocess
        print("measuring the source (work/_lib/auto.py) ...")
        if subprocess.run([sys.executable, str(ROOT / "work/_lib/auto.py"), slug], cwd=ROOT).returncode:
            sys.exit("measuring failed - see the error above")
    for name, text in (("design.md", DESIGN), ("redesign.py", TEMPLATE), ("concepts/make_concepts.py", CONCEPTS)):
        p = w / name
        if p.exists():
            print("kept", p.relative_to(ROOT))
        else:
            p.write_text(text.format(slug=slug), encoding="utf-8")
            print("created", p.relative_to(ROOT))
    sys.path.insert(0, str(ROOT / "work/_lib"))
    from obj import describe
    print()
    print(describe(slug))
    print(f"""
Next (REDESIGN.md):
  2. look at work/{slug}/source.png and docs/redesign/gnome-objects.png; fill anchors + function object
  3. edit work/{slug}/concepts/make_concepts.py (3 different ideas), then
     python3 work/{slug}/concepts/make_concepts.py && python3 tools/concepts.py {slug}
  4. show work/{slug}/concepts.png to the human, ask which one (2-4 options); write "approved:" with their answer
  5. build the chosen concept in work/{slug}/redesign.py  ->  python3 tools/make_icon.py {slug}""")


if __name__ == "__main__":
    main()
