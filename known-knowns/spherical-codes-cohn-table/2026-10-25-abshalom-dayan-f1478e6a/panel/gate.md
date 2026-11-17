# Honesty gate, claim (6, 256), spherical-codes-cohn-table

Read by the run's main session (2026-10-25T06:50:23Z): panel/reproduce.md (pass: true), panel/novelty.md (pass: true; live index
and /plain fetched once each at 2026-10-25T06:33:58Z and 06:34:00Z, HTTP 200, byte-identical to the claim-moment read
(same sha256); row 0.704931969352, "Pavlos Moros, 2026.", no star, no label, still the minimum over d' <= 6 and
N' >= 256), panel/criterion.md (pass: true). The skeptics ran one after another, each in a fresh context on Opus 5.5,
after the self-break (selfbreak/verdict.md: SURVIVES, with eight wording and record findings; five repaired before
the claim2 read, claim_build/REPAIR1.md).

Downgrade checks (kit/RUN.md step 7):
- Hedging panelist: none. Each states the limits of its role (no network for REPRODUCE and CRITERION; titles and
  abstracts for most papers and no non-arXiv sources for NOVELTY) as limits, and none leaves a known code at or
  below c*.
- Reproduction mismatch: none. REPRODUCE checked all 32,640 pairs exactly and at 50 and 100 digits; its two
  REPRODUCE.md runs are byte-identical to expected_output.txt. NOVELTY and CRITERION computed c* themselves and agree
  (0.7048987224974410014733 at pair (55, 247)).
- Strictly better than the live table: yes, by 3.32469e-5 against the margin 1e-10, at NOVELTY's fetch about 7
  minutes after the claim fetch.
- Stretched criterion or hidden quantifier: CRITERION took the conjuncts one by one. The p2 question (the posted code
  was unconverged: 1 pair within 1e-14 of its maximum, 998 within 1e-8) is decided by the criterion's wording: the
  live row carries no 'needs more optimization', so this is the full criterion, not partial win p2. CLAIM.md
  discloses the convergence facts and the package README keeps them. The 26 printed digits are binary64 values
  written with %.25e (CRITERION); the criterion asks for coordinates given to >= 20 digits and c* is computed from
  the file as written.
- Scope wider than reproduced: the confirmed scope below is the CRITERION skeptic's sentence, which names its own
  limits.
- Sample presented as complete, capped search used as an exclusion, probable prime: not applicable (one explicit
  object; REPRODUCE's and CRITERION's exact tests cover every pair).
- Table value obtained by evasion: no. Every table read is one GET with the V3R1T4S User-Agent, HTTP 200, no
  retries, no cookies (self-break access audit; NOVELTY's own fetch log).
- Several objects bundled: no (one code, one cell).
- Panel table fetch older than 6 hours: no (06:33:58Z).
- Null test: PREREG.md gives null_test: not needed (explicit object judged by deterministic checkers); the posted-code
  control (3.89e-13 below the table, fails the exact bar on 2 pairs) was run by every skeptic.

status: CONFIRMED_SOLUTION
confirmed_scope: In the claim package's saved pages, fetched 2026-10-25T06:26:36Z (index) and 06:26:38Z (/plain), 3 s before CLAIM.md was written according to the file times, the 256 vectors of object/code_6_256.txt (26 significant digits per coordinate), normalised in mpmath at 50 digits, have c* = 0.7048987224974410014733 at pair (55, 247), which is 0.00003324685455899852672 below the unstarred, unlabelled /plain row 6,256,0.704931969352 (exact-rational check: no pair above 0.704931969352 − 1e-10) and below every row with d' <= 6 and N' >= 256 in /plain, in the index and in arXiv:2610.19988's three tables; no saved arXiv feed or full text shows a (6, 256) code at or below c*, and d = 6 lies outside the kissing clause; not confirmed are the row's live state after 06:26:38Z (my timing check ran 21.8 minutes after that fetch), any arXiv paper posted after about 05:54Z or missed by the saved title and abstract feeds, and the truth of the fetch-log lines beyond their sha256 matching the saved bytes.
