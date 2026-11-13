# PREREG (frozen 2026-11-12T18:50:58Z, before any 1971 waveform is read and before any 1972 waveform is decoded)

Target: apollo-moonquake-missed-vs-pds-catalog. Run folder runs/2026-11-12-1842.

null_test: required

## Criterion (bank, verbatim)

Success criterion: A saved event package (UTC time, station/channel list, FDSN request URLs, waveforms, template or
detector code) such that: for a deep moonquake, normalised cross-correlation >= 0.5 with the stack of a catalogued
nest on >= 2 stations with consistent relative arrival times (within 2 s of the nest's moveout) and occurrence phase
consistent with the nest's tidal periodicity; for other types, coherent arrivals on >= 2 stations with a location
solution (RMS <= 3 s); the detection statistic exceeds the maximum obtained on a null set (the same templates
correlated with time-reversed data and with data circularly shifted between stations by >= 1 h) over the full searched
span; data-gap, thermal moonquake (sunrise/sunset) and instrument-glitch checks pass; and no event within +/- 5 min in
levent.1008weber.csv and the other tables of
https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ re-fetched live immediately
before claiming, nor in any published expanded deep-moonquake list of the last 24 months found by search.

- p1: A new member of a catalogued nest seen on a single station with CC >= 0.6 and the null test passed (single-station detections are weaker evidence).
- p2: Recovery of >= 90% of one nest's catalogued events in one year with a measured false-alarm rate, saved and re-runnable.
- p3: Relocation of a catalogued nest with formal errors at least 30% smaller than Nakamura 2005, using added arrival picks.

## Data (fixed)

- Waveforms: NASA PDS Geosciences bundle urn:nasa:pds:apollo_pse (Nunn et al. 2022 restoration), MiniSEED Steim2,
  read with this run's own decoder tools/mseed_steim2.py, validated on xa.s12.00.mhz.1973.001.0 against the PDS
  GeoCSV twin (572,344 samples identical, times within 16 microseconds; validation/). Sample value -1 is treated as
  a gap (missing sample) marker. EarthScope FDSN is unreachable from this network and is not used; where the
  criterion says "FDSN request URLs" the package gives the PDS file URLs.
- Catalogue: levent.1008weber.csv (sha256 f95743b2...b0b9b93c, fetched 2026-11-12T18:42:53Z) and the other tables of
  the PDS event catalogue data directory.

## Selection rule (applied by tools/select_rule.py from the catalogue and PDS inventory only; output in selection/)

- Nest: the nest with the most catalogued events (T2 = 'A'): A1 (N2 = 1, 443 events).
- Station and channels: S12, long-period MH1, MH2, MHZ, location 00 (peaked mode). S12 is the only station
  recording A1 in every year 1970-1977 and A1 is most often seen on S12 LP in the catalogue.
- Scored year: the calendar year with the most A1 events among years where S12 has all three LP components in peaked
  mode on every day: 1971 (67 events; 1970: 58, 1973: 57, 1972: 54).
- Development year: 1972 (only the S12 LP days containing 1972 A1 catalogued events, 52 days). Templates, band,
  window and threshold are chosen on 1972 only. No 1971 waveform is read before the detector freeze below.

## Readings chosen before any result (most favourable fair readings, stated)

- R1 (p2 "recovery"): a catalogued 1971 A1 event (Y=71, T2='A', N2=1) is recovered if a declustered detection
  (statistic >= theta) has its onset time within +/- 5 min of the catalogued signal start (column S, HHMM, minute
  resolution). +/- 5 min is the bank's own identity window for "an event in the catalogue".
- R2 (p2 denominator): primary = catalogued 1971 A1 events for which the detector is defined (scanned) at some lag
  inside that +/- 5 min window (events that fall in S12 data gaps cannot be recovered from S12 data). Secondary,
  also reported: all 67.
- R3 (p2 "measured false-alarm rate"): the rate (per day of scanned data) of declustered detections >= theta on the
  bank's null for one station, the same templates correlated with the time-reversed data over the full 1971 span.
  Also reported: the chance-coincidence recovery of randomly shifted catalogue times.
- R4 (p1 "CC >= 0.6 on a single station"): the normalised cross-correlation of the nest stack with the data on at
  least one S12 LP component at the detection's lag (single-channel NCC, the usual meaning of CC). The 3-component
  mean is also reported.
- R5 (p1 "the null test passed"): the candidate's detection statistic exceeds the maximum of the same statistic
  over the full searched span (all of 1971) in every control of the null set below.
- R6 ("no event within +/- 5 min"): a candidate is not new if any row of any table of the PDS catalogue data
  directory has a time within +/- 5 min of the candidate onset, or if the onset lies between a levent row's signal
  start and its stop time (column E; 9999 = continues to the next event).

## Detector (fixed design; free parameters chosen on 1972 only, then frozen in PREREG.v2.md before 1971 is read)

- Daily arrays at 6.625 Hz on a uniform grid from record start times; -1 samples and missing records are gaps.
  Demean, gap samples set to zero after filtering and flagged invalid.
- Band-pass (zero-phase Butterworth) and decimation by 2 to 3.3125 Hz. Band chosen on 1972 from
  {0.25-1.0, 0.3-1.2, 0.4-1.5} Hz.
- Templates: per component, the stack of 1972 A1 events aligned by iterative cross-correlation (start: the 1972
  event with the largest catalogue amplitude; align within +/- 3 min of the catalogued start; stack events whose
  3-component CC with the current stack is >= 0.3; 3 iterations). Window length chosen on 1972 from {300, 450, 600} s
  starting 30 s before the stack's P onset.
- Statistic D(t) = mean over available components of the single-channel normalised cross-correlation at common lag
  t. D is defined only where >= 2 of 3 components have >= 90% valid samples in the window.
- Detections: local maxima of D, declustered (largest within +/- 5 min kept). Onset = window start + 30 s.
- Threshold rule (fixed now): theta = the smallest value such that the declustered detections of the same detector on
  time-reversed 1972 dev data occur at <= 1 per day of scanned dev data. Recorded in PREREG.v2.md.

## Null design (fixed now)

- C0 (bank-literal for one station): the frozen templates correlated with the time-reversed data of every scanned
  1971 day (each day's arrays reversed in time), full span.
- C1..C400: 400 phase-randomised templates (for each control, one set of uniformly random Fourier phases, seed
  20261112 + k, applied to all three components' template spectra so the inter-component phase relations are kept;
  amplitude spectra unchanged), correlated with the forward 1971 data, full span, same statistic.
- p1/claim null: real candidate D must exceed the full-span maximum of D in every control C0..C400 (401 controls).
  null_test.md reports controls, best_control, real, real_beats_all_controls, command.
- p2 false-alarm rate: from C0 at theta (R3).

## Candidate checks (fixed now)

- Gap: >= 99% valid samples on every used component in [onset - 10 min, onset + window + 10 min]; no record timing
  discontinuity (inter-record gap or overlap larger than one sample interval) in that span.
- Glitch: no sample in the demeaned raw window exceeds 8 times the window's median absolute deviation on any used
  component unless D stays above theta with that component excluded; CC computed separately on the first and second
  halves of the template must both be positive.
- Thermal: local solar elevation at S12 from a low-precision ephemeris (subsolar selenographic longitude 180 deg minus
  the Moon's mean elongation D of Meeus); a candidate within +/- 12 deg of the terminator (about +/- 1 Earth day of
  sunrise or sunset) is flagged and not claimed.
- Novelty: R6 against all PDS catalogue tables re-fetched live immediately before claiming, plus a literature search
  (last 24 months) for expanded deep-moonquake lists.

## Thresholds and outcomes

- p2 is met if the R2-primary recovery at the frozen theta is >= 0.90 on 1971, with the C0 false-alarm rate reported.
- p1 candidate: R4 and R5 and every candidate check pass.
- Full criterion: needs a second station; any multi-station test is pre-registered in a new timestamped file before
  its data are scored.

## Escape hatches (declared now)

- E1: if more than 20% of 1971 S12 days are missing or unreadable, the scored year becomes the next eligible year by
  count (1970, then 1973); 1972 stays dev.
- E2: if fewer than 10 dev events enter the stack, the dev set is widened to 1973 A1 event days by the same rule.
- E3: if the 1971 recovery is below 0.90, the result is reported as is with its full recall/false-alarm curve; no
  1971-based re-tuning. A different design is a new prereg on a different scored year.
