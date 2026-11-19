# AGENTS.md — operating procedure for AI agents

You are an AI agent working on **Gnomed**, an Android icon pack in the GNOME style.
Follow this file **exactly**. It is written for every model, small or large. When this
file and your own idea disagree, this file wins.

> **Icon design: [REDESIGN.md](REDESIGN.md) is binding and comes first.** The automatic
> pipeline (`tools/make_icon.py` for an app without `work/<slug>/redesign.py`) only makes
> a draft — the logo on a plate — and the gate FAILs it (`redesign` check). Steps C3–C6
> below are the measuring/draft stage; the icon itself is designed with REDESIGN.md.

Learn the job first: [REDESIGN.md](REDESIGN.md) and
`docs/redesign/examples/build_examples.py`. [`docs/course/`](docs/course/README.md)
explains the draft pipeline and its tools (recipes for measuring problems). Background
and rules for humans: [`CONTRIBUTING.md`](CONTRIBUTING.md).

Talk to the human in **their** language. Keep messages short.

**Before you start: read [docs/MISTAKES.md](docs/MISTAKES.md)** — every mistake this
project already made, why, and the rule that prevents it. Add new ones there.

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
* the source is a poster, a photo or a character (free adaptation needs their OK),
* after the concept board (REDESIGN.md step 4) and after the final review (step 6),
* before `tools/pack_add.py` without `--dry-run` (show the dry-run diff first),
* anything would delete or overwrite.

Ask with 2–4 short options.

## C. Procedure (do the steps in order, for each app)

```
C0  git config core.hooksPath tools/hooks                      (once per clone; section 0)
    git switch -c icons/<slug>                                 (never work on main)
C1  python3 tools/gnome-android-icons/scripts/doctor.py        -> must end "result: READY"
C2  python3 tools/import_request.py <request zip | folder | request.txt>     (section G)
        -> lists the apps (NEW / NO-ICON / IN-PACK); then add --add --only <slug>
    or, for one app by hand:
    python3 tools/add_source.py <slug> <icon.png> "<Label>" '<ComponentInfo{...}>'
        slug: lowercase a-z0-9_, starts with a letter. Single quotes around the component.
C3  python3 tools/make_icon.py <slug>
C4  read the last block "summary: N PASS, N WARN, N FAIL"
        FAIL > 0  -> C5
        FAIL = 0  -> C6
C5  for each FAIL/WARN line, read "-> FIX: R<n>", open docs/course/04-recipes.md, apply
    recipe R<n> exactly (usually one line in OVERRIDES of work/_lib/build_auto.py,
    with a "note"), then go back to C3 (use --remeasure after editing auto.py tables)
C6  if you can see images: open work/<slug>/styles.png and answer the 5 questions in D;
    fix what is wrong (lesson 4), back to C3.
    if you cannot see images: write that in your report (E).
C7  python3 tools/pack_add.py <slug> --category <Category> --dry-run
        -> show the diff to the human, wait for "yes"
C8  python3 tools/pack_add.py <slug> --category <Category>
C9  python3 tools/gnome-android-icons/scripts/pack_audit.py --project .
        -> no ERROR mentioning <slug>
    python3 tools/size_audit.py
        -> "0 icon(s) outside the ranges" (same baseline and size as the rest of the pack)
C10 git branch --show-current          -> must NOT be main
    python3 tools/pr_guard.py           -> 0 ERROR (nothing deleted, no [release])
    git add -A; git commit -m "Add <App> (styles)"; git push -u origin icons/<slug>
C11 open a pull request from icons/<slug> to main (template), post the report (E), STOP.
    The human merges or not. Never merge it yourself.
```

Work on one app at a time until C9, or on a batch of up to 10 apps where every app
reaches 0 FAIL before C7.

## D. Five questions for `styles.png` (if you can see images)

Each row: source | Faithful | Disc | Rimmed | Symbol, on light and dark.

1. Is it the same shape as the source (count the parts, holes, points)?
2. Is there anything that is NOT in the source (a box, a blob, a glow, stripes)?
3. Is anything from the source missing (a dot, a hole, a second colour)?
4. Does any style disappear on the light or the dark half?
5. Does anything look cut, crushed, too small or too big?

A "yes" to 2–5 or a "no" to 1 → find the recipe in lesson 4.

## E. Report (copy, fill, post to the human and into the PR)

```
App: <name> (<slug>)   Component: <ComponentInfo>  from: <Gnomed request / IconRequest app / cmd package on the phone / APK>
Styles built: Faithful, Disc, Rimmed, Symbol   (skipped: <style> because <reason>)
Gate: <N> PASS, <N> WARN, 0 FAIL
WARN lines: <copy them>
Fixes applied: <recipe numbers + the OVERRIDES line>
Looked at styles.png: yes / NO - I cannot see images, please review work/<slug>/styles.png
Not verified: on-device launcher look
Model/tool: <your name>
```

## E2. Improving existing icons

`docs/STATUS.md` lists every app's gate warnings (worst first). For an app already in
the pack: fix it (lesson 4), `python3 tools/make_icon.py <slug>` until 0 FAIL and fewer
WARN, then `python3 tools/pack_refresh.py <slug>` (never pack_add), then
`python3 tools/pack_status.py`, commit, PR.

## F. Facts you must not get wrong

* Canvas 128×128 units. Plate 104×104 at (12,12) r8, chin 4. Disc Ø118 at (64,63), chin 2.
* Pure black → `#241f31`. White mark's side → `#deddda`.
* Every app needs Faithful. A style that cannot be made well is skipped (`"skip": [...]`).
* Hex colours for OVERRIDES come from `work/<slug>/geometry.json` → `info.regions[].fill`.
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
