# Honesty gate (run 2026-10-14-0239, claim: hsp4 N = 66)

gate_by: the run's main session, after reading reproduce.md, novelty.md and criterion.md in full
gate_time_utc: 2026-10-14 03:20 UTC

status: CONFIRMED_SOLUTION
confirmed_scope: In d=4 with N=66, the 66 centres in hsp4-66-candidate.txt have feasible radius r* = 0.264976367513876 (mpmath, 50 digits, container-bound) in the unit ball centred at the origin, exceeding the snapshot table value 0.264968466676 by 7.90e-6 and non-isometric to the posted packing (all 2145 sorted pairwise distances differ by more than 1e-8), subject to the live history/queue re-fetch and the unresolved 'Moki & Julio *many* 4666 candidates' bundle caveat.

## Downgrade checklist (each considered; none triggered)

- Hedging panelist: none. The CRITERION scope's "subject to the live history/queue re-fetch" names the clauses it could
  not see from claim/; NOVELTY verified exactly those live (radius.txt row 66 unchanged at 2026-10-14T03:16:42Z, HTTP 200;
  hsp4.html "Last update: 06-Jul-2025" with no newer history entry; pending-requests.html has no hsp4 entry). The
  bundle caveat is required verbatim by the bank's criterion, not a hedge.
- Reproduction mismatch: none. REPRODUCE's own checker gives r* = 0.26497636751387602328900871272524886345982755040961,
  identical to the author's and to the standard-library decimal checker; deterministic across two runs.
- Value not strictly better than the live table: gain 7.90e-6 >= 1e-10, live table re-fetched by NOVELTY 3 minutes before
  this gate (under the 6 h rule) and by the main session at 03:14:33 UTC (byte-identical to the scout's copy).
- Stretched criterion or hidden quantifier: none found by CRITERION; container convention and N verified; no tolerance.
- Scope wider than reproduced: the scope names one cell (d = 4, N = 66), one file, one value.
- Sample presented as complete, capped search as exclusion, probable prime as proof: not applicable (explicit object).
- Table value obtained by evasion: no; one plain curl per file with a V3R1T4S User-Agent, no retries, all HTTP 200;
  attempt code contains no fetching at all.
- Several objects bundled: no; the other 14 improved rows stay in the run folder as PROMISING (single-context, unpanelled).

## Not claimed

Optimality, a "record" in any sense beyond "strictly above the posted value in this 12-decimal table on this date", and
anything about hsp5/hsp6 or other N.
