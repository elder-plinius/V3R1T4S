# Honesty gate — labs-merit-factor-records, L = 401

status: CONFIRMED_SOLUTION
confirmed_scope: The sequence in sequence_L401.txt is an explicit +-1 sequence of length 401 whose exactly computed integer energy E = 10776 is strictly below the minimum L = 401 energy over the criterion's named sources as archived in this package (11888, from the borkob/git_labs skew tables at commit 1aa1234, with the arXiv:2607.09688v1 and arXiv:2504.00987v2 tables and the 2026-10-24 arXiv search listing no L = 401 value), below every other published L = 401 value in the package (ERK'2025 Figure 2: 11000; arXiv:2206.12070: 11456; arXiv:2011.00068v1: 11472), and below every truncate-then-extend (up to 10 symbols) derivation of a verified package witness (lowest 11200).

Read by the run's main session: panel/reproduce.md, panel/novelty.md and panel/criterion.md all end with pass: true, each written by
a fresh subagent context that saw only claim/. Checked against the downgrade list. No panelist hedges its verdict. No reproduction
mismatch touches the comparison. 10776 is strictly below the named table's 11888 and every published value (lowest 11000,
ERK'2025 Figure 2). The scope is the CRITERION sentence, unchanged. The derivation search is bounded and the scope says so. There is
one object, and every table fetch was a single honest request. NOVELTY's fetches were at 2026-10-24T21:02Z, so no re-fetch is needed.

Disclosed, not affecting the comparison (from the panel):
- CLAIM.md's arXiv:2409.07222v1 row says "no value at L = 401". The paper's tables have none, but one of its figures plots Dimitrov's
  value (F 7.018, E 11456), which is already in the comparison.
- ERK'2025's L = 450 Table 3 value reproduces only if truncated, not rounded. That length is outside the derivation window.
- The file bar/data/eprints/arxiv_abs_2607.09688.html has no row in table_record.md (its sha256 matches the scout record).
- The description of arXiv:2504.00987v2's tab:fit table ("a runtime fit over N = 20..70") is loose wording.
- Unread: the journal version of Dimitrov's DSP 2025 methods paper (its arXiv version holds only an L = 449 record), and a PSL preprint
  whose sequences have F around 5. Both were judged implausible by NOVELTY.
Earlier panel rounds are kept unchanged: panel_v1 (claim_v1), panel_v3 (claim_v3), panel_v5 (claim_v5), each failed on package-text
accuracy and never on the numbers. ERRATA.md items 5-8 record the fixes.
