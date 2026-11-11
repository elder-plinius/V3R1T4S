# REPRODUCE skeptic: Erdős 677, k = 29, n ≤ 10^494 (run 2026-11-09-0917)

context: subagent (fresh context, Claude Code Agent tool)

Scope read: `claim/` only (CLAIM.md, REPRODUCE.md, PATCH_NOTE.md, deep_rig_patch.diff, object/, checker/). Nothing else in
the workspace was read. The run folder's top-level `pids.txt` lists PIDs from an earlier container. None of them were
alive when this panel started (the machine had been up 2 minutes), so the machine was idle and all 4 cores were free.
Working copy: `panel_work/reproduce/object/` (copy of `claim/object/`). Raw outputs are in `panel_work/reproduce/runs/`, own
checks are in `panel_work/reproduce/own/`, and the PIDs of every background job are in `panel_work/reproduce/pids.txt`.
Python: the workspace venv (gmpy2 2.3.2, mpmath 1.3.0, numpy 2.5.4); gcc 13.3.0.

## 1. Full rerun of REPRODUCE.md (every step, whole ratio list)

All commands were run from `panel_work/reproduce/object/` (PY = workspace venv python, always with `-I`).

| step | command | result (from saved output) | vs `claim/object/out/` |
|---|---|---|---|
| build | `gcc -O2 -march=native -o search677b search677b.c -lm` | ok | – |
| small X | `./search677b 1100000 20261109 ../runs/my_search.txt` | `# COMPLETE kmin=3 kmax=147 total_candidates=2`; k=29 line `cand=0` (193705 prime-free m-windows) | identical to `search_N1.1e6.txt` with times stripped |
| verify | `PY -I verify_cands.py ../runs/my_search.txt` | `candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0` | identical apart from the `elapsed=` field (4 s vs 5 s) |
| ratio audit | `PY -I taskA_ratio_audit_k.py 400 29 29` | `|admissible_r|=114817 missing=0 extra=0`; `TOTAL missing over k=29..29: 0`; 110 equal-lcm pairs n<m≤400, 0 outside the set | byte-identical |
| margin (mpmath intervals) | `PY -I rig_margin.py 29 29 1000000 1 1000` | `k=29 pairs=114817 proved=114817 failures=0 undecided=0 ... worst_rel_margin_lower_bound=0.99999994 at r=21736/21735`; `TOTAL pairs=114817 failures=0 undecided=0` (332 s) | identical with time stripped |
| enumeration | `SHARD=$I/4 QEXP=495 PY -I shard_rig.py 29 29 1040 0.001 1000000` for I = 0..3, 4 in parallel | see below; each ~3950-3980 s | each shard identical with `t=` stripped |
| exact margin | `SHARD=$I/4 PY -I shard_margin.py 29 29 1000000 1 1000` for I = 0..3, 4 in parallel (started automatically when the 4 enumeration shards ended) | pairs 28705 + 28704 + 28704 + 28704 = 114817, each `proved=all failures=0 undecided=0`, worst relative margin lower bound 0.99999994; ~2592-2608 s per shard | each shard identical with `time_s=` stripped |

Enumeration shards (QMAX = 10^495 confirmed in every TOTAL line):

```
shard0 k=29 admissible_r=28705 enumerated_pairs=833627 window_candidates=822606 product_solutions=0 t=3978s
shard1 k=29 admissible_r=28704 enumerated_pairs=832852 window_candidates=821979 product_solutions=0 t=3977s
shard2 k=29 admissible_r=28704 enumerated_pairs=833512 window_candidates=822638 product_solutions=0 t=3945s
shard3 k=29 admissible_r=28704 enumerated_pairs=832536 window_candidates=821629 product_solutions=0 t=3973s
```

`sum_shards.py` on my four shard files: `k=29 shards=4 admissible_r=114817 enumerated_pairs=3332527 window_candidates=3288852
product_solutions=0`, identical to `out/shard_sums.txt`. 28705 + 3·28704 = 114817 = |admissible_r(29)|.

Shard wrappers: I read `shard_rig.py` and `shard_margin.py`. Each imports the unchanged program module, replaces its
module-level name `admissible_r` by a function returning `[r for j, r in enumerate(admissible_r(k)) if j % S == I]`, and
calls its `main()`. Both `deep_rig.main` and `rig_margin_exact.main` look up `admissible_r` as a module global at call
time (deep_rig.py line 152 and 186, rig_margin_exact.py line 155), so the patch takes effect, and the per-ratio work is
independent of other ratios. The residue classes j mod 4 partition the list. deep_rig.py sha256 =
0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341, as stated.

`checker/check677.py` gives FAIL for `4 18 53` ("lcms differ") and for `0 1 29` ("blocks overlap"), as expected.

## 2. Own independent checks (written from the definition and from my reading of PROOF.md)

All in `panel_work/reproduce/own/`, outputs next to each script.

1. **Exact checker and Lemma A, empirically** (`own_lemmaA.py`, output `own_lemmaA.txt`). M(x,k) = math.lcm of the block.
   Every equal-lcm pair n < m ≤ 600 for 1 ≤ k ≤ 40 (3139 pairs, 123 of them at k = 29; all overlapping, none
   disjoint): f(m)/f(n) equals ∏ p^{d_p} with d_p = Σ_{p^i<k}(c_{p^i}(m) − c_{p^i}(n)), each summand in {−1,0,1} and 0
   when p^i | k, 1 < r ≤ R(k), and r lies in my ratio set. Lemma-A failures: 0. The two near misses (3,4,13) and
   (4,18,53) have different lcms (210 vs 1680; 87780 vs 1580040).
2. **Own ratio set** (same script). For k = 29: primes < 29 with N_p = 4,3,2,1,1,1,1,1,1 (2,3,5,7,…,23), R(29) =
   80313433200 = lcm(1..28). The exponent box has 9·7·5·3^6 = 229635 points. The values are distinct by unique
   factorisation, the box is symmetric under r ↦ 1/r, and its maximum is R(29), so A_29 has (229635 − 1)/2 = 114817
   elements. My enumerated set equals `deep_cf.admissible_r(29)` exactly (114817, missing 0, extra 0, sorted, no
   duplicates). Smallest ratio 21736/21735, largest 80313433200.
3. **Own small-X search for k = 29** (`own_smallx.py`, output `own_smallx.txt`). This is a numpy re-implementation that
   does not use search677b.c. It uses a random 64-bit additive hash of the (≥ 29)-prime part of each block, every n with
   n + 29 ≤ 1.1·10^6 and every m with n + 29 ≤ m and m + 29 ≤ 3(n + 29). That bound is wider than Lemma A(b)'s factor
   R(29)^{1/29} = 2.37699. Result: 0 hash candidates, 0 exact-equal. Implication sanity check: all 164 lcm-equal pairs
   with n < m < 3000 have equal hashes.
4. **Own enumerator for Step 5** (`own_enum.py`). It uses no continued fractions, no s-interval quadratics and no
   floating point. For each dyadic block q ∈ [Q, 2Q) it takes the exact integer lattice (q, t = q·⌊ρN⌋ − pN), N =
   10^1100, and enumerates every lattice point in the box q ∈ [Q, min(2Q−1, QMAX)], t ∈ (−2Q, ⌈N·U/Q⌉]. It does this
   from an exact weighted-Gauss-reduced basis with exact coefficient bounds, then tests e > 0 exactly (a·q^29 > b·p^29)
   and q·e < U at 1090 digits. Its own correctness was checked against brute force (every q ≤ 3000, every p) on 300
   random ratios × 3 windows ([0.999c, 1.001c], [c/2, 1.001c], [c/2, 3c]). The same 900 tests compared
   `deep_rig.enum_pairs` with and without the float pre-filter: 0 mismatches (`own_brute_q3000.txt`).
   At the full QMAX = 10^495, with 1040-digit CFs, it was compared with `deep_rig.enum_pairs` (unfiltered: full set
   with q(qρ−p) < U; filtered: must contain every pair with g ∈ (L, U)) and with deep_rig.main's window-candidate
   selection. The ratios were:
   - the 10 ratios with the largest partial quotient below 10^495 over all 114817 ratios. A full scan
     (`own_cfscan_all.txt`) found maxima 2801331524 (r = 320229/95), 199676104, 130604083, 106113001, 16902850, …
     These cells take the patched exact-u branch with Qn ≈ 3.6·10^−10 (`own_enum_top10pq.txt`);
   - 9 further large-quotient ratios, the smallest, the middle and the largest ratio (`own_enum_extreme.txt`);
   - 40 random ratios (`own_enum_random40.txt`).
   All 63 ratios: the own full set equals enum_pairs' unfiltered set (from 9 pairs at r = 21736/21735 to 86666 pairs at
   r = 612612/19), the filtered set contains every own window pair, the window candidates agree, and my exact product
   test finds 0 solutions. `ALL OK` in all three files.
5. **Own margin spot check** (`own_margin.py`, output `own_margin.txt`). G_C(X) = rF(X) − F(ρX − C/X) is formed as a
   Laurent polynomial by multiplying the 29 factors directly (not with the binomial formula of Step 4), in 200 digits.
   The checks: coefficients of X^29 and of all X^{29−odd} vanish; a_1 − T > 0 for C₊ and −a_1 − T > 0 for C₋. In
   addition, F(Y) = rF(X) is solved directly at X ∈ {10^6, 10^6 + ½, 10^9, 10^30} and c(1−η) < X(ρX − Y) < c(1+η)
   is tested. This covered 3039 ratios (3000 random, the 20 smallest and the 20 largest): 0 failures of either kind.
   The worst relative margin is 0.9999999433 (at r = 21736/21735), matching the claimed 0.99999994.

## 3. Re-derivation of the PROOF.md steps

- **Lemma A.** I re-derived it. For p^i ≥ k with i ≤ v_p(L), each block has exactly one multiple of p^i: at least one
  because some element attains v_p(L), at most one because the gap is ≥ k. For i > v_p(L) neither block has one. So
  primes ≥ k cancel. Levels p^i < k contribute c ∈ {⌊k/p^i⌋, ⌊k/p^i⌋+1}, with the difference 0 when p^i | k. The count
  of levels with p^i < k and p^i ∤ k is v_p(lcm(1..k)) − v_p(k), so r ≤ R(k). Consequence (b) holds because
  (m+j)/(n+j) decreases in j. Consequence (c) holds because a prime P in the m-block would have to divide an n-block
  element < P. Correct.
- **Step 2 coverage.** X < 10^6 ⇔ n + 15 < 10^6, so n + 29 < 10^6 + 14 ≤ 1.1·10^6. I read search677b.c. It removes
  primes < k from the additive hash (removing prime k−1 when stepping to k), restricts to prime-free m-blocks, uses
  m ≤ (n+k)ρ_k + 2 − k with a float ρ_k < 3 (ψ bound), and probes all duplicate keys. Hash equality is implied by
  Lemma A step 2. Correct; my own k = 29 search confirms it independently.
- **Step 4 reduction.** I re-derived it. c = s(ρ²−1)/(kρ) = (k²−1)(ρ²−1)/(24ρ) from the X^{k−2} balance. X(ρX − Y) > C
  ⇔ Y < Y_C ⇔ (F increasing beyond the largest root (k−1)/2) G_C(X) < 0. So the margin ⇔ G_{C₊} > 0 and G_{C₋} < 0,
  with the strict inequalities in the right directions. The expansion gives a_t = r e_{k−2t} − ρ^{k−2t} Σ_v
  e_{k−2t+2v} C(k−2t+2v, v)(−Cρ)^v, a_0 = 0, and a_1 = ρ^{k−2}s(ρ²−1)(C/c − 1) = ±ρ^{k−2}s(ρ²−1)η. The bound
  |Σ_{t≥2} a_t X^{−2(t−1)}| ≤ T for X ≥ X0 holds. t ≤ k always (t = u + v with v ≤ k − 2u), so rig_margin_exact.py's
  table t = 1..k is complete. Its D = (k²−1)/24·fac·(ρ²−1) = Cρ, and the domain test ρX0 − C/X0 > (k−1)/2 is included.
  The code matches the derivation.
- **Step 5 bound |r'| ≤ 2U+1.** I re-derived it. For q_i ≤ q < q_{i+1}, r' ≠ 0 forces s ≠ 0 with opposite sign. Then
  |qρ − p| = |r'||d_{i+1}| + |s||d_i| ≥ |s||d_i| > |s|/(q_i + q_{i+1}). Together with q·e < U this gives |s|q_i <
  U(q_i + q_{i+1}). If r' > 0: r' q_{i+1} = q + |s|q_i < q_{i+1} + U(q_i+q_{i+1}), so r' < 1 + 2U. If r' < 0:
  |r'|q_{i+1} < s q_i < U(q_i+q_{i+1}) ≤ 2U q_{i+1}. The code uses R = ⌊2U⌋ + 2. Correct.
- **Pre-filter error bound (PATCH_NOTE).** I re-derived it. With r', s of opposite sign, |s·Qn| ≤ |r'| + 1, so the float
  u = r' + s·Qn has absolute error ≲ 3(|r'|+1)·2^−53 and relative error ≤ 3.4·10^−16(R+1)/Qn. The code switches to the
  exact u = q/q_{i+1} whenever that exceeds 10^−9 or Qn < 10^−4. w = r'D1 + sD0 has same-sign terms. Both are far
  below the 10^−6 filter tolerance. The s-interval endpoints have absolute error ≲ 2·2^−53·|B|/|A| ≲ 2.2·10^−4·|r'| at
  the 10^12 quotient cap, against a ±2 widening (and the program raises rather than skips on amax > 10^12 or an s-range
  > 10^5). Correct.
- **Covering.** k = 29 is odd: q = X = n + 15 ≤ 10^494 + 15 ≤ 10^495, and p = Y = m + 15. m is uncapped because Lemma
  A(b) and the margin fix Y from X. The final test is the exact f(m)·b = a·f(n), for every m > n.

## 4. Remarks on the claim (none invalidates it)

- PROOF.md Step 5 item 4 says the admissible s "form an interval". When the quadratic opens downward (A ≤ 0) the set is
  the union of two rays cut to the cell, and deep_rig.py does handle both pieces (lines 92-98). Only the prose is
  imprecise.
- As CLAIM.md says, the window bounds L, U in deep_rig.py are 1090-digit mpmath values, not intervals. The proven
  margin is strict, and the actual deviation X(ρX−Y) − c is O(c/X²) (relative margin lower bound 0.99999994), so an
  error of order 10^−1000 cannot drop a solution. Not formally rigorous, but negligible.
- The run times differ from REPRODUCE.md. Here the enumeration took ~3950-3980 s per shard (claimed ~5390 s) and the
  exact margin took 2592-2608 s per shard (claimed 3218-3230 s). The counts are identical, so this is only a matter of
  machine load.
- The claim is a partial result (k = 29 only, n ≤ 10^494), computer-assisted and not kernel-checked, as it states. It
  is not a solution of Erdős 677.

## Verdict

Every step of REPRODUCE.md was rerun in full on the whole ratio list (no sampling): the small-X search plus exact verification, the
ratio audit, rig_margin.py on all 114817 ratios, the exact margin on 4 shards (114817 pairs, 0 failures, 0 undecided)
and the enumeration on 4 shards with QMAX = 10^495 (114817 ratios, 3332527 enumerated pairs, 3288852 window candidates,
0 product solutions). Every output matches `claim/object/out/` apart from run times. My independent checks agree with
the claim: Lemma A on 3139 equal-lcm pairs, the ratio set, the k = 29 small-X search, the lattice enumerator at full
QMAX on 63 ratios including the most extreme partial quotients, brute force at q ≤ 3000 on 300 ratios, and the margin
expansion on 3039 ratios. The proof steps re-derive correctly. I found nothing wrong beyond the two minor remarks in
section 4. The claim is right as stated: for k = 29, 0 ≤ n ≤ 10^494, m ≥ n + 29, lcm(m+1..m+29) ≠ lcm(n+1..n+29). It is
computer-assisted, not kernel-checked, and a partial result only.

Finished at 11:10 UTC (all jobs ended; the deadline was 12:45 UTC). Background PIDs are in
`panel_work/reproduce/pids.txt`, and none are still running.

pass: true
