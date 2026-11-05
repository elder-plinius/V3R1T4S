# Honesty gate — 2026-11-05

status: CONFIRMED_PARTIAL
confirmed_scope: object/candidate_n4153.txt's 50-digit feasible radius exceeds the live Packomania value for N=4153 by 2.706e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4153 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

## Panel tally
- panel/reproduce.md: pass: true (own mpmath 50-digit script from the
  definition, own live table re-fetch, margin +2.70581765756971e-06,
  binding term the boundary; file sanity 4153 rows). context: subagent.
- panel/novelty.md: pass: true (argue-against skeptic; own multiset
  recomputation max diff 3.178732e-03; live queue re-fetch — only cci
  lines Patankar 652–3943 and Karl 126–4141, 4153 outside both; live
  cci.html byte-identical to the scout, history newest 11-Oct-2026;
  file integrity clean; stale-margin blemish in polish logs noted,
  claimed value is the recomputed/certified one). context: subagent.
- panel/criterion.md: pass: true (literal (a)–(d) judgment; all four
  PASS; bank FULL CRITERION MET, p2 also fits but subsumed; scope
  guard respected — carrier object/candidate_n4153.txt only). context: subagent.
- Main-session verification: SURVIVES (own 50-digit checker run:
  margin 2.706e-06; two independent double evaluators agree
  +2.705818e-06; own non-isometry max diff 3.179e-03; queue/table
  re-verified live at verification time).

## Downgrade checks
- Hedging panelist: no. No panelist hedged; the criterion judge's
  FULL CRITERION MET ruling is recorded below as a disagreement, not
  a hedge.
- Reproduction mismatch: no. Five independent computations agree
  (main session double x2 + 50-digit, REPRODUCE 50-digit, NOVELTY
  double + 50-digit + fresh checker run, CRITERION double + 50-digit).
- Value strictly better than the live table: yes, +2.706e-06 ≥ 1e-11
  (270,582x headroom).
- Stretched criterion / hidden quantifier: none found.
- Scope wider than reproduced: no; confirmed_scope is the single
  object/candidate_n4153.txt at N=4153.
- Sample presented as complete: no (full O(N^2) checks, not samples).
- Table value obtained by evasion: no (single plain curls of the public table
  files; the reproduce fetch used a browser UA, the novelty fetch used an
  honest V3R1T4S-skeptic UA — no login, no bypass).
- Panel table fetch age at gate: under 1 h. No re-fetch needed.
- Bundling: one object, one cell (N=4153); the three other above-bar
  polished files are cited, not bundled.

## Why PARTIAL and not SOLUTION
The bank's enumerated partial win p2 exactly describes this object
("a certified improvement for one of the gap values N > 2600 ...
where the record is a lattice-like seed by Specht"; "e.g. N=4495,
5000" is non-exhaustive, and N=4153 is such a gap value with a
Specht-authored seed). Per RULES 4 (statuses only go down; never
upgrade), the gate takes the bank's own taxonomy at face value:
CONFIRMED_PARTIAL — the same reading as the 2026-10-20 gate for
N=3949. Recorded disagreement: the CRITERION skeptic argued the
full success criterion is also met literally and p2 is subsumed; the
gate downgrades on the taxonomy reading and keeps the
confirmed_scope exactly as written above.

## Verdict
CONFIRMED_PARTIAL. Proceed to packaging (outbox/), then check_run.py --package.
Credit: E. Specht (Packomania table + posted seed); Jorgy72 & Sine.
