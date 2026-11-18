# Android icon pack integration (CandyBar and compatible dashboards)

Verified against `zixpo/candybar-sample` (commit 3bf109c, 2026-06-12) and the
CandyBar library source (`IconsHelper.java`, `RequestHelper.java`).

## How icon packs work

Launchers (Nova, Lawnchair, Niagara, Smart Launcher, Hyperion, many OEM
launchers incl. POCO/MIUI via theme apps) read the pack's **appfilter.xml**:
each `<item component="ComponentInfo{package/activity}" drawable="name"/>` maps
an app's *launcher activity* to a drawable in the pack. The dashboard app
(CandyBar) shows **drawable.xml** as the gallery and handles icon requests.
Unmapped apps get the pack's fallback (`iconback`/`iconmask`/`scale`).

## Files in the CandyBar sample (both copies exist and are identical)

| File | Purpose |
|---|---|
| `app/src/main/res/drawable-nodpi/<name>.png` | the icon (256 x 256 PNG recommended; PNG/WebP/XML vector allowed) |
| `app/src/main/res/xml/appfilter.xml` + `app/src/main/assets/appfilter.xml` | component -> drawable mapping (launchers read one or the other) |
| `app/src/main/res/xml/drawable.xml` + `app/src/main/assets/drawable.xml` | dashboard gallery: `<category title="..."/>` then `<item drawable="name" name="Optional Label"/>` |
| `res/values/dashboard_configurations.xml` | dashboard behaviour (request limits, etc.) |
| `res/values/dashboard_icon_name_replacer.xml` | display-name cleanup (`_` -> space by default) |

`appfilter.xml` also holds `<iconback img1="iconback"/>`, `<iconmask img1="iconmask"/>`,
`<scale factor="0.64"/>`: these affect **unthemed** apps only. Leave them alone
unless the user asks.

Special components for Nova-style "generic" icons exist: `:BROWSER`,
`:CALCULATOR`, `:CALENDAR`, `:CAMERA`, `:CLOCK`, `:CONTACTS`, `:EMAIL`,
`:GALLERY`, `:PHONE`, `:SMS`, `:LAUNCHER_ACTION_APP_DRAWER`.

## Getting the component - never guess

| Way | Command |
|---|---|
| Phone over USB (best) | `python3 scripts/find_component.py --adb org.example.app` |
| All launcher apps on the phone | `python3 scripts/find_component.py --adb-all --grep example` |
| From an APK | `python3 scripts/find_component.py --apk app.apk` |
| On-phone | CandyBar's own request screen / "Icon Request" style apps export appfilter lines |

One app can have several launcher activities (or change activity names between
versions/flavours). Map all of them to the same drawable.

## Adding an icon

```bash
python3 scripts/candybar_add.py --project ~/IconPack --name example_app \
    --svg work/example/example-faithful.svg --label "Example" --category "Social" \
    --component "ComponentInfo{org.example.app/org.example.app.MainActivity}" \
    --alt work/example/example-disc.svg:"Example (Disc)" \
    --alt work/example/example-rimmed.svg:"Example (Rimmed)" \
    --keep-source --dry-run        # review the diff, then rerun without --dry-run
```

Guarantees: additive edits only; both XML copies updated when both exist;
refuses invalid names (lowercase `a-z0-9_`, starts with a letter, no Java
keyword), refuses overwriting an existing drawable or remapping a component
(unless `--replace`), re-parses all XML after writing. Without `--component`
the icon is only added to the gallery - say so to the user.

Then build: `./gradlew assembleDebug` (needs Android SDK/JDK) and test on a
launcher. If you could not build or test, say it.

Relative activity names (`ComponentInfo{pkg/.Main}`) are expanded to the full
class (`pkg.Main`) by `candybar_add.py`; `pack_audit.py` warns about any left in
the XML - several launchers only match full names.

## Auditing the whole pack

```bash
python3 scripts/pack_audit.py --project ~/IconPack --sheet work/pack-audit.png --json work/pack-audit.json
```
ERROR: appfilter/drawable.xml entries without a resource file, one component
mapped to two drawables, malformed components, invalid resource names, broken
XML. WARN: res/xml vs assets copies out of sync, orphan PNGs, non-RGBA or tiny
PNGs, and icons whose visual mass / box / bottom edge leave the official GNOME
band (they will look heavier or lighter than the rest of the pack). The family
sheet frames those in red. (Tested on the official CandyBar sample: its template
appfilter points at 12 placeholder drawables that do not exist - the audit lists
them, exactly the kind of silent failure it is for.)

## What the phone will really show

- Launcher icon: 48-60 dp; on a 1080 x 2400, 440 dpi phone (density 2.75) that is
  ~132-165 px - the 256 px PNG is downscaled, so 256 is enough.
- Folder previews, widgets, search results: ~16-24 dp (~45-65 px) - this is where
  the 32/48 px legibility checks matter on Android.
- Some launchers can force one icon shape or reshape/wrap non-adaptive icons
  (e.g. Nova's legacy-icon reshaping; option names differ per launcher and
  version): then a GNOME silhouette is shrunk onto a white circle or squircle. `launcher_preview.py --shape all` shows how the
  pack looks with that option on or off - tell the user which setting suits the pack.

## Alternatives in a pack

Primary drawable -> appfilter. Alternatives (`<name>_alt1`...) -> drawable.xml
only, ideally with labels. Users long-press the app -> Edit -> pick from the pack.

## Adaptive icons are a different system

Android adaptive icons (108 dp canvas, 72 dp visible, 66 dp safe zone,
foreground/background/monochrome layers) are how an *app* ships its own icon.
Icon packs replace the whole icon with a bitmap (or vector), and the
launcher may or may not mask it. A GNOME silhouette with transparency is the
whole point here - do not force it into an adaptive squircle. Some launchers
"normalise" icon size; GNOME icons already respect consistent visual weight,
so they look right without extra padding.

## Formats

- PNG 256 x 256 RGBA in `drawable-nodpi` (CandyBar recommendation; 512 if the user wants crisper large previews - costs APK size).
- WebP lossless also works; XML VectorDrawable possible but gradients/clip
  paths need API 24+ and conversion care - PNG is the safe default.

## Distribution / licences

The CandyBar library is Apache-2.0. Brand logos and trademarks belong to their
owners; GNOME reference icons are GPL/CC-BY-SA (see `assets/reference-library/`).
Personal use is one thing; publishing a pack on a store is the user's legal
decision - point it out, do not decide it.
