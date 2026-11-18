"""Tests for the v1.1 additions (hygiene and behaviour only - not aesthetics).

Run from the skill root:  python3 -m unittest discover -s tests -v
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import gnome_kit as gk  # noqa: E402
from _common import render_svg, hex_to_oklab  # noqa: E402


def run(script, *args, check=True, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, check=check, cwd=cwd)


def svg_doc(body, extra_defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
            f"<title>t</title><defs>{extra_defs}</defs>{body}</svg>")


class TestKitV11(unittest.TestCase):
    def test_glyphs_paint_all_sides_first(self):
        ic = gk.Icon("t")
        ic.glyphs({"a": gk.rrect_d(20, 20, 20, 20, 3), "b": gk.rrect_d(50, 20, 20, 20, 3)})
        ids = re.findall(r'id="(mark-[ab]-(?:lift|face))"', ic.svg())
        self.assertEqual(ids, ["mark-a-lift", "mark-b-lift", "mark-a-face", "mark-b-face"])

    def test_pieces_paint_all_chins_first(self):
        ic = gk.Icon("t")
        ic.pieces([gk.rrect_d(20, 20, 20, 20, 3), gk.rrect_d(50, 20, 20, 20, 3)], face="#33d17a")
        ids = re.findall(r'id="(mark-p\d-(?:chin|face))"', ic.svg())
        self.assertEqual(ids, ["mark-p0-chin", "mark-p1-chin", "mark-p0-face", "mark-p1-face"])

    def test_glyph_fill_rule(self):
        ic = gk.Icon("t")
        ic.glyph(gk.circle_d(64, 64, 20) + gk.circle_d(64, 64, 8), fill_rule="evenodd")
        self.assertEqual(ic.svg().count('fill-rule="evenodd"'), 2)

    def test_chin_colors_dark_and_light_faces(self):
        dark = gk.chin_colors("#3d3846")
        self.assertGreater(hex_to_oklab(dark["highlight"])[0], hex_to_oklab("#3d3846")[0])  # lighter corners
        self.assertLess(abs(hex_to_oklab(dark["base"])[0] - hex_to_oklab("#3d3846")[0]), 0.08)
        light = gk.chin_colors("#f6f5f4")
        self.assertLess(hex_to_oklab(light["base"])[0], 0.92)
        self.assertGreater(hex_to_oklab(light["base"])[0], 0.80)

    def test_fit_parts_keeps_aspect(self):
        parts = {"a": gk.rrect_d(0, 0, 40, 20, 2)}
        out = gk.fit_parts(parts, box=(14, 14, 114, 114))
        x0, y0, x1, y1 = gk.bbox_d(out["a"])
        self.assertAlmostEqual(x1 - x0, 100, delta=0.5)
        self.assertAlmostEqual(y1 - y0, 50, delta=0.5)
        self.assertAlmostEqual((y0 + y1) / 2, 64, delta=0.5)

    def test_translate_compact_arc_fallback(self):
        d = "M10 10a5 5 0 011 1h10z"     # compact arc flags "011"
        t = gk.translate_d(d, 0, 4)
        b0, b1 = gk.bbox_d(d), gk.bbox_d(t)
        self.assertAlmostEqual(b1[1] - b0[1], 4, delta=0.01)

    def test_load_parts(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.svg"
            p.write_text(svg_doc('<path id="one" d="M0 0H10V10Z"/><path d="M20 20H30V30Z"/>'))
            parts = gk.load_parts(p)
            self.assertEqual(list(parts), ["one", "p1"])


class TestFlatten(unittest.TestCase):
    def test_flatten_transforms_strokes_gradients_masks(self):
        import flatten_svg
        body = ('<mask id="m"><rect width="128" height="128" fill="#fff"/></mask>'
                '<g transform="translate(10 20)"><rect x="0" y="0" width="40" height="30" fill="url(#g)"/></g>'
                '<path d="M70 70L110 110" stroke="#e01b24" stroke-width="6" fill="none"/>'
                '<g style="display:none"><circle cx="64" cy="64" r="60" fill="#000"/></g>')
        defs = '<linearGradient id="g"><stop offset="0" stop-color="#3584e4"/><stop offset="1" stop-color="rgb(100%,0%,0%)"/></linearGradient>'
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "in.svg"
            p.write_text(svg_doc(body, defs))
            svg, warns = flatten_svg.flatten(str(p))
        self.assertEqual(svg.count("<path"), 2, svg)              # rect + outlined stroke; mask + hidden removed
        self.assertIn('data-gradient="#3584e4 #ff0000"', svg)
        self.assertIn('fill="#e01b24"', svg)
        out = Path(tempfile.mkdtemp()) / "o.svg"
        out.write_text(svg)
        x0, y0, x1, y1 = gk.bbox_d(re.findall(r'\sd="([^"]+)"', svg)[0])
        self.assertAlmostEqual(x0, 10, delta=0.2)                  # native placement kept for 128 viewBox
        self.assertAlmostEqual(y1, 50, delta=0.2)
        self.assertTrue(any("stroke converted" in w for w in warns))


class TestAutodraft(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        # flat "source": coral rounded tile, white ring with a coral cut-out (hole)
        (self.tmp / "source-geometry.svg").write_text(svg_doc(
            f'<path id="tile" fill="#ff6b57" d="{gk.rrect_d(4, 4, 120, 120, 28)}"/>'
            f'<path id="ring" fill="#ffffff" d="{gk.circle_d(64, 64, 34)}"/>'
            f'<path id="hole" fill="#ff6b57" d="{gk.circle_d(64, 64, 14)}"/>'))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_source_split_and_drafts(self):
        import autodraft as ad
        src = ad.Source(self.tmp)
        self.assertIsNotNone(src.ground)
        self.assertEqual(src.ground_color, "#ff6b57")
        self.assertEqual(src.ground_shape, "square")
        self.assertEqual(src.brand_color(), "#ff6b57")
        files = []
        for name, fn in ad.DRAFTS.items():
            p = self.tmp / f"d-{name}.svg"
            fn(src).save(p)
            files.append(p)
        r = run("lint_svg.py", *files, check=False)
        self.assertEqual(r.returncode, 0, r.stdout)
        # Free Symbol: the white ring becomes coral and the coral cut-out turns white (figure/ground kept)
        sym = (self.tmp / "d-symbol.svg").read_text()
        self.assertIn('fill="#ff6b57"', sym)
        self.assertIn('fill="#ffffff"', sym)

    def test_cutouts_become_holes(self):
        import autodraft as ad
        placed = {"ring": (gk.circle_d(64, 64, 34), "#c88a3a", None), "hole": (gk.circle_d(64, 64, 14), "#bfeee6", None)}
        out = ad._cutouts_to_holes(placed, "#bfeee6")
        self.assertEqual(list(out), ["ring"])
        self.assertEqual(out["ring"][2], "evenodd")


class TestTraceV11(unittest.TestCase):
    def test_monochrome_one_layer_and_small_details(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            im = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            from PIL import ImageDraw
            d = ImageDraw.Draw(im)
            d.ellipse([40, 40, 472, 472], fill=(255, 255, 255, 255))
            im.save(t / "mono.png")
            r = run("trace_source.py", t / "mono.png", "--out", t / "m.svg")
            self.assertIn("colours: #ffffff", r.stdout)
            im2 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            d = ImageDraw.Draw(im2)
            d.ellipse([40, 40, 472, 472], fill=(208, 140, 60, 255))
            d.ellipse([190, 230, 214, 262], fill=(36, 31, 49, 255))   # small dark "eyes"
            d.ellipse([298, 230, 322, 262], fill=(36, 31, 49, 255))
            im2.save(t / "eyes.png")
            r = run("trace_source.py", t / "eyes.png", "--out", t / "e.svg")
            self.assertIn("#24", r.stdout.lower(), r.stdout)            # the dark detail got its own layer


class TestTraceDetailsGradients(unittest.TestCase):
    """v1.1 tracer: lost-detail pass, gradient bands merged, report JSON."""

    def _png(self, body, defs, path, size=512):
        svg = Path(str(path) + ".svg")
        svg.write_text(svg_doc(body, defs))
        render_svg(svg, size).save(path)

    def test_gradient_bands_become_one_part(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            defs = ('<linearGradient id="l" x1="0" y1="8" x2="0" y2="120" gradientUnits="userSpaceOnUse">'
                    '<stop offset="0" stop-color="#62a0ea"/><stop offset="1" stop-color="#1a5fb4"/></linearGradient>')
            self._png(f'<path fill="url(#l)" d="{gk.circle_d(64, 64, 56)}"/>'
                      f'<path fill="#ffffff" d="{gk.rrect_d(44, 36, 40, 56, 20)}"/>', defs, t / "g.png")
            r = run("trace_source.py", t / "g.png", "--out", t / "g.svg", "--work-size", "512")
            svg = (t / "g.svg").read_text()
            self.assertEqual(svg.count("<path"), 2, r.stdout)          # one gradient disc + one white mark
            grads = re.findall(r'data-gradient="([^"]+)"', svg)
            self.assertEqual(len(grads), 1)
            self.assertGreaterEqual(len(grads[0].split()), 2)
            rep = json.loads((t / "g.json").read_text())
            self.assertEqual(len(rep["gradient_parts"]), 1)
            import autodraft as ad                                       # autodraft sees one gradient ground
            (t / "source-trace.svg").write_text(svg)
            src = ad.Source(t)
            self.assertEqual(src.ground_shape, "circle")
            self.assertTrue(src.ground_gradient)
            sym = ad.draft_symbol(src).svg()
            self.assertIn('fill="url(#', sym)                            # plateless mark carries the ramp

    def test_small_details_restored(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            seeds = "".join(f'<path fill="#fff4dc" d="{gk.ellipse_d(x, y, 2.0, 1.1)}"/>'
                            for x, y in [(44, 50), (64, 36), (84, 50), (40, 70), (88, 70)])
            self._png(f'<path fill="#d08c3c" d="{gk.circle_d(64, 64, 44)}"/>{seeds}', "", t / "s.png")
            run("trace_source.py", t / "s.png", "--out", t / "s0.svg", "--no-details")
            run("trace_source.py", t / "s.png", "--out", t / "s1.svg")
            base, det = (t / "s0.svg").read_text(), (t / "s1.svg").read_text()
            self.assertEqual(base.count("<path"), 1, base)               # too small for the normal trace
            self.assertGreaterEqual(det.count("<path"), 6)              # disc + 5 seeds
            rep = json.loads((t / "s1.json").read_text())
            self.assertGreaterEqual(rep["detail_pass"]["regions"], 5)

    def test_potrace_math_error_falls_back(self):
        import potrace
        import trace_source as ts
        orig = potrace.Bitmap.trace

        def flaky(self, *args, **kw):
            if kw.get("opticurve", True):
                raise ValueError("math domain error")     # what potracer's opti_penalty raises
            return orig(self, *args, **kw)
        m = np.zeros((64, 64), bool)
        m[16:48, 20:44] = True
        potrace.Bitmap.trace = flaky
        try:
            self.assertEqual(len(ts._potrace(m, 1.0)), 1)
        finally:
            potrace.Bitmap.trace = orig

    def test_extract_icon_on_white_jpeg(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            im = Image.new("RGB", (512, 512), (255, 255, 255))
            icon = render_svg(Path(gk.__file__).parent.parent / "examples/demo-original-apps/svg/marti-source.svg", 440)
            im.paste(icon, (36, 36), icon)
            im.save(t / "w.jpg", quality=80)
            run("extract_icon.py", t / "w.jpg", "--out", t / "o.png", "--report", t / "o.json")
            rep = json.loads((t / "o.json").read_text())
            self.assertEqual(rep["content_detection"], "component")    # not a viewer band
            self.assertTrue(rep["background"].startswith("removed"))
            self.assertAlmostEqual(rep["aspect"], 1.0, delta=0.03)
            a = np.asarray(Image.open(t / "o.png"))[..., 3]
            self.assertLess(a[4, 4], 10)                                 # corner is transparent
            self.assertGreater(a[256, 256], 245)


class TestLegibility(unittest.TestCase):
    def test_narrow_gap_detected_wide_gap_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            body_n = (f'<path fill="#3d3846" d="{gk.rrect_d(10, 20, 108, 80, 8)}"/>'
                      f'<path fill="#ffffff" d="{gk.rrect_d(20, 30, 40, 60, 2)}"/><path fill="#ffffff" d="{gk.rrect_d(62, 30, 40, 60, 2)}"/>')
            body_w = (f'<path fill="#3d3846" d="{gk.rrect_d(10, 20, 108, 80, 8)}"/>'
                      f'<path fill="#ffffff" d="{gk.rrect_d(20, 30, 36, 60, 2)}"/><path fill="#ffffff" d="{gk.rrect_d(72, 30, 36, 60, 2)}"/>')
            (t / "n.svg").write_text(svg_doc(body_n))
            (t / "w.svg").write_text(svg_doc(body_w))
            import legibility_check as lc
            rn, _, _ = lc.analyse(t / "n.svg", sizes=(32,))
            rw, _, _ = lc.analyse(t / "w.svg", sizes=(32,))
            self.assertGreaterEqual(rn["sizes"][32]["gap_regions"], 1)
            self.assertEqual(rw["sizes"][32]["gap_regions"], 0)

    def test_baseline_present(self):
        b = json.loads((ROOT / "assets/reference-library/legibility-baseline.json").read_text())
        self.assertEqual(b["n"], 98)
        self.assertTrue(0.6 < b["ssim32"]["median"] < 0.95)


class TestBoardsAndPack(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.svg = self.tmp / "i.svg"
        gk.skeleton("disc", "#3584e4").save(self.svg)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_launcher_preview(self):
        out = self.tmp / "l.png"
        run("launcher_preview.py", f"{self.svg}:Test", "--refs", "3", "--out", out)
        im = Image.open(out)
        self.assertGreater(im.width, 1000)

    def test_preview_explicit_refs_include_system_icons(self):
        import argparse
        import preview_sheet as ps
        a = argparse.Namespace(refs=None, ref_ids="folder,org.gnome.Nautilus", ref_kind=None, ref_shape=None, n_refs=6)
        refs = ps.pick_refs(a, {"circle"})
        self.assertEqual([Path(r).stem for r in refs], ["folder", "org.gnome.Nautilus"])

    def test_recolor_moves_key_hue_keeps_neutrals(self):
        out = self.tmp / "c"
        run("recolor.py", self.svg, "--out-dir", out, "--key", "#3584e4", "--families", "green,red")
        g = (out / "i-green.svg").read_text()
        self.assertNotIn("#3584e4", g)
        self.assertIn("#ffffff", g)        # white glyph untouched
        self.assertIn("#c0bfbc", g)        # neutral lift untouched

    def _project(self, appfilter_items, drawable_items, pngs):
        main = self.tmp / "proj/app/src/main"
        (main / "res/xml").mkdir(parents=True)
        (main / "res/drawable-nodpi").mkdir(parents=True)
        (main / "res/xml/appfilter.xml").write_text("<resources>\n" + appfilter_items + "</resources>\n")
        (main / "res/xml/drawable.xml").write_text('<resources>\n<category title="A" />\n' + drawable_items + "</resources>\n")
        for n in pngs:
            render_svg(self.svg, 256).save(main / f"res/drawable-nodpi/{n}.png")
        return self.tmp / "proj"

    def test_pack_audit_errors_and_clean(self):
        bad = self._project('<item component="ComponentInfo{a.b/.Main}" drawable="missing" />\n',
                            '<item drawable="ok" />\n', ["ok", "orphan"])
        r = run("pack_audit.py", "--project", bad, check=False)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("'missing' has no resource file", r.stdout)
        self.assertIn("relative activity", r.stdout)
        self.assertIn("orphan resource", r.stdout)
        shutil.rmtree(self.tmp / "proj")
        good = self._project('<item component="ComponentInfo{a.b/a.b.Main}" drawable="ok" />\n',
                             '<item drawable="ok" />\n', ["ok"])
        r = run("pack_audit.py", "--project", good, "--sheet", self.tmp / "s.png", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue((self.tmp / "s.png").exists())


class TestNewIconE2E(unittest.TestCase):
    def test_svg_input_to_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = ROOT / "examples/demo-original-apps/svg/marti-source.svg"
            run("new_icon.py", "--slug", "m", "--app", "M", "--input", src, "--alts", "faithful,disc,symbol,object",
                "--work", tmp)
            d = Path(tmp) / "m"
            for f in ("source-geometry.svg", "source.png", "identity.md", "brief.md", "build.py",
                      "m-faithful.svg", "m-disc.svg", "m-symbol.svg", "review.png", "legibility.png"):
                self.assertTrue((d / f).exists(), f)
            self.assertFalse((d / "m-object.svg").exists())   # metaphor needs a hand-made concept
            r = run("lint_svg.py", d / "m-faithful.svg", d / "m-disc.svg", d / "m-symbol.svg", check=False)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_doctor(self):
        r = run("doctor.py", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("READY", r.stdout)


class TestCandyBarRelative(unittest.TestCase):
    def test_relative_activity_expanded(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            main = tmp / "app/src/main"
            (main / "res/xml").mkdir(parents=True)
            (main / "res/xml/appfilter.xml").write_text("<resources>\n</resources>\n")
            (main / "res/xml/drawable.xml").write_text('<resources>\n<category title="A" />\n</resources>\n')
            svg = tmp / "i.svg"
            gk.skeleton("disc", "#3584e4").save(svg)
            run("candybar_add.py", "--project", tmp, "--name", "x_app", "--svg", svg, "--category", "A",
                "--component", "ComponentInfo{com.x/.ui.Main}")
            af = (main / "res/xml/appfilter.xml").read_text()
            self.assertIn("ComponentInfo{com.x/com.x.ui.Main}", af)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
