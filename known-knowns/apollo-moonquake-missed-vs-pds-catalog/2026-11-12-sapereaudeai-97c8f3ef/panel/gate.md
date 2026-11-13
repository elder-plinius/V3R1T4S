# Honesty gate (kit/RUN.md step 7), run main session

target: apollo-moonquake-missed-vs-pds-catalog
partial win: p2
time: 2026-11-12T21:36:23Z
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three fresh subagent contexts that saw only claim/)
table fetch age: status source re-fetched by NOVELTY at 2026-11-12T21:07:16Z and by REPRODUCE at 21:33:58Z (levent sha256 unchanged); less than 6 h old.

Downgrade checks (none triggered):
- hedging panelist: no; all three write pass: true with reasons and recomputed numbers.
- reproduction mismatch: no; every claimed number reproduced exactly with the claim's code; REPRODUCE's independent detector also gives 63/67 (one event swapped each way, explained by the 20 s gap widening and a 0.001-level D shift); its false-alarm rate is 0.900 vs the claimed 1.196 per day, i.e. the claimed rate is the more pessimistic one.
- stretched criterion or hidden quantifier: no; CRITERION checked looser and stricter readings (threshold above the reversed-null maximum 61/67, narrow window 61/67, visual-catalogue subset 44/48).
- scope wider than reproduced: no; confirmed_scope below is CRITERION's sentence.
- table value by evasion: no; all fetches single honest requests (data/fetch_log.tsv).
- unresolved baseline: not applicable (absolute 90% bar; baseline/README.md).
Disclosures carried to the report and package (no scored number changes): the claim's code copies differ from the PREREG.v2 frozen hashes by path rewrites only (tools/sanitize_paths.py), shown functionally identical by both REPRODUCE and CRITERION; preprocessing widens gaps by 20 s and declustering is greedy over samples rather than over local maxima (REPRODUCE: no effect on counts); PREREG.md's "52 dev days" counts day files, 49 hold events.

status: CONFIRMED_PARTIAL
confirmed_scope: With templates and threshold (theta = 0.10898) fixed on 1972 data alone, the saved three-component S12 long-period template detector re-runs to recover 63 of the 67 nest-A1 deep moonquakes catalogued for 1971 in levent.1008weber.csv (94.0%, detection onset within +/- 5 min of the catalogued start), at a measured false-alarm rate of 1.196 declustered detections per scanned day on the time-reversed 1971 data (400 over 334.54 scanned day-equivalents).
