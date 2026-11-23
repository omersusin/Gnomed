# kamera - fixes from the audit (2026-11-23): today's gates on the finished icon
group: audit-2026-11-23
owner: "şu ana kadar yaptığı simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın" (2026-11-23)
review: python3 tools/audit.py (2026-11-23)
shown:

Fix EXACTLY these styles (scope 'app' = the whole app). A gate that is wrong for this design:
do not change the icon - write 'warn-ok: <check> - <why, one plain sentence>' in design.md and tick
the line with '-> now: warn-ok'. How: docs/PLAYBOOK.md#owner-fix and #fix-warn

- [ ] rimmed: gate same_object WARN (picture frame - also used by foto_raflar) - pick a FREE object of the category's family for this style (python3 tools/next.py kamera lists USED/free) - BATCH.md 7: two apps of one category never share an object
