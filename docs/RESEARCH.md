# Research — how GNOME and other open icon projects work, and what Gnomed takes from them

Collected 2026-11-22 for the owner's request: *"Önce GNOME ve benzeri GNOME projelerini incele …
sonrasında bizim paketi iyileştirmek için PR aç."* Every rule that came out of it is now in
[REDESIGN.md](../REDESIGN.md) (§3 choosing the object, §5 keylines / thickness / flat faces / no
strokes). This file says **where each rule comes from**, so a model or a person can check it.

## 1. GNOME's own rules (Human Interface Guidelines → App Icons)

Source: [developer.gnome.org/hig/guidelines/app-icons](https://developer.gnome.org/hig/guidelines/app-icons.html).

| HIG says | Gnomed now |
|---|---|
| One simple, recognisable **metaphor** with a clear relation to the app's name or function: a physical object it uses, an object of its domain or an older analog form, a domain symbol, a simplified piece of its UI | REDESIGN §3 "Choosing the object" (+ the concept ladder) |
| Avoid metaphors unrelated to the name, **characters or mascots**, and logos that depend on a specific visual style | REDESIGN §3b (games: no characters); mascot apps are on the redo list ([ROADMAP](ROADMAP.md)) |
| Simple, geometric — many icons are only basic shapes. **Not flat**: depth comes from a bottom **profile** (the object's front), darker than the top; usually no taller than 2 detail units (**4 px**) | REDESIGN §5 Thickness 2–4 px by default |
| Draw in 128 × 128 without filling it; size with the **template guides** so the visual weight matches; avoid extreme aspect ratios; bottom on the **baseline** | REDESIGN §5 keylines + [docs/template/](template/) ; gate `baseline`, `mass`, `size_audit` |
| Materials (wood, metal, glass) only when needed; base colours from the **standard palette** | REDESIGN §5 palette + [docs/palette/](palette/) |
| **Flat colours on straight surfaces, gradients on curved ones**; no shadows where possible, light straight from above; no shadows outside the silhouette | REDESIGN §5 "Flat faces flat" |
| Defined at 128, seen at 64, down to 32: avoid excessive detail, follow the 2 px grid | gate `legibility32`; REDESIGN §5 "Edges on the 2 px grid" |
| Every app has a **symbolic** (monochrome 16 px) version | not done — note: Gnomed's *Symbol* style is NOT GNOME's *symbolic*; a monochrome style is an idea in [ROADMAP](ROADMAP.md) |
| Nightly / beta builds get a distinct variant | done for Firefox Beta / Nightly |

### The template (gitlab.gnome.org/Teams/Design/HIG-app-icons, `template.svg`)

Keylines measured from the file (relative to its 128 px canvas): **circle** centre 64,64 r 59.5;
**square** 12.5…115.5 (103 px); **tall rectangle** 20.5…107.5 × 8.5…119.5 (87 × 111); **wide
rectangle** 8.5…119.5 × 28.5…115.5 (111 × 87); corner radius ≈ 8; **baseline** a 2 px line at
y = 117 (116…118). Gnomed's own template with the same numbers: [docs/template/gnomed-template.svg](template/gnomed-template.svg).

### The palette (same repository, `GNOME HIG.gpl`)

45 colours: Blue, Green, Yellow, Orange, Red, Purple, Brown, Light 1–5 and Dark 1–5 — identical
to `RAMP` in `work/_lib/objects.py` except Dark 5 (`#000000`), which Gnomed never uses. Exported
for every program by `tools/make_palettes.py` → [docs/palette/](palette/).

### The designers' process (Tobias Bernard, "Designing an Icon for Your App", 2019)

Source: [blogs.gnome.org/tbernard/2019/12/](https://blogs.gnome.org/tbernard/2019/12/).

1. **List physical objects** related to the app, widen the list with a thesaurus; drop the ones
   that are too generic ("a book is probably too generic" for a reading-list app), too stylised,
   random, or mascots. → Gnomed's 4 concepts per app (Q1) are this list, drawn.
2. **Sketch** several, on the template shapes; a distinctive overall silhouette helps.
3. Build from **rectangles and circles**; design for 64 px, check 32 px; edges on the 8 px grid
   where possible. → `objects.py` (32 ready objects), `legibility32`.
4. **Perspective**: fold the top view and the front view together, the darker "chin" at the
   bottom. Folding from the top or the back looks wrong.
5. Colour example (a bookshelf): top Brown 3, chin Brown 4–5, corner highlights Brown 2–3 —
   the "three steps of one ramp" rule in REDESIGN §5.
6. Mistakes he lists: too generic / too stylised / random / mascot metaphors, wrong perspective
   fold, drop shadows, heavy inner shadows, off-grid drawing.

## 2. Community icon sets for third-party apps

### MoreWaita — Adwaita-style icons for non-GNOME apps (Linux)

Source: [github.com/somepaulo/MoreWaita](https://github.com/somepaulo/MoreWaita) (GPL-3.0, ~1.1 k stars,
518 app SVGs + ~950 symlinked aliases, checked 2026-11-22).

- **Brand icons stay close to the original logo** ("to the point of using them in full") with
  Adwaita's flatness, perspective and a **4 px chin**, and **keep brand colours**. Measured in the
  skill (`tools/gnome-android-icons/references/community-themes.md`): circles 120 × 122, squares
  104 × 104, median 5 paths.
- Contributing rules: avoid strokes, no mesh gradients, plain SVG, start from an existing icon of
  a similar shape, use GNOME's template, every app icon has a symbolic twin, one app per PR.
- What Gnomed takes: one app per PR, plain SVG, no strokes, template sizes. What it does not:
  "logo + chin" is exactly what the owner rejected ("orijinal logoya sadece gölge eklenmiş gibi");
  in Gnomed that level is at most the **Faithful** slot, never the Symbol.


### Delta — a large open-source Android icon pack (CandyBar, like Gnomed)

Source: [github.com/Delta-Icons/android](https://github.com/Delta-Icons/android) (~890 stars, 13 k+ vector icons).

- **Palette files** in `resources/palettes/`: `palette.ase` (Illustrator), `palette.gpl`
  (Inkscape, Karbon), `palette.svg` + a simplified palette; a few named colours and fixed white /
  black overlay opacities. → Gnomed now has `docs/palette/` (`.gpl`, `.ase`, `.json`, `.css`, sheet).
- Canvas 192 px; strict naming (`lowercase_underscores`, `_alt_N` for old versions — never
  overwrite an icon, rename it and keep the old ComponentInfos linked).
- **Requests are data**: `contribs/requests.yml` (ComponentInfo → name, request count, store
  links), updated by a workflow; contributors pick from it. A CI job checks new icons for
  conflicts on every PR. → Gnomed: `tools/validate_pack.py` in the PR guard.
- Distribution: GitHub Releases + Google Play + **F-Droid (foss flavour)** + **Obtainium** links;
  `metadata/en-US/` (title, short/full description, screenshots, changelogs) for F-Droid-style
  stores. → Gnomed now has `fastlane/metadata/android/` and an Obtainium link in the README.

### Arcticons — line icons, very large community

Source: [github.com/Arcticons-Team](https://github.com/Arcticons-Team) (guides such as the Inkscape guide).
Lesson: a short, picture-heavy contributor guide per tool (Inkscape, Illustrator…) brings many
human contributors. → Gnomed's new short [CONTRIBUTING.md](../CONTRIBUTING.md) with an Inkscape path.

## 3. Honest review of the pack (2026-11-22)

What a GNOME user notices first, from the Symbol contact sheet of all 96 apps
(`python3 tools/readme_previews.py` → [docs/images/preview.png](images/preview.png)):

1. **Two languages mixed.** 6 apps are real GNOME objects (Telegram, Pokémon UNITE, Rush Royale,
   Aurex Browser, Horus, AnDVM); ~90 are earlier versions (automatic or hand-built) — mostly the brand
   logo with some depth. Side by side, the automatic ones look unfinished.
2. **Outlines.** Several icons are thin line art (Apple Music note, ChatGPT knot, Termux `>_`,
   Walpy) — GNOME app icons never are.
3. **Logos on tiles / wordmarks** (Anker Soundcore, Trendyol Milla, Hepsiburada, Qobuz, Terminal
   Emulator, MT Manager) — the HIG's "logos that depend on a specific visual style".
4. **Mascots and faces** (Kafa Topu 2 — redo agreed —, Duolingo, Reddit, Android robots).
5. **Uneven weight**: very light icons (Today Weather, Binance TR, Data Backup, Stride: painted
   area < 30 %) next to heavy tiles.
6. **System apps** (Ayarlar, Saat, Kamera, Telefon, Mesajlar, Kişiler, Hesap Makinesi…) have an
   obvious GNOME answer (GNOME's own Settings, Clocks, Snapshot, Calls, Chatty, Contacts,
   Calculator) but do not use it yet.

Cause: not too little research — the first pipeline was built to *measure and keep* logos, and
the "object" rules came later. The order to fix it is in [ROADMAP.md](ROADMAP.md).

## 4. Sources

- GNOME HIG, App Icons — https://developer.gnome.org/hig/guidelines/app-icons.html
- GNOME HIG app-icon templates and palette — https://gitlab.gnome.org/Teams/Design/HIG-app-icons
- Tobias Bernard, Designing an Icon for Your App — https://blogs.gnome.org/tbernard/2019/12/
- MoreWaita — https://github.com/somepaulo/MoreWaita (README, CONTRIBUTING.md)
- Delta Icons for Android — https://github.com/Delta-Icons/android (README, CONTRIBUTING.md, workflows)
- Arcticons — https://github.com/Arcticons-Team/Arcticons (guides/)
