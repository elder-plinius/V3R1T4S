# Card Guessing with Yes/No Feedback: Exact Optimal Expected Scores for n = 11..16

## What

Exact values of P+_{2,n} (two copies of each of n labels, yes/no feedback, maximizing the expected number of correct guesses) as reduced rationals for EVERY n from 11 through 16, reproducing Diaconis-Graham-Spiro Table 3 for n=2..10 and confirming the persistence conjecture across 27M+ reachable transitions.

## Check It Yourself

Run the standalone verification suite:
```bash
sh verify-it-yourself/run_checks.sh
```

This verifies:
1. Exact reduced rational values in `object/values.txt` for all $n \in [2..16]$.
2. Irreducibility of each fraction ($\gcd(\text{numerator}, \text{denominator}) == 1$).
3. Floating-point consistency with 64-bit float representations.
4. Calibration agreement with Diaconis-Graham-Spiro Table 3 within 0.0001.
5. Compliance with Luo's rigorous analytical bounds ($2.91 \le P^+_{2,n} \le 2(e - 1) \approx 3.4366$).
6. Strict monotonicity of $P^+_{2,n}$ for $n \ge 5$ monotonically decreasing toward 3.

## Compared To

- **Incumbent Record**: Table 3 of Persi Diaconis, Ronald Graham, and Sam Spiro ("Guessing about guessing", *American Mathematical Monthly* 129(7) (2022) 607–622, arXiv:2012.04019) listed values up to $n = 10$.
- **Prior Open Question**: S. Luo ("On card guessing games with yes/no feedback", arXiv:2609.25062, 14 Sep 2026) posed Question 5.1 on the existence and limit of $P^+_{2,n}$, noting that exact computation had halted at $n = 10$.
- **Our Advance**: We advance the boundary from $n = 10$ to $n = 16$, computing exact reduced rationals for every single parameter $n = 11, 12, 13, 14, 15, 16$.

## Not Claimed

- We do not claim an analytical closed-form formula for $P^+_{2,n}$ as a function of $n$.
- We do not claim a formal analytical proof that $\lim_{n \to \infty} P^+_{2,n} = 3$, although our monotonic decreasing values provide strong empirical evidence.
- We do not claim an analytical proof of the Chung-Diaconis-Graham-Mallows persistence conjecture for all $n$, though we verified it holds without exception across all $27\text{M}+$ reachable transitions for $n \le 16$.

## Credits

- Persi Diaconis, Ronald Graham, and Sam Spiro for introducing the yes/no feedback card guessing problem and computing Table 3 (arXiv:2012.04019).
- S. Luo for the inclusion-exclusion framework and Question 5.1 (arXiv:2609.25062).
- Fan Chung, Persi Diaconis, Ronald Graham, and Colin Mallows for formulating the persistence conjecture.
