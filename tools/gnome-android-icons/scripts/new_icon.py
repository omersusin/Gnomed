#!/usr/bin/env python3
"""MEASURE step of references/redesign.md: scaffold a work folder for one app icon,
get the real source geometry, and prepare the redesign (concepts/, redesign.py, brief.md).

The autodraft it builds (default: one, "faithful") is the source logo placed on a
GNOME template - a MEASURING DRAFT that checks geometry and colours. It is NOT a
design candidate: the icon is designed as an object (concepts -> user approval ->
redesign.py), see references/redesign.md.

Input routing (--input):
  .png .jpg .jpeg .webp .bmp  screenshot / logo image -> extract_icon.py -> source.png
                              -> trace_source.py -> source-trace.svg (real contours)
  .svg                        flatten_svg.py -> source-geometry.svg (exact vector geometry)
  .xml                        Android VectorDrawable -> SVG -> source-geometry.svg
  .apk                        apk_icon.py -> adaptive/vector layers -> source-geometry.svg
                              (bitmap-only icons fall back to the raster route)
Always: analyze_source.py -> analysis.json + identity.md (TODO slots to fill by looking).

Writes  <work>/<slug>/ :
  concepts/     put 3 rough concept SVGs here (A.svg B.svg C.svg) -> concepts.py
  redesign.py   the real build (scripts/obj.py) - write the APPROVED concept here
  brief.md      the decision record; its "approved:" line holds the user's choice
  build.py      measuring drafts (autodraft.py): logo on template shapes
  <slug>-<alt>.svg + review.png   measuring drafts (unless --no-draft)

Usage:
  new_icon.py --slug example --app "Example" --input logo.png \
      [--alts faithful] [--work work] [--no-trace] [--no-draft]
      (--alts faithful,disc,rimmed,symbol,light: more measuring drafts on other templates)
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ALT_DOC = {
    "faithful": "A · Adwaita Faithful - source geometry kept 1:1 on its own template shape + chin, brand colours",
    "disc": "B · Sound Disc - disc face with curvature light, mark lifted/engraved (only if the mark reads on a circle)",
    "rimmed": "C · Rimmed - light Adwaita rim + recessed brand-coloured inner disc (Clocks/Mousai construction)",
    "symbol": "D · Free Symbol - the mark itself is the silhouette, extruded with a chin, no backplate",
    "object": "E · GNOME Metaphor - a domain object that carries the identity anchors (needs a written concept)",
    "light": "F · Light variant - neutral paper plate, mark in brand colour",
}
RASTER = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}

BUILD = '''#!/usr/bin/env python3
"""Build script for {app}.   Run:  python3 build.py

Each build_<alt>() returns one gnome_kit Icon. The bodies start as autodraft
DRAFTS (correct GNOME construction around the REAL source geometry). Refine them:
copy the draft logic, then adjust colours, mark size, glyph lift, chins - but keep
the identity geometry from SRC (source-geometry.svg / source-trace.svg), never
redraw it from memory. See references/archetypes.md for the class of this icon.
"""
import sys
from pathlib import Path

sys.path.insert(0, r"{scripts}")
import gnome_kit as gk  # noqa: E402,F401
import autodraft as ad  # noqa: E402

OUT = Path(__file__).resolve().parent
SRC = ad.Source(OUT)   # SRC.ground / SRC.mark / SRC.brand_color() / SRC.place(box)
{funcs}

ALTS = [{alt_list}]

if __name__ == "__main__":
    print(SRC.describe())
    for name in ALTS:
        icon = globals()["build_" + name]()
        if icon is None:
            print(f"{{name}}: not drafted (needs a hand-made concept)")
            continue
        path = OUT / f"{slug}-{{name}}.svg"
        icon.save(path)
        print(path)
'''

REDESIGN = '''#!/usr/bin/env python3
"""{app} - GNOME redesign (references/redesign.md).
Concept: <the APPROVED concept from brief.md, one line>.
Run: python3 redesign.py   -> {slug}.svg (+ approved alternatives)"""
import sys
from pathlib import Path

sys.path.insert(0, r"{scripts}")
from obj import *  # noqa: F401,F403,E402

OUT = Path(__file__).resolve().parent


def design():
    ic = gk.Icon("{app} - GNOME redesign")
    # 1. the main object: its silhouette IS the icon - not a plate with the logo on it
    body = rounded(box(18, 22, 110, 106), 12)
    solid(ic, body, face=[(0, "#99c1f1"), (0.5, "#62a0ea"), (1, "#3584e4")], depth=8, layer="body")
    # 2. what sits ON or IN it: recess (screen / label / inlay) or hole (lens / slot)
    recess(ic, rounded(box(30, 34, 98, 80), 6), [(0, "#f6f5f4"), (1, "#deddda")], layer="label")
    # 3. optional secondary object in front, lower and smaller, with its own side
    # solid(ic, circ(94, 96, 16), face=[(0, "#ffbe6f"), (1, "#ff7800")], depth=4, layer="badge")
    raise SystemExit("replace the placeholder shapes with the approved concept, then remove this line")
    return ic


if __name__ == "__main__":
    design().save(OUT / "{slug}.svg")
    print(OUT / "{slug}.svg")
'''

FUNC = '''

def build_{alt}():
    """{doc}"""
    return ad.draft_{alt}(SRC, "{app} - {title}")
'''

FUNC_OBJECT = '''

def build_object():
    """{doc}
    Write the concept first (brief.md): which domain object, which identity anchors it
    carries, why it is not a wrapper. Then build it here with gk.Icon / ic.slab / ic.glyphs."""
    return None
'''

TITLES = {"faithful": "Adwaita Faithful", "disc": "Sound Disc", "rimmed": "Rimmed", "symbol": "Free Symbol",
          "light": "Light", "object": "GNOME Metaphor"}


def run(*cmd, check=True):
    print("$", " ".join(map(str, cmd)))
    return subprocess.run([sys.executable, *map(str, cmd)], check=check)


def prepare_source(inp: Path, d: Path, trace: bool):
    ext = inp.suffix.lower()
    if ext in RASTER:
        run(HERE / "extract_icon.py", inp, "--out", d / "source.png", "--report", d / "source.json")
        if trace:
            run(HERE / "trace_source.py", d / "source.png", "--out", d / "source-trace.svg", "--work-size", "768")
        return "raster"
    from _common import render_svg
    if ext == ".svg":
        shutil.copy(inp, d / "source-original.svg")
        run(HERE / "flatten_svg.py", inp, "--out", d / "source-geometry.svg")
    elif ext == ".xml":
        import apk_icon
        (d / "source-vector.svg").write_text(apk_icon.vector_to_svg(inp.read_bytes()))
        run(HERE / "flatten_svg.py", d / "source-vector.svg", "--out", d / "source-geometry.svg")
    elif ext == ".apk":
        run(HERE / "apk_icon.py", "--apk", inp, "--out", d / "apk")
        vis = d / "apk" / "adaptive-visible.svg"
        vec = d / "apk" / "layers" / "icon.svg"
        if vis.exists() or vec.exists():
            run(HERE / "flatten_svg.py", vis if vis.exists() else vec, "--out", d / "source-geometry.svg")
        else:
            bmp = next(iter(sorted((d / "apk").glob("launcher.*"))), None)
            if not bmp:
                sys.exit("APK icon could not be resolved - see apk_icon.py output; pass a screenshot instead")
            return prepare_source(bmp, d, trace)
    else:
        sys.exit(f"unsupported input type: {ext}")
    render_svg(d / "source-geometry.svg", 512).save(d / "source.png")
    return "vector"


def _trace_notes(path: Path) -> str:
    """What the tracer rebuilt or could not capture (source-trace.json) as brief lines."""
    if not path.exists():
        return ""
    import json
    rep = json.loads(path.read_text())
    lines = ["## Trace notes (source-trace.json - check against source.png)"]
    for g in rep.get("gradient_parts") or []:
        lines.append(f"- Gradient surface {g['fill']} (stops {' '.join(g['stops'])}): drafts rebuild it as a GNOME diagonal gradient")
    dp = rep.get("detail_pass") or {}
    if dp.get("regions"):
        lines.append(f"- Detail pass restored {dp['regions']} small region(s)"
                     + (f" (new colours {', '.join(dp['colours_added'])})" if dp.get("colours_added") else ""))
    for m in (rep.get("missed_details") or [])[:6]:
        x0, y0, x1, y1 = m["bbox128"]
        lines.append(f"- NOT traced: {m['colour']} detail at x {x0:.0f}-{x1:.0f}, y {y0:.0f}-{y1:.0f} (128 grid)"
                     " - redraw it by hand if it carries identity")
    if rep.get("smooth_shading") and not rep.get("gradient_parts"):
        lines.append("- Source has smooth shading the flat trace does not carry (decide: GNOME gradient or flat)")
    return "\n".join(lines) + "\n\n" if len(lines) > 1 else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="drawable-style name: lowercase a-z0-9_")
    ap.add_argument("--app", required=True)
    ap.add_argument("--input")
    ap.add_argument("--alts", default="faithful", help="measuring drafts to build (not design candidates)")
    ap.add_argument("--work", default="work")
    ap.add_argument("--no-trace", action="store_true", help="raster input: skip potrace (no drafts possible)")
    ap.add_argument("--trace", action="store_true", help=argparse.SUPPRESS)  # v1.0 compatibility (now default)
    ap.add_argument("--no-draft", action="store_true", help="do not run build.py / review board")
    ap.add_argument("--ref-ids", help="catalog ids for the review board (default: chosen by shape)")
    a = ap.parse_args()
    d = Path(a.work) / a.slug
    d.mkdir(parents=True, exist_ok=True)
    alts = [x.strip() for x in a.alts.split(",") if x.strip()]
    bad = [x for x in alts if x not in ALT_DOC]
    if bad:
        sys.exit(f"unknown alternative(s) {bad}; choose from {list(ALT_DOC)}")
    kind = None
    if a.input:
        kind = prepare_source(Path(a.input), d, trace=not a.no_trace)
        run(HERE / "analyze_source.py", d / "source.png", "--out-md", d / "identity.md", "--json", d / "analysis.json",
            "--name", a.app)
    funcs = "".join(FUNC_OBJECT.format(doc=ALT_DOC[x]) if x == "object" else
                    FUNC.format(alt=x, doc=ALT_DOC[x], app=a.app, title=TITLES[x]) for x in alts)
    bp = d / "build.py"
    if not bp.exists():
        bp.write_text(BUILD.format(app=a.app, scripts=HERE, funcs=funcs, slug=a.slug,
                                   alt_list=", ".join(f'"{x}"' for x in alts)))
    (d / "concepts").mkdir(exist_ok=True)
    rp = d / "redesign.py"
    if not rp.exists():
        rp.write_text(REDESIGN.format(app=a.app, scripts=HERE, slug=a.slug))
    brief = d / "brief.md"
    trace_notes = _trace_notes(d / "source-trace.json")
    if not brief.exists():
        rows = "\n".join(f"| {ALT_DOC[x].split(' - ')[0]} | {a.slug}-{x}.svg |" for x in alts)
        brief.write_text(f"""# {a.app} - icon brief  (status: DRAFT)

## Source
- Input: {a.input or 'TODO'}  ({kind or 'none'} route; see source.json / source-geometry.svg / source-trace.svg)
- Geometry origin: TODO official SVG / APK vector / trace of user image
- Licence / ownership notes: TODO

{trace_notes}## Identity (from identity.md)
- Anchors: TODO
- Must not change: TODO

## Archetype + references
- Archetype: TODO (references/archetypes.md)
- GNOME references compared: TODO ids from assets/reference-library/catalog.json
- Community refs looked at (not policy): TODO

## Function object
- What the app does, as a physical thing: TODO

## Concepts (concepts/*.svg -> concepts.png; references/redesign.md)
- A (L1 the mark becomes an object): TODO
- B (L2 a GNOME object that carries the mark): TODO
- C (L3 material tile, only if A and B fail): TODO

approved:
alternatives (other approved concepts): -

## Measuring drafts (logo on a template - NOT design candidates)
| Draft | File |
|---|---|
{rows}

## Build (redesign.py)
- Techniques used (min. 3): TODO thickness / material / top light / recess / hole / secondary object / glass
- Palette (HIG ramps): TODO

## Review (fill after review.png, legibility.png, launcher.png)
- 32 px: TODO   - 48/64 px: TODO   - family fit: TODO   - launcher: TODO
- Known defects (do not hide): TODO

## Android
- drawable name: {a.slug}
- ComponentInfo: TODO via find_component.py (never guessed)
""")
    have_geometry = (d / "source-geometry.svg").exists() or (d / "source-trace.svg").exists()
    if not a.no_draft and have_geometry:
        run(bp)
        svgs = [str(d / f"{a.slug}-{x}.svg") for x in alts if (d / f"{a.slug}-{x}.svg").exists()]
        if svgs:
            extra = ["--ref-ids", a.ref_ids] if a.ref_ids else []
            run(HERE / "preview_sheet.py", *svgs, "--source", d / "source.png", "--title", f"{a.app} - MEASURING DRAFT (logo on a template, not a design)",
                "--out", d / "review.png", *extra, check=False)
            run(HERE / "legibility_check.py", *svgs, "--out", d / "legibility.png", check=False)
    print(f"""
scaffolded {d}/  - next (references/redesign.md):
  2 STUDY     source.png + examples/redesign/gnome-objects.png; brief.md: anchors, function object
  3 CONCEPTS  {d}/concepts/A.svg B.svg C.svg  ->  concepts.py {d}
  4 ASK       the user picks (multiple choice); write "approved:" in brief.md
  5 BUILD     the approved concept in {d}/redesign.py (scripts/obj.py)""")


if __name__ == "__main__":
    main()
