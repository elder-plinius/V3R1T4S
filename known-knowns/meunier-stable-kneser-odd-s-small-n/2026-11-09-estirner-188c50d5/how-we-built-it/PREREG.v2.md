# PREREG v2: meunier-stable-kneser-odd-s-small-n (run 2026-11-09-1305)

Written at 2026-11-09T13:10:24Z (date -u). Reason for a v2: with the v1 encoding the five instances are UNSAT and every DRAT proof
verifies (attempts/sat-drat/out_run_all.txt), but the n = 21 proof is 308 MB, too large to ship in a package
(kit limit 1 MB per file). Only the symmetry-breaking clique changes; the criterion, the judge, the thresholds and
every other part of the CNF stay exactly as in PREREG.md.

## Changed: the clique whose colours are fixed

Still the only kind of symmetry breaking the criterion allows (fixed colours on a clique of pairwise disjoint
s-stable sets), but the largest such clique of the form below:
- t = floor(n/3); Q_j = {j, j+t, j+2t} for j = 1..m with m = min(t, C); unit clause x(Q_j, j-1).
- For (k,s) = (3,5): n = 17 gives t = 5 (gaps 5, 5, 7), n = 18 gives 6 (6, 6, 6), n = 19, 20 give 6 (6, 6, 7 and
  6, 6, 8), n = 21 gives 7 (7, 7, 7): every Q_j is 5-stable and the Q_j are pairwise disjoint.
- For the calibration (3,3): t = 3, 3, 3, 4, 4, 4 for n = 9..14, every Q_j 3-stable; m = min(t, C).
The generator asserts both properties before writing the CNF.

The v1 results stay in the run as evidence of the same verdicts under the smaller clique.
