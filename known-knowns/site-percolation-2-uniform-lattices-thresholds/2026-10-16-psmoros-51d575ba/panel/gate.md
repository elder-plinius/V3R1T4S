# Honesty gate (kit RUN.md step 7): p2 claim, row #22 bond, word TSS

Written by the main session of run 2026-10-16-0731 at 2026-10-16T09:54:40Z (date -u), after reading the three panel files above in
full. The claim package is claim/ of this folder (built 2026-10-16 about 06:52Z by the previous session, unchanged).

status: CONFIRMED_PARTIAL
partial_win: p2
confirmed_scope: For the bond threshold of row #22 of the 2-uniform table in Wikipedia's "Percolation threshold" article (lattice (2/3)(3^3,4^2) + (1/3)(4^4), built as the row tiling TSS), the claim's extrapolation of eigenvalue-form critical-polynomial roots on W x infinity cylinders (W = 2..10, reproduced here for W = 5..10) gives an independent estimate p_c = 0.445287065(21) whose one-sigma bar is a convergence-and-calibration estimate rather than a rigorous bound (23 alternative extrapolations all lie within 3.4e-8 of it), and this lies 9.6e-7 above the table's "citation needed" value 0.44528611(40), a discrepancy 2.4 times that value's stated error bar but within 3 combined sigma.

## Panel
- reproduce.md: pass: true (fresh subagent, model fable). Own lattice builder; own transfer-matrix code reproduces TSS
  W = 2..8 and TS W = 2..6 to <= 2.1e-15; both programs rebuilt and rerun, 38 values to <= 2.7e-15; own rule-4/9/v2
  code gives the claimed E1, sigma_B, sigma_v2 and verdict.
- novelty.md: pass: true (fresh subagent, model opus). Live table fetched once at 2026-10-16T07:52:05Z, HTTP 200,
  sha256 2f44ce40...7e95, identical to the claim's copy; row #22 bond 0.44528611(40) [citation needed]. Wikipedia history
  traces the value to an unpublished 2007 "Gu and Ziff, to be published" reference. No published bond value for this
  lattice found; no V3R1T4S pull request or trophy on percolation.
- criterion.md: pass: true (fresh subagent, model opus). Main branch of rule 4 applies; 23 alternative extrapolations
  within 3.4e-8; p2 met under both readings (rule 9 "confirms"; literally a discrepancy larger than the stated bar).

## Downgrade checks (RUN.md step 7)
- Hedging panelist: none. Caveats raised (E1 probably about 1e-8 high; 7th rounded digit not secure; eig kagome n = 5
  agrees to 4.3e-15, not 2.5e-15; Lebrecht et al. 2021 full text behind stopped hosts) are inside the stated scope.
- Reproduction mismatch: none (worst 2.7e-15).
- Strictly better than the live table: sigma 2.093e-8 against the table's 4e-7; no tie; table fetch 07:52:05Z, under
  6 h before this gate (this run's own scout fetch 07:42:06Z: same sha256).
- Stretched criterion or hidden quantifier: "7 digits" read as sigma <= 5e-8 (frozen rule 9, 03:03:58Z, before any
  computation); the claim's sentence asserts neither "confirms" nor "refutes" beyond the numbers.
- Scope wider than reproduced: the confirmed_scope says W = 5..10 reproduced by CRITERION; REPRODUCE reproduced W = 2..10.
- E3 choice of rule 4: the smuggler lens's NOTES.md (runs/2026-10-16-0245/attempts/smuggler/NOTES.md, section "Extrapolation
  rules fixed BEFORE looking at any 2-uniform sequence (03:45Z)") states the Richardson 4,6,8 E3 before the TSS bond
  results (03:49Z). It gives the larger of the two candidate sigmas.
- Evidence after the panel (this run, attempts/extender, a new memory-lean code validated to about 1e-15): TSS bond
  W = 11 gives p(11) = 0.44528707914717824 and E1(9,10,11) = 0.445287059999838 with sigma_v2 1.567e-8; the move from the
  claimed value is -5.46e-9, 0.26 of the claimed sigma. No downgrade.
- Table access by evasion: none (one GET per resource through the shared helper; stop list of this session empty when
  the panel ran).
- Bundling: one cell.

Final status: CONFIRMED_PARTIAL (p2). check_run.py must print CHECK_RUN: PASS for this folder and for the package
before this status stands.
