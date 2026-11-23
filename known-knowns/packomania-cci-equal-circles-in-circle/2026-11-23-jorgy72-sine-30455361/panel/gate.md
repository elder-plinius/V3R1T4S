# Honesty gate — 2026-11-23

status: CONFIRMED_PARTIAL
confirmed_scope: polished01.txt's 50-digit feasible radius exceeds the live Packomania value for N=4405 by 3.607323049e-06 and its sorted pairwise-distance multiset differs from the posted seed's, with N=4405 outside the live queued cci ranges and absent from history updates newer than 22-Nov-2026.

## Panel tally
- panel/reproduce.md: pass: true (own mpmath 50-digit script from the
  definition, own live table re-fetch, margin +3.607323049e-06,
  PAIR term binds at circles (4130, 4394) 1-based, gap to second-closest
  pair 1.7399e-07; file sanity 4405 rows; polished03 independently
  reproduced at +2.03836019e-06). context: subagent.
- panel/novelty.md: pass: true (argue-against skeptic; own multiset
  recomputation max diff 2.426e-03, 99.9999% of 9,699,810 entries
  differ by >1e-9; live queue re-fetch — only cci lines Patankar
  652–3943 and Karl 126–4141, 4405 outside both; live cci.html
  byte-identical to the scout, history newest 22-Nov-2026; file
  integrity clean; polished01 sha256 30455361…; checker inspected, no
  flattering artifact — one non-killing observation: check() itself
  does not run the isometry comparison its docstring promises; the
  panel's independent multiset comparison closes that gap).
  context: subagent.
- panel/criterion.md: pass: true (literal (a)–(d) judgment; all four
  PASS; 12-decimal-vs-30-decimal subtlety judged — the live bar is the
  stricter one and the claim clears it; mp.nstr 31-digit printing
  leaves no gap that could matter at the 1e-11 bar; scope guard
  respected — carrier polished01.txt only; margin-reporting rule
  verified). context: subagent.
- Main-session verification: SURVIVES (own 50-digit checker run:
  margin +3.607e-06; verify_claim.py float64 + mpmath-on-binding-terms
  agrees to all printed digits, PAIR binds at (4129, 4393) 0-based,
  gap to second-closest pair 1.7399e-07, wall 2.24e-06 above; own
  non-isometry max diff 2.426e-03, 100% of 9,699,810 pairs differ
  by >1e-9; queue/table/history re-verified live at verification time;
  all four verification-time re-fetches byte-identical to the scout).

## True 50-digit values (agreed by three independent computations)
- r* = 0.01419381937604937731901147206750715011991 (reproduce, novelty,
  criterion judges and main-session checker all agree to all printed
  digits; PAIR term binds at circles (4130, 4394) 1-based;
  pair term 0.01419381937604937731901147206750715011991;
  wall term 0.0141960620906344455531287505440639736866 for circle 4394,
  pair-wall gap 2.2427e-06).
- Margin = +3.607323049e-06 vs the live 12-decimal table value
  0.014190212053, i.e. 360,732x the 1e-11 bar. Margin vs the archived
  30-decimal value 0.014190212052536014904153227050 would be
  +3.607323513e-06 — also far above the bar. The claim clears the
  stricter live bar.
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
- Seed check: the posted seed reproduces its table row to ~1e-12
  (-1.046e-12 vs the live 12-decimal table; -5.817e-13 vs the archived
  30-decimal value) — the posted coordinates' 12-decimal rounding, as
  expected; the seed is isometric to itself, so no claim question
  arises. PREREG's criterion (c) is satisfied: the newest History entry
  is the 22-Nov-2026 Specht wave (N=259..998), and no entry touches
  N=4405.

## Narrow-walk lens
NOT RUN. The verified above-bar claim supersedes the walk per the
prereg (same as 2026-11-17, 2026-11-18, 2026-11-19 and 2026-11-20).

## Second above-bar file
polished03.txt (+2.03836019e-06, 50-digit certified, r* =
0.01419225041318986275009834058249294798707) stays banked, not bundled,
per the scope guard (one carrier per claim).

check_run.py --run: see run REPORT.md (must print CHECK_RUN: PASS
for anything to be reported; this run reports CONFIRMED_PARTIAL).
