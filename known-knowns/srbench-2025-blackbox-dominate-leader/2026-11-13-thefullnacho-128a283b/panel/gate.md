# Honesty gate — srbench-2025-blackbox-dominate-leader / 522_pm10 (GAM shape compression)

status: CONFIRMED_SOLUTION
confirmed_scope: The fixed GAM-shape-compression procedure in code/gam_sr.py returns one closed-form expression per listed seed for dataset 522_pm10 with median test R2 0.331263, strictly above PS-Tree's live-table median 0.300852, at median complexity 145.5, at or below PS-Tree's median model size 4996.5.

Panel (three fresh subagent contexts, each seeing only claim/):
- panel/reproduce.md — context: subagent — pass: true. Independent checker written before reading the author's code; all 30 expressions re-scored, medians reproduced exactly (R2 0.331262948, complexity 145.5); bar re-derived from the saved table; procedure re-run on seeds 769 and 32157, twice each, deterministic, character-for-character match; leakage audit clean. Flagged one packaging defect: claim/data/ was missing read_file.py (imported by symbolic_utils.py), so the packaged checker did not run standalone. FIXED by the main session before the gate: SRBench's read_file.py vendored into claim/data/ (sha256 a98cd7bc...); REPRODUCE.md step 1 re-run verbatim from claim/ after the fix reproduces median R2 0.3312629480085087 and median complexity 145.5. The defect changed no number.
- panel/novelty.md — context: subagent — pass: true. Live table fetched once 2026-11-13 06:21 UTC (HTTP 200, sha256 identical to the scout's record); leader confirmed PS-Tree 0.300852 / 4996.5; no literature, code, release, PR, trophy-case or known-knowns entry at or above the claim; no trivial edit of a published expression yields it; procedure not seeded from a published object.
- panel/criterion.md — context: subagent — pass: true. Literal clause-by-clause check: splits are the listed ones, expressions are genuine closed forms, median R2 strictly greater than the live leader, median complexity below the leader's size, procedure fixed before scoring with no per-split hand edits, p1 also met, null model (constant-mean median -0.004441) beaten by 0.335704. No stretched definitions.

Downgrade checks (RUN.md step 7): no hedging panelist; no reproduction mismatch (exact to 0.0 on the full-precision check); value strictly better than the live table; no stretched criterion or hidden quantifier; scope exactly as reproduced; all 30 splits re-scored (no sample presented as complete); no capped search used as an exclusion; no table value obtained by evasion (one honest GET each; NOVELTY's fetch 06:21 UTC, under 6 hours old); one procedure, one claim about its medians — the criterion's own shape, not several objects bundled. No unresolved benchmark baseline (explicit object checked deterministically).

Break-it (main session, code/break_it.py): independent re-derivation reproduces the claim exactly (worst |dR2| = 0.0 vs results.json, 0 complexity mismatches). Verdict: SURVIVES.

Final status: CONFIRMED_SOLUTION. Package: outbox/2026-11-13-thefullnacho-522pm10-gam (see REPORT.md).
