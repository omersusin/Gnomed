#!/usr/bin/env python3
"""Self-test of the checks the agent cannot pass by itself (DUZELTME-PLANI Part D).

    python3 tools/selftest.py        -> "selftest: N passed, 0 failed", exit 1 on any failure

1. the 8 apps of PR #12 PASS the `holes` check (their Symbol holes are real holes)
2. a Symbol with PAINTED letter counters / eyes (the pre-PR #12 qobuz and discord SVGs from
   git history) FAILs the `holes` check
3. `approved: yes` FAILs the `redesign` approval format; a quote + date passes
4. obj.poly() rounds corners without erasing thin parts; obj.body() keeps the holes
5. the handoff tools: tools/next.py (states), tools/describe_icon.py, work/_lib/objects.py,
   the docs/LOG.md rule of tools/pr_guard.py
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "work/_lib"))
_spec = importlib.util.spec_from_file_location("check_icon", ROOT / "tools/check_icon.py")
ci = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ci)

ok = bad = 0


def expect(cond, what):
    global ok, bad
    print(("PASS  " if cond else "FAIL  ") + what)
    ok, bad = ok + bool(cond), bad + (not cond)


def holes_status(slug, svg):
    """the check_icon rule, on one SVG: (status, source %, transparent %)"""
    src, transp, _iou = ci.hole_measure(slug, svg)
    if src < 0.004:
        return "PASS", src, transp
    return ("PASS" if transp >= 0.5 * src else "FAIL"), src, transp


def run_json(slug):
    out = subprocess.run([sys.executable, str(ROOT / "tools/check_icon.py"), slug, "--json"],
                         capture_output=True, text=True, cwd=ROOT).stdout
    return json.loads(out[out.index("["):])


# 1. PR #12 apps: real holes
for slug in ("qobuz", "discord", "saat", "trestle", "swift_backup", "obtainx", "thunderbird", "scene"):
    rows = [r for r in run_json(slug) if r["check"] == "holes"]
    expect(rows and all(r["status"] == "PASS" for r in rows), f"holes PASS for {slug}: {rows[0]['value'] if rows else 'no row'}")

# 2. painted counters (before PR #12) must FAIL
with tempfile.TemporaryDirectory() as tmp:
    for slug, rev in (("qobuz", "711fb99"), ("discord", "711fb99")):
        txt = subprocess.run(["git", "show", f"{rev}:work/{slug}/{slug}-symbol.svg"], capture_output=True, text=True, cwd=ROOT).stdout
        if not txt:
            expect(False, f"git history has {slug}-symbol.svg at {rev}")
            continue
        p = Path(tmp) / f"{slug}-painted.svg"
        p.write_text(txt, encoding="utf-8")
        st, src, tr = holes_status(slug, p)
        expect(st == "FAIL", f"painted {slug} Symbol FAILs holes (source {src:.1%} -> transparent {tr:.1%})")

# 3. approval format
expect(not ci.is_quote("yes"), "approved: yes FAILs the redesign approval format")
expect(not ci.is_quote("A - the hat with crown (owner: oyuna uygun)"), "an approval without quotes + date FAILs")
expect(ci.is_quote('B - "Bunu seçtim" (2026-11-21)'), "a quoted, dated approval passes")

# 4. obj helpers
from obj import poly, body  # noqa: E402
expect(poly([(0, 0), (40, 0), (40, 3), (0, 3)], 4).area > 100, "poly(): a 3-unit thin part survives r=4")
expect(poly([(0, 0), (40, 0), (40, 40), (0, 40)], 6).area < 1580, "poly(): convex corners are rounded")
b = body("qobuz")
expect(sum(len(g.interiors) for g in getattr(b, "geoms", [b])) > 0, "body(qobuz) keeps the letter counters as holes")

# 5. handoff tools
def run(*cmd):
    r = subprocess.run([sys.executable, *cmd], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def state(slug):
    code, out = run("tools/next.py", slug)
    m = [ln.split()[1] for ln in out.splitlines() if ln.startswith("STATE")]
    return m[0] if m else f"no STATE line (exit {code}): {out[-200:]}"


on_main = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() in ("main", "master")
if on_main:
    expect(state("rush_royale") == "ON_MAIN", "next.py refuses to work on main")
else:
    expect(state("zz_no_such_app") == "NO_SOURCE", "next.py: an unknown app -> NO_SOURCE")
    expect(state("kafa_topu_2") == "REDO", "next.py: kafa_topu_2 (owner's redo: line) -> REDO")
    expect(state("qobuz") == "NOT_STARTED", "next.py: a plate app -> NOT_STARTED")
    expect(state("andvm") == "BUILD", "next.py: a redesign without a Symbol -> BUILD")
    st = state("rush_royale")
    expect(st in ("LOG", "COMMIT", "PUSH", "DONE"), f"next.py: a shipped redesign is past Q2 ({st})")
code, out = run("tools/next.py")
expect(code == 0 and "Which app next?" in out, "next.py without a slug lists the next apps")
code, out = run("tools/describe_icon.py", "work/pokemon_unite/pokemon_unite-symbol.svg")
expect(code == 0 and "box:" in out and "holes: 1" in out and "ASCII" in out, "describe_icon.py describes an SVG (box, holes, ASCII)")
import objects as O  # noqa: E402
broken = []
for fname, kw, _ in O.CATALOGUE:
    try:
        g = getattr(O, fname)(O.gk.Icon(fname), 64, 118, 90, **kw)
        if g.is_empty or g.bounds[3] > 118.5:
            broken.append(fname)
    except Exception as e:  # noqa: BLE001
        broken.append(f"{fname}: {e}")
expect(not broken, f"objects.py: all {len(O.CATALOGUE)} objects build inside the baseline {broken or ''}")
with tempfile.TemporaryDirectory() as tmp:
    t = O.gk.Icon("tile")
    O.solid(t, O.rounded(O.box(14, 14, 114, 112), 16), face="#33d17a", depth=6)
    O.solid(t, O.circ(64, 60, 22), face="#ffffff", depth=2)
    t.save(Path(tmp) / "tile.svg")
    expect(ci.shape_kind(Path(tmp) / "tile.svg")[0] == "tile", "check_icon.shape_kind: the logo on a rounded tile -> 'tile' (plain_shape WARN)")
expect(ci.shape_kind(ROOT / "work/pokemon_unite/pokemon_unite-symbol.svg")[0] == "object", "check_icon.shape_kind: a real object -> 'object'")
_g = importlib.util.spec_from_file_location("pr_guard", ROOT / "tools/pr_guard.py")
pg = importlib.util.module_from_spec(_g)
_g.loader.exec_module(pg)
expect(pg.log_problems({"work/x/redesign.py"}, ""), "pr_guard: work/ changed without a LOG entry -> ERROR")
expect(not pg.log_problems({"work/x/redesign.py", "docs/LOG.md"}, "+## 2026-11-22 — m via t — `x`"), "pr_guard: with a new LOG entry -> ok")
expect(pg.log_problems({"docs/LOG.md"}, "-## 2026-11-18 old\n+## 2026-11-18 new"), "pr_guard: an edited LOG line -> ERROR (append-only)")

# gradients (2026-11-22, Deezer concepts looked melted): a source gradient must come back as ONE
# part with a real gradient, and flat bands in a style must FAIL the `bands` check
import obj as OB  # noqa: E402
_grp = [(n, f) for n, _, f in OB.regions("exteraless") if "+" in n]
expect(_grp and isinstance(_grp[0][1], OB.Grad), "regions(): exteraless's gradient bands come back merged with a Grad fill")
if _grp:
    _names = _grp[0][0].split("+")
    _flat = "".join(f'<path d="M0 0" fill="{OB.colour("exteraless", k)}"/>' for k in _names[:2])
    expect(OB.banded("exteraless", _flat), "banded(): two bands of one gradient painted flat -> found (check `bands` FAILs)")
    _ic = OB.gk.Icon("g")
    OB.solid(_ic, OB.rounded(OB.box(20, 20, 108, 110), 10), face=_grp[0][1], depth=4)
    with tempfile.TemporaryDirectory() as tmp:
        _ic.save(Path(tmp) / "g.svg")
        _t = (Path(tmp) / "g.svg").read_text()
    expect("linearGradient" in _t and not OB.banded("exteraless", _t), "solid(face=Grad) paints a real gradient, no bands")
_tmp = ROOT / "work" / "_selftest_grad"
try:
    import numpy as _np
    from PIL import Image as _Im
    _tmp.mkdir(exist_ok=True)
    _y, _x = _np.mgrid[0:256, 0:256] / 256
    _a = _np.zeros((256, 256, 4))
    _a[..., 3] = 1
    _a[..., :3] = 0.08
    _m = (_x > 0.2) & (_x < 0.8) & (_y > 0.3) & (_y < 0.7)
    for _k, (_c0, _c1) in enumerate(((1.0, 0.2), (0.6, 0.3), (0.1, 0.9))):
        _a[..., _k] = _np.where(_m, _c0 + (_c1 - _c0) * _x, _a[..., _k])
    _Im.fromarray((_a * 255).astype(_np.uint8)).save(_tmp / "source.png")
    _tr = OB.traced("_selftest_grad", (0, 0, 128, 128), n=6, exclude=["#141414"])
    expect(len(_tr) == 1 and isinstance(_tr[0][1], OB.Grad), f"traced(): one gradient bar -> ONE part with a Grad (got {len(_tr)})")
finally:
    import shutil
    shutil.rmtree(_tmp, ignore_errors=True)

print(f"selftest: {ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
