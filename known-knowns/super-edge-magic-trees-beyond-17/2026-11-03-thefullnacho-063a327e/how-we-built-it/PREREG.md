# PREREG (written 2026-11-03T08:20:26Z, before any attack output)
criterion: as in target.md, verbatim (bank success_criterion and partial wins p1, p2).
statistic / checker: for each order n, a certificate file with one line per tree "n;edges;labels". It passes iff
checker/verify_sem_coverage.py reports: every line is a tree on n vertices, its labeling passes check_sem.check,
AHU centre-rooted canonical codes are pairwise distinct, and their number equals A000055(n) from the OEIS b-file.
Thresholds: an order counts only on PASS with zero unlabeled lines. p1 needs PASS for every n in 18..20; p2 for 18..22.
A tree that the capped searches leave unlabeled is NOT a counterexample; it is only reported as "unlabeled within cap".
null_test: not needed because each claim is an explicit object (a labeling per tree) checked by a deterministic checker against the definition, with coverage checked against A000055.
Self-limit: no fresh contexts on this harness, so any claim stays at most PROMISING (single-context, unpanelled).
