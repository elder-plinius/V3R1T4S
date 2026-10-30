# Honesty gate, claim (6, 575), spherical-codes-cohn-table

Read by the run's main session (2026-10-25T00:27:12Z): panel/reproduce.md (pass: true), panel/novelty.md (pass: true;
live index and /plain fetched once each at 2026-10-25T00:14:17Z and 00:14:19Z, HTTP 200, row 0.792780236785,
"Pavlos Moros, 2026.", no star, no label, still the minimum over d' <= 6 and N' >= 575), panel/criterion.md
(pass: true).

Downgrade checks (kit/RUN.md step 7):
- Hedging panelist: none. Each states the limits of its role (no network for REPRODUCE and CRITERION; uploads not
  yet posted and non-arXiv literature for NOVELTY) as limits, and none leaves a known code at or below c*.
- Reproduction mismatch: none. REPRODUCE checked all 165,025 pairs exactly and at 50 and 80 digits; its two
  REPRODUCE.md transcripts are byte-identical to expected_output.txt. NOVELTY and CRITERION computed c* themselves
  and agree.
- Strictly better than the live table: yes, by 1.004011e-4 against the margin 1e-10, at NOVELTY's fetch about 10
  minutes after the claim fetch.
- Stretched criterion or hidden quantifier: CRITERION took the ten conjuncts one by one. The p2 question (the posted
  code was unconverged, 1 pair at its maximum) is decided by the criterion's wording: the live row carries no
  'needs more optimization', so this is the full criterion, not partial win p2. CLAIM.md discloses the convergence
  facts and any write-up keeps them.
- Scope wider than reproduced: the confirmed scope below is the CRITERION skeptic's sentence, which names its own
  limits.
- Sample presented as complete, capped search used as an exclusion, probable prime: not applicable (one explicit
  object; REPRODUCE's exact test covers every pair; CRITERION's exact test covers the 3,039 pairs within 1e-3 of the
  table value with all pairs computed at 50 digits).
- Table value obtained by evasion: no. Every table read is one GET with the V3R1T4S User-Agent, HTTP 200, no
  retries, no cookies (self-break access audits, both rounds).
- Several objects bundled: no (one code, one cell).
- Panel table fetch older than 6 hours: no (00:14:17Z).
- Null test: PREREG.md gives null_test: not needed (explicit object judged by deterministic checkers); the posted-code
  control (9.2e-13 below the table, fails the exact bar) was run by every skeptic.

status: CONFIRMED_SOLUTION
confirmed_scope: The 575 vectors in object/code_6_575.txt (26 significant digits per coordinate), each normalised in mpmath at 50 digits, have maximum pairwise cosine c* = 0.7926798356844868804983 (22 significant digits), which is 0.00010040110051 (at least 1e-10, confirmed with exact rationals) below the cosine 0.792780236785 of the (6, 575) row in the /plain and HTML index pages recorded in the-record-we-beat/RECORD.md (logged as fetched at 2026-10-25T00:04:42Z and 00:04:44Z, 3 to 5 seconds before the claim files were written at 00:04:47Z), a row that in those saved pages has no '&ast;' and no 'needs more optimization', is the lowest of all listed rows with d' <= 6 and N' >= 575, and is not matched at or below c* by arXiv:2610.19988's three tables or by any paper in the saved arXiv keyword feeds; not confirmed are the row's live state after that fetch, the fetch times beyond their agreement with file times and sha256, and arXiv papers outside those keyword feeds.
