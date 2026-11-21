#!/usr/bin/env python3
"""THE ONE COMMAND: what to do next. Run it first, do ONLY what it prints, run it again.

    python3 tools/next.py <slug>          # the next step for one app
    python3 tools/next.py                 # which app to work on next
    python3 tools/next.py <slug> --start-redo   # (only when it tells you) archive an old
                                                # approved design so the app can be redone

It reads the files of work/<slug>/ (design.md, concepts/, redesign.py, the built SVGs),
the pack (pack/styles.json, artwork/) and git, and prints exactly ONE state:

  STATE  <name>   - where the app is
  GOAL           - what this step is for (one line)
  DO             - the exact command(s) or edits
  ASK THE OWNER  - (only when it is his turn) the Turkish text to send, then STOP and wait
  DETAILS        - docs/PLAYBOOK.md section for this state

States, in order: NO_SOURCE, NOT_STARTED, FILL_DESIGN, DRAW_CONCEPTS, BOARD, ASK_Q1,
REDO, BUILD, FIX_FAIL, ASK_Q2, PACK, LOG, COMMIT, PUSH, DONE.
"""
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from stamps import board_current, build_current  # noqa: E402
TODAY = date.today().isoformat()
QUOTED_DATED = re.compile(r'"[^"]+".*\((\d{4}-\d{2}-\d{2})\)')
STYLES = ("faithful", "disc", "rimmed", "symbol")
GAME_HINTS = ("game", "oyun")

# what a check means and how to fix it (check_icon.py names -> recipe). PLAYBOOK.md has more.
RECIPES = {
    "redesign": "design.md 'approved:' must be the owner's Q1 answer in quotes + date, e.g.\n"
                '    approved: B - "B" (2026-11-21)\n'
                "  Never write it yourself. If the owner has not answered Q1 yet, ask Q1 (next.py prints it).",
    "lint": "The SVG contains something forbidden (<text>, <image>, filters, blur) or touches the canvas edge.\n"
            "  Draw only with obj.py / objects.py shapes; keep the object inside 8..120.",
    "visible": "The icon disappears on a light or dark wallpaper. Give the object a darker side (ramp step 4-5)\n"
               "  and a lighter top (step 1-2); do not make it only white or only near-black.",
    "visible_light": "The Symbol is too pale on a LIGHT wallpaper: use darker ramp steps (3-5) for the face/side,\n"
                     "  or add a darker secondary object. White objects need a grey side (Light 4-5).",
    "visible_dark": "The Symbol is too dark on a DARK wallpaper: use lighter ramp steps (1-3) for the face,\n"
                    "  keep the top light (toplight()), avoid Dark 3/4 as the main colour.",
    "mass": "Painted area is low (the icon looks thin/small among its neighbours). Make the main object bigger\n"
            "  (its size argument +10..15 %), make a wide object taller, or add the secondary object in front.\n"
            "  Stay inside 8..120 and on the baseline 118.",
    "baseline": "The bottom edge is not on the baseline. Set the object's `base` (or the fit() box bottom) so that\n"
                "  the bottom INCLUDING its side is 118. Check: python3 tools/describe_icon.py <svg>.",
    "legibility32": "Details vanish at 32 px. Use fewer and bigger parts, strokes >= 2 px, drop tiny details.",
    "holes": "Holes of the source (letter counters, eyes, ring centres) must be TRANSPARENT, not painted.\n"
             "  Use body(slug) or shape.difference(hole_shape). Never paint the hole white or in a tile colour.",
    "plain_shape": "The silhouette is a plain disc/square = the logo on a plate. Build the app's OBJECT instead\n"
                   "  (work/_lib/objects.py, docs/redesign/OBJECTS.md).",
    "faithful": "No Faithful SVG. In redesign.py end with save_styles(SLUG, {\"symbol\": main(), ...}) - it writes\n"
                "  every slot (missing ones get the main design). Then python3 tools/make_icon.py <slug>.",
    "box_in_plate": "Old plate style only: the mark is a box inside the plate. A redesign does not have this.",
    "stripes": "Automatic draft only (bands of one gradient). A redesign does not draw the measured bands.",
    "trace_iou": "Automatic draft only (traced parts do not match). A redesign draws its own shapes.",
}
WARN_TR = {
    "mass": "simge biraz ince/küçük görünebilir (komşularından az dolu)",
    "visible_light": "açık duvar kâğıdında biraz soluk",
    "visible_dark": "koyu duvar kâğıdında biraz soluk",
    "legibility32": "küçük boyutta bazı ayrıntılar kayboluyor",
    "baseline": "diğer simgelerden biraz yukarıda/aşağıda duruyor",
    "plain_shape": "dış hatları düz bir kare gibi",
    "visible": "bir duvar kâğıdında zor görünüyor",
}


# ------------------------------------------------------------------ helpers
def sh(*cmd):
    r = subprocess.run(list(cmd), capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def design_text(w):
    p = w / "design.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def line(text, key):
    for ln in text.splitlines():
        if ln.lower().startswith(key + ":"):
            return ln.split(":", 1)[1].strip()
    return ""


def quoted(v):
    m = QUOTED_DATED.search(v or "")
    return m.group(1) if m else None


def label_of(slug):
    tsv = ROOT / "work/_lib/batch_apps.tsv"
    if tsv.exists():
        for ln in tsv.read_text(encoding="utf-8").splitlines():
            p = ln.split("\t")
            if p and p[0] == slug and len(p) > 1:
                return p[1]
    return slug.replace("_", " ").title()


def is_game(w, text):
    k = line(text, "kind").lower()
    if k:
        return k.startswith("game")
    return (w / "refs").is_dir() or "POSTER" in text or any(h in line(text, "function object (what the app does, as a physical thing)").lower() for h in GAME_HINTS)


def anchors_filled(text):
    m = re.search(r"anchors[^\n]*\n((?:[ \t]+\d\.[^\n]*\n?)+)", text)
    if not m:
        return False
    items = [re.sub(r"^\s*\d\.\s*", "", x).strip() for x in m.group(1).splitlines()]
    return sum(1 for x in items if x) >= 2


def function_filled(text):
    v = line(text, "function object (what the app does, as a physical thing)")
    return bool(v.strip())


def concept_lines(text):
    out = {}
    m = re.search(r"concepts[^\n]*\n((?:[ \t]+[A-H]\b[^\n]*\n?)+)", text)
    if m:
        for ln in m.group(1).splitlines():
            mm = re.match(r"\s*([A-H])\b[^:]*:\s*(.*)", ln)
            if mm:
                out[mm.group(1)] = mm.group(2).strip()
    return out


def check_rows(slug):
    code, out = sh(sys.executable, "tools/check_icon.py", slug, "--json")
    try:
        return json.loads(out[out.index("["):out.rindex("]") + 1])
    except ValueError:
        return [{"scope": "app", "check": "gate", "status": "FAIL", "value": out[-300:], "fix": "run check_icon.py by hand"}]


def pack_state(slug):
    """-> (in_pack, missing_slots, stale) for the built styles of a redesign."""
    w = ROOT / "work" / slug
    icons = json.loads((ROOT / "pack/styles.json").read_text())["icons"]
    in_pack = (ROOT / f"app/src/main/res/drawable-nodpi/{slug}.png").exists()
    slots = icons.get(slug, {}) if in_pack else {}
    missing, stale = [], []
    for st in STYLES:
        svg = w / f"{slug}-{st}.svg"
        if not svg.exists():
            continue
        name = slug if st == "faithful" else slots.get(st)
        if name is None:
            missing.append(st)
            continue
        art = ROOT / f"artwork/{name}.svg"
        if not art.exists() or art.read_bytes() != svg.read_bytes():
            stale.append(st)
    return in_pack, missing, stale


def categories():
    p = ROOT / "app/src/main/res/xml/drawable.xml"
    return re.findall(r'<category title="([^"]+)"', p.read_text(encoding="utf-8")) if p.exists() else []


def category_of(slug):
    p = ROOT / "app/src/main/res/xml/drawable.xml"
    cur = None
    for ln in (p.read_text(encoding="utf-8").splitlines() if p.exists() else []):
        m = re.search(r'<category title="([^"]+)"', ln)
        if m:
            cur = m.group(1)
        if f'drawable="{slug}"' in ln:
            return cur
    return None


def concept_shapes(slug):
    """-> [(letter, kind)] for concepts that look like a plain disc or a square tile/plate."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_icon", ROOT / "tools/check_icon.py")
    ci = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ci)
    out = []
    for p in sorted((ROOT / "work" / slug / "concepts").glob("*.svg")):
        kind, _, fill = ci.shape_kind(p)
        if kind in ("disc", "tile"):
            out.append((p.stem, kind, fill))
    return out


def plate_warning(slug):
    bad = concept_shapes(slug)
    if not bad:
        return []
    lines = []
    for letter, kind, fill in bad:
        what = "a plain DISC" if kind == "disc" else f"a square TILE/plate (fills {fill:.0%} of its box)"
        lines.append(f"WARNING concept {letter} looks like {what}.")
    lines.append("  If it is the logo on a tile/disc: REPLACE it with a different object before asking (REDESIGN.md 1 -")
    lines.append("  the owner rejects 'the logo on a plate' every time). If it is a real square/round OBJECT")
    lines.append("  (a window, a calendar page, a die, a coin, a lens), keep it. Exception: L3 tile for a pure wordmark.")
    return lines


def git_dirty(slug):
    _, out = sh("git", "status", "--porcelain", "--", f"work/{slug}", "artwork", "app/src", "pack", "docs/LOG.md")
    return [ln for ln in out.splitlines() if ln.strip()]


def branch():
    return sh("git", "rev-parse", "--abbrev-ref", "HEAD")[1].strip()


def unpushed(slug):
    """commits on this branch that touch the app and are not pushed yet (no upstream: not on main)"""
    code, _ = sh("git", "rev-parse", "--abbrev-ref", "@{u}")
    base = "@{u}" if code == 0 else "origin/main"
    _, out = sh("git", "rev-list", "--count", f"{base}..HEAD", "--", f"work/{slug}", "artwork", "app/src", "pack")
    try:
        return int(out.strip() or 0)
    except ValueError:
        return 0


def log_has(slug, since):
    p = ROOT / "docs/LOG.md"
    if not p.exists():
        return False
    entries = re.split(r"\n(?=## \d{4}-\d{2}-\d{2})", p.read_text(encoding="utf-8"))
    for e in entries:
        m = re.match(r"## (\d{4}-\d{2}-\d{2})", e)
        if m and m.group(1) >= (since or "0000") and f"`{slug}`" in e:
            return True
    return False


# ------------------------------------------------------------------ output
def say(state, goal, do, ask=None, play=None, extra=None):
    print(f"STATE  {state}")
    print(f"GOAL   {goal}")
    print("DO")
    for d in do:
        print("  " + d.replace("\n", "\n  "))
    if ask:
        print("ASK THE OWNER  (send this, in Turkish, then STOP and wait for his answer)")
        print("  " + ask.replace("\n", "\n  "))
    if extra:
        print(extra)
    print(f"DETAILS docs/PLAYBOOK.md#{(play or state).lower().replace('_', '-')}")
    print("Then run this command again:  python3 tools/next.py" + (f" {SLUG}" if SLUG else ""))


SLUG = None


def q1_text(slug, w, text, game):
    name = label_of(slug)
    cs = concept_lines(text)
    letters = sorted(p.stem for p in (w / "concepts").glob("*.svg"))
    desc = "\n".join(f"  {k}: {cs.get(k, '(design.md concepts satırına yaz)')}" for k in letters)
    refs = list((w / "refs").glob("*.png")) + list((w / "refs").glob("*.jpg")) if (w / "refs").is_dir() else []
    need_refs = game and len(refs) < 2
    numbered = [f"{i + 1}) {k}" for i, k in enumerate(letters)] + [f"{len(letters) + 1}) Hiçbiri, yeniden dene"]
    t = (f"{name} için {len(letters)} fikir hazır. Resim: work/{slug}/concepts.png\n"
         f"(en solda kaynak, sağında {', '.join(letters)}; üst sıra açık, alt sıra koyu duvar kâğıdı)\n{desc}\n\n"
         f"Soru 1: Telefonunda göreceğin ana simge (Symbol) hangisi olsun?\n  " + "  ".join(numbered) + "\n"
         f"Soru 2: Uygulamadaki diğer stiller (Faithful/Disc/Rimmed) için hangilerini de tutayım? Harfleri yaz\n"
         f"  (örnek: \"A, D\"); hiçbiri ise \"0\" yaz, o zaman hepsinde ana simge olur.")
    if need_refs:
        t += ("\nNot: Bu bir oyun; elimde oyun içi ekran görüntüsü yok. 2-3 tane atarsan oyunun nesnelerini\n"
              "onlara göre düzeltirim.")
    t += ("\n\n(With AskUserQuestion: the same text as two questions - Soru 1 single choice with the letters +\n"
          " \"Hiçbiri, yeniden dene\", Soru 2 multiSelect with the letters. Without it: send the text as is.)")
    return t


def q2_text(slug, w, text, rows, in_pack, missing, stale):
    name = label_of(slug)
    styles = line(text, "styles") or "symbol=<main>"
    f = sum(r["status"] == "FAIL" for r in rows)
    wn = [r for r in rows if r["status"] == "WARN"]
    p = sum(r["status"] == "PASS" for r in rows)
    weak = sorted({WARN_TR.get(r["check"], r["check"]) for r in wn})
    if not in_pack:
        cat = category_of(slug)
        phone = ("yeni simge pakete eklenir (her stil için bir resim; kategori: "
                 f"{cat or '<KATEGORİ - listeden seç>'}); hiçbir şey silinmez")
    else:
        parts = []
        if stale or True:
            parts.append(f"eski {name} simgesinin yerine bu gelir")
        if missing:
            parts.append(f"{len(missing)} yeni resim eklenir ({', '.join(missing)})")
        parts.append("hiçbir şey silinmez")
        phone = "; ".join(parts)
    return (f"{name} hazır. Telefonda görünümü: work/{slug}/phone.png (açık/koyu duvar kâğıdında, diğer simgelerin\n"
            f"arasında); tüm stiller: work/{slug}/review.png.\n"
            f"Stiller: {styles}\n"
            f"Telefonuna: {phone}.\n"
            f"Kontrol: {p} geçti, {len(wn)} uyarı, {f} hata.\n"
            f"Zayıf yanlar: {'; '.join(weak) + '; ' if weak else ''}<SENİN DÜRÜST NOTLARIN - bunu değiştir>\n\n"
            f"  1) Tamam, pakete ekle   2) Şunu değiştir (ne olduğunu yaz)   3) Konseptlere dön\n\n"
            f"(With AskUserQuestion: one question with these three options. Without it: send the text as is.)")


# ------------------------------------------------------------------ the state machine
def state_of(slug, cheap=False, use_git=True):
    """-> (state, info). cheap=True skips the quality gate; use_git=False stops after LOG
    (the overview and docs/APPS.md describe the app, not your working tree)."""
    w = ROOT / "work" / slug
    if not (w / "source.png").exists():
        return "NO_SOURCE", {}
    text = design_text(w)
    if not (w / "geometry.json").exists() or not text or not (w / "redesign.py").exists():
        return "NOT_STARTED", {}
    if line(text, "redo") and quoted(line(text, "redo")):
        return "REDO", {}
    game = is_game(w, text)
    approved = line(text, "approved")
    if not quoted(approved):
        if not anchors_filled(text) or not function_filled(text) or \
                not line(text, "kind").lower().startswith(("app", "game")) or \
                (game and line(text, "characters").lower().startswith("yes")):
            return "FILL_DESIGN", {"game": game}
        svgs = sorted((w / "concepts").glob("*.svg"))
        if len(svgs) < 4:
            return "DRAW_CONCEPTS", {"game": game, "n": len(svgs)}
        cl = concept_lines(text)
        missing = [p.stem for p in svgs if not cl.get(p.stem)]
        if missing:
            return "DRAW_CONCEPTS", {"game": game, "n": len(svgs), "lines": missing}
        if not (w / "concepts.png").exists() or board_current(slug) is False:
            return "BOARD", {}
        return "ASK_Q1", {"game": game, "text": text}
    red = (w / "redesign.py").read_text(encoding="utf-8")
    built = [w / f"{slug}-{st}.svg" for st in ("faithful", "symbol")]     # the other slots may fall back
    if "copy the approved concept here" in red:
        return "BUILD", {"game": game}
    if not all(p.exists() for p in built):
        return "BUILD", {"game": game, "no_symbol": True}
    if build_current(slug) is False or not (w / "phone.png").exists() or not (w / "review.png").exists():
        return "BUILD", {"game": game, "rebuild": True}
    final = line(text, "final")
    if not quoted(final):
        if cheap:
            return "ASK_Q2", {}
        rows = check_rows(slug)
        fails = [r for r in rows if r["status"] == "FAIL"]
        if fails:
            return "FIX_FAIL", {"fails": fails}
        in_pack, missing, stale = pack_state(slug)
        return "ASK_Q2", {"rows": rows, "text": text, "pack": (in_pack, missing, stale)}
    in_pack, missing, stale = pack_state(slug)
    if not in_pack or missing or stale:
        return "PACK", {"pack": (in_pack, missing, stale), "final": quoted(final)}
    if not log_has(slug, quoted(final)):
        return "LOG", {"final": quoted(final)}
    if not use_git:
        return "DONE", {}
    if git_dirty(slug):
        return "COMMIT", {"dirty": git_dirty(slug)}
    if unpushed(slug) > 0:
        return "PUSH", {}
    return "DONE", {}


def run_slug(slug):
    global SLUG
    SLUG = slug
    w = ROOT / "work" / slug
    if branch() in ("main", "master"):
        say("ON_MAIN", "never work on main (AGENTS.md section 0)",
            [f"git config core.hooksPath tools/hooks && git switch -c icons/{slug}"], play="on-main")
        return
    st, info = state_of(slug)
    name = label_of(slug)
    if st == "NO_SOURCE":
        say(st, f"get the app's icon + ComponentInfo into work/{slug}/source.png",
            ["Look for the owner's request: a zip / folder / request.txt he gave you, or requests/inbox/.",
             "python3 tools/import_request.py <zip | folder | request.txt>          # lists the apps in it",
             f"python3 tools/import_request.py <same> --add --only {slug}",
             "or, with an icon PNG and the ComponentInfo FROM HIS PHONE (never guessed):",
             f'python3 tools/add_source.py {slug} <icon.png> "{name}" "ComponentInfo{{pkg/pkg.Activity}}"',
             "Nothing found? Ask the owner (Turkish): 'Bu uygulamanın simgesini Gnomed'in İstek ekranından\n"
             "  (Görsel + metin olarak paylaş) gönderebilir misin?'"])
    elif st == "NOT_STARTED":
        say(st, "measure the source and create the design files",
            [f"python3 tools/new_redesign.py {slug}",
             f"(writes work/{slug}/geometry.json, design.md, concepts/make_concepts.py, redesign.py and prints the parts)"])
    elif st == "FILL_DESIGN":
        g = info["game"]
        ex = ("  kind: game\n  references (...): store icon = <what it shows>; refs/ screenshots = <what they show>\n"
              "  anchors (...):\n    1. the gold goal ring with a blue inner face\n    2. the glowing energy ball\n"
              "    3. purple / orange team colours\n"
              "  function object (what the app does, as a physical thing): the ball going into the goal ring") if g else (
              "  kind: app\n  anchors (...):\n    1. the white paper plane (measured, tip right-top)\n"
              "    2. Telegram blue #31a5df -> HIG Blue 3\n    3. the round shape\n"
              "  function object (what the app does, as a physical thing): a message flying off - an envelope / paper plane")
        say(st, f"write in work/{slug}/design.md what makes {name} recognisable and what it does as an object",
            [f"Open work/{slug}/design.md and fill these lines (example):", ex,
             f"Facts about the source: python3 tools/describe_icon.py work/{slug}/source.png  and the parts list:",
             f"python3 -c \"import sys; sys.path.insert(0,'work/_lib'); from obj import describe; print(describe('{slug}'))\"",
             "Game? REDESIGN.md 3b: no characters, faces or animals - 1-3 of the game's OBJECTS.",
             "Pick the object from the decision table in docs/PLAYBOOK.md (app type -> object) and docs/redesign/OBJECTS.md."])
    elif st == "DRAW_CONCEPTS" and info.get("lines"):
        say(st, "describe each concept in one line in design.md (the owner's Q1 text is built from them)",
            [f"In work/{slug}/design.md, under 'concepts (...) - four different ideas:', write for {', '.join(info['lines'])}:",
             "  A: <in plain words, what the object is and where the mark sits>   (example: 'A: a blue glass bottle, the",
             "     drop on its white label'). One line each, indented two spaces, letter + colon."])
    elif st == "DRAW_CONCEPTS":
        say(st, f"draw FOUR different rough ideas A-D (now {info['n']}) in work/{slug}/concepts/make_concepts.py",
            ["Each function A()..D() returns an icon; ideas from REDESIGN.md 3 (L1 mark as object / L2 object that carries\n"
             "  the mark / L3 material tile) - for games: the game's objects only.",
             "Compose ready objects:  from objects import *   (catalogue: docs/redesign/OBJECTS.md, picture objects.png)",
             "The app's own mark ALWAYS from the source:  P = parts(slug); mark = body(slug); fit([...], box, anchor='bottom')",
             "Working examples: work/pokemon_unite/concepts/make_concepts.py (game), work/telegram/redesign.py (app).",
             f"Then: python3 work/{slug}/concepts/make_concepts.py",
             f"Write one line per concept in design.md under 'concepts' (  A: ..., B: ...)."])
    elif st == "BOARD":
        say(st, "render the concept board the owner will look at",
            plate_warning(slug) + [f"python3 tools/concepts.py {slug}",
             f"Cannot see images? For each concept: python3 tools/describe_icon.py work/{slug}/concepts/A.svg (B, C, D)\n"
             "  and replace a concept that is only the logo on a plain disc or square."])
    elif st == "ASK_Q1":
        say(st, "Q1: the owner chooses the main design and which others to keep",
            plate_warning(slug) + ["Translate the concept lines (A: ..., B: ...) into short, plain Turkish in the text.",
                                   "Send the text below (Turkish). Then STOP. When he answers, write his words in design.md:",
             f'  approved: <letter> - "<his answer to Soru 1, verbatim>" ({TODAY})',
             f'  keep: <letters or none> - "<his answer to Soru 2, verbatim>" ({TODAY})',
             "If he answered 'Hiçbiri, yeniden dene': archive concepts/ as concepts-roundN/ and draw 4 new ones.",
             "If he wrote a change request inside his answer: do it in the build (and quote it in design.md)."],
            ask=q1_text(slug, w, info["text"], info["game"]))
    elif st == "REDO":
        say(st, f"{name} was approved before but the owner wants it redone - archive the old design first",
            [f"python3 tools/next.py {slug} --start-redo",
             "(moves concepts/ to concepts-roundN/, keeps the old approval lines as 'history:' and clears them;\n"
             " the pack is not touched - the old icon stays on his phone until the new one is approved)"],
            extra=f"  the owner's words: {line(design_text(w), 'redo')}")
    elif st == "BUILD":
        game = info.get("game")
        ex = "work/pokemon_unite/redesign.py + kit.py (game objects)" if game else \
            "work/telegram/redesign.py (mark on an envelope stamp) or work/aurex_browser/redesign.py (mark on a window page)"
        if info.get("no_symbol"):
            do = [f"work/{slug}/redesign.py exists but does not write a Symbol (the owner's style - no app is done",
                  "  without one). Make its last line save every slot, the main design as the Symbol:",
                  "  save_styles(SLUG, {\"symbol\": main(), \"faithful\": ...})   (missing slots get the main design)",
                  "  If you do not know which design is the main one: it is the 'approved:' letter in design.md."]
        elif info.get("rebuild"):
            do = []
        else:
            do = [
            f"Write work/{slug}/redesign.py: copy the APPROVED concept function from concepts/make_concepts.py,",
            "  and each KEPT one; polish them (thickness, top light, secondary object - REDESIGN.md 5).",
            f"  End with: save_styles(SLUG, {{\"symbol\": main(), \"faithful\": ..., \"disc\": ..., \"rimmed\": ...}})",
            "  (slots: closest to the original logo -> faithful, a round one -> disc, the next -> rimmed;",
            "   a missing slot gets the main design). Write the slots in design.md 'styles:'.",
            f"  Closest worked example: {ex}; annotated in docs/playbook/."]
        say(st, "build the approved design(s) and render the review + phone preview",
            do + [f"python3 tools/make_icon.py {slug}      # build + review.png + phone.png + the gate"])
    elif st == "FIX_FAIL":
        do = []
        for r in info["fails"]:
            do.append(f"FAIL {r['scope']} {r['check']}: {r['value']}")
            do.append("  -> " + RECIPES.get(r["check"], r.get("fix") or "see docs/PLAYBOOK.md#fix-fail"))
        do.append(f"then: python3 tools/make_icon.py {slug}")
        say(st, "fix every FAIL of the quality gate (never ask the owner with a FAIL)", do)
    elif st == "ASK_Q2":
        in_pack, missing, stale = info["pack"]
        cat = category_of(slug) or "<Category>"
        cmd = f"python3 tools/pack_add.py {slug} --category {cat} --dry-run" if (not in_pack or missing) else \
            f"python3 tools/pack_refresh.py {slug} --dry-run"
        wn = [r for r in info["rows"] if r["status"] == "WARN"]
        do = ["Look at phone.png and review.png (cannot see images? describe_icon.py on each style SVG and say so).",
              f"Run the dry-run and keep only its new lines for yourself: {cmd}"]
        if cat == "<Category>":
            do.append("  <Category>: pick the one that fits from: " + ", ".join(categories()))
        do.append("Replace <SENİN DÜRÜST NOTLARIN ...> in the text with your honest weak points (Turkish). Cannot see")
        do.append("  images? write: \"Resimleri göremiyorum; ölçümlere göre: ...\" and the describe_icon facts.")
        for r in wn:
            do.append(f"WARN {r['scope']} {r['check']} {r['value']} - optional fix: " + RECIPES.get(r["check"], "").split("\n")[0])
        do += ["Send the text below. When he answers:",
               f'  "Tamam, pakete ekle" -> design.md:  final: "Tamam, pakete ekle" ({TODAY})',
               "  \"Şunu değiştir ...\"   -> change EXACTLY that, write his words under 'decisions', make_icon, ask Q2 again",
               "  \"Konseptlere dön\"     -> archive concepts/ as concepts-roundN/, new concepts, Q1 again"]
        say(st, "Q2: the owner sees the result and approves it for the pack", do,
            ask=q2_text(slug, w, info["text"], info["rows"], in_pack, missing, stale))
    elif st == "PACK":
        in_pack, missing, stale = info["pack"]
        do = []
        if not in_pack or missing:
            cat = category_of(slug) or "<Category>"
            do += [f"python3 tools/pack_add.py {slug} --category {cat} --dry-run    # read it",
                   f"python3 tools/pack_add.py {slug} --category {cat}"]
            if cat == "<Category>":
                do.append("  <Category>: one of " + ", ".join(categories()) + " (a new name makes a new category)")
        if in_pack:
            do += [f"python3 tools/pack_refresh.py {slug}"]
        do += ["python3 tools/gnome-android-icons/scripts/pack_audit.py --project .   # no ERROR line with " + slug,
               "python3 tools/size_audit.py                                           # 0 icon(s) outside",
               f"python3 tools/check_icon.py {slug}                                    # 0 FAIL"]
        say(st, "put the approved icons into the pack (only after \"Tamam, pakete ekle\")", do)
    elif st == "LOG":
        say(st, "write what this session did in docs/LOG.md (append-only)",
            ["Append at the END of docs/LOG.md (copy the format of the last entry):",
             f"## {TODAY} — <model> via <tool> (e.g. DeepSeek V4 via OpenCode) — `{slug}`",
             "- What: <main design -> Symbol, kept -> slots>",
             "- Why: <the owner's choices>",
             f"- Owner: approved / keep / final quotes from work/{slug}/design.md",
             "- PR: <link, or 'opened after this commit'>",
             "- Open problems: <honest weak points>"])
    elif st == "COMMIT":
        say(st, "commit the work on your branch",
            [f"git add -A && git commit -m \"{slug}: <what> - owner: \\\"Tamam, pakete ekle\\\"\"",
             "(never on main, never [release] in the message, never --no-verify)"] + [f"  changed: {d}" for d in info["dirty"][:8]])
    elif st == "PUSH":
        b = branch()
        say(st, "push your branch and open ONE pull request to main",
            [f"python3 tools/pr_guard.py           # must say 0 ERROR",
             f"git push -u origin {b}",
             "Open a pull request from this branch to main (GitHub website, or your tool's PR command) with the",
             "REDESIGN.md 9 report in Turkish. Give the owner the link. Never merge it yourself."])
    elif st == "DONE":
        nxt = overall(print_it=False, exclude=slug)
        say(st, f"{name} is finished and pushed",
            ["If the pull request is not open yet: open it (see PUSH) and give the owner the link.",
             f"Next app: {nxt}" if nxt else "Next app: ask the owner which app (python3 tools/next.py)",
             "Start the next app in a NEW session (/clear) - one app per session."])


# ------------------------------------------------------------------ overview
def overall(print_it=True, exclude=None):
    slugs = sorted(p.parent.name for p in (ROOT / "work").glob("*/source.png") if not p.parent.name.startswith(("_", "test_")))
    open_, redo, plate = [], [], []
    for s in slugs:
        if s == exclude:
            continue
        st, _ = state_of(s, cheap=True, use_git=False)
        if st == "REDO":
            redo.append(s)
        elif st in ("NOT_STARTED",):
            plate.append(s)
        elif st not in ("DONE", "NO_SOURCE"):
            open_.append((s, st))
    if not print_it:
        if open_:
            return f"{open_[0][0]} (unfinished: {open_[0][1]})"
        if redo:
            return f"{redo[0]} (the owner asked for a redo)"
        return None
    print("Which app next?  (docs/APPS.md has the full table: python3 tools/pack_status.py)")
    if open_:
        print("1. Unfinished redesigns - finish these first:")
        for s, st in open_:
            print(f"     {s:24s} {st:10s} -> python3 tools/next.py {s}")
    if redo:
        print("2. The owner asked for a redo:")
        for s in redo:
            print(f"     {s:24s} -> python3 tools/next.py {s}")
    print(f"3. Not redesigned yet ({len(plate)} apps, still the logo on a plate). Do NOT pick one yourself:")
    print("   ask the owner which one (Turkish, numbered):")
    print("     'Hangi uygulamayı yapayım? Önerim: her gün gördüğün simgelerden başlamak.")
    print("      1) <app>  2) <app>  3) <app>  4) Başka (adını yaz)'")
    print("   " + ", ".join(plate))
    print("One app per session. Start it with: python3 tools/next.py <slug>")


# ------------------------------------------------------------------ --start-redo
def start_redo(slug):
    w = ROOT / "work" / slug
    text = design_text(w)
    if not quoted(line(text, "redo")):
        sys.exit("no quoted 'redo:' line in design.md - nothing to do")
    n = 1
    while (w / f"concepts-round{n}").exists():
        n += 1
    dst = w / f"concepts-round{n}"
    dst.mkdir()
    tracked = sh("git", "ls-files", f"work/{slug}/concepts")[1].split()
    for p in sorted((w / "concepts").glob("*")) + [w / "concepts.png"]:
        if not p.exists() or p.is_dir():
            continue
        rel = str(p.relative_to(ROOT))
        if rel in tracked or rel == f"work/{slug}/concepts.png":
            if sh("git", "mv", rel, str((dst / p.name).relative_to(ROOT)))[0]:
                shutil.move(str(p), dst / p.name)
        else:
            shutil.move(str(p), dst / p.name)
    (w / "concepts").mkdir(exist_ok=True)
    tpl = dst / "make_concepts.py"
    if tpl.exists():
        (w / "concepts/make_concepts.py").write_text(
            '"""' + f"{slug} - NEW concepts for the redo (the old ones are in concepts-round{n}/).\n"
            "Draw FOUR different ideas A-D; compose work/_lib/objects.py; see docs/PLAYBOOK.md#draw-concepts." + '"""\n'
            "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[2] / \"_lib\"))\n"
            "from objects import *  # noqa: F401,F403,E402\nOUT = Path(__file__).resolve().parent\n\n\n"
            "def A():\n    ic = gk.Icon(\"A\")\n    # ... compose objects here ...\n    return ic\n\n\n"
            "if __name__ == \"__main__\":\n    for name, fn in ((\"A\", A),):   # add B, C, D\n"
            "        fn().save(OUT / f\"{name}.svg\")\n        print(\"wrote\", name)\n", encoding="utf-8")
    out, in_old, in_anch = [], False, False
    for ln in text.splitlines():
        key = ln.split(":", 1)[0].lower() if ":" in ln else ""
        if in_anch and not re.match(r"\s+\d\.", ln):
            out += ["anchors (2-4 things that make the app recognisable; they must survive):", "  1.", "  2.", "  3."]
            in_anch = False
        if ln.lower().startswith("anchors"):
            out.append("old anchors (before the redo):")
            in_anch = True
            continue
        if in_anch:
            out.append(re.sub(r"^(\s+)(\d\.)", r"\1old \2", ln))
            continue
        if key.startswith("function object"):
            out.append("old " + ln)
            out.append("function object (what the app does, as a physical thing):")
            continue
        if key == "characters" and line(text, "kind").lower().startswith("game"):
            out.append("characters: no   (REDESIGN.md 3b; before the redo: " + ln.split(":", 1)[1].strip() + ")")
            continue
        if key == "ladder":
            out.append("ladder:   (old: " + ln.split(":", 1)[1].strip() + ")")
            continue
        if in_old and not re.match(r"\s+[A-H]\b", ln):
            out += ["concepts (work/" + slug + "/concepts.png) - four different ideas:", "  A:", "  B:", "  C:", "  D:"]
            in_old = False
        if key in ("approved", "keep", "final"):
            out.append(f"history-{key}: {ln.split(':', 1)[1].strip()}   [before the redo, concepts-round{n}/]")
            out.append(f"{key}:")
        elif key == "redo":
            out.append("redo-started:" + ln.split(":", 1)[1] + f" ({TODAY}, old concepts -> concepts-round{n}/)")
        elif ln.lower().startswith("concepts"):
            out.append(f"old concepts (round {n}, before the redo):")
            in_old = True
        elif in_old:
            out.append(re.sub(r"^(\s+)([A-H])\b", r"\1old \2", ln))
        else:
            out.append(ln)
    if in_old:
        out += ["concepts (work/" + slug + "/concepts.png) - four different ideas:", "  A:", "  B:", "  C:", "  D:"]
    (w / "design.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"redo started: old concepts in work/{slug}/concepts-round{n}/, approval lines cleared in design.md.")
    print(f"Fix design.md (kind / anchors / function object for the new rule), then: python3 tools/next.py {slug}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if "--start-redo" in sys.argv and args:
        start_redo(args[0])
    elif args:
        run_slug(args[0])
    else:
        overall()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:          # next.py | head
        pass
