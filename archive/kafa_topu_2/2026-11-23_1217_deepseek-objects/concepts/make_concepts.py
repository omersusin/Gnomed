"""kafa_topu_2 - NEW concepts for the redo (the old ones are in concepts-round3/).
Draw FOUR different ideas A-D; compose work/_lib/objects.py; see docs/PLAYBOOK.md#draw-concepts."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
from objects import *  # noqa: F401,F403,E402
OUT = Path(__file__).resolve().parent


def A():
    ic = gk.Icon("A")
    # ... compose objects here ...
    return ic


if __name__ == "__main__":
    for name, fn in (("A", A),):   # add B, C, D
        fn().save(OUT / f"{name}.svg")
        print("wrote", name)
