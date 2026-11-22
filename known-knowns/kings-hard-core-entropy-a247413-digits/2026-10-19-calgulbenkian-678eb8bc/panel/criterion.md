# Criterion report, cell kings-a247413-d33

context: Claude Code subagent, fresh context

Read only the package folder. Claim hashes checked against the contributor's hash list (no mismatch). One live fetch, made once with the honest curl client and logged (the log is not shipped in this package): the OEIS A247413 json search, 2026-10-19T01:45Z (UTC), HTTP 200, sha256 12c0e725...da40ef8 (identical to the author's hash), DATA = 1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9 = 18 terms, revision 30. So the bar is D >= 22; the claim's D = 33 clears it.

Own recount (small script, from the saved tables, not the author's checker):
- Method A, chi = 70, 80, 90, 100: 36 common decimals; chi = 80, 90, 100: 38.
- Method B, windows of four successive mmax ending at 34..40: 27, 28, 29, 30, 31, 32, 33 common decimals. Window 37..40 = 33.
- A (chi = 100) vs B (E(40)): 35 common decimals. All of A70..A100 and B37..B40 together: 33.

Clause by clause
- D >= terms + 4: met (33 >= 22, term count re-confirmed live).
- (a) two independent methods agree on all D decimals: met. A is a site corner transfer matrix (iterative fixed point, bond dimension chi); B is exact open-strip transfer-matrix eigenvalues (widths 2..40) with Wynn epsilon extrapolation; different algorithms, different code (tm.c, tmlean.c, prereg_b.py versus ctmgen2.py). The file states no CTM value feeds B. The criterion's own example names exactly this pair. Both share only the author and the definition. Method C shares code with A and is correctly not counted. A and B agree to 35 decimals, above 33.
- (b) both reproduce the 18 published digits (1.34264395112460129): met; the first 17 decimals match in both (verified in the tables).
- (c) stable over at least three increases of the truncation parameter, read literally for each method: met. A: four values chi = 70..100 share 36 decimals. B: four values mmax = 37..40 share 33 decimals. D = 33 is the smaller. B's agreement grows steadily with mmax, one decimal per width, not by accident.
- (d) literature/OEIS search finds no published value with D or more decimals: cannot be fully decided from the folder. The record shows the OEIS entry has 18 terms, an OEIS search for 21 terms gave no results, and Liang's bracket has 21 decimals and contains the value. The author states no general web search was made. The novelty skeptic owns this clause; nothing in the folder contradicts it.

Hidden quantifiers and stretched definitions
- B's start width m0 = 3 was chosen after seeing widths up to 28 (disclosed in PREREG_B.md); widths 29..40 are new data under the unchanged recipe, and the first blind run (m0 = 4) already gave 21 stable decimals. Widths 35..40 were added after the stated target of 34, by the same recipe. A slight forking-path concern, but the headline is corroborated by A independently (A and B agree on 35 decimals), so it does not change the 33.
- B's stability is a sequence-extrapolation convergence, not a bound. A's is a fixed-point convergence of truncated iterations with a float64 SVD subspace choice. There is no rigorous error bound, which the claim discloses. The criterion asks for agreement and stability, not a proof.
- Null check: the 4-value window of B has decimal 34 equal to 2 at mmax = 37 and 3 at 38..40, so 33 is the true common count and not padded; truncation and rounding agree at 33 (next digits 39 in both).
- The Argon attempt was not read or used.

Limits: numerical agreement across two methods, not a rigorous error bound; clause (d) rests on a limited search.

confirmed_scope: The A247413 constant (Lambda = e^kappa, independent sets of the king graph) is 1.342643951124601297851730161875740 to 33 decimals, the digits agreeing between the site corner transfer matrix (36 decimals stable over chi = 70..100) and open-strip transfer matrices with Wynn extrapolation (33 decimals stable over mmax = 37..40), as numerical agreement and not a rigorous error bound, and subject to the novelty skeptic's verdict on clause (d).

pass: true
