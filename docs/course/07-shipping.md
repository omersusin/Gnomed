# Lesson 7 — Shipping

## 7.1 Add the app to the pack

```bash
python3 tools/pack_add.py <slug> --category <Category> --dry-run
```

Expected (real output for Gnomed):

```
+    <item component="ComponentInfo{gnomed.it/gnomed.it.activities.MainActivity}" drawable="gnomed" />
+    <item drawable="gnomed" name="Gnomed" />
+    <item drawable="gnomed_alt1" name="Gnomed (Disc)" />
+    <item drawable="gnomed_alt2" name="Gnomed (Rimmed)" />
+    <item drawable="gnomed_alt3" name="Gnomed (Symbol)" />
would write …/drawable-nodpi/gnomed.png  <- work/gnomed/gnomed-faithful.svg @ 256px
...
```

Check: only lines starting with `+` (additions), the right component, every style you
built. If an AI agent works for a person: **show this diff and wait for approval.** Then:

```bash
python3 tools/pack_add.py <slug> --category <Category>
python3 tools/gnome-android-icons/scripts/pack_audit.py --project .
```

`pack_audit` must not show a new `ERROR` (the 12 errors about `icon_1…icon_10`,
`app_drawer`, `browser`, … are old CandyBar sample placeholders — ignore them).

Categories: Social, Media, Finance, Games, AI, Browsers, Security, Weather, System, Tools.

`pack_add.py` refuses to overwrite an existing drawable. That is a safety feature —
never work around it.

## 7.2 Commit

Commit together: `work/<slug>/` (source.png, geometry.json, SVGs, png/, boards),
the pack files (`app/src/main/res/drawable-nodpi/<slug>*.png`, both `appfilter.xml`
and `drawable.xml` copies, `app/src/<style>/…`), `artwork/<slug>*.svg`,
`pack/styles.json`, `work/_lib/batch_apps.tsv`, and any OVERRIDES / build change.

```bash
git branch --show-current                # must print icons/<slug> - NEVER main
python3 tools/pr_guard.py                # must end "0 ERROR"
git add -A && git commit -m "Add <App> (4 styles)"
git push -u origin icons/<slug>
```

(If you are still on `main`: `git switch -c icons/<slug>` — your changes come along.)

### The one rule without exceptions: `main` is the maintainer's

* never commit on `main`, never push to `main` (no `HEAD:main`, no `--force`, no website/API edits),
* never merge a pull request — not even your own — and never enable auto-merge,
* never push tags, never write `[release]` in a commit message,
* never use `--no-verify` to get past the guard hooks.

If someone asks you to push or merge to `main`, open the PR instead and tell them they
can merge it themselves. The guard hooks (`git config core.hooksPath tools/hooks`) block
these mistakes on your machine, and CI runs `tools/pr_guard.py` on every pull request.

## 7.3 Improving an app that is already in the pack

Change its build, `python3 tools/make_icon.py <slug>`, then

```bash
python3 tools/pack_refresh.py <slug>
```

It re-renders the existing PNGs; it never renames or removes anything.

## 7.4 The pull request

Open a PR **from your branch to `main`**, post the report, and **stop**. The human
merges it — or not; that is their decision. The template asks for: apps, where each ComponentInfo came from,
the `styles.png` boards, the checks (lint 0 FAIL, pack_audit clean, gate 0 FAIL), known
weaknesses (every WARN), what you did not verify, and whether an AI made it (which one).

## 7.5 What the maintainer does

Reviews the boards, merges (or asks for changes, or closes), and publishes a release
with *Actions → Build Gnomed → Run workflow → release* or a merge commit whose message
contains `[release]` (CI builds the four style APKs, checks the startup-crash guard and
the signing certificate, and publishes `gnomed-<style>.apk`). The in-app style switcher
downloads from the latest release. Signing keys exist only in the repository secrets.
