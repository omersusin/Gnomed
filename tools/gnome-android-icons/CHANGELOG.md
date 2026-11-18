# Changelog

## 1.2 (2026-11-18)
- **Redesign-first.** A GNOME icon is the app's idea built as an object, not the app's logo
  on a plate. Reason: an 89-app pack built with v1.1 (Gnomed) came out as the source logo
  on plates/discs/rims with a chin, four copies each — the "logo + shadow" the user rejected.
- New `references/redesign.md`: concept ladder (L1 the mark becomes an object, L2 a GNOME
  object that carries the mark, L3 material tile), procedure (measure -> study -> 3 rough
  concepts -> the user picks with a multiple-choice question -> build -> look -> ship),
  construction rules (thickness, light from the top, recess, hole, secondary object,
  materials), HIG palette, budget rules.
- New `scripts/obj.py`: objects from shapely shapes — `solid` (side + face + top light),
  `recess`, `hole`, `toplight`, `rounded`, `circ`, `poly`, `geom_d`.
- New `scripts/concepts.py`: concept board (concepts vs source vs real GNOME object icons).
- New `examples/redesign/`: two invented apps as source / logo on a plate (wrong) / object
  (target), with code; `gnome-objects.png` labels the techniques of 8 official icons.
- `new_icon.py` is now the MEASURE step: creates `concepts/`, `redesign.py` and a brief with
  concepts and an `approved:` line; builds ONE measuring draft by default (`--alts faithful`),
  titled as a draft, not a candidate.
- SKILL.md workflow, alternatives.md (alternatives = other approved concepts), archetypes.md
  (where to look for concepts first), review-protocol.md (question 0: is it a redesign?),
  lessons-and-rejections.md (the Gnomed lesson), svg-construction.md (obj.py) updated.

## 1.1 (2026-11-07)
- `new_icon.py` routes PNG/JPG/WebP screenshots, SVG, VectorDrawable XML and APK inputs, then builds autodrafts for every family and renders review + legibility boards in one command.
- New: `autodraft.py` (ground/mark detection, source proportions on template shapes, figure/ground kept readable, ground gradients rebuilt, cut-outs -> real holes), `flatten_svg.py` (transforms baked, strokes -> outlines, masks/hidden layers removed, rgb()/hex gradient stops), `legibility_check.py` (+ official baseline in `assets/reference-library/legibility-baseline.json`), `launcher_preview.py`, `pack_audit.py`, `recolor.py`, `doctor.py`.
- gnome_kit: `glyph(fill_rule=)`, `glyphs()`, `pieces()`, `fit_parts()`, `bbox_d()`, `load_parts()`, `safe_box()`, `group()`, `chin_gradient(corners=)`, `lift_color()`; `chin_colors()` handles dark faces (lighter corner highlights) and light neutrals (official rim greys); robust `translate_d()` fallback for compact arc syntax. Demo renders are pixel-identical to v1.0.
- `measure_style.py`: visual-mass metric (`area`), raster `image_metrics()`, `--compare official` fixed (group aliases); catalog re-measured; measured-style tables now include visual mass and the legibility baseline; community summaries stored as JSON.
- `trace_source.py` (rewritten pipeline, same CLI): monochrome marks traced as one layer; small distinct details (eyes, dots) get their own colour; **detail pass** renders the trace, compares it with the source in OKLab and restores small sharp regions it lost (seeds, cheeks, eye highlights); **gradient pass** merges colour bands of one gradient (no edge between them in the source) back into one shape with `data-gradient` stops, so gradient icons (radial/linear backgrounds) get a real ground in autodraft; anti-aliasing blends can no longer become rings of a third colour; thin rims between an eye and its highlight survive; abutting shapes overlap 2 px (no seams); `<out>.json` report (gradients rebuilt, details restored, details still missing, smooth shading) that `new_icon.py` copies into `brief.md`; a potracer curve-optimiser math error (it crashed v1.0 on a gradient disc) now falls back to unoptimised curves instead of aborting.
- `extract_icon.py`: an icon on a plain white/grey canvas (JPEG from a website, a saved store icon) is no longer mistaken for a photo-viewer band and cropped to a strip; the viewer band must span the full screen width (or height); otherwise the icon region + nearby pieces are taken with a rim of canvas, so the canvas is removed and corners become transparent.
- `autodraft.py`: plateless drafts (Free Symbol, Light) carry the source gradient on the mark when the mark takes the gradient ground's colour.
- `preview_sheet.py`: explicit `--ref-ids` always honoured (Adwaita system icons included, user order kept); source on a checkerboard; every icon in the family row labelled.
- `candybar_add.py`: relative activity names expanded to full class names.
- `apk_icon.py`: compiled gradient drawables (aapt-extracted `<gradient>` resources) resolved; androguard debug logging silenced; verified on real APKs (adaptive vector icons incl. monochrome layer, bitmap-only icons).
- Docs: archetypes K (logo lockups) and L (monochrome marks), review protocol with measurements + launcher step, Android phone sizes and forced-shape notes, pack audit, lessons from the v1.0 sessions.

## 1.0 (2026-11-05) - rewrite of v0.9
- Reference library: 134 real, unmodified upstream SVGs (52 GNOME core, 14 GNOME games, 32 GNOME Circle/GNOME-styled, 36 Adwaita system) with repo, commit, path, licence, sha256 and metrics in `catalog.json` (v0.9 had 1 official GNOME app SVG).
- Measured style (`measured-style.md`): template boxes, chin heights, palette share, gradient use - official vs MoreWaita (516) vs Adwaita++ (739).
- `gnome_kit.py` construction library encoding official techniques (chin copy, chin gradient with corner highlights, glyph lift, rimmed disc, recessed crescent, calibrated chin colours).
- New tools: `extract_icon.py`, `analyze_source.py`, `trace_source.py` (potrace), `apk_icon.py` (VectorDrawable -> SVG), `find_component.py` (adb/APK), `community_refs.py`, `ref_search.py`, `preview_sheet.py`, `lint_svg.py`, `measure_style.py`, `new_icon.py`, safer `candybar_add.py` (both XML copies, alternatives, dry-run diff, refusals).
- Alternatives system (3-5 families) and archetype guide.
- Removed from the bundle: MoreWaita/Adwaita++ brand icons and earlier brand-logo derivative examples (third-party marks); community themes are now read from the user's own archives.
