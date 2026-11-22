#!/usr/bin/env python3
"""Find REFERENCES for an app anywhere it is published - screenshots, the store icon, the category,
the description - so any model (also one that cannot browse or cannot see images) knows what the
app is and shows. The owner (2026-11-22): "DeepSeek could not find screenshots ... look on GitHub,
Uptodown, APKMirror, everywhere (exteraless, a Telegram client)".

    python3 tools/fetch_refs.py <slug>                       # package + name from the pack / request
    python3 tools/fetch_refs.py <slug> --package com.exteraless.app --name exteraless
    python3 tools/fetch_refs.py <slug> --url https://github.com/exteraless/exteraless
    python3 tools/fetch_refs.py <slug> --url https://t.me/s/somechannel --n 8 --force

Where it looks, in this order (the first place with screenshots wins; text is merged):
  1. system apps (com.android.*, Google/Samsung/Xiaomi system packages): no screenshots needed -
     the GNOME app for the same job is the reference (Settings, Clocks, Snapshot ...)
  2. Google Play - the US page, then TR, IN, GB, DE (region-locked apps: TikTok Lite ...)
  3. F-Droid, 4. IzzyOnDroid (FOSS apps that are not on Play)
  5. GitHub - repository search by package and by name, the repository VERIFIED by finding the
     package name in its gradle files / README; screenshots from fastlane/metadata, screenshot
     folders and the README (forks, Telegram/YouTube clients, root and developer tools ...)
  6. Uptodown - its page for the app name, verified by the package name on the page
  -  any --url you give: GitHub / GitLab / Codeberg repository, Uptodown, F-Droid, IzzyOnDroid,
     Play, a Telegram channel (t.me), or any web page (its og:image and big images)
APKMirror and APKPure block scripts (HTTP 403); open them in a browser yourself if needed.

Writes work/<slug>/refs/store/ (NOT in git - store images are not ours):
  shot-1.jpg ...      screenshots          icon.png   the store icon (often sharper than the phone's)
  sheet.jpg           all on one image     store.json everything below + where it searched
and in work/<slug>/design.md (only if missing): 'category: <key>' and 'store: <url> (...)'.
It prints all of it as TEXT (title, category, description, the screenshots' main colours with GNOME
names, the category's object family) for models without vision.

Nothing found? The owner is asked in Q1 for 2-3 screenshots, or they are taken on the phone:
  adb exec-out screencap -p > work/<slug>/refs/phone-1.png        (USB debugging)
  su -c 'screencap -p /sdcard/s.png'                               (rooted phone, then copy it)
Owner screenshots go to work/<slug>/refs/ (committed); fetched ones stay in refs/store/ (ignored).
GitHub without a token allows 60 requests an hour: export GITHUB_TOKEN=... (or log in with gh).
"""
import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36"
ITEM_RE = re.compile(r'<item\s+component="ComponentInfo\{([^/"]+)/[^"]*\}"\s+drawable="([^"]+)"')
PLAY_REGIONS = ("US", "TR", "IN", "GB", "DE")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
NOT_SHOT = re.compile(r"badge|shields\.io|logo|icon|banner|sponsor|donat|ko-fi|buymeacoffee|paypal|liberapay|"
                      r"get-it-on|getiton|google-play|fdroid\.png|obtainium|izzy|avatar|\.svg($|\?)|emoji", re.I)
sys.path.insert(0, str(ROOT / "work/_lib"))
sys.path.insert(0, str(ROOT / "tools"))

# system packages: no store page - the GNOME app for the same job is the reference
SYSTEM = {
    "settings": ("system", "Settings (GNOME Settings: gears / a control panel)"),
    "camera": ("photo", "Camera (GNOME Snapshot: a camera lens)"),
    "vending": ("shopping", "Play Store (a shopping bag with the play triangle - GNOME Software is a bag)"),
    "dialer": ("messaging", "Phone (GNOME Calls: a handset)"),
    "contacts": ("messaging", "Contacts (GNOME Contacts: an address card)"),
    "messaging": ("messaging", "Messages (GNOME Chatty: a speech bubble)"),
    "mms": ("messaging", "Messages (GNOME Chatty: a speech bubble)"),
    "deskclock": ("system", "Clock (GNOME Clocks: a clock face)"),
    "calculator": ("system", "Calculator (GNOME Calculator)"),
    "gallery": ("photo", "Gallery (GNOME Loupe / Photos: a photo print)"),
    "documentsui": ("files", "Files (GNOME Files: a filing cabinet)"),
    "calendar": ("productivity", "Calendar (GNOME Calendar: a calendar page)"),
}
SYSTEM_PREFIXES = ("com.android.", "com.google.android.apps.nexuslauncher", "com.sec.android.app.",
                   "com.samsung.android.", "com.miui.", "com.xiaomi.", "com.coloros.", "com.oplus.", "com.oneplus.")


# ------------------------------------------------------------------ network
def get(url, binary=False, timeout=25, headers=None):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"}
    h.update(headers or {})
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


_TOKEN = None


def gh_token():
    global _TOKEN
    if _TOKEN is None:
        _TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
        if not _TOKEN and shutil.which("gh"):
            r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
            _TOKEN = r.stdout.strip() if r.returncode == 0 else ""
    return _TOKEN


def gh_api(path):
    h = {"Accept": "application/vnd.github+json"}
    if gh_token():
        h["Authorization"] = f"Bearer {gh_token()}"
    for attempt in range(2):
        try:
            return json.loads(get("https://api.github.com/" + path.lstrip("/"), headers=h))
        except urllib.error.HTTPError as e:
            if e.code == 403 and attempt == 0 and "search" in path:
                time.sleep(7)                     # search: 10 a minute without a token
                continue
            raise


# ------------------------------------------------------------------ the app
def package_of(slug):
    p = ROOT / "app/src/main/res/xml/appfilter.xml"
    if p.exists():
        for pkg, d in ITEM_RE.findall(p.read_text(encoding="utf-8")):
            if d == slug:
                return pkg
    tsv = ROOT / "work/_lib/batch_apps.tsv"
    if tsv.exists():
        for ln in tsv.read_text(encoding="utf-8").splitlines():
            c = ln.split("\t")
            if len(c) > 2 and c[0] == slug:
                m = re.search(r"ComponentInfo\{([^/]+)/", c[2])
                if m:
                    return m.group(1)
    d = ROOT / "work" / slug / "design.md"
    m = re.search(r"^package:\s*([A-Za-z0-9_.]+)", d.read_text(encoding="utf-8"), re.M) if d.exists() else None
    return m.group(1) if m else None


def name_of(slug):
    tsv = ROOT / "work/_lib/batch_apps.tsv"
    if tsv.exists():
        for ln in tsv.read_text(encoding="utf-8").splitlines():
            c = ln.split("\t")
            if len(c) > 1 and c[0] == slug:
                return c[1]
    return slug.replace("_", " ").strip()


def text_of(fragment):
    t = re.sub(r"<br\s*/?>|</p>|</li>", "\n", fragment)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(t)).strip()


def md_text(md):
    """README markdown -> plain text (no badges, images, html, code)"""
    t = re.sub(r"```.*?```", "", md, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"^[#>*\-\s|:]+", "", t, flags=re.M)
    lines = [ln.strip() for ln in t.splitlines() if len(ln.strip()) > 2 and not ln.strip().startswith("[")]
    return html.unescape("\n".join(lines))[:1500]


# ------------------------------------------------------------------ sources
def system(pkg, name):
    if not pkg.startswith(SYSTEM_PREFIXES) or pkg.startswith("com.google.android.apps.photos"):
        return None
    for k, (cat, what) in SYSTEM.items():
        if k in pkg.lower():
            return {"source": "system app", "url": "", "title": name, "category_key": cat,
                    "summary": f"system app - reference: {what}", "description": "", "shots": [], "icon": ""}
    return {"source": "system app", "url": "", "title": name, "category_key": "system",
            "summary": "system app - use the GNOME app for the same job as the reference", "description": "",
            "shots": [], "icon": ""}


def parse_play(s, url):
    """a Play Store app page (HTML) -> info dict (title, category, summary, description, icon, shots)"""
    info = {"source": "Google Play", "url": url}
    m = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S)
    if m:
        try:
            d = json.loads(m.group(1))
            info.update(title=d.get("name", ""), category=d.get("applicationCategory", ""),
                        summary=d.get("description", ""), icon=d.get("image", ""))
        except ValueError:
            pass
    m = re.search(r'data-g-id="description"[^>]*>(.*?)</div>', s, re.S)
    info["description"] = text_of(m.group(1))[:1500] if m else ""
    shots = []
    for u in re.findall(r'<img[^>]+src="(https://play-lh\.googleusercontent\.com/[^"=]+)[^"]*"[^>]*alt="Screenshot image"', s):
        if u not in shots:
            shots.append(u)
    info["shots"] = [u + "=s1280" for u in shots]
    if info.get("icon") and "=" not in info["icon"].rsplit("/", 1)[-1]:
        info["icon"] += "=s512"
    if not info.get("title"):
        raise ValueError("not a Play Store app page")
    return info


def play(pkg, name):
    for gl in PLAY_REGIONS:
        url = f"https://play.google.com/store/apps/details?id={pkg}&hl=en&gl={gl}"
        try:
            return parse_play(get(url), url)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
    raise ValueError("not on Google Play (US, TR, IN, GB, DE)")


def fdroid(pkg, name, url=None):
    url = url or f"https://f-droid.org/en/packages/{pkg}/"
    s = get(url)
    info = {"source": "F-Droid", "url": url, "category": ""}
    m = re.search(r'<h3 class="package-name">(.*?)</h3>', s, re.S)
    info["title"] = text_of(m.group(1)) if m else name
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    info["summary"] = html.unescape(m.group(1)) if m else ""
    m = re.search(r'<div class="package-description"[^>]*>(.*?)</div>', s, re.S)
    info["description"] = text_of(m.group(1))[:1500] if m else ""
    m = re.search(r'og:image" content="([^"]+)"', s)
    info["icon"] = m.group(1) if m else ""
    info["shots"] = list(dict.fromkeys(re.findall(r'src="(https://f-droid\.org/repo/[^"]*Screenshots/[^"]+)"', s)))
    m = re.search(r'href="(https://(?:github\.com|gitlab\.com|codeberg\.org)/[^"/]+/[^"/#?]+)', s)
    info["code"] = m.group(1) if m else ""
    return info


def izzy(pkg, name, url=None):
    url = url or f"https://apt.izzysoft.de/fdroid/index/apk/{pkg}"
    s = get(url)
    info = {"source": "IzzyOnDroid", "url": url, "category": ""}
    m = re.search(r"<title>([^<]*)</title>", s)
    info["title"] = text_of(m.group(1)).split(" - ")[0].strip() if m else name
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    info["summary"] = html.unescape(m.group(1)) if m else ""
    m = re.search(r"<div[^>]*class=['\"][^'\"]*(?:appdetails|description)[^'\"]*['\"][^>]*>(.*?)</div>", s, re.S)
    info["description"] = text_of(m.group(1))[:1500] if m else ""
    shots = re.findall(r"src=['\"](/fdroid/repo/[^'\"]*Screenshots/[^'\"]+)['\"]", s)
    info["shots"] = list(dict.fromkeys("https://apt.izzysoft.de" + p for p in shots))
    m = re.search(r"src=['\"](/fdroid/repo/[^'\"]*/icon[^'\"]*\.png)['\"]", s)
    info["icon"] = "https://apt.izzysoft.de" + m.group(1) if m else ""
    m = re.search(r'href="(https://(?:github\.com|gitlab\.com|codeberg\.org)/[^"/]+/[^"/#?]+)', s)
    info["code"] = m.group(1) if m else ""
    if not (info["shots"] or info["description"] or info["summary"]):
        raise ValueError("not on IzzyOnDroid")
    return info


def _readme_images(md, raw_base):
    out = []
    for u in re.findall(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)", md) + re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", md):
        if NOT_SHOT.search(u):
            continue
        if u.startswith("//"):
            u = "https:" + u
        elif not u.startswith("http"):
            u = raw_base + u.lstrip("./")
        u = re.sub(r"https://github\.com/([^/]+/[^/]+)/blob/", r"https://raw.githubusercontent.com/\1/", u)
        if u not in out:
            out.append(u)
    return out


def _git_files(full):
    """file list of a GitHub repository without the API (blobless shallow clone; needs git)"""
    import tempfile
    if not shutil.which("git"):
        return []
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                            f"https://github.com/{full}", tmp + "/r"], capture_output=True, text=True, timeout=120)
        if r.returncode:
            return []
        r = subprocess.run(["git", "-C", tmp + "/r", "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True)
        return r.stdout.splitlines()


def github_repo(full, pkg, name, hint=None):
    """screenshots + text of one GitHub repository (owner/name); `hint` = its search result"""
    hint = hint or {}
    try:
        meta = gh_api(f"repos/{full}")
    except (urllib.error.URLError, ValueError):
        meta = hint                                     # API blocked / rate-limited: search data
    branch = meta.get("default_branch") or "HEAD"
    raw = f"https://raw.githubusercontent.com/{full}/{branch}/"
    info = {"source": "GitHub", "url": meta.get("html_url") or f"https://github.com/{full}",
            "title": meta.get("name") or full.split("/")[1], "summary": meta.get("description") or "",
            "topics": meta.get("topics") or [], "category": "", "icon": ""}
    try:
        paths = [t["path"] for t in gh_api(f"repos/{full}/git/trees/{branch}?recursive=1").get("tree", [])
                 if t.get("type") == "blob"]
    except (urllib.error.URLError, ValueError):
        paths = _git_files(full)
    # app resources (res/, src/) are UI parts, not screenshots: only docs-like places count
    imgs = [p for p in paths if p.lower().endswith(IMG_EXT) and not re.search(r"(^|/)(res|src|build)/", p)]
    fast = sorted([p for p in imgs if re.search(r"phoneScreenshots/", p)], key=lambda p: ("en-US" not in p, p))
    other = [p for p in imgs if re.search(r"screenshot|screens?/|preview", p, re.I) and p not in fast and not NOT_SHOT.search(p)]
    shots = [raw + p for p in fast + other]
    info["quality"] = "store" if fast else "readme"           # fastlane screenshots = as good as a store
    icons = [p for p in paths if re.search(r"(fastlane/metadata/android/en-US/images/icon\.png|"
                                           r"res/mipmap-xxxhdpi/ic_launcher(_round)?\.(png|webp))$", p)]
    info["icon"] = raw + icons[0] if icons else ""
    readme = next((p for p in paths if re.fullmatch(r"readme(\.md|\.markdown)?", p, re.I)), "README.md")
    try:
        md = get(raw + readme)
    except urllib.error.URLError:
        md = ""
    info["description"] = md_text(md)
    shots += [u for u in _readme_images(md, raw) if u not in shots]
    info["shots"] = shots
    # verified: "code" = the package (or its base without .beta/.foss/...) is in a gradle file or the
    # manifest of THIS repository; "readme" = only mentioned in the README (a fork, a mod, a list)
    base = re.sub(r"\.(beta|canary|debug|foss|plus|pro|nightly|dev|lite|free|revived)$", "", pkg)
    checks = [p for p in paths if re.search(r"(^|/)(build\.gradle(\.kts)?|AndroidManifest\.xml|gradle\.properties|"
                                             r"libs\.versions\.toml)$", p) and p.count("/") <= 3][:12]
    verified = False
    for p in checks:
        try:
            t = get(raw + p)
        except urllib.error.URLError:
            continue
        if re.search(rf"""(applicationId|namespace|package)\s*=?\s*["']({re.escape(pkg)}|{re.escape(base)})["']""", t) \
                or pkg in t:
            verified = "code"
            break
    if not verified and pkg.lower() in md.lower():
        verified = "readme"
    info["verified"] = verified
    return info


def github(pkg, name, url=None):
    if url:
        full = "/".join(urllib.parse.urlparse(url).path.strip("/").split("/")[:2])
        return github_repo(full, pkg, name)
    cands = {}
    segs = pkg.split(".")
    if len(segs) >= 3 and segs[0] in ("io", "com") and segs[1] in ("github", "gitlab"):      # io.github.<user>.<repo>
        for repo in dict.fromkeys([segs[3] if len(segs) > 3 else segs[2], (segs[3] if len(segs) > 3 else segs[2]).replace("_", "-")]):
            try:
                r = gh_api(f"repos/{segs[2]}/{repo}")
                cands[r["full_name"]] = (True, -1, r)
            except (urllib.error.URLError, ValueError):
                try:                                    # API blocked: does the repository exist at all?
                    get(f"https://raw.githubusercontent.com/{segs[2]}/{repo}/HEAD/README.md")
                    cands[f"{segs[2]}/{repo}"] = (True, -1, {"full_name": f"{segs[2]}/{repo}"})
                except urllib.error.URLError:
                    pass
    queries = [f'"{pkg}" in:readme,description', f"{name} android in:name,description", f"{name} in:name"]
    if len(segs) >= 3 and segs[1] not in ("android", "google", "github", "app", "apps"):
        queries.insert(1, f"{name} user:{segs[1]}")                                           # com.<user>.<app>
    for q in queries:
        try:
            res = gh_api("search/repositories?per_page=5&q=" + urllib.parse.quote(q))
        except (urllib.error.URLError, ValueError):
            continue
        for rank, r in enumerate(res.get("items", [])):
            if not r.get("archived"):
                cands.setdefault(r["full_name"], (q.startswith('"'), rank, r))
    if not cands:
        raise ValueError("no GitHub repository found")
    norm = re.sub(r"[^a-z0-9]", "", name.lower())
    named = lambda full: re.sub(r"[^a-z0-9]", "", full.split("/")[1].lower()) == norm  # noqa: E731
    # a repo named like the app first, then the ones that mention the package, then stars; forks last
    order = sorted(cands.items(), key=lambda kv: (not named(kv[0]), not kv[1][0], kv[1][2].get("fork", False),
                                                  -kv[1][2].get("stargazers_count", 0)))
    weak = []
    for full, (_by_pkg, _rank, r) in order[:6]:
        try:
            info = github_repo(full, pkg, name, hint=r)
        except (urllib.error.URLError, ValueError, subprocess.TimeoutExpired):
            continue
        if info["verified"] == "code":
            return info
        if info["verified"] == "readme":                # only a mention: a fork, a mod, a list - keep looking
            weak.append(info)
    if weak:
        best = weak[0]
        best["summary"] = ("(NOT VERIFIED: the package name is not in this repository's code - check that it is the "
                           "right app) " + best["summary"])
        return best
    raise ValueError("GitHub: no repository contains " + pkg + " (tried " + ", ".join(k for k, _ in order[:6]) + ")")


def uptodown(pkg, name, url=None):
    guesses = [url] if url else []
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    segs = [x.lower() for x in pkg.split(".") if x.lower() not in ("com", "org", "app", "android", "net", "io", "dev",
                                                                     "beta", "canary", "plus", "pro", "lite", "free")]
    for g in dict.fromkeys([base, base.replace("-", "")] + segs[:3]):
        if g and not url:
            guesses.append(f"https://{g}.en.uptodown.com/android")
    core = re.sub(r"\.(beta|canary|debug|foss|plus|pro|nightly|dev|lite|free|revived)$", "", pkg)
    for u in guesses:
        try:
            s = get(u)
        except urllib.error.URLError:
            continue
        m = re.search(r"Package Name</th>\s*<td[^>]*>\s*([A-Za-z0-9_.]+)", s)
        if not url and (not m or m.group(1) not in (pkg, core)):
            continue
        info = {"source": "Uptodown", "url": u, "category": ""}
        m = re.search(r'<meta property="og:title" content="([^"]*)"', s)
        info["title"] = re.sub(r"\s*\((Android|APK)\)\s*$", "", html.unescape(m.group(1)).split(" for Android")[0]) if m else name
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        info["summary"] = html.unescape(m.group(1)) if m else ""
        m = re.search(r'<div class="text-description"[^>]*>(.*?)</div>', s, re.S)
        info["description"] = text_of(m.group(1))[:1500] if m else ""
        shots = re.findall(r"(https://img\.utdstc\.com/screen/[0-9a-f/]+)", s)
        info["shots"] = [u2 + ":800" for u2 in dict.fromkeys(shots)]
        m = re.search(r"(https://img\.utdstc\.com/icon/[0-9a-f/]+)", s)
        info["icon"] = m.group(1) + ":512" if m else ""
        return info
    raise ValueError("not on Uptodown (guessed: " + ", ".join(guesses) + ")")


def telegram(pkg, name, url):
    chan = urllib.parse.urlparse(url).path.strip("/").split("/")[-1]
    u = f"https://t.me/s/{chan}"
    s = get(u)
    m = re.search(r'<div class="tgme_channel_info_description">(.*?)</div>', s, re.S)
    shots = re.findall(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('(https://[^']+)'\)", s)
    m2 = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    return {"source": "Telegram channel", "url": u, "title": chan, "category": "", "quality": "readme",
            "summary": text_of(m.group(1)) if m else "", "description": "", "icon": m2.group(1) if m2 else "",
            "shots": list(dict.fromkeys(reversed(shots)))}


def gitlab_like(pkg, name, url):
    p = urllib.parse.urlparse(url)
    full = "/".join(p.path.strip("/").split("/")[:2])
    host = f"{p.scheme}://{p.netloc}"
    md, raw = "", ""
    for br in ("HEAD", "main", "master"):
        raw = f"{host}/{full}/-/raw/{br}/" if "gitlab" in p.netloc else f"{host}/{full}/raw/branch/{br}/"
        try:
            md = get(raw + "README.md")
            break
        except urllib.error.URLError:
            continue
    shots = []
    for i in range(1, 9):
        for ext in ("png", "jpg"):
            shots.append(f"{raw}fastlane/metadata/android/en-US/images/phoneScreenshots/{i}.{ext}")
    return {"source": p.netloc, "url": url, "title": full.split("/")[-1], "category": "", "quality": "readme",
            "summary": "", "description": md_text(md), "icon": "", "shots": _readme_images(md, raw) + shots}


def web(pkg, name, url):
    s = get(url)
    og = lambda k: (re.search(rf'<meta[^>]+property="og:{k}"[^>]+content="([^"]*)"', s) or [None, ""])[1]  # noqa: E731
    imgs = [urllib.parse.urljoin(url, u) for u in re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", s) if not NOT_SHOT.search(u)]
    return {"source": urllib.parse.urlparse(url).netloc, "url": url, "title": html.unescape(og("title")) or name,
            "category": "", "quality": "readme", "summary": html.unescape(og("description")), "description": "", "icon": og("image"),
            "shots": list(dict.fromkeys(imgs))}


def from_url(pkg, name, url):
    host = urllib.parse.urlparse(url).netloc.lower()
    if "play.google.com" in host:
        return parse_play(get(url), url)
    if "f-droid.org" in host:
        return fdroid(pkg, name, url)
    if "izzysoft" in host:
        return izzy(pkg, name, url)
    if host.endswith("github.com"):
        return github(pkg, name, url)
    if "gitlab" in host or "codeberg.org" in host:
        return gitlab_like(pkg, name, url)
    if "uptodown.com" in host:
        return uptodown(pkg, name, url)
    if host in ("t.me", "telegram.me"):
        return telegram(pkg, name, url)
    return web(pkg, name, url)


# ------------------------------------------------------------------ images
def download_shots(urls, n, out):
    """download, drop tiny/duplicate/non-screenshot images; -> list of PIL images"""
    imgs, seen = [], set()
    for u in urls:
        if len(imgs) >= n:
            break
        try:
            data = get(u, binary=True)
            im = Image.open(io.BytesIO(data)).convert("RGB")
        except (urllib.error.URLError, OSError, ValueError):
            continue
        h = hashlib.md5(data).hexdigest()
        w_, h_ = im.size
        if h in seen or min(w_, h_) < 240 or max(w_, h_) < 400:
            continue                                    # icons, badges, thumbnails
        seen.add(h)
        im.save(out / f"shot-{len(imgs) + 1}.jpg", quality=85)
        imgs.append(im)
    return imgs


def main_colours(images, k=6):
    """the main colours of the screenshots (k-means), with the nearest GNOME HIG name"""
    import describe_icon as di
    if not images:
        return []
    px = np.concatenate([np.asarray(im.convert("RGB").resize((96, 96))).reshape(-1, 3).astype(float) for im in images])
    from scipy.cluster.vq import kmeans2
    cent, lbl = kmeans2(px, k, minit="++", seed=0)
    out = []
    for c in np.argsort(-np.bincount(lbl, minlength=k)):
        share = float((lbl == c).mean())
        if share < 0.03:
            continue
        hx = "#%02x%02x%02x" % tuple(int(v) for v in np.clip(cent[c], 0, 255))
        (cname, h), dist = di.nearest(cent[c])
        out.append(f"{hx} {share:4.0%} ~ {cname} {h}" + ("" if dist < 40 else " (far from HIG)"))
    return out


def sheet(icon, shots, out):
    H = 640
    tiles = [icon.convert("RGBA").resize((256, 256))] if icon is not None else []
    tiles += [im.convert("RGBA").resize((int(im.width * H / im.height), H)) for im in shots]
    if not tiles:
        return
    W = sum(t.width for t in tiles) + 16 * (len(tiles) + 1)
    s = Image.new("RGB", (W, H + 32), (246, 245, 244))
    x = 16
    for t in tiles:
        s.paste(t, (x, 16), t)
        x += t.width + 16
    s.save(out, quality=85)


def fill_design(slug, info, key):
    d = ROOT / "work" / slug / "design.md"
    if not d.exists():
        return []
    text = d.read_text(encoding="utf-8")
    added = []
    cat_line = re.search(r"^category:[ \t]*(.*)$", text, re.M)
    if key and (not cat_line or not cat_line.group(1).strip() or cat_line.group(1).strip().startswith("<")):
        how = info.get("category_how", "")
        val = f"category: {key}" + ("   (guessed from the text - check it)" if how.startswith("guessed") else "")
        if cat_line:
            text = text[:cat_line.start()] + val + text[cat_line.end():]
        else:
            text = re.sub(r"^(kind:.*)$", lambda m: m.group(1) + "\n" + val, text, count=1, flags=re.M)
        added.append(val)
    if not re.search(r"^store:", text, re.M):
        where = info.get("url") or info["source"]
        line = f"store: {where} ({info.get('category') or info['source']}, fetched {date.today()}; refs/store/, not in git)"
        text = re.sub(r"^(source:.*)$", rf"\1\n{line}", text, count=1, flags=re.M)
        added.append("store: ...")
    d.write_text(text, encoding="utf-8")
    return added


def category_key(info):
    """Gnomed category: system app > Play Store code > words in the title/description/topics
    (a word guess is marked in store.json as category_how = "guessed" - the agent checks it)"""
    import categories
    if info.get("category_key"):
        return info["category_key"]
    k = categories.from_play(info.get("category"))
    head = " ".join([info.get("title", ""), info.get("summary", ""), " ".join(info.get("topics", []))])
    if k:
        g, n = categories.guess_score(head)
        if k in categories.GENERIC and g and g != k and n >= 1:      # TOOLS -> a terminal is "dev"
            info["category_how"] = f"store says {info.get('category')}; its name/summary say {g}"
            return g
        info["category_how"] = "store"
        return k
    k = categories.guess((head + " ") * 3 + info.get("description", "")[:800])
    if k:
        info["category_how"] = "guessed from the words of the store/README text - check it"
    return k


def known_url(slug):
    """a source the owner or an earlier run wrote in design.md ('store:' / 'refs-url:')"""
    d = ROOT / "work" / slug / "design.md"
    if d.exists():
        for key in ("refs-url", "store"):
            m = re.search(rf"^{key}:\s*(https?://\S+)", d.read_text(encoding="utf-8"), re.M)
            if m:
                return m.group(1)
    return None


# ------------------------------------------------------------------ main
def collect(pkg, name, urls):
    """try every source; the first with screenshots wins, text is merged. -> (info, tried)"""
    tried, best_text, found = [], None, None
    steps = [("url " + u, lambda u=u: from_url(pkg, name, u)) for u in urls]
    steps += [("system", lambda: system(pkg, name)), ("Google Play", lambda: play(pkg, name)),
              ("F-Droid", lambda: fdroid(pkg, name)), ("IzzyOnDroid", lambda: izzy(pkg, name)),
              ("Uptodown", lambda: uptodown(pkg, name)), ("GitHub", lambda: github(pkg, name))]
    for label, fn in steps:
        try:
            info = fn()
        except (urllib.error.URLError, ValueError, TimeoutError, OSError, KeyError) as e:
            tried.append(f"{label}: {str(e)[:90]}")
            continue
        if info is None:
            continue
        tried.append(f"{label}: {info.get('url') or 'ok'} ({len(info.get('shots', []))} images)")
        if info.get("source") == "system app":
            return info, tried
        if best_text is None and (info.get("description") or info.get("summary")):
            best_text = info
        if info.get("code") and not any("github" in u or "gitlab" in u or "codeberg" in u for u in urls):
            steps.append((f"code {info['code']}", lambda c=info["code"]: from_url(pkg, name, c)))
        if info.get("shots"):
            if info.get("quality", "store") == "store":     # real screenshots: stop here
                found = info
                break
            if found is None:                                # README / page images: keep looking
                found = info
    if found is None and best_text is None:
        return None, tried
    info = dict(found or best_text)
    if best_text and found and not found.get("description"):
        info["description"] = best_text.get("description", "")
        info["summary"] = info.get("summary") or best_text.get("summary", "")
        info["category"] = info.get("category") or best_text.get("category", "")
    return info, tried


def main():
    argv = sys.argv[1:]
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or not argv[i - 1] in ("--package", "--n", "--url", "--name"))]
    if not args:
        sys.exit(__doc__)
    slug = args[0]
    val = lambda k: argv[argv.index(k) + 1] if k in argv else None  # noqa: E731
    pkg = val("--package") or package_of(slug)
    name = val("--name") or name_of(slug)
    n = int(val("--n") or 6)
    urls = [argv[i + 1] for i, a in enumerate(argv) if a == "--url" and i + 1 < len(argv)]
    if not urls and known_url(slug):
        urls = [known_url(slug)]
    if not pkg:
        sys.exit(f"no package for {slug}: python3 tools/fetch_refs.py {slug} --package <package.name> [--name 'App name']")
    out = ROOT / "work" / slug / "refs" / "store"
    if (out / "store.json").exists() and "--force" not in argv:
        info = json.loads((out / "store.json").read_text(encoding="utf-8"))
        print(f"already fetched ({info.get('source')}, {info.get('fetched')}) - --force to search again\n")
    else:
        info, tried = collect(pkg, name, urls)
        if info is None:
            print("searched:\n  " + "\n  ".join(tried))
            sys.exit(f"\n{name} [{pkg}]: nothing found. Give a page with --url (GitHub, Telegram channel, website), or\n"
                     "ask the owner in Q1 for 2-3 screenshots (or adb/su screencap - see the top of this file).")
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        imgs = download_shots(info.get("shots", []), n, out)
        icon = None
        if info.get("icon"):
            try:
                icon = Image.open(io.BytesIO(get(info["icon"], binary=True))).convert("RGBA")
                icon.save(out / "icon.png")
            except (urllib.error.URLError, OSError, ValueError):
                icon = None
        sheet(icon, imgs, out / "sheet.jpg")
        info["colours"] = main_colours(imgs)
        info.update(package=pkg, name=name, fetched=str(date.today()), saved=len(imgs), tried=tried)
        info["category_key"] = category_key(info)
        (out / "store.json").write_text(json.dumps(info, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    import categories
    key = info.get("category_key") or category_key(info)
    added = fill_design(slug, info, key)
    print(f"{info.get('title')}  [{pkg}]  - {info['source']}: {info.get('url') or '-'}")
    how = info.get("category_how", "")
    print(f"store category: {info.get('category') or '-'}  ->  Gnomed category: {key or '? (write category: in design.md)'}"
          + (f"  [{how}]" if how.startswith("guessed") else ""))
    for k in ("summary",):
        if info.get(k):
            print(f"{k}: {info[k]}")
    if info.get("description"):
        print("description (first lines):\n  " + "\n  ".join(info["description"][:700].splitlines()))
    if info.get("colours"):
        print("screenshots' main colours (share -> nearest GNOME HIG colour):\n  " + "\n  ".join(info["colours"]))
    print(f"files: work/{slug}/refs/store/ ({info.get('saved', 0)} screenshots, icon.png, sheet.jpg) - not in git")
    if info.get("tried"):
        print("searched:\n  " + "\n  ".join(info["tried"]))
    if info.get("saved", 0) == 0 and info.get("source") != "system app":
        print("NO SCREENSHOTS: ask the owner in Q1 for 2-3 (or --url a page that has them).")
    if added:
        print(f"design.md: added {', '.join(added)}")
    print()
    print(categories.suggest(slug))


if __name__ == "__main__":
    main()
