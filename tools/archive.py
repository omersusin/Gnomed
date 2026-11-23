#!/usr/bin/env python3
"""The archive: every version of every icon, as plain files you can open and bring back.

The owner (2026-11-23): "çalışma alanındaki eski simgeleri ve diğer şeyleri arşive eklesin. Böylece
hiçbir şey kaybetmemiş oluruz. ... bir şeyi beğenmedim. O şeyi geri döndürebilirim."

    archive/<slug>/<date>_<time>_<label>/   one version of one app (names sort in time order)
        <slug>-symbol.svg ...           the four styles (whatever existed)
        symbol.png ...                  pack snapshots only: the PNG that shipped
        redesign.py, design.md          the code and the decisions behind them
        concepts/                       the concept drawings of that round (when they changed)
        fixes*.md                       the review lists of that time
        info.txt                        where it came from (work / pack / git commit) and when

    python3 tools/archive.py snap <slug> [--label before-x]      the app's work/ files now
    python3 tools/archive.py pack <slug> ... | --all              the icons now in the pack
    python3 tools/archive.py history <slug> ... | --all [--ref R] every version in git history
    python3 tools/archive.py list <slug>                          the versions of an app
    python3 tools/archive.py restore <slug> <version> [--style disc]
    python3 tools/archive.py compare <slug> ... [--old pack|<version>] --out old-new.png
    python3 tools/archive.py index                                archive/INDEX.md (local, not committed:
                                                                  it would conflict between branches)

A version that is already in the archive (same four styles) is not stored twice. next.py takes a
snapshot by itself before the owner's fixes and before a redo; pack_refresh.py before it
overwrites the pack. Nothing in archive/ is ever deleted.
"""
import hashlib
import io
import json
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "archive"
STYLES = ("symbol", "faithful", "disc", "rimmed")
NODPI = ROOT / "app/src/main/res/drawable-nodpi"


def git(*args, binary=False):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def style_names(slug, styles_json=None):
    icons = (styles_json or json.loads((ROOT / "pack/styles.json").read_text()))["icons"]
    return {"faithful": slug, **icons.get(slug, {})}


def versions(slug):
    d = ARCH / slug
    return sorted(p for p in d.iterdir() if p.is_dir()) if d.exists() else []


def fingerprint(files):
    """the styles decide whether two versions are the same"""
    h = hashlib.sha1()
    for name in sorted(files):
        if name.endswith(".svg") and any(name.endswith(f"-{s}.svg") for s in STYLES):
            h.update(name.encode() + b"\0" + files[name])
    return h.hexdigest()


def stored_fingerprint(v):
    files = {p.name: p.read_bytes() for p in v.glob("*.svg")}
    return fingerprint(files) if files else None


def write_version(slug, label, files, info, day=None):
    """files: {relative name: bytes}. -> the new folder, or None when that version is already archived
    (pack snapshots are compared with pack snapshots, the others with the others)"""
    if not any(n.endswith(".svg") or n.endswith(".png") for n in files):
        return None
    fp = fingerprint(files)
    is_pack = label.startswith("pack")
    same_kind = [v for v in versions(slug) if ("_pack" in v.name) == is_pack]
    if fp != hashlib.sha1().hexdigest() and any(stored_fingerprint(v) == fp for v in same_kind):
        return None
    day = day or datetime.now().strftime("%Y-%m-%d_%H%M")      # the folder names sort in time order
    base = ARCH / slug / f"{day}_{label}"
    dst, n = base, 2
    while dst.exists():
        dst, n = base.with_name(f"{base.name}_{n}"), n + 1
    for name, data in files.items():
        p = dst / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    (dst / "info.txt").write_text(info.rstrip() + "\n", encoding="utf-8")
    return dst


def work_files(slug):
    w = ROOT / "work" / slug
    files = {}
    for st in STYLES:
        p = w / f"{slug}-{st}.svg"
        if p.exists():
            files[p.name] = p.read_bytes()
    for name in ("redesign.py", "design.md"):
        if (w / name).exists():
            files[name] = (w / name).read_bytes()
    for p in sorted(w.glob("fixes*.md")):
        files[p.name] = p.read_bytes()
    for p in sorted((w / "concepts").glob("*")) if (w / "concepts").exists() else []:
        if p.suffix in (".svg", ".py") and p.is_file():
            files[f"concepts/{p.name}"] = p.read_bytes()
    return files


def snap(slug, label="work", quiet=False):
    head = git("rev-parse", "--short", "HEAD").strip()
    dst = write_version(slug, label, work_files(slug),
                        f"source: work/{slug}/ (the working copy)\nbranch commit: {head}\ntaken: {date.today()}\nlabel: {label}")
    if not quiet:
        print(f"{slug}: " + (f"stored {dst.relative_to(ROOT)}" if dst else "same as the newest archived version - nothing stored"))
    return dst


def pack(slug, label="pack", quiet=False):
    files = {}
    for st, name in style_names(slug).items():
        png, svg = NODPI / f"{name}.png", ROOT / f"artwork/{name}.svg"
        if png.exists():
            files[f"{st}.png"] = png.read_bytes()
        if svg.exists():
            files[f"{slug}-{st}.svg"] = svg.read_bytes()
    if not files:
        if not quiet:
            print(f"{slug}: not in the pack")
        return None
    dst = write_version(slug, label, files,
                        f"source: the pack (app/src/main/res/drawable-nodpi + artwork/) as it shipped\ntaken: {date.today()}\nlabel: {label}")
    if not quiet:
        print(f"{slug}: " + (f"stored {dst.relative_to(ROOT)}" if dst else "same as the newest archived version"))
    return dst


def history(slug, ref="HEAD"):
    paths = [f"work/{slug}/{slug}-{st}.svg" for st in STYLES]
    commits = git("log", "--full-history", "--reverse", "--date=format:%Y-%m-%d_%H%M", "--format=%H %cd %s",
                  ref, "--", *paths).splitlines()
    stored = 0
    for c in commits:
        sha, day, subject = c.split(" ", 2)
        listed = git("ls-tree", "-r", "--name-only", sha, f"work/{slug}/").split()
        files = {}
        for rel in listed:
            name = rel[len(f"work/{slug}/"):]
            keep = (name in {f"{slug}-{st}.svg" for st in STYLES} or name in ("redesign.py", "design.md")
                    or (name.startswith("fixes") and name.endswith(".md"))
                    or (name.startswith("concepts/") and name.count("/") == 1 and name.endswith((".svg", ".py"))))
            if keep:
                files[name] = git("show", f"{sha}:{rel}", binary=True)
        dst = write_version(slug, sha[:7], files,
                            f"source: git commit {sha} ({day})\nsubject: {subject}\nlabel: {sha[:7]}", day=day)
        stored += bool(dst)
    print(f"{slug}: {len(commits)} commit(s) in history, {stored} new version(s) stored")


def restore(slug, ver, style=None):
    v = ARCH / slug / ver
    if not v.is_dir():
        sys.exit(f"no version {ver} - python3 tools/archive.py list {slug}")
    snap(slug, "before-restore")
    w = ROOT / "work" / slug
    styles = [style] if style else list(STYLES)
    done = []
    for st in styles:
        src = v / f"{slug}-{st}.svg"
        if src.exists():
            shutil.copy(src, w / src.name)
            done.append(st)
    if not style and (v / "redesign.py").exists():
        shutil.copy(v / "redesign.py", w / "redesign.py")
        if (v / "concepts").is_dir():
            for p in (v / "concepts").iterdir():
                (w / "concepts").mkdir(exist_ok=True)
                shutil.copy(p, w / "concepts" / p.name)
        done.append("redesign.py")
    with open(w / "design.md", "a", encoding="utf-8") as f:
        f.write(f"\nrestored: {', '.join(done)} from archive/{slug}/{ver} ({date.today()})\n")
    print(f"restored {', '.join(done)} from archive/{slug}/{ver} (the version before it is archived as before-restore)")
    if style and (v / "redesign.py").exists():
        print(f"NOTE: make_icon.py rebuilds {style} from work/{slug}/redesign.py and would overwrite it. Take the\n"
              f"{style} function from archive/{slug}/{ver}/redesign.py into work/{slug}/redesign.py, then build.")
    elif style:
        print(f"NOTE: this version has no redesign.py (a pack snapshot): the SVG is back in work/{slug}/; "
              f"to ship it, copy it to the pack with tools/pack_refresh.py only if redesign.py draws the same.")


def compare(slugs, old="pack", out="old-new.png"):
    import cairosvg
    from PIL import Image, ImageDraw
    cell, lw = 140, 200
    im = Image.new("RGB", (lw + 4 * cell + 10, 40 + len(slugs) * 2 * cell), (246, 245, 244))
    d = ImageDraw.Draw(im)
    for j, st in enumerate(STYLES):
        d.text((lw + j * cell + 40, 14), st.capitalize(), fill=(36, 31, 49))

    def icon(path):
        if path.suffix == ".png":
            return Image.open(path).convert("RGBA").resize((128, 128))
        return Image.open(io.BytesIO(cairosvg.svg2png(url=str(path), output_width=128, output_height=128))).convert("RGBA")
    for i, slug in enumerate(slugs):
        vs = versions(slug)
        if old == "pack":
            cand = [v for v in vs if "_pack" in v.name]
        elif old == "latest":
            cand = vs
        else:
            cand = [ARCH / slug / old]
        ov = cand[-1] if cand else None
        for k, (title, folder) in enumerate(((f"{slug}\nOLD {ov.name if ov else '-'}", ov),
                                             (f"{slug}\nNOW (work/)", ROOT / "work" / slug))):
            y = 40 + (2 * i + k) * cell
            d.text((10, y + 50), title, fill=(36, 31, 49) if k else (120, 120, 120))
            if folder is None:
                continue
            for j, st in enumerate(STYLES):
                p = folder / f"{slug}-{st}.svg"
                if not p.exists() and (folder / f"{st}.png").exists():
                    p = folder / f"{st}.png"
                if p.exists():
                    ic = icon(p)
                    im.paste(ic, (lw + j * cell + 6, y + 6), ic)
    out = Path(out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print("wrote", out)


def index():
    lines = ["# Archive index", "",
             "Every archived version of every app (tools/archive.py). Open a folder to see its SVGs;",
             "to bring one back: `python3 tools/archive.py restore <slug> <version> [--style disc]`.", "",
             "| App | Versions (oldest first) |", "|---|---|"]
    for d in sorted(p for p in ARCH.iterdir() if p.is_dir()):
        vs = [v.name for v in versions(d.name)]
        lines.append(f"| {d.name} | " + " · ".join(f"[{v}]({d.name}/{v}/)" for v in vs) + " |")
    (ARCH / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote archive/INDEX.md")


def all_slugs():
    styles_json = json.loads((ROOT / "pack/styles.json").read_text())
    from_pack = {s for s in styles_json["icons"]} | {p.parent.name for p in (ROOT / "work").glob("*/design.md")}
    return sorted(s for s in from_pack if not s.startswith(("_", "zz_", "test_")))


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd, rest = a[0], a[1:]
    opts = {rest[i][2:]: rest[i + 1] for i in range(len(rest) - 1) if rest[i].startswith("--") and not rest[i + 1].startswith("--")}
    flags = {x for x in rest if x.startswith("--")}
    slugs = [x for i, x in enumerate(rest) if not x.startswith("--") and (i == 0 or not rest[i - 1].startswith("--")
                                                                            or rest[i - 1] in ("--all", "--quiet"))]
    if "--all" in flags:
        slugs = all_slugs()
    if cmd == "snap":
        for s in slugs:
            snap(s, opts.get("label", "work"), quiet="--quiet" in flags)
    elif cmd == "pack":
        for s in slugs:
            pack(s, opts.get("label", "pack"), quiet="--quiet" in flags)
    elif cmd == "history":
        for s in slugs:
            history(s, opts.get("ref", "HEAD"))
    elif cmd == "list":
        for s in slugs:
            for v in versions(s):
                first = (v / "info.txt").read_text(encoding="utf-8").splitlines()[0] if (v / "info.txt").exists() else ""
                print(f"{s}  {v.name:32s} {first}")
    elif cmd == "restore":
        if len(slugs) != 2:
            sys.exit("restore <slug> <version> [--style disc]")
        restore(slugs[0], slugs[1], opts.get("style"))
    elif cmd == "compare":
        compare(slugs, opts.get("old", "pack"), opts.get("out", "old-new.png"))
    elif cmd == "index":
        index()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
