"""App categories -> GNOME object FAMILIES (REDESIGN.md 3 "Choosing the object").

The owner (2026-11-22): every app drawn as an object of its kind - a music app as a record,
a cassette, a speaker, a player... ("tarza ve kategoriye uygun"). GNOME's HIG asks the same
(a physical object related to the app's function) AND that every app icon is unique. So:

  1. the app's CATEGORY gives the family of objects (music -> record, cassette, speaker ...);
  2. apps of the same category take DIFFERENT objects of the family when they can;
  3. if two must share an object, the brand colours + the mark (gate `mark_size`) tell them apart.

    from categories import category_of, suggest
    print(suggest("apple_music"))        # the family, what is already used, what is free

The category comes from design.md 'category:' or from the store (tools/fetch_refs.py writes
work/<slug>/refs/store/store.json with the Play Store category). docs/redesign/CATEGORIES.md is
this table as text (python3 work/_lib/categories.py --md).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# key: (title, Play Store category codes, [(object, objects.py function or "", keywords in design.md)],
#       GNOME / GNOME Circle apps of this kind (study their icons), extra notes)
CATEGORIES = {
    "music": ("Music & audio", ["MUSIC_AND_AUDIO"],
              [("vinyl record", "vinyl_record", r"record|vinyl|plak"),
               ("cassette", "cassette", r"cassette|kaset"),
               ("speaker", "speaker", r"speaker|hoparl"),
               ("headphones", "headphones", r"headphone|kulakl"),
               ("pocket music player", "", r"music player|mp3|ipod|walkman|çalar"),
               ("radio", "", r"radio|radyo"),
               ("microphone", "", r"microphone|mikrofon"),
               ("music note", "music_note", r"music note|nota")],
              "Mousai, Amberol, Lollypop, Rhythmbox, Shortwave, Podcasts", ""),
    "video": ("Video & TV", ["VIDEO_PLAYERS", "ENTERTAINMENT"],
              [("play button / screen", "play_button", r"play button|screen|tv|televizyon"),
               ("film reel", "", r"reel|film|makara"),
               ("clapperboard", "", r"clapper|klaket"),
               ("projector", "", r"projector|projeksiyon"),
               ("video camera", "", r"camcorder|video camera")],
              "Showtime, Celluloid, Clapper, Video Trimmer", ""),
    "messaging": ("Messaging & calls", ["COMMUNICATION"],
                  [("speech bubble", "speech_bubble", r"bubble|balon"),
                   ("envelope", "envelope", r"envelope|zarf|mektup"),
                   ("paper plane", "paper_plane", r"paper plane|uçak"),
                   ("phone handset", "phone_handset", r"handset|ahize|phone"),
                   ("walkie-talkie", "", r"walkie|telsiz"),
                   ("mailbox", "", r"mailbox|posta kutusu")],
                  "Chatty, Fractal, Polari, Calls, Geary, Tuba", ""),
    "social": ("Social & community", ["SOCIAL", "DATING"],
               [("speech bubble", "speech_bubble", r"bubble|balon"),
                ("photo print / frame", "", r"photo|frame|çerçeve|polaroid"),
                ("megaphone", "", r"megaphone|megafon"),
                ("notice board", "", r"board|pano"),
                ("camera", "camera_lens", r"camera|kamera|lens")],
               "Tuba, Fractal, Flare", ""),
    "browser": ("Web browsers", [],
                [("browser window", "browser_window", r"browser window|pencere|window"),
                 ("globe", "globe", r"globe|küre|dünya"),
                 ("compass", "", r"compass|pusula")],
                "Web (Epiphany) = a compass/globe", ""),
    "files": ("Files, storage, backup", [],
              [("folder", "folder", r"folder|klasör"),
               ("filing cabinet", "", r"cabinet|dolap"),
               ("archive box", "", r"archive|box|kutu"),
               ("cloud", "cloud", r"cloud|bulut"),
               ("hard drive / USB stick", "", r"drive|disk|usb")],
              "Files (cabinet), File Roller (box), Disks, Déjà Dup", ""),
    "security": ("Passwords, 2FA, VPN, privacy", [],
                 [("shield", "shield", r"shield|kalkan"),
                  ("padlock", "lock", r"lock|kilit|padlock"),
                  ("key", "key", r"\bkey\b|anahtar"),
                  ("safe / vault", "", r"safe|vault|kasa"),
                  ("ID card", "card", r"id card|kimlik")],
                 "Passwords and Keys (Seahorse), Secrets, Authenticator, Key Rack", ""),
    "finance": ("Banks, wallets, crypto", ["FINANCE"],
                [("bank card", "card", r"\bcard\b|kart"),
                 ("coin", "coin", r"coin|para|madeni"),
                 ("wallet", "", r"wallet|cüzdan"),
                 ("piggy bank", "", r"piggy|kumbara"),
                 ("safe", "", r"safe|kasa"),
                 ("chart / ticker", "", r"chart|grafik")],
                "Denaro, Money", ""),
    "shopping": ("Shopping & delivery", ["SHOPPING", "FOOD_AND_DRINK"],
                 [("shopping bag", "shopping_bag", r"bag|çanta|poşet"),
                  ("parcel box", "", r"parcel|box|koli|paket"),
                  ("basket / cart", "", r"basket|cart|sepet"),
                  ("price tag", "", r"tag|etiket")],
                 "", ""),
    "photo": ("Camera, photos, gallery", ["PHOTOGRAPHY", "ART_AND_DESIGN"],
              [("camera lens", "camera_lens", r"lens|camera|kamera|objektif"),
               ("photo print", "", r"photo print|\bprints?\b|polaroid|fotoğraf baskı"),
               ("film roll", "", r"film roll|rulo"),
               ("picture frame", "", r"picture frame|photo frame|çerçeve")],
              "Snapshot, Loupe, Shotwell, Camera", ""),
    "weather": ("Weather", ["WEATHER"],
                [("sun (always yellow/orange)", "sun", r"\bsun\b|güneş"),
                 ("cloud", "cloud", r"cloud|bulut"),
                 ("umbrella", "", r"umbrella|şemsiye"),
                 ("thermometer", "", r"thermometer|termometre"),
                 ("water drop", "water_drop", r"drop|damla")],
                "Weather", ""),
    "maps": ("Maps, travel, transport", ["MAPS_AND_NAVIGATION", "TRAVEL_AND_LOCAL", "AUTO_AND_VEHICLES"],
             [("folded map + pin", "", r"\bmap\b|harita|pin"),
              ("globe", "globe", r"globe|küre"),
              ("compass", "", r"compass|pusula"),
              ("signpost", "", r"sign|tabela")],
             "Maps, Railway, Pipeline", ""),
    "productivity": ("Notes, docs, calendar, tasks", ["PRODUCTIVITY", "BUSINESS"],
                     [("notebook / book", "book", r"book|notebook|defter|kitap"),
                      ("calendar page", "calendar_page", r"calendar|takvim"),
                      ("clipboard / checklist", "", r"clipboard|checklist|liste"),
                      ("pencil + paper", "", r"pencil|kalem"),
                      ("sticky note", "", r"sticky|yapışkan")],
                     "Notes, Text Editor, Calendar, Errands, Papers", ""),
    "dev": ("Terminals, developer and root tools", [],
            [("terminal window", "browser_window", r"terminal|console|konsol|>_"),
             ("toolbox / wrench", "", r"tool|wrench|anahtar takımı|alet"),
             ("circuit chip", "", r"chip|çip|circuit"),
             ("package / box", "", r"package|paket|box")],
            "Console, Builder, Terminal, Sysprof", "never a robot/mascot (HIG)"),
    "system": ("System, settings, launchers, utilities", ["TOOLS", "PERSONALIZATION", "LIBRARIES_AND_DEMO"],
               [("gear", "gear", r"gear|çark|dişli"),
                ("battery", "battery", r"battery|pil|batarya"),
                ("paint palette / brush", "", r"palette|brush|fırça|palet"),
                ("phone home screen", "", r"home screen|ana ekran|launcher"),
                ("calculator", "", r"calculator|hesap makinesi"),
                ("clock (digits: digital_display)", "", r"clock|saat")],
               "Settings, Tweaks, Clocks, Calculator, Characters", ""),
    "ai": ("AI assistants", [],
           [("speech bubble + spark", "speech_bubble", r"bubble|balon|spark"),
            ("crystal / gem", "crystal", r"crystal|kristal|gem"),
            ("notebook", "book", r"notebook|defter"),
            ("lightbulb", "", r"bulb|ampul")],
           "Newelle, Alpaca", "the brand mark (a knot, a burst) printed on the object"),
    "learning": ("Learning, languages, reading, news", ["EDUCATION", "BOOKS_AND_REFERENCE", "NEWS_AND_MAGAZINES"],
                 [("book", "book", r"book|kitap"),
                  ("flash cards", "", r"flash|kart"),
                  ("chalkboard", "", r"chalk|tahta"),
                  ("newspaper", "", r"newspaper|gazete"),
                  ("globe", "globe", r"globe|küre")],
                 "Dialect, Read It Later, Foliate, Newsflash", "no mascot (Duolingo: an object, not the owl)"),
    "health": ("Health & fitness", ["HEALTH_AND_FITNESS", "MEDICAL", "SPORTS"],
               [("running shoe", "", r"shoe|ayakkabı"),
                ("dumbbell", "", r"dumbbell|dambıl"),
                ("stopwatch", "", r"stopwatch|kronometre"),
                ("water bottle", "bottle", r"bottle|şişe|matara"),
                ("heart", "", r"heart|kalp")],
               "Workbench, Health", ""),
    "game": ("Games", ["GAME_"],
             [("ball", "football", r"ball|\btop\b"),
              ("goal / ring", "goal_ring", r"goal|ring|kale"),
              ("dice", "die", r"\bdie\b|dice|zar"),
              ("board / tiles", "board_tiles", r"board|tile|tahta"),
              ("magic hat / crystal / potion", "wizard_hat", r"hat|şapka|crystal|potion|iksir"),
              ("sword / shield", "shield", r"sword|kılıç"),
              ("trophy", "", r"trophy|kupa"),
              ("playing cards", "", r"cards|iskambil")],
             "Chess, Tali, Mahjongg, Mines, Quadrapassel", "REDESIGN.md 3b: the game's objects, no characters"),
}


# words in a store/README text -> category (for apps that are not on Google Play)
KEYWORDS = {
    "music": r"music|song|playlist|audio player|podcast|lyrics|equali[sz]er|spotify|deezer|tidal|qobuz",
    "video": r"video|movie|stream|youtube|newpipe|\btv\b|anime|series|film",
    "messaging": r"telegram|messenger|whatsapp|\bchat\b|\bsms\b|\bmms\b|e-?mail|dialer|phone calls?|contacts",
    "social": r"social network|reddit|instagram|tiktok|mastodon|twitter|feed",
    "browser": r"browser|gecko|chromium|web ?view|webkit",
    "files": r"file manager|file explorer|backup|restore|storage|archive|\bzip\b|cloud drive",
    "security": r"password|2fa|two-factor|authenticator|\bvpn\b|privacy|encrypt|vault",
    "finance": r"bank|wallet|crypto|payment|exchange|trading|money|finance",
    "shopping": r"shop|store front|marketplace|delivery|e-commerce|order",
    "photo": r"camera|photo|gallery|picture|image editor|wallpaper",
    "weather": r"weather|forecast",
    "maps": r"\bmaps?\b|navigation|travel|transit",
    "productivity": r"notes?\b|to-?do|calendar|tasks|office|document|pdf",
    "dev": r"terminal|shell|\broot\b|\badb\b|kernel|magisk|kernelsu|shizuku|apk installer|payload|"
           r"developer|linux|ssh|code editor|virtual machine|\bvm\b",
    "system": r"launcher|keyboard|icon pack|theme|material you|settings|battery|clock|calculator|dsp|tweak",
    "ai": r"\bai\b|assistant|chatgpt|\bllm\b|gemini|claude|qwen|copilot",
    "learning": r"learn|language|course|lesson|dictionary|news|read(er|ing)|books?",
    "health": r"fitness|workout|health|running|steps|water|sleep",
    "game": r"\bgame\b|play with friends|multiplayer|levels|puzzle",
}


def guess_score(text):
    """-> (the category whose words appear most in `text`, how many times)"""
    t = (text or "").lower()
    best, score = None, 0
    for key, rx in KEYWORDS.items():
        n = len(re.findall(rx, t))
        if n > score:
            best, score = key, n
    return best, score


def guess(text):
    """the category whose words appear most in `text` (store / README text) -> key or None"""
    return guess_score(text)[0]


GENERIC = ("system", "productivity")       # Play's TOOLS / PRODUCTIVITY say little: the app's words decide


def _design(slug):
    p = ROOT / "work" / slug / "design.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _line(text, key):
    for ln in text.splitlines():
        if ln.lower().startswith(key + ":"):
            return ln.split(":", 1)[1].strip()
    return ""


def store_info(slug):
    p = ROOT / "work" / slug / "refs" / "store" / "store.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except ValueError:
        return {}


def from_play(code):
    """Play Store category code -> our key (or None)."""
    code = (code or "").upper()
    for key, (_t, codes, _o, _g, _n) in CATEGORIES.items():
        if any(code == c or (c.endswith("_") and code.startswith(c)) for c in codes):
            return key
    return None


def category_of(slug):
    """-> (key or None, where it came from)."""
    v = _line(_design(slug), "category").split()[0].lower() if _line(_design(slug), "category") else ""
    v = v.strip("<>,")
    if v in CATEGORIES:
        return v, "design.md"
    st = store_info(slug)
    k = st.get("category_key") or from_play(st.get("category"))
    if k:
        return k, st.get("source", "store")
    return None, ""


def object_of(slug, key):
    """Which object of family `key` this app uses -> object name or ''. Read from the APPROVED
    concept's line in design.md (the object named first wins), else the 'function object' line."""
    text = _design(slug)
    approved = _line(text, "approved")
    letter = approved[:1].upper() if approved[:1].isalpha() else ""
    sources = []
    if letter:
        m = re.search(rf"^\s+{letter}\b[^:\n]*:\s*(.+)$", text, re.M)
        if m:
            sources.append(m.group(1))
    sources.append(_line(text, "function object (what the app does, as a physical thing)"))
    for src in sources:
        best = None
        for name, _fn, kw in CATEGORIES[key][2]:
            m = re.search(kw, src.lower())
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), name)
        if best:
            return best[1]
    return ""


# objects that ARE another app's logo: never "free" for a different app (owner 2026-11-22:
# Mesajlar got Telegram's paper plane)
RESERVED = {"paper plane": "telegram (its logo)", "music note": "apple_music (its logo)"}


def _first_object(src, key):
    best = None
    for name, _fn, kw in CATEGORIES[key][2]:
        m = re.search(kw, src.lower())
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), name)
    return best[1] if best else ""


def style_objects(slug, key):
    """{style: object of family `key`} for every style of the app: design.md 'styles:'
    (symbol=C faithful=A ...) -> each letter's concept line -> the object named first in it."""
    text = _design(slug)
    out = {}
    for st, letter in re.findall(r"\b(symbol|faithful|disc|rimmed)\s*=\s*([A-H])\b", _line(text, "styles")):
        m = re.search(rf"^\s+{letter}\b[^:\n]*:\s*(.+)$", text, re.M)
        if m and re.search(r"\b(logo|mark|measured)\b[^.(]{0,40}\bitself\b", m.group(1), re.I):
            continue                     # the mark IS the object: its gear/wrench is the logo's, no family object
        o = _first_object(m.group(1), key) if m else ""
        if o:
            out[st] = o
    return out


def clashes(slug):
    """[(style, object, [other apps])]: a style uses an object that another app of the same
    category already uses in ANY of its styles (owner 2026-11-22: Apple Music got Deezer's
    cassette). An app's own reserved logo object (RESERVED) is never a clash for it."""
    key, _ = category_of(slug)
    if not key:
        return []
    mine = style_objects(slug, key)
    if not mine:
        return []
    others = {}
    for name, who in RESERVED.items():
        if not who.startswith(slug):
            others.setdefault(name, []).append(who.split()[0])
    for d in sorted((ROOT / "work").glob("*/design.md")):
        s = d.parent.name
        if s == slug or s.startswith(("_", "zz_", "test_")):
            continue
        if category_of(s)[0] != key:
            continue
        objs = set(style_objects(s, key).values()) or ({object_of(s, key)} - {""})
        for o in objs:
            others.setdefault(o, []).append(s)
    return [(st, o, sorted(set(others[o]))) for st, o in mine.items() if o in others]


def used(key, skip=None):
    """{object name: [slugs]} for every app of category `key` that already has a design."""
    out = {name: [who] for name, who in RESERVED.items()
           if any(o[0] == name for o in CATEGORIES[key][2]) and not who.startswith(str(skip))}
    for d in sorted((ROOT / "work").glob("*/design.md")):
        slug = d.parent.name
        if slug == skip or slug.startswith(("_", "zz_")):
            continue
        k, _ = category_of(slug)
        if k != key:
            continue
        o = object_of(slug, key)
        if o and slug not in " ".join(out.get(o, [])):
            out.setdefault(o, []).append(slug)
    return out


def suggest(slug):
    """Text block for tools/next.py: the family, what is used, what is free."""
    key, src = category_of(slug)
    if not key:
        return ("CATEGORY: unknown - run  python3 tools/fetch_refs.py " + slug + "  (reads the store category), or write\n"
                "  'category: <key>' in design.md, key one of: " + ", ".join(CATEGORIES))
    title, _codes, objs, gnome, note = CATEGORIES[key]
    u = used(key, skip=slug)
    lines = [f"CATEGORY: {key} ({title}; from {src}) - its object family (REDESIGN.md 3):"]
    for name, fn, _kw in objs:
        who = u.get(name)
        lines.append(f"  - {name:28s} {('objects.py: ' + fn + '()') if fn else '(compose it)':28s} "
                     + (f"USED by {', '.join(who)}" if who else "free"))
    if gnome:
        lines.append(f"  GNOME apps of this kind (their icons are the model): {gnome}")
    if note:
        lines.append(f"  note: {note}")
    lines.append("  Prefer a FREE object for the main concept. Sharing one is allowed only when the brand colours")
    lines.append("  and the mark (>= 36 px, gate mark_size) make it clearly a different app.")
    return "\n".join(lines)


def markdown():
    out = ["# Categories → object families",
           "",
           "Generated by `python3 work/_lib/categories.py --md` from `work/_lib/categories.py`. Rule:",
           "[REDESIGN.md §3](../../REDESIGN.md). An app's category gives the family of objects; apps of the same",
           "category take **different** objects of the family when they can (`tools/next.py` lists which are",
           "used). Functions are in `work/_lib/objects.py` ([OBJECTS.md](OBJECTS.md)); *compose it* = no ready",
           "object yet, build it from primitives.",
           ""]
    for key, (title, codes, objs, gnome, note) in CATEGORIES.items():
        out.append(f"## `{key}` — {title}")
        if codes:
            out.append(f"Play Store: {', '.join('`' + c + '*`' if c.endswith('_') else '`' + c + '`' for c in codes)}")
        out.append("")
        out.append("| Object | Ready function | Used by |")
        out.append("|---|---|---|")
        u = used(key)
        for name, fn, _kw in objs:
            out.append(f"| {name} | {('`' + fn + '()`') if fn else 'compose it'} | {', '.join(u.get(name, [])) or '—'} |")
        if gnome:
            out.append(f"\nGNOME apps of this kind: {gnome}.")
        if note:
            out.append(f"Note: {note}.")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    if "--md" in sys.argv:
        (ROOT / "docs/redesign/CATEGORIES.md").write_text(markdown() + "\n", encoding="utf-8")
        print("wrote docs/redesign/CATEGORIES.md")
    elif len(sys.argv) > 1:
        print(suggest(sys.argv[1]))
    else:
        print(__doc__)
