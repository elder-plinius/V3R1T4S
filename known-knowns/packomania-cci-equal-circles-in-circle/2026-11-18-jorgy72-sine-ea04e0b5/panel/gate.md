# Honesty gate — 2026-11-18

status: CONFIRMED_PARTIAL
confirmed_scope: object/candidate_n4339.txt's 50-digit feasible radius exceeds the live Packomania value for N=4339 by 1.014393041e-05 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4339 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

## Panel tally
- panel/reproduce.md: pass: true (own mpmath 50-digit script from the
  definition, own live table re-fetch, margin +1.014393040862e-05,
  binding pair (3861, 4096), pairwise term binds; file sanity 4339 rows).
  context: subagent.
- panel/novelty.md: pass: true (argue-against skeptic; own multiset
  recomputation max diff 3.048e-03, 100% of 9,411,291 entries differ
  by >1e-9; live queue re-fetch — only cci lines Patankar 652–3943 and
  Karl 126–4141, 4339 outside both; live cci.html byte-identical to the
  scout, history newest 11-Oct-2026; file integrity clean; polished03
  independently certified +8.34515568667e-06; check50 float-print
  artifact found and bounded, see below). context: subagent.
- panel/criterion.md: pass: true (literal (a)–(d) judgment; all four
  PASS; bank FULL CRITERION MET literally, p2 also fits — precedence
  unresolved in the bank text; scope guard respected — carrier
  polished00.txt only). context: subagent.
- Main-session verification: SURVIVES (own 50-digit checker run:
  margin +1.014e-05; two independent double evaluators agree
  +1.01439304086e-05; own non-isometry max diff 3.048e-03, 100% of
  9,411,291 pairs differ by >1e-9; queue/table/history re-verified live
  at verification time; all three verification-time re-fetches
  byte-identical to the scout).

## True 50-digit values (agreed by three independent computations)
- r* = 0.01428914037842894912706195794112189732227 (reproduce, novelty,
  criterion judges all agree to ~1e-15; binding pair (3861, 4096),
  pairwise term binds; wall term 0.01428914971938918257 is larger).
- Margin = +1.01439304086e-05, i.e. 1,014,393x the 1e-11 bar.
- The run's check50 logs print r*/table via the checker's float-rounded
  `%.30f` prints (float(r_star)), so their printed values are off by
  ~7e-19 (r*) from the true 50-digit values. The artifact is 13 orders
  below the margin and 7 orders below the bar; it changes no digit of
  the claim at any reported precision. The package's verify.py computes
  with the decimal module from the exact strings (no binary float) and
  its INDEX.csv carries the true r*. The check50 logs are not cited as
  50-digit certification; the genuine 50-digit certification is the
  three panel computations plus the main-session checker run (whose
  margin print, +1.014e-05, agrees to ~1e-15). Lesson (carried):
  print mpmath values with mp.nstr, never via float().
- Seed check: the posted seed reproduces its table row to ~1e-30
  (-1.100e-30 by the run's checker; -1.10048e-30 by the novelty
  skeptic; -8.84e-31 by the criterion judge — the difference is which
  term binds at 50 digits), i.e. the posted coordinates' 30-decimal
  rounding, 19 orders below the bar. PREREG's "reproduces at 50 digits"
  wording is loose; the precise statement is "reproduces to ~1e-30".

## Downgrade checks
- Hedging panelist: no. No panelist hedged; the criterion judge's
  FULL CRITERION MET ruling is recorded below as a disagreement, not
  a hedge. (The reproduce skeptic noted honestly that |its margin −
  the 4-significant-figure quoted claim| = 3.93e-9 literally exceeds
  the 1e-9 alarm threshold — but that is rounding residue of the
  quoted value, not a discrepancy; its margin agrees with the claim
  to every digit the claim states.)
- Reproduction mismatch: no. Six independent computations agree
  (main session double x2 + 50-digit checker, REPRODUCE 50-digit,
  NOVELTY double x2 + 50-digit, CRITERION double + 50-digit).
- Value strictly better than the live table: yes, +1.014393041e-05 >=
  1e-11 (1,014,393x headroom).
- Stretched criterion / hidden quantifier: none found.
- Scope wider than reproduced: no; confirmed_scope is the single
  object polished00.txt at N=4339.
- Sample presented as complete: no (full O(N^2) checks, not samples).
- Table value obtained by evasion: no (single honest curls, honest UA).
- Panel table fetch age at gate: under 1 h. No re-fetch needed.
- Bundling: one object, one cell (N=4339); the other above-bar polished
  file (polished03, +8.34515568667e-06, independently 50-digit certified
  by the novelty skeptic) is cited, not bundled.

## Why PARTIAL and not SOLUTION
The bank's enumerated partial win p2 exactly describes this object
("a certified improvement for one of the gap values N > 2600 ... where
the record is a lattice-like seed by Specht"; N=4339 is such a gap value
with a Specht-authored seed). Per RULES 4 (statuses only go down; never
upgrade), the gate takes the bank's own taxonomy at face value:
CONFIRMED_PARTIAL — the same reading as the 2026-10-20 gate for N=3949,
the 2026-11-05 gate for N=4153, and the 2026-11-17 gate for N=4315.
Recorded disagreement: the CRITERION skeptic argued the full success
criterion is also met literally and p2 is subsumed; the gate downgrades
on the taxonomy reading and keeps the confirmed_scope exactly as written
above.

## Verdict
CONFIRMED_PARTIAL. Proceed to packaging (outbox/), then check_run.py --package.
Credit: E. Specht (Packomania table + posted seed); Jorgy72 & Sine.
