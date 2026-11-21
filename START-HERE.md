# START HERE — the only entry point (any model, any tool, any person)

**Gnomed** is an Android icon pack (CandyBar app, package `gnomed.it`). Every app icon is redrawn
as a **GNOME/Adwaita object** in code (Python → SVG → PNG) — never with an image generator.
One owner decides everything; he writes **Turkish** and uses the **Symbol** style. `main` is his:
you work on a branch and open a pull request; he merges.

## 1. Read, in this order (and nothing else at the start)

1. this file
2. [REDESIGN.md](REDESIGN.md) — how an icon must look (§0 how to talk to the owner, §3b games, §5 rules)
3. [AGENTS.md](AGENTS.md) — git, ComponentInfo, pack files, what is forbidden
4. [docs/MISTAKES.md](docs/MISTAKES.md) **§10 only** — the owner's decisions (the rest when a topic comes up)
5. [docs/PLAYBOOK.md](docs/PLAYBOOK.md) — **only the section of the step you are on** (`tools/next.py` names it)

Old and NOT for designing: `docs/course/` (incl. `CONTRIBUTING-legacy.md`, the legacy plate pipeline).
For people (not agents): [CONTRIBUTING.md](CONTRIBUTING.md) is the short human guide.
Tools that read a file automatically: Claude Code reads `CLAUDE.md`; OpenCode and Codex CLI read
`AGENTS.md`; Gemini CLI reads `GEMINI.md`; Qwen Code reads `QWEN.md`. All of them point here.

## 2. Where are we?

- [docs/APPS.md](docs/APPS.md) — every app: redesigned or not, the owner's approvals, what is in
  each style slot, the next step. (Regenerate: `python3 tools/pack_status.py`, a few minutes.)
- [docs/LOG.md](docs/LOG.md) — what each session did, by which model, and why. Append-only.
- [docs/ROADMAP.md](docs/ROADMAP.md) — which apps to redo first and why (the owner still picks).
  [docs/RESEARCH.md](docs/RESEARCH.md) — where the design rules come from (GNOME HIG, MoreWaita, Delta).
- Which app next? `python3 tools/next.py` (no slug). Unfinished apps come first; otherwise the
  **owner** picks the app — ask him, never pick one yourself.

## 3. The one command

```
python3 tools/next.py <slug>
```

It prints `STATE`, `GOAL`, `DO` (exact commands/edits), sometimes `ASK THE OWNER` (the Turkish
text to send), and `DETAILS` (the PLAYBOOK section). **Always run it first, do only what it
prints, then run it again.** Repeat until `STATE DONE`. If what it prints is wrong or unclear,
stop and write down why (that is a bug in the docs — tell the owner in your final message).

Before the first `next.py` of a session (once):

```
git config core.hooksPath tools/hooks
git branch --show-current           # on main? -> git switch -c icons/<slug>
                                    # on another branch (yours, or one your tool made)? stay on it
python3 tools/gnome-android-icons/scripts/doctor.py     # must end with "result: READY"
```
If your tool refuses the `git config` line, do not work around it: go on, run `python3 tools/pr_guard.py`
before every push (the same checks), and tell the owner in your final message that hooks are off.
No `START-HERE.md` or no `tools/next.py` in your checkout? You are on an old branch: run
`git fetch origin && git switch -c icons/<slug> origin/main` and start again.

The flow `next.py` walks you through (one app = one session, then `/clear` or a new chat):

```
NO_SOURCE → NOT_STARTED → FILL_DESIGN → DRAW_CONCEPTS → BOARD → ASK_Q1 (owner) →
BUILD → FIX_FAIL → ASK_Q2 (owner) → PACK → LOG → COMMIT → PUSH → DONE
REDO = the owner asked to redo an app that was already approved
```

## 4. Asking the owner — exactly two questions per app

Q1 (which concept) and Q2 (final approval). `next.py` prints both texts. Nothing else is asked;
decide the rest yourself and write why in `work/<slug>/design.md`.

- **With AskUserQuestion** (Claude Code): one call; options = the letters / the three answers.
- **Without it** (OpenCode, Codex, chat): send the text with **numbered options** in Turkish and
  wait. He answers with a number or words, e.g. `1` or `B` or `A, D`.
  ```
  Telefonunda göreceğin ana simge (Symbol) hangisi olsun?
  1) A   2) B   3) C   4) D   5) Hiçbiri, yeniden dene
  ```
- Write his answer **verbatim, in quotes, with the date** into design.md (`approved:`, `keep:`,
  `final:`). Never write these lines from your own idea — a check fails them.
- He often types by voice: read a strange word from the context (REDESIGN.md §0.3).

## 5. If you cannot see images

Say so to the owner, once, plainly: *"Resimleri göremiyorum; ölçümlere göre çalışıyorum, son karar
senin gözün."* Then:

- `python3 tools/describe_icon.py <file.svg|png>` — box, baseline, painted area, colours with
  GNOME names, holes, the size rules, an ASCII preview.
- `python3 tools/check_icon.py <slug>` — the quality gate (PASS/WARN/FAIL + the fix).
- The object catalogue as text: [docs/redesign/OBJECTS.md](docs/redesign/OBJECTS.md).
- Two different pictures: `docs/redesign/gnome-objects.png` / `gnome-games.png` = REAL GNOME icons
  (how a GNOME object looks); `docs/redesign/objects.png` = our ready objects (OBJECTS.md as text).
- Never claim you looked at a picture. The owner is the eye: Q1 and Q2 show him the PNGs.

## 6. Ten hard rules (the rest is in REDESIGN.md and AGENTS.md)

1. Never commit or push to `main`, never merge, never `--no-verify`, never `[release]`.
2. No image-generation or image-editing models of any kind.
3. A brand mark comes from `work/<slug>/source.png` (`parts()` / `body()`), never from memory.
4. A ComponentInfo comes from the owner's request or his phone — never guessed.
5. Pack files (`app/src/main/res/`, the XMLs, `artwork/`, `pack/styles.json`) change only through
   `tools/pack_add.py` / `tools/pack_refresh.py`, and only after his "Tamam, pakete ekle".
6. Games: the game's objects only — no characters, faces or animals (REDESIGN.md §3b).
7. Holes are real holes (transparent), never painted.
8. "Change X" means change exactly X. "Varsayılan/default" = the Symbol style he sees.
9. One app per session; append docs/LOG.md before the commit (`pr_guard` checks it).
10. Never say "done" while `check_icon` shows a FAIL; never say "impossible" before checking.

## 7. Tools (one line each — `next.py` tells you when to use them)

| Command | Does |
|---|---|
| `tools/next.py [<slug>]` | the next step (always first) |
| `tools/new_redesign.py <slug>` | measures the source, creates design.md, concept + build templates |
| `tools/concepts.py <slug>` | the concept board `work/<slug>/concepts.png` |
| `tools/make_icon.py <slug>` | builds redesign.py → SVGs, review.png, phone.png, runs the gate |
| `tools/check_icon.py <slug>` | the quality gate |
| `tools/describe_icon.py <file>` | an icon as text (for models without vision) |
| `tools/pack_add.py` / `tools/pack_refresh.py` | put approved icons into the pack (`--dry-run` first) |
| `tools/size_audit.py`, `tools/pr_guard.py`, `tools/selftest.py` | pack-wide checks before a PR |
| `tools/validate_pack.py` | appfilter / drawable.xml / styles.json point to real PNGs, no conflicting ComponentInfos (PR guard runs it) |
| `tools/readme_previews.py` | after the pack changed: README pictures + store screenshots from the real PNGs |
| `tools/make_palettes.py` | the GNOME palette for every program → `docs/palette/` (from `RAMP` in objects.py) |
| `work/_lib/objects.py` | 32 ready GNOME objects to compose ([picture](docs/redesign/objects.png), [text](docs/redesign/OBJECTS.md)) |

Worked examples from source to the pack: [docs/playbook/](docs/playbook/) (Telegram, Aurex
Browser, Pokémon UNITE, Rush Royale). History of every mistake: [docs/MISTAKES.md](docs/MISTAKES.md).
