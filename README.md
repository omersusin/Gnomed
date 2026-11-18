# Gnomed
Gnome looking icon pack for Android 

## Structure

- `app/` – CandyBar dashboard (based on `zixpo/candybar-sample`), package `gnomed.it`.
- `work/<app>/` – editable SVG sources, PNG exports and review boards per icon.
- `pack/styles.json` – which drawable each app uses in each icon style.
- `tools/gen_styles.py` – generates the per-style appfilters (`app/src/<style>/`). Run it after adding icons.

## Icon styles

Launchers read an icon pack's `appfilter.xml` and drawables from the installed APK,
so one APK cannot switch style at runtime. Gnomed is built once per style
(Gradle flavors `faithful`, `disc`, `rimmed`, `symbol`) with the same package name
and signing key. The in-app **Icon style** picker (drawer, Apply screen, app shortcut)
downloads `gnomed-<style>.apk` from the latest GitHub release and installs it as an
update of itself. Single icons can also be picked per app from the launcher's
edit-icon dialog (CandyBar icon picker).

## Building

GitHub Actions (`.github/workflows/build.yml`) builds all four APKs on every push.
Tag `v*`, run the workflow manually with *release*, or push a commit whose message contains `[release]` to publish a release.
Release signing needs four repository secrets: `GNOMED_KEYSTORE_BASE64`,
`GNOMED_KEYSTORE_PASSWORD`, `GNOMED_KEY_ALIAS`, `GNOMED_KEY_PASSWORD`.
