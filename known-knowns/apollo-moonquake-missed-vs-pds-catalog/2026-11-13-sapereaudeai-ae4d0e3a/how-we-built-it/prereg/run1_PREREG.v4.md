# PREREG.v4: lens network-2station, full criterion for A1 in 1971 (frozen 2026-11-12T19:24:35Z)

Written before any S14 1971 file was downloaded (0 in the cache at this time) and before the S12+S14 templates
exist. PREREG.md and PREREG.v2.md stay in force (R6, candidate checks, frozen preprocessing).

## Templates

- Joint A1 templates for S12 MH1/MH2/MHZ and S14 MH1/MH2 (S14 MHZ excluded: it oscillates, seen on dev 1972-017),
  built from the 1972 dev A1 events with the frozen builder (tools/nesttemplates.py; reference 1972-017 04:12, the
  largest A1 + A2; common alignment, so both stations' windows start at the same absolute time and the template
  carries the nest's S12-S14 moveout). Frozen preprocessing of PREREG.v2.

## Statistic

- Dn(t) = mean of the single-channel NCC over valid channels of both stations at the common lag; defined only
  where >= 2 S12 channels and >= 1 S14 channel have >= 90% valid samples.
- Scan: 1971 days 36-365 (S14 starts on day 36), both stations' files from the PDS bundle.

## Null set (bank wording: time-reversed data, and data circularly shifted between stations by >= 1 h)

- C0: all channels time-reversed. C1..C400: S14 channels circularly rolled within each day span by
  3600 + 180 k seconds (k = 0..399; all >= 1 h) relative to S12. The same Dn, the same full span. Candidate Dn must
  exceed every control's full-span maximum (401 controls). null_test.md reports it.

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

## Outcome

- Full criterion met for a candidate only if all of the above pass. Otherwise lens 2 reports the best new
  network detections with their per-station CC, moveout and null margin.
