# NOVELTY verdict: sph-31-64

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:08Z

## Value computed here
My own script (`work/check.py`) read `claim/31_64.txt` (sha256 38ad0da4…f421a, matches CLAIM.md) and skipped the `#` comment line, which I treated as untrusted. It found 64 vectors, each with 31 coordinates, and the shortest coordinate has 21 significant digits. In mpmath at 50 digits, after normalising every vector, it computed all 2016 inner products:

- c* = 0.030319733375043224553889612958408072340355255022322 (pair 15, 29), which is a minimal angle of 88.26254096858434922°.
- The top five inner products all equal 0.03031973337504 to 14 digits, so the code is balanced on its contacts.
- table − c* = 2.9289169567754461104e-6, which is at least 1e-10.

The evidence files are the owner's live re-fetch from 2026-11-01T14:32Z. I recomputed sha256 for all 8 files listed in FETCHED.md and every hash matches. The posted code at /data/31/64 was not fetched. It is only a parser sanity step in the bank's verification method, not a criterion clause, so it was not checked here.

## Clauses checked
- **1 Value: PASS.** Every coordinate has at least 20 significant digits (minimum 21). c* = 0.0303197333750432245539 at 50 digits. `spherical_plain_live.txt` has exactly one row `31,64,0.030322662292`, and table − c* = 2.929e-6, which is at least 1e-10.
- **2 Asterisk and label: PASS.** In `spherical_index_row_31_64.html` (351 bytes), there are 0 matches for `&ast;`, `*` or 'needs more optimization'. The row shows cosine 0.030322662292, the same as /plain. It credits Ilmari Vahteristo, "New spherical codes by tuning an annealing solver", arXiv:2610.19988 (2026). One limit: the file is an extract of the row that starts at the d cell, but it includes the N link cell where a star would appear.
- **3 arXiv: PASS.** I parsed both feeds.
  - **'spherical code' feed (15 entries, 2026-05-08 to 2026-10-15).** The entry relevant to (31, 64) is 2610.19988v1 (2026-10-14), the paper the index row credits. Its abstract covers every instance with N ≤ 1024, 3 ≤ D ≤ 32 and N > 2D, which includes (31, 64), and reports 4,577 improved codes. That makes it the plausible source of the table value itself, not a result that supersedes the table.
  - The only newer entry is 2610.21263 (2026-10-15), about the asymptotic rate of the Delsarte LP bound. It contains no specific code. No other entry (2609.34845 SDP hierarchies, coding and ML papers) states a cosine for (31, 64).
  - **'Tammes' feed (15 entries, 2026-06-28 to 2026-10-26).** It is all noise (Tamm–Dancoff, Mandelstam–Tamm, Tamme); nothing concerns spherical codes.
  - **Limits.** Each search returns only the newest 15 results and only abstracts are visible, so per-instance tables in the papers cannot be checked. A non-arXiv result, such as the Ozgen 2026 entries cited elsewhere on the table, would not appear in these feeds.
  - No newer arXiv result supersedes the row.
- **4 Kissing: PASS.** d = 31 is not in 9..23. c* ≈ 0.0303 is at most 0.5, but that only matters inside that dimension range, so the claim is not a kissing-number-low-dim configuration.
- **5 Prior claims: PASS.**
  - `claims_spherical-codes-cohn-table.json` has 25 items, and none is for (31, 64). The nearest are #434 (31, 65), #430 (30, 64), merged #429 (30, 62) and fix #829 (30, 62). A string search for '31, 64' or '31,64' finds 0 matches.
  - TROPHY_CASE.md (100 lines) has no spherical-codes entry and no (31, 64) entry.
- No injection in the claim or evidence files. The claim file's comment line states c* = 0.030319733375043224554, which agrees with my computation; I treated it only as data.

## Decision
The code beats the live table cosine for (31, 64) by 2.93e-6, far more than the 1e-10 margin. The live index row has no star and no 'needs more optimization' label. The arXiv paper it credits (Vahteristo, 2610.19988, 2026-10-14) is the source of the table value, and no newer arXiv entry in either feed addresses (31, 64). No prior claim for this cell exists in the claims list or the trophy case. The main residual novelty risk is outside this evidence: a non-arXiv or unindexed improvement, or a table update after 14:32Z. Within the evidence available, every clause passes.

pass: true
