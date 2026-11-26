# Honesty gate — 2026-11-17

status: CONFIRMED_PARTIAL
confirmed_scope: object/candidate_n4315.txt's 50-digit feasible radius exceeds the live Packomania value for N=4315 by 1.006294675e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4315 outside the live queued cci ranges and absent from history updates newer than 11-Oct-2026.

## Panel tally
- panel/reproduce.md: pass: true (own mpmath 50-digit script from the
  definition, own live table re-fetch, margin +1.0062946747e-06,
  binding pair (3823, 4061), pairwise term binds; file sanity 4315 rows).
  context: subagent.
- panel/novelty.md: pass: true (argue-against skeptic; own multiset
  recomputation max diff 6.607512e-03, 100% of 9,307,455 entries differ
  by >1e-9; live queue re-fetch — only cci lines Patankar 652–3943 and
  Karl 126–4141, 4315 outside both; live cci.html byte-identical to the
  scout, history newest 11-Oct-2026; file integrity clean; check50
  float-print artifact found and bounded, see below). context: subagent.
- panel/criterion.md: pass: true (literal (a)–(d) judgment; all four
  PASS; bank FULL CRITERION MET literally, p2 also fits — precedence
  unresolved in the bank text; scope guard respected — carrier
  polished00.txt only). context: subagent.
- Main-session verification: SURVIVES (own 50-digit checker run:
  margin +1.006e-06; two independent double evaluators agree
  +1.006e-06; own non-isometry max diff 6.608e-03; queue/table/history
  re-verified live at verification time; all three verification-time
  re-fetches byte-identical to the scout).

## True 50-digit values (agreed by three independent computations)
- r* = 0.01432454777069287128759443799585792968662 (reproduce, novelty,
  criterion judges all agree to ~1e-15; binding pair (3823, 4061),
  pairwise term binds; wall term 0.0143246492317705051 is larger).
- Margin = +1.0062946746985619e-06, i.e. 100,629x the 1e-11 bar.
- The run's check50 logs print r*/table via the checker's float-rounded
  `%.30f` prints (float(r_star)), so their printed values are off by
  ~6.8e-19 (r*) and +4.679e-19 (table) from the true 50-digit values.
  The artifact is 12 orders below the margin and 7 orders below the bar;
  it changes no digit of the claim at any reported precision. The
  package's verify.py computes with the decimal module from the exact
  strings (no binary float) and its INDEX.csv carries the true r*.
  The check50 logs are not cited as 50-digit certification; the genuine
  50-digit certification is the three panel computations plus the
  main-session checker run (whose margin print, +1.006e-06, agrees to
  ~1e-15). Lesson for the next run: print mpmath values with
  mp.nstr, never via float().
- Seed check: the posted seed reproduces its table row to ~1e-31
  (-5.874e-31 by the criterion judge's exact script; -8.5e-32 by the
  novelty skeptic's — the difference is which term binds at 50 digits),
  i.e. the posted coordinates' 30-decimal rounding, 21 orders below
  the bar. PREREG's "reproduces at 50 digits" wording is loose; the
  precise statement is "reproduces to ~1e-31".

## Downgrade checks
- Hedging panelist: no. No panelist hedged; the criterion judge's
  FULL CRITERION MET ruling is recorded below as a disagreement, not
  a hedge.
- Reproduction mismatch: no. Six independent computations agree
  (main session double x2 + 50-digit checker, REPRODUCE 50-digit,
  NOVELTY double x2 + 50-digit, CRITERION double + 50-digit).
- Value strictly better than the live table: yes, +1.006294675e-06 >=
  1e-11 (100,629x headroom).
- Stretched criterion / hidden quantifier: none found.
- Scope wider than reproduced: no; confirmed_scope is the single
  object polished00.txt at N=4315.
- Sample presented as complete: no (full O(N^2) checks, not samples).
- Table value obtained by evasion: no (single honest curls, honest UA).
- Panel table fetch age at gate: under 1 h. No re-fetch needed.
- Bundling: one object, one cell (N=4315); the other above-bar polished
  file (polished01, +9.735e-07, independently 50-digit certified by
  the novelty skeptic at +9.734751654e-07) is cited, not bundled.

## Why PARTIAL and not SOLUTION
The bank's enumerated partial win p2 exactly describes this object
("a certified improvement for one of the gap values N > 2600 ... where
the record is a lattice-like seed by Specht"; N=4315 is such a gap value
with a Specht-authored seed). Per RULES 4 (statuses only go down; never
upgrade), the gate takes the bank's own taxonomy at face value:
CONFIRMED_PARTIAL — the same reading as the 2026-10-20 gate for N=3949
and the 2026-11-05 gate for N=4153. Recorded disagreement: the
CRITERION skeptic argued the full success criterion is also met literally
and p2 is subsumed; the gate downgrades on the taxonomy reading and keeps
the confirmed_scope exactly as written above.

## Verdict
CONFIRMED_PARTIAL. Proceed to packaging (outbox/), then check_run.py --package.
Credit: E. Specht (Packomania table + posted seed); Jorgy72 & Sine.
