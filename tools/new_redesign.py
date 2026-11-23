#!/usr/bin/env python3
"""Start the REDESIGN of one app (REDESIGN.md step 1).

    python3 tools/new_redesign.py <slug>

Needs work/<slug>/source.png (tools/add_source.py or tools/import_request.py made it).
Does, only what is missing (nothing existing is overwritten):
  work/<slug>/geometry.json  - MEASURES the source (work/_lib/auto.py): colour parts r0, r1 ...
  work/<slug>/design.md      - the design note; the gate reads its "approved:" line
  work/<slug>/concepts/make_concepts.py - a WORKING template for the 4 rough concepts
                               (run it: it writes concepts/A.svg B.svg C.svg D.svg)
  work/<slug>/redesign.py    - the final build (template; uses the measured parts)
and prints the measured parts as text (colour, size, position) - no image needed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DESIGN = """# {slug} - design note (REDESIGN.md)

source: work/{slug}/source.png
kind: <app | game>
category: <music | video | messaging | social | browser | files | security | finance | shopping | photo | weather | maps | productivity | dev | system | ai | learning | health | game>  (python3 tools/fetch_refs.py {slug} fills it)
ladder: <L1 mark as object | L2 object carries the mark | L3 material tile | game objects>
characters: no
references (games: store icon + >= 2 in-game screenshots; what they show: number of
  characters, how they face each other, signature gear, key object, colours):
anchors (2-4 things that make THIS app recognisable, seen in source.png and the screenshots in
  work/{slug}/refs/store/ - each with its real colour and WHERE you saw it; they must survive):
  1. <thing, colour> - <source.png | refs/store/shot-2.jpg | the owner's words>
  2. <thing, colour> - <where>
function object (what the app does, as a physical thing):

worksheet (docs/METHOD.md §2 - fill it BEFORE drawing; one line per style):
  A symbol:   thing=<a thing of THIS app, big>  logo=<on a light part | on a brand-colour part | in front>  silhouette=<one word>  main colour=<colour>
  B faithful: thing=the logo itself (put_mark body=)  silhouette=the logo  main colour=<the logo's colour>
  C disc:     thing=<a ROUND thing: lens, dial, fan, cup, coin, radar>  logo=<where>  silhouette=round + <what breaks the circle>  main colour=<colour>
  D rimmed:   thing=<the fourth thing>  logo=<where>  silhouette=<one word>  main colour=<colour>
  checks: four different silhouettes? at most two main colours black/charcoal? NO plain plate (disc, tile,
  kite, shield) behind the logo? every thing named by an anchor? no UI card / list / screen drawn small?

concepts (work/{slug}/concepts.png) - four different ideas, EACH carrying anchors (cite them):
  A: <the idea> (anchors 1, 2)
  B: the logo itself as a solid object - <what it looks like> (anchors 1, 2)
  C: <the idea> (anchors ...)
  D: <the idea> (anchors ...)

# the next three lines are the owner's answers, quoted verbatim + date (REDESIGN.md 7), e.g.
#   approved: B - "B" (2026-11-21)      keep: A, D - "A, D" (2026-11-21)      final: "Tamam, pakete ekle" (2026-11-21)
approved:
keep:
final:
styles: symbol=<main> faithful=<kept or main> disc=<kept or main> rimmed=<kept or main>
decisions I made myself (and why; mention them in Q2):
techniques used (min. 3): thickness / material gradient / top light / recess / hole / secondary object / glass
palette (GNOME HIG names):
review (phone.png + review.png: light + dark, holes, baseline, what is still weak):
"""

TEMPLATE = '''#!/usr/bin/env python3
"""{slug} - Gnomed redesign.  The four styles, each a different THING of this app carrying its
measured logo (docs/METHOD.md §1-2, design.md 'worksheet:').
Build:  python3 tools/make_icon.py {slug}      (runs this file, then review + gate)

FIRST look at docs/kit.png: every carrier of work/_lib/carriers.py drawn with real logos. Pick
one per style by the app's own anchors - one line each, the carrier places the logo itself.
No carrier fits an anchor? Draw it yourself like work/reddit, work/duolingo, work/scene,
work/f_droid, work/binance_tr (copy their structure)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "work/_lib"))
from carriers import *  # noqa: F401,F403,E402   (the kit + objects.py + obj.py: gk, solid, put_mark ...)
SLUG = Path(__file__).resolve().parent.name
BRAND = "<the app's main colour, hex, measured from source.png / the screenshots>"


def A():
    """Symbol - <the strongest thing of THIS app> (anchors ...)"""
    ic = gk.Icon("{slug} - symbol")
    raise SystemExit("pick a carrier for the Symbol (docs/kit.png), e.g.  bag(ic, SLUG, BRAND)  - then remove this line")
    return ic


def B():
    """Faithful - the logo itself as a solid object (anchors 1, 2)"""
    ic = gk.Icon("{slug} - faithful")
    logo_object(ic, SLUG, brand=BRAND)
    return ic


def C():
    """Disc - <a ROUND thing of this app> (anchors ...)"""
    ic = gk.Icon("{slug} - disc")
    raise SystemExit("pick a round carrier for the Disc: lens / dial / radar / fan / coin / cup - then remove this line")
    return ic


def D():
    """Rimmed - <the fourth thing, another silhouette> (anchors ...)"""
    ic = gk.Icon("{slug} - rimmed")
    raise SystemExit("pick a carrier for the Rimmed (docs/kit.png) - then remove this line")
    return ic


if __name__ == "__main__":
    save_styles(SLUG, {{"symbol": A(), "faithful": B(), "disc": C(), "rimmed": D()}})
'''

CONCEPTS = '''#!/usr/bin/env python3
"""{slug} - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/{slug}/concepts/make_concepts.py && python3 tools/concepts.py {slug}
Each function is ONE different idea from the ladder; flat shapes are fine. REPLACE the example bodies.
The app's mark always comes from P (measured), never from memory. Ready objects: from objects import *
(catalogue: docs/redesign/OBJECTS.md). NEVER the logo on a plain tile/square or disc (REDESIGN.md 1)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402   (objects.py + obj.py: gk, solid, parts, fit, RAMP ...)

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)        # r0, r1 ... = colour regions; "holes" = what the mark ENCLOSES (a letter's
                       # counter, or a figure inside a ring - e.g. Telegram's plane). Which is which:
                       # print(describe(SLUG)) - colour + box of every part.
R = regions(SLUG)      # the coloured parts [(name, shape, fill)]. Bands of ONE source gradient come
                       # back merged ("r1+r2") with a real gradient fill (Grad) - never colour() per band:
                       # flat bands look melted (docs/PLAYBOOK.md#gradients)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]
# THE MARK ON EVERY STYLE (REDESIGN.md 5, gate `mark`): put_mark(ic, SLUG, box, face=...) draws the
# measured mark WITHOUT the tile under it, inside a layer named "mark" - the gate finds it there.


def A():
    """L1 - the mark itself becomes the object (thickness, light), no plate.
    If one region is only the logo's BACKGROUND (a tile or circle behind the figure), leave it out."""
    ic = gk.Icon("{slug} concept A")
    put_mark(ic, SLUG, (14, 12, 114, 112), body=6, anchor="bottom")    # L1: bottom 112 + side 6 = 118
    return ic


def B():
    """L2 - a GNOME object that carries the mark (the app's FUNCTION as a thing).
    EXAMPLE: an envelope with the mark on its stamp - REPLACE envelope/envelope_stamp with the
    app's object from docs/redesign/OBJECTS.md (bottle + bottle_label, browser_window + browser_page,
    shopping_bag + bag_front, ...). Not a plain rounded square with the logo on it."""
    ic = gk.Icon("{slug} concept B")
    envelope(ic, 64, 118, 108, ramp=RAMP["Blue"])
    put_mark(ic, SLUG, envelope_stamp(64, 118, 108))      # face="#ffffff" for a white mark on a dark part
    return ic


def C():
    """a second, DIFFERENT object idea (another L2 object, or L1 with a secondary object in front)."""
    ic = gk.Icon("{slug} concept C")
    put_mark(ic, SLUG, (16, 12, 112, 115), depth=3, anchor="bottom")   # bottom 115 + side 3 = 118
    return ic


def D():
    """a fourth, different idea - e.g. a ROUND object (it can fill the Disc slot): a coin, a lens,
    a globe ... with the mark. L3 (a material tile) only for a pure wordmark when L1/L2 fail."""
    ic = gk.Icon("{slug} concept D")
    put_mark(ic, SLUG, (24, 22, 104, 114), depth=4, anchor="bottom")     # bottom 114 + side 4 = 118
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
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
Next: python3 tools/next.py {slug}   (it prints each step; the list below is the overview)
  2. fill design.md: kind, anchors, function object. Look at work/{slug}/source.png and
     docs/redesign/gnome-objects.png (REAL GNOME icons: how objects look) - without vision use
     python3 tools/describe_icon.py work/{slug}/source.png and docs/redesign/OBJECTS.md
  3. edit work/{slug}/concepts/make_concepts.py (4 different ideas, A-D), then
     python3 work/{slug}/concepts/make_concepts.py && python3 tools/concepts.py {slug}
  4. Q1 (REDESIGN.md 7): main design + which to keep; write approved:/keep: as his quotes + date
  5. build main + kept in redesign.py  ->  python3 tools/make_icon.py {slug}  ->  Q2""")


if __name__ == "__main__":
    main()
