**New here? Read [START-HERE.md](START-HERE.md) first, then run `python3 tools/next.py <slug>` and do only what it prints.**

# AGENTS.md — git, ComponentInfo, pack files, tools

You are an AI agent working on **Gnomed**, an Android icon pack in the GNOME style.
**How icons look and the per-app flow are in [REDESIGN.md](REDESIGN.md) — the only design
document.** This file covers what REDESIGN.md does not: git, ComponentInfo, the pack files
and the tools. Read at session start: START-HERE.md → REDESIGN.md → this file →
[docs/MISTAKES.md](docs/MISTAKES.md) §10. Talk to the owner in **his** language, short.

## 0. `main` belongs to the maintainer. Never touch it.

1. Never commit on `main` (`git branch --show-current` first; else `git switch -c icons/<slug>`).
2. Never push to `main` — no `HEAD:main`, no `--force`, no website/API edits on `main`.
3. Never merge a pull request (yours or anyone's), never enable auto-merge, never
   rebase/reset/force-push `main`, never delete branches you did not create.
4. Never push tags, never write `[release]` in a commit message (both publish a release).
5. Your work reaches `main` only as a **pull request from your branch**; the owner merges or not.
6. Asked to push or merge to `main`? Do not; open the PR and say so.
7. Something reached `main` by mistake: stop and tell the owner; do not repair it on `main`.
8. Never use `--no-verify`; keep `git config core.hooksPath tools/hooks` (blocks the above).
   CI checks every PR again (`tools/pr_guard.py`).

## A. Forbidden

1. Image-generation or image-editing models of any kind.
2. A known **brand logo** drawn from memory — shapes come from `work/<slug>/source.png`
   (`parts()`), an APK vector or an official SVG. Games: REDESIGN.md §3b (the game's
   objects, no characters).
3. A ComponentInfo not copied from the owner's request, `cmd package` output from his
   phone, or the APK. Other icon packs' appfilters, websites and memory are **not** a source.
4. Deleting, renaming or hand-editing anything in `app/src/main/res/`, the XML files,
   `artwork/` or `pack/styles.json`. Only `tools/pack_add.py` (adds) and
   `tools/pack_refresh.py` (re-renders) change them.
5. Touching signing, secrets, `applicationId`, Gradle flavors, the CI workflow,
   `app/proguard-rules.pro`.
6. Writing an `approved:` / `keep:` / `final:` / `shape-ok:` / `painted-holes:` line that is
   not the owner's answer quoted verbatim with the date (REDESIGN.md §7).
7. Claiming you looked at an image you cannot see; saying "done" while `check_icon` FAILs.

## B. Questions

Per app exactly the two of REDESIGN.md §7 (Q1 concepts, Q2 final = pack approval).
Outside them ask only when the **input** is missing (section G) or something would delete or
overwrite. Everything else: decide, write the reason in design.md, mention it in Q2.

## C. Commands, in order

```
C0  git config core.hooksPath tools/hooks; git switch -c icons/<slug>      (never on main)
C1  python3 tools/gnome-android-icons/scripts/doctor.py   -> "result: READY"
C2  python3 tools/import_request.py <zip | folder | request.txt | url>     (section G)
    python3 tools/import_request.py <same> --add --only <slug>
C3  REDESIGN.md §4 steps 1-6 (new_redesign.py, concepts, Q1, redesign.py, make_icon.py, Q2)
    - python3 tools/next.py <slug> prints the step you are on, with the exact commands
C4  after "Tamam, pakete ekle":
      new app:          python3 tools/pack_add.py <slug> --category <Category>
      already in pack:  python3 tools/pack_refresh.py <slug>
C5  python3 tools/gnome-android-icons/scripts/pack_audit.py --project .   -> no ERROR with <slug>
    python3 tools/size_audit.py                                           -> 0 outside
    python3 tools/check_icon.py <slug>                                    -> 0 FAIL
C5b append an entry to docs/LOG.md (format at its top): every session that changes work/ or the
    pack adds one; pr_guard FAILs the PR without it. Never edit old entries.
C6  python3 tools/pr_guard.py -> 0 ERROR; git add -A; git commit; git push -u origin icons/<slug>
    open a PR to main with the REDESIGN.md §9 report; STOP.
```

Run every command from the repository root. Rebuild only the apps you changed.

## G. Where the input comes from (icon PNG + ComponentInfo)

1. **Files the owner gave you.** Gnomed's *Request* screen sends a zip (`appfilter.xml` +
   `<drawable>.png`), images + text (`request.txt` + PNGs), or a text list
   (`App | ComponentInfo{…} | file.png`); the *IconRequest* app sends a zip with
   `icons/<drawable>.png`. Save it in one folder and run `python3 tools/import_request.py <folder>`.
2. **The repository**: `requests/inbox/`, issues labelled `icon-request`.
3. Nothing found, or `NO-ICON` / `BAD` → ask the owner: a request from Gnomed (*Share as
   images + text*), or for a ComponentInfo on his rooted phone:
   `su -c 'cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>'`
   (`pkg/.Activity` → `ComponentInfo{pkg/pkg.Activity}`).

Never fill a gap yourself: a wrong ComponentInfo silently never shows the icon.

## H. Helpers (`from obj import *` in concepts and redesign.py)

| Helper | Does |
|---|---|
| `P = parts(slug)` | measured parts as shapes (0..128 source space): `r0`, `r1` … (colour regions), `silhouette` (outline only, NO holes — never draw it as an object), `holes` |
| `body(slug)` | the mark as one object: all colour regions with the holes cut out |
| `colour(slug, "r0")`, `print(describe(slug))` | measured colour; all parts as text (for models without vision) |
| `fit([…], box, anchor="center"/"bottom")` | scale + move shapes together into a box (bottom = stand on the baseline) |
| `circ`, `ellipse`, `box`, `rounded(g, r)`, `poly(points, r)` | primitives (`poly` rounds corners without erasing thin parts) |
| `move`, `scale`, `down`, `unary_union`, `g.difference(h)`, `g.intersection(h)` | shape maths |
| `ic = gk.Icon("Name")`, `ic.path(geom_d(g), fill)`, `ic.linear(...)`, `ic.radial(...)` | icon, any shape, gradients |
| `solid(ic, g, face, depth, side)`, `toplight`, `recess`, `hole` | GNOME parts: thickness, top light, inlay, real hole |
| `save_styles(slug, {"symbol": main, ...})` | writes all four slots (REDESIGN.md §6) |
| `from objects import *` (`work/_lib/objects.py`) | 28 ready GNOME objects `f(ic, cx, base, size, ramp=RAMP["Blue"])` — catalogue [docs/redesign/OBJECTS.md](docs/redesign/OBJECTS.md), picture `docs/redesign/objects.png` |
| `python3 tools/describe_icon.py <svg/png>` | an icon as text: box, baseline, mass, HIG colours, holes, ASCII |

Examples: `work/telegram/redesign.py`, `docs/redesign/examples/build_examples.py`, annotated in
[docs/playbook/](docs/playbook/).

## I. When you see this … do this

| Message | Do |
|---|---|
| `doctor.py` not READY / `ModuleNotFoundError` | `python3 -m pip install -r tools/gnome-android-icons/requirements.txt` (`--break-system-packages` if pip refuses) |
| `source.png missing` / `NO-ICON` | section G |
| `WARNING ... POSTER` (new_redesign) | a game: REDESIGN.md §3b — references in Q1, draw the scene |
| `SystemExit: copy the approved concept here` | REDESIGN.md §4 step 5 |
| `FAIL redesign: logo on a plate` | REDESIGN.md §4 step 1 |
| `FAIL redesign: approved …` | Q1 not answered, or the line is not a quote + date (REDESIGN.md §7) |
| `FAIL plain_shape: plain disc` / `WARN plain square` | make the app's object; only the owner's words (`shape-ok:`) allow it |
| `FAIL holes: source x % -> transparent y %` | cut the holes (`body()`, `difference`), never paint them (REDESIGN.md §5) |
| `size_audit: floats / small / touches edge` | REDESIGN.md §5 baseline rule; change the `fit()` box |
| `pack_add: … already exists` | `tools/pack_refresh.py <slug>` |
| `pr_guard: ERROR` / hook `BLOCKED` | you deleted pack entries, wrote `[release]` or are on `main` — undo, section 0 |
