#!/usr/bin/env python3
"""Re-check the icons the batch already finished, with TODAY's gates (docs/BATCH.md 1).

    python3 tools/audit.py              # the batch's apps (design.md 'approved: ... "batch: ...')
    python3 tools/audit.py <slug> ...   # only these apps
    python3 tools/audit.py --all        # every redesigned app
    python3 tools/audit.py --dry-run    # only print, write nothing

Gates get stricter as the owner finds new kinds of mistakes (2026-11-23: "şu ana kadar yaptığı
simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın"). An icon that passed yesterday can
fail today's gate. For every app whose must-fix gates (next.py MUST_TRY, and every FAIL) now
complain - and no 'warn-ok:' in its design.md covers it - this writes
    work/<slug>/fixes-audit-<date>.md
one line per style and gate, with the gate's own FIX. That is the same fix-list flow as the
owner's reviews: next.py shows OWNER_FIX for those apps before any other app, and prints the
overview of the group when all are done. Nothing else is changed. An app that already has an
open audit list is left alone (finish that one first).
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import next as NX  # noqa: E402


def batch_apps():
    out = []
    for d in sorted((ROOT / "work").glob("*/design.md")):
        text = d.read_text(encoding="utf-8")
        if '"batch' in NX.line(text, "approved") and (d.parent / "redesign.py").exists():
            out.append(d.parent.name)
    return out


def all_redesigned():
    return sorted(d.parent.name for d in (ROOT / "work").glob("*/redesign.py") if not d.parent.name.startswith("_"))


def problems(slug):
    text = (ROOT / "work" / slug / "design.md").read_text(encoding="utf-8")
    rows = NX.check_rows(slug)
    bad = []
    for r in rows:
        if r["status"] == "FAIL" or (r["status"] == "WARN" and r["check"] in NX.MUST_TRY
                                     and not NX.warn_ok(text, r["check"])):
            bad.append(r)
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    slugs = args or (all_redesigned() if "--all" in sys.argv else batch_apps())
    today = date.today().isoformat()
    group = f"audit-{today}"
    wrote, clean = [], []
    for i, slug in enumerate(slugs, 1):
        print(f"[{i}/{len(slugs)}] {slug} ...", end=" ", flush=True)
        if any(p.name.startswith("fixes-audit") and NX.read_fixes(p)[0] for p in NX.fix_files(slug)):
            print("has an open audit list - finish it first")
            continue
        bad = problems(slug)
        if not bad:
            print("ok")
            clean.append(slug)
            continue
        print(f"{len(bad)} problem(s)")
        lines = []
        for r in bad:
            fix = " ".join(str(r.get("fix") or "").split())
            lines.append(f"- [ ] {r['scope']}: gate {r['check']} {r['status']} ({r['value']}) - {fix}")
        body = (f"# {slug} - fixes from the audit ({today}): today's gates on the finished icon\n"
                f"group: {group}\n"
                f"owner: \"şu ana kadar yaptığı simgelerin üzerinden geçsin ve gelecekte hiç hata yapmasın\" (2026-11-23)\n"
                f"review: python3 tools/audit.py ({today})\n"
                f"shown:\n\n"
                "Fix EXACTLY these styles (scope 'app' = the whole app). A gate that is wrong for this design:\n"
                "do not change the icon - write 'warn-ok: <check> - <why, one plain sentence>' in design.md and tick\n"
                "the line with '-> now: warn-ok'. How: docs/PLAYBOOK.md#owner-fix and #fix-warn\n\n"
                + "\n".join(lines) + "\n")
        if not dry:
            (ROOT / "work" / slug / f"fixes-audit-{today}.md").write_text(body, encoding="utf-8")
        wrote.append(slug)
    print()
    print(f"clean: {len(clean)}   with problems: {len(wrote)}" + ("   (dry run: nothing written)" if dry else ""))
    if wrote and not dry:
        print("Fix lists written. Next: python3 tools/next.py   (it lists them first: OWNER_FIX)")


if __name__ == "__main__":
    main()
