# A second uncatalogued signal matching deep-moonquake nest A100 on Apollo S14 and S16, 1973-10-30 02:25 UTC (full criterion)

Target: apollo-moonquake-missed-vs-pds-catalog, full success criterion (deep-moonquake branch: NCC >= 0.5 with the
stack of a catalogued nest on >= 2 stations, moveout within 2 s, phase consistent with the nest's tidal periodicity,
statistic above the bank's null over the full searched span, gap / thermal / glitch checks, not in the PDS tables).

This is an additional object from the same scan as the claimant's earlier full-criterion package
2026-11-13-[credit]-9ff1c507 (the A100-like event of 1973-11-26 07:46:28.6 UTC). It does not replace that claim, and
the two events are not independent confirmations of each other: they share the template, the statistic, the null,
the readings of the criterion and the explanation of the silent S16 MH2 channel. Strength in one line: above all 401
controls of its template (p <= 1/402 per template; max-T family-wise over the scan's 12 templates p <= 1/402,
Bonferroni 0.03); the station pair S14 + S16 was chosen after this event had been a near miss on S12 + S14, and over
all 55 two-station template scans of the claimant's run the plain empirical bound is only 0.14.

## What

In the saved PDS Apollo PSE data (Nunn et al. 2022 restoration), an S14 + S16 signal with onset 1973-10-30 02:25:51.5 UTC (MiniSEED Earth-received time) matches the frozen five-event 1973 S14 + S16 stack of catalogued deep-moonquake nest A100 with best single-channel NCC 0.621 on S14 MH2 and 0.620 on S16 MH1 (S16 MH2 unresponsive at the time; S14 reaches only 0.37 with the separate S12 + S14 A100 stack), an ATT-corrected S16-minus-S14 timing 0.10 s from the nest's median, an anomalistic phase of 161.5 deg inside the nest's 95% interval and about 0.1-0.2 d from the times predicted by the catalogued 1973 A100 monthly sequence, and a coincidence statistic of 0.298 above all 401 time-reversed and >= 1 h-shifted full-1973 controls of that template (best 0.191; p <= 1/402 per template and, by the pre-registered max-T test, family-wise over the scan's 12 templates; Bonferroni 12/402 = 0.03; the choice of the S14 + S16 lens after this event's S12 + S14 near miss is not covered, 55/402 = 0.14 over the parent run's scans), passes the pre-registered gap, thermal and glitch checks, and has no row of the 12 PDS catalogue tables as saved 2026-11-13T16:15Z within +/- 5 min or spanning it (nearest: an A1 deep moonquake 01:00-02:00), with the live re-fetch and the 24-month literature search left to NOVELTY, membership in A100 resting on the bank's tests and the attribution tests (a source without catalogued 1973 events and with A100-like waveform and moveout not excluded), and the event not independent of the earlier claimed 1973-11-26 event (same template, statistic, null and readings).

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (Python 3 standard library; set PYTHON if `python3` is not on PATH). Expected
last line: `PASS`, in under a second. From the saved preprocessed S14 and S16 windows and the saved A100 stack it
recomputes every channel's NCC at each lag within +/- 7 samples, each station's best lag, the two-station statistic
Dt, R7 (best channel >= 0.5 at both stations), the null (Dt above all 401 controls' full-span maxima), R8 (ATT-corrected
S16 - S14 within 2 s of the nest's median), R9 (anomalistic phase in the 95% interval of the 62 catalogued A100 events),
the thermal check, and the saved catalogue distances. The full re-run from the PDS waveforms (stacks, the 12-nest scan
of all of 1973 with 401 controls each, attribution tests, glitch-catalogue gates, multiplicity) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| PDS Apollo seismic event catalogue (levent.1008weber.csv and the 11 other tables of the data directory) | rows near 1973-10-30 02:25:51.5 UTC | nearest row 85.9 min before (levent 73-303 0100 A1, stops 02:00); none within +/- 5 min, no span containing the onset | https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ | 2026-11-13T17:30:46-17:31:42Z (NOVELTY, live) |
| Knapmeyer-Endrun and Hammer (2015), Tables S1-S3 (new Apollo 16 events, 1972-1975) | rows near the onset | nearest 1973-10-26 09:06:07.6 (-89.3 h); none within +/- 5 min | https://doi.org/10.1002/2015JE004862 | supporting information obtained by hand 2026-11-13 |
| Shi, Li and Wang (2025) deep-moonquake catalogues | rows near the onset | nearest is the catalogued A1 event (-85.9 min); none within +/- 5 min | https://doi.org/10.5281/zenodo.16809589 | 2026-11-13 (NOVELTY) |
| Liu, Xiao and Li (2025) acceleration-glitch catalogue, S14 and S16 (Spike, Step-Up, Step-Down; MH1, MH2, MHZ) | intervals overlapping the S14 and S16 windows | none; nearest S14 entry ends 1250 s before the onset, nearest S16 entry starts 5730 s after | https://doi.org/10.5281/zenodo.15715187 | release v1.0.1 (files checked against SHA256SUMS) |

## Not claimed

- No location solution. Membership in A100 rests on the bank's own tests (R7, R8, R9) and on attribution tests that
  could have taken it away and did not (how-we-built-it/results/): only the A100 stack of the 12 is above its own
  null; the lag maxima sit at the claimed lags; the event's own waveform, scanned over 1973, ranks six catalogued A100
  events first to sixth of 998 catalogued deep moonquakes; no catalogued 1973 deep moonquake of another nest reaches
  the A100 null. A source without catalogued 1973 events whose waveform and moveout resemble A100's is not excluded.
  A100 is poorly located (-2 +/- 4.2 N, 32.2 +/- 17.1 E); A35 (5 N, 36.1 E; S16 - S14 S-pick difference 1 s from
  A100's) lies about 1.7 sigma from it, and its 1973 events score at most 0.118 in the reverse search. A244 (moveout
  2 s from A100's) has no 1973 events.
- R7 is met on the best single channel per station (S14 MH2 0.621, S16 MH1 0.620); station means are 0.557 (S14) and
  0.298 (S16). S16 MH2 did not respond to any catalogued event of 1973 days 297-305 (how-we-built-it/results/
  a3_decision_1030.txt and the panel), so S16 rests on MH1 alone; no catalogued 1973 A100 event was recorded in that
  instrument state. R7 at S14 depends on the stack: with the separate S12 + S14 A100 stack S14 reaches only 0.366. On
  the other decimation phase, with the stack rebuilt on that grid, the values are 0.621 / 0.587.
- R8 is a weak discriminator here (each station's lag is confined to +/- 2.1 s around a template carrying the nest's
  80 s moveout), and R9 is wide for this nest (95% interval 272 deg); the closeness of the onset to the times
  predicted by the catalogued 1973 A100 monthly sequence (panel/criterion.md) is descriptive support, not a gate.
- Multiplicity: the per-template null covers taking the second of several A100 peaks, but not the choice among
  templates, station pairs and lenses. Max-T over the 12 templates of the scan gives p <= 1/402 (Bonferroni 0.03);
  over the 26 two-station template scans of 1973 in the claimant's run the plain empirical bound is 0.065, over all 55
  it is 0.14; a fitted tail (GEV, model-based) gives 4.7e-10 per template. The S14 + S16 lens was written after this
  event was the strongest new A100 detection on S12 + S14 (where S12 also sees it, above that lens's null: S12 0.514).
- Times are MiniSEED (Earth-received, nominal-rate) times of the PDS restoration; sub-second accuracy is not claimed.
  The bank asks for FDSN request URLs; EarthScope FDSN was not reachable from the claimant's network, so the package
  gives the PDS file URLs of the same Nunn et al. (2022) restoration (how-we-built-it/waveforms_urls.txt).
- The raw S14 signal is at digitiser level (median absolute deviation 0 DU in the window); the detection rests on
  correlation, with energy at the 91st-95th percentile of random times that day on S14 MH1, S14 MH2 and S16 MH1.

## Credits

- Apollo Passive Seismic Experiment data: NASA Apollo program; restored archive by C. Nunn, Y. Nakamura, S. Kedar and
  M. P. Panning, PSJ 3, 219 (2022), https://iopscience.iop.org/article/10.3847/PSJ/ac87af, PDS Geosciences Node
  (https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/).
- Event catalogue: Y. Nakamura and co-workers (levent), expanded by R. C. Weber with the events of R. C. Bulow,
  C. L. Johnson and P. M. Shearer (2005, JGR 110, E10003, https://doi.org/10.1029/2005JE002414; 2007),
  https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/.
- Nest S-wave picks and locations: Y. Nakamura (2005), in the same PDS catalogue bundle.
- Glitch catalogue checked: Liu, Xiao and Li (2025), JGR Planets 130, e2025JE009277, https://doi.org/10.5281/zenodo.15715187.
- Event lists checked: B. Knapmeyer-Endrun and C. Hammer (2015), JGR Planets 120, https://doi.org/10.1002/2015JE004862
  (supporting-information Tables S1-S3); K. Onodera (SP catalogue, Zenodo 8373651); Shi, Li and Wang (2025, Zenodo
  15420872 and 16809589).
- Prior work by the same claimant: package 2026-11-13-[credit]-9ff1c507 (the 1973-11-26 event, same scan).
