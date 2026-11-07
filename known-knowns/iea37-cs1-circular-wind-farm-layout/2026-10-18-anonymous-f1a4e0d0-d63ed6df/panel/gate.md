# Honesty gate (Sun Oct 18 03:29:20 UTC 2026)
Read by the run's main session: reproduce.md (pass: true), novelty.md (pass: true), criterion.md (pass: true); each
written by a fresh subagent that saw only a copy of claim/.
Downgrade checks: reproduction exact (own checker from the PDFs, exact-rational constraint check, official evaluator
3 runs byte-identical); value 1539447.11737 strictly above the live table's best 1526474.80248 (NOVELTY re-fetched the
official results tree at 2026-10-18T03:20:29Z, < 6 h old, same sha256 as scout); no table value obtained by evasion
(single honest GETs; one 301 followed; no 4xx retries); one object; criterion read literally ("on or within",
2 rotor diameters, unmodified evaluator); scope kept exactly as CRITERION wrote it; the result is not a polish of
par12 (RMS 208.8 m to nearest par12 hub; only 2 hubs within 10 m), though its search was seeded from par12's basin.
Recorded caveats (do not change the status, must accompany every mention): (1) like every entry, the layout exploits
the 16-bin wind rose: rotating the rose by 1 degree costs 0.5 %, by 5 degrees 11-14 %; (2) the search started from a
repaired par12, although chains that never saw par12 also beat it (1533259, 1528741); (3) boundary hubs sit 1e-6 m
inside: copies must keep full float precision (rounding to 3-4 decimals pushes them outside); (4) NOVELTY could not
read one aggregator page (rsi-bench.duckdns.org, DNS failure, not retried); (5) cosmetic: claim/REPRODUCE.md calls
check_constraints.py "20 lines", it has 11; (6) not submitted anywhere (IEA37 case study closed in 2019; any
publication is the human's choice).
status: CONFIRMED_SOLUTION
confirmed_scope: The single 64-turbine layout in object/iea37-v3r1t4s-opt64.yaml (sha256 d63ed6df...dd93c851) lies on or within the 3000 m boundary with every pair at least 260 m apart in float64, and the unmodified iea37-aepcalc.py run on it with the official wind-rose and turbine files gives 1539447.11737 MWh, strictly above every 64-turbine value in the package's table and papers (highest 1526474.80248 for participant 12, published winner 1513311.19361).

---
Note added 2026-11-07 (UTC) at the maintainer's request on V3R1T4S PR #938, after the gate.
In the confirmed_scope line above, the path claim/object/iea37-v3r1t4s-opt64.yaml was changed to
object/iea37-v3r1t4s-opt64.yaml (the same file, sha256 d63ed6df...dd93c851) so that README.md quotes it word for word.
No other word above this note was changed. Its paths are relative to the run folder runs/2026-10-18-0107/, not to this package.
In this package, claim/object/iea37-v3r1t4s-opt64.yaml and claim/object/layout64.json are object/iea37-v3r1t4s-opt64.yaml
and object/layout64.json. These are not in this package, by design: claim/evaluator/ (the official IEA37 files,
including iea37-aepcalc.py; RUN_IT_YOURSELF.md says where to download them) and the run's check_constraints.py (this
package's own checker is verify-it-yourself/check_layout.py); claim/table/ (the results-folder snapshot, whose URL,
fetch times and sha256 are in the-record-we-beat/record.md); claim/scratch/; and the run's CLAIM.md and REPRODUCE.md
(README.md and RUN_IT_YOURSELF.md cover the same ground).
