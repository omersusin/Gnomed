# Lesson 5 — Worked example: one app from zero

This is **the routine**. Do exactly these steps, in this order, for every new app.
The outputs shown are real (from the app *Recon*).

## Step 0 — Setup (once per machine)

```bash
git clone https://github.com/omersusin/Gnomed && cd Gnomed
python3 -m pip install -r tools/gnome-android-icons/requirements.txt
python3 tools/gnome-android-icons/scripts/doctor.py
```

Expected last line: `result: READY`. If not, install what it names.

## Step 1 — Get the icon and the ComponentInfo

From the user's icon-request zip: open `appfilter.xml`, find the app:

```xml
<!-- Recon -->
<item component="ComponentInfo{dev.wolzard.recon/dev.wolzard.recon.MainActivity}" drawable="recon" />
```

and the icon `icons/recon.png`. **Never type a ComponentInfo from memory.**

## Step 2 — Register

```bash
python3 tools/add_source.py recon /path/to/icons/recon.png "Recon" 'ComponentInfo{dev.wolzard.recon/dev.wolzard.recon.MainActivity}'
```

Expected: `ok: work/recon/source.png + batch_apps.tsv. Next: …`

Errors you may see: *slug must be lowercase…* (rename: `_1dm` → `onedm`), *already
registered* (the app exists — see lesson 7 §7.3 to improve it instead).

## Step 3 — Make the icon

```bash
python3 tools/make_icon.py recon
```

It prints, among other things:

```
recon flat [('#e8ece9', 0.1017), ('#a8e06c', 0.0167)]      <- auto.py: tile kind + mark colours
recon ok flat symbol: margin                                <- build_auto.py: built, Symbol mode
[OK] recon/recon-faithful.svg  size 104.0x104.0 bottom 116.0 chin 4.0 …   <- lint
recon-faithful.svg
   32px  gaps  2 (12.4 u2)  thin 9.6 u2  ssim 0.806          <- legibility
...
PASS  faithful  visible        light 0.89 / dark 0.14
...
WARN  symbol    legibility32   0.717   -> FIX: R11 (bigger mark, drop tiny details, thicker strokes)
summary: 24 PASS, 1 WARN, 0 FAIL  (OK to continue)
```

Read it like this:

* `flat` + colours: the tile was one colour; the mark has a light grey and a green part.
* lint `[OK]` / `[WARN]`: only `[FAIL]` blocks you. A `WARN` like "no chin detected" on a
  dark disc is normal; "file is 119 KB" means the paths are heavy (not blocking).
* The gate summary: **0 FAIL → continue.** WARNs are listed in your PR as weaknesses.

## Step 4 — If the gate shows FAIL

Find the recipe number after `FIX:` in [lesson 4](04-recipes.md), apply it, run
`python3 tools/make_icon.py recon` again. Repeat until **0 FAIL**. Typical loop:

```
FAIL  symbol    visible_light  0.21   -> FIX: R6: symbol mode margin, or skip the symbol
```

→ add to OVERRIDES in `work/_lib/build_auto.py`:

```python
"recon": {"symbol": "margin", "note": "white brackets: Symbol keeps a dark tile margin"},
```

→ run again → `PASS symbol visible_light 0.59`.

## Step 5 — Look (if you can see images)

Open `work/recon/styles.png`: source + four styles on light and dark. Ask for every
style: *same shape as the source? anything extra or missing? stripes? blobs? does it
disappear anywhere?* If something looks wrong that the gate did not catch, use lesson 4.
If you cannot see images, say so in the PR.

## Step 6 — Ship (lesson 7)

```bash
python3 tools/pack_add.py recon --category Tools --dry-run
python3 tools/pack_add.py recon --category Tools
python3 tools/gnome-android-icons/scripts/pack_audit.py --project .
```

## Summary card (print this)

```
1 add_source.py <slug> <png> "<Label>" '<ComponentInfo>'
2 make_icon.py <slug>
3 FAIL? -> lesson 4 recipe -> OVERRIDES / auto.py tables / build_weak.py -> back to 2
4 look at work/<slug>/styles.png (or say you could not)
5 pack_add.py --dry-run -> show diff -> pack_add.py -> pack_audit.py
6 commit work/<slug>/ + pack files, open a PR (lesson 7)
```
