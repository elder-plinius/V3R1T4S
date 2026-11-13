# An uncatalogued signal matching deep-moonquake nest A100 on Apollo S14 and S16, 1973-11-26 07:46 UTC (full criterion)

Target: apollo-moonquake-missed-vs-pds-catalog, full success criterion (deep-moonquake branch: NCC >= 0.5 with the
stack of a catalogued nest on >= 2 stations, moveout within 2 s, phase consistent with the nest's tidal periodicity,
statistic above the bank's null over the full searched span, gap / thermal / glitch checks, not in the PDS tables).

## What

In the saved PDS Apollo PSE data, a signal at 1973-11-26 07:46:28.6 (MiniSEED Earth-received time) on S14 and S16 matches the frozen 1973 stack of catalogued deep-moonquake nest A100 with best single-channel NCC 0.562 (S14 MH2) and 0.699 (S16 MH1), an ATT-corrected S16-minus-S14 timing 0.11 s from the nest's median, an anomalistic phase inside the nest's 95% interval, and a coincidence statistic of 0.343 above all 401 reversed and shifted controls over 1973 (maximum 0.191); it passes the pre-registered gap, thermal and glitch checks, and no row of the PDS catalogue tables as saved at 2026-11-13T04:29Z lies within 70 min, with the live re-fetch and the 24-month literature search left to NOVELTY.

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (Python 3 standard library; set PYTHON if `python3` is not on PATH). Expected
last line: `PASS`, in under a second. From the saved preprocessed S14 and S16 windows and the saved A100 stack it
recomputes every channel's NCC at each lag within +/- 7 samples, each station's best lag, the two-station statistic
Dt, R7 (best channel >= 0.5 at both stations), the null (Dt above all 401 controls' full-span maxima), R8 (ATT-corrected
S16 - S14 within 2 s of the nest's median), R9 (anomalistic phase in the 95% interval of the 62 catalogued A100 events),
the thermal check, and the saved catalogue distances. The full re-run from the PDS waveforms (stacks, scan over all of
1973 with 401 controls, attribution tests, glitch-catalogue gates) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| PDS Apollo seismic event catalogue (levent.1008weber.csv and the 11 other tables of the data directory) | rows near 1973-11-26 07:46:28.6 UTC | nearest row 70.5 min before (levent 73-330 0636 A203, stops 07:05); none within +/- 5 min, no span containing the onset | https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ | 2026-11-13T09:40:32-09:41:22Z (NOVELTY, live) |
| Knapmeyer-Endrun and Hammer (2015), Tables S1-S3 (new Apollo 16 events, 1972-1975) | rows near the onset | nearest 1973-11-28 14:40:37.5 (+54.9 h); none within +/- 5 min | https://doi.org/10.1002/2015JE004862 | supporting information obtained by hand 2026-11-13 |
| Liu, Xiao and Li (2025) acceleration-glitch catalogue, S14 and S16 (Spike, Step-Up, Step-Down; MH1, MH2, MHZ) | intervals overlapping the S14 and S16 windows | none; nearest S16 entry +774 s, nearest S14 entry +1090 s after the onset | https://doi.org/10.5281/zenodo.15715187 | release v1.0.1, record read 2026-11-13T09:12:31Z |

## Not claimed

- Times are MiniSEED (Earth-received, nominal-rate) times of the PDS restoration; sub-second accuracy is not claimed.
  The bank asks for FDSN request URLs; EarthScope FDSN was not reachable from the claimant's network, so the package
  gives the PDS file URLs of the same Nunn et al. (2022) restoration (how-we-built-it/waveforms_urls.txt).
- R7 is met on the best single channel per station (S14 MH2 0.562, S16 MH1 0.699). Station means are 0.494 (S14) and
  0.343 (S16): S16 MH2 did not respond to any catalogued deep moonquake on 1973-11-25 to 11-27 (A3 test,
  how-we-built-it/results/a3_decision.txt), so S16 rests on MH1. S14 MH2 is 0.468 on the other decimation phase of the
  frozen pipeline and about 0.566 at near-continuous lag.
- The pre-registered phase test (R9) is weak for this nest (95% interval 272 deg wide); the monthly 1973 A100 sequence
  (27.15, 27.22, 27.34 d spacings around the event) is descriptive support, not a gate.
- No location solution is claimed. Membership in A100 rests on the bank's tests plus the attribution tests in
  how-we-built-it/results/ (all 12 stacked nests, Nakamura 2005 moveouts, reverse search over 998 catalogued 1973 deep
  moonquakes); a source without catalogued 1973 events, with an A100-like waveform and moveout, is not excluded.
- A second A100-like event (1973-10-30 02:25:51.5 UTC) also meets R7, R8 and R9 and is not part of this claim; a third
  (1973-01-30 23:06) lies in an Onodera SP window and is not claimed.
- Independent re-implementations by the REPRODUCE panelist give slightly different values (S14 MH2 0.576, R8 nest median
  0.62-0.68 s, null maxima 0.172-0.179) because the frozen code widens data gaps by 20 s and reads "running MAD" one
  of two ways; no check changes (panel/reproduce.md).
- Twelve nests were stacked and scanned, each with its own null; S12 sees the event above a separate S12 + S14 null
  (how-we-built-it/results/s12_third_station.txt), not used for the claim.

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
  (supporting-information Tables S1-S3); K. Onodera (SP catalogue, Zenodo 8373651).
