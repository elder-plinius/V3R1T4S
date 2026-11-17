# Proof: no counterexample to Erdős 677 with n ≤ 5871·k

## Notation

- k ≥ 1, n ≥ 0, m ≥ n + k (integers), N = n + k.
- A = {n+1, …, N} and B = {m+1, …, m+k}.
- M(n, k) = lcm(A). This is `lcmInterval n k = (Finset.Ioc n (n + k)).lcm id` on ℕ (checker/spec_677.lean).
- For a finite set X of positive integers, D(X) = ∏X / lcm(X).
- A **counterexample** is a triple (n, m, k) with these constraints and lcm(B) = lcm(A) =: L.
- ψ is Chebyshev's function. lcm(1, …, k) = e^{ψ(k)}.

**Theorem.** Every counterexample has n > 5871·k. Equivalently, for every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every
m ≥ n + k: M(m, k) ≠ M(n, k).

## Step 0: k = 1

Here lcm(B) = m + 1 > n + 1 = lcm(A). From now on, k ≥ 2.

## Step S0: prime powers and large primes in B

Let b ∈ B. Then b | L.

1. **Prime powers in B are at most N.** Let p^e | b with p prime and e ≥ 1. Then p^e | L = lcm(A). Since
   v_p(L) = max_{a∈A} v_p(a), p^e divides some a ∈ A, so p^e ≤ N.
2. **B contains no prime.** Every b ∈ B satisfies b ≥ m + 1 ≥ N + 1 > N. By point 1, b is not a prime power; in
   particular b is not prime. Equivalently, the interval (m, m+k] contains no prime.
3. **Large primes pin N.** Let P > k be a prime dividing some b ∈ B. Then P | L, so P divides some element of A.
   A = (N − k, N] consists of k consecutive integers, so it contains a multiple of P exactly when N mod P ≤ k − 1.
   Hence N mod P < k.

## Step S1: the size bound

Let X be a block of k consecutive positive integers and p a prime. Put c_e = #{x ∈ X : p^e | x} for e ≥ 1.

Then v_p(∏X) = Σ_{e≥1} c_e. Since c_e is non-increasing in e, v_p(lcm X) = #{e ≥ 1 : c_e ≥ 1}. Hence

  v_p(D(X)) = Σ_{e≥1} (c_e − 1)^+.

A block of k consecutive integers contains either ⌊k/p^e⌋ or ⌈k/p^e⌉ multiples of p^e. So
c_e ∈ {⌊k/p^e⌋, ⌈k/p^e⌉}, which gives two bounds.

- **Upper bound.** (c_e − 1)^+ ≤ ⌈k/p^e⌉ − 1 = ⌊(k−1)/p^e⌋. Summing over e gives v_p(D(X)) ≤ v_p((k−1)!).
- **Lower bound.**
  - If p^e ≤ k, then c_e ≥ ⌊k/p^e⌋ ≥ 1, so (c_e − 1)^+ ≥ ⌊k/p^e⌋ − 1.
  - If p^e > k, then (c_e − 1)^+ ≥ 0 = ⌊k/p^e⌋.
  - Summing over e gives v_p(D(X)) ≥ v_p(k!) − #{e ≥ 1 : p^e ≤ k} = v_p(k!) − v_p(lcm(1, …, k)).

Therefore, for every such block X,

  k!/lcm(1, …, k) ≤ D(X) ≤ (k − 1)!.

For a counterexample, ∏B = D(B)·L and ∏A = D(A)·L. So

  ∏B/∏A = D(B)/D(A) ≤ (k − 1)!·lcm(1, …, k)/k! = lcm(1, …, k)/k.

Since m ≥ n, the ratio (m+i)/(n+i) is non-increasing in i ≥ 1. Hence ∏B/∏A ≥ ((m+k)/N)^k, and so

  (E1)  k·(m + k)^k ≤ lcm(1, …, k)·N^k,

in particular m + k ≤ c_k·N with c_k = (lcm(1, …, k)/k)^{1/k}.

By Rosser–Schoenfeld [RS62], ψ(x) < 1.03883·x for every x > 0. So lcm(1, …, k) < e^{1.03883·k}, and

  c_k < e^{1.03883} = 2.82591… < 2.8260   for every k ≥ 1.

## Step S2: the Schoenfeld step

Assume n ≤ 5871·k. Then N ≤ 5872·k, and by S1,

  m + k < 2.8260·5872·k < 16594.3·k,

so k > m/16593.3.

Schoenfeld [Sch76]: for every real x > 2010759.9 there is a prime p with x < p < x·(1 + 1/16597).

Suppose m ≥ 2010760. Take x = m and such a prime p. By S0, (m, m+k] contains no prime, so p > m + k, and
therefore k < m/16597. This contradicts k > m/16593.3. Hence m ≤ 2010759.

## Step S3: the finite enumeration

By S0–S2, every counterexample with k ≥ 2 and n ≤ 5871·k satisfies all of the following.

- (a) m ≤ 2010759, and the block (m, m+k] contains no prime (S0, S2).
- (b) m + k ≤ 2.8260·5872·k (S1 with N ≤ 5872·k).
- (c) max(Q, k, (m+k)/c_k) ≤ N ≤ min(m, 5872·k), where Q is the largest prime power dividing an element of B:
  - N ≥ Q by S0;
  - N ≥ k because n ≥ 0;
  - N ≥ (m+k)/c_k by S1;
  - N ≤ m because m ≥ n + k;
  - N ≤ 5872·k by assumption.
- (d) N mod P < k for each prime P > k that divides an element of B (S0). The program uses this for the two largest
  such primes.
- (e) (E1) holds.
- (f) lcm(n+1, …, N) = lcm(m+1, …, m+k).

### What object/range_nCk.py (run with argument 5871) does

1. It sieves the primes up to 2,100,000.
2. For every pair of consecutive primes a < b with a ≤ 2010760, it visits every m with a ≤ m ≤ b − 3 and every k
   with 2 ≤ k ≤ b − 1 − m. These are exactly the prime-free blocks (m, m+k] with k ≥ 2 whose largest prime ≤ m is a.
   Every m ≤ 2010760 is reached, because the largest prime ≤ m is then ≤ 2010760.
3. It discards the (m, k) violating (b).
4. It lists the N allowed by (c) and by (d) for the two largest primes P1 > P2 that divide elements of B and exceed
   k.
5. For each candidate N, it tests (e) exactly in integers, then (f) by exact big-integer lcm.

### Floating point

Floating point appears only in two places, and both only loosen the filters:

- The lower bound (m+k)/c_k in (c) is computed with c_k·(1 + 10^-9), truncated, and then reduced by 1. The
  candidate set is therefore a superset.
- The constant 2.8260·5872 in (b) exceeds the true bound c_k·5872, since c_k ≤ 2.82591.

Test (e) is exact.

### Output (object/out/range_nCk_C5871.txt)

- 1449175 prime-free pairs (m, k) were examined (largest k: 147).
- 7567449 candidate N were produced, and 7567420 exact lcm comparisons were made.
- No triple satisfies (f).

The program also checks numerically that no gap between consecutive primes in (2010760, 2099800) violates the
Schoenfeld statement. That check is a sanity check of the citation, not a step of the proof.

Steps 0–S3 cover every k ≥ 1, every 0 ≤ n ≤ 5871·k and every m ≥ n + k, with no cap on m. ∎

## References (KNOWN results used)

- [RS62] J. B. Rosser and L. Schoenfeld, "Approximate formulas for some functions of prime numbers", Illinois J. Math.
  6 (1962), 64–94: ψ(x) < 1.03883·x for x > 0.
- [Sch76] L. Schoenfeld, "Sharper bounds for the Chebyshev functions θ(x) and ψ(x). II", Math. Comp. 30 (1976),
  337–360: for x > 2010759.9 there is a prime p with x < p < x·(1 + 1/16597).
