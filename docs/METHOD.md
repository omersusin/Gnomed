# METHOD — how the group-4 icons were made (Claude, 2026-11-23)

The owner (2026-11-23), after group 4 (Duolingo, Reddit, F-Droid, Payload Dumper, Scene,
IconRequest): *"Sana yani senin yaptığın ikonlara hayran kaldım ... Diğer modellerin tıpkı senin gibi
yapmalarını sağlayabilir misin? ... ne düşündün de böyle sonuç çıkardın?"*

This file is that answer: the way of thinking, in the order it happened, with the real cases.
Read it before every app, together with REDESIGN.md. The steps of the pipeline (next.py, the
gates, the pack) stay as they are; this file is about **what to draw and why**.

> **Türkçe özet (sahip için):** Önce bakıyorum (logo + bütün ekran görüntüleri + açıklama + uygulamanın
> adı). Uygulamayı kullanan birinin her gün gördüğü 4 şeyi buluyorum. Her stile bunlardan BİRİNİ
> veriyorum ve her stilde ölçülmüş logoyu taşıyorum. Logoyu hiç ezberden çizmiyorum. Sonra çiziyorum,
> kontrol ettiriyorum, resme bakıyorum, düzeltiyorum.

---

## 0. The one idea

**Icon = the app's own logo (measured, never redrawn) + one thing from the app's own world.**
Four styles = four DIFFERENT things, each carrying the logo.

Not: four drawings of the logo. Not: four objects of the category (a stopwatch, a trophy, a book,
a globe could be any app). Not: the app's screen drawn small.

## 1. Look first — collect the app's own things

Before any code, open and really look at, in this order:

1. `work/<slug>/source.png` — the logo: its shape, its colours, what is in it (a robot, a box, a
   gear, eyes, a wrench).
2. `work/<slug>/refs/store/sheet.jpg` (all screenshots in one picture) and each `shot-N.jpg`.
3. `refs/store/store.json` — the store's one-line description.
4. **The app's name.**

Write down, for each, what a person who USES this app sees every day. These are the candidates:

| Where | What to look for | The real cases |
|---|---|---|
| the logo | the mark itself, its colours, things inside it | F-Droid: a robot in a box; Payload Dumper: a robot with a wrench and a screwdriver; Scene: a gear over the Android head |
| the screenshots' big words | the slogans on the store screenshots | Duolingo "keep your daily streak" → the streak flame; F-Droid "Find people nearby" → a radar; IconRequest "Select apps and share" → an envelope |
| the screens' signature parts | the buttons, bars, badges that only THIS app has | Reddit: the orange up-vote arrow, the comments bubble, the search bar with Snoo; IconRequest: "Health Status 99%" in yellow, the Health Check shield |
| what the screens show happening | the content | Duolingo: two lessons about ordering coffee → a coffee cup; Payload Dumper: partitions "31% - Extracting" → a progress dial |
| the app's name | read it literally | Payload **Dumper** → a dump truck tipping out the partitions |
| the description (no screenshots) | what the app does to the phone | Scene: "CPU/GPU frequency, temperature control, FPS" → a chip, a cooling fan, a gauge |

Keep 4-6 of them as **anchors** in design.md, each with its colour and where you saw it
(`- source.png`, `- refs/store/shot-3.jpg`). If a thing could belong to ANY app of the category, it
is not an anchor.

## 2. Choose four things — one per style

The assignment that worked every time:

| Style | What it is | Cases |
|---|---|---|
| **Faithful** | the logo ITSELF as a solid object: `put_mark(ic, SLUG, box, anchor="bottom", body=7, side=<darker brand colour>)`. Concept line: `B: the logo itself as a solid object - ...` | Duolingo: Duo's head; F-Droid: the robot on its box; Scene; IconRequest; Payload Dumper |
| **Symbol** (main) | the strongest thing of the app's own world, big, with the logo on or in front of it | Duolingo: the streak flame with Duo in front; Reddit: the up-vote arrow with Snoo printed on it; F-Droid: GNOME Software's shopping bag in F-Droid colours with the logo label; IconRequest: the request envelope with the logo as its stamp |
| **Disc** | a ROUND thing of the app's world, the logo in/on it | F-Droid: the Nearby radar; Reddit: the search lens; Scene: a cooling fan; Duolingo: the coffee cup seen from above; IconRequest: the "Health Status" dial |
| **Rimmed** | the fourth thing, with a clearly different silhouette | Reddit: the comments bubble; Scene: the gauge; F-Droid: a phone with "Update all"; IconRequest: the Health Check shield |

Before you draw, test the four ideas:

- **Four different silhouettes?** A bag and an open parcel are twin containers (F-Droid's parcel
  was replaced by a phone). Two discs with the logo are twins.
- **Cover the logo with your thumb: can you still name each thing?** (a flame, an arrow, a lens,
  a fan, an envelope, a shield: yes. "A tile with the logo": no.)
- **Is each one THIS app's?** Name the anchor it carries. "A globe" for Duolingo: no anchor → drop it.
- **Will it survive 32 px?** One bold thing beats a scene. A UI card (avatar + text lines + photo +
  buttons) or a list on a clipboard **always** failed legibility (0.63-0.71); take ONE element of
  that screen instead (the comments bubble, the shield).
- **Round thing ≠ the logo on a plain disc.** A disc needs a reason to be round (a lens, a dial, a
  fan, a cup) and something that breaks the circle (a handle, a saucer, ticks).

## 3. The logo — measured, never drawn

1. **First render the measured mark alone and LOOK at it** — before any design:
   ```
   python3 - <<'EOF'
   import sys; sys.path.insert(0, "work/_lib")
   import obj as O, cairosvg
   for n, g, f in O.mark_parts("SLUG"): print(n, [round(v) for v in g.bounds], f)
   ic = O.gk.Icon("m"); O.put_mark(ic, "SLUG", (14, 14, 114, 114)); ic.save("/tmp/m.svg")
   cairosvg.svg2png(url="/tmp/m.svg", write_to="/tmp/m.png", output_width=256, output_height=256, background_color="#f6f5f4")
   EOF
   ```
2. If it is wrong, fix the **measurement** in `work/<slug>/geometry.json` → `info.ground`
   (never draw the logo yourself):
   - a part missing (its colour is close to the tile: Duo's light-green head) → `"mark_keep": ["r0"]`
   - a part cut straight by the tile edge (Duo's head ran off the tile) → `"mark_round": 10`
   - several things measured as one muddy region (Payload Dumper's wrench + screwdriver + the
     robot's rim) → `"mark_split": {"r1": [[x0, y0, x1, y1, "#hex"], ...]}`
   - a face's eyes are see-through holes (Snoo's orange eyes) → `"mark_hole_fill": "#hex"` and in
     design.md `painted-holes: "Logodaki gibi boya" (2026-11-23)`
3. A mascot or a face that IS the logo (Duo, Snoo, a robot) is the logo: it goes on every style.
   Never `mark: none` without the owner's words.
4. Where the logo sits:
   - **on a light part** (a white label, a stamp, paper, a hub, a dial) **in its own colours** —
     the clearest (F-Droid bag label, IconRequest stamp, Scene fan hub);
   - **on a part in the brand colour** when the logo is white (Snoo on the orange arrow / bubble);
   - `face="#ffffff"` only on dark parts;
   - **a white or black logo standing free melts** into one of the two wallpapers: give it a part
     behind it in the brand colour (Reddit's Faithful = a die-cut sticker with an orange margin), or
     a mid-grey face with a lighter side (ChatGPT's knot).
5. Size ≥ 36 px of 128 (Faithful ≥ 44). Box INSIDE its part with ≥ 1 unit of room. Nothing drawn
   over it after it (holes, handles, needles go elsewhere). A CD's hole never crosses the letters.

## 4. Drawing — what made them look good

- **One big object fills 8..120**; a secondary thing overlaps it (Duo in front of the flame, the
  needle over the dial). Leave the canvas edge alone: 8 units on every side.
- **Brand colours come from the source** (measured hex), materials from GNOME ramps: steel
  (`#ffffff → #deddda → #9a9996`), paper, wood, dark plastic (`#5e5c64 → #3d3846`). A gradient
  light at the top, darker at the bottom; `depth` 3-8 with a darker side.
- **Few parts, all bold.** Lines ≥ 2.5 units thick, gaps ≥ 2.5 units. Remove what cannot be seen at
  48 px: text lines, small icons on a card, thin rings, a dark case with a bezel around a light
  dial (Scene's gauge: legibility 0.70 → 0.77 when the case went).
- **Both wallpapers:** a dark object (a navy truck) disappears on the dark wallpaper; a white one
  (an envelope, a white head) on the light one — the Symbol must read on BOTH: colour it (the
  envelope became IconRequest green).
- **Never `rounded(g, r)` with r ≥ half the part's thinnest side** — it shrinks now, but the shape
  you get is a pill.
- Reuse what exists: `put_mark`, `solid`, `recess`, `football`, `sun`, the helpers in
  `work/_lib/objects.py`; copy a worked example: `work/reddit/redesign.py`,
  `work/duolingo/redesign.py`, `work/scene/redesign.py`, `work/f_droid/redesign.py`.

## 5. The loop — measure, then LOOK

```
python3 work/<slug>/redesign.py                         # writes the 4 SVGs
python3 tools/make_icon.py <slug>                        # build + the gate
python3 tools/overview.py <slug> --out /tmp/<slug>.png   # LOOK at it: logo + screenshots + 4 styles, light + dark
```
Fix every FAIL and every must-fix WARN (next.py says which), then look again. What the gate said
in group 4 and what fixed it:

| Gate said | What it really was | Fix |
|---|---|---|
| `mark` contrast 2 | white Snoo on the light wallpaper | a brand-coloured part behind it |
| `mark_fit` room 0.5 | the logo touched its label / window / bow | a smaller box or a bigger part |
| `mark_fit` over the edge 30 % | rings / spirals drawn under the logo cut its "part" in pieces | stop the rings where the logo is printed |
| `legibility32` 0.63 | a post card with avatar, lines, photo, buttons | one bold thing instead (the bubble) |
| `empty_layer` | `rounded()` erased a pill / a `difference` left nothing | fix the geometry |
| `same_object` on the Faithful | the logo's own gear/wrench matched a keyword | write the line as "the logo itself ..." |
| `visible_light` 0.29 | a white envelope as the Symbol | colour it |

Then the **owner's eye** — answer each with yes, or redraw:
1. Can I name each of the four in two words? (the streak flame, the search lens ...)
2. Would a user of THIS app recognise it without the name? (the logo is on all four)
3. Are the four silhouettes different? Different dominant colours?
4. Is anything touching, crossing or covering the logo?
5. At 48 px (the phone row of the overview), is every part still there?

## 6. Special cases

- **Games** (REDESIGN §3b): the same looking-first; characters only when they ARE the game (Kafa
  Topu 2: the two big heads - Symbol a header, Faithful the store icon, Disc the round pitch,
  Rimmed the fireball goal of a screenshot). Otherwise the game's own objects, from ITS screenshots.
- **The phone's own apps** (Ayarlar, Saat, Kamera, Telefon, Mesajlar, Kişiler, Hesap Makinesi,
  Hava Durumu, Fotoğraflar - `SYSTEM_APPS`): no logo to carry; GNOME's own app for the same job is
  the model (Settings, Clocks, Snapshot, Calls, Chatty, Contacts, Calculator, Weather, Loupe), and
  the phone app's screenshots give the anchors (its colours, its signature screen).
- **A redo** (`redo:` line, next.py REDO): `--start-redo` archives the old design; read the old
  concepts (`concepts-round*/`) and the archive only to NOT repeat them; start again at §1.
  The owner (2026-11-23) wants every icon Claude did not draw redone this way: 26 apps carry his
  `redo:` line (next.py lists them under "2. The owner asked for a redo").

## 7. Without repository tools (a chat model)

The owner can test a model in a chat (claude.ai, any app) with a bundle:
`python3 tools/chat_bundle.py <slug>` → `~/Downloads/gnomed/<slug>-chat.zip`. It holds this file,
the app's logo, screenshots and measurement, the drawing library, the gate and three worked
examples, plus `CHAT.md` (the steps). The chat model unzips it, installs the Python packages,
writes `work/<slug>/redesign.py` + `design.md`, runs the gate and the overview itself, and returns
those two files. The owner (or DeepSeek) copies them into the repository and runs
`python3 tools/make_icon.py <slug>` and `python3 tools/next.py <slug>` as usual.
