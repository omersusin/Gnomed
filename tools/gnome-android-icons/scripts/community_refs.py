#!/usr/bin/env python3
"""Search MoreWaita and Adwaita++ (community Adwaita-style themes) for an app.

These themes are NOT GNOME policy, and many of their icons are third-party
brand marks, so this skill does not redistribute them.  Point this script at
your own local copy (zip or extracted folder) - e.g. the MoreWaita-main.zip /
adwaita-plus-master.zip archives - or let it shallow-clone from GitHub.

Usage:
  community_refs.py --search telegram [--search "google chrome"] \
      [--morewaita ~/src/MoreWaita-main.zip] [--adwaitapp ~/src/adwaita-plus-master.zip] \
      [--fetch] [--sheet work/community.png] [--copy-to work/community/]

Config: paths can also come from env GNOME_ICONS_MOREWAITA / GNOME_ICONS_ADWAITAPP.
Copies go to your *work* folder for study only; keep them out of the icon pack.
"""
import argparse
import difflib
import io
import os
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REPOS = {"morewaita": "https://github.com/somepaulo/MoreWaita",
         "adwaitapp": "https://github.com/Bonandry/adwaita-plus"}
APP_DIRS = {"morewaita": ["scalable/apps"], "adwaitapp": ["Adwaita++/apps/scalable"]}
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "gnome-android-icons"


class Source:
    def __init__(self, kind, path):
        self.kind, self.path = kind, Path(path).expanduser()
        self.zip = zipfile.ZipFile(self.path) if self.path.suffix == ".zip" else None
        self.index = {}  # lower name -> (member, is_link_target)
        self._build()

    def _build(self):
        dirs = APP_DIRS[self.kind]
        if self.zip:
            for zi in self.zip.infolist():
                n = zi.filename
                if n.endswith(".svg") and any(f"/{d}/" in "/" + n for d in dirs):
                    is_link = (zi.external_attr >> 16) & 0o170000 == 0o120000
                    self.index[Path(n).stem.lower()] = (n, is_link)
        else:
            for d in dirs:
                for p in self.path.glob(f"**/{d}/*.svg"):
                    self.index[p.stem.lower()] = (str(p), p.is_symlink())

    def read(self, member, depth=0):
        if self.zip:
            data = self.zip.read(member)
            is_link = self.index.get(Path(member).stem.lower(), (None, False))[1]
            if is_link and depth < 5 and len(data) < 300:  # symlink stored as text
                target = (Path(member).parent / data.decode().strip()).as_posix()
                return self.read(target, depth + 1)
            return data
        return Path(member).resolve().read_bytes()

    def search(self, q, n=8):
        q = q.lower().replace(" ", "")
        names = list(self.index)
        hits = [k for k in names if q in k.replace("-", "").replace("_", "").replace(".", "")]
        if not hits:  # fuzzy only as a fallback
            hits = difflib.get_close_matches(q, names, n=n, cutoff=0.75)
        return hits[:n]


def ensure_clone(kind):
    dest = CACHE / kind
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", REPOS[kind], str(dest)], check=True)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--search", action="append", required=True)
    ap.add_argument("--morewaita", default=os.environ.get("GNOME_ICONS_MOREWAITA"))
    ap.add_argument("--adwaitapp", default=os.environ.get("GNOME_ICONS_ADWAITAPP"))
    ap.add_argument("--fetch", action="store_true", help="shallow-clone missing themes from GitHub into ~/.cache")
    ap.add_argument("--sheet", help="render hits into a contact sheet PNG")
    ap.add_argument("--copy-to", help="copy hit SVGs into this work folder (study only)")
    a = ap.parse_args()
    srcs = []
    for kind in ("morewaita", "adwaitapp"):
        p = getattr(a, kind)
        if not p and a.fetch:
            p = ensure_clone(kind)
        if p and Path(p).expanduser().exists():
            srcs.append(Source(kind, p))
        else:
            print(f"[{kind}] not available (pass --{kind} PATH or --fetch)", file=sys.stderr)
    if not srcs:
        sys.exit(2)
    out_dir = Path(a.copy_to or (Path(a.sheet).parent / "community" if a.sheet else "community-refs"))
    found, seen = [], set()
    import hashlib
    for q in a.search:
        for s in srcs:
            for k in s.search(q):
                member, is_link = s.index[k]
                data = s.read(member)
                h = hashlib.sha1(data).hexdigest()
                if h in seen:
                    continue  # alias of an icon already listed
                seen.add(h)
                out_dir.mkdir(parents=True, exist_ok=True)
                dst = out_dir / f"{s.kind}__{Path(member).name}"
                dst.write_bytes(data)
                found.append(str(dst))
                print(f"[{s.kind}] {q!r}: {Path(member).name}{' (alias)' if is_link else ''} -> {dst}")
    if a.sheet and found:
        subprocess.run([sys.executable, str(Path(__file__).with_name("contact_sheet.py")), a.sheet, *found,
                        "--size", "128", "--cols", "6", "--bg", "both", "--title", "Community Adwaita-style refs (not GNOME policy)"],
                       check=True)
    if not found:
        print("no matches - the app is not themed there; use official GNOME analogues instead")


if __name__ == "__main__":
    main()
