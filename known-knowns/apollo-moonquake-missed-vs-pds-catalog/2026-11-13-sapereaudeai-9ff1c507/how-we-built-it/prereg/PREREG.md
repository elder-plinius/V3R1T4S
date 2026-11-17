# PREREG (frozen 2026-11-13T03:40:56Z in run 2026-11-12-1842 as PREREG.v15.md; copied here verbatim below with the rules it inherits)

null_test: required

Copied on 2026-11-13T04:31:07Z into this continuation run folder; the sources in 2026-11-12-1842 are unchanged.

---

# PREREG.v15: lens lagtol-s14s16-1973, full criterion for 25 nests on S14 + S16 in 1973 (frozen 2026-11-13T03:40:56Z)

S14 and S16 data of 1973 were scanned before only for nest A1 (lens s14-s16-coinc-1973) and S14 for A1 (lens
s14-single-1973); for the nests below no S14 + S16 analysis exists. The S12 + S14 lag-tolerant scan of these nests in
1973 (PREREG.v14) found 18 uncatalogued two-station detections above their nulls, none with CC >= 0.5 at both
stations; S16 is a different station pair, not a re-test of those.

## Scope

- Nests: the 25 lens-8 nests (A18, A10, A9, A6, A218, A14, A204, A39, A23, A36, A7, A26, A16, A20, A201, A100, A210,
  A29, A25, A216, A86, A38, A257, A22, A319); not A1.
- Stations S14 MH1/MH2 + S16 MH1/MH2 (location 00), all 365 days of 1973.
- Joint templates per nest from its own 1973 catalogued events, glitch-screened builder (tools/nesttemplates2.py),
  clean reference (largest positive A1 + A2 + A4 among events whose four reference-window channels pass the screen);
  drop rule: fewer than 3 members or a template channel max|t|/rms > 8.

## Statistic, null, criterion (as PREREG.v14, stations S14 and S16)

- D14, D16 = mean single-channel NCC over each station's valid channels (>= 1 each); Dt(t) = min(max over |d| <= 7
  samples (2.11 s at 3.3125 Hz; the PREREG.v14 implementation uses the same 7 samples) of D14(t + d), the same for
  D16). Declustered peaks (+/- 5 min).
- C0 time-reversed; C1..C400 S16 rolled by 3600 + 180 k s. Candidate Dt above every control's full-span maximum.
- R7: best single-channel NCC >= 0.5 at S14 and at S16, each at its own best lag within 7 samples of the common lag.
  R8: ATT-corrected S16-minus-S14 arrival difference within 2 s of the nest's median over its catalogued 1973 events
  above the null (else Dt >= 0.2). R9: anomalistic phase inside the nest's 95% interval. Gap, glitch and thermal
  checks at both stations; R6 live; Onodera; literature.
- Time box: if the scan has not finished by 05:15Z, the lens is reported as incomplete.

---

## Inherited: 2026-11-12-1842/PREREG.v14.md (frozen 2026-11-13T01:18:14Z), verbatim

# PREREG.v14: lens lagtol-25nests-1973, full criterion for 25 nests on S12 + S14 in 1973 (frozen 2026-11-13T01:18:14Z)

Written when 3 of the 1,098 S12 1973 files had been downloaded and none read. S14 1973 data were scanned before
only for nest A1 (lenses s14-single-1973 and s14-s16-coinc-1973); A1 is therefore excluded here.

Design lesson carried over from 1971 (lens coinc-25nests-1971, which stays as reported): after whitening, the
template-data NCC oscillates with lag at about 0.8 Hz, so a common-lag coincidence statistic loses events whose
S12-S14 timing differs from the template's by a fraction of a cycle (example: the A38 event of 1971-05-13 18:39,
S12 part 0.485 and S14 part 0.742 one sample apart, common-lag minimum 0.110). The bank already allows 2 s for the
relative arrival times, so the statistic below lets each station take its best lag within +/- 2 s.

## Scope

- Nests: the 25 lens-8 nests (A18, A10, A9, A6, A218, A14, A204, A39, A23, A36, A7, A26, A16, A20, A201, A100, A210,
  A29, A25, A216, A86, A38, A257, A22, A319); not A1.
- Stations S12 MH1/MH2/MHZ + S14 MH1/MH2 (location 00), all 365 days of 1973.
- Joint templates per nest from its own 1973 catalogued events, glitch-screened builder (tools/nesttemplates2.py,
  PREREG.v11), clean reference; drop rule: fewer than 3 members or a template channel with max|t|/rms > 8.

## Statistic

- D12(t) = mean single-channel NCC over valid S12 channels (>= 2), D14(t) = over valid S14 channels (>= 1), with the
  joint template's windows at common lag t. Dt(t) = min( max over |d| <= 2 s of D12(t + d), max over |d| <= 2 s of
  D14(t + d) ). Declustered peaks (+/- 5 min).

## Null (bank wording)

- C0: all channels time-reversed; C1..C400: S14 channels circularly rolled within each day span by 3600 + 180 k s.
  Same Dt, full span (365 days). A candidate's Dt must exceed every control's full-span maximum of its own nest.

## Full criterion for a candidate (all required)

- R7: at each station's own best lag within +/- 2 s of the common lag, the best single-channel NCC is >= 0.5 at S12
  and >= 0.5 at S14.
- R8: the two station lags converted to Earth-received time with each station's ATT trace; S14-minus-S12 difference
  within 2 s of the median of the same quantity over the nest's catalogued 1973 events whose Dt exceeds the null
  maximum (else those with Dt >= 0.2).
- R9: anomalistic phase inside the nest's 95% interval (all its catalogued events).
- Gap, glitch (PREREG.md rule with the null maximum) and thermal checks at both stations; R6 against every PDS table
  re-fetched live; Onodera windows; literature search of the last 24 months.
- p1 through this lens is not claimed (p1 is carried by run 2026-11-12-2317).
- Time box: if the scan has not finished by 05:20Z on 2026-11-13, the lens is reported as incomplete.

## Inherited: 2026-11-12-1842/PREREG.v5.md (R8 with ATT timing, frozen 2026-11-12T19:27:29Z), verbatim

# PREREG.v5: amendment to PREREG.v4 R8 (frozen 2026-11-12T19:27:29Z, no S14 1971 file downloaded yet)

Reason, from the PDS description document (apollo_pse_description.pdf, section 3.3.1, fetched 19:26:00Z): MiniSEED
sample times use the nominal sampling interval from the day's first timestamp and can diverge from the original
Earth-received timestamps (timing trace ATT) by a few seconds over 24 hours, independently per station. A +/- 2 s
moveout test on nominal times could therefore pass or fail for timing reasons alone.

R8 (replaces the PREREG.v4 wording): for a candidate, each station's arrival is the time of its best station-mean
NCC within +/- 10 s of the common lag, converted to Earth-received time with that station's ATT trace (the ATT
value of the nearest sample; ATT files fetched only for candidate days). The nest moveout is the median of the same
ATT-corrected S14-minus-S12 difference over the 1971 catalogued A1 events whose network detection exceeds the same
null maximum (if fewer than 5 such events, all 1971 catalogued A1 events with Dn >= 0.2). R8 passes if the
candidate's ATT-corrected difference is within 2 s of that median.

Also clarified: -1 marks missing samples on MH1/MH2/MHZ/SHZ (description section 3.3.2), as already assumed.

## Inherited from 2026-11-12-1842/PREREG.md (frozen 2026-11-12T18:50:58Z): R6 and the candidate checks, verbatim

- R6 ("no event within +/- 5 min"): a candidate is not new if any row of any table of the PDS catalogue data
  directory has a time within +/- 5 min of the candidate onset, or if the onset lies between a levent row's signal
  start and its stop time (column E; 9999 = continues to the next event).

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

## Inherited from 2026-11-12-1842/PREREG.v4.md (frozen 2026-11-12T19:24:35Z): R7 and R9 readings, verbatim

## Readings (most favourable fair, fixed now)

- R7 ("normalised cross-correlation >= 0.5 with the stack of a catalogued nest on >= 2 stations"): at the
  detection's common lag, the best single-channel NCC at S12 >= 0.5 and the best single-channel NCC at S14 >= 0.5
  (the same per-channel reading as R4). Station means are also reported.
- R8 ("consistent relative arrival times, within 2 s of the nest's moveout"): each station's lag re-optimised
  separately (station mean NCC) within +/- 10 s of the common lag; |lag(S14) - lag(S12)| <= 2 s, since the template
  carries the nest moveout.
- R9 ("occurrence phase consistent with the nest's tidal periodicity"): the anomalistic phase (Moon's mean anomaly
  M') of the onset lies in the shortest circular interval holding 95% of all 443 catalogued A1 events,
  [228.3, 101.9] deg (attempts/network-2station/out/a1_anomalistic_phase.txt).
- Gap, glitch and thermal checks of PREREG.md on both stations (thermal: solar elevation at each station).
- R6 against every PDS table re-fetched live before any claim; literature search for expanded lists.

