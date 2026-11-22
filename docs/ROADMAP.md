# ROADMAP — what makes Gnomed better next (a proposal; the owner decides the order)

Why this order: [docs/RESEARCH.md](RESEARCH.md) §3 (the honest review). Each app is one session
with any model: `python3 tools/next.py <slug>` (an app already in the pack starts at
NOT_STARTED and keeps its old icon until the owner approves the new one in Q2). No zip and no
new request are needed — the source logo is already in `work/<slug>/source.png`.

## 1. Redo the existing icons, best value first

**Batch (2026-11-22):** the owner wants every icon redone, including the apps redone before
(Telegram, Pokémon UNITE, Rush Royale, Deezer, Apple Music) — procedure: [BATCH.md](BATCH.md).

| # | Group | Apps (slugs) | Why first | The object (start point for Q1) |
|---|---|---|---|---|
| 1 | **System apps** — seen every day | `ayarlar`, `saat`, `kamera`, `telefon`, `mesajlar`, `ki_iler`, `hesap_makinesi`, `y_hava_durumu`, `foto_raflar` | GNOME has the answer: its own app for the same job | Settings gears · Clocks · Snapshot lens · Calls handset · Chatty bubble · Contacts card · Calculator · Weather · Loupe photo |
| 2 | **Outline / line art** | `apple_music`, `chatgpt`, `termux_api`, `termux_boot`, `termux_widget`, `walpy` | GNOME icons are never outlines | a solid note on a speaker/record · the knot as a solid object · a terminal window with `>_` on its screen · a picture/wallpaper frame |
| 3 | **Logo on a tile, wordmarks** | `anker_soundcore`, `trendyolmilla`, `hepsiburada`, `qobuz`, `terminal_em_lat_r`, `mt_manager`, `enpara` | "logo on a plate" — the thing the owner rejects | speaker/earbuds case · shopping bag · parcel/bag · record/headphones · terminal · folder/archive · card/coin |
| 4 | **Mascots, faces** | `kafa_topu_2` (redo agreed), `duolingo`, `reddit`, `f_droid`, `payload_dumper`, `scene`, `iconrequest` | HIG: no mascots | ball + boot · book/flashcard · speech bubble/antenna · bag/box with the mark · a package · … |
| 5 | **Light icons** (painted area < 30 %) | `today_weather`, `binance_tr`, `databackup`, `stride`, `bcr`, `midas`, `mornye`, `kadraj` | they look small among neighbours | a bigger object, or a secondary object in front |
| 6 | the rest | see [APPS.md](APPS.md) | | |

Within a group: the apps on the owner's home screen first.

**New requests (registered 2026-11-22, not in the pack yet):** `busuu`, `meta_ai`, `misspipe`, `termux`,
`wlingua` (from his request zips; `deezer` is being done in its own session). Start each with
`python3 tools/next.py <slug>`; `tools/fetch_refs.py` already finds all five (Play / GitHub).

Every app: its **category's object family** (docs/redesign/CATEGORIES.md) — e.g. Apple Music, Qobuz,
BitChord, Mochy and Deezer are all `music`, so they share out record, cassette, speaker, headphones,
player and radio instead of five records.

## 2. Getting Gnomed to people

- [x] README with pictures, download links and an **Obtainium** button (this PR).
- [x] `fastlane/metadata/android/` (title, descriptions EN + TR, screenshots, icon) — what
      F-Droid-style stores read.
- [ ] **IzzyOnDroid / F-Droid**: probably **not** possible now. IzzyOnDroid's inclusion policy
      (https://izzyondroid.org/docs/general/AppInclusionPolicy/, checked 2026-11-22) rejects
      "vibe-coded" apps whose code contains LLM output, and asks for explicit opt-in before an
      app downloads APKs (Gnomed's style switcher does). **Obtainium** (GitHub releases) is the
      realistic channel; the fastlane metadata is ready if that changes.
- [ ] A fresh **release** after the redone icons land (the last one, v1.0.24, is from 18 Nov).
- [ ] GitHub repository settings (owner, 1 minute): description, topics `icon-pack`,
      `gnome`, `adwaita`, `android`, `candybar`, and the website field → the README.

## 3. Ideas (only if the owner wants them)

- **Monochrome style** (GNOME's *symbolic* icons, Android 13+ "themed icons" look): one colour,
  2 px strokes, tinted by the wallpaper. A fifth APK flavour; all icons generated from the
  Symbol shapes' silhouettes, checked by hand.
- **MoreWaita as a reference board**: for apps that MoreWaita has, show its icon on the Q1 board
  next to the source (as a reference only, GPL-3.0 credited) — never shipped as Gnomed's design.
- **Dynamic calendar icon** (CandyBar supports it) in the GNOME Calendar look.
- **Request list as data** (like Delta's `contribs/requests.yml`): every request with a count,
  so the most requested apps are done first.
