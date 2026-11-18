# MoreWaita and Adwaita++ - what they do (measured), how to use them

Both are **community** icon themes in the Adwaita style - useful precedent for
"how do other people put third-party brands into GNOME's look", **not** GNOME
policy. Both are copyleft-licensed works (GPL / LGPL / CC-BY-SA) whose brand icons derive from third-party
trademarks, so this skill does not redistribute them; `community_refs.py`
reads your local copies (the user's `MoreWaita-main.zip` /
`adwaita-plus-master.zip`) or clones them on demand.

```bash
export GNOME_ICONS_MOREWAITA=~/archives/MoreWaita-main.zip
export GNOME_ICONS_ADWAITAPP=~/archives/adwaita-plus-master.zip
python3 scripts/community_refs.py --search "app name" --sheet work/app/community.png
```

## MoreWaita (somepaulo/MoreWaita, GPL-3.0)

- 516 unique app SVGs (+ thousands of symlink aliases), 128 canvas.
- README policy: for branded icons "stay as close as possible to the original
  icons - to the point of using them in full - and give them the distinct Adwaita
  perspective and general flatness"; **keeps brand colours** (median only 27 %
  HIG swatches).
- CONTRIBUTING: avoid strokes, no mesh gradients, plain SVG, start from an
  existing icon of similar shape, use GNOME's template, every app icon has a
  symbolic variant.
- Measured: sizes snap to the template (circles 120 x 122 bottom 125; squares
  104 x 104 bottom 116); chin almost always **4 px**; median **5 paths**;
  3 horizontal gradients (chin highlights).
- Technique in one line: *original logo, flattened, on the template shape,
  plus a 4 px darker chin with corner highlights.* That is "level 0-1" in
  `identity-preservation.md` - good for recognisability, but the user wants more
  GNOME-ification than that on its own.

## Adwaita++ (Bonandry/adwaita-plus: LGPL-3.0 or CC-BY-SA-3.0 per COPYING; README credits GPL-3 Papirus-derived parts)

- 739 unique app SVGs in `Adwaita++/apps/scalable` (plus Light/Dark/Colorful variants).
- Re-colours toward the HIG palette (median 80 %), fewer gradients (median 1),
  thinner chins (median 4, p25 2).
- Frequent construction: brand mark on a disc with a **light neutral rim**
  (Clocks-like), or the brand shape with soft Adwaita shading. Several brands
  have multiple historic alternatives (e.g. many browser versions).

## How to use them in a conversion

1. Search the app. If both themes have it, render them side by side with the source.
2. Note what each kept (anchors) and changed (container, colours, depth).
3. Use them as *evidence of what is recognisable*, then build your own SVG with
   `gnome_kit` from the best geometry source (`identity-preservation.md`).
4. If you adapt their paths, keep the GPL notice and tell the user - never
   present adapted community art as newly drawn.
