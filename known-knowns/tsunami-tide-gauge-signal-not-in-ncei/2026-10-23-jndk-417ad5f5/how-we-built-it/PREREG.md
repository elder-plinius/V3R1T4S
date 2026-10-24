# PREREG (frozen 2026-10-23T21:49:48Z, before any sweep output exists)

Target: tsunami-tide-gauge-signal-not-in-ncei. Run <RUN>.
Detector library frozen: attempts/catalogue-gap/code/tsu.py, sha256 61bccc50777e893634ff2e199a836fa79c8a30e50a13aa796de0f0f6e6f85a54. Only the validation job (2272) has run with it,
on a known positive (NCEI 6068, 2025-11-09 Sanriku) and its shifted negative; no candidate event has been scored.

## Criterion (verbatim, bank)
A saved bundle (raw IOC SLSMF series for >= 2 gauges, de-tiding code, source parameters) showing: on each gauge, a band-passed (2-120 min) signal with peak amplitude > 5x the RMS of the preceding 24 h in the same band; arrival times at all gauges consistent within +/- 10 min with shallow-water travel times computed from the source (earthquake from USGS ComCat, or a meteotsunami pressure jump with propagating-front check); signals absent on the same gauges in the same hours on control days; and the NCEI events API (https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events) and runups API, re-fetched live immediately before claiming, have no event within +/- 1 day of the source in that region (main win) or no runup row for those gauges (partial win).
p1 (verbatim): Gauge observations (amplitude, arrival) for a listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations.

## Frozen operational rules (as coded in tsu.py)
- Series: IOC API v1 service.php?query=data, window [t0-36 h, t0+12 h]. Sensor = the one with native median interval <= 60 s
  and most samples in [t0-24 h, t0+4 h]. Reject the gauge if, in [t0-24 h, t0+4 h]: a level run (identical consecutive raw
  values) >= 30 min, > 10% missing minutes, or any gap > 10 min. 1-min bin means; despike: |x - 7-min running median| >
  max(10 robust sigma, 0.05 m) set missing; gaps <= 10 min linearly interpolated.
- De-tiding: least-squares fit of mean + linear trend + 12 constituents (M2 S2 N2 K2 K1 O1 P1 Q1 M4 MS4 M6 M8) over the
  48 h window, then zero-phase 4th-order Butterworth high-pass at 120 min (the 2-120 min band at 1-min sampling).
- RMS24 = rms of the band-passed series on [t0-24 h, t0).
- Travel time: ETOPO1 (NCEI THREDDS, grid-registered) at 2 arcmin; water = z < 0; speed sqrt(g max(depth, 10 m));
  Dijkstra on the lat/lon grid with the 32 coprime offsets (|di|,|dj| <= 3), edge cost = great-circle length x mean
  slowness of 5 points along the edge, all of them water. Source = nearest cell with depth >= 20 m within 50 km of the
  ComCat epicentre (else: not offshore, skipped). Gauge = nearest cell with depth >= 20 m within 30 km (else no ETA).
  Flat-ocean check (job 2272): max error +1.3% (equator), +2.3% (45 N).
- Onset = first minute in [t0+ETA-30 min, t0+ETA+60 min] (not before t0) with |bp| >= 3 RMS24.
  dt_arr = onset - (t0+ETA). Peak = max |bp| on [onset, onset+180 min]. R = peak/RMS24.
- Per-gauge DETECT: onset exists, |dt_arr| <= 10 min, R > 5.
- Control days: the same rules with t0 shifted by d days, d in {-7..-2, +2..+7} (12 days). A gauge's signal is "absent on
  control days" only if DETECT is false on all 12 (a control day failing QC counts as not available; at least 8 of 12
  must be available).
- NCEI conflict (main win): any NCEI event of any validity and any cause with date within +/-1 day and either within
  3000 km of the epicentre or without coordinates. Runup-row conflict (p1): any NCEI runup row of that event (any type)
  within 20 km of the IOC station.

## Pipelines
- Lens catalogue-gap (main win): USGS ComCat M >= 6.0, depth <= 70 km, 2015-01-01 to 2026-10-22, newest first; drop NCEI
  conflicts; IOC stations (any status) within 800 km, nearest 8 distinct codes. Stage 1 screen: R over [t0, t0+4 h] > 5
  at >= 2 gauges (heuristic filter only, not an exclusion claim). Stage 2: DETECT at >= 2 gauges. Stage 3: control days.
- Lens p1-gauge-rows (p1): NCEI events with causeCode 1 (earthquake) since 2024-01-01; IOC stations within 1500 km not
  conflicting with that event's runup rows; Stage 2 + Stage 3 as above on all of them.
- Lens settled-already: on every survivor, live NCEI re-query (events and runups), all validity codes, +/-1 day; check
  weather (storm) and gauge behaviour by reading the series; a survivor that fails any check is dropped.

## Null test
null_test: required
For each surviving candidate: 400 control origin times drawn uniformly (seed 20261023) from [t0-60 d, t0+60 d] with
|t - t0| >= 2 d, same gauges, same ETAs, same pipeline (controls failing QC are redrawn). Statistic S = min over the
claimed gauges of R_g, where R_g = R if |dt_arr| <= 10 min else 0. The real S must beat every one of the 400 controls.
Reported with the scan size (number of quakes and gauges screened) as the look-elsewhere context.

## Outcome labels
Main-win candidate = >= 2 gauges with DETECT, absent on control days, real S beats all 400 controls, no NCEI conflict on
the live re-query. p1 candidate = the same with the runup-row rule. Anything else is negative. p3 (completeness map)
is not attempted this run: its denominator is unresolved (repo issue #253, PR #371).
