context: Claude Code subagent, fresh context [Sonnet 5.5]

# Reproduce report, erdos-7-odd-covering-system, partial win p2 (L >= 168,131,152,814,625)

No downloads or fetches were made.

## 1. The lemma chain (README.md, re-derived by me)
Let B0 = 168,131,152,814,624. A hypothetical odd distinct-moduli covering with L <= B0 is turned into a contradiction in five steps.
- L1 (prime replacement, Berger-Felzenbaum-Fraenkel style). Map the primes of L onto the first r odd primes with the same exponents, using the base-p digit embedding. The covering pulls back to a covering of Z/L*Z, L* <= L, with distinct moduli dividing L* and sigma(L*) >= 2L*. I re-derived this and found it sound. Digits of a fixed class are the low digits, and a class with a digit >= p_m pulls back to the empty set. Distinct exponent vectors stay distinct. No use of Hough-Nielsen is needed, since 3 is the first prime.
- L2 (3-band scaling). Multiply L* by 3^k, largest k with N <= B0, so N is in (B0/3, B0]. The same congruences cover Z/N, and N is still abundant. Sound.
- L3 (pure prime-power completion). Disjoint pure classes mod p^t can always be chosen, because (p^t-p)/(p-1) < p^t. Replaced classes lie inside earlier pure classes, so nothing is uncovered. Sound.
- L4(1) (pure-deletion sum) and L4(2) plus L5 (capped fibre kernels, comonotone/convex comparison with the hinge). I re-derived the identity (1 - C u(G))_+ <= C(rho + sum p^-t N_t - delta)_+, the nested conditional use of Lemma 5, and the count prod(1+T_m) - 1. I found them sound. Multiple classes of equal depth are fine, since Lemma 5 only needs P(E_j) <= alpha_j.

Coverage of every L <= B0: it does not rely on listed L values. Every L <= B0 maps to an abundant initial-prime profile L*, then to its band profile N. The certificate only has to refute every abundant initial-prime N in (B0/3, B0].

## 2. My own exact checker (written from README definitions before reading package code; Fraction arithmetic)
- I enumerated all initial-prime profiles (exponents >= 1 on the first r odd primes) with N <= B0. I got 30,598 profiles, of which 30,147 have sigma >= 2N. Matches the package.
- Band scaling gives exactly 7,036 distinct profiles. Every abundant profile with N > floor(B0/3) is among them. floor(B0/3) = 56,043,717,604,874.
- Pure-deletion value < 1 for exactly 2,519 of them (max 124651682101/124657827840). The other 4,517 profiles equal the certificate's rows, with no extras and no omissions.
- For each of the 4,517 rows I recomputed, from scratch, the L4(2) bound with theta, rho, lambda, the exact distribution of T_m and the hinge expectation. I checked the preconditions 1 <= k0 < r, 1 < C_i <= p_i and delta_i >= rho_i. Every bound is < 1 and equals the stated exact_upper_bound (0 mismatches). The maximum is 16615714572403899891/16710819340101877760.
- Arithmetic: 3^4*5^3*7^2*11^2*13*17*19*23*29 = 168131152814625 = B0+1. It is exactly 14637315 x 11486475 and 17325 x 9704539845.

## 3. Null and soundness tests
- Even null model. The classic covering of Z/12 with moduli 2,3,4,6,12 was verified to be a covering. The same pure-deletion sum for p=(2,3), e=(2,1) gives 3/2 >= 1, so the method correctly does not rule it out. For odd 945 = 3^3*5*7 the value is 157/336 < 1, so the method refutes it, consistent with the known 945 bound.
- Soundness of the measure inequality. On small odd N (shapes (1,1,1), (1,1,1,1), (2,1,1), (1,2,1), (1,1,2), (2,1,1,1), (3,1,1)), I built random adversarial F with a random Lemma-3 pure completion, all mixed divisors present, and the exact kernels of Lemma 4(2). For all k0 and cap choices tried, the exact mu(covered) was <= the formula bound. Some cases are tight, e.g. 0.125 = 0.125. No violation was found. This is a spot check of the lemma and not a proof, but the proof was also re-derived by hand above.

## 4. Package's own check
sh verify-it-yourself/run_checks.sh in a copy: both the C and Python verifiers print PASS and the final line is PASS (about 9 s). Counts agree with mine: 30147, 7036, 2519, 4517, min surplus 95104767697977869.

## Limits
Exhaustive (not sampled). Every one of the 7,036 band profiles was checked exactly. The proof is a research-level argument built from published methods. I verified each lemma by hand, but nothing is machine-checked in Lean, and p2 asks for a rigorous proof rechecked by independent code. Noted package limit: L = B0+1 itself is not excluded.

pass: true
