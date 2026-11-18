# Alternatives (3-5 designs per app) — v1.2

The user wants 3-5 alternatives per app. In v1.0-1.1 that became the same logo on four
template shapes (plate, disc, rimmed disc, extruded symbol) — and a whole pack of
"logo + chin" icons the user rejected. Now:

**An alternative is another concept the user approved, built as an object.**

## How they come about

1. `references/redesign.md` step 3: three rough concepts from the ladder
   (L1 the mark becomes an object, L2 a GNOME object carrying the mark, L3 material tile).
2. The user picks with the multiple-choice tool. He may pick one (primary only) or
   several (primary + alternatives). Never build an alternative he did not pick.
3. Each picked concept gets its own `design_<x>()` in `redesign.py`, same identity
   geometry (anchors measured once from the source), different idea.

## The old families — what they are now

| Code | Family | Ladder | When it is still right |
|---|---|---|---|
| D | Free Symbol | L1 | the mark itself is a strong object shape — only with material, thickness and light, not just a chin |
| E | GNOME Metaphor | L2 | the app's function has an obvious object (record, lens, book, box, bag) that can carry the mark |
| B | Sound Disc | L3 | music/audio-like apps (the user liked it for Spotify-like marks); never by default |
| C | Rimmed | L3 | circular marks that need a neutral frame |
| A / F | Faithful / Light | L3 | pure wordmarks or abstract marks where L1/L2 fail — with a real material, never a flat tile |

`autodraft.py` still builds A/B/C/D/F automatically: use them to **measure** (does the
geometry read? which colours?), never as candidates.

## Rules

1. Same identity geometry in every alternative (one source definition, measured).
2. Order by expected fit; one line each on why it exists.
3. Drop an alternative that fails the review instead of shipping weak ones.
4. Naming: primary `<app>.svg`, alternatives `<app>-<concept>.svg`; in the pack
   `<drawable>`, `<drawable>_alt1`, ... with labels like `"App (Disc)"`
   (`candybar_add.py --alt FILE:Label`). Only the primary is mapped in `appfilter.xml`.
5. Colour is a separate axis: `recolor.py` on the chosen design instead of more alternatives.
6. Present all of them in one board (`concepts.py` / `preview_sheet.py`) with honest notes.
