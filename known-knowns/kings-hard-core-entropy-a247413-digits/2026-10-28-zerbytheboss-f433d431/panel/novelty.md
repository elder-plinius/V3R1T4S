# Novelty Skeptic Report — `kings-hard-core-entropy-a247413-digits`

context: subagent (fresh invocation)
target_id: kings-hard-core-entropy-a247413-digits
review_utc: 2026-10-28T22:55:00Z

## Novelty & Literature Audit

1. **Live Status Verification**:
   - Status Source URL: `https://oeis.org/A247413`
   - Canonical Page SHA-256: `c1abba56516d1f3abdc2bddffcda5a2a7a1d7bf49942a953aed124ad861bcdf5` (HTTP 200, fetched 2026-10-28T22:26:00Z).
   - Text Data SHA-256: `a00c2171a759f4b3b082153c48332f74e0d27f1cf0e8d84714e2ceba3f82b3eb` (HTTP 200).
   - Live OEIS A247413 DATA records 26 digits: `1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9,7,8,5,1,7,3,0,1` (updated October 18, 2026 by Anzal Abidi).
   - Prior to Abidi's update, Kai Liang (arXiv:2505.12776, added October 24, 2025) published 18 digits with bracket $[1.342643951124601297851, 1.342643951124601298092]$.

2. **Target Decimals Requirement**:
   - Success criterion specifies: $D \ge (\text{number of terms in A247413 DATA, re-fetched live immediately before claiming}) + 4$.
   - Since live DATA contains 26 terms, the required threshold is $D \ge 26 + 4 = 30$ decimal digits.
   - This submission provides and certifies $D = 36$ decimal digits:
     `1.3426439511246012978517301618757403957`
   - This extends 10 decimals beyond the live 26-digit record and 18 decimals beyond Kai Liang's 18 digits.

3. **Repository & Conflict Check**:
   - Inspected `repo/TROPHY_CASE.md`: no prior trophy exists for `kings-hard-core-entropy-a247413-digits`.
   - Inspected `known-knowns/`: no competing packages exist for this target.
   - Inspected open PRs on `elder-plinius/V3R1T4S`: zero competing pull requests.

4. **Verdict**:
   - The result is genuinely novel, strictly extends the state-of-the-art live record of OEIS A247413 by 10 decimal digits, and meets all novelty criteria.

pass: true
