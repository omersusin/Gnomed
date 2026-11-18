# Alternatives system (3-5 designs per app)

Icon packs ship alternatives so users can pick a look per app. This skill makes
**3 by default, up to 5**, each a *different construction*, not the same icon
with a different corner radius.

## The families

| Code | Name | Construction (gnome_kit) | Use when | Never when |
|---|---|---|---|---|
| A | **Adwaita Faithful** | source geometry 1:1 on its own template shape (`plate()` / `slab()`), brand colours, chin + chin gradient, glyph lift | always possible; default primary for tile glyphs, multicolour marks | - |
| B | **Sound Disc** | `disc()` d118, 2 px chin, curvature light, soft `top_light`, mark lifted or engraved | source is circular, or the mark is compact and centred | the identity *is* a non-circular silhouette (a tall letter, an animal outline) - then offer it last or not at all |
| C | **Rimmed** | `rimmed_disc()`: Adwaita light rim + recessed brand disc (Clocks/Mousai construction) | circular marks, marks that need a neutral frame on dark wallpapers | busy marks that need every pixel |
| D | **Free Symbol** | the mark itself is the silhouette: `slab()` with chin, no backplate | strong, compact glyphs (play, note, bubble, letter) | glyph thinner than ~0.6 aspect without compensation; white-only glyphs (vanish on light wallpapers) |
| E | **GNOME Metaphor** | a domain object that *carries* the identity (record label, lens, book cover, plate) | the app's function has an obvious analog object and the anchors stay readable at 48 px | as a wrapper for an unrelated logo (TV around a play icon, camera around a social logo) |
| F | **Light / Dark** | neutral plate (`#f6f5f4` or `#3d3846`), mark in brand colour | brands whose colour is the mark, not the background | when it turns the icon into a generic grey tile |

User preference recorded in the history: **Sound Disc look liked** (for
Spotify-like and Instagram-like marks), "Speaker Grille"-like object wrappers
not wanted, every icon round **not** wanted. So: B is offered where it fits,
never forced.

## Rules

1. Every alternative uses the **same identity geometry** (one source definition,
   scaled with `xform_d()`); only the construction around it changes.
2. Order alternatives by expected fit (primary first); say in one line why each exists.
3. Drop an alternative that fails the review (32 px mush, identity lost) instead of shipping 5 weak ones. Three good > five mediocre.
4. Naming: primary `<app>.svg`, alternatives `<app>-<code-name>.svg` in work;
   in the pack `<drawable>`, `<drawable>_alt1`, `_alt2`... with dashboard labels
   `"App (Disc)"`, `"App (Rimmed)"` (`candybar_add.py --alt FILE:Label`).
5. Only the primary is mapped in `appfilter.xml`; alternatives live in
   `drawable.xml` so the user picks them via the launcher's edit-icon dialog.
6. Present all of them in one `preview_sheet.py` board, with honest per-variant notes
   (e.g. "D: weakest at 32 px - stem 1.5 px"), plus `legibility_check.py` and
   `launcher_preview.py` boards.
7. Lockups (symbol + letters): one alternative may drop or enlarge parts
   (symbol-only / letters-larger) - from the same parts, say what was dropped.
8. Colour is a separate axis: when the source has no colour (white-only mark) or
   the user wants another, run `recolor.py` on the chosen alternative instead of
   multiplying alternatives.

## Example (demo `lale`, invented app)

| File | Family | Note from the review |
|---|---|---|
| `lale-disc.svg` | B Sound Disc (primary: source is a disc) | reads at 32 px; closest to source |
| `lale-rimmed.svg` | C Rimmed | best separation on dark wallpapers |
| `lale-record.svg` | E Metaphor: vinyl, label carries the mark | mark is small: tulip shape mushes at 32 px |
| `lale-symbol.svg` | D Free Symbol | narrow (aspect 0.45): looks light next to GNOME icons; weakest |
