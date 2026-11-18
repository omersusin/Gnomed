# AGENTS.md — operating procedure for AI agents

You are an AI agent working on **Gnomed**, an Android icon pack in the GNOME style.
Follow this file **exactly**. It is written for every model, small or large. When this
file and your own idea disagree, this file wins.

Learn the job first: read [`docs/course/`](docs/course/README.md) lessons 1–5
(lesson 4 and 6 when you need a fix). Background and rules for humans:
[`CONTRIBUTING.md`](CONTRIBUTING.md).

Talk to the human in **their** language. Keep messages short.

---

## A. Forbidden — never do these

1. Never use an image-generation or image-editing model (DALL·E, Midjourney, Stable
   Diffusion, Flux, Gemini image, "AI upscale", …) for anything.
2. Never draw a known logo from memory. All shapes come from `work/<slug>/source.png`
   (or an APK vector / official SVG).
3. Never write a ComponentInfo that you did not copy from the user's icon-request export,
   adb output or APK.
4. Never delete, rename or overwrite anything in `app/src/main/res/`, the XML files,
   `artwork/` or `pack/styles.json` by hand. Only `tools/pack_add.py` (adds) and
   `tools/pack_refresh.py` (re-renders existing) may change them.
5. Never touch signing, secrets, `applicationId`, Gradle flavors, the CI workflow,
   `app/proguard-rules.pro`.
6. Never push to `main`, never write `[release]` in a commit message, never push tags.
7. Never claim you looked at an image if you cannot see images.
8. Never say "done" while `tools/check_icon.py` shows a FAIL.

## B. Stop and ask the human when

* you do not have the app's icon PNG **and** its ComponentInfo,
* the gate still shows FAIL after you tried the recipe 3 times,
* the source is a poster, a photo or a character (free adaptation needs their OK),
* before `tools/pack_add.py` without `--dry-run` (show the dry-run diff first),
* anything would delete or overwrite.

Ask with 2–4 short options.

## C. Procedure (do the steps in order, for each app)

```
C1  python3 tools/gnome-android-icons/scripts/doctor.py        -> must end "result: READY"
C2  python3 tools/add_source.py <slug> <icon.png> "<Label>" '<ComponentInfo{...}>'
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
C10 git checkout -b icons/<slug>; git add -A; git commit -m "Add <App> (styles)"; git push -u origin icons/<slug>
C11 open a pull request (template) and post the report (E)
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
App: <name> (<slug>)   Component: <ComponentInfo>  from: <icon request / adb / APK>
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
