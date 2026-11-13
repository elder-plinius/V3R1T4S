# Apollo PSE nest A1, 1971: catalogued-event recovery with a measured false-alarm rate (p2)

Target: apollo-moonquake-missed-vs-pds-catalog, partial win p2 ("Recovery of >= 90% of one nest's catalogued events
in one year with a measured false-alarm rate, saved and re-runnable.").

## What

With templates and threshold (theta = 0.10898) fixed on 1972 data alone, the saved three-component S12 long-period template detector re-runs to recover 63 of the 67 nest-A1 deep moonquakes catalogued for 1971 in levent.1008weber.csv (94.0%, detection onset within +/- 5 min of the catalogued start), at a measured false-alarm rate of 1.196 declustered detections per scanned day on the time-reversed 1971 data (400 over 334.54 scanned day-equivalents).

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (Python 3 standard library; set PYTHON if `python3` is not on PATH). Expected
last line: `PASS`. Under a second on a laptop. It checks the object files and recomputes the recovery count and the
false-alarm rate from them. The full re-run from the waveforms (download of the PDS files listed in
how-we-built-it/waveforms_manifest.csv, then about 15-20 s per day of 1971) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| PDS Apollo seismic event catalogue, levent.1008weber.csv | nest A1 (T2 = A, N2 = 1), 1971 | 67 catalogued events; bar 61 | https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/levent.1008weber.csv | 2026-11-12T21:04:14Z |

## Not claimed

- No new moonquake is claimed here: not the full criterion, not p1, not p3.
- The false-alarm rate is the bank's single-station null (time-reversed data); the inter-station shift null does not
  apply to a one-station detector. Another implementation of the same frozen definitions measured 0.90 per day
  (REPRODUCE panel file); the 1.196 per day stated here is the higher of the two.
- Waveforms come from the NASA PDS restoration (EarthScope FDSN was not reachable from the claimant's network), so
  file URLs replace FDSN request URLs.

## Credits

- Apollo Passive Seismic Experiment data: NASA Apollo program; restored archive by C. Nunn, Y. Nakamura, S. Kedar and
  M. P. Panning, "A New Archive of Apollo's Lunar Seismic Data", PSJ 3, 219 (2022),
  https://iopscience.iop.org/article/10.3847/PSJ/ac87af, served by the PDS Geosciences Node
  (https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/).
- Event catalogue: Y. Nakamura and co-workers (levent), expanded by R. C. Weber with the template-matched events of
  J. Bulow, C. L. Johnson and P. M. Shearer (2005, JGR 110, E10003; 2007), PDS bundle
  https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/.
- Deep-moonquake nest locations: Y. Nakamura (2005, JGR 110, E01001).
- Related recent work found by the NOVELTY panel: Shi et al. matched-filter A1 arrivals (Zenodo 10.5281/zenodo.18476476
  and 10.5281/zenodo.22113858), measured at catalogue times without a false-alarm rate.
