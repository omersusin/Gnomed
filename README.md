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

## Wallpapers and icon requests

- Wallpapers are not embedded: the dashboard reads `wallpapers/wallpapers.json` from the
  `main` branch (raw GitHub), so new wallpapers arrive without an app update.
- *Request* → send offers e-mail, the zip for any app, **images + text without zip**
  (for AI agents and chats), or the app list as text. `tools/import_request.py` reads
  every format, also IconRequest-app zips.

## Building

GitHub Actions (`.github/workflows/build.yml`) builds all four APKs on every push.
The maintainer publishes a release (manual run with *release*, a `v*` tag, or a commit
message with `[release]`); contributors and agents never do.
Release signing needs four repository secrets: `GNOMED_KEYSTORE_BASE64`,
`GNOMED_KEYSTORE_PASSWORD`, `GNOMED_KEY_ALIAS`, `GNOMED_KEY_PASSWORD`.

## Contributing

**Only the maintainer touches `main`.** Everyone else — people and AI agents — works on
a branch and opens a pull request; the maintainer merges or not.

**How a Gnomed icon is designed: [REDESIGN.md](REDESIGN.md)** — the app's idea built as a
GNOME object, never the logo on a plate. The tools and how to send a pull request are in
**[CONTRIBUTING.md](CONTRIBUTING.md)**. AI agents: read
**[AGENTS.md](AGENTS.md)** as well. Ask for an app with the *Icon request* issue template.
