# Honesty gate (run main session), 2026-10-24T22:07:27Z

status: CONFIRMED_PARTIAL
confirmed_scope: In a map that reruns byte-for-byte offline from the saved code and data, of the 264 USGS ComCat M >= 6.5, depth <= 70 km earthquakes of 2015-2025 whose epicentre lies in an ETOPO1 2-arcmin water cell, 188 could be scored at open IOC SLSMF tide gauges within 1000 km (model travel time 10-150 min, at least one usable site, and no other M >= 6.5, depth <= 70 km ComCat earthquake, land or sea, within 1000 km in the preceding 24 h; 25 had no gauge in scope, 17 had no usable data and 34 were set aside by that post-hoc 24 h rule), and 26 of the 188 (0.138, Wilson 95 % 0.096-0.195; 26 of 221 = 0.118 without the post-hoc 24 h rule; 35 of 221 = 0.158 under the pre-registered v4 rules) passed, at one or more sites and on every usable tied sensor, the target's per-gauge test (band-passed peak above 5 times the preceding 24 h RMS, arrival within +/-10 min of a model travel time that puts 0.468 of held-out NCEI tide-gauge arrivals outside +/-10 min, and no peak above 5 times RMS in the same hours on any of at least 10 usable control days), which is a test-pass fraction and not the fraction with any observable tsunami signal, against a fake-origin chance rate of 0.027 (best of 400 fake catalogues 0.0495), with 24 of the 26 listed by NCEI (an NCEI event of any validity or cause within +/-1 day and 1000 km, events snapshot of 2026-10-24T19:20Z) and the 2 unlisted ones passing at a single site, as many as chance predicts (2.8 expected among the 102 unlisted scored quakes).

Partial win p3 (completeness map) of tsunami-tide-gauge-signal-not-in-ncei. Panel round 2, three fresh Opus contexts run
one after another: reproduce.md pass: true, novelty.md pass: true, criterion.md pass: true.

Downgrade checks:
- Hedging panelist: none. NOVELTY states where the claim does not beat issue #253's run 4 (listed recall 45/82 against
  24/86, 195 against 188 scored); run 4 was posted without code, unpanelled and unclaimed, at a looser test, so it does not
  provide p3 "reproducible from saved code". Not a tie and not subsumed; the gate accepts NOVELTY's judgement.
- Reproduction mismatch: none in any result. REPRODUCE's open item: CLAIM.md says "31 IOC GETs (1.0 MB)" while the bundle
  holds 29 files fetched after the PREREG.v6 freeze (973,170 bytes). The fetch log has 31 GETs for 30 distinct URLs (one
  window, char2 2018-10-13T22:00-10-14T05:00, fetched twice in the same second by the two map shards, same bytes) and one
  window (lpbc 2018-10-14T00:00-04:00, 16,324 bytes) that the offline rerun does not read because an overlapping window
  covers it: 1,014,686 - 25,192 - 16,324 = 973,170. The statement is true as written; no result depends on it.
- Value not strictly better than a live table: p3 has no record number; no prior p3 claim, confirmation or merge
  (NOVELTY, GitHub API and TROPHY_CASE.md at 2026-10-24T21:4xZ; status page re-fetched 21:43:20Z, unchanged sha256).
- Stretched criterion or hidden quantifier: CRITERION names them (test-pass fraction, IOC SLSMF within 1000 km, the
  post-hoc overlap rule, the generous LISTED rule) and its confirmed_scope carries each; the gate uses it verbatim.
- Scope wider than reproduced, sample as complete, capped search, probable prime, table access by evasion, bundling: none.
  Every quake at every origin was checked by REPRODUCE's own code (792 origins, 0 class mismatches).
- Panel table fetch age: under 1 hour (NOVELTY 21:43:20Z), so no re-fetch.

History, disclosed: panel round 1 (panel_round1/reproduce.md) failed the as-run v5 map on three code departures from the
frozen text; NOVELTY and CRITERION were not started for it. Repair round 2 (PREREG.v6, frozen 20:56:56Z) corrected the code
only; no class changed at any origin; self-break round 3 SURVIVES (self_break/round3/verdict.md); then this fresh panel.
This status stands only if check_run.py prints CHECK_RUN: PASS.
