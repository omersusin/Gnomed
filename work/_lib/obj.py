"""Object-building helpers for Gnomed REDESIGNS (REDESIGN.md).

Everything comes from the vendored skill (tools/gnome-android-icons/scripts/obj.py:
solid, recess, hole, toplight, shapely shapes, geom_d); this file only adds the
repository part: save_styles() for work/<slug>/<slug>-<style>.svg.

    from obj import *
    ic = gk.Icon("App - Gnomed")
    solid(ic, rounded(box(20, 30, 108, 110), 10), face=[(0, "#62a0ea"), (1, "#1c71d8")], depth=6)
    save_styles("myapp", {"faithful": ic})
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_SK = ROOT / "tools/gnome-android-icons/scripts"
sys.path.insert(0, str(_SK))
_spec = importlib.util.spec_from_file_location("_skill_obj", _SK / "obj.py")
_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_skill)
globals().update({k: getattr(_skill, k) for k in _skill.__all__})

__all__ = list(_skill.__all__) + ["save_styles", "ROOT"]


def save_styles(slug, icons):
    """Write work/<slug>/<slug>-<style>.svg for the given styles.  A style NOT given is
    overwritten with the primary ONLY if an old (pre-redesign) SVG of it exists, so no
    old logo-on-plate version survives in the pack after tools/pack_refresh.py."""
    w = ROOT / "work" / slug
    primary = icons.get("faithful") or next(iter(icons.values()))
    for st in ("faithful", "disc", "rimmed", "symbol"):
        out = w / f"{slug}-{st}.svg"
        if st in icons:
            icons[st].save(out)
        elif out.exists():
            primary.save(out)
        else:
            continue
        print("wrote", out.relative_to(ROOT))
