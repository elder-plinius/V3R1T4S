# CRITERION verdict: sph-31-64

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:08Z

## Value computed here
- Own checker (mpmath dps=50, each vector normalised, all 2016 inner products). object/31_64.txt sha256 38ad0da4...421a matches SHA256SUMS; 64 non-comment lines x 31 coordinates.
- c* = 0.030319733375043224553889612958408072340355255022322
- minimal angle = 88.26254096858434922 deg; 1451 pairs within 1e-12 of c* (heavily rigid contact graph); min coordinate significant digits = 21 (>= 20).
- Table (https://spherical-codes.org/plain (fetched 2026-11-01T14:32Z, sha256 b7c6a76fe07eab18f4da729f1162a65d1e5042678d7568013b1d49737df254c1), single row `31,64,0.030322662292`): table - c* = 2.92891695677545e-6 >= 1e-10.
- The evidence files are the live re-fetch for this panel (fetched 2026-11-01T14:32Z); I re-ran sha256sum on every fetched file and each hash matches the values listed in the-record-we-beat/RECORD.md. The comment line in 31_64.txt was ignored as data (its value agrees with mine). No injection suspected.

## Clauses checked
- Clause 1 (value): c* = 0.0303197333750432245539 at 50 digits, all coordinates >= 21 sig. digits, table 0.030322662292, margin 2.929e-6 >= 1e-10. PASS.
- Clause 2 (asterisk/label): the index-row extract for (31, 64) from https://spherical-codes.org/ (sha256 e137904fb8a1c1fcd2c72574e9f3e9eb520a046b71ecba28d4079e676dddfe65): 0 occurrences of '&ast;' or '*', 0 of 'needs more optimization'; row cosine 0.030322662292 = /plain; credited reference Ilmari Vahteristo, "New spherical codes by tuning an annealing solver", arXiv:2610.19988. PASS.
- Clause 3 (arXiv): parsed both newest-15 feeds. The credited paper 2610.19988 (2026-10-14) is the source of the table value itself (annealing-solver sweep of all N<=1024, 3<=D<=32, N>2D; (31,64) qualifies). Only newer 'spherical code' entry that touches the topic is 2610.21263 (2026-10-15, asymptotic Delsarte LP bound rate) - no constructions, no (31,64) cosine. All other newer entries are unrelated; the 'Tammes' feed is all physics (Tamm-Dancoff, Mandelstam-Tamm) with nothing on spherical codes. Limits: a newest-15 keyword search cannot exclude papers indexed under other terms, papers not mentioning (31,64) in abstracts, or non-arXiv sources; it covers only ~5 months for 'spherical code'. No superseding arXiv result found. PASS.
- Clause 4 (kissing): d = 31 is not in 9..23 (c* = 0.0303 <= 0.5 is irrelevant), so not kissing-number-low-dim. PASS.
- Clause 5 (prior claims): the repository's claim list for spherical-codes-cohn-table (open, merged and closed claim pull requests, read 2026-11-01) has no claim (open, merged or closed) for (31, 64) (neighbours (31,65), (30,64), (30,62) exist, different cells); TROPHY_CASE.md (https://github.com/elder-plinius/V3R1T4S/blob/f3b19b475065f35d0a7f93e8a6078c9b2f12566e/TROPHY_CASE.md, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113) has no spherical-codes / (31,64) entry. No conflict. PASS.
- Not done: the posted code /data/31/64 was not fetched (parser-sanity step of the bank's verification method, not a criterion clause).

## Decision
Every criterion clause is satisfied on my own computation and the supplied live re-fetch: c* beats the 12-decimal table cosine by 2.93e-6 (far above 1e-10), coordinates carry >= 21 digits, the index row is unstarred and unlabelled, the credited source (Vahteristo 2610.19988) is the table value's own origin and nothing newer on arXiv supersedes it, d = 31 lies outside the kissing range, and there is no prior claim for this cell.

pass: true
