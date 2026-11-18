"""v1.2: redesign-first workflow (obj.py, concepts.py, new_icon scaffold, examples)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import numpy as np  # noqa: E402
from _common import render_svg  # noqa: E402


def run(script, *args, check=True):
    return subprocess.run([sys.executable, str(script if Path(str(script)).is_absolute() else SCRIPTS / script),
                           *map(str, args)], capture_output=True, text=True, check=check)


class TestObj(unittest.TestCase):
    def test_parts_are_clean_vectors(self):
        from obj import gk, rounded, box, circ, solid, recess, hole, geom_d
        ic = gk.Icon("obj test")
        body = rounded(box(18, 22, 110, 106), 12)
        solid(ic, body, face=[(0, "#99c1f1"), (1, "#3584e4")], depth=8, layer="body")
        recess(ic, rounded(box(30, 34, 98, 80), 6), [(0, "#f6f5f4"), (1, "#deddda")])
        hole(ic, circ(64, 94, 6))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "o.svg"
            ic.save(p)
            r = run("lint_svg.py", p, check=False)
            self.assertNotIn("[FAIL]", r.stdout, r.stdout)
            a = np.asarray(render_svg(p, 128))[..., 3]
            ys = np.nonzero(a.max(1) > 127)[0]
            self.assertGreaterEqual(ys.max(), 106 + 6)           # the side shows under the face
        self.assertEqual(geom_d(box(0, 0, 1, 1).difference(box(0, 0, 1, 1))), "")

    def test_rounded_keeps_size(self):
        from obj import rounded, box
        g = rounded(box(10, 10, 110, 110), 12)
        x0, y0, x1, y1 = g.bounds
        self.assertAlmostEqual(x0, 10, delta=0.2)
        self.assertAlmostEqual(x1, 110, delta=0.2)
        self.assertLess(g.area, 100 * 100)                       # corners really rounded


class TestExamplesAndConcepts(unittest.TestCase):
    def test_examples_build_and_lint(self):
        ex = ROOT / "examples/redesign"
        run(ex / "build_examples.py")
        for n in ("bulut", "kasa"):
            for v in ("1-source", "2-plate", "3-redesign"):
                self.assertTrue((ex / f"{n}-{v}.svg").exists())
            r = run("lint_svg.py", ex / f"{n}-3-redesign.svg", check=False)
            self.assertNotIn("[FAIL]", r.stdout, r.stdout)
        self.assertTrue((ex / "target.png").exists())

    def test_concepts_board(self):
        ex = ROOT / "examples/redesign"
        with tempfile.TemporaryDirectory() as tmp:
            w = Path(tmp) / "kasa"
            (w / "concepts").mkdir(parents=True)
            render_svg(ex / "kasa-1-source.svg", 256).save(w / "source.png")
            for k, v in (("A", "2-plate"), ("B", "3-redesign")):
                (w / "concepts" / f"{k}.svg").write_text((ex / f"kasa-{v}.svg").read_text())
            r = run("concepts.py", w)
            self.assertIn("board:", r.stdout)
            self.assertTrue((w / "concepts.png").exists())
            r = run("concepts.py", Path(tmp) / "empty", check=False)
            self.assertNotEqual(r.returncode, 0)


class TestNewIconScaffold(unittest.TestCase):
    def test_scaffold_prepares_redesign(self):
        ex = ROOT / "examples/redesign"
        with tempfile.TemporaryDirectory() as tmp:
            run("new_icon.py", "--slug", "kasa", "--app", "Kasa", "--input", ex / "kasa-1-source.svg", "--work", tmp)
            d = Path(tmp) / "kasa"
            self.assertTrue((d / "concepts").is_dir())
            self.assertTrue((d / "redesign.py").exists())
            brief = (d / "brief.md").read_text()
            self.assertIn("\napproved:", brief)
            self.assertIn("NOT design candidates", brief)
            self.assertTrue((d / "kasa-faithful.svg").exists())     # one measuring draft by default
            self.assertFalse((d / "kasa-disc.svg").exists())
            r = run(d / "redesign.py", check=False)                   # placeholder refuses to ship
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("approved concept", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
