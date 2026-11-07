# Honesty gate (fresh-context panel, claim: hsp4 N = 80)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-10-16 17:57 UTC

status: CONFIRMED_SOLUTION
confirmed_scope: For d=4, N=80, the 80 centres in hsp4-80-candidate.txt lie in the origin-centred unit 4-ball with feasible radius r* = 0.255469606984850 (mpmath 50 digits, no tolerance, wall-bound), exceeding the snapshot table value 0.255463163131 by 6.44385384976114e-6 (above the 1e-10 margin), and are not isometric to hsp4-80-posted.txt (all 3160 sorted pairwise distances differ, max 1.22e-2); the live-table, history and pending-queue clauses are recorded in CLAIM.md but not re-fetched here, and the Moki and Julio bundle caveat applies.

## Panel

Three fresh contexts (subagents), EACH started for this one claim and seeing only this claim's folder: REPRODUCE
(pass: true), NOVELTY (pass: true; live fetches at see file),
CRITERION (pass: true). This replaces the batch-context panel kept in panel_batch/ (same verdicts), after the
maintainer's 2026-10-15 request for fresh, separate contexts per claim. Gain (claims/ORDER.txt): 6.444e-06; object found by
lens warm-polish-77-300 of run 2026-10-14-1528. Hedge-word counts {'reproduce': 0, 'novelty': 0, 'criterion': 0}; leaked paths or placeholders {'reproduce': 0, 'novelty': 0, 'criterion': 0}.

## Downgrade checklist (each considered)

- Hedging panelist: none.
- Reproduction mismatch: none. Value not strictly better than the live table: no; live row equals the snapshot, gain >= 1e-10 at 50 digits.
- Stretched criterion, hidden quantifier, wrong container, mislabelled N: none found by CRITERION.
- Scope wider than reproduced: one cell (d = 4, N = 80), one file, one value.
- Table value obtained by evasion: no; one plain GET per URL by the NOVELTY context, no retries.
- Several objects bundled: no.

## Not claimed

Optimality; a "record" beyond strictly exceeding the posted 12-decimal value on this date; anything about other N or
hsp5/hsp6. The bank's caveat about the unresolved "Moki & Julio *many* 4666 candidates" bundle applies.
