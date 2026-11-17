# REPRODUCE skeptic: erdos-677-lcm-blocks, claim "no counterexample with n ≤ 5871·k"

context: subagent (fresh context, Claude Code Agent tool)

What I read: claim/ only (CLAIM.md, REPRODUCE.md, object/PROOF.md, object/out/range_nCk_C5871.txt, checker/, source/).
I read object/range_nCk.py only after my own checker had been written, validated and run. My scratch files are in
../panel_work/reproduce/.

## 1. The definition

From checker/spec_677.lean, which is verbatim from source/fc_GCDMonoid_Finset.lean and from the body of
`Erdos677.erdos_677` in source/fc_Erdos677.lean (I compared them by eye and they are identical):

```
def lcmInterval {α : Type*} [CommSemiring α] [NormalizedGCDMonoid α]
    [Preorder α] [LocallyFiniteOrder α] (n k : α) : α := (Finset.Ioc n (n + k)).lcm id

def spec : Prop :=
  ∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k
```

On ℕ, `Finset.Ioc n (n+k)` is {n+1, …, n+k}. `Finset.lcm id` is the ordinary lcm: it is 1 on the empty set, and here
k > 0 and every element is ≥ 1. Write M(x, k) = lcm(x+1, …, x+k).

What must be true: for all naturals k ≥ 1, n ≤ 5871·k and m ≥ n + k, M(m, k) ≠ M(n, k). Overlapping pairs
(m < n + k) are outside the statement.

The sha256 of all object and checker files matches the table in CLAIM.md. The two source/*.lean files match
source/fetch_log.txt.

## 2. Re-derivation of object/PROOF.md

Notation: N = n + k, A = (N−k, N], B = (m, m+k], and L = lcm A = lcm B for a counterexample.

- **Step 0 (k = 1).** M(m,1) = m+1 ≥ n+2 > n+1. Correct.
- **S0.1.** If p^e | b ∈ B, then p^e | L. Since v_p(L) = max_a v_p(a), p^e divides some a ∈ A, so p^e ≤ N. Correct.
  This step does not use disjointness.
- **S0.2.** Every b ∈ B is > m ≥ N, so no b is a prime power, and B contains no prime. Correct.
- **S0.3.** A = (N−k, N] contains a multiple of q iff N mod q ≤ k−1. The largest multiple of q that is ≤ N is
  N − (N mod q), and it is ≥ N−k+1 ≥ 1 exactly in that case. Correct for every q, and vacuous for q ≤ k. My checker
  uses it for all prime powers, not only for primes.
- **S1.**
  - The valuations: v_p(∏X) = Σ_e c_e, and v_p(lcm X) = #{e : c_e ≥ 1} because c_e is non-increasing. So
    v_p(D(X)) = Σ_e (c_e − 1)^+.
  - The bounds: c_e ∈ {⌊k/p^e⌋, ⌈k/p^e⌉}.
    - Upper: ⌈k/p^e⌉ − 1 = ⌊(k−1)/p^e⌋ sums to v_p((k−1)!).
    - Lower: c_e − 1 ≥ ⌊k/p^e⌋ − 1 when p^e ≤ k, and ≥ 0 otherwise. This sums to v_p(k!) − #{e : p^e ≤ k}.
    - Hence k!/lcm(1..k) ≤ D(X) ≤ (k−1)!.
  - For a counterexample, ∏B/∏A = D(B)/D(A) ≤ lcm(1..k)/k.
  - (m+i)/(n+i) is non-increasing in i (its derivative is (n−m)/(n+i)² ≤ 0), so ((m+k)/N)^k ≤ ∏B/∏A.
  - This gives (E1) k(m+k)^k ≤ lcm(1..k)·N^k, and so m + k ≤ c_k·N with
    c_k = exp((ψ(k) − ln k)/k) ≤ exp(ψ(k)/k). Correct.
- **Constant.** e^1.03883 = 2.825908766147356… < 2.8260 (mpmath, 50 digits; ../panel_work/reproduce/consts.py).
  PROOF.md's "2.82591…" is right.
- **S2.**
  - n ≤ 5871k gives N ≤ 5872k, so m + k < 2.8260·5872·k = 16594.272·k (exactly 2074284/125), hence m < 16593.272·k.
  - Suppose m ≥ 2010760 (> 2010759.9). [Sch76] gives a prime p ∈ (m, m(1+1/16597)). B is prime-free and p > m, so
    p > m+k. Hence k < m/16597, i.e. m > 16597k > 16593.272k: a contradiction. So m ≤ 2010759.
  - 2.8260·5872 = 16594.272 < 16597: checked.
  - The step also works with the non-strict variant "x ≥ 2010760, x < p ≤ x(1+1/16597)". Correct.
- **S3.** Conditions (a)–(f) each follow from S0–S2. Correct. With m ≤ 2010759, the largest prime-free block lies in
  the gap 2010733 → 2010881 (length 148), so k ≤ 147.

**The two cited KNOWN results, as I know them:**

- [RS62] J. B. Rosser and L. Schoenfeld, Illinois J. Math. 6 (1962), 64–94: ψ(x) < 1.03883·x for every x > 0. As I
  recall, this is Theorem 12. The supremum of ψ(x)/x is reached at x = 113. PROOF.md states it correctly.
- [Sch76] L. Schoenfeld, Math. Comp. 30 (1976), 337–360: if x > 2010759.9, there is a prime p with
  x < p < x(1 + 1/16597). As I recall, this is Theorem 12 and it is unconditional (it does not assume RH). PROOF.md
  states it correctly.

**Fetches.** I sent one plain request to each publisher PDF: [Sch76] from the AMS at 2026-10-15T09:53:16Z, and [RS62]
from Project Euclid at 09:53:17Z. I used curl with default settings and no retry. The egress proxy refused both
("CONNECT tunnel failed, response 403"). The statements above therefore come from my own knowledge, not from re-reading
the papers in this session.

**Numerical consistency** (sanity only, not proof steps; ../panel_work/reproduce/sanity.c, PID 13333):

- The maximum of ψ(n)/n for n ≤ 10^8 is 1.038820578, at n = 113. This is below 1.03883.
- The maximum of c_n for n ≤ 10^8 is 2.743705, at n = 199.
- The [Sch76] statement holds for every x in (2010759.9, 10^9): 50,697,845 consecutive-prime pairs, 0 violations.
  The tightest case is the gap 2010733 → 2010881, at ratio 0.99957.
- 2010881/(1 + 1/16597) = 2010759.848. This explains the threshold 2010759.9.

## 3. My own checker (written and run before reading object/range_nCk.py)

../panel_work/reproduce/mycheck.c is written in C and uses exact integers only, with no floating point. The finite set
that the reduction (S0.2 + S2) leaves is

  T = {(n, m, k) : k ≥ 2, 0 ≤ m ≤ 2010759, (m, m+k] prime-free, k ≤ N ≤ min(m, 5872k)}.

**How it walks T.** It iterates m = 0..2010759. For each m it takes k = 1, 2, … until m + k is prime, so every
prime-free block is visited with every k. It skips only k = 1, which Step 0 covers. For each N it uses only these
proven facts:

- **R1 (S0.1):** N ≥ qstar, the largest prime power dividing an element of B.
- **R3 (S0.3):** N mod q ≤ k−1 for every maximal prime power q = p^(max v_p over B) with q > k.
- **Exact comparison:** lcm A = lcm B iff, for every prime p, max over A of p^v_p equals max over B of p^v_p. It is
  checked in both directions. Every element (≤ 2.1·10^6) is factored exactly with a smallest-prime-factor sieve.

It uses no size bound (E1), no floating point, and no restriction to two primes. The candidate N are the windows
[t·qstar, t·qstar + k − 1] ∩ [max(k, qstar), min(m, 5872k)]. That is exactly the set of N with N mod qstar ≤ k−1.

**Validation against pure brute force.** ../panel_work/reproduce/brute.py computes the big-integer lcm for every x
and k, groups the values, and uses no pruning.

- Overlap mode: blocks may overlap, with n < m ≤ 20000, k ≤ 40 and n ≤ 5871k. R1 and R3 do not use disjointness, so
  they still apply. My checker found 5004 equalities and brute force found 5004. The two sets are identical, and both
  include (2,3,3) and (0,1,11). PIDs 12063 and 12066.
- Disjoint mode, m ≤ 20000: brute force (k ≤ 40) finds 0 and my checker finds 0. PIDs 12189 and 12206.

**Main run** (background job PID 12161, `nice -n 15 timeout 3000`, m ≤ 2010759):

| quantity | value |
|---|---|
| prime-free pairs (m, k ≥ 2) | 19,745,817 (largest k 147) |
| pairs with a nonempty N-range | 3,887,930 (largest k 131) |
| pairs with no prime power > k in B | 0 |
| candidate N after pinning by qstar | 89,006,987 |
| survivors of all R3 congruences | 0 |
| lcm equalities | 0 |
| CPU time | 3.94 s |

**Further runs:**

- **Determinism:** a rerun (PID 17448) gave identical output, apart from the CPU-time line.
- **Superset, m ≤ 2010878** (PID 17514): 19,752,957 pairs, 89,011,091 candidates, 0 survivors, 0 equalities.
- **Weaker pruning,** so that the exact comparison runs on many disjoint candidates
  (../panel_work/reproduce/mycheck_depth.c):
  - DEPTH=2, using only the two largest prime powers (PID 17994): 10,557,495 exact comparisons, 0 equalities, 15.2 CPU s.
  - DEPTH=1, using only qstar (PID 18384): all 89,006,987 candidates compared exactly, 0 equalities, 41.4 CPU s.

My exhaustive check covers the whole of T, not a sample, and finds no counterexample. With Step 0 and S0–S2, this
confirms the claim for every k ≥ 1, every 0 ≤ n ≤ 5871k and every m ≥ n + k, given [RS62] and [Sch76].

## 4. The author's program

**The run.** I ran REPRODUCE.md with claim/ as the working directory and the exact command
`python3 -I object/range_nCk.py 5871`. The interpreter was the system Python 3.13.16, wrapped in
`nice -n 15 timeout 3000` (python PID 15231, under timeout 15229). I sent stdout to
../panel_work/reproduce/my_range_nCk_C5871.txt instead of into claim/, so that the package was not modified. Result:
exit 0, 133.8 s wall time, empty stderr.

**Byte comparison.**

- `cmp` with object/out/range_nCk_C5871.txt: **IDENTICAL**.
- Both files are 672 bytes, with sha256 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14, as listed in
  CLAIM.md.
- The last line is `RESULT: no counterexample with n <= 5871 k`.

**Reading object/range_nCk.py against PROOF.md:**

- **Sieve.** It sieves to 2,100,000 and finds 155,805 primes. I get π(2100000) = 155805 independently.
- **Blocks.** M1 = min(int(16594.272·147)+1, 2010760) = 2010760. It loops over consecutive primes a < b with
  a ≤ 2010760, taking m ∈ [a, b−3] and k ∈ [1, b−1−m].
  - Every element m+1..m+k then lies strictly between consecutive primes. So these are exactly the prime-free blocks,
    and every m ≤ 2010878 is reached.
  - The k = 1 element is factored (for Q, P1 and P2) and then skipped.
- **Pinning quantities.** Q = max p^(v_p(b)). P1 > P2 are the two largest distinct primes dividing elements of B (I
  checked the update logic); they are kept only if > k.
- **(b)** `m + k > c_big*k`, with c_big = 2.826·5872 as a double. It discards only pairs with
  m + k > 16594.27k > 16593.74k ≥ c_k·5872k, and those cannot hold a counterexample. Safe.
- **(c)** lo = max(Q, k, int((m+k)/(c_k·(1+1e-9))) − 1) and hi = min(m, 5872k). c_k is computed in double precision
  with relative error around 1e-15. The 1e-9 inflation, the truncation and the −1 keep lo strictly below the exact E1
  bound, so the candidate set is a superset. Safe.
- **(d)** The windows j·Pa … j·Pa + k − 1 start at j = max(1, ⌊(lo−k+1)/Pa⌋), which is never above the first useful
  window, and are then filtered by N mod Pb < k. Complete.
- **(e), (f)** The exact integer test k(m+k)^k ≤ lcm(1..k)·N^k comes first, then the exact big-integer lcm equality.
- No candidate is dropped except by one of these proven reasons.
- **Determinism.** There is no randomness, and set and dict use does not affect stdout.
- **Cosmetic only.** The docstring mentions "NOTES.md, Theorem S" (not in the package) and "C = 1000 by default".
  Neither affects the run.

**Counts compared with mine:**

- **Pairs passing (b).** I counted prime-free pairs satisfying (b) as an exact rational test,
  1000(m+k) ≤ 16594272k (../panel_work/reproduce/counts.c). The count is 1,449,175 with max k 147, whether m is
  capped at 2010759, 2010760 or 2010878. The author reports 1449175 (max k 147).
- **Independent C re-implementation** of the procedure in PROOF.md S3 (../panel_work/reproduce/replicate.c,
  PID 16484). It uses the same double formula for the float lower bound, and exact E1 in long double with a 1e-9 tie
  flag. All of these equal the author's figures:

  | quantity | value |
  |---|---|
  | pairs | 1,449,175 |
  | pairs with no prime > k | 0 |
  | candidates | 7,567,449 |
  | E1-passing (= full lcm comparisons) | 7,567,420 |
  | tie flags | 0 |

- **Not comparable.** My own checker's counts come from a different pruning (no size bound). Its 0 equalities agree
  with the author's 0.

## 5. Edge cases (checker/check677.py, arguments n m k)

| n m k | M(n,k) | M(m,k) | judge |
|---|---|---|---|
| 0 1 1 | 1 | 2 | FAIL (lcms differ) |
| 0 5 5 | 60 | 2520 | FAIL (differ) |
| 0 147 147 | 62 digits | 130 digits | FAIL (differ) |
| 2 3 3 | 60 | 60 | FAIL: "blocks overlap: m < n + k" (equal lcms, excluded by the statement) |
| 0 1 11 | 27720 | 27720 | FAIL: overlap (equal lcms, excluded) |
| 3 4 4 | 420 | 840 | FAIL: overlap, and the lcms differ |
| 5 6 1 | 6 | 7 | FAIL (differ) |
| 11742 11744 2 (n = 5871k, m = n + k) | 137909792 | 137956770 | FAIL (differ) |
| 587100 2010733 100 | 446 digits | 502 digits | FAIL (differ) |
| 0 2010733 147 | 62 digits | 705 digits | FAIL (differ) |
| 1 2 0 | 1 | 1 | FAIL: "k must be > 0" |
| 4 13 3 --allow-different-length 2 | 210 | 210 | PASS (Erdős's different-length example) |
| 3 19 4 --allow-different-length 2 | 420 | 420 | PASS (Erdős's different-length example) |

Equal lcms on overlapping blocks do exist (5004 in my small overlap test), and the statement and the judge correctly
exclude them. No coincidence between disjoint blocks was found anywhere.

## 6. Mismatches and gaps

- **No mismatch.** The output is byte-identical. All of the author's reported statistics were reproduced
  independently. My own exhaustive check of the whole finite set finds no counterexample.
- **Gap (not a failure).** I could not re-read [RS62] or [Sch76] in this session (proxy 403 on both fetches, not
  retried). The statements above are from my own knowledge. The numerical checks agree with them, but cannot verify
  [RS62] for all x, or [Sch76] beyond 10^9.
- **Deviation from REPRODUCE.md.** I wrote the output to scratch instead of inside claim/. The command, interpreter,
  flags, argument and working directory were exactly as given.
- **Note for the criterion skeptic.** The saved output is a summary log that a rerun reproduces, not a per-case
  certificate.
- **Process notes.**
  - A PID file I created landed briefly in the workspace root because I backgrounded a whole `cd && …` chain. I
    removed it immediately.
  - One wrapper attempt (PID 15051) exited 127 because /usr/bin/time is absent, so nothing ran.
  - At most two of my processes ran at any time, and none is still running.

pass: true
