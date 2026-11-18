#!/usr/bin/env python3
"""Find the real launcher component (ComponentInfo{package/activity}) of an app.

Never guess components: a wrong activity name silently does nothing on the
launcher.  Sources, most to least reliable:

  --adb PACKAGE        ask the connected phone (USB debugging): resolves the
                       MAIN/LAUNCHER activity exactly as the launcher does
  --adb-all [--grep X] list every launcher activity on the phone
  --apk FILE.apk       read the APK manifest (androguard, or `aapt` if installed)
  --pull PACKAGE --out DIR   copy the installed APK(s) from the phone (for apk_icon.py)

Alternative without a computer: the "Icon Request" style apps (and CandyBar's own
request screen) export appfilter lines from the phone.

Output lines are ready to paste: ComponentInfo{pkg/full.activity.Name}
"""
import argparse
import re
import shutil
import subprocess
import sys


def norm(pkg, act):
    act = act.strip()
    if act.startswith("."):
        act = pkg + act
    elif "." not in act:
        act = f"{pkg}.{act}"
    return f"ComponentInfo{{{pkg}/{act}}}"


def parse_brief(text):
    """Parse lines like 'com.pkg/.Main' or 'com.pkg/com.pkg.Main' (resolve-activity --brief)."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_.]+)/([A-Za-z0-9_.$]+)\s*$", line)
        if m:
            out.append(norm(m.group(1), m.group(2)))
    return out


def adb(*args):
    if not shutil.which("adb"):
        sys.exit("adb not found: install Android platform-tools and enable USB debugging")
    r = subprocess.run(["adb", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip() or "adb failed")
    return r.stdout


def from_apk(path):
    try:
        from androguard.core.apk import APK  # androguard >= 4
    except ImportError:
        try:
            from androguard.core.bytecodes.apk import APK  # androguard 3
        except ImportError:
            APK = None
    if APK:
        apk = APK(path)
        pkg = apk.get_package()
        return [norm(pkg, act) for act in sorted(apk.get_main_activities())]
    if shutil.which("aapt"):
        out = subprocess.run(["aapt", "dump", "badging", path], capture_output=True, text=True).stdout
        pkg = re.search(r"package: name='([^']+)'", out).group(1)
        return [norm(pkg, a) for a in re.findall(r"launchable-activity: name='([^']+)'", out)]
    sys.exit("pip install androguard (or install aapt) to read APKs")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--adb")
    g.add_argument("--adb-all", action="store_true")
    g.add_argument("--apk")
    g.add_argument("--pull")
    ap.add_argument("--grep")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    if a.adb:
        res = parse_brief(adb("shell", "cmd", "package", "resolve-activity", "--brief", "-a", "android.intent.action.MAIN",
                              "-c", "android.intent.category.LAUNCHER", a.adb))
        if not res:
            sys.exit(f"{a.adb}: no launcher activity (not installed, or no launcher entry)")
        print("\n".join(res))
    elif a.adb_all:
        res = parse_brief(adb("shell", "cmd", "package", "query-activities", "--brief", "-a", "android.intent.action.MAIN",
                              "-c", "android.intent.category.LAUNCHER"))
        print("\n".join(r for r in res if not a.grep or a.grep.lower() in r.lower()))
    elif a.apk:
        print("\n".join(from_apk(a.apk)))
    elif a.pull:
        paths = [l.split(":", 1)[1].strip() for l in adb("shell", "pm", "path", a.pull).splitlines() if l.startswith("package:")]
        for p in paths:
            print(adb("pull", p, a.out).strip())


if __name__ == "__main__":
    main()
