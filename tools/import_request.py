#!/usr/bin/env python3
"""Read an icon request from the phone and register its apps - with or without zip.

    python3 tools/import_request.py <input> [<more inputs> ...]          # list only (safe)
    python3 tools/import_request.py <input> --add [--only slug1,slug2]   # register new apps

<input> may be any of these (mix them freely, e.g. a text file + a folder of PNGs):

  * a zip from Gnomed's request screen        appfilter.xml + <drawable>.png
  * a zip from the IconRequest app             appfilter.xml + icons/<drawable>.png
    (de.kaiserdragon.iconrequest)
  * a folder: an unpacked zip, or the files Gnomed shares with
    "Share as images + text (no zip)"          request.txt + <drawable>.png
  * a text file: request.txt, appfilter.xml, or any text you saved from a chat that
    contains appfilter lines or "App | ComponentInfo{...} | file.png" lines
  * an http(s) URL of a zip (e.g. a file attached to a GitHub issue)
  * "-" to read pasted text from stdin

Without --add nothing is written. The table shows, for every app in the request:

  NEW         not in the pack, icon PNG found        -> --add registers it
  NO-ICON     not in the pack, but no PNG for it     -> ask the human for the icon
  IN-PACK     the component is already in appfilter.xml (nothing to do)
  REGISTERED  the slug is already in work/_lib/batch_apps.tsv (work in progress)
  BAD         the line is not a valid ComponentInfo  -> ask the human

--add calls the same code as tools/add_source.py (work/<slug>/source.png + batch_apps.tsv).
It never touches the pack; next step per app: python3 tools/make_icon.py <slug>.
ComponentInfo lines in these files come from the phone - that is a valid source.
"""
import argparse
import re
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import add_source  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PACK_APPFILTER = ROOT / "app/src/main/res/xml/appfilter.xml"

# <!-- Label --> <item component="ComponentInfo{...}" drawable="name" />
XML_ITEM = re.compile(r"<!--\s*(.*?)\s*-->\s*<item\s+component=\"(ComponentInfo\{[^}]*\})\"\s+drawable=\"([^\"]+)\"", re.S)
XML_BARE = re.compile(r"<item\s+component=\"(ComponentInfo\{[^}]*\})\"\s+drawable=\"([^\"]+)\"")
# Label | ComponentInfo{...} | drawable.png   (Gnomed's request.txt)
TXT_ROW = re.compile(r"^\s*(.+?)\s*\|\s*(ComponentInfo\{[^}]*\})\s*\|\s*([^|\s]+?)(?:\.png)?\s*$", re.M)
DIGITS = "zero one two three four five six seven eight nine".split()


def to_slug(drawable):
    """CandyBar drawable names must start with a letter: _1dm -> onedm, 2fas -> twofas."""
    import unicodedata
    t = drawable.replace("ı", "i").replace("İ", "i")          # Turkish dotless i (pokemon_unıte)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9_]+", "_", t.lower()).strip("_")
    s = re.sub(r"_+", "_", s)
    if s and s[0].isdigit():
        s = DIGITS[int(s[0])] + s[1:]
    return s or "app"


def parse_text(text):
    """-> list of (label, component, drawable) in order, de-duplicated by component."""
    rows, seen = [], set()
    for m in XML_ITEM.finditer(text):
        rows.append((m.group(1), m.group(2), m.group(3)))
    if not rows:
        for m in XML_BARE.finditer(text):
            rows.append((m.group(2), m.group(1), m.group(2)))
    for m in TXT_ROW.finditer(text):
        rows.append((m.group(1), m.group(2), m.group(3)))
    out = []
    for r in rows:
        if r[1] not in seen:
            seen.add(r[1])
            out.append(r)
    return out


def fetch(url, tmp):
    dest = Path(tmp) / "download.zip"
    req = urllib.request.Request(url, headers={"User-Agent": "gnomed-import-request"})
    with urllib.request.urlopen(req, timeout=60) as r, dest.open("wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def collect(inputs, tmp):
    """-> (texts, {drawable_lower: png_path})"""
    texts, pngs = [], {}

    def add_png(path):
        pngs.setdefault(path.stem.lower(), path)

    def scan_dir(d):
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            low = p.name.lower()
            if low.endswith(".png"):
                add_png(p)
            elif low in ("appfilter.xml", "request.txt") or low.endswith((".txt", ".md")):
                texts.append(p.read_text(encoding="utf-8", errors="replace"))

    for i, inp in enumerate(inputs):
        if inp == "-":
            texts.append(sys.stdin.read())
            continue
        if re.match(r"https?://", inp):
            inp = str(fetch(inp, tmp))
        p = Path(inp)
        if not p.exists():
            sys.exit(f"not found: {inp}")
        if p.is_dir():
            scan_dir(p)
        elif zipfile.is_zipfile(p):
            d = Path(tmp) / f"zip{i}"
            with zipfile.ZipFile(p) as z:
                for info in z.infolist():
                    name = Path(info.filename)
                    if info.is_dir() or ".." in name.parts or name.is_absolute():
                        continue
                    target = d / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(z.read(info))
            scan_dir(d)
        elif p.suffix.lower() == ".png":
            add_png(p)
        else:
            texts.append(p.read_text(encoding="utf-8", errors="replace"))
    return texts, pngs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--add", action="store_true", help="register the NEW apps (default: list only)")
    ap.add_argument("--only", help="comma-separated slugs to add (default: every NEW app)")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        texts, pngs = collect(args.inputs, tmp)
        rows = parse_text("\n".join(texts))
        if not rows:
            sys.exit("no apps found: expected appfilter lines or 'App | ComponentInfo{...} | file.png' lines")
        in_pack = set(re.findall(r"ComponentInfo\{[^}]*\}", PACK_APPFILTER.read_text(encoding="utf-8")))
        registered = add_source.registered_slugs()
        only = set(args.only.split(",")) if args.only else None

        plan = []
        for label, comp, drawable in rows:
            slug = to_slug(drawable)
            png = pngs.get(drawable.lower()) or pngs.get(slug)
            if not re.fullmatch(add_source.COMP_RE, comp):
                status = "BAD"
            elif comp in in_pack:
                status = "IN-PACK"
            elif slug in registered and (ROOT / "work" / slug / "source.png").exists():
                status = "REGISTERED"
            elif png is None:
                status = "NO-ICON"
            else:
                status = "NEW"
            plan.append((status, slug, label, comp, png))

        w = max(len(p[1]) for p in plan)
        for status, slug, label, comp, png in plan:
            print(f"{status:<10} {slug:<{w}}  {label}  {comp}")
        counts = {s: sum(1 for p in plan if p[0] == s) for s in ("NEW", "NO-ICON", "IN-PACK", "REGISTERED", "BAD")}
        print("summary: " + ", ".join(f"{n} {s}" for s, n in counts.items() if n))

        if not args.add:
            if counts["NEW"]:
                print("list only - nothing written. Register with --add (or --add --only slug1,slug2).")
            return
        added = 0
        for status, slug, label, comp, png in plan:
            if status != "NEW" or (only and slug not in only):
                continue
            err = add_source.register(slug, png, label, comp)
            if err:
                print(f"SKIP {slug}: {err}")
            else:
                added += 1
                print(f"added {slug}: work/{slug}/source.png  -> next: python3 tools/make_icon.py {slug}")
        print(f"added {added} app(s). The pack is unchanged until tools/pack_add.py.")


if __name__ == "__main__":
    main()
