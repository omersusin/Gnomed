# Instructions for AI agents (Claude Code, Codex, OpenCode, …)

You are working on **Gnomed**, an Android icon pack that redraws app icons as
GNOME/Adwaita app icons. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) completely before
you change anything — it is the handbook; this file adds the rules that apply to you
as an agent. The knowledge base for icon design is in
`tools/gnome-android-icons/` (`SKILL.md` + `references/`): read it instead of
researching the web.

Speak to the human in their language. Ask them (multiple choice, short) when a
decision is theirs: which apps, whether to add to the pack, anything irreversible.

---

## Non-negotiable rules

1. **Never use an image-generation or image-editing model** (DALL·E, ImageGen,
   Midjourney, Stable Diffusion, Flux, Gemini image, "AI upscale", …) for anything in
   this repository — not icons, not drafts, not wallpapers, not previews. Everything is
   SVG written by code from measured source geometry, rendered with CairoSVG.
2. **Never draw a known logo from memory.** Measure or trace the source
   (`work/<slug>/source.png`, an APK vector, an official SVG). If you adapt freely
   (posters, §5.4 of CONTRIBUTING), say so and still measure colours and shapes.
3. **Never invent a ComponentInfo.** Use the icon-request export, adb or the APK. If you
   cannot get it, the icon stays gallery-only and you say so.
4. **Never delete or overwrite pack entries.** Use `tools/pack_add.py` (refuses to
   overwrite) and `tools/pack_refresh.py` (re-renders existing ones). Always `--dry-run`
   first and show the human the diff. Do not touch the CandyBar sample placeholders.
5. **Never touch signing**: no keystores in the repo, no changes to secrets, the signing
   config, `applicationId` or the flavor names.
6. **Never push to `main`, never add `[release]`** to a commit message, never push tags —
   unless the human maintainer explicitly asks you to.
7. **Look at your output.** Open the boards (`styles.png`, `review.png`, legibility) as
   images and judge them. Passing `lint_svg.py` or tests is *not* proof of a good icon.
8. **Report honestly**: what you did, where the geometry came from, known weaknesses,
   what you did not verify. Never call an icon "fixed" or "GNOME" because a check passed.

---

## Your workflow for a batch of apps

```bash
python3 -m pip install -r tools/gnome-android-icons/requirements.txt
python3 tools/gnome-android-icons/scripts/doctor.py          # READY
# per app (icon + component from the human's icon-request zip):
python3 tools/add_source.py <slug> <icon.png> "<Label>" '<ComponentInfo{…}>'   # single quotes! ($ in names)
python3 work/_lib/auto.py <slug>
python3 work/_lib/build_auto.py <slug>
python3 work/_lib/design_grid.py work /tmp/<batch>.png <slug1>,<slug2>,…      # look at it
# fix with OVERRIDES / auto.py SMOOTH-THRESH-HALO / build_weak.py, rebuild, look again
tools/review.sh <slug>                                       # lint 0 FAIL, exports, boards
python3 tools/pack_add.py <slug> --category <Cat> --dry-run  # show the human, get approval
python3 tools/pack_add.py <slug> --category <Cat>
python3 tools/gnome-android-icons/scripts/pack_audit.py --project .   # no new ERROR
```

Work in batches of ~8–12 apps: build all, render one grid per batch, review every row,
fix, re-render, then ask the human once for the whole batch.

## How to review a grid (what "broken" looks like)

For each row (source | Faithful | Disc | Rimmed | Symbol, on light and dark):

* **Wrong ground**: a plate in the wrong colour, a grey gradient plate for a white tile,
  tile shapes/glows inside the mark → `light`, `keep_ground`, `flat`+`face`, `drop`, `only_white`.
* **Stripes** in what was a smooth gradient → `merge_grad`.
* **Blob / lumpy edges** → blurry source: `SMOOTH`, `THRESH`, `HALO`; keep the source's proportion (`scale`).
* **Mark vanishes** on light or dark → Symbol `margin`, or skip that Symbol.
* **Box on a plate**, poster traced into mush, cropped mascot → hand-build in `build_weak.py`.
* **Floating** symbol, wrong size → baseline/scale.
* **Layer peeking out** (a lighter band under a dark outline, a wrong-coloured inner wall)
  → the side/chin colour must match what it is the side of.

Be strict. In this project the human found real defects that the checks did not
(an inverted logo, orange inner layers, stripes). Look at 32 px too.

## Definition of done for an icon

* Built from measured geometry (IoU of traces ≥ 0.99 is reported by the tools).
* All four styles reviewed visually; weak styles dropped (fall back to Faithful) rather than shipped.
* `lint_svg.py`: 0 FAIL. `pack_audit.py`: no new ERROR.
* `work/<slug>/brief.md` (or the OVERRIDES `note`) states decisions and weaknesses.
* Human approved the dry-run before `pack_add.py` ran.

## Commits and PRs

* Small, descriptive commits; one batch or one fix per PR; fill in the PR template.
* Commit generated files together with their source (SVG + PNG + XML + styles.json).
* Do not commit `__pycache__`, logs, keystores, or files outside the change.
* Mention in the PR that an AI agent did the work and which model/tool.

## Where things are

* Style numbers and evidence: `tools/gnome-android-icons/references/gnome-style-guide.md`, `measured-style.md`
* Which treatment for which kind of icon: `references/archetypes.md`
* Review questions: `references/review-protocol.md`
* CandyBar specifics: `references/android-candybar.md`
* The project's own lessons: CONTRIBUTING.md §15 and `references/lessons-and-rejections.md`
