# PREREG v4 (frozen 2026-11-02 15:41:23 UTC, before any order-21 or order-22 search ran)
Change from PREREG.v3.md: scope extended to n = 21 and n = 22 (full success criterion (a): every tree on 13..22 vertices),
using the small-data-direct lens's hybrid search (code/run_hybrid_order.sh: deterministic og_direct with node cap 1e5 per
attempt, then og_restart on the leftovers). The labeling checker, thresholds and null-test decision are unchanged
(null_test: not needed because every object is an explicit labeling judged by a deterministic checker).
Coverage check, stated before measuring: for each n, (1) every certificate line is a tree on n vertices whose labeling passes
checker/check_odd_graceful.py; (2) the AHU centre-rooted canonical codes of the certificate trees are pairwise distinct;
(3) their number equals A000055(n) from data/b000055.txt. (1)-(3) together imply every isomorphism class on n vertices is
covered exactly once, without trusting the enumerator that produced the trees. For n <= 18 the leaf-attachment
regeneration check of PREREG.v2 also runs. Note: the bank's verification method names nauty gentreeg for regeneration;
nauty is not installed on this machine (no installs outside a workspace venv), so the count-and-distinct argument stands in
for it and the report says so. A full (a) claim needs PASS for every n in 13..22 with 0 unlabeled trees.
Any claim stays at most PROMISING (single-context, unpanelled).
