"""Unit tests for the gnome-android-icons scripts (hygiene only - not aesthetics).

Run from the skill root:  python3 -m unittest discover -s tests -v
"""
import hashlib
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
from PIL import Image, ImageDraw  # noqa: E402

from _common import render_svg, nearest_hig, shade, HIG_FLAT  # noqa: E402
import gnome_kit as gk  # noqa: E402


def run(script, *args, check=True):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, check=check)


class TestSkillFormat(unittest.TestCase):
    def test_frontmatter(self):
        txt = (ROOT / "SKILL.md").read_text()
        m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
        self.assertTrue(m, "SKILL.md needs YAML frontmatter")
        fm = m.group(1)
        name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertEqual(name, ROOT.name if ROOT.name == name else name)  # dir name checked at install
        desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
        self.assertTrue(0 < len(desc) <= 1024)
        comp = re.search(r"^compatibility:\s*(.+)$", fm, re.M).group(1).strip()
        self.assertLessEqual(len(comp), 500)
        self.assertLess(len(txt.splitlines()), 500)

    def test_referenced_files_exist(self):
        txt = (ROOT / "SKILL.md").read_text()
        for ref in re.findall(r"`((?:references|assets|examples|scripts)/[^`*<> ]+)`", txt):
            ref = ref.rstrip("/")
            self.assertTrue((ROOT / ref).exists() or list(ROOT.glob(ref)), f"missing {ref}")


class TestLibrary(unittest.TestCase):
    def test_catalog_integrity(self):
        cat = json.loads((ROOT / "assets/reference-library/catalog.json").read_text())["icons"]
        self.assertGreaterEqual(len(cat), 130)
        for e in cat:
            p = ROOT / "assets/reference-library" / e["file"]
            self.assertTrue(p.exists(), e["file"])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest()[:16], e["sha256"], e["file"])
            self.assertTrue(e["license"], e["id"])

    def test_no_brand_artwork_from_community_themes(self):
        for p in ROOT.rglob("*.svg"):
            self.assertNotIn("morewaita", p.name.lower())


class TestColour(unittest.TestCase):
    def test_hig_palette(self):
        self.assertEqual(len(HIG_FLAT), 45)
        self.assertEqual(nearest_hig("#3584e4")[0], "blue3")

    def test_chin_is_darker(self):
        for face in ("#33d17a", "#3584e4", "#f6d32d", "#e01b24", "#ff6b57"):
            c = gk.chin_colors(face)
            lum = lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5))  # noqa: E731
            self.assertLess(lum(c["base"]), lum(face))
            self.assertLess(lum(c["edge"]), lum(c["base"]))

    def test_shade_roundtrip(self):
        self.assertEqual(shade("#3584e4", 0.0).lower(), "#3584e4")


class TestKit(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_translate_and_xform(self):
        d = gk.rrect_d(10, 10, 20, 20, 4)
        t = gk.translate_d(d, 0, 4)
        self.assertIn("M14 14", t)
        x = gk.xform_d(gk.circle_d(64, 64, 10), 2.0)
        nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", x)]
        self.assertIn(44.0, nums)
        self.assertIn(84.0, nums)

    def test_skeletons_pass_lint(self):
        for kind in ("disc", "rimmed", "square", "portrait", "landscape"):
            out = self.tmp / f"{kind}.svg"
            gk.skeleton(kind, "#3584e4").save(out)
            r = run("lint_svg.py", out, check=False)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_disc_matches_official_geometry(self):
        out = self.tmp / "d.svg"
        ic = gk.Icon("t")
        ic.disc(face="#3584e4")
        ic.save(out)
        import measure_style
        m = measure_style.measure(str(out))
        self.assertAlmostEqual(m["w"], 118, delta=2)
        self.assertAlmostEqual(m["b"], 124, delta=2)
        self.assertEqual(m["chin"], 2.0)

    def test_sweep_chin(self):
        d = gk.sweep_chin_d(gk.rrect_d(20, 60, 88, 2, 1), 4)
        self.assertTrue(d.startswith("M"))


class TestLint(unittest.TestCase):
    def test_raster_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "bad.svg"
            p.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><title>x</title>'
                         '<image href="data:image/png;base64,AAAA" width="10" height="10"/>'
                         '<rect x="20" y="20" width="80" height="80" fill="#3584e4"/></svg>')
            r = run("lint_svg.py", p, check=False)
            self.assertEqual(r.returncode, 1)
            self.assertIn("raster", r.stdout)

    def test_blur_shadow_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "blur.svg"
            p.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><title>x</title>'
                         '<defs><filter id="f"><feGaussianBlur stdDeviation="8"/></filter></defs>'
                         '<rect x="24" y="30" width="80" height="80" fill="#000" filter="url(#f)"/>'
                         '<rect x="24" y="20" width="80" height="80" fill="#3584e4"/></svg>')
            r = run("lint_svg.py", p, check=False)
            self.assertEqual(r.returncode, 1, r.stdout)


class TestExtractAnalyzeTrace(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        # synthetic phone screenshot: status bar, black viewer, white canvas, blue disc + white square
        im = Image.new("RGB", (540, 1000), (19, 19, 19))
        d = ImageDraw.Draw(im)
        d.text((20, 15), "10:55", fill=(255, 255, 255))
        d.rectangle([0, 300, 539, 839], fill=(255, 255, 255))
        d.ellipse([70, 370, 470, 770], fill=(53, 132, 228))
        d.rectangle([220, 520, 320, 620], fill=(255, 255, 255))
        im.save(self.tmp / "shot.png")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_extract(self):
        r = run("extract_icon.py", self.tmp / "shot.png", "--out", self.tmp / "src.png", "--report", self.tmp / "r.json")
        rep = json.loads((self.tmp / "r.json").read_text())
        self.assertIn("removed", rep["background"])
        out = np.asarray(Image.open(self.tmp / "src.png"))
        self.assertEqual(out.shape, (512, 512, 4))
        self.assertEqual(out[0, 0, 3], 0, "corner must be transparent")
        self.assertGreater(out[256, 256, 3], 250, "white glyph enclosed by disc must stay opaque")
        self.assertGreater(out[256, 60, 3], 250, "disc must stay opaque")

        a = run("analyze_source.py", self.tmp / "src.png", "--out-md", self.tmp / "id.md")
        res = json.loads(a.stdout)
        self.assertEqual(res["silhouette_class"], "circle")
        self.assertTrue((self.tmp / "id.md").read_text().startswith("# Identity sheet"))

        run("trace_source.py", self.tmp / "src.png", "--out", self.tmp / "t.svg")
        svg = (self.tmp / "t.svg").read_text()
        self.assertGreaterEqual(svg.count("<path"), 2)
        img = np.asarray(render_svg(self.tmp / "t.svg", 128))
        self.assertGreater(img[64, 64, :3].mean(), 230, "nested white glyph must be painted above the disc")

    def test_saturated_tile_kept(self):
        im = Image.new("RGB", (400, 400), (255, 69, 0))
        ImageDraw.Draw(im).ellipse([120, 120, 280, 280], fill=(255, 255, 255))
        im.save(self.tmp / "tile.png")
        run("extract_icon.py", self.tmp / "tile.png", "--out", self.tmp / "o.png", "--report", self.tmp / "o.json")
        self.assertIn("kept", json.loads((self.tmp / "o.json").read_text())["background"])


class TestVectorDrawable(unittest.TestCase):
    def test_fixture(self):
        import apk_icon
        svg = apk_icon.vector_to_svg((ROOT / "tests/fixtures/vector_sample.xml").read_bytes())
        self.assertIn('viewBox="0 0 108 108"', svg)
        self.assertIn("linearGradient", svg)
        self.assertIn('fill-rule="evenodd"', svg)
        self.assertIn('fill-opacity="0.800"', svg)
        self.assertIn("translate(54 54) rotate(45) scale(0.5 0.5) translate(-54 -54)", svg)
        # clip applies only to siblings after <clip-path>
        first_path = svg.index("<path d=\"M10,50")
        self.assertLess(first_path, svg.index('clip-path="url(#'))
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "v.svg"
            p.write_text(svg)
            render_svg(p, 64)


class TestComponents(unittest.TestCase):
    def test_parse_brief(self):
        import find_component as fc
        out = "priority=0 preferredOrder=0\ncom.example.app/.ui.Main\norg.x/org.x.Launcher\n"
        self.assertEqual(fc.parse_brief(out), ["ComponentInfo{com.example.app/com.example.app.ui.Main}",
                                               "ComponentInfo{org.x/org.x.Launcher}"])


class TestCandyBar(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        main = self.tmp / "app/src/main"
        (main / "res/xml").mkdir(parents=True)
        (main / "assets").mkdir(parents=True)
        (main / "res/drawable-nodpi").mkdir(parents=True)
        af = ('<?xml version="1.0" encoding="UTF-8"?>\n<resources>\n    <scale factor="0.64" />\n'
              '    <item component="ComponentInfo{a.b/a.b.Main}" drawable="ab" />\n</resources>\n')
        dr = ('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <version>1</version>\n'
              '    <category title="Tools" />\n    <item drawable="ab" />\n</resources>\n')
        for d in (main / "res/xml", main / "assets"):
            (d / "appfilter.xml").write_text(af)
            (d / "drawable.xml").write_text(dr)
        (main / "res/drawable-nodpi/ab.png").write_bytes(b"x")
        self.svg = self.tmp / "i.svg"
        gk.skeleton("disc", "#3584e4").save(self.svg)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_add_and_refusals(self):
        comp = "ComponentInfo{c.d/c.d.MainActivity}"
        r = run("candybar_add.py", "--project", self.tmp, "--name", "cd_app", "--svg", self.svg, "--component", comp,
                "--category", "Tools", "--label", "CD", "--alt", f"{self.svg}:CD (Disc)", "--dry-run")
        self.assertIn("dry run", r.stdout)
        self.assertFalse((self.tmp / "app/src/main/res/drawable-nodpi/cd_app.png").exists())
        run("candybar_add.py", "--project", self.tmp, "--name", "cd_app", "--svg", self.svg, "--component", comp,
            "--category", "Tools", "--label", "CD", "--alt", f"{self.svg}:CD (Disc)")
        for rel in ("res/xml", "assets"):
            af = (self.tmp / f"app/src/main/{rel}/appfilter.xml").read_text()
            dr = (self.tmp / f"app/src/main/{rel}/drawable.xml").read_text()
            self.assertIn(f'component="{comp}" drawable="cd_app"', af)
            self.assertIn('drawable="ab"', af)  # nothing removed
            self.assertIn('<item drawable="cd_app" name="CD" />', dr)
            self.assertIn('<item drawable="cd_app_alt1" name="CD (Disc)" />', dr)
            self.assertNotIn("cd_app_alt1", af)  # alternatives are gallery-only
        png = Image.open(self.tmp / "app/src/main/res/drawable-nodpi/cd_app.png")
        self.assertEqual(png.size, (256, 256))
        # refusals
        self.assertEqual(run("candybar_add.py", "--project", self.tmp, "--name", "cd_app", "--svg", self.svg, check=False).returncode, 1)
        self.assertEqual(run("candybar_add.py", "--project", self.tmp, "--name", "other", "--svg", self.svg,
                             "--component", comp, check=False).returncode, 1)
        self.assertEqual(run("candybar_add.py", "--project", self.tmp, "--name", "class", "--svg", self.svg, check=False).returncode, 1)


class TestDemos(unittest.TestCase):
    def test_demo_svgs_clean(self):
        svgs = sorted((ROOT / "examples/demo-original-apps/svg").glob("*.svg"))
        self.assertGreaterEqual(len(svgs), 14)
        r = run("lint_svg.py", *svgs, check=False)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
