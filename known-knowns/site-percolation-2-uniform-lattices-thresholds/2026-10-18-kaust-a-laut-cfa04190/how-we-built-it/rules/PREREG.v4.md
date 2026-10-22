# PREREG.v4: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-16T17:59:19Z (date -u), before any new transfer-matrix root is computed with tmcrit_stream.exe (its regression test
re-ran small-n roots of #20-#23 that were already in the series files, and #15 site at n = 6) and before any bond series
goes beyond the n already listed in its series file. PREREG.md, PREREG.v2.md and PREREG.v3.md
stay in force unchanged; this file changes no threshold and no decision rule.

null_test: not needed because the claim is a measured constant checked against calibration lattices with exactly known or published high-precision thresholds (unchanged from PREREG.md)

## Evaluator

tmcrit_stream.exe (attempts/exact-polynomial/code/tmcrit_stream.c, generated from tmcrit.c by make_stream.py; only the
storage of the transfer structure differs: written to disk during the build, read back in the same order on every
sweep). test_stream.py: 15 of 15 cases (11 lattices, site and bond) print the same root, bracket and state counts as
tmcrit.exe, bit for bit (test_stream_output.txt). Either program may produce any n of any series.

## n_max for the decision (extends PREREG.v3 addition D to bond series)

Each series is extended as far as disk, memory (11 GB for all jobs) and time allow: #20-#23 bond to n = 13. At the
one look of a lattice (PREREG.v2), each of its series is extrapolated with every n then present in its series file.
Availability decides, not the value.
