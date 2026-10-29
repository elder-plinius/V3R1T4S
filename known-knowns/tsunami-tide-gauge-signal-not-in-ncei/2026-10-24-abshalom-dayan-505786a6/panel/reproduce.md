# REPRODUCE skeptic: p3 completeness map (claim/)

context: subagent (Claude Agent tool, fresh context, model claude-opus-5-5)

Scope of reading: only claim/ (CLAIM.md, REPRODUCE.md, PREREG*.md, data/, result/, result_v4/, and, after my own
checker was written and run, lib/ and attempts/*/code). Everything I wrote is in panel/work_reproduce/ (scripts
mycheck.py, mytt.py, mysummary.py, compare.py; outputs next to them). The authors' pipeline was run offline
(V3_OFFLINE=1) in a byte-copy of claim/ (panel/work_reproduce/claim_copy) so that nothing could be written into claim/;
a sha256 manifest of all 5276 files of claim/ is identical before and after (no __pycache__ either).

## Bottom line

Every number in the one-sentence claim, the known limits and the rules history that the bundle can check
reproduces. I checked all of them for all 264 quakes at all 3 origins (real, o-5 h, o-7 h). Nothing was checked on a
sample only. My checker, written from the PREREG text before I opened lib/det.py, lib/det5.py or the map code, gives
the same class as the authors at all 792 origins. My own travel-time solver, written from PREREG.md section 1, gives
the same ETAs (max difference 0.005 min) and the same scope for all 4729 candidate codes. Two items are open (not
mismatches in any result): the "31 IOC GETs" figure in the rules history cannot be confirmed (the bundle shows 29
files), and some readings of points the text leaves open move the counts by 1-3 quakes. Every reading keeps the
real fraction above all 400 fake catalogues.

## 1. Rerun of the authors' pipeline (REPRODUCE.md steps 1-6), offline

| step | result |
|---|---|
| 1. v5 map, 2 shards | OFFLINE_MISS 0 and 0; 264 quake files |
| 2. v4 map + summarize_map.py | OFFLINE_MISS 0; map.csv, null.json, map_summary.txt, listed_rows.txt, land_listed.txt and all 264 quakes/*.json byte-identical to result_v4/ |
| 3. summarize_v6.py, no_overlap.py | map.csv, null.json, map_summary.txt, listed_rows.txt, land_listed.txt, quakes/ byte-identical to result/; no_overlap.txt identical |
| 4. test_impl6.py | output identical to attempts/completeness-map-v6/out/test_impl6.txt |
| 5. provenance | 4447 rows; 0 files differ from sha256_logged_at_fetch (sha256 of the decompressed JSON); 0 missing; all HTTP 200; every URL matches its file name (code, timestart, timestop); host www.ioc-sealevelmonitoring.org only; no IOC file on disk outside the table |
| 6. calibrate.py, flat_ocean.py | tt_selected.json and calibrate.txt identical; flat_ocean output identical except the timing/RSS lines; 800 km error -0.39 % to +0.15 % at latitudes 0, 30, 60 |

The rerun's trace files list 4447 distinct data files read by the two maps. That is exactly the provenance list, no
more and no fewer. Determinism: my offline rerun of their pipeline is byte-identical to the saved outputs, and I saw no run-to-run
variation.

## 2. Independent checker (panel/work_reproduce/mycheck.py), written from the text

Definitions implemented, quoted from the frozen files:
- PREREG.md s2: sensors "{rad, ra2, ras, prs, prt, prte, pr1, pr2, bub, bub1, flt, enc, en2, aqu, pwl, wls, ecs, bwl, stp}";
  "1-min grid; gaps up to 5 min linearly filled; longer gaps NaN", read with PREREG.v6's clarification "time-weighted
  linear interpolation of the raw samples onto whole minutes, kept only at minutes with a raw sample exactly on the
  minute or within 5 min on both sides".
- Spike rule: "m = centred 11-min running median, s = 1.4826 x centred 11-min running median of |x - m|, floored at
  0.003 ... spike when |x - m| > 8 s while both neighbouring minutes have |x - m| < 3 s".
- Stuck (v6 item 2): "a run of >= 60 identical consecutive raw values", "on the scored sensor's raw samples (numeric
  slevel, duplicate time stamps dropped, sorted by time) with time stamps in [o-24 h, o-1 min]".
- Band: "zero-phase Butterworth high-pass, order 4, cutoff 1/120 cpm, per contiguous segment >= 6 h"; v6 item 3 "a run
  of at most 30 missing minutes between two present minutes is filled linearly for the filter; a longer run is not
  filled at all"; "Glitch rule: |bp| > 10 -> NaN"; v2 causal filter for the arrival "initial state at steady state for
  the first sample".
- "RMS24 = RMS of bp over [o-24 h, o-1 min]; W = [o+ETA-10, o+ETA+120] min; r = max |bp| over W / RMS24; arrival = first
  minute in [o+ETA-30, o+ETA+60]" with |causal bp| > 3 x causal RMS24 (v2); "USABLE: pre-window bp coverage >= 80 %, not
  stuck, and W bp coverage >= 50 %"; "DETECTS: USABLE, r > 5 and |arrival - ETA| <= 10 min".
- v5 rule 1 "passes only if >= 10 of its 14 control days are usable and on none of the usable ones r > 5 in the same
  window"; rule 2 tied sensors ("USABLE if any tied sensor is usable; it DETECTS only if every usable tied sensor
  detects; it PASSES only if every usable tied sensor passes", UNDECIDED as quoted there, stage 2 never re-picks);
  rule 3 OVERLAP ("any other ComCat event ... has its origin in the 24 h before it and its epicentre within 1000 km");
  rule 4 class order NO_GAUGE, OVERLAP, NO_DATA, SIGNAL / SIGNAL_UNDECIDED / NO_SIGNAL.
- Windows: stage 1 "[floor_h(o-31 h), ceil_h(o+7 h)]"; stage 2 "[floor_h(o-8 d-1 h), ceil_h(o+9 d)]", relative to the
  fake origin for fake origins (v6 item 1). Sites: "codes within 2 km of each other are one site".
- Data: for each code and window, the union of all saved raw rows of that code (data/ioc, data/ioc_old) with time
  stamps in the window. 0 conflicting duplicate rows were found across overlapping files, so this equals any valid
  composition.

Inputs taken from the authors: only the list of codes in scope and the ETA per code, from result/quakes/*.json.
Section 3 below checks both independently.

Result over all 264 quakes x 3 origins, compared with result/quakes/*.json (compare.py, compare_mine.txt):

| item | compared | mismatches |
|---|---|---|
| class per origin | 792 | 0 |
| OVERLAP flag per origin | 792 | 0 |
| tied-sensor set per code | 3608 | 0 |
| USABLE / DETECTS / PASSES / UNDECIDED per code and origin | 3608 codes x 3 | 0 / 0 / 0 / 0 |
| stuck flag per sensor and origin | 8835 | 0 |
| arrival, usable sensor-origin pairs | 7869 | 0 (differences <= 0.02 min, from their origin floored to the second) |
| r, usable sensor-origin pairs | 7869 | 3 beyond 3-decimal rounding: us10008kce juan rad fake7 2.205 vs 2.139; us7000l7si iqui rad real 2.797 vs 2.811 and fake5 5.272 vs 5.302 (both detect; the code fails on its tied prs). No decision changes |
| control-day r (detecting codes) | 3190 | 3 differ by 0.003-0.011 (us7000jkbd rbct prs days -1, +2; rfrt prs day -5; r 2.3-2.8); no decision changes |
| pre-window / W coverage | 8835 | 1 beyond 0.001 (us2000cjfy anto prs fake5 0.883 vs 0.882); no decision changes |
| site partition | 264 quakes | 0 (single-linkage 2 km gives the same sites as their greedy grouping) |

My classes: real NO_SIGNAL 162, OVERLAP 34, SIGNAL 26, NO_GAUGE 25, NO_DATA 17; o-5 h NO_SIGNAL 196, NO_GAUGE 25,
NO_DATA 19, OVERLAP 18, SIGNAL 6; o-7 h NO_SIGNAL 200, NO_GAUGE 25, NO_DATA 20, OVERLAP 14, SIGNAL 5. All three equal
result/map.csv row by row.

## 3. Travel times and scope (panel/work_reproduce/mytt.py), written from PREREG.md section 1

I wrote my own AEQD grid (3.7 km cells, half-width 1700 km), ETOPO1 sampled at the nearest 2-arcmin node, water =
altitude < 0, speed sqrt(9.81 max(h, 1 m)) and scikit-fmm order 2. The source is the epicentre cell, or the nearest
water cell within 50 km. Gauges snap to the nearest water cell with depth >= 10 m within 30 km. ETA = T - 6.1 min.
The candidate codes are every station-list code with a sea-level sensor, not DART, within 1000 km great-circle.
- 264 quakes, 4729 candidate code-quake pairs. My [10, 150] min scope equals the authors' 3608 in-scope pairs exactly,
  with 0 disagreements either way (1121 candidates are excluded by ETA or have no ETA in both).
- My ETA minus their ETA over the 3608 pairs: median 0.000, max |d| 0.005 min (their rounding to 0.01).
- Calibration (PREREG.md s1), recomputed from the saved rows attempts/evaluator-first/out/tt_rows.csv: NCEI tt
  = 60 travHours + travMins matches the column, and all rows are in [15, 150], validity 4, cause 1, type 2. Per dmin
  1/10/20/50: c -9.7/-6.1/-5.3/-3.0, share within 10 min 0.454/0.464/0.454/0.440, so (10 m, -6.1) is selected. Outside
  +/-10 min with that model: calibration 0.536, 2012-2014 0.422, hold-out 2015-2026 0.468 (79 rows, 25 events). The model
  times in that table come from their solver, which section 3 cross-checks on the map gauges.

## 4. Population, LISTED, overlap (mysummary.py, checks_misc.txt)

- data/comcat/m65_d70_2015_2025.csv: 343 rows, all type earthquake, M >= 6.5, depth <= 70, 2015-01-07 to
  2025-12-27, 343 unique ids. Nearest 2-arcmin cell altitude < 0 gives 264, and the ids equal result/quakes/.
  Land: 79 quakes, 25 with an NCEI event (+/-1 calendar day, 1000 km). Same ids as result/land_listed.txt.
- NCEI events pages: sha256 bdc6a6b4... and 64745d27... as stated in CLAIM.md; 230 events, newest 6193 (2026-10-09).
- LISTED (NCEI event within +/-1 calendar day and 1000 km, or no coordinates): equal to map.csv for 264 of 264, and
  LISTED validity 4 for 264 of 264.
- OVERLAP: my own computation matches at all 792 origins. Boundary cases: us7000lfxx o-5 h has an event 24.21 h earlier
  (not OVERLAP either way). The near-simultaneous pairs us6000f4ly/us6000f53e (2.4 min) and us7000l9h2/us7000l9h4
  (1 min) do not depend on < versus <=. No pair lies within 15 km of the 1000 km limit.

## 5. Recount of the claimed numbers from my per-quake classes

| claimed | mine |
|---|---|
| 26 / 188 = 0.138, Wilson 0.096-0.195 | 26 / 188 = 0.1383, Wilson 0.0962-0.1949; SIGNAL_UNDECIDED 0 |
| 26 / 264 = 0.098, bounds 0.098-0.386 | 0.0985, [0.0985, 0.3864] (OVERLAP 34, NO_DATA 17, NO_GAUGE 25) |
| fake rate 0.027 (6/202, 5/205) | 6/202, 5/205, pooled 0.0270, expected 5.08 |
| best of 400 0.0495 (seed 20261024) | their draw order on my classes: max 0.0495, mean 0.0271. My own draw order: max 0.0495, mean 0.0270. 200 other seeds: best-of-400 0.0441-0.0545. Real beats all in every case |
| excess 0.111 | 26 - 5.08 = 20.92 = 0.1113 of 188; per-quake fake means 3.50 |
| no overlap: 26/221 = 0.118 vs 0.032, best 0.055 | 26/221 = 0.1176; fake 8/219 + 6/218 = 14/437 = 0.0320; best 0.0550, mean 0.0316/0.0323; 1 UNDECIDED |
| v4 rules: 35/221 = 0.158 vs 0.0526, best 0.078 | my v4-rules variant (single sensor, stage-2 re-pick, "no counted control day DETECTS", no overlap): 35/221 = 0.1584, 14/219 + 9/218 = 0.0526, best 0.0780 (their draw order). Class equal to result_v4 at 792 of 792 origins and per code at 6255 code-origins |
| SIGNAL x LISTED: 24 listed, 2 unlisted; 62/100 among NO_SIGNAL; 24 of 86 listed scored | (SIGNAL, L) 24, (SIGNAL, -) 2, (NO_SIGNAL, L) 62, (NO_SIGNAL, -) 100. Validity 4: 23/3/57/105 |
| LISTED among NO_DATA 6/17, NO_GAUGE 0/25, OVERLAP 23/34 | 6/17, 0/25, 23/34 |
| 19 of 26 single-site; 7 multi-site, all listed; unlisted 2 single-site | 19, 7, 7 listed; us7000nhjw (alofi) and usd000j5jt (ouve), 1 site each |
| all 11 fake SIGNALs single-site | o-5 h: us7000lff4 bitu, us1000ga0z adak2, us7000dz5t kusm, us20009ynd syro, us7000dfk3 gbit, us1000hfgn lpbc; o-7 h: us1000hfh3 char2, us60004zhq maju, us2000brgk lena, us20003kfj cald, us1000hfgv char2; all 1 site |
| rule 3 removes 32 NO_SIGNAL, 1 UNDECIDED, 1 NO_DATA at the real origin and no SIGNAL | 34 real OVERLAP origins whose rules-1-2 class is NO_SIGNAL 32, SIGNAL_UNDECIDED 1, NO_DATA 1 |
| v4 -> v5 transitions (map_summary.txt) | identical table; the 9 v4 SIGNALs that are not v5 SIGNALs are the same; no origin goes from non-SIGNAL to SIGNAL |
| longitude bands | identical table |
| PREREG.v3 main-win candidates 0 | 0 (both unlisted SIGNALs are single-site) |
| Kamchatka us6000qw60 NO_SIGNAL; petr r 10.8, +21.8 min | NO_SIGNAL; petr rad r 10.796, arrival - ETA +21.75 |
| us10003x8t: us10003x9g 51.7 min later, 5 km; peaks +135.4 min; r before +108.3 min 7.20, 8.56, 6.36, 7.98; arrival +7.8 | 51.7 min, 5.0 km; peaks at +135.4 min on all four sensors; 7.20, 8.56, 6.36, 7.98; arrival - ETA 7.79 (juan2 prs, juan ra2) |
| fake SIGNALs of other quakes: us20003kfj o-7 h (Illapel 119 min later), us7000dfk3 o-5 h (us7000dffl 46 min later) | 119.3 min (16.6 km); 46.2 min (902.8 km) |
| as-run -> corrected: 0 class changes; us2000bmhe 4 -> 3; us700098qd fakes 19 -> 20; juan2 12.581 -> 12.604; coqu 23.619 -> 23.633 (v4) | I reran with V3_IMPL6=0: 0 class changes (v5 and v4); my as-run v5 classes equal attempts/completeness-map-v5/out/map.csv at every origin; the same four row-level changes, and no others at passing codes. Caveat: this offline as-run rerun hit 24 (v5) and 26 (v4) OFFLINE_MISS windows (the real-origin stage-2 windows that only the as-run code reads for fake detections, read as empty), so it is a consistency check, not an exact reproduction of the as-run maps. No claimed result depends on it |
| PREREG hashes | all six match PREREG.sha256 |

## 6. Readings the definition leaves open

I took: full ComCat origin time (they floor it to the second; this changes no arrival by more than 0.02 min);
running medians ignoring NaN (they need >= 6 of 11; no decision changes); scipy sosfiltfilt with its default edge
padding (they use filtfilt(b, a), whose padding also defaults); tied-sensor counts on numeric unique samples (they
count raw rows; the tied sets are identical at all 3608 codes); "within 5 min" as <= 5 min; LISTED by calendar day.
I reran all 264 quakes under each alternative:

| reading | real SIGNAL / USABLE | fake SIGNAL / USABLE (pooled) | best of 400 | real beats all |
|---|---|---|---|---|
| as claimed (mine) | 26 / 188 = 0.138 | 11 / 407 = 0.0270 | 0.0495 | yes |
| spike neighbours judged with the centre minute's s | 26 / 188 (same classes) | 11 / 407 | 0.0495 | yes |
| zero-phase filter without edge padding | 25 / 188 = 0.133 (us7000dffl drops) | 8 / 407 = 0.0197 | 0.0396 | yes |
| "within 5 min" strict (< 5) | 26 / 187 = 0.139 | 11 / 403 = 0.0273 | 0.0500 | yes |
| PREREG.md "gaps up to 5 min" as raw gap <= 5 min (instead of v6's both-sides rule) | 26 / 187 = 0.139 | 10 / 403 = 0.0248 | 0.0450 | yes |
| fake origins with their own stage-1 window [oo-31 h, oo+7 h] | 26 / 188 | 11 / 405 = 0.0272 | 0.0498 | yes |
| LISTED as +/-24 h instead of calendar day | table unchanged (only us7000lfxx, an OVERLAP quake, becomes unlisted: OVERLAP 22/34 listed) | - | - | - |

Without edge padding, the drops come from control days near segment edges: gbit day +8 r 5.23, thio rad day -3
r 5.23 and char2 day +3 r 5.05, all below 5 with padding. The headline counts therefore move by 1 to 3 quakes
depending on unstated filter and gridding details. The conclusion (real fraction about 0.13-0.14, above every fake
catalogue, excess about 0.11) holds in every reading. The claimed numbers follow from the stated v6 reading and
standard filtfilt padding.

## 7. Mismatches and open items

1. Rules history: "New data: 31 IOC GETs (all HTTP 200, 1.0 MB)". The provenance table (data/ioc_provenance.tsv)
   has 29 files fetched after the PREREG.v6 freeze (20:58:45Z-21:00:08Z, all HTTP 200, 973,170 bytes) and none between
   the v5 and v6 freezes. The fetch log is not in the bundle, so 31 cannot be confirmed (repeat GETs of the same window
   would explain it). No result depends on it. Suggest restating it as "29 files (0.97 MB)" or explaining the 2.
2. Three r values differ from mine by 0.5-3 % (section 2). None is at a decision boundary.
3. The as-run maps cannot be rerun exactly offline from the bundle (section 5). The corrected maps, which carry the
   claim, are rerun exactly.
4. Not verifiable offline, and not attempted: that the raw IOC windows, the ETOPO1 grid, the ComCat CSV and the NCEI
   pages equal what those services serve. I checked only the internal hash consistency, and the NCEI hashes against
   CLAIM.md. The freeze timestamps also cannot be checked from the bundle.

No mismatch was found in any claimed result, class, count, bound, table, null or chance correction. All were checked
for every one of the 264 quakes at the real and both fake origins, not on a sample.

pass: true
