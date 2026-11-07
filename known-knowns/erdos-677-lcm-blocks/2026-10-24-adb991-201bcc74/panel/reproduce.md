# REPRODUCE skeptic report: Erdős 677, k ≤ 25, n ≤ 10^494

context: subagent (fresh context, Claude Code Agent tool)

Scope: I read only the claim package `claim/` (CLAIM.md, REPRODUCE.md, object/, checker/, source/). All work is in
`panel_work/reproduce/`. `claim/` was not modified (the code was copied to `panel_work/reproduce/obj/`; sha256 of the
copies equals the originals, e.g. deep_rig.py 0e7d7d72…, deep_cf.py dc74be2f…). Python: the workspace venv, always
with `-I`. Every PID I started is in `panel_work/reproduce/pids.txt`. To stay at ≤ 3 cores while the 3-process
enumeration was running, every additional job was run while one of my own enumeration processes was paused with
SIGSTOP/SIGCONT (logged in pids.txt); the last exact-margin runs used cores freed by finished enumeration jobs. Note: pids.txt records the `timeout` wrapper PIDs; the python children were
3043 (k=25), 3044 (k=23), 3045 (k=24).

## 1. The definition (quoted) and my own checker

From `source/fc_677.lean` (formal-conjectures, `Erdos677.erdos_677`):

> Denote by $M(n, k)$ the least common multiple of the finite set $\{n+1, \dotsc, n+k\}$.
> Is it true that for all $m \geq n + k$, we get $M(m, k) \neq M(n, k)$?
>
> `theorem erdos_677 : ∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k`

with (CLAIM.md, checker/spec_677.lean) `lcmInterval n k := (Finset.Ioc n (n + k)).lcm id`, i.e. lcm{n+1,…,n+k}.
The claim is the restriction 1 ≤ k ≤ 25, 0 ≤ n ≤ 10^494, m ≥ n + k arbitrary.

My checker, written before reading any author code (`panel_work/reproduce/my_check_triple.py`):

```python
def lcm_interval(n, k):
    L = 1
    for x in range(n + 1, n + k + 1):   # Ioc n (n+k) = {n+1,...,n+k}
        L = L * x // gcd(L, x)
    return L
def is_counterexample(n, m, k):
    return k > 0 and m >= n + k and lcm_interval(m, k) == lcm_interval(n, k)
```

Output on the two near-misses of Step 2 (k, n, m) = (3, 4, 13), (4, 18, 53):
```
$ python3 -I my_check_triple.py 4 13 3
n=4 m=13 k=3 M(n,k)=210 M(m,k)=1680 counterexample=False
$ python3 -I my_check_triple.py 18 53 4
n=18 m=53 k=4 M(n,k)=87780 M(m,k)=1580040 counterexample=False
```
The author's checker/check677.py (read after writing mine) computes the same lcm the same way and prints `FAIL` for
`18 53 4`.

## 2. Step 1, Lemma A: re-derived

Let 0 ≤ n < m, M(n,k) = M(m,k) = L, f(x) = ∏_{j=1}^k (x+j), c_q(x) = #{1 ≤ j ≤ k : q | x+j}.

1. Every block element divides L, so each has v_p ≤ v_p(L); hence v_p(f(x)) = Σ_{i≥1} c_{p^i}(x) and
   c_{p^i}(x) = 0 for i > v_p(L) (an element divisible by p^i would have v_p > v_p(L)). Correct.
2. p^i ≥ k, i ≤ v_p(L): some element has v_p = v_p(L) ≥ i (L is the lcm of the block) so c ≥ 1; two multiples of p^i
   differ by ≥ p^i ≥ k > k−1 = span of the block, so c ≤ 1. So c_{p^i}(m) = c_{p^i}(n) = 1, and for i > v_p(L) both are
   0. Levels p^i ≥ k contribute nothing to v_p(f(m)) − v_p(f(n)); in particular primes p ≥ k contribute 0. Correct.
3. p^i < k: k consecutive integers contain ⌊k/p^i⌋ or ⌈k/p^i⌉ multiples (exactly k/p^i when p^i | k), so
   c(m) − c(n) ∈ {−1,0,1}, and 0 if p^i | k. Since p^i ≤ k−1 the block contains a multiple of p^i, so p^i | L and
   i ≤ v_p(L) automatically. Correct.
4. Hence r = f(m)/f(n) = ∏_{p<k} p^{d_p}, d_p = Σ_{p^i<k}(c_{p^i}(m) − c_{p^i}(n)), |d_p| ≤ #{i : p^i < k, p^i ∤ k}.
5. #{i : p^i ≤ k} = v_p(lcm(1..k)); #{i : p^i | k} = v_p(k); {p^i | k} ⊂ {p^i ≤ k}, and p^i = k implies p^i | k, so
   #{i : p^i < k, p^i ∤ k} = v_p(lcm(1..k)) − v_p(k); hence r ≤ ∏ p^{that} = lcm(1..k)/k = R(k). Correct.
6. r > 1 since f is strictly increasing on x ≥ 0. Correct.

Consequences: (a) R(1) = 1, R(2) = lcm(1,2)/2 = 1, so no r exists for k ≤ 2. Correct. (b) (m+j)/(n+j) is decreasing in
j (m > n), so r ≥ ((m+k)/(n+k))^k, giving m+k ≤ (n+k)R(k)^{1/k}. Correct. (c) a prime P ∈ (m, m+k] divides L, hence
some n+j ≤ n+k ≤ m < P, impossible. Correct. (Note: (c) needs m ≥ n+k; it is only used in that case.)

Additional sanity audit (my own script `my_lemmaA_audit.py 3000`, using my own ratio generator): all equal-lcm pairs
n < m ≤ 3000, 3 ≤ k ≤ 25, satisfy r ∈ A_k, the window bound in exact integers ((m+k)^k·k ≤ (n+k)^k·lcm(1..k)), and
prime-freeness of the m-block when m ≥ n+k:
```
k=24 equal_lcm_pairs=104
k=25 equal_lcm_pairs=111
TOTAL equal-lcm pairs n<m<=3000: 970  violations: 0
```
(970 equals the author's audit total in object/out/taskA_ratio_audit_NB3000.txt.)

## 3. Step 2 (X < 10^6, i.e. n + k ≤ 1.1·10^6): independently re-established

Coverage arithmetic: X = n + (k+1)/2 < 10^6 ⇒ n + k < 10^6 + (k−1)/2 ≤ 10^6 + 12 ≤ 1.1·10^6. Correct.

**Own program** `panel_work/reproduce/my_small.c` (written from Lemma A, not from search677b.c). For each 3 ≤ k ≤ 25 and
every n with n + k ≤ 1.1·10^6 it lists every m with m ≥ n+k, m+k ≤ (n+k)R(k)^{1/k} (long double, slack 1e-15
relative, only enlarging), prime-free m-block, and EXACTLY equal (≥k)-prime parts, i.e. identical multisets
{(q, v_q(f(x))) : q prime ≥ k} computed by exact factorisation (smallest-prime-factor sieve). It pins candidates with
the largest prime factor P of the n-block: if P ≥ k, P divides exactly one n+i and (equal v_P) the m-block must contain
a multiple n+i+tP (t ≥ 1) and have the same largest prime factor P; if P < k the m-block must also be (k−1)-smooth and
every window m is listed. (By Lemma A step 2, equal (≥k)-parts is a necessary condition for a counterexample.)

Validation against an independent Python brute force (`brute_small.py`, exact big-integer (≥k)-parts, exact window
test), with the window widened ×3 so that the sets are non-empty, N0 = 600: both give exactly
`3 4 13` and `4 18 53` (diff empty); with the true window, N0 = 3000: both empty.

Full run (`./my_small 1100000 3 25`, 70 s):
```
# k=3 rho=1.259921049895 exact_compared=7378050 equal_large_part=0
...
# k=25 rho=2.297148531153 exact_compared=2507670 equal_large_part=0
# DONE N0=1100000 k=3..25 total=0
```
Every k = 3..25 has equal_large_part = 0: no in-window pair with equal (≥k)-parts, hence no counterexample with
n + k ≤ 1.1·10^6, k ≤ 25.

**Author's command rerun** (`gcc -O2 -march=native -o search677b search677b.c -lm; ./search677b 1100000 4242
my_search.txt; verify_cands.py my_search.txt`): `# COMPLETE kmin=3 kmax=147 total_candidates=2`, candidates `3 4 13`,
`4 18 53`; `diff` against object/out/search_N1.1e6.txt differs only in the `t=`/`elapsed=` fields;
`candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0` identical to object/out/verify_N1.1e6.txt.
With seed 777: same 2 candidates, `exact-equal: 0`. (The 2 author candidates lie outside the Lemma A window — the
chunked search uses a looser m-bound — which is why my in-window list is empty; consistent.) I also read search677b.c:
the additive hash over all prime powers minus primes < k is a function of the (≥k)-part, the sliding windows and
table probing find every equal-hash pair, the bound K = 147 from the largest prime gap below 3.3·10^6 is correct
(a prime-free (m, m+k] with m < 3N0 forces a gap ≥ k+1), and ρ_k < 3 is checked.

## 4. Step 3: the ratio set

Own generator `my_ratios.py` (product over primes p < k of p^e, |e| ≤ #{i : p^i < k, k mod p^i ≠ 0}, keep
1 < a/b, a·k ≤ lcm(1..k)·b), compared as exact (num, den) sets with `deep_cf.admissible_r(k)`:
```
k=3 mine=1 author=1 missing_in_author=0 extra_in_author=0
...
k=23 mine=16402 author=16402 missing_in_author=0 extra_in_author=0
k=24 mine=9841 author=9841 missing_in_author=0 extra_in_author=0
k=25 mine=16402 author=16402 missing_in_author=0 extra_in_author=0
TOTAL mine=63041 mismatches=0
```
A_k as defined in PROOF.md Step 3 is exactly the set Lemma A allows (r = ∏ p^{d_p} with the proven exponent bounds and
1 < r ≤ R(k)). ρ = r^{1/k} is irrational for every r ∈ A_k (r = (u/v)^k would need k·|e_p| ≤ L_p < k, so r = 1).

## 5. Step 4: margin

**Reduction, re-derived.** F(Z) = ∏(Z + s_j), s_j = j − (k+1)/2, Σ s_j = 0, Σ s_j² = k(k²−1)/12, so
F(Z) = Z^k − (k(k²−1)/24) Z^{k−2} + … with only k−2t powers. F is increasing on ((k−1)/2, ∞). If
ρX − C/X > (k−1)/2 (domain; ρX − C/X is increasing in X for C > 0, so checking X0 suffices), then
X(ρX − Y) < C ⇔ Y > ρX − C/X ⇔ rF(X) > F(ρX − C/X) ⇔ P_C(X) := X^k[rF(X) − F(ρX − C/X)] > 0. Expanding
X^k (ρX − C/X)^j = Σ_v C(j,v) ρ^{j−v} (−C)^v X^{k+j−2v} gives P_C = Σ_t a_t X^{2k−2t} with
a_t = r e_{k−2t} − ρ^{k−2t} Σ_v e_{k−2t+2v} C(k−2t+2v, v)(−Cρ)^v — exactly the code's formula with D = Cρ.
a_0 = r − ρ^k = 0 exactly (dropped by identity, never computed). I derived
a_1 = ρ^k e_{k−2} − ρ^{k−2} e_{k−2} + kρ^{k−2}D = ±η·k(k²−1)ρ^{k−2}(ρ²−1)/24 for C = c(1±η): the non-η part cancels
exactly, so a_1 > 0 on the upper side and −a_1 > 0 on the lower side. Numerical check of the author code's a_1 against
my closed form (`my_a1_check.py`, 40 ratios per k, both sides): max relative difference 3.2e−69. The sufficient
condition a_1 > Σ_{t≥2}|a_t| X0^{−2(t−1)} implies P_C > 0 on [X0, ∞). Correct. The integer variables: odd k,
(p,q) = (Y,X), S = 1; even k, (p,q) = (2Y, 2X), q(qρ − p) = 4X(ρX − Y), S = 4. Correct.

**Reruns.**
- `rig_margin.py 3 25 1000000 1 1000` (interval, 151 s): `TOTAL pairs=63041 failures=0 undecided=0`; every per-k line
  identical to object/out/rig_margin_k3-25_X1e6_eta1e-3.txt apart from time_s.
- `rig_margin_exact.py 3 18 1000000 1 1000` (exact rationals, 99 s): `TOTAL pairs=4360 failures=0 undecided=0`;
  after the enumeration freed cores also `rig_margin_exact.py 19 22 …` (`TOTAL pairs=16036 failures=0 undecided=0`)
  and `rig_margin_exact.py 24 24 …` (`TOTAL pairs=9841 failures=0 undecided=0`). Also `rig_margin_exact.py 23 23 …` (`TOTAL pairs=16402 failures=0 undecided=0`). All 22 per-k lines (k = 3..24) are
  identical to object/out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt apart from time_s (`diff` empty for k = 3..22, 24; k = 23 line equal by inspection). k = 25 of
  the exact checker was not rerun (no time); the interval checker covers it.
- Additional (closes a gap, see §8): `rig_margin.py 3 25 1000000 1 1000000` (η = 10^−6, 150 s):
  `TOTAL pairs=63041 failures=0 undecided=0` (worst relative margin 0.9999586 at k=25, r=2737/2736). So every true
  solution with X ≥ 10^6 has q(qρ−p) within relative 10^−6 of S·c, far inside the enumeration window (L, U) = S·c(1 ∓ 10^−3).

## 6. Step 5: enumeration — completeness re-derived

- Decomposition: for q_i ≤ q < q_{i+1}, (p,q) = r'(p_{i+1},q_{i+1}) + s(p_i,q_i) with integer r', s (determinant ±1).
  r' = 0: multiples of a convergent; s = 0 and r' ≠ 0 impossible; r', s of equal sign give q ≥ q_{i+1} or q < 0, so
  opposite signs. Then r'd_{i+1} and s d_i have equal signs and |qρ−p| = |r'||d_{i+1}| + |s||d_i| ≥ |s||d_i|.
- r' bound: q|qρ−p| < U and q ≥ q_i give |s| < U/(q_i|d_i|) < U(q_i+q_{i+1})/q_i (using |d_i| > 1/(q_i+q_{i+1})). If r' > 0: r'q_{i+1} = q + |s|q_i < q_{i+1} + U(q_i+q_{i+1}),
  so r' < 1 + U(1+q_i/q_{i+1}) ≤ 1 + 2U. If r' < 0: |r'|q_{i+1} = s q_i − q < U(q_i+q_{i+1}), |r'| < 2U. The code uses
  R = int(2U) + 2 ≥ 2U + 1. Correct.
- g(s) = q(qρ−p) = (r' + sQn)(r'D1 + sD0), Qn = q_i/q_{i+1}, D_j = d_j q_{i+1}; A = QnD0, B = r'(QnD1 + D0),
  C0 = r'²D1 − U; constraints u = r' + sQn ∈ [Qn, 1), w = r'D1 + sD0 > 0. Case analysis in the code (A > 0 between the
  roots; A < 0 outside the roots or everywhere if disc < 0) is correct. Exact identities I used:
  q_{i+1}|d_i| + q_i|d_{i+1}| = 1, QnD1 + D0 = ±(1 − 2q_i|d_{i+1}|) with 0 < 1 − 2q_i|d_{i+1}| ≤ 1,
  |D0| ≥ 1/2. A > 0 forces r' < 0 < s; A < 0 forces r' > 0 > s.
- Float stage (my own error analysis; PROOF.md only asserts "widened by 2"): with the asserted run-time limits
  1/Qn ≤ 10^12 + 1 and |r'| ≤ R ≤ 343 (max over k ≤ 25: k = 24, U ≈ 170.6), the bounds lo, hi and the relevant root
  are computed without catastrophic cancellation (A > 0: −B > 0 and disc = B² + 4A|C0|; A < 0, Qn < 10^−4:
  disc ≥ 0.93 B²; A < 0, Qn ≥ 10^−4: roots ≤ ~3.4·10^6 in size), so the absolute error of every s-bound is ≲ 0.4,
  below the ±2 widening; where disc is near 0 (A < 0) a wrongly excluded gap has length ≪ 4 and is covered by the
  two ±2-widened pieces; a wrongly negative disc for A < 0 admits all of [lo, hi] (superset). Every generated pair is
  re-checked with 1090-digit e = qρ − p (absolute error ≈ 10^−595 vs e ≥ ~10^−498).
- Pre-filter (patched): exact-u branch u = float(mpq(q, q_{i+1})), w has no cancellation ⇒ rel. error ~10^−15;
  float branch: |sQn| ≤ |r'|+1, abs. error ≤ 3(|r'|+1)2^−53, relative ≤ 3.4·10^−16(R+1)/Qn ≤ 10^−9 by the branch
  condition; tolerance 10^−6. r' = 0 branch: smax = min(√(U/(QnD0)), 1/Qn) + 2, g = s²QnD0. Correct.
- Mapping and parity: odd k n = q − (k+1)/2, m = p − (k+1)/2; even k requires q, p odd (q = 2n+k+1 is odd),
  n = (q−k−1)/2. X0 filter 2n+k+1 < 2X0 ⇔ X < X0. Coverage: n ≤ 10^494 ⇒ q ≤ 2·10^494 + 25 < 10^495 = QMAX. The final
  test f(m)·b = a·f(n) is exact. Correct.
- 1,174,616 = 42649 + 248311 + 314109 + 202516 + 367031 (CLAIM total): correct.

**Validate mode** (brute force q ≤ 4000, DIG = 200): `deep_rig.py 3 12 200 0.001 1000000 validate`: 394 lines, all
`OK` (8 s); additionally `deep_rig.py 13 18 200 0.001 1000000 validate`: 3966 lines, all `OK` (98 s).

**Own enumerator** (`my_enum.py`, my own CF from a 1100-digit ρ with determinant and |q_iρ−p_i| < 1/q_{i+1} asserts,
s-intervals solved in 40-digit mpmath, ±1 widening, 1100-digit exact re-check), validated against brute force
q ≤ 4000 for all ratios k = 3..9 (`brute_ok_ratios` = 1,1,7,4,22,13,31 = all), then run at QMAX = 10^495:
```
k=3 own_enum: pairs(g<U)=213 pairs(L(1-1e-6)<g<U)=0 window_candidates=0 product_solutions=0
k=4 own_enum: pairs(g<U)=1657 pairs(L(1-1e-6)<g<U)=4 window_candidates=2 product_solutions=0
k=5 own_enum: pairs(g<U)=3623 pairs(L(1-1e-6)<g<U)=13 window_candidates=13 product_solutions=0
k=6 own_enum: pairs(g<U)=12397 pairs(L(1-1e-6)<g<U)=25 window_candidates=8 product_solutions=0
k=7 own_enum: pairs(g<U)=23524 pairs(L(1-1e-6)<g<U)=43 window_candidates=43 product_solutions=0
k=8 own_enum: pairs(g<U)=77275 pairs(L(1-1e-6)<g<U)=149 window_candidates=39 product_solutions=0
k=9 own_enum: pairs(g<U)=55390 pairs(L(1-1e-6)<g<U)=108 window_candidates=107 product_solutions=0
k=10 own_enum: pairs(g<U)=286693 pairs(L(1-1e-6)<g<U)=551 window_candidates=137 product_solutions=0
```
These equal the author's enumerated_pairs / window_candidates for k = 3..10 (0/0, 4/2, 13/13, 25/8, 43/43, 149/39,
108/107, 551/137). (k ≥ 11 not run with my enumerator: no free core.) This is a spot check of the method, not a substitute for the full rerun.

## 7. Step 5: full enumeration rerun (k = 3..25, QMAX = 10^495, DIG = 1040, η = 0.001, X0 = 10^6)

Command (as in REPRODUCE.md, one k per process so three processes could be balanced):
`QEXP=495 nice -n 10 timeout <until 11:59 UTC> python3 -I obj/deep_rig.py K K 1040 0.001 1000000 > enum/kK.txt`
for every K = 3..25, at most 3 at a time (worker scripts `worker.sh`, `waiter.sh`, `waiter2.sh`; status logs
`enum/*.status`). Start 10:28:46 UTC. Each output file ends with
`TOTAL window candidates=… product solutions=0 (X0=1000000, QMAX=10^495)` and contains no `PRODUCT SOLUTION` line.

Comparison (`compare_enum.sh`: per-k lines of all five object/out/deep_rig_final_*.txt files vs the rerun, `t=` field
stripped, `diff`):

```
$ ./compare_enum.sh
saved lines: 23  rerun lines: 23
ALL PER-K LINES IDENTICAL (times ignored)
```
All 23 per-k lines (k = 3..25) are identical; product_solutions = 0 for every k; window candidates sum to
1,174,616. Every run finished before the deadline (last one, k = 24, at about 11:36 UTC).

Rerun per-k lines (identical to the saved ones):
```
k=3 admissible_r=1 enumerated_pairs(q(q rho-p)<U)=0 window_candidates=0 product_solutions=0
k=4 admissible_r=1 enumerated_pairs(q(q rho-p)<U)=4 window_candidates=2 product_solutions=0
k=5 admissible_r=7 enumerated_pairs(q(q rho-p)<U)=13 window_candidates=13 product_solutions=0
k=6 admissible_r=4 enumerated_pairs(q(q rho-p)<U)=25 window_candidates=8 product_solutions=0
k=7 admissible_r=22 enumerated_pairs(q(q rho-p)<U)=43 window_candidates=43 product_solutions=0
k=8 admissible_r=13 enumerated_pairs(q(q rho-p)<U)=149 window_candidates=39 product_solutions=0
k=9 admissible_r=31 enumerated_pairs(q(q rho-p)<U)=108 window_candidates=107 product_solutions=0
k=10 admissible_r=37 enumerated_pairs(q(q rho-p)<U)=551 window_candidates=137 product_solutions=0
k=11 admissible_r=157 enumerated_pairs(q(q rho-p)<U)=799 window_candidates=780 product_solutions=0
k=12 admissible_r=121 enumerated_pairs(q(q rho-p)<U)=2745 window_candidates=678 product_solutions=0
k=13 admissible_r=472 enumerated_pairs(q(q rho-p)<U)=3388 window_candidates=3343 product_solutions=0
k=14 admissible_r=337 enumerated_pairs(q(q rho-p)<U)=10984 window_candidates=2734 product_solutions=0
k=15 admissible_r=283 enumerated_pairs(q(q rho-p)<U)=2418 window_candidates=2365 product_solutions=0
k=16 admissible_r=202 enumerated_pairs(q(q rho-p)<U)=7884 window_candidates=1884 product_solutions=0
k=17 admissible_r=1822 enumerated_pairs(q(q rho-p)<U)=20404 window_candidates=20134 product_solutions=0
k=18 admissible_r=850 enumerated_pairs(q(q rho-p)<U)=42369 window_candidates=10382 product_solutions=0
k=19 admissible_r=5467 enumerated_pairs(q(q rho-p)<U)=79038 window_candidates=77951 product_solutions=0
k=20 admissible_r=3037 enumerated_pairs(q(q rho-p)<U)=191057 window_candidates=46823 product_solutions=0
k=21 admissible_r=3280 enumerated_pairs(q(q rho-p)<U)=53594 window_candidates=52854 product_solutions=0
k=22 admissible_r=4252 enumerated_pairs(q(q rho-p)<U)=286131 window_candidates=70683 product_solutions=0
k=23 admissible_r=16402 enumerated_pairs(q(q rho-p)<U)=318320 window_candidates=314109 product_solutions=0
k=24 admissible_r=9841 enumerated_pairs(q(q rho-p)<U)=822422 window_candidates=202516 product_solutions=0
k=25 admissible_r=16402 enumerated_pairs(q(q rho-p)<U)=372097 window_candidates=367031 product_solutions=0
```
Wall times of my rerun (t= field): k=23 1950 s, k=25 2192 s, k=22 1247 s, k=20 988 s, k=19 448 s, k=24 4033 s (k = 24 was paused about 7 min in total by my SIGSTOPs).
Determinism: two independent processes produce the same counts as the author's saved files; the enumeration has no
random component.

## 8. Mismatches, gaps and caveats

Mismatches: none found. Every rerun output I compared (Step 2 search and verify, ratio set, interval margin k=3..25,
exact margin k=3..24, validate k=3..18, enumeration k=3..25 all 23 lines) agrees with the saved outputs apart from times.

Gaps / caveats (none of them, after my own checks, is an error):
1. PROOF.md Step 5.4 asserts the ±2 widening of the double-precision s-interval without an error analysis. I supplied
   one (§6); it is a hand analysis with explicit bounds (errors ≲ 0.4 ≪ 2), relying on the run-time assertions
   partial quotient ≤ 10^12 and s-range ≤ 10^5 which did not fire. My own 40-digit enumerator agrees with the author's
   counts for k = 3..10 at QMAX = 10^495, and validate mode agrees with brute force for q ≤ 4000, k = 3..18.
2. The window bounds L, U in deep_rig.py are computed in 1090-digit floating point, not interval arithmetic (CLAIM
   says so). Closed by my η = 10^−6 run of the rigorous interval checker: true solutions sit within relative 10^−6
   of S·c, i.e. ~10^−3 away from L and U, while all 1090-digit errors are ~10^−590 relative.
3. The exact-rational margin checker was rerun for k = 3..24, not k = 25 (the interval checker, which is rigorous
   on its own, was rerun in full for k = 3..25 at η = 10^−3 and at η = 10^−6).
4. PROOF.md Step 2 says search677b lists m with m + k ≤ (n+k)R(k)^{1/k} + slack; its chunked mode actually uses the
   looser chunk-wide bound, which is why its two candidates (3,4,13), (4,18,53) lie outside the Lemma A window.
   Harmless (superset); my exact in-window search finds none.
5. Stale comments in deep_rig.py ("margin_check.py --tight", "1050-digit") and references to NOTES.md (not in the
   package); I re-derived the margin reduction myself instead.
6. CLAIM.md's statements comparing patched vs unpatched code cannot be checked from the package (the unpatched code is
   not included); they are not needed for validity.
7. The result is computer-assisted and not kernel-checked (as CLAIM.md states); it is a partial result (k ≤ 25,
   n ≤ 10^494), not a proof of erdos_677.


## 9. Verdict

Everything required was done before the 12:00 UTC hard stop: own checker from the quoted definition; Lemma A and its
consequences re-derived; Step 2 re-established by my own exact program (0 in-window pairs with equal (≥k)-parts for
k = 3..25, n + k ≤ 1.1·10^6) and by the author's command (identical output); ratio set reproduced by my own generator
(63041, 0 mismatches); margin reduction re-derived, exact cancellation of a_0 and the closed form of a_1 checked,
domain condition checked; interval margin checker rerun in full (and at η = 10^−6), exact checker rerun for most k;
enumeration completeness re-derived (decomposition, r'-bound, s-interval, ±2 widening with my own float error
analysis, pre-filter and patch, mapping, parity, coverage, X0 split); the FULL enumeration rerun for every
k = 3..25 matches all 23 saved per-k lines exactly with product_solutions = 0; validate mode OK for k = 3..18; my
own independent enumerator reproduces k = 3..10. No mismatch, no missing object, no non-determinism found.

pass: true
