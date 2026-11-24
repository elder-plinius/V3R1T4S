# Run it yourself

Fresh shell, from this package folder. Needs python3 (>= 3.9), a C compiler (cc), and pip access once
(run_checks.sh installs python-flint==0.9.0 into verify-it-yourself/.venv unless python3 already has that version).

```sh
sh verify-it-yourself/run_checks.sh      # about 20 s on 6 cores; last line: PASS
```

What it does (real output in verify-it-yourself/RECEIPTS.md):
0. Compiles verify-it-yourself/vcount.c, a segmented odd-only sieve written from the definition. For each requested n it
   outputs S(n) = sum over odd squarefree m <= n of floor(2^64 / prod_{p|m}(p-2)), an exact integer with S(n)/2^64 <= V(n),
   and M(n) = #{odd squarefree m <= n}. These are checked against pure Python at 2859 points n <= 20000.
1. Reads object/a_bound_certificate.json: for each of the 9906 intervals, the sieve parameter z_i (an exact double, or
   z_i = exp(t_i) with t_i an exact double when z_i > 1e12) and the stated sup of that interval's term. Checks
   1 <= z_i < m_i^(1/4).
2. Re-evaluates each term 2*(c1/V(z_i) + c_pi(m_i; z_i) c2 r(z_i)^2) in arb at 128 bits and requires the stated value to
   agree to 1e-18 relative. The total uses the recomputed sups.
3. Recomputes the V-lemma constant A(1e10) <= 0.0107001 (Rankin bound at s = 0.44, exact product over odd primes <= 1e7).
4. Adds the tail 32*0.6601619/log(10^2000) + 8/10^1000, the head 1.840518 - 2*pi_2(4e18)/4e18 and the pi_2(z) correction
   2*sum z_i/m_i, then checks the total < 2.156967.

The formulas are in object/proof.md. The checker evaluates them but does not prove them.

To rebuild the object with the contributor's code (tables, replay, certificate), see how-we-built-it/COMMANDS.md.
