# Honesty gate: base-13 claim (claim/)

Read by the run's main session at 2026-10-23T22:45:53Z. Three fresh contexts (Claude Code Agent tool subagents), each
seeing only its own copy of claim/:
- reproduce.md: pass: true. Own checker written from the definition before reading the author's code; all-m symbolic
  argument with threshold 0; author's two REPRODUCE.md commands reproduced exactly; reruns deterministic.
- criterion.md: pass: true. Conditions (1)-(4) met literally; level stated as partial win p1 (novelty not established
  by the package itself), not full CONFIRMED. Cosmetic note: code/prove_claim.py's docstring names the base-9 file
  name; the code reads whatever JSON is passed and was run on result/lychrel_base13.json. Left unchanged after the panel.
- novelty.md: pass: true, after a follow-up. Its first verdict was pass: false for search gaps (2023 paper full text,
  open-PR list, arXiv). The main session then supplied the 2023 paper PDF archived earlier from the author's own
  preprint host (the skeptic checked its sha256 against the receipt) and allowed one read of the filtered open-PR
  search (a different page, not a retry). No blocked source was retried. The skeptic read all 30 pages (bases 3-10
  only; its construction is base 4), found one open PR (#517, bases 50/98/146), no arXiv hit, and rewrote its verdict.
  Wikipedia fetched 2026-10-23T22:36:25Z (HTTP 200), lists only 11, 17, 20, 26 and powers of 2: under 6 h old.
Re-read 2026-10-23T22:55:26Z after the NOVELTY panelist reworded one citation (a MathPages URL path that the leak
checker reads as a home directory) at the main session's request; its findings and verdict are unchanged.
Downgrade checks: no reproduction mismatch; no hedging panelist; scope no wider than the CRITERION sentence; the
all-m statement rests on an exact symbolic computation with threshold 0 (no sampled or capped step used as an
exclusion); one object; no evasive table access.
Related prior work credited (not the same base): github.com/dew-web/lychrel-self-similar (base 9, 2026-10-10, same
two-run method family; its README says the central-uniform-run type is not included in its results; this object is
that type). Level: partial win p1 per the CRITERION panelist; never upgraded.

Mechanical gate (2026-10-23T22:59:12Z): with the package built in outbox/, the package check printed CHECK_RUN: PASS
(1 warning, the credit name), but the workspace check printed CHECK_RUN: FAIL (1 problem): the foreign package
outbox/2026-10-23-jndk-1c440b13 (another session's, not this target) failed its own checker. RUN.md step 7 then
forced PROMISING, and the built package was kept out of outbox/.
Re-gate (2026-10-24, after the human reported that foreign package fixed): the workspace check printed
CHECK_RUN: PASS (5 warnings, all login-name matches in older packages); outbox/2026-10-23-jndk-1c440b13 now passes its
own checker (server job 2422). Nothing in this claim or its panel changed. The panel's Wikipedia fetch
(2026-10-23T22:36:25Z) is under 6 h old. With the panel's 3/3 pass and none of the downgrade conditions present, the
status is the CRITERION panelist's level, partial win p1: CONFIRMED_PARTIAL (novelty not established by this package;
an expert check is still needed before publication).

status: CONFIRMED_PARTIAL
confirmed_scope: In base 13, the 134-digit number n of result/seed_base13.txt equals T_0(0) of the 10 affine run-length templates in result/lychrel_base13.json, and a mechanically checked symbolic carry computation with threshold 0 (re-run in jobs 2340 and 2344, cross-checked by integer brute force for m <= 400 and a 100000-step simulation in job 2347) proves RA(T_i(m)) = T_(i+1)(m) for i < 9 and RA(T_9(m)) = T_0(m+1) for every m >= 0, with no T_i(m) a palindrome, so n is a Lychrel number in base 13 at the level of partial win p1 (novelty not established by this package).
