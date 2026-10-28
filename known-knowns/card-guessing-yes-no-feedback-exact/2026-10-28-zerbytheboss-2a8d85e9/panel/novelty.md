# Novelty Skeptic Report — `card-guessing-yes-no-feedback-exact`

context: subagent (fresh invocation)
target_id: card-guessing-yes-no-feedback-exact
review_utc: 2026-10-28T18:45:00Z

## Novelty & Prior Art Audit

1. **Status Source and Literature Verification**:
   - Status source: `https://export.arxiv.org/api/query?search_query=abs:%22card%20guessing%22&sortBy=submittedDate&sortOrder=descending&max_results=50`, fetched and saved in `data/arxiv_card_guessing.xml`.
   - Diaconis, Graham, and Spiro (2022, arXiv:2012.04019) computed optimal play numerically up to $n = 10$, where table generation was halted due to state space growth.
   - S. Luo ("On card guessing games with yes/no feedback", arXiv:2609.25062, 14 Sep 2026) developed the inclusion-exclusion formula $C(r, f)$ and proved global bounds, leaving the exact values for $n \ge 11$ and the existence/value of $\lim_{n \to \infty} P^+_{2,n}$ as an open question (Question 5.1).
   - Prior to this run, no exact reduced rational or Bellman policy certificate was published for any $n \ge 11$.

2. **Benchmarking against Incumbent Records**:
   - Incumbent published frontier was $n = 10$ ($P^+_{2,10} \approx 3.0186$, exact: $170757866939041 / 56568592080000$).
   - This submission provides exact reduced rationals for every $n$ from 11 through 16, advancing the solved frontier by 6 full levels.
   - For $n = 16$, the denominator contains 29 digits, evaluated across 18,623,134 canonical states.

3. **Repository and PR Check**:
   - Inspected `repo/TROPHY_CASE.md`: no prior entry exists for `card-guessing-yes-no-feedback-exact`.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero competing pull requests claim this target.
   - The computed exact values for $n = 11..16$ constitute a new, uncontested mathematical milestone.

pass: true
