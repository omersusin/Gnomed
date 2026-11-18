# Lessons from this project's history (read before every new icon)

The user (Turkish-speaking; replies in Turkish) has been building this pack
across several agents. These are their standing rules and the outcomes of
earlier attempts. Treat them as requirements.

## Standing rules from the user

1. **No generative image tools, ever** (ImageGen, DALL-E, Stable Diffusion,
   image-edit models). Only real SVG sources, hand/code-written SVG, and
   code tools (Python, CairoSVG, Pillow, potrace, Inkscape). This rule was
   broken by earlier agents several times - do not be the next.
2. No PNG inside SVG presented as vector (`lint_svg.py` fails it).
3. Shadow/emboss/recolour on top of the original logo is **not** a GNOME conversion.
4. No random TV, camera body, speaker, square/squircle backplate, frame or coin
   added to make something "look GNOME".
5. Silhouette, character anatomy, pose, negative space and colour relations of
   the original must survive.
6. No guessed curves for known shapes (Firefox's face/tail, a mascot's arms).
7. Do not force one recipe on every icon.
8. Passing technical checks is not aesthetic success - never call a design
   "fixed" or "GNOME" because tests pass.
9. Do not redo the same internet research for every icon - the bundle is the
   knowledge base.
10. If something could not be done or verified, say it plainly.

## Outcomes of earlier attempts

| Case | What happened | Lesson |
|---|---|---|
| Three-triangle media logo | a meaningless blue TV/screen was built around the triangles | never invent a container object; a GNOME icon can be just the symbol (Totem, Showtime are play *emblems*) |
| Instagram | thick plastic toy camera bodies, heavy rims, glossy reflections - rejected | simplify to flat planes; the user preferred a calm Sound-Disc-family look |
| Spotify | **"1. Sound Disc" chosen**: plain green disc, subtle depth, soft top light, engraved waves; "Speaker Grille" was a different, unwanted direction | the reference for family B (see `alternatives.md`) - but not every icon becomes a disc |
| Firefox | ears, horizontal snout, purple globe and rising yellow tail broken repeatedly; or just the original logo with a shadow | work from real vectors; the MoreWaita-based version was better; then remove stray inner contours the user marked |
| ChatGPT | two variants from MoreWaita's knot symbol (green/teal and white/ivory) | example only; no family decision taken |
| TikTok | note silhouette and colour relationship are the identity; the small lightning detail in the source is a real element | keep small identity details if they are in the source; check them at 48 px |
| Clash Royale (game poster with two kings) | reducing a character game to a symbol loses identity | archetype H: pick one known identity element, offer alternatives on different elements |
| White/turquoise dinosaur mascot | first vector: arms tangled, body/feet broken, back spikes lost; later contour-preserving version better | archetype G protocol: trace, split into parts, define once, verify limbs |

## Lessons from the v1.0 -> v1.1 sessions (2026-11-05 .. 07)

| Case | What happened | Rule now |
|---|---|---|
| User's own channel logo (robot head + two letters, white only) | 5 alternatives worked; at 32 px the dot and bar of the letter fused with the stem in every plated variant; the plate-less Free Symbol read best | lockups = archetype K: check `legibility_check.py`, offer a symbol-only or letters-larger variant |
| Same logo on a dark plate | the default darker chin disappeared on dark wallpapers | `chin_colors()` now keeps dark faces' chins close and lightens their corner highlights |
| Same logo had no colour of its own | colours had to be chosen for it | archetype L: offer a colour sweep (`recolor.py`), do not present an invented colour as the brand's |
| Original file-manager icon | the split-front folder read as a book/cabinet until the tab strip + front flap separation was drawn; chin highlights at a sharp inner corner looked wrong | metaphor icons need the object's *signature line* (folder tab); `chin_gradient(corners=...)` puts highlights only on rounded outer corners |
| Review board | the user had to ask which icons the family row showed | every reference in the family row is now labelled; reports explain the board sections |
| A requested reference (Adwaita folder) silently missing from the board | the board dropped Adwaita system icons even when asked by id | explicit `--ref-ids` are always honoured, in the given order |
| **Gnomed pack (89 apps, built by Claude Code with v1.1)** | every app came out as the source logo on a plate/disc/rim with a chin, four copies each - exactly the "logo + shadow" the user rejected. Causes: autodrafts treated as designs, a procedure that said "follow exactly", a quality gate that measured fidelity to the source and hygiene but never "is it a redesign" | v1.2: references/redesign.md (object, not logo on a plate), concepts -> user picks -> build, `obj.py`, `concepts.py`, autodrafts only measure. In the Gnomed repo the gate fails apps without an approved redesign |
| Tracer stress test (gradient tiles, a mascot with seeds/cheeks/eye highlights, JPEG copies) | gradients came out as 2-5 flat bands, so no ground was found and every draft broke; seeds, cheeks and highlights vanished; a third colour ringed the eye highlights | gradient pass + detail pass in `trace_source.py`; read the "Trace notes" in `brief.md` and redraw whatever is listed as NOT traced |
| Mascot JPEG on a white page | the extractor took it for a photo-viewer band and kept only a strip of the picture | viewer bands must span the full screen width/height; plain-canvas icons are cut out whole with transparent corners. Still: open `source.png` before anything else |

## Failure modes to self-check (each was seen at least once)

- glyph shrunk into a big plate -> low visual weight next to GNOME icons
- chin as a blurred shadow, or chin on all sides (bevel)
- each sub-shape extruded separately so pieces float
- white arc highlight pasted on top-left of every icon
- dark tile icons vanishing on dark wallpapers (add light edge / chin highlight)
- grey glyph side reading as dirt (use the glyph's own side colour, 1-2 px)
- re-lettering a logo with a system font
- reporting "done" without looking at the 32 px row
- a wordmark's dots/letters fusing at 32 px (see the RED marks of `legibility_check.py`)
- a dark plate whose chin vanishes on dark wallpapers
- relative activity names (`pkg/.Main`) in appfilter
- trusting the trace: it is flat reference geometry - gradients live in `data-gradient`, lost details are listed in the brief
- shipping autodrafts / "0 FAIL" icons without a concept the user picked: that is the logo on a plate
- four template versions of the same logo as "alternatives"

## Images of past outputs

The user keeps the old visual examples (original logos, the preferred Sound
Disc PNG, rejected attempts) in their handoff archive (`visual-examples/`).
They are third-party brand derivatives and are not redistributed in this
skill; if the user attaches them, read them as context, never as templates.
