---
name: gnome-android-icons
description: Redesign any Android app icon (logo, screenshot, APK or SVG the user gives) as a real GNOME/Adwaita-style app icon - editable SVG built with code, transparent PNGs, 3-5 alternative designs, small-size, launcher and GNOME-reference reviews - and add it safely to a CandyBar (or compatible) icon-pack project, including whole-pack audits. Use for GNOME/Adwaita icon conversion, icon-pack work, appfilter/drawable.xml edits, and reviewing GNOME-style icons. Never uses image-generation tools.
license: MIT (skill code and docs). Bundled GNOME reference SVGs keep their own licences - see NOTICE.md
compatibility: Python 3.9+ with cairosvg, pillow, numpy, scipy, lxml, scikit-image, svgpathtools, shapely, potracer, svgelements (requirements.txt; check with scripts/doctor.py). Optional adb, androguard. Works offline. For Claude Code, Codex, OpenCode and other Agent Skills clients.
metadata:
  version: "1.1"
  replaces: "gnome-android-icons v1.0"
---

# GNOME Android Icons (v1.1)

Turn an app's icon into an icon that looks like the GNOME design team drew it,
while the user still recognises the app instantly; ship it as editable SVG +
transparent PNG; add it to the user's Android icon pack and keep the pack coherent.

## Non-negotiable rules

1. **No generative image tools** - no ImageGen/DALL-E/Stable Diffusion/image-edit
   models, not even "for a quick draft". Only SVG written by code or hand,
   real source vectors, and deterministic tools in `scripts/`.
2. **Final art is real vector**: paths/shapes/gradients. No `<image>`, base64,
   `<text>`, filters. `scripts/lint_svg.py` must report no FAIL.
3. **Identity geometry comes from a source, never from memory** (APK vector,
   official SVG, or a trace of the user's image). See `references/identity-preservation.md`.
4. **A logo + shadow/emboss/recolour is not a conversion. No invented containers**
   (TV, camera body, speaker, coin, frame, forced squircle/circle). Autodrafts are
   only the starting point (level 0-1).
5. **Mascots keep their anatomy** (pose, limbs, face, spikes) - define the parts once, reuse.
6. **Passing tests or good numbers is not success.** Look at the boards; report
   weaknesses; only the user approves. Say plainly what you could not do or verify.
7. **Never invent an Android ComponentInfo.** Get it from the phone/APK or leave the
   icon gallery-only and say so. Never delete or overwrite pack entries silently.
8. Talk to the user in their language (this user writes Turkish).

## Knowledge base (read on demand, do not re-research the web)

| Need | Read |
|---|---|
| GNOME style rules with evidence (chin, light, colour, sizes, visual mass) | `references/gnome-style-guide.md` |
| The numbers (official vs MoreWaita vs Adwaita++), legibility baseline, key reference ids | `references/measured-style.md` |
| Which treatment for which kind of icon (incl. lockups, monochrome marks) | `references/archetypes.md` |
| The 3-5 alternatives system, naming, colour sweeps | `references/alternatives.md` |
| Source-first geometry, input routing, autodraft levels, mascot protocol | `references/identity-preservation.md` |
| This user's history, preferences, rejected patterns, recent lessons | `references/lessons-and-rejections.md` (+ `user-requirements-tr.md`) |
| Quality gate: hygiene -> measurements -> looking -> honest report | `references/review-protocol.md` |
| CandyBar files, components, adb, pack audit, phone sizes, forced shapes | `references/android-candybar.md` |
| MoreWaita / Adwaita++ findings and lookup | `references/community-themes.md` |
| gnome_kit / autodraft API and SVG patterns | `references/svg-construction.md` |
| 134 real reference SVGs (98 app icons + 36 Adwaita system icons) | `assets/reference-library/` (`catalog.json`, `sheets/*.png`) |
| HIG template + palette | `assets/template/` |
| Worked example (3 invented apps, 11 alternatives, all boards) | `examples/demo-original-apps/` |

## Workflow

Run commands from the skill root (`python3 scripts/...`). Work in `work/<slug>/`
of the user's project (or a temp dir), never inside `assets/`.

**0. Setup (once):** `python3 -m pip install -r requirements.txt` (add
`--break-system-packages` on PEP 668 systems), then `python3 scripts/doctor.py`.
Optional: `export GNOME_ICONS_MOREWAITA=/path/MoreWaita-main.zip GNOME_ICONS_ADWAITAPP=/path/adwaita-plus-master.zip`.

**1. Scaffold, get geometry, draft** - one command:
```bash
python3 scripts/new_icon.py --slug <drawable_name> --app "<App>" --input <image|svg|xml|apk> \
        --alts faithful,disc,rimmed,symbol --work work [--ref-ids <catalog ids>]
```
Routes the input (`.png/.jpg/.webp` screenshot -> `extract_icon.py` + `trace_source.py`;
`.svg` -> `flatten_svg.py`; `.xml` VectorDrawable / `.apk` -> `apk_icon.py` -> flatten),
runs `analyze_source.py` (-> `identity.md`), writes `build.py` + `brief.md`, builds
**autodrafts** (correct GNOME construction around the real geometry) and renders
`review.png` + `legibility.png`. **Open `source.png` and `review.png`** - if extraction
guessed wrong, rerun `extract_icon.py` with `--crop/--keep-bg/--remove-bg`. For traced
images read "Trace notes" in `brief.md`: gradients it rebuilt, details it restored,
details it could NOT capture (redraw those by hand if they carry identity).
Best geometry first: APK vector (`find_component.py --pull <pkg>`) > official SVG > trace.
Community versions for comparison: `community_refs.py --search "<app>" --sheet ...`.

**2. Understand**: fill `identity.md` (2-4 anchors, must-not-change, archetype from
`references/archetypes.md`); pick 3-6 references (`ref_search.py --kind ... --shape ...`,
`inspect_svg.py <ref.svg>` to see their layers).

**3. Design**: refine each `build_<alt>()` in `build.py` with `gnome_kit` (families
A Faithful, B Sound Disc, C Rimmed, D Free Symbol, E GNOME Metaphor, F Light -
`references/alternatives.md`). Geometry stays from `SRC` (autodraft.Source); scale with
`xform_d()` / `fit_parts()`. Core numbers: canvas 128; circle d118-120 + 2 px chin;
square 104 r8 + 4 px chin; chin = darker copy moved down + horizontal chin gradient;
flat faces flat, curved faces gradient; glyph lift 1-2 px; no outer shadows; visual
mass ~0.62 of the canvas. Colourless marks: `recolor.py` sweep for the user to pick.

**4. Check**: `lint_svg.py` (no FAIL), `measure_style.py --compare official`,
`legibility_check.py` (RED gaps at identity anchors?), then **look**:
`preview_sheet.py` (source vs candidates, 64/48/32 px, labelled family row) and
`launcher_preview.py --shape all` (real phone size, 3 wallpapers, forced shapes).
Answer the 8 questions in `references/review-protocol.md`; fix structure, re-render,
re-look; drop weak alternatives.

**5. Export**: `export_png.py <svg> --out-dir work/<slug>/png` (512 + 256, transparent, verified).

**6. Integrate (only if the user gave the pack project)**: components via
`find_component.py`; `candybar_add.py ... --dry-run`, show the diff, run for real
(alternatives go to drawable.xml only); `pack_audit.py --project ... --sheet ...`
for XML integrity and family consistency; build if possible.

**7. Report** with the template in `references/review-protocol.md`: status, geometry
origin, per-alternative one-liners, measured numbers, known weaknesses, what was
not verified, files (SVG, PNG 512/256, review/legibility/launcher boards).

## Script index (`scripts/`)

| Script | Job |
|---|---|
| `new_icon.py` | scaffold + input routing + autodrafts + review/legibility boards |
| `extract_icon.py` | isolate icon from screenshot / viewer capture / icon on a plain canvas -> transparent PNG + report |
| `analyze_source.py` | measured identity facts + identity.md draft |
| `trace_source.py` | potrace colour layers -> reference SVG (detail pass, gradient bands -> `data-gradient`, report JSON) |
| `flatten_svg.py` | any SVG -> flat geometry (transforms baked, strokes outlined, masks removed) |
| `apk_icon.py` | APK / VectorDrawable -> SVG (adaptive background/foreground) |
| `autodraft.py` | ground/mark detection + level 0-1 drafts for every family |
| `gnome_kit.py` | construction library (plate, disc, rimmed_disc, slab, pieces, glyph(s), chin, fit) |
| `recolor.py` | colour sweep of a finished SVG across the HIG families |
| `find_component.py` | real ComponentInfo via adb / APK; pull APKs |
| `community_refs.py` | search MoreWaita / Adwaita++ local archives |
| `ref_search.py` | search the bundled GNOME library by kind/shape/text |
| `inspect_svg.py` | readable z-order layer dump of any SVG |
| `lint_svg.py` | hygiene FAIL/WARN (raster, text, filters, size, chin, colours) |
| `measure_style.py` | metrics (size, visual mass, chin, palette) vs official distribution |
| `legibility_check.py` | gaps that fuse / parts that vanish at 32-48 px, SSIM vs official baseline |
| `preview_sheet.py` | review board: 256 light/dark, true 64/48/32, labelled family row |
| `launcher_preview.py` | phone home screen at real size, 3 wallpapers, forced icon shapes |
| `pack_audit.py` | whole-pack XML integrity + visual consistency + family sheet |
| `contact_sheet.py` | any SVG grid |
| `export_png.py` | transparent PNG export with checks |
| `candybar_add.py` | safe, additive CandyBar import (+alternatives, dry-run diff, activity expansion) |
| `doctor.py` | environment check with install hints |

Tests: `python3 -m unittest discover -s tests -v`.
