# BATCH — redoing many apps in one run (the owner's batch rule)

The owner (2026-11-22): *"Önce bir tanesini yapsın, bize çıktısını downloads klasörüne versin.
Biz onayladıktan sonra hepsini yapsın."* and, after the first results: *"hiçbiri olmamış … hepsini
baştan yapalım"*, *"sürekli bir şeyleri eksik bırakıyorsun … repoya da işleyelim"*.

This file is the **complete** batch procedure. Do not add or skip steps from a chat message; if the
owner changes something, it is written here first (a pull request), then followed.
To start a batch, the owner sends one line: **"docs/BATCH.md'yi oku ve uygula."**

## 1. Start of EVERY session (also after a compaction)

```
git fetch origin
git branch --show-current          # stay on the batch branch (line 1 of progress.md: "branch: <name>")
#   no batch branch yet:  git switch -c icons/redo-batch origin/main   and write "branch: icons/redo-batch"
#   as line 1 of progress.md. Never "git switch -C" / "reset --hard": they throw away unpushed icons.
git pull --no-rebase --no-edit      # fixes the owner or Claude pushed to YOUR batch branch (first session: skip)
git merge --no-edit origin/main     # the owner's newest rules, checks and fix lists
git config core.hooksPath tools/hooks
python3 tools/gnome-android-icons/scripts/doctor.py      # "result: READY"; do NOT run selftest.py (too slow on a phone)
mkdir -p ~/Downloads/gnomed        # on the phone: /sdcard/Download/gnomed
python3 tools/next.py              # "0. The owner's FIXES" first, if it lists any
```
A merge conflict: keep both sides (rules from main, your icons from the batch), never delete his work.

## 2. Scope — every app, none skipped

- **All apps in the pack**, also the ones redone before (Telegram, Pokémon UNITE, Rush Royale, Deezer,
  Apple Music …): the owner liked none of them. For an app that already has an approval:
  `python3 tools/next.py <slug> --start-redo`, then four NEW concepts, different from the old
  rounds (read `work/<slug>/concepts-round*/` and do not repeat those ideas).
- **New requests** too: busuu, meta_ai, misspipe, termux, wlingua (and any app the owner adds).
- Order: [ROADMAP.md](ROADMAP.md) §1 (system apps → outline icons → logos on tiles → mascots → light
  icons → the rest → new requests → the apps redone before).

## 3. Every app

Before every app: read [START-HERE.md](../START-HERE.md) and run `python3 tools/next.py <slug>`.
If it says OWNER_FIXES_FIRST, do the owner's fix lists first (§4).

1. `python3 tools/fetch_refs.py <slug>` — screenshots, category. Nothing found: do your best, note it.
2. Four concepts, **four different objects**, from the category's family
   ([redesign/CATEGORIES.md](redesign/CATEGORIES.md)); no object another app of the category already uses;
   no characters, faces or mascots.
3. **All four are used** (REDESIGN.md §6): main → **Symbol**, closest to the original logo →
   **Faithful**, a round one → **Disc**, the rest → **Rimmed**. Four styles, four different designs.
4. In design.md (Q1 is replaced by the owner's batch rule):
   ```
   approved: <main letter> - "batch: Biz onayladıktan sonra hepsini yapsın" (<date>)
   keep: <the other three letters> - "batch: hepsi kullanılsın" (<date>)
   ```
5. Build (`python3 tools/make_icon.py <slug>`), then fix **every FAIL and every FIX_WARN**
   (`mark_size`, `visible_light`, `visible_dark`, `legibility32`, `slots`) — `next.py` says how.
6. **Look at it like the owner** (he found these in batch 1, 2026-11-22). For each of the four
   styles write in progress.md what it shows in 2–4 plain words. Redo a style when:
   - you cannot name it as a real thing (a box with dots, a card pile, a black disc with a strip);
   - a real thing has the wrong colour (a red sun - use `sun()`); digits do not read (use
     `digital_display()`);
   - it uses another app's logo object (Telegram's paper plane - `RESERVED` in categories.py);
   - two styles are the same object restyled (gate `slots` measures it);
   - **the app's mark is missing or wrong** (ara-2: Apple Music, Soundcore, ChatGPT's "M") - every
     style carries the measured mark, `put_mark(ic, SLUG, box)`; gate `mark` measures it;
   - **two equal round things side by side look like eyes** (ara-2: Soundcore's earbuds = a face) -
     give them their real shape: stems and ear tips, spokes, pointers; mirrored and tilted;
   - **cover the mark**: hide it - can you still name the object? A plain tile/box whose face is the
     wordmark is the logo on a plate, whatever it is called (overview-3: "server rack", "album sleeve",
     "safe"); a wordmark is a LABEL on the object;
   - two box-shaped containers in one app (cabinet + archive box) are twins; an object that reads as
     another category's (a platter with an arm = a record player) is wrong;
   - **Faithful is not the closest to the logo** - the mark big, in the logo's colours, often the mark
     itself as the object (a turntable or a cardboard box is not);
   - another app of the category already has the object in any style (ara-2: Apple Music's cassette
     was Deezer's) - gate `same_object`.
   Cannot see images? Use `python3 tools/describe_icon.py <svg>` and the concept code: if the code
   draws "rounded box + 3 circles", it is not a nameable object.
7. When `next.py` says ASK_Q2: **do not ask**. Copy `work/<slug>/review.png` and `phone.png` to
   `~/Downloads/gnomed/<slug>/`, add the app to the current group of 10.
8. Append one line to `~/Downloads/gnomed/progress.md`: `- [x] <slug> - S: <object> / F: <object> / D: <object> / R: <object> - <problems>`.

## 4. Every 10 apps — stop and show

```
python3 tools/overview.py <the 10 slugs> --out ~/Downloads/gnomed/overview-<N>.png
git add -A && git commit -m "batch <N>: <slugs>" && git push -u origin HEAD
```
Then send the owner a short Turkish message: the picture's path, the 10 apps, what you could not fix.
**STOP and wait.** His answer:
- **"Devam"** → the next 10.
- **"<app> olmamış (…)"** → redo exactly that app (new concepts), show it again.
- **A list of fixes per app** → it is written in the repository, not in a chat message (owner
  2026-11-22: *"Bıktım bana prompt vermenden, yaz depoya"*): `work/<slug>/fixes.md`, one line per style;
  a later round for the same app is a new file `work/<slug>/fixes-<group>.md`.
  After the owner merges it: `git merge origin/main` (§1), then `python3 tools/next.py` lists the
  apps under "0. The owner's FIXES"; each app's `next.py <slug>` says OWNER_FIX with the lines.
  Change exactly those styles, nothing else; tick each line with `-> now: <what it is now>`.
  When the whole group is done, `next.py` (no slug) prints the overview command for only those
  apps: run it, push, write `shown: <date>` in their fixes.md, send him the path, wait again.

## 5. Into the pack — only with his words

Nothing goes into the pack before he writes **"Tamam, pakete ekle"** for a group (or for all).
Then: for the approved apps `final: "<his words>" (<date>)` in design.md, `pack_add.py` /
`pack_refresh.py` (dry-run first), append docs/LOG.md, push, **one** pull request. Never touch `main`.

## 6. If your context is compacted

`~/Downloads/gnomed/progress.md` is the truth: continue after its last `[x]` line. Re-read this file
and do §1 again (it merges main and shows open fix lists).

## 7. Not allowed in a batch

`pack_add` / `pack_refresh` before his approval · touching `main` · `selftest.py` (slow) · skipping
an app · reusing an old concept · two apps of one category with the same object · a style that
repeats another style's design · characters, faces, mascots · image generators.
