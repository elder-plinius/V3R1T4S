# p3 completeness map: open tide-gauge tsunami signals vs the NCEI listing, M >= 6.5 shallow subsea quakes 2015-2025, under the pre-registered rules

## What
In a map scored under the rules pre-registered before scoring (PREREG.md to PREREG.v4), of the 264 USGS ComCat M >= 6.5, depth <= 70 km earthquakes of 2015-2025 whose epicenter lies in an ETOPO1 2-arcmin water cell, 221 could be scored at open IOC SLSMF tide gauges within 1000 km (model travel time 10-150 min and at least one usable site; 25 had no gauge in scope and 18 had no usable data), and 35 of the 221 (0.158, Wilson 95 % 0.116-0.212; 1 more of the 221 is undecided, with fewer than 10 usable control days) passed, at one or more sites, the target's per-gauge test on the gauge's most-sampled sea-level sensor (band-passed peak above 5 times the preceding 24 h RMS, arrival within +/-10 min of a model travel time that puts 0.468 of held-out NCEI tide-gauge arrivals outside +/-10 min, and the same test passing on none of at least 10 usable control days), which is a test-pass fraction and not the fraction with any observable tsunami signal, against a fake-origin chance rate of 23 of 437 = 0.053 (best of 400 fake catalogs 0.078), with 33 of the 35 listed by NCEI (an NCEI event of any validity or cause dated within 1 calendar day of the origin and within 1000 km, or without coordinates; the same flags against the live events API on 2026-11-07) and the 2 unlisted ones passing at a single site, fewer than chance predicts (5.9 expected among the 113 unlisted scored quakes).

The map under the post-hoc PREREG.v5 rules (26 of 188 = 0.138) is not the claim; it is in the section "Sensitivity analysis" below.

Path note: the panel files, the PREREG files and `how-we-built-it/null_test.md` refer to the run's folders. There,
`claim/` is the claim folder: `claim/CLAIM.md` is `README.md`, `claim/REPRODUCE.md` is `RUN_IT_YOURSELF.md`,
`claim/result/` (the PREREG.v5 map) is `sensitivity-v5/` plus `object/quakes/` (its per-quake files) and
`object/land_listed.txt`, and `claim/result_v4/` (the map under the v4 rules) is `object/map.csv` (its own `quakes/`,
`map_summary.txt` and `null.json` are not shipped; `object/map_summary.txt` and `object/null.json` are recomputed from
`object/map.csv` by `how-we-built-it/code/summarize_v4_from_map.py`). `claim/data/` holds the saved listing pages (not
shipped; their URLs, fetch times and sha256 values are in `the-record-we-beat/RECORD.md` and
`how-we-built-it/inputs.tsv`). `lib/`, `attempts/` and `code/` are the run folder's code, shipped (only the files listed
there) under `how-we-built-it/code/`; `attempts/completeness-map-v6/out_v4rules/` is the headline map (`object/map.csv`)
and `attempts/completeness-map-v6/out/` the PREREG.v5 map (`sensitivity-v5/` and `object/quakes/`). `data/` holds the
fetched inputs (not shipped; listed in `how-we-built-it/inputs.tsv`, and every raw IOC response in
`how-we-built-it/ioc_windows_1.tsv` and `_2.tsv`; `data/ioc_provenance.tsv` is the run's own list of those responses, not
shipped). `panel/work_reproduce/`, `panel/work_novelty/` and `panel/work_criterion/` are the panelists' work folders, not
shipped. The PREREG files are kept byte for byte as frozen (sha256 in `how-we-built-it/PREREG.sha256`), so they still
name run files that are not shipped: `NEXT_RUN.md` (the run's brief), `code/budget_watch.sh`, `data/fetch_log.tsv`,
`self_break/verdict.md` (the run's own break-it notes) and `panel_round1/reproduce.md` (an earlier panel file). Dated
run names ("run" followed by a date and time) name runs of the contributor's workspace, which are not shipped either.

## Implementation fixes in the headline map
The headline map is the v4-rules map scored by the run's code with the three corrections of PREREG.v6. Each one only
makes the code do what the frozen PREREG.md text says; no rule, threshold, population or data choice changes:
1. Fake-origin control days. PREREG.md section 3 puts a fake origin's control days relative to the fake origin, and
   section 2 fetches [floor_h(o-8 d-1 h), ceil_h(o+9 d)]. The code read the real origin's window, which cut day -7's
   24 h pre-window short by 4 h (o-5 h) and 6 h (o-7 h). Corrected: the window around the fake origin.
2. Stuck sensor. PREREG.md section 2 counts "a run of >= 60 identical consecutive raw values inside the 24 h
   pre-window". The code ran it on the gridded, gap-filled, spike-cleaned series. Corrected: on the raw samples of the
   scored sensor in [o-24 h, o-1 min].
3. Gap bridging. PREREG.md section 2 bridges "gaps <= 30 min ... for the filter only". The code also filled the first
   30 minutes of longer gaps. Corrected: only runs of at most 30 missing minutes are filled.

The run records no class change at any origin between the as-run v4 map (not shipped) and the corrected one, and 35 of
221 for both (how-we-built-it/null_test.md; panel/reproduce.md section 5 reports the same from an offline rerun, with
the caveat stated there). Nothing else differs from the frozen v4 rules.

How the shipped files carry this map: object/quakes/ holds, per quake and gauge code, the per-sensor results of every
tied sensor (from the PREREG.v5 run with the same corrections; stage 1 reads the same window in both runs, and the r
and arrival of all 85 passing codes in object/map.csv equal those of the first tied sensor there). The v4
rules score the first tied sensor (the one with the most samples in the stage-1 window). Where that sensor detects but
another tied sensor does not, the v5 run computed no control days, so for those 13 codes (6 origins whose class
depends on them, 3 more whose passing-site count does) the v4 control days were recomputed on 2026-11-07 from IOC
windows fetched again that day (object/v4_ctrl_refetch.json, how-we-built-it/code/recheck_refetch.py): all 13 pass, as
in the v4 map. The v4 code picks the sensor with the most samples again in the 17-day control-day window; in those 13
windows it picked the stage-1 sensor. With these inputs the v4 rules re-derive every class and every usable, detecting
and passing site count of object/map.csv at all 792 origins (264 quakes, real and two fake origins).

## Check it yourself
    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (under a second on a laptop; Python 3 standard library, no network). It checks the sha256 of
every file in object/ and sensitivity-v5/; re-derives every class at the real and both fake origins from the per-sensor
results, under the v4 rules for object/map.csv and under the PREREG.v5 rules for sensitivity-v5/map.csv; re-derives the
LISTED flag and NCEI ids of every quake from the NCEI events pages saved on 2026-11-07; checks that every gauge in scope
has a model arrival time and a request row in how-we-built-it/ioc_requests.csv; and recomputes the headline, bounds,
SIGNAL x LISTED counts and fake-origin rate of both maps. It cannot recompute r, arrivals or control days: that needs
the raw IOC series (about 1.4 GB), which are not shipped. RUN_IT_YOURSELF.md rebuilds them from IOC.

IOC requests: how-we-built-it/ioc_requests.csv has one row per quake, gauge code and window read (stage 1, and the
control-day windows of stage 2), with the code's site, its model arrival time (ETA, minutes after the origin), its tied
sensors and the sensor the v4 rules score, the UTC window, and the IOC responses that supply it. Each response is a line
of how-we-built-it/ioc_windows_1.tsv or _2.tsv with its URL (station and UTC window), UTC fetch time, HTTP status and
the sha256 of the raw JSON as fetched on 2026-10-24: 4447 responses in all, every one read by the maps. On 2026-11-07,
107 windows were fetched again from the IOC API, one at a time with 1 s between requests
(how-we-built-it/refetch_2026-11-07.tsv: URL, UTC time, HTTP status, sha256 of today's response). The 39 whose URL equals
an original request have the same sha256 as on 2026-10-24, and r, arrival and sensor recomputed from today's stage-1
windows equal the shipped values for all 94 codes checked (how-we-built-it/refetch_stage1_check.tsv). The other
hashes in that file are of today's responses.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| NCEI Global Historical Tsunami Database, events API (the listing the map is set against) | tsunami events 2015-2026 | 230 events on 2026-10-24, 231 on 2026-11-07; 115 of the 264 quakes listed on both dates, with the same NCEI ids | https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events | 2026-10-24T19:20:31Z, 19:20:37Z; 2026-11-07T00:12:11Z, 00:12:18Z |
| NCEI tsunami event search (status source) | page | HTTP 200 (app shell) | https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search | 2026-10-24T19:20:24Z |
| this repository, partial win p3 | p3 | no claimed or merged p3 result | TROPHY_CASE.md and GitHub search on elder-plinius/V3R1T4S | 2026-10-24T19:20Z |
| issue #253 (walshne-mit, posted as data, not panelled) | p3-like map | 60 of 195 usable quakes detected, different rules | https://github.com/elder-plinius/V3R1T4S/issues/253 | 2026-10-24T19:21:04Z |

Details and hashes: the-record-we-beat/RECORD.md. Panel round 2's own fetches: panel/novelty.md.

## LISTED: the matching rule and the live re-check
The rule is PREREG.md section 3 as implemented (attempts/completeness-map/code/summarize_map.py, listed()): an NCEI
event of any validity and any cause matches a quake when its UTC calendar date (a missing month or day read as 1)
differs from the origin's UTC calendar date by at most 1 day (or it has no day and the same year and month), and its
epicenter is within 1000 km of the ComCat epicenter or it has no coordinates. The time tolerance is therefore 1
calendar day on either side, which allows clock-time gaps of up to just under 48 h; it is not +/-24 h.

Against the live events API (231 events for 2015-2026, fetched 2026-11-07T00:12Z, saved in
how-we-built-it/ncei_2026-11-07/ with sha256 in RECORD.md), how-we-built-it/code/relist_ncei.py gives the same LISTED
flag and the same NCEI ids for all 264 quakes as both maps; no class or count changes. The pairs the rule matches only
loosely (how-we-built-it/ncei_2026-11-07/relist.txt):
- us7000gbu4 (M 6.6, 2022-01-14, Sunda Strait, NO_SIGNAL) matches NCEI 6087, an event in the Rio de la Plata estuary,
  Argentina (cause code 9), only because 6087 has no coordinates.
- us7000lfxx (M 6.9, 2023-12-03, Mindanao, NO_SIGNAL) matches NCEI 5903, dated 29.2 h before the ComCat origin and
  52 km away; one calendar day apart.
- Four more pairs are 25.5-25.7 h apart; each of those quakes also has an NCEI match within 24 h, or is NO_DATA.
Neither named quake is a SIGNAL. With coordinates required and a strict +/-24 h clock tolerance, 106 instead of 108 of
the 221 scored quakes are listed and all 33 listed SIGNALs stay listed; the headline does not change.

## Sensitivity analysis: the post-hoc PREREG.v5 rules (not the claim)
After the v4 map was scored, the run's own break-it check found passes with strong control-day peaks at the wrong time,
results that depend on which of two tied sensors is scored, and two aftershocks inside a mainshock's tsunami coda.
PREREG.v5 (frozen after the v4 map) is a declared post-hoc repair: (1) a code passes only if no usable control day has
a peak above 5 times RMS in the same hours, whatever its arrival; (2) every tied sensor is scored and all must pass;
(3) an origin with another M >= 6.5, depth <= 70 km ComCat event within 1000 km in the 24 h before is OVERLAP and not
scored. With the same PREREG.v6 corrections (files in sensitivity-v5/; the checker re-derives them):
- 26 of 188 = 0.138 (Wilson 95 % 0.096-0.195), 34 quakes set aside as OVERLAP; fake-origin rate 11 of 407 = 0.027,
  best of 400 fake catalogs 0.0495; 24 of the 26 listed, the 2 unlisted ones single-site.
- Without rule 3: 26 of 221 = 0.118, fake-origin rate 14 of 437 = 0.032, best of 400 0.055
  (sensitivity-v5/no_overlap.txt). Rule 3 removed no real pass and so raised the fraction from 0.118 to 0.138.
- From the v4 map, no quake becomes a SIGNAL; 26 stay SIGNAL, 7 become NO_SIGNAL (us200030aq, us10007mn3, us1000c2zy,
  us60007idc, us6000ae4n, us7000c7y0, us6000rtdt) and 2 become OVERLAP (us20003kfj and us10003x9g, aftershocks of the
  2015 Illapel and Coquimbo sequences); all 9 also fail rules 1-2 alone (sensitivity-v5/map_summary.txt and
  no_overlap.txt).

## Not claimed
- Not the fraction of quakes with any physically present tsunami: a SIGNAL is a pass of the bank's fixed per-gauge test
  (5x RMS, +/-10 min of a calibrated point-source travel time that misses 0.468 of held-out NCEI arrivals, control
  days). Listed tsunamis with clear signals can fail it on timing. This map reads p3's "tsunami signal" as that
  per-gauge test, the bank's own definition of a signal for this target; it is a lower bound on any-signal detection.
- The v4 control-day rule fails a code only when a control day passes the same test, timing included. A control day
  with a peak above 5 times RMS at another time does not fail it, and the v4 rules score one sensor per code, so a tied
  second sensor can disagree: 9 of the 35 SIGNALs fail the stricter PREREG.v5 rules 1-2 (section above), 2 of them
  aftershocks inside a mainshock's tsunami coda (us20003kfj, us10003x9g).
- Timing misses are larger for smaller quakes: 195 of the 221 scored quakes are M < 7.5, where the held-out timing miss
  is 0.667 on 21 held-out rows (how-we-built-it/code/attempts/evaluator-first/out/calibrate.txt); the model also runs
  early by a median 6.3 min on held-out rows (NCEI minus model arrival).
- Not a main win and not a missed tsunami: the 2 unlisted SIGNALs (usd000j5jt at ouve, us7000nhjw at alofi) are
  single-site, fewer than chance predicts (2 vs 5.9 expected); no PREREG.v3 main-win candidate.
- 43 of the 264 quakes are not scored (25 no gauge in scope, 18 no usable data); over all 264 only bounds
  (0.133-0.299) are given.
- NCEI event 5942 p1 (PR #642) is not part of this package.

## Credits
- NOAA NCEI / World Data Service for Geophysics, Global Historical Tsunami Database (events and runups API):
  https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search
- IOC Sea Level Station Monitoring Facility (VLIZ / UNESCO-IOC), raw gauge series, cited as requested: Flanders Marine
  Institute (VLIZ); Intergovernmental Oceanographic Commission (IOC) (2026): Sea level station monitoring facility.
  Accessed 2026-10-24 and 2026-11-07 at https://www.ioc-sealevelmonitoring.org, https://doi.org/10.14284/482. IOC
  states the data are not quality-controlled and may not be used for commercial purposes
  (https://www.ioc-sealevelmonitoring.org/disclaimer.php).
- USGS ComCat earthquake catalog: https://earthquake.usgs.gov/fdsnws/event/1/
- ETOPO1 Global Relief Model (NOAA NCEI, Amante and Eakins 2009): https://www.ncei.noaa.gov/products/etopo-global-relief-model
- scikit-fmm (fast marching): https://github.com/scikit-fmm/scikit-fmm
- walshne-mit, issue #253 (the earlier unpanelled map): https://github.com/elder-plinius/V3R1T4S/issues/253
- DmitrL-dev, PR #371 (the bank pitfalls this map follows: travel-time error, solver check, p3 denominator), with
  walshne-mit's solver measurements on that PR: https://github.com/elder-plinius/V3R1T4S/pull/371
- The V3R1T4S bank entry tsunami-tide-gauge-signal-not-in-ncei and its pitfalls (bank/targets.json).
- Submitted by Abshalom Dayan.
