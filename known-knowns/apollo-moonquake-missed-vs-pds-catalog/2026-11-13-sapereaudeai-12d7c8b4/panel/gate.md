# Honesty gate (kit/RUN.md step 7), run main session

target: apollo-moonquake-missed-vs-pds-catalog
partial win: p1 (nest A39, S14, 1971-09-05 01:25:44.150 UTC window)
time: 2026-11-13T06:18:07Z
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three fresh subagent contexts that saw only claim/)
table fetch age: status source and levent fetched by the claimant at 2026-11-13T05:52:08-09Z; all 11 tables re-fetched by NOVELTY at 05:57:39-05:57:55Z and index and levent by CRITERION at about 06:07Z, all byte-identical; less than 6 h old.

Downgrade checks (none triggered):
- hedging panelist: no. REPRODUCE passes and lists sensitivities: the result rests on the pre-registered best-channel reading (MH1 0.595), and the fixed-template half-sample test (0.613 / 0.349, results/decimation_phase_A39_A38.txt) is in results/ but not quoted in CLAIM.md. CRITERION explains that test as the 1.2 s carrier oscillation of the narrow-band NCC; the pre-registered fair test D1 (templates rebuilt on the other grid) gives 0.600 / 0.690. Both are disclosed in the package.
- reproduction mismatch: no. Claim code exact; full-span null bit-identical over 330 days (C0 0.2205, best control 0.3180); independent code within 1e-4; A39 stack bit-identical; G1/G2 identical.
- stretched criterion or hidden quantifier: no. CRITERION accepts the CC bar under both station-level readings (best channel 0.693; two-channel mean 0.644) and covers the bank's shift null in single-station form (between-channel 1-23 h shift 0.529 over all 25 templates) and a 25-template time-reversed control (0.246), all below 0.644.
- value not strictly better / table by evasion: no. NOVELTY read the live PDS tables (no row within +/- 5 min; levent empty on 1971 days 247-248), every readable expanded list of the last 24 months, and all nine S14 files of the Liu, Xiao and Li 2025 glitch catalogue (Spike, Step-Up, Step-Down on MH1/MH2/MHZ): no overlap.
- unresolved baseline: not applicable (existence claim).
Disclosures for the report and package: levent has no rows from 1971-09-03 22:57 to 1971-09-06 19:12 (a catalogue-coverage gap, one of five longer than 2.5 days in 1971); the onset carries a one-cycle (about 1.2 s) ambiguity; the detection is a few-DU signal; fast_null.py equals score_scan.py on 1971-248 to the 1e-5 rounding (and on day 290, REPRODUCE).

status: CONFIRMED_PARTIAL
confirmed_scope: On Apollo station S14 alone (long-period MH1/MH2, PDS MiniSEED, frozen phase-0 pipeline), the 450 s window starting 1971-09-05 01:25:44.150 UTC (onset 01:26:14 UTC, about +/- 1.2 s cycle ambiguity) matches the frozen S14 stack of sixteen catalogued 1971 A39 deep-moonquake events with NCC 0.693 on MH2 and 0.595 on MH1 (mean 0.644); this mean exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.221 for A39, 0.246 over all 25 searched nest templates), of 400 phase-randomised A39 templates (0.318) and of a between-channel 1-23 h shift control (0.529 over all 25 templates); no other of the 25 templates exceeds 0.18 there, it passes the pre-registered gap, thermal and glitch checks (including no overlap with the Liu, Xiao and Li 2025 S14 ACC-Spike catalogue), and no row of the 11 PDS Apollo seismic event catalogue tables lies within +/- 5 min of it, so it is a single-station (p1) detection of an A39 member absent from the PDS catalogue, not a multi-station or located event, and not checked here against the literature clause.
