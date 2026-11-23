# chatgpt - fixes from the audit (2026-11-23): today's gates on the finished icon
group: audit-2026-11-23
owner: "şu ana kadar yaptığı simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın" (2026-11-23)
review: python3 tools/audit.py (2026-11-23)
shown: 2026-11-23

Fix EXACTLY these styles (scope 'app' = the whole app). A gate that is wrong for this design:
do not change the icon - write 'warn-ok: <check> - <why, one plain sentence>' in design.md and tick
the line with '-> now: warn-ok'. How: docs/PLAYBOOK.md#owner-fix and #fix-warn

- [x] faithful: gate empty_layer FAIL (knot-inner) - these layers are EMPTY - the part is missing from the icon: rounded(g, r) needs r < half the part's thinnest side; check intersections/differences; or delete the layer if the part is not wanted -> now: the part is drawn again (rounded() never erases a whole part; sun() edge fixed; chatgpt's empty knot-inner layer removed)
- [x] faithful: gate mark WARN (107 px of 128, contrast 13, shape match 0.53, visible 78% - does not stand out) - the mark melts into what is under it (measured on the light AND the dark wallpaper): a white/light mark on a dark part, a dark or strong-coloured mark on a light part; a mark standing on nothing needs a colour that reads on both wallpapers, or a part behind it (put_mark(..., face="#ffffff") / a darker ramp step) -> now: the knot is mid grey with a lighter side: reads on both wallpapers (gate PASS)
- [x] symbol: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] faithful: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] disc: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
- [x] rimmed: gate anchors WARN (0 anchor(s) say where they were seen) - design.md anchors: 2-4 things that make THIS app recognisable, each '- <where>' (source.png, refs/store/shot-N.jpg): look at the logo AND the screenshots, not at the category -> now: design.md anchors 1, 2 say where they were seen (source.png) and every concept line cites them; the styles carry the measured mark in its colours
