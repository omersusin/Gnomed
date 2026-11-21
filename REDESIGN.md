# REDESIGN.md — how a Gnomed icon is made (binding)

This is the **only** design document. AGENTS.md covers git, ComponentInfo, pack files and
tools; docs/MISTAKES.md is the history (read its §10 every session). `docs/course/` and
`CONTRIBUTING.md` are LEGACY (the old plate pipeline) — do not design with them.

## 1. The one rule

**A Gnomed icon is the app's idea built as a GNOME object — not the app's logo on a plate.**

![what a redesign is](docs/redesign/target.png)

Test: cover the plate/disc and the chin. If what is left is the original logo, it is not done.
The automatic builds (`build_auto.py`, the skill's autodrafts) only **measure** shapes and
colours; the gate FAILs them (`redesign`) until the app has `work/<slug>/redesign.py`.

Study before every app: [docs/redesign/gnome-objects.png](docs/redesign/gnome-objects.png)
(objects) and, for games, [docs/redesign/gnome-games.png](docs/redesign/gnome-games.png).

## 2. What the owner wants

- the real GNOME / Adwaita look; premium, made by a professional; every app its own idea
- the app recognisable at a glance: its 2–4 **anchors** survive (shape, colour field, accent,
  composition)
- **he uses the Symbol style**: every board shows Symbol first; an app is not done without
  a Symbol (§6)
- **not**: the logo with a shadow/emboss/chin; the logo inside a plate, disc or rim; every icon
  round; invented wrappers; toys; image-generation models of any kind

## 3. The concept ladder

| Level | What | GNOME examples |
|---|---|---|
| **L1** | the mark **becomes an object**: its silhouette gets thickness, material, light | Calls, Polari, *Kasa* example |
| **L2** | a GNOME **object that carries the mark** (the app's function as a thing) | Weather, FileRoller, Mousai, *Bulut* example |
| **L3** | **material tile** (glass, enamel, metal, paper with thickness) — only for pure wordmarks/abstract marks when L1/L2 fail | Meld, Tangram |

Wordmarks: letter shapes come from the source (`parts()`), never a font, never `<text>`.

### 3b. Games and characters

Owner: *"Oyunun resmini çizsin ama oyuncak gibi olmasın, ciddi bir iş olsun… simgesi
oyunu anlatsın."*

1. **References**: the store icon **plus at least 2 in-game screenshots** (from the owner —
   ask for them in Q1 if you have none — or the store page's screenshots if you can open
   them). Write in design.md what they show: number of characters, how they face each
   other, signature gear (boots, ball, hat), key object, colours.
2. **The icon tells the game**: its core scene with its own elements, simplified into 1–3
   GNOME objects. **Keep the composition and the count** — they are the identity
   (Kafa Topu 2 = two heads facing each other + their boots + the ball; Pokémon UNITE =
   three characters + the goal).
3. **Serious, not a toy**: realistic proportions, no big googly eyes, no cartoon outlines,
   no blob shapes; real materials (leather, rubber, metal, cloth, glass) with GNOME light
   and thickness; the HIG palette near the game's colours. Model: `docs/redesign/gnome-games.png`.
4. **Adapt, do not copy**: redraw from the references; never trace or paste the poster.
   Brand logos are never drawn from memory (AGENTS A2); for game characters the references
   above replace memory — never draw a character from memory alone.

## 4. Procedure — one app per session

```
1  MEASURE   python3 tools/new_redesign.py <slug>
             -> geometry.json, the parts as text, design.md, concepts/make_concepts.py
                (4 concept stubs A-D), redesign.py
2  STUDY     source.png + gnome-objects.png (+ gnome-games.png and the screenshots for a
             game, §3b). Fill design.md: anchors, function object, references.
3  CONCEPTS  FOUR different ideas A-D from the ladder in concepts/make_concepts.py (rough,
             flat is fine; shapes from parts()/fit(), never from memory), then
             python3 work/<slug>/concepts/make_concepts.py && python3 tools/concepts.py <slug>
             -> look at concepts.png yourself; replace any concept that is the logo on a
             plain disc or square.
4  Q1        the concept question (§7)                                    -> STOP, wait
5  BUILD     the main design + the kept ones in redesign.py; save_styles(§6);
             python3 tools/make_icon.py <slug>   (review + gate + phone preview)
             fix every FAIL (AGENTS.md I); look at work/<slug>/phone.png and review.png:
             same anchors? Symbol good on light AND dark? holes real? same size and
             baseline as the neighbours? at least 3 techniques of §5?
6  Q2        the final question (§7); "Şunu değiştir" -> change EXACTLY that, ask Q2 again
7  SHIP      only after "Tamam, pakete ekle":
             new app: python3 tools/pack_add.py <slug> --category <C>
             in the pack: python3 tools/pack_refresh.py <slug>
             then AGENTS.md C (audits, commit, push, PR)
```

## 5. Construction rules

- Canvas 128 × 128; the object inside 8…120; painted area about 45–65 %.
- **One baseline, one size**: free objects (every redesign, every Symbol) have their bottom
  edge (side included) at **116–120** (target 118) and their larger side ≥ 96; plates end at
  114–118, discs at 120–125. A wide, short object is made wider (≤ 112) and stands on the
  baseline — never centred and floating. Margins/outlines count in the size.
  Check: `python3 tools/size_audit.py`.
- **Holes are holes**: what is a hole in the source (letter counters, eyes, a ring's
  centre) is **transparent** in every free style — cut it (`body(slug)`, `difference`),
  never paint it white or in the tile colour. Exceptions only with the owner's words
  (`painted-holes:` in design.md) or the `painted_counters` override for white parts that
  are figure, not holes. Gate: `holes`.
- **Thickness**: 2 px thin parts/discs, 4–6 px flat objects, 8–24 px boxes/devices/cylinders.
- **Light from the top**: curved faces get a vertical gradient (top lighter); 1–1.5 px top
  light on upper edges (`toplight()`). **Recess** (screen, label, inlay): darker top inner
  wall (`recess()`). **Hole** (lens, slot): dark body, darker top wall (`hole()`).
- **Secondary object**: smaller, in front, bottom centre or lower right, with its own side.
- **Materials**: metal = Light 1–4, lighter middle on the side; glass = deep centre, rings,
  1–2 soft highlights; paper = Light 1–2; enamel/plastic = 3 steps of one ramp.
- No outer shadows, blur, filters, `<text>`, raster images, no pure black (`#241f31`).
  Details under 2 px vanish at 32 px.
- **Palette** (GNOME HIG): map the brand colour to the nearest ramp, keep its lightness;
  3 steps of one ramp per part (top light / face / side):

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

## 6. Style slots — every slot a different design

The pack has four slots (`faithful`, `disc`, `rimmed`, `symbol`); each is a separate APK.
Owner: *"her stil yuvası farklı olursa çok iyi olur"*.

1. The concept board shows **4 concepts** (A–D), four different ideas.
2. Q1 asks (a) the **main** design → it goes to **Symbol** (his style) and to every slot
   without a design of its own; (b) which others to **keep** (may be none) → they fill the
   other slots: the one closest to the original logo → **Faithful**, a round one → **Disc**,
   the next → **Rimmed**.
3. Polish only the main and the kept ones.
4. `save_styles(slug, {"symbol": main, "faithful": …, "disc": …, "rimmed": …})` writes
   every slot: missing slots get the main design, so an app already in the pack loses its
   old plate/disc/rim versions.
5. "Disc" and "Rimmed" are slot names — they do **not** mean "put the logo in a disc".

## 7. Questions and approvals — exactly two per app

**Q1 — concepts** (one AskUserQuestion call, Turkish, phone words, no jargon):
- the board path `work/<slug>/concepts.png`;
- question (a) main design: single choice A / B / C / D / "Hiçbiri, yeniden dene";
- question (b) keep: multiSelect of the other concepts (none is fine);
- a game without screenshots: ask for them here (§3b).

**Q2 — final**: the message names `work/<slug>/phone.png` (Symbol first, light + dark, phone
size among pack neighbours) and `review.png`, the `pack_add --dry-run` summary (new lines
only), and your honest weak points. Options: **"Tamam, pakete ekle"** (this answer IS the
pack approval) / "Şunu değiştir" (he types what) / "Konseptlere dön".

Everything else: decide yourself, write the decision and the reason in design.md, mention
it in Q2. No other questions.

**Approval lines quote him** — verbatim, in quotes, with the date; never written from a
general instruction (the gate checks the format):

```
approved: B - "<his answer to Q1 (a)>" (2026-11-21)
keep: A, D - "<his answer to Q1 (b)>" (2026-11-21)
final: "Tamam, pakete ekle" (2026-11-21)
shape-ok: "<his words>" (date)          only if a plain square/disc is really meant
painted-holes: "<his words>" (date)     only if a hole is really meant to be painted
```

## 8. Budget — he pays for every message

- **One app per session**, then `/clear`. Effort `high` for design, `medium` for git/docs.
- At session start read only: CLAUDE.md, this file, AGENTS.md, docs/MISTAKES.md §10, and the
  files the task names.
- Concepts are cheap and rough; polish only the chosen ones.
- Never rebuild the whole pack blindly: rebuild only what you changed, compare pixels with
  `git show HEAD:<png>`, keep only real changes. Never redo old apps on your own.

## 9. Report (Turkish, short)

```
Uygulama: <name> (<slug>)
Ana tasarım: <letter> → Symbol (+ <kept letters> → <slots>)     Onay: "<his words>"
Teknikler: <thickness / material / top light / recess / hole / secondary object>
Kapı (gate): <N> PASS, <N> WARN, 0 FAIL     Delikler: <source % -> transparent %>
Zayıf yanlar: <honest>
Bakılacak: work/<slug>/phone.png, work/<slug>/review.png
```

## 10. History

Every mistake so far with its fix: [docs/MISTAKES.md](docs/MISTAKES.md) — §10 (the owner's
decisions) every session, the rest when a topic comes up. When the owner has to point out a
new mistake, add it there in the same PR.
