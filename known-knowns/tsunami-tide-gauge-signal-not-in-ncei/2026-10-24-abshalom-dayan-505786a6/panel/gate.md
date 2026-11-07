# Honesty gate (run main session), 2026-10-24T22:07:27Z

status: CONFIRMED_PARTIAL
confirmed_scope: In a map scored under the rules pre-registered before scoring (PREREG.md to PREREG.v4), of the 264 USGS ComCat M >= 6.5, depth <= 70 km earthquakes of 2015-2025 whose epicenter lies in an ETOPO1 2-arcmin water cell, 221 could be scored at open IOC SLSMF tide gauges within 1000 km (model travel time 10-150 min and at least one usable site; 25 had no gauge in scope and 18 had no usable data), and 35 of the 221 (0.158, Wilson 95 % 0.116-0.212; 1 more of the 221 is undecided, with fewer than 10 usable control days) passed, at one or more sites, the target's per-gauge test on the gauge's most-sampled sea-level sensor (band-passed peak above 5 times the preceding 24 h RMS, arrival within +/-10 min of a model travel time that puts 0.468 of held-out NCEI tide-gauge arrivals outside +/-10 min, and the same test passing on none of at least 10 usable control days), which is a test-pass fraction and not the fraction with any observable tsunami signal, against a fake-origin chance rate of 23 of 437 = 0.053 (best of 400 fake catalogs 0.078), with 33 of the 35 listed by NCEI (an NCEI event of any validity or cause dated within 1 calendar day of the origin and within 1000 km, or without coordinates; the same flags against the live events API on 2026-11-07) and the 2 unlisted ones passing at a single site, fewer than chance predicts (5.9 expected among the 113 unlisted scored quakes).

Scope revised 2026-11-07: the headline is now the map under the rules frozen before scoring (PREREG.md to PREREG.v4,
with the PREREG.v6 implementation corrections). criterion.md (table row "pre-registered v4") and reproduce.md
(section 5) report the counts of that map. The scope of 2026-10-24 stated the post-hoc PREREG.v5 map (26 of 188 =
0.138); that map is now the sensitivity analysis in README.md.

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

History, disclosed: an earlier REPRODUCE panelist (its file is not shipped) failed the as-run v5 map on three code
departures from the frozen text; NOVELTY and CRITERION were not started for it. Repair round 2 (PREREG.v6, frozen
20:56:56Z) corrected the code only; no class changed at any origin; then a further break-it round on the corrected map
(its notes are not shipped) and this fresh panel.
This status stands only if check_run.py prints CHECK_RUN: PASS.
