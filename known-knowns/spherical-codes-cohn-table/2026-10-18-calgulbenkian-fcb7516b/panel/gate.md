# Honesty gate (spherical-codes-cohn-table), fresh panel of 2026-11-08 for the single row (7, 365)

status: CONFIRMED_SOLUTION
confirmed_scope: As of the 2026-11-08 live fetch of spherical-codes.org, object/7x365.txt (365 vectors in R^7, coordinates to at least 26 digits) has a 50-digit maximum pairwise inner product of 0.670467035142 (20 digits: 0.67046703514181086524), 2.0345e-7 below the live /plain cosine 0.670467238587 of the (7, 365) row, on an index row with no proven-optimal mark and no "needs more optimization" text, with no dimension-7 row of larger N at or below this value, while supersession by a newer arXiv result was not checked here.

## Gate notes
- Object: object/7x365.txt, sha256 fcb7516bada8a9fe8aee81aca8579d82f739661f0d91e4397cf2bd0804e7cf37 (also in INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true` (the three files beside this one).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh on 2026-11-08 and given only the claim folder (this package without panel/); the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Live table at panel time (2026-11-08T14:58Z, novelty and criterion fetches): /plain row 7,365,0.670467238587, unchanged since the 2026-11-03 fetch saved in the-record-we-beat/; the index row has no proven-optimal mark and no "needs more optimization" text; no dimension-7 row with N > 365 is at or below our value.
- The criterion skeptic left the newer-arXiv clause to the novelty skeptic, who found no arXiv paper naming a (7, 365) code; the Zenodo data set behind arXiv:2610.19988 was not fetched by either, so an unposted better code there is not excluded (README, "Not claimed").
- The earlier panel of 2026-10-18 reviewed the 24-row package this one was cut from; its files are in panel/2026-10-18/, unchanged.
- On 2026-11-09, at the maintainer's request on the pull request, the three reports were edited to remove mentions of files that are not in this package and to give the arXiv responses' sha256 values in full; each report carries a dated note. Verdicts, numbers and the confirmed_scope sentence are unchanged.
- No downgrade triggers found.
