#!/usr/bin/env python3
"""Add a reviewed app to the CandyBar pack (all its styles) - additive only.

    python3 tools/pack_add.py <slug> [--category Tools] [--dry-run]

Reads label + component from work/_lib/batch_apps.tsv, maps Faithful in appfilter and
Disc/Rimmed/Symbol as <slug>_alt1.. in drawable.xml, records them in pack/styles.json
and regenerates the per-style appfilters (tools/gen_styles.py). candybar_add.py refuses
to overwrite an existing drawable or remap a component - nothing is ever deleted.
Always run with --dry-run first and read the diff.

An app that is ALREADY in the pack: only its missing styles are added (e.g. a Symbol
built later) as the next free <slug>_altN, in the app's existing category; the
Faithful icon and the existing styles are not touched.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADD = ROOT / "tools/gnome-android-icons/scripts/candybar_add.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--category", default="Tools")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows = {l.split("\t")[0]: l.rstrip("\n").split("\t") for l in (ROOT / "work/_lib/batch_apps.tsv").read_text(encoding="utf-8").splitlines()}
    if a.slug not in rows:
        sys.exit(f"{a.slug} not in work/_lib/batch_apps.tsv (tools/add_source.py registers it)")
    _, label, comp, _ = rows[a.slug]
    w = ROOT / "work" / a.slug
    if (ROOT / f"app/src/main/res/drawable-nodpi/{a.slug}.png").exists():
        return add_missing_styles(a, label, w)
    if not (w / f"{a.slug}-faithful.svg").exists():
        sys.exit("work/<slug>/<slug>-faithful.svg missing - every app needs a Faithful style")
    cmd = [sys.executable, str(ADD), "--project", str(ROOT), "--name", a.slug, "--svg", str(w / f"{a.slug}-faithful.svg"),
           "--label", label, "--category", a.category, "--component", comp, "--keep-source"]
    styles = {}
    for st in ("disc", "rimmed", "symbol"):
        f = w / f"{a.slug}-{st}.svg"
        if f.exists():
            cmd += ["--alt", f"{f}:{label} ({st.capitalize()})"]
            styles[st] = f"{a.slug}_alt{len(styles) + 1}"
    if a.dry_run:
        cmd.append("--dry-run")
    r = subprocess.run(cmd)
    if r.returncode or a.dry_run:
        sys.exit(r.returncode)
    p = ROOT / "pack/styles.json"
    c = json.loads(p.read_text())
    c["icons"][a.slug] = styles
    p.write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n")
    subprocess.run([sys.executable, str(ROOT / "tools/gen_styles.py")], check=True)
    print("added. Now: python3 tools/gnome-android-icons/scripts/pack_audit.py --project .")


def add_missing_styles(a, label, w):
    """The app is in the pack: add only styles that have an SVG but no drawable yet."""
    p = ROOT / "pack/styles.json"
    c = json.loads(p.read_text())
    have = c["icons"].get(a.slug, {})
    xml = (ROOT / "app/src/main/res/xml/drawable.xml").read_text(encoding="utf-8")
    m = re.search(r'<category title="([^"]+)"\s*/>(?:(?!<category).)*?<item drawable="' + re.escape(a.slug) + '"', xml, re.S)
    category = m.group(1) if m else a.category
    used = [int(n) for n in re.findall(r'drawable="' + re.escape(a.slug) + r'_alt(\d+)"', xml)]
    nxt = max(used, default=0) + 1
    todo = [st for st in ("disc", "rimmed", "symbol") if st not in have and (w / f"{a.slug}-{st}.svg").exists()]
    if not todo:
        sys.exit(f"{a.slug} is already in the pack with every style it has an SVG for - nothing to add "
                 "(to improve existing icons use tools/pack_refresh.py)")
    plan = {}
    for st in todo:
        name = f"{a.slug}_alt{nxt}"
        nxt += 1
        cmd = [sys.executable, str(ADD), "--project", str(ROOT), "--name", name,
               "--svg", str(w / f"{a.slug}-{st}.svg"), "--label", f"{label} ({st.capitalize()})",
               "--category", category, "--keep-source"] + (["--dry-run"] if a.dry_run else [])
        print(f"{a.slug}: add style {st} as {name} (category {category})")
        r = subprocess.run(cmd)
        if r.returncode:
            sys.exit(r.returncode)
        plan[st] = name
    print(f"pack/styles.json: {a.slug} {have} -> {dict(have, **plan)}")
    for st, name in plan.items():
        print(f"app/src/{st}/ appfilter: {a.slug} -> {name} (tools/gen_styles.py)")
    if a.dry_run:
        return
    c["icons"][a.slug] = dict(have, **plan)
    p.write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n")
    subprocess.run([sys.executable, str(ROOT / "tools/gen_styles.py")], check=True)
    print("added. Now: python3 tools/gnome-android-icons/scripts/pack_audit.py --project .")


if __name__ == "__main__":
    main()
