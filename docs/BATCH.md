# BATCH — redoing many apps in one run (the owner's batch rule)

The owner (2026-11-22): *"Önce bir tanesini yapsın, bize çıktısını downloads klasörüne versin.
Biz onayladıktan sonra hepsini yapsın."* and, after the first results: *"hiçbiri olmamış … hepsini
baştan yapalım"*, *"sürekli bir şeyleri eksik bırakıyorsun … repoya da işleyelim"*.

This file is the **complete** batch procedure. Do not add or skip steps from a chat message; if the
owner changes something, it is written here first (a pull request), then followed.
To start a batch, the owner sends one line: **"docs/BATCH.md'yi oku ve uygula."**

## 1. Setup (once)

```
git fetch origin && git switch -C icons/redo-batch origin/main
git config core.hooksPath tools/hooks
python3 tools/gnome-android-icons/scripts/doctor.py      # "result: READY"; do NOT run selftest.py (too slow on a phone)
mkdir -p ~/Downloads/gnomed        # on the phone: /sdcard/Download/gnomed
```

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
6. When `next.py` says ASK_Q2: **do not ask**. Copy `work/<slug>/review.png` and `phone.png` to
   `~/Downloads/gnomed/<slug>/`, add the app to the current group of 10.
7. Append one line to `~/Downloads/gnomed/progress.md`: `- [x] <slug> - <main object> - <problems>`.

## 4. Every 10 apps — stop and show

```
python3 tools/overview.py <the 10 slugs> --out ~/Downloads/gnomed/overview-<N>.png
git add -A && git commit -m "batch <N>: <slugs>" && git push -u origin icons/redo-batch
```
Then send the owner a short Turkish message: the picture's path, the 10 apps, what you could not fix.
**STOP and wait.** His answer:
- **"Devam"** → the next 10.
- **"<app> olmamış (…)"** → redo exactly that app (new concepts), show it again.

## 5. Into the pack — only with his words

Nothing goes into the pack before he writes **"Tamam, pakete ekle"** for a group (or for all).
Then: for the approved apps `final: "<his words>" (<date>)` in design.md, `pack_add.py` /
`pack_refresh.py` (dry-run first), append docs/LOG.md, push, **one** pull request. Never touch `main`.

## 6. If your context is compacted

`~/Downloads/gnomed/progress.md` is the truth: continue after its last `[x]` line. Re-read this file.

## 7. Not allowed in a batch

`pack_add` / `pack_refresh` before his approval · touching `main` · `selftest.py` (slow) · skipping
an app · reusing an old concept · two apps of one category with the same object · a style that
repeats another style's design · characters, faces, mascots · image generators.
