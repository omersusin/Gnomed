## What

<!-- e.g. "Add 6 apps: …" / "Fix banding in exteraless" -->

## Apps and sources

| App | slug | ComponentInfo source (icon request / adb / APK) | Styles (F/D/R/S) |
|---|---|---|---|
|  |  |  |  |

## Boards

<!-- drag in work/<slug>/styles.png (and review.png for hand-built icons) -->

## Checks

- [ ] `lint_svg.py`: 0 FAIL
- [ ] `pack_audit.py`: no new ERROR
- [ ] I looked at every style on light and dark, and at 32 px
- [ ] `pack_add.py --dry-run` diff was additive only
- [ ] No image-generation model was used; geometry is measured from the source
- [ ] No keystore / secrets / applicationId / flavor changes

## Known weaknesses

<!-- be honest: what is still not great -->

## Not verified

<!-- e.g. not tested on a real launcher -->

## Made with an AI agent?

<!-- no / yes: which tool + model -->
