# PLAYBOOK — every step from A to Z (for small models)

Read **only the section `tools/next.py` names** (`DETAILS docs/PLAYBOOK.md#<state>`). Every
section: the goal, the exact commands, a filled-in example, "if this fails", common mistakes
(from [MISTAKES.md](MISTAKES.md)), and when to stop and ask the owner.

Worked examples from source to the pack: [playbook/telegram.md](playbook/telegram.md),
[playbook/aurex_browser.md](playbook/aurex_browser.md), [playbook/pokemon_unite.md](playbook/pokemon_unite.md),
[playbook/rush_royale.md](playbook/rush_royale.md). Decision tables and question templates are at
the end: [tables](#decision-tables), [questions](#question-templates).

All commands run from the repository root. `<slug>` = the app's folder name in `work/`.

---

## on-main

**Goal:** never work on `main` (it is the owner's).
```
git config core.hooksPath tools/hooks
git switch -c icons/<slug>
```
If this fails: the branch exists → `git switch icons/<slug>`. Never `--force`, never push to main.

## no-source

**Goal:** `work/<slug>/source.png` (the app's icon) + its ComponentInfo from the owner's phone.
```
python3 tools/import_request.py <zip | folder | request.txt>        # lists the apps it contains
python3 tools/import_request.py <same> --add --only <slug>
# or, with a PNG and a ComponentInfo copied from his request / phone:
python3 tools/add_source.py <slug> <icon.png> "<Label>" "ComponentInfo{pkg/pkg.Activity}"
```
Example: `python3 tools/add_source.py telegram ~/telegram.png "Telegram" "ComponentInfo{org.telegram.messenger/org.telegram.messenger.DefaultIcon}"`

| If this fails | Do |
|---|---|
| `NO-ICON` / `BAD` / nothing in `requests/inbox/` | ask the owner (Turkish): "Bu uygulamanın simgesini Gnomed'in İstek ekranından (Görsel + metin olarak paylaş) gönderebilir misin?" |
| no ComponentInfo | ask him to run on his rooted phone: `su -c 'cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>'` |
| the slug has `_un_te`-like junk | Turkish letters: use the transliterated slug (`pokemon_unite`) |

Mistakes: a guessed ComponentInfo never shows the icon (AGENTS.md A3); a blurry 192 px icon is
not final — ask for a sharp copy (BCR).
Stop and ask: when there is no icon or no ComponentInfo. Never invent either.

## not-started

**Goal:** measure the source and create the design files.
```
python3 tools/new_redesign.py <slug>
```
It writes `geometry.json` (the measured colour parts), `design.md`, `concepts/make_concepts.py`,
`redesign.py`, and prints the parts as text. Nothing that exists is overwritten.

If it prints `WARNING ... POSTER`: the source is game art → it is a game (`kind: game`, §3b).
If this fails with `ModuleNotFoundError`: `python3 -m pip install -r tools/gnome-android-icons/requirements.txt`
(`--break-system-packages` if pip refuses), then run `python3 tools/gnome-android-icons/scripts/doctor.py`.

## references

**Goal:** know what the app is and shows before drawing anything — any model, with or without vision.
```
python3 tools/fetch_refs.py <slug>                    # package + name from the pack / the request
python3 tools/fetch_refs.py <slug> --url <page>       # a page the owner names (GitHub, Telegram channel, site)
```
It searches, in order: **system app** (com.android.* → the GNOME app for the same job, no screenshots
needed) → **Google Play** (US, then TR, IN, GB, DE for region-locked apps) → **F-Droid** →
**IzzyOnDroid** → **Uptodown** (its page for the app's name, accepted only when the page shows the
same package) → **GitHub** (repository search; accepted when the package is in the repository's
gradle files / manifest — a README mention is marked NOT VERIFIED). Real store screenshots win over
README pictures. APKMirror / APKPure block scripts (HTTP 403).

It saves `work/<slug>/refs/store/` (screenshots, the store icon, `sheet.jpg`, `store.json` with every
place it searched — not in git: store images are not ours), writes `category:` and `store:` into
design.md, and prints the title, the description, the screenshots' main colours with GNOME names and
the category's object family — as TEXT, so a model without vision can use it. A category guessed
from words is marked "guessed - check it". The store `icon.png` is often sharper than the phone
export: if `source.png` is small or blurry, say so in Q1 and offer it.

Tested on the owner's 92 apps (2026-11-22): Play + F-Droid alone gave screenshots for 59; with the
other places **78** (exteraless, MiX, MT Manager: Uptodown; BCR, KonaBess, Mochy, Recon, Quarry:
GitHub; TikTok Lite: Play TR), 8 more with text only (their repository has no screenshots), 3 system
apps (no screenshots needed), 3 nothing (closed apps from a website, his own test builds).

| If this fails | Do |
|---|---|
| `nothing found` | Q1 asks the owner where he got it (a site, a Telegram channel) → `--url <it>`; or for 2–3 screenshots → `work/<slug>/refs/` |
| GitHub `403` / rate limit | without a token GitHub allows 60 requests an hour: `export GITHUB_TOKEN=<token>` or `gh auth login` |
| wrong app (NOT VERIFIED, other title) | `--url <the right page>` or `--package <the real package>` with `--force` |
| no network in your tool | the owner runs it on his PC, or sends screenshots; never invent what the app looks like |
| screenshots from the phone | USB debugging: `adb exec-out screencap -p > work/<slug>/refs/phone-1.png`; rooted: `su -c 'screencap -p /sdcard/s.png'` |

## fill-design

**Goal:** write in `work/<slug>/design.md` what makes the app recognisable and what it does.
Fill (example = Telegram):
```
kind: app
ladder: L2 - an envelope carries the paper plane on its stamp     (may be filled after Q1)
characters: no
anchors (2-4 things that make the app recognisable; they must survive):
  1. the white paper plane (measured from source.png: tip right-top, notch under the wing)
  2. Telegram blue #31a5df (between HIG Blue 2 and 3)
  3. the round shape (the blue circle)
function object (what the app does, as a physical thing): a message flying off - paper plane / envelope
```
Game example (Rush Royale): `kind: game`; anchors: the purple wizard hat, the gold crown band with
the magenta gem, the ice-blue crystals; function object: the hat as a game piece on the board.

**The measured parts** (`parts(slug)`, listed by `describe(slug)`): `r0`, `r1`, … are the colour
regions (`r0` is often the background tile/circle — leave it out of the object); `holes` is what
the mark ENCLOSES — a letter's counter (a real hole), or a figure inside a ring (Telegram's white
plane sits inside the blue circle, so it is measured as `holes`). Decide which by its colour and
box in `describe()`; write it in design.md (e.g. `figure: holes = the white plane`).

How to find the facts without seeing the image:
```
python3 tools/describe_icon.py work/<slug>/source.png
python3 -c "import sys; sys.path.insert(0,'work/_lib'); from obj import describe; print(describe('<slug>'))"
```
Choose the object with the [decision table](#decision-tables) and [OBJECTS.md](redesign/OBJECTS.md).
No object fits? Then **L1** (the mark itself as a thick object) or compose one from the primitives
(`rounded`, `poly`, `circ`, `ellipse` + `solid`) and write why in design.md. **Never** fall back to
"the logo on a plain tile/square or disc" — that is the old pack the owner wants replaced.
L3 (a material tile) is only for a pure wordmark (letters only) when L1 and L2 fail.
Mistakes: an anchor dropped (Aurex without its blue field → "hiç benzemiyor"); an invented
wrapper unrelated to the app (YouTube in a TV); games with characters (forbidden, §3b).
A game needs **≥ 2 in-game screenshots** in `work/<slug>/refs/` — if you have none, Q1 asks for them.

## draw-concepts

**Goal:** FOUR different rough ideas A–D in `work/<slug>/concepts/make_concepts.py`.
Rules: four *different* ideas from the ladder (REDESIGN.md §3); the app's mark always from the
source (`parts()` / `body()` / `fit()`), never from memory; ready objects from `objects.py`;
rough is fine; stand on the baseline (`base=118`). **No concept may be the logo on a plain
tile/square or disc** — `next.py` warns when one looks like it.

`new_redesign.py` already wrote the file with four example functions (A = L1 the mark as an
object, B = an envelope carrying the mark, C, D) — replace their bodies with your ideas. A
filled-in example (Telegram; its figure is the `holes` part):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from objects import *                      # objects.py + obj.py (gk, solid, parts, body, fit ...)
OUT = Path(__file__).resolve().parent
SLUG = "telegram"
P = parts(SLUG)                            # the measured parts; print(describe(SLUG)) lists them
FIGURE = P["holes"]                        # Telegram: the white paper plane is the "holes" part.
                                           # Use the FIGURE, not body(SLUG): body() of a logo on a
                                           # circle IS a disc - "the logo on a disc" is rejected.

def A():                                   # L1: the figure itself as a thick white object
    ic = gk.Icon("A")
    (mark,) = fit([FIGURE], (14, 20, 114, 112), anchor="bottom")
    solid(ic, mark, face=[(0, "#ffffff"), (1, "#deddda")], depth=6, side="#9a9996")
    return ic

def B():                                   # L2: an object that carries the figure (on its stamp)
    ic = gk.Icon("B")
    envelope(ic, 64, 118, 108, ramp=RAMP["Blue"])
    (mark,) = fit([FIGURE], envelope_stamp(64, 118, 108))
    solid(ic, mark, face=RAMP["Blue"][2], depth=0, top=False)
    return ic

# C(), D(): two more DIFFERENT ideas (another object, a round one, a material tile ...)

if __name__ == "__main__":
    for name, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        fn().save(OUT / f"{name}.svg")
```
```
python3 work/<slug>/concepts/make_concepts.py
```
Then one line per concept in design.md (`  A: the mark as a thick blue object`, …).
Game example: [pokemon_unite concepts](../work/pokemon_unite/concepts/make_concepts.py) (objects only).

| If this fails | Do |
|---|---|
| `KeyError` in `parts()` | the part names are in `describe(slug)` (r0, r1, …, holes) |
| an object is cut off / floats | `size` smaller; `base=118`; check with `describe_icon.py` |
| empty SVG | you drew nothing on `ic`, or a shape is empty (`rounded()` radius ≥ half the width erases it) |

Mistakes: concepts that are "the logo on a disc/square" (rejected every time); generic objects
unrelated to the app (games round 1); traced poster blobs (games round 2).

## board

**Goal:** the concept board the owner looks at.
```
python3 tools/concepts.py <slug>          # -> work/<slug>/concepts.png
```
Without vision: `python3 tools/describe_icon.py work/<slug>/concepts/A.svg` (B, C, D) — each must be
an object of its own, not the source logo on a plain disc or square; inside 8..120; bottom ≈ 118.

## ask-q1

**Goal:** the owner picks the main design (→ Symbol) and the ones to keep (→ other slots).
`next.py` prints the exact Turkish text. Send it, then **stop and wait**.
Write his answers verbatim (the gate checks quotes + date):
```
approved: B - "B" (2026-11-21)
keep: A - "A,A'daki halkanın içindeki mavi hilali kaldır." (2026-11-21)
```
- "Hiçbiri, yeniden dene" → move `concepts/` to `concepts-round<N>/`, draw 4 new ones, Q1 again.
- Every option + "Sen karar ver" → keep all, choose the slot order yourself, say it in Q2 (§0.4).
- A change request inside his answer ("…mavi hilali kaldır") → do exactly that in the build and
  write it under `decisions` in design.md.
- Slots for kept ones: closest to the original → faithful; a round one → disc; the next → rimmed.
Mistakes: writing `approved:` yourself ("beni sorma" ≠ approve for me); asking more than Q1/Q2.

## redo

**Goal:** an app the owner approved before must be redone (a `redo:` line with his words).
```
python3 tools/next.py <slug> --start-redo
```
It moves `concepts/` + `concepts.png` to `concepts-round<N>/`, keeps the old approval lines as
`history-…:` and empties `approved:/keep:/final:`, renames `redo:` → `redo-started:`. The pack is
not touched (his old icon stays until the new one is approved). Then update design.md for the
new rule (e.g. Kafa Topu 2: `characters: no`, anchors = the ball and the boot) and continue.

## owner-fix

**Goal:** the owner looked at an overview and wrote what is wrong; do exactly that, nothing else.
His review lives in the repository — `work/<slug>/fixes.md` — not in a chat message (owner,
2026-11-22: *"Bıktım bana prompt vermenden, yaz depoya"*):
```
# apple_music - fixes (the owner's review of ara-2)
group: ara-2
owner: "Bıktım bana prompt vermenden, yaz depoya" (2026-11-22)
shown:

- [ ] disc: the microphone/record mix is odd - a round object you can name, the note on it
```
1. `next.py <slug>` prints the open lines (state OWNER_FIX). Change only those styles in
   `redesign.py`; `all:` = every style. Then `make_icon.py <slug>`.
2. Done = ticked **and** what it is now: `- [x] disc: … -> now: a red speaker with the note`.
   A tick without `-> now:` is still open.
3. While any app has open lines, `next.py <other app>` says OWNER_FIXES_FIRST.
4. When every app of the group is done, `next.py` (no slug) prints the overview command for
   only those apps; push, write `shown: <date>` in their fixes.md, send him the path, wait.

## build

**Goal:** the approved concept (and the kept ones) as finished GNOME objects + review images.
1. Copy the approved function from `concepts/make_concepts.py` into `work/<slug>/redesign.py`
   (and the kept ones). redesign.py must `from objects import *` (as the concepts file does) to
   use the ready objects. Polish: thickness, light from the top, a secondary object (REDESIGN.md §5).
   A mark printed on a white/light surface (label, stamp, page) must be in a strong colour (the
   brand colour) — a white mark on a white label vanishes.
2. End with `save_styles(SLUG, {"symbol": main(), "faithful": …, "disc": …, "rimmed": …})`;
   a slot you leave out gets the main design. Write the slots into design.md `styles:`.
3. Build:
```
python3 tools/make_icon.py <slug>     # -> <slug>-<style>.svg, review.png, phone.png, the gate
```
Annotated examples: [telegram](playbook/telegram.md) (mark on an envelope stamp),
[aurex_browser](playbook/aurex_browser.md) (mark on a window page),
[pokemon_unite](playbook/pokemon_unite.md) / [rush_royale](playbook/rush_royale.md) (game objects).

| If this fails | Do |
|---|---|
| `SystemExit: copy the approved concept here` | the template line is still in redesign.py — replace the function body |
| `STATE BUILD` again with "does not write a Symbol" | `save_styles` must get `"symbol"` |
| size_audit `floats` / `small` / `touches edge` | `base=118`, larger side ≥ 96, inside 8..120 |

## fix-fail

**Goal:** zero FAIL in `python3 tools/check_icon.py <slug>`. Never ask Q2 with a FAIL.
`next.py` prints the recipe of each FAIL. All recipes:

| check | means | fix |
|---|---|---|
| `redesign` | `approved:` empty or not a quote + date | ask Q1; write his words in quotes + date |
| `holes` | a hole of the source is painted | cut it: `body(slug)` or `g.difference(hole)`. A PASS "(the mark sits ON an object)" is right: a stamp/page/label shows through the mark's holes — do not cut through that object |
| `plain_shape` FAIL (disc) / WARN (tile, box) | the silhouette is a plain disc / square tile | make the app's object (objects.py); a real square object (window, calendar) may stay — say so in Q2 |
| `lint` | `<text>`, raster, filter, or touching the edge | only obj/objects shapes, inside 8..120 |
| `visible_light` / `visible_dark` (WARN < 0.55, FAIL < 0.25) | vanishes on a light / dark wallpaper | darker side (ramp 4–5) / lighter face (ramp 1–3) |
| `legibility32` | details vanish at 32 px | fewer, bigger parts; strokes ≥ 2 px |
| `faithful` | no Faithful SVG | `save_styles` writes all slots |
| `mass` (WARN, < 0.35) | the icon looks thin | object +10–15 %, taller, or a secondary object. A TALL thin object (bottle) cannot grow: add a secondary object in front at the lower right (e.g. `water_drop`), or choose a wider object |
| `baseline` (WARN) | not on the line | the bottom incl. side at 118 |
| `mark_size` (WARN, fixed before Q2) | the app's own mark/colours are < 36 px of 128 | [fix-warn](#fix-warn) |
| `bands` | a gradient of the source is painted as flat bands (looks melted) | [gradients](#gradients): `regions(slug)` / `gradient(slug, shape)` |
Then `python3 tools/make_icon.py <slug>` again.

## gradients

**Goal:** a gradient of the source stays ONE smooth gradient — never flat bands.
The measurement (`geometry.json`) cuts every gradient into 2–5 flat colours (`r1`, `r2` … in
near colours). Drawn one by one with `colour()` they look **melted/broken** (Deezer, 2026-11-22).
`print(describe(slug))` lists them as `GRADIENT: r1, r2 are bands of ONE gradient`.

```python
R = regions(SLUG)                 # [(name, shape, fill)] - "r1+r2" = bands merged, fill = Grad
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]
for g, f in zip(fit(MARK, (14, 12, 114, 112), anchor="bottom"), COL):
    solid(ic, g, face=f, depth=6)  # solid/recess/cutout paint a Grad as a real SVG gradient

face = gradient(SLUG, P["r2"])    # the source's gradient under any shape (also a union of parts)
face = Grad([(0, "#ffa348"), (1, "#e01b24")], angle=90)   # your own: 90 = top->bottom, 0 = left->right
pieces = traced(SLUG, box_)       # posters: gradients=True (default) keeps them as Grad
```

| If this fails | Do |
|---|---|
| gate `bands` FAIL | you painted two bands flat: replace `colour(SLUG, "rN")` per band by the `regions()` fill |
| the gradient is gone (flat) | you used `ic.path(d, fill)`: a `Grad` there paints only its middle colour — use `solid()`/`recess()` |
| two really different colours got merged | draw them from `parts()` + `colour()` instead, and say so in Q2 |

## fix-warn

**Goal:** fix the WARNs the owner would notice on his phone **before** Q2 — he is not the
reviewer of things a check can see (owner, 2026-11-22: *"ikide bir bana mesaj verip bunu, şunu,
onu mu düzelteceksin?"*). `next.py` stops here for `mark`, `mark_size`, `visible_light`,
`visible_dark`, `legibility32`, `slots`, `same_object`.

| WARN | Do |
|---|---|
| `mark` | the app's mark is missing / small / melts in / not the source's shape. Draw the MEASURED mark on the object: `put_mark(ic, SLUG, box, face="#ffffff")` (on a label, screen, lid, stamp, page), or the mark as the object: `put_mark(ic, SLUG, (14, 12, 114, 112), depth=6, anchor="bottom")`. ≥ 36 px (Faithful ≥ 44), white on dark parts, dark/strong colour on light parts. Hand-drawn? wrap it in `with ic.group("mark"):` — the gate only finds layers named `mark` |
| `same_object` | another app of the category has this object in some style: take a FREE one from the family (`next.py <slug>` in FILL_DESIGN/DRAW_CONCEPTS lists USED/free; or `python3 -c "import sys; sys.path.insert(0,'work/_lib'); import categories; print(categories.suggest('<slug>'))"`) |
| `mark_size` | make the part that carries the mark bigger (record label, cassette label, stamp, screen, page) and `fit()` the mark into ≥ 36 px of 128; drop decoration that takes its room. Ready boxes keep it: `record_label()`, `cassette_label()`, `speaker_badge()`, `envelope_stamp()`, `bottle_label()` |
| `visible_dark` | a dark object vanishes on a dark wallpaper: a light rim / top light, or lighter ramp steps (1–3) for its face |
| `visible_light` | a pale object vanishes on a light wallpaper: a darker side (ramp 4–5) or a darker secondary object |
| `legibility32` | fewer, bigger parts; strokes ≥ 2 px; drop tiny details |
| `slots` | the 4 styles repeat a design: build the kept concepts and `save_styles(SLUG, {"symbol": main, "faithful": closest-to-logo, "disc": round, "rimmed": rest})` (REDESIGN.md §6) |

Tried and a real fix would break the approved design? Write ONE line per check in design.md —
`warn-ok: mark_size - <why, one plain sentence>` — the owner reads it in Q2. Never write it
without trying first.

## ask-q2

**Goal:** the owner sees the result (phone.png, review.png) and approves it for the pack.
`next.py` prints the Turkish text with the pass/warn counts and the WARNs in plain words. Replace
`<SENİN DÜRÜST NOTLARIN - bunu değiştir>` with your own honest weak points (never hide one; without
vision say "Resimleri göremiyorum; ölçümlere göre: …"). Run the dry-run it names; tell him only what changes on
his phone (new icon / which replaces which / nothing deleted) — no jargon.
- "Tamam, pakete ekle" → `final: "Tamam, pakete ekle" (2026-11-21)` → next state PACK.
- "Şunu değiştir …" → change **exactly** that, quote it under `decisions`, `make_icon`, Q2 again.
- "Konseptlere dön" → `concepts-round<N>/`, new concepts, Q1 again.
Mistakes: publishing icons he has not seen ("The pushed icons are broken"); hiding a WARN.

## pack

**Goal:** the approved icons into the pack — only after "Tamam, pakete ekle".
```
python3 tools/pack_add.py <slug> --category <Category> --dry-run    # new app or new slots: read it
python3 tools/pack_add.py <slug> --category <Category>
python3 tools/pack_refresh.py <slug>                                # app already in the pack
python3 tools/gnome-android-icons/scripts/pack_audit.py --project .   # no ERROR line with <slug>
python3 tools/size_audit.py                                           # 0 icon(s) outside
python3 tools/check_icon.py <slug>                                    # 0 FAIL
```
An app already in the pack but without Disc/Rimmed/Symbol slots needs `pack_add` (adds the
`_alt1/_alt2/_alt3` slots) **and** `pack_refresh` (re-renders the main icon). Category: `next.py`
fills in the app's current one; for a new app it lists them (Security, Social, Media, System, AI,
Tools, Browsers, Finance, Weather, Games, Education, Shopping) — pick the closest and name it in Q2
(`Telefonuna: … kategori: X`). A new category only when the owner asks for one.
Mistakes: hand-editing XML/PNG (forbidden); `pack_refresh` on the whole pack (rebuild only yours).

## log

**Goal:** one entry at the END of [LOG.md](LOG.md) (append-only; `pr_guard` checks it).
```
## 2026-11-22 — DeepSeek V4 via OpenCode — `kafa_topu_2`
- What: redone with objects only: B (ball + boot) -> Symbol, A -> Faithful
- Why: the owner's redo ("Evet, yeni oturumda", 2026-11-21)
- Owner: approved B - "B" / keep A - "A" / final "Tamam, pakete ekle" (2026-11-22)
- PR: opened after this commit
- Open problems: the boot is small at 32 px (WARN legibility32)
```

## commit

```
git add -A
git commit -m "<slug>: <what> - owner: \"Tamam, pakete ekle\""
```
Never on main, never `[release]`, never `--no-verify`.

## push

```
python3 tools/pr_guard.py              # 0 ERROR
git push -u origin <your branch>
```
Open ONE pull request to `main` with the REDESIGN.md §9 report in Turkish; give the owner the link.
Never merge it yourself. If the push is rejected: `git pull --no-rebase origin <branch>`, push again.

## done

The app is finished. If the PR is not open yet, open it. Next app: a NEW session (`/clear`),
`python3 tools/next.py` (no slug) lists what is next; the owner chooses among the plate apps.

---

## Decision tables

### App type → ladder level and typical object (objects.py function)

The full table with every category and which apps already use which object:
[docs/redesign/CATEGORIES.md](redesign/CATEGORIES.md) (`tools/next.py` prints the part you need).

| App type | Ladder | Typical object |
|---|---|---|
| messenger, SMS | L2 | `speech_bubble`, `envelope` (mark on the stamp), `paper_plane` |
| mail | L2 | `envelope` |
| browser | L2 | `browser_window` (mark on the page), `globe` |
| bank, wallet, payments | L2 | `card`, `coin` |
| crypto / exchange | L2 | `coin` with the mark |
| password, 2FA, VPN, security | L2 | `shield`, `lock`, `key` |
| settings, system, root tools | L2 | `gear` |
| files, backup, cloud storage | L2 | `folder`, `cloud` |
| camera, scanner, gallery | L2 | `camera_lens` |
| video, media player | L1 / L2 | `play_button` |
| music, audio, equaliser | L2 | `vinyl_record` (mark on `record_label`), `cassette` (`cassette_label`), `speaker` (`speaker_badge`), `headphones`, `music_note` — a different one per app |
| reading, docs, learning | L2 | `book` |
| phone, dialer | L1 | `phone_handset` |
| calendar, planner | L2 | `calendar_page` |
| battery, power | L2 | `battery` |
| weather | L2 | `cloud` (+ a sun disc) |
| a strong geometric mark (letter, emblem) | L1 | the mark itself (`body(slug)`) with thickness |
| water, hydration, drinks | L2 | `water_drop`, `bottle` (mark on `bottle_label`), `mug` |
| health, fitness tracker | L1 / L2 | the mark as an object, or `water_drop` / `battery`-like gauge |
| shop, marketplace | L2 | `shopping_bag` (mark on `bag_front`) |
| a pure wordmark that fails L1/L2 | L3 | a material tile (enamel/metal/glass) with the letters from `parts()` |
| nothing fits | L1 | the mark itself as a thick object; or compose from primitives — never a plain tile/disc |
| **game** | game objects | 1–3 of its objects: `goal_ring`, `energy_ball`, `wizard_hat`, `crystal`, `football`, `team_ball`, `die`, `board_tiles` — never characters |

### Brand colour → GNOME HIG ramp (keep the lightness: light brand → steps 1–2, dark → 4–5)

| Brand colour (hue) | Ramp | Steps (1 light … 5 dark) |
|---|---|---|
| blue, cyan (190–250°) | Blue | #99c1f1 #62a0ea #3584e4 #1c71d8 #1a5fb4 |
| green, teal (90–170°) | Green | #8ff0a4 #57e389 #33d17a #2ec27e #26a269 |
| yellow, gold (45–65°) | Yellow | #f9f06b #f8e45c #f6d32d #f5c211 #e5a50a |
| orange (20–45°) | Orange | #ffbe6f #ffa348 #ff7800 #e66100 #c64600 |
| red, pink-red (345–20°) | Red | #f66151 #ed333b #e01b24 #c01c28 #a51d2d |
| purple, violet, magenta (260–330°) | Purple | #dc8add #c061cb #9141ac #813d9c #613583 |
| brown, wood, leather | Brown | #cdab8f #b5835a #986a44 #865e3c #63452c |
| white, grey, metal | Light | #ffffff #f6f5f4 #deddda #c0bfbc #9a9996 |
| black, charcoal | Dark | #77767b #5e5c64 #3d3846 #241f31 (never #000) |

`describe_icon.py` prints the nearest HIG colour of every main colour. Keep a brand colour that has
no HIG match only when it is an anchor (Rush Royale's magenta gem: the owner asked for it).

### "The owner said X" → what it means (REDESIGN.md §0)

| He says | It means |
|---|---|
| "varsayılan", "default" | the icon he sees = the **Symbol** style |
| "Tamam, pakete ekle" | Q2 approval: pack it (the only pack approval) |
| "Şunu değiştir: …" | change exactly that, ask Q2 again |
| "Hiçbiri, yeniden dene" | four new concepts, Q1 again |
| "Sen karar ver" (with every option) | keep all; you choose the slot order and show it in Q2 |
| "Beni sorma", "ikide bir sorma" | fewer questions — still Q1 and Q2; never approve for him |
| "Anlamadım" | your question had jargon: ask again in phone words |
| "Mümkün, yapanları görüyorum" | research and find the way; do not repeat "impossible" |
| a strange word in a sentence | voice typing: read it from the context (Oyunu öğren = A'nın) |
| "%10 büyüt" | the painted size +10 % (mass up), staying inside 8..120 on the baseline |

---

## Question templates

### Q1 — with AskUserQuestion (Claude Code)
One call, two questions:
- "<App>: 4 fikir (resim: work/<slug>/concepts.png). A: …, B: …, C: …, D: …. Telefonunda göreceğin
  ana simge hangisi olsun?" — options A, B, C, D (single choice; "Hiçbiri, yeniden dene" is typed in "Other").
- "Diğer stiller (Faithful/Disc/Rimmed) için hangilerini de tutayım? Hiçbirini seçmezsen hepsinde
  ana simge olur." — options A–D, multiSelect.

### Q1 — without AskUserQuestion
```
<App> için 4 fikir hazır. Resim: work/<slug>/concepts.png
  A: …   B: …   C: …   D: …
Soru 1: Telefonunda göreceğin ana simge (Symbol) hangisi olsun?
  1) A  2) B  3) C  4) D  5) Hiçbiri, yeniden dene
Soru 2: Diğer stiller için hangilerini de tutayım? Harfleri yaz (örnek: "A, D"); hiçbiri ise "0".
```
A game without screenshots: add "Bu bir oyun; elimde oyun içi ekran görüntüsü yok. 2-3 tane
atarsan oyunun nesnelerini onlara göre düzeltirim."

### Q2 — with or without AskUserQuestion
```
<App> hazır. Telefonda görünümü: work/<slug>/phone.png; tüm stiller: work/<slug>/review.png.
Stiller: Symbol = B (…), Faithful = A (…), Disc/Rimmed = B
Telefonuna: eski <App> simgesinin yerine bu gelir; 3 yeni resim eklenir; hiçbir şey silinmez.
Kontrol: 28 geçti, 3 uyarı, 0 hata. Zayıf yanlar: simge biraz ince görünebilir; …
  1) Tamam, pakete ekle   2) Şunu değiştir (ne olduğunu yaz)   3) Konseptlere dön
```
