# Run it yourself

Fresh shell, from this package folder. Needs python3 (>= 3.9), a C compiler (cc), and pip access once
(run_checks.sh installs python-flint==0.9.0 into verify-it-yourself/.venv unless python3 already has that version).

```sh
sh verify-it-yourself/run_checks.sh      # about 70 s on 8 cores (both precisions); last line: PASS
```

What it does (real output in verify-it-yourself/RECEIPTS.md). The whole check runs twice, at 128 and at 256 bits,
and PASS needs both:
0. Compiles verify-it-yourself/wvcount.c, a segmented odd-only sieve written from the definition. For each requested n
   it outputs exact integers S(n) = sum over odd squarefree m <= n of floor(2^64 / prod_{p|m}(p-2)) (so S/2^64 <= V(n)),
   M(n) = #{odd squarefree m <= n}, and SW(n) = sum of ceil(2^40 * prod_{p|m} p/(p-2)) (so SW/2^40 >= W(n)).
   These are checked against pure Python at 2859 points n <= 20000.
1. Reads object/a_bound_certificate.json: for each of the 9906 intervals, the sieve parameter z_i (an exact double, or
   z_i = exp(t_i) with t_i an exact double when z_i > 1e12) and the stated sup of that interval's term. Checks
   1 <= z_i < m_i^(1/4).
2. Re-evaluates each term 2*(c1/V(z_i) + c_pi(m_i; z_i) c2 Lambda(z_i)^2) + 2 z_i/m_i in arb, with Lambda(z) <= W(z)/V(z)
   (exact up to 1e10; beyond that the W lemma z/(2*0.6601618) + z^s S'(s), minimised over 9 values of s, with S'(s)
   recomputed). The stated value must be >= the recomputed sup (to 1e-15 relative) and at most 1e-5 above it.
   The total uses the recomputed sups.
3. Recomputes the V-lemma constant A(1e10) <= 0.0107001 (Rankin bound at s = 0.44, exact product over odd primes <= 1e7).
4. Adds the tail 32*0.6601619/log(10^2000) + 8/10^1000 and the head 1.840518 - 2*pi_2(4e18)/4e18, then checks the
   total < 2.126988.

The certificate fields `B_upper_without_pi2z` and `note` are stale labels (the terms do include 2 z_i/m_i); the
checker does not read them. See how-we-built-it/CLAIM_CHANGES.md (d).

The formulas are in object/proof.md. The checker evaluates them but does not prove them.

To rebuild the object with the contributor's code (tables, certificate), see how-we-built-it/COMMANDS.md.
