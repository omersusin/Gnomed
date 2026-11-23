#!/usr/bin/env python3
"""trendyolmilla - FOUR rough concepts A-D (REDESIGN.md step 3; docs/PLAYBOOK.md#draw-concepts). Run:
    python3 work/trendyolmilla/concepts/make_concepts.py && python3 tools/concepts.py trendyolmilla
A shopping bag, a woven clothing label, a round hat box and a wicker basket - the shopping
family, four different objects."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "work/_lib"))
from objects import *  # noqa: F401,F403,E402

SLUG = Path(__file__).resolve().parents[1].name
OUT = Path(__file__).resolve().parent
P = parts(SLUG)
R = regions(SLUG)
MARK = [g for _, g, _ in R]
COL = [f for _, _, f in R]

PURPLE = RAMP["Purple"]
LIGHT = RAMP["Light"]


def rr(x0, y0, x1, y1, r):
    return rounded(box(x0, y0, x1, y1), min(r, 0.45 * min(x1 - x0, y1 - y0)))


def A():
    """Symbol - a paper shopping bag with the wordmark on its front."""
    ic = gk.Icon("trendyolmilla concept A")
    body = rr(20, 54, 108, 116, 6)
    handles = circ(64, 56, 28).difference(circ(64, 56, 21)).intersection(box(0, 0, 128, 57))
    solid(ic, handles, face="#9a9996", depth=1.5, side="#77767b", top=False, layer="handles")
    solid(ic, body, face=gradient(SLUG, body), depth=5, side=PURPLE[4], layer="bag")
    put_mark(ic, SLUG, (28, 70, 100, 100), face="#ffffff")
    return ic


def B():
    """Faithful - a woven clothing label: the wordmark itself, white on brand-gradient fabric."""
    ic = gk.Icon("trendyolmilla concept B")
    tag = rr(12, 36, 116, 104, 5)
    solid(ic, tag, face=gradient(SLUG, tag), depth=4, side=PURPLE[4], layer="label")
    put_mark(ic, SLUG, (22, 50, 106, 90), face="#ffffff")
    return ic


def C():
    """Disc - a round hat box with the wordmark on its band."""
    ic = gk.Icon("trendyolmilla concept C")
    body = rr(14, 44, 114, 112, 18)
    solid(ic, body, face=[(0, PURPLE[2]), (1, PURPLE[4])], depth=6, side=PURPLE[4], layer="box")
    band = rr(14, 48, 114, 72, 10)
    solid(ic, band, face=[(0, PURPLE[1]), (1, PURPLE[3])], depth=4, side=PURPLE[4], layer="band")
    put_mark(ic, SLUG, (22, 51, 106, 69), face="#ffffff")
    return ic


def D():
    """Rimmed - a wicker basket with a fabric tag."""
    ic = gk.Icon("trendyolmilla concept D")
    body = poly([(14, 52), (114, 52), (102, 114), (26, 114)], 8)
    solid(ic, body, face=[(0, "#c99a5b"), (1, "#8b5a2b")], depth=5, side="#5b3a1a", layer="basket")
    handle = circ(64, 54, 34).difference(circ(64, 54, 27)).intersection(box(0, 0, 128, 55))
    solid(ic, handle, face=[(0, "#c99a5b"), (1, "#8b5a2b")], depth=4, side="#5b3a1a", layer="handle")
    tag = rr(34, 66, 94, 96, 3)
    solid(ic, tag, face=gradient(SLUG, tag), depth=2, side=PURPLE[4], layer="tag")
    put_mark(ic, SLUG, (38, 72, 90, 90), face="#ffffff")
    return ic


for f in (A, B, C, D):
    f().save(OUT / f"{f.__name__}.svg")
print("wrote", *(f.name for f in OUT.glob("*.svg")))
