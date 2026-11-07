# PREREG: erdos-677-lcm-blocks, run 2026-11-06-0918

Frozen at: 2026-11-06T09:21:22Z (date -u), before any attack program of this run was started.

## Criterion (verbatim, from target.md)

Success = a kernel-checked proof of `Erdos677.erdos_677` ("∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠
lcmInterval n k") or of its negation (a counterexample). Partial wins (workspace only, not prize solutions): an
exhaustive, uncapped verification of the statement for a stated range of (n, k) with a checkable certificate; a
machine-checked proof for a fixed small k.

## Planned claim
"For every k with 26 ≤ k ≤ 28, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k, M(m,k) ≠ M(n,k)."
Made only if every step below holds for all three k, computed in this run after this timestamp.

## The judge (as in run 2026-10-29-0821, with the enumeration split over processes)
1. Small X: search677b 1100000 (any seed) COMPLETE with K ≥ 28 and 0 exact-equal candidates (verify_cands.py).
2. Ratio set: the independent audit taskA_ratio_audit_k.py shows deep_cf.admissible_r(k) contains every Lemma-A ratio,
   for k = 26..28.
3. Margin: c(1−10^−3) < X(ρX − Y) < c(1+10^−3) for all X ≥ 10^6 and every admissible r, by rig_margin_exact.py with 0
   failures and 0 undecided (run per k); rig_margin.py (interval) as a second check.
4. Enumeration: deep_rig.py (sha256 0e7d7d72…, equal to outbox/2026-10-24-adb991-201bcc74/object/deep_rig.py, bytes
   unchanged) with QEXP = 495, 1040 digits, η = 0.001, X0 = 10^6, run through shard_rig.py on 4 shards (shard I keeps
   the ratios at positions j ≡ I mod 4 of admissible_r(k)): for each k = 26, 27, 28 the four shards' admissible_r
   counts must add up to len(admissible_r(k)) (21262, 16402, 21262 as recorded on 2026-10-29) and every shard must
   print a TOTAL line with product_solutions = 0.
5. Any reported triple is judged by checker/check677.py.
6. The three-skeptic panel (REPRODUCE about 4 h) cannot fit in this run: a claim, if any, is assembled in claim/ and
   stays PROMISING (single-context, unpanelled) until a later run panels it.

null_test: not needed because the claim is an exhaustive deterministic verification judged by exact arithmetic; no statistical or search-score claim is made.
