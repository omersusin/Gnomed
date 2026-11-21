# Mistakes, fixes and decisions — the project's memory (binding)

Everything here really happened while building Gnomed (Nov 2026, owner + Claude Code,
plus one DeepSeek PR). Each line: **what happened → why → how it was fixed → the rule
or check that prevents it now.** Read **§10 (the owner's decisions) every session**; read
the other sections when their topic comes up. When the owner has to point out a new
mistake, add it here in the same pull request that fixes it.

Linked from [REDESIGN.md](../REDESIGN.md) §10, [AGENTS.md](../AGENTS.md) and CLAUDE.md.

Contents: 1 Talking to the owner · 2 Identity and design · 3 Colours and gradients ·
4 Size and baseline · 5 Styles and what the owner sees · 6 Pipeline and tools ·
7 App, CI, releases · 8 Git and pull requests · 9 Agents and documentation ·
10 Decisions the owner made (do not undo them)

---

## 1. Talking to the owner

| What happened | Why | Fix | Rule |
|---|---|---|---|
| The owner answered a question with **"Anlamadım"** (twice: "add Bitwarden? dry-run…, 4 PNG, appfilter…", and "the Symbol slot has the cloud") | jargon (dry-run, appfilter, slot, drawable) and two questions in one | asked again in plain words: "Bitwarden'ın 4 halini Gnomed uygulamasına koyayım mı?" | ask in his language, short, **no internal terms**; say what he will see on the phone; one decision per question |
| "Bu soruyu sor diyince tekrar sor" | a decision was asked before he wanted to decide | asked later when he said "Sor" | when he postpones, wait; do not ask the same thing again unprompted |
| "Benim istediğim gibi nasıl mümkün değil???? Mümkün ve yapan developerlar görüyorum" | the in-app style switch was called "not possible on Android" too early | researched; built it (per-style APKs + in-app self-update, see §7) | never say "impossible" before researching; offer the closest working design |
| "Ben orijinal Telegram ikonunu oraya koy demedim. Sadece o kağıttan uçağı düzelttim." | "fix the plane on the stamp" was widened to "put the whole logo on the stamp" | only the measured paper plane on the stamp | **change exactly what was asked, nothing more**; if unsure, ask |
| "Varsayılan mektup değil ama" | "default" was taken as the Faithful slot; he uses the **Symbol** APK | envelope in Faithful AND Symbol | "default" = what he sees on his phone (§5) |
| He asked only a question ("why are these not the same size?") | — | answered first, offered the fix, did it when he said so | a question is not an order: answer, then offer |
| Answers in English after he once wrote English | — | — | default language Turkish (CLAUDE.md); follow his last message's language |
| "Beni böyle ikide bir sorma" — the owner was asked again and again (concept rounds, direction, permission) | every uncertainty became a question | exactly two questions per app: Q1 concepts (main + keep), Q2 final = pack approval (REDESIGN §7, owner's decision 2026-11-21) | everything else: decide, write the reason in design.md, mention it in Q2 |

## 2. Identity and design
| BCR's handset was lumpy | the phone's 192 px icon was blurry | traced from a sharp copy the owner sent (`work/bcr/clean-source.png`) | a blurry source is not final: ask for or use a sharp official copy |
| Türk Telekom had an extra dark triangle at the bottom, and the logo sat off-centre | a blurred **background** shape was traced as part of the logo; the mark box included it, so placement was wrong | `erase` override removes it from regions + silhouette and re-measures the box; leftover blur rims dropped | background decorations are not the logo — check every traced piece against the source; alignment comes from the mark box, so fix the box too |

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| The whole pack was "the logo on a plate with a chin" | the automatic pipeline only copies the logo | REDESIGN.md: the app's idea built as a GNOME object; 3 rough concepts → his choice → build | `check_icon.py` FAILs automatic drafts (`redesign`) |
| A play logo inside an invented TV; Instagram as a toy camera | invented containers | removed | never invent wrappers unrelated to the app |
| Firefox's ears/tail redrawn from memory | memory instead of measurement | traced from the source | every shape from `source.png` / `geometry.json` / official SVG |
| ChatGPT came out inverted ("ChatGPT bozuk") | built from the black lines only | figure = white strands outlined in black; light side → `#3d3846` | check figure vs ground first |
| Instagram had an orange "inner layer" | the side face used another colour | side = darkened copy of the face gradient | sides follow their face |
| YouTube as a red disc with a triangle | read as YouTube Music | superellipse button fitted to the source | keep the distinctive outline |
| Group 1 Symbols were broken ("Düzelt bozuklukları") | invert mode applied blindly | per-app symbol mode (`keep` / `margin` / `invert`) | look at every Symbol on light AND dark before asking to ship |
| "The pushed icons are broken" | unreviewed WIP drafts were pushed | fixed with overrides; drafts reviewed before pushing | never push a board you have not looked at |
| "2. option, plus there are more weak ones" | weak icons were not reported before asking to add | 10 weak apps redrawn by hand | list weak icons yourself, honestly, before the approval question |
| Posters / mascots (Clash Royale, Survivor.io) traced into mush | no clean vector element in a 192 px poster | free adaptation (owner: "İlla oyun ile aynı olmasına gerek yok") — two crowns, witch hat + coins | free adaptation only for posters/crops, with his OK; primitives for generic objects, never a brand logo from memory |
| Shizuku / Duolingo heads cut by the tile → no Symbol | a cropped head reads as a mask | Shizuku: hexagon badge; Duolingo: the cut sides closed with one ellipse meeting the measured contour | close cuts geometrically from measured curves; do not skip a style silently (§5) |
| Telegram concepts A/B/C rejected ("Hiçbiri, yeniden dene") | first ideas too close to "logo on a shape" | new ladder ideas (ring, cloud, envelope); he picked "one + others as alternatives" | concepts must be different ideas; rough is fine |
| Hepsiburada's phone icon was an outdated poster | the installed app shows an old icon | the owner sent the official logos ("bunlardan birini kullan veya kendin yap") | an owner-supplied official logo is a valid source; keep the phone icon as `phone-icon.png` |
| A white wordmark alone as Symbol | vanishes on light wallpapers | no Symbol, a margin, or the brand's own layout (Hepsiburada: orange wordmark + colour bar) | `check_icon` `visible_light/dark` |
| Firefox Beta "BETA" letters thin slivers | letters are holes; the badge's lift side filled them | `holes_inlay` | look at letters/holes at 256 px |
| Games round 1 (Kafa Topu 2, Pokémon UNITE, Rush Royale): a plain ball, a bolt, a hat — "hiç benzemiyorlar" | the docs said "ONE generic element from primitives" and I banned characters ("no character from memory" read too widely) | superseded by REDESIGN.md §3b (2026-11-21): references, the scene's composition and count, serious materials | recognisable first; a generic object fails even if it is clean |
| Games round 2: blobby traces of the poster — rejected | tracing a 512 px poster with few colours gives crude cut-outs; the owner wants a designed logo, not a copy | round 3 (one hero each) was also rejected ("iki kafa… üç karakter… çok çirkin", "ayakkabıları var"); see the 2026-11-21 games row | "direkt kopyala yapıştır yapmayacaksın"; REDESIGN §3b |
| Aurex round 2: a white A without its blue field — "hiç benzemiyor" | an anchor (the blue field) was dropped | the A on a blue browser-window object | keep every anchor the owner sees: shape, colour field, accent |
| Aurex: a gap inside the A ("orijinalinde boşluk yok") | the measured counter above the bead was kept as a hole | counter and the open notch above the bead filled | compare holes with the source |

## 3. Colours and gradients

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| SD Maid's dark apron vanished into the dark tile | apron only dE 8 from the tile, below the detection threshold | `THRESH` for the app; star recoloured (`split`); Symbol `keep` | `python3 tools/region_check.py <slug>`: no blob ≥ 1.5 % with a changed colour |
| exteraless lost its pale pink tile; ObtainX's gear turned lavender; Proton VPN's turquoise tip went pale | `light: True` forced white; k-means medians drifted | `face`, `regions`, `merge_grad` | compare with the source, not by memory |
| Gradients flattened to one colour (Firefox Beta 32 % of the tile, Thunderbird, Play Store …) | every region drawn with its median colour | big regions with a clear source gradient keep a fitted gradient automatically (`flat_regions` opts out) | — |
| One gradient cut into bands (exteraless, BitChord, Today Weather, Morphe, Nuvio, Smart Launcher, Stride, Firefox Nightly) | k-means splits a gradient into 3–5 colours | `merge_grad` | `check_icon` `stripes` → recipe R1 |
| Black parts got a black-to-grey gradient (aShell, KernelSU) | the automatic gradient ignored the Dark-4 rule | near-black regions stay flat `#241f31` | no `#000` anywhere |
| White marks got a dirty grey gradient (Mix, Reddit) | antialias/shadow pixels in the fit | whites excluded from automatic gradients | white marks stay clean white |
| Quarry's chart bars came out blue | thin dark parts folded into the blue cluster | `split` override | — |
| Wallpapers showed banding | 8-bit gradients | fine film grain, JPEG | — |

## 4. Size, baseline, canvas

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| Telegram's envelope looked smaller than Instagram/WhatsApp ("niye aynı boyutta değil?") | bottom edge 107: a wide object floating above the line; the old rule "bottom 108…126" let it pass | scaled as one unit to 112 wide, standing on 118 | **baseline rule** REDESIGN.md §5; `python3 tools/size_audit.py` → `0 icon(s) outside the ranges` |
| Scene's Symbol floated | sized by the whole mark incl. dropped parts | sized by the drawn parts | — |
| aShell's Symbol overflowed (y 1…124); 9 margin Symbols sat low | the margin grows outward; the box ignored it | object + margin kept in 5…118 | outward growth counts in the size |
| MT Manager's Symbol touched the canvas edge | one scale for all styles | `symbol_scale` | — |
| Kamera / Saat Symbols 2 units too low | hand-built coordinates by eye | lifted | hand-built icons go through `size_audit.py` too |
| Wide Symbols centred mid-canvas (old pipeline) | centred instead of standing | stand on the baseline | — |

## 5. Styles and what the owner sees

| What happened | Why | Fix | Rule |
|---|---|---|---|
| Duolingo on a square plate among free icons ("Duolingo yanlış") | he uses the **Symbol APK**; the DeepSeek PR skipped the Symbol it had made | Symbol built | every app needs a Symbol, or his OK to skip it |
| Envelope "default" not seen | see §1 | Faithful + Symbol | — |
| "Long-press → edit icon" was offered for picking styles | he wants the choice inside the app ("Uzun bas düzenle ile istemiyorum") | in-app style picker (§7) | — |

## 6. Pipeline and tools
| `pokemon_unıte` became slug `pokemon_un_te` | Turkish dotless ı not transliterated | `import_request.py` transliterates (ı→i, accents removed) | — |
| Apps listed in `batch_apps.tsv` without a `source.png` (lines added by another agent) blocked a later import ("REGISTERED") | the tools treated "listed" as "registered" | listed-without-source counts as NEW; `add_source` writes the source without a duplicate line | — |

| What happened | Why | Fix | Rule / check |
|---|---|---|---|
| 6 hand-built icons replaced by automatic drafts in the pack (after "Herşeyi merge ettim, bak bakalım") | `build_auto.py` was run over every app, then `pack_refresh` | `work/_lib/builders.py`; `build_auto.py` refuses hand-built apps; `pack_refresh.py` rebuilds with the right builder; restored pixel-identical | never rebuild "all apps" and ship without a pixel diff against `main` |
| `make_icon.py whatsapp` would have overwritten WhatsApp etc. | it only knew `build_weak.py`, not `build_group1.py` | `builders.py` | — |
| Potrace traced the inverse | potracer traces False pixels | pass `~mask` | — |
| Fake regions from antialias edges | k-means on every pixel | cluster only stable core pixels | — |
| Walpy's skeleton re-stroke lost the loops | experimental re-stroke | reverted to the core trace | keep what is measured when a redraw loses shape |
| `check_icon` false FAILs (light plates, thin parts) | thresholds too strict | max(light, dark) for plates; area-aware trace IoU | calibrate checks on the whole pack |
| `post.sh` broke | ran under `sh` (no brace expansion) | bash shebang | — |
| `__pycache__` got committed | no ignore | `.gitignore` | — |
| `rsync` missing in the container | — | `cp -r` | — |
| A concept script re-ran when imported and rewrote old concepts | module-level code | `if __name__ == "__main__":` | — |
| Commit hook blocked my own commit message | the message described `[release]` | reworded | the hooks also apply to agents' descriptions |
| A `find` over the repo hung (timeout) | searched build dirs | targeted `git grep` / `ls` | — |
| Pixel comparisons said "changed" for every refreshed PNG | different PNG compression | compare pixels, not bytes; `pack_refresh` saves with `optimize` | — |

## 7. App, CI, releases

| What happened | Why | Fix | Rule |
|---|---|---|---|
| The app crashed at start ("Uygulama çöküyor") | R8 removed `WorkDatabase_Impl.<init>()` (Room/WorkManager) | keep rules in `app/proguard-rules.pro` + CI guard (apkanalyzer) | never touch ProGuard/CI without the owner |
| In-app style switch got 404 | no GitHub release existed; tag pushes are blocked by the proxy | release on manual run / `[release]` commit (owner: "Yes, publish releases") | only the maintainer releases |
| A launcher reads one appfilter per APK, so one APK cannot switch styles | Android | 4 Gradle flavors (faithful/disc/rimmed/symbol), same applicationId + signing key; `StyleSwitcher` downloads `gnomed-<style>.apk` and installs it as an update | do not change applicationId, flavors, signing |
| CI gave one zip with all four APKs ("ci'da apkları ayırabilir misin") | one artifact | one artifact per style, plain `.apk` (`upload-artifact@v7`, `archive: false`) | — |
| Wallpapers made the APK 2.4 MB bigger | embedded in assets | read from `main` (`wallpapers/wallpapers.json`) | new wallpapers need only a merged PR |
| Agents could not take zip requests ("bazı ajanlar zip kabul etmiyor") | CandyBar only e-mails a zip | request dialog: e-mail / images + text / zip / copy list; `tools/import_request.py` reads every format | — |

## 8. Git and pull requests

| What happened | Why | Fix | Rule |
|---|---|---|---|
| Agents could reach `main` | no guard | AGENTS.md §0, `tools/hooks/`, `pr_guard.py` in CI | never commit/push/merge to `main`; open a PR and stop |
| A `--force-with-lease` push was refused | not needed: the remote branch was already in `main` | normal fast-forward push | never force-push; check `git merge-base --is-ancestor` |
| The second redesign patch contained an already-merged commit | PR #7 was merged before the new patch | `git am --3way` skipped it ("already applied") | restart the branch from `main` after a merge |
| A stop hook asked to commit untracked files | build outputs in the tree | commit only real work; ignore caches | — |

## 9. Agents and documentation
| While reviewing the `horustest` branch I first reported "andvm.png missing, assets not updated" | I read only the last 40 lines of a long diff stat | checked again: both were there | never conclude from truncated output; verify the file itself before reporting a problem |

| What happened | Why | Fix | Rule |
|---|---|---|---|
| DeepSeek could not follow the docs ("dokümanlar eksik") | written for strong models | `docs/course/` lessons with real images, `check_icon.py` that works without seeing images, one-command `make_icon.py` | write for the weakest model that will read it |
| DeepSeek copied Duolingo's ComponentInfo from other icon packs | not from the phone | verified on the phone (`cmd package resolve-activity`) | AGENTS.md A3: phone / request / APK only |
| DeepSeek built a Duolingo Symbol, then skipped it | its own rule reading ("mask") | Symbol rebuilt later | report what was built and why it was dropped |
| The size rule was too loose to catch a floating icon | "bottom 108…126" | REDESIGN.md §5 baseline rule + `size_audit.py` | — |
| DeepSeek worked for over an hour on 3 apps ("kah toollar eksik, kah yönergeler") and the result was weak | the docs were written for a strong model; the gaps below | the fixes below; one procedure in AGENTS.md C with exact commands | **if a weaker model gets stuck, the docs are wrong** — fix the docs/tools, not the model |
| It rewrote the same two functions (path → shape, place shapes in a box) in all 6 of its files | `obj.py` had no helper to read the measured parts or to place them | `parts()`, `colour()`, `describe()`, `fit()` in `work/_lib/obj.py`; AGENTS.md section H lists every helper | every repeated chore gets a helper and a line in section H |
| The docs said "measure from geometry.json" but nothing created it in the REDESIGN flow | `new_redesign.py` did not measure; the file only appeared after the old pipeline | `new_redesign.py` measures and prints every part as text | a step may only use files an earlier step created |
| No concept template: each agent invented its own concept script | step 3 said "draw 3 SVGs" | `new_redesign.py` writes a working `concepts/make_concepts.py` (A/B/C from the measured parts, standing on the baseline) | — |
| AGENTS.md mixed two procedures (old "make_icon → recipe" loop and REDESIGN) | REDESIGN was added on top | AGENTS.md C rewritten as ONE path (C0–C11); D = REDESIGN's review questions; section I = what to do for every error message | one procedure per job, never two |
| Aurex Browser shipped as the logo on a blue disc with faint rings — and passed the gate | the gate only checked that redesign.py exists | `check_icon` `plain_shape`: FAIL for a plain disc, WARN for a plain square; lifted only by `shape-ok: <owner's words>` in design.md | a check must test the rule, not the file name |
| `make_icon` told redesigned apps to use the old recipes and go to pack_add | old hint text | redesign-aware hint: review → ask the owner → pack_add | — |
| `fit()` centred wide marks, so free objects floated | centring is right for a mark ON an object, wrong for a free object | `fit(..., anchor="bottom")`, used by the templates | — |
| Text-only models could not "open source.png" | the steps assumed eyes | `describe()` prints the parts; a POSTER warning when parts cover the whole tile | every visual step has a text alternative or says "ask the owner" |
| Symbol insides filled: qobuz "o", saat face, discord eyes ("O harfinin içi dolu… saatin içi dolu") | Symbol builders painted tile-coloured enclosed areas white; `offset_d` dropped interior rings | PR #12: real holes, `painted_counters` only for white figure | `holes` check (D1) |
| Games added to the pack without approval; `approved:` written by the agent | "beni sorma" read as "decide everything" | approval lines are quotes + date; Q2 = pack approval | `redesign` check format (D2) |
| Game icons "çok çirkin", wrong composition (one head instead of two, no boots) | only the store poster, no screenshots, drawn from memory | games rule: screenshots, composition + count, serious materials | REDESIGN §3b |
| One giant session (758k tokens), hours per app | everything in one conversation | new session per app/part | Budget rules (REDESIGN §8) |
| `pack_refresh.py kafa_topu_2 --dry-run` overwrote the pack PNG before approval (2026-11-21, reverted at once) | the tool had no `--dry-run` and took the flag as a slug | `pack_refresh.py` has `--dry-run`, refuses unknown flags | `pack_refresh.py --dry-run` |

## 10. Decisions the owner made (do not undo them — read every session)

- App name **Gnomed**, applicationId **gnomed.it**, default language **English** (Turkish strings in `values-tr`).
- Style choice **inside the app** (drawer, Apply popup, shortcut) and from the launcher popup; four styles Faithful / Disc / Rimmed / Symbol.
- Releases are public on GitHub; signing key only in repository secrets.
- Requests come from the phone (Gnomed's Request screen, any of its export ways); the owner uploads them.
- Wallpapers calm, with grain, loaded from the repository.
- Only the owner touches `main`; every change is a PR he merges or not.
- REDESIGN.md is the only design document; one app per session (`/clear` between apps).
- **The owner uses the Symbol style**: every board shows Symbol first; no app is done without a Symbol.
- **Every style slot a different design** (2026-11-21): "her stil yuvası farklı olursa çok iyi olur" — 4 concepts; main → Symbol, kept ones → Faithful / Disc / Rimmed (REDESIGN §6).
- **Exactly two questions per app** (2026-11-21): Q1 concepts (main + keep), Q2 final; "Tamam, pakete ekle" is the pack approval (REDESIGN §7). Approval lines are his words in quotes + date.
- ~~Games (2026-11-21): draw the game's scene with its characters~~ — replaced the same day by:
- **Games: no characters, the game's objects** (2026-11-21): "Karakter yok, oyunun nesnesi" — no characters, faces or animals; 1–3 of the game's objects (Pokémon UNITE = goal ring + ball, Kafa Topu 2 = ball + boot, Rush Royale = its distinctive object), real materials, GNOME light + thickness, HIG colours near the game's (REDESIGN §3b).
- Holes are real holes in free styles (PR #12); painting them needs his words.
- Telegram: envelope (Faithful + Symbol), ring (Disc).
- Pokémon UNITE: the character version (shipped 2026-11-21) is dropped; redo with objects only. Rush Royale: not approved, objects only. Kafa Topu 2 shipped with characters before this rule (redo only if the owner asks).
