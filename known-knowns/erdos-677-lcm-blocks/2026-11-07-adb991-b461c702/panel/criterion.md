# CRITERION skeptic: Erdős 677, 26 ≤ k ≤ 28, n ≤ 10^494

Read: CLAIM.md, REPRODUCE.md, object/PROOF.md, all of object/ (code and out/), checker/, source/. Nothing outside claim/.
Light checks of a few seconds each, run in panel_work/criterion/ (the claim folder was not modified; Python run with -I -B).

## 1. Which criterion is in play

- **Full success criterion** (kernel-checked proof of `Erdos677.erdos_677` or its negation): **not met**, and the claim
  does not say it is. Nothing is kernel-checked, and only k ∈ {26, 27, 28} with bounded n is covered.
- **Partial win 2** (machine-checked proof for a fixed small k): **not met**. There is no Lean proof, and n is capped.
- **Partial win 1** ("an exhaustive, uncapped verification of the statement for a stated range of (n, k) with a
  checkable certificate"): this is the one claimed. Judged below.

## 2. Is the claimed statement exactly a restriction of `Erdos677.erdos_677`?

checker/spec_677.lean: `∀ m n k : ℕ, k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k`, with
`lcmInterval n k = lcm of Ioc n (n+k) = lcm(n+1..n+k)`. The claim fixes k ∈ {26, 27, 28} (so k > 0), takes n ∈ [0, 10^494]
(n = 0 included) and leaves m universally quantified over m ≥ n + k. That is a literal restriction of the Lean statement
in (n, k) only. The quantifiers check out:

- **m is really uncapped.** No cap on m appears anywhere. Lemma A(b) *derives* m + k ≤ (n + k)·R(k)^{1/k} from equal lcms.
  The derivation is correct: (m+j)/(n+j) decreases in j, and f(m)/f(n) = r ≤ R(k). In the enumeration only q, which
  encodes X and hence n, is bounded by QMAX. p (that is, m) is whatever satisfies the window. The small-X search's
  m-range, `X = floor(N0·ρ)+2−k` in object/search677b.c, is exactly this derived bound plus slack.
- **Every n is covered, both parities, no gap at the seam.**
  - Step 2 covers every (n, k) with n + k ≤ 1.1·10^6, for every k ≤ 147. The log line for each of k = 26, 27, 28 is in
    object/out/search_N1.1e6.txt.
  - Step 5 keeps a candidate iff `2n + k + 1 ≥ 2·X0` (object/deep_rig.py), i.e. X ≥ 10^6 exactly. The margin of Step 4
    is proved for every real X ≥ 10^6.
  - X < 10^6 gives n + k < 10^6 + (k−1)/2 ≤ 10^6 + 13.5 < 1.1·10^6, so the two ranges overlap and nothing at the
    boundary falls between them.
  - Parity mapping: odd k (27) uses (p, q) = (Y, X) with n = q − (k+1)/2. Even k (26, 28) uses (2Y, 2X) with q = 2n + k + 1
    odd, and the code skips even q and even p, which is correct.
  - Upper end: q ≤ 10^495 corresponds to n ≤ 10^495 − 14 (odd k) and about 5·10^494 (even k). Both exceed 10^494, so
    the stated n-range is conservative, not stretched.
- **k = 26, 27, 28 all appear.** Each of the four shard outputs object/out/deep_rig_shard0..3.txt has per-k lines for 26,
  27 and 28, with product_solutions = 0, and ends with a TOTAL line.
  - The admissible_r counts per shard (5316+5316+5315+5315, 4101+4101+4100+4100, 5316+5316+5315+5315) add up to 21262,
    16402 and 21262. These match the independent audit (object/out/taskA_ratio_audit_k26-28.txt: missing 0, extra 0).
  - `admissible_r` returns a sorted list, so the j mod 4 shard split is deterministic and partitions the ratio set.
    object/shard_rig.py only swaps the iterated list. object/deep_rig.py hashes to 0e7d7d72…, matching CLAIM.md.
- **Lemma A** (PROVED-HERE): I checked each step. Steps 1–6 are correct, including the levels p^i = k and primes p ≥ k.
  A_k is a superset of what Lemma A allows, which is the safe direction. Lemma A uses only n < m, which is weaker than the
  Lean hypothesis m ≥ n + k.

## 3. Null models and small checks I ran

- Recompiled and reran object/search677b.c with `1100000 20261106` (4 s). The output is identical to
  object/out/search_N1.1e6.txt apart from timings: COMPLETE, K = 147, the same 2 candidates.
  - checker/check677.py returns FAIL (the lcms differ) for both near-misses, (n, m, k) = (4, 13, 3) and (18, 53, 4).
  - The audit's brute force finds 290 equal-lcm pairs with n < m ≤ 400 for k = 26..28. These are all overlapping
    blocks, a reminder that the m ≥ n + k quantifier matters. All of their ratios lie in the admissible sets.
- Ran deep_rig's own `validate` mode through shard_rig (SHARD=0/1500, 41 ratios across k = 26, 27, 28, q ≤ 4000). The
  convergent enumeration matched brute force in 41 of 41 cases. PROOF.md's validation (run 2026-10-15) was only for k ≤ 12,
  so this extends that spot check to the claimed k values.
- Independent mpmath spot check of the Step 4 margin (panel_work/criterion/margin_spot.py). For the extreme ratios of
  each k, X(ρX − Y(X))/c − 1 ≈ 5·10^−11 at X = 10^6 and ≈ 5·10^−79 at X = 10^40. That is far inside η = 10^−3, consistent
  with the reported worst relative margin 0.99999995.
- I did **not** rerun the ~2 h enumeration or the ~1.5 h exact-margin run (another skeptic is doing full reruns). My
  verdict on the criterion assumes those outputs reproduce.

## 4. Overstatements and gaps found (none changes the scope; all should be recorded)

1. **The Step 4 reduction is not in the claim folder.** PROOF.md says "This reduces to the positivity on [10^6, ∞) of two
   explicit polynomials". object/rig_margin_exact.py cites "NOTES.md, Task B" for that reduction, and NOTES.md is not in
   claim/. The reduction can be reconstructed from the code, but it is not written as PROVED-HERE.
2. **Dangling reference.** PROOF.md Step 5 item 5 cites "(CLAIM.md, patch note)". CLAIM.md has no patch note; the patch
   is described in a comment in object/deep_rig.py, which in turn cites NOTES.md.
3. **Parts of Step 5 are not interval arithmetic.**
   - The window bounds L and U, the s-intervals (computed in floats and widened by 2) and the 10^−6 float pre-filter are
     not interval arithmetic. CLAIM.md discloses this for L and U.
   - The margin headroom (relative deviation about 10^−11 against η = 10^−3) makes a rounding failure implausible.
   - Still, "COMPUTED, rigorous arithmetic" applies only to Step 4, not to Step 5. Step 5 is high-precision numerical
     with an argued-but-informal completeness bound: |r'| ≤ 2U + 1 (I re-derived it and it is correct), plus floating
     quadratic roots.
4. **Unshipped reference for the cross-check.** The cross-check against the "unsharded run of 2026-10-29" (k = 26, 27)
   relies on reference files that are not shipped in claim/. object/out/shard_sums.txt only reports "EQUAL".
5. **The certificate is checkable only by rerunning.** It is a proof document plus deterministic programs and count-level
   outputs. No candidate list is saved, so checking it means re-running for several CPU-hours. I accept this as
   "checkable" in the partial-win sense, since it is deterministic, documented and reproducible, but it is weaker than a
   compact, independently verifiable certificate.
6. **Labels are honest.** The status line ("single-context, unpanelled", "not kernel-checked", "computer-assisted") does
   not overstate. The title and the one-sentence claim match the evidence exactly. I found no "n ≤ 5871·k" range anywhere
   in claim/.

## 5. Subsumption

- The earlier confirmed claim cited in CLAIM.md covers k ≤ 25 only, so k ∈ {26, 27, 28} is new ground and is not covered by
  it.
- Any earlier k ≤ 28 result restricted to n ≤ 5871·k (which the panel brief mentions as possible; it is not in claim/)
  would be strictly contained in this claim, not the other way round.
- The problem page snapshot (source/erdosproblems_677.html, edited 30 September 2025) lists no solved marker and no
  computational range of this kind. Its 8 comments are not rendered in the snapshot. The novelty skeptic should rule on
  the literature.
- The win is incremental: the same method applied to three more values of k. It is still a genuine, non-subsumed
  instance of partial win 1.

## Verdict

The claim meets enumerated partial win 1, conditional on the full rerun reproducing the shard and margin outputs. It does
not meet the full success criterion or partial win 2. The (n, k) restriction is literal, m is truly uncapped, the
small-X/enumeration seam at X = 10^6 is covered on both sides for odd and even k, and every one of k = 26, 27, 28 is
present. The rigor caveats in section 4 (the reduction not in the folder, Step 5 being numerical rather than interval
arithmetic, a dangling reference) should be recorded with the claim. They do not widen or break the stated scope.

confirmed_scope: For every k ∈ {26, 27, 28}, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k (m uncapped), lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k), as established by a computer-assisted, not kernel-checked argument (Lemma A, an exhaustive search for n + k ≤ 1.1·10^6, a margin proved in exact rational interval arithmetic for X ≥ 10^6, and a high-precision but not interval-arithmetic continued-fraction enumeration up to q ≤ 10^495), which is enumerated partial win 1 and not a solution of Erdős Problem 677.
context: subagent (fresh context, Claude Code Agent tool)
pass: true
