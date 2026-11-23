# termux_boot - fixes from the audit (2026-11-23): today's gates on the finished icon
group: audit-2026-11-23
owner: "şu ana kadar yaptığı simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın" (2026-11-23)
review: python3 tools/audit.py (2026-11-23)
shown:

Fix EXACTLY these styles (scope 'app' = the whole app). A gate that is wrong for this design:
do not change the icon - write 'warn-ok: <check> - <why, one plain sentence>' in design.md and tick
the line with '-> now: warn-ok'. How: docs/PLAYBOOK.md#owner-fix and #fix-warn

- [x] rimmed: gate mark_fit WARN (over the edge 7%, room to the edge 0.5 u, covered 7%) - the mark runs off, touches the edge of, or is covered on the part it sits on (a label, lid, screen, disc): make the mark SMALLER or the part BIGGER so it keeps >= 1 unit of room on every side, and draw nothing over it (a CD hole, a handle, a strap goes under it or elsewhere). Check with: python3 tools/check_icon.py SLUG -> now: the mark sits inside its part with >= 1 unit of room, nothing over it (gate PASS)
- [x] symbol: gate mark_fit WARN (over the edge 3%, room to the edge 0.5 u, covered 0%) - the mark runs off, touches the edge of, or is covered on the part it sits on (a label, lid, screen, disc): make the mark SMALLER or the part BIGGER so it keeps >= 1 unit of room on every side, and draw nothing over it (a CD hole, a handle, a strap goes under it or elsewhere). Check with: python3 tools/check_icon.py SLUG -> now: the mark sits inside its part with >= 1 unit of room, nothing over it (gate PASS)
- [x] symbol: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] faithful: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] disc: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] rimmed: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
