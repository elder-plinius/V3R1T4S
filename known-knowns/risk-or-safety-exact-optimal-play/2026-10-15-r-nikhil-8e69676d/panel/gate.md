# Honesty gate (kit/RUN.md step 7), main session of run 2026-10-15-0312, written Thu Oct 15 09:37:56 UTC 2026 (first written 09:35 UTC; re-written only to quote the re-issued criterion.md, see note)

Claim: the 15 exact terms A387261(n)/A387262(n), n = 16..30, each with a full Bellman certificate (claim/).
Panel: three fresh subagent contexts started 09:08 UTC, each given only claim/; files panel/reproduce.md, panel/novelty.md,
panel/criterion.md, all ending "pass: true", all naming files relative to claim/ only.

Gate reading of the three files:
- REPRODUCE (pass): its own exact checker, written before opening the claim's code, passes all 30 certificates at every
  position (complete position sets, reduced values in [0,1], forced toss, max attained, 0 ties); its own independent exact
  solver reproduces all 30 tables, 112,840 positions, value for value and action for action; P(0,0,0) matches values.txt
  (15/15) and the OEIS b-files (15/15); mutation tests catch every failure mode incl. self-consistent sub-optimal policies;
  the claim's solver regenerates everything byte-identically twice; all 38 hashes verify; both rule conventions are the
  paper's; the proof note holds (with one phrase to be read as "the first n tosses of the block", which leaves the
  conclusion unchanged).
- NOVELTY (pass): status source https://oeis.org/A387261 fetched once at 2026-10-15T09:10:19Z, HTTP 200, 15 terms
  (n = 1..15), b-files identical to the claim's copies; A387262, A394776, A387260 and arXiv:2603.01002 fetched once each;
  OEIS term search for the claimed values (with a positive control) finds nothing; Piglet PRIMARY SOURCE READ (the authors'
  own copy of Neller-Presser 2004, one request, HTTP 200): same game, exact values for goal 2 only (4/7 = the published
  n = 2 term), a goal-2 value-iteration plot, nothing for goal 10 or beyond; Crocce-Mordecki (arXiv:1808.06707, 2018) solve
  Piglet exactly by the same equations and print the goal-3 table only; teaching code (PigletSolver.java) is floating point
  for goal 10; 22 web searches, arXiv, Stack Exchange API, GitHub code search, OpenAlex, TROPHY_CASE.md and the open pull
  requests: no term n >= 16 anywhere. Semantic Scholar answered 429 three times (not retried). Verdict: the 15 terms are new.
- CRITERION (pass): all six requirements of the criterion checked literally (15 reduced values in (0,1) equal to the
  certificates' P(0,0,0); starting-player convention confirmed against the paper's n = 3 text and a Monte Carlo of the prose
  rules; complete position sets with actions; exact equations incl. max attained; three exact checkers; the same solver
  regenerates n = 1..15 equal to the b-files term by term); uniqueness argument sound; rules match the paper; its own
  independent replication (float value iteration then exact evaluation) reproduces every value and action; no null test
  applies (deterministic exact certificate), checker-corruption tests used instead; full criterion met (p2 contained; p1
  not claimed).

Downgrade triggers checked: no hedging panelist (the caveats are credits and presentation); no reproduction mismatch; the
value set strictly extends the live table (published n = 1..15 only; the claimed n = 16..30 are disjoint from it, no tie);
no stretched criterion or hidden quantifier; scope no wider than reproduced (n = 16..30 only; nothing about n > 30 is in
this claim); nothing sampled or capped; no probable prime; table access honest (one request per page, blocks not retried);
one object (the 15-term extension of one sequence pair) per claim. The panel's status fetch is under one hour old.

Carried into the package and the report (not downgrades): credit Neller-Presser (Piglet, UMAP J. 2004; Fendel et al.'s
"Pig Tails") and Crocce-Mordecki (arXiv:1808.06707) as prior exact or numerical work on the same game, alongside Jehn and
Jinyuan Wang; the OEIS "Last modified" line quoted in claim.md is the site footer, the entries' HTTP last-modified is
10 Apr 2026; claim.md's status record names a page file kept in the run's data/, not in claim/ (nothing in the
reproduction needs it).

Note on criterion.md: after the first gate (09:35 UTC) the package checker flagged the file-name notation "object/n" followed by the letter n in angle brackets and ".json" in
criterion.md as an unfilled template placeholder; at the main session's request the CRITERION skeptic (same context)
re-issued its file with only that notation changed (now "object/nK.json with K = n"; a bracketed scratch-folder token in one command became "SCRATCH"),
no other wording, finding or verdict changed (its own diff against a backup, reported to the main session). The gate
quotes the re-issued sentence; the verdicts and this gate's status are unchanged.

status: CONFIRMED_SOLUTION
confirmed_scope: For each n = 16, ..., 30, the reduced fraction given for n in values.txt and claim.md is P(0,0,0) of object/nK.json with K = n, which lists a value and an action at every one of the n^2(n+1)/2 non-terminal positions and satisfies the criterion's equations exactly in rational arithmetic (P = 1 when a + b >= n, forced toss at a = 0, P = max(continue, stop) for a >= 1 with the listed action attaining the max and no exact ties), so by the proof note's uniqueness argument (checked sound) it is the starting player's win probability from (0, 0, 0) under optimal play in the game of Sections 1-4 of arXiv:2603.01002, and the same solver, re-run, regenerates all 30 certificates byte-for-byte with its n = 1..15 values equal to the A387261/A387262 terms in the package's OEIS snapshot (data/), n = 1..6 also equal to the values printed in the paper.
