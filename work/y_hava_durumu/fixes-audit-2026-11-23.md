# y_hava_durumu - fixes from the audit (2026-11-23): today's gates on the finished icon
group: audit-2026-11-23
owner: "şu ana kadar yaptığı simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın" (2026-11-23)
review: python3 tools/audit.py (2026-11-23)
shown: 2026-11-23

Fix EXACTLY these styles (scope 'app' = the whole app). A gate that is wrong for this design:
do not change the icon - write 'warn-ok: <check> - <why, one plain sentence>' in design.md and tick
the line with '-> now: warn-ok'. How: docs/PLAYBOOK.md#owner-fix and #fix-warn

- [x] disc: gate empty_layer FAIL (sun-edge-side, sun-edge-face) - these layers are EMPTY - the part is missing from the icon: rounded(g, r) needs r < half the part's thinnest side; check intersections/differences; or delete the layer if the part is not wanted -> now: the part is drawn again (rounded() never erases a whole part; sun() edge fixed; chatgpt's empty knot-inner layer removed)
- [x] symbol: gate empty_layer FAIL (sun-edge-side, sun-edge-face) - these layers are EMPTY - the part is missing from the icon: rounded(g, r) needs r < half the part's thinnest side; check intersections/differences; or delete the layer if the part is not wanted -> now: the part is drawn again (rounded() never erases a whole part; sun() edge fixed; chatgpt's empty knot-inner layer removed)
