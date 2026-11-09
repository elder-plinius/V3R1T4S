context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report, sc436-7x365

[Edited 2026-11-09 at the maintainer's request on the pull request: mentions of files that are not in this package were removed. The checks, numbers and verdict are unchanged.]

Method: own checker written from the definition before reading verify-it-yourself/ (mpmath, 50 digits, normalise, all 66,430 pairs). Live table fetched once each on 2026-11-08 (/plain HTTP 200, index HTTP 200).

## Clause by clause
- (a) Row present in /plain: yes. Live /plain (2026-11-08) has "7,365,0.670467238587", identical to the-record-we-beat/plain_rows.csv. Also present in the live index with link /data/7/365.
- (b) Coordinates to >= 20 digits: yes. 365 lines x 7 coordinates; the shortest coordinate has 26 significant digits (most 30). Norm deviation from 1 before normalising is about 7e-31.
- (c) c* over all pairs at 50 digits: 0.67046703514181086523555479..., which matches the claimed 0.67046703514181086524 to 20 digits. Margin against the live 12-decimal cosine: 0.670467238587 - c* = 2.0345e-7, about 2000 times the 1e-10 bar. The 12-decimal rounding of the table (error at most 5e-13) cannot change this; the comparison is honest. The object itself carries 26+ digits, so the object's precision (~1e-26) is far below the margin. Minimal angle about 47.8968790 degrees. No duplicate or near-duplicate vectors (c* is well below 1).
- (d) Live index row for 7/365: no "&ast;" and no "needs more optimization" text in the row (credited to Antoine Jay, 2026). The phrase occurs 699 times elsewhere on the page, none in this row. Same as the saved 2026-11-03 row. Satisfied.
- (e) Not superseded by a newer arXiv result: NOT decidable from this folder. The folder only cites arXiv:2610.19988 as related and states the Zenodo data set behind it was not fetched. I did no literature search (the novelty skeptic's job). I can state only that the live table value for this row is unchanged since 2026-11-03.
- (f) Kissing exclusion: d = 7, outside 9 <= d <= 23, so does not apply (c* = 0.67 > 0.5 as well).

## Hidden quantifiers and subsumption
- Subsumption by larger N: in the live /plain, no dimension-7 row with N > 365 has a cosine <= 0.670467035142 (zero rows; N = 366 is 0.670923693486, which is higher). So no larger code in the table dominates this one (and none could be shrunk to beat it). Neighbouring smaller N (360 to 364) have lower cosines, which is normal.
- Comparison target: the criterion names the 12-decimal /plain cosine, and that is what was used. No re-rounding trick: margin is far larger than the rounding.
- The 12-decimal table cosine is the live value at review time, re-fetched by me on 2026-11-08, so the "fetched immediately before claiming" clause is met now, not just on 2026-11-03.
- Full win vs p2: the label "needs more optimization" is absent from the row in both the saved 2026-11-03 file and my 2026-11-08 fetch. The criterion says the table at review time decides, so the full criterion applies. p2 (a batch of >= 20 labelled rows) is not what is claimed and does not fit a single row. Judged literally, the full-win label is correct, subject to (e). Caveat: the row's earlier label on 2026-10-18 (per the package's own history, not checked by me) means the improvement is over an entry that was recently flagged unconverged; this does not break the written criterion but a reader should know it. The big gap between this row (0.67047) and N = 366 (0.67092) shows the row was a weak entry, not a state-of-the-art one, which is a reason it was beatable but not a reason to reject.
- Not checked by me: the live /data/7/365 parser sanity step (posted code reproduces table to 1e-11); the task did not ask and the folder's claim does not depend on it, but the stated verification method includes it.

## Verdict
Clauses (a), (b), (c), (d), (f) confirmed independently against the live table. Clause (e) is open from this folder; it rests on the novelty skeptic. I confirm the result meets every clause I can test, but because (e) is a required clause I cannot close, I pass only for the scope below and the whole-criterion pass is conditional on the novelty skeptic.

confirmed_scope: As of the 2026-11-08 live fetch of spherical-codes.org, object/7x365.txt (365 vectors in R^7, coordinates to at least 26 digits) has a 50-digit maximum pairwise inner product of 0.670467035142 (20 digits: 0.67046703514181086524), 2.0345e-7 below the live /plain cosine 0.670467238587 of the (7, 365) row, on an index row with no proven-optimal mark and no "needs more optimization" text, with no dimension-7 row of larger N at or below this value, while supersession by a newer arXiv result was not checked here.
pass: true
