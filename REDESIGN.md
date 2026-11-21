# REDESIGN.md — how a Gnomed icon is made (binding)

Read this first. Where `docs/course/`, `CONTRIBUTING.md` or the old pipeline disagree
with this file, **this file wins**. Git, ComponentInfo and pack-file rules stay in
[AGENTS.md](AGENTS.md) (sections 0, A, B, G and steps C7–C11).

## 1. The one rule

**A Gnomed icon is the app's idea built as a GNOME object — not the app's logo on a plate.**

![what a redesign is](docs/redesign/target.png)

Test: cover the plate/disc and the chin. If what is left is the original logo, the icon
is not done.

The automatic builds (`tools/make_icon.py` for an app without `work/<slug>/redesign.py`,
`build_auto.py`, the skill's autodrafts) only **measure** shapes and colours. Their
output is a draft. The gate fails it (`redesign` check) until the app is redesigned.

The same method, without the repository parts, is in the vendored skill:
`tools/gnome-android-icons/references/redesign.md` (v1.2).

Real GNOME icons to study before every app: [docs/redesign/gnome-objects.png](docs/redesign/gnome-objects.png)
(SVGs in `tools/gnome-android-icons/assets/reference-library/`).

## 2. What the human wants (his own words, summarised)

- the real GNOME / Adwaita look — he loves the official GNOME app icons
- the app recognisable at a glance: 2–4 **anchors** of the source survive
- premium, made-by-a-professional look; every app gets its own idea
- **not**: the logo with a shadow, emboss or chin; the logo inside a plate, disc or rim;
  every icon round; invented wrappers (TV, camera body, speaker, coin) that have nothing
  to do with the app; image-generation models of any kind
- liked: the "Sound Disc" look for music-like apps — only where it fits

## 3. The concept ladder (choose per app)

| Level | What | GNOME examples |
|---|---|---|
| **L1** | The mark **becomes an object**: its own silhouette gets thickness, material, light | Calls (handset), Polari (bubbles), the *Kasa* example |
| **L2** | A GNOME **object that carries the mark**: the app's function as a thing; the mark is its label, print, inlay, lens or the thing it holds | Weather, FileRoller, Software, Mousai, the *Bulut* example |
| **L3** | **Material tile** — only for pure wordmarks/abstract marks when L1 and L2 fail: glass, enamel, metal or paper with real thickness, never a flat colour square | Meld, Tangram |

### 3b. Games and posters (owner's rule)

A game's icon is a poster or a scene, not a logo. **Design an ORIGINAL logo inspired by
the game** — "oyunun logosuna bakarak, esinlenerek yapacaksın; direkt kopyala yapıştır
yapmayacaksın; oyuna uygun bir logo yap":

- pick what the players know: the hero item or mascot TRAITS and the game's palette
  (Clash Royale → two crowns; Rush Royale → the wizard hat with crown band, gem and
  crystals; Head Ball 2 → an angry big-head footballer heading the ball; Pokémon UNITE →
  a yellow electric face with dark-tipped ears and red cheeks on the purple/orange goal ring);
- draw it new, as a GNOME object (thickness, light from the top, secondary object) with
  colours measured from the poster;
- **not** a copy or trace of the poster (rejected: "hiç benzemiyor" for blobby traces),
  **not** a generic object that could be any game (rejected: a plain ball, bolt or hat);
- test: a player of the game names it at a glance.
- The owner's permission for this adaptation is given once for all games — do not ask it again.

Wordmarks: letter shapes come from the source (trace / geometry.json), never from a font
and never `<text>`; make the letters the object (L1) or print them on one (L2).

## 4. Procedure — one app, in this order

```
1  python3 tools/new_redesign.py <slug>   -> MEASURES the source (geometry.json), prints
           every part as text (colour, % of tile, box), creates design.md,
           concepts/make_concepts.py (a working template) and redesign.py.
           "WARNING ... POSTER" -> ask the owner which element to adapt.
2  STUDY   open work/<slug>/source.png and docs/redesign/gnome-objects.png (cannot see
           images? use the printed parts). design.md: anchors, function object.
           Shapes and colours come from the measurement: parts(), colour(), describe()
           (AGENTS.md section H) - never from memory.
3  CONCEPTS  edit work/<slug>/concepts/make_concepts.py: A/B/C = three different ideas
           from the ladder (fit() places the measured parts; flat shapes are fine).
           python3 work/<slug>/concepts/make_concepts.py && python3 tools/concepts.py <slug>
           -> open work/<slug>/concepts.png; replace any concept that is the logo on a
           plain disc or square.
4  ASK     (question budget: the concept choice and the final look are the ONLY two
           questions per app - several apps in ONE AskUserQuestion; never ask a third time
           in another form: after "none" twice, decide yourself with §3/§3b and show the result)
           AskUserQuestion, in Turkish: "Hangi yön?" options A / B / C / "Hiçbiri, yeniden dene",
           each with one short line; tell him the board is work/<slug>/concepts.png.
           STOP until he answers. Write in design.md:  approved: <letter> - <his words>
           Never fill "approved" yourself.
5  BUILD   copy the approved concept into work/<slug>/redesign.py (design()), delete the
           "raise SystemExit" line, polish with obj.py (solid, recess, hole, toplight, fit,
           parts - AGENTS.md section H). Models: work/telegram/redesign.py,
           docs/redesign/examples/build_examples.py.
           python3 tools/make_icon.py <slug>   (FAIL? AGENTS.md section I)
6  LOOK    open work/<slug>/review.png and answer:
           a) same idea and anchors as the source?
           b) does it belong in the family row next to the real GNOME icons?
           c) reads at 48 and 32 px on light AND dark?
           d) at least 3 techniques of section 5 used?
           e) nothing that is only "logo + chin", not the logo on a plain disc/square
              (the gate's plain_shape check FAILs a plain disc)?
           f) same baseline and size as its neighbours in the family row (no floating)?
           Fix (max 3 rounds), then show him review.png with AskUserQuestion:
           "Tamam" / "Şunu değiştir" / "Konseptlere dön".
7  SHIP    tools/check_icon.py <slug> = 0 FAIL, tools/size_audit.py = 0 outside,
           then AGENTS.md C7-C11:
           new app: pack_add.py --dry-run -> his yes -> pack_add.py
           app already in the pack: tools/pack_refresh.py <slug>
```

## 5. Construction rules

- Canvas 128 × 128; the object inside 8…120; painted area about 45–65 % of the canvas.
- **One baseline, one size** (every icon stands next to the others on the home screen):
  free objects (every redesign, every Symbol) have their **bottom edge (side included)
  at 116–120** (target 118) and their larger side ≥ 96; plates end at 114–118, discs at
  120–125. A wide, short object (envelope, cloud, keyboard) is made **wider (up to 112)
  and stands on the baseline** — it never floats in the middle. Anything that grows
  outward (margin, outline, glow) counts in the size and must stay inside 5…118 + side.
  Check: `python3 tools/size_audit.py` → `0 icon(s) outside the ranges`.
- **Thickness** (the side under the face): 2 px thin parts and discs, 4–6 px flat objects,
  8–24 px boxes, devices, cylinders. `solid()` derives the side colour from the face.
- **Light from the top**: curved faces get a vertical gradient (top lighter), flat faces
  are almost flat; a 1–1.5 px **top light** on upper edges (`toplight()`).
- **Recess** (screen, label, inlay): its top inner wall is darker (`recess()`).
  **Hole** (lens, slot, keyhole): dark body, darker top wall (`hole()`).
- **Secondary object**: smaller, in front, bottom centre or lower right, with its own side.
- **Materials**: metal = Light 1–4 with a lighter middle on the side; glass = deep centre,
  rings, 1–2 soft highlights; paper = Light 1–2, almost flat; enamel/plastic = 3 steps of one ramp.
- No outer shadows, no blur or filters, no `<text>`, no raster images, no pure black
  (`#241f31` is the darkest). One idea per icon: drop decoration that does not carry identity.
- Details under 2 px vanish at 32 px: merge them or leave them out.
- **Palette** (GNOME HIG). Map the brand colour to the nearest ramp, keep its lightness;
  use 3 steps of one ramp per part (top light / face / side):

| Ramp | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Blue | #99c1f1 | #62a0ea | #3584e4 | #1c71d8 | #1a5fb4 |
| Green | #8ff0a4 | #57e389 | #33d17a | #2ec27e | #26a269 |
| Yellow | #f9f06b | #f8e45c | #f6d32d | #f5c211 | #e5a50a |
| Orange | #ffbe6f | #ffa348 | #ff7800 | #e66100 | #c64600 |
| Red | #f66151 | #ed333b | #e01b24 | #c01c28 | #a51d2d |
| Purple | #dc8add | #c061cb | #9141ac | #813d9c | #613583 |
| Brown | #cdab8f | #b5835a | #986a44 | #865e3c | #63452c |
| Light | #ffffff | #f6f5f4 | #deddda | #c0bfbc | #9a9996 |
| Dark | #77767b | #5e5c64 | #3d3846 | #241f31 | — |

## 6. Styles and alternatives

The pack has four slots: `faithful`, `disc`, `rimmed`, `symbol`. The approved design goes
into `faithful`. Fill another slot **only** with a concept he also approved.
`save_styles()` overwrites the old wrapper SVGs of an app that is already in the pack with
the new design, so no logo-on-plate version survives. Never make four versions by default.

## 7. Budget — he pays for every message

- One app per session; start the next app after `/clear`. Batches only after he approved
  three redesigns in a row, and only the apps he names.
- Do not read the whole course or CONTRIBUTING.md; this file, AGENTS.md (0, A, B, G) and
  `docs/redesign/examples/build_examples.py` are enough.
- Concepts are cheap and rough; polish only the approved one.
- Never redo old apps on your own; he picks the next app.
- Stuck after 3 rounds: stop, show the board, ask.

## 8. Report (Turkish, short)

```
Uygulama: <name> (<slug>)
Konsept: <A/B/C> - <one line>        Onay: <his words>
Teknikler: <thickness / material / top light / recess / hole / secondary object>
Kapı (gate): <N> PASS, <N> WARN, 0 FAIL
Zayıf yanlar: <honest>
Bakılacak: work/<slug>/review.png
```

## 9. Mistakes already made — do not repeat them

The full list with causes and fixes is [docs/MISTAKES.md](docs/MISTAKES.md) — read it
once per session. The ones that cost the owner most:

- **Floating / small icons**: a wide object centred in the canvas (Telegram envelope,
  bottom 107). → baseline rule in §5, `tools/size_audit.py`.
- **The owner uses the Symbol style**: an app without a Symbol shows its plate there
  (Duolingo); "make X the default" means the slot he sees — put it in Faithful AND
  Symbol, or ask which style he uses.
- **Change exactly what was asked**: "fix the paper plane on the stamp" is not "put the
  whole logo on the stamp".
- **Never rebuild "all apps" blindly**: a builder run over every app replaced hand-built
  icons in the pack; diff pixels before shipping (`work/_lib/builders.py`).
- **Colours must be the source's**: dark parts lost into a dark tile, gradients flattened,
  black gradients — `tools/region_check.py <slug>`.
- **Talk plainly**: he answered "Anlamadım" to questions full of internal terms (dry-run,
  appfilter, slot). Ask in Turkish, in phone words, one decision per question; never say
  "impossible" before researching (the in-app style switch was possible).
- **Look before you ask to ship**: unreviewed drafts were pushed ("the pushed icons are
  broken"); weak icons must be listed by you, not found by him.
- **Recognisable first**: concepts that drop the anchors (Aurex without its blue field,
  games as a generic ball/bolt/hat) were rejected outright ("hiç benzemiyorlar").
- **Do not keep asking**: "beni böyle ikide bir sorma" - two questions per app at most (§4).
- When the owner has to point out a new mistake, add it to docs/MISTAKES.md in the same PR.
