Frozen UTC: 2026-11-04T20:19:37Z
Search plan: 64 turbines only. Byte-identical copies of runs/2026-11-03-2334 code: attempts/optimizer64/code/quadruple_vacancies.py (sha256 e4400720...fdc9), attempts/coordinate64/code/insertion.py (138eaeb0...c3e), attempts/optimizer64/code/engine_search.py (59b039d8...4e). Start: own data/starting-own-64.json only (sha256 ecd78a907730e61668c9166d0f8f51f43e5d82831731c48c0e51e481434a4faa). Five seeds exchange only their own best.json files. No published coordinates (including PR #938) are loaded by the search. nice 10, hard timeout, PIDs recorded; search deadline 2026-11-04T21:15:00Z at the latest (earlier via STOP files if a hit is found).

Criterion targeted (verbatim, full success criterion, 64-turbine cell):
A layout for the 16-, 36- or 64-turbine scenario with every hub at distance at most R from (0,0) and every pair at least 260 m apart, both checked with no tolerance in double precision. Its AEP from the official iea37-aepcalc.py model (16-bin rose, constant 9.8 m/s, iea37-335mw.yaml) must be STRICTLY GREATER (direction: max) by at least 0.01 MWh than the posted record, used as posted even though it lies outside the boundary: 421561.8972 (16), 882383.3040 (36) or 1526474.8025 (64), and also strictly greater than every CONFIRMED V3R1T4S known-known for the same scenario at claim time. Re-check the known-knowns and open claims (PR #578 reports 424131.9503 at 16) immediately before claiming; a claim must state which of them it beats.

Statistic and thresholds:
1. Exactly 64 hubs; max radius <= 3000.0 m; min pair distance >= 260.0 m over 2016 pairs; exact rational re-check.
2. AEP from own validated evaluator AND the unmodified official iea37-aepcalc.py, agreeing within 1e-4 MWh, and >= 1539447.1274 MWh (PR #938's independently reproduced 1539447.1173686478 + 0.01, which also exceeds the posted record by >= 0.01).
3. Re-check V3R1T4S known-knowns and open PRs at claim time; the object must exceed every 64-turbine value found there.
4. Diagnostic: rigid-transform comparison against PR #938 and all posted opt64 layouts, to show the object is not a transformed copy of #938.
Stop rule: no panel unless 1-4 pass.
null_test: not needed because only deterministic properties of one explicit object would be claimed (no search-yield or statistical inference)
