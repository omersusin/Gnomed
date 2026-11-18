# Sources (what was studied for this skill, 2026-11-05)

Everything the agent needs is bundled; these links are for provenance and for
refreshing the knowledge base later. Network access is never required to use
the skill.

## GNOME official
- HIG: https://developer.gnome.org/hig/ - App Icons: https://developer.gnome.org/hig/guidelines/app-icons - Tools: https://developer.gnome.org/hig/resources - Palette: https://developer.gnome.org/hig/reference/palette.html - UI/symbolic icons: https://developer.gnome.org/hig/guidelines/ui-icons.html - Themed icons: https://developer.gnome.org/documentation/tutorials/themed-icons.html
- HIG-app-icons (template, palette): https://gitlab.gnome.org/Teams/Design/HIG-app-icons (bundled copy: `assets/template/`)
- Tobias Bernard, *Designing an Icon for Your App*: https://blogs.gnome.org/tbernard/2019/12/30/designing-an-icon-for-your-app/
- App Icon Preview: https://flathub.org/apps/org.gnome.design.AppIconPreview
- Adwaita icon theme: https://github.com/GNOME/adwaita-icon-theme (36 full-colour device/place/mimetype icons bundled)
- Official app icons: 66 icons from GNOME core + games repos via https://github.com/GNOME/<repo> mirrors (Totem, Snapshot, Calendar, Nautilus, Epiphany, Clocks, ...). Exact repo, path and commit per file: `assets/reference-library/catalog.json`.
- GNOME Circle / GNOME-styled apps (32): Mousai, Kooha, Delineate (SeaDve), Dialect, Blanket, Forge Sparks, Tangram, Junction, Commit, Workbench, Biblioteca, Eyedropper, Hieroglyphic, Flowtime, Paper Clip, Curtail, Alpaca, Bottles, Keypunch, Fretboard, Warehouse, Wike, Cartridges, Gear Lever, Extension Manager, Errands, Color Code, Flatseal, Tuba family (Archives, Calligraphy, Collision, Turntable) - see catalog for URLs.

## Community Adwaita-style (studied from the user's archives, not bundled)
- MoreWaita: https://github.com/somepaulo/MoreWaita (README, CONTRIBUTING)
- Adwaita++: https://github.com/Bonandry/adwaita-plus

## Android / icon packs
- CandyBar: https://github.com/zixpo/candybar (commit 0aa2f57, read `IconsHelper.java`, `RequestHelper.java`)
- CandyBar sample: https://github.com/zixpo/candybar-sample (commit 3bf109c)
- Adding icons: https://github.com/zixpo/candybar-sample/wiki/Adding-icons-and-making-them-work
- Adaptive icons: https://developer.android.com/develop/ui/compose/system/icon_design_adaptive
- `adb shell cmd package resolve-activity` / `query-activities` (Android package manager shell)

## Skill format
- Agent Skills spec: https://agentskills.io/specification
- Claude Code skills: https://code.claude.com/docs/en/skills
- Codex skills: https://developers.openai.com/codex/skills (redirects to learn.chatgpt.com/docs/build-skills)
- OpenCode skills: https://docs.opencode.ai/docs/skills/

## Licences
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/ - CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/ - GNU licences: https://www.gnu.org/licenses/
- Texts bundled in `assets/reference-library/licenses/`.

## Not reachable from the build environment (honesty note)
gitlab.gnome.org and developer.gnome.org could not be fetched directly from the
build sandbox; the HIG pages were read through a web fetcher and the GNOME
repos through their official GitHub mirrors. Some GNOME apps without a GitHub
mirror (e.g. Screenshot, Cheese, Podcasts, Fractal) are therefore not in the
bundled library.
