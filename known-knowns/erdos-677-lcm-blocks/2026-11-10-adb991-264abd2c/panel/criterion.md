# CRITERION skeptic: claim of run 2026-11-09-0917 (Erdős 677, k = 29, n ≤ 10^494)

Scope of reading: the claim folder only (CLAIM.md, REPRODUCE.md, PATCH_NOTE.md, deep_rig_patch.diff, object/ incl.
PROOF.md, all code and out/, checker/, source/). My scripts and outputs are in panel_work/criterion/.

## 1. Which criterion, and is the statement exactly a restriction of erdos_677?

- **Criterion in play:** the partial win "an exhaustive, uncapped verification of the statement for a stated range of
  (n, k) with a checkable certificate". It is NOT the success criterion (no kernel-checked proof of `erdos_677` or of
  its negation) and not the "machine-checked proof for fixed small k" partial win (nothing is kernel-checked). CLAIM.md
  says so itself ("A partial result, not a solution ... not kernel-checked"). Correct framing.
- **Statement:** "k = 29, all 0 ≤ n ≤ 10^494, all m ≥ n + k: M(m,k) ≠ M(n,k)". The checker specs define
  `lcmInterval n k = (Ioc n (n+k)).lcm id` = lcm(n+1..n+k) over ℕ, matching M(n,k). Restriction is in (n, k) only:
  m is quantified over all m ≥ n + k. OK.
- **m uncapped:** no cap is assumed. In step 2 the m-range comes from Lemma A(b) (m + k ≤ (n+k)R(k)^{1/k}, derived
  from f(m)/f(n) = r ≤ R(k) and monotonicity of (m+j)/(n+j)) plus 2 of slack; the search677b loop actually uses the
  coarser global bound m ≤ N0·ρ + 2 − k. In step 5, p (= Y) is not capped at all: only q(qρ − p) ∈ (0, U) is used, and
  Y is forced by the margin theorem for every real X ≥ X0. OK.
- **n = 0:** included: search677b's n-loop starts at n = 0 (initial window 1..k); my independent search also starts at 0.
- **Seam (odd k = 29):** X = n + 15. Step 2 covers n + 29 ≤ 1.1·10^6, i.e. n ≤ 1 099 971 (X ≤ 1 099 986). Step 5
  keeps exactly X ≥ X0 (code: skip iff 2n + k + 1 < 2·X0, i.e. X < 10^6), i.e. n ≥ 999 985. Overlap of ~10^5; no gap.
  The search output's k = 29 line has nmax = 1099971, cand = 0.
- **Upper end:** n ≤ 10^494 ⇒ q = X = n + 15 ≤ 10^494 + 15 ≤ 10^495 = QMAX (shard outputs print QMAX=10^495, so
  QEXP=495 was set). The claim is conservative: the enumeration actually reaches n ≤ 10^495 − 15.
- **Parity mapping, odd k:** (k+1)/2 = 15 is an integer, (p, q) = (Y, X) = (m+15, n+15), S = 1; deep_rig's odd branch
  maps back n = q − 15, m = p − 15 with no parity filter. Correct. (The even-k branch is irrelevant here.)
- **k > 0 hypothesis and k ≤ 2:** irrelevant for k = 29 (Lemma A(a) only matters for k ≤ 2).

## 2. Certificate: completeness and checkability

**PROOF.md read in full.** Lemma A (proof steps 1–6) checked: for p ≥ k each level p^i ≤ v_p(L) has exactly one
multiple in each block; levels above v_p(L) have none; levels p^i < k contribute d ∈ {−1,0,1}, 0 when p^i | k; the bound
r ≤ lcm(1..k)/k follows. Consequences (b) window and (c) prime-free m-block correct.

**Step 4 reduction, verified by hand.** With Y_C = ρX − C/X: X(ρX − Y) > C ⇔ Y < Y_C ⇔ F(Y) < F(Y_C) (F increasing on
((k−1)/2, ∞), both points there) ⇔ G_C(X) = rF(X) − F(Y_C(X)) < 0. Expanding e_j(ρX − C/X)^j: the term
e_j C(j,v)ρ^{j−v}(−C)^v X^{j−2v} has exponent k − 2t iff j = k − 2t + 2v, and then ρ^{j−v} = ρ^{k−2t}ρ^v, giving
a_t = r e_{k−2t} − ρ^{k−2t} Σ_v e_{k−2t+2v} C(k−2t+2v, v)(−Cρ)^v. t = 0 cancels (ρ^k = r); odd exponents never occur
(e_j = 0 for k − j odd). a_1 = r(−s) − ρ^{k−2}(−s − kD) = ρ^{k−2}(kCρ − s(ρ²−1)); with kcρ = s(ρ²−1) (c =
(k²−1)(ρ²−1)/(24ρ), s = k(k²−1)/24) this is ρ^{k−2}s(ρ²−1)(C/c − 1) = ±ρ^{k−2}s(ρ²−1)η. Correct. The tail bound
|Σ_{t≥2} a_t X^{−2(t−1)}| ≤ Σ|a_t| X0^{−2(t−1)} for X ≥ X0 is valid; the largest t is (k+j)/2 ≤ k, so t ∈ 1..k suffices.
The sign conditions (a_1(C₊) > T(C₊), −a_1(C₋) > T(C₋), domain Y_C(X0) > (k−1)/2) imply the two-sided margin for
all real X ≥ X0.

**rig_margin_exact.py implements exactly this test.** tab enumerates t = 1..k, v with 0 ≤ j0+2v ≤ k and v ≤ j
(C(j,v) ≠ 0); a = r·e_{k−2t} − ρ^{k−2t}·Σ e_j C(j,v)(−D)^v with D = (k²−1)/24·(1±η)(ρ²−1) = Cρ (an exact identity, so
using it is sound); lead = a_1, tail = Σ_{t≥2}|a_t|X0^{−2(t−1)}; PROVED iff dom and L.lo − tail.hi > 0 with L = ±a_1 for
C±. ρ is enclosed by [A/2^96, (A+1)/2^96] with the enclosure asserted from exact integers; all arithmetic on Fraction
endpoints. Sound.

**Sharding.** shard_margin.py and shard_rig.py only replace the module-level name `admissible_r` (which both programs
use via `from deep_cf import admissible_r`) by the j ≡ I (mod S) sublist of the same sorted list; program bytes are
unchanged (deep_rig.py sha256 0e7d7d72…ad0341 as stated). Counts: margin shards 28705 + 28704 + 28704 + 28704 = 114817;
enumeration shards admissible_r 28705 + 3×28704 = 114817, enumerated 833627 + 832852 + 833512 + 832536 = 3332527,
window 822606 + 821979 + 822638 + 821629 = 3288852 = shard_sums.txt. Wrap test (k = 5..12): 0/1 shard identical to
unsharded apart from times; 3 shards sum to 392 pairs (per k: 7, 4, 22, 13, 31, 37, 157, 121 all add up).

**Outputs say what CLAIM.md says.** rig_margin_k29: 114817 pairs, 0 failures, 0 undecided, worst 0.99999994 at
21736/21735. Exact shards: each failures=0 undecided=0, worst 0.99999994, 3217.8–3230.3 s. deep_rig shards: each
product_solutions=0, X0=1000000, QMAX=10^495. Ratio audit: |S_A| = |admissible_r| = 114817, missing 0, extra 0,
110 equal-lcm pairs (n < m ≤ 400) all with ratio in the set. Small-X: COMPLETE kmax=147, 2 candidates, 0 exact-equal;
k = 29 line cand = 0. Source hashes match the status table.

## 3. My own cheap checks (all single-threaded, all passed)

- search677b rebuilt and run for k = 29 only (N0 = 1.1·10^6, same seed): 193705 prime-free m-windows, cand = 0 —
  identical to the shipped k = 29 line.
- Independent small-X search in numpy (different random 64-bit prime weights, per-n Lemma-A window, n from 0):
  k = 29, n + 29 ≤ 1.1·10^6: 193705 prime-free m-blocks, 0 hash candidates (also 0 without the per-n window).
  Positive controls: without the window it finds (4,13) for k = 3 and (18,53) for k = 4.
- Independent count of the Lemma-A ratio set for k = 29 (levels 2:4, 3:3, 5:2, 7..23:1; R = 80313433200): 114817.
- deep_rig.enum_pairs vs an exact brute force (floor(qρ) by integer k-th roots) for 30 k = 29 ratios (smallest,
  largest, the four shard-worst ratios, random ones, and ratios with large early partial quotients up to 84838, which
  exercises the exact-u patch branch Qn < 1e-4), q ≤ 2·10^5, three windows each (wide 2c + 0.1 without pre-filter;
  c(1 ± 10^−3) with pre-filter; c(1 ± 1/2) with pre-filter): 0 mismatches (after discarding p ≤ 0 pairs, which the
  brute force excludes by construction and which can never map to n ≥ 0 with X ≥ X0).
- Margin at sample points (mpmath Newton solve of F(Y) = rF(X), up to 1100 digits) for 7 ratios at X = 10^6, 10^6+1,
  10^9, 10^30, 10^100, 10^494: X(ρX − Y)/c − 1 ≈ 5.6·10^−11 at X = 10^6, scaling like X^−2, and at most numerical
  noise beyond — far inside ±10^−3. This matches the reported worst relative margin (1 − 0.99999994 ≈ 5.7·10^−8 = 5.6·10^−11/η).
- Independent Laurent expansion of G_C(X) (direct polynomial arithmetic, not the tab formula) for 5 ratios: X^k and
  X^{k−1} coefficients vanish, no odd-parity coefficients, a_1 equals the closed form to relative 10^−112, T/|a_1| ≈
  5.7·10^−8, lowest exponent −29 (so t ≤ 29 = k).
- rig_margin_exact.check on 45 ratios (5 above + 40 random): all PROVED, rel 0.99999994…; negative controls behave:
  η = 10^−11 → UNDECIDED (the true deviation 5.6·10^−11 exceeds it), X0 = 3 → UNDECIDED.
- Shard_rig on a 1/1000 shard (115 ratios, DIG 1040, QEXP 495, X0 10^6): η = 0.001 gives 28.58 window candidates per
  ratio vs 28.64 for the full run (η = 0.0005 gives 14.1), so the shipped enumeration was run with η = 10^−3 (the
  shard outputs do not print η or DIG; this inference is mine). product_solutions = 0.
- check677.py: (4,13,3), (18,53,4), (0,29,29), (999985,2400000,29) → FAIL (lcms differ); positive controls
  M(4,3) = M(13,2) and M(3,4) = M(19,2) → PASS.

## 4. Gaps, caveats, overstatements

- **Not kernel-checked; computer-assisted.** Only the partial-win criterion applies. The claim says so.
- **What is rigorous arithmetic and what is not.** Interval/exact: the margin (exact rational intervals, plus an mpmath
  interval run), the continued fractions of ρ (exact integer roots, common-prefix rule), the final product test
  f(m)·b = a·f(n), Lemma A and the ratio set. Not interval: the window bounds L, U (1090-digit mpmath), the float
  s-interval generation (±2 widening, `≥ x − 4` cell test) and the float pre-filter (tolerance 10^−6 vs a stated error
  ≤ 10^−9; patch documented). The L/U caveat is harmless in substance: solutions satisfy the margin with a relative
  slack of ~5.6·10^−11 against η = 10^−3 (my η = 10^−9 run of the exact checker still PROVES on samples), but the
  certificate as written does not formalise that slack. The float enumeration is backed by an error argument plus
  brute-force validation (historically k ≤ 12, q ≤ 4000; by me for 30 k = 29 ratios to q ≤ 2·10^5), not by a proof
  in interval arithmetic.
- **Hash search:** 64-bit additive hash; collisions only add candidates, so completeness does not depend on it.
- **Minor text issues (not affecting validity):** deep_rig.py's docstring says "1050-digit" (it is DIG + 50 = 1090);
  PROOF.md Step 5 item 6 cites a validation for k ≤ 12 only; η and DIG are not echoed in the enumeration outputs.
  CLAIM.md's status line ("unpanelled") predates this panel. A `__pycache__/deep_cf.cpython-313.pyc` appeared in
  claim/object at 09:20:33 UTC today, not created by me (I ran all Python with bytecode writing off); it does not
  affect any shipped output.
- **Subsumption:** not subsumed. The problem page notes only the ineffective Thue–Siegel finiteness for fixed k; the
  workspace's earlier confirmed claims cover k ≤ 25 and 26 ≤ k ≤ 28; this claim adds k = 29 only. Problem page and
  catalog still list the problem as open (catalog: Lean proof No).

## Verdict

The statement is exactly a restriction of `Erdos677.erdos_677` to k = 29, 0 ≤ n ≤ 10^494, with m uncapped; the seam,
n = 0, the upper end and the odd-k parity mapping are all correct; the Step 4 algebra is right and the exact checker
implements it; the shards partition the 114817-ratio set and the outputs match the claim. It meets the
partial-win criterion (exhaustive, uncapped-in-m verification with a checkable certificate), with the stated
floating-point caveats on the enumeration's bookkeeping. It is not a prize solution.

confirmed_scope: For k = 29, every 0 ≤ n ≤ 10^494 and every m ≥ n + 29 (m unbounded), lcm(m+1, …, m+29) ≠ lcm(n+1, …, n+29), established by a computer-assisted, not kernel-checked certificate (Lemma A, a complete small-X search for n + 29 ≤ 1.1·10^6, an exact-rational-interval margin for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 whose window bounds and candidate generation use high-precision/float arithmetic with error bounds and brute-force validation rather than interval arithmetic) — a workspace partial win for `Erdos677.erdos_677`, not a prize solution.
context: subagent (fresh context, Claude Code Agent tool)
pass: true
