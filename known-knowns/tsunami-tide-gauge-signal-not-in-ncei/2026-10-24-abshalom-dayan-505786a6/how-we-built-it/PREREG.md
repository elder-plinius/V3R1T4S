# PREREG (run 2026-10-24-1916), frozen 2026-10-24T19:30:15Z (date -u), before any gauge series is scored in this run

null_test: required

## 0. Criterion and partial wins (verbatim, bank/targets.json at repo_commit 1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25)

Criterion: A saved bundle (raw IOC SLSMF series for >= 2 gauges, de-tiding code, source parameters) showing: on each gauge, a band-passed (2-120 min) signal with peak amplitude > 5x the RMS of the preceding 24 h in the same band; arrival times at all gauges consistent within +/- 10 min with shallow-water travel times computed from the source (earthquake from USGS ComCat, or a meteotsunami pressure jump with propagating-front check); signals absent on the same gauges in the same hours on control days; and the NCEI events API (https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events) and runups API, re-fetched live immediately before claiming, have no event within +/- 1 day of the source in that region (main win) or no runup row for those gauges (partial win).

- p1: Gauge observations (amplitude, arrival) for a listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations.
- p2: A meteotsunami (atmospheric pressure jump with matching propagation speed) with > 0.3 m amplitude on >= 2 gauges not in NCEI.
- p3: A completeness map: fraction of M >= 6.5 shallow subsea earthquakes 2015-2025 with any tsunami signal on open gauges vs NCEI listing, reproducible from saved code.

Unchanged for every claim (your human's NEXT_RUN.md): the 5x RMS24 bar and the +/- 10 min arrival rule. NCEI 5942 p1 is taken (PR #642) and not packaged.

## 1. Travel-time model (TT), lib/tt.py

- Bathymetry: ETOPO1 Ice, grid-registered (NCEI THREDDS `global/ETOPO1_Ice_g_gmt4.nc`), stride 2 = 2 arcmin, six OPeNDAP slabs (data/fetch_log.tsv), stored as data/bathy/etopo1_2min_int16.npy. No other bathymetry.
- Solver: azimuthal-equidistant grid centred on the source epicentre, cell 3.7 km, half-width 1700 km; water = altitude < 0;
  speed sqrt(9.81 max(h, 1 m)); scikit-fmm second-order fast marching. Source = the epicentre cell, or if that cell is
  land the nearest water cell within 50 km (otherwise no ETA).
- Flat-ocean check, run before this file (attempts/evaluator-first/out/flat_ocean.txt): 4000 m flat ocean, 48 azimuths,
  error at 800 km between -0.39 % and +0.15 % at latitudes 0, 30 and 60.
- Gauge: snapped to the nearest water cell with depth >= dmin within 30 km (otherwise no ETA). ETA = T(snapped cell) + c.
- Calibration (code attempts/evaluator-first/code/calibrate.py), run after this file is frozen and before any gauge
  series is scored:
  - Rows: NCEI runup rows with typeMeasurementId 2 (tide gauge), fetched per event (data/ncei_tg/ev/), of NCEI events with
    causeCode 1 and eventValidity 4, with row coordinates and event coordinates; NCEI travel time = 60 travHours + travMins
    (a missing part read as 0; rows with neither are dropped), kept when in [15, 150] min. Source for the model = NCEI's
    event latitude/longitude.
  - Calibration set: events of 2005-2011. Positive-control years 2012-2014 and 2026 and the population years 2015-2025
    are never used to choose anything.
  - Candidates: dmin in {1, 10, 20, 50} m. For each, c = median(NCEI - model) over the calibration rows, rounded to 0.1 min.
    Selected: the dmin with the largest share of calibration rows with |NCEI - (model + c)| <= 10 min; ties go to the
    smaller |c|. The selected (dmin, c) is written to attempts/evaluator-first/out/tt_selected.json and is then fixed
    for everything below (a frozen, calibrated model, as NEXT_RUN.md requires).
  - Reported once, never used to select: the same statistics on 2012-2014 and on 2015-2026 rows (hold-out): share
    within +/-10, +/-15, +/-20 min, median error, M < 7.5 vs M >= 7.5 (NCEI eqMagnitude), events with >= 1 and with all
    rows within +/-10 min, 95 % CI by bootstrap over events (2000 resamples, seed 20261024). The +/-10 min rule's own
    miss rate on listed tsunamis is this hold-out share outside +/-10 min; it is reported separately from detection misses.

## 2. Detector D5 (lib/det.py), used for the map, the positive control and the main-win screen

- Series: IOC SLSMF `service.php?query=data&code=..&timestart=..&timestop=..&format=json`, one honest GET per window,
  cached (old runs' identical windows reused byte-for-byte; never re-requested after 401/403/429/503, which stops the job).
- Sensor: among sea-level sensors {rad, ra2, ras, prs, prt, prte, pr1, pr2, bub, bub1, flt, enc, en2, aqu, pwl, wls, ecs,
  bwl, stp} (never bat, atm, sw1, sw2), the one with the most samples in the window. ('aqu' added: dossier lead 6.)
- 1-min grid; gaps up to 5 min linearly filled; longer gaps NaN.
- Spike rule v5 (fix for the deleted near-field waves): m = centred 11-min running median, s = 1.4826 x centred 11-min
  running median of |x - m|, floored at 0.003 (native units). A sample is a spike when |x - m| > 8 s while both
  neighbouring minutes have |x - m| < 3 s (an isolated one-sample excursion). Spikes -> NaN. No other spike rule.
- Stuck sensor: a run of >= 60 identical consecutive raw values inside the 24 h pre-window makes the gauge unusable
  for that origin (checked only in the pre-window, never in the signal window).
- Band: zero-phase Butterworth high-pass, order 4, cutoff 1/120 cpm, per contiguous segment >= 6 h, gaps <= 30 min
  bridged for the filter only (bridged minutes return to NaN). Glitch rule: |bp| > 10 (native units) -> NaN.
- Per gauge and origin o (real, fake or control day): RMS24 = RMS of bp over [o-24 h, o-1 min];
  peak window W = [o+ETA-10, o+ETA+120] min; r = max |bp| over W / RMS24;
  arrival = first minute in [o+ETA-30, o+ETA+60] with |bp| > 3 RMS24.
- USABLE (fix for the 80 % rule; usability is decided by data availability and the pre-window only): pre-window bp
  coverage >= 80 %, not stuck, and W bp coverage >= 50 %.
- DETECTS: USABLE, r > 5 and |arrival - ETA| <= 10 min (the criterion's bar and window, unchanged).
- Control days: same gauge, same clock window on days -7..-1 and +2..+8 (fetch [floor_h(o-8 d-1 h), ceil_h(o+9 d)]);
  a control day counts when USABLE; at least 10 must count. PASSES = DETECTS and no counted control day DETECTS.
- Sites: codes within 2 km of each other are one site; a site is USABLE / DETECTS / PASSES when any of its codes is.
- Scope per source: every IOC code with a sea-level sensor in data/ioc_stationlist.json (fetched 19:28:22Z, any
  status), excluding DART stations, within 1000 km great-circle of the epicentre, with an ETA (section 1) in [10, 150]
  min. No cap on the number of gauges. A code with no data or no sea-level sensor in the window is simply not USABLE.

## 3. p3 completeness map

- Population: USGS ComCat M >= 6.5, depth <= 70 km, 2015-01-01 to 2025-12-31, type earthquake
  (data/comcat/m65_d70_2015_2025.csv, 343 rows); subsea = the ETOPO1 2-arcmin cell nearest the epicentre has
  altitude < 0 (264 quakes; the bank pitfall counts 264). Land-epicentre quakes that NCEI lists are tabulated
  separately and are not in the denominator.
- Per quake, stage 1 fetches [floor_h(o-31 h), ceil_h(o+7 h)] per code (or, when an earlier run cached exactly
  [floor_h(o-25 h), ceil_h(o+7 h)], that file plus [floor_h(o-31 h), floor_h(o-25 h)]); stage 2 (control days) only for
  codes that DETECT in stage 1.
- Classes (every one of the 264 is counted): NO_GAUGE (no code in scope), NO_DATA (codes in scope, none USABLE),
  USABLE (>= 1 USABLE site); among USABLE: SIGNAL (>= 1 site PASSES) or NO_SIGNAL. A quake whose stage 2 cannot be
  completed (fewer than 10 counted control days at every detecting site) is SIGNAL_UNDECIDED and reported as such.
- LISTED: an NCEI tsunami event (any validity, any cause; events API re-fetched for 2015-2026 at 19:20Z) dated within
  +/- 1 day of the origin and within 1000 km (or without coordinates). Also reported: LISTED with validity 4.
- Outputs: one row per quake (attempts/completeness-map/out/map.csv) with id, time, lat, lon, depth, M, class, sites in
  scope, usable sites, detecting sites, passing sites (code, r, arrival - ETA), LISTED, NCEI ids and validity; the
  headline fraction SIGNAL / USABLE with a Wilson 95 % interval; SIGNAL / 264 and the bounds
  [SIGNAL / 264, (SIGNAL + NO_DATA + NO_GAUGE) / 264]; the 2 x 2 table SIGNAL x LISTED over USABLE quakes; LISTED
  counts within NO_DATA and NO_GAUGE; the same by 30-degree longitude band. Single-site SIGNALs are reported as such
  and are never claims of a missed tsunami.
- Null for the map (null_test: required): for every quake, the same pipeline at two fake origins, o-5 h and o-7 h (same
  codes and ETAs; their control days are relative to the fake origin; stage 2 for fake detections as for real ones).
  400 fake catalogues (seed 20261024): each takes, per quake, one of its two fake origins at random; statistic =
  SIGNAL / USABLE at those fake origins. The real fraction must beat every one of the 400; the best control and the
  expected number of chance SIGNALs (mean fake rate x real USABLE count) are reported next to the real value.

## 4. Positive control (run before the map; it checks the frozen pipeline, it never tunes it)

- Events: NCEI events with causeCode 1 and eventValidity 4 dated 2012-01-01..2014-12-31 or 2026-01-01..2026-10-24,
  matched to the largest ComCat event M >= 6.0 within +/- 15 min and 300 km (data/comcat/m60_2012_2014.csv,
  m60_2026.csv), kept when ComCat M >= 6.5, depth <= 70 km, subsea (as in section 3), and NCEI has >= 1 tide-gauge row
  within 5 km of an IOC code in scope.
- Run: exactly the map pipeline of section 3 (stage 1 and 2; no fake origins). Report: event recall (SIGNAL among
  USABLE events), and for every NCEI tide-gauge row at an IOC code in scope one outcome: NO_DATA, PASS, DETECT but
  control day fails, r > 5 but arrival outside +/-10 min, r <= 5. Rows whose NCEI travel time is itself more than 10 min
  from the model ETA are counted as "rule misses" separately from detection misses.
- If the positive control exposes a code bug (not a threshold), the fix goes into PREREG.v2.md with the reason before
  the map is scored; thresholds are never changed.

## 5. Main-win screen of the 45 unscreened quakes

- List: the 45 rows of runs/2026-10-24-0850/attempts/catalog-auditor/out/screen_summary.csv with class "bathymetry not
  cached after the 503s (not screened)", parameters from data/comcat/m60_d70_2020_2026_m6.0only.csv; re-checked against
  the NCEI events fetched at 19:20Z (no event within +/- 1 day and 1000 km, any validity, any cause).
- Stage 1 and 2 as section 3 (scope 1000 km, ETA in [10, 150]). Survivor = >= 2 sites PASS.
- Network null for a survivor: frozen site list = every site in scope USABLE at the real origin; 400 control origins
  uniform on minutes in [o-40 d, o-2 d] U [o+3 d, o+40 d] (seed 20261024), same codes and ETAs, real window rule only;
  score = (K = number of DETECTING sites, S = second-largest r among them), compared lexicographically. The real score
  must beat every control. Then the live NCEI events and runups re-fetch, then the panel.

## 6. Honesty

- Selection by distance and ETA only, never by looking at series first. One map, scored once; any later change is a
  new timestamped PREREG.vN.md and the report says so.
- Data budget: no single download over 100 MB, at most 2 GB new data in total (logged bytes in data/fetch_log.tsv);
  at most 3 CPU-heavy processes; peak memory under 3 GB.
