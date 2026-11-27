# Run it yourself

## Verify the object (Python 3, standard library only)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected: one "ok" line per check and the last line `PASS`, as in verify-it-yourself/RECEIPTS.md (about a minute).
Without sh: `python -I -B verify-it-yourself/check_threshold.py object`.

## Recompute the roots and the fits with the code that produced them
how-we-built-it/ holds the code, the frozen rules (rules/PREREG.md to PREREG.v6.md), the run's outputs, and the
claim's REPRODUCE.md, written for a folder laid out like how-we-built-it/. Step 4 there reads Monte Carlo histograms
from timeline-aligner/mc/: how-we-built-it/timeline-aligner/mc/ holds the calibration datasets and the two smallest
sizes; the fitted sizes are in object/mc/. Both are packed in .tar.xz archives. Unpack them together first, from this
folder (each command checks every archive and file against its sha256 and ends with PASS):

    cp -R how-we-built-it work
    python verify-it-yourself/unpack_mc.py how-we-built-it/timeline-aligner/mc work/timeline-aligner
    python verify-it-yourself/unpack_mc.py object/mc work/timeline-aligner
    cd work

then follow REPRODUCE.md (needs numpy, scipy, mpmath and a C compiler). The #23 site roots n <= 10 take minutes;
n = 15 and 16 take about half an hour and one hour of compute with tmcrit_stream (under 1 GB of RAM, about 10 GB of
scratch disk). The panel's REPRODUCE skeptic recomputed n = 9..16 and got every root bit-identical.

## Rebuild the object
    python how-we-built-it/make_object.py <workspace root> <output folder>

make_object.py reads the run's saved outputs from the original workspace layout (runs/2026-10-17-2357 and
runs/2026-10-16-1714); it is included to show how object/threshold_23_site.json was assembled: every number in it is
parsed from those outputs, none typed by hand except the two table cells.
