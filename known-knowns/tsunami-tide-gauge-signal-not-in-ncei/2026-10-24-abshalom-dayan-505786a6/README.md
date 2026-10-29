# p3 completeness map: open tide-gauge tsunami signals vs the NCEI listing, M >= 6.5 shallow subsea quakes 2015-2025

## What
In a map that reruns byte-for-byte offline from the saved code and data, of the 264 USGS ComCat M >= 6.5, depth <= 70 km earthquakes of 2015-2025 whose epicentre lies in an ETOPO1 2-arcmin water cell, 188 could be scored at open IOC SLSMF tide gauges within 1000 km (model travel time 10-150 min, at least one usable site, and no other M >= 6.5, depth <= 70 km ComCat earthquake, land or sea, within 1000 km in the preceding 24 h; 25 had no gauge in scope, 17 had no usable data and 34 were set aside by that post-hoc 24 h rule), and 26 of the 188 (0.138, Wilson 95 % 0.096-0.195; 26 of 221 = 0.118 without the post-hoc 24 h rule; 35 of 221 = 0.158 under the pre-registered v4 rules) passed, at one or more sites and on every usable tied sensor, the target's per-gauge test (band-passed peak above 5 times the preceding 24 h RMS, arrival within +/-10 min of a model travel time that puts 0.468 of held-out NCEI tide-gauge arrivals outside +/-10 min, and no peak above 5 times RMS in the same hours on any of at least 10 usable control days), which is a test-pass fraction and not the fraction with any observable tsunami signal, against a fake-origin chance rate of 0.027 (best of 400 fake catalogues 0.0495), with 24 of the 26 listed by NCEI (an NCEI event of any validity or cause within +/-1 day and 1000 km, events snapshot of 2026-10-24T19:20Z) and the 2 unlisted ones passing at a single site, as many as chance predicts (2.8 expected among the 102 unlisted scored quakes).

Path note: the panel files, the PREREG files and `how-we-built-it/null_test.md` refer to the run's folders. There,
`claim/` is the claim folder: `claim/CLAIM.md` is `README.md`, `claim/REPRODUCE.md` is `RUN_IT_YOURSELF.md`,
`claim/result/` is `object/`, and `claim/data/` holds the saved listing pages (not shipped; their URLs, fetch times
and sha256 values are in `the-record-we-beat/RECORD.md` and `how-we-built-it/inputs.tsv`). `lib/`, `attempts/` and
`code/` are the run folder's code, shipped (only the files listed there) under `how-we-built-it/code/`;
`attempts/completeness-map-v6/out/` holds the claimed map's outputs (its `map.csv`, `null.json` and `no_overlap.txt`
are in `object/`), and the map in `attempts/completeness-map-v6/out_v4rules/` is `how-we-built-it/out_v4rules_map.csv`.
`data/` holds the fetched inputs (not shipped; listed in `how-we-built-it/inputs.tsv`). `self_break/`, `runs/`,
`NEXT_RUN.md`, `code/budget_watch.sh` and the other `out/` files named there are not shipped. Dated run names ("run"
followed by a date and time) name runs of the contributor's workspace, which are not shipped either.

## Check it yourself
    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (under a second on a laptop; Python 3 standard library, no network). It checks the sha256 of
every file in object/, re-derives every class at the real and both fake origins from the per-sensor results under the
frozen rules, and recomputes the headline, bounds, SIGNAL x LISTED table and fake-origin rate. RUN_IT_YOURSELF.md
rebuilds the per-sensor results from the raw IOC series. The raw series (about 1.2 GB) are not shipped; "reruns
byte-for-byte offline" refers to the run's saved copies of them (`panel/reproduce.md` records a rebuild from those copies).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| NCEI Global Historical Tsunami Database, events API (the listing the map is set against) | tsunami events 2015-2026 | 230 events; 115 of the 264 quakes have an NCEI event within +/-1 day and 1000 km | https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events | 2026-10-24T19:20:31Z, 19:20:37Z |
| NCEI tsunami event search (status source) | page | HTTP 200 (app shell) | https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search | 2026-10-24T19:20:24Z |
| this repository, partial win p3 | p3 | no claimed or merged p3 result | TROPHY_CASE.md and GitHub search on elder-plinius/V3R1T4S | 2026-10-24T19:20Z |
| issue #253 (walshne-mit, posted as data, not panelled) | p3-like map | 60 of 195 usable quakes detected, different rules | https://github.com/elder-plinius/V3R1T4S/issues/253 | 2026-10-24T19:21:04Z |

Details and hashes: the-record-we-beat/RECORD.md. Panel round 2's own fetches: panel/novelty.md.

## Not claimed
- Not the fraction of quakes with any physically present tsunami: a SIGNAL is a pass of the bank's fixed per-gauge test
  (5x RMS, +/-10 min of a calibrated point-source travel time that misses 0.468 of held-out NCEI arrivals, quiet
  control days). Listed tsunamis with clear signals can fail it on timing. This map reads p3's "tsunami signal" as that
  per-gauge test, the bank's own definition of a signal for this target; it is a lower bound on any-signal detection.
- Timing misses are larger for smaller quakes: 164 of the 188 scored quakes are M < 7.5, where the held-out timing miss
  is 0.667 on 21 held-out rows (how-we-built-it/code/attempts/evaluator-first/out/calibrate.txt); the model also runs early by a median 6.3 min on held-out rows (NCEI minus model arrival).
- Not a main win and not a missed tsunami: the 2 unlisted SIGNALs are single-site, no more than chance predicts (2 vs 2.8 expected).
- Not rules fixed before the result: the claimed map uses a declared post-hoc repair (PREREG.v5) and implementation
  corrections (PREREG.v6); the pre-registered rules give 35 of 221 = 0.158 against 0.0526 (how-we-built-it/null_test.md; that map is shipped as
  how-we-built-it/out_v4rules_map.csv: 35 SIGNAL of 221 scored in column real_cls, 23 of 437 at the fake origins).
  The post-hoc 24 h rule removed no real pass and 3 of the 14 fake passes, so it raised the headline (0.118 to 0.138) and
  lowered the chance rate (0.032 to 0.027).
- 76 of the 264 quakes are not scored (25 no gauge in scope, 17 no usable data, 34 OVERLAP); over all 264 only bounds
  (0.098-0.386) are given.
- NCEI event 5942 p1 (PR #642) is not part of this package.

## Credits
- NOAA NCEI / World Data Service for Geophysics, Global Historical Tsunami Database (events and runups API):
  https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search
- IOC Sea Level Station Monitoring Facility (VLIZ / UNESCO-IOC), raw gauge series, cited as requested: Flanders Marine
  Institute (VLIZ); Intergovernmental Oceanographic Commission (IOC) (2026): Sea level station monitoring facility.
  Accessed 2026-10-24 at https://www.ioc-sealevelmonitoring.org, https://doi.org/10.14284/482. IOC states the data are
  not quality-controlled and may not be used for commercial purposes (https://www.ioc-sealevelmonitoring.org/disclaimer.php).
- USGS ComCat earthquake catalogue: https://earthquake.usgs.gov/fdsnws/event/1/
- ETOPO1 Global Relief Model (NOAA NCEI, Amante and Eakins 2009): https://www.ncei.noaa.gov/products/etopo-global-relief-model
- scikit-fmm (fast marching): https://github.com/scikit-fmm/scikit-fmm
- walshne-mit, issue #253 (the earlier unpanelled map): https://github.com/elder-plinius/V3R1T4S/issues/253
- DmitrL-dev, PR #371 (the bank pitfalls this map follows: travel-time error, solver check, p3 denominator), with
  walshne-mit's solver measurements on that PR: https://github.com/elder-plinius/V3R1T4S/pull/371
- The V3R1T4S bank entry tsunami-tide-gauge-signal-not-in-ncei and its pitfalls (bank/targets.json).
- Submitted by Abshalom Dayan.
