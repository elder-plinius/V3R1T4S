# A new member of deep-moonquake nest A39 on Apollo S14, 1971-09-05 01:26 UTC (p1)

Target: apollo-moonquake-missed-vs-pds-catalog, partial win p1 ("A new member of a catalogued nest seen on a single
station with CC >= 0.6 and the null test passed (single-station detections are weaker evidence).").

## What

On Apollo station S14 alone (long-period MH1/MH2, PDS MiniSEED, frozen phase-0 pipeline), the 450 s window starting 1971-09-05 01:25:44.150 UTC (onset 01:26:14 UTC, about +/- 1.2 s cycle ambiguity) matches the frozen S14 stack of sixteen catalogued 1971 A39 deep-moonquake events with NCC 0.693 on MH2 and 0.595 on MH1 (mean 0.644); this mean exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.221 for A39, 0.246 over all 25 searched nest templates), of 400 phase-randomised A39 templates (0.318) and of a between-channel 1-23 h shift control (0.529 over all 25 templates); no other of the 25 templates exceeds 0.18 there, it passes the pre-registered gap, thermal and glitch checks (including no overlap with the Liu, Xiao and Li 2025 S14 ACC-Spike catalogue), and no row of the 11 PDS Apollo seismic event catalogue tables lies within +/- 5 min of it, so it is a single-station (p1) detection of an A39 member absent from the PDS catalogue, not a multi-station or located event, and not checked here against the literature clause.

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (Python 3 standard library; set PYTHON if `python3` is not on PATH). Expected last
line: `PASS`, in about a second. It recomputes both channels' NCC from the saved window and template and compares the
detection statistic with all 401 null maxima. The full re-run from the PDS waveforms (templates, scan, null, checks) is
in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| PDS Apollo seismic event catalogue (levent.1008weber.csv and 10 other tables) | events near 1971-09-05 01:26 UTC | nearest row 1589 min away; none within +/- 5 min | https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ | 2026-11-13T05:52:08Z |
| Liu, Xiao and Li (2025) S14 acceleration-glitch catalogue (ACC-Spike MH1/MH2) | intervals overlapping the 450 s window | none; nearest spike start 1487 s after the onset | https://doi.org/10.5281/zenodo.15715187 | copies of 2026-11-13T05:29Z |

## Not claimed

- Not the full criterion: one station only (S12 near the same time with the S12 A39 stack: D 0.306, not claimed); no
  location, moveout or inter-station null.
- Membership rests on waveform similarity with the A39 stack (0.69 / 0.60), the other 24 nest templates' scores near
  that time (declustered peaks within +/- 5 min all <= 0.173; the scan stores peaks >= 0.15 only) and the anomalistic
  phase (332 deg, 0.3 deg from the nearest of 65 catalogued A39 members); correlation alone does not prove membership.
- MH1 alone is below 0.6 (0.595); the p1 CC reading is the best single channel (MH2 0.693).
- Times are MiniSEED (Earth-received, nominal-rate) times; sub-second accuracy is not claimed.
- Waveforms come from the NASA PDS restoration (EarthScope FDSN was not reachable from the claimant's network).
- Two other A39 seeds (1971-05-19, 1971-12-11) are not part of this claim.
- levent has no rows at all from 1971-09-03 22:57 to 1971-09-06 19:12 (days 247-248 empty; also in levent.1008c), so
  the absence from the catalogue may partly reflect days the original analysts did not read; S14 and S12 data exist.

## Credits

- Apollo Passive Seismic Experiment data: NASA Apollo program; restored archive by C. Nunn, Y. Nakamura, S. Kedar and
  M. P. Panning, PSJ 3, 219 (2022), https://iopscience.iop.org/article/10.3847/PSJ/ac87af, PDS Geosciences Node
  (https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/).
- Event catalogue: Y. Nakamura and co-workers (levent), expanded by R. C. Weber with the events of J. Bulow,
  C. L. Johnson and P. M. Shearer (2005, 2007), https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/.
- Nest locations: Y. Nakamura (2005). SP event windows checked: K. Onodera (Zenodo 8373651).
- Glitch catalogue checked: Liu, Xiao and Li (2025), JGR Planets 130, e2025JE009277, https://doi.org/10.5281/zenodo.15715187.
