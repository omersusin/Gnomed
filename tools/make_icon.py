#!/usr/bin/env python3
"""One command for one app: measure (if needed), build, review, quality gate.

    python3 tools/make_icon.py <slug>            # after tools/add_source.py registered it
    python3 tools/make_icon.py <slug> --remeasure

Steps it runs, in order (each is also a command you can run alone):
  1. work/_lib/auto.py <slug>           -> work/<slug>/geometry.json   (skipped if it exists)
  2. build: work/_lib/build_weak.py / build_group1.py if the app is hand-built there,
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
    sys.path.insert(0, str(ROOT / "work/_lib"))
    import builders
    if run([sys.executable, builders.builder_of(slug), slug]):
        sys.exit("build failed")
    run(["bash", "tools/review.sh", slug])
    code = run([sys.executable, "tools/check_icon.py", slug])
    if builders.redesigned(slug):
        print(f"\nNext (AGENTS.md C7-C9): a FAIL -> AGENTS.md section I, fix redesign.py, run this again. "
              f"0 FAIL -> open work/{slug}/review.png, answer AGENTS.md D, then ASK the owner "
              f"(Tamam / Şunu değiştir / Konseptlere dön). Only after his OK: "
              f"python3 tools/pack_add.py {slug} --category <Category> --dry-run "
              f"(already in the pack: python3 tools/pack_refresh.py {slug})")
    else:
        print(f"\nThis is the automatic DRAFT (measuring only). Next: python3 tools/new_redesign.py {slug} "
              f"(AGENTS.md C3). Wrong parts/colours in the measurement: python3 tools/region_check.py {slug}")
    sys.exit(code)


if __name__ == "__main__":
    main()
