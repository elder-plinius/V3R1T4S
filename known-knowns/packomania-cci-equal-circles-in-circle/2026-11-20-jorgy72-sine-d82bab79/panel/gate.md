# Honesty gate — 2026-11-20

status: CONFIRMED_PARTIAL
confirmed_scope: object/candidate_n4357.txt's 50-digit feasible radius exceeds the live Packomania value for N=4357 by 4.93845300182e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4357 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

## Panel tally
- panel/reproduce.md: pass: true (own mpmath 50-digit script from the
  definition, own live table re-fetch, margin +4.938453002e-06,
  WALL term binds at circle 4348, binding pair (4110, 4348), gap to
  second-closest pair 3.053e-07; file sanity 4357 rows; polished00
  independently reproduced at -2.348462829e-07). context: subagent.
- panel/novelty.md: pass: true (argue-against skeptic; own multiset
  recomputation max diff 3.765097e-03, 99.9999% of 9,489,546 entries
  differ by >1e-9; live queue re-fetch — only cci lines Patankar
  652–3943 and Karl 126–4141, 4357 outside both; live cci.html
  byte-identical to the scout, history newest 11-Oct-2026; file
  integrity clean; polished01 sha256 d82bab79…; checker inspected, no
  flattering artifact — see below). context: subagent.
- panel/criterion.md: pass: true (literal (a)–(d) judgment; all four
  PASS; bank FULL CRITERION MET literally, p2 also fits — precedence
  unresolved in the bank text; scope guard respected — carrier
  polished01.txt only; margin-reporting rule verified). context: subagent.
- Main-session verification: SURVIVES (own 50-digit checker run:
  margin +4.938e-06; verify_claim.py float64 + mpmath-on-binding-terms
  agrees to all printed digits, wall binds, binding pair (4109, 4347);
  own non-isometry max diff 3.765e-03, 100% of 9,489,546 pairs differ
  by >1e-9; queue/table/history re-verified live at verification time;
  all three verification-time re-fetches byte-identical to the scout).

## True 50-digit values (agreed by three independent computations)
- r* = 0.01426010900644796452099252854563731797493935762124 (reproduce,
  novelty, criterion judges all agree to all printed digits; WALL term
  binds at center 4347, wall term 0.014260109006447964520992528545637;
  pair term 0.014260414315076214818780048668902 for binding pair
  (4109, 4347), pair-wall gap 3.053e-07).
- Margin = +4.93845300182e-06, i.e. 493,845x the 1e-11 bar.
- The run's check50 logs print r*/table via the checker's mp.nstr(...,
  31) prints — 31 significant digits, not 50 (the 2026-11-18 lesson was
  applied: mp.nstr, never float(); the novelty skeptic notes the
  remaining 31-vs-50 wording gap). Print truncation is ~1e-33 absolute;
  the largest conceivable artifact is bounded at ~1e-30 — 19 orders
  below the bar, 24 orders below the margin. The package's verify.py
  computes with the decimal module from the exact strings (no binary
  float) and its INDEX.csv carries the true r*. The check50 logs are
  not the sole 50-digit certification; the genuine certification is the
  three panel computations plus the main-session checker run.
- Seed check: the posted seed reproduces its table row to ~1e-30
  (-3.436e-31 by the run's checker; +2.1e-32 by the criterion judge —
  the difference is which term binds at 50 digits), i.e. the posted
  coordinates' 30-decimal rounding, 19 orders below the bar. PREREG's
  "reproduces at 50 digits" wording is loose; the precise statement is
  "reproduces to ~1e-30".

## Downgrade checks
- Hedging panelist: no. No panelist hedged; the criterion judge's
  FULL CRITERION MET ruling is recorded below as a disagreement, not
  a hedge.
- Reproduction mismatch: no. Six independent computations agree
  (main session double + 50-digit checker + verify_claim binding-term
  recomputation, REPRODUCE 50-digit, NOVELTY double + 50-digit,
  CRITERION double + 50-digit).
- Value strictly better than the live table: yes, +4.93845300182e-06 >=
  1e-11 (493,845x headroom).
- Stretched criterion / hidden quantifier: none found.
- Scope wider than reproduced: no; confirmed_scope is the single
  object polished01.txt at N=4357.
- Sample presented as complete: no (full O(N^2) checks, not samples).
- Table value obtained by evasion: no (single honest curls, honest UA).
- Panel table fetch age at gate: under 1 h. No re-fetch needed.
- Bundling: one object, one cell (N=4357); there is no second above-bar
  polished file this night (polished00 is below the bar at -2.348e-07,
  cited as work history, not bundled).

## Why PARTIAL and not SOLUTION
The bank's enumerated partial win p2 exactly describes this object
("a certified improvement for one of the gap values N > 2600 ... where
the record is a lattice-like seed by Specht"; N=4357 is such a gap value
with a Specht-authored seed). Per RULES 4 (statuses only go down; never
upgrade), the gate takes the bank's own taxonomy at face value:
CONFIRMED_PARTIAL — the same reading as the 2026-10-20 gate for N=3949,
the 2026-11-05 gate for N=4153, the 2026-11-17 gate for N=4315, the
2026-11-18 gate for N=4339, and the 2026-11-19 gate for N=4345.
Recorded disagreement: the CRITERION skeptic argued the full success
criterion is also met literally and p2 is subsumed; the gate downgrades
on the taxonomy reading and keeps the confirmed_scope exactly as written
above.

## Verdict
CONFIRMED_PARTIAL. Proceed to packaging (outbox/), then check_run.py --package.
Credit: E. Specht (Packomania table + posted seed); Jorgy72 & Sine.
