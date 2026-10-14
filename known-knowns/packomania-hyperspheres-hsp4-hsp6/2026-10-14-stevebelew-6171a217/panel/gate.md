# Honesty gate (run 2026-10-14-1528, claim: hsp4 N = 42)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-10-14 15:36 UTC

status: CONFIRMED_SOLUTION
confirmed_scope: For d = 4 and N = 42, the 42 centres in hsp4-42-candidate.txt lie in the unit ball centred at the origin and have feasible radius r* = 0.293369217477315 (mpmath 50 digits, no tolerance), which exceeds the 12-decimal table value 0.293368844389 in hsp4_radius_as_fetched.txt by 3.73088315494127e-7 (>= 1e-10) and is not isometric to hsp4-42-posted.txt (sorted distance multisets differ by up to 0.040786804); the live re-fetch, History-of-updates and pending-queue clauses, including the unresolved category-unspecified Moki & Julio bundle, are not verifiable from these files and the pass is conditional on them.

## Panel

Three fresh contexts (subagents), each of which judged the 14 carried claims one claim folder at a time and wrote one
verdict file per claim; this claim's three files all end in `pass: true`. REPRODUCE wrote its own 50-digit checker before
reading the author's commands; NOVELTY fetched each live page exactly once for the whole panel (radius.txt at
2026-10-14T15:31:59Z, HTTP 200, byte-identical to the snapshot; hsp4.html "Last update: 06-Jul-2025"; no hsp4 queue entry;
TROPHY_CASE.md and the 11 open PRs clear; the only hsp4 PR, #127, claims N = 66); CRITERION judged every clause with its
own script. Gain from CRITERION's output: 3.73088315494127e-7.

## Downgrade checklist (each considered; none triggered)

- Hedging panelist: none (zero hedge words; the conditional clauses in the scope are the live-fetch clauses NOVELTY verified).
- Reproduction mismatch: none; r* identical across the author's checker, REPRODUCE's and CRITERION's, deterministic.
- Value not strictly better than the live table: no; live row equals the snapshot and the gain is >= 1e-10 at 50 digits.
- Stretched criterion, hidden quantifier, wrong container, mislabelled N: none found.
- Scope wider than reproduced: one cell (d = 4, N = 42), one file, one value.
- Table value obtained by evasion: no; one plain GET per URL with a V3R1T4S User-Agent, no retries, HTTP 200.
- Several objects bundled: no; each of the 14 carried claims has its own folder, panel files, gate and package.

## Not claimed

Optimality; a "record" beyond strictly exceeding the posted 12-decimal value on this date; anything about other N or
hsp5/hsp6. The bank's caveat about the unresolved "Moki & Julio *many* 4666 candidates" bundle applies.

## Gate note (2026-10-14 15:38 UTC)

After this gate, the mechanical package check flagged an angle-bracketed "claim_dir" token in reproduce.md as an unfilled placeholder. The
REPRODUCE skeptic (same fresh context, resumed) reissued its file replacing angle-bracket notation with plain words; checker
code, pasted output, verdicts and the final line are unchanged (re-verified: still ends in pass: true). No other panel file was touched.
