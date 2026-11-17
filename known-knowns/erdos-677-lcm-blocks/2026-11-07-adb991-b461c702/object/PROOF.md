# Proof: no counterexample to Erdős 677 with 26 ≤ k ≤ 28 and n ≤ 10^494

Notation: M(x, k) = lcm(x+1, …, x+k); f(x) = (x+1)(x+2)…(x+k); R(k) = lcm(1..k)/k.

**Claim.** For every k with 26 ≤ k ≤ 28, every n with 0 ≤ n ≤ 10^494, and every m ≥ n + k (no cap on m):
M(m, k) ≠ M(n, k).

Here the range is K = {26, 27, 28}; in the text below, "k ≤ K*" is to be read as "k ∈ K" (the same proof was used for
k ≤ 25 in an earlier, separately confirmed claim). Each step is
labelled PROVED-HERE (an argument in this file), COMPUTED (a deterministic program whose saved output is in object/),
or KNOWN (a cited standard fact).

## Step 1. Lemma A (PROVED-HERE)

**Statement.** Let 0 ≤ n < m, k ≥ 1, and M(n, k) = M(m, k) = L. Then

  f(m)/f(n) = r = ∏_{p<k} p^{d_p},  where d_p = Σ_{i ≥ 1, p^i < k} (c_{p^i}(m) − c_{p^i}(n)).

Here c_q(x) = #{1 ≤ j ≤ k : q | x + j}. Each summand lies in {−1, 0, 1}, and it is 0 when p^i | k. Moreover
1 < r ≤ R(k).

**Proof.**
1. Every element of either block divides L. So for every prime p, v_p(f(x)) = Σ_{i=1}^{v_p(L)} c_{p^i}(x) for x = n, m,
   since every element's p-adic valuation is at most v_p(L).
2. Take p^i ≥ k with i ≤ v_p(L).
   - Each block contains at least one multiple of p^i: some element attains v_p = v_p(L) ≥ i, because L is the lcm of
     the block.
   - Each block contains at most one multiple of p^i: two multiples differ by at least p^i ≥ k, but block elements
     differ by at most k − 1.
   - So c_{p^i}(m) = c_{p^i}(n) = 1.
   - In particular, every prime p ≥ k contributes v_p(f(m)) = v_p(f(n)).
3. Take p^i < k. Among k consecutive integers, c_{p^i} ∈ {⌊k/p^i⌋, ⌊k/p^i⌋ + 1}, and c_{p^i} = k/p^i exactly when
   p^i | k. Also i ≤ v_p(L) automatically: the block contains a multiple of p^i because k > p^i, so p^i | L.
4. Combining steps 1–3, f(m)/f(n) = ∏_{p<k} p^{d_p}, with the stated d_p.
5. The bound r ≤ R(k).
   - r ≤ ∏_{p<k} p^{#{i : p^i < k, p^i ∤ k}}.
   - v_p(lcm(1..k)) = #{i ≥ 1 : p^i ≤ k}, and v_p(k) = #{i ≥ 1 : p^i | k}.
   - The levels with p^i ∤ k are exactly those with p^i ≤ k and p^i ∤ k. Since p^i = k implies p^i | k, these are the
     levels with p^i < k and p^i ∤ k. Their number is v_p(lcm(1..k)) − v_p(k), so the product equals lcm(1..k)/k.
6. r > 1 because m > n implies f(m) > f(n). ∎

**Consequences.**
- (a) k ≤ 2: R(1) = R(2) = 1, so no r with 1 < r ≤ R(k) exists. Hence M(m, k) ≠ M(n, k) for all n < m, in particular
  for all m ≥ n + k.
- (b) Window. For j ≤ k, (m+j)/(n+j) ≥ (m+k)/(n+k). Hence ((m+k)/(n+k))^k ≤ r ≤ R(k), so
  m + k ≤ (n+k)·R(k)^{1/k}.
- (c) The m-block is prime-free. A prime P in (m, m+k] would divide L and hence some element of the n-block, which is
  impossible: n + k ≤ m < P.

## Step 2. Small X: n + k ≤ 1.1·10^6, every k (COMPUTED)

`object/search677b.c`, run as `search677b 1100000 20261106` (output `object/out/search_N1.1e6.txt`).

- For every k and n with n + k ≤ 1.1·10^6, it lists every m with n + k ≤ m and m + k ≤ (n+k)·R(k)^{1/k} + slack,
  whose m-block is prime-free, and for which a 64-bit additive hash of the (≥ k)-prime part of f equals that of n.
- Only 3 ≤ k ≤ 147 can occur, because a prime-free block of length k below 3.3·10^6 needs k < 148 (the sieve's
  largest prime gap, printed as K=147).
- By Lemma A (b), (c) and step 2 of its proof, every counterexample in this range is listed. Hash collisions can only
  add pairs.
- Every listed pair is then compared exactly (`object/verify_cands.py`, output `object/out/verify_N1.1e6.txt`): there
  are 2 pairs, (k, n, m) = (3, 4, 13) and (4, 18, 53), and neither has equal lcm.

This covers every (n, k) with X := n + (k+1)/2 < 10^6 and k ≤ K*, because then n + k < 10^6 + (k−1)/2 ≤ 1.1·10^6.

## Step 3. The curves (PROVED-HERE + COMPUTED)

By Lemma A, a counterexample with 3 ≤ k ≤ K* satisfies f(m) = r·f(n) for some r in

  A_k = {∏_{p<k} p^{d_p} : |d_p| ≤ #{i : p^i < k, p^i ∤ k}, 1 < r ≤ R(k)}.

`deep_cf.admissible_r(k)` lists exactly this set; the rigor-margin lens audited its completeness (see CLAIM.md).

Put X = n + (k+1)/2, Y = m + (k+1)/2, and F(Z) = ∏_{j=1}^{k} (Z + j − (k+1)/2). Then f(n) = F(X), f(m) = F(Y), and
F(Y) = r·F(X). All roots of F are ≤ (k−1)/2, so F is increasing on ((k−1)/2, ∞). Given X, Y is therefore the unique
real solution there.

## Step 4. Margin (COMPUTED, rigorous arithmetic)

Let ρ = r^{1/k} and c = (k²−1)(ρ²−1)/(24ρ). For every r ∈ A_k, every k ≤ K* and every real X ≥ 10^6:

  c(1 − 10^−3) < X(ρX − Y(X)) < c(1 + 10^−3).

This reduces to the positivity on [10^6, ∞) of two explicit polynomials in X. The rigor-margin lens proves it with
rigorous arithmetic (method and output named in CLAIM.md), with 0 failures and 0 undecided cases.

## Step 5. Complete enumeration (COMPUTED + PROVED-HERE)

Put (p, q) = (Y, X) for odd k and (2Y, 2X) for even k. Both are integers. Let S = 1 for odd k and S = 4 for even k.
Step 4 gives

  L := S·c(1−η) < q(qρ − p) < S·c(1+η) =: U.

**The enumeration.** `object/deep_rig.py` lists every integer pair (p, q) with 1 ≤ q ≤ 10^495, qρ − p > 0 and
q(qρ − p) < U. Let p_j/q_j be the convergents of ρ, computed exactly from integer k-th roots in `deep_cf.cf_of_root`.

1. For q_i ≤ q < q_{i+1}, write (p, q) = r'(p_{i+1}, q_{i+1}) + s(p_i, q_i). The basis is unimodular, so r' and s are
   integers.
2. r' = 0 gives multiples of a convergent.
3. For r' ≠ 0, r' and s have opposite signs, and q·|qρ − p| ≥ q_i·|s|·|d_i| with d_i = q_iρ − p_i. Together with
   q < q_{i+1}, this gives |r'| ≤ 2U + 1.
4. For each (i, r'), the admissible real s form an interval cut out by a quadratic inequality. The program generates
   every integer s in that interval, widened by 2 on each side, and re-checks each pair in 1090-digit arithmetic.
5. A double-precision pre-filter on g = q(qρ − p) is applied only with a relative tolerance of 10^−6. It is computed
   either from the exact integer q, or from float values whose relative error is provably below 10^−9 (CLAIM.md, patch
   note).
6. The enumeration was validated against brute force for q ≤ 4000 on all curves with k ≤ 12 (run 2026-10-15).

**Covering n.** n ≤ 10^494 implies q ≤ 10^495: for odd k, q = n + (k+1)/2; for even k, q = 2n + k + 1.

**Final test.** Each enumerated pair with q(qρ − p) > L, the right parity and X ≥ 10^6 is mapped back to (n, m) and
tested exactly: f(m)·b = a·f(n), where r = a/b. Output: `product_solutions = 0` for every k ≤ K*
(`object/out/deep_rig_shard0.txt` … `shard3.txt`, run through `object/shard_rig.py`).

## Conclusion

Take k ≤ K*, n ≤ 10^494 and m ≥ n + k, and suppose M(m, k) = M(n, k).

- k ≤ 2 is impossible by Lemma A (a).
- For k ≥ 3, f(m) = r f(n) with r ∈ A_k (step 3).
- If X < 10^6, step 2 excludes it.
- If X ≥ 10^6, step 4 puts (p, q) in the enumerated set, and step 5 finds no product solution.

Contradiction. ∎
