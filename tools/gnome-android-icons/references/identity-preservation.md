# Identity preservation - source first, never from memory

The fastest way to ruin an icon is to redraw a well-known shape from memory:
ears move, tails flip, limbs fuse, letters change weight. Previous attempts in
this project failed exactly that way (see `lessons-and-rejections.md`).

## 1. Geometry source hierarchy (use the highest available)

1. **The app's own vector**: `apk_icon.py --apk base.apk` converts the adaptive
   icon's VectorDrawable layers to SVG (exact designer paths). Get the APK from
   the phone: `find_component.py --pull <package> --out work/`.
2. **Official brand SVG** the user supplies (press kit, website). Note its licence/terms.
3. **A community Adwaita-style version** (MoreWaita / Adwaita++ via
   `community_refs.py`) - only as *reference* for how others solved it; they are
   GPL third-party works and not GNOME policy. Say so if you adapt one.
4. **Trace of the user's image**: `extract_icon.py` -> `trace_source.py`
   (potrace). Real contours of the real logo; clean them, do not invent them.
5. Nothing usable -> say so, ask for a better image. Do not guess curves and call
   the result faithful.

Record the origin in the SVG `<desc>` and in `brief.md`.

`new_icon.py --input` routes all of these automatically: `.svg` -> `flatten_svg.py`
(transforms baked in, strokes outlined, gradients kept as stop lists, masks
removed) -> `source-geometry.svg`; `.xml` VectorDrawable and `.apk` -> SVG -> same;
images -> `extract_icon.py` + `trace_source.py` -> `source-trace.svg`. Then
`autodraft.py` builds level 0-1 drafts from those parts (see below) - a correct
starting point, never the finished design.

What the tracer does for you, and what it cannot (read `source-trace.json`,
copied into `brief.md` as "Trace notes"):

- **Gradients**: bands of one colour ramp are merged back into one shape with
  `data-gradient` stops; autodraft rebuilds them as a GNOME diagonal gradient.
  The trace itself is flat - judge the ramp against `source.png`, not the trace.
- **Small details** (eyes, highlights, cheeks, seeds, dots) lost by colour
  quantisation are restored by the detail pass. Whatever is listed as "NOT traced"
  (too small, or blurred away in a JPEG) must be redrawn by hand if it carries
  identity - check the listed position on `source.png`.
- **Soft shading** (glows, soft shadows) is not traced; GNOME style usually drops
  it anyway - decide consciously.
- Low-quality inputs (small, JPEG, upscaled screenshots) give wobbly contours:
  simplify and snap them; never present the raw trace as the design.

## 2. Identity sheet (before drawing)

`analyze_source.py --out-md work/<app>/identity.md` writes measured facts and
empty slots. Fill:

- **Anchors (2-4):** what makes it recognisable at 32 px. Silhouette, a key
  angle, a negative space, a colour relation.
- **Must not change:** pose, element count, orientation, tilt, corner style,
  stroke contrast, colour order.
- **May be GNOME-ified:** gloss -> flat planes, add chin, brand hue -> nearest
  HIG swatch if dE < ~10, merge sub-32-px detail, unify light direction.

## 3. Transformation levels

| Level | What changes | Verdict |
|---|---|---|
| 0 | original logo + chin only (MoreWaita-style baseline) | Recognisable but the user rejected it as *not* a GNOME conversion **on its own**. Acceptable only as the "Faithful" base *after* level-1 work |
| 1 | Adwaita restyle: GNOME template shape, flat planes, palette roles (face/chin/highlight), glyph lift, curvature light only on curved faces, 2 px grid, simplified detail | the default target |
| 2 | GNOME metaphor: identity anchors carried by a domain object | alternative E only, with justification |

`autodraft.py` produces level 0-1 automatically (ground/mark detection, the
source's proportions on the template shape, chins, lifts, figure/ground kept
readable, cut-outs turned into real holes when the plate is gone). The agent's
job starts there: archetype treatment, proportions, colour roles, restraint.

## 4. Allowed edits vs forbidden edits

Allowed: re-proportion the container; thicken hairlines optically (+0.5-1 px);
merge tiny decorations; replace gradients with flat planes + chin; move hue a
little toward the palette; snap straight edges to the 2 px grid.

Forbidden: changing the number of rays/petals/limbs; changing a pose; moving a
negative space; re-lettering with a font; mirroring; adding objects the source
does not have (screens, cameras, speakers, coins, frames, rims stacked on rims);
replacing a mascot with a generic animal.

## 5. Mascot / character protocol

1. Trace or import the character; split it into named parts (head, body, arm_l,
   arm_r, leg_l, leg_r, eyes, mouth, accessories). One function returns them all
   (see `examples/demo-original-apps/build_demos.py: simit_parts`).
2. Paint order = depth order: limbs behind the body first, body, then limbs in
   front, then face details. Check each limb has exactly one attachment point.
3. Give body parts flat faces + 2-4 px chins; eyes 2 tones + 1 glint.
4. Scale the *whole* character per alternative with `xform_d()` - never edit
   one variant's anatomy.
5. Verify: render source and result at 256 side by side; count limbs, fingers,
   spikes, eye positions; check silhouette overlap visually. Report any mismatch.

## 6. Overlay check (any archetype)

Put the source PNG and the candidate in the first row of `preview_sheet.py`,
or overlay: `contact_sheet.py` both at the same size and flip between them.
Questions: same silhouette? same negative spaces? same angles? same colour
order? If not identical, is the difference a deliberate GNOME-ification listed
in the sheet?
