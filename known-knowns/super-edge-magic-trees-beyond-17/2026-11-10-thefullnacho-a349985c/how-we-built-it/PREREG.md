# PREREG (written 2026-11-04T11:35:52Z, before any attack output of this run)
criterion: as in target.md, verbatim (bank success_criterion (a); partial wins p1, p2 already claimed). This run aims at
n = 23, 24, 25, which with 18..22 (Zenodo 10.5281/zenodo.23935954) completes (a).
statistic / checker: for each order n, one certificate file, one line per tree "n;edges;labels[;...]". It passes iff BOTH
(1) checker/verify_sem_coverage.py (unchanged from run 2026-11-03-2244) reports every line a tree on n vertices with a
labeling passing check_sem.check, AHU canonical codes pairwise distinct, count = A000055(n) from the OEIS b-file, and
(2) checker/indep_check.py --regen reports lines = distinct = regenerated = A000055(n) by Otter's formula, missing 0,
extra 0, no bad tree or labeling. A000055(23) = 14828074, A000055(24) = 39299897, A000055(25) = 104636890.
Thresholds: an order counts only with both PASS and zero unlabeled lines; (a) needs every n in 18..25.
Pipeline per chunk (fixed now, unchanged): alpha_sem (cap 300, 200 attempts) -> sem_direct on NOALPHA (cap 300, 100000
attempts) -> ELNR caterpillar construction -> sem_direct deep (cap 2000, 10^7 attempts, 900 s per chunk) -> residue.
Chunks: M = 4096 (n = 23), 8192 (24), 16384 (25); 16 workers; nice 19, ionice idle, 500 MB virtual per chunk.
A tree the capped searches leave unlabeled is NOT a counterexample; it is reported as "residue within cap" and gets a
separate longer search; only two independent exhaustive methods could make it a counterexample (criterion (b)).
If a checker cannot fit n = 25 in memory, it may be run on a partition of the certificate (by canonical-key hash),
summing the per-part counts; the partition rule is fixed before that run and recorded here as an addendum.
Smoke test (calibration, not a claim): n = 18 from this account, 64 chunks: 123867 labelled, coverage PASS (done
2026-11-04 06:35 EST, output/n18_smoke.log).
null_test: not needed because each claim is an explicit object (a labeling per tree) checked by deterministic checkers against the definition, with coverage checked against A000055.
Self-limit: any claim from this run stays PROMISING until a three-skeptic panel passes it.

## Addendum 1 (written 2026-11-04T20:33:59Z, after n = 23 labelling, before any n = 24 or 25 output)
Observed at n = 23: the pipeline left 301 trees as residue within cap in three chunks (2383, 2389, 2400; the deep stage
hit its 900 s chunk timeout). All 301 are bushy small-diameter trees with several hubs. Fixed now, for every order:
1. Residue retry: residue trees get sem_direct with node cap 2000 and up to 10^9 attempts, in 16 parts, 3 h per part
   (n = 23: all 301 labelled within minutes). Every retry labeling must pass check_sem.check before it is used.
2. The order's certificate is the run's certificate plus the retry labelings (merged, one line per tree); both
   checkers (verify_sem_coverage.py and indep_check.py --regen) are run on the merged file, and the order counts only
   if both PASS on it. The run.sh coverage result on the unmerged file is kept as a record, not as the verdict.
3. For n = 24 and 25 the deep stage's per-chunk timeout is raised from 900 s to 3600 s (DEEP_SEC=3600); all other
   pipeline parameters and chunk counts (M = 8192, 16384) are unchanged.
4. A tree still unlabelled after step 1 is not a counterexample; it gets an exhaustive search and, only if that finds
   nothing, an independent second exhaustive method (criterion (b)), and goes to the human first.
5. (added 2026-11-04T20:44:31Z, before any n = 24 output) Worker count for n = 24 raised from 16 to 28 at the
   contributor's request (the contributor's own desktop; run.sh cap raised from 16 to 30). Operational only: every chunk is
   independent, so the worker count changes wall time, not which labelings are searched or how they are checked.
6. (added 2026-11-06T21:21:23Z, before any n = 25 output) n = 25 runs with the same settings as n = 24 (28 workers,
   DEEP_SEC=3600, M = 16384, residue retry as in item 1) from the worker folder on a second SSD (/data/v3-worker; files
   unchanged, copy verified). Operational only: the two checkers on the merged certificate run one after the other
   instead of side by side, because each needed 3.5 GB at n = 24 and about 10 GB is expected at n = 25.

## Addendum 2 (written 2026-11-10T11:53:50Z, during the n = 25 residue retry, before its results are final)
Observed at n = 25: the search left 23,458 trees as residue within cap (44 chunks hit the 3600 s deep stage), far more
than n = 24's 1,012. The step-1 retry (item 1: 16 parts, 3 h per part) cannot reach every tree in some parts before its
timeout, and a tree a part never reaches produces no output line. Fixed now, with the contributor's approval:
1. The n = 25 driver script was stopped; the 16 step-1 retry processes run on to their 3 h timeout unchanged.
2. Second pass: every residue tree without a labeling from step 1 (found by set difference against residue_all.txt,
   not by counting UNLABELED lines) gets sem_direct with the same parameters (cap 2000, up to 10^9 attempts) in 28
   parts with a 12 h timeout per part. Every labeling must pass check_sem.check before use.
3. Merge and check exactly as item 2 (both checkers on the merged certificate, run one after the other), but only if
   every residue tree has a labeling; otherwise stop and report the count to the contributor.
4. More search time can only find more labelings, each checked against the definition, so it cannot produce a false
   PASS. A tree still unlabelled after step 2 is not a counterexample (item 4 of addendum 1 applies).
