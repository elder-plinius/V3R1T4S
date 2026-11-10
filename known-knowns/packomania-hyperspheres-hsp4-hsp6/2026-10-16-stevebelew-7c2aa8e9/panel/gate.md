# Honesty gate (fresh-context panel, claim: hsp4 N = 83)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: Fri Oct 16 21:34:26 UTC 2026

status: CONFIRMED_SOLUTION
confirmed_scope: For d=4, N=83, the 83 centres in hsp4-83-candidate.txt lie in the unit ball centred at the origin with feasible radius r* = 0.252010684947089 (mpmath, 50 digits, no tolerance), exceeding the snapshot Packomania table value 0.252008330509 by 2.354438e-06 (margin clause met by 23544x), and are not isometric to hsp4-83-posted.txt (sorted pairwise-distance multisets differ by up to 0.01185), with the history and queue clauses recorded in CLAIM.md as of 2026-10-16 16:29:32 UTC but left to the live re-fetch.

## Panel

Three fresh contexts (subagents), EACH started for this one claim and seeing only this claim's folder: REPRODUCE
(pass: true), NOVELTY (pass: true; live fetches at see file),
CRITERION (pass: true). This replaces the batch-context panel kept in panel_batch/ (same verdicts), after the
maintainer's 2026-10-15 request for fresh, separate contexts per claim. Gain (claims/ORDER.txt): 2.354e-06; object found by
lens warm-polish-77-300 of run 2026-10-14-1528. Hedge-word counts {'reproduce': 0, 'novelty': 0, 'criterion': 0}; leaked paths or placeholders {'reproduce': 0, 'novelty': 0, 'criterion': 0} (the count includes the published credit handle inside repository URLs, which is not a leak).

## Pending-bundle check (gate, after the panel)

The authors of the pending bundle publish a manifest (data/moki-julio/comparison.md, fetched once Fri Oct 16 21:32:52 UTC 2026); for hsp4 N = 83 our r* is strictly ahead of their listed value by more than 1e-10, so the queue caveat is resolved in our favour as far as their public claim goes (their coordinates were not verified).

## Downgrade checklist (each considered)

- Hedging panelist: none.
- Reproduction mismatch: none. Value not strictly better than the live table: no; live row equals the snapshot, gain >= 1e-10 at 50 digits.
- Stretched criterion, hidden quantifier, wrong container, mislabelled N: none found by CRITERION.
- Scope wider than reproduced: one cell (d = 4, N = 83), one file, one value.
- Table value obtained by evasion: no; one plain GET per URL by the NOVELTY context, no retries.
- Equal or better value publicly claimed elsewhere (bundle manifest): no.
- Several objects bundled: no.

## Not claimed

Optimality; a "record" beyond strictly exceeding the posted 12-decimal value on this date; anything about other N or
hsp5/hsp6. The bank's caveat about the unresolved "Moki & Julio *many* 4666 candidates" bundle applies.
