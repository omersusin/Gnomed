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
import re
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


_g = importlib.util.spec_from_file_location("nextpy", ROOT / "tools/next.py")
NX = importlib.util.module_from_spec(_g)
_g.loader.exec_module(NX)


def NX_open_fixes():
    code, out = run("-c", "import sys; sys.path.insert(0, 'tools'); import next as n; print(len(n.open_fix_slugs()))")
    return out.strip().splitlines()[-1:] != ["0"]


def state(slug, app_only=True):
    code, out = run("tools/next.py", slug, *(["--app-only"] if app_only else []))
    m = [ln.split()[1] for ln in out.splitlines() if ln.startswith("STATE")]
    return m[0] if m else f"no STATE line (exit {code}): {out[-200:]}"


on_main = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() in ("main", "master")
if on_main:
    expect(state("rush_royale") == "ON_MAIN", "next.py refuses to work on main")
else:
    expect(state("zz_no_such_app") == "NO_SOURCE", "next.py: an unknown app -> NO_SOURCE")
    # REDO / NOT_STARTED on a throw-away app: real apps move on (kafa_topu_2 and qobuz were these once)
    with tempfile.TemporaryDirectory() as tmp:
        _w = Path(tmp) / "work" / "zz_redo"
        _w.mkdir(parents=True)
        (_w / "source.png").write_bytes((ROOT / "work/qobuz/source.png").read_bytes())
        _orig = NX.ROOT
        try:
            NX.ROOT = Path(tmp)
            _s0 = NX.state_of("zz_redo", cheap=True)[0]
            for f in ("geometry.json", "redesign.py"):
                (_w / f).write_text("{}" if f.endswith(".json") else "")
            (_w / "design.md").write_text('# zz\nredo: "Kabul edilemez" (2026-11-23)\n')
            _s1 = NX.state_of("zz_redo", cheap=True)[0]
        finally:
            NX.ROOT = _orig
    expect(_s1 == "REDO", f"next.py: the owner's redo: line -> REDO ({_s1})")
    expect(_s0 == "NOT_STARTED", f"next.py: an app with only its source -> NOT_STARTED ({_s0})")
    expect(state("andvm") == "BUILD", "next.py: a redesign without a Symbol -> BUILD")
    st = state("kafa_topu_2")          # a shipped redesign (rush_royale has the owner's redo line now)
    expect(st in ("LOG", "COMMIT", "PUSH", "DONE"), f"next.py: a shipped redesign is past Q2 ({st})")
    if list((ROOT / "work").glob("*/fixes.md")) and NX_open_fixes():
        expect(state("rush_royale", app_only=False) == "OWNER_FIXES_FIRST",
               "next.py: open owner fix lists come before any other app (OWNER_FIXES_FIRST)")
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

# pack consistency + design resources (2026-11-22)
code, out = run("tools/validate_pack.py")
expect(code == 0 and "0 ERROR" in out, "validate_pack.py: every pack entry points to a real PNG (0 ERROR)")
_gpl = (ROOT / "docs/palette/gnomed.gpl").read_text().splitlines()
_hex = {"#%02x%02x%02x" % tuple(int(v) for v in ln.split("\t")[0].split()) for ln in _gpl if ln[:1].isdigit() or ln[:1] == " "}
expect({h for steps in O.RAMP.values() for h in steps} <= _hex and "#000000" not in _hex,
       "docs/palette/gnomed.gpl = RAMP of objects.py, no pure black (re-run tools/make_palettes.py)")
expect((ROOT / "docs/template/gnomed-template.svg").exists(), "docs/template/gnomed-template.svg exists")

# categories, references, mark size, FIX_WARN (2026-11-22: "kategoriye uygun", screenshots, Deezer's tiny bars)
import categories as CAT  # noqa: E402
expect(CAT.from_play("MUSIC_AND_AUDIO") == "music" and CAT.from_play("GAME_SPORTS") == "game"
       and CAT.from_play("COMMUNICATION") == "messaging", "categories.from_play: Play Store codes -> object families")
expect(CAT.object_of("telegram", "messaging") == "envelope", "categories.object_of: Telegram's approved concept -> 'envelope'")
expect("CATEGORY: messaging" in CAT.suggest("telegram"), "categories.suggest prints the family for next.py")
_fr = importlib.util.spec_from_file_location("fetch_refs", ROOT / "tools/fetch_refs.py")
FR = importlib.util.module_from_spec(_fr)
_fr.loader.exec_module(FR)
_html = ('<script type="application/ld+json">{"name":"X Music","applicationCategory":"MUSIC_AND_AUDIO",'
         '"description":"Songs.","image":"https://play-lh.googleusercontent.com/ICON"}</script>'
         '<div data-g-id="description">Line one<br>Line two</div>'
         '<img src="https://play-lh.googleusercontent.com/AAA=w526-h296" alt="Screenshot image">'
         '<img src="https://play-lh.googleusercontent.com/BBB=w526-h296" alt="Screenshot image">'
         '<img src="https://play-lh.googleusercontent.com/AAA=w526-h296" alt="Screenshot image">')
_inf = FR.parse_play(_html, "u")
expect(_inf["title"] == "X Music" and _inf["category"] == "MUSIC_AND_AUDIO" and len(_inf["shots"]) == 2
       and "Line two" in _inf["description"], "fetch_refs.parse_play: title, category, description, 2 unique screenshots")
with tempfile.TemporaryDirectory() as tmp:
    _t = O.gk.Icon("m")
    O.solid(_t, O.rounded(O.box(16, 20, 112, 112), 10), face="#9a9996", depth=6)
    O.solid(_t, O.box(56, 56, 72, 72), face="#2aa1da", depth=0, top=False)      # Telegram blue, 16 px
    _t.save(Path(tmp) / "small.svg")
    _m = ci.mark_measure("telegram", Path(tmp) / "small.svg")
    expect(_m is not None and _m[0] < 36, f"check_icon.mark_measure: a 16 px mark -> below 36 (mark_size WARN) {_m and round(_m[0])}")
_m = ci.mark_measure("telegram", ROOT / "work/telegram/telegram-symbol.svg")
expect(_m is not None and _m[0] >= 36, "check_icon.mark_measure: Telegram's envelope -> >= 36 (PASS)")
expect(NX.warn_ok("warn-ok: mark_size - the label cannot grow without hiding the reels", "mark_size")
       and not NX.warn_ok("warn-ok: mark_size - ok", "mark_size") and "mark_size" in NX.MUST_TRY,
       "next.py: FIX_WARN needs a real reason in 'warn-ok:' (>= 10 characters)")

expect(CAT.guess("exteraless: a Telegram client") == "messaging" and CAT.guess("Terminal emulator for Android") == "dev",
       "categories.guess: words of a README/store text -> a category (apps not on Play)")
_imgs = FR._readme_images("![s](docs/s1.png) ![b](https://img.shields.io/x.svg) <img src='logo.png'> ![g](get-it-on-fdroid.png)",
                          "https://raw.githubusercontent.com/o/r/HEAD/")
expect(_imgs == ["https://raw.githubusercontent.com/o/r/HEAD/docs/s1.png"], "fetch_refs: README screenshots kept, badges/logos dropped")
expect(FR.system("com.android.settings", "Ayarlar")["category_key"] == "system" and FR.system("com.whatsapp", "x") is None,
       "fetch_refs.system: system packages need no screenshots (GNOME app for the same job)")

# batch 1 lessons (2026-11-22): look-alike styles, reserved logo objects
with tempfile.TemporaryDirectory() as tmp:
    _sv = {}
    for _st, _frame in (("symbol", "#1c71d8"), ("faithful", "#f6f5f4"), ("disc", "#1c71d8"), ("rimmed", "#1c71d8")):
        _t = O.gk.Icon(_st)
        if _st in ("symbol", "faithful"):              # the same framed photo, only the frame colour differs
            O.solid(_t, O.rounded(O.box(16, 20, 112, 110), 6), face=_frame, depth=5)
            O.solid(_t, O.box(26, 30, 102, 100), face="#62a0ea", depth=0, top=False)
        elif _st == "disc":
            O.sun(_t, 64, 118, 96)
        else:
            O.speaker(_t, 64, 118, 80)
        _sv[_st] = Path(tmp) / f"{_st}.svg"
        _t.save(_sv[_st])
    _groups, _alike = ci.style_groups(_sv)
    expect(len(_groups) == 3 and _alike, f"check_icon.style_groups: the same photo in two frame colours = ONE design ({_alike})")
expect("telegram" in " ".join(CAT.used("messaging").get("paper plane", [])),
       "categories: Telegram's paper plane is reserved (not free for other messaging apps)")

# overview ara-2 lessons (2026-11-22): the mark on every style, objects per category, fix lists in the repo
with tempfile.TemporaryDirectory() as tmp:
    _no = O.gk.Icon("no mark")
    O.cassette(_no, 64, 112, 104, ramp=O.RAMP["Red"])
    _no.save(Path(tmp) / "no.svg")
    _yes = O.gk.Icon("mark")
    O.cassette(_yes, 64, 112, 104, ramp=O.RAMP["Red"])
    O.put_mark(_yes, "apple_music", (44, 28, 84, 68), face="#241f31")
    _yes.save(Path(tmp) / "yes.svg")
    _m_ = O.gk.Icon("M")
    O.cassette(_m_, 64, 112, 104, ramp=O.RAMP["Red"])
    with _m_.group("mark"):
        O.solid(_m_, O.poly([(44, 70), (50, 34), (64, 52), (78, 34), (84, 70), (78, 70), (76, 48), (64, 62), (52, 48), (50, 70)]),
                face="#241f31", depth=0, top=False)
    _m_.save(Path(tmp) / "m.svg")
    _ww = O.gk.Icon("white on white")
    O.cassette(_ww, 64, 112, 104, ramp=O.RAMP["Light"])
    O.put_mark(_ww, "apple_music", (44, 28, 84, 68), face="#ffffff")
    _ww.save(Path(tmp) / "ww.svg")
    _r = {k: ci.mark_layer_measure("apple_music", Path(tmp) / f"{k}.svg") for k in ("no", "yes", "m", "ww")}
    expect(_r["no"] is None, "check_icon.mark: a style without a 'mark' layer -> WARN (Apple Music lost its note)")
    expect(_r["yes"] and _r["yes"][0] >= 36 and _r["yes"][1] >= 25 and _r["yes"][2] >= 0.5 and _r["yes"][3] >= 0.6,
           f"check_icon.mark: put_mark() on a cassette label -> PASS {_r['yes'] and [round(x, 2) for x in _r['yes']]}")
    expect(_r["m"] and _r["m"][2] < 0.5, "check_icon.mark: an 'M' in the mark layer is not the source's mark (ChatGPT's bulb)")
    expect(_r["ww"] and (_r["ww"][1] < 25 or _r["ww"][3] < 0.6), "check_icon.mark: a white mark on a white label does not stand out")
expect([n for n, _, _ in O.mark_parts("anker_soundcore")] == ["r3"],
       "obj.mark_parts: Soundcore's mark is the white wordmark, not the blue tile bands under it")
expect(NX.MUST_TRY and "mark" in NX.MUST_TRY and "same_object" in NX.MUST_TRY, "next.py: gates mark and same_object are fixed before Q2")
with tempfile.TemporaryDirectory() as tmp:
    _fx = Path(tmp) / "fixes.md"
    _fx.write_text("# x\ngroup: g1\nshown:\n\n- [ ] disc: a\n- [x] symbol: b\n- [x] rimmed: c -> now: a red radio\n")
    _orig = NX.ROOT
    try:
        (Path(tmp) / "work" / "zz_fix").mkdir(parents=True)
        (Path(tmp) / "work" / "zz_fix" / "fixes.md").write_text(_fx.read_text())
        NX.ROOT = Path(tmp)
        _o, _d, _h = NX.owner_fixes("zz_fix")
    finally:
        NX.ROOT = _orig
    expect(len(_o) == 2 and len(_d) == 1 and _h.get("group") == "g1",
           "next.py: a fix line is done only when ticked AND '-> now: <what it is now>' (OWNER_FIX)")

# mark_fit (2026-11-23): the mark must sit INSIDE its part with room, nothing drawn over it
with tempfile.TemporaryDirectory() as tmp:
    def _plate_with_mark(box_, hole=False):
        ic = O.gk.Icon("fit")
        O.solid(ic, O.rounded(O.box(20, 30, 108, 100), 10), face="#ffffff", depth=4)
        O.put_mark(ic, "apple_music", box_, face="#e01b24")
        if hole:
            O.solid(ic, O.circ(64, 65, 9), face="#3d3846", depth=0, top=False)
        return ic
    _plate_with_mark((44, 45, 84, 85)).save(Path(tmp) / "in.svg")
    _plate_with_mark((70, 45, 120, 95)).save(Path(tmp) / "off.svg")
    _plate_with_mark((44, 45, 84, 85), hole=True).save(Path(tmp) / "hole.svg")
    _fi = {k: ci.mark_fit_measure(Path(tmp) / f"{k}.svg") for k in ("in", "off", "hole")}

    def _bad(r):
        return r["cross"] > 0.01 or r["margin"] < 1.0 or r["covered"] > 0.03
    expect(_fi["in"] and not _bad(_fi["in"]), f"check_icon.mark_fit: a mark inside its plate -> PASS {_fi['in']}")
    expect(_fi["off"] and _bad(_fi["off"]), "check_icon.mark_fit: a mark running off its plate -> WARN (hepsiburada's cart)")
    expect(_fi["hole"] and _fi["hole"]["covered"] > 0.03, "check_icon.mark_fit: a hole drawn over the mark -> WARN (the CD hole on '>_')")
expect("mark_fit" in NX.MUST_TRY, "next.py: gate mark_fit is fixed before Q2")

# empty_layer (2026-11-23): rounded() on a strip thinner than 2r returns nothing - the part vanished silently
expect(not O.rounded(O.box(8, 102, 120, 114), 6).is_empty,
       "obj.rounded: r = half the height used to erase the part (Kafa Topu's turf) - now it survives")
with tempfile.TemporaryDirectory() as tmp:
    ic = O.gk.Icon("empty")
    O.solid(ic, O.circ(64, 60, 20).difference(O.circ(64, 60, 20)), face="#57e389", depth=4, layer="turf")  # sun()'s old edge
    ic.save(Path(tmp) / "e.svg")
    _empty = re.findall(r'<path id="([^"]+)" d=""', (Path(tmp) / "e.svg").read_text())
    expect("turf-face" in _empty, f"check_icon.empty_layer: the vanished turf is found: {_empty}")
expect("empty_layer" in NX.RECIPES and "empty_layer" in NX.WARN_TR, "next.py: empty_layer has a recipe and a Turkish line")


# 2026-11-23 takeover: what broke while Claude redid group 4 and the audit
_mp = OB.mark_parts("duolingo")
expect([n for n, _, _ in _mp][0] == "r0" and len(_mp) == 6,
       "obj.mark_parts: mark_keep puts Duo's head FIRST (under the eyes), not on top of them")
expect(any(n == "holes" and f == "#ff4500" for n, _, f in OB.mark_parts("reddit")),
       "obj.mark_parts: mark_hole_fill paints Snoo's eyes orange (owner: \"Logodaki gibi boya\")")
expect({f for _, _, f in OB.mark_parts("payload_dumper")} >= {"#9a9996", "#f08a24"},
       "obj.mark_parts: mark_split gives the wrench and the screwdriver their real colours")
expect(not O.rounded(O.box(38, 80, 90, 98), 9).is_empty, "obj.rounded: an 18-unit pill with r 9 survives (was empty)")
_ic = O.gk.Icon("body")
O.put_mark(_ic, "reddit", (10, 14, 118, 111), anchor="bottom", body=6, side="#c0bfbc")
with tempfile.TemporaryDirectory() as tmp:
    _ic.save(Path(tmp) / "b.svg")
    _t = (Path(tmp) / "b.svg").read_text()
expect('id="mark-side"' in _t and 'd=""' not in _t, "obj.put_mark(body=): one side under the mark, inside the mark layer")
with tempfile.TemporaryDirectory() as tmp:
    _w = Path(tmp) / "zz_mark"
    _w.mkdir()
    (_w / "design.md").write_text("kind: app\nmark: none - a mascot\n")
    _a = ci.mark_applies(_w)
    (_w / "design.md").write_text('kind: app\nmark: none - "Logo olmasın" (2026-11-23)\n')
    _b = ci.mark_applies(_w)
expect(_a and not _b, "check_icon.mark_applies: 'mark: none' counts only with the owner's words + date")


# Sonnet's Binance test (2026-11-23): the Faithful on a dark kite -> faithful_logo; four dark styles -> dark_family
with tempfile.TemporaryDirectory() as tmp:
    ic = O.gk.Icon("kite")
    O.solid(ic, O.Polygon([(64, 10), (116, 52), (64, 118), (12, 52)]), face="#2b3139", depth=5, side="#0b0e11", layer="kite")
    O.put_mark(ic, "binance_tr", (44, 34, 84, 84))
    ic.save(Path(tmp) / "k.svg")
    _f = ci.mark_fit_measure(Path(tmp) / "k.svg")
    _d = ci.dark_share(ci.render(Path(tmp) / "k.svg"))
expect(_f is not None and _f["share"] < 0.45, f"check_icon.faithful_logo: the logo on a dark kite is a plate ({_f and round(_f['share'], 2)})")
expect(_d > 0.45, f"check_icon.dark_share: a dark kite counts as dark ({_d:.2f})")
expect("faithful_logo" in NX.MUST_TRY and "dark_family" in NX.MUST_TRY, "next.py: faithful_logo and dark_family are fixed before Q2")

print(f"selftest: {ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
