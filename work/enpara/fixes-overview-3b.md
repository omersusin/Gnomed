# enpara - fixes, round 2 (Claude's review of overview-3-fixed for the owner)
group: overview-3b
owner: "Başla" (2026-11-23) - after "Bekle ben başla diyince yaz"; standing rule: reviews go into the repository
review: overview-3-fixed.png (2026-11-23)
shown: 2026-11-23

Change EXACTLY this style; the others stay. How: docs/PLAYBOOK.md#owner-fix

- [x] faithful: the letters SINK into the four-colour stripe - their side (depth 6) runs from y 94 to 100 over the stripe, because the put_mark box ends at y 94, the stripe's top. With anchor='bottom' the side adds `depth` BELOW the box: end the box `depth` above the surface - put_mark(ic, SLUG, (20, 34, 108, 88), depth=6, anchor='bottom', ...) - so the letters STAND on the stripe and nothing of them covers it -> now: put_mark box (20, 34, 108, 88) with depth 6 and anchor bottom, so the side ends exactly on the stripe top at y 94 - the letters stand on the stripe, nothing of them covers it (legibility 0.839)
