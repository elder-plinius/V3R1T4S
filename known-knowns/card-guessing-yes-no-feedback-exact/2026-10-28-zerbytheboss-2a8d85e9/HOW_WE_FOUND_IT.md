# How We Found It — `card-guessing-yes-no-feedback-exact`

contributor text, unverified

The problem of exact card guessing with yes/no feedback for two-copy decks (m = 2) was investigated following Diaconis, Graham, and Spiro (2022, arXiv:2012.04019), who provided numerical approximations up to n = 10, and S. Luo (2026, arXiv:2609.25062), who provided inclusion-exclusion formulas and open questions regarding asymptotic limits.

To scale the dynamic programming frontier from n = 10 to n = 16:
1. **Generating Polynomial Convolution**: Evaluating Luo's inclusion-exclusion formula C(r, f) directly via subsets requires O(3^n) operations. By representing the formula as the discrete convolution of individual label generating polynomials P_i(t) = 1 + f_i t (for r_i = 1) and P_i(t) = 1 + 2 f_i t + f_i(f_i - 1) t^2 (for r_i = 2), the count C(r, f) evaluates in O(n^2) operations (< 1 microsecond per state).
2. **Integer Bellman Dynamic Programming**: By clearing denominators C(s), the rational dynamic program transforms into an exact integer recursion W(s) = max_i [ C(s_{succ, i}) + W(s_{succ, i}) + W(s_{fail, i}) ]. This avoids rational arithmetic and GCD reductions during search, allowing millions of canonical multiset states to be evaluated in seconds.
3. **Clean-Room Dual Solvers**: We constructed two independent solvers: a high-throughput compiled Rust engine and a pure Python standard library solver. Both reproduce Diaconis-Graham-Spiro Table 3 for n = 2..10 within 0.00007, and agree bit-for-bit across all computed exact rationals for n = 11..16.
4. **Persistence Audit**: We screened all 27,118,527 reachable failure transitions across n <= 16, verifying that the Chung-Diaconis-Graham-Mallows persistence conjecture holds without exception.
