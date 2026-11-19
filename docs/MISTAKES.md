# Mistakes made in this project — and the rule that prevents each one (binding)

Every line below really happened. Read this list before you change an icon, a tool or
the app. When you make a new mistake that the owner has to point out, add it here in
the same pull request that fixes it: **what happened → why → the fix → the rule/tool**.

Linked from [REDESIGN.md](../REDESIGN.md) §9 and [AGENTS.md](../AGENTS.md).

## 1. Size, baseline, canvas

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| Telegram's envelope looked smaller than Instagram and WhatsApp next to it on the phone | its bottom edge was at 107: a wide, short object "floating" above the line the others stand on; the old rule "bottom 108…126" let it pass | scaled as one unit to 112 wide and put on the baseline (bottom 118) | **Baseline rule** (REDESIGN.md §5): free objects stand on 116–120, plates 114–118, discs 120–125. Larger side ≥ 96 (objects) / 100–108 (plates) / 112–120 (discs). `python3 tools/size_audit.py` must print `0 icon(s) outside the ranges` |
| Scene's Symbol floated (bottom 108) | the Symbol was sized by the WHOLE mark, but parts listed in `drop` are not drawn — the drawn object was shorter than the box | `build_auto.box()` sizes the Symbol by the drawn parts | size and place by what is drawn, never by what was measured and then dropped |
| aShell's Symbol overflowed the canvas (y 1…124); Apple Music, KernelSU, Qobuz, Recon, Reddit, Termux, Walpy sat low | margin-mode Symbols: the white/coloured margin grows outward on every side, but the box ignored it | object + margin must fit 5…118; the margin's bottom is on the baseline | anything that grows outward (margin, outline, glow) counts in the size |
| Kamera and Saat Symbols 2 units too low | hand-built coordinates chosen by eye | lifted onto the baseline | hand-built icons go through `size_audit.py` too |
| Wide Symbols floating in the middle of the canvas (old pipeline) | centred vertically instead of standing | free objects stand on the baseline | — |

## 2. Identity, colours, shapes

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| The pack was "the logo on a plate with a chin" for every app | the automatic pipeline only copies the logo | REDESIGN.md: the app's idea built as a GNOME object | `check_icon.py` FAILs automatic drafts (`redesign`) |
| A play logo wrapped in an invented TV; Instagram as a toy camera | invented containers | removed | never invent wrappers that have nothing to do with the app |
| Firefox ears/tail drawn from memory | memory instead of measurement | traced from the source | every shape from `source.png` / `geometry.json` / official SVG |
| ChatGPT came out inverted | built from the black lines only | figure = white strands outlined in black | check figure vs ground before building |
| Orange "inner layer" inside Instagram's frame | side face in a different colour | side = darkened copy of the face gradient | sides follow their face |
| SD Maid's dark apron vanished into the dark tile | its colour was only dE 8 from the tile, below the detection threshold | lower `THRESH` for that app; Symbol keeps the white bow (`symbol: keep`) | `python3 tools/region_check.py <slug>`: no blob ≥ 1.5 % with a changed colour |
| exteraless lost its pale pink tile, ObtainX's gear turned lavender, Proton VPN's turquoise tip went pale | `light: True` forced white; k-means medians drifted | `face`, `regions`, `merge_grad` | compare colours with the source (`region_check.py`), not by memory |
| Gradients flattened to one colour (Firefox Beta 32 % of the tile, Thunderbird, Proton …) | each region drawn with its median colour | big regions with a clear source gradient keep a fitted gradient automatically | — |
| Stripes: one gradient cut into bands (Today Weather, Morphe, Nuvio …) | k-means splits a gradient into 3–5 colours | `merge_grad` (one fitted gradient) | `check_icon` `stripes` WARN → recipe R1 |
| Pure black parts got a black gradient (aShell, KernelSU) | the automatic gradient ignored the Dark-4 rule | near-black regions stay flat `#241f31` | no `#000`, darkest is `#241f31` |
| Firefox Beta's "BETA" letters were thin slivers | the letters are holes; the badge's own lift side filled them | `holes_inlay`: holes drawn on top in the tile colour | look at letters/holes at 256 px |
| Quarry's chart bars came out blue | thin dark parts folded into the blue ring cluster | `split` override | — |
| Wobbly edges / blobs from blurry 192 px sources | pixel staircase | smoothed tracing (`gtrace`), `SMOOTH`, `THRESH`, `HALO` | — |
| A white wordmark alone as a Symbol | vanishes on light wallpapers | no Symbol, or a margin | `check_icon` `visible_light/dark` |

## 3. Styles and what the owner sees

| What happened | Why | Fix | Rule |
|---|---|---|---|
| Duolingo showed a square plate among plate-less icons | the owner uses the **Symbol** APK; an app without a Symbol falls back to Faithful | Symbol built | every app needs a Symbol that fits the Symbol style, or the owner's OK to skip it |
| "Make the envelope the default" — but the phone still showed the cloud | "default" was read as the Faithful slot; the owner's phone shows the **Symbol** slot | the envelope in Faithful AND Symbol | "default" = what the owner sees: ask which style he uses, or put it in every slot he uses |
| Telegram stamp: asked to fix the paper plane, the whole Telegram logo (circle + plane) was put on it | the request was widened | only the plane, measured | change exactly what was asked, nothing more; when unsure, ask |
| Hand-built icons (Shizuku, Clash Royale, …) were replaced by automatic drafts in the pack | `build_auto.py` was run over every app | `work/_lib/builders.py` decides the builder; `build_auto.py` refuses hand-built apps; `pack_refresh.py` rebuilds with the right builder | never run a builder over "all apps" and ship the result without a pixel diff |

## 4. Process, git, app

| What happened | Why | Fix | Rule |
|---|---|---|---|
| An agent's PR used a ComponentInfo copied from other icon packs | not from the phone | verified with `cmd package resolve-activity` | ComponentInfo only from the owner's phone / request / APK (AGENTS.md A3) |
| `Shell$HomeActivity` lost its `$` | shell expansion | single quotes | always single-quote ComponentInfos |
| Release APK crashed at start | R8 removed a Room constructor | `proguard-rules.pro` + CI guard | never touch ProGuard/CI without the owner |
| In-app style switch got 404 | no release existed; tag pushes are blocked | release on `[release]` / manual run | only the maintainer releases |
| Wallpapers made the APK 2.4 MB bigger | embedded in assets | loaded from the repo (`wallpapers/wallpapers.json`) | — |
| Agents could reach `main` | no guard | AGENTS.md §0, `tools/hooks/`, `pr_guard.py` in CI | never commit/push/merge to `main` |
| "Tests pass, so it's done" | checks measure, they do not see | look at the boards; report weaknesses | the owner approves, not the gate |
