# REPRODUCE skeptic: claim of run 2026-11-06-0918 (Erdős 677, 26 ≤ k ≤ 28, n ≤ 10^494)

context: subagent (fresh context, Claude Code Agent tool)

Scope read: only the claim folder (CLAIM.md, REPRODUCE.md, object/ incl. object/PROOF.md and object/out/, checker/).
Work copy: object/ copied to ../panel_work/reproduce/object/ (paths below are relative to claim/); my own scripts
and all fresh outputs are in ../panel_work/reproduce/mine/. Python: the workspace venv (gmpy2 2.3.2, mpmath 1.3.0,
numpy 2.5.4); gcc 13.3.0. Machine: 4 cores. Started 09:20 UTC.

## Definition implemented (quoted)

From CLAIM.md / checker/spec_677.lean:
"`lcmInterval n k := (Finset.Ioc n (n + k)).lcm id`" and
"`∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k`".
Claimed range: "For every k with 26 ≤ k ≤ 28, every n with 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m),
lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k)."

My implementation (../panel_work/reproduce/mine/my_check.py, written before reading any of the author's code):
`lcm_interval(n, k)` = exact integer lcm of n+1..n+k (Python ints, gcd fold). `ratio_set(k)` = the set A_k of
PROOF.md step 3 built from my own reading of Lemma A: products ∏_{p<k} p^{d_p} with |d_p| ≤ #{i ≥ 1 : p^i < k,
p^i ∤ k}, kept when 1 < r ≤ R(k) = lcm(1..k)/k (exact Fractions).

## Own independent checks (my code, before reading the author's code unless noted)

| check | command (in ../panel_work/reproduce/mine) | result |
|---|---|---|
| definition brute force, no lemma used | `my_check.py brute 28 3000 9000` | `brute KMAX=28 NMAX=3000 MMAX=9000: equal pairs=0` (detector validated: it finds 56 overlapping equal-lcm groups for k ≤ 11, x < 3000) |
| Lemma A proof steps 1–3 on single blocks | `my_check.py lemmaparts 30 400` | `lemmaparts KMAX=30 XMAX=400: tests=556937 fails=0` (v_p(f) = Σ_{i ≤ v_p(L)} c_{p^i}; c_q ∈ {⌊k/q⌋, ⌊k/q⌋+1}; c_q = k/q iff q ∣ k; c_q = 1 for q = p^i ≥ k, i ≤ v_p(L)) |
| Lemma A statement on every equal-lcm pair (overlapping, n < m) | `my_lemmaA.py 28 2000` | `LemmaA test k=3..28 x<=2000: equal-lcm pairs=1339 violations=0` (ratio equals the d_p product, lies in my A_k, 1 < r ≤ R(k)) |
| ratio-set sizes | `my_check.py ratios 26 27 28` | `k=26 \|A_k\|=21262`, `k=27 \|A_k\|=16402`, `k=28 \|A_k\|=21262`; after reading deep_cf.py: my sets equal `admissible_r(k)` exactly as sets (True ×3), list sorted, no duplicates |
| independent small-X search for k = 26, 27, 28 (n ≤ 10^6, all m in the Lemma A(b) window; equal k-rough part G of f is necessary, hashed mod 2^61−1, every same-hash disjoint pair compared exactly) | `my_smallx.py K 1000000` | `k=26 NMAX=1000000 mtop=2221537 hashgroups>1=418 window pairs checked exactly=0 equal=0`; `k=27 ... mtop=2243260 hashgroups>1=415 ... =0 equal=0`; `k=28 ... mtop=2176632 hashgroups>1=462 ... =0 equal=0`. Without the window filter, k=26: `ALL disjoint same-hash pairs (no window filter) checked exactly=0 equal=0` (all same-hash groups are overlapping blocks). Detector validated on k = 3, 4: finds (4,13) and (18,53) when the window filter is off. |
| margin, non-rigorous own spot check | `my_margin_spot.py` (Y solved from F(Y) = rF(X) at 80 digits; 26 ratios per k incl. extremes; X ∈ {10^6, 10^6+1/2, 10^9, 10^20}) | `max \|X(rho X - Y)/c - 1\| ... : 5.2e-11 (eta = 1e-3)` |
| enumeration vs my brute force (after reading deep_rig.py; code under test is `deep_rig.enum_pairs`) | `my_enum_test.py ../object 100000` (10 ratios per k incl. min and max; U = S c(1+η) and U = 30 S c; q ≤ 10^5) | `enum test q<=100000: (k,r,U) cases=60 brute pairs total=358126 mismatches/CF failures=0`; also checked on the full 1040-digit CF of these 30 ratios: d_i alternate in sign, q_{i+1}\|d_i\| > 1/2, q_i increasing, last q > 10^495. (enum_pairs also returns pairs with p < 0 at tiny q; they cannot map to n ≥ 0, m > n and are discarded by main.) |
| enumeration at the full QMAX = 10^495, own re-implementation (60-digit cell geometry, 1090-digit re-check, no floats) vs `enum_pairs` window set | `my_enum2.py ../object 4 2026` (18 ratios: min, max and 4 random per k) | `enum2 sampled ratios=18 mismatches=0` (e.g. `k=28 r=2868336900 ... mine=475 theirs=475 OK`, `k=26 r=1029659400 ... mine=459 theirs=459 OK`). This is a spot check only; the complete enumeration is the full shard rerun below. |
| checker/check677.py on the two small-X near-misses | `check677.py 4 13 3`, `check677.py 18 53 4` | `M(n,k) = 210 / M(m,k) = 1680 ... FAIL` and `87780 / 1580040 ... FAIL` (lcms differ; my lcm_interval gives the same four values) |

## Proof steps re-derived (object/PROOF.md)

**Step 1, Lemma A (PROVED-HERE): verified.**
- 1: every block element divides L, so each element's v_p ≤ v_p(L) and v_p(f(x)) = Σ_{i=1}^{v_p(L)} c_{p^i}(x). Correct.
- 2: for p^i ≥ k with i ≤ v_p(L), an element of each block attains v_p = v_p(L) ≥ i (L is the block lcm), and two
  multiples of p^i differ by ≥ p^i ≥ k > k−1, so c = 1 in both blocks. Correct (includes p^i = k).
- 3: c_q ∈ {⌊k/q⌋, ⌊k/q⌋+1}, = k/q iff q ∣ k; p^i < k implies p^i ∣ L. So d_p has summands in {−1,0,1}, 0 when p^i ∣ k. Correct.
- 5: Σ over levels with p^i < k, p^i ∤ k equals v_p(lcm(1..k)) − v_p(k) (p^i ∣ k ⇒ p^i ≤ k; p^i = k ⇒ p^i ∣ k), so
  r ≤ lcm(1..k)/k. Correct. 6: f strictly increasing on n ≥ 0, so r > 1. Correct.
- (b): (m+j)/(n+j) is decreasing in j for m > n, so ((m+k)/(n+k))^k ≤ r ≤ R(k). Correct.
- (c): a prime P ∈ (m, m+k] divides L but every n-block element is in [1, n+k] ⊂ [1, P). Correct.
- Empirically confirmed by my Lemma A test above (1339 equal-lcm pairs, 0 violations).

**Step 2, small X (COMPUTED): verified.** Read object/search677b.c: hash A[y] = Σ_p v_p(y)·h(p) with all primes < k
removed (primes < kmin initially, then k−1 when prime at each k), sliding-window sums = additive hash of G_k; m runs
over prime-free blocks up to floor(N0·R(k)^{1/k}) + 2 − k (≥ the Lemma A(b) bound for every n ≤ N0 − k), n over
0..N0−k, all equal-key entries of the probe chain are reported when m ≥ n+k. K = maxgap − 1 = 147 from the sieve
(gap 148 at 2010733) bounds k for a prime-free block below 3·N0. Coverage X < 10^6 ⇒ n + k < 1.1·10^6: correct.
Independently confirmed for k = 26..28 by my own search (no prime-free filter, different hash, exact lcm).

**Step 3, ratio set (PROVED-HERE + COMPUTED): verified.** A_k as defined follows from Lemma A; `admissible_r` equals
my independently built set exactly. F has roots (k+1)/2 − j ≤ (k−1)/2 and X = n + (k+1)/2 > (k−1)/2. Correct.

**Step 4, margin (COMPUTED, rigorous): verified.** I re-derived the asymptotics: with s = k(k²−1)/12 = Σ a_j²,
log F(Z) = k log Z − s/(2Z²) + O(Z^−4), giving X(ρX − Y) → (k²−1)(ρ²−1)/(24ρ) = c. Reduction used by
object/rig_margin_exact.py and object/rig_margin.py (read): with C = c(1±η), D = Cρ, G(X) = rF(X) − F(ρX − C/X) =
Σ_{t≥1} a_t X^{k−2t}, a_t = r e_{k−2t} − ρ^{k−2t} Σ_v e_{k−2t+2v} binom(k−2t+2v, v)(−D)^v; I checked this expansion
by hand, and a_1 = ±ρ^{k−2} s'(ρ²−1)η with s' = k(k²−1)/24, so the sign test a_1 > Σ_{t≥2}|a_t|X0^{−2(t−1)} is the right
sufficient condition; the domain check ρX0 − C/X0 > (k−1)/2 (monotone in X) makes the monotonicity of F applicable in
both directions. rig_margin_exact.py uses exact rational intervals with ρ ∈ [A/2^96, (A+1)/2^96] certified by exact
integer powers. Negative tests I ran on 20 ratios of k = 26: η = 10^−12 gives `undecided=20`; CF = 101/100 gives
`failures=20`; η = 10^−3 gives `proved=20`. So the checker discriminates.

**Step 5, enumeration (COMPUTED + PROVED-HERE): verified, with one documentation remark.**
- Unimodular basis, r' = 0 multiples, opposite signs of r' and s, |r'| ≤ 2U+1: re-derived. With r' > 0 > s,
  q = r'q_{i+1} − |s|q_i ≥ 1 ⇒ |s|q_i > (r'−1)q_{i+1}, and q|qρ−p| ≥ q_i|s||d_i| > (r'−1)q_{i+1}|d_i| > (r'−1)/2
  (q_{i+1}|d_i| > q_{i+1}/(q_i+q_{i+1}) ≥ 1/2); with r' < 0 < s, |r'| < 2U. Code uses R = int(2U)+2. Correct.
- object/deep_rig.py `enum_pairs` (read in full): cells i with q_i ≤ QMAX, error if the CF is too short; r' = 0 branch
  s·(p_i,q_i) with s q_i < q_{i+1}, s ≤ sqrt(U/(q_i d_i)) + 2; r' ≠ 0 branch: s-interval from u = q/q_{i+1} ∈ [Qn, 1),
  w = (qρ−p)q_{i+1} > 0 and the quadratic g = u·w < U (all four sign cases of the leading coefficient handled),
  widened by 2, RuntimeError on any interval > 100000; every pair re-checked at 1090 digits. Float error analysis
  (mine): roots and endpoints have absolute error ≲ 0.1 for Qn ≥ 10^−12 (amax ≤ 10^12 is enforced), and the
  discriminant sign cannot flip for any pair with g ≤ U(1 − 10^−4) (a real solution has g = S·c(1 ± 10^−10)).
  Pre-filter: u from the exact integer q when Qn < 10^−4 or 3.4·10^−16(R+1)/Qn > 10^−9, otherwise float with
  relative error ≤ 3(|r'|+1)2^−53/Qn ≤ 10^−9; w is a same-sign sum; tolerance 10^−6. Correct.
- cf_of_root (object/deep_cf.py): floor(bρ·10^1040) via exact `iroot`, CF of both bracket endpoints, common prefix
  minus its last term. Correct (cylinder sets are intervals).
- Final mapping (k odd: (n, m) = (q, p) − (k+1)/2; k even: p, q odd, (n, m) = ((q, p) − k − 1)/2; X ≥ X0 test
  2n+k+1 ≥ 2X0) and the exact test f(m)·b = a·f(n). Correct. n ≤ 10^494 ⇒ q ≤ 2·10^494 + 29 < 10^495.
- object/shard_rig.py (read): replaces `deep_rig.admissible_r` by the sublist j ≡ I (mod S) of the sorted list and
  calls the unchanged `deep_rig.main()`, whose loop looks the name up in its module globals. It only restricts the
  ratio list. object/deep_rig.py sha256 = 0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 (matches CLAIM.md prefix).
- Remarks (do not change the verdict): (i) PROOF.md step 5.5 and step 3 cite "CLAIM.md, patch note" / "see CLAIM.md"
  for the float bound and the ratio audit; CLAIM.md has no patch note (the code comment cites NOTES.md, not in the
  claim folder). I re-derived the bound myself (above). (ii) As CLAIM.md says, L and U are computed in 1090-digit
  mpmath, not interval arithmetic; since a true solution has g/(S c) − 1 of order 10^−10 (my spot check: ≤ 5.2·10^−11)
  and η = 10^−3, rounding at 10^−1088 cannot matter. (iii) "lists every pair with q(qρ−p) < U" is exact up to pairs
  within float slack of the boundary U; irrelevant for the same reason.

**Conclusion paragraph of PROOF.md:** k ∈ {26,27,28} ≥ 3; X < 10^6 by step 2; X ≥ 10^6 by steps 4–5. Logic is complete.

## Computed steps rerun in full (REPRODUCE.md), compared with object/out/

All runs from ../panel_work/reproduce/object (copy of object/), fresh outputs in ../panel_work/reproduce/mine/.
Long jobs ran with nohup, PIDs recorded in ../panel_work/reproduce/pids.txt; all exited normally (stderr files empty).

**Step 2.** `gcc -O2 -march=native -o search677b search677b.c -lm`; `./search677b 1100000 20261106 ../mine/my_search.txt`:
```
# search677b N0=1100000 seed=20261106 Y=3400000 maxgap(primes<3N0)=148 at 2010733 => K=147 ; kmin=3 kmax=147 test=0 SHIFT=0 FORCE=auto CHUNK=16777216
3 4 13
4 18 53
# done k=26 nmax=1099974 X=2443602 rho=2.221478 primefree_m_windows=237786 insert_m=1 probes=1099975 cand=0 t=6s
# done k=27 nmax=1099973 X=2467492 rho=2.243198 primefree_m_windows=219386 insert_m=1 probes=1099974 cand=0 t=7s
# done k=28 nmax=1099972 X=2394200 rho=2.176569 primefree_m_windows=191192 insert_m=1 probes=1099973 cand=0 t=7s
# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=15s
```
Whole file identical to object/out/search_N1.1e6.txt apart from the t=/elapsed= fields (diff after stripping times:
empty). `verify_cands.py ../mine/my_search.txt`: `candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint
exact-equal: 0` and `disjoint candidates whose mismatch involves a prime outside the small range (hash collision?): 0`;
identical to object/out/verify_N1.1e6.txt apart from `elapsed=15s` vs `elapsed=6s`. MATCH.

**Step 3.** `taskA_ratio_audit_k.py 400 26 28`: output byte-identical to object/out/taskA_ratio_audit_k26-28.txt:
```
k=26 R=1029659400 levels=12 |S_A|=21262 |admissible_r|=21262 missing=0 extra=0 |S_cnt|=21262 C_subset_A=True narrowed_primes={}
k=27 R=2974571600 levels=12 |S_A|=16402 |admissible_r|=16402 missing=0 extra=0 |S_cnt|=16402 C_subset_A=True narrowed_primes={}
k=28 R=2868336900 levels=12 |S_A|=21262 |admissible_r|=21262 missing=0 extra=0 |S_cnt|=21262 C_subset_A=True narrowed_primes={}
TOTAL missing over k=26..28: 0
brute force n<m<=400: equal-lcm pairs per k {26: 88, 27: 93, 28: 109}; total 290; r outside sets: 0
```
MATCH (and my own set equality above).

**Step 4a.** `rig_margin.py 26 28 1000000 1 1000`:
```
k=26 pairs=21262 proved=21262 failures=0 undecided=0 time_s=72.3 worst_rel_margin_lower_bound=0.99999995 at r=3060/3059
k=27 pairs=16402 proved=16402 failures=0 undecided=0 time_s=47.5 worst_rel_margin_lower_bound=0.99999995 at r=1496/1495
k=28 pairs=21262 proved=21262 failures=0 undecided=0 time_s=67.0 worst_rel_margin_lower_bound=0.99999995 at r=8075/8073
TOTAL pairs=58926 failures=0 undecided=0
```
Identical to object/out/rig_margin_k26-28.txt apart from time_s. MATCH.

**Step 4b.** `rig_margin_exact.py K K 1000000 1 1000` for K = 26, 27, 28 (in parallel):
```
k=26 pairs=21262 proved=21262 failures=0 undecided=0 time_s=2470.3 worst_rel_margin_lower_bound=0.99999995 at r=3060/3059
TOTAL pairs=21262 failures=0 undecided=0
k=27 pairs=16402 proved=16402 failures=0 undecided=0 time_s=2250.0 worst_rel_margin_lower_bound=0.99999995 at r=1496/1495
TOTAL pairs=16402 failures=0 undecided=0
k=28 pairs=21262 proved=21262 failures=0 undecided=0 time_s=2862.3 worst_rel_margin_lower_bound=0.99999995 at r=8075/8073
TOTAL pairs=21262 failures=0 undecided=0
```
Each identical to object/out/rig_margin_exact_k26.txt, _k27.txt, _k28.txt apart from time_s. MATCH.

**Step 5.** `SHARD=I/4 QEXP=495 python3 -I shard_rig.py 26 28 1040 0.001 1000000` for I = 0..3 (4 processes,
09:20–11:06 UTC):
```
SHARD 0/4
k=26 admissible_r=5316 enumerated_pairs(q(q rho-p)<U)=496885 window_candidates=122523 product_solutions=0 t=3503s
k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104170 window_candidates=102823 product_solutions=0 t=4011s
k=28 admissible_r=5316 enumerated_pairs(q(q rho-p)<U)=560271 window_candidates=138789 product_solutions=0 t=6302s
TOTAL window candidates=364135 product solutions=0 (X0=1000000, QMAX=10^495)
SHARD 1/4
k=26 admissible_r=5316 enumerated_pairs(q(q rho-p)<U)=498434 window_candidates=122589 product_solutions=0 t=3487s
k=27 admissible_r=4101 enumerated_pairs(q(q rho-p)<U)=104192 window_candidates=102783 product_solutions=0 t=3990s
k=28 admissible_r=5316 enumerated_pairs(q(q rho-p)<U)=561724 window_candidates=138254 product_solutions=0 t=6282s
TOTAL window candidates=363626 product solutions=0 (X0=1000000, QMAX=10^495)
SHARD 2/4
k=26 admissible_r=5315 enumerated_pairs(q(q rho-p)<U)=497397 window_candidates=122961 product_solutions=0 t=3525s
k=27 admissible_r=4100 enumerated_pairs(q(q rho-p)<U)=104102 window_candidates=102798 product_solutions=0 t=4031s
k=28 admissible_r=5315 enumerated_pairs(q(q rho-p)<U)=560016 window_candidates=137846 product_solutions=0 t=6322s
TOTAL window candidates=363605 product solutions=0 (X0=1000000, QMAX=10^495)
SHARD 3/4
k=26 admissible_r=5315 enumerated_pairs(q(q rho-p)<U)=497072 window_candidates=122324 product_solutions=0 t=3527s
k=27 admissible_r=4100 enumerated_pairs(q(q rho-p)<U)=104543 window_candidates=103172 product_solutions=0 t=4031s
k=28 admissible_r=5315 enumerated_pairs(q(q rho-p)<U)=559985 window_candidates=138529 product_solutions=0 t=6327s
TOTAL window candidates=364025 product solutions=0 (X0=1000000, QMAX=10^495)
```
Every shard file is identical to object/out/deep_rig_shard0.txt … shard3.txt apart from the t= fields (diff after
stripping times: empty for all four), so the run is deterministic and reproduces. `sum_shards.py` on my outputs:
```
k=26 shards=4 admissible_r=21262 enumerated_pairs=1989788 window_candidates=490397 product_solutions=0
k=27 shards=4 admissible_r=16402 enumerated_pairs=417007 window_candidates=411576 product_solutions=0
k=28 shards=4 admissible_r=21262 enumerated_pairs=2241996 window_candidates=553418 product_solutions=0
```
equal to object/out/shard_sums.txt (and to the numbers in CLAIM.md; 490397 + 411576 + 553418 = 1455391).
Partition check (own code on `admissible_r`): shard sizes [5316, 5316, 5315, 5315], [4101, 4101, 4100, 4100],
[5316, 5316, 5315, 5315]; sums 21262, 16402, 21262; union equals the full list, no element twice. The shards
partition the ratio list. MATCH.

## Verdict per step

| step | type | verdict |
|---|---|---|
| 1 Lemma A (+ consequences a–c) | PROVED-HERE | confirmed (re-derived; own empirical test 0 violations) |
| 2 small X | COMPUTED | confirmed (full rerun identical; own independent search for k = 26..28: 0 pairs) |
| 3 ratio set | PROVED-HERE + COMPUTED | confirmed (own set equals admissible_r; audit identical) |
| 4 margin | COMPUTED (rigorous) | confirmed (reduction re-derived; both checkers rerun in full, identical; negative tests discriminate) |
| 5 enumeration | COMPUTED + PROVED-HERE | confirmed (bounds re-derived; code read; full 4-shard rerun identical, product_solutions=0 for every k; own re-implementation agrees on 18 ratios at QMAX = 10^495 and brute force agrees on 60 cases at q ≤ 10^5) |
| conclusion | logic | confirmed |

Non-blocking remarks: PROOF.md refers to a "patch note" in CLAIM.md that is not there (I re-derived the float bound
it should cover); L and U are high-precision mpmath values, not intervals (harmless by a margin of about 10^7 in
relative terms); the claim is computer-assisted and not kernel-checked, as CLAIM.md says.

No mismatch, no missing object, no non-determinism found. All steps finished before the deadline (last at 11:06 UTC).

pass: true
