# Archive - every version of every icon

The owner (2026-11-23): *"çalışma alanındaki eski simgeleri ve diğer şeyleri arşive eklesin. Böylece
hiçbir şey kaybetmemiş oluruz ... bir şeyi beğenmedim. O şeyi geri döndürebilirim."*

- One folder per app, one sub-folder per version: `archive/<slug>/<date>_<time>_<label>/`, oldest first.
  Labels: a git commit (`3376fc7`), `pack` (the icons as they shipped), `before-<review>` (taken by
  next.py before the owner's fixes), `before-redo`, `pack-before-refresh`, `before-restore`.
- Each holds the four styles (`<slug>-symbol.svg` ...), and where they existed `redesign.py`,
  `design.md`, `concepts/`, the review lists (`fixes*.md`); pack versions also the shipped PNGs;
  `info.txt` says where it came from. GitHub shows the SVGs when you open them.
- On GitHub, open `archive/<slug>/`: the versions are listed oldest first. Locally `python3 tools/archive.py index`
  writes a table of everything to archive/INDEX.md (not committed).

Bring a version back (tools/archive.py; the current one is archived first, nothing is lost):

    python3 tools/archive.py list <slug>
    python3 tools/archive.py restore <slug> <version>                 # all four styles + redesign.py
    python3 tools/archive.py restore <slug> <version> --style disc    # one style
    python3 tools/archive.py compare <slug> ... --old pack --out old-new.png

Nothing in archive/ is ever deleted or edited by hand; it is not part of the APK.
