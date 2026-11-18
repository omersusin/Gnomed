# Icon requests

`inbox/` holds icon requests exported from the maintainer's phone, for contributors and
AI agents who cannot receive e-mail or zip files.

**Maintainer:** on GitHub, *Add file → Upload files* into `requests/inbox/` (any of the
formats below; a dated folder such as `inbox/2026-11-18/` keeps batches apart).

**Contributors / agents:**

```bash
python3 tools/import_request.py requests/inbox/<file or folder>          # list: NEW / NO-ICON / IN-PACK
python3 tools/import_request.py requests/inbox/<file or folder> --add --only <slug>
```

Accepted formats (from Gnomed's *Request* screen → send → choose a way, or other apps):

| Format | Contents |
|---|---|
| Gnomed zip (e-mail / "Share or save the zip") | `appfilter.xml` + `<drawable>.png` |
| Gnomed "Share as images + text (no zip)" | `request.txt` + `<drawable>.png` |
| Gnomed "Copy the app list" (saved as `.txt`) | `App \| ComponentInfo{…} \| file.png` lines (no icons) |
| IconRequest app (de.kaiserdragon.iconrequest) zip | `appfilter.xml` + `icons/<drawable>.png` |

Do not delete or rename files here — the maintainer cleans the inbox.
