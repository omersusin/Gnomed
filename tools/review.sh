#!/bin/bash
# Checks + exports for one app:  tools/review.sh <slug>
# lint (must be 0 FAIL), PNG 512/256 export, 32 px legibility, review board.
set -u
s=$1; ROOT=$(cd "$(dirname "$0")/.." && pwd); S=$ROOT/tools/gnome-android-icons/scripts; cd "$ROOT/work"
F=$(ls $s/$s-{faithful,disc,rimmed,symbol}.svg 2>/dev/null)
[ -z "$F" ] && { echo "no SVGs for $s - build first"; exit 1; }
python3 $S/lint_svg.py $F
rm -rf $s/png; for f in $F; do python3 $S/export_png.py $f --out-dir $s/png >/dev/null || echo "EXPORT FAILED $f"; done
python3 $S/legibility_check.py $F --out $s/legibility.png | grep -E "svg$|32px"
python3 $S/preview_sheet.py $F --source $s/source.png --title "$s" --out $s/review.png >/dev/null && echo "board: work/$s/review.png"
python3 _lib/design_grid.py . $s/styles.png $s >/dev/null && echo "styles: work/$s/styles.png"
