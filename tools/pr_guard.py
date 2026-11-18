#!/usr/bin/env python3
"""Check that a branch only ADDS to the pack and does not do maintainer-only things.

    python3 tools/pr_guard.py                       # your branch vs origin/main
    python3 tools/pr_guard.py <base> <head>         # e.g. origin/main HEAD

Run it before you open a pull request; CI runs it on every pull request
(.github/workflows/pr-guard.yml). Exit 1 on any ERROR.

ERROR (the PR cannot be merged like this):
  * an icon PNG, artwork SVG or work/<slug>/source.png was deleted or renamed
  * an <item> was removed or changed in appfilter.xml / drawable.xml (res/xml or assets)
  * an app or one of its styles was removed from pack/styles.json
  * a commit message contains [release] (that would publish a release)
  * the branch is main / master
WARN (allowed, but the maintainer must look closely):
  * CI workflows, Gradle build files, ProGuard rules, signing, AGENTS.md
"""
import json
import re
import subprocess
import sys

PACK_FILES = ("app/src/main/res/drawable-nodpi/", "artwork/")
ITEM_FILES = ("app/src/main/res/xml/appfilter.xml", "app/src/main/assets/appfilter.xml",
              "app/src/main/res/xml/drawable.xml", "app/src/main/assets/drawable.xml")
SENSITIVE = (".github/", "app/build.gradle", "build.gradle", "settings.gradle", "gradle/",
             "app/proguard-rules.pro", "AGENTS.md", "tools/hooks/", "tools/pr_guard.py")
ITEM = re.compile(r"<item\b[^>]*?/>")


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def show(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def items(text):
    return {re.sub(r"\s+", " ", m.group(0)) for m in ITEM.finditer(text)}


def main():
    base, head = (sys.argv[1:3] + [None, None])[:2]
    base = base or "origin/main"
    head = head or "HEAD"
    errors, warns = [], []

    branch = git("rev-parse", "--abbrev-ref", head, check=False).strip()
    if branch in ("main", "master"):
        errors.append(f"you are on '{branch}' - create your own branch (AGENTS.md section 0)")

    for line in git("diff", "--name-status", "-M", base, head).splitlines():
        status, *paths = line.split("\t")
        old, new = paths[0], paths[-1]
        if status[0] in "DR" and (old.startswith(PACK_FILES) or re.fullmatch(r"work/[^/]+/source\.png", old)):
            errors.append(f"{old} was {'deleted' if status[0] == 'D' else 'renamed to ' + new} - never delete or rename pack files")
        for p in {old, new}:
            if p.startswith(SENSITIVE) or p == "gradle.properties":
                warns.append(f"{p} changed ({status}) - maintainer-only area, review it line by line")

    for path in ITEM_FILES:
        gone = items(show(base, path)) - items(show(head, path))
        for it in sorted(gone):
            errors.append(f"{path}: removed or changed {it}")

    try:
        old = json.loads(show(base, "pack/styles.json") or "{}").get("icons", {})
        new = json.loads(show(head, "pack/styles.json") or "{}").get("icons", {})
    except json.JSONDecodeError as e:
        errors.append(f"pack/styles.json is not valid JSON: {e}")
        old, new = {}, {}
    for app, styles in old.items():
        if app not in new:
            errors.append(f"pack/styles.json: app '{app}' removed")
            continue
        for st, dr in styles.items():
            if new[app].get(st) != dr:
                errors.append(f"pack/styles.json: {app}.{st} '{dr}' -> '{new[app].get(st)}'")

    for line in git("log", "--format=%h %s%n%b%x00", f"{base}..{head}").split("\x00"):
        if re.search(r"\[release\]", line, re.I):
            errors.append(f"commit {line.split()[0]} has [release] in its message - only the maintainer releases")

    for w in sorted(set(warns)):
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"pr_guard: {len(errors)} ERROR, {len(set(warns))} WARN ({base}..{head})")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
