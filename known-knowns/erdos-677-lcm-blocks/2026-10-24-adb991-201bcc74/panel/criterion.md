context: subagent (fresh context, Claude Code Agent tool)

# CRITERION skeptic: Erdős 677, claim "no counterexample with k ≤ 25, n ≤ 10^494"

Inputs read: only claim/ (CLAIM.md, REPRODUCE.md, object/PROOF.md, every program in object/, every output in
object/out/, checker/, source/). Scratch computations: panel_work/criterion/ (PIDs in pids.txt; nice -n 10, one core,
hard timeouts).

## 0. Which criterion is being tested

- **Full success criterion** (CLAIM.md, verbatim): "a kernel-checked proof of this statement or of its negation".
  - NOT met. The package contains no Lean proof of `Erdos677.erdos_677` and no counterexample.
  - The claim itself says "not kernel-checked".
- **Named partial win tested:** "an exhaustive, uncapped verification of the statement for a stated range of (n, k)
  with a checkable certificate".
  - The other partial win, "a machine-checked proof for a fixed small k", is not claimed. No Lean is present beyond
    the frozen spec files.

## 1. Statement match (stretched definitions)

- `lcmInterval n k := (Finset.Ioc n (n + k)).lcm id` over ℕ is lcm{n+1, …, n+k}. This is exactly M(n, k) in
  object/PROOF.md and `M()` in object/deep_cf.py, object/verify_cands.py and checker/check677.py.
- The quantifiers match: k > 0 (the claim covers 1 ≤ k ≤ 25), n ∈ ℕ including n = 0, and m ≥ n + k.
- The claim's range is a strict sub-case of the formal statement. No definition is stretched.

## 2. Hidden quantifiers

- **k = 1, 2.** Lemma A(a) applies: R(1) = R(2) = 1, so no ratio r with 1 < r ≤ R(k) exists.
  - This is also elementary: k = 1 is injective, and for k = 2, lcm(n+1, n+2) = (n+1)(n+2) is strictly increasing.
  - Covered with no computation.
- **Lemma A.** I re-derived it and it is correct.
  - Prime powers p^i ≥ k occur exactly once in each block (when i ≤ v_p(L)) or not at all.
  - Prime powers p^i < k contribute differences in {−1, 0, 1}, and 0 when p^i | k.
  - The bound r ≤ lcm(1..k)/k holds.
  - Because ρ = r^{1/k} is never rational for 1 < r ∈ A_k (|d_p| < k forces d_p = 0), the continued fractions
    are infinite and the enumeration is well defined.
- **Is m really uncapped? Yes, genuinely.**
  - For a given n and r, m is not a free variable: F(Y) = r·F(X) with F increasing on ((k−1)/2, ∞) fixes Y.
  - **Step 2 (C search).** It scans every m up to the Lemma A(b) bound m + k ≤ (n+k)·R(k)^{1/k}, plus a slack of
    2 that absorbs float error.
  - **Step 5.** It enumerates by q (= X or 2X) and puts no bound on p.
    - For each q, it keeps every p with 0 < qρ − p and q(qρ − p) < U.
    - So "q ≤ 10^495" bounds n only. Every m belonging to such an n is reached, because Y < ρX is forced by the
      margin.
- **Every n ≤ 10^494, both parities.**
  - Odd k: q = n + (k+1)/2.
  - Even k: q = 2n + k + 1, which is odd, and the code keeps only odd p and q.
  - In both cases q ≤ 2·10^494 + 26 < 10^495 = QMAX, and `check_add` keeps q ≤ QMAX inclusive.
  - The coverage actually exceeds n ≤ 10^494.
  - `enum_pairs` raises an error rather than truncating if the continued fraction is too short. It was not
    triggered.
- **n = 0.** It is covered by Step 2: the n-loop starts at 0.
- **Boundary m = n + k.**
  - search677b.c keeps m ≥ n + k. Its m-loop starts at a + k, and the block is still prime-free there.
  - deep_rig.py keeps every m > n.
  - Both include the boundary.
- **The X ≈ 10^6 split.**
  - Step 2 covers every n + k ≤ 1.1·10^6, every k ≤ 147, every m. This contains X = n + (k+1)/2 < 10^6 for k ≤ 25.
  - Step 5 keeps exactly X ≥ 10^6 (the test `2n+k+1 ≥ 2·X0`).
  - The margin (Step 4) is proved for all real X ≥ 10^6, including half-integer X for even k.
  - The two regions overlap, with no gap.
- **The Step 2 search, read in full.**
  - The additive hash Σ_{p ≥ k} v_p·h(p) is a function of the (≥ k)-prime part of f. That part is equal for any
    counterexample (proof of Lemma A, step 2), so collisions can only add candidates.
  - The table uses linear probing with no deletions and reports every key match.
  - Primes < k are removed incrementally and correctly.
  - The prime-free filter is justified by Lemma A(c).
  - I recompiled it and reran it with a different seed (777): the same 2 candidates came out, 0 exact-equal.

## 3. Is "exhaustive" literally true? The code paths that can drop a pair

- **Step 4 margin (object/rig_margin_exact.py): rigorous.**
  - CLAIM.md and PROOF.md defer the reduction's derivation to a NOTES.md that is not in the package. That is a
    checkability gap, so I reconstructed the reduction from the code.
  - With Z = ρX − C/X, the code builds the coefficients of rF(X) − F(Z) in powers X^{k−2t}.
  - The t = 0 term cancels exactly because ρ^k = r.
  - The leading term is ±η·s(ρ²−1)ρ^{k−2}.
  - The tail is bounded by Σ|a_t|·X0^{−2(t−1)} for X ≥ X0.
  - A domain check puts Z in the region where F is increasing.
  - It uses exact rational intervals for ρ, at 96 bits, with the enclosure verified by integer k-th powers.
  - This is correct, and it is proved for every r in the 63041-element ratio set: 0 failures, 0 undecided.
- **Ratio set.**
  - `admissible_r` matches the A_k definition.
  - object/taskA_ratio_audit.py regenerates it independently: missing 0, extra 0.
  - My own brute force (k ≤ 25, n < m ≤ 30000, panel_work/criterion/brute_30000.txt) found 0 disjoint equal-lcm
    pairs.
- **Step 5 float64 stage (object/deep_rig.py).** Three float decisions can discard a pair. None has a written error
  proof in the package beyond the patch note.
  - **(a) The s-interval from float roots and bounds, widened by 2.** My error analysis:
    - The absolute error is about ε·|B/A| ≲ ε·2(R+1)/Qn.
    - Catastrophic cancellation in the discriminant can only happen when A < 0. There the code's fallbacks give
      supersets: the whole range if the discriminant computes negative, and a gap of less than 4 between the roots
      that the widening covers.
    - When A > 0, the discriminant is ≥ r²·D0², so it cannot cancel.
    - I scanned the continued fractions of all 63041 ρ up to q ≤ 10^495 (pqscan.txt). The largest partial
      quotient is 3.6·10^8, at k = 23 and r = 2223/1360.
    - So the worst float error is about 10^−5, which is far below 2.
  - **(b) The 10^−6 relative pre-filter on g = q(qρ − p).**
    - The stated bound on u's relative error, ≤ 3.4·10^−16·(R+1)/Qn ≤ 10^−9, holds. Otherwise the exact integer q
      is used.
    - w = r·D1 + s·D0 has no cancellation, because r and s have opposite signs and so do D1 and D0.
    - I confirm the patch logic.
  - **(c) The bound |r| ≤ 2U + 1.** I re-derived it and it is correct.
  - **Independent cross-check.** I wrote a separate enumerator in scaled exact-integer arithmetic, with no floats
    and a wider r range of 3U + 6 (panel_work/criterion/indep_enum.py).
    - It ran on 123 sampled (k, r) for k = 3..25, QMAX = 10^495.
    - The sample covered, for every k, the 2 ratios with the largest partial quotients, 2 random ratios, and the
      smallest and largest r.
    - It found exactly the same full sets (2,229,236 pairs) and window sets (4458 pairs) as `enum_pairs`, with and
      without the pre-filter.
    - There were 0 mismatches.
- **Non-interval high precision.** ρ, d_i, L, U and the final window tests use 1090-digit mpmath, not interval
  arithmetic.
  - The resulting errors are about 10^−100 relative on q(qρ − p).
  - True solutions sit about 10^−3 relative inside (L, U): the proved margin is open, with worst relative lower
    bound 0.99999996.
  - This is a NON-RIGOROUS component, but the safety factor is enormous.
- **Final test.** f(m)·b == a·f(n) is checked in exact integers. All 1,174,616 window candidates fail it.
- **Earlier brute-force validation.** The "validated against brute force for q ≤ 4000, k ≤ 12 (run 2026-10-15)"
  output is not in the package. It is unverifiable from claim/, but superseded by my cross-check above.
- **Missing artifact.** NOTES.md (the margin reduction) is referenced but not shipped.

## 4. Checkable certificate and determinism

- Commands are given in REPRODUCE.md. The programs are deterministic, apart from the Step 2 hash seed, which is
  irrelevant to correctness.
- I reproduced Step 2 (seed 777, 4 s) and Step 5 for k = 3..14 at QEXP = 495. The per-k counts match
  object/out/deep_rig_final_k3-18_d1040.txt exactly.
- Note: running deep_rig.py without QEXP silently uses QMAX = 10^515. REPRODUCE.md sets QEXP correctly.
- k = 15..25 were not rerun by me. They take about 5 CPU-hours, and only the saved outputs attest them.
- The certificate is a program-plus-output certificate. A third party can check it in hours on 4 cores. It is not a
  proof object that a kernel checks.

## 5. Null model / consistency

- A null test does not apply to the verdict itself, since this is a deterministic search with an exact final test.
- A count-level null model is useful as a sanity check: equidistribution predicts about Σ_r 2η·c_r·ln(QMAX/10^6)
  window candidates per k.
- The observed per-k counts match that prediction to within Poisson noise for every k from 7 to 25. Examples:
  - k = 23: 314109 observed vs 313032 expected.
  - k = 25: 367031 observed vs 367244 expected.
- So no systematic loss of candidates larger than about 0.5% is plausible. Isolated drops are addressed by the
  exact cross-check in section 3.

## 6. Subsumption

- **Earlier workspace claim ("n ≤ 5871·k", every k).**
  - For k ≤ 25 it covers only n ≤ 146,775.
  - It does not subsume this claim, and this claim does not subsume it.
- **Literature.**
  - The problem page records only Thue–Siegel finiteness for each fixed k, and no range verification. Its forum
    has none either.
  - I know of no published result settling f(m) = r·f(n) for all ratios in A_k for every k ≤ 25, and none
    verifying Erdős 677 to n ≈ 10^494.
  - Individual small cases are classical. Equations such as (m+1)(m+2)(m+3) = 2(n+1)(n+2)(n+3) for k = 3 are
    elliptic curves and may be solved completely in the literature. Even so, they would cover only a few (k, r)
    and would not subsume the claim.
  - Confidence: moderate. No literature search was run.

## 7. Verdict reasoning

- Every hidden quantifier I hunted (m, n = 0, both parities, k ≤ 2, the boundary m = n + k, the X = 10^6 split) is
  covered.
- The definitions match formal-conjectures.
- The only non-rigorous parts are float64 and 1090-digit (non-interval) numerics. Their error margins are many
  orders of magnitude inside tolerance, as shown by my error analysis and by the independent exact enumerator on
  123 worst-case and random curves.
- The result is not subsumed by anything I know.
- Therefore it meets the named partial win, read literally: exhaustive and uncapped in m for the stated (n, k), with
  a reproducible certificate.
- Caveats that stay open:
  - It is computer-assisted and not kernel-checked.
  - The float stage of Step 5 has no written error proof in the package.
  - NOTES.md is missing.
  - k = 15..25 were not independently rerun.
- It does not meet the full success criterion.

confirmed_scope: For every 1 ≤ k ≤ 25, every 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m), lcm(m+1..m+k) ≠ lcm(n+1..n+k), as a computer-assisted, not kernel-checked result. It rests on a hand proof of Lemma A, an exact hash-plus-verification search for n + k ≤ 1.1·10^6, a margin proved in exact rational interval arithmetic for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 with exact final tests. That enumeration uses float64 pre-filters and 1090-digit non-interval arithmetic, whose correctness is supported by error analysis and an independent exact cross-check on 123 sampled curves but not formally proved.
pass: true
