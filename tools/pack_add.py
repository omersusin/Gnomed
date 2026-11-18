#!/usr/bin/env python3
"""Add a reviewed app to the CandyBar pack (all its styles) - additive only.

    python3 tools/pack_add.py <slug> [--category Tools] [--dry-run]

Reads label + component from work/_lib/batch_apps.tsv, maps Faithful in appfilter and
Disc/Rimmed/Symbol as <slug>_alt1.. in drawable.xml, records them in pack/styles.json
and regenerates the per-style appfilters (tools/gen_styles.py). candybar_add.py refuses
to overwrite an existing drawable or remap a component - nothing is ever deleted.
Always run with --dry-run first and read the diff.
"""
import argparse
import json
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


if __name__ == "__main__":
    main()
