#!/usr/bin/env python3
"""Safely add an icon (and its alternatives) to a CandyBar-style icon-pack project.

What it does (only additive edits, never deletes):
  * renders the SVG to a transparent PNG (default 256 px, CandyBar's recommendation)
    into app/src/main/res/drawable-nodpi/<name>.png
  * adds <item drawable="name" [name="Label"]/> to drawable.xml (res/xml AND
    assets copies when both exist) inside the requested <category>
  * adds <item component="ComponentInfo{pkg/activity}" drawable="name"/> to
    appfilter.xml (res/xml AND assets copies) - ONLY for components you pass
  * alternatives (--alt FILE.svg[:Label]) become <name>_alt1, _alt2 ... in
    drawable.xml only: users pick them in the launcher's "edit icon" dialog;
    the automatic mapping stays on the primary icon
  * optionally keeps the editable SVG under <project>/artwork/<name>.svg

Safety: refuses invalid/duplicate resource names, refuses a component that is
already mapped to a different drawable (unless --replace), validates every XML
file after editing, and --dry-run prints a unified diff without writing.
It never invents a ComponentInfo: get one with find_component.py.

Usage:
  candybar_add.py --project PATH --name telegram_x --svg work/final.svg \
      --component "ComponentInfo{com.example/com.example.MainActivity}" \
      --category "Social" --label "Example" \
      --alt work/alt-disc.svg:"Example (Disc)" --dry-run
"""
import argparse
import difflib
import keyword
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import render_svg  # noqa: E402

JAVA_KW = set("""abstract assert boolean break byte case catch char class const continue default do double else
enum extends final finally float for goto if implements import instanceof int interface long native new package
private protected public return short static strictfp super switch synchronized this throw throws transient try void
volatile while true false null""".split()) | set(keyword.kwlist)
NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
COMP_RE = re.compile(r"^(ComponentInfo\{[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+\}|:[A-Z_]+)$")


class Edit:
    def __init__(self, path: Path):
        self.path = path
        self.before = path.read_text(encoding="utf-8")
        self.after = self.before

    def diff(self):
        return "".join(difflib.unified_diff(self.before.splitlines(True), self.after.splitlines(True),
                                            str(self.path), str(self.path) + " (new)"))


def indent_of(text, tag="<item"):
    m = re.search(r"^([ \t]*)" + re.escape(tag), text, re.M)
    return m.group(1) if m else "    "


def insert_before_close(text, block, close_tag):
    i = text.rfind(close_tag)
    if i < 0:
        raise ValueError(f"no {close_tag} found")
    j = text.rfind("\n", 0, i) + 1
    return text[:j] + block + text[j:]


def add_to_drawable_xml(text, items, category):
    ind = indent_of(text)
    lines = "".join(f'{ind}<item drawable="{n}"' + (f' name="{lab}"' if lab else "") + " />\n" for n, lab in items)
    cats = list(re.finditer(r'<category\s+title="([^"]*)"\s*/>', text))
    target = [m for m in cats if m.group(1) == category]
    if target:
        m = target[0]
        nxt = [c for c in cats if c.start() > m.end()]
        end = nxt[0].start() if nxt else text.rfind("</resources>")
        seg = text[m.end():end]
        last_item = list(re.finditer(r"^[ \t]*<item[^>]*/>[ \t]*\n", seg, re.M))
        pos = m.end() + (last_item[-1].end() if last_item else seg.find("\n") + 1)
        return text[:pos] + lines + text[pos:]
    block = f'\n{ind}<category title="{category}" />\n' + lines
    return insert_before_close(text, block, "</resources>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True)
    ap.add_argument("--name", required=True, help="drawable resource name (lowercase, a-z0-9_)")
    ap.add_argument("--svg", required=True)
    ap.add_argument("--component", action="append", default=[], help="ComponentInfo{pkg/activity}; repeatable")
    ap.add_argument("--category", default="New")
    ap.add_argument("--label", help="display name in the dashboard (drawable.xml name attribute)")
    ap.add_argument("--alt", action="append", default=[], help="alternative SVG[:Label]; repeatable")
    ap.add_argument("--alt-category", help="put alternatives in this category instead")
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--module", default="app")
    ap.add_argument("--keep-source", action="store_true", help="copy SVGs to <project>/artwork/")
    ap.add_argument("--replace", action="store_true", help="allow overwriting an existing drawable/mapping")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    root = Path(a.project)
    main_dir = root / a.module / "src" / "main"
    if not main_dir.exists():
        sys.exit(f"not an Android module: {main_dir} missing (use --module)")
    nodpi = main_dir / "res" / "drawable-nodpi"
    appfilters = [p for p in (main_dir / "res/xml/appfilter.xml", main_dir / "assets/appfilter.xml") if p.exists()]
    drawables = [p for p in (main_dir / "res/xml/drawable.xml", main_dir / "assets/drawable.xml") if p.exists()]
    if not drawables:
        sys.exit("drawable.xml not found in res/xml or assets: inspect the project layout and adapt manually")
    if (main_dir / "res/values/icon_pack.xml").exists():
        print("note: res/values/icon_pack.xml exists - not modified (add entries manually if your fork uses it)")

    names = [(a.name, a.label, Path(a.svg))]
    for i, spec in enumerate(a.alt, 1):
        f, _, lab = spec.partition(":")
        names.append((f"{a.name}_alt{i}", lab or (f"{a.label} (alt {i})" if a.label else None), Path(f)))
    problems = []
    for n, _, f in names:
        if not NAME_RE.match(n) or n in JAVA_KW:
            problems.append(f"invalid resource name: {n}")
        if not f.exists():
            problems.append(f"missing SVG: {f}")
        existing = [p for p in main_dir.glob(f"res/drawable*/{n}.*")]
        if existing and not a.replace:
            problems.append(f"drawable '{n}' already exists: {existing[0]} (use --replace to overwrite deliberately)")
    normalized = []
    for c in a.component:
        m = re.match(r"^ComponentInfo\{([A-Za-z0-9_.]+)/([A-Za-z0-9_.$]+)\}$", c)
        if m and (m.group(2).startswith(".") or "." not in m.group(2)):
            pkg, act = m.groups()
            full = f"ComponentInfo{{{pkg}/{pkg}{act if act.startswith('.') else '.' + act}}}"
            print(f"note: relative activity expanded: {c} -> {full}")
            c = full
        normalized.append(c)
        if not COMP_RE.match(c):
            problems.append(f"malformed component: {c}  (expected ComponentInfo{{pkg/activity}})")
    a.component = normalized
    edits = [Edit(p) for p in drawables + appfilters]
    for e in edits:
        if e.path.name == "appfilter.xml":
            for c in a.component:
                m = re.search(r'component="' + re.escape(c) + r'"\s+drawable="([^"]+)"', e.before)
                if m and m.group(1) != a.name and not a.replace:
                    problems.append(f"{e.path}: {c} already mapped to '{m.group(1)}' (use --replace)")
    if problems:
        print("REFUSED:\n  " + "\n  ".join(problems))
        sys.exit(1)

    for e in edits:
        if e.path.name == "drawable.xml":
            present = set(re.findall(r'<item\s+drawable="([^"]+)"', e.before))
            prim = [(n, l) for n, l, _ in names[:1] if n not in present]
            alts = [(n, l) for n, l, _ in names[1:] if n not in present]
            t = e.before
            if prim:
                t = add_to_drawable_xml(t, prim, a.category)
            if alts:
                t = add_to_drawable_xml(t, alts, a.alt_category or a.category)
            e.after = t
        else:
            t = e.before
            ind = indent_of(t)
            block = ""
            for c in a.component:
                if re.search(r'component="' + re.escape(c) + r'"\s+drawable="' + re.escape(a.name) + '"', t):
                    continue
                if a.replace:
                    t = re.sub(r'^[ \t]*<item\s+component="' + re.escape(c) + r'"[^>]*/>[ \t]*\n', "", t, flags=re.M)
                block += f'{ind}<item component="{c}" drawable="{a.name}" />\n'
            if block:
                close = "</resources>" if "</resources>" in t else "</appfilter>"
                t = insert_before_close(t, block, close)
            e.after = t

    for e in edits:
        d = e.diff()
        if d:
            print(d)
    for n, _, f in names:
        print(f"{'would write' if a.dry_run else 'write'} {nodpi / (n + '.png')}  <- {f} @ {a.size}px")
    if not a.component:
        print("NOTE: no --component given: icons appear in the dashboard gallery only; launchers will NOT apply them automatically.")
    if a.dry_run:
        print("dry run: nothing written")
        return

    from lxml import etree
    nodpi.mkdir(parents=True, exist_ok=True)
    for n, _, f in names:
        render_svg(f, a.size).save(nodpi / f"{n}.png", optimize=True)
        if a.keep_source:
            (root / "artwork").mkdir(exist_ok=True)
            shutil.copy(f, root / "artwork" / f"{n}.svg")
    for e in edits:
        if e.after != e.before:
            etree.fromstring(e.after.encode("utf-8"))  # raises on malformed XML before writing
            e.path.write_text(e.after, encoding="utf-8")
    # verification
    for e in edits:
        txt = e.path.read_text(encoding="utf-8")
        etree.fromstring(txt.encode("utf-8"))
        for n, _, _ in names:
            if e.path.name == "drawable.xml":
                assert f'drawable="{n}"' in txt, f"{n} missing in {e.path}"
    for n, _, _ in names:
        assert (nodpi / f"{n}.png").exists()
    print("done: XML re-parsed OK, PNGs present. Build the app (./gradlew assembleDebug) and test on a launcher.")


if __name__ == "__main__":
    main()
