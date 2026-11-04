# Novelty Skeptic Report — `coin-basket-random-expected-values`

target_id: coin-basket-random-expected-values
review_utc: 2026-10-28T00:46:00Z

## Novelty & Prior Art Audit

1. **Status Source Verification**:
   - Status source URL: `https://oeis.org/A391791`
   - Secondary source: `https://oeis.org/A391792`
   - Fetched: 2026-10-28T00:31:50Z (HTTP 200, SHA256 `f4ca4c77d1c41c96dab40e5f51e2756147aba06cdbd83067bfd5e1d807f79b59`)
   - OEIS A391791 lists terms $n=1..22$, ending with $A391791(22) = 405700861$.
   - OEIS A391792 lists terms $n=1..18$, ending with $A391792(18) = 13615817865$.
   - Neither the OEIS sequence entries, their official b-files (`b391791.txt`, `b391792.txt`), nor their edit histories contain the terms $n \ge 23$ for A391791 or $n \ge 19$ for A391792.

2. **Literature & Repository Audit**:
   - `repo/TROPHY_CASE.md` contains zero prior claims for `coin-basket-random-expected-values`.
   - GitHub open pull requests and branches across the repository contain zero competing claims for this target.
   - The reference Julia program by Ruediger Jehn (`a391791_1.jl.txt`) computes the published terms up to $n=22$ for A391791 and $n=18$ for A391792.

3. **Strict Novelty Assessment**:
   - The claimed terms strictly exceed all known records:
     - A391791: 3 new terms ($n=23, 24, 25$)
     - A391792: 3 new terms ($n=19, 20, 21$)
   - Jehn's conjecture (stating that for $n > 9$ the optimal first move is coin $\lfloor (n+3)/2 \rfloor$) is confirmed by exact computation for n = 10..25.
   - This submission strictly beats everything known in the public record.

pass: true
