# PREREG (frozen 2026-10-14T19:21:28Z, before any attack output of this run)

Criterion: as in target.md (verbatim from the bank). Aim: partial win p3 ("An exhaustive verification for all n <= 10^9
and all valid pairs (i,j), beyond Cong's n <= 10^7 and the targeted ~1.34e8 checks, reproduced by an independent
implementation (e.g. Lucas-theorem bitsets versus direct gcd factorisation on a random sample of n plus full Kummer scan)").
Judge for (A), any candidate: checker/check699.py n i j must print COUNTEREXAMPLE.

Lens scanner (full scan): seg699.c = the algorithm of runs/2026-10-14-1615/attempts/replicator/code/indep699.c with the
smallest-prime-factor table replaced by a segmented factor sieve (memory). Used only after it (1) matches brute699 for
every n <= 3000 in both modes (0 failures non-strict; identical strict lists n <= 1500), (2) finds the strict-mode
positive controls (2048;2,713), (2188;3,1094), (1594324;3,797162), (3) reproduces indep699's case count on chunk
[10^7, 10^7+10^6-1]. Coverage counts only finished chunks (.part renamed to .txt) with candidates=0 and overflow=0,
contiguous, from n = 4 to n = 10^9.

Lens sampler (independent implementation on a random sample): fast699.c (runs 1142/1452/1615, different algorithm and
code) on 300 windows of 2,000 consecutive n, window starts drawn by python3 random.Random(699).randrange(100000,
999998000) (300 draws), plus the already finished fast699 chunks [4,10^5] and [10^7, 7.7*10^7). Pass: for every window
fast699's nontrivial_i equals seg699's case count on the same window, and both report 0 candidates.

Lens contrarian (third implementation, Python, written separately): 200 random n in [10^8, 10^9]
(random.Random(6990).randrange), for each the per-n count of non-trivial (n,i) and the candidate count, compared with
seg699 run on [n, n]. Pass: all equal, all 0 candidates.

p3 is claimed (partial_win_claim) only if the full scan reaches 10^9 and both cross-checks pass with zero disagreements;
any disagreement stops the claim until explained. Then the three-skeptic panel (fresh subagents) and the gate.

null_test: not needed because the claim is an exhaustive interval checked by deterministic exact programs (no
statistical or chance comparison); the random sample is a cross-implementation check, not a statistic.
