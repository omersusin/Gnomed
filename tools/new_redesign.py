#!/usr/bin/env python3
"""Start the REDESIGN of one app (REDESIGN.md step 1).

    python3 tools/new_redesign.py <slug>

Needs work/<slug>/source.png (tools/add_source.py or tools/import_request.py made it).
Creates, only if missing:
  work/<slug>/design.md      - the design note; the gate reads its "approved:" line
  work/<slug>/concepts/      - put 3 rough concept SVGs here: A.svg, B.svg, C.svg
  work/<slug>/redesign.py    - the final build (template: docs/redesign/examples/build_examples.py)
Nothing existing is overwritten.
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


def design():
    ic = gk.Icon("{slug} - Gnomed")
    # 1. the main object: silhouette = the object, NOT a plate with a logo on it
    body = rounded(box(18, 22, 110, 106), 12)
    solid(ic, body, face=[(0, "#99c1f1"), (0.5, "#62a0ea"), (1, "#3584e4")], depth=8, layer="body")
    # 2. what sits ON or IN it: recess (screen/label/inlay) or hole (lens/slot/keyhole)
    recess(ic, rounded(box(30, 34, 98, 80), 6), [(0, "#f6f5f4"), (1, "#deddda")], layer="label")
    # 3. a secondary object in front (optional, lower and smaller)
    # solid(ic, circ(94, 96, 16), face=[(0, "#ffbe6f"), (1, "#ff7800")], depth=4, layer="badge")
    raise SystemExit("replace the placeholder shapes with the approved concept, then remove this line")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {{"faithful": design()}})   # add "disc"/"rimmed"/"symbol" only for user-approved alternatives
'''


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    w = ROOT / "work" / slug
    if not (w / "source.png").exists():
        sys.exit(f"work/{slug}/source.png missing - run tools/add_source.py or tools/import_request.py first")
    (w / "concepts").mkdir(exist_ok=True)
    for name, text in (("design.md", DESIGN), ("redesign.py", TEMPLATE)):
        p = w / name
        if p.exists():
            print("kept", p.relative_to(ROOT))
        else:
            p.write_text(text.format(slug=slug), encoding="utf-8")
            print("created", p.relative_to(ROOT))
    print(f"""
Next (REDESIGN.md):
  2. look at work/{slug}/source.png and docs/redesign/gnome-objects.png; fill anchors + function object
  3. draw 3 rough concepts: work/{slug}/concepts/A.svg B.svg C.svg  ->  python3 tools/concepts.py {slug}
  4. show work/{slug}/concepts.png to the human, ask which one (2-4 options); write "approved:" with their answer
  5. build the chosen concept in work/{slug}/redesign.py  ->  python3 tools/make_icon.py {slug}""")


if __name__ == "__main__":
    main()
