#!/usr/bin/env python3
"""One command for one app: measure (if needed), build, review, quality gate.

    python3 tools/make_icon.py <slug>            # after tools/add_source.py registered it
    python3 tools/make_icon.py <slug> --remeasure

Steps it runs, in order (each is also a command you can run alone):
  1. work/_lib/auto.py <slug>           -> work/<slug>/geometry.json   (skipped if it exists)
  2. build: work/_lib/build_weak.py if the app has a hand-built function there,
            otherwise work/_lib/build_auto.py <slug>                  -> work/<slug>/<slug>-<style>.svg
  3. tools/review.sh <slug>             -> lint, PNG export, legibility, review.png, styles.png
  4. tools/check_icon.py <slug>         -> PASS/WARN/FAIL with the FIX for each problem
Exit code = check_icon's (0 = no FAIL).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd):
    print("\n$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    if not (ROOT / "work" / slug / "source.png").exists():
        sys.exit(f"work/{slug}/source.png missing - run tools/add_source.py first")
    if "--remeasure" in sys.argv or not (ROOT / "work" / slug / "geometry.json").exists():
        if run([sys.executable, "work/_lib/auto.py", slug]):
            sys.exit("auto.py failed")
    hand = f"def {slug}(" in (ROOT / "work/_lib/build_weak.py").read_text()
    if run([sys.executable, "work/_lib/build_weak.py" if hand else "work/_lib/build_auto.py", slug]):
        sys.exit("build failed")
    run(["bash", "tools/review.sh", slug])
    code = run([sys.executable, "tools/check_icon.py", slug])
    print(f"\nNext: open work/{slug}/styles.png (if you can see images), fix every FAIL "
          f"(docs/course/04-recipes.md), re-run this command. When it ends with 0 FAIL: "
          f"python3 tools/pack_add.py {slug} --category <Category> --dry-run")
    sys.exit(code)


if __name__ == "__main__":
    main()
