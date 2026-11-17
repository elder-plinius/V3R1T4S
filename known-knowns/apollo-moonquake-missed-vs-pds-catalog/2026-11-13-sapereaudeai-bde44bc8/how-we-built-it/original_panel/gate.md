# Honesty gate (kit/RUN.md step 7), run main session

target: apollo-moonquake-missed-vs-pds-catalog
partial win: p1
time: 2026-11-13T01:40:38Z
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three fresh subagent contexts that saw only claim/)
table fetch age: status source re-fetched by NOVELTY at 2026-11-12T23:48:59Z (all 12 CSVs byte-identical), by CRITERION at 23:55:27Z and by REPRODUCE at 2026-11-13T00:06-00:07Z; less than 6 h old.

Downgrade checks (none triggered):
- hedging panelist: no. REPRODUCE reports a stack-construction sensitivity (its own reading of the screen rule gave a 5-member stack with best single-channel CC 0.593 at its own window, 0.626 at the claimed window, still far above its null 0.259) and passes because the pre-registered builder (tools/nesttemplates2.py) rebuilds the six-member stack bit-identically and gives 0.757; the confirmed scope below names that stack.
- reproduction mismatch: no; every claimed number reproduced exactly with the claim's code; REPRODUCE's independent code gives D 0.7385 vs 0.7417 and null maximum 0.2956 vs 0.2868.
- stretched criterion or hidden quantifier: no; CRITERION checked selection among 25 nests and 14 seeds with its own cross-nest null (75 controls, maximum 0.306) and a channel-shift stress test (0.486), both below 0.742.
- table value by evasion: no.
- unresolved baseline: not applicable (existence claim).
Disclosures for the report and package: the null was computed with tools/fast_null.py, an exact re-implementation of the pre-registered score_scan.py (equal on 1971-133 for all 401 controls, checked by the claimant and by CRITERION and REPRODUCE); membership rests on S14 waveform similarity, the other nests' low scores at that time and the tidal phase; an A38-like signal on 1971-06-09 17:05 is catalogued as a meteoroid impact (possible misclassification, not claimed).

status: CONFIRMED_PARTIAL
confirmed_scope: On Apollo S14 long-period channels MH1/MH2 (PDS MiniSEED, Earth-received time), the 450 s window starting 1971-05-13 18:39:33.7 UTC correlates with the S14 stack of six catalogued 1971 A38 deep-moonquake events at NCC 0.757 (MH2) and 0.727 (MH1), its two-channel mean 0.742 exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.212) and of all 400 phase-randomised-template controls (best 0.287), and no dated row of any PDS Apollo seismic event catalogue table lies within +/- 5 min of it (nearest 120 min), which meets bank partial win p1 as a single-station detection of an A38 nest member absent from the PDS catalogue.
