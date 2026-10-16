# Honesty gate (fresh-context panel, claim: hsp4 N = 94)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-10-16 17:57 UTC

status: CONFIRMED_SOLUTION
confirmed_scope: In d=4 with N=94, the 94 centres in hsp4-94-candidate.txt lie in the unit ball centred at the origin and have tolerance-free 50-digit feasible radius r* = 0.245941019536845 (to 15 significant digits), exceeding the snapshot radius.txt table value 0.245932827006 by 8.19253084519902e-06 (at least 1e-10), and their sorted pairwise-distance multiset differs from that of hsp4-94-posted.txt by up to 0.0096 (more than 1e-8), so the configuration is not isometric to the posted one; the live-table, history-of-updates and pending-queue clauses are recorded in CLAIM.md but were not re-fetched here.

## Panel

Three fresh contexts (subagents), EACH started for this one claim and seeing only this claim's folder: REPRODUCE
(pass: true), NOVELTY (pass: true; live fetches at 2026-10-16T17:55:11Z),
CRITERION (pass: true). This replaces the batch-context panel kept in panel_batch/ (same verdicts), after the
maintainer's 2026-10-15 request for fresh, separate contexts per claim. Gain (claims/ORDER.txt): 8.193e-06; object found by
lens warm-polish-77-300 of run 2026-10-14-1528. Hedge-word counts {'reproduce': 0, 'novelty': 0, 'criterion': 0}; leaked paths or placeholders {'reproduce': 0, 'novelty': 0, 'criterion': 0}.

## Downgrade checklist (each considered)

- Hedging panelist: none.
- Reproduction mismatch: none. Value not strictly better than the live table: no; live row equals the snapshot, gain >= 1e-10 at 50 digits.
- Stretched criterion, hidden quantifier, wrong container, mislabelled N: none found by CRITERION.
- Scope wider than reproduced: one cell (d = 4, N = 94), one file, one value.
- Table value obtained by evasion: no; one plain GET per URL by the NOVELTY context, no retries.
- Several objects bundled: no.

## Not claimed

Optimality; a "record" beyond strictly exceeding the posted 12-decimal value on this date; anything about other N or
hsp5/hsp6. The bank's caveat about the unresolved "Moki & Julio *many* 4666 candidates" bundle applies.
