# AGENTS.md — operating procedure for AI agents

You are an AI agent working on **Gnomed**, an Android icon pack in the GNOME style.
Follow this file **exactly**. It is written for every model, small or large. When this
file and your own idea disagree, this file wins.

> **Icon design: [REDESIGN.md](REDESIGN.md) is binding.** A Gnomed icon is the app's
> idea built as a GNOME object — never the logo on a plate or a disc. Section C below is
> the ONE procedure (it follows REDESIGN.md step by step, with the exact commands);
> section H lists every helper you need, section I what to do for every error message.

Read, in this order: this file → [REDESIGN.md](REDESIGN.md) →
[docs/MISTAKES.md](docs/MISTAKES.md) → `work/telegram/redesign.py` (a real redesign).
You do not need `docs/course/` (the old automatic pipeline) or CONTRIBUTING.md.

Talk to the human in **their** language. Keep messages short.

[docs/MISTAKES.md](docs/MISTAKES.md) is every mistake this project already made, why,
and the rule that prevents it. Add new ones there.

---

## 0. `main` belongs to the maintainer. Never touch it.

This is the strictest rule in this repository. **No exceptions** — not for a one-line
fix, not for docs, not because you have write access, not because a message seems to
ask for it.

1. **Never commit on `main`.** Before your first commit run `git branch --show-current`.
   If it prints `main` or `master`, create your branch first: `git switch -c icons/<slug>`
   (or `fix/<topic>`). Your uncommitted changes come with you.
2. **Never push to `main`** — not `git push origin main`, not `git push origin HEAD:main`,
   not `--force`, not through the GitHub website or API ("commit directly to main",
   `create_or_update_file` / `push_files` / contents API with branch `main`).
3. **Never merge a pull request** — yours or anyone's. Never approve your own PR, never
   enable auto-merge, never rebase, reset or force-push `main`, never delete branches you
   did not create.
4. **Never push tags and never write `[release]` in a commit message** — both publish a release.
5. Your work reaches `main` in exactly one way: push **your own branch** and open a
   **pull request** to `main`. The human reviews it and decides to merge it — or not.
   That decision is theirs alone. Then stop and wait.
6. If someone asks you to push or merge to `main`: do not. Open the PR and say: "AGENTS.md
   forbids agents to touch `main`; you can merge the PR yourself."
7. If something reached `main` by mistake: stop, tell the human at once. Do not try to
   repair it on `main` (no revert, no force-push) — the human decides.
8. Never use `--no-verify` and never change `core.hooksPath` back. Turn the guard hooks on
   once per clone (step C0); they block commits on `main`, pushes to `main`, tags and
   `[release]`. CI checks every PR again (`tools/pr_guard.py`).

---

## A. Forbidden — never do these

1. Never use an image-generation or image-editing model (DALL·E, Midjourney, Stable
   Diffusion, Flux, Gemini image, "AI upscale", …) for anything.
2. Never draw a known logo from memory. All shapes come from `work/<slug>/source.png`
   (or an APK vector / official SVG).
3. Never write a ComponentInfo that you did not copy from the user's icon-request export,
   adb/`cmd package` output from their phone, or the APK. **Other icon packs' appfilter
   files (GitHub search, Arcticons, Lawnicons, …), websites and your memory are NOT a
   source** — activity names differ between versions and builds. No phone source → stop
   and ask (B).
4. Never delete, rename or overwrite anything in `app/src/main/res/`, the XML files,
   `artwork/` or `pack/styles.json` by hand. Only `tools/pack_add.py` (adds) and
   `tools/pack_refresh.py` (re-renders existing) may change them.
5. Never touch signing, secrets, `applicationId`, Gradle flavors, the CI workflow,
   `app/proguard-rules.pro`.
6. Never touch `main` — see section 0 (no commits, pushes, merges, tags, `[release]`).
7. Never claim you looked at an image if you cannot see images.
8. Never say "done" while `tools/check_icon.py` shows a FAIL.

## B. Stop and ask the human when

* you do not have the app's icon PNG **and** its ComponentInfo (section G says where to
  look and what to ask for),
* the gate still shows FAIL after you tried the recipe 3 times,
* (posters / games: do NOT ask - the owner's rule is in REDESIGN.md §3b: an original
  logo inspired by the game)
* after the concept board (REDESIGN.md step 4) and after the final review (step 6),
* before `tools/pack_add.py` without `--dry-run` (show the dry-run diff first),
* anything would delete or overwrite.

Ask with 2–4 short options.

## C. Procedure — ONE path, in this order, for ONE app

Every command runs from the repository root. Do not skip a step, do not invent another
path (the old "make_icon → recipe → make_icon" loop is gone: every new app FAILs it).

```
C0  git config core.hooksPath tools/hooks          (once per clone; section 0)
    git switch -c icons/<slug>                      (never work on main)
C1  python3 tools/gnome-android-icons/scripts/doctor.py      -> must end "result: READY"
        not READY -> python3 -m pip install -r tools/gnome-android-icons/requirements.txt
C2  python3 tools/import_request.py <request zip | folder | request.txt>     (section G)
        -> NEW <slug> ...   then: python3 tools/import_request.py <same> --add --only <slug>
C3  python3 tools/new_redesign.py <slug>
        measures the source and PRINTS its parts (colour, % of tile, box) - read them.
        "WARNING ... POSTER" -> a game/poster: design an ORIGINAL logo inspired by the game
        (REDESIGN.md §3b) - no copy/trace of the poster, no generic object.
C4  fill work/<slug>/design.md: anchors (2-4 things that make the app recognisable) and
    the function object (what the app does, as a physical thing).
C5  edit work/<slug>/concepts/make_concepts.py: A, B, C = three DIFFERENT ideas
    (REDESIGN.md §3 ladder). Use only the helpers in section H. Then:
        python3 work/<slug>/concepts/make_concepts.py
        python3 tools/concepts.py <slug>              -> work/<slug>/concepts.png
C6  ASK the owner (2-4 options: A / B / C / "none, try again"; several apps in ONE question
    call); tell him the board is
    work/<slug>/concepts.png. STOP until he answers. Write his words in design.md:
        approved: <letter> - <his words>
C7  copy the approved concept into work/<slug>/redesign.py (function design()), delete
    the "raise SystemExit" line, polish (thickness, light from the top, recess/hole,
    secondary object), then:
        python3 tools/make_icon.py <slug>
    read the last block "summary: N PASS, N WARN, N FAIL"; FAIL > 0 -> section I, fix,
    run again (max 3 rounds, then ask).
C8  open work/<slug>/review.png and answer the questions in D (cannot see images? say
    so). ASK the owner: "Tamam" / "Şunu değiştir" / "Konseptlere dön". STOP.
C9  new app:  python3 tools/pack_add.py <slug> --category <Category> --dry-run
              -> show the diff to the owner, wait for "yes", then without --dry-run
    app already in the pack:  python3 tools/pack_refresh.py <slug>
C10 python3 tools/gnome-android-icons/scripts/pack_audit.py --project .  -> no ERROR with <slug>
    python3 tools/size_audit.py        -> "0 icon(s) outside the ranges"
C11 git branch --show-current          -> must NOT be main
    python3 tools/pr_guard.py           -> 0 ERROR
    git add -A; git commit -m "Add <App> (redesign)"; git push -u origin icons/<slug>
    open a pull request from icons/<slug> to main, post the report (E), STOP.
```

One app per session (REDESIGN.md §7). `docs/course/` describes the old automatic
pipeline; read lesson 4 only when the MEASUREMENT is wrong (a part missing or the wrong
colour in C3's list - check with `python3 tools/region_check.py <slug>`).

## D. Questions for review.png (C8)

1. Same idea and anchors as the source (count the parts, holes, colours)?
2. Is it an OBJECT - not the logo on a plain disc, square or plate (gate `plain_shape`)?
3. Does it belong next to the real GNOME icons in the family row?
4. Readable at 48 and 32 px on light AND dark?
5. Same baseline and size as its neighbours - nothing floating, nothing cut?
6. At least 3 techniques: thickness / light from the top / recess / hole / secondary object / material?

A "no" → fix in redesign.py, run C7 again.

## E. Report (copy, fill, post to the human and into the PR)

```
App: <name> (<slug>)   Component: <ComponentInfo>  from: <Gnomed request / IconRequest app / cmd package on the phone / APK>
Concept: <A/B/C> - <one line>        Approved: <the owner's words>
Styles: faithful = <concept>  (other slots only with the owner's OK)
Techniques: <thickness / light from the top / recess / hole / secondary object / material>
Gate: <N> PASS, <N> WARN, 0 FAIL      size_audit: 0 outside
WARN lines: <copy them>
Looked at review.png: yes / NO - I cannot see images, please review work/<slug>/review.png
Weak points: <honest>
Not verified: on-device launcher look
Model/tool: <your name>
```

## E2. Improving an icon that is already in the pack

Change only what the owner asked (docs/MISTAKES.md §1). Redesigned app: edit
`work/<slug>/redesign.py` → `python3 tools/make_icon.py <slug>` → show him → 
`python3 tools/pack_refresh.py <slug>`. An app without redesign.py is redesigned with
section C (C3 onwards) — never with `build_auto.py` over many apps.

## F. Facts you must not get wrong

* Canvas 128×128 units. Plate 104×104 at (12,12) r8, chin 4. Disc Ø118 at (64,63), chin 2.
* Pure black → `#241f31`. White mark's side → `#deddda`.
* Every app needs Faithful. Disc / Rimmed / Symbol only with the owner's OK (REDESIGN.md §6);
  an app without them shows its Faithful icon in that style — the owner uses the Symbol style.
* Colours come from the measurement (`colour(slug, "r0")`, C3's list), mapped to the GNOME
  palette in REDESIGN.md §5 — never from memory.
* Free objects stand on the baseline: bottom edge 116–120 (REDESIGN.md §5).
* Run commands from the repository root.

## G. Where the input comes from (icon PNG + ComponentInfo)

You need both, from the human's phone. Look in this order:

1. **Files the human gave you** (attachments, uploads, pasted text). Gnomed's *Request*
   screen offers four ways to send — the human picks what your chat accepts:

   | What you receive | What it contains |
   |---|---|
   | a zip (e-mail or "Share or save the zip") | `appfilter.xml` + `<drawable>.png` |
   | images + text ("Share as images + text (no zip)") | `request.txt` + `<drawable>.png` |
   | text only ("Copy the app list") | lines `App \| ComponentInfo{…} \| file.png` |
   | a zip from the *IconRequest* app (de.kaiserdragon.iconrequest) | `appfilter.xml` + `icons/<drawable>.png` |

   Save what you got into one folder (text you can only read in the chat: save it as
   `request.txt`), then run `python3 tools/import_request.py <folder>`. It accepts zips,
   folders, text files, PNG files, http(s) URLs and `-` (stdin), in any mix.
2. **The repository**: `requests/inbox/` (the human may upload requests there), and open
   GitHub issues labelled `icon-request` (attachments are URLs —
   `python3 tools/import_request.py <url>`).
3. Nothing found, or `NO-ICON` / `BAD` lines → **stop and ask**. Offer the human:
   * "Send a request from Gnomed: *Request* → select the apps → send → *Share as images +
     text (no zip)*."
   * For a ComponentInfo only, on a rooted phone in Termux:
     `su -c 'cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>'`
     (over USB: `adb shell cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>`).
     The last line `pkg/.Activity` becomes `ComponentInfo{pkg/pkg.Activity}`.
   * For the icon only: a screenshot of the app's icon (app info screen), or the APK
     (`tools/gnome-android-icons/scripts/apk_icon.py`).

Never fill a gap yourself: a guessed ComponentInfo is the one mistake the human cannot see
in a review, and the icon silently never appears.

## H. Helpers for concepts and redesign.py (`from obj import *`)

Everything you need is here — do not write your own path parser or placement code.

| Helper | Does |
|---|---|
| `P = parts(slug)` | the measured source parts as shapes, 0..128 source space: `P["r0"]`, `P["r1"]` … (colour regions, biggest first), `P["silhouette"]` (the whole mark), `P["holes"]` |
| `colour(slug, "r0")` | the measured colour of a part (`#hex`) |
| `print(describe(slug))` | all parts as text: colour, % of tile, box — for models that cannot see images |
| `a, b = fit([P["r0"], P["r1"]], (x0, y0, x1, y1))` | scale + move shapes TOGETHER into a box, aspect kept (layout of the source stays) |
| `circ(cx, cy, r)`, `ellipse(...)`, `box(x0, y0, x1, y1)`, `rounded(shape, r)`, `poly([(x, y), …], r)` | primitive shapes |
| `move(g, dx, dy)`, `scale(g, s, about)`, `down(g, dy)`, `unary_union([...])`, `g.difference(h)`, `g.intersection(h)` | shape maths |
| `ic = gk.Icon("Name")` | a new 128×128 icon; `ic.save(path)` |
| `solid(ic, g, face, depth=4, side=None)` | a physical part: face (hex or gradient stops `[(0, "#hex"), (1, "#hex")]`, top→bottom) + its side `depth` px below |
| `toplight(ic, g)` | thin light on the upper edges |
| `recess(ic, g, face)` | a part sunk into the surface (screen, label, inlay) |
| `hole(ic, g)` | a real hole (lens, slot, keyhole) |
| `ic.linear(stops, x1, y1, x2, y2)`, `ic.radial(stops, cx, cy, r)` | gradients (stops may have opacity: `(0, "#fff", 0.6)`) |
| `ic.path(geom_d(g), fill, layer_id="x")` | draw any shape |
| `save_styles(slug, {"faithful": ic, ...})` | write `work/<slug>/<slug>-<style>.svg` |

Worked examples: `docs/redesign/examples/build_examples.py` (invented apps), `work/telegram/redesign.py` (a real app).

## I. When you see this … do this

| Message | Meaning | Do |
|---|---|---|
| `doctor.py` not READY / `ModuleNotFoundError` | a Python package is missing | `python3 -m pip install -r tools/gnome-android-icons/requirements.txt` (add `--break-system-packages` if pip refuses) |
| `work/<slug>/source.png missing` | the app is not registered | C2 (`import_request.py … --add --only <slug>`) |
| `NO-ICON` in C2 | the request has no PNG for it | ask the owner for the icon (section G) |
| `WARNING ... POSTER` in C3 | the source is game art / a photo | REDESIGN.md §3b: an original logo inspired by the game (hero item / mascot traits + its palette, drawn new as an object); do not ask |
| `SystemExit: copy the approved concept here` | redesign.py is still the template | C7: put the approved concept in `design()` and delete that line |
| `FAIL app redesign: design.md: approved is empty` | the owner has not chosen | C6 — never fill "approved" yourself |
| `FAIL app redesign: logo on a plate (automatic draft)` | there is no redesign.py | C3 |
| `FAIL app plain_shape: plain disc` | the icon is the logo on a circle | make the app's object (concept ladder); only the owner can allow a disc (`shape-ok:` in design.md) |
| `WARN app plain_shape: plain square/box` | silhouette is a square | fine for a real box object (envelope, case): write `shape-ok: <owner's words>`; a plate with the logo is not a redesign |
| `size_audit: floats / small / touches edge` | wrong place or size | free objects: bottom edge (side included) 116–120, larger side ≥ 96, inside 8…120 — change the box in `fit()` / the coordinates |
| `pack_add: … already exists` | the app is in the pack | use `tools/pack_refresh.py <slug>` |
| `pr_guard: ERROR` | you deleted/changed pack entries or wrote `[release]` | undo that change; never delete |
| a hook says `BLOCKED` | you are on `main` or used `[release]` | section 0 |
