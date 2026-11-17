# PREREG: erdos-677-lcm-blocks, k = 29, run 2026-11-09-0917

Frozen at: 2026-11-09T09:19:35Z (date -u), before any attack program of this run was started.

## Criterion (verbatim, from target.md)

Success = a kernel-checked proof of `Erdos677.erdos_677` ("∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠
lcmInterval n k") or of its negation (a counterexample). Partial wins (workspace only, not prize solutions): an
exhaustive, uncapped verification of the statement for a stated range of (n, k) with a checkable certificate; a
machine-checked proof for a fixed small k.

## Planned claim
"For k = 29, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k, M(m,k) ≠ M(n,k)."
Made only if every step below holds for k = 29, computed in this run after this timestamp.

## The judge (as in run 2026-11-06-0918, with the exact margin also split over processes)
1. Small X: search677b 1100000 (any seed) COMPLETE with K ≥ 29 and 0 exact-equal candidates (verify_cands.py).
2. Ratio set: taskA_ratio_audit_k.py shows deep_cf.admissible_r(29) contains every Lemma-A ratio (0 missing).
3. Margin: c(1−10^−3) < X(ρX − Y) < c(1+10^−3) for all X ≥ 10^6 and every admissible r, by rig_margin_exact.py
   (bytes unchanged) run through shard_margin.py on 4 shards (shard I keeps positions j ≡ I mod 4 of
   admissible_r(29)): the shards' pair counts must add up to len(admissible_r(29)) (114817 as forecast on
   2026-11-07; a different length is recorded, not a stop, if steps 2 and 4 agree on it) with 0 failures and
   0 undecided; rig_margin.py (interval) on the whole list as a second check.
4. Enumeration: deep_rig.py (sha256 0e7d7d72…, bytes unchanged) with QEXP = 495, 1040 digits, η = 0.001, X0 = 10^6,
   run through shard_rig.py on 4 shards: the four admissible_r counts must add up to len(admissible_r(29)) and every
   shard must print a TOTAL line with product_solutions = 0.
5. Any reported triple is judged by checker/check677.py.
6. The three-skeptic panel cannot fit in this run (REPRODUCE needs about 2 h of full reruns): the claim, if any, is
   assembled in claim/ and stays PROMISING (single-context, unpanelled) until the next run panels it.

null_test: not needed because the claim is an exhaustive deterministic verification judged by exact arithmetic; no statistical or search-score claim is made.
