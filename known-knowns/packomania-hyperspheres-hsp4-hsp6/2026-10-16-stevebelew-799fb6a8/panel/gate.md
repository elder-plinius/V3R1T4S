# Honesty gate (fresh-context panel, claim: hsp4 N = 79)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-10-16 17:55 UTC

status: CONFIRMED_SOLUTION
confirmed_scope: In d=4 with N=79, the 79 centres in hsp4-79-candidate.txt lie in the unit ball centred at the origin with feasible radius r* = 0.256565783134456 (mpmath 50 digits, no tolerance), exceeding the snapshot table value 0.256468324828 by 9.74583064563133e-5 and not isometric to the posted hsp4-79 packing, conditional on the live history and queue checks recorded in CLAIM.md.

## Panel

Three fresh contexts (subagents), EACH started for this one claim and seeing only this claim's folder: REPRODUCE
(pass: true), NOVELTY (pass: true; live fetches at 2026-10-16T17:48:37Z),
CRITERION (pass: true). This replaces the batch-context panel kept in panel_batch/ (same verdicts), after the
maintainer's 2026-10-15 request for fresh, separate contexts per claim. Gain (claims/ORDER.txt): 9.746e-05; object found by
lens warm-polish-77-300 of run 2026-10-14-1528. Hedge-word counts {'reproduce': 0, 'novelty': 0, 'criterion': 1}; leaked paths or placeholders {'reproduce': 0, 'novelty': 2, 'criterion': 0}.

## Downgrade checklist (each considered)

- Hedging panelist: hedge words present; read in context by the gate, judged not to weaken the verdicts.
- Reproduction mismatch: none. Value not strictly better than the live table: no; live row equals the snapshot, gain >= 1e-10 at 50 digits.
- Stretched criterion, hidden quantifier, wrong container, mislabelled N: none found by CRITERION.
- Scope wider than reproduced: one cell (d = 4, N = 79), one file, one value.
- Table value obtained by evasion: no; one plain GET per URL by the NOVELTY context, no retries.
- Several objects bundled: no.

## Not claimed

Optimality; a "record" beyond strictly exceeding the posted 12-decimal value on this date; anything about other N or
hsp5/hsp6. The bank's caveat about the unresolved "Moki & Julio *many* 4666 candidates" bundle applies.
