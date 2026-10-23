# Honesty gate — 2026-10-20T10:1xZ (main session)

status: CONFIRMED_PARTIAL
confirmed_scope: Candidate_n3949.txt's 50-digit feasible radius exceeds the record-quoted live Packomania value for N=3949 by 2.372e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=3949 outside the record-quoted queued cci ranges and absent from record-quoted history updates — but the Moki & Julio "*many*" category-unspecified pending bundle leaves the queue rule unresolved until the bundle disappears and the criterion's required re-check happens.

## Panel tally
- panel/reproduce.md: pass: true (own checker from the definition, own 50-digit spot check,
  non-isometry recomputed, SHA256SUMS ok). context: subagent.
- panel/novelty.md: pass: true (live table re-fetched 2026-10-20T09:54:13Z, value identical;
  queue re-checked 09:54:21Z, N=3949 outside cci 652–3943; history clean; 24-month
  literature + trophy case + 30 open PRs clean). context: subagent.
- panel/criterion.md: pass: true (literal (a)–(g) judgment; null-test waiver agreed).
  context: subagent.
- Main-session Step-5 adversarial re-check: SURVIVES (own 50-digit checker run:
  margin 2.372e-06; own non-isometry: max diff 0.0051; queue/history re-verified live
  2026-10-20T09:52:24Z).

## Downgrade checks (Step 7)
- Hedging panelist: no. The Moki & Julio caveat is the bank criterion's own prescribed
  path (state the caveat + re-check later), not a hedge.
- Reproduction mismatch: no. Four independent computations agree (main session double +
  50-digit, REPRODUCE double + 50-digit spot, CRITERION double + 50-digit run).
- Value strictly better than the live table: yes, +2.372e-06 ≥ 1e-11 (5 orders of headroom).
- Stretched criterion / hidden quantifier: none found (CRITERION (g)).
- Scope wider than reproduced: no; confirmed_scope is the CRITERION sentence verbatim.
- Sample presented as complete: no (full O(N²) checks, not samples).
- Table value obtained by evasion: no (single honest curls, honest UA, no retries).
- Panel table fetch age at gate: ~20 min (< 6 h). No re-fetch needed.
- Bundling: one object, one cell (N=3949).

## Why PARTIAL and not SOLUTION
The bank's enumerated partial win p2 exactly describes this object ("a certified
improvement for one of the gap values N > 2600 ... where the record is a lattice-like
seed by Specht"; "e.g. N=4495, 5000" is non-exhaustive, and N=3949 is such a gap value
with a Specht-authored seed). Per RULES 4 (statuses only go down; never upgrade), the
gate takes the bank's own taxonomy at face value: CONFIRMED_PARTIAL. Recorded
disagreement: the CRITERION skeptic argued the full success criterion is also met
literally; the gate downgrades on the taxonomy reading and keeps the confirmed_scope
exactly as the panelist wrote it.

## Mechanical note (before the gate, verdict unaffected)
panel/novelty.md line 46 contained one absolute workspace path; replaced with a relative
reference ("repo/TROPHY_CASE.md") so the package passes the leak scan. No finding changed.

## Verdict
CONFIRMED_PARTIAL. Proceed to packaging (outbox/), then check_run.py --package.
Credit: E. Specht (Packomania table + posted seed); Jorgy72 & Sine.
