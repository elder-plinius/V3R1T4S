# PREREG (written 2026-11-03T22:44:50Z, before any attack output of this run)
criterion: as in target.md, verbatim (bank success_criterion and partial wins p1, p2). This run aims at the n = 21 and 22 part of p2.
statistic / checker: for each order n, a certificate file with one line per tree "n;edges;labels[;...]". It passes iff
checker/verify_sem_coverage.py (copied unchanged from run 2026-11-03-0818) reports: every line is a tree on n vertices, its
labeling passes check_sem.check, AHU centre-rooted canonical codes are pairwise distinct, and their number equals A000055(n)
from the OEIS b-file (A000055(21) = 2144505, A000055(22) = 5623756).
Thresholds: an order counts only on PASS with zero unlabeled lines. p2 needs PASS for every n in 18..22 (18..20 from run 2026-11-03-0818).
Trees are produced by nauty 2.8.9 gentreeg with res/mod splitting on the worker; coverage does not trust gentreeg, because the
checker counts distinct canonical codes against A000055.
A tree that the capped searches leave unlabeled is NOT a counterexample; it is reported prominently as "residue within cap"
and only a separate exhaustive method (exact search to completion, plus an independent one such as SAT/UNSAT proof) could make it one.
Pipeline per chunk (fixed now): alpha_sem (cap 300, 200 attempts) -> sem_direct on NOALPHA (cap 300, 100000 attempts) ->
ELNR caterpillar construction on the rest -> sem_direct deep (cap 2000, 10^7 attempts, 900 s per chunk) -> residue.
Every output labeling is checked with check_sem.check before it enters a certificate.
Smoke test (calibration, not a claim): n = 18 must reproduce 123867 labelled trees and verify_sem_coverage PASS.
null_test: not needed because each claim is an explicit object (a labeling per tree) checked by a deterministic checker against the definition, with coverage checked against A000055.
Self-limit: the panel needs fresh contexts; any claim from this run stays PROMISING until a three-skeptic panel passes it.
