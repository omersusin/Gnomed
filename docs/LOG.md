# Gnomed — work log (append-only)

One entry per session that changed `work/` or the pack. **Append at the end; never edit or
delete an old entry.** `tools/pr_guard.py` fails a pull request that changes `work/` or the pack
without adding an entry here. `tools/next.py` sends you here (state LOG) before the commit.

Format (copy it):

```
## YYYY-MM-DD — <model> via <tool> — `slug`, `slug`
- What: <what changed, per app; main design -> Symbol, kept -> slots>
- Why: <the owner's reason / request>
- Owner: <his words, verbatim in quotes, with the date>
- PR: <#number or link>
- Open problems: <honest weak points, what is left>
```

Backfilled on 2026-11-21 from `git log`, `docs/MISTAKES.md`, `work/*/design.md` and the pull
requests. The repository starts on 2026-11-18: there is no record of any work before that date.
Times are from the commits; the model of a backfilled session is what the commits and PRs show.

---

## 2026-11-18 — Claude via Claude Code (cloud session) — `bitwarden` + the app
- What: CandyBar dashboard base (zixpo/candybar-sample); Bitwarden in 4 styles; the Gnomed app:
  package `gnomed.it`, one APK per style (Gradle flavors), in-app style switch, CI; release crash
  fixed (Room/WorkManager keep rule) + a CI guard against it.
- Why: the owner's first request (install the skill, a CandyBar pack, 4 alternatives per icon).
- Owner: "Benim istediğim gibi nasıl mümkün değil????" (2026-11-18) — after the agent first said an
  in-app style switch was impossible; it was then built (REDESIGN.md §0.5).
- PR: #1, #2
- Open problems: Bitwarden is the old "logo on a plate" style.

## 2026-11-18 — Claude via Claude Code (cloud session) — group 1 + 73 apps
- What: group 1 hand-built (`whatsapp`, `instagram`, `youtube`, `telefon`, `mesajlar`, `kamera`,
  `foto_raflar`, `saat`, `ayarlar`, `chatgpt`); a batch pipeline (auto measuring + generic builds)
  for 73 more apps, 63 added at once; 10 weak ones redrawn (`clash_royale`, `survivor_io`,
  `shizuku`, `konabess`, …); wallpapers with grain; releases.
- Why: "Tüm uygulamalarımi yapabilir misin? Hemen kullanmak istiyorum" (2026-11-18).
- Owner: "The pushed icons are broken" (2026-11-18) — the 73-app batch went out with one approval
  at the end; broken icons reached his phone (REDESIGN.md §0.7).
- PR: #2, #4
- Open problems: every one of these is the old "logo on a plate" style (see docs/APPS.md).

## 2026-11-18 — DeepSeek via another tool (the owner's account) — `duolingo`
- What: Duolingo (owl face, three styles), as a test of the contributor docs with a weaker model.
- Why: "Deepseek için yeterli olur mu o doküman? Deneyelim mi bir ikon için" (2026-11-18).
- Owner: "Duolingo yanlış" (2026-11-18) — fixed by Claude the same day (Symbol added).
- PR: #3, #6
- Open problems: the docs were too long and contradictory for a small model (fixed later, Part C).

## 2026-11-18 — Claude via Claude Code (cloud session) — fixes, `hepsiburada`, `quarry`, redesign-first
- What: restored 6 hand-built icons overwritten by the automatic builder (+ guard); Hepsiburada and
  Quarry; lost colours/flattened gradients fixed pack-wide (`sd_maid_se` and others); Firefox
  Beta/Nightly letters; the owner's redesign patch: REDESIGN.md, object helpers, concept board,
  redesign gate; skill 1.2 vendored.
- Why: "Fix sdmaid and others that changed colors. Fix Gradients too." (2026-11-18); the owner's
  `gnomed-redesign.patch`.
- PR: #5, #6, #7, #8
- Open problems: the pack is still "logo on a plate" except the apps redesigned later.

## 2026-11-19 — Claude via Claude Code (cloud session) — `telegram`, size audit, MISTAKES.md
- What: Telegram redesigned (envelope with the paper plane on its stamp = Faithful + Symbol, ring =
  Disc); a size/baseline audit of the whole pack (18 icons fixed); docs/MISTAKES.md written;
  `bcr` from a sharp source; `t_rk_telekom` without the background triangle.
- Why: "Bir şey soracağım. Bu simgeler niye aynı boyutta değil…" (2026-11-19).
- Owner: "Defaultu o mektup yap" (2026-11-19); "Varsayılan mektup değil ama. Düzelt lütfen"
  (2026-11-19) — "varsayılan" meant the Symbol he uses, not Faithful (REDESIGN.md §0.2);
  "Ben orijinal Telegram ikonunu oraya koy demedim. Sadece o kağıttan uçağı düzelttim." (2026-11-19)
  (REDESIGN.md §0.8).
- PR: #9, #10
- Open problems: Telegram has no own Rimmed (falls back to Faithful).

## 2026-11-19 — DeepSeek via OpenCode — `andvm`, `horus`, `aurex_browser`
- What: AndVM (two peaks as enamel objects), Horus (the eye as an amulet, sclera a real hole),
  Aurex Browser (first version) on branch `horustest`.
- Why: the owner tested whether a cheaper model can follow the docs.
- Owner: Horus Q1: "a ama gözün içi transparan değil (gözbebeğinden bahsetmiyorum, gozakindan
  bahsediyorum)" (2026-11-19). "Deepseek 1 saatten fazladır simgeleri yapmak için uğraşıyor. Kah
  toollar eksik, kah yonergeler…" (2026-11-19).
- PR: merged later through `horustest` (#13, #14)
- Open problems: AndVM and Horus have no Symbol and no Q2 approval (`final:` empty) — see docs/APPS.md.

## 2026-11-19 — Claude via Claude Code (cloud session) — `aurex_browser`, games (first try), docs for weak models
- What: Aurex Browser redone (browser window + A, concept C); first versions of `kafa_topu_2`,
  `pokemon_unite`, `rush_royale` (rejected); "make the redesign flow work for weaker models".
- Owner: Aurex: "C" (2026-11-19); "Oyunu öğren içinde niye bir boşluk var? Orijinalinde bir boşluk
  yok, onu düzelt." (2026-11-19) — voice typing for "A'nın içinde" (REDESIGN.md §0.3);
  games: "Bak, Kafa Topu oyununda iki kafa olması gerekiyor, böyle karşı karşıya…" (2026-11-19).
- PR: #11 (closed, included in #13)
- Open problems: Aurex has no Symbol and no Q2 answer; the games were added without his approval
  and with an approval line the agent wrote itself (fixed 2026-11-21).

## 2026-11-21 — Claude via Claude Code (the owner's chat) — real holes
- What: Symbol holes made real (transparent) for `qobuz`, `discord`, `saat`, `trestle`,
  `swift_backup`, `obtainx`, `thunderbird`, `scene`; `painted_counters` override for white figure parts.
- Why: "O harfinin içi dolu… saatin içi dolu" (the owner's review).
- PR: #12 (merged through `horustest`)

## 2026-11-21 — Claude via Claude Code (cloud session) — DUZELTME-PLANI A–D, `kafa_topu_2`
- What: Part A (saved `horustest`), B (merged the holes fix), C (one rule set: REDESIGN.md = design,
  AGENTS.md = git/pack/tools), D (`holes` + approval-format checks, phone preview, `tools/selftest.py`);
  Kafa Topu 2 redone from the owner's screenshots: two players facing + ball (B = Symbol, A/C/D kept).
- Owner: Kafa Topu 2 Q1 "B" / "A,B,C,D,Sen karar ver"; Q2 "Tamam, pakete ekle" (2026-11-21).
- PR: #13
- Open problems: Kafa Topu 2 still draws two faces; the owner agreed to redo it with objects only
  ("Evet, yeni oturumda", 2026-11-21) — `python3 tools/next.py kafa_topu_2` starts the redo.

## 2026-11-21 — Claude via Claude Code (cloud session) — `pokemon_unite`, `rush_royale`, games rule
- What: Pokémon UNITE first with characters (shipped), then — after the owner's new rule "Karakter
  yok, oyunun nesnesi" — redone with objects only: gold goal ring on a post + energy ball
  (B = Symbol/Disc/Rimmed, A = Faithful); Rush Royale with objects only: wizard hat with gold crown
  band + magenta gem + two ice crystals (C = Symbol/Faithful/Rimmed, D round tile = Disc);
  REDESIGN.md §0 (talking to the owner) and §3b (games: objects, no characters).
- Owner: Pokémon UNITE: "B" / "A,A'daki halkanın içindeki mavi hilali kaldır." / "B'deki mavi hilali
  de kaldır. Simgeyi yaklaşık %10 büyüt, direği biraz kalınlaştır (32 px'te kaybolmasın)." /
  "Tamam, pakete ekle" (2026-11-21). Rush Royale: "C" / "D,Şapkanın kenarını kaynaktaki gibi daha
  geniş ve kıvrık yap, ortadaki taş pembe/macenta olsun." / "Simgeyi yaklaşık %10 büyüt…" /
  "Tamam, pakete ekle" (2026-11-21).
- PR: #14
- Open problems: both are a little thin (mass 0.36–0.37, WARN); the magenta gem is outside the HIG
  palette (his choice).

## 2026-11-21 — Claude via Claude Code (cloud session) — handoff docs (no icons changed)
- What: START-HERE.md (the only entry point; CLAUDE.md, AGENTS.md, GEMINI.md, QWEN.md point to it),
  `tools/next.py` (one next step per app + the owner's Turkish Q1/Q2 text; `--start-redo`),
  `tools/describe_icon.py` (an icon as text), `tools/stamps.py` (is a build/board current),
  docs/APPS.md (generated by `tools/pack_status.py`), this log, docs/PLAYBOOK.md (A–Z per state,
  decision tables, question templates), docs/playbook/ (Telegram, Aurex Browser, Pokémon UNITE,
  Rush Royale: pictures + annotated code + what went wrong), `work/_lib/objects.py` (32 ready
  GNOME objects) + docs/redesign/objects.png / OBJECTS.md; `pr_guard` LOG rule; selftest 29 checks;
  gate: `plain_shape` also catches a square tile/plate and checks the Symbol; one `mass` range for
  every slot of a redesign; clearer `holes` message; REDESIGN.md §5 sentence on marks printed on an
  object; metadata lines (`kind:`, `ladder:`, `characters:`) in the 7 redesigned design.md files and
  the owner's `redo:` line for `kafa_topu_2`.
- Why: the owner's PROMPT-BAGIMSIZLIK.md — any model must be able to continue without Claude.
- Tested: a smaller, weaker model (as a sub-agent) with only START-HERE.md and an invented app (`test_dummy`,
  deleted, never pushed), twice. Run 1 reached Q2 but chose "the logo on a tile" (the concept
  template's own example was a plate) — fixed. Run 2 drew four real objects (bottle, drop, mug, the
  mark as an object), 0 FAIL; its remaining findings were fixed (see the PR).
- PR: the `docs/handoff` pull request
- Open problems: a model without vision still cannot judge beauty — the owner's eye in Q1/Q2 is the
  only check of looks; `andvm`, `horus`, `aurex_browser` have no Symbol and no Q2 answer yet.

## 2026-11-22 — Claude via Claude Code (cloud session) — tools only (no icons changed)
- What: gradients no longer break into bands. `Grad` fill (any direction) in the vendored
  skill's obj.py (`solid`/`recess` paint it); `work/_lib/obj.py`: `gradient(slug, shape)`,
  `regions(slug)` (bands of one source gradient merged back, measured by how smoothly the colour
  runs across their border; cached in `work/<slug>/gradients.json`, git-ignored), `banded()`,
  `traced(gradients=True)`, `cutout()` paints `Grad`, `describe()` prints GRADIENT lines; the
  concept/redesign templates use `regions()`; gate `bands` (FAIL) + concept warnings in
  `next.py`/`concepts.py`; selftest +4; REDESIGN §5, PLAYBOOK#gradients, MISTAKES §3.
- Why: DeepSeek's Deezer concept A had melted bars; the owner: "gradyanlar bozuk. Onun için bir
  şey yapamaz mıyız? Depoya da ekleyelim." (2026-11-22)
- Tested: a synthetic gradient-bars source (not committed): old template -> bands, gate FAIL;
  new template -> smooth gradients, PASS. All 417 existing SVGs: 0 `bands` hits. selftest 33/33.
- PR: fix/gradients
- Open problems: the Deezer work is on the owner's machine (OpenCode), not in the repo — redraw
  its concept A with the new template (`regions()`) before Q1.

## 2026-11-22 — DeepSeek V4.1 Flash Free via OpenCode — `deezer`
- What: new Deezer redesign from the owner's OG multicolour logo: C (vinyl record half out of
  a light sleeve, silver rim, enlarged white label and bars) -> Symbol and Disc; A (the 10
  measured equaliser bars, one smooth source gradient per bar via `regions()`/`gradient()`) ->
  Faithful; D (cassette with the measured columns) -> Rimmed. Added to the pack in Media.
  Also merged `origin/fix/gradients` into `gem` before drawing, as the owner asked.
- Why: the owner's new app request; Q1 chose C, kept A and D, dropped B; after the first Q2 he
  asked to enlarge C's label and bars so they read at 32 px, changing nothing else.
- Owner: "Soru 1 cevabım: Ana tasarım C (plak). Kalsın: A ve D. B kalmasın." (2026-11-22);
  "tamam, pakete ekle ama Plağın ortasındaki beyaz etiketi ve içindeki renkli çubukları biraz
  büyüt, küçük boyutta da çubuklar seçilsin. Başka hiçbir şeyi değiştirme." (2026-11-22)
- PR: opened after this commit
- Open problems: Faithful mass 0.30 (WARN; the bar mark is naturally wide/short); C's label bars
  are readable but still small at 32 px; D visible_dark 0.56 is close to the 0.55 threshold.

## 2026-11-22 — Claude via Claude Code (cloud session) — tools + docs; `busuu`, `meta_ai`, `misspipe`, `termux`, `wlingua` registered
- What: public face (README EN/TR, CONTRIBUTING, issue forms, palette, Inkscape template, fastlane
  metadata, docs/RESEARCH.md, docs/ROADMAP.md, `tools/validate_pack.py` in the PR guard); gate
  `mark_size` + next.py state FIX_WARN (fix what a check can see before Q2); `tools/fetch_refs.py`
  (references from Play in 5 regions, F-Droid, IzzyOnDroid, Uptodown, GitHub - verified by the
  package in the code -, any --url; text for blind models); `work/_lib/categories.py` +
  docs/redesign/CATEGORIES.md (category -> object family, which objects are used); 4 music objects
  (`vinyl_record`, `cassette`, `speaker`, `headphones` with mark boxes); `category:`/`store:` lines in
  the 7 redesigned apps' design.md; five new apps from his request zips registered (sources only).
- Why: the owner (2026-11-22): "Sence ikon paketimiz yeterince iyi mi? ... insanların kurmasını,
  katkı sağlamalarını, ajanların çok iyi anlamasını istiyorum"; "ikide bir bana mesaj verip bunu, şunu,
  onu mu düzelteceksin?"; "tarza ve kategoriye uygun şekilde"; "ekran görüntülerini nasıl bulacak? ...
  GitHub, Uptodown, APKMirror ... her yerde"
- Tested: fetch_refs on his 92 apps: screenshots for 78 (Play + F-Droid alone: 59), text for 8,
  3 system apps, 3 nothing; mark_size on a synthetic record label (25 px WARN, 42 px PASS) and the
  redesigned apps (no new WARN); selftest 46/46. No pack icon changed.
- PR: improve/public (#17)
- Open problems: APKMirror/APKPure block scripts (403); Deezer's design.md (DeepSeek's branch) needs
  `category: music` after it is merged; the Bing/DuckDuckGo web search is not usable from scripts.

## 2026-11-22 — DeepSeek V4.1 Flash Free via OpenCode — `apple_music`
- What: pilot redesign of Apple Music in four different styles (REDESIGN §6): B pocket music
  player -> Symbol, A red note -> Faithful, D round speaker -> Disc, C headphones -> Rimmed;
  `pack_refresh` replaced the old apple_music PNG/SVG (4 files). 36 PASS, 0 WARN, 0 FAIL.
- Why: the owner's "redo every app icon the Gnomed way" request; this is the one pilot he
  approves before the batch.
- Owner: Q1 "Soru 1 cevabım: Ana tasarım B (cep müzik çalar). Kalsın: A, C ve D - hepsi.
  A -> Faithful, C -> Rimmed, D -> Disc." (2026-11-22); Q2 "1) Tamam, pakete ekle." (2026-11-22)
- PR: #20
- Open problems: Faithful mass 0.35 (at the limit), Disc legibility 0.739 (near the 0.72 limit),
  Rimmed mass 0.36; the red is the app's UI accent, the store icon itself is monochrome.

## 2026-11-22 — Claude via Claude Code (cloud session) — tools/rules only (no icons changed)
- What: batch-1 lessons as rules and checks: `slots` compares how the four styles look; `sun()`,
  `digital_display()`; reserved logo objects in categories.py; REDESIGN §5 nameable objects / real
  colours / other apps' logos; BATCH.md self-review step and fix-list answers.
- Why: the owner on DeepSeek's first 9 system apps: "Bozukluklar yok mu sence de?" … "Repoyu düzelt"
- Owner: "Repoyu düzelt ve promptu buna göre yaz" (2026-11-22)
- PR: #22
- Open problems: whether an object is "nameable" can only be checked by eye; the batch overview
  every 10 apps stays the owner's check.

## 2026-11-22 — Claude via Claude Code (cloud session) — tools/rules + fix lists (no icons changed)
- What: the owner's review of overview ara-2 written into the repository as fix lists
  (`work/{anker_soundcore,apple_music,chatgpt,termux_api,termux_boot,termux_widget,walpy}/fixes.md`);
  `next.py` state OWNER_FIX (and OWNER_FIXES_FIRST for every other app), group overview when done;
  gate `mark` (the measured mark in a layer named `mark` on every style: present, size, contrast,
  shape) with `put_mark()` / `mark_parts()` in obj.py; gate `same_object` (objects of all four
  styles per category); REDESIGN §5 "The mark stays", Faithful = closest to the logo; BATCH.md §1
  merges main at every session start and never resets the batch branch.
- Why: ara-2 — Apple Music and Soundcore lost their marks in every style, ChatGPT's bulb carried
  an "M", Apple Music took Deezer's cassette, Faithful was a turntable / a cardboard box.
- Owner: "Bıktım bana prompt vermenden, yaz depoya" (2026-11-22)
- PR: opened after this commit
- Open problems: the gate finds a mark only in a layer named `mark` (put_mark does it); apps
  redesigned before this rule warn until they are redone; whether an object is nameable is still
  checked by eye (the overview).


## 2026-11-23 — Claude via Claude Code (cloud session) — review of overview-3 as fix lists, rules (no icons changed)
- What: `work/{trendyolmilla,hepsiburada,qobuz,terminal_em_lat_r,mt_manager,enpara}/fixes-overview-3.md`
  (12 styles); REDESIGN §5 + BATCH step 6: cover the mark, a wordmark is a label, twins, objects of
  another category; gate `mark` measures contrast and visibility on the light AND the dark wallpaper.
- Why: overview-3 — wordmarks on plain tiles, a mark invisible on the light wallpaper, twin boxes,
  a platter that reads as a record player, unnameable discs and a robot-like microphone.
- Owner: "Bıktım bana prompt vermenden, yaz depoya" (2026-11-22) - his standing rule for reviews
- PR: opened after this commit
- Open problems: chatgpt Faithful (black knot) now warns on the dark wallpaper under the stricter
  gate; "cover the mark" and twins are checked by eye, not measured.

## 2026-11-23 — Claude via Claude Code (cloud session) — faster gate (same results; no icons changed)
- What: legibility_check.py: disc morphology through distance transforms on the mask's own box
  (the same pixels, 40 icons compared) and a result cache per SVG; check_icon.py: the whole result
  cached on its inputs (`.cache/check/`, `--no-cache` to force), lint and legibility in-process,
  each mark variant rendered once; export_png.py takes several SVGs (review.sh: one call).
  Build + next.py for qobuz: 33.6 s -> 11.7 s; a cold gate on 14 apps 143 s -> 40 s, identical JSON.
- Why: the owner: "hızlandırmak için ne yapılabilir?" (2026-11-23) - DeepSeek on the phone waits
  on these steps, not on the model.
- Owner: "Python'u hızlandır (Önerilen)" (2026-11-23)
- PR: opened after this commit
- Open problems: rendering (CairoSVG) and preview_sheet.py are now the slowest steps.

## 2026-11-22 — Claude via Claude Code (cloud session) — rule "pairs read as eyes", fix rounds (no icons changed here)
- What: REDESIGN §5 + BATCH step 6: two equal round things side by side read as eyes; next.py
  reads every `work/<slug>/fixes*.md` (one file per review round, no conflicts with the batch
  branch); BATCH §1 pulls the batch branch's own upstream. The Soundcore buds themselves are
  redrawn in a separate pull request into icons/redo-batch.
- Why: the owner's review of ara-2-fixed.png (Soundcore Faithful: the buds looked like eyes).
- Owner: "Tamam, o göz gibi çıkmış dediklerini kulaklık gibi yapsın. Ve sonra depoya atsın." /
  "Ya da sen yap o düzeltmeyi, sonra da o hatayı dokumana yaz ki sorun olmasın gelecekte" (2026-11-22)
- PR: opened after this commit
- Open problems: none.
